"""Narrow read-only check of the S4600 PR00/K007 contracts."""

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


OUTPUT = ROOT / "runtime/sap_reads/s4600_pricing_contracts.json"


def metadata(client, service: str) -> dict:
    response = client.request("GET", f"sap/opu/odata/sap/{service}/$metadata?sap-client=600")
    result = {"http_status": response.status}
    if response.status != 200:
        result["error"] = response.sanitized_sap_error()
        return result
    root = ET.fromstring(response.body)
    result["entity_sets"] = sorted({
        node.attrib["Name"] for node in root.iter()
        if node.tag.endswith("EntitySet") and "Name" in node.attrib
        and ("Condition" in node.attrib["Name"] or "Pricing" in node.attrib["Name"])
    })
    return result


def condition_type(client, code: str) -> dict:
    query = urlencode({
        "$filter": f"ConditionType eq '{code}'",
        "$select": "ConditionType,AccessSequence",
        "$top": "5",
    })
    response = client.request(
        "GET", f"sap/opu/odata/sap/API_SLSPRICINGPROCEDURE_SRV/A_SlsPricingConditionType?{query}"
    )
    result = {"http_status": response.status}
    if response.status != 200:
        result["error"] = response.sanitized_sap_error()
        return result
    rows = response.json().get("d", {}).get("results")
    if not isinstance(rows, list):
        result["status"] = "UNVERIFIED_RESPONSE"
        return result
    result["status"] = "VERIFIED_PRESENT" if rows else "CONFIRMED_NOT_FOUND_BY_EXACT_FILTER"
    result["rows"] = [{k: v for k, v in row.items() if k != "__metadata"} for row in rows]
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise SystemExit("S4600 pricing check requires A4H/600/ABDELJ")
    client = UrllibSapTransport(config)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": config.client, "user": config.username.upper()},
        "mode": "READ_ONLY",
        "condition_types": {code: condition_type(client, code) for code in ("PR00", "K007")},
        "service_contracts": {
            service: metadata(client, service)
            for service in ("API_SLSPRICINGPROCEDURE_SRV", "SD_PRICING_CONDITIONRECORD_SRV", "ZSD_PRICING_CONDITIONRECORD_SRV")
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
