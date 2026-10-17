import copy
import json
import unittest
from pathlib import Path

from src.sap_runtime.cli import parser
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.ledger import ExecutionLedger
from src.sap_runtime.models import CheckResult
from src.sap_runtime.errors import PreflightBlocked
from src.sap_runtime.sales_order import SalesOrderRuntime
from src.training_context import (
    InvalidTrainingUserCode,
    PlaceholderResolver,
    UnresolvedPlaceholderError,
)


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_OBJECT_ID = "S4615_CH10_EX13_SALES_ORDER_FI_REFERENCE"


class NoopVerifier:
    def verify(self, payload, transport):
        return [CheckResult("DEPENDENCIES", "PASS", "not used by payload builder")]


class NoopTransport:
    def request(self, method, path, *, headers=None, body=None):
        raise AssertionError("placeholder resolution and payload building must be offline")


def fixture(value):
    return {
        "object_id": "TRAINING_FIXTURE",
        "readiness_status": "BLOCKED",
        "blocking_reasons": [
            {
                "code": "UNRESOLVED_MANDATORY_PLACEHOLDER",
                "message": "training value unresolved",
                "field_path": "data.value",
            }
        ],
        "placeholders": [
            {
                "raw": "##",
                "resolved": None,
                "status": "UNRESOLVED",
                "mandatory": True,
                "field_path": "data.value",
            }
        ],
        "data": {"value": value},
    }


class TrainingContextTests(unittest.TestCase):
    def setUp(self):
        self.resolver = PlaceholderResolver()

    def test_supported_codes_00_01_07_10_99(self):
        for code in ("00", "01", "07", "10", "99"):
            with self.subTest(code=code):
                result = self.resolver.resolve(fixture("C615-F##"), code)
                self.assertEqual(f"C615-F{code}", result.canonical_object["data"]["value"])
                self.assertEqual("INSTRUCTOR" if code == "00" else "PARTICIPANT", result.training_user_role)

    def test_invalid_codes_are_rejected(self):
        for code in (1, 7, "1", "7", "100", "AA", "", None):
            with self.subTest(code=code):
                with self.assertRaises(InvalidTrainingUserCode):
                    self.resolver.resolve(fixture("P615-6##"), code)

    def test_examples_multiple_replacements_and_trace(self):
        obj = fixture("##S4615-AZ/##")
        result = self.resolver.resolve(obj, "07")
        self.assertEqual("07S4615-AZ/07", result.canonical_object["data"]["value"])
        trace = result.trace_metadata()
        self.assertEqual("07", trace["training_user_code"])
        self.assertEqual(2, trace["placeholders_resolved"][0]["replacements"])
        self.assertEqual("##S4615-AZ/##", trace["placeholders_resolved"][0]["original_template"])

    def test_nested_dicts_and_lists_are_resolved_recursively(self):
        obj = fixture("C615-F##")
        obj["data"]["nested"] = {
            "items": ["P615-6##", {"reference": "##S4615-AZ"}],
            "number": 10,
            "empty": None,
        }
        resolved = self.resolver.resolve(obj, "07").canonical_object
        self.assertEqual("P615-607", resolved["data"]["nested"]["items"][0])
        self.assertEqual("07S4615-AZ", resolved["data"]["nested"]["items"][1]["reference"])
        self.assertEqual(10, resolved["data"]["nested"]["number"])
        self.assertIsNone(resolved["data"]["nested"]["empty"])

    def test_source_object_is_never_mutated(self):
        obj = fixture("C615-F##")
        before = copy.deepcopy(obj)
        resolved = self.resolver.resolve(obj, "07").canonical_object
        self.assertEqual(before, obj)
        self.assertNotEqual(obj, resolved)
        self.assertEqual("##", obj["placeholders"][0]["raw"])

    def test_resolved_runtime_copy_updates_placeholder_and_readiness(self):
        resolved = self.resolver.resolve(fixture("P615-6##"), "07").canonical_object
        self.assertEqual("P615-607", resolved["placeholders"][0]["resolved"])
        self.assertEqual("RESOLVED", resolved["placeholders"][0]["status"])
        self.assertEqual("READY", resolved["readiness_status"])
        self.assertEqual([], resolved["blocking_reasons"])

    def test_remaining_executable_placeholder_blocks(self):
        obj = fixture("resolved")
        obj["data"]["illegal##key"] = "value"
        with self.assertRaises(UnresolvedPlaceholderError):
            self.resolver.resolve(obj, "07")

    def test_object_without_placeholder_is_identical(self):
        obj = {
            "object_id": "NO_PLACEHOLDER",
            "readiness_status": "READY",
            "blocking_reasons": [],
            "placeholders": [],
            "data": {"value": "P615-100", "items": [1, 2]},
        }
        result = self.resolver.resolve(obj, "07")
        self.assertEqual(obj, result.canonical_object)
        self.assertIsNot(obj, result.canonical_object)
        self.assertEqual((), result.placeholders_resolved)

    def test_cli_accepts_training_user(self):
        args = parser().parse_args([
            "sales-order", "--object", "X", "--dry-run", "--training-user", "07"
        ])
        self.assertEqual("07", args.training_user)

    def test_sales_order_builder_resolves_runtime_copy_only(self):
        canonical_path = ROOT / "data/validated/canonical_objects.json"
        before = canonical_path.read_bytes()
        runtime = SalesOrderRuntime(
            config=SapRuntimeConfig(
                base_url="https://sap.invalid",
                client="600",
                username="offline",
                password="offline",
                ledger_path=ROOT / ".test-training-ledger.sqlite3",
            ),
            transport=NoopTransport(),
            ledger=ExecutionLedger(ROOT / ".test-training-ledger.sqlite3"),
            dependency_verifier=NoopVerifier(),
        )
        self.addCleanup(lambda: (ROOT / ".test-training-ledger.sqlite3").unlink(missing_ok=True))
        obj, payload = runtime.build_payload(
            PLACEHOLDER_OBJECT_ID,
            training_user_code="07",
            customer_reference="TRAINING-07",
        )
        self.assertNotIn("##", json.dumps(payload, ensure_ascii=False))
        self.assertEqual("ZA07", payload["SalesOrderType"])
        self.assertEqual("C615-A07", payload["SoldToParty"])
        self.assertEqual("P615-107", payload["to_Item"][0]["Material"])
        self.assertEqual("READY", obj["readiness_status"])
        self.assertEqual(before, canonical_path.read_bytes())

    def test_runtime_payload_rejects_placeholder_from_operator_override(self):
        runtime = SalesOrderRuntime(
            config=SapRuntimeConfig(
                base_url="https://sap.invalid", client="600", username="offline",
                password="offline", ledger_path=ROOT / ".test-placeholder-ledger.sqlite3",
            ),
            transport=NoopTransport(),
            ledger=ExecutionLedger(ROOT / ".test-placeholder-ledger.sqlite3"),
            dependency_verifier=NoopVerifier(),
        )
        self.addCleanup(lambda: (ROOT / ".test-placeholder-ledger.sqlite3").unlink(missing_ok=True))
        with self.assertRaises(PreflightBlocked):
            runtime.build_payload(
                "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT",
                customer_reference="INVALID-##",
            )


if __name__ == "__main__":
    unittest.main()
