import unittest
from urllib.parse import parse_qs, urlsplit

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


class _Response:
    status = 200
    headers = {}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return b""


class _Opener:
    def __init__(self):
        self.requests = []

    def open(self, request, timeout):
        self.requests.append(request)
        return _Response()


class SapTransportClientTests(unittest.TestCase):
    def setUp(self):
        config = SapRuntimeConfig("https://sap.example.test:8023", "600", "ABDELJ", "test-secret")
        self.transport = UrllibSapTransport(config)
        self.opener = _Opener()
        self.transport._opener = self.opener

    def test_metadata_adds_client_and_requests_xml(self):
        self.transport.request("GET", "sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata")
        request = self.opener.requests[0]
        self.assertEqual(["600"], parse_qs(urlsplit(request.full_url).query)["sap-client"])
        self.assertEqual("application/xml", request.get_header("Accept"))

    def test_entity_keeps_one_client_and_requests_json(self):
        self.transport.request("GET", "sap/opu/odata/sap/API_BUSINESS_PARTNER/A_Customer?$select=Customer&sap-client=600")
        request = self.opener.requests[0]
        self.assertEqual(["600"], parse_qs(urlsplit(request.full_url).query)["sap-client"])
        self.assertEqual("application/json", request.get_header("Accept"))

    def test_wrong_or_duplicate_client_fails_before_network(self):
        for query in ("sap-client=100", "sap-client=600&sap-client=600"):
            with self.subTest(query=query), self.assertRaises(ValueError):
                self.transport.request("GET", "sap/opu/odata/sap/API_BUSINESS_PARTNER/A_Customer?" + query)
        self.assertFalse(self.opener.requests)

    def test_metadata_cannot_be_forced_to_json(self):
        self.transport.request("GET", "sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata", headers={"Accept": "application/json"})
        self.assertEqual("application/xml", self.opener.requests[0].get_header("Accept"))


if __name__ == "__main__":
    unittest.main()
