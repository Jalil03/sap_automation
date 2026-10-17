import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_s4615_e2e import EXPECTED, _book_payload, main as e2e_main
from scripts.run_phase5_execute import main as phase5_main
from src.provisioning.phase5 import Phase5ProvisioningEngine


ROOT = Path(__file__).resolve().parents[1]


def complete_decisions():
    return {
        "COMPANY_CODE_1010": {
            "creation_strategy": "MANUAL_CREATE",
            "company_name": "DECIDED_COMPANY_NAME",
            "city": "DECIDED_CITY",
            "country": "ZZ",
            "currency": "ZZZ",
            "language": "EN",
        },
        "SALES_ORGANIZATION_1010": {
            "creation_strategy": "MANUAL_CREATE",
            "description": "DECIDED_SALES_ORG_DESCRIPTION",
            "statistics_currency": "ZZZ",
            "intercompany_customer": None,
            "purchasing_organization": None,
            "purchasing_group": None,
            "purchasing_order_type": None,
            "rebate_active": False,
            "address_text": None,
            "letter_header_text": None,
            "footer_text": None,
            "sales_org_calendar": None,
            "greeting_text": None,
            "standard_text": None,
        },
        "CUSTOMER_C615_D00": {
            "grouping": "DECIDED_GROUPING",
            "name": "DECIDED_CUSTOMER_NAME",
            "roles": ["DECIDED_ROLE"],
            "addresses": [{"country": "ZZ"}],
            "reconciliation_account": "DECIDED_ACCOUNT",
            "payment_terms": "DECIDED_TERMS",
            "currency": "ZZZ",
            "shipping_conditions": "DECIDED_SHIPPING",
            "delivering_plant": "DECIDED_PLANT",
            "incoterms": "DECIDED_INCOTERMS",
            "incoterms_location": "DECIDED_LOCATION",
            "account_assignment_group": "DECIDED_GROUP",
            "customer_pricing_procedure": "DECIDED_PROCEDURE",
            "tax_classifications": [{"category": "DECIDED", "classification": "DECIDED"}],
            "partner_functions": [{"role": "DO", "partner": "C615-D00"}],
        },
        "PRODUCT_P615_400": {
            "description": "DECIDED_PRODUCT_DESCRIPTION",
            "material_type": "DECIDED_TYPE",
            "industry_sector": "DECIDED_SECTOR",
            "base_unit": "PC",
            "plants": ["DECIDED_PLANT"],
            "delivering_plant": "DECIDED_PLANT",
            "item_category_group": "DECIDED_GROUP",
            "tax_classification": "DECIDED_TAX",
            "availability_check": "DECIDED_CHECK",
            "alternative_units": ["PC"],
        },
    }


class FakeBackend:
    writable = True

    def __init__(self, states=None, *, readback=True, write_result=None):
        self.states = states or {}
        self.calls = []
        self.readback_enabled = readback
        self.write_result = write_result or {"accepted": True}

    def lookup(self, operation, target):
        self.calls.append(("lookup", operation, dict(target)))
        return self.states.get(operation, "MISSING")

    def provision(self, operation, target, values):
        self.calls.append(("provision", operation, dict(target), dict(values)))
        return self.write_result

    def readback(self, operation, target):
        self.calls.append(("readback", operation, dict(target)))
        return dict(target) if self.readback_enabled else None


