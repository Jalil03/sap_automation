"""Final bounded GET-only audit for S4600 and S4615 in A4H/600.

The script deliberately has no file output and exposes no mutating verb.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICES = {
    "bp": "sap/opu/odata/sap/API_BUSINESS_PARTNER/",
    "product": "sap/opu/odata/sap/API_PRODUCT_SRV/",
    "plant": "sap/opu/odata/sap/API_PLANT_SRV/",
    "company": "sap/opu/odata/sap/API_COMPANYCODE_SRV/",
    "warehouse": "sap/opu/odata/sap/API_WAREHOUSE/",
    "sales_order": "sap/opu/odata/sap/API_SALES_ORDER_SRV/",
    "pricing": "sap/opu/odata/sap/API_SLSPRICINGPROCEDURE_SRV/",
}


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, service: str, resource: str, params: dict[str, str] | None = None):
    path = SERVICES[service] + resource
    if params:
        path += "?" + urlencode(params)
    response = client.request("GET", path, headers={"Accept": "application/json"})
    result = {"http": response.status}
    if response.status == 200:
        result["data"] = clean(response.json().get("d", {}))
    else:
        result["error"] = response.sanitized_sap_error()
    return result


def filtered(client, service: str, entity: str, expression: str, select: str = "", top: int = 50):
    params = {"$filter": expression, "$top": str(top)}
    if select:
        params["$select"] = select
    return get(client, service, entity, params)


def bp_state(client, bp: str):
    return {
        "root": get(client, "bp", f"A_BusinessPartner('{bp}')", {"$select": "BusinessPartner,BusinessPartnerCategory,BusinessPartnerGrouping,OrganizationBPName1,SearchTerm1"}),
        "addresses": filtered(client, "bp", "A_BusinessPartnerAddress", f"BusinessPartner eq '{bp}'", "BusinessPartner,AddressID,StreetName,HouseNumber,PostalCode,CityName,Country,Region,Language"),
        "roles": filtered(client, "bp", "A_BusinessPartnerRole", f"BusinessPartner eq '{bp}'", "BusinessPartner,BusinessPartnerRole"),
        "customer": get(client, "bp", f"A_Customer('{bp}')", {"$select": "Customer,CustomerAccountGroup"}),
        "company_1010": get(client, "bp", f"A_CustomerCompany(Customer='{bp}',CompanyCode='1010')"),
        "sales_1010_10_00": get(client, "bp", f"A_CustomerSalesArea(Customer='{bp}',SalesOrganization='1010',DistributionChannel='10',Division='00')"),
        "partners": filtered(client, "bp", "A_CustSalesPartnerFunc", f"Customer eq '{bp}' and SalesOrganization eq '1010' and DistributionChannel eq '10' and Division eq '00'"),
        "tax": filtered(client, "bp", "A_CustomerSalesAreaTax", f"Customer eq '{bp}'"),
    }


def product_state(client, product: str):
    entities = (
        "A_ProductDescription", "A_ProductSalesDelivery", "A_ProductSalesTax",
        "A_ProductPlant", "A_ProductValuation", "A_ProductValuationAccount",
        "A_ProductValuationCosting", "A_ProductMLAccount", "A_ProductPlantCosting",
    )
    result = {
        "root": get(client, "product", f"A_Product('{product}')", {"$select": "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"})
    }
    for entity in entities:
        result[entity] = filtered(client, "product", entity, f"Product eq '{product}'", top=100)
    return result


def metadata(client, service_name: str):
    response = client.request("GET", f"sap/opu/odata/sap/{service_name}/$metadata?sap-client=600", headers={"Accept": "application/xml"})
    result = {"http": response.status}
    if response.status != 200:
        result["error"] = response.sanitized_sap_error()
    return result


def rows(result):
    data = result.get("data", {}) if isinstance(result, dict) else {}
    value = data.get("results", []) if isinstance(data, dict) else []
    return value if isinstance(value, list) else []


def compact_output(output):
    compact = {
        "captured_at_utc": output["captured_at_utc"],
        "mode": output["mode"],
        "environment": output["environment"],
        "business_partners": {},
        "products": {},
        "unresolved_business_partner_lookups": {},
        "unresolved_product_lookups": {},
        "organization": output["organization"],
        "condition_types": output["condition_types"],
        "service_metadata": output["service_metadata"],
        "sales_order_references": {},
    }
    for logical, state in output["business_partners"].items():
        compact["business_partners"][logical] = {
            "root": state["root"],
            "addresses": rows(state["addresses"]),
            "roles": rows(state["roles"]),
            "customer_http": state["customer"]["http"],
            "customer": state["customer"].get("data"),
            "company_1010_http": state["company_1010"]["http"],
            "company_1010": state["company_1010"].get("data"),
            "sales_1010_10_00_http": state["sales_1010_10_00"]["http"],
            "sales_1010_10_00": state["sales_1010_10_00"].get("data"),
            "partner_functions": [row.get("PartnerFunction") for row in rows(state["partners"])],
            "tax": rows(state["tax"]),
        }
    for logical, state in output["products"].items():
        root = state["root"]
        compact["products"][logical] = {
            "root": root,
            "descriptions": rows(state["A_ProductDescription"]),
            "sales_delivery": rows(state["A_ProductSalesDelivery"]),
            "sales_tax": rows(state["A_ProductSalesTax"]),
            "plants": rows(state["A_ProductPlant"]),
            "valuation": rows(state["A_ProductValuation"]),
            "valuation_account": rows(state["A_ProductValuationAccount"]),
            "ml_account": rows(state["A_ProductMLAccount"]),
        }
    for logical, state in output["unresolved_business_partner_lookups"].items():
        compact["unresolved_business_partner_lookups"][logical] = {
            "literal_http": state["literal_bp"]["http"], "search_term_rows": rows(state["search_term"])
        }
    for logical, state in output["unresolved_product_lookups"].items():
        compact["unresolved_product_lookups"][logical] = {
            "literal_http": state["literal_product"]["http"], "old_id_rows": rows(state["old_id"])
        }
    for reference, state in output["sales_order_references"].items():
        compact["sales_order_references"][reference] = {"http": state["http"], "rows": rows(state)}
    return compact


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("This audit is restricted to A4H/600/ABDELJ")
    client = UrllibSapTransport(config)

    if "--supplemental-references" in sys.argv:
        references = ("01S4615-KO", "01S4615-Réf")
        result = {
            reference: filtered(
                client, "sales_order", "A_SalesOrder",
                f"PurchaseOrderByCustomer eq '{reference}'",
                "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,PurchaseOrderByCustomer",
                20,
            ) for reference in references
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    bps = {logical: bp_state(client, sap_id) for logical, sap_id in {
        "T-S50A01": "1000000116", "C615-A01": "1000000115", "C615-D00": "1000000114",
    }.items()}
    products = {logical: product_state(client, sap_id) for logical, sap_id in {
        "T-D101": "90000132", "T-MS101": "60000445", "T-MS201": "60000446",
        "P615-101": "10000289", "P615-400": "10000287",
    }.items()}

    unresolved_bp = {}
    for logical in ("T-S50B01", "T-CUS01", "C615-B01", "C615-C01", "C615-E01", "C615-F01"):
        unresolved_bp[logical] = {
            "literal_bp": get(client, "bp", f"A_BusinessPartner('{logical}')"),
            "search_term": filtered(client, "bp", "A_BusinessPartner", f"SearchTerm1 eq '{logical}'", "BusinessPartner,OrganizationBPName1,SearchTerm1", 20),
        }
    unresolved_product = {}
    for logical in ("T-MS301", "T-MS401", "T-F101", "P615-201", "P615-501", "P615-601"):
        unresolved_product[logical] = {
            "literal_product": get(client, "product", f"A_Product('{logical}')"),
            "old_id": filtered(client, "product", "A_Product", f"ProductOldID eq '{logical}'", "Product,ProductOldID,ProductType,BaseUnit,Division", 20),
        }

    references = (
        "01S4615-A1", "01S4615-A3", "01S4615-A4", "01S4615-A5", "01S4615-A6",
        "01S4615-A10", "01S4615-BV", "01S4615-PF", "01S4615-BS", "01S4615-AZ",
        "01S6415-PB", "01S4615-PB",
    )
    documents = {
        reference: filtered(
            client, "sales_order", "A_SalesOrder",
            f"PurchaseOrderByCustomer eq '{reference}'",
            "SalesOrder,SalesOrderType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,PurchaseOrderByCustomer",
            50,
        ) for reference in references
    }

    output = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "STRICT_READ_ONLY_GET",
        "environment": {"system": "A4H", "client": config.client, "user": config.username.upper()},
        "business_partners": bps,
        "products": products,
        "unresolved_business_partner_lookups": unresolved_bp,
        "unresolved_product_lookups": unresolved_product,
        "organization": {
            "plant_1010": get(client, "plant", "A_Plant('1010')"),
            "plant_1020": get(client, "plant", "A_Plant('1020')"),
            "plant_1710": get(client, "plant", "A_Plant('1710')"),
            "company_1010": get(client, "company", "A_CompanyCode('1010')"),
            "company_1710": get(client, "company", "A_CompanyCode('1710')"),
            "warehouse_1010": get(client, "warehouse", "Warehouse('1010')"),
        },
        "condition_types": {
            code: filtered(client, "pricing", "A_SlsPricingConditionType", f"ConditionType eq '{code}'", "ConditionType,AccessSequence", 10)
            for code in ("PR00", "K007", "PPSV")
        },
        "service_metadata": {
            name: metadata(client, name) for name in (
                "API_BUSINESS_PARTNER", "API_PRODUCT_SRV", "API_SALES_ORDER_SRV",
                "API_SLSPRICINGPROCEDURE_SRV", "SD_PRICING_CONDITIONRECORD_SRV",
                "ZSD_PRICING_CONDITIONRECORD_SRV_0001",
            )
        },
        "sales_order_references": documents,
    }
    if "--compact" in sys.argv:
        output = compact_output(output)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
