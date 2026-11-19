"""Reconcile the incomplete service-order save attempt and inspect existing TAD patterns."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_service_order_incomplete_reconciliation_2026-10-22.json"
SERVICE = "sap/opu/odata/sap/API_SALES_ORDER_SRV"


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def rows(client, entity: str, query: dict[str, str]) -> dict:
    response = client.request("GET", f"{SERVICE}/{entity}?{urlencode(query)}", headers={"Accept": "application/json"})
    result = {"http_status": response.status}
    if response.status == 200:
        result["rows"] = clean(response.json().get("d", {}).get("results", []))
    else:
        result["error"] = response.sanitized_sap_error()
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: {identity!r}")
    client = UrllibSapTransport(config)
    duplicate = rows(client, "A_SalesOrder", {
        "$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '8-600'",
        "$top": "50",
    })
    tad_items = rows(client, "A_SalesOrderItem", {
        "$filter": "SalesOrderItemCategory eq 'TAD'",
        "$select": "SalesOrder,SalesOrderItem,Material,SalesOrderItemCategory,ProductionPlant,RequestedQuantity,RequestedQuantitySAPUnit,NetAmount,TransactionCurrency,SDProcessStatus,OrderRelatedBillingStatus,DeliveryStatus",
        "$top": "50",
    })
    order_ids = sorted({str(row.get("SalesOrder")) for row in tad_items.get("rows", []) if row.get("SalesOrder")})
    headers = rows(client, "A_SalesOrder", {
        "$filter": " or ".join(f"SalesOrder eq '{number}'" for number in order_ids) if order_ids else "SalesOrder eq '0'",
        "$select": "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,PurchaseOrderByCustomer,OverallSDProcessStatus,OverallTotalDeliveryStatus,OverallOrdReltdBillgStatus",
        "$top": "50",
    })
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "attempt_reconciliation": duplicate,
        "existing_tad_items": tad_items,
        "existing_tad_headers": headers,
        "interpretation": {
            "current_order_created": bool(duplicate.get("rows")),
            "tad_examples_found": len(tad_items.get("rows", [])),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "duplicate_http_status": duplicate.get("http_status"),
        "current_order_matches": duplicate.get("rows", []),
        "tad_http_status": tad_items.get("http_status"),
        "tad_items": tad_items.get("rows", []),
        "tad_headers": headers.get("rows", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
