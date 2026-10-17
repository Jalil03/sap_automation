import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.identity import (
    load_verified_identity_mappings,
    resolve_sales_order_payload_identities,
)


class RuntimeIdentityTests(unittest.TestCase):
    def test_runtime_config_honors_legacy_verify_ssl_setting(self):
        with patch.dict("os.environ", {
            "SAP_BASE_URL": "https://sap.example.test",
            "SAP_CLIENT": "600",
            "SAP_USERNAME": "ABDELJ",
            "SAP_PASSWORD": "secret",
            "SAP_VERIFY_SSL": "false",
        }, clear=True):
            self.assertFalse(SapRuntimeConfig.from_env().verify_tls)

    def test_resolves_customer_and_material_without_mutating_source(self):
        source = {
            "SoldToParty": "C615-D00",
            "to_Item": [{"Material": "P615-400"}],
        }
        resolved = resolve_sales_order_payload_identities(
            source, {"C615-D00": "1000000114", "P615-400": "10000287"}
        )
        self.assertEqual("1000000114", resolved["SoldToParty"])
        self.assertEqual("10000287", resolved["to_Item"][0]["Material"])
        self.assertEqual("C615-D00", source["SoldToParty"])
        self.assertEqual("P615-400", source["to_Item"][0]["Material"])

    def test_unmapped_values_are_preserved(self):
        source = {"SoldToParty": "EXISTING", "to_Item": [{"Material": "MAT1"}]}
        self.assertEqual(source, resolve_sales_order_payload_identities(source, {}))

    def test_only_live_verified_records_are_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mappings.json"
            path.write_text(json.dumps({"mappings": {
                "C615-D00": {"logical_id": "C615-D00", "sap_id": "1000000114", "status": "LIVE_VERIFIED"},
                "PENDING": {"logical_id": "PENDING", "sap_id": "999", "status": "PENDING"},
            }}), encoding="utf-8")
            self.assertEqual(
                {"C615-D00": "1000000114"}, load_verified_identity_mappings(path)
            )


if __name__ == "__main__":
    unittest.main()
