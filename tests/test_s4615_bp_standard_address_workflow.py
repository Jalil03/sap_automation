import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from src.provisioning import s4615_bp_standard_address as workflow
from src.provisioning import s4615_bp_address_gui as gui
from src.sap_runtime.transport import HttpResponse


def response(rows):
    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())


def address_row():
    return {"BusinessPartner": gui.BP, "AddressID": "1558", **gui.ADDRESS}


def usage_row():
    return {"BusinessPartner": gui.BP, "AddressID": "1558",
            "AddressUsage": "XXDEFAULT", "ValidityStartDate": "/Date(0)/",
            "ValidityEndDate": "/Date(253402214400000)/"}


class FakeTransport:
    def __init__(self, addresses, usages):
        self.addresses = addresses
        self.usages = usages
        self.calls = []

    def request(self, method, path):
        self.calls.append((method, path))
        return response(self.addresses if "A_BusinessPartnerAddress" in path else self.usages)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.approval = base / "approval.json"
        self.mapping = base / "mapping.json"
        self.attempt = base / "attempt.json"
        self.checkpoint = base / "checkpoint.json"
        self.approval.write_text(json.dumps({
            "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
            "existing_business_partner": gui.BP,
            "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "approval_scopes_evidenced": ["CUSTOMER_MASTER_OWNER"],
            "approved_scope": ["BP_ADDRESS"],
            "step_authorizations": {"BP_ADDRESS": {"execute": True}},
            "proposed_values": {"address": gui.ADDRESS},
        }), encoding="utf-8")
        self.mapping.write_text(json.dumps({"mappings": {"C615-A01": {
            "sap_id": gui.BP, "status": "LIVE_VERIFIED"}}}), encoding="utf-8")
        for module in (workflow, gui):
            for name, value in (("APPROVAL_PATH", self.approval),
                                ("MAPPING_PATH", self.mapping), ("ATTEMPT_PATH", self.attempt)):
                item = patch.object(module, name, value)
                item.start()
                self.addCleanup(item.stop)
        item = patch.object(workflow, "CHECKPOINT_PATH", self.checkpoint)
        item.start()
        self.addCleanup(item.stop)
        self.config = type("Config", (), {"client": "600", "username": "ABDELJ"})()

    def test_read_state_requires_current_default_and_exact_values(self):
        now = datetime(2026, 10, 18, tzinfo=timezone.utc)
        self.assertEqual("MISSING", workflow.read_state(FakeTransport([], []), today=now)["state"])
        self.assertEqual("EXISTS", workflow.read_state(
            FakeTransport([address_row()], [usage_row()]), today=now)["state"])
        self.assertEqual("UNKNOWN", workflow.read_state(
            FakeTransport([address_row()], []), today=now)["state"])
        wrong = {**address_row(), "Country": "US"}
        self.assertEqual("UNKNOWN", workflow.read_state(
            FakeTransport([wrong], [usage_row()]), today=now)["state"])

    def test_dry_run_inspects_but_does_not_write(self):
        client = FakeTransport([], [])
        actions = []

        def sender(action, params, mode):
            actions.append((action, mode))
            return {"request_id": "read"}

        def waiter(request_id, timeout_seconds):
            return {"status": "SUCCESS", "sap": {"system": "A4H", "client": "600", "user": "ABDELJ"},
                    "result": {"bp": gui.BP, "english_key": "E",
                               "fields": {name: {"value": ""} for name in gui.ADDRESS}}}

        result = workflow.ensure_address(self.config, transport_factory=lambda _: client,
                                         sender=sender, waiter=waiter)
        self.assertEqual("WOULD_CREATE", result["status"])
        self.assertEqual([("INSPECT_BP_STANDARD_ADDRESS", "READ")], actions)
        self.assertEqual(2, len(client.calls))
        self.assertFalse(self.checkpoint.exists())

    def test_execute_one_save_then_independent_readback_and_checkpoint(self):
        clients = [FakeTransport([], []), FakeTransport([address_row()], [usage_row()])]
        actions = []

        def sender(action, params, mode):
            actions.append((action, mode))
            return {"request_id": action}

        def waiter(request_id, timeout_seconds):
            result = ({"bp": gui.BP, "english_key": "E",
                       "fields": {name: {"value": ""} for name in gui.ADDRESS}}
                      if request_id == "INSPECT_BP_STANDARD_ADDRESS"
                      else {"save_attempted": True})
            return {"status": "SUCCESS", "sap": {"system": "A4H", "client": "600", "user": "ABDELJ"},
                    "result": result}

        result = workflow.ensure_address(self.config, execute=True,
                                         transport_factory=lambda _: clients.pop(0),
                                         sender=sender, waiter=waiter)
        self.assertEqual({"status": "CREATED_AND_VERIFIED", "address_id": "1558"}, result)
        self.assertEqual(1, actions.count(("PHASE5_OPERATION", "EXECUTE")))
        self.assertEqual("VERIFIED", json.loads(self.checkpoint.read_text())["operations"]["ENSURE_BP_STANDARD_ADDRESS"]["status"])
        self.assertEqual("EXISTS_CURRENT_XXDEFAULT", json.loads(self.approval.read_text())["verified_step_states"]["BP_ADDRESS"])

    def test_prior_attempt_blocks_before_sap_write(self):
        self.attempt.write_text('{"status":"SAVE_ATTEMPTED"}', encoding="utf-8")
        actions = []

        def sender(action, params, mode):
            actions.append(action)
            return {"request_id": action}

        def waiter(request_id, timeout_seconds):
            return {"status": "SUCCESS", "sap": {"system": "A4H", "client": "600", "user": "ABDELJ"},
                    "result": {"bp": gui.BP, "english_key": "E",
                               "fields": {name: {"value": ""} for name in gui.ADDRESS}}}

        result = workflow.ensure_address(self.config, execute=True,
                                         transport_factory=lambda _: FakeTransport([], []),
                                         sender=sender, waiter=waiter)
        self.assertEqual("BLOCKED", result["status"])
        self.assertNotIn("PHASE5_OPERATION", actions)


if __name__ == "__main__":
    unittest.main()
