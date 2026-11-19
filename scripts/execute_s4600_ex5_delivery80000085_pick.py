"""Set storage location 0001 and pick delivery 80000085, never PGI.

Dry-run is the default. ``--execute`` requires the exact recorded approval,
checkpoints before every request, never retries a write, and reads back state.
"""

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
ITEMS = ("000010", "000020")
WORKFLOW = {
    "delivery_document": DELIVERY,
    "operations": [
        {
            "method": "PATCH",
            "target": "A_OutbDeliveryItem(DeliveryDocument=80000085,DeliveryDocumentItem=000010)",
            "body": {"StorageLocation": "0001"},
        },
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
APPROVAL_PATH = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH3_EX5.delivery80000085_pick.workflow_approval.json"
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex5_delivery80000085_pick_result.json"
DRY_RUN_PATH = ROOT / "runtime" / "sap_reads" / "s4600_ex5_delivery80000085_pick_dry_run.json"


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
    path = DRY_RUN_PATH if result.get("mode") == "DRY_RUN" else RESULT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def item_path(item: str) -> str:
    return f"{SERVICE_ROOT}/A_OutbDeliveryItem(DeliveryDocument='{DELIVERY}',DeliveryDocumentItem='{item}')"


def read_item(client, item: str) -> tuple[int, dict, str | None]:
    query = urlencode({"$select": "DeliveryDocument,DeliveryDocumentItem,Material,Plant,StorageLocation,ActualDeliveryQuantity"})
    response = client.request("GET", f"{item_path(item)}?{query}", headers={"Accept": "application/json"})
    row = clean(response.json().get("d", {})) if response.status == 200 else {}
    return response.status, row, response.header("ETag")


def read_header(client) -> tuple[int, dict]:
    query = urlencode({"$select": "DeliveryDocument,OverallPickingStatus,OverallGoodsMovementStatus,ActualGoodsMovementDate"})
    response = client.request("GET", f"{SERVICE_ROOT}/A_OutbDeliveryHeader('{DELIVERY}')?{query}", headers={"Accept": "application/json"})
    return response.status, clean(response.json().get("d", {})) if response.status == 200 else {}


def load_approval() -> dict:
    value = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    expected = {
        "status": "APPROVED",
        "operation_scope": "UPDATE_DELIVERY_80000085_STORAGE_AND_PICK_ONLY",
        "workflow_sha256": workflow_hash(),
        "environment": EXPECTED,
    }
    if any(value.get(k) != v for k, v in expected.items()):
        raise RuntimeError("Exact workflow approval does not match")
    constraints = value.get("constraints", {})
    if constraints.get("post_goods_issue_approved") is not False:
        raise RuntimeError("Approval must explicitly exclude goods issue")
    if constraints.get("maximum_attempts_per_operation") != 1:
        raise RuntimeError("Approval must limit every write to one attempt")
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
        "operation": "S4600_CH3_EX5_DELIVERY_80000085_STORAGE_AND_PICK",
        "workflow": WORKFLOW,
        "workflow_sha256": workflow_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "write_attempts": [],
    }
    before = {}
    etags = {}
    for item in ITEMS:
        status, row, etag = read_item(client, item)
        before[item] = {"http_status": status, "row": row}
        etags[item] = etag
    header_status, header = read_header(client)
    result["preflight"] = {"items": before, "header_http_status": header_status, "header": header}
    valid_items = all(
        before[i]["http_status"] == 200
        and before[i]["row"].get("DeliveryDocument") == DELIVERY
        and before[i]["row"].get("DeliveryDocumentItem") == i
        and before[i]["row"].get("Plant") == "FR10"
        and before[i]["row"].get("StorageLocation") in ("", "0001")
        and etags[i]
        for i in ITEMS
    )
    valid_header = (
        header_status == 200
        and header.get("DeliveryDocument") == DELIVERY
        and header.get("OverallGoodsMovementStatus") == "A"
        and header.get("ActualGoodsMovementDate") is None
    )
    if not (valid_items and valid_header):
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
    for item in ITEMS:
        if before[item]["row"].get("StorageLocation") == "0001":
            result["write_attempts"].append({"operation": f"PATCH_STORAGE_{item}", "status": "ALREADY_SET"})
            continue
        attempt = {"operation": f"PATCH_STORAGE_{item}", "status": "SUBMITTED", "target": item_path(item), "body": {"StorageLocation": "0001"}}
        result["write_attempts"].append(attempt)
        result["status"] = "SUBMITTED"
        save(result)
        try:
            response = client.request(
                "PATCH", item_path(item),
                headers={"Content-Type": "application/json", "Accept": "application/json", "X-CSRF-Token": token, "If-Match": etags[item]},
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
        check_status, check_row, _ = read_item(client, item)
        attempt["readback"] = {"http_status": check_status, "row": check_row}
        if check_status != 200 or check_row.get("StorageLocation") != "0001":
            attempt["status"] = "READBACK_FAILED"
            result["status"] = "READBACK_FAILED"
            save(result)
            return 2
        attempt["status"] = "VERIFIED"
        save(result)
    # Re-read both exact targets before picking.
    storage_readback = {}
    for item in ITEMS:
        status, row, _ = read_item(client, item)
        storage_readback[item] = {"http_status": status, "row": row}
    result["storage_readback"] = storage_readback
    if not all(x["http_status"] == 200 and x["row"].get("StorageLocation") == "0001" for x in storage_readback.values()):
        result["status"] = "BLOCKED_BEFORE_PICK"
        save(result)
        return 2
    pick = {"operation": "POST_PICK_ALL_ITEMS", "status": "SUBMITTED", "delivery_document": DELIVERY}
    result["write_attempts"].append(pick)
    result["status"] = "PICK_SUBMITTED"
    save(result)
    pick_query = urlencode({"DeliveryDocument": f"'{DELIVERY}'"})
    try:
        response = client.request(
            "POST", f"{SERVICE_ROOT}/PickAllItems?{pick_query}",
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
    final_header_status, final_header = read_header(client)
    final_items = {}
    for item in ITEMS:
        status, row, _ = read_item(client, item)
        final_items[item] = {"http_status": status, "row": row}
    result["final_readback"] = {"header_http_status": final_header_status, "header": final_header, "items": final_items}
    if final_header_status != 200 or final_header.get("OverallGoodsMovementStatus") != "A" or final_header.get("ActualGoodsMovementDate") is not None:
        result["status"] = "SAFETY_READBACK_FAILED"
        save(result)
        return 2
    result["status"] = "VERIFIED_PICKED" if final_header.get("OverallPickingStatus") == "C" else "PICK_ACCEPTED_STATUS_NOT_COMPLETE"
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "VERIFIED_PICKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
