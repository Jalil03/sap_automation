"""Execute one explicitly approved PGI and independently read it back."""

from __future__ import annotations

import argparse
import hashlib
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
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
DELIVERY = "80000085"
DELIVERY_SERVICE = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV;v=2"
STOCK_SERVICE = "sap/opu/odata/sap/API_MATERIAL_STOCK_SRV"
OPERATION = "POST_GOODS_ISSUE_DELIVERY_80000085_2026_10_22"
WORKFLOW = {
    "operation": OPERATION,
    "environment": EXPECTED,
    "write_contract": {
        "method": "POST",
        "service": "API_OUTBOUND_DELIVERY_SRV;v=2",
        "function_import": "PostGoodsIssue",
        "parameters": {"DeliveryDocument": DELIVERY},
        "maximum_post_attempts": 1,
        "no_automatic_retry": True,
    },
    "expected_scope": {
        "goods_movement_date": "2026-10-22",
        "plant": "FR10",
        "storage_location": "0001",
        "movement_type": "601",
        "items": [
            {"item": "000010", "material": "10000282", "quantity": "10"},
            {"item": "000020", "material": "10000283", "quantity": "20"},
        ],
    },
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH3_EX6.delivery80000085_pgi.workflow_approval.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex6_delivery80000085_pgi_result.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def workflow_hash() -> str:
    return hashlib.sha256(canonical(WORKFLOW)).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def save(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def delivery_state(client) -> dict:
    header_query = urlencode({"$select": "DeliveryDocument,OverallPickingStatus,OverallGoodsMovementStatus,ActualGoodsMovementDate"})
    header_response = client.request(
        "GET", f"{DELIVERY_SERVICE}/A_OutbDeliveryHeader('{DELIVERY}')?{header_query}",
        headers={"Accept": "application/json"},
    )
    items_query = urlencode({
        "$filter": f"DeliveryDocument eq '{DELIVERY}'",
        "$select": (
            "DeliveryDocument,DeliveryDocumentItem,Material,Plant,StorageLocation,"
            "ActualDeliveryQuantity,ActualDeliveredQtyInBaseUnit,PickingStatus,"
            "GoodsMovementStatus,GoodsMovementType"
        ),
    })
    items_response = client.request(
        "GET", f"{DELIVERY_SERVICE}/A_OutbDeliveryItem?{items_query}",
        headers={"Accept": "application/json"},
    )
    return {
        "header_http_status": header_response.status,
        "header_etag": header_response.header("ETag"),
        "header": clean(header_response.json().get("d", {})) if header_response.status == 200 else {},
        "items_http_status": items_response.status,
        "items": clean(items_response.json().get("d", {}).get("results", [])) if items_response.status == 200 else [],
    }


def stock_state(client) -> dict:
    result = {}
    for material in ("10000282", "10000283"):
        query = urlencode({
            "$filter": f"Material eq '{material}' and Plant eq 'FR10' and StorageLocation eq '0001'",
            "$top": "100",
        })
        response = client.request(
            "GET", f"{STOCK_SERVICE}/A_MatlStkInAcctMod?{query}", headers={"Accept": "application/json"}
        )
        rows = clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else []
        result[material] = {
            "http_status": response.status,
            "rows": rows,
            "total_quantity": str(sum((Decimal(str(row.get("MatlWrhsStkQtyInMatlBaseUnit", "0"))) for row in rows), Decimal("0"))),
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    return result


def document_flow(client) -> dict:
    query = urlencode({"$filter": f"PrecedingDocument eq '{DELIVERY}'", "$top": "100"})
    response = client.request(
        "GET", f"{DELIVERY_SERVICE}/A_OutbDeliveryDocFlow?{query}", headers={"Accept": "application/json"}
    )
    return {
        "http_status": response.status,
        "rows": clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else [],
        "error": None if response.status == 200 else response.sanitized_sap_error(),
    }


def ready(state: dict) -> bool:
    expected = {
        "000010": {"material": "10000282", "quantity": Decimal("10")},
        "000020": {"material": "10000283", "quantity": Decimal("20")},
    }
    rows = {str(row.get("DeliveryDocumentItem")): row for row in state["items"]}
    return (
        state["header_http_status"] == 200
        and state["items_http_status"] == 200
        and bool(state["header_etag"])
        and state["header"].get("OverallPickingStatus") == "C"
        and state["header"].get("OverallGoodsMovementStatus") == "A"
        and state["header"].get("ActualGoodsMovementDate") is None
        and set(rows) == set(expected)
        and all(
            rows[item].get("Material") == values["material"]
            and rows[item].get("Plant") == "FR10"
            and rows[item].get("StorageLocation") == "0001"
            and rows[item].get("PickingStatus") == "C"
            and rows[item].get("GoodsMovementStatus") == "A"
            and rows[item].get("GoodsMovementType") == "601"
            and Decimal(str(rows[item].get("ActualDeliveryQuantity"))) == values["quantity"]
            for item, values in expected.items()
        )
    )


def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    constraints = value.get("constraints", {})
    if (
        value.get("status") != "APPROVED"
        or value.get("environment") != EXPECTED
        or value.get("operation_scope") != OPERATION
        or value.get("workflow_sha256") != workflow_hash()
        or constraints.get("maximum_post_attempts") != 1
        or constraints.get("no_automatic_retry") is not True
        or constraints.get("independent_readback_required") is not True
    ):
        raise RuntimeError("Exact PGI workflow approval does not match")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--print-fingerprint", action="store_true")
    args = parser.parse_args()
    if args.print_fingerprint:
        print(workflow_hash())
        return 0

    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    if RESULT.exists():
        prior = json.loads(RESULT.read_text(encoding="utf-8"))
        if prior.get("attempts"):
            raise SystemExit("Blocked: a PGI attempt is already recorded; reconcile instead of retrying")

    client = UrllibSapTransport(config)
    preflight = delivery_state(client)
    stock_before = stock_state(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": OPERATION,
        "workflow": WORKFLOW,
        "workflow_sha256": workflow_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "preflight": preflight,
        "stock_before": stock_before,
        "attempts": [],
    }
    if not ready(preflight):
        result["status"] = "BLOCKED_PREFLIGHT"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    if not args.execute:
        result["status"] = "DRY_RUN_OK"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval = load_approval()
    result["approval_id"] = approval["approval_id"]
    token_response = client.request(
        "GET", f"{DELIVERY_SERVICE}/", headers={"X-CSRF-Token": "Fetch", "Accept": "application/json"}
    )
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        result["status"] = "BLOCKED_CSRF"
        save(result)
        return 2

    current = delivery_state(client)
    result["write_session_preflight"] = current
    if not ready(current):
        result["status"] = "BLOCKED_AFTER_CSRF_PREFLIGHT"
        save(result)
        return 2

    attempt = {
        "operation": "POST PostGoodsIssue",
        "target": DELIVERY,
        "status": "SUBMITTED",
        "attempt_number": 1,
        "used_current_delivery_etag": True,
    }
    result["attempts"].append(attempt)
    result["status"] = "SUBMITTED"
    save(result)
    query = urlencode({"DeliveryDocument": f"'{DELIVERY}'"})
    try:
        response = client.request(
            "POST", f"{DELIVERY_SERVICE}/PostGoodsIssue?{query}",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-CSRF-Token": token,
                "If-Match": current["header_etag"],
            },
            body=b"",
        )
    except AmbiguousTransportError as error:
        attempt["status"] = "AMBIGUOUS_NO_RETRY"
        attempt["error"] = f"{type(error).__name__}: transport outcome unknown"
        result["status"] = "AMBIGUOUS_RECONCILIATION_REQUIRED"
        save(result)
        return 2

    attempt["http_status"] = response.status
    if response.status not in (200, 201, 204):
        attempt["status"] = "FAILED_NO_RETRY"
        attempt["error"] = response.sanitized_sap_error()
        result["status"] = "FAILED"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    attempt["status"] = "ACCEPTED"
    try:
        attempt["response"] = clean(response.json()) if response.body else {}
    except (ValueError, UnicodeDecodeError):
        attempt["response"] = {"body_parsed": False}

    final_delivery = delivery_state(client)
    final_stock = stock_state(client)
    flow = document_flow(client)
    result["final_readback"] = {
        "delivery": final_delivery,
        "stock": final_stock,
        "document_flow": flow,
    }
    before_quantities = {key: Decimal(value["total_quantity"]) for key, value in stock_before.items()}
    after_quantities = {key: Decimal(value["total_quantity"]) for key, value in final_stock.items()}
    result["stock_delta"] = {key: str(after_quantities[key] - before_quantities[key]) for key in before_quantities}
    verified = (
        final_delivery["header_http_status"] == 200
        and final_delivery["header"].get("OverallGoodsMovementStatus") == "C"
        and final_delivery["header"].get("ActualGoodsMovementDate") is not None
        and all(row.get("GoodsMovementStatus") == "C" for row in final_delivery["items"])
    )
    result["status"] = "VERIFIED_PGI" if verified else "ACCEPTED_READBACK_INCOMPLETE"
    attempt["status"] = result["status"]
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
