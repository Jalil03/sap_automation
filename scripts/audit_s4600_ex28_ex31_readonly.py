"""Strict GET-only audit for S4600 exercises 28 and 31 on A4H/600.

The script probes only interfaces already evidenced in the repository and
persists sanitized, bounded evidence.  It cannot submit or modify SAP data.
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_ex31_audit_2026-10-21.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}


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
    result = {"service": service, "resource": resource, "http_status": response.status}
    if response.status != 200:
        result["classification"] = "READ_ERROR"
        result["error"] = response.sanitized_sap_error()
        return result
    payload = clean(response.json().get("d", {}))
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        rows = payload["results"]
        result.update(
            classification="ROWS_RETURNED" if rows else "NO_ROWS_FOR_EXACT_FILTER",
            count=len(rows),
            rows=rows,
        )
    else:
        result.update(classification="EXACT_KEY_RETURNED", row=payload)
    return result


def metadata(client, service: str) -> dict:
    response = client.request("GET", f"sap/opu/odata/sap/{service}/$metadata")
    result = {"service": service, "http_status": response.status}
    if response.status != 200:
        result["classification"] = "READ_ERROR"
        result["error"] = response.sanitized_sap_error()
        return result
    try:
        root = ET.fromstring(response.body)
    except ET.ParseError:
        return {**result, "classification": "INVALID_METADATA_XML"}
    sets = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] == "EntitySet":
            name = node.attrib.get("Name")
            if name:
                sets.append(name)
    result.update(classification="METADATA_RETURNED", entity_sets=sorted(set(sets)))
    return result


def rows(result: dict) -> list[dict]:
    value = result.get("rows", [])
    return value if isinstance(value, list) else []


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    actual = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if actual != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {actual!r}")
    client = UrllibSapTransport(config)

    service_metadata = {
        name: metadata(client, name)
        for name in (
            "API_SALES_INQUIRY_SRV",
            "ZAPI_SALES_INQUIRY_SRV_0001",
            "API_SALES_QUOTATION_SRV",
            "ZAPI_SALES_QUOTATION_SRV_0001",
        )
    }
    sales_types = {
        code: get(
            client,
            "API_SALESORDERTYPE_SRV",
            "A_SalesOrderType",
            {"$filter": f"SalesDocumentType eq '{code}'", "$select": "SalesDocumentType", "$top": "2"},
        )
        for code in ("AF", "AG", "TA")
    }
    presales_documents = {
        "inquiries_fr10_customer": get(
            client,
            "API_SALES_INQUIRY_SRV",
            "A_SalesInquiry",
            {
                "$filter": (
                    "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and "
                    "OrganizationDivision eq '1W' and SoldToParty eq '1000000112'"
                ),
                "$top": "50",
            },
        ),
        "quotations_fr10_customer": get(
            client,
            "API_SALES_QUOTATION_SRV",
            "A_SalesQuotation",
            {
                "$filter": (
                    "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and "
                    "OrganizationDivision eq '1W' and SoldToParty eq '1000000112'"
                ),
                "$top": "50",
            },
        ),
    }
    service_items = get(
        client,
        "API_SALES_ORDER_SRV",
        "A_SalesOrderItem",
        {
            "$filter": "Material eq '90000133'",
            "$select": (
                "SalesOrder,SalesOrderItem,SalesOrderItemCategory,Material,RequestedQuantity,"
                "RequestedQuantityUnit,TransactionCurrency,NetAmount,OrderRelatedBillingStatus,"
                "ProductionPlant,ShippingPoint"
            ),
            "$top": "50",
        },
    )
    service_headers = {}
    pricing = {}
    for item in rows(service_items):
        order = item.get("SalesOrder")
        position = item.get("SalesOrderItem")
        if not order or not position:
            continue
        service_headers[order] = get(
            client,
            "API_SALES_ORDER_SRV",
            f"A_SalesOrder('{order}')",
        )
        pricing[f"{order}/{position}"] = get(
            client,
            "API_SALES_ORDER_SRV",
            f"A_SalesOrderItem(SalesOrder='{order}',SalesOrderItem='{position}')/to_PricingElement",
            {"$top": "100"},
        )

    product = {
        "root": get(client, "API_PRODUCT_SRV", "A_Product('90000133')"),
        "sales": get(
            client,
            "API_PRODUCT_SRV",
            "A_ProductSalesDelivery",
            {
                "$filter": (
                    "Product eq '90000133' and ProductSalesOrg eq 'FR10' and "
                    "ProductDistributionChnl eq '10'"
                ),
                "$top": "10",
            },
        ),
    }
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": actual,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "scope": ["S4600_CH8_EX28", "S4600_CH8_EX31"],
        "service_metadata": service_metadata,
        "sales_document_types_internal": sales_types,
        "historical_presales_documents": presales_documents,
        "service_product_90000133": product,
        "historical_service_order_items": service_items,
        "historical_service_order_headers": service_headers,
        "historical_service_item_pricing": pricing,
        "interpretation_rules": [
            "HTTP 200 metadata proves the service is reachable, not that copy control is configured.",
            "Historical documents prove only their observed determination and flow.",
            "No matching historical row does not prove customizing or condition-record absence.",
            "READ_ERROR remains UNKNOWN.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "output": str(OUTPUT.relative_to(ROOT)),
        "environment": actual,
        "service_metadata": {key: value["classification"] for key, value in service_metadata.items()},
        "sales_document_types_internal": {key: value["classification"] for key, value in sales_types.items()},
        "historical_presales_documents": {
            key: {"classification": value["classification"], "count": value.get("count")}
            for key, value in presales_documents.items()
        },
        "service_items": {"classification": service_items["classification"], "count": service_items.get("count")},
        "service_item_categories": sorted({str(item.get("SalesOrderItemCategory")) for item in rows(service_items)}),
        "pricing_conditions": sorted({
            str(row.get("ConditionType"))
            for result in pricing.values() for row in rows(result) if row.get("ConditionType")
        }),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
