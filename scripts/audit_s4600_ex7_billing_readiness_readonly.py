"""Read-only exercise 7 readiness and billing API contract discovery."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
DELIVERY = "80000085"
DELIVERY_SERVICE = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV"
BILLING_SERVICE = "sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_billing_readiness_2026-10-22.json"


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def metadata_summary(body: bytes) -> dict:
    root = ET.fromstring(body)
    entity_types = {}
    entity_sets = []
    function_imports = []
    for node in root.iter():
        if local(node.tag) == "EntityType":
            properties = []
            navigation = []
            for child in node:
                if local(child.tag) == "Property":
                    properties.append({
                        "name": child.attrib.get("Name"),
                        "type": child.attrib.get("Type"),
                        "nullable": child.attrib.get("Nullable"),
                        "creatable": next((v for k, v in child.attrib.items() if k.endswith("creatable")), None),
                        "updatable": next((v for k, v in child.attrib.items() if k.endswith("updatable")), None),
                    })
                elif local(child.tag) == "NavigationProperty":
                    navigation.append({"name": child.attrib.get("Name"), "relationship": child.attrib.get("Relationship")})
            entity_types[node.attrib.get("Name")] = {"properties": properties, "navigation": navigation}
        elif local(node.tag) == "EntitySet":
            entity_sets.append({
                "name": node.attrib.get("Name"),
                "entity_type": node.attrib.get("EntityType"),
                "creatable": next((v for k, v in node.attrib.items() if k.endswith("creatable")), None),
                "updatable": next((v for k, v in node.attrib.items() if k.endswith("updatable")), None),
                "deletable": next((v for k, v in node.attrib.items() if k.endswith("deletable")), None),
            })
        elif local(node.tag) == "FunctionImport":
            function_imports.append({
                "name": node.attrib.get("Name"),
                "http_method": next((v for k, v in node.attrib.items() if k.endswith("HttpMethod")), None),
                "parameters": [
                    {"name": child.attrib.get("Name"), "type": child.attrib.get("Type"), "mode": child.attrib.get("Mode")}
                    for child in node if local(child.tag) == "Parameter"
                ],
            })
    billing_sets = [row for row in entity_sets if "Billing" in str(row["name"])]
    used_types = {str(row["entity_type"]).split(".")[-1] for row in billing_sets}
    return {
        "entity_sets": billing_sets,
        "entity_types": {key: value for key, value in entity_types.items() if key in used_types},
        "function_imports": function_imports,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    delivery_response = client.request(
        "GET", f"{DELIVERY_SERVICE}/A_OutbDeliveryHeader('{DELIVERY}')", headers={"Accept": "application/json"}
    )
    billing_query = urlencode({"$filter": f"ReferenceSDDocument eq '{DELIVERY}'", "$top": "100"})
    billing_items_response = client.request(
        "GET", f"{BILLING_SERVICE}/A_BillingDocumentItem?{billing_query}", headers={"Accept": "application/json"}
    )
    metadata_response = client.request("GET", f"{BILLING_SERVICE}/$metadata", headers={"Accept": "application/xml"})
    delivery = clean(delivery_response.json().get("d", {})) if delivery_response.status == 200 else {}
    billing_items = (
        clean(billing_items_response.json().get("d", {}).get("results", []))
        if billing_items_response.status == 200 else []
    )
    contract = metadata_summary(metadata_response.body) if metadata_response.status == 200 else {}
    if billing_items:
        classification = "EXISTS"
    elif (
        delivery_response.status == 200
        and billing_items_response.status == 200
        and delivery.get("OverallGoodsMovementStatus") == "C"
        and delivery.get("OverallDelivReltdBillgStatus") == "A"
    ):
        classification = "MISSING_READY_FOR_EVIDENCED_BILLING_ROUTE"
    else:
        classification = "UNKNOWN_OR_NOT_READY"
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "delivery_document": DELIVERY,
        "delivery_http_status": delivery_response.status,
        "delivery": delivery,
        "billing_lookup": {
            "http_status": billing_items_response.status,
            "filter": f"ReferenceSDDocument eq '{DELIVERY}'",
            "rows": billing_items,
            "error": None if billing_items_response.status == 200 else billing_items_response.sanitized_sap_error(),
        },
        "metadata_http_status": metadata_response.status,
        "billing_api_contract": contract,
        "classification": classification,
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "classification": classification,
        "delivery_statuses": {
            "goods_movement": delivery.get("OverallGoodsMovementStatus"),
            "delivery_related_billing": delivery.get("OverallDelivReltdBillgStatus"),
            "overall_process": delivery.get("OverallSDProcessStatus"),
        },
        "existing_billing_items": billing_items,
        "metadata_http_status": metadata_response.status,
        "entity_sets": contract.get("entity_sets", []),
        "function_imports": contract.get("function_imports", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
