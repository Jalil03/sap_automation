import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.execution_policy import target_fingerprint
from src.provisioning.s4615_customer_company import OPERATION, PAYLOAD, TARGET, ensure_company_once
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import HttpResponse


METADATA = b'''<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx" xmlns:edm="http://schemas.microsoft.com/ado/2008/09/edm"><edmx:DataServices><edm:Schema Namespace="X"><edm:EntityType Name="Company"><edm:Key><edm:PropertyRef Name="Customer"/><edm:PropertyRef Name="CompanyCode"/></edm:Key><edm:Property Name="Customer" Type="Edm.String" Nullable="false" MaxLength="10"/><edm:Property Name="CompanyCode" Type="Edm.String" Nullable="false" MaxLength="4"/><edm:Property Name="ReconciliationAccount" Type="Edm.String" MaxLength="10"/><edm:Property Name="PaymentTerms" Type="Edm.String" MaxLength="4"/></edm:EntityType><edm:EntityContainer Name="C"><edm:EntitySet Name="A_CustomerCompany" EntityType="X.Company"/></edm:EntityContainer></edm:Schema></edmx:DataServices></edmx:Edmx>'''


class FakeSap:
    def __init__(self, post_status=201):
        self.exists = False
        self.posts = 0
        self.post_status = post_status

    def factory(self, config):
        owner = self

        class Client:
            def request(self, method, path, *, headers=None, body=None):
                if "$metadata" in path:
                    return HttpResponse(200, {}, METADATA)
                if "A_CustomerCompany(" in path:
                    if owner.exists:
                        return HttpResponse(200, {}, json.dumps({"d": PAYLOAD}).encode())
                    return HttpResponse(404, {})
                if method == "GET" and headers and headers.get("X-CSRF-Token") == "Fetch":
                    return HttpResponse(200, {"X-CSRF-Token": "test"})
                if method == "POST":
                    owner.posts += 1
                    assert json.loads(body) == PAYLOAD
                    if owner.post_status == 201:
                        owner.exists = True
                    return HttpResponse(owner.post_status, {})
                raise AssertionError((method, path))

        return Client()


class CompanyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.approval = self.root / "approval.json"
        self.mapping = self.root / "mapping.json"
        self.checkpoint = self.root / "checkpoint.json"
        self.attempt = self.root / "attempt.json"
        env = {"system": "A4H", "client": "600", "user": "ABDELJ"}
        fi_approval = {"environment": env, "operation": OPERATION, "scope": "FI_MM",
                       "approved_by": "USER_FI_OWNER", "authorization_evidence": "Scoped FI approval"}
        self.document = {
            "environment": env, "existing_business_partner": "1000000115",
            "step_authorizations": {"CUSTOMER_COMPANY_1010": {"execute": True}},
            "proposed_values": {"reconciliation_account": {"value": "400000"},
                                "payment_terms": {"value": "0004"}},
            "verified_step_states": {"CUSTOMER_SALES_AREA_1010_10_00": "EXISTS", "FLCU00_ROLE": "EXISTS"},
            "company_extension_policy": {
                "mode": "AUTONOMOUS_TRAINING", "workflow_id": "S4615_CUSTOMER_A01", "environment": env,
                "approval": {"workflow_id": "S4615_CUSTOMER_A01", "environment": env,
                             "approved_by": "USER_FI_OWNER", "authorization_evidence": "Scoped FI approval",
                             "operations": [OPERATION], "scopes": ["FI_MM"],
                             "target_fingerprints": {OPERATION: target_fingerprint(OPERATION, TARGET, PAYLOAD)}},
                "operation_scopes": {OPERATION: "FI_MM"},
                "route_evidence": {OPERATION: "Installed metadata and controlled first write"},
                "sensitive_approvals": {OPERATION: fi_approval},
            },
        }
        self.approval.write_text(json.dumps(self.document))
        self.mapping.write_text(json.dumps({"mappings": {"C615-A01": {
            "sap_id": "1000000115", "status": "LIVE_VERIFIED"}}}))
        self.config = SapRuntimeConfig("https://example.invalid", "600", "ABDELJ", "secret")

    def run_once(self, fake):
        return ensure_company_once(self.config, self.approval, self.mapping,
                                   self.checkpoint, self.attempt, fake.factory)

    def test_exact_first_write_and_independent_readback(self):
        fake = FakeSap()
        self.assertEqual("CREATED_AND_VERIFIED", self.run_once(fake)["status"])
        self.assertEqual("VERIFIED", json.loads(self.attempt.read_text())["status"])
        self.assertEqual("EXISTS", self.run_once(fake)["status"])
        self.assertEqual(1, fake.posts)

    def test_missing_fi_approval_blocks_before_network(self):
        self.document["company_extension_policy"]["sensitive_approvals"] = {}
        self.approval.write_text(json.dumps(self.document))
        fake = FakeSap()
        with self.assertRaisesRegex(ValueError, "Separate FI_MM approval missing"):
            self.run_once(fake)
        self.assertEqual(0, fake.posts)

    def test_changed_value_fingerprint_blocks(self):
        self.document["company_extension_policy"]["approval"]["target_fingerprints"][OPERATION] = "wrong"
        self.approval.write_text(json.dumps(self.document))
        fake = FakeSap()
        with self.assertRaisesRegex(ValueError, "Scoped workflow approval missing"):
            self.run_once(fake)
        self.assertEqual(0, fake.posts)

    def test_rejected_write_is_not_retried(self):
        fake = FakeSap(post_status=400)
        self.assertEqual("BLOCKED", self.run_once(fake)["status"])
        self.assertEqual("BLOCKED", self.run_once(fake)["status"])
        self.assertEqual(1, fake.posts)


if __name__ == "__main__":
    unittest.main()
