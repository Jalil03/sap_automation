import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.provisioning import s4615_bp_address_gui as address
from src.sap_gui_bridge.errors import ActionBlockedError


class FakeCombo:
    def __init__(self):
        self.Id = address.FIELD_IDS["Language"]
        self.Type = "GuiComboBox"
        self.Key = ""
        self.Entries = FakeEntries()


class FakeEntries:
    Count = 2

    def __call__(self, index):
        values = [("E", "Anglais"), ("F", "FranÃ§ais")]
        return SimpleNamespace(Key=values[index][0], Value=values[index][1])


class FakeField:
    def __init__(self, control_id, type_name):
        self.Id = control_id
        self.Type = type_name
        self.Text = ""
        self.Changeable = True


class FakeButton:
    def __init__(self):
        self.Id = address.SAVE_ID
        self.Type = "GuiButton"
        self.Text = "Sauvegarder"
        self.presses = 0

    def press(self):
        self.presses += 1


class FakeSession:
    def __init__(self):
        self.controls = {name: FakeField(control_id, address.FIELD_TYPES[name])
                         for name, control_id in address.FIELD_IDS.items() if name != "Language"}
        self.controls["Language"] = FakeCombo()
        self.button = FakeButton()
        self.audits = []

    def validate_identity(self):
        pass

    def find(self, control_id):
        if control_id == address.SAVE_ID:
            return self.button
        return next(value for value in self.controls.values() if value.Id == control_id)

    def audit(self, action, **kwargs):
        self.audits.append(action)

    def snapshot(self):
        fields = [{"id": address.HEADER, "type": "GuiCTextField", "text": address.BP}]
        fields.extend({"id": control.Id, "type": control.Type,
                       "text": getattr(control, "Text", ""), "changeable": True}
                      for control in self.controls.values())
        return {
            "transaction": "BP", "program": "SAPLBUS_LOCATOR", "screen_number": "3000",
            "window_title": "Modifier Organisation : 1000000115", "popups": [],
            "truncated": False, "input_fields": fields,
            "buttons": [{"id": address.SAVE_ID, "type": "GuiButton", "text": "Sauvegarder"}],
            "status_bar": {"text": "", "message_type": ""},
        }


class BpAddressGuiTests(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.attempt = Path(self.temp.name) / "attempt.json"
        self.approval = Path(self.temp.name) / "approval.json"
        self.mapping = Path(self.temp.name) / "mapping.json"
        self.approval.write_text(json.dumps({
            "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
            "existing_business_partner": address.BP,
            "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "approval_scopes_evidenced": ["CUSTOMER_MASTER_OWNER"],
            "approved_scope": ["BP_ADDRESS"],
            "step_authorizations": {"BP_ADDRESS": {"execute": True}},
            "proposed_values": {"address": address.ADDRESS},
        }), encoding="utf-8")
        self.mapping.write_text(json.dumps({"mappings": {"C615-A01": {
            "sap_id": address.BP, "status": "LIVE_VERIFIED"}}}), encoding="utf-8")
        patches = [
            patch.object(address, "ATTEMPT_PATH", self.attempt),
            patch.object(address, "APPROVAL_PATH", self.approval),
            patch.object(address, "MAPPING_PATH", self.mapping),
            patch.object(address, "inspect_screen", lambda session: session.snapshot()),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)

    def test_inspection_resolves_language_from_live_combo(self):
        form = address.inspect_form(self.session)
        self.assertEqual("E", form["english_key"])
        self.assertEqual(address.BP, form["bp"])

    def test_exact_one_save_and_attempt_marker(self):
        result = address.save_once(self.session, address.TARGET, address.ADDRESS)
        self.assertTrue(result["save_attempted"])
        self.assertEqual(1, self.session.button.presses)
        self.assertEqual("E", self.session.controls["Language"].Key)
        self.assertEqual("SAVE_ATTEMPTED", json.loads(self.attempt.read_text())["status"])
        with self.assertRaisesRegex(ActionBlockedError, "Prior BP address"):
            address.save_once(self.session, address.TARGET, address.ADDRESS)
        self.assertEqual(1, self.session.button.presses)

    def test_wrong_target_or_values_never_save(self):
        for target, values in (({"sap_id": "other"}, address.ADDRESS),
                               (address.TARGET, {**address.ADDRESS, "Country": "US"})):
            with self.assertRaisesRegex(ActionBlockedError, "mismatch"):
                address.save_once(self.session, target, values)
        self.assertEqual(0, self.session.button.presses)

    def test_missing_language_choice_blocks_before_fields(self):
        self.session.controls["Language"].Entries = SimpleNamespace(Count=0)
        with self.assertRaisesRegex(ActionBlockedError, "not deterministically observed"):
            address.save_once(self.session, address.TARGET, address.ADDRESS)
        self.assertEqual(0, self.session.button.presses)
        self.assertFalse(self.attempt.exists())

    def test_existing_address_form_blocks_overwrite(self):
        self.session.controls["StreetName"].Text = "Existing"
        with self.assertRaisesRegex(ActionBlockedError, "not blank"):
            address.save_once(self.session, address.TARGET, address.ADDRESS)
        self.assertEqual(0, self.session.button.presses)

    def test_missing_step_approval_blocks(self):
        value = json.loads(self.approval.read_text())
        value["step_authorizations"]["BP_ADDRESS"]["execute"] = False
        self.approval.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(ActionBlockedError, "approval mismatch"):
            address.save_once(self.session, address.TARGET, address.ADDRESS)
        self.assertEqual(0, self.session.button.presses)


if __name__ == "__main__":
    unittest.main()
