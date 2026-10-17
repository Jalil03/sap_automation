import hashlib
import json
import unittest
from pathlib import Path

from scripts.build_training_requirements import (
    BOOKS,
    CANONICAL_PATH,
    CATEGORIES,
    OUTPUT_PATH,
    REPORT_PATH,
    RISKS,
    SAP_STATUSES,
    SCOPES,
    STRATEGIES,
    build_inventory,
    render_report,
)


class TrainingEnvironmentRequirementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.persisted = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        cls.requirements = cls.persisted["requirements"]

    def test_outputs_are_deterministic_and_synced(self):
        rebuilt = build_inventory()
        self.assertEqual(rebuilt, self.persisted)
        self.assertEqual(render_report(rebuilt), REPORT_PATH.read_text(encoding="utf-8"))

    def test_canonical_is_immutable_during_build(self):
        before = hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest()
        build_inventory()
        after = hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(before, self.persisted["source"]["canonical_sha256"])

    def test_required_fields_enums_and_ids(self):
        expected = {
            "requirement_id", "category", "type", "value_template", "source_book",
            "source_scenario", "scope", "contains_placeholder", "placeholder_pattern",
            "depends_on", "sap_interface_candidate", "current_known_sap_status",
            "evidence_source", "provisioning_strategy", "risk", "canonical_object_ids",
        }
        ids = {r["requirement_id"] for r in self.requirements}
        self.assertEqual(len(ids), len(self.requirements))
        for req in self.requirements:
            self.assertEqual(set(req), expected)
            self.assertIn(req["category"], CATEGORIES)
            self.assertIn(req["scope"], SCOPES)
            self.assertIn(req["current_known_sap_status"], SAP_STATUSES)
            self.assertIn(req["provisioning_strategy"], STRATEGIES)
            self.assertIn(req["risk"], RISKS)
            self.assertTrue(set(req["source_book"]).issubset(BOOKS))
            self.assertTrue(set(req["depends_on"]).issubset(ids))

    def test_every_canonical_object_is_covered(self):
        canonical = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))["objects"]
        covered = {oid for r in self.requirements for oid in r["canonical_object_ids"]}
        self.assertEqual({o["object_id"] for o in canonical}, covered)

    def test_all_books_are_covered(self):
        observed = {book for req in self.requirements for book in req["source_book"]}
        self.assertEqual(set(BOOKS), observed)

    def test_common_sales_organization_is_deduplicated(self):
        matches = [r for r in self.requirements if r["type"] == "SALES_ORGANIZATION" and r["value_template"] == "1010"]
        self.assertEqual(1, len(matches))
        self.assertEqual("GLOBAL", matches[0]["scope"])
        self.assertEqual("MISSING", matches[0]["current_known_sap_status"])
        self.assertEqual(set(BOOKS), set(matches[0]["source_book"]))

    def test_confirmed_live_statuses(self):
        expected = {
            ("DISTRIBUTION_CHANNEL", "10"): "EXISTS",
            ("SALES_DIVISION", "00"): "EXISTS",
            ("SALES_ORDER_TYPE", "BV"): "EXISTS",
            ("BUSINESS_PARTNER", "C615-D##"): "MISSING",
            ("MATERIAL", "P615-4##"): "MISSING",
            ("BUSINESS_PARTNER", "T-S50A##"): "MISSING",
            ("MATERIAL", "T-MS1##"): "MISSING",
            ("BUSINESS_PARTNER", "C610-A##"): "MISSING",
            ("MATERIAL", "P610-5##"): "MISSING",
            ("BUSINESS_PARTNER", "C620-A##"): "MISSING",
            ("MATERIAL", "P620-1##"): "MISSING",
            ("BUSINESS_PARTNER", "C650-A##"): "MISSING",
            ("MATERIAL", "P650-1##"): "MISSING",
            ("MATERIAL", "P650-100"): "MISSING",
        }
        index = {(r["type"], r["value_template"]): r for r in self.requirements}
        for key, status in expected.items():
            self.assertIn(key, index)
            self.assertEqual(status, index[key]["current_known_sap_status"])

    def test_placeholders_are_preserved_and_per_user(self):
        templated = [r for r in self.requirements if "##" in r["value_template"]]
        self.assertTrue(templated)
        for req in templated:
            self.assertTrue(req["contains_placeholder"])
            self.assertEqual("##", req["placeholder_pattern"])
            self.assertEqual("PER_USER", req["scope"])
        golden = next(r for r in self.requirements if "S4615_CH4_EX5_SALES_ORDER_CASH_SALE" in r["canonical_object_ids"])
        self.assertTrue(golden["contains_placeholder"])
        self.assertEqual("PER_USER", golden["scope"])

    def test_product_uom_contract_is_product_specific(self):
        context = self.persisted["live_evidence_context"]["confirmed_product_uom_contract"]
        self.assertEqual("A_ProductUnitsOfMeasure", context["entity_set"])
        self.assertEqual(["Product", "AlternativeUnit"], context["keys"])
        self.assertEqual({"Product": "FG228", "AlternativeUnit": "PC", "status": "EXISTS"}, context["observed_pair"])
        book_uoms = [r for r in self.requirements if r["type"] == "PRODUCT_UNIT_OF_MEASURE"]
        self.assertTrue(book_uoms)
        self.assertTrue(all(r["current_known_sap_status"] == "UNKNOWN" for r in book_uoms))
        self.assertTrue(all(r["provisioning_strategy"] == "BLOCKED" for r in book_uoms))

    def test_report_contains_complete_inventory(self):
        report = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("## Inventaire complet", report)
        for req in self.requirements:
            self.assertIn(req["requirement_id"], report)

    def test_summary_counts_match_rows(self):
        summary = self.persisted["summary"]
        self.assertEqual(len(self.requirements), summary["total"])
        for dimension, field in (("by_category", "category"), ("by_scope", "scope"), ("by_sap_status", "current_known_sap_status"), ("by_risk", "risk")):
            counts = {}
            for req in self.requirements:
                counts[req[field]] = counts.get(req[field], 0) + 1
            enum = {
                "by_category": CATEGORIES,
                "by_scope": SCOPES,
                "by_sap_status": SAP_STATUSES,
                "by_risk": RISKS,
            }[dimension]
            self.assertEqual({key: counts.get(key, 0) for key in sorted(enum)}, summary[dimension])


if __name__ == "__main__":
    unittest.main()
