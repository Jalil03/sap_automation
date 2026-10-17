import os
import requests
import urllib3
from dotenv import load_dotenv

load_dotenv()

base_url = os.environ["SAP_BASE_URL"].rstrip("/")
client = os.environ["SAP_CLIENT"]
username = os.environ["SAP_USERNAME"]
password = os.environ["SAP_PASSWORD"]

verify_ssl = os.getenv("SAP_VERIFY_SSL", "true").lower() == "true"

if not verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = (
    base_url
    + "/sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata"
)

response = requests.get(
    url,
    params={"sap-client": client},
    auth=(username, password),
    timeout=30,
    verify=verify_ssl,
)

print("HTTP =", response.status_code)
print("CONTENT_TYPE =", response.headers.get("Content-Type"))
print("HAS_A_CUSTOMER =", "A_Customer" in response.text)