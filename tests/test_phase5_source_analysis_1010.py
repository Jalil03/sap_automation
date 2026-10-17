import json
import unittest

from scripts.run_phase5_source_discovery import (
    OUTPUT_JSON,
    OUTPUT_REPORT,
    build_analysis,
    render_report,
    write_outputs,
)


class Phase5SourceAnalysis1010Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analysis = build_analysis()

    def test_no_candidate_is_automatically_selected(self):
        self.assertIsNone(self.analysis["automatic_selection"])
        candidates = [
            candidate
            for item in self.analysis["objects"].values()
            for candidate in item["candidates"]
        ]
        self.assertTrue(candidates)
        self.assertTrue(all(not item["automatically_selected"] for item in candidates))

    def test_company_candidates_are_ranked_only_by_observed_evidence(self):
        candidates = self.analysis["objects"]["COMPANY_CODE_1010"]["candidates"]
        tier_one = [item["candidate_id"] for item in candidates if item["rank_tier"] == 1]
        self.assertEqual(
            ["AE01", "AR01", "AT01", "AU01", "BE01", "BR01", "CH01", "CL01"],
            tier_one,
        )
        self.assertTrue(all(item["suitability"] == "NOT_DETERMINED" for item in candidates))

    def test_sales_org_candidates_have_no_template_claim(self):
        candidates = self.analysis["objects"]["SALES_ORGANIZATION_1010"]["candidates"]
        self.assertEqual(13, len(candidates))
        self.assertTrue(all(item["confidence"] == "LOW" for item in candidates))
        self.assertTrue(all(item["suitability"] == "NOT_DETERMINED" for item in candidates))

    def test_1710_is_observed_but_never_defaulted(self):
        for object_data in self.analysis["objects"].values():
            candidate = next(
                item for item in object_data["candidates"] if item["candidate_id"] == "1710"
            )
            self.assertFalse(candidate["automatically_selected"])
            self.assertIn("not a default", candidate["notes"])

    def test_missing_values_remain_explicit(self):
        company = self.analysis["objects"]["COMPANY_CODE_1010"]
        sales_org = self.analysis["objects"]["SALES_ORGANIZATION_1010"]
        self.assertEqual(
            {"company_name", "city", "country", "currency", "language"},
            {
                item["field"]
                for item in company["missing_required_values"]
                if item["status"] == "BLOCKED_NEEDS_VALUE"
            },
        )
        self.assertEqual(
            {"description", "statistics_currency"},
            {
                item["field"]
                for item in sales_org["missing_required_values"]
                if item["status"] == "BLOCKED_NEEDS_VALUE"
            },
        )

    def test_live_follow_up_is_status_and_inspect_only(self):
        self.assertTrue(self.analysis["live_read_only_required"])
        self.assertEqual(
            ["STATUS", "INSPECT"],
            self.analysis["live_constraints"]["allowed_actions"],
        )

    def test_generation_is_idempotent_and_outputs_are_synced(self):
        before_json = OUTPUT_JSON.read_bytes()
        before_report = OUTPUT_REPORT.read_bytes()
        write_outputs(build_analysis())
        self.assertEqual(before_json, OUTPUT_JSON.read_bytes())
        self.assertEqual(before_report, OUTPUT_REPORT.read_bytes())
        self.assertEqual(
            self.analysis,
            json.loads(OUTPUT_JSON.read_text(encoding="utf-8")),
        )
        self.assertEqual(render_report(self.analysis), OUTPUT_REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
