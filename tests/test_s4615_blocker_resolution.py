import json
import re
import unittest
from pathlib import Path

from scripts.build_s4615_blocker_resolution import (
    ALLOWED_CLASSIFICATIONS,
    OUTPUT_JSON,
    OUTPUT_REPORT,
    build_resolution,
    render_report,
    write_outputs,
)
from src.provisioning.phase5 import Phase5ProvisioningEngine, REQUIRED_DECISION_FIELDS


ROOT = Path(__file__).resolve().parents[1]


class MissingBackend:
    writable = False

    def lookup(self, operation, target):
        return "MISSING"

    def provision(self, operation, target, values):
        raise AssertionError("dry-run must not write")

    def readback(self, operation, target):
        raise AssertionError("dry-run must not read back a write")


class S4615BlockerResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolution = build_resolution()

    def test_primary_facts_only_and_no_full_clean_or_pdf(self):
        self.assertEqual(
            "data/books/S4615/S4615_provisioning_facts.md",
            self.resolution["primary_source"]["path"],
        )
        self.assertFalse(self.resolution["secondary_source_read"])
        serialized = json.dumps(self.resolution, ensure_ascii=False)
        self.assertNotIn("S4615_full_clean.md", serialized)
        self.assertNotIn(".pdf", serialized.casefold())

    def test_exact_target_is_immutable_and_has_no_forbidden_substitution(self):
        self.assertEqual(
            {
                "training_user": "S4615-00",
                "company_code": "1010",
                "sales_organization": "1010",
                "distribution_channel": "10",
                "sales_division": "00",
                "sales_area": "1010/10/00",
                "customer": "C615-D00",
                "product": "P615-400",
                "sales_order_type": "BV",
                "customer_reference": "00S4615-BV",
                "quantity": 1,
                "unit": "PC",
            },
            self.resolution["exact_target"],
        )
        target = json.dumps(self.resolution["exact_target"])
        for forbidden in ("1710", "FG228", '"CS"', "BE01", "FR00"):
            self.assertNotIn(forbidden, target)

    def test_every_fact_has_an_allowed_classification(self):
        facts = [item for group in self.resolution["facts"].values() for item in group]
        self.assertGreater(len(facts), 50)
        self.assertTrue(
            all(item["classification"] in ALLOWED_CLASSIFICATIONS for item in facts)
        )
        self.assertTrue(
            all(item["value"] is None for item in facts if item["classification"] == "UNKNOWN" and not item["field"].endswith("live_state"))
        )

    def test_same_family_objects_are_read_only_candidates_not_invented_values(self):
        inspections = self.resolution["same_family_read_only_inspections"]
        self.assertEqual(
            ["C615-A00", "C615-B00", "P615-100", "P615-200"],
            [item["target"] for item in inspections],
        )
        self.assertTrue(all(item["allowed_method"] == "GET_READ_ONLY" for item in inspections))
        self.assertTrue(all(item["classification"] == "UNKNOWN" for item in inspections))
        self.assertTrue(all(item["usage"] == "EVIDENCE_TEMPLATE_ONLY_NEVER_SUBSTITUTE" for item in inspections))
        self.assertTrue(all(item["resolved_fields"] == {} for item in inspections))
        self.assertTrue(all(item["required_phase5_fields"] for item in inspections))

    def test_company_chart_of_accounts_int_is_book_confirmed(self):
        common = {
            item["field"]: item
            for item in self.resolution["facts"]["common_environment"]
        }
        self.assertEqual("INT", common["company_code_chart_of_accounts"]["value"])
        self.assertEqual(
            "BOOK_CONFIRMED",
            common["company_code_chart_of_accounts"]["classification"],
        )

    def test_sales_org_optional_fields_do_not_block(self):
        self.assertEqual(
            ("creation_strategy", "description", "statistics_currency"),
            REQUIRED_DECISION_FIELDS["SALES_ORGANIZATION_1010"],
        )
        decision = {
            "creation_strategy": "MANUAL_CREATE",
            "description": "DECIDED",
            "statistics_currency": "EUR",
        }
        result = Phase5ProvisioningEngine(
            backend=MissingBackend(),
            decisions={"SALES_ORGANIZATION_1010": decision},
        )._ensure("SALES_ORGANIZATION_1010")
        self.assertEqual("WOULD_PROVISION", result.status)

    def test_statuses_remain_fail_closed(self):
        self.assertEqual("BLOCKED_NEEDS_HUMAN_DECISION", self.resolution["common_environment_status"])
        self.assertEqual("BLOCKED_NEEDS_SOURCE", self.resolution["customer_status"])
        self.assertEqual("BLOCKED_NEEDS_SOURCE", self.resolution["product_status"])
        self.assertEqual("BLOCKED_NOT_EXECUTION_READY", self.resolution["s4615_status"])
        self.assertTrue(self.resolution["final_human_decisions"])

    def test_null_mandatory_decisions_stop_before_write(self):
        decisions = {
            "COMPANY_CODE_1010": {
                "creation_strategy": "MANUAL_CREATE",
                "company_name": None,
                "city": None,
                "country": None,
                "currency": None,
                "language": None,
            }
        }
        result = Phase5ProvisioningEngine(
            backend=MissingBackend(), decisions=decisions
        ).ensure_company_code()
        self.assertEqual("BLOCKED_NEEDS_VALUE", result.status)
        self.assertEqual("PREPARE", result.action)

    def test_workflow_is_exact_and_post_order_contracts_remain_explicit(self):
        stages = [item["stage"] for item in self.resolution["workflow"]]
        self.assertEqual(
            [
                "COMMON_ENV",
                "CUSTOMER_C615_D00",
                "PRODUCT_P615_400",
                "PRECHECKS",
                "ANTI_DUPLICATE_00S4615_BV",
                "BV_CASH_SALE",
                "VERIFY_AUTO_CREATED_DELIVERY",
                "PGI",
                "BILLING_BV",
                "ACCOUNTING_READBACK",
            ],
            stages,
        )
        self.assertEqual("148", self.resolution["execution_policy"]["protected_sales_order"])
        self.assertEqual("--execute", self.resolution["execution_policy"]["write_gate"])

    def test_browser_family_checks_are_get_only(self):
        source = (ROOT / "scripts/browser_checks_s4615_ch4_ex5.js").read_text(encoding="utf-8")
        for expected in ("C615-A00", "C615-B00", "P615-100", "P615-200"):
            self.assertIn(expected, source)
        for expected in (
            "A_CustomerCompany", "A_CustomerSalesArea", "A_ProductPlant",
            "A_ProductSalesDelivery", "A_ProductUnitsOfMeasure", "EVIDENCE",
        ):
            self.assertIn(expected, source)
        self.assertEqual({"GET"}, set(re.findall(r'method:\s*"([A-Z]+)"', source)))
        self.assertNotRegex(source, r"\b(POST|PATCH|PUT|DELETE)\b")

    def test_generation_is_deterministic_and_synced(self):
        before_json = OUTPUT_JSON.read_bytes()
        before_report = OUTPUT_REPORT.read_bytes()
        write_outputs(build_resolution())
        self.assertEqual(before_json, OUTPUT_JSON.read_bytes())
        self.assertEqual(before_report, OUTPUT_REPORT.read_bytes())
        self.assertEqual(
            self.resolution, json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
        )
        self.assertEqual(render_report(self.resolution), OUTPUT_REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
