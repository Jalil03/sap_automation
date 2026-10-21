import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.provisioning import s4600_t_s50a01_bp_address as workflow
from src.provisioning import s4600_t_s50a01_bp_address_gui as gui
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_runtime.transport import HttpResponse


class FakeField:
    def __init__(self, control_id, type_name):
        self.Id, self.Type, self.Text, self.Changeable = control_id, type_name, "", True


class FakeEntries:
    Count = 1

    def __call__(self, index):
        return SimpleNamespace(Key="E", Value="Anglais")


class FakeCombo:
    def __init__(self):
        self.Id, self.Type, self.Key = gui.FIELD_IDS["Language"], "GuiComboBox", ""
        self.Entries = FakeEntries()


class FakeButton:
    def __init__(self):
        self.Id, self.Type, self.Text, self.presses = gui.SAVE_ID, "GuiButton", "Sauvegarder", 0

    def press(self):
        self.presses += 1


class FakeSession:
    def __init__(self):
        self.controls = {
            name: FakeField(control_id, gui.FIELD_TYPES[name])
            for name, control_id in gui.FIELD_IDS.items() if name != "Language"
        }
        self.controls["Language"] = FakeCombo()
        self.button = FakeButton()

    def validate_identity(self):
        pass

    def find(self, control_id):
        if control_id == gui.SAVE_ID:
            return self.button
        return next(value for value in self.controls.values() if value.Id == control_id)

    def audit(self, *args, **kwargs):
        pass

    def snapshot(self):
        fields = [{"id": gui.HEADER, "type": "GuiCTextField", "text": gui.BP}]
        fields += [{"id": item.Id, "type": item.Type, "text": getattr(item, "Text", ""), "changeable": True}
                   for item in self.controls.values()]
        return {
            "transaction": "BP", "program": "SAPLBUS_LOCATOR", "screen_number": "3000",
            "window_title": f"Modifier Organisation : {gui.BP}", "popups": [], "truncated": False,
            "input_fields": fields,
            "buttons": [{"id": gui.SAVE_ID, "type": "GuiButton", "text": "Sauvegarder"}],
            "status_bar": {"text": "", "message_type": ""},
        }


def response(rows):
    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())


class FakeTransport:
    def __init__(self, addresses, usages):
        self.addresses, self.usages = addresses, usages

    def request(self, method, path):
        return response(self.addresses if "A_BusinessPartnerAddress" in path else self.usages)


class T_S50A01AddressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.approval, self.mapping = base / "approval.json", base / "mapping.json"
        self.attempt, self.checkpoint = base / "attempt.json", base / "checkpoint.json"
        self.approval.write_text(json.dumps({
            "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
            "operation": gui.OPERATION, "existing_business_partner": gui.BP,
            "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "approval_scopes_evidenced": ["CUSTOMER_MASTER_OWNER", "TRAINING_MASTER_DATA_BP_ADDRESS"],
            "approved_scope": ["BP_ADDRESS"], "target_fingerprint": gui.FINGERPRINT,
            "step_authorizations": {"BP_ADDRESS": {"execute": True}},
            "proposed_values": {"address": gui.ADDRESS},
        }), encoding="utf-8")
        self.mapping.write_text(json.dumps({"mappings": {"T-S50A01": {
            "sap_id": gui.BP, "status": "LIVE_VERIFIED", "evidence": {}}}}), encoding="utf-8")
        for module in (workflow, gui):
            for name, value in (("APPROVAL_PATH", self.approval), ("MAPPING_PATH", self.mapping),
                                ("ATTEMPT_PATH", self.attempt)):
                item = patch.object(module, name, value); item.start(); self.addCleanup(item.stop)
        item = patch.object(workflow, "CHECKPOINT_PATH", self.checkpoint); item.start(); self.addCleanup(item.stop)
        item = patch.object(gui, "inspect_screen", lambda session: session.snapshot()); item.start(); self.addCleanup(item.stop)
        self.config = type("Config", (), {"client": "600", "username": "ABDELJ"})()

    def test_exact_one_gui_save_and_attempt_marker(self):
        session = FakeSession()
        result = gui.save_once(session, gui.TARGET, gui.ADDRESS)
        self.assertTrue(result["save_attempted"])
        self.assertEqual(1, session.button.presses)
        with self.assertRaisesRegex(ActionBlockedError, "Prior"):
            gui.save_once(session, gui.TARGET, gui.ADDRESS)
        self.assertEqual(1, session.button.presses)

    def test_wrong_fingerprint_blocks_before_save(self):
        value = json.loads(self.approval.read_text())
        value["target_fingerprint"] = "wrong"
        self.approval.write_text(json.dumps(value), encoding="utf-8")
        session = FakeSession()
        with self.assertRaisesRegex(ActionBlockedError, "approval mismatch"):
            gui.save_once(session, gui.TARGET, gui.ADDRESS)
        self.assertEqual(0, session.button.presses)

    def test_read_state_requires_exact_current_default(self):
        address = {"BusinessPartner": gui.BP, "AddressID": "2000", **gui.ADDRESS}
        usage = {"BusinessPartner": gui.BP, "AddressID": "2000", "AddressUsage": "XXDEFAULT",
                 "ValidityStartDate": "/Date(0)/", "ValidityEndDate": "/Date(253402214400000)/"}
        now = datetime(2026, 10, 20, tzinfo=timezone.utc)
        self.assertEqual("MISSING", workflow.read_state(FakeTransport([], []), today=now)["state"])
        self.assertEqual("EXISTS", workflow.read_state(FakeTransport([address], [usage]), today=now)["state"])

    def test_dry_run_never_sends_execute(self):
        actions = []
        def sender(action, params, mode):
            actions.append((action, mode)); return {"request_id": action}
        def waiter(request_id, timeout_seconds):
            return {"status": "SUCCESS", "sap": {"system": "A4H", "client": "600", "user": "ABDELJ"},
                    "result": {"bp": gui.BP, "english_key": "E",
                               "fields": {name: {"value": ""} for name in gui.ADDRESS}}}
        result = workflow.ensure_address(self.config, transport_factory=lambda _: FakeTransport([], []),
                                         sender=sender, waiter=waiter)
        self.assertEqual("WOULD_CREATE", result["status"])
        self.assertEqual([(workflow.INSPECT_ACTION, "READ")], actions)


if __name__ == "__main__":
    unittest.main()
