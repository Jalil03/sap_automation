"""Read delivery-item document flow after the exercise 6 PGI."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
SERVICE = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV;v=2"
DELIVERY = "80000085"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex6_post_pgi_document_flow_2026-10-22.json"


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
    flows = {}
    for item in ("000010", "000020"):
        path = f"{SERVICE}/A_OutbDeliveryItem(DeliveryDocument='{DELIVERY}',DeliveryDocumentItem='{item}')/to_DocumentFlow"
        response = client.request("GET", path, headers={"Accept": "application/json"})
        flows[item] = {
            "http_status": response.status,
            "rows": clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else [],
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    subsequent_documents = sorted({
        str(row.get("Subsequentdocument"))
        for value in flows.values()
        for row in value["rows"]
        if row.get("Subsequentdocument")
    })
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "delivery_document": DELIVERY,
        "item_document_flows": flows,
        "subsequent_documents": subsequent_documents,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **evidence}, ensure_ascii=False, indent=2))
    return 0 if all(value["http_status"] == 200 for value in flows.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
