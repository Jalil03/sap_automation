import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.sap_runtime.cli import _confirmed
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError, ConfigurationError, PreflightBlocked
from src.sap_runtime.ledger import ExecutionLedger
from src.sap_runtime.models import CheckResult, ExecutionStatus
from src.sap_runtime.prechecks import ConfiguredDependencyVerifier, REQUIRED_PROBES
from src.sap_runtime.sales_order import SalesOrderRuntime
from src.sap_runtime.security import sanitize_error
from src.sap_runtime.transport import HttpResponse


ROOT = Path(__file__).resolve().parents[1]
OBJECT_ID = "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT"
REFERENCE = "TECH-PILOT-002"
ORDER_DATE = "2026-10-13"


def response(status=200, value=None, headers=None):
    return HttpResponse(
        status=status,
        headers=headers or {},
        body=json.dumps(value or {}).encode("utf-8"),
    )


class PassingVerifier:
    def verify(self, payload, transport):
        return [CheckResult("DEPENDENCIES", "PASS", "mocked read-only master checks")]


class BlockingVerifier:
    def verify(self, payload, transport):
        return [CheckResult("DEPENDENCY_MATERIAL", "BLOCKED", "mocked missing material")]


class FakeTransport:
    def __init__(self, *, post_status=201, post_timeout=False, mismatch=False, duplicate=False, csrf_token=True):
        self.post_status = post_status
        self.post_timeout = post_timeout
        self.mismatch = mismatch
        self.duplicate = duplicate
        self.csrf_token = csrf_token
        self.calls = []

    def request(self, method, path, *, headers=None, body=None):
        headers = dict(headers or {})
        self.calls.append({"method": method, "path": path, "headers": headers, "body": body})
        if method == "POST":
            if self.post_timeout:
                raise AmbiguousTransportError("password=secret X-CSRF-Token: super-secret")
            if self.post_status != 201:
                return HttpResponse(
                    self.post_status,
                    {},
                    b'{"error":"password=secret Authorization: abc X-CSRF-Token: xyz"}',
                )
            return response(
                201, {"d": {"SalesOrder": "148"}},
                {"ETag": 'W/"created"', "Location": "A_SalesOrder('148')"},
            )
        if headers.get("X-CSRF-Token") == "Fetch":
            token_headers = {"X-CSRF-Token": "mock-token"} if self.csrf_token else {}
            return response(200, {"d": {}}, token_headers)
        if "$top=1" in path:
            return response(200, {"d": {"results": [{"SalesOrder": "148"}]}})
        if "$filter=" in path and "A_SalesOrder?" in path:
            rows = [{"SalesOrder": "148"}] if self.duplicate else []
            return response(200, {"d": {"results": rows}})
        if "A_SalesOrder('148')" in path:
            sold_to = "WRONG" if self.mismatch else "C615-A00"
            return response(200, {"d": {
                "SalesOrder": "148", "SalesOrderType": "OR", "SalesOrganization": "1010",
                "DistributionChannel": "10", "OrganizationDivision": "00",
                "SoldToParty": sold_to, "PurchaseOrderByCustomer": REFERENCE,
                "CustomerPurchaseOrderDate": "/Date(1791849600000)/",
                "CustomerPaymentTerms": "0004", "TransactionCurrency": "USD",
                "TotalNetAmount": "35.35",
            }})
        if "A_SalesOrderItem" in path:
            return response(200, {"d": {"results": [{
                "SalesOrderItem": "10", "Material": "P615-100",
                "RequestedQuantity": "10", "RequestedQuantityUnit": "PC",
                "RequestedQuantitySAPUnit": "ST", "RequestedQuantityISOUnit": "PCE",
                "ProductionPlant": "1710", "ShippingPoint": "1710",
            }]}})
        if "A_SalesOrderHeaderPartner" in path:
            return response(200, {"d": {"results": [{
                "PartnerFunction": "DO", "PartnerFunctionInternalCode": "AG",
                "Customer": "C615-A00",
            }]}})
        raise AssertionError(f"Unexpected request: {method} {path}")


