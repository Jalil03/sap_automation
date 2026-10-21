import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.provisioning.s4615_zf01_accounting_block_gui import (
    APPROVAL_PATH, OPERATION, TARGET, VALUES, FIELD_ID, SAVE_ID, KEY_ID,
    save_once, verify_readback,
)
from src.sap_gui_bridge.errors import ActionBlockedError


OTHER_ID = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVFK-OTHER"


def _fixture():
    session = Mock()
    controls = {
        FIELD_ID: Mock(Id=FIELD_ID, Type="GuiCheckBox", Text="Blocage comptabil.", Selected=False),
        SAVE_ID: Mock(Id=SAVE_ID, Type="GuiButton", Text="Sauvegarder"),
        OTHER_ID: Mock(Id=OTHER_ID, Type="GuiCTextField", Text="unchanged"),
    }
    session.find.side_effect = controls.__getitem__
    snapshot = {
        "transaction": "VOFA", "program": "SAPL081F", "screen_number": "101", "popups": [],
        "input_fields": [
            {"id": KEY_ID, "type": "GuiTextField", "text": "ZF01"},
            {"id": FIELD_ID, "type": "GuiCheckBox", "text": "Blocage comptabil.", "changeable": True},
            {"id": OTHER_ID, "type": "GuiCTextField", "text": "unchanged"},
        ],
        "buttons": [{"id": SAVE_ID, "type": "GuiButton", "text": "Sauvegarder"}],
    }
    return session, controls, snapshot


class Zf01AccountingBlockTests(unittest.TestCase):
    def test_scoped_approval(self):
        policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
        policy.authorize(OPERATION, TARGET, VALUES)
        with self.assertRaises(ValueError):
            policy.authorize(OPERATION, TARGET, {**VALUES, "transport": "OTHER"})

    def test_exact_checkbox_and_one_save_with_checkpoint(self):
        session, controls, snapshot = _fixture()
        with tempfile.TemporaryDirectory() as folder, patch(
            "src.provisioning.s4615_zf01_accounting_block_gui._checkpoint",
            side_effect=lambda: ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION),
        ), patch("src.provisioning.s4615_zf01_accounting_block_gui.inspect_screen", return_value=snapshot):
            result = save_once(session)
            self.assertTrue(result["save_attempted"])
            self.assertEqual("AMBIGUOUS", ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION).status(OPERATION))
            with self.assertRaises(ActionBlockedError):
                save_once(session)
        self.assertTrue(controls[FIELD_ID].Selected)
        controls[SAVE_ID].press.assert_called_once_with()

    def test_unrelated_field_change_blocks_save(self):
        session, controls, snapshot = _fixture()
        altered = {**snapshot, "input_fields": [dict(x) for x in snapshot["input_fields"]]}
        altered["input_fields"][2]["text"] = "changed"
        with tempfile.TemporaryDirectory() as folder, patch(
            "src.provisioning.s4615_zf01_accounting_block_gui._checkpoint",
            side_effect=lambda: ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION),
        ), patch("src.provisioning.s4615_zf01_accounting_block_gui.inspect_screen", side_effect=[snapshot, altered]):
            with self.assertRaises(ActionBlockedError):
                save_once(session)
        controls[SAVE_ID].press.assert_not_called()

    def test_wrong_billing_type_blocks_save(self):
        session, controls, snapshot = _fixture()
        snapshot["input_fields"][0]["text"] = "F2"
        with patch("src.provisioning.s4615_zf01_accounting_block_gui.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                save_once(session)
        controls[SAVE_ID].press.assert_not_called()

    def test_readback_requires_true(self):
        session, controls, snapshot = _fixture()
        with tempfile.TemporaryDirectory() as folder, patch(
            "src.provisioning.s4615_zf01_accounting_block_gui._checkpoint",
            side_effect=lambda: ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION),
        ), patch("src.provisioning.s4615_zf01_accounting_block_gui.inspect_screen", return_value=snapshot):
            checkpoint = ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION)
            checkpoint.record(OPERATION, "AMBIGUOUS")
            with self.assertRaises(ActionBlockedError):
                verify_readback(session)
            controls[FIELD_ID].Selected = True
            self.assertTrue(verify_readback(session)["RFBFK"])
            self.assertEqual("VERIFIED", ExecutionCheckpoint(Path(folder) / "checkpoint.json", OPERATION).status(OPERATION))


if __name__ == "__main__":
    unittest.main()
