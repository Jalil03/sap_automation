import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from src.provisioning.s4615_shipping_point_gui import (
    NEW_ENTRIES_ID, TABLE_ID, SAVE_ID, KEY_ID, DESCRIPTION_ID, VALUES,
    inspect_new_entry_form, lookup_from_snapshot, save_once, cancel_empty_address_popup,
    confirm_discard_address,
)
from src.sap_gui_bridge.errors import ActionBlockedError


def overview(keys):
    return {
        "transaction": "OVXD", "program": "SAPLV03B", "screen_number": "500", "popups": [],
        "tables": [{"id": TABLE_ID, "visible_rows": [
            {"index": index, "values": [{"column": "0", "text": key}]}
            for index, key in enumerate(keys)
        ]}],
        "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO",
                          "text": f"Entrée 1 / {len(keys)}"}],
        "buttons": [{"id": NEW_ENTRIES_ID, "type": "GuiButton", "text": "Nouvelles entrées"}],
    }


class ShippingPointGuiTests(unittest.TestCase):
    def test_complete_rows_prove_missing(self):
        self.assertEqual("MISSING", lookup_from_snapshot(overview(["0001", "1710"]))["state"])

    def test_target_found_or_incomplete_does_not_prove_missing(self):
        self.assertEqual("EXISTS", lookup_from_snapshot(overview(["0001", "1010"]))["state"])
        partial = overview(["0001"])
        partial["input_fields"][0]["text"] = "Entrée 1 / 19"
        self.assertEqual("UNKNOWN", lookup_from_snapshot(partial)["state"])

    def test_form_inspect_uses_exact_button_without_save(self):
        button = Mock(Id=NEW_ENTRIES_ID, Type="GuiButton")
        session = Mock()
        session.find.return_value = button
        with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen",
                   side_effect=[overview(["0001", "1710"]), {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "510", "popups": [], "input_fields": []}]):
            result = inspect_new_entry_form(session)
        button.press.assert_called_once_with()
        self.assertFalse(result["saved"])
        self.assertEqual(2, session.validate_identity.call_count)

    def test_wrong_button_blocks_without_press(self):
        session = Mock()
        snapshot = overview(["0001"])
        snapshot["buttons"][0]["text"] = "Supprimer"
        with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                inspect_new_entry_form(session)
        session.find.assert_not_called()

    def test_existing_form_reports_native_required_fields_without_press(self):
        session = Mock()
        session.find.return_value.Required = 1
        form = {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "510",
                "popups": [], "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVST-VSTEL",
                                                 "text": None, "changeable": True}]}
        with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", return_value=form):
            result = inspect_new_entry_form(session)
        self.assertTrue(result["field_requirements"][0]["required"])
        self.assertFalse(result["saved"])
        session.find.return_value.press.assert_not_called()

    def test_address_popup_is_inspected_without_another_save(self):
        session = Mock()
        session.find.return_value.Required = 1
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Traiter l'adresse:  1010",
                 "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY",
                                  "text": None, "changeable": True}]}
        snapshot = {"transaction": "OVXD", "program": "SAPLSZA1", "screen_number": "201", "popups": [popup]}
        with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", return_value=snapshot):
            result = inspect_new_entry_form(session)
        self.assertTrue(result["address_field_requirements"][0]["required"])
        session.find.return_value.press.assert_not_called()

    def test_single_save_stages_only_approved_fields_and_checkpoints(self):
        controls = {
            NEW_ENTRIES_ID: Mock(Id=NEW_ENTRIES_ID, Type="GuiButton"),
            KEY_ID: Mock(Id=KEY_ID, Type="GuiTextField", MaxLength=4),
            DESCRIPTION_ID: Mock(Id=DESCRIPTION_ID, Type="GuiTextField", MaxLength=20),
            SAVE_ID: Mock(Id=SAVE_ID, Type="GuiButton", Text="Sauvegarder"),
        }
        session = Mock()
        session.find.side_effect = lambda control_id: controls[control_id]
        blank = {"transaction": "OVXD", "program": "SAPLV03B", "screen_number": "510", "popups": [],
                 "input_fields": [{"id": KEY_ID, "text": None, "changeable": True, "type": "GuiTextField"},
                                  {"id": DESCRIPTION_ID, "text": None, "changeable": True, "type": "GuiTextField"}]}
        staged = {**blank, "input_fields": [
            {"id": KEY_ID, "text": "1010", "changeable": True, "type": "GuiTextField"},
            {"id": DESCRIPTION_ID, "text": VALUES["description"], "changeable": True, "type": "GuiTextField"},
        ]}
        with tempfile.TemporaryDirectory() as temp, patch(
            "src.provisioning.s4615_shipping_point_gui.CHECKPOINT_PATH", Path(temp) / "checkpoint.json"
        ), patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", side_effect=[
            overview(["0001", "1710"]), overview(["0001", "1710"]), blank, staged, {"transaction": "OVXD"}
        ]):
            result = save_once(session, {"shipping_point": "1010"}, VALUES)
            self.assertTrue((Path(temp) / "checkpoint.json").exists())
            with self.assertRaises(ActionBlockedError):
                save_once(session, {"shipping_point": "1010"}, VALUES)
        self.assertTrue(result["save_attempted"])
        self.assertFalse(result["verified"])
        self.assertEqual("1010", controls[KEY_ID].Text)
        self.assertEqual(VALUES["description"], controls[DESCRIPTION_ID].Text)
        controls[SAVE_ID].press.assert_called_once_with()

    def test_unapproved_values_block_before_gui(self):
        session = Mock()
        with self.assertRaises(ActionBlockedError):
            save_once(session, {"shipping_point": "1010"}, {"description": "Other"})
        session.find.assert_not_called()

    def test_only_untouched_exact_address_popup_can_be_cancelled(self):
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Traiter l'adresse:  1010",
                 "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY", "text": None}],
                 "buttons": [{"id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[12]",
                              "type": "GuiButton", "tooltip": "Annuler   (F12)"}]}
        before = {"transaction": "OVXD", "program": "SAPLSZA1", "screen_number": "201", "popups": [popup]}
        button = Mock(Id="/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[12]", Type="GuiButton", Tooltip="Annuler   (F12)")
        session = Mock()
        session.find.return_value = button
        with tempfile.TemporaryDirectory() as temp, patch(
            "src.provisioning.s4615_shipping_point_gui.CHECKPOINT_PATH", Path(temp) / "checkpoint.json"
        ):
            from src.provisioning.execution_policy import ExecutionCheckpoint
            ExecutionCheckpoint(Path(temp) / "checkpoint.json", "S4615_SHIPPING_POINT_1010").record(
                "S4615_SHIPPING_POINT_1010", "AMBIGUOUS")
            with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen",
                       side_effect=[before, {"transaction": "OVXD", "popups": []}]):
                result = cancel_empty_address_popup(session)
        self.assertTrue(result["address_popup_cancelled"])
        button.press.assert_called_once_with()

    def test_entered_address_prevents_cancel(self):
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Traiter l'adresse:  1010",
                 "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY", "text": "BE"}],
                 "buttons": []}
        session = Mock()
        with tempfile.TemporaryDirectory() as temp, patch(
            "src.provisioning.s4615_shipping_point_gui.CHECKPOINT_PATH", Path(temp) / "checkpoint.json"
        ):
            from src.provisioning.execution_policy import ExecutionCheckpoint
            ExecutionCheckpoint(Path(temp) / "checkpoint.json", "S4615_SHIPPING_POINT_1010").record(
                "S4615_SHIPPING_POINT_1010", "AMBIGUOUS")
            with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", return_value={
                "transaction": "OVXD", "program": "SAPLSZA1", "screen_number": "201", "popups": [popup]
            }):
                with self.assertRaises(ActionBlockedError):
                    cancel_empty_address_popup(session)
        session.find.assert_not_called()

    def test_exact_discard_confirmation_does_not_retry_save(self):
        address = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Traiter l'adresse:  1010",
                   "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY", "text": None}]}
        confirm = {"id": "/app/con[0]/ses[0]/wnd[2]", "window_title": "Interrompre gestion des adresses",
                   "input_fields": [{"text": "Les données seront perdues."}],
                   "buttons": [{"id": "/app/con[0]/ses[0]/wnd[2]/usr/btnSPOP-OPTION1",
                                "text": "Oui", "type": "GuiButton"}]}
        session = Mock()
        button = Mock(Id="/app/con[0]/ses[0]/wnd[2]/usr/btnSPOP-OPTION1", Type="GuiButton", Text="Oui")
        session.find.return_value = button
        with tempfile.TemporaryDirectory() as temp, patch(
            "src.provisioning.s4615_shipping_point_gui.CHECKPOINT_PATH", Path(temp) / "checkpoint.json"
        ):
            from src.provisioning.execution_policy import ExecutionCheckpoint
            ExecutionCheckpoint(Path(temp) / "checkpoint.json", "S4615_SHIPPING_POINT_1010").record(
                "S4615_SHIPPING_POINT_1010", "AMBIGUOUS")
            with patch("src.provisioning.s4615_shipping_point_gui.inspect_screen", side_effect=[
                {"transaction": "OVXD", "program": "SAPLSPO1", "screen_number": "200", "popups": [address, confirm]},
                {"transaction": "OVXD", "popups": []},
            ]):
                result = confirm_discard_address(session)
        self.assertTrue(result["address_discard_confirmed"])
        button.press.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
