import unittest
from pathlib import Path

from src.provisioning.sap_api_backend import load_operation, root_payload


ROOT = Path(__file__).resolve().parents[1]


class Phase5ProductODataTests(unittest.TestCase):
    def test_product_root_is_seed_driven_and_preserves_book_unit(self):
        operation = load_operation(ROOT / "config/s4615_training_seed.yaml", "PRODUCT_P615_400")
        payload = root_payload(operation)
        self.assertEqual("P615-400", payload["Product"])
        self.assertEqual("PC", payload["BaseUnit"])
        self.assertEqual("FERT", payload["ProductType"])
        self.assertEqual("M", payload["IndustrySector"])
        self.assertNotEqual("289", payload["BaseUnit"])
        self.assertEqual(["1710"], operation["fields"]["plants"]["value"])
        self.assertEqual("1710", operation["fields"]["delivering_plant"]["value"])


if __name__ == "__main__":
    unittest.main()
