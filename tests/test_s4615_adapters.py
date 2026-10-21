import json
import unittest
from unittest.mock import patch

from src.provisioning.customer_bp_root import (
    assess_bp_root_identity_readback, capture_generated_bp_id, generated_bp_readback_keys, inspect_creation_metadata,
    inspect_root_metadata, prepare_bp_root, verify_generated_bp_readback,
)
from src.provisioning.product_creation import prepare_material_bapi, prepare_mm01_fallback
from src.provisioning.s4615_customizing import prepare_customizing_contract
from src.provisioning.s4615_implementation import build_dry_run
from src.sap_runtime.transport import HttpResponse


METADATA = '''<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx"
 xmlns:edm="http://schemas.microsoft.com/ado/2008/09/edm"
 xmlns:sap="http://www.sap.com/Protocols/SAPData">
 <edmx:DataServices><edm:Schema Namespace="API">
 <edm:EntityType Name="A_BusinessPartnerType">
 <edm:Property Name="BusinessPartner" Type="Edm.String" MaxLength="10" sap:creatable="false" />
 <edm:Property Name="BusinessPartnerGrouping" Type="Edm.String" MaxLength="4" />
 <edm:Property Name="BusinessPartnerCategory" Type="Edm.String" MaxLength="1" />
 <edm:Property Name="OrganizationBPName1" Type="Edm.String" MaxLength="40" />
 <edm:Property Name="SearchTerm1" Type="Edm.String" MaxLength="20" />
 <edm:Property Name="Language" Type="Edm.String" MaxLength="2" />
 <edm:Property Name="BusinessPartnerFullName" Type="Edm.String" sap:creatable="false" />
 </edm:EntityType><edm:EntityContainer Name="Container">
 <edm:EntitySet Name="A_BusinessPartner" EntityType="API.A_BusinessPartnerType" sap:creatable="true" />
 </edm:EntityContainer></edm:Schema></edmx:DataServices></edmx:Edmx>'''


