"""Read-only comparison of header and item ETags for delivery 80000085."""

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


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: {identity!r}")
    client = UrllibSapTransport(config)
    root = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV"
    paths = {
        "header": f"{root}/A_OutbDeliveryHeader('80000085')",
        "item_000010": f"{root}/A_OutbDeliveryItem(DeliveryDocument='80000085',DeliveryDocumentItem='000010')",
        "item_000020": f"{root}/A_OutbDeliveryItem(DeliveryDocument='80000085',DeliveryDocumentItem='000020')",
        "header_version_2": "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV;v=2/A_OutbDeliveryHeader('80000085')",
    }
    observations = {}
    for name, path in paths.items():
        response = client.request("GET", path, headers={"Accept": "application/json"})
        observations[name] = {"http_status": response.status, "etag": response.header("ETag")}
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_GET",
        "delivery_document": "80000085",
        "observations": observations,
    }
    output = ROOT / "runtime" / "sap_reads" / "s4600_delivery80000085_etags_2026-10-21.json"
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
