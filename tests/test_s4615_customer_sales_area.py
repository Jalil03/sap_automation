import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.execution_policy import target_fingerprint
from src.provisioning.s4615_customer_sales_area import OPERATION, PAYLOAD, TARGET, ensure_sales_area_once
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import HttpResponse


def metadata():
    fields = ''.join(
        f'<edm:Property Name="{name}" Type="Edm.String" Nullable="{str(name not in {"Customer", "SalesOrganization", "DistributionChannel", "Division"}).lower()}"/>'
        for name in PAYLOAD
    )
    return (f'<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx" '
            f'xmlns:edm="http://schemas.microsoft.com/ado/2008/09/edm">'
            f'<edmx:DataServices><edm:Schema Namespace="X"><edm:EntityType Name="Sales">'
            f'<edm:Key>{"".join(f"<edm:PropertyRef Name={json.dumps(x)}/>" for x in ("Customer", "SalesOrganization", "DistributionChannel", "Division"))}</edm:Key>'
            f'{fields}</edm:EntityType><edm:EntityContainer Name="C">'
            f'<edm:EntitySet Name="A_CustomerSalesArea" EntityType="X.Sales"/>'
            f'</edm:EntityContainer></edm:Schema></edmx:DataServices></edmx:Edmx>').encode()


class FakeSap:
    def __init__(self, post_status=201):
        self.created = False
        self.posts = 0
        self.post_status = post_status

    def factory(self, config):
        owner = self

        class Client:
            def request(self, method, path, *, headers=None, body=None):
                if "$metadata" in path:
                    return HttpResponse(200, {}, metadata())
                if "A_CustomerSalesArea(" in path:
                    if owner.created:
                        return HttpResponse(200, {}, json.dumps({"d": PAYLOAD}).encode())
                    return HttpResponse(404, {})
                if method == "GET" and headers and headers.get("X-CSRF-Token") == "Fetch":
                    return HttpResponse(200, {"X-CSRF-Token": "test"})
                if method == "POST":
                    owner.posts += 1
                    assert json.loads(body) == PAYLOAD
                    if owner.post_status == 201:
                        owner.created = True
                    return HttpResponse(owner.post_status, {})
                raise AssertionError((method, path))

        return Client()


class SalesAreaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.approval = self.root / "approval.json"
        self.mapping = self.root / "mapping.json"
        self.checkpoint = self.root / "checkpoint.json"
        self.attempt = self.root / "attempt.json"
        self.document = {
            "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
            "existing_business_partner": "1000000115", "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "approval_scopes_evidenced": ["CUSTOMER_MASTER_OWNER"],
            "approved_scope": ["CUSTOMER_SALES_AREA_1010_10_00"],
            "step_authorizations": {"CUSTOMER_SALES_AREA_1010_10_00": {"execute": True}},
            "sales_area_approved_payload": PAYLOAD,
            "sales_area_target_fingerprint": target_fingerprint(OPERATION, TARGET, PAYLOAD),
            "verified_step_states": {"FLCU01_ROLE": "EXISTS"},
        }
        self.approval.write_text(json.dumps(self.document))
        self.mapping.write_text(json.dumps({"mappings": {"C615-A01": {
            "sap_id": "1000000115", "status": "LIVE_VERIFIED"}}}))
        self.config = SapRuntimeConfig("https://example.invalid", "600", "ABDELJ", "secret")

    def run_once(self, fake):
        return ensure_sales_area_once(self.config, self.approval, self.mapping,
                                      self.checkpoint, self.attempt, fake.factory)

    def test_create_and_independent_readback_once(self):
        fake = FakeSap()
        self.assertEqual("CREATED_AND_VERIFIED", self.run_once(fake)["status"])
        self.assertEqual("VERIFIED", json.loads(self.attempt.read_text())["status"])
        self.assertEqual("EXISTS", self.run_once(fake)["status"])
        self.assertEqual(1, fake.posts)

    def test_unapproved_payload_blocks_before_network(self):
        self.document["sales_area_approved_payload"]["Currency"] = "USD"
        self.approval.write_text(json.dumps(self.document))
        self.assertRaisesRegex(ValueError, "approval", self.run_once, FakeSap())

    def test_rejected_write_is_not_retried(self):
        fake = FakeSap(post_status=400)
        self.assertEqual("BLOCKED", self.run_once(fake)["status"])
        self.assertEqual("BLOCKED", self.run_once(fake)["status"])
        self.assertEqual(1, fake.posts)

    def test_wrong_client_blocks(self):
        fake = FakeSap()
        self.assertRaises(ValueError, ensure_sales_area_once,
                          SapRuntimeConfig("https://example.invalid", "100", "ABDELJ", "secret"),
                          self.approval, self.mapping, self.checkpoint, self.attempt, fake.factory)
        self.assertEqual(0, fake.posts)


if __name__ == "__main__":
    unittest.main()