class S4615AdapterTests(unittest.TestCase):
    def test_bp_root_internal_numbering_and_metadata_allowlist(self):
        self.assertTrue(inspect_root_metadata(METADATA)["metadata_allows_create"])
        result = prepare_bp_root({"bp_grouping": "BPAB", "bp_category": "2",
                                  "training_name": "S4615 Training Customer",
                                  "duplicate_key": "C615-A01"}, METADATA)
        self.assertEqual("PAYLOAD_PREPARED", result["status"])
        self.assertFalse(result["write_route_ready"])
        self.assertEqual({"BusinessPartnerGrouping": "BPAB", "BusinessPartnerCategory": "2",
                          "OrganizationBPName1": "S4615 Training Customer",
                          "SearchTerm1": "C615-A01"}, result["payload"])
        self.assertNotIn("BusinessPartner", result["payload"])

    def test_exact_belgian_a01_candidate_keeps_later_fields_out_of_root(self):
        values = {"logical_id": "C615-A01", "bp_grouping": "BPAB", "bp_category": "2",
                  "training_name": "S4615 Training Customer A01", "duplicate_key": "C615-A01",
                  "country": "BE", "language": "EN", "sales_currency": "EUR"}
        result = prepare_bp_root(values, METADATA)
        self.assertTrue(result["data_ready"])
        self.assertFalse(result["write_route_ready"])
        self.assertEqual({
            "BusinessPartnerGrouping": "BPAB", "BusinessPartnerCategory": "2",
            "OrganizationBPName1": "S4615 Training Customer A01",
            "SearchTerm1": "C615-A01", "Language": "EN",
        }, result["payload"])
        self.assertEqual("BE", result["later_extensions"]["address"]["Country"])
        self.assertEqual("EUR", result["later_extensions"]["sales_area"]["Currency"])
        self.assertNotIn("Country", result["payload"])
        self.assertNotIn("Currency", result["payload"])
        self.assertEqual("SearchTerm1 eq 'C615-A01'",
                         result["duplicate_checks"]["project_marker"])
        self.assertEqual("BLOCKED_DATA", prepare_bp_root(
            {**values, "duplicate_key": "OTHER"}, METADATA)["status"])

    def test_bp_root_rejects_unproven_fields_and_missing_metadata(self):
        values = {"bp_grouping": "BPAB", "bp_category": "2", "training_name": "Training",
                  "duplicate_key": "C615-A01"}
        self.assertEqual("BLOCKED_METADATA", prepare_bp_root(values, None)["status"])
        self.assertEqual("BLOCKED_CONTRACT", prepare_bp_root(
            {**values, "business_partner": "C615-A01"}, METADATA)["status"])
        self.assertEqual("BLOCKED_DATA", prepare_bp_root(
            {**values, "training_name": "X" * 41}, METADATA)["status"])
        self.assertEqual("BLOCKED_CONTRACT", prepare_bp_root(
            values, METADATA.replace('Name="OrganizationBPName1" Type="Edm.String"',
                                     'Name="OrganizationBPName1" Type="Edm.String" sap:creatable="false"'))["status"])

    def test_absent_creatable_annotation_is_not_a_post_authorization(self):
        metadata = METADATA.replace(' sap:creatable="true" />', ' />')
        result = inspect_root_metadata(metadata)
        self.assertIsNone(result["create_annotation"])
        self.assertTrue(result["metadata_allows_create"])
        self.assertFalse(prepare_bp_root({"bp_grouping": "BPAB", "bp_category": "2",
                                          "training_name": "Training", "duplicate_key": "C615-A01"},
                                         metadata)["write_route_ready"])

    def test_metadata_distinguishes_noncreatable_customer_root(self):
        metadata = METADATA.replace('</edm:EntityType><edm:EntityContainer',
            '</edm:EntityType><edm:EntityType Name="A_CustomerType">'
            '<edm:Property Name="Customer" Type="Edm.String" Nullable="false" />'
            '</edm:EntityType><edm:EntityContainer')
        metadata = metadata.replace('</edm:EntityContainer>',
            '<edm:EntitySet Name="A_Customer" EntityType="API.A_CustomerType" '
            'sap:creatable="false" /></edm:EntityContainer>')
        contracts = inspect_creation_metadata(metadata, entities=("A_BusinessPartner", "A_Customer"))
        self.assertTrue(contracts["A_BusinessPartner"]["metadata_allows_create"])
        self.assertFalse(contracts["A_Customer"]["metadata_allows_create"])

    def test_generated_bp_capture_and_independent_readback_keys(self):
        response = HttpResponse(201, {}, json.dumps({"d": {"BusinessPartner": "1000001234"}}).encode())
        sap_id = capture_generated_bp_id(response)
        keys = generated_bp_readback_keys(sap_id)
        self.assertEqual("A_BusinessPartner('1000001234')", keys["root"])
        self.assertIn("FLCU00", keys["flcu00"])
        expected = {"BusinessPartnerGrouping": "BPAB", "SearchTerm1": "C615-A01"}
        readback = HttpResponse(200, {}, json.dumps({"d": {
            "BusinessPartner": sap_id, **expected}}).encode())
        self.assertTrue(verify_generated_bp_readback(readback, sap_id, expected))
        self.assertFalse(verify_generated_bp_readback(readback, "OTHER", expected))
        for bad in (HttpResponse(400, {}, response.body), HttpResponse(201, {}, b'{"d":{}}')):
            with self.assertRaises(ValueError):
                capture_generated_bp_id(bad)
        with self.assertRaises(ValueError):
            generated_bp_readback_keys("1'23")

    def test_optional_root_language_mismatch_is_recorded_not_silently_ignored(self):
        expected = {"BusinessPartnerGrouping": "BPAB", "BusinessPartnerCategory": "2",
                    "OrganizationBPName1": "S4615 Training Customer A01",
                    "SearchTerm1": "C615-A01", "Language": "EN"}
        actual = {"BusinessPartner": "1000000115", **expected, "Language": ""}
        response = HttpResponse(200, {}, json.dumps({"d": actual}).encode())
        result = assess_bp_root_identity_readback(response, "1000000115", expected, METADATA)
        self.assertTrue(result["verified"])
        self.assertEqual("", result["observed_language"])
        self.assertEqual({"expected": "EN", "observed": ""}, result["optional_mismatches"]["Language"])
        self.assertEqual({}, result["mandatory_mismatches"])
        actual["SearchTerm1"] = "OTHER"
        broken = HttpResponse(200, {}, json.dumps({"d": actual}).encode())
        self.assertFalse(assess_bp_root_identity_readback(broken, "1000000115", expected, METADATA)["verified"])

    def test_contract_preparation_never_calls_sap(self):
        values = {"bp_grouping": "BPAB", "bp_category": "2",
                  "training_name": "S4615 Training Customer A01", "duplicate_key": "C615-A01"}
        with patch("src.sap_runtime.transport.UrllibSapTransport.request",
                   side_effect=AssertionError("network call forbidden")) as request:
            result = prepare_bp_root(values, METADATA)
            self.assertEqual("PAYLOAD_PREPARED", result["status"])
            self.assertFalse(result["write_route_ready"])
            request.assert_not_called()

    def test_bp_root_has_no_ovl2_dependency_and_readiness_is_independent(self):
        root = build_dry_run()["steps"][4]
        self.assertEqual("S4615_CUSTOMER_BP_ROOT", root["operation"])
        self.assertEqual([], root["depends_on"])
        self.assertEqual({"DATA_READY": True, "WRITE_ROUTE_READY": False,
                          "EXECUTION_AUTHORIZED": False}, root["readiness"])

    def test_data_ready_does_not_imply_write_route_or_authorization(self):
        root = build_dry_run(decisions={"S4615_CUSTOMER_BP_ROOT": {
            "bp_grouping": "BPAB", "bp_category": "2",
            "training_name": "S4615 Training Customer", "duplicate_key": "S4615-C615-A01",
        }})["steps"][4]
        self.assertEqual({"DATA_READY": True, "WRITE_ROUTE_READY": False,
                          "EXECUTION_AUTHORIZED": False}, root["readiness"])
        self.assertEqual("BLOCKED", root["status"])

    def test_bapi_is_candidate_only_without_installed_signature_and_valuation_contract(self):
        values = {"sap_material_id": "P615-101", "material_type": "FERT",
                  "industry_sector": "M", "base_unit": "PC", "sales_organization": "1010",
                  "distribution_channel": "10", "plant": "P101", "valuation_class": "7920",
                  "price_control": "S", "price_determination": "2", "standard_price": "27.19",
                  "valuation_currency": "EUR"}
        result = prepare_material_bapi(values)
        self.assertEqual("BAPI_MATERIAL_SAVEDATA", result["interface"])
        self.assertFalse(result["write_route_ready"])
        self.assertEqual("P615-101", result["payloads"][0]["body"]["HEADDATA"]["MATERIAL"])
        self.assertIn("INSTALLED_BAPI_SIGNATURE_REQUIRED", [b["code"] for b in result["blockers"]])
        self.assertIn("VALUATION_MAPPER_CONTRACT_REQUIRED", [b["code"] for b in result["blockers"]])
        with self.assertRaises(ValueError):
            prepare_material_bapi({**values, "plant": "1710"})

    def test_mm01_fallback_is_not_silently_ready(self):
        self.assertFalse(prepare_mm01_fallback()["write_route_ready"])
        complete = {key: ["observed"] for key in (
            "lookup_controls", "create_controls", "plant_view_controls",
            "accounting_view_controls", "save_controls", "readback_controls")}
        self.assertFalse(prepare_mm01_fallback(captured_contract=complete)["write_route_ready"])

    def test_customizing_routes_are_read_only_contracts_with_exact_keys(self):
        cases = (
            ("S4615_TRAINING_PLANT", {"plant": "P101", "company_code": "1010", "valuation_area": "P101"}, "T001W"),
            ("S4615_SALES_CHANNEL_PLANT", {"sales_organization": "1010", "distribution_channel": "10", "plant": "P101"}, "TVKWZ"),
            ("S4615_PLANT_SHIPPING_POINT", {"plant": "P101", "shipping_point": "1010"}, "TVSWZ"),
            ("S4615_OVL2_DETERMINATION", {"shipping_condition": "01", "loading_group": "0001", "plant": "P101", "shipping_point": "1010"}, "OVL2"),
        )
        for operation, target, expected in cases:
            with self.subTest(operation=operation):
                result = prepare_customizing_contract(operation, target)
                self.assertFalse(result["write_route_ready"])
                self.assertTrue(result["lookup_before_write"])
                self.assertTrue(result["independent_readback"])
                self.assertIn(expected, str(result["read_contract"]))
        with self.assertRaises(ValueError):
            prepare_customizing_contract("S4615_TRAINING_PLANT", {"plant": "1710"})


if __name__ == "__main__":
    unittest.main()
