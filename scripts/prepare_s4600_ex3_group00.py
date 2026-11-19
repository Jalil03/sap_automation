"""Read-only preflight for the S4600 exercise 3 group-00 FR10 pilot.

This script deliberately exposes GET only.  It prepares the exact candidate
payload, performs anti-duplicate and dependency lookups, and persists evidence.
It cannot submit or modify an SAP document.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex3_group00_preflight_2026-10-21.json"
EXPECTED_IDENTITY = {"system": "A4H", "client": "600", "user": "ABDELJ"}


def odata_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    instant = datetime.combine(parsed, time.min, tzinfo=timezone.utc)
    return f"/Date({int(instant.timestamp() * 1000)})/"


PAYLOAD = {
    "SalesOrderType": "CS",
    "SalesOrganization": "FR10",
    "DistributionChannel": "10",
    "OrganizationDivision": "1W",
    "SoldToParty": "1000000112",
    "PurchaseOrderByCustomer": "4-200",
    "CustomerPurchaseOrderDate": odata_date("2026-10-21"),
    "RequestedDeliveryDate": odata_date("2026-10-28"),
    "to_Item": [
        {
            "SalesOrderItem": "10",
            "Material": "10000282",
            "RequestedQuantity": "10",
            "RequestedQuantityUnit": "289",
        },
        {
            "SalesOrderItem": "20",
            "Material": "10000283",
            "RequestedQuantity": "20",
            "RequestedQuantityUnit": "289",
        },
    ],
}


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, service: str, entity: str, query: dict[str, str]) -> dict:
    path = f"sap/opu/odata/sap/{service}/{entity}?{urlencode(query)}"
    response = client.request("GET", path, headers={"Accept": "application/json"})
    if response.status != 200:
        return {
            "http_status": response.status,
            "classification": "READ_ERROR",
            "error": response.sanitized_sap_error(),
        }
    data = clean(response.json().get("d", {}))
    rows = data.get("results") if isinstance(data, dict) else None
    return {
        "http_status": response.status,
        "classification": (
            "ROWS_RETURNED" if isinstance(rows, list) and rows else
            "NO_ROWS_FOR_EXACT_FILTER" if isinstance(rows, list) else
            "EXACT_KEY_RETURNED"
        ),
        "count": len(rows) if isinstance(rows, list) else 1,
        "rows": rows if isinstance(rows, list) else [data],
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    actual_identity = {
        "system": "A4H",
        "client": config.client,
        "user": config.username,
    }
    if actual_identity != EXPECTED_IDENTITY:
        raise SystemExit(f"Blocked: unexpected SAP identity {actual_identity!r}")
    client = UrllibSapTransport(config)

    exact_header = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        "SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '4-200'"
    )
    checks = {
        "duplicate_exact_header": get(
            client, "API_SALES_ORDER_SRV", "A_SalesOrder",
            {"$filter": exact_header, "$select": "SalesOrder,PurchaseOrderByCustomer", "$top": "5"},
        ),
        "sales_order_type_catalog": get(
            client, "API_SALESORDERTYPE_SRV", "A_SalesOrderType",
            {"$select": "SalesDocumentType", "$top": "300"},
        ),
        "existing_cs_order_fr10": get(
            client, "API_SALES_ORDER_SRV", "A_SalesOrder",
            {
                "$filter": (
                    "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
                    "DistributionChannel eq '10' and OrganizationDivision eq '1W'"
                ),
                "$select": "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision",
                "$top": "1",
            },
        ),
        "customer_sales_area": get(
            client, "API_BUSINESS_PARTNER", "A_CustomerSalesArea",
            {
                "$filter": (
                    "Customer eq '1000000112' and SalesOrganization eq 'FR10' and "
                    "DistributionChannel eq '10' and Division eq '1W'"
                ),
                "$select": "Customer,SalesOrganization,DistributionChannel,Division,Currency,ShippingCondition",
                "$top": "1",
            },
        ),
    }
    for product in ("10000282", "10000283"):
        checks[f"product_{product}_sales"] = get(
            client, "API_PRODUCT_SRV", "A_ProductSalesDelivery",
            {
                "$filter": (
                    f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and "
                    "ProductDistributionChnl eq '10'"
                ),
                "$select": "Product,ProductSalesOrg,ProductDistributionChnl,SupplyingPlant,ItemCategoryGroup",
                "$top": "1",
            },
        )
        checks[f"product_{product}_plant"] = get(
            client, "API_PRODUCT_SRV", "A_ProductPlant",
            {
                "$filter": f"Product eq '{product}' and Plant eq 'FR10'",
                "$select": "Product,Plant,AvailabilityCheckType",
                "$top": "1",
            },
        )
        checks[f"product_{product}_units"] = get(
            client, "API_PRODUCT_SRV", "A_ProductUnitsOfMeasure",
            {
                "$filter": f"Product eq '{product}'",
                "$select": "Product,AlternativeUnit",
                "$top": "20",
            },
        )

    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": actual_identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "operation": "S4600_CH3_EX3_SALES_ORDER_STANDARD_GROUP00_FR10_PREFLIGHT",
        "candidate_payload_not_submitted": PAYLOAD,
        "checks": checks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "output": str(OUTPUT.relative_to(ROOT)),
        "environment": actual_identity,
        "mode": evidence["mode"],
        "checks": {
            name: {
                "classification": result["classification"],
                "count": result.get("count"),
            }
            for name, result in checks.items()
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
