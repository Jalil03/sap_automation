import hashlib
import json
import re
import unittest

from scripts.build_golden_book_provisioning import (
    BROWSER_SCRIPT_PATH,
    CANONICAL_ID,
    CANONICAL_PATH,
    OUTPUT_PATH,
    REPORT_PATH,
    build_plan,
    browser_script,
    render_report,
)


class GoldenBookProvisioningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        cls.reqs = cls.plan["requirements"]
        cls.index = {r["requirement_id"]: r for r in cls.reqs}

    def test_outputs_are_deterministic(self):
        rebuilt = build_plan()
        self.assertEqual(rebuilt, self.plan)
        self.assertEqual(render_report(rebuilt), REPORT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(browser_script(), BROWSER_SCRIPT_PATH.read_text(encoding="utf-8"))

    def test_canonical_is_immutable(self):
        before = hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest()
        build_plan()
        self.assertEqual(before, hashlib.sha256(CANONICAL_PATH.read_bytes()).hexdigest())
        self.assertEqual(before, self.plan["source_integrity"]["canonical_sha256"])

    def test_exact_scenario_and_user(self):
        scenario = self.plan["scenario"]
        self.assertEqual(CANONICAL_ID, scenario["canonical_object_id"])
        self.assertEqual("00", scenario["training_user_code"])
        self.assertEqual("S4615-00", scenario["training_user_runtime"])

    def test_templates_and_runtime_values(self):
        values = {(r["type"], r["template"]): r["runtime_value"] for r in self.reqs}
        self.assertEqual("C615-D00", values[("BUSINESS_PARTNER", "C615-D##")])
        self.assertEqual("P615-400", values[("MATERIAL", "P615-4##")])
        self.assertEqual("P615-400|PC", values[("PRODUCT_UNIT_OF_MEASURE", "P615-4##|PC")])
        self.assertTrue(all("##" not in r["runtime_value"] for r in self.reqs))

    def test_minimal_known_statuses(self):
        values = {(r["type"], r["runtime_value"]): r for r in self.reqs}
        self.assertEqual("MISSING", values[("SALES_ORGANIZATION", "1010")]["current_sap_status"])
        self.assertEqual("EXISTS", values[("DISTRIBUTION_CHANNEL", "10")]["current_sap_status"])
        self.assertEqual("EXISTS", values[("SALES_DIVISION", "00")]["current_sap_status"])
        self.assertEqual("EXISTS", values[("SALES_ORDER_TYPE", "BV")]["current_sap_status"])
        self.assertEqual("MISSING", values[("BUSINESS_PARTNER", "C615-D00")]["current_sap_status"])
        self.assertEqual("MISSING", values[("MATERIAL", "P615-400")]["current_sap_status"])

    def test_customer_and_product_remain_qualified_unknown(self):
        self.assertEqual("C_CANNOT_DETERMINE_WITHOUT_LIVE_CHECK", self.plan["customer_assessment"]["decision"])
        self.assertEqual("C_CANNOT_DETERMINE_WITHOUT_LIVE_CHECK", self.plan["product_assessment"]["decision"])
        self.assertIn("PC remains PC", self.plan["product_assessment"]["uom_rule"])

    def test_dependencies_exist_and_dag_is_acyclic(self):
        for req in self.reqs:
            self.assertTrue(set(req["depends_on"]).issubset(self.index))
        visiting, visited = set(), set()
        def visit(node):
            if node in visiting:
                self.fail(f"cycle at {node}")
            if node in visited:
                return
            visiting.add(node)
            for dep in self.index[node]["depends_on"]:
                visit(dep)
            visiting.remove(node)
            visited.add(node)
        for node in self.index:
            visit(node)

    def test_no_unrelated_s4615_scenario_is_included(self):
        serialized = json.dumps(self.plan["requirements"], ensure_ascii=False)
        self.assertNotIn("S4615_CH8", serialized)
        self.assertNotIn("SALES_ORDER_PRO_FORMA", serialized)

    def test_first_write_is_sales_org_customizing(self):
        first = self.plan["first_required_sap_write"]
        self.assertEqual("SALES_ORGANIZATION_1010", first["component"])
        self.assertEqual("MANUAL_CUSTOMIZING_REQUIRED", first["kind"])
        self.assertFalse(first["authorized"])

    def test_browser_script_is_get_only_and_sanitized(self):
        script = BROWSER_SCRIPT_PATH.read_text(encoding="utf-8")
        methods = re.findall(r'method:\s*"([A-Z]+)"', script)
        self.assertEqual(["GET"], sorted(set(methods)))
        self.assertIn('credentials: "include"', script)
        self.assertIn("console.table(results)", script)
        self.assertNotRegex(script, re.compile(r"authorization|password|csrf|cookie", re.I))
        self.assertNotIn("289", script)

    def test_summary_matches(self):
        summary = self.plan["summary"]
        self.assertEqual(len(self.reqs), summary["total"])
        self.assertEqual(summary["total"], summary["direct"] + summary["transitive"])
        self.assertEqual(summary["total"], summary["exists"] + summary["missing"] + summary["unknown"])
        self.assertEqual(summary["total"], summary["customizing"] + summary["master_data"] + summary["transactional"])
        self.assertEqual(summary["total"] - summary["exists"], summary["high_risk"])


if __name__ == "__main__":
    unittest.main()
