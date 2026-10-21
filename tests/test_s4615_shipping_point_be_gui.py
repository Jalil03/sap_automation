import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.provisioning.s4615_shipping_point_be_gui import (
    ADDRESS_ID, OPERATION, TARGET, VALUES, confirm_address, confirm_transport,
    provision_once, verify_readback, _open_new_entries, NEW_ENTRIES_MENU_ID,
)
from src.sap_gui_bridge.errors import ActionBlockedError


class ShippingPointBeTests(unittest.TestCase):
    def test_separate_approval_fingerprint(self):
        import json
        from src.provisioning.s4615_shipping_point_be_gui import APPROVAL_PATH
        policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
        policy.authorize(OPERATION, TARGET, VALUES)
        with self.assertRaises(ValueError):
            policy.authorize(OPERATION, TARGET, {**VALUES, "address_country": "DE"})

    def test_old_rejected_checkpoint_not_reused(self):
        from src.provisioning.s4615_shipping_point_be_gui import CHECKPOINT_PATH
        self.assertNotEqual(CHECKPOINT_PATH.name, "shipping_point_1010_checkpoint.json")

    def test_existing_or_unknown_blocks_before_save(self):
        session = Mock()
        for state in ("EXISTS", "UNKNOWN"):
            with patch("src.provisioning.s4615_shipping_point_be_gui.inspect_screen", return_value={}), patch(
                "src.provisioning.s4615_shipping_point_be_gui.lookup_from_snapshot", return_value={"state": state}
            ), patch("src.provisioning.s4615_shipping_point_be_gui._checkpoint") as checkpoint:
                checkpoint.return_value.status.return_value = None
                with self.assertRaises(ActionBlockedError):
                    provision_once(session, TARGET, VALUES)
                checkpoint.return_value.before_write.assert_not_called()

    def test_exact_live_menu_opens_new_entries_when_toolbar_button_hidden(self):
        session = Mock()
        menu = Mock(Id=NEW_ENTRIES_MENU_ID, Type="GuiMenu", Text="Nouvelles entrées")
        session.find.return_value = menu
        overview = {"buttons": [{"id": NEW_ENTRIES_MENU_ID, "type": "GuiMenu", "text": "Nouvelles entrées"}]}
        form = {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "510", "popups": []}
        with patch("src.provisioning.s4615_shipping_point_be_gui.inspect_screen", return_value=form):
            self.assertEqual(form, _open_new_entries(session, overview))
        menu.select.assert_called_once_with()

    def test_only_be_address_is_entered_and_exact_button_pressed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            ExecutionCheckpoint(path, OPERATION).record(OPERATION, "AMBIGUOUS")
            popup = {
                "id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Traiter l'adresse:  1010",
                "input_fields": [{"id": ADDRESS_ID, "text": "", "type": "GuiCTextField", "changeable": True}],
                "buttons": [{"id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]", "type": "GuiButton", "tooltip": "Reprendre   (Entrée)"}],
            }
            before = {"transaction": "OVXD", "program": "SAPLSZA1", "screen_number": "201", "popups": [popup]}
            staged_popup = {**popup, "input_fields": [{**popup["input_fields"][0], "text": "BE"}]}
            staged = {**before, "popups": [staged_popup]}
            field = Mock(Id=ADDRESS_ID, Type="GuiCTextField", Text="")
            button = Mock(Id="/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]", Type="GuiButton", Tooltip="Reprendre   (Entrée)")
            session = Mock()
            session.find.side_effect = lambda cid: field if cid == ADDRESS_ID else button
            with patch("src.provisioning.s4615_shipping_point_be_gui._checkpoint", return_value=ExecutionCheckpoint(path, OPERATION)), patch(
                "src.provisioning.s4615_shipping_point_be_gui.inspect_screen", side_effect=[before, staged, staged]
            ):
                confirm_address(session)
            self.assertEqual("BE", field.Text)
            button.press.assert_called_once_with()

    def test_unapproved_transport_blocks_without_press(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            ExecutionCheckpoint(path, OPERATION).record(OPERATION, "AMBIGUOUS")
            popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Demande : ordre du Customizing",
                     "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR", "text": "OTHER"}]}
            snapshot = {"transaction": "OVXD", "program": "SAPLSTRD", "screen_number": "300", "popups": [popup]}
            session = Mock()
            with patch("src.provisioning.s4615_shipping_point_be_gui._checkpoint", return_value=ExecutionCheckpoint(path, OPERATION)), patch(
                "src.provisioning.s4615_shipping_point_be_gui.inspect_screen", return_value=snapshot
            ):
                with self.assertRaises(ActionBlockedError):
                    confirm_transport(session)
            session.find.assert_not_called()

    def test_independent_tvst_readback_verifies_only_exact_row(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            ExecutionCheckpoint(path, OPERATION).record(OPERATION, "AMBIGUOUS")
            from src.provisioning.s4615_shipping_point_be_gui import TABLE_ID, DETAIL_MENU_ID, KEY_ID, COUNTRY_DETAIL_ID, DESCRIPTION_ID
            overview = {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "500", "popups": [],
                        "tables": [{"id": TABLE_ID, "visible_rows": [{"index": 2, "values": [
                            {"column": "0", "text": "1010"}, {"column": "1", "text": "Pt exp�dition 1010"}]}]}],
                        "buttons": [{"id": DETAIL_MENU_ID, "text": "D�tail", "type": "GuiMenu"}]}
            detail = {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "510", "popups": [],
                      "input_fields": [{"id": KEY_ID, "text": "1010"}, {"id": COUNTRY_DETAIL_ID, "text": "BE"},
                                       {"id": DESCRIPTION_ID, "text": "Pt exp�dition 1010"}]}
            table = Mock(Id=TABLE_ID, Type="GuiTableControl")
            menu = Mock(Id=DETAIL_MENU_ID, Type="GuiMenu", Text="D�tail")
            session = Mock()
            session.find.side_effect = lambda cid: table if cid == TABLE_ID else menu
            with patch("src.provisioning.s4615_shipping_point_be_gui._checkpoint", side_effect=lambda: ExecutionCheckpoint(path, OPERATION)), patch(
                "src.provisioning.s4615_shipping_point_be_gui.inspect_screen", side_effect=[overview, detail]
            ):
                self.assertEqual("CREATED_AND_VERIFIED", verify_readback(session)["status"])
            table.GetAbsoluteRow.assert_called_once_with(2)
            menu.select.assert_called_once_with()
            self.assertEqual("VERIFIED", ExecutionCheckpoint(path, OPERATION).status(OPERATION))


if __name__ == "__main__":
    unittest.main()
