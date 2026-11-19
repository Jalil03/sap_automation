"""One-shot controlled creation of the S4600 Exercise 3 group-00 order.

Dry-run is the default.  ``--execute`` requires the exact recorded approval,
repeats all live GET checks, records SUBMITTED before the POST, never retries,
and performs an independent GET readback after an unambiguous HTTP 201.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.prepare_s4600_ex3_group00 import EXPECTED_IDENTITY, PAYLOAD, clean
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError, TransportError
from src.sap_runtime.ledger import ExecutionLedger
from src.sap_runtime.models import ExecutionStatus
from src.sap_runtime.transport import HttpResponse, UrllibSapTransport


OBJECT_ID = "S4600_CH3_EX3_SALES_ORDER_STANDARD_GROUP00_FR10"
APPROVAL_PATH = (
    ROOT / "data" / "provisioning" / "s4600" /
    "S4600_CH3_EX3.group00.workflow_approval.json"
)
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex3_group00_result.json"
SERVICE_ROOT = "sap/opu/odata/sap/API_SALES_ORDER_SRV"
CUSTOMER_REFERENCE = "4-200"


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def payload_hash() -> str:
    return hashlib.sha256(canonical_bytes(PAYLOAD)).hexdigest()


def correlation_id() -> str:
    value = hashlib.sha256(f"{OBJECT_ID}|{payload_hash()}".encode()).hexdigest()[:20].upper()
    return f"SO-RUNTIME-{value}"


def query(entity: str, parameters: dict[str, str]) -> str:
    return f"{SERVICE_ROOT}/{entity}?{urlencode(parameters)}"


def rows(response: HttpResponse) -> list[dict]:
    if response.status != 200:
        return []
    value = response.json().get("d", {})
    return value.get("results", []) if isinstance(value, dict) else []


def get_rows(client, service: str, entity: str, parameters: dict[str, str]) -> tuple[int, list[dict]]:
    path = f"sap/opu/odata/sap/{service}/{entity}?{urlencode(parameters)}"
    response = client.request("GET", path, headers={"Accept": "application/json"})
    value = response.json().get("d", {}) if response.status == 200 else {}
    result = value.get("results", []) if isinstance(value, dict) else []
    return response.status, clean(result)


def approval() -> dict:
    document = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    expected = {
        "status": "APPROVED",
        "operation_scope": "CREATE_ONE_S4600_EX3_GROUP00_SALES_ORDER",
        "payload_sha256": payload_hash(),
    }
    if any(document.get(key) != value for key, value in expected.items()):
        raise RuntimeError("Exact workflow approval does not match the candidate operation")
    if document.get("environment") != EXPECTED_IDENTITY:
        raise RuntimeError("Workflow approval environment does not match")
    if document.get("constraints", {}).get("maximum_post_attempts") != 1:
        raise RuntimeError("Workflow approval does not enforce one POST attempt")
    return document


def preflight(client, ledger: ExecutionLedger) -> dict:
    checks: dict[str, dict] = {}
    duplicate_filter = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        "SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '4-200'"
    )
    status, duplicate_rows = get_rows(
        client, "API_SALES_ORDER_SRV", "A_SalesOrder",
        {"$filter": duplicate_filter, "$select": "SalesOrder", "$top": "2"},
    )
    checks["SAP_DUPLICATE"] = {
        "status": "PASS" if status == 200 and not duplicate_rows else "DUPLICATE",
        "http_status": status,
        "matches": [row.get("SalesOrder") for row in duplicate_rows],
    }

    status, customer_rows = get_rows(
        client, "API_BUSINESS_PARTNER", "A_CustomerSalesArea",
        {
            "$filter": (
                "Customer eq '1000000112' and SalesOrganization eq 'FR10' and "
                "DistributionChannel eq '10' and Division eq '1W'"
            ),
            "$select": "Customer,SalesOrganization,DistributionChannel,Division",
            "$top": "1",
        },
    )
    checks["CUSTOMER_SALES_AREA"] = {
        "status": "PASS" if status == 200 and len(customer_rows) == 1 else "BLOCKED",
        "http_status": status,
    }

    status, type_rows = get_rows(
        client, "API_SALES_ORDER_SRV", "A_SalesOrder",
        {
            "$filter": (
                "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
                "DistributionChannel eq '10' and OrganizationDivision eq '1W'"
            ),
            "$select": "SalesOrder,SalesOrderType",
            "$top": "1",
        },
    )
    checks["CS_ROUTE_EVIDENCE"] = {
        "status": "PASS" if status == 200 and len(type_rows) == 1 else "BLOCKED",
        "http_status": status,
        "evidence_order": type_rows[0].get("SalesOrder") if type_rows else None,
    }

    for product in ("10000282", "10000283"):
        status, sales_rows = get_rows(
            client, "API_PRODUCT_SRV", "A_ProductSalesDelivery",
            {
                "$filter": (
                    f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and "
                    "ProductDistributionChnl eq '10'"
                ),
                "$select": "Product,ProductSalesOrg,ProductDistributionChnl,SupplyingPlant",
                "$top": "1",
            },
        )
        checks[f"PRODUCT_{product}_SALES"] = {
            "status": (
                "PASS" if status == 200 and len(sales_rows) == 1 and
                sales_rows[0].get("SupplyingPlant") == "FR10" else "BLOCKED"
            ),
            "http_status": status,
        }
        status, unit_rows = get_rows(
            client, "API_PRODUCT_SRV", "A_ProductUnitsOfMeasure",
            {
                "$filter": f"Product eq '{product}' and AlternativeUnit eq '289'",
                "$select": "Product,AlternativeUnit",
                "$top": "1",
            },
        )
        checks[f"PRODUCT_{product}_UNIT"] = {
            "status": "PASS" if status == 200 and len(unit_rows) == 1 else "BLOCKED",
            "http_status": status,
        }

    service = client.request(
        "GET", query("A_SalesOrder", {"$select": "SalesOrder", "$top": "1"})
    )
    checks["SERVICE_ACCESS"] = {
        "status": "PASS" if service.status == 200 else "BLOCKED",
        "http_status": service.status,
    }
    conflict = ledger.execution_conflict(
        canonical_object_id=OBJECT_ID,
        correlation_id=correlation_id(),
        payload_sha256=payload_hash(),
        customer_reference=CUSTOMER_REFERENCE,
    )
    checks["LEDGER_DUPLICATE"] = {
        "status": "PASS" if conflict is None else "DUPLICATE",
        "detail": conflict or "no conflict",
    }
    return checks


def ready(checks: dict) -> bool:
    return all(check.get("status") == "PASS" for check in checks.values())


def created_id(response: HttpResponse) -> str | None:
    try:
        value = response.json().get("d", {})
        if isinstance(value, dict) and value.get("SalesOrder"):
            return str(value["SalesOrder"])
    except (ValueError, json.JSONDecodeError):
        pass
    match = re.search(r"A_SalesOrder\('([^']+)'\)", response.header("Location") or "")
    return match.group(1) if match else None


def readback(client, sales_order: str) -> dict:
    key = sales_order.replace("'", "''")
    header = client.request(
        "GET",
        query(
            f"A_SalesOrder('{key}')",
            {"$select": (
                "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,"
                "OrganizationDivision,SoldToParty,PurchaseOrderByCustomer,"
                "CustomerPurchaseOrderDate,RequestedDeliveryDate,OverallSDProcessStatus"
            )},
        ),
    )
    items = client.request(
        "GET",
        query(
            "A_SalesOrderItem",
            {
                "$filter": f"SalesOrder eq '{key}'",
                "$select": (
                    "SalesOrder,SalesOrderItem,Material,RequestedQuantity,"
                    "RequestedQuantityUnit,RequestedQuantitySAPUnit,RequestedQuantityISOUnit,"
                    "ProductionPlant,ShippingPoint,NetAmount,TransactionCurrency"
                ),
            },
        ),
    )
    if header.status != 200 or items.status != 200:
        raise RuntimeError("Independent readback did not return HTTP 200")
    return {
        "header": clean(header.json().get("d", {})),
        "items": clean(items.json().get("d", {}).get("results", [])),
    }


def verify_readback(value: dict) -> list[str]:
    mismatches: list[str] = []
    header = value["header"]
    for field in (
        "SalesOrderType", "SalesOrganization", "DistributionChannel",
        "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
        "CustomerPurchaseOrderDate", "RequestedDeliveryDate",
    ):
        if header.get(field) != PAYLOAD.get(field):
            mismatches.append(f"header {field} mismatch")
    actual = {str(row.get("SalesOrderItem")): row for row in value["items"]}
    for expected in PAYLOAD["to_Item"]:
        row = actual.get(expected["SalesOrderItem"])
        if not row:
            mismatches.append(f"missing item {expected['SalesOrderItem']}")
            continue
        for field in ("Material", "RequestedQuantity", "RequestedQuantityUnit"):
            if str(row.get(field)) != str(expected[field]):
                mismatches.append(f"item {expected['SalesOrderItem']} {field} mismatch")
        if row.get("ProductionPlant") != "FR10":
            mismatches.append(f"item {expected['SalesOrderItem']} ProductionPlant mismatch")
        if row.get("ShippingPoint") != "FR10":
            mismatches.append(f"item {expected['SalesOrderItem']} ShippingPoint mismatch")
    return mismatches


def save(result: dict) -> None:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username}
    if identity != EXPECTED_IDENTITY:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")

    client = UrllibSapTransport(config)
    ledger = ExecutionLedger(config.ledger_path)
    checks = preflight(client, ledger)
    base = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": OBJECT_ID,
        "payload_sha256": payload_hash(),
        "candidate_payload": PAYLOAD,
        "checks": checks,
    }
    if not ready(checks):
        result = {**base, "mode": "EXECUTE" if args.execute else "DRY_RUN", "status": "BLOCKED"}
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    if not args.execute:
        entry = ledger.start(
            canonical_object_id=OBJECT_ID, correlation_id=correlation_id(),
            customer_reference=CUSTOMER_REFERENCE, payload_sha256=payload_hash(),
            mode="DRY_RUN", status=ExecutionStatus.DRY_RUN_OK,
        )
        ledger.finish(entry, status=ExecutionStatus.DRY_RUN_OK)
        result = {**base, "mode": "DRY_RUN", "status": "DRY_RUN_OK"}
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval_document = approval()
    if not ledger.has_successful_dry_run(OBJECT_ID, payload_hash()):
        raise SystemExit("Blocked: no successful dry-run for the exact payload")
    token_response = client.request(
        "GET", f"{SERVICE_ROOT}/",
        headers={"X-CSRF-Token": "Fetch", "Accept": "application/json"},
    )
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        raise SystemExit("Blocked: CSRF token fetch failed")

    entry = ledger.start(
        canonical_object_id=OBJECT_ID, correlation_id=correlation_id(),
        customer_reference=CUSTOMER_REFERENCE, payload_sha256=payload_hash(),
        mode="EXECUTE", status=ExecutionStatus.SUBMITTED,
    )
    try:
        response = client.request(
            "POST", f"{SERVICE_ROOT}/A_SalesOrder",
            headers={"Content-Type": "application/json", "X-CSRF-Token": token},
            body=canonical_bytes(PAYLOAD),
        )
    except AmbiguousTransportError:
        ledger.finish(entry, status=ExecutionStatus.AMBIGUOUS, sanitized_error="ambiguous POST transport outcome")
        result = {**base, "mode": "EXECUTE", "status": "AMBIGUOUS", "approval_id": approval_document["approval_id"]}
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    if response.status != 201:
        error = response.sanitized_sap_error()
        ledger.finish(
            entry, status=ExecutionStatus.FAILED, http_status=response.status,
            sanitized_error=json.dumps(error, ensure_ascii=False),
        )
        result = {
            **base, "mode": "EXECUTE", "status": "FAILED",
            "approval_id": approval_document["approval_id"], "http_status": response.status,
            "error": error,
        }
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    sales_order = created_id(response)
    if not sales_order:
        ledger.finish(entry, status=ExecutionStatus.FAILED, http_status=201, sanitized_error="missing created ID")
        result = {**base, "mode": "EXECUTE", "status": "FAILED", "http_status": 201, "error": "missing created ID"}
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    ledger.finish(
        entry, status=ExecutionStatus.CREATED, http_status=201,
        created_sales_order_id=sales_order, response_etag=response.header("ETag"),
    )
    try:
        value = readback(client, sales_order)
        mismatches = verify_readback(value)
    except (TransportError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        value = None
        mismatches = [f"readback failed: {type(error).__name__}"]
    final_status = ExecutionStatus.VERIFIED if not mismatches else ExecutionStatus.FAILED
    ledger.finish(
        entry, status=final_status, http_status=201, created_sales_order_id=sales_order,
        response_etag=response.header("ETag"),
        sanitized_error="; ".join(mismatches) if mismatches else None,
    )
    result = {
        **base, "mode": "EXECUTE", "status": final_status.value,
        "approval_id": approval_document["approval_id"], "http_status": 201,
        "created_sales_order_id": sales_order, "readback": value,
        "readback_mismatches": mismatches,
    }
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if final_status == ExecutionStatus.VERIFIED else 2


if __name__ == "__main__":
    raise SystemExit(main())
