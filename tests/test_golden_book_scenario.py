import hashlib
import json
import unittest
from pathlib import Path

from src.golden_book import build_golden_book_scenario
from src.golden_book.scenario import CANONICAL_PATH
from src.training_context import InvalidTrainingUserCode


ROOT = Path(__file__).resolve().parents[1]
OBJECT_ID = "S4615_CH4_EX5_SALES_ORDER_CASH_SALE"


class GoldenBookScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical_bytes = CANONICAL_PATH.read_bytes()
        cls.canonical = json.loads(cls.canonical_bytes.decode("utf-8"))
        cls.result = build_golden_book_scenario("07")

    def test_existing_canonical_object_is_reused_once(self):
        matches = [
            item for item in self.canonical["objects"] if item["object_id"] == OBJECT_ID
        ]
        self.assertEqual(1, len(matches))
        self.assertEqual(OBJECT_ID, self.result["source"]["canonical_object_id"])
        self.assertEqual("S4615_CH4_EX5", matches[0]["scenario_id"])

    def test_source_identity_pages_and_original_values(self):
        source = self.result["source"]
        self.assertEqual("S4615", source["course_code"])
        self.assertEqual(4, source["chapter"])
        self.assertEqual(5, source["exercise"])
        self.assertEqual(73, source["exercise_page"])
        self.assertEqual(75, source["solution_page"])
        self.assertEqual({
            "training_user": "S4615-##",
            "sales_order_type": "BV",
            "sales_organization": "1010",
            "distribution_channel": "10",
            "organization_division": "00",
            "sold_to_party": "C615-D##",
            "customer_reference": "##S4615-BV",
            "material": "P615-4##",
            "quantity": 1,
            "unit": "PC",
        }, self.result["original_book_data"])

    def test_training_user_07_runtime_values(self):
        runtime = self.result["runtime_data"]
        self.assertEqual("S4615-07", runtime["training_user"])
        self.assertEqual("C615-D07", runtime["sold_to_party"])
        self.assertEqual("07S4615-BV", runtime["customer_reference"])
        self.assertEqual("P615-407", runtime["material"])
        self.assertNotIn("##", json.dumps(runtime, ensure_ascii=False))

    def test_canonical_is_byte_for_byte_immutable(self):
        self.assertEqual(self.canonical_bytes, CANONICAL_PATH.read_bytes())
        self.assertEqual(
            hashlib.sha256(self.canonical_bytes).hexdigest(),
            hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest(),
        )

    def test_extracted_workflow_has_both_supported_branches(self):
        workflow = self.result["workflow"]
        self.assertEqual(5, len(workflow["nodes"]))
        self.assertEqual(4, len(workflow["edges"]))
        cash = [node["object_type"] for node in workflow["nodes"] if node["branch"] == "CASH_SALE"]
        pro_forma = [node["object_type"] for node in workflow["nodes"] if node["branch"] == "PRO_FORMA"]
        self.assertEqual(["SALES_ORDER", "OUTBOUND_DELIVERY", "BILLING"], cash)
        self.assertEqual(["SALES_ORDER", "BILLING"], pro_forma)
        self.assertTrue(all(edge["status"] == "RESOLVED" for edge in workflow["edges"]))

    def test_sap_mapping_is_source_derived_and_locally_ready(self):
        mapping = self.result["sap_mapping"]
        self.assertEqual("API_SALES_ORDER_SRV", mapping["service"])
        self.assertEqual("A_SalesOrder", mapping["entity_set"])
        self.assertEqual("EXECUTION_READY", mapping["local_runtime_status"])
        self.assertTrue(mapping["local_contract_valid"])
        payload = mapping["offline_payload_preview"]
        self.assertEqual("BV", payload["SalesOrderType"])
        self.assertEqual("C615-D07", payload["SoldToParty"])
        self.assertEqual("07S4615-BV", payload["PurchaseOrderByCustomer"])
        self.assertEqual("P615-407", payload["to_Item"][0]["Material"])
        rendered = json.dumps(mapping, ensure_ascii=False)
        self.assertNotIn("148", rendered)
        self.assertNotIn("TECH-PILOT", rendered)
        self.assertFalse(mapping["write_executed"])

    def test_seven_prechecks_are_individual_and_fail_closed(self):
        checks = self.result["prechecks"]
        self.assertEqual(7, len(checks))
        self.assertEqual({
            "CUSTOMER", "MATERIAL", "SALES_ORGANIZATION", "DISTRIBUTION_CHANNEL",
            "ORGANIZATION_DIVISION", "SALES_ORDER_TYPE", "UNIT_OF_MEASURE",
        }, {check["name"] for check in checks})
        self.assertTrue(all(check["method"] == "GET" for check in checks))
        self.assertTrue(all(check["status"] == "NEEDS_LIVE_VALIDATION" for check in checks))
        self.assertTrue(all(check["contract_status"] == "NEEDS_LIVE_VALIDATION" for check in checks))

    def test_final_result_is_blocked_only_by_unvalidated_sap_prechecks(self):
        result = self.result["final_result"]
        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("EXECUTION_READY", result["local_mapping_status"])
        self.assertEqual(7, len(result["blocking_reasons"]))
        self.assertTrue(all(
            reason["code"].startswith("PRECHECK_") for reason in result["blocking_reasons"]
        ))

    def test_not_found_and_unavailable_read_only_evidence_are_precise_blockers(self):
        result = build_golden_book_scenario("07", read_only_precheck_evidence={
            "CUSTOMER": "NOT_FOUND", "MATERIAL": "INTERFACE_UNAVAILABLE"
        })
        checks = {item["name"]: item for item in result["prechecks"]}
        self.assertEqual("BLOCKED", checks["CUSTOMER"]["status"])
        self.assertIn("did not find", checks["CUSTOMER"]["reason"])
        self.assertEqual("BLOCKED", checks["MATERIAL"]["status"])
        self.assertIn("unavailable", checks["MATERIAL"]["reason"])

    def test_positive_observation_cannot_bypass_unconfirmed_contract(self):
        result = build_golden_book_scenario(
            "07", read_only_precheck_evidence={"CUSTOMER": "FOUND"}
        )
        customer = next(item for item in result["prechecks"] if item["name"] == "CUSTOMER")
        self.assertEqual("NEEDS_LIVE_VALIDATION", customer["status"])

    def test_invalid_training_user_is_rejected(self):
        for value in ("7", "100", "AA", "", None):
            with self.subTest(value=value):
                with self.assertRaises(InvalidTrainingUserCode):
                    build_golden_book_scenario(value)

    def test_view_is_local_read_only_and_contains_required_sections(self):
        html = (ROOT / "src/golden_book/static/index.html").read_text(encoding="utf-8")
        script = (ROOT / "src/golden_book/static/app.js").read_text(encoding="utf-8")
        for title in (
            "Ancrage source", "Données originales", "Données résolues",
            "Workflow détecté", "Mapping SAP", "Sept prechecks", "Résultat final",
        ):
            self.assertIn(title, html)
        self.assertIn("method: 'GET'", script)
        self.assertNotIn("method: 'POST'", script)
        self.assertTrue(self.result["policy"]["canonical_immutable"])
        self.assertFalse(self.result["policy"]["post_allowed"])


if __name__ == "__main__":
    unittest.main()
