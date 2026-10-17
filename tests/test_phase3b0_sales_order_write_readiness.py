import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from src.sap_mapping import validate_payload_body, validate_runtime_contract
from src.sap_mapping.odata_metadata import parse_odata_v2_metadata


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "evidence/pilot"


def json_hash(value):
    compact = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


class Phase3B0SalesOrderWriteReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objects = json.loads((ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8"))["objects"]
        cls.index = {obj["object_id"]: obj for obj in cls.objects}
        cls.candidate = json.loads((PILOT / "sales_order_candidate.json").read_text(encoding="utf-8"))
        cls.payload = json.loads((PILOT / "sales_order_proposed_payload.json").read_text(encoding="utf-8"))
        cls.checklist = json.loads((PILOT / "sales_order_dependency_checklist.json").read_text(encoding="utf-8"))
        cls.metadata = parse_odata_v2_metadata(ROOT / "evidence/sap_live/odata/API_SALES_ORDER_SRV.metadata.xml")

    def test_candidate_is_the_only_execution_ready_sales_order(self):
        ready = []
        for obj in self.objects:
            if obj["object_type"] != "SALES_ORDER":
                continue
            result = validate_runtime_contract(
                obj, object_index=self.index,
                structural_fixture=obj["readiness_status"] == "BLOCKED",
            )
            if result["runtime_status"] == "EXECUTION_READY":
                ready.append(obj["object_id"])
        self.assertEqual(
            ["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT"], ready
        )
        self.assertEqual(self.index[ready[0]], self.candidate)

    def test_proposed_payload_is_exact_and_locally_valid(self):
        self.assertEqual({
            "SalesOrderType": "OR",
            "SalesOrganization": "1010",
            "DistributionChannel": "10",
            "OrganizationDivision": "00",
            "SoldToParty": "C615-A00",
            "PurchaseOrderByCustomer": "4712",
            "CustomerPaymentTerms": "R001",
            "to_Partner": [{"PartnerFunction": "DO", "Customer": "C615-A00"}],
            "to_Item": [{
                "SalesOrderItem": "10", "Material": "P615-100",
                "RequestedQuantity": 10, "RequestedQuantityUnit": "PC",
            }],
        }, self.payload)
        self.assertEqual([], validate_payload_body("SALES_ORDER", self.payload))

    def test_payload_matches_offline_mapper(self):
        result = validate_runtime_contract(self.candidate, object_index=self.index)
        self.assertEqual("EXECUTION_READY", result["runtime_status"])
        self.assertEqual(self.payload, result["payloads"][0]["body"])

    def test_every_payload_property_is_metadata_backed_and_creatable(self):
        header = self.metadata["entity_types"]["A_SalesOrderType"]
        item = self.metadata["entity_types"]["A_SalesOrderItemType"]
        partner = self.metadata["entity_types"]["A_SalesOrderHeaderPartnerType"]
        self.assertEqual("API_SALES_ORDER_SRV.A_SalesOrderItemType", header["navigation_properties"]["to_Item"]["target_type"])
        self.assertEqual("API_SALES_ORDER_SRV.A_SalesOrderHeaderPartnerType", header["navigation_properties"]["to_Partner"]["target_type"])
        for field in set(self.payload) - {"to_Item", "to_Partner"}:
            self.assertTrue(header["properties"][field]["creatable"]["metadata_effective"], field)
        for field in self.payload["to_Item"][0]:
            self.assertTrue(item["properties"][field]["creatable"]["metadata_effective"], field)
        for field in self.payload["to_Partner"][0]:
            self.assertTrue(partner["properties"][field]["creatable"]["metadata_effective"], field)

    def test_external_partner_code_is_used_without_internal_code(self):
        row = self.payload["to_Partner"][0]
        self.assertEqual("DO", row["PartnerFunction"])
        self.assertNotIn("PartnerFunctionInternalCode", row)
        internal = self.metadata["entity_types"]["A_SalesOrderHeaderPartnerType"]["properties"]["PartnerFunctionInternalCode"]
        self.assertFalse(internal["creatable"]["metadata_effective"])
        self.assertFalse(internal["updatable"]["metadata_effective"])

    def test_dependency_prechecks_are_complete_and_unexecuted(self):
        expected = {
            "CUSTOMER", "PARTNER_FUNCTION", "MATERIAL", "SALES_ORGANIZATION",
            "DISTRIBUTION_CHANNEL", "SALES_DIVISION", "SALES_DOCUMENT_TYPE",
            "UNIT_OF_MEASURE", "PAYMENT_TERMS", "PLANT", "SHIPPING_POINT",
        }
        dependencies = self.checklist["dependencies"]
        self.assertEqual(expected, {item["type"] for item in dependencies})
        self.assertTrue(all(item["status"] == "REQUIRES_LIVE_PRECHECK" for item in dependencies))
        self.assertEqual("NOT_RUN", self.checklist["all_checks_status"])
        self.assertTrue(all(item["on_failure"] == "ABORT_BEFORE_POST" for item in dependencies))

    def test_idempotency_identity_hash_and_retry_policy_are_deterministic(self):
        control = self.checklist["application_idempotency"]
        self.assertEqual(self.candidate["object_id"], control["canonical_object_id"])
        self.assertEqual(json_hash(self.payload), self.checklist["payload_sha256"])
        seed = f"{self.candidate['object_id']}|{self.checklist['payload_sha256']}"
        expected = "SO-PILOT-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20].upper()
        self.assertEqual(expected, control["migration_correlation_id"])
        self.assertIn("csrf_token", control["forbidden_ledger_fields"])
        self.assertTrue(any("Never retry blindly" in rule for rule in control["safe_retry_abort_policy"]))

    def test_acceptance_gate_and_unproven_items_are_explicit(self):
        self.assertEqual({
            "deep-insert write behavior", "CREATE authorization",
            "accepted write serialization", "transaction behavior",
            "idempotency in SAP itself",
        }, set(self.checklist["unproven"]))
        self.assertEqual(
            "NO_GO_UNTIL_ALL_LIVE_PRECHECKS_PASS_AND_EXECUTION_IS_EXPLICITLY_AUTHORIZED",
            self.checklist["current_gate"],
        )
        self.assertTrue(any("HTTP 201" in item for item in self.checklist["acceptance_criteria"]["http"]))
        self.assertTrue(self.checklist["acceptance_criteria"]["get_reread"])
        self.assertTrue(self.checklist["acceptance_criteria"]["manual_va03_or_fiori"])
        self.assertTrue(self.checklist["acceptance_criteria"]["abort_failure_conditions"])

    def test_artifacts_contain_no_token_or_secret_value(self):
        payload_text = (PILOT / "sales_order_proposed_payload.json").read_text(encoding="utf-8").lower()
        candidate_text = (PILOT / "sales_order_candidate.json").read_text(encoding="utf-8").lower()
        self.assertNotIn("csrf", payload_text)
        self.assertNotIn("token", payload_text)
        self.assertNotIn("authorization", payload_text)
        self.assertNotIn("csrf", candidate_text)

    def test_artifact_generation_is_deterministic(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_phase3b0_artifacts.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)


if __name__ == "__main__":
    unittest.main()
