"""One-shot resume: set item 000020 storage location, then pick delivery."""

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
SERVICE_ROOT = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV"
DELIVERY = "80000085"
WORKFLOW = {
    "delivery_document": DELIVERY,
    "operations": [
        {
            "method": "PATCH",
            "target": "A_OutbDeliveryItem(DeliveryDocument=80000085,DeliveryDocumentItem=000020)",
            "body": {"StorageLocation": "0001"},
        },
        {
            "method": "POST",
            "target": "PickAllItems",
            "parameters": {"DeliveryDocument": DELIVERY},
        },
    ],
}
APPROVAL_PATH = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH3_EX5.delivery80000085_resume_pick.workflow_approval.json"
DRY_RUN_PATH = ROOT / "runtime" / "sap_reads" / "s4600_ex5_delivery80000085_resume_pick_dry_run.json"
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex5_delivery80000085_resume_pick_result.json"


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
    path = RESULT_PATH if result["mode"] == "EXECUTE" else DRY_RUN_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def item_path(item: str) -> str:
    return f"{SERVICE_ROOT}/A_OutbDeliveryItem(DeliveryDocument='{DELIVERY}',DeliveryDocumentItem='{item}')"


def read_item(client, item: str):
    query = urlencode({"$select": "DeliveryDocument,DeliveryDocumentItem,Material,Plant,StorageLocation,ActualDeliveryQuantity"})
    response = client.request("GET", f"{item_path(item)}?{query}", headers={"Accept": "application/json"})
    row = clean(response.json().get("d", {})) if response.status == 200 else {}
    return response.status, row, response.header("ETag")


def read_header(client):
    query = urlencode({"$select": "DeliveryDocument,OverallPickingStatus,OverallGoodsMovementStatus,ActualGoodsMovementDate"})
    response = client.request("GET", f"{SERVICE_ROOT}/A_OutbDeliveryHeader('{DELIVERY}')?{query}", headers={"Accept": "application/json"})
    row = clean(response.json().get("d", {})) if response.status == 200 else {}
    return response.status, row


def approval() -> dict:
    value = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED" or value.get("environment") != EXPECTED:
        raise RuntimeError("Approval identity/status mismatch")
    if value.get("operation_scope") != "RESUME_DELIVERY_80000085_ITEM_000020_AND_PICK_ONLY":
        raise RuntimeError("Approval scope mismatch")
    if value.get("workflow_sha256") != workflow_hash():
        raise RuntimeError("Approval fingerprint mismatch")
    constraints = value.get("constraints", {})
    if constraints.get("maximum_attempts_per_operation") != 1 or constraints.get("post_goods_issue_approved") is not False:
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
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": "S4600_CH3_EX5_RESUME_DELIVERY_80000085_ITEM_000020_AND_PICK",
        "workflow": WORKFLOW,
        "workflow_sha256": workflow_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "attempts": [],
    }
    states = {}
    etag_20 = None
    for item in ("000010", "000020"):
        status, row, etag = read_item(client, item)
        states[item] = {"http_status": status, "row": row}
        if item == "000020":
            etag_20 = etag
    h_status, header = read_header(client)
    result["preflight"] = {"items": states, "header_http_status": h_status, "header": header}
    ready = (
        states["000010"]["http_status"] == 200
        and states["000010"]["row"].get("StorageLocation") == "0001"
        and states["000020"]["http_status"] == 200
        and states["000020"]["row"].get("StorageLocation") in ("", "0001")
        and bool(etag_20)
        and h_status == 200
        and header.get("OverallGoodsMovementStatus") == "A"
        and header.get("ActualGoodsMovementDate") is None
    )
    if not ready:
        result["status"] = "BLOCKED_PREFLIGHT"
        save(result)
        return 2
    if not args.execute:
        result["status"] = "DRY_RUN_OK"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    approval_value = approval()
    result["approval_id"] = approval_value["approval_id"]
    token_response = client.request("GET", f"{SERVICE_ROOT}/", headers={"X-CSRF-Token": "Fetch", "Accept": "application/json"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        result["status"] = "BLOCKED_CSRF"
        save(result)
        return 2
    if states["000020"]["row"].get("StorageLocation") != "0001":
        attempt = {"operation": "PATCH_STORAGE_000020", "status": "SUBMITTED", "etag_freshly_read": True}
        result["attempts"].append(attempt)
        result["status"] = "PATCH_SUBMITTED"
        save(result)
        try:
            response = client.request(
                "PATCH", item_path("000020"),
                headers={"Content-Type": "application/json", "Accept": "application/json", "X-CSRF-Token": token, "If-Match": etag_20},
                body=canonical({"StorageLocation": "0001"}),
            )
        except AmbiguousTransportError:
            attempt["status"] = "AMBIGUOUS"
            result["status"] = "AMBIGUOUS"
            save(result)
            return 2
        attempt["http_status"] = response.status
        if response.status not in (200, 204):
            attempt["status"] = "FAILED"
            attempt["error"] = response.sanitized_sap_error()
            result["status"] = "FAILED"
            save(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 2
        check_status, check_row, _ = read_item(client, "000020")
        attempt["readback"] = {"http_status": check_status, "row": check_row}
        if check_status != 200 or check_row.get("StorageLocation") != "0001":
            attempt["status"] = "READBACK_FAILED"
            result["status"] = "READBACK_FAILED"
            save(result)
            return 2
        attempt["status"] = "VERIFIED"
        save(result)
    both = {}
    for item in ("000010", "000020"):
        status, row, _ = read_item(client, item)
        both[item] = {"http_status": status, "row": row}
    result["before_pick_readback"] = both
    if not all(v["http_status"] == 200 and v["row"].get("StorageLocation") == "0001" for v in both.values()):
        result["status"] = "BLOCKED_BEFORE_PICK"
        save(result)
        return 2
    pick = {"operation": "POST_PICK_ALL_ITEMS", "status": "SUBMITTED"}
    result["attempts"].append(pick)
    result["status"] = "PICK_SUBMITTED"
    save(result)
    query = urlencode({"DeliveryDocument": f"'{DELIVERY}'"})
    try:
        response = client.request(
            "POST", f"{SERVICE_ROOT}/PickAllItems?{query}",
            headers={"Content-Type": "application/json", "Accept": "application/json", "X-CSRF-Token": token},
            body=b"",
        )
    except AmbiguousTransportError:
        pick["status"] = "AMBIGUOUS"
        result["status"] = "AMBIGUOUS"
        save(result)
        return 2
    pick["http_status"] = response.status
    if response.status not in (200, 201, 204):
        pick["status"] = "FAILED"
        pick["error"] = response.sanitized_sap_error()
        result["status"] = "FAILED"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    pick["status"] = "ACCEPTED"
    final_h_status, final_header = read_header(client)
    result["final_readback"] = {"header_http_status": final_h_status, "header": final_header}
    if final_h_status != 200 or final_header.get("OverallGoodsMovementStatus") != "A" or final_header.get("ActualGoodsMovementDate") is not None:
        result["status"] = "SAFETY_READBACK_FAILED"
    elif final_header.get("OverallPickingStatus") == "C":
        result["status"] = "VERIFIED_PICKED"
    else:
        result["status"] = "PICK_ACCEPTED_STATUS_NOT_COMPLETE"
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "VERIFIED_PICKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
