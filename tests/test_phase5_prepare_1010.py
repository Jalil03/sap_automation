import json
import unittest
from pathlib import Path

from scripts.prepare_phase5_provisioning import (
    OUTPUT_JSON,
    OUTPUT_REPORT,
    build_plan,
    render_report,
    write_outputs,
)


class Phase5Prepare1010Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = build_plan()

    def test_exact_order_and_required_step_fields(self):
        steps = self.plan["ordered_steps"]
        self.assertEqual(
            [
                "COMPANY_CODE_1010",
                "SALES_ORGANIZATION_1010",
                "SALES_ORG_1010_TO_COMPANY_CODE_1010",
                "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
                "DIVISION_00_TO_SALES_ORG_1010",
            ],
            [step["step_id"] for step in steps],
        )
        required = {
            "target",
            "current_state",
            "evidence",
            "required_action",
            "source_candidates",
            "missing_values",
            "status",
        }
        self.assertTrue(all(required <= set(step) for step in steps))

    def test_company_code_uses_authoritative_sap_total(self):
        company = self.plan["ordered_steps"][0]
        scan = company["evidence"][0]
        self.assertEqual("MISSING", company["current_state"])
        self.assertEqual(112, scan["sap_total_entries"])
        self.assertEqual(112, scan["unique_rows_read"])
        self.assertIsNone(scan["found_row"])
        self.assertEqual("BLOCKED_NEEDS_SOURCE", company["status"])

    def test_five_current_states_are_evidence_bounded(self):
        self.assertEqual(
            ["MISSING", "MISSING", "UNKNOWN", "UNKNOWN", "UNKNOWN"],
            [step["current_state"] for step in self.plan["ordered_steps"]],
        )

    def test_missing_foundations_need_sources_and_assignments_need_dependencies(self):
        company, sales_org, *assignments = self.plan["ordered_steps"]
        self.assertEqual("BLOCKED_NEEDS_SOURCE", company["status"])
        self.assertEqual("BLOCKED_NEEDS_SOURCE", sales_org["status"])
        self.assertTrue(company["missing_values"])
        self.assertTrue(sales_org["missing_values"])
        self.assertTrue(all(step["status"] == "BLOCKED_DEPENDENCY" for step in assignments))
        self.assertTrue(all(not step["missing_values"] for step in assignments))

    def test_1710_is_never_a_source_candidate(self):
        for step in self.plan["ordered_steps"]:
            serialized = json.dumps(step["source_candidates"], ensure_ascii=False)
            self.assertNotIn("1710", serialized)
        self.assertFalse(self.plan["safety"]["automatic_template_selection"])

    def test_plan_is_offline_prepare_only(self):
        self.assertEqual("PREPARE", self.plan["mode"])
        self.assertFalse(self.plan["execution_performed"])
        self.assertFalse(self.plan["sap_connection_performed"])
        self.assertEqual(
            ["READ_LOCAL_ARTIFACTS", "PREPARE_PLAN"], self.plan["safety"]["allowed"]
        )

    def test_generation_is_idempotent_and_outputs_are_synced(self):
        before_json = OUTPUT_JSON.read_bytes()
        before_report = OUTPUT_REPORT.read_bytes()
        write_outputs(build_plan())
        self.assertEqual(before_json, OUTPUT_JSON.read_bytes())
        self.assertEqual(before_report, OUTPUT_REPORT.read_bytes())
        self.assertEqual(
            self.plan,
            json.loads(OUTPUT_JSON.read_text(encoding="utf-8")),
        )
        self.assertEqual(render_report(self.plan), OUTPUT_REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
