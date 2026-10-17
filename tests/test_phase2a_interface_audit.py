import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_sap_interfaces import build_registry, render_registry  # noqa: E402


class Phase2AInterfaceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = build_registry()
        cls.entries = cls.registry["object_types"]
        cls.canonical = json.loads((ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8"))

    def test_every_canonical_type_is_covered_once(self):
        canonical_types = {obj["object_type"] for obj in self.canonical["objects"]}
        self.assertEqual(canonical_types, set(self.entries))
        self.assertEqual(39, len(self.entries))

    def test_candidate_classifications_are_contract_values(self):
        allowed = set(self.registry["allowed_candidate_classifications"])
        for entry in self.entries.values():
            self.assertTrue(entry["candidates"])
            for candidate in entry["candidates"]:
                self.assertIn(candidate["classification"], allowed)

    def test_named_candidates_have_exact_inventory_evidence(self):
        for entry in self.entries.values():
            for candidate in entry["candidates"]:
                if candidate["classification"] not in {"NO_INTERFACE_FOUND", "NO_EXECUTION_REQUIRED"}:
                    self.assertIsNotNone(candidate["exact_name"])
                    self.assertIn(candidate["inventory"], {"odata_services.xlsx", "rfc_remote_functions.xlsx"})

    def test_preferred_interface_is_a_declared_candidate(self):
        for entry in self.entries.values():
            self.assertIn(entry["preferred_interface"], entry["candidates"])

    def test_unresolved_types_are_explicit(self):
        unresolved = {name for name, item in self.entries.items() if item["resolution"] == "UNRESOLVED"}
        self.assertEqual(
            {
                "ACCESS_SEQUENCE", "ACCOUNT_DETERMINATION", "CONDITION_TABLE",
                "COPY_CONTROL", "EXTENSION_CONFIGURATION", "OUTPUT_DETERMINATION",
                "PRICING_PROCEDURE_DETERMINATION", "SHARED_MASTER_DATA_ASSIGNMENT",
                "TEXT_DETERMINATION",
            },
            unresolved,
        )

    def test_no_sap_connection_or_mapper_claim(self):
        self.assertFalse(self.registry["sap_connection_performed"])
        self.assertFalse(self.registry["mapper_implemented"])

    def test_registry_is_deterministic_and_current(self):
        path = ROOT / "mappings/sap/interface_registry.yaml"
        self.assertEqual(render_registry(self.registry), path.read_text(encoding="utf-8"))
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_sap_interfaces.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr or completed.stdout)


if __name__ == "__main__":
    unittest.main()