class Phase3BSalesOrderRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = SapRuntimeConfig(
            base_url="https://sap.invalid",
            client="600",
            username="runtime-user",
            password="runtime-password",
            ledger_path=Path(self.temp.name) / "ledger.sqlite3",
        )

    def runtime(self, transport):
        return SalesOrderRuntime(
            config=self.config,
            transport=transport,
            ledger=ExecutionLedger(self.config.ledger_path),
            dependency_verifier=PassingVerifier(),
        )

    def dry_run(self, runtime):
        return runtime.dry_run(
            OBJECT_ID,
            customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )

    def test_minimal_payload_builder_uses_odata_v2_decimal_and_date(self):
        runtime = self.runtime(FakeTransport())
        _, payload = runtime.build_payload(
            OBJECT_ID,
            customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        self.assertEqual("10", payload["to_Item"][0]["RequestedQuantity"])
        self.assertEqual("/Date(1791849600000)/", payload["CustomerPurchaseOrderDate"])
        self.assertEqual(REFERENCE, payload["PurchaseOrderByCustomer"])
        self.assertNotIn("CustomerPaymentTerms", payload)
        self.assertNotIn("to_Partner", payload)
        self.assertTrue({"SalesOrderItem", "Material", "RequestedQuantity", "RequestedQuantityUnit"} == set(payload["to_Item"][0]))

    def test_dry_run_checks_get_dependencies_duplicate_and_never_posts(self):
        transport = FakeTransport()
        result = self.dry_run(self.runtime(transport))
        self.assertEqual(ExecutionStatus.DRY_RUN_OK, result.status)
        self.assertFalse(any(call["method"] == "POST" for call in transport.calls))
        self.assertTrue(any("$filter=" in call["path"] for call in transport.calls))

    def test_duplicate_blocks_without_post(self):
        transport = FakeTransport(duplicate=True)
        result = self.dry_run(self.runtime(transport))
        self.assertEqual(ExecutionStatus.DUPLICATE, result.status)
        self.assertFalse(any(call["method"] == "POST" for call in transport.calls))

    def test_failed_dependency_blocks_without_post(self):
        transport = FakeTransport()
        runtime = SalesOrderRuntime(
            config=self.config, transport=transport,
            ledger=ExecutionLedger(self.config.ledger_path),
            dependency_verifier=BlockingVerifier(),
        )
        result = self.dry_run(runtime)
        self.assertEqual(ExecutionStatus.BLOCKED, result.status)
        self.assertFalse(any(call["method"] == "POST" for call in transport.calls))

    def test_execute_requires_successful_exact_dry_run(self):
        runtime = self.runtime(FakeTransport())
        with self.assertRaises(PreflightBlocked):
            runtime.execute(
                OBJECT_ID, customer_reference=REFERENCE,
                customer_purchase_order_date=ORDER_DATE,
            )

    def test_http_201_runs_one_post_and_verified_read_back(self):
        transport = FakeTransport()
        runtime = self.runtime(transport)
        self.assertEqual(ExecutionStatus.DRY_RUN_OK, self.dry_run(runtime).status)
        result = runtime.execute(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        self.assertEqual(ExecutionStatus.VERIFIED, result.status)
        self.assertEqual("148", result.created_sales_order_id)
        posts = [call for call in transport.calls if call["method"] == "POST"]
        self.assertEqual(1, len(posts))
        self.assertEqual("mock-token", posts[0]["headers"]["X-CSRF-Token"])
        self.assertTrue(any(call["headers"].get("X-CSRF-Token") == "Fetch" for call in transport.calls))

    def test_missing_csrf_token_blocks_without_post(self):
        transport = FakeTransport(csrf_token=False)
        runtime = self.runtime(transport)
        self.dry_run(runtime)
        result = runtime.execute(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        self.assertEqual(ExecutionStatus.BLOCKED, result.status)
        self.assertFalse(any(call["method"] == "POST" for call in transport.calls))

    def test_http_400_403_and_500_fail_without_retry(self):
        for status in (400, 403, 500):
            with self.subTest(status=status):
                transport = FakeTransport(post_status=status)
                runtime = self.runtime(transport)
                self.dry_run(runtime)
                result = runtime.execute(
                    OBJECT_ID, customer_reference=REFERENCE,
                    customer_purchase_order_date=ORDER_DATE,
                )
                self.assertEqual(ExecutionStatus.FAILED, result.status)
                self.assertEqual(status, result.http_status)
                self.assertEqual(1, sum(call["method"] == "POST" for call in transport.calls))

    def test_timeout_after_submission_is_ambiguous_and_not_retried(self):
        transport = FakeTransport(post_timeout=True)
        runtime = self.runtime(transport)
        self.dry_run(runtime)
        result = runtime.execute(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        self.assertEqual(ExecutionStatus.AMBIGUOUS, result.status)
        self.assertEqual(1, sum(call["method"] == "POST" for call in transport.calls))
        self.assertNotIn("super-secret", result.sanitized_error)
        self.assertNotIn("secret", json.dumps(runtime.ledger.rows()).lower())

    def test_read_back_mismatch_is_failed(self):
        transport = FakeTransport(mismatch=True)
        runtime = self.runtime(transport)
        self.dry_run(runtime)
        result = runtime.execute(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        self.assertEqual(ExecutionStatus.FAILED, result.status)
        self.assertEqual("148", result.created_sales_order_id)
        self.assertIn("SoldToParty", result.sanitized_error)

    def test_reserved_and_nonunique_references_are_rejected(self):
        runtime = self.runtime(FakeTransport())
        for reference in ("TECH-PILOT-001", "4712"):
            _, payload = runtime.build_payload(
                OBJECT_ID, customer_reference=reference,
                customer_purchase_order_date=ORDER_DATE,
            )
            # Seed an exact dry run only to reach the execute-specific reference gate.
            result = runtime.dry_run(
                OBJECT_ID, customer_reference=reference,
                customer_purchase_order_date=ORDER_DATE,
            )
            self.assertEqual(ExecutionStatus.DRY_RUN_OK, result.status)
            with self.assertRaises(PreflightBlocked):
                runtime.execute(
                    OBJECT_ID, customer_reference=reference,
                    customer_purchase_order_date=ORDER_DATE,
                )
            self.assertTrue(payload)

    def test_sensitive_values_are_sanitized(self):
        value = sanitize_error(
            "password=real-secret Authorization: BasicABC X-CSRF-Token: token123 Cookie: session456"
        )
        for secret in ("real-secret", "BasicABC", "token123", "session456"):
            self.assertNotIn(secret, value)

    def test_cli_confirmation_interactive_and_ci(self):
        args = type("Args", (), {
            "non_interactive_approved": False,
            "object_id": OBJECT_ID,
            "customer_reference": REFERENCE,
            "approval_id": None,
        })()
        with patch("builtins.input", return_value=f"EXECUTE {OBJECT_ID} {REFERENCE}"):
            self.assertTrue(_confirmed(args, self.config))
        args.non_interactive_approved = True
        args.approval_id = "CHANGE-123"
        ci_config = SapRuntimeConfig(**{**self.config.__dict__, "ci_approval_id": "CHANGE-123"})
        self.assertTrue(_confirmed(args, ci_config))

    def test_configured_master_prechecks_are_read_only_and_client_scoped(self):
        probes = [
            {"name": name, "path_template": f"/lookup/{name}/{{{name}}}"}
            for name in sorted(REQUIRED_PROBES)
        ]
        verifier = ConfiguredDependencyVerifier(probes, client="600")

        class ProbeTransport:
            def __init__(self):
                self.calls = []

            def request(self, method, path, *, headers=None, body=None):
                self.calls.append((method, path, body))
                return response(200, {"d": {"results": [{"exists": True}]}})

        transport = ProbeTransport()
        _, payload = self.runtime(FakeTransport()).build_payload(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        payload["to_Item"].append({
            "SalesOrderItem": "20", "Material": "SECOND-MATERIAL",
            "RequestedQuantity": "1", "RequestedQuantityUnit": "KG",
        })
        results = verifier.verify(payload, transport)
        self.assertEqual(7, len(results))
        self.assertTrue(all(result.status == "PASS" for result in results))
        self.assertEqual(9, len(transport.calls))
        self.assertTrue(all(method == "GET" and body is None for method, _, body in transport.calls))
        self.assertTrue(all("sap-client=600" in path for _, path, _ in transport.calls))
        with self.assertRaises(ConfigurationError):
            ConfiguredDependencyVerifier(probes[:-1], client="600")

    def test_unverified_prechecks_fail_closed_without_requests(self):
        config = json.loads(
            (ROOT / "config/sap_sales_order_prechecks.example.json").read_text(encoding="utf-8")
        )
        verifier = ConfiguredDependencyVerifier(config["probes"], client="600")

        class NoRequestTransport:
            def request(self, method, path, *, headers=None, body=None):
                raise AssertionError("NEEDS_LIVE_VALIDATION must not call an endpoint")

        _, payload = self.runtime(FakeTransport()).build_payload(
            OBJECT_ID, customer_reference=REFERENCE,
            customer_purchase_order_date=ORDER_DATE,
        )
        results = verifier.verify(payload, NoRequestTransport())
        self.assertEqual(7, len(results))
        self.assertTrue(all(result.status == "BLOCKED" for result in results))
        self.assertTrue(all("NEEDS_LIVE_VALIDATION" in result.detail for result in results))

    def test_precheck_audit_contract_is_complete_and_explicit(self):
        config = json.loads(
            (ROOT / "config/sap_sales_order_prechecks.example.json").read_text(encoding="utf-8")
        )
        self.assertEqual(REQUIRED_PROBES, {probe["name"] for probe in config["probes"]})
        self.assertEqual(7, len(config["probes"]))
        required = {
            "canonical_paths", "payload_paths", "status", "service", "entity_set",
            "key_or_filter", "path_template", "expected_result", "on_not_found",
            "on_interface_unavailable", "evidence_note",
        }
        for probe in config["probes"]:
            with self.subTest(probe=probe["name"]):
                self.assertTrue(required <= set(probe))
                self.assertEqual("NEEDS_LIVE_VALIDATION", probe["status"])
                self.assertEqual("BLOCKED", probe["on_not_found"])
                self.assertEqual("BLOCKED", probe["on_interface_unavailable"])


if __name__ == "__main__":
    unittest.main()
