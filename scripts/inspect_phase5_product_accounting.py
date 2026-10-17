"""Read-only comparison of Product accounting views for the S4615 target/template."""

from __future__ import annotations

import json
import os

import requests
import urllib3
from dotenv import load_dotenv


load_dotenv()
base = os.environ["SAP_BASE_URL"].rstrip("/")
client = os.environ["SAP_CLIENT"]
auth = (os.environ["SAP_USERNAME"], os.environ["SAP_PASSWORD"])
verify = os.getenv("SAP_VERIFY_SSL", os.getenv("SAP_VERIFY_TLS", "true")).lower() == "true"
if not verify:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

service = f"{base}/sap/opu/odata/sap/API_PRODUCT_SRV"
entity_sets = (
    "A_ProductValuation",
    "A_ProductValuationAccount",
    "A_ProductValuationCosting",
    "A_ProductMLAccount",
    "A_ProductPlantCosting",
)
result: dict[str, object] = {}
for product in ("FG228", "10000287"):
    product_result = {}
    for entity_set in entity_sets:
        response = requests.get(
            f"{service}/{entity_set}",
            params={
                "sap-client": client,
                "$filter": f"Product eq '{product}'",
                "$top": "20",
            },
            auth=auth,
            headers={"Accept": "application/json"},
            verify=verify,
            timeout=30,
        )
        rows = []
        if response.status_code == 200:
            rows = [
                {key: value for key, value in row.items() if key != "__metadata"}
                for row in response.json().get("d", {}).get("results", [])
            ]
        product_result[entity_set] = {"http": response.status_code, "rows": rows}
    result[product] = product_result

print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
