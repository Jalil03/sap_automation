"""Read-only PGI readiness audit for S4600 exercise 6 delivery 80000085."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex6_pgi_readiness_2026-10-22.json"
SERVICE = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV"
DELIVERY = "80000085"


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
    header_response = client.request(
        "GET", f"{SERVICE}/A_OutbDeliveryHeader('{DELIVERY}')", headers={"Accept": "application/json"}
    )
    query = urlencode({"$filter": f"DeliveryDocument eq '{DELIVERY}'", "$top": "20"})
    items_response = client.request(
        "GET", f"{SERVICE}/A_OutbDeliveryItem?{query}", headers={"Accept": "application/json"}
    )
    header = clean(header_response.json().get("d", {})) if header_response.status == 200 else {}
    items = clean(items_response.json().get("d", {}).get("results", [])) if items_response.status == 200 else []
    expected_items = {"000010": ("10000282", "10"), "000020": ("10000283", "20")}
    observed = {str(row.get("DeliveryDocumentItem")): row for row in items}
    item_checks = {}
    for item, (material, quantity) in expected_items.items():
        row = observed.get(item, {})
        item_checks[item] = {
            "material": row.get("Material"),
            "plant": row.get("Plant"),
            "storage_location": row.get("StorageLocation"),
            "delivery_quantity": row.get("ActualDeliveryQuantity"),
            "picked_quantity": row.get("ActualDeliveredQtyInBaseUnit"),
            "picking_status": row.get("PickingStatus"),
            "goods_movement_status": row.get("GoodsMovementStatus"),
            "goods_movement_type": row.get("GoodsMovementType"),
            "expected_material": material,
            "expected_quantity": quantity,
        }
    ready = (
        header_response.status == 200
        and items_response.status == 200
        and header.get("OverallPickingStatus") == "C"
        and header.get("OverallGoodsMovementStatus") == "A"
        and header.get("ActualGoodsMovementDate") is None
        and set(observed) == set(expected_items)
        and all(
            observed[item].get("Material") == expected_items[item][0]
            and observed[item].get("Plant") == "FR10"
            and observed[item].get("StorageLocation") == "0001"
            and observed[item].get("PickingStatus") == "C"
            and observed[item].get("GoodsMovementStatus") == "A"
            and observed[item].get("GoodsMovementType") == "601"
            for item in expected_items
        )
    )
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "delivery_document": DELIVERY,
        "header_http_status": header_response.status,
        "header_etag": header_response.header("ETag"),
        "header": header,
        "items_http_status": items_response.status,
        "items": items,
        "item_checks": item_checks,
        "classification": "READY_FOR_SEPARATELY_APPROVED_PGI" if ready else "NOT_READY_OR_UNKNOWN",
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)), "classification": evidence["classification"],
        "header_etag": evidence["header_etag"],
        "header_statuses": {
            "picking": header.get("OverallPickingStatus"),
            "goods_movement": header.get("OverallGoodsMovementStatus"),
            "actual_goods_movement_date": header.get("ActualGoodsMovementDate"),
        },
        "item_checks": item_checks,
    }, ensure_ascii=False, indent=2))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
