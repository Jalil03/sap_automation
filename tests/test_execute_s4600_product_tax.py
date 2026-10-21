import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/execute_s4600_product_tax.py"
SPEC = importlib.util.spec_from_file_location("execute_s4600_product_tax", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ProductTaxExecutorTests(unittest.TestCase):
    def test_all_approved_fingerprints_are_bound_to_payloads(self):
        for logical_id in MODULE.EXPECTED_ROOTS:
            operation, target, payload, fingerprint = MODULE.load_approved(logical_id)
            self.assertEqual(fingerprint, MODULE.target_fingerprint(operation, target, payload))

    def test_checkpoint_blocks_ambiguous_retry(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "checkpoint.json"
            checkpoint = MODULE.ExecutionCheckpoint(path, "S4600_GROUP01_PRODUCT_TAX")
            checkpoint.before_write(MODULE.operation_for("T-D101"))
            self.assertEqual("ATTEMPTED", MODULE.ExecutionCheckpoint(path, "S4600_GROUP01_PRODUCT_TAX").status(
                MODULE.operation_for("T-D101")
            ))

    def test_atomic_json_replaces_complete_document(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "value.json"
            MODULE.atomic_json(path, {"ok": True})
            self.assertEqual({"ok": True}, json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
