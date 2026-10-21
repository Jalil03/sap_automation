import json
import unittest

from src.sap_runtime.transport import HttpResponse


class SanitizedSapErrorTests(unittest.TestCase):
    def test_json_error_code_message_and_transaction_id(self):
        body = json.dumps({"error": {"code": "BUS/123", "message": {"value": "Role rejected"},
                                      "innererror": {"transactionid": "ABC123"}}}).encode()
        self.assertEqual({"http_status": 400, "sap_code": "BUS/123", "sap_message": "Role rejected",
                          "correlation_id": "ABC123"}, HttpResponse(400, {}, body).sanitized_sap_error())
        self.assertEqual("BUS/123", HttpResponse(400, {}, body).error_evidence["sap_code"])
        self.assertIsNone(HttpResponse(200, {}, body).error_evidence)

    def test_xml_error_and_header_correlation(self):
        response = HttpResponse(400, {"X-Correlation-ID": "XYZ"},
                                b"<error><code>ABC</code><message>Invalid role</message></error>")
        self.assertEqual("ABC", response.sanitized_sap_error()["sap_code"])
        self.assertEqual("XYZ", response.sanitized_sap_error()["correlation_id"])

    def test_secrets_are_redacted_and_malformed_body_not_retained(self):
        body = json.dumps({"error": {"code": "X", "message": {"value": "Authorization: Basic abc123 password=hidden token=secret"}}}).encode()
        evidence = HttpResponse(400, {}, body).sanitized_sap_error()
        self.assertNotIn("abc123", str(evidence))
        self.assertNotIn("hidden", str(evidence))
        self.assertNotIn("secret", str(evidence))
        self.assertIsNone(HttpResponse(400, {}, b"invalid").sanitized_sap_error()["sap_message"])


if __name__ == "__main__":
    unittest.main()
