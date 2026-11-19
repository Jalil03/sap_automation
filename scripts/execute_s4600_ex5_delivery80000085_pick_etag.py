"""One authorized PickAllItems attempt with a freshly read delivery ETag."""

from __future__ import annotations

import argparse
import hashlib
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
from src.sap_runtime.errors import AmbiguousTransportError
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
SERVICE_ROOT = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV;v=2"
DELIVERY = "80000085"
WORKFLOW = {
    "delivery_document": DELIVERY,
    "service_version": 2,
    "operation": {
        "method": "POST",
        "target": "PickAllItems",
        "parameters": {"DeliveryDocument": DELIVERY},
        "requires_current_delivery_etag": True,
    },
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH3_EX5.delivery80000085_pick_v2.workflow_approval.json"
DRY_RUN = ROOT / "runtime" / "sap_reads" / "s4600_ex5_delivery80000085_pick_etag_dry_run.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex5_delivery80000085_pick_v2_result.json"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def workflow_hash() -> str:
    return hashlib.sha256(canonical(WORKFLOW)).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != "__metadata"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def save(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path = RESULT if result["mode"] == "EXECUTE" else DRY_RUN
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_state(client):
    header_query = urlencode({"$select": "DeliveryDocument,OverallPickingStatus,OverallGoodsMovementStatus,ActualGoodsMovementDate"})
    header_response = client.request(
        "GET", f"{SERVICE_ROOT}/A_OutbDeliveryHeader('{DELIVERY}')?{header_query}",
        headers={"Accept": "application/json"},
    )
    items_query = urlencode({
        "$filter": f"DeliveryDocument eq '{DELIVERY}'",
        "$select": "DeliveryDocument,DeliveryDocumentItem,Material,Plant,StorageLocation,ActualDeliveryQuantity",
    })
    items_response = client.request(
        "GET", f"{SERVICE_ROOT}/A_OutbDeliveryItem?{items_query}",
        headers={"Accept": "application/json"},
    )
    return {
        "header_http_status": header_response.status,
        "header_etag": header_response.header("ETag"),
        "header": clean(header_response.json().get("d", {})) if header_response.status == 200 else {},
        "items_http_status": items_response.status,
        "items": clean(items_response.json().get("d", {}).get("results", [])) if items_response.status == 200 else [],
    }


def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED" or value.get("environment") != EXPECTED:
        raise RuntimeError("Approval identity/status mismatch")
    if value.get("operation_scope") != "PICK_ALL_ITEMS_DELIVERY_80000085_V2_WITH_CURRENT_ETAG_ONLY":
        raise RuntimeError("Approval scope mismatch")
    if value.get("workflow_sha256") != workflow_hash():
        raise RuntimeError("Approval fingerprint mismatch")
    constraints = value.get("constraints", {})
    if constraints.get("maximum_post_attempts") != 1 or constraints.get("post_goods_issue_approved") is not False:
        raise RuntimeError("Approval safety constraints mismatch")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    state = get_state(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": "S4600_CH3_EX5_PICK_ALL_DELIVERY_80000085_WITH_ETAG",
        "workflow": WORKFLOW,
        "workflow_sha256": workflow_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "preflight": state,
        "attempts": [],
    }
    expected_items = {"000010", "000020"}
    actual_items = {str(row.get("DeliveryDocumentItem")): row for row in state["items"]}
    ready = (
        state["header_http_status"] == 200
        and bool(state["header_etag"])
        and state["header"].get("OverallPickingStatus") == "A"
        and state["header"].get("OverallGoodsMovementStatus") == "A"
        and state["header"].get("ActualGoodsMovementDate") is None
        and expected_items.issubset(actual_items)
        and all(actual_items[i].get("StorageLocation") == "0001" for i in expected_items)
    )
    if not ready:
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
    token_response = client.request("GET", f"{SERVICE_ROOT}/", headers={"X-CSRF-Token": "Fetch", "Accept": "application/json"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        result["status"] = "BLOCKED_CSRF"
        save(result)
        return 2
    # Refresh business state and ETag only after the write session/CSRF token is established.
    write_state = get_state(client)
    write_items = {str(row.get("DeliveryDocumentItem")): row for row in write_state["items"]}
    write_ready = (
        write_state["header_http_status"] == 200
        and bool(write_state["header_etag"])
        and write_state["header"].get("OverallPickingStatus") == "A"
        and write_state["header"].get("OverallGoodsMovementStatus") == "A"
        and write_state["header"].get("ActualGoodsMovementDate") is None
        and expected_items.issubset(write_items)
        and all(write_items[i].get("StorageLocation") == "0001" for i in expected_items)
    )
    result["write_session_preflight"] = write_state
    if not write_ready:
        result["status"] = "BLOCKED_AFTER_CSRF_PREFLIGHT"
        save(result)
        return 2
    attempt = {"operation": "POST_PICK_ALL_ITEMS", "status": "SUBMITTED", "used_current_delivery_etag": True, "etag_read_after_csrf": True}
    result["attempts"].append(attempt)
    result["status"] = "SUBMITTED"
    save(result)
    query = urlencode({"DeliveryDocument": f"'{DELIVERY}'"})
    try:
        response = client.request(
            "POST", f"{SERVICE_ROOT}/PickAllItems?{query}",
            headers={
                "Accept": "application/json", "Content-Type": "application/json",
                "X-CSRF-Token": token, "If-Match": write_state["header_etag"],
            },
            body=b"",
        )
    except AmbiguousTransportError:
        attempt["status"] = "AMBIGUOUS"
        result["status"] = "AMBIGUOUS"
        save(result)
        return 2
    attempt["http_status"] = response.status
    if response.status not in (200, 201, 204):
        attempt["status"] = "FAILED"
        attempt["error"] = response.sanitized_sap_error()
        result["status"] = "FAILED"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    attempt["status"] = "ACCEPTED"
    final = get_state(client)
    result["final_readback"] = final
    safe = final["header"].get("OverallGoodsMovementStatus") == "A" and final["header"].get("ActualGoodsMovementDate") is None
    if not safe:
        result["status"] = "SAFETY_READBACK_FAILED"
    elif final["header"].get("OverallPickingStatus") == "C":
        result["status"] = "VERIFIED_PICKED"
    else:
        result["status"] = "PICK_ACCEPTED_STATUS_NOT_COMPLETE"
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "VERIFIED_PICKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
