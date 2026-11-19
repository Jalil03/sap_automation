"""Read the exact ZPR0 condition-type definition used by the staged order."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_condition_type_2026-10-22.json"


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    query = urlencode({
        "$filter": "ConditionType eq 'ZPR0'",
        "$select": "ConditionType,AccessSequence",
        "$top": "5",
    })
    response = client.request(
        "GET",
        f"sap/opu/odata/sap/API_SLSPRICINGPROCEDURE_SRV/A_SlsPricingConditionType?{query}",
        headers={"Accept": "application/json"},
    )
    rows = response.json().get("d", {}).get("results", []) if response.status == 200 else []
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "READ_ONLY",
        "condition_type": "ZPR0",
        "http_status": response.status,
        "classification": "VERIFIED_PRESENT" if response.status == 200 and rows else "UNKNOWN",
        "rows": [{key: value for key, value in row.items() if key != "__metadata"} for row in rows],
    }
    if response.status != 200:
        evidence["error"] = response.sanitized_sap_error()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if evidence["classification"] == "VERIFIED_PRESENT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
