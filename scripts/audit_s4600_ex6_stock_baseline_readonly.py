"""Read the exact pre-PGI stock baseline for exercise 6 materials."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex6_stock_baseline_2026-10-22.json"
SERVICE = "sap/opu/odata/sap/API_MATERIAL_STOCK_SRV"


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
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: {identity!r}")
    client = UrllibSapTransport(config)
    metadata = client.request("GET", f"{SERVICE}/$metadata", headers={"Accept": "application/xml"})
    stocks = {}
    for material in ("10000282", "10000283"):
        query = urlencode({
            "$filter": f"Material eq '{material}' and Plant eq 'FR10' and StorageLocation eq '0001'",
            "$top": "100",
        })
        response = client.request("GET", f"{SERVICE}/A_MatlStkInAcctMod?{query}", headers={"Accept": "application/json"})
        stocks[material] = {
            "http_status": response.status,
            "rows": clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else [],
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "metadata_http_status": metadata.status,
        "selection": {"plant": "FR10", "storage_location": "0001", "materials": ["10000282", "10000283"]},
        "stocks": stocks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **evidence}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
