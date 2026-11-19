"""Narrow GET-only readiness audit for S4600 exercises 17, 18, 19, 20 and 36.

The script is deliberately unable to issue a write.  It verifies the exact
A4H/600/ABDELJ identity, checks exercise-specific duplicate references and
captures the customer/product evidence needed before any later TESTRUN.
"""

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


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex17_18_19_20_36_readiness_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, service: str, entity: str, parameters: dict[str, str]) -> dict:
    path = f"sap/opu/odata/sap/{service}/{entity}?{urlencode(parameters)}"
    response = client.request("GET", path, headers={"Accept": "application/json"})
    result = {"http_status": response.status, "request": {"service": service, "entity": entity, **parameters}}
    if response.status != 200:
        result.update(classification="READ_ERROR", error=response.sanitized_sap_error())
        return result
    payload = clean(response.json().get("d", {}))
    rows = payload.get("results", []) if isinstance(payload, dict) else []
    result.update(
        classification="ROWS_RETURNED" if rows else "NO_ROWS_FOR_EXACT_FILTER",
        count=len(rows), rows=rows,
    )
    return result


def exact_duplicate(client, reference: str, customer: str) -> dict:
    expression = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        f"SoldToParty eq '{customer}' and PurchaseOrderByCustomer eq '{reference}'"
    )
    return get(client, "API_SALES_ORDER_SRV", "A_SalesOrder", {
        "$filter": expression,
        "$select": (
            "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,"
            "OrganizationDivision,SoldToParty,PurchaseOrderByCustomer,"
            "RequestedDeliveryDate,OverallSDProcessStatus"
        ),
        "$top": "5",
    })


def customer_sales_area(client, customer: str) -> dict:
    return get(client, "API_BUSINESS_PARTNER", "A_CustomerSalesArea", {
        "$filter": (
            f"Customer eq '{customer}' and SalesOrganization eq 'FR10' and "
            "DistributionChannel eq '10' and Division eq '1W'"
        ),
        "$select": (
            "Customer,SalesOrganization,DistributionChannel,Division,Currency,"
            "CustomerPaymentTerms,ShippingCondition,SupplyingPlant,"
            "CustomerPricingProcedure,CustomerAccountAssignmentGroup"
        ),
        "$top": "2",
    })


def product_state(client, product: str) -> dict:
    return {
        "root": get(client, "API_PRODUCT_SRV", "A_Product", {
            "$filter": f"Product eq '{product}'",
            "$select": "Product,ProductType,BaseUnit,Division,ItemCategoryGroup",
            "$top": "2",
        }),
        "sales_delivery": get(client, "API_PRODUCT_SRV", "A_ProductSalesDelivery", {
            "$filter": (
                f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and "
                "ProductDistributionChnl eq '10'"
            ),
            "$select": "Product,ProductSalesOrg,ProductDistributionChnl,SupplyingPlant",
            "$top": "2",
        }),
        "plant": get(client, "API_PRODUCT_SRV", "A_ProductPlant", {
            "$filter": f"Product eq '{product}' and Plant eq 'FR10'",
            "$select": "Product,Plant,AvailabilityCheckType",
            "$top": "2",
        }),
        "storage": get(client, "API_PRODUCT_SRV", "A_ProductStorageLocation", {
            "$filter": f"Product eq '{product}' and Plant eq 'FR10' and StorageLocation eq '0001'",
            "$select": "Product,Plant,StorageLocation",
            "$top": "2",
        }),
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Refusing live reads outside A4H/600/ABDELJ: {identity!r}")
    client = UrllibSapTransport(config)

    evidence = {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "exercise_targets": {
            "17": {"reference": "3-900", "sold_to": "1000000112", "product": "10000283", "quantity": "10"},
            "18": {"reference": "6-100", "sold_to": "1000000113", "products": {"10000282": "7", "10000283": "8"}},
            "19": {"reference": "6-400", "sold_to": "1000000112", "items": [
                {"product": "10000282", "quantity": "5", "ship_to": "1000000112"},
                {"product": "10000284", "quantity": "1", "ship_to": "1000000113"},
            ]},
            "20": {"customer": "1000000113", "product": "10000284", "plant": "FR10"},
            "36": {"operation": "READ_ONLY_FIORI_ANALYTICS", "currency": "EUR"},
        },
        "duplicate_lookups": {
            "17": exact_duplicate(client, "3-900", "1000000112"),
            "18": exact_duplicate(client, "6-100", "1000000113"),
            "19": exact_duplicate(client, "6-400", "1000000112"),
        },
        "customers": {
            customer: customer_sales_area(client, customer)
            for customer in ("1000000112", "1000000113")
        },
        "products": {
            product: product_state(client, product)
            for product in ("10000282", "10000283", "10000284")
        },
        "historical_item_determination": {
            product: get(client, "API_SALES_ORDER_SRV", "A_SalesOrderItem", {
                "$filter": f"Material eq '{product}'",
                "$select": (
                    "SalesOrder,SalesOrderItem,Material,ProductionPlant,ShippingPoint,"
                    "RequestedQuantity,RequestedQuantityUnit"
                ),
                "$top": "20",
            })
            for product in ("10000282", "10000283", "10000284")
        },
        "exercise_36_note": (
            "OData master-data readiness cannot prove the assigned Fiori tile/catalog. "
            "Exercise 36 remains a GUI/Fiori access validation until the app opens."
        ),
        "interpretation_rules": [
            "Only HTTP GET is used.",
            "NO_ROWS_FOR_EXACT_FILTER proves no match for that exact supported filter only.",
            "READ_ERROR remains UNKNOWN.",
            "No result in this file authorizes a write.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    summary = {
        "output": str(OUTPUT.relative_to(ROOT)),
        "duplicates": {key: value["classification"] for key, value in evidence["duplicate_lookups"].items()},
        "customers": {key: value["classification"] for key, value in evidence["customers"].items()},
        "products": {
            key: {name: result["classification"] for name, result in value.items()}
            for key, value in evidence["products"].items()
        },
        "historical_item_determination": {
            key: value["classification"]
            for key, value in evidence["historical_item_determination"].items()
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
