import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data/extracted/full/S4620/objects.json"
NORMALIZED = ROOT / "data/normalized/full/S4620/objects.json"
PRIOR = {course: ROOT / f"data/normalized/full/{course}/objects.json"
         for course in ("S4600", "S4610", "S4615")}
ARTIFACTS = [EXTRACTED, NORMALIZED,
    ROOT / "metadata/lineage/full/S4620/lineage.json",
    ROOT / "metadata/lineage/full/S4620/section_inventory.json",
    ROOT / "metadata/lineage/full/S4620/cross_document_checks.json",
    ROOT / "metadata/dependencies/full/S4620/dependency_graph.json",
    ROOT / "metadata/confidence/full/S4620/confidence.json",
    ROOT / "metadata/confidence/full/S4620/extraction_summary.json"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def strings(value, path="data"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


class S4620FullExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extracted = load(EXTRACTED)["objects"]
        cls.normalized = load(NORMALIZED)["objects"]
        cls.by_id = {item["object_id"]: item for item in cls.normalized}

    def test_stable_inventory(self):
        expected = {"ACCESS_SEQUENCE": 2, "CONDITION_CONTRACT": 1,
                    "CONDITION_TABLE": 4, "CONDITION_TYPE": 5,
                    "CUSTOMER_HIERARCHY": 1, "PRICING_CONDITION": 11,
                    "PRICING_PROCEDURE": 3,
                    "PRICING_PROCEDURE_DETERMINATION": 3,
                    "SALES_ORDER": 18, "SETTLEMENT_DOCUMENT": 3}
        self.assertEqual(len(self.normalized), 51)
        self.assertEqual(Counter(item["object_type"] for item in self.normalized), expected)
        self.assertEqual(len(self.by_id), 51)

    def test_schema_validation_and_lifecycle(self):
        for item in self.normalized + self.extracted:
            self.assertEqual(validate_object(ROOT, item), [], item["object_id"])
        self.assertTrue(all(item["lifecycle_status"] == "VALIDATED" for item in self.normalized))
        self.assertTrue(all(item["lifecycle_status"] == "EXTRACTED" for item in self.extracted))

    def test_provenance_scenarios_and_solution_dedup(self):
        for item in self.normalized:
            self.assertTrue(any(source["section_type"] == "EXERCISE" for source in item["provenance"]),
                            item["object_id"])
            self.assertTrue(any(source["section_type"] == "SOLUTION" for source in item["provenance"]),
                            item["object_id"])
            for source in item["provenance"]:
                self.assertEqual(source["course_code"], "S4620")
                self.assertEqual(source["source_file"], "S4620_FR_Col12_ILT_FV_Inst_A4.pdf")
                self.assertTrue(1 <= source["page"] <= 351)
                self.assertTrue(source["source_term"])
        inventory = load(ROOT / "metadata/lineage/full/S4620/section_inventory.json")["sections"]
        self.assertEqual(len(inventory), 27)
        self.assertEqual(next(row for row in inventory if row["exercise"] == 13)["decision"],
                         "ENRICH_EXISTING")
        self.assertEqual(next(row for row in inventory if row["exercise"] == 10)["decision"], "SKIP")

    def test_placeholder_preservation_and_readiness(self):
        for item in self.normalized:
            placeholders = {entry["field_path"]: entry for entry in item["placeholders"]}
            for path, value in strings(item["data"]):
                if "##" in value:
                    self.assertIn(path, placeholders, (item["object_id"], path))
                    self.assertIsNone(placeholders[path]["resolved"])
                    self.assertEqual(placeholders[path]["status"], "UNRESOLVED")
                    self.assertEqual(item["readiness_status"], "BLOCKED")
        self.assertEqual(Counter(item["readiness_status"] for item in self.normalized),
                         {"BLOCKED": 40, "READY": 11})

    def test_quantity_value_and_weight_scales(self):
        quantity = self.by_id["S4620_CH1_EX1_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL_SCALE"]
        self.assertEqual([(row["threshold"], row["amount"]) for row in quantity["data"]["scales"]],
                         [(1, 250), (10, 240), (100, 230)])
        value = self.by_id["S4620_CH1_EX1_PRICING_CONDITION_K007_CUSTOMER_VALUE_SCALE"]
        self.assertEqual(value["data"]["scale_basis"], "VALUE")
        self.assertEqual([(row["threshold"], row["rate"]) for row in value["data"]["scales"]],
                         [(100, 2), (1000, 3), (5000, 5)])
        weight = self.by_id["S4620_CH4_EX15_PRICING_CONDITION_ZW_GROUP_WEIGHT_SCALE"]
        self.assertEqual(weight["data"]["scales"][-1]["threshold"], 30.001)
        self.assertEqual(weight["data"]["scales"][-1]["amount"], 0)

    def test_condition_technique_chain_and_determination(self):
        access = self.by_id["S4620_CH2_EX7_ACCESS_SEQUENCE_PR02"]
        self.assertEqual(access["data"]["condition_tables"], ["305", "306", "304"])
        custom = self.by_id["S4620_CH2_EX9_PRICING_PROCEDURE_Z_GROUP_PRC"]
        self.assertEqual([step["condition_type"] for step in custom["data"]["steps"]],
                         ["ZW##", "ZF##"])
        self.assertEqual(custom["data"]["exclusion_groups"][0]["comparison_procedure"], "D")
        settlement = self.by_id["S4620_CH7_EX21_PRICING_PROCEDURE_DETERMINATION_SETTLEMENT"]
        self.assertEqual(settlement["data"]["settlement_document_schema_group"], "0S")
        self.assertEqual(settlement["data"]["pricing_procedure"], "A10005")

    def test_hierarchy_contract_and_settlements(self):
        hierarchy = self.by_id["S4620_CH5_EX19_CUSTOMER_HIERARCHY_TOPCO_WESTERN_EUROPE"]
        self.assertEqual(hierarchy["data"]["nodes"][1]["node_id"], "C620-ZEW")
        contract = self.by_id["S4620_CH7_EX23_CONDITION_CONTRACT_SALES_REBATE"]
        self.assertEqual([row["condition_type"] for row in contract["data"]["conditions"]],
                         ["RES1", "REA1"])
        settlements = [item for item in self.normalized if item["object_type"] == "SETTLEMENT_DOCUMENT"]
        self.assertEqual([(item["data"]["settlement_type"], item["data"]["amount"])
                          for item in settlements],
                         [("DELTA_ACCRUAL", 200), ("PARTIAL_SETTLEMENT_CREDIT", 200),
                          ("FINAL_SETTLEMENT_CREDIT", 100)])

    def test_dependency_integrity_and_relative_values(self):
        for item in self.normalized:
            for dependency in item["dependencies"]:
                if dependency["status"] == "RESOLVED":
                    self.assertIn(dependency["target_id"], self.by_id,
                                  (item["object_id"], dependency))
                    self.assertEqual(self.by_id[dependency["target_id"]]["object_type"],
                                     dependency["target_type"])
                else:
                    self.assertIsNone(dependency["target_id"])
        future = self.by_id["S4620_CH3_EX12_PRICING_CONDITION_PR00_P620_2_NEXT_YEAR"]
        self.assertEqual(future["data"]["valid_from"]["offset"], "NEXT_YEAR_START")
        final = self.by_id["S4620_CH7_EX27_SETTLEMENT_DOCUMENT_FINAL_CREDIT"]
        self.assertEqual(final["data"]["settlement_date"]["offset"], "CURRENT_YEAR_END")

    def test_cross_document_immutability_return_issue_and_publication_guard(self):
        checks = load(ROOT / "metadata/lineage/full/S4620/cross_document_checks.json")
        self.assertEqual(checks["return_delivery_issue"]["status"], "UNRESOLVED_CARRIED_FORWARD")
        self.assertIsNone(checks["return_delivery_issue"]["s4620_evidence"])
        for course, path in PRIOR.items():
            self.assertEqual(checks["prior_stage_normalized_sha256"][course],
                             hashlib.sha256(path.read_bytes()).hexdigest())
        # A later explicitly authorized Phase 1 consolidation may publish globally;
        # Stage 4 itself must never publish a course-specific validated dataset.
        self.assertFalse((ROOT / "data/validated/S4620").exists())
        # Stage 5 may now exist; this Stage 4 regression continues to guard publication only.

    def test_deterministic_rerun_and_prior_stage_immutability(self):
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        prior_before = {course: hashlib.sha256(path.read_bytes()).hexdigest()
                        for course, path in PRIOR.items()}
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/extract_s4620.py")], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(before, {path: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in ARTIFACTS})
        self.assertEqual(prior_before, {course: hashlib.sha256(path.read_bytes()).hexdigest()
                                        for course, path in PRIOR.items()})


if __name__ == "__main__":
    unittest.main()
