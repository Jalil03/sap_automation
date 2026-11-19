"""Controlled one-shot creation of the Exercise 5 delivery for sales order 154."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError, TransportError
from src.sap_runtime.transport import HttpResponse, UrllibSapTransport


SERVICE_ROOT = "sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV"
SALES_SERVICE = "sap/opu/odata/sap/API_SALES_ORDER_SRV"
APPROVAL_PATH = (
    ROOT / "data" / "provisioning" / "s4600" /
    "S4600_CH3_EX5.order154.workflow_approval.json"
)
DRY_RUN_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex5_delivery_order154_dry_run.json"
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex5_delivery_order154_result.json"
EXPECTED_IDENTITY = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {"to_DeliveryDocumentItem": {"results": [{"ReferenceSDDocument": "154"}]}}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def fingerprint() -> str:
    return hashlib.sha256(canonical_bytes(PAYLOAD)).hexdigest()


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_collection(client, service: str, entity: str, parameters: dict[str, str]) -> tuple[int, list[dict]]:
    path = f"{service}/{entity}?{urlencode(parameters)}"
    response = client.request("GET", path, headers={"Accept": "application/json"})
    if response.status != 200:
        return response.status, []
    value = response.json().get("d", {})
    return response.status, value.get("results", []) if isinstance(value, dict) else []


def linked_deliveries(client) -> tuple[int, dict[str, list[dict]]]:
    status, items = get_collection(
        client, SERVICE_ROOT, "A_OutbDeliveryItem",
        {
            "$filter": "ReferenceSDDocument eq '154'",
            "$select": (
                "DeliveryDocument,DeliveryDocumentItem,ReferenceSDDocument,"
                "ReferenceSDDocumentItem,Material,ActualDeliveryQuantity,"
                "DeliveryQuantityUnit,"
                "Plant,StorageLocation"
            ),
            "$top": "100",
        },
    )
    grouped: dict[str, list[dict]] = {}
    for item in items:
        grouped.setdefault(str(item.get("DeliveryDocument")), []).append(item)
    return status, grouped


def preflight(client) -> dict:
    checks: dict[str, dict] = {}
    status, deliveries = linked_deliveries(client)
    checks["NO_EXISTING_DELIVERY"] = {
        "status": "PASS" if status == 200 and not deliveries else "DUPLICATE",
        "http_status": status,
        "delivery_documents": sorted(deliveries),
    }
    header = client.request(
        "GET",
        f"{SALES_SERVICE}/A_SalesOrder('154')?" + urlencode({
            "$select": (
                "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,"
                "OrganizationDivision,SoldToParty,PurchaseOrderByCustomer,OverallSDProcessStatus"
            )
        }),
    )
    header_value = header.json().get("d", {}) if header.status == 200 else {}
    header_ok = all({
        header_value.get("SalesOrder") == "154",
        header_value.get("SalesOrderType") == "CS",
        header_value.get("SalesOrganization") == "FR10",
        header_value.get("DistributionChannel") == "10",
        header_value.get("OrganizationDivision") == "1W",
        header_value.get("SoldToParty") == "1000000112",
        header_value.get("PurchaseOrderByCustomer") == "4-200",
        header_value.get("OverallSDProcessStatus") == "A",
    })
    checks["SOURCE_ORDER"] = {
        "status": "PASS" if header.status == 200 and header_ok else "BLOCKED",
        "http_status": header.status,
        "readback": header_value,
    }
    status, items = get_collection(
        client, SALES_SERVICE, "A_SalesOrderItem",
        {
            "$filter": "SalesOrder eq '154'",
            "$select": (
                "SalesOrderItem,Material,RequestedQuantity,RequestedQuantityUnit,"
                "ProductionPlant,ShippingPoint,SalesDocumentRjcnReason,DeliveryStatus"
            ),
            "$top": "20",
        },
    )
    actual = {str(item.get("SalesOrderItem")): item for item in items}
    expected = {
        "10": ("10000282", "10"),
        "20": ("10000283", "20"),
    }
    items_ok = status == 200 and set(actual) == set(expected)
    for item_id, (material, quantity) in expected.items():
        item = actual.get(item_id, {})
        items_ok = items_ok and all({
            item.get("Material") == material,
            str(item.get("RequestedQuantity")) == quantity,
            item.get("ProductionPlant") == "FR10",
            item.get("ShippingPoint") == "FR10",
            not item.get("SalesDocumentRjcnReason"),
            item.get("DeliveryStatus") == "A",
        })
    checks["SOURCE_ITEMS"] = {
        "status": "PASS" if items_ok else "BLOCKED",
        "http_status": status,
        "readback": items,
    }
    service = client.request(
        "GET", f"{SERVICE_ROOT}/A_OutbDeliveryHeader?" + urlencode({"$select": "DeliveryDocument", "$top": "1"})
    )
    checks["DELIVERY_SERVICE_ACCESS"] = {
        "status": "PASS" if service.status == 200 else "BLOCKED",
        "http_status": service.status,
    }
    return checks


def is_ready(checks: dict) -> bool:
    return all(check.get("status") == "PASS" for check in checks.values())


def load_approval() -> dict:
    value = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED":
        raise RuntimeError("Approval is not active")
    if value.get("operation_scope") != "CREATE_ONE_OUTBOUND_DELIVERY_FROM_SALES_ORDER_154":
        raise RuntimeError("Approval scope mismatch")
    if value.get("environment") != EXPECTED_IDENTITY:
        raise RuntimeError("Approval environment mismatch")
    if value.get("payload_sha256") != fingerprint():
        raise RuntimeError("Approval payload fingerprint mismatch")
    if value.get("constraints", {}).get("maximum_post_attempts") != 1:
        raise RuntimeError("Approval does not enforce one POST")
    return value


def response_delivery(response: HttpResponse) -> str | None:
    try:
        value = response.json().get("d", {})
        if isinstance(value, dict) and value.get("DeliveryDocument"):
            return str(value["DeliveryDocument"])
    except (ValueError, json.JSONDecodeError):
        pass
    match = re.search(r"A_OutbDeliveryHeader\('([^']+)'\)", response.header("Location") or "")
    return match.group(1) if match else None


def delivery_readback(client, delivery: str) -> dict:
    key = delivery.replace("'", "''")
    header = client.request(
        "GET",
        f"{SERVICE_ROOT}/A_OutbDeliveryHeader('{key}')?" + urlencode({
            "$select": (
                "DeliveryDocument,DeliveryDocumentType,ShippingPoint,ShipToParty,"
                "OverallPickingStatus,OverallGoodsMovementStatus,ActualGoodsMovementDate"
            )
        }),
    )
    status, items = get_collection(
        client, SERVICE_ROOT, "A_OutbDeliveryItem",
        {
            "$filter": f"DeliveryDocument eq '{key}'",
            "$select": (
                "DeliveryDocument,DeliveryDocumentItem,ReferenceSDDocument,"
                "ReferenceSDDocumentItem,Material,ActualDeliveryQuantity,"
                "DeliveryQuantityUnit,"
                "Plant,StorageLocation"
            ),
            "$top": "20",
        },
    )
    if header.status != 200 or status != 200:
        raise RuntimeError("Delivery readback did not return HTTP 200")
    return {"header": header.json().get("d", {}), "items": items}


def validate_readback(value: dict, delivery: str) -> list[str]:
    mismatches: list[str] = []
    header = value["header"]
    if header.get("DeliveryDocument") != delivery:
        mismatches.append("delivery ID mismatch")
    if header.get("ShippingPoint") != "FR10":
        mismatches.append("shipping point is not FR10")
    if header.get("OverallGoodsMovementStatus") not in ("A", ""):
        mismatches.append("goods movement is unexpectedly posted")
    by_reference = {
        str(item.get("ReferenceSDDocumentItem", "")).lstrip("0") or "0": item
        for item in value["items"]
    }
    for item_id, material, quantity in (
        ("10", "10000282", "10"),
        ("20", "10000283", "20"),
    ):
        item = by_reference.get(item_id)
        if not item:
            mismatches.append(f"missing reference item {item_id}")
            continue
        if item.get("ReferenceSDDocument") != "154":
            mismatches.append(f"item {item_id} reference mismatch")
        if item.get("Material") != material:
            mismatches.append(f"item {item_id} material mismatch")
        try:
            quantity_matches = Decimal(str(item.get("ActualDeliveryQuantity"))) == Decimal(quantity)
        except InvalidOperation:
            quantity_matches = False
        if not quantity_matches:
            mismatches.append(f"item {item_id} quantity mismatch")
        if item.get("Plant") != "FR10":
            mismatches.append(f"item {item_id} plant mismatch")
        if item.get("StorageLocation") != "0001":
            mismatches.append(f"item {item_id} storage location is not 0001")
    return mismatches


def reconcile(client, before: set[str], response: HttpResponse | None) -> tuple[list[str], str | None]:
    _, after = linked_deliveries(client)
    created = sorted(set(after) - before)
    response_id = response_delivery(response) if response is not None else None
    return created, response_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--reconcile", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username}
    if identity != EXPECTED_IDENTITY:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    if args.reconcile:
        if not RESULT_PATH.exists():
            raise SystemExit("Blocked: no prior delivery result to reconcile")
        previous = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        delivery = previous.get("delivery_document")
        if not delivery:
            raise SystemExit("Blocked: prior result has no delivery document")
        _, linked = linked_deliveries(client)
        if delivery not in linked:
            raise SystemExit("Blocked: delivery is not linked to sales order 154")
        readback = delivery_readback(client, delivery)
        mismatches = validate_readback(readback, delivery)
        status = "VERIFIED" if not mismatches else "CREATED_WITH_READBACK_GAPS"
        result = {
            **previous,
            "reconciled_at_utc": now(),
            "status": status,
            "readback": readback,
            "readback_mismatches": mismatches,
        }
        save(RESULT_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if status == "VERIFIED" else 2
    checks = preflight(client)
    base = {
        "captured_at_utc": now(),
        "environment": identity,
        "operation": "S4600_CH3_EX5_CREATE_DELIVERY_FROM_ORDER_154",
        "payload_sha256": fingerprint(),
        "payload": PAYLOAD,
        "checks": checks,
    }
    if not is_ready(checks):
        result = {**base, "mode": "EXECUTE" if args.execute else "DRY_RUN", "status": "BLOCKED"}
        save(RESULT_PATH if args.execute else DRY_RUN_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    if not args.execute:
        result = {**base, "mode": "DRY_RUN", "status": "DRY_RUN_OK"}
        save(DRY_RUN_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval = load_approval()
    prior = json.loads(DRY_RUN_PATH.read_text(encoding="utf-8")) if DRY_RUN_PATH.exists() else {}
    if prior.get("status") != "DRY_RUN_OK" or prior.get("payload_sha256") != fingerprint():
        raise SystemExit("Blocked: exact successful dry-run is missing")
    if RESULT_PATH.exists():
        previous = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        if previous.get("status") in {"SUBMITTED", "AMBIGUOUS", "CREATED", "VERIFIED"}:
            raise SystemExit("Blocked: prior material attempt requires reconciliation, not retry")

    _, before_map = linked_deliveries(client)
    before = set(before_map)
    token_response = client.request(
        "GET", f"{SERVICE_ROOT}/",
        headers={"X-CSRF-Token": "Fetch", "Accept": "application/json"},
    )
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        raise SystemExit("Blocked: CSRF token fetch failed")
    checkpoint = {
        **base, "mode": "EXECUTE", "status": "SUBMITTED",
        "approval_id": approval["approval_id"], "submitted_at_utc": now(),
        "preexisting_delivery_documents": sorted(before),
    }
    save(RESULT_PATH, checkpoint)

    response: HttpResponse | None = None
    ambiguous = False
    try:
        response = client.request(
            "POST", f"{SERVICE_ROOT}/A_OutbDeliveryHeader",
            headers={"Content-Type": "application/json", "X-CSRF-Token": token},
            body=canonical_bytes(PAYLOAD),
        )
    except AmbiguousTransportError:
        ambiguous = True

    try:
        created, response_id = reconcile(client, before, response)
    except TransportError:
        created, response_id = [], response_delivery(response) if response else None
    if ambiguous:
        status = "RECONCILED_CREATED" if len(created) == 1 else "AMBIGUOUS"
        result = {**checkpoint, "status": status, "new_delivery_documents": created}
        save(RESULT_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if status == "RECONCILED_CREATED" else 2
    assert response is not None
    if response.status != 201:
        result = {
            **checkpoint, "status": "FAILED", "http_status": response.status,
            "error": response.sanitized_sap_error(), "new_delivery_documents": created,
        }
        save(RESULT_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    if len(created) != 1 or response_id not in created:
        result = {
            **checkpoint, "status": "CREATED_WITH_RECONCILIATION_ERROR",
            "http_status": 201, "response_delivery_document": response_id,
            "new_delivery_documents": created,
        }
        save(RESULT_PATH, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    delivery = created[0]
    try:
        readback = delivery_readback(client, delivery)
        mismatches = validate_readback(readback, delivery)
    except (RuntimeError, TransportError, ValueError, json.JSONDecodeError) as error:
        readback = None
        mismatches = [f"readback failed: {type(error).__name__}"]
    status = "VERIFIED" if not mismatches else "CREATED_WITH_READBACK_GAPS"
    result = {
        **checkpoint, "status": status, "http_status": 201,
        "delivery_document": delivery, "response_delivery_document": response_id,
        "readback": readback, "readback_mismatches": mismatches,
    }
    save(RESULT_PATH, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
