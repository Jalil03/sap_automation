import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

from src.sap_mapping import validate_runtime_contract
from src.sap_mapping.contracts import mapping_contracts
from src.sap_mapping.odata_metadata import parse_odata_v2_metadata
from src.sap_mapping.odata_runtime import load_odata_v2_results, parse_entity_identity


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "evidence/sap_live/runtime"
EVIDENCE_CONTRACT = ROOT / "schemas/sap/sales_order_runtime_evidence_contract.json"
RESPONSE_SCHEMA = ROOT / "schemas/sap/sales_order_runtime_response.schema.json"
METADATA = ROOT / "evidence/sap_live/odata/API_SALES_ORDER_SRV.metadata.xml"

FILES = {
    "sales_order_sample.json": ("root_response", "A_SalesOrderType"),
    "sales_order_partners_sample.json": ("partner_response", "A_SalesOrderHeaderPartnerType"),
    "sales_order_items_sample.json": ("item_response", "A_SalesOrderItemType"),
    "sales_order_schedule_lines_sample.json": ("schedule_line_response", "A_SalesOrderScheduleLineType"),
}


class Phase3A2SalesOrderRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(EVIDENCE_CONTRACT.read_text(encoding="utf-8"))
        cls.response_schema = json.loads(RESPONSE_SCHEMA.read_text(encoding="utf-8"))
        cls.metadata = parse_odata_v2_metadata(METADATA)
        cls.results = {
            name: load_odata_v2_results(RUNTIME_DIR / name) for name in FILES
        }

    def test_evidence_hashes_and_counts_are_pinned(self):
        for name, expected in self.contract["evidence"].items():
            content = (RUNTIME_DIR / name).read_bytes()
            self.assertEqual(expected["sha256"], hashlib.sha256(content).hexdigest())
            self.assertEqual(expected["record_count"], len(self.results[name]))

    def test_all_captures_match_strict_read_response_schemas(self):
        for name, (schema_name, _) in FILES.items():
            value = json.loads((RUNTIME_DIR / name).read_text(encoding="utf-8"))
            schema = {
                "$schema": self.response_schema["$schema"],
                "$ref": f"#/$defs/{schema_name}",
                "$defs": self.response_schema["$defs"],
            }
            errors = list(Draft202012Validator(schema).iter_errors(value))
            self.assertEqual([], errors, name)

    def test_entity_types_fields_and_json_values_match_metadata(self):
        for name, (_, entity_name) in FILES.items():
            metadata_properties = self.metadata["entity_types"][entity_name]["properties"]
            for record in self.results[name]:
                self.assertEqual(
                    f"API_SALES_ORDER_SRV.{entity_name}", record["__metadata"]["type"]
                )
                for field, value in record.items():
                    if field == "__metadata":
                        continue
                    self.assertIn(field, metadata_properties)
                    edm_type = metadata_properties[field]["edm_type"]
                    if value is None:
                        self.assertTrue(metadata_properties[field]["nullable"])
                    elif edm_type in {"Edm.String", "Edm.Decimal", "Edm.DateTime"}:
                        self.assertIsInstance(value, str)

    def test_runtime_entity_sets_and_key_formatting(self):
        root = parse_entity_identity(self.results["sales_order_sample.json"][0]["__metadata"]["uri"])
        item = parse_entity_identity(self.results["sales_order_items_sample.json"][0]["__metadata"]["uri"])
        schedule = [
            parse_entity_identity(row["__metadata"]["uri"])
            for row in self.results["sales_order_schedule_lines_sample.json"]
        ]
        self.assertEqual({"entity_set": "A_SalesOrder", "keys": {"$value": "1"}}, {k: root[k] for k in ("entity_set", "keys")})
        self.assertEqual("A_SalesOrderItem", item["entity_set"])
        self.assertEqual({"SalesOrder": "1", "SalesOrderItem": "10"}, item["keys"])
        self.assertEqual(["1", "2"], [entry["keys"]["ScheduleLine"] for entry in schedule])
        self.assertTrue(all(entry["keys"]["SalesOrder"] == "1" for entry in schedule))
        self.assertTrue(all(entry["keys"]["SalesOrderItem"] == "10" for entry in schedule))

    def test_runtime_relationship_keys_align_with_metadata_navigation(self):
        header = self.metadata["entity_types"]["A_SalesOrderType"]["navigation_properties"]
        item_nav = self.metadata["entity_types"]["A_SalesOrderItemType"]["navigation_properties"]
        self.assertEqual("API_SALES_ORDER_SRV.A_SalesOrderHeaderPartnerType", header["to_Partner"]["target_type"])
        self.assertEqual("API_SALES_ORDER_SRV.A_SalesOrderItemType", header["to_Item"]["target_type"])
        self.assertEqual("API_SALES_ORDER_SRV.A_SalesOrderScheduleLineType", item_nav["to_ScheduleLine"]["target_type"])
        partner_keys = [parse_entity_identity(row["__metadata"]["uri"])["keys"] for row in self.results["sales_order_partners_sample.json"]]
        self.assertTrue(all(keys["SalesOrder"] == "1" for keys in partner_keys))

    def test_partner_codes_are_observed_without_semantic_inference(self):
        partners = self.results["sales_order_partners_sample.json"]
        self.assertEqual({"DO", "PY", "RF", "RM"}, {row["PartnerFunction"] for row in partners})
        self.assertEqual({"17100002"}, {row["Customer"] for row in partners})
        self.assertFalse(self.contract["observed_partner_values"]["business_semantics_verified"])
        self.assertEqual("NOT_VERIFIED", self.contract["assessments"]["partner_business_semantics"]["classification"])

    def test_decimal_date_null_unit_and_etag_representations(self):
        item = self.results["sales_order_items_sample.json"][0]
        schedules = self.results["sales_order_schedule_lines_sample.json"]
        root = self.results["sales_order_sample.json"][0]
        self.assertEqual("1", item["RequestedQuantity"])
        self.assertEqual("289", item["RequestedQuantityUnit"])
        self.assertEqual(["1", "0"], [row["ScheduleLineOrderQuantity"] for row in schedules])
        self.assertEqual(["289", "289"], [row["OrderQuantityUnit"] for row in schedules])
        self.assertEqual("/Date(1756857600000)/", schedules[0]["RequestedDeliveryDate"])
        self.assertIsNone(schedules[1]["RequestedDeliveryDate"])
        self.assertTrue(root["__metadata"]["etag"].startswith('W/"datetimeoffset'))
        self.assertTrue(all("etag" not in row["__metadata"] for name in FILES if name != "sales_order_sample.json" for row in self.results[name]))

    def test_assessment_matrix_is_complete_and_uses_only_allowed_classes(self):
        counts = Counter(item["classification"] for item in self.contract["assessments"].values())
        self.assertEqual(
            {"RUNTIME_CONFIRMED": 19, "NOT_VERIFIED": 8, "METADATA_ONLY": 2, "MATCH": 1},
            dict(counts),
        )
        self.assertNotIn("MISMATCH", counts)

    def test_get_serialization_does_not_change_write_mapper_contract(self):
        contracts = mapping_contracts()
        sales_contract = contracts["objects"]["SALES_ORDER"]
        self.assertEqual("CAPTURED_GET_RESPONSES_ONLY", sales_contract["read_runtime_validation"]["scope"])
        objects = json.loads((ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8"))["objects"]
        index = {obj["object_id"]: obj for obj in objects}
        obj = index["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT"]
        result = validate_runtime_contract(obj, object_index=index)
        self.assertIsInstance(result["payloads"][0]["body"]["to_Item"][0]["RequestedQuantity"], (int, float))
        self.assertEqual("EXECUTION_READY", result["runtime_status"])


if __name__ == "__main__":
    unittest.main()
