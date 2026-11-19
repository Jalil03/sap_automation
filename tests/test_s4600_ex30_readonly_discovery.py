"""Offline safety checks: no SAP connection or live write."""
import unittest
from scripts.audit_s4600_ex30_mto_candidates_readonly import bounded_read

class Response:
    def __init__(self,status,payload):self.status=status;self.payload=payload
    def json(self):return self.payload
    def sanitized_sap_error(self):return {'http_status':self.status}

class Client:
    def __init__(self,response):self.response=response;self.calls=[]
    def request(self,method,path,headers):
        self.calls.append((method,path));assert method=='GET'
        return self.response

class ReadOnlyDiscoveryTests(unittest.TestCase):
    def test_only_get_and_no_mapping_inference(self):
        c=Client(Response(200,{'d':{'results':[{'Product':'123','__metadata':{}}]}}))
        r=bounded_read(c,'API_PRODUCT_SRV','A_Product',{'$top':'2'})
        self.assertEqual(c.calls[0][0],'GET')
        self.assertEqual(r['classification'],'BOUNDED_MATCHES_NOT_AUTOMATIC_MAPPING')
        self.assertNotIn('__metadata',r['rows'][0])
    def test_pagination_is_not_silently_exhaustive(self):
        c=Client(Response(200,{'d':{'results':[],'__next':'next'}}))
        self.assertTrue(bounded_read(c,'S','E',{'$top':'21'})['has_next_page'])
    def test_read_failure_is_unknown(self):
        c=Client(Response(403,{}))
        self.assertEqual(bounded_read(c,'S','E',{'$top':'1'})['classification'],'UNKNOWN_READ_ERROR')
    def test_excessive_read_is_rejected_before_request(self):
        c=Client(Response(200,{}))
        with self.assertRaises(AssertionError):bounded_read(c,'S','E',{'$top':'22'})
        self.assertEqual(c.calls,[])

if __name__=='__main__':unittest.main()
