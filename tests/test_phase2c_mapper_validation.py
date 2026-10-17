import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from src.sap_mapping import (
    PayloadValidationError,
    validate_payload_body,
    validate_runtime_contract,
)
from src.sap_mapping.contracts import mapping_contracts


ROOT = Path(__file__).resolve().parents[1]


def schema_leaf_paths(properties, contract_fields, prefix=""):
    paths = set()
    for name, schema in properties.items():
        path = f"{prefix}.{name}" if prefix else name
        if path in contract_fields:
            paths.add(path)
            continue
        if schema.get("properties"):
            paths |= schema_leaf_paths(schema["properties"], contract_fields, path)
            continue
        items = schema.get("items", {})
        if items.get("properties"):
            paths |= schema_leaf_paths(items["properties"], contract_fields, path + "[]")
            continue
        paths.add(path)
    return paths


class Phase2CMapperValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.objects = json.loads(
            (ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8")
        )["objects"]
        cls.index = {obj["object_id"]: obj for obj in cls.objects}
        cls.contracts = mapping_contracts()
        cls.ready_sales = cls.index["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT"]
        cls.ready_delivery = cls.index["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_OUTBOUND_DELIVERY_INSTALLMENT"]
        cls.ready_billing = cls.index["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_BILLING_INSTALLMENT"]

    def validate(self, obj, **kwargs):
        return validate_runtime_contract(obj, object_index=self.index, **kwargs)

    def issue_codes(self, result):
        return {issue["code"] for issue in result["contract_validation"]["issues"]}

    def test_every_canonical_field_has_exactly_one_disposition(self):
        schema_index = json.loads((ROOT / "schemas/index.json").read_text(encoding="utf-8"))
        allowed = set(self.contracts["dispositions"])
        for object_type, contract in self.contracts["objects"].items():
            schema = json.loads((ROOT / schema_index[object_type]["schema"]).read_text(encoding="utf-8"))
            actual = schema_leaf_paths(schema["properties"]["data"]["properties"], set(contract["fields"]))
            self.assertEqual(actual, set(contract["fields"]), object_type)
            self.assertTrue(all(field["disposition"] in allowed for field in contract["fields"].values()))

    def test_contract_interfaces_equal_registry_preferences(self):
        registry = json.loads((ROOT / "mappings/sap/interface_registry.yaml").read_text(encoding="utf-8"))
        for object_type, contract in self.contracts["objects"].items():
            preferred = registry["object_types"][object_type]["preferred_interface"]
            expected_interface = (
                preferred["external_name"]
                if contract.get("live_metadata_validation", {}).get("status") == "VALIDATED"
                else preferred["exact_name"]
            )
            self.assertEqual(contract["interface"], expected_interface)
            if "technical_registration" in contract:
                self.assertEqual(contract["technical_registration"], preferred["exact_name"])
            expected_protocol = "BAPI" if preferred["classification"] == "STANDARD_BAPI" else preferred["classification"]
            self.assertEqual(contract["protocol"], expected_protocol)

    def test_core_chain_runtime_states_and_bindings(self):
        sales = self.validate(self.ready_sales)
        delivery = self.validate(self.ready_delivery)
        billing = self.validate(self.ready_billing)
        self.assertEqual("EXECUTION_READY", sales["runtime_status"])
        self.assertEqual("RUNTIME_BINDING_REQUIRED", delivery["runtime_status"])
        self.assertEqual("BLOCKED", billing["runtime_status"])
        delivery_binding = delivery["runtime_bindings"][0]
        billing_binding = billing["runtime_bindings"][0]
        self.assertEqual(self.ready_sales["object_id"], delivery_binding["target_object_id"])
        self.assertEqual(self.ready_delivery["object_id"], billing_binding["target_object_id"])
        self.assertIn("UNSUPPORTED_FIELD_POPULATED", self.issue_codes(billing))

    def test_invalid_value_type_fails_deterministically(self):
        obj = copy.deepcopy(self.ready_sales)
        obj["data"]["items"][0]["quantity"] = "ten"
        first = self.validate(obj)
        second = self.validate(copy.deepcopy(obj))
        self.assertEqual(first["contract_validation"], second["contract_validation"])
        self.assertEqual("BLOCKED", first["runtime_status"])
        self.assertIn("CANONICAL_SCHEMA_INVALID", self.issue_codes(first))
        self.assertIn("PAYLOAD_SCHEMA_INVALID", self.issue_codes(first))

    def test_placeholder_unresolved_dependency_and_missing_field_block(self):
        cases = []
        placeholder = copy.deepcopy(self.ready_sales)
        placeholder["placeholders"] = [{
            "raw": "##", "resolved": None, "status": "UNRESOLVED",
            "mandatory": True, "field_path": "data.sold_to_party",
        }]
        cases.append((placeholder, "UNRESOLVED_PLACEHOLDER"))

        dependency = copy.deepcopy(self.ready_sales)
        dependency["dependencies"].append({
            "relation": "PRICED_BY", "target_type": "PRICING_CONDITION", "target_id": None,
            "status": "UNRESOLVED", "critical": True, "source_phrase": "previous condition",
        })
        cases.append((dependency, "UNRESOLVED_CRITICAL_DEPENDENCY"))

        missing = copy.deepcopy(self.ready_sales)
        missing["data"]["order_type"] = None
        cases.append((missing, "MISSING_MANDATORY_FIELD"))

        for obj, code in cases:
            result = self.validate(obj)
            self.assertEqual("BLOCKED", result["runtime_status"])
            self.assertIn(code, self.issue_codes(result))

    def test_populated_unsupported_field_blocks(self):
        obj = copy.deepcopy(self.ready_sales)
        obj["data"]["pricing_elements"] = [{"condition_type": "PR00"}]
        result = self.validate(obj)
        self.assertEqual("BLOCKED", result["runtime_status"])
        self.assertIn("UNSUPPORTED_FIELD_POPULATED", self.issue_codes(result))

    def test_payload_validator_rejects_unknown_fields_and_bad_types(self):
        result = self.validate(self.ready_sales)
        body = copy.deepcopy(result["payloads"][0]["body"])
        body["InventedSAPField"] = "not allowed"
        issues = validate_payload_body("SALES_ORDER", body)
        self.assertTrue(issues)
        with self.assertRaises(PayloadValidationError):
            validate_payload_body("SALES_ORDER", body, raise_on_error=True)

        material_body = {
            "HEADDATA": {"MATERIAL": "P100", "IND_SECTOR": "M", "MATL_TYPE": "HAWA"},
            "CLIENTDATA": {"BASE_UOM": 123},
        }
        self.assertTrue(validate_payload_body("MATERIAL", material_body))

    def test_blocked_raise_mode_is_structured_and_stable(self):
        obj = copy.deepcopy(self.ready_sales)
        obj["data"]["order_type"] = None
        with self.assertRaises(PayloadValidationError) as first:
            self.validate(obj, raise_on_blocked=True)
        with self.assertRaises(PayloadValidationError) as second:
            self.validate(copy.deepcopy(obj), raise_on_blocked=True)
        self.assertEqual(str(first.exception), str(second.exception))

    def test_blocked_canonical_objects_are_fixture_only(self):
        obj = next(o for o in self.objects if o["object_type"] == "BUSINESS_PARTNER" and o["readiness_status"] == "BLOCKED")
        result = self.validate(obj, structural_fixture=True)
        self.assertEqual("BLOCKED", result["runtime_status"])
        self.assertFalse(result["execution_ready"])

    def test_coverage_and_snapshots_are_deterministic(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_phase2c_artifacts.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)
        coverage = json.loads((ROOT / "reports/phase2c_mapping_coverage.json").read_text(encoding="utf-8"))
        self.assertEqual(129, coverage["totals"]["canonical_object_count"])
        self.assertEqual(138, coverage["totals"]["field_count"])
        snapshots = json.loads((ROOT / "tests/snapshots/phase2c_core_payloads.json").read_text(encoding="utf-8"))
        self.assertEqual(6, len(snapshots["snapshots"]))

    def test_contract_does_not_claim_live_sap_validation(self):
        self.assertFalse(self.contracts["live_sap_metadata_validated"])
        coverage = json.loads((ROOT / "reports/phase2c_mapping_coverage.json").read_text(encoding="utf-8"))
        self.assertFalse(coverage["live_sap_metadata_validated"])


if __name__ == "__main__":
    unittest.main()
