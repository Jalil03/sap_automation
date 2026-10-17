import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
NORMALIZED = ROOT / "data/normalized/full/S4600/objects.json"
EXTRACTED = ROOT / "data/extracted/full/S4600/objects.json"
ARTIFACTS = [
    EXTRACTED,
    NORMALIZED,
    ROOT / "metadata/lineage/full/S4600/lineage.json",
    ROOT / "metadata/lineage/full/S4600/section_inventory.json",
    ROOT / "metadata/dependencies/full/S4600/dependency_graph.json",
    ROOT / "metadata/confidence/full/S4600/confidence.json",
    ROOT / "metadata/confidence/full/S4600/extraction_summary.json",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def walk_strings(value, path="data"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


class S4600FullExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normalized = load(NORMALIZED)["objects"]
        cls.extracted = load(EXTRACTED)["objects"]

    def test_stable_inventory(self):
        expected = {
            "BILLING": 6, "BUSINESS_PARTNER": 2, "CREDIT_MEMO_REQUEST": 1,
            "CUSTOMER_MATERIAL_INFO": 1, "DISTRIBUTION_CHANNEL": 1,
            "GOODS_ISSUE": 3, "INQUIRY": 1, "MATERIAL": 4,
            "OUTBOUND_DELIVERY": 7, "PAYMENT_REFERENCE": 1,
            "PRICING_CONDITION": 3, "QUOTATION": 1, "RETURN_ORDER": 1,
            "SALES_AREA": 1, "SALES_DIVISION": 1, "SALES_ORDER": 18,
            "SALES_ORGANIZATION": 1, "SHIPPING_POINT": 1,
        }
        self.assertEqual(len(self.normalized), 54)
        self.assertEqual(Counter(item["object_type"] for item in self.normalized), expected)
        self.assertEqual(len({item["object_id"] for item in self.normalized}), 54)

    def test_schema_validation_and_lifecycle(self):
        for item in self.normalized + self.extracted:
            self.assertEqual(validate_object(ROOT, item), [], item["object_id"])
        self.assertTrue(all(item["lifecycle_status"] == "VALIDATED" for item in self.normalized))
        self.assertTrue(all(item["lifecycle_status"] == "EXTRACTED" for item in self.extracted))

    def test_provenance_is_complete_and_s4600_only(self):
        for item in self.normalized:
            self.assertTrue(item["provenance"], item["object_id"])
            self.assertTrue(any(ref["section_type"] == "EXERCISE" for ref in item["provenance"]), item["object_id"])
            self.assertTrue(any(ref["section_type"] == "SOLUTION" for ref in item["provenance"]), item["object_id"])
            for ref in item["provenance"]:
                self.assertEqual(ref["course_code"], "S4600")
                self.assertEqual(ref["source_file"], "P2W_S4600_FR_Col23.pdf")
                self.assertGreaterEqual(ref["page"], 1)
                self.assertLessEqual(ref["page"], 353)
                self.assertTrue(ref["source_term"])

    def test_scenario_id_consistency_and_solution_deduplication(self):
        for item in self.normalized:
            exercises = {ref["scenario_id"] for ref in item["provenance"] if ref["section_type"] == "EXERCISE"}
            self.assertIn(item["scenario_id"], exercises, item["object_id"])
        inventory = load(ROOT / "metadata/lineage/full/S4600/section_inventory.json")["sections"]
        ex4 = next(section for section in inventory if section["exercise"] == 4)
        self.assertEqual(ex4["decision"], "VERIFY_ONLY")
        self.assertEqual(ex4["object_ids"], ["S4600_CH3_EX3_SALES_ORDER_STANDARD"])

    def test_placeholder_preservation_and_blocking(self):
        for item in self.normalized:
            placeholders = {placeholder["field_path"]: placeholder for placeholder in item["placeholders"]}
            for path, value in walk_strings(item["data"]):
                if "##" in value:
                    self.assertIn(path, placeholders, (item["object_id"], path))
                    self.assertEqual(placeholders[path]["raw"], "##")
                    self.assertIsNone(placeholders[path]["resolved"])
                    self.assertEqual(placeholders[path]["status"], "UNRESOLVED")
                    self.assertEqual(item["readiness_status"], "BLOCKED")

    def test_normalized_terminology_and_relative_values(self):
        forbidden = {"organisation_commerciale", "canal_distribution", "secteur_activité", "donneur_ordre"}
        for item in self.normalized:
            self.assertFalse(forbidden.intersection(item["data"]), item["object_id"])
        orders = [item for item in self.normalized if item["object_type"] == "SALES_ORDER"]
        self.assertTrue(any(item["data"]["requested_delivery_date"] ==
                            {"kind": "RELATIVE", "raw": "dans 1 semaine", "offset": "P1W"}
                            for item in orders))
        self.assertFalse(any(isinstance(item["data"]["requested_delivery_date"], str) and
                             item["data"]["requested_delivery_date"].startswith("20") for item in orders))

    def test_dependency_integrity(self):
        by_id = {item["object_id"]: item for item in self.normalized}
        for item in self.normalized:
            for dependency in item["dependencies"]:
                if dependency["status"] == "RESOLVED":
                    self.assertIn(dependency["target_id"], by_id, (item["object_id"], dependency))
                    self.assertEqual(by_id[dependency["target_id"]]["object_type"], dependency["target_type"])
                else:
                    self.assertIsNone(dependency["target_id"])
        cancellation = by_id["S4600_CH9_EX33_BILLING_CANCELLATION_OF_CREDIT_MEMO"]
        self.assertEqual(cancellation["dependencies"][0]["target_id"],
                         "S4600_CH9_EX32_BILLING_CREDIT_MEMO_FROM_REQUEST")

    def test_quantity_and_value_scale_semantics(self):
        by_id = {item["object_id"]: item for item in self.normalized}
        quantity = by_id["S4600_CH4_EX13_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL"]
        value = by_id["S4600_CH4_EX14_PRICING_CONDITION_K007_CUSTOMER_VALUE_SCALE"]
        self.assertEqual(quantity["data"]["scale_basis"], "QUANTITY")
        self.assertEqual([(row["threshold"], row["amount"]) for row in quantity["data"]["scales"]],
                         [(1, 53), (10, 51), (20, 49)])
        self.assertEqual(value["data"]["scale_basis"], "VALUE")
        self.assertEqual([(row["threshold"], row["rate"]) for row in value["data"]["scales"]],
                         [(100, -1), (500, -2), (1000, -3)])

    def test_deterministic_rerun(self):
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/extract_s4600.py")], cwd=ROOT,
                                   check=False, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
