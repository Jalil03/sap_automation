import copy
import json
import unittest
from pathlib import Path

from src.sap_mapping import (
    BlockedObjectError,
    UnsupportedObjectTypeError,
    map_canonical_object,
    supported_object_types,
)


ROOT = Path(__file__).resolve().parents[1]
TARGET_TYPES = {
    "BUSINESS_PARTNER", "MATERIAL", "SALES_ORDER", "PRICING_CONDITION",
    "OUTBOUND_DELIVERY", "BILLING",
}


class Phase2BCoreMapperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = json.loads(
            (ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8")
        )["objects"]
        cls.registry = json.loads(
            (ROOT / "mappings/sap/interface_registry.yaml").read_text(encoding="utf-8")
        )
        cls.by_type = {}
        for obj in cls.canonical:
            cls.by_type.setdefault(obj["object_type"], []).append(obj)

    def ready_fixture(self, object_type, data):
        template = copy.deepcopy(self.by_type[object_type][0])
        template.update({
            "object_id": f"TEST_{object_type}",
            "scenario_id": "TEST_PHASE2B",
            "readiness_status": "READY",
            "blocking_reasons": [],
            "placeholders": [],
            "dependencies": [],
            "data": data,
        })
        return template

    def test_supported_scope_is_exact(self):
        self.assertEqual(TARGET_TYPES, set(supported_object_types()))

    def test_registry_preferred_interfaces_drive_protocol_and_name(self):
        expected = {
            "BUSINESS_PARTNER": ("ODATA", "ZAPI_BUSINESS_PARTNER"),
            "MATERIAL": ("STANDARD_BAPI", "BAPI_MATERIAL_SAVEDATA"),
            "SALES_ORDER": ("ODATA", "ZAPI_SALES_ORDER_SRV"),
            "PRICING_CONDITION": ("ODATA", "ZSD_PRICING_CONDITIONRECORD_SRV"),
            "OUTBOUND_DELIVERY": ("ODATA", "ZAPI_OUTBOUND_DELIVERY_SRV"),
            "BILLING": ("ODATA", "ZAPI_BILLING_DOCUMENT_SRV"),
        }
        for object_type, pair in expected.items():
            preferred = self.registry["object_types"][object_type]["preferred_interface"]
            self.assertEqual(pair, (preferred["classification"], preferred["exact_name"]))

    def test_blocked_objects_require_explicit_fixture_mode(self):
        blocked = next(obj for obj in self.canonical if obj["object_type"] in TARGET_TYPES and obj["readiness_status"] == "BLOCKED")
        with self.assertRaises(BlockedObjectError):
            map_canonical_object(blocked)
        result = map_canonical_object(blocked, structural_fixture=True)
        self.assertTrue(result["structural_fixture"])
        self.assertFalse(result["execution_ready"])
        self.assertEqual("STRUCTURAL_FIXTURE", result["payload_state"])

    def test_no_mapper_for_lookup_no_execution_or_unresolved_types(self):
        for object_type in ("COMPANY_CODE", "PAYMENT_REFERENCE", "COPY_CONTROL"):
            with self.assertRaises(UnsupportedObjectTypeError):
                map_canonical_object(self.by_type[object_type][0], structural_fixture=True)

    def test_business_partner_odata_payload(self):
        obj = self.ready_fixture("BUSINESS_PARTNER", {
            "partner_id": "C1000", "grouping": "ZC01", "name": "Test Customer",
            "roles": ["FLCU00", "FLCU01"],
            "addresses": [{"city": "Hamburg", "country": "DE", "postal_code": "20111", "street": "Main street"}],
            "sales_areas": ["1010/10/00"], "currency": "EUR", "shipping_conditions": "01",
            "delivering_plant": "1010", "incoterms": "DAP", "incoterms_location": "Hamburg",
            "payment_terms": "ZB00", "account_assignment_group": "01",
            "customer_pricing_procedure": "1", "company_code": "1010",
            "reconciliation_account": "12100000", "tax_classifications": [],
            "partner_functions": [], "fax_number": None,
        })
        result = map_canonical_object(obj)
        payloads = result["payloads"]
        body = payloads[0]["body"]
        self.assertEqual("ZAPI_BUSINESS_PARTNER", result["interface"]["exact_name"])
        self.assertEqual(
            [
                "A_BusinessPartner", "A_BusinessPartnerRole", "A_BusinessPartnerRole",
                "A_CustomerCompany", "A_CustomerSalesArea",
            ],
            [payload["entity_set"] for payload in payloads],
        )
        self.assertEqual("C1000", body["BusinessPartner"])
        self.assertEqual("Test Customer", body["OrganizationBPName1"])
        self.assertNotIn("BusinessPartnerFullName", body)
        self.assertFalse(any(key.startswith("to_") for key in body))
        self.assertNotIn("A_Customer", [payload["entity_set"] for payload in payloads])
        sales_area = payloads[-1]["body"]
        self.assertEqual("00", sales_area["Division"])
        self.assertEqual("01", sales_area["CustomerAccountAssignmentGroup"])
        self.assertFalse(result["execution_ready"])
        self.assertIn(
            "data.addresses.sequential_create_contract",
            result["missing_required_mappings"],
        )

    def test_material_bapi_payload_and_update_flags(self):
        obj = self.ready_fixture("MATERIAL", {
            "material_id": "P100", "description": "Test product", "base_unit": "PC",
            "plants": ["1010", "1020"], "industry_sector": "M", "material_type": "HAWA",
            "sales_organization": "1010", "distribution_channel": "10", "tax_classification": "1",
            "minimum_order_quantity": 10, "minimum_order_unit": "PC", "sales_text": None,
            "availability_check": "02", "delivering_plant": "1010", "strategy_group": None,
            "item_category_group": "NORM",
        })
        result = map_canonical_object(obj)
        self.assertEqual("BAPI", result["protocol"])
        self.assertEqual(2, len(result["payloads"]))
        first = result["payloads"][0]["body"]
        self.assertEqual("P100", first["HEADDATA"]["MATERIAL"])
        self.assertEqual("X", first["CLIENTDATAX"]["BASE_UOM"])
        self.assertEqual("1010", first["PLANTDATA"]["PLANT"])
        self.assertTrue(result["execution_ready"])

    def test_sales_order_ready_payload_is_concrete(self):
        obj = next(o for o in self.by_type["SALES_ORDER"] if o["readiness_status"] == "READY")
        result = map_canonical_object(obj)
        body = result["payloads"][0]["body"]
        self.assertEqual("ZAPI_SALES_ORDER_SRV", result["interface"]["exact_name"])
        self.assertEqual("C615-A00", body["SoldToParty"])
        self.assertEqual("P615-100", body["to_Item"][0]["Material"])
        self.assertTrue(result["execution_ready"])
        self.assertEqual("CONCRETE", result["payload_state"])

    def test_pricing_condition_quantity_scales(self):
        obj = self.ready_fixture("PRICING_CONDITION", {
            "condition_type": "PR00",
            "key_combination": {"sales_organization": "1010", "distribution_channel": "10", "customer": "C1000", "material": "P100"},
            "valid_from": None, "valid_to": None, "rate": None, "currency": "EUR", "pricing_unit": 1,
            "scales": [
                {"scale_basis": "QUANTITY", "threshold": 1, "threshold_unit": "PC", "amount": 53, "currency": "EUR", "pricing_unit": 1},
                {"scale_basis": "QUANTITY", "threshold": 10, "threshold_unit": "PC", "amount": 51, "currency": "EUR", "pricing_unit": 1},
            ],
            "scale_basis": "QUANTITY", "rate_unit": None, "calculation_semantics": None,
            "record_status": "ACTIVE", "source_operation": "CREATE", "adjustment_percent": None,
            "maximum_order_count": None, "maximum_quantity": None, "maximum_quantity_unit": None,
            "deletion_indicator": False,
        })
        result = map_canonical_object(obj)
        scales = result["payloads"][0]["body"]["to_PricingScale"]
        self.assertEqual([1, 10], [row["ConditionScaleValue"] for row in scales])
        self.assertEqual([53, 51], [row["ConditionRateValue"] for row in scales])
        self.assertTrue(result["execution_ready"])

    def test_ready_dependency_objects_are_templates_not_fabricated_documents(self):
        for object_type, sap_field in (("OUTBOUND_DELIVERY", "ReferenceSDDocument"), ("BILLING", "ReferenceSDDocument")):
            obj = next(o for o in self.by_type[object_type] if o["readiness_status"] == "READY")
            result = map_canonical_object(obj)
            self.assertFalse(result["execution_ready"])
            self.assertEqual("TEMPLATE", result["payload_state"])
            self.assertTrue(any(binding["sap_field"] == sap_field for binding in result["runtime_bindings"]))
            self.assertNotIn(sap_field, result["payloads"][0]["body"])

    def test_mapping_is_deterministic(self):
        obj = next(o for o in self.by_type["SALES_ORDER"] if o["readiness_status"] == "READY")
        original = copy.deepcopy(obj)
        first = map_canonical_object(obj)
        second = map_canonical_object(copy.deepcopy(obj))
        self.assertEqual(original, obj)
        self.assertEqual(first, second)
        self.assertEqual(
            json.dumps(first, sort_keys=True, ensure_ascii=False),
            json.dumps(second, sort_keys=True, ensure_ascii=False),
        )

    def test_nonpayload_business_state_is_retained_explicitly(self):
        obj = next(o for o in self.by_type["BILLING"] if o["readiness_status"] == "READY")
        result = map_canonical_object(obj)
        retained_paths = {entry["canonical_path"] for entry in result["retained_nonpayload_fields"]}
        self.assertIn("data.billing_status", retained_paths)
        self.assertIn("data.fi_co_dependencies", retained_paths)

    def test_mapping_package_has_no_connector_module(self):
        files = {path.name for path in (ROOT / "src/sap_mapping").glob("*.py")}
        self.assertNotIn("connector.py", files)
        source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src/sap_mapping").glob("*.py"))
        for forbidden in ("import requests", "from requests", "import urllib", "import socket", "http.client", "sapgui"):
            self.assertNotIn(forbidden, source.lower())


if __name__ == "__main__":
    unittest.main()
