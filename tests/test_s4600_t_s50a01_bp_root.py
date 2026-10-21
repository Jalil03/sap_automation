import json
import tempfile
import unittest
from pathlib import Path

from src.provisioning.s4600_t_s50a01_bp_root import (
    OPERATION,
    PAYLOAD,
    REQUIRED_SCOPES,
    execute_once,
    preflight,
    target_fingerprint,
)
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import HttpResponse
from tests.test_s4615_adapters import METADATA


class FakeSap:
    def __init__(self, *, duplicate=False, ambiguous=False):
        self.calls = []
        self.duplicate = duplicate
        self.ambiguous = ambiguous
        self.sessions = 0

    def factory(self, _config):
        self.sessions += 1
        session = self.sessions
        owner = self

        class Client:
            def request(self, method, path, *, headers=None, body=None):
                owner.calls.append((session, method, path, headers or {}, body))
                if "$metadata" in path:
                    return HttpResponse(200, {}, METADATA.encode())
                if method == "GET" and "A_BusinessPartner?" in path:
                    rows = [{"BusinessPartner": "1000009997"}] if owner.duplicate else []
                    return HttpResponse(200, {}, json.dumps({"d": {"results": rows}}).encode())
                if method == "GET" and path.endswith("?sap-client=600"):
                    return HttpResponse(200, {"X-CSRF-Token": "test-token"})
                if method == "POST":
                    if owner.ambiguous:
                        raise AmbiguousTransportError("unknown")
                    self_payload = json.loads(body)
                    assert self_payload == PAYLOAD
                    return HttpResponse(201, {}, b'{"d":{"BusinessPartner":"1000009996"}}')
                if "A_BusinessPartner('1000009996')" in path:
                    row = {"BusinessPartner": "1000009996", **PAYLOAD}
                    return HttpResponse(200, {}, json.dumps({"d": row}).encode())
                raise AssertionError((method, path))

        return Client()


class T50A01RootTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.approval = root / "approval.json"
        self.attempt = root / "attempt.json"
        self.mapping = root / "mappings.json"
        self.mapping.write_text('{"version":1,"mappings":{}}', encoding="utf-8")
        self.config = SapRuntimeConfig(
            base_url="https://example.invalid", client="600", username="ABDELJ", password="test-only"
        )
        self.approval.write_text(json.dumps({OPERATION: {
            "system": "A4H", "client": "600", "user": "ABDELJ", "operation": OPERATION,
            "allow_write": True, "approved_by": "TRAINING_DATA_OWNER",
            "approval_scopes": sorted(REQUIRED_SCOPES), "target_fingerprint": target_fingerprint(),
            "limit": "ONE_BP_ROOT_POST_ONLY",
        }}), encoding="utf-8")

    def run_once(self, fake):
        return execute_once(
            config=self.config, approval_path=self.approval, attempt_path=self.attempt,
            mapping_path=self.mapping, transport_factory=fake.factory,
        )

    def test_one_post_fresh_readback_and_mapping(self):
        fake = FakeSap()
        result = self.run_once(fake)
        self.assertEqual("1000009996", result["sap_id"])
        self.assertEqual(1, len([call for call in fake.calls if call[1] == "POST"]))
        self.assertEqual(2, fake.sessions)
        mapping = json.loads(self.mapping.read_text())["mappings"]["T-S50A01"]
        self.assertEqual("LIVE_VERIFIED", mapping["status"])
        with self.assertRaisesRegex(RuntimeError, "already attempted"):
            self.run_once(fake)

    def test_preflight_is_read_only(self):
        fake = FakeSap()
        result = preflight(
            config=self.config, attempt_path=self.attempt, mapping_path=self.mapping,
            transport_factory=fake.factory,
        )
        self.assertEqual("WRITE_CONTRACT_READY_AWAITING_APPROVAL", result["status"])
        self.assertEqual(0, len([call for call in fake.calls if call[1] == "POST"]))
        self.assertFalse(self.attempt.exists())

    def test_missing_scope_blocks_before_network(self):
        document = json.loads(self.approval.read_text())
        document[OPERATION]["approval_scopes"] = []
        self.approval.write_text(json.dumps(document))
        fake = FakeSap()
        with self.assertRaisesRegex(ValueError, "scopes"):
            self.run_once(fake)
        self.assertEqual([], fake.calls)

    def test_duplicate_blocks_post(self):
        fake = FakeSap(duplicate=True)
        with self.assertRaisesRegex(RuntimeError, "duplicate"):
            self.run_once(fake)
        self.assertFalse(self.attempt.exists())
        self.assertEqual(0, len([call for call in fake.calls if call[1] == "POST"]))

    def test_ambiguous_post_is_never_retried(self):
        fake = FakeSap(ambiguous=True)
        with self.assertRaises(AmbiguousTransportError):
            self.run_once(fake)
        self.assertTrue(self.attempt.exists())
        with self.assertRaisesRegex(RuntimeError, "already attempted"):
            self.run_once(fake)
        self.assertEqual(1, len([call for call in fake.calls if call[1] == "POST"]))


if __name__ == "__main__":
    unittest.main()
