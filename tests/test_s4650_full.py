import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data/extracted/full/S4650/objects.json"
NORMALIZED = ROOT / "data/normalized/full/S4650/objects.json"
PRIOR = {course: ROOT / f"data/normalized/full/{course}/objects.json"
         for course in ("S4600", "S4610", "S4615", "S4620")}
ARTIFACTS = [EXTRACTED, NORMALIZED,
    ROOT / "metadata/lineage/full/S4650/lineage.json",
    ROOT / "metadata/lineage/full/S4650/section_inventory.json",
    ROOT / "metadata/lineage/full/S4650/cross_document_checks.json",
    ROOT / "metadata/dependencies/full/S4650/dependency_graph.json",
    ROOT / "metadata/confidence/full/S4650/confidence.json",
    ROOT / "metadata/confidence/full/S4650/extraction_summary.json"]


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


class S4650FullExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extracted = load(EXTRACTED)["objects"]
        cls.normalized = load(NORMALIZED)["objects"]
        cls.by_id = {item["object_id"]: item for item in cls.normalized}

    def test_stable_inventory(self):
        expected = {"BUSINESS_PARTNER": 1, "COPY_CONTROL": 4,
                    "DISTRIBUTION_CHANNEL": 1, "EXTENSION_CONFIGURATION": 2,
                    "OUTBOUND_DELIVERY": 3, "OUTPUT_DETERMINATION": 3,
                    "SALES_AREA": 2, "SALES_DIVISION": 2, "SALES_ORDER": 7,
                    "SALES_ORGANIZATION": 1, "SHARED_MASTER_DATA_ASSIGNMENT": 1,
                    "TEXT_DETERMINATION": 2}
        self.assertEqual(len(self.normalized), 29)
        self.assertEqual(Counter(item["object_type"] for item in self.normalized), expected)
        self.assertEqual(len(self.by_id), 29)

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
                self.assertEqual(source["course_code"], "S4650")
                self.assertEqual(source["source_file"], "S4650_FR_Col12_ILT_FV_Inst_A4.pdf")
                self.assertTrue(1 <= source["page"] <= 267)
                self.assertTrue(source["source_term"])
        inventory = load(ROOT / "metadata/lineage/full/S4650/section_inventory.json")["sections"]
        self.assertEqual(len(inventory), 13)
        self.assertEqual(next(row for row in inventory if row["exercise"] == 8)["decision"], "SKIP")
        self.assertEqual(next(row for row in inventory if row["exercise"] == 6)["decision"],
                         "EXTRACT_AND_ENRICH")

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
                         {"BLOCKED": 25, "READY": 4})

    def test_organization_shared_data_and_copy_control(self):
        areas = [item for item in self.normalized if item["object_type"] == "SALES_AREA"]
        self.assertEqual({item["data"]["sales_division"] for item in areas}, {"00", "03"})
        self.assertTrue(all(item["data"]["business_area_assignment_rule"] == "1" for item in areas))
        shared = self.by_id["S4650_CH1_EX2_SHARED_MASTER_DATA_ASSIGNMENT_CHANNEL_10"]
        self.assertEqual(shared["data"]["scope"],
                         ["PRICING_CONDITIONS", "CUSTOMER_MASTER", "MATERIAL_MASTER"])
        delivery_copy = self.by_id["S4650_CH2_EX4_COPY_CONTROL_ZA_GROUP_TO_LF"]
        self.assertEqual(delivery_copy["data"]["grouping_requirement"], "051")
        self.assertEqual(delivery_copy["data"]["item_data_transfer_routine"], "699")
        self.assertTrue(delivery_copy["data"]["document_flow_update"])

    def test_text_and_output_determination(self):
        text = self.by_id["S4650_CH3_EX7_TEXT_DETERMINATION_HEADER_GROUP"]
        self.assertEqual(text["data"]["text_object"], "VBBK")
        self.assertEqual(text["data"]["text_ids"], ["Y001"])
        self.assertEqual(text["data"]["access_sequence"], "90##")
        ba00 = self.by_id["S4650_CH4_EX9_OUTPUT_DETERMINATION_BA00"]
        zld0 = self.by_id["S4650_CH4_EX10_OUTPUT_DETERMINATION_ZLD0"]
        new = self.by_id["S4650_CH4_EX11_OUTPUT_DETERMINATION_ORDER_CONFIRMATION_GROUP"]
        self.assertEqual((ba00["data"]["framework"], zld0["data"]["framework"]), ("NAST", "NAST"))
        self.assertEqual(new["data"]["framework"], "NEW_OUTPUT_MANAGEMENT")
        self.assertEqual(zld0["data"]["processing_routines"][0]["program"], "RLE_DELNOTE")
        self.assertEqual(new["data"]["form_template"], "SD_SLS_ORDER_CONFIRM")
        self.assertEqual(new["data"]["number_of_copies"], 1)

    def test_extension_configuration_and_terminology(self):
        configs = [item for item in self.normalized if item["object_type"] == "EXTENSION_CONFIGURATION"]
        self.assertEqual({item["data"]["configuration_family"] for item in configs},
                         {"REPORT_LAYOUT", "MATERIAL_FIELD_SELECTION"})
        field_selection = self.by_id["S4650_CH5_EX13_EXTENSION_CONFIGURATION_MATERIAL_FIELD_SELECTION"]
        self.assertIn({"field": "MVKE-DWERK", "canonical_term": "delivering_plant"},
                      field_selection["data"]["settings"])
        for item in self.normalized:
            self.assertNotIn("division", item["data"])

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
        order = self.by_id["S4650_CH4_EX10_SALES_ORDER_ZLD0_DELIVERY_SOURCE"]
        delivery = self.by_id["S4650_CH4_EX10_OUTBOUND_DELIVERY_ZLD0_TEST"]
        self.assertEqual(order["data"]["requested_delivery_date"]["offset"], "P1W")
        self.assertEqual(delivery["data"]["planned_creation_date"]["offset"], "NEXT_WEEK_END")

    def test_cross_document_immutability_return_issue_and_publication_guard(self):
        checks = load(ROOT / "metadata/lineage/full/S4650/cross_document_checks.json")
        self.assertEqual(checks["return_delivery_issue"]["status"], "UNRESOLVED_CARRIED_FORWARD")
        self.assertIsNone(checks["return_delivery_issue"]["s4650_evidence"])
        for course, path in PRIOR.items():
            self.assertEqual(checks["prior_stage_normalized_sha256"][course],
                             hashlib.sha256(path.read_bytes()).hexdigest())
        # A later explicitly authorized Phase 1 consolidation may publish globally;
        # Stage 5 itself must never publish a course-specific validated dataset.
        self.assertFalse((ROOT / "data/validated/S4650").exists())

    def test_deterministic_rerun_and_prior_stage_immutability(self):
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        prior_before = {course: hashlib.sha256(path.read_bytes()).hexdigest()
                        for course, path in PRIOR.items()}
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/extract_s4650.py")], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(before, {path: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in ARTIFACTS})
        self.assertEqual(prior_before, {course: hashlib.sha256(path.read_bytes()).hexdigest()
                                        for course, path in PRIOR.items()})


if __name__ == "__main__":
    unittest.main()
