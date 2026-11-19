"""Controlled one-shot OData execution for S4600 exercise 18 group 00.

This specializes the already proven Exercise 3 execution lifecycle while
keeping an exercise-specific preflight, approval fingerprint and ledger key.
Dry-run remains the default; ``--execute`` permits at most one POST.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.execute_s4600_ex3_group00 as runtime
from scripts.prepare_s4600_ex18_group00 import EXPECTED, PAYLOAD


OBJECT_ID = "S4600_CH5_EX18_SALES_ORDER_STANDARD_GROUP00_FR10"
APPROVAL_PATH = (
    ROOT / "data" / "provisioning" / "s4600" /
    "S4600_CH5_EX18.group00.workflow_approval.json"
)
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex18_group00_result.json"


def approval() -> dict:
    document = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    expected = {
        "status": "APPROVED",
        "operation_scope": "CREATE_ONE_S4600_EX18_GROUP00_SALES_ORDER",
        "payload_sha256": runtime.payload_hash(),
    }
    if any(document.get(key) != value for key, value in expected.items()):
        raise RuntimeError("Exact Exercise 18 approval does not match the candidate operation")
    if document.get("environment") != EXPECTED:
        raise RuntimeError("Exercise 18 approval environment does not match")
    constraints = document.get("constraints", {})
    if constraints.get("maximum_post_attempts") != 1:
        raise RuntimeError("Exercise 18 approval does not enforce one POST attempt")
    if constraints.get("retry_after_ambiguous_or_failed_write") is not False:
        raise RuntimeError("Exercise 18 approval does not prohibit automatic retry")
    return document


def preflight(client, ledger) -> dict:
    checks: dict[str, dict] = {}
    duplicate_filter = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        "SoldToParty eq '1000000113' and PurchaseOrderByCustomer eq '6-100'"
    )
    status, values = runtime.get_rows(
        client, "API_SALES_ORDER_SRV", "A_SalesOrder",
        {"$filter": duplicate_filter, "$select": "SalesOrder", "$top": "2"},
    )
    checks["SAP_DUPLICATE"] = {
        "status": "PASS" if status == 200 and not values else "DUPLICATE",
        "http_status": status,
        "matches": [row.get("SalesOrder") for row in values],
    }

    status, values = runtime.get_rows(
        client, "API_BUSINESS_PARTNER", "A_CustomerSalesArea", {
            "$filter": (
                "Customer eq '1000000113' and SalesOrganization eq 'FR10' and "
                "DistributionChannel eq '10' and Division eq '1W'"
            ),
            "$select": "Customer,CustomerPaymentTerms,SupplyingPlant,Currency",
            "$top": "1",
        },
    )
    customer_ok = (
        status == 200 and len(values) == 1 and
        values[0].get("CustomerPaymentTerms") == "0004" and
        values[0].get("SupplyingPlant") == "FR10" and
        values[0].get("Currency") == "EUR"
    )
    checks["CUSTOMER_SALES_AREA"] = {
        "status": "PASS" if customer_ok else "BLOCKED", "http_status": status,
        "readback": values,
    }

    for product in ("10000282", "10000283"):
        status, values = runtime.get_rows(
            client, "API_PRODUCT_SRV", "A_ProductSalesDelivery", {
                "$filter": (
                    f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and "
                    "ProductDistributionChnl eq '10'"
                ),
                "$select": "Product,SupplyingPlant,ItemCategoryGroup",
                "$top": "1",
            },
        )
        checks[f"PRODUCT_{product}_SALES"] = {
            "status": (
                "PASS" if status == 200 and len(values) == 1 and
                values[0].get("SupplyingPlant") == "FR10" else "BLOCKED"
            ),
            "http_status": status,
        }
        status, units = runtime.get_rows(
            client, "API_PRODUCT_SRV", "A_ProductUnitsOfMeasure", {
                "$filter": f"Product eq '{product}' and AlternativeUnit eq '289'",
                "$select": "Product,AlternativeUnit", "$top": "1",
            },
        )
        checks[f"PRODUCT_{product}_UNIT"] = {
            "status": "PASS" if status == 200 and len(units) == 1 else "BLOCKED",
            "http_status": status,
        }

    service = client.request(
        "GET", runtime.query("A_SalesOrder", {"$select": "SalesOrder", "$top": "1"})
    )
    checks["SERVICE_ACCESS"] = {
        "status": "PASS" if service.status == 200 else "BLOCKED",
        "http_status": service.status,
    }
    conflict = ledger.execution_conflict(
        canonical_object_id=OBJECT_ID,
        correlation_id=runtime.correlation_id(),
        payload_sha256=runtime.payload_hash(),
        customer_reference="6-100",
    )
    checks["LEDGER_DUPLICATE"] = {
        "status": "PASS" if conflict is None else "DUPLICATE",
        "detail": conflict or "no conflict",
    }
    return checks


def specialize_runtime() -> None:
    runtime.PAYLOAD = PAYLOAD
    runtime.EXPECTED_IDENTITY = EXPECTED
    runtime.OBJECT_ID = OBJECT_ID
    runtime.APPROVAL_PATH = APPROVAL_PATH
    runtime.RESULT_PATH = RESULT_PATH
    runtime.CUSTOMER_REFERENCE = "6-100"
    runtime.approval = approval
    runtime.preflight = preflight


if __name__ == "__main__":
    specialize_runtime()
    raise SystemExit(runtime.main())
