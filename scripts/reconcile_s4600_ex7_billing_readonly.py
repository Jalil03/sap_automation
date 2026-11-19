"""Independently reconcile the single real exercise 7 billing result."""

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
SERVICE = "sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV"
INTERNAL = "0090000090"
EXTERNAL = "90000090"
DELIVERY = "80000085"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_billing_90000090_reconciliation_2026-10-22.json"


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
    headers = {}
    for candidate in (INTERNAL, EXTERNAL):
        response = client.request("GET", f"{SERVICE}/A_BillingDocument('{candidate}')", headers={"Accept": "application/json"})
        headers[candidate] = {
            "http_status": response.status,
            "row": clean(response.json().get("d", {})) if response.status == 200 else {},
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    item_reads = {}
    filters = {
        "billing_internal": f"BillingDocument eq '{INTERNAL}'",
        "billing_external": f"BillingDocument eq '{EXTERNAL}'",
        "reference_external": f"ReferenceSDDocument eq '{DELIVERY}'",
        "reference_internal": f"ReferenceSDDocument eq '00{DELIVERY}'",
    }
    for label, expression in filters.items():
        query = urlencode({"$filter": expression, "$top": "100"})
        response = client.request("GET", f"{SERVICE}/A_BillingDocumentItem?{query}", headers={"Accept": "application/json"})
        item_reads[label] = {
            "filter": expression,
            "http_status": response.status,
            "rows": clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else [],
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    found_headers_by_id = {
        str(value["row"].get("BillingDocument")): value["row"]
        for value in headers.values()
        if value["http_status"] == 200 and value["row"].get("BillingDocument")
    }
    found_headers = list(found_headers_by_id.values())
    found_items = []
    for value in item_reads.values():
        for row in value["rows"]:
            if row not in found_items:
                found_items.append(row)
    verified = False
    if len(found_headers) == 1:
        header = found_headers[0]
        verified = (
            header.get("CompanyCode") == "FR10"
            and header.get("PayerParty") == "1000000112"
            and header.get("TransactionCurrency") == "EUR"
            and header.get("TotalNetAmount") == "3100.00"
            and header.get("TaxAmount") == "620.00"
            and bool(header.get("AccountingDocument"))
            and header.get("AccountingPostingStatus") == "C"
            and header.get("AccountingTransferStatus") == "C"
            and {(str(row.get("BillingDocumentItem")).lstrip("0") or "0") for row in found_items} == {"10", "20"}
        )
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_RECONCILIATION",
        "bapi_returned_billing_document": INTERNAL,
        "external_candidate": EXTERNAL,
        "headers": headers,
        "item_reads": item_reads,
        "deduplicated_found_items": found_items,
        "classification": "VERIFIED_BILLING_AND_FI_POSTING" if verified else "CREATED_NOT_FULLY_RECONCILED",
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "classification": evidence["classification"],
        "headers": headers,
        "found_items": found_items,
    }, ensure_ascii=False, indent=2))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
