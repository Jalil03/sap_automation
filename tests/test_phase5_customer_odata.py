import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.sap_api_backend import customer_payloads, load_operation, persist_mapping


ROOT = Path(__file__).resolve().parents[1]


class Phase5CustomerODataTests(unittest.TestCase):
    def test_seed_drives_customer_payloads(self):
        operation = load_operation(ROOT / "config/s4615_training_seed.yaml", "CUSTOMER_C615_D00")
        company, sales = customer_payloads(operation)
        self.assertEqual("1000000114", company["Customer"])
        self.assertEqual("400000", company["ReconciliationAccount"])
        self.assertEqual("1010", sales["SalesOrganization"])
        self.assertEqual("10", sales["DistributionChannel"])
        self.assertEqual("00", sales["Division"])

    def test_mapping_persistence_is_idempotent_and_conflict_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mappings.json"
            evidence = {"company_readback": "EXISTS", "sales_area_readback": "EXISTS"}
            persist_mapping(path, "C615-D00", "1000000114", evidence)
            persist_mapping(path, "C615-D00", "1000000114", evidence)
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("1000000114", saved["mappings"]["C615-D00"]["sap_id"])
            with self.assertRaisesRegex(RuntimeError, "mapping conflict"):
                persist_mapping(path, "C615-D00", "1000000999", evidence)


if __name__ == "__main__":
    unittest.main()
