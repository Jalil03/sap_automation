import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.customer_bp_root import execute_approved_bp_root_once
from src.provisioning.s4615_implementation import load_contract, target_fingerprint
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import HttpResponse
from tests.test_s4615_adapters import METADATA


class FakeSap:
    def __init__(self, *, duplicate=False, ambiguous=False, readback_ok=True, language_blank=False):
        self.calls = []
        self.duplicate = duplicate
        self.ambiguous = ambiguous
        self.readback_ok = readback_ok
        self.language_blank = language_blank
        self.sessions = 0

    def factory(self, _config):
        self.sessions += 1
        number = self.sessions
        owner = self

        class Client:
            def request(self, method, path, *, headers=None, body=None):
                owner.calls.append((number, method, path, headers or {}, body))
                if "$metadata" in path:
                    return HttpResponse(200, {}, METADATA.encode())
                if method == "GET" and "A_BusinessPartner?" in path:
                    rows = [{"BusinessPartner": "1000009999"}] if owner.duplicate else []
                    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())
                if method == "GET" and path.endswith("?sap-client=600"):
                    return HttpResponse(200, {"X-CSRF-Token": "test-only-token"})
                if method == "POST":
                    if owner.ambiguous:
                        raise AmbiguousTransportError("unknown result")
                    return HttpResponse(201, {}, b'{"d":{"BusinessPartner":"1000009998"}}')
                if method == "GET" and "A_BusinessPartner('1000009998')" in path:
                    fields = {"BusinessPartner": "1000009998",
                              "BusinessPartnerGrouping": "BPAB", "BusinessPartnerCategory": "2",
                              "OrganizationBPName1": "S4615 Training Customer A01",
                              "SearchTerm1": "C615-A01", "Language": "EN"}
                    if not owner.readback_ok:
                        fields["SearchTerm1"] = "OTHER"
                    if owner.language_blank:
                        fields["Language"] = ""
                    return HttpResponse(200, {}, json.dumps({"d": fields}).encode())
                raise AssertionError((method, path))

        return Client()


class BPRootOnceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.approval = self.root / "approval.json"
        self.mapping = self.root / "mappings.json"
        self.attempt = self.root / "attempt.json"
        self.config = SapRuntimeConfig(base_url="https://example.invalid", client="600",
                                       username="ABDELJ", password="test-only")
        op = next(x for x in load_contract()["operations"] if x["id"] == "S4615_CUSTOMER_BP_ROOT")
        self.approval_data = {
            "system": "A4H", "client": "600", "user": "ABDELJ",
            "operation": op["id"], "allow_write": True,
            "approved_by": "REQUESTING_USER_SELF_ATTESTED",
            "authorization_evidence": "USER_REPORTED_SU01D_SAP_ALL_AND_SAP_SYSTEM_A4H_600_ABDELJ",
            "approval_scopes": ["CUSTOMER_MASTER_OWNER"],
            "target_fingerprint": target_fingerprint(op["id"], op["target"], op["values"]),
            "limit": "ONE_BP_ROOT_POST_ONLY",
        }
        self._write_approval()

    def _write_approval(self):
        self.approval.write_text(json.dumps({"S4615_CUSTOMER_BP_ROOT": self.approval_data}))

    def _run(self, fake):
        return execute_approved_bp_root_once(
            config=self.config, approval_path=self.approval, mapping_path=self.mapping,
            attempt_path=self.attempt, transport_factory=fake.factory,
        )

    def test_exactly_one_post_and_fresh_readback_then_mapping(self):
        fake = FakeSap()
        result = self._run(fake)
        self.assertEqual("1000009998", result["sap_id"])
        posts = [call for call in fake.calls if call[1] == "POST"]
        self.assertEqual(1, len(posts))
        self.assertTrue(posts[0][2].endswith("A_BusinessPartner?sap-client=600"))
        self.assertNotIn("BusinessPartner", json.loads(posts[0][4]))
        self.assertEqual(2, fake.sessions)
        self.assertEqual("LIVE_VERIFIED", json.loads(self.mapping.read_text())["mappings"]["C615-A01"]["status"])
        with self.assertRaisesRegex(RuntimeError, "already been attempted"):
            self._run(fake)
        self.assertEqual(1, len([call for call in fake.calls if call[1] == "POST"]))

    def test_approval_failure_prevents_network_and_post(self):
        self.approval_data["approval_scopes"] = []
        self._write_approval()
        fake = FakeSap()
        with self.assertRaises(ValueError):
            self._run(fake)
        self.assertEqual([], fake.calls)

    def test_duplicate_prevents_post(self):
        fake = FakeSap(duplicate=True)
        with self.assertRaisesRegex(RuntimeError, "duplicate"):
            self._run(fake)
        self.assertFalse(self.attempt.exists())
        self.assertFalse(self.mapping.exists())

    def test_ambiguous_post_leaves_attempt_marker_and_never_retries(self):
        fake = FakeSap(ambiguous=True)
        with self.assertRaises(AmbiguousTransportError):
            self._run(fake)
        self.assertEqual("POST_ATTEMPTED", json.loads(self.attempt.read_text())["status"])
        with self.assertRaisesRegex(RuntimeError, "already been attempted"):
            self._run(fake)
        self.assertEqual(1, len([call for call in fake.calls if call[1] == "POST"]))

    def test_failed_independent_readback_never_persists_mapping(self):
        fake = FakeSap(readback_ok=False)
        with self.assertRaisesRegex(RuntimeError, "readback failed"):
            self._run(fake)
        self.assertFalse(self.mapping.exists())
        self.assertTrue(self.attempt.exists())

    def test_nullable_language_mismatch_persists_identity_with_evidence(self):
        fake = FakeSap(language_blank=True)
        result = self._run(fake)
        self.assertEqual("VERIFIED", result["status"])
        evidence = json.loads(self.mapping.read_text())["mappings"]["C615-A01"]["evidence"]
        self.assertEqual("", evidence["observed_language"])
        self.assertEqual("EN", evidence["optional_field_mismatches"]["Language"]["expected"])


if __name__ == "__main__":
    unittest.main()
