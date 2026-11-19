"""Read-only live audit for S4600 group 00 exercises 9 and 11.

Only HTTP GET requests are issued. Negative alias searches are recorded as
bounded evidence and are not, on their own, treated as global absence.
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


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex9_ex11_group00_2026-10-21.json"


def get(client: UrllibSapTransport, service: str, entity: str, **query: str) -> dict:
    path = f"sap/opu/odata/sap/{service}/{entity}"
    if query:
        path += "?" + urlencode(query)
    response = client.request("GET", path)
    result: dict = {"http_status": response.status, "method": "GET"}
    if response.status == 404:
        result["classification"] = "KEY_NOT_FOUND"
        return result
    if response.status != 200:
        result["classification"] = "READ_ERROR"
        result["error"] = response.sanitized_sap_error()
        return result
    payload = response.json().get("d", {})
    rows = payload.get("results") if isinstance(payload, dict) else None
    if isinstance(rows, list):
        clean = [{k: v for k, v in row.items() if k != "__metadata"} for row in rows]
        result.update(classification="ROWS_RETURNED", count=len(clean), rows=clean)
    elif isinstance(payload, dict):
        result.update(
            classification="EXACT_KEY_RETURNED",
            row={k: v for k, v in payload.items() if k != "__metadata"},
        )
    else:
        result["classification"] = "UNEXPECTED_RESPONSE_SHAPE"
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise SystemExit("Audit requires A4H client 600 / user ABDELJ")
    client = UrllibSapTransport(config)

    customer = "T-CUS00"
    product = "T-MS400"
    evidence = {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": config.client, "user": config.username.upper()},
        "mode": "READ_ONLY_HTTP_GET_ONLY",
        "scope": "S4600_GROUP00_EXERCISES_9_11",
        "book_values": {
            "exercise_9": {
                "logical_id": customer,
                "category": "ORGANIZATION",
                "grouping": "BPAB",
                "name": "Motos et autres",
                "roles": ["FLCU00", "FLCU01"],
                "address": {"street": "Rue principale", "house_number": "00", "postal_code": "20111", "city": "Hambourg", "country": "DE", "region": "HH", "language": "EN"},
                "book_sales_area": "1010/10/00",
                "runtime_sales_area_proposal": "FR10/10/1W",
                "currency": "EUR",
                "shipping_condition": "50",
                "book_supplying_plant": "1010",
                "runtime_supplying_plant_proposal": "FR10",
                "incoterms": "DAP",
                "incoterms_location": "Hambourg",
                "payment_terms": "ZB00",
                "customer_account_assignment_group_label": "Revenus intérieurs",
                "customer_pricing_procedure": "S",
                "book_tax": {"country": "DE", "category": "TTX1", "classification": "1"},
                "book_company_code": "1010",
                "runtime_company_code_proposal": "FR10",
                "reconciliation_account": "12100000",
            },
            "exercise_11": {
                "logical_id": product,
                "reference_logical_id": "T-MS100",
                "reference_runtime_mapping": "10000282",
                "industry_label": "Commerce",
                "material_type_label": "Prod. commercialisables",
                "description": "Phare standard",
                "book_plant": "1010",
                "runtime_plant_proposal": "FR10",
                "book_sales_area": "1010/10",
                "runtime_sales_area_proposal": "FR10/10",
                "tax_classification": "1",
                "minimum_order_quantity": 10,
                "minimum_order_unit": "PC",
                "sales_text": "Article fragile !",
                "pricing": {"condition_type": "PR00", "rate": 35, "currency": "EUR", "pricing_unit": 1, "quantity_unit": "PC", "scale_from_quantity": 1},
            },
        },
        "customer_checks": {
            "exact_bp_key": get(client, "API_BUSINESS_PARTNER", f"A_BusinessPartner('{customer}')", **{"$select": "BusinessPartner,BusinessPartnerCategory,BusinessPartnerGrouping,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1"}),
            "exact_customer_key": get(client, "API_BUSINESS_PARTNER", f"A_Customer('{customer}')", **{"$select": "Customer,CustomerAccountGroup"}),
            "external_id": get(client, "API_BUSINESS_PARTNER", "A_BusinessPartner", **{"$filter": f"BusinessPartnerIDByExtSystem eq '{customer}'", "$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1", "$top": "20"}),
            "search_term": get(client, "API_BUSINESS_PARTNER", "A_BusinessPartner", **{"$filter": f"SearchTerm1 eq '{customer}'", "$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1", "$top": "20"}),
            "exact_name": get(client, "API_BUSINESS_PARTNER", "A_BusinessPartner", **{"$filter": "OrganizationBPName1 eq 'Motos et autres'", "$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1", "$top": "20"}),
        },
        "product_checks": {
            "exact_product_key": get(client, "API_PRODUCT_SRV", f"A_Product('{product}')", **{"$select": "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"}),
            "old_id": get(client, "API_PRODUCT_SRV", "A_Product", **{"$filter": f"ProductOldID eq '{product}'", "$select": "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup", "$top": "20"}),
            "exact_description": get(client, "API_PRODUCT_SRV", "A_ProductDescription", **{"$filter": "ProductDescription eq 'Phare standard'", "$select": "Product,Language,ProductDescription", "$top": "50"}),
            "reference_10000282": get(client, "API_PRODUCT_SRV", "A_Product('10000282')", **{"$select": "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"}),
        },
        "pricing_contract": {
            "condition_type_PR00": get(client, "API_SLSPRICINGPROCEDURE_SRV", "A_SlsPricingConditionType", **{"$filter": "ConditionType eq 'PR00'", "$select": "ConditionType,AccessSequence", "$top": "5"}),
            "condition_record_metadata": get(client, "SD_PRICING_CONDITIONRECORD_SRV", "$metadata"),
        },
        "classification_rule": "EXISTS only by deterministic exact/readback evidence; MISSING only where the exercise requires the exact external key and that exact key is reliably absent; otherwise UNKNOWN.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "environment": evidence["environment"],
        "output": str(OUTPUT.relative_to(ROOT)),
        "customer": {k: (v.get("classification"), v.get("count")) for k, v in evidence["customer_checks"].items()},
        "product": {k: (v.get("classification"), v.get("count")) for k, v in evidence["product_checks"].items()},
        "pricing": {k: (v.get("classification"), v.get("http_status")) for k, v in evidence["pricing_contract"].items()},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
