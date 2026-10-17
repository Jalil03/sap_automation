"""Focused GET-only evidence for the Product currency-type 30 blocker."""

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


def get(path: str, *, params: dict[str, str] | None = None) -> dict[str, object]:
    response = requests.get(
        f"{base}{path}",
        params={"sap-client": client, **(params or {})},
        auth=auth,
        headers={"Accept": "application/json"},
        verify=verify,
        timeout=30,
    )
    body: object = None
    if response.status_code == 200:
        body = response.json().get("d")
    return {"http": response.status_code, "body": body}


result = {
    "plant_1710": get("/sap/opu/odata/sap/API_PLANT_SRV/A_Plant('1710')"),
    "fg228_ml": get(
        "/sap/opu/odata/sap/API_PRODUCT_SRV/A_ProductMLAccount",
        params={"$filter": "Product eq 'FG228' and ValuationArea eq '1710'", "$top": "10"},
    ),
    "target_ml": get(
        "/sap/opu/odata/sap/API_PRODUCT_SRV/A_ProductMLAccount",
        params={"$filter": "Product eq '10000287' and ValuationArea eq '1710'", "$top": "10"},
    ),
}
print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
