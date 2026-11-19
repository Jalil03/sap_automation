"""Read-only live contract inspection for creating Exercise 5 delivery."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex5_delivery_contract_2026-10-21.json"
SERVICE = "API_OUTBOUND_DELIVERY_SRV"
SAP = "http://www.sap.com/Protocols/SAPData"
EDM = "http://schemas.microsoft.com/ado/2008/09/edm"


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username}
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    response = client.request("GET", f"sap/opu/odata/sap/{SERVICE}/$metadata")
    if response.status != 200:
        raise SystemExit(f"Blocked: metadata returned HTTP {response.status}")
    root = ET.fromstring(response.body)
    entity_sets = []
    for node in root.findall(f".//{{{EDM}}}EntitySet"):
        name = node.attrib.get("Name", "")
        if "Delivery" in name or "Outb" in name:
            entity_sets.append({
                "name": name,
                "entity_type": node.attrib.get("EntityType"),
                "creatable": node.attrib.get(f"{{{SAP}}}creatable"),
                "updatable": node.attrib.get(f"{{{SAP}}}updatable"),
                "deletable": node.attrib.get(f"{{{SAP}}}deletable"),
            })
    function_imports = []
    for node in root.findall(f".//{{{EDM}}}FunctionImport"):
        function_imports.append({
            "name": node.attrib.get("Name"),
            "http_method": node.attrib.get(f"{{{SAP}}}http-method"),
            "return_type": node.attrib.get("ReturnType"),
            "parameters": [
                {"name": item.attrib.get("Name"), "type": item.attrib.get("Type"), "mode": item.attrib.get("Mode")}
                for item in node.findall(f"{{{EDM}}}Parameter")
            ],
        })
    types = {}
    for node in root.findall(f".//{{{EDM}}}EntityType"):
        name = node.attrib.get("Name", "")
        if "Delivery" not in name and "Outb" not in name:
            continue
        types[name] = {
            "properties": [
                {
                    "name": item.attrib.get("Name"),
                    "type": item.attrib.get("Type"),
                    "nullable": item.attrib.get("Nullable"),
                    "creatable": item.attrib.get(f"{{{SAP}}}creatable"),
                    "updatable": item.attrib.get(f"{{{SAP}}}updatable"),
                }
                for item in node.findall(f"{{{EDM}}}Property")
            ],
            "navigation": [
                {"name": item.attrib.get("Name"), "relationship": item.attrib.get("Relationship")}
                for item in node.findall(f"{{{EDM}}}NavigationProperty")
            ],
        }
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_METADATA_GET",
        "service": SERVICE,
        "entity_sets": entity_sets,
        "function_imports": function_imports,
        "entity_types": types,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "entity_sets": entity_sets,
        "function_imports": function_imports,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
