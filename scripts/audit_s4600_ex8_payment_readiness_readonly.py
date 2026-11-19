"""Read-only pricing and clearing readiness for S4600 exercise 8."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
SERVICE = "sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV"
BILLING = "90000090"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex8_payment_readiness_2026-10-22.json"


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
    header_response = client.request("GET", f"{SERVICE}/A_BillingDocument('{BILLING}')", headers={"Accept": "application/json"})
    query = urlencode({"$filter": f"BillingDocument eq '{BILLING}'", "$top": "500"})
    pricing_response = client.request(
        "GET", f"{SERVICE}/A_BillingDocumentItemPrcgElmnt?{query}", headers={"Accept": "application/json"}
    )
    header_pricing_response = client.request(
        "GET", f"{SERVICE}/A_BillingDocumentPrcgElmnt?{query}", headers={"Accept": "application/json"}
    )
    header = clean(header_response.json().get("d", {})) if header_response.status == 200 else {}
    pricing = clean(pricing_response.json().get("d", {}).get("results", [])) if pricing_response.status == 200 else []
    header_pricing = (
        clean(header_pricing_response.json().get("d", {}).get("results", []))
        if header_pricing_response.status == 200 else []
    )
    skto = [row for row in pricing + header_pricing if str(row.get("ConditionType", "")).upper() == "SKTO"]
    skto_values = []
    for row in skto:
        for field in ("ConditionAmount", "ConditionRateValue", "ConditionBaseValue"):
            value = row.get(field)
            if value not in (None, ""):
                try:
                    skto_values.append({"item": row.get("BillingDocumentItem"), "field": field, "value": str(Decimal(str(value)))})
                except Exception:
                    pass
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "billing_document": BILLING,
        "header_http_status": header_response.status,
        "header": header,
        "pricing_http_status": pricing_response.status,
        "pricing_elements": pricing,
        "header_pricing_http_status": header_pricing_response.status,
        "header_pricing_elements": header_pricing,
        "skto_elements": skto,
        "skto_numeric_values": skto_values,
        "payment_target_from_book": {
            "company_code_mapped": "FR10",
            "posting_date": "2026-10-22",
            "document_date": "2026-10-22",
            "document_type": "DZ",
            "book_gl_account": "11100000",
            "customer_mapped": "1000000112",
            "currency": "EUR"
        },
        "classification": (
            "PRICING_READ_READY_PAYMENT_VALUES_REQUIRE_REVIEW"
            if header_response.status == 200 and pricing_response.status == 200 and header_pricing_response.status == 200
            else "UNKNOWN"
        ),
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "classification": evidence["classification"],
        "header": {
            "gross": header.get("TotalGrossAmount"),
            "net": header.get("TotalNetAmount"),
            "tax": header.get("TaxAmount"),
            "currency": header.get("TransactionCurrency"),
            "payment_terms": header.get("CustomerPaymentTerms"),
            "clearing_status": header.get("InvoiceClearingStatus"),
            "accounting_document": header.get("AccountingDocument"),
        },
        "skto_elements": skto,
        "skto_numeric_values": skto_values,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
