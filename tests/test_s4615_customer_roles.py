import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.s4615_customer_roles import ensure_roles_once, ensure_roles_after_verified_address
from src.provisioning.execution_policy import ExecutionCheckpoint, target_fingerprint
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import HttpResponse


METADATA = b'''<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx" xmlns:edm="http://schemas.microsoft.com/ado/2008/09/edm" xmlns:sap="http://www.sap.com/Protocols/SAPData"><edmx:DataServices><edm:Schema Namespace="X"><edm:EntityType Name="Role"><edm:Key><edm:PropertyRef Name="BusinessPartner"/><edm:PropertyRef Name="BusinessPartnerRole"/></edm:Key><edm:Property Name="BusinessPartner" Type="Edm.String" Nullable="false"/><edm:Property Name="BusinessPartnerRole" Type="Edm.String" Nullable="false"/></edm:EntityType><edm:EntityContainer Name="C"><edm:EntitySet Name="A_BusinessPartnerRole" EntityType="X.Role"/></edm:EntityContainer></edm:Schema></edmx:DataServices></edmx:Edmx>'''


class FakeSap:
    def __init__(self, ambiguous=False, post_status=201, post_status_by_role=None, address_ready=True):
        self.roles = set()
        self.posts = []
        self.ambiguous = ambiguous
        self.post_status = post_status
        self.post_status_by_role = post_status_by_role or {}
        self.address_ready = address_ready
        self.sessions = 0

    def factory(self, _):
        self.sessions += 1
        owner = self

        class Client:
            def request(self, method, path, *, headers=None, body=None):
                if "$metadata" in path:
                    return HttpResponse(200, {}, METADATA)
                if "A_BusinessPartnerAddress" in path:
                    rows = ([{"BusinessPartner": "1000000115", "AddressID": "1581",
                              "StreetName": "1 Rue de la Formation S4615", "PostalCode": "1000",
                              "CityName": "Bruxelles", "Country": "BE", "Language": "EN"}]
                            if owner.address_ready else [])
                    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())
                if "A_BuPaAddressUsage" in path:
                    rows = ([{"BusinessPartner": "1000000115", "AddressID": "1581",
                              "AddressUsage": "XXDEFAULT", "ValidityStartDate": "/Date(0)/",
                              "ValidityEndDate": "/Date(253402214400000)/"}]
                            if owner.address_ready else [])
                    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())
                if method == "GET" and "A_BusinessPartnerRole(" in path:
                    role = next((r for r in ("FLCU00", "FLCU01") if r in path), None)
                    if role in owner.roles:
                        return HttpResponse(200, {}, json.dumps({"d": {"BusinessPartner": "1000000115", "BusinessPartnerRole": role}}).encode())
                    return HttpResponse(404, {})
                if method == "GET" and headers and headers.get("X-CSRF-Token") == "Fetch":
                    return HttpResponse(200, {"X-CSRF-Token": "test-token"})
                if method == "POST":
                    owner.posts.append(path)
                    role = json.loads(body)["BusinessPartnerRole"]
                    post_status = owner.post_status_by_role.get(role, owner.post_status)
                    if owner.ambiguous:
                        raise AmbiguousTransportError("ambiguous")
                    if post_status in (200, 201, 204):
                        owner.roles.add(role)
                    if post_status == 400:
                        return HttpResponse(400, {"X-Correlation-ID": "TEST-CORR"},
                                            b'{"error":{"code":"BP/400","message":{"value":"Role rejected"}}}')
                    return HttpResponse(post_status, {})
                raise AssertionError((method, path))

        return Client()


class CustomerRoleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.approval = self.root / "approval.json"
        self.mapping = self.root / "mappings.json"
        self.approval.write_text(json.dumps({"environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
            "existing_business_partner": "1000000115", "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "approval_scopes_evidenced": ["CUSTOMER_MASTER_OWNER"],
            "approved_scope": ["FLCU00_ROLE", "FLCU01_ROLE"],
            "role_target_fingerprints": {role: target_fingerprint(
                f"ENSURE_{role}_ROLE_AFTER_ADDRESS" if role == "FLCU00" else "ENSURE_FLCU01_ROLE",
                {"logical_id": "C615-A01", "sap_id": "1000000115"},
                {"BusinessPartner": "1000000115", "BusinessPartnerRole": role})
                for role in ("FLCU00", "FLCU01")},
            "proposed_values": {"roles": ["FLCU00", "FLCU01"]},
            "verified_step_states": {"BP_ADDRESS": "EXISTS_CURRENT_XXDEFAULT"},
            "address_evidence": {"verified_address_id": "1581", "role_error": "FSBP_ECC025: missing standard address"},
            "step_authorizations": {"FLCU00_ROLE": {"execute": True}, "FLCU01_ROLE": {"execute": True}}}))
        self.mapping.write_text(json.dumps({"mappings": {"C615-A01": {"sap_id": "1000000115", "status": "LIVE_VERIFIED"}}}))
        self.config = SapRuntimeConfig("https://example.invalid", "600", "ABDELJ", "test-secret")

    def run_roles(self, fake):
        return ensure_roles_once(self.config, self.approval, self.mapping, self.root, fake.factory)

    def run_reconciled(self, fake):
        return ensure_roles_after_verified_address(
            self.config, self.approval, self.mapping, self.root,
            self.root / "checkpoint.json", fake.factory)

    def prior_rejected_marker(self):
        (self.root / "C615-A01.FLCU00.attempt.json").write_text(json.dumps({
            "logical_id": "C615-A01", "sap_id": "1000000115", "role": "FLCU00",
            "status": "POST_REJECTED_HTTP_400", "independent_readback_http": 404,
            "retry_allowed": False,
        }))

    def lock_rejected_markers(self):
        self.prior_rejected_marker()
        approval = json.loads(self.approval.read_text())
        approval["lock_release_evidence"] = {"bp_id": "1000000115", "user_reported_exit": True}
        approval["role_lock_recovery_fingerprints"] = {role: target_fingerprint(
            f"ENSURE_{role}_ROLE_AFTER_LOCK_RELEASE",
            {"logical_id": "C615-A01", "sap_id": "1000000115"},
            {"BusinessPartner": "1000000115", "BusinessPartnerRole": role})
            for role in ("FLCU00", "FLCU01")}
        self.approval.write_text(json.dumps(approval))
        checkpoint = ExecutionCheckpoint(self.root / "checkpoint.json", "S4615_CUSTOMER_A01")
        for role in ("FLCU00", "FLCU01"):
            operation = f"ENSURE_{role}_ROLE_AFTER_ADDRESS" if role == "FLCU00" else "ENSURE_FLCU01_ROLE"
            checkpoint.record(operation, "REJECTED", detail="R1/084")
            marker = (self.root / ("C615-A01.FLCU00.after_address.attempt.json"
                                   if role == "FLCU00" else "C615-A01.FLCU01.attempt.json"))
            marker.write_text(json.dumps({"logical_id": "C615-A01", "sap_id": "1000000115",
                                          "role": role, "status": "POST_REJECTED_HTTP_400",
                                          "sap_error": {"sap_code": "R1/084"}, "retry_allowed": False}))

    def test_create_once_with_independent_readback_then_skip(self):
        fake = FakeSap()
        self.assertEqual({"FLCU00": "CREATED", "FLCU01": "CREATED"}, self.run_roles(fake))
        self.assertEqual(2, len(fake.posts))
        self.assertEqual(3, fake.sessions)
        self.assertEqual("VERIFIED", json.loads((self.root / "C615-A01.FLCU00.attempt.json").read_text())["status"])
        self.assertEqual({"FLCU00": "EXISTS", "FLCU01": "EXISTS"}, self.run_roles(fake))
        self.assertEqual(2, len(fake.posts))

    def test_scope_failure_prevents_network(self):
        document = json.loads(self.approval.read_text())
        document["approved_scope"].remove("FLCU01_ROLE")
        self.approval.write_text(json.dumps(document))
        fake = FakeSap()
        with self.assertRaises(ValueError):
            self.run_roles(fake)
        self.assertEqual(0, fake.sessions)

    def test_ambiguous_post_is_never_retried(self):
        fake = FakeSap(ambiguous=True)
        with self.assertRaises(AmbiguousTransportError):
            self.run_roles(fake)
        self.assertEqual("POST_ATTEMPTED", json.loads((self.root / "C615-A01.FLCU00.attempt.json").read_text())["status"])
        with self.assertRaisesRegex(RuntimeError, "prior write attempt"):
            self.run_roles(fake)
        self.assertEqual(1, len(fake.posts))

    def test_wrong_identity_prevents_network(self):
        fake = FakeSap()
        with self.assertRaises(ValueError):
            ensure_roles_once(SapRuntimeConfig("https://example.invalid", "100", "ABDELJ", "x"),
                              self.approval, self.mapping, self.root, fake.factory)
        self.assertEqual(0, fake.sessions)

    def test_rejected_post_is_recorded_and_never_retried(self):
        fake = FakeSap(post_status=400)
        with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
            self.run_roles(fake)
        marker = json.loads((self.root / "C615-A01.FLCU00.attempt.json").read_text())
        self.assertEqual("POST_REJECTED_HTTP_400", marker["status"])
        self.assertEqual("BP/400", marker["sap_error"]["sap_code"])
        self.assertEqual("TEST-CORR", marker["sap_error"]["correlation_id"])
        with self.assertRaisesRegex(RuntimeError, "prior write attempt"):
            self.run_roles(fake)
        self.assertEqual(1, len(fake.posts))

    def test_corrected_address_contract_creates_both_roles_once(self):
        self.prior_rejected_marker()
        fake = FakeSap()
        result = self.run_reconciled(fake)
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU00"]["status"])
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU01"]["status"])
        self.assertEqual(2, len(fake.posts))
        self.assertEqual("POST_REJECTED_HTTP_400", json.loads(
            (self.root / "C615-A01.FLCU00.attempt.json").read_text())["status"])
        self.assertEqual("VERIFIED", json.loads(
            (self.root / "C615-A01.FLCU00.after_address.attempt.json").read_text())["status"])
        again = self.run_reconciled(fake)
        self.assertEqual("EXISTS", again["FLCU00"]["status"])
        self.assertEqual(2, len(fake.posts))

    def test_missing_address_blocks_before_role_post(self):
        self.prior_rejected_marker()
        fake = FakeSap(address_ready=False)
        with self.assertRaisesRegex(RuntimeError, "standard address 1581"):
            self.run_reconciled(fake)
        self.assertEqual([], fake.posts)

    def test_changed_role_fingerprint_blocks_before_network(self):
        self.prior_rejected_marker()
        document = json.loads(self.approval.read_text())
        document["role_target_fingerprints"]["FLCU00"] = "wrong"
        self.approval.write_text(json.dumps(document))
        fake = FakeSap()
        with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
            self.run_reconciled(fake)
        self.assertEqual(0, fake.sessions)

    def test_prior_ambiguous_marker_is_not_reconciled(self):
        self.prior_rejected_marker()
        marker = self.root / "C615-A01.FLCU00.attempt.json"
        value = json.loads(marker.read_text())
        value["status"] = "POST_ATTEMPTED"
        marker.write_text(json.dumps(value))
        fake = FakeSap()
        result = self.run_reconciled(fake)
        self.assertEqual("BLOCKED", result["FLCU00"]["status"])
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU01"]["status"])
        self.assertEqual(1, len(fake.posts))

    def test_deterministic_role_failure_does_not_block_independent_role(self):
        self.prior_rejected_marker()
        fake = FakeSap(post_status_by_role={"FLCU00": 400})
        result = self.run_reconciled(fake)
        self.assertEqual("BLOCKED", result["FLCU00"]["status"])
        self.assertEqual("BP/400", result["FLCU00"]["sap_error"]["sap_code"])
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU01"]["status"])
        self.assertEqual(2, len(fake.posts))

    def test_reconciled_lock_rejection_uses_new_one_shot_markers(self):
        self.lock_rejected_markers()
        fake = FakeSap()
        result = self.run_reconciled(fake)
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU00"]["status"])
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU01"]["status"])
        self.assertEqual(2, len(fake.posts))
        self.assertEqual("POST_REJECTED_HTTP_400", json.loads(
            (self.root / "C615-A01.FLCU01.attempt.json").read_text())["status"])
        self.assertEqual("VERIFIED", json.loads(
            (self.root / "C615-A01.FLCU01.after_lock_release.attempt.json").read_text())["status"])
        self.assertEqual("EXISTS", self.run_reconciled(fake)["FLCU00"]["status"])
        self.assertEqual(2, len(fake.posts))

    def test_lock_recovery_without_human_exit_is_blocked(self):
        self.lock_rejected_markers()
        approval = json.loads(self.approval.read_text())
        approval["lock_release_evidence"]["user_reported_exit"] = False
        self.approval.write_text(json.dumps(approval))
        fake = FakeSap()
        result = self.run_reconciled(fake)
        self.assertEqual("BLOCKED", result["FLCU00"]["status"])
        self.assertEqual("BLOCKED", result["FLCU01"]["status"])
        self.assertEqual([], fake.posts)

    def test_lock_recovery_fingerprint_change_is_blocked(self):
        self.lock_rejected_markers()
        approval = json.loads(self.approval.read_text())
        approval["role_lock_recovery_fingerprints"]["FLCU00"] = "wrong"
        self.approval.write_text(json.dumps(approval))
        fake = FakeSap()
        result = self.run_reconciled(fake)
        self.assertEqual("BLOCKED", result["FLCU00"]["status"])
        self.assertEqual("CREATED_AND_VERIFIED", result["FLCU01"]["status"])
        self.assertEqual(1, len(fake.posts))


if __name__ == "__main__":
    unittest.main()
