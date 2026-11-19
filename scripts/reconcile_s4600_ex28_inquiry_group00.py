"""GET-only reconciliation of the already-created exercise-28 inquiry."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.execute_s4600_ex28_inquiry_group00 import EXPECTED, RESULT_PATH, readback
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


def main() -> int:
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    number = str(result.get("sales_inquiry") or "")
    if not number or result.get("status") not in {"READBACK_MISMATCH", "VERIFIED"}:
        raise SystemExit("Blocked: no exact created inquiry to reconcile")
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    current = readback(client, number)
    header = current["header"]
    items = current["items"]
    verified = (
        current["header_http_status"] == 200
        and header.get("SalesInquiry") == number
        and header.get("SalesInquiryType") == "DO"
        and header.get("SalesOrganization") == "FR10"
        and header.get("DistributionChannel") == "10"
        and header.get("OrganizationDivision") == "1W"
        and header.get("SoldToParty") == "1000000112"
        and header.get("BindingPeriodValidityEndDate") == "/Date(1792886400000)/"
        and header.get("TotalNetAmount") == "240.00"
        and header.get("TransactionCurrency") == "EUR"
        and len(items) == 1
        and items[0].get("SalesInquiryItemCategory") == "AFN"
        and items[0].get("Material") == "10000283"
        and str(items[0].get("RequestedQuantity")) in {"3", "3.0", "3.000"}
        and items[0].get("RequestedQuantityUnit") == "289"
    )
    result["prior_status"] = result.get("status")
    result["readback"] = current
    result["reconciliation"] = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "GET_ONLY",
        "classification_correction": "API_SALES_INQUIRY_SRV returns localized type DO, not internal AF",
        "status": "VERIFIED" if verified else "READBACK_MISMATCH",
    }
    result["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"
    result["save_attempt"]["status"] = result["status"]
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "sales_inquiry": number,
        "status": result["status"],
        "header": header,
        "items": items,
    }, ensure_ascii=False, indent=2))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
