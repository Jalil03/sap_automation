"""Targeted, fail-closed READ-only audit for the proposed S4600 FR10 route.

Only HTTP GET is exposed by this script.  The evidence file is intentionally
raw enough to support an independent review and contains no credentials.
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


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_fr10_audit_2026-10-21.json"
ENVIRONMENT = {"system": "A4H", "client": "600", "user": "ABDELJ"}
CUSTOMERS = ("1000000112", "1000000113")
PRODUCTS = ("10000282", "10000283", "10000284", "90000133")


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, service: str, resource: str, query: dict[str, str] | None = None) -> dict:
    path = f"sap/opu/odata/sap/{service}/{resource}"
    if query:
        path += "?" + urlencode(query)
    response = client.request("GET", path, headers={"Accept": "application/json"})
    result = {"http_status": response.status}
    if response.status != 200:
        result["classification"] = "KEY_NOT_FOUND" if response.status == 404 else "READ_ERROR"
        result["error"] = response.sanitized_sap_error()
        return result
    payload = clean(response.json().get("d", {}))
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        result.update(
            classification="ROWS_RETURNED" if payload["results"] else "NO_ROWS_FOR_EXACT_FILTER",
            count=len(payload["results"]),
            rows=payload["results"],
        )
    else:
        result.update(classification="EXACT_KEY_RETURNED", row=payload)
    return result


def filtered(client, service: str, entity: str, expression: str, select: str = "", top: int = 100) -> dict:
    query = {"$filter": expression, "$top": str(top)}
    if select:
        query["$select"] = select
    return get(client, service, entity, query)


def customer_state(client, customer: str) -> dict:
    sales_filter = (
        f"Customer eq '{customer}' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and Division eq '1W'"
    )
    return {
        "root": get(client, "API_BUSINESS_PARTNER", f"A_BusinessPartner('{customer}')"),
        "roles": filtered(
            client, "API_BUSINESS_PARTNER", "A_BusinessPartnerRole",
            f"BusinessPartner eq '{customer}'", "BusinessPartner,BusinessPartnerRole",
        ),
        "customer": get(client, "API_BUSINESS_PARTNER", f"A_Customer('{customer}')"),
        "company_fr10": get(
            client, "API_BUSINESS_PARTNER",
            f"A_CustomerCompany(Customer='{customer}',CompanyCode='FR10')",
        ),
        "sales_fr10_10_1w": get(
            client, "API_BUSINESS_PARTNER",
            f"A_CustomerSalesArea(Customer='{customer}',SalesOrganization='FR10',DistributionChannel='10',Division='1W')",
        ),
        "partner_functions": filtered(
            client, "API_BUSINESS_PARTNER", "A_CustSalesPartnerFunc", sales_filter,
        ),
        "sales_taxes": filtered(
            client, "API_BUSINESS_PARTNER", "A_CustomerSalesAreaTax", sales_filter,
        ),
    }


def product_state(client, product: str) -> dict:
    state = {
        "root": get(client, "API_PRODUCT_SRV", f"A_Product('{product}')"),
    }
    for entity in (
        "A_ProductDescription",
        "A_ProductSalesDelivery",
        "A_ProductSalesTax",
        "A_ProductPlant",
        "A_ProductStorageLocation",
        "A_ProductValuation",
    ):
        state[entity] = filtered(client, "API_PRODUCT_SRV", entity, f"Product eq '{product}'")
    return state


def result_rows(result: dict) -> list[dict]:
    rows = result.get("rows", [])
    return rows if isinstance(rows, list) else []


def document_flow_state(client, sales_orders_result: dict) -> dict:
    orders = [
        row["SalesOrder"] for row in result_rows(sales_orders_result)
        if row.get("SoldToParty") in CUSTOMERS and row.get("SalesOrder")
    ]
    order_items = {
        order: filtered(
            client, "API_SALES_ORDER_SRV", "A_SalesOrderItem",
            f"SalesOrder eq '{order}'", top=100,
        ) for order in orders
    }
    delivery_items_by_order = {
        order: filtered(
            client, "API_OUTBOUND_DELIVERY_SRV", "A_OutbDeliveryItem",
            f"ReferenceSDDocument eq '{order}'", top=100,
        ) for order in orders
    }
    delivery_ids = sorted({
        row["DeliveryDocument"]
        for result in delivery_items_by_order.values()
        for row in result_rows(result)
        if row.get("DeliveryDocument")
    })
    deliveries = {
        delivery: get(
            client, "API_OUTBOUND_DELIVERY_SRV",
            f"A_OutbDeliveryHeader('{delivery}')",
        ) for delivery in delivery_ids
    }
    billing_items_by_delivery = {
        delivery: filtered(
            client, "API_BILLING_DOCUMENT_SRV", "A_BillingDocumentItem",
            f"ReferenceSDDocument eq '{delivery}'", top=100,
        ) for delivery in delivery_ids
    }
    billing_ids = sorted({
        row["BillingDocument"]
        for result in billing_items_by_delivery.values()
        for row in result_rows(result)
        if row.get("BillingDocument")
    })
    billings = {
        billing: get(
            client, "API_BILLING_DOCUMENT_SRV",
            f"A_BillingDocument('{billing}')",
        ) for billing in billing_ids
    }
    return {
        "sales_orders_for_proposed_customers": orders,
        "sales_order_items": order_items,
        "delivery_items_by_sales_order": delivery_items_by_order,
        "deliveries": deliveries,
        "billing_items_by_delivery": billing_items_by_delivery,
        "billings": billings,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    observed = {"client": config.client, "user": config.username.upper()}
    if observed != {"client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Refusing live audit outside A4H/600/ABDELJ: {observed}")
    client = UrllibSapTransport(config)

    sales_orders = filtered(
        client, "API_SALES_ORDER_SRV", "A_SalesOrder",
        "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W'",
        "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,PurchaseOrderByCustomer,OverallSDProcessStatus",
        50,
    )
    evidence = {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": ENVIRONMENT,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "proposal": {"sales_area": "FR10/10/1W", "plant": "FR10", "storage_location": "0001"},
        "organization": {
            "company_code_fr10": get(client, "API_COMPANYCODE_SRV", "A_CompanyCode('FR10')"),
            "plant_fr10": get(client, "API_PLANT_SRV", "A_Plant('FR10')"),
        },
        "customers": {customer: customer_state(client, customer) for customer in CUSTOMERS},
        "products": {product: product_state(client, product) for product in PRODUCTS},
        "pricing": {
            "pr00_type": filtered(
                client, "API_SLSPRICINGPROCEDURE_SRV", "A_SlsPricingConditionType",
                "ConditionType eq 'PR00'", "ConditionType,AccessSequence", 10,
            ),
        },
        "route_evidence": {
            "sales_orders": sales_orders,
            "outbound_deliveries_fr10": filtered(
                client, "API_OUTBOUND_DELIVERY_SRV", "A_OutbDeliveryHeader",
                "ShippingPoint eq 'FR10'", "DeliveryDocument,ShippingPoint,OverallGoodsMovementStatus", 50,
            ),
        },
        "interpretation_rules": [
            "HTTP 200 with an exact key proves presence of that key only.",
            "An empty filtered collection proves no row matched that exact supported filter, not global absence.",
            "READ_ERROR and unsupported entity sets remain UNKNOWN.",
            "Historical documents are supporting evidence, not authorization for a new write.",
        ],
    }
    evidence["document_flow"] = document_flow_state(client, sales_orders)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "environment": evidence["environment"],
        "mode": evidence["mode"],
        "output": str(OUTPUT.relative_to(ROOT)),
        "organization": {key: value["classification"] for key, value in evidence["organization"].items()},
        "customers": {
            key: {name: value["classification"] for name, value in state.items()}
            for key, state in evidence["customers"].items()
        },
        "products": {
            key: {name: value["classification"] for name, value in state.items()}
            for key, state in evidence["products"].items()
        },
        "pricing": {key: value["classification"] for key, value in evidence["pricing"].items()},
        "route_evidence": {key: value["classification"] for key, value in evidence["route_evidence"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
