"""GET-only inspection of the configured Phase 5 product template and contract."""

from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import urllib3
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
seed = json.loads((ROOT / "config/s4615_training_seed.yaml").read_text(encoding="utf-8"))
operation = seed["operations"]["PRODUCT_P615_400"]
template = operation["template_policy"]["template_id"]
target = operation["target"]["material_id"]

load_dotenv()
base = os.environ["SAP_BASE_URL"].rstrip("/")
client = os.environ["SAP_CLIENT"]
auth = (os.environ["SAP_USERNAME"], os.environ["SAP_PASSWORD"])
verify = os.getenv("SAP_VERIFY_SSL", os.getenv("SAP_VERIFY_TLS", "true")).lower() == "true"
if not verify:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
service_root = f"{base}/sap/opu/odata/sap/API_PRODUCT_SRV"

metadata = requests.get(
    f"{service_root}/$metadata", params={"sap-client": client}, auth=auth,
    headers={"Accept": "application/xml"}, verify=verify, timeout=60,
)
result: dict[str, object] = {"metadata_http": metadata.status_code, "template": template, "target": target}
targets = (
    "A_Product",
    "A_ProductPlant",
    "A_ProductSalesDelivery",
    "A_ProductUnitsOfMeasure",
    "A_ProductDescription",
    "A_ProductValuation",
    "A_ProductValuationAccount",
    "A_ProductValuationCosting",
    "A_ProductMLAccount",
    "A_ProductPlantCosting",
)
if metadata.status_code == 200:
    edm = "{http://schemas.microsoft.com/ado/2008/09/edm}"
    sap = "{http://www.sap.com/Protocols/SAPData}"
    root = ET.fromstring(metadata.content)
    types = {node.attrib["Name"]: node for node in root.iter(f"{edm}EntityType")}
    contracts = {}
    for entity_set in root.iter(f"{edm}EntitySet"):
        name = entity_set.attrib.get("Name")
        if name not in targets:
            continue
        type_name = entity_set.attrib.get("EntityType", "").split(".")[-1]
        entity_type = types[type_name]
        keys = {node.attrib["Name"] for node in entity_type.findall(f"{edm}Key/{edm}PropertyRef")}
        properties = []
        for prop in entity_type.findall(f"{edm}Property"):
            properties.append({
                "name": prop.attrib.get("Name"),
                "type": prop.attrib.get("Type"),
                "nullable": prop.attrib.get("Nullable", "true"),
                "creatable": prop.attrib.get(f"{sap}creatable"),
                "key": prop.attrib.get("Name") in keys,
            })
        contracts[name] = {
            "creatable": entity_set.attrib.get(f"{sap}creatable"),
            "updatable": entity_set.attrib.get(f"{sap}updatable"),
            "properties": properties,
        }
    result["contracts"] = contracts

for entity_set in targets:
    response = requests.get(
        f"{service_root}/{entity_set}",
        params={"sap-client": client, "$filter": f"Product eq '{template}'", "$top": "100"},
        auth=auth, headers={"Accept": "application/json"}, verify=verify, timeout=30,
    )
    rows = []
    if response.status_code == 200:
        rows = [
            {key: value for key, value in row.items() if key != "__metadata"}
            for row in response.json().get("d", {}).get("results", [])
        ]
    result[f"template_{entity_set}"] = {"http": response.status_code, "rows": rows}

    target_view = requests.get(
        f"{service_root}/{entity_set}",
        params={"sap-client": client, "$filter": f"Product eq '{target}'", "$top": "100"},
        auth=auth, headers={"Accept": "application/json"}, verify=verify, timeout=30,
    )
    target_rows = []
    if target_view.status_code == 200:
        target_rows = [
            {key: value for key, value in row.items() if key != "__metadata"}
            for row in target_view.json().get("d", {}).get("results", [])
        ]
    result[f"target_{entity_set}"] = {
        "http": target_view.status_code,
        "rows": target_rows,
    }

target_response = requests.get(
    f"{service_root}/A_Product('{target}')", params={"sap-client": client}, auth=auth,
    headers={"Accept": "application/json"}, verify=verify, timeout=30,
)
result["target_lookup_http"] = target_response.status_code
print(json.dumps(result, indent=2, sort_keys=True))
