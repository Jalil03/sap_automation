import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.provisioning.s4615_vtflc_gui import (
    APPROVAL_PATH, APPROVED_VALUES, HEADER, ITEM, OPERATION, ROOT, TARGET,
    prepare_header, prepare_item, save_once, confirm_transport, verify_item,
)
from src.sap_gui_bridge.errors import ActionBlockedError


def _session(kind):
    session = Mock()
    controls = {}
    suffix = "K" if kind == "header" else "P"
    for name in (HEADER if kind == "header" else ITEM):
        cid = f"{ROOT}/usr/ctxtV_TVCPFL{suffix}-{name}"
        controls[cid] = Mock(Id=cid, Type="GuiCTextField", Text="")
    if kind == "item":
        for name, value in (("FKARN", "ZF01"), ("LFARV", "LF")):
            cid = f"{ROOT}/usr/ctxtV_TVCPFLP-{name}"
            controls[cid] = Mock(Id=cid, Type="GuiCTextField", Text=value)
    cid = f"{ROOT}/usr/chkV_TVCPFL{suffix}-{'POSVO' if kind == 'header' else 'KVPRS'}"
    controls[cid] = Mock(Id=cid, Type="GuiCheckBox", Selected=False)
    save_id = f"{ROOT}/tbar[0]/btn[11]"
    controls[save_id] = Mock(Id=save_id, Type="GuiButton", Text="Sauvegarder")
    session.find.side_effect = controls.__getitem__
    return session, controls


