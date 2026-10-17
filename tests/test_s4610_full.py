import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data/extracted/full/S4610/objects.json"
NORMALIZED = ROOT / "data/normalized/full/S4610/objects.json"
S4600 = ROOT / "data/normalized/full/S4600/objects.json"
ARTIFACTS = [
    EXTRACTED,
    NORMALIZED,
    ROOT / "metadata/lineage/full/S4610/lineage.json",
    ROOT / "metadata/lineage/full/S4610/section_inventory.json",
    ROOT / "metadata/lineage/full/S4610/cross_document_checks.json",
    ROOT / "metadata/dependencies/full/S4610/dependency_graph.json",
    ROOT / "metadata/confidence/full/S4610/confidence.json",
    ROOT / "metadata/confidence/full/S4610/extraction_summary.json",
]


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


class S4610FullExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extracted = load(EXTRACTED)["objects"]
        cls.normalized = load(NORMALIZED)["objects"]
        cls.by_id = {item["object_id"]: item for item in cls.normalized}

    def test_stable_inventory(self):
        expected = {"COPY_CONTROL": 2, "GOODS_ISSUE": 1, "INBOUND_DELIVERY": 2,
                    "OUTBOUND_DELIVERY": 3, "PLANT": 1, "PURCHASE_ORDER_REFERENCE": 2,
                    "SALES_ORDER": 3, "SHIPPING_POINT": 2, "STORAGE_LOCATION": 2,
                    "WAREHOUSE_NUMBER": 1, "WAREHOUSE_TASK": 2}
        self.assertEqual(len(self.normalized), 21)
        self.assertEqual(Counter(item["object_type"] for item in self.normalized), expected)
        self.assertEqual(len(self.by_id), 21)

    def test_schema_validation_and_lifecycle(self):
        for item in self.normalized + self.extracted:
            self.assertEqual(validate_object(ROOT, item), [], item["object_id"])
        self.assertTrue(all(item["lifecycle_status"] == "VALIDATED" for item in self.normalized))
        self.assertTrue(all(item["lifecycle_status"] == "EXTRACTED" for item in self.extracted))

    def test_provenance_and_scenario_consistency(self):
        for item in self.normalized:
            self.assertTrue(any(source["section_type"] == "EXERCISE" for source in item["provenance"]), item["object_id"])
            self.assertTrue(any(source["section_type"] == "SOLUTION" for source in item["provenance"]), item["object_id"])
            primary = {source["scenario_id"] for source in item["provenance"]
                       if source["section_type"] == "EXERCISE"}
            self.assertIn(item["scenario_id"], primary, item["object_id"])
            for source in item["provenance"]:
                self.assertEqual(source["course_code"], "S4610")
                self.assertEqual(source["source_file"], "S4610_FR_Col12_ILT_FV_Inst_A4.pdf")
                self.assertTrue(1 <= source["page"] <= 202)
                self.assertTrue(source["source_term"])

    def test_placeholder_preservation_and_readiness(self):
        for item in self.normalized:
            placeholders = {entry["field_path"]: entry for entry in item["placeholders"]}
            for path, value in strings(item["data"]):
                if "##" in value:
                    self.assertIn(path, placeholders, (item["object_id"], path))
                    self.assertEqual(placeholders[path]["raw"], "##")
                    self.assertIsNone(placeholders[path]["resolved"])
                    self.assertEqual(item["readiness_status"], "BLOCKED")
        self.assertEqual(Counter(item["readiness_status"] for item in self.normalized),
                         {"BLOCKED": 17, "READY": 4})

    def test_outbound_inbound_and_system_representation_semantics(self):
        outbound = [item for item in self.normalized if item["object_type"] == "OUTBOUND_DELIVERY"]
        inbound = [item for item in self.normalized if item["object_type"] == "INBOUND_DELIVERY"]
        self.assertEqual(len(outbound), 3)
        self.assertEqual(len(inbound), 2)
        self.assertTrue(all(item["data"]["delivery_type"] == "INBOUND" for item in inbound))
        for item in inbound:
            systems = [entry["system"] for entry in item["data"]["system_representations"]]
            self.assertEqual(systems, ["LE", "EWM"])
        ex10 = self.by_id["S4610_CH5_EX10_OUTBOUND_DELIVERY_FROM_ORDER"]
        self.assertEqual([entry["system"] for entry in ex10["data"]["system_representations"]],
                         ["LE", "EWM"])

    def test_plant_storage_warehouse_and_purchase_order_integrity(self):
        self.assertEqual(self.by_id["S4610_SHARED_PLANT_1010"]["data"]["code"], "1010")
        self.assertEqual({self.by_id["S4610_SHARED_STORAGE_LOCATION_101C"]["data"]["code"],
                          self.by_id["S4610_SHARED_STORAGE_LOCATION_101D"]["data"]["code"]},
                         {"101C", "101D"})
        warehouse = self.by_id["S4610_SHARED_WAREHOUSE_NUMBER_1010"]
        self.assertEqual(warehouse["data"]["plant_storage_locations"], ["1010/101C", "1010/101D"])
        inbound = self.by_id["S4610_CH5_EX14_INBOUND_DELIVERY_FROM_PURCHASE_ORDER"]
        self.assertEqual(inbound["data"]["storage_location"], "101D")
        self.assertEqual(inbound["data"]["warehouse_number"], "1010")
        self.assertEqual(inbound["dependencies"][0]["target_type"], "PURCHASE_ORDER_REFERENCE")

    def test_dependency_integrity(self):
        for item in self.normalized:
            for dep in item["dependencies"]:
                if dep["status"] == "RESOLVED":
                    self.assertIn(dep["target_id"], self.by_id, (item["object_id"], dep))
                    self.assertEqual(self.by_id[dep["target_id"]]["object_type"], dep["target_type"])
                else:
                    self.assertIsNone(dep["target_id"])

    def test_exercise_solution_dedup_and_skips(self):
        inventory = load(ROOT / "metadata/lineage/full/S4610/section_inventory.json")["sections"]
        self.assertEqual(len(inventory), 14)
        self.assertEqual(next(row for row in inventory if row["exercise"] == 5)["decision"], "ENRICH_EXISTING")
        self.assertEqual(next(row for row in inventory if row["exercise"] == 8)["decision"], "ENRICH_EXISTING")
        self.assertEqual(next(row for row in inventory if row["exercise"] == 9)["decision"], "SKIP")
        # One canonical inbound delivery per exercise despite LE and EWM document representations.
        for exercise in (13, 14):
            self.assertEqual(sum(item["object_type"] == "INBOUND_DELIVERY" and
                                 item["scenario_id"] == f"S4610_CH5_EX{exercise}"
                                 for item in self.normalized), 1)

    def test_cross_document_check_and_return_issue(self):
        checks = load(ROOT / "metadata/lineage/full/S4610/cross_document_checks.json")
        self.assertEqual(checks["return_delivery_issue"]["status"], "UNRESOLVED_CARRIED_FORWARD")
        self.assertEqual(checks["potential_entity_matches"][0]["status"],
                         "POTENTIAL_MATCH_UNRESOLVED_PLACEHOLDER")
        self.assertEqual(checks["s4600_normalized_sha256"], hashlib.sha256(S4600.read_bytes()).hexdigest())

    def test_deterministic_rerun_and_s4600_immutability(self):
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        s4600_before = hashlib.sha256(S4600.read_bytes()).hexdigest()
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/extract_s4610.py")], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        self.assertEqual(before, after)
        self.assertEqual(s4600_before, hashlib.sha256(S4600.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
