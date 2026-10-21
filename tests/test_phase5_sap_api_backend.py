import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.composite_backend import CompositeBackend
from src.provisioning.phase5 import Phase5ProvisioningEngine, load_seed
from src.provisioning.sap_api_backend import CUSTOMER, PRODUCT, SapApiBackend
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import HttpResponse


ROOT = Path(__file__).resolve().parents[1]
TARGETS = Phase5ProvisioningEngine._targets()


def response(status, row=None, headers=None):
    return HttpResponse(status, headers or {}, json.dumps({"d": row or {}}).encode())


class FakeSap:
    def __init__(self):
        self.root = True
        self.company = False
        self.sales = False
        self.product = False
        self.calls = []
        self.post_error = None
        self.post_error_on = None
        self.drop_readback = False
        self.fresh_count = 0

    def fresh(self, _config):
        self.fresh_count += 1
        return self

    def request(self, method, path, *, headers=None, body=None):
        self.calls.append((method, path))
        if method == "GET" and (headers or {}).get("X-CSRF-Token") == "Fetch":
            return response(200, headers={"X-CSRF-Token": "fake-token"})
        if method == "POST":
            if self.post_error and (self.post_error_on is None or self.post_error_on in path):
                raise self.post_error
            payload = json.loads(body)
            if "/A_CustomerCompany?" in path:
                self.company = payload
            elif "/A_CustomerSalesArea?" in path:
                self.sales = payload
            else:
                raise AssertionError("Unallowlisted POST")
            return response(201)
        if "/A_Customer('" in path:
            return response(200, {"Customer": "1000000114"}) if self.root else response(404)
        if "/A_CustomerCompany(" in path:
            return response(200, self.company) if self.company and not self.drop_readback else response(404)
        if "/A_CustomerSalesArea(" in path:
            return response(200, self.sales) if self.sales else response(404)
        if "/A_Product('" in path:
            return response(200, {"Product": "10000287", "ProductType": "FERT", "IndustrySector": "M",
                                  "BaseUnit": "PC", "Division": "00"}) if self.product else response(404)
        raise AssertionError(f"Unexpected request: {method} {path}")


class SapApiBackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.mapping_path = Path(self.temp.name) / "mappings.json"
        self.fake = FakeSap()
        self.config = SapRuntimeConfig("https://example.invalid", "600", "ABDELJ", "dummy")
        self.backend = SapApiBackend(
            config=self.config, transport=self.fake, transport_factory=self.fake.fresh,
            mapping_path=self.mapping_path,
        )
        self.values = load_seed(ROOT / "config/s4615_training_seed.yaml")[CUSTOMER]

    def test_customer_missing_extensions_then_post_once_and_fresh_readback(self):
        self.assertEqual("MISSING", self.backend.lookup(CUSTOMER, TARGETS[CUSTOMER]))
        self.assertEqual({"accepted": True, "service": "API_BUSINESS_PARTNER"},
                         self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values))
        result = self.backend.readback(CUSTOMER, TARGETS[CUSTOMER])
        self.assertEqual("1000000114", result["sap_partner_id"])
        self.assertEqual("1000000114", json.loads(self.mapping_path.read_text())["mappings"]["C615-D00"]["sap_id"])
        self.assertEqual(2, sum(method == "POST" for method, _ in self.fake.calls))
        self.assertGreater(self.fake.fresh_count, 0)
        self.assertEqual("EXISTS", self.backend.lookup(CUSTOMER, TARGETS[CUSTOMER]))
        self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values)
        self.assertEqual(2, sum(method == "POST" for method, _ in self.fake.calls))

    def test_customer_missing_root_is_unknown_and_never_posts(self):
        self.fake.root = False
        self.assertEqual("UNKNOWN", self.backend.lookup(CUSTOMER, TARGETS[CUSTOMER]))
        result = self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values)
        self.assertTrue(result["provisioning_blocked"])
        self.assertFalse(any(method == "POST" for method, _ in self.fake.calls))

    def test_customer_partial_post_failure_never_retries(self):
        self.fake.post_error = AmbiguousTransportError("timeout")
        with self.assertRaisesRegex(RuntimeError, "do not retry"):
            self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values)
        self.assertEqual(1, sum(method == "POST" for method, _ in self.fake.calls))
        self.assertFalse(self.mapping_path.exists())

    def test_second_post_failure_preserves_first_write_and_stops(self):
        self.fake.post_error = AmbiguousTransportError("timeout")
        self.fake.post_error_on = "A_CustomerSalesArea"
        with self.assertRaisesRegex(RuntimeError, "do not retry"):
            self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values)
        self.assertTrue(self.fake.company)
        self.assertFalse(self.fake.sales)
        self.assertEqual(2, sum(method == "POST" for method, _ in self.fake.calls))
        self.assertFalse(self.mapping_path.exists())

    def test_failed_fresh_readback_stops_without_second_post(self):
        self.fake.drop_readback = True
        with self.assertRaisesRegex(RuntimeError, "readback failed"):
            self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], self.values)
        self.assertEqual(1, sum(method == "POST" for method, _ in self.fake.calls))
        self.assertFalse(self.mapping_path.exists())

    def test_customer_mismatched_decision_and_mapping_fail_closed(self):
        changed = dict(self.values, reconciliation_account="999999")
        with self.assertRaisesRegex(ValueError, "decision mismatch"):
            self.backend.provision(CUSTOMER, TARGETS[CUSTOMER], changed)
        self.assertFalse(any(method == "POST" for method, _ in self.fake.calls))
        self.mapping_path.write_text(json.dumps({"mappings": {"C615-D00": {"sap_id": "wrong", "status": "LIVE_VERIFIED"}}}))
        with self.assertRaisesRegex(RuntimeError, "conflicts with seed"):
            self.backend.lookup(CUSTOMER, TARGETS[CUSTOMER])

    def test_product_root_lookup_readback_and_create_blocked(self):
        self.mapping_path.write_text(json.dumps({"mappings": {"P615-400": {"sap_id": "10000287", "status": "LIVE_VERIFIED"}}}))
        self.assertEqual("MISSING", self.backend.lookup(PRODUCT, TARGETS[PRODUCT]))
        self.assertTrue(self.backend.provision(PRODUCT, TARGETS[PRODUCT], {})["provisioning_blocked"])
        self.assertFalse(any(method == "POST" for method, _ in self.fake.calls))
        self.fake.product = True
        self.assertEqual("EXISTS", self.backend.lookup(PRODUCT, TARGETS[PRODUCT]))
        self.assertEqual("10000287", self.backend.readback(PRODUCT, TARGETS[PRODUCT])["sap_product_id"])

    def test_wrong_identity_target_and_operation_blocked_before_request(self):
        backend = SapApiBackend(config=SapRuntimeConfig("https://example.invalid", "601", "ABDELJ", "dummy"),
                                transport=self.fake, mapping_path=self.mapping_path)
        with self.assertRaisesRegex(ValueError, "client 600"):
            backend.lookup(CUSTOMER, TARGETS[CUSTOMER])
        with self.assertRaisesRegex(ValueError, "target mismatch"):
            self.backend.lookup(CUSTOMER, {"partner_id": "other"})
        with self.assertRaisesRegex(ValueError, "No API route"):
            self.backend.lookup("UNKNOWN", {})
        wrong_user = SapApiBackend(config=SapRuntimeConfig("https://example.invalid", "600", "OTHER", "dummy"),
                                   transport=self.fake, mapping_path=self.mapping_path)
        with self.assertRaisesRegex(ValueError, "user ABDELJ"):
            wrong_user.lookup(CUSTOMER, TARGETS[CUSTOMER])

    def test_registry_mismatch_blocks_before_request(self):
        registry = Path(self.temp.name) / "registry.json"
        registry.write_text(json.dumps({"object_types": {"BUSINESS_PARTNER": {"candidates": []}}}))
        backend = SapApiBackend(config=self.config, transport=self.fake, registry_path=registry,
                                mapping_path=self.mapping_path)
        with self.assertRaisesRegex(ValueError, "not evidenced"):
            backend.lookup(CUSTOMER, TARGETS[CUSTOMER])
        self.assertEqual([], self.fake.calls)

    def test_engine_dry_run_does_not_post(self):
        engine = Phase5ProvisioningEngine(backend=self.backend, decisions=load_seed(), execute=False)
        result = engine._ensure(CUSTOMER)
        self.assertEqual("WOULD_PROVISION", result.status)
        self.assertFalse(any(method == "POST" for method, _ in self.fake.calls))
        self.assertFalse(self.mapping_path.exists())

    def test_existing_mapping_evidence_is_not_overwritten(self):
        original = {"version": 1, "mappings": {"C615-D00": {
            "sap_id": "1000000114", "status": "LIVE_VERIFIED", "evidence": {"address": "1557"},
        }}}
        self.mapping_path.write_text(json.dumps(original))
        from src.provisioning.sap_api_backend import persist_mapping
        persist_mapping(self.mapping_path, "C615-D00", "1000000114", {"company_readback": "EXISTS"})
        self.assertEqual(original, json.loads(self.mapping_path.read_text()))


class CompositeBackendTests(unittest.TestCase):
    def test_routes_explicitly_and_blocks_unknown(self):
        class Stub:
            def __init__(self): self.calls = []
            def lookup(self, operation, target): self.calls.append(("lookup", operation)); return "EXISTS"
            def provision(self, operation, target, values): self.calls.append(("provision", operation)); return {"accepted": True}
            def readback(self, operation, target): self.calls.append(("readback", operation)); return target
        api, gui = Stub(), Stub()
        backend = CompositeBackend(api=api, gui=gui)
        self.assertEqual("EXISTS", backend.lookup(CUSTOMER, TARGETS[CUSTOMER]))
        self.assertEqual("EXISTS", backend.lookup("COMPANY_CODE_1010", TARGETS["COMPANY_CODE_1010"]))
        backend.provision(PRODUCT, TARGETS[PRODUCT], {})
        backend.readback("SALES_ORGANIZATION_1010", TARGETS["SALES_ORGANIZATION_1010"])
        self.assertEqual(2, len(api.calls))
        self.assertEqual(2, len(gui.calls))
        with self.assertRaisesRegex(ValueError, "No proven"):
            backend.lookup("UNSUPPORTED", {})


if __name__ == "__main__":
    unittest.main()
