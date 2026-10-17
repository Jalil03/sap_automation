import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
COURSES = ("S4600", "S4610", "S4615", "S4620", "S4650")
INPUTS = {course: ROOT / f"data/normalized/full/{course}/objects.json" for course in COURSES}
VALIDATED = ROOT / "data/validated/canonical_objects.json"
GRAPH = ROOT / "metadata/dependencies/global_dependency_graph.json"
LINEAGE = ROOT / "metadata/lineage/global_lineage.json"
ARTIFACTS = (VALIDATED, GRAPH, LINEAGE)


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


class Phase1ConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load(VALIDATED)
        cls.objects = cls.dataset["objects"]
        cls.summary = cls.dataset["consolidation_summary"]
        cls.by_id = {item["object_id"]: item for item in cls.objects}
        cls.graph = load(GRAPH)
        cls.lineage = load(LINEAGE)

    def test_stable_inventory_and_classifications(self):
        self.assertEqual(self.summary["input_object_count"], 203)
        self.assertEqual(len(self.objects), 201)
        self.assertEqual(len(self.by_id), 201)
        self.assertEqual(self.summary["duplicates_merged"], 2)
        self.assertEqual(Counter(item["classification"] for item in self.objects),
                         {"CUSTOMIZING": 45, "MASTER_DATA": 24,
                          "REFERENCE_DATA": 9, "TRANSACTION": 123})
        self.assertEqual(Counter(item["object_type"] for item in self.objects)["SALES_ORDER"], 57)
        self.assertEqual(Counter(item["object_type"] for item in self.objects)["BILLING"], 30)

    def test_schema_validity_and_provenance(self):
        for item in self.objects:
            self.assertEqual(validate_object(ROOT, item), [], item["object_id"])
            self.assertEqual(item["lifecycle_status"], "VALIDATED")
            self.assertTrue(item["provenance"])
            for source in item["provenance"]:
                self.assertIn(source["course_code"], COURSES)
                self.assertTrue(source["source_file"])
                self.assertGreater(source["page"], 0)
                self.assertTrue(source["section_type"])

    def test_deterministic_merges_and_preserved_lineage(self):
        merges = self.lineage["deterministic_merges"]
        self.assertEqual(len(merges), 2)
        self.assertEqual({row["identity_key"] for row in merges},
                         {"SALES_ORGANIZATION|1010", "SALES_DIVISION|00"})
        organization = self.by_id["S4600_SHARED_SALES_ORGANIZATION_1010"]
        division = self.by_id["S4600_SHARED_SALES_DIVISION_00"]
        self.assertEqual(organization["data"]["company_code"], "1010")
        self.assertEqual({source["course_code"] for source in organization["provenance"]},
                         {"S4600", "S4650"})
        self.assertEqual({source["course_code"] for source in division["provenance"]},
                         {"S4600", "S4650"})
        self.assertNotIn("S4650_CH1_EX1_SALES_ORGANIZATION_1010", self.by_id)
        self.assertNotIn("S4650_CH1_EX1_SALES_DIVISION_00", self.by_id)

    def test_symbolic_duplicate_candidate_is_not_merged(self):
        candidates = self.lineage["symbolic_duplicate_candidates"]
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["identity_key"], "SHIPPING_POINT|Z0##")
        self.assertEqual(candidates[0]["decision"], "KEEP_SEPARATE_SYMBOLIC_PLACEHOLDER_IDENTITY")
        for object_id in candidates[0]["source_object_ids"]:
            self.assertIn(object_id, self.by_id)
        self.assertEqual(self.lineage["merge_conflicts"], [])

    def test_readiness_and_placeholder_integrity(self):
        self.assertEqual(Counter(item["readiness_status"] for item in self.objects),
                         {"BLOCKED": 175, "READY": 26})
        self.assertEqual(self.summary["placeholder_count"], 355)
        self.assertEqual(self.summary["objects_with_placeholders"], 149)
        for item in self.objects:
            paths = {entry["field_path"] for entry in item["placeholders"]
                     if entry["status"] == "UNRESOLVED"}
            for path, value in strings(item["data"]):
                if "##" in value:
                    self.assertIn(path, paths, (item["object_id"], path))
            if item["readiness_status"] == "READY":
                self.assertEqual(item["blocking_reasons"], [])
                self.assertFalse(any(entry["mandatory"] and entry["status"] == "UNRESOLVED"
                                     for entry in item["placeholders"]))

    def test_global_dependency_integrity_and_cross_resolution(self):
        self.assertEqual(len(self.graph["nodes"]), 201)
        self.assertEqual(len(self.graph["edges"]), 319)
        self.assertEqual(self.graph["summary"]["resolved"], 169)
        self.assertEqual(self.graph["summary"]["unresolved"], 150)
        for edge in self.graph["edges"]:
            if edge["status"] == "RESOLVED":
                self.assertIn(edge["target"], self.by_id, edge)
                self.assertEqual(self.by_id[edge["target"]]["object_type"], edge["target_type"])
            else:
                self.assertIsNone(edge["target"])
        self.assertEqual(self.graph["cross_document_resolutions"], [{
            "relation": "ASSIGNED_TO",
            "resolution_basis": "Exact non-placeholder company_code 1010",
            "source_object_id": "S4600_SHARED_SALES_ORGANIZATION_1010",
            "target_object_id": "S4615_SHARED_COMPANY_CODE_1010"}])

    def test_return_delivery_issue_remains_open(self):
        issue = self.lineage["open_issues"][0]
        self.assertEqual(issue["object_id"],
                         "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER")
        self.assertEqual(issue["status"], "UNRESOLVED_CARRIED_FORWARD")
        self.assertIsNone(issue["resolution"])

    def test_terminology_and_lifecycle_consistency(self):
        def walk(value):
            if isinstance(value, dict):
                self.assertNotIn("division", value)
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        for item in self.objects:
            walk(item["data"])
            self.assertIn(item["readiness_status"], {"READY", "BLOCKED"})
            self.assertEqual(item["validation"]["schema_valid"], True)

    def test_all_publication_gates_pass(self):
        self.assertEqual(self.summary["publication_status"], "PUBLISHED_VALIDATED")
        self.assertTrue(all(status == "PASS" for status in self.summary["gates"].values()))
        self.assertEqual(self.summary["schema_invalid_count"], 0)
        self.assertEqual(self.summary["merge_conflict_count"], 0)

    def test_staged_inputs_are_immutable(self):
        recorded = self.lineage["staged_normalized_sha256"]
        for course, path in INPUTS.items():
            self.assertEqual(recorded[course], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_deterministic_rerun(self):
        artifacts_before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        inputs_before = {course: hashlib.sha256(path.read_bytes()).hexdigest()
                         for course, path in INPUTS.items()}
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/consolidate_phase1.py")], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(artifacts_before,
                         {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS})
        self.assertEqual(inputs_before,
                         {course: hashlib.sha256(path.read_bytes()).hexdigest()
                          for course, path in INPUTS.items()})


if __name__ == "__main__":
    unittest.main()
