"""Discover installed read-only finance OData routes for S4600 exercise 8."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex8_finance_odata_discovery_2026-10-22.json"
SERVICES = [
    "API_BANKACCOUNT_SRV",
    "API_CHARTOFACCOUNTS_SRV",
    "API_GLACCOUNTLINEITEM",
    "API_JOURNALENTRYITEMBASIC_SRV",
    "API_COMPANYCODE_SRV",
    "FAC_MANAGE_GLACCOUNT_SRV",
    "FAR_PAYMENT_POST_SRV",
]


def metadata_summary(body: bytes) -> dict:
    try:
        root = ET.fromstring(body)
    except ET.ParseError as error:
        return {"parse_error": str(error)}
    entity_sets = []
    entity_types = []
    for node in root.iter():
        if node.tag.endswith("EntitySet"):
            entity_sets.append({
                "name": node.attrib.get("Name"),
                "entity_type": node.attrib.get("EntityType"),
                "creatable": node.attrib.get("{http://www.sap.com/Protocols/SAPData}creatable"),
                "updatable": node.attrib.get("{http://www.sap.com/Protocols/SAPData}updatable"),
            })
        elif node.tag.endswith("EntityType"):
            properties = []
            for child in node:
                if child.tag.endswith("Property"):
                    properties.append({"name": child.attrib.get("Name"), "type": child.attrib.get("Type")})
            entity_types.append({"name": node.attrib.get("Name"), "properties": properties})
    return {"entity_sets": entity_sets, "entity_types": entity_types}


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    results = {}
    for service in SERVICES:
        try:
            response = client.request(
                "GET",
                f"sap/opu/odata/sap/{service}/$metadata",
                headers={"Accept": "application/xml"},
            )
            results[service] = {
                "http_status": response.status,
                "metadata": metadata_summary(response.body) if response.status == 200 else None,
                "error_excerpt": response.body.decode("utf-8", errors="replace")[:1000] if response.status != 200 else None,
            }
        except Exception as error:
            results[service] = {
                "http_status": None,
                "metadata": None,
                "transport_error": f"{type(error).__name__}: {error}",
            }
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "environment": identity,
        "services": results,
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "services": {
            service: {
                "http_status": item["http_status"],
                "entity_sets": (item["metadata"] or {}).get("entity_sets", []),
            }
            for service, item in results.items()
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