class VtflcContractTests(unittest.TestCase):
    def test_scoped_approval_fingerprint(self):
        policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
        policy.authorize(OPERATION, TARGET, APPROVED_VALUES)
        with self.assertRaises(ValueError):
            policy.authorize(OPERATION, TARGET, {**APPROVED_VALUES, "transport": "OTHER"})

    def test_prepare_header_sets_only_approved_fields(self):
        session, controls = _session("header")
        snapshot = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "111", "popups": []}
        with patch("src.provisioning.s4615_vtflc_gui.inspect_screen", return_value=snapshot), patch(
            "src.provisioning.s4615_vtflc_gui._checkpoint"
        ) as checkpoint:
            checkpoint.return_value.status.return_value = None
            result = prepare_header(session)
        self.assertFalse(result["saved"])
        for name, value in HEADER.items():
            self.assertEqual(controls[f"{ROOT}/usr/ctxtV_TVCPFLK-{name}"].Text, value)
        self.assertTrue(controls[f"{ROOT}/usr/chkV_TVCPFLK-POSVO"].Selected)
        controls[f"{ROOT}/tbar[0]/btn[11]"].press.assert_not_called()

    def test_prepare_item_preserves_kvprs_and_blank_pfk(self):
        session, controls = _session("item")
        snapshot = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "113", "popups": []}
        with patch("src.provisioning.s4615_vtflc_gui.inspect_screen", return_value=snapshot), patch(
            "src.provisioning.s4615_vtflc_gui._checkpoint"
        ) as checkpoint:
            checkpoint.return_value.status.side_effect = lambda key: "VERIFIED" if key == "HEADER" else None
            result = prepare_item(session)
        self.assertTrue(result["kvprs_unchanged"])
        for name, value in ITEM.items():
            self.assertEqual(controls[f"{ROOT}/usr/ctxtV_TVCPFLP-{name}"].Text, value)
        self.assertFalse(controls[f"{ROOT}/usr/chkV_TVCPFLP-KVPRS"].Selected)
        controls[f"{ROOT}/tbar[0]/btn[11]"].press.assert_not_called()

    def test_save_is_checkpointed_and_never_marked_verified_early(self):
        session, controls = _session("header")
        for name, value in HEADER.items():
            controls[f"{ROOT}/usr/ctxtV_TVCPFLK-{name}"].Text = value
        controls[f"{ROOT}/usr/chkV_TVCPFLK-POSVO"].Selected = True
        snapshot = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "111", "popups": []}
        with tempfile.TemporaryDirectory() as directory, patch(
            "src.provisioning.s4615_vtflc_gui._checkpoint",
            side_effect=lambda: ExecutionCheckpoint(Path(directory) / "checkpoint.json", OPERATION),
        ), patch("src.provisioning.s4615_vtflc_gui.inspect_screen", return_value=snapshot):
            result = save_once(session, "header")
            self.assertFalse(result["verified"])
            self.assertEqual("AMBIGUOUS", ExecutionCheckpoint(Path(directory) / "checkpoint.json", OPERATION).status("HEADER"))
            with self.assertRaises(ActionBlockedError):
                save_once(session, "header")
        controls[f"{ROOT}/tbar[0]/btn[11]"].press.assert_called_once_with()

    def test_unapproved_or_wrong_context_never_saves(self):
        session, controls = _session("header")
        with patch("src.provisioning.s4615_vtflc_gui.inspect_screen", return_value={
            "transaction": "VOFA", "program": "SAPL081F", "screen_number": "101", "popups": []
        }), patch("src.provisioning.s4615_vtflc_gui._checkpoint") as checkpoint:
            checkpoint.return_value.status.return_value = None
            with self.assertRaises(ActionBlockedError):
                save_once(session, "header")
        controls[f"{ROOT}/tbar[0]/btn[11]"].press.assert_not_called()

    def test_transport_requires_exact_object_request_and_description(self):
        session = Mock()
        prefix = "/app/con[0]/ses[0]/wnd[1]"
        button_id = prefix + "/tbar[0]/btn[0]"
        button = Mock(Id=button_id, Type="GuiButton", Tooltip="Suite   (EntrÃ©e)")
        session.find.return_value = button
        popup = {"id": prefix, "window_title": "Demande : ordre du Customizing",
                 "input_fields": [
                     {"id": prefix + "/usr/txtKO008-OBJ_NAME", "text": "V_TVCPFL"},
                     {"id": prefix + "/usr/ctxtKO008-TRKORR", "text": "A4HK908422"},
                     {"id": prefix + "/usr/txtKO008-AS4TEXT", "text": "S4615 Training Setup"}],
                 "buttons": [{"id": button_id, "type": "GuiButton", "tooltip": "Suite   (EntrÃ©e)"}]}
        snapshot = {"transaction": "VTFLC", "program": "SAPLSTRD", "screen_number": "300",
                    "popups": [popup]}
        with patch("src.provisioning.s4615_vtflc_gui._checkpoint") as checkpoint, patch(
            "src.provisioning.s4615_vtflc_gui.inspect_screen", return_value=snapshot
        ):
            checkpoint.return_value.status.return_value = "AMBIGUOUS"
            confirm_transport(session, "header")
            button.press.assert_called_once_with()
            popup["input_fields"][1]["text"] = "OTHER"
            with self.assertRaises(ActionBlockedError):
                confirm_transport(session, "header")
            button.press.assert_called_once_with()

    def test_item_readback_requires_prior_attempt_and_exact_values(self):
        session, controls = _session("item")
        for name, value in ITEM.items():
            controls[f"{ROOT}/usr/ctxtV_TVCPFLP-{name}"].Text = "003" if name == "GRURP" else value
        snapshot = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "113", "popups": []}
        with patch("src.provisioning.s4615_vtflc_gui.inspect_screen", return_value=snapshot), patch(
            "src.provisioning.s4615_vtflc_gui._checkpoint"
        ) as checkpoint:
            checkpoint.return_value.status.side_effect = lambda key: "VERIFIED" if key == "HEADER" else "AMBIGUOUS"
            result = verify_item(session)
            self.assertEqual("CREATED_AND_VERIFIED", result["result"])
            self.assertEqual("003", result["item"]["GRURP"])
            checkpoint.return_value.record.assert_called_once()
            controls[f"{ROOT}/usr/ctxtV_TVCPFLP-KNPRS"].Text = "G"
            with self.assertRaises(ActionBlockedError):
                verify_item(session)


if __name__ == "__main__":
    unittest.main()