class Phase5OneShotTests(unittest.TestCase):
    def test_exact_book_payload_is_preserved_for_user_00(self):
        payload, trace = _book_payload("00")
        for field, value in EXPECTED.items():
            self.assertEqual(value, payload[field])
        self.assertEqual("P615-400", payload["to_Item"][0]["Material"])
        self.assertEqual(1, payload["to_Item"][0]["RequestedQuantity"])
        self.assertEqual("PC", payload["to_Item"][0]["RequestedQuantityUnit"])
        self.assertEqual("00", trace["training_user_code"])

    def test_default_dry_run_is_offline_and_consolidates_decision_blockers(self):
        backend = FakeBackend()
        backend.writable = False
        result = Phase5ProvisioningEngine(backend=backend).plan(include_book_data=True)
        self.assertEqual("BLOCKED", result["status"])
        operations = {item["operation"] for item in result["blockers"]}
        self.assertIn("COMPANY_CODE_1010", operations)
        self.assertIn("SALES_ORGANIZATION_1010", operations)
        self.assertIn("CUSTOMER_C615_D00", operations)
        self.assertIn("PRODUCT_P615_400", operations)
        self.assertFalse(any(call[0] == "provision" for call in backend.calls))

    def test_exists_skips_without_write(self):
        backend = FakeBackend(states={"COMPANY_CODE_1010": "EXISTS"})
        engine = Phase5ProvisioningEngine(backend=backend, execute=True)
        result = engine.ensure_company_code()
        self.assertEqual("SKIPPED_EXISTS", result.status)
        self.assertFalse(any(call[0] == "provision" for call in backend.calls))

    def test_live_exists_overrides_unknown_planned_state_and_continues(self):
        backend = FakeBackend(states={
            "COMPANY_CODE_1010": "EXISTS",
            "SALES_ORGANIZATION_1010": "EXISTS",
            "SALES_ORG_1010_TO_COMPANY_CODE_1010": "EXISTS",
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": "EXISTS",
            "DIVISION_00_TO_SALES_ORG_1010": "EXISTS",
        })
        backend.planned_states = {"COMPANY_CODE_1010": "UNKNOWN"}

        result = Phase5ProvisioningEngine(
            backend=backend, execute=True
        ).plan()

        self.assertEqual(
            ["LOOKUP"] * 5,
            [call[0].upper() for call in backend.calls],
        )
        self.assertEqual(
            [
                "COMPANY_CODE_1010",
                "SALES_ORGANIZATION_1010",
                "SALES_ORG_1010_TO_COMPANY_CODE_1010",
                "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
                "DIVISION_00_TO_SALES_ORG_1010",
            ],
            [call[1] for call in backend.calls],
        )
        self.assertEqual(
            ["SKIPPED_EXISTS"] * 5,
            [item["status"] for item in result["results"]],
        )
        self.assertEqual("EXISTS", result["results"][0]["before_state"])

    def test_missing_complete_dry_run_would_provision_without_write(self):
        backend = FakeBackend()
        engine = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=False
        )
        result = engine.ensure_company_code()
        self.assertEqual("WOULD_PROVISION", result.status)
        self.assertFalse(any(call[0] == "provision" for call in backend.calls))

    def test_live_missing_reaches_provisioning_after_lookup(self):
        backend = FakeBackend(states={"COMPANY_CODE_1010": "MISSING"})
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        ).ensure_company_code()

        self.assertEqual("PROVISIONED_VERIFIED", result.status)
        self.assertEqual(
            ["lookup", "provision", "readback"],
            [call[0] for call in backend.calls],
        )

    def test_execute_is_ordered_and_reads_back_every_write(self):
        backend = FakeBackend()
        engine = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        )
        result = engine.plan(include_book_data=True)
        self.assertEqual("READY", result["status"])
        provisions = [call[1] for call in backend.calls if call[0] == "provision"]
        readbacks = [call[1] for call in backend.calls if call[0] == "readback"]
        expected = [
            "COMPANY_CODE_1010",
            "SALES_ORGANIZATION_1010",
            "SALES_ORG_1010_TO_COMPANY_CODE_1010",
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
            "DIVISION_00_TO_SALES_ORG_1010",
            "CUSTOMER_C615_D00",
            "PRODUCT_P615_400",
        ]
        self.assertEqual(expected, provisions)
        self.assertEqual(expected, readbacks)

    def test_unknown_state_blocks_before_write(self):
        backend = FakeBackend(states={"COMPANY_CODE_1010": "UNKNOWN"})
        engine = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        )
        result = engine.ensure_company_code()
        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", result.status)
        self.assertEqual(["lookup"], [call[0] for call in backend.calls])
        self.assertFalse(any(call[0] == "provision" for call in backend.calls))

    def test_live_unknown_is_reported_at_operation_before_dependency_block(self):
        backend = FakeBackend(states={
            "COMPANY_CODE_1010": "UNKNOWN",
            "SALES_ORGANIZATION_1010": "UNKNOWN",
        })
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        ).plan()

        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", result["results"][0]["status"])
        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", result["results"][1]["status"])
        self.assertEqual(
            [
                "COMPANY_CODE_1010",
                "SALES_ORGANIZATION_1010",
                "SALES_ORG_1010_TO_COMPANY_CODE_1010",
                "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
                "DIVISION_00_TO_SALES_ORG_1010",
            ],
            [call[1] for call in backend.calls],
        )
        self.assertFalse(any(call[0] == "provision" for call in backend.calls))

    def test_live_exists_satisfies_downstream_dependencies(self):
        backend = FakeBackend(states={
            "COMPANY_CODE_1010": "EXISTS",
            "SALES_ORGANIZATION_1010": "EXISTS",
            "SALES_ORG_1010_TO_COMPANY_CODE_1010": "EXISTS",
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": "EXISTS",
            "DIVISION_00_TO_SALES_ORG_1010": "EXISTS",
        })
        result = Phase5ProvisioningEngine(
            backend=backend, execute=True
        ).plan()

        self.assertEqual(
            ["SKIPPED_EXISTS"] * 3,
            [item["status"] for item in result["results"][:3]],
        )
        self.assertEqual(
            [
                "COMPANY_CODE_1010",
                "SALES_ORGANIZATION_1010",
                "SALES_ORG_1010_TO_COMPANY_CODE_1010",
                "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
                "DIVISION_00_TO_SALES_ORG_1010",
            ],
            [call[1] for call in backend.calls],
        )

    def test_execute_does_not_bypass_unknown_assignment_read(self):
        backend = FakeBackend(states={
            "COMPANY_CODE_1010": "EXISTS",
            "SALES_ORGANIZATION_1010": "EXISTS",
            "SALES_ORG_1010_TO_COMPANY_CODE_1010": "UNKNOWN",
        })
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        ).plan()
        assignment = next(
            item for item in result["results"]
            if item["operation"] == "SALES_ORG_1010_TO_COMPANY_CODE_1010"
        )
        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", assignment["status"])
        self.assertFalse(any(
            call[0] == "provision" and call[1] == "SALES_ORG_1010_TO_COMPANY_CODE_1010"
            for call in backend.calls
        ))

    def test_readback_failure_blocks(self):
        backend = FakeBackend(readback=False)
        engine = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        )
        result = engine.ensure_company_code()
        self.assertEqual("BLOCKED_READBACK", result.status)

    def test_transport_request_stops_without_readback_or_release(self):
        backend = FakeBackend(write_result={"transport_request": "REQ-REDACTED"})
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_TRANSPORT_REQUIRED", result.status)
        self.assertFalse(any(call[0] == "readback" for call in backend.calls))

    def test_unexpected_popup_stops_without_retry(self):
        backend = FakeBackend(write_result={"unexpected_popup": "unknown"})
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=complete_decisions(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_UNEXPECTED_POPUP", result.status)
        self.assertEqual(1, sum(call[0] == "provision" for call in backend.calls))
        self.assertFalse(any(call[0] == "readback" for call in backend.calls))

    def test_reference_copy_strategy_is_rejected(self):
        decisions = complete_decisions()
        decisions["COMPANY_CODE_1010"]["creation_strategy"] = "COPY_1710"
        result = Phase5ProvisioningEngine(
            backend=FakeBackend(), decisions=decisions
        ).ensure_company_code()
        self.assertEqual("BLOCKED_INVALID_DECISION", result.status)

    def test_product_requires_pc_explicitly(self):
        decisions = complete_decisions()
        decisions["PRODUCT_P615_400"]["base_unit"] = "EA"
        decisions["PRODUCT_P615_400"]["alternative_units"] = []
        result = Phase5ProvisioningEngine(
            backend=FakeBackend(), decisions=decisions
        )._ensure("PRODUCT_P615_400")
        self.assertEqual("BLOCKED_INVALID_DECISION", result.status)

    def test_execute_cli_requires_explicit_backend_and_decisions(self):
        with patch("builtins.input", return_value="EXECUTE PHASE5 COMMON 1010"):
            self.assertEqual(2, phase5_main(["--execute"]))

    def test_cli_mode_defaults_to_dry_run(self):
        self.assertEqual(2, phase5_main([]))
        self.assertEqual(0, e2e_main(["--training-user", "00"]))

    def test_e2e_rejects_non_book_user(self):
        self.assertEqual(2, e2e_main(["--training-user", "07", "--dry-run"]))

    def test_canonical_file_is_immutable(self):
        path = ROOT / "data/validated/canonical_objects.json"
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        _book_payload("00")
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
