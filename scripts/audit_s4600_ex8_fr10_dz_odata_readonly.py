"""Read-only lookup of successful FR10 DZ postings and their bank G/L account."""

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

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex8_fr10_dz_line_items_2026-10-22.json"
SERVICE = "sap/opu/odata/sap/API_GLACCOUNTLINEITEM"
ENTITY = "GLAccountLineItem"
FIELDS = [
    "CompanyCode", "FiscalYear", "AccountingDocument", "LedgerGLLineItem",
    "PostingDate", "AccountingDocumentType", "AccountingDocumentItem",
    "GLAccount", "Customer", "HouseBank", "HouseBankAccount",
    "TransactionCurrency", "AmountInTransactionCurrency", "DebitCreditCode",
    "ClearingDate", "ClearingAccountingDocument",
]


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get_rows(client, filter_text: str, top: int = 200) -> dict:
    query = urlencode({
        "$filter": filter_text,
        "$select": ",".join(FIELDS),
        "$orderby": "PostingDate desc",
        "$top": str(top),
    })
    response = client.request("GET", f"{SERVICE}/{ENTITY}?{query}", headers={"Accept": "application/json"})
    body = response.json() if response.status == 200 else {}
    return {
        "http_status": response.status,
        "filter": filter_text,
        "rows": clean(body.get("d", {}).get("results", [])) if response.status == 200 else [],
        "error_excerpt": response.body.decode("utf-8", errors="replace")[:1500] if response.status != 200 else None,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    dz = get_rows(client, "CompanyCode eq 'FR10' and AccountingDocumentType eq 'DZ'")
    bank_tagged = get_rows(client, "CompanyCode eq 'FR10' and HouseBank ne ''", top=100)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "environment": identity,
        "target": {"company_code": "FR10", "document_type": "DZ", "currency": "EUR"},
        "dz_line_items": dz,
        "house_bank_tagged_line_items": bank_tagged,
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "dz_http_status": dz["http_status"],
        "dz_rows": dz["rows"],
        "bank_tagged_http_status": bank_tagged["http_status"],
        "bank_tagged_rows": bank_tagged["rows"],
    }, ensure_ascii=False, indent=2))
    return 0 if dz["http_status"] == 200 and bank_tagged["http_status"] == 200 else 2


if __name__ == "__main__":
    raise SystemExit(main())
