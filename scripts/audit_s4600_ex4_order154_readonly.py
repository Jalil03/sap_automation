"""Read-only completion audit for S4600 exercise 4 using sales order 154."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex4_order154_readback_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
SERVICE = "API_SALES_ORDER_SRV"


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != "__metadata"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def get(client, resource: str) -> dict:
    response = client.request(
        "GET", f"sap/opu/odata/sap/{SERVICE}/{resource}", headers={"Accept": "application/json"}
    )
    result = {"http_status": response.status}
    if response.status != 200:
        result["error"] = response.sanitized_sap_error()
        return result
    payload = clean(response.json().get("d", {}))
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        result["rows"] = payload["results"]
    else:
        result["row"] = payload
    return result


def odata_date(value):
    match = re.fullmatch(r"/Date\((\d+)\)/", str(value or ""))
    if not match:
        return value
    return datetime.fromtimestamp(int(match.group(1)) / 1000, tz=timezone.utc).date().isoformat()


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    actual = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if actual != EXPECTED:
        raise SystemExit(f"Blocked outside A4H/600/ABDELJ: {actual!r}")
    client = UrllibSapTransport(config)
    header = get(client, "A_SalesOrder('154')")
    items = get(client, "A_SalesOrder('154')/to_Item")
    partners = get(client, "A_SalesOrder('154')/to_Partner")
    schedules = {
        item: get(client, f"A_SalesOrderItem(SalesOrder='154',SalesOrderItem='{item}')/to_ScheduleLine")
        for item in ("10", "20")
    }
    pricing = {
        item: get(client, f"A_SalesOrderItem(SalesOrder='154',SalesOrderItem='{item}')/to_PricingElement")
        for item in ("10", "20")
    }
    reads = {"header": header, "items": items, "partners": partners, "schedules": schedules, "pricing": pricing}
    statuses = [header.get("http_status"), items.get("http_status"), partners.get("http_status")]
    statuses += [entry.get("http_status") for entry in schedules.values()]
    statuses += [entry.get("http_status") for entry in pricing.values()]
    if any(status != 200 for status in statuses):
        result = {
            "captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": EXPECTED,
            "mode": "STRICT_READ_ONLY_HTTP_GET", "status": "BLOCKED_READ_ERROR", "reads": reads,
        }
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "http_statuses": statuses}, indent=2))
        return 2

    h = header["row"]
    item_rows = items.get("rows", [])
    by_item = {str(row.get("SalesOrderItem")): row for row in item_rows}
    gross_weight = sum(Decimal(str(row.get("ItemGrossWeight") or "0")) for row in item_rows)
    unit_prices = {}
    for item, row in by_item.items():
        quantity = Decimal(str(row.get("RequestedQuantity") or "0"))
        net = Decimal(str(row.get("NetAmount") or "0"))
        unit_prices[item] = str(net / quantity) if quantity else None
    partner_rows = partners.get("rows", [])
    bill_to = [row for row in partner_rows if row.get("PartnerFunction") == "RF"]
    schedule_answers = {
        item: [
            {
                key: row.get(key) for key in (
                    "SalesOrder", "SalesOrderItem", "ScheduleLine", "ScheduleLineDeliveryDate",
                    "RequestedDeliveryDate", "ConfirmedDeliveryDate", "ConfirmedDeliveryQuantity",
                    "OrderQuantityUnit", "OrderQuantitySAPUnit",
                ) if key in row
            }
            for row in result.get("rows", [])
        ] for item, result in schedules.items()
    }
    answers = {
        "sales_order": "154",
        "customer_payment_terms": h.get("CustomerPaymentTerms"),
        "total_net_amount": h.get("TotalNetAmount"),
        "transaction_currency": h.get("TransactionCurrency"),
        "total_gross_weight_calculated_from_items": str(gross_weight),
        "weight_unit": next((row.get("ItemWeightSAPUnit") for row in item_rows if row.get("ItemWeightSAPUnit")), None),
        "complete_delivery_required": h.get("CompleteDeliveryIsDefined"),
        "item_10_plant": by_item.get("10", {}).get("ProductionPlant"),
        "unit_prices_calculated": unit_prices,
        "item_10_schedule_lines": schedule_answers.get("10", []),
        "item_10_confirmed_delivery_date": odata_date(
            next((row.get("ConfirmedDeliveryDate") for row in schedules["10"].get("rows", []) if row.get("ConfirmedDeliveryDate")), None)
        ),
        "item_20_confirmed_quantity": by_item.get("20", {}).get("ConfdDelivQtyInOrderQtyUnit"),
        "bill_to_partners": bill_to,
        "overall_process_status": h.get("OverallSDProcessStatus"),
    }
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "status": "COMPLETED_AND_VERIFIED",
        "answers": answers,
        "reads": reads,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "status": result["status"], "answers": answers}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
