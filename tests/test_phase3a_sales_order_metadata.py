import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from src.sap_mapping import validate_payload_body, validate_runtime_contract
from src.sap_mapping.contracts import mapping_contracts
from src.sap_mapping.odata_metadata import parse_odata_v2_metadata


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "evidence/sap_live/odata/API_SALES_ORDER_SRV.metadata.xml"
LIVE_CONTRACT = ROOT / "schemas/sap/sales_order_live_metadata_contract.json"


class Phase3ASalesOrderMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata = parse_odata_v2_metadata(METADATA)
        cls.live = json.loads(LIVE_CONTRACT.read_text(encoding="utf-8"))
        cls.contract = mapping_contracts()["objects"]["SALES_ORDER"]
        objects = json.loads(
            (ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8")
        )["objects"]
        cls.index = {obj["object_id"]: obj for obj in objects}
        cls.ready = cls.index["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT"]

    def test_complete_metadata_identity_and_inventory(self):
        self.assertEqual("2.0", self.metadata["data_service_version"])
        self.assertEqual(self.live["external_service_name"], self.metadata["namespace"])
        self.assertEqual(self.live["evidence_sha256"], self.metadata["sha256"])
        self.assertEqual(286853, self.metadata["byte_count"])
        self.assertEqual(22, len(self.metadata["entity_types"]))
        self.assertEqual(22, len(self.metadata["entity_sets"]))
        self.assertEqual(54, self.metadata["association_count"])
        self.assertNotIn(self.live["technical_registration_name"], METADATA.read_text(encoding="utf-8"))

    def test_entity_sets_and_root_crud_capabilities(self):
        for entity_set, entity_type in self.live["entity_sets"].items():
            self.assertEqual(entity_type, self.metadata["entity_sets"][entity_set]["entity_type"])
        root = self.metadata["entity_sets"][self.live["root_entity_set"]]
        for operation in ("create", "update", "delete"):
            self.assertEqual("UNSPECIFIED", root[operation]["annotation"])
            self.assertTrue(root[operation]["metadata_effective"])

    def test_header_item_partner_and_schedule_property_facets(self):
        for entity_name, expected_properties in self.live["property_contract"].items():
            actual_properties = self.metadata["entity_types"][entity_name]["properties"]
            for property_name, expected in expected_properties.items():
                actual = actual_properties[property_name]
                observed = [
                    actual["edm_type"], actual["max_length"], actual["nullable"],
                    actual["creatable"]["metadata_effective"],
                    actual["updatable"]["metadata_effective"],
                ]
                self.assertEqual(expected, observed, f"{entity_name}.{property_name}")

    def test_navigation_targets_and_cardinality(self):
        for entity_name, navigations in self.live["navigation_contract"].items():
            actual = self.metadata["entity_types"][entity_name]["navigation_properties"]
            for navigation, expected in navigations.items():
                self.assertEqual(expected["target_type"], actual[navigation]["target_type"])
                self.assertEqual(expected["multiplicity"], actual[navigation]["multiplicity"])

    def test_every_sales_order_contract_field_is_classified(self):
        assessment = self.live["field_assessment"]
        self.assertEqual(set(self.contract["fields"]), set(assessment))
        counts = Counter(item["classification"] for item in assessment.values())
        self.assertEqual(
            {"MATCH": 14, "MISMATCH": 5, "NOT_VERIFIED": 3, "RUNTIME_ONLY": 1},
            dict(counts),
        )

    def test_corrected_mapper_uses_external_service_contract_and_valid_fields(self):
        obj = copy.deepcopy(self.ready)
        obj["data"]["ship_to_party"] = "C000000001"
        obj["data"]["items"][0].update({
            "ship_to_party": "C000000001", "route": "R001",
            "net_weight": 12.5, "net_weight_unit": "KG",
        })
        result = validate_runtime_contract(obj, object_index=self.index)
        body = result["payloads"][0]["body"]
        item = body["to_Item"][0]
        self.assertEqual("API_SALES_ORDER_SRV", self.contract["interface"])
        self.assertEqual("ZAPI_SALES_ORDER_SRV", self.contract["technical_registration"])
        self.assertEqual("API_SALES_ORDER_SRV", result["interface"]["consumer_service_name"])
        self.assertEqual("ZAPI_SALES_ORDER_SRV", result["interface"]["technical_registration_name"])
        self.assertNotIn("ShipToParty", body)
        self.assertTrue({"ShipToParty", "Route", "NetWeight", "WeightUnit"}.isdisjoint(item))
        self.assertEqual("BLOCKED", result["runtime_status"])
        self.assertEqual(5, sum(
            issue["code"] == "UNSUPPORTED_FIELD_POPULATED"
            for issue in result["contract_validation"]["issues"]
        ))

    def test_payload_schema_enforces_live_lengths_and_rejects_removed_fields(self):
        result = validate_runtime_contract(self.ready, object_index=self.index)
        self.assertEqual("EXECUTION_READY", result["runtime_status"])
        self.assertTrue(result["contract_validation"]["live_sap_metadata_validated"])
        self.assertEqual([], validate_payload_body("SALES_ORDER", result["payloads"][0]["body"]))
        too_long = copy.deepcopy(result["payloads"][0]["body"])
        too_long["DistributionChannel"] = "123"
        self.assertTrue(validate_payload_body("SALES_ORDER", too_long))
        invalid = copy.deepcopy(result["payloads"][0]["body"])
        invalid["ShipToParty"] = "C000000001"
        self.assertTrue(validate_payload_body("SALES_ORDER", invalid))


if __name__ == "__main__":
    unittest.main()
