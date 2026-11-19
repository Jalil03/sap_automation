"""Read exact sales document categories for the exercise-28 document types."""

from __future__ import annotations

import json
import sys
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
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise SystemExit("Blocked: unexpected identity")
    client = UrllibSapTransport(config)
    rows = {}
    for code in ("AF", "AG", "TA"):
        response = client.request(
            "GET",
            f"sap/opu/odata/sap/API_SALESORDERTYPE_SRV/A_SalesOrderType('{code}')",
            headers={"Accept": "application/json"},
        )
        rows[code] = {
            "http_status": response.status,
            "data": {key: value for key, value in response.json().get("d", {}).items() if key != "__metadata"} if response.status == 200 else {},
        }
    output = ROOT / "runtime" / "sap_reads" / "s4600_ex28_sales_document_categories_2026-10-21.json"
    output.write_text(json.dumps({"environment": {"system": "A4H", "client": "600", "user": "ABDELJ"}, "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
