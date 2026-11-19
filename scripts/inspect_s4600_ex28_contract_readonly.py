"""Inspect the live S4600 exercise-28 inquiry contract using GET only."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_inquiry_contract_2026-10-21.json"
SERVICE = "API_SALES_INQUIRY_SRV"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != "__metadata"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    response = client.request("GET", f"sap/opu/odata/sap/{SERVICE}/$metadata")
    if response.status != 200:
        raise SystemExit(f"Blocked: metadata HTTP {response.status}")
    root = ET.fromstring(response.body)
    entity_sets = []
    entity_types = {}
    functions = []
    for node in root.iter():
        kind = local(node.tag)
        if kind == "EntitySet":
            entity_sets.append({
                "name": node.attrib.get("Name"),
                "entity_type": node.attrib.get("EntityType"),
                "creatable": node.attrib.get("{http://www.sap.com/Protocols/SAPData}creatable"),
                "updatable": node.attrib.get("{http://www.sap.com/Protocols/SAPData}updatable"),
            })
        elif kind == "EntityType":
            properties = []
            navigation = []
            for child in node:
                child_kind = local(child.tag)
                if child_kind == "Property":
                    properties.append({
                        "name": child.attrib.get("Name"),
                        "type": child.attrib.get("Type"),
                        "nullable": child.attrib.get("Nullable"),
                        "creatable": child.attrib.get("{http://www.sap.com/Protocols/SAPData}creatable"),
                        "updatable": child.attrib.get("{http://www.sap.com/Protocols/SAPData}updatable"),
                    })
                elif child_kind == "NavigationProperty":
                    navigation.append(child.attrib.get("Name"))
            entity_types[node.attrib.get("Name")] = {"properties": properties, "navigation": navigation}
        elif kind == "FunctionImport":
            functions.append({
                "name": node.attrib.get("Name"),
                "http_method": node.attrib.get("{http://www.sap.com/Protocols/SAPData}HttpMethod"),
            })
    query = urlencode({"$top": "5", "$orderby": "SalesInquiry desc"})
    recent = client.request(
        "GET", f"sap/opu/odata/sap/{SERVICE}/A_SalesInquiry?{query}",
        headers={"Accept": "application/json"},
    )
    query = urlencode({"$top": "10"})
    items = client.request(
        "GET", f"sap/opu/odata/sap/{SERVICE}/A_SalesInquiryItem?{query}",
        headers={"Accept": "application/json"},
    )
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_GET",
        "service": SERVICE,
        "metadata_http_status": response.status,
        "entity_sets": entity_sets,
        "entity_types": entity_types,
        "function_imports": functions,
        "recent_headers_http_status": recent.status,
        "recent_headers": clean(recent.json().get("d", {}).get("results", [])) if recent.status == 200 else [],
        "sample_items_http_status": items.status,
        "sample_items": clean(items.json().get("d", {}).get("results", [])) if items.status == 200 else [],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    focus = {
        "output": str(OUTPUT.relative_to(ROOT)),
        "header_set": next((x for x in entity_sets if x["name"] == "A_SalesInquiry"), None),
        "item_set": next((x for x in entity_sets if x["name"] == "A_SalesInquiryItem"), None),
        "header_fields": [x["name"] for x in entity_types.get("A_SalesInquiryType", {}).get("properties", [])],
        "item_fields": [x["name"] for x in entity_types.get("A_SalesInquiryItemType", {}).get("properties", [])],
        "header_navigation": entity_types.get("A_SalesInquiryType", {}).get("navigation", []),
        "recent_count": len(evidence["recent_headers"]),
        "sample_item_count": len(evidence["sample_items"]),
    }
    print(json.dumps(focus, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
