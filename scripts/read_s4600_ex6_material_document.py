"""Discover and read back the material document created by exercise 6."""

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
SERVICE = "sap/opu/odata/sap/API_MATERIAL_DOCUMENT_SRV"
DOCUMENT = "4900000263"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex6_material_document_4900000263_2026-10-22.json"


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    metadata = client.request("GET", f"{SERVICE}/$metadata", headers={"Accept": "application/xml"})
    entity_sets = []
    if metadata.status == 200:
        root = ET.fromstring(metadata.body)
        for node in root.iter():
            if node.tag.rsplit("}", 1)[-1] == "EntitySet" and "MaterialDocument" in node.attrib.get("Name", ""):
                entity_sets.append({"name": node.attrib.get("Name"), "entity_type": node.attrib.get("EntityType")})
    reads = {}
    for entry in entity_sets:
        name = str(entry["name"])
        query = urlencode({"$filter": f"MaterialDocument eq '{DOCUMENT}'", "$top": "100"})
        response = client.request("GET", f"{SERVICE}/{name}?{query}", headers={"Accept": "application/json"})
        reads[name] = {
            "http_status": response.status,
            "rows": clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else [],
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_METADATA_AND_ENTITY_GET",
        "service": "API_MATERIAL_DOCUMENT_SRV",
        "material_document": DOCUMENT,
        "metadata_http_status": metadata.status,
        "discovered_entity_sets": entity_sets,
        "readbacks": reads,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **evidence}, ensure_ascii=False, indent=2))
    return 0 if metadata.status == 200 and any(value["rows"] for value in reads.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
