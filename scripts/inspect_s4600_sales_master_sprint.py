"""Targeted read-only state and metadata check for the S4600 sales sprint."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


BP = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
PRODUCT = "sap/opu/odata/sap/API_PRODUCT_SRV/"
EXPECTED = {
    "T-S50A01": "1000000116",
    "T-D101": "90000132",
    "T-MS101": "60000445",
    "T-MS201": "60000446",
}


def get(client: UrllibSapTransport, service: str, resource: str, select: str = "") -> dict[str, object]:
    suffix = "?" + urlencode({"$select": select}) if select else ""
    response = client.request("GET", service + resource + suffix)
    value: dict[str, object] = {"http": response.status}
    if response.status == 200:
        value["data"] = response.json().get("d", {})
    return value


def compact_metadata(client: UrllibSapTransport, service: str, names: tuple[str, ...]) -> dict[str, object]:
    response = client.request("GET", service + "$metadata", headers={"Accept": "application/xml"})
    if response.status != 200:
        raise RuntimeError(f"metadata HTTP {response.status}")
    parsed = inspect_creation_metadata(response.body, entities=names)
    result: dict[str, object] = {}
    for name, entity in parsed.items():
        result[name] = {
            "metadata_allows_create": entity["metadata_allows_create"],
            "keys": entity["keys"],
            "mandatory": sorted(field for field, spec in entity["fields"].items() if not spec["nullable"]),
            "creatable_fields": sorted(field for field, spec in entity["fields"].items() if spec["creatable"]),
        }
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    mappings = json.loads((ROOT / "data/provisioning/phase5_identity_mappings.json").read_text(encoding="utf-8"))["mappings"]
    mapping_state = {}
    for logical_id, sap_id in EXPECTED.items():
        row = mappings.get(logical_id, {})
        mapping_state[logical_id] = {
            "sap_id": row.get("sap_id"), "status": row.get("status"),
            "matches_expected": row.get("sap_id") == sap_id and row.get("status") == "LIVE_VERIFIED",
        }

    customer = "1000000116"
    customer_state = {
        "root": get(client, BP, f"A_BusinessPartner('{customer}')", "BusinessPartner,BusinessPartnerCategory,OrganizationBPName1,SearchTerm1"),
        "address": get(client, BP, "A_BusinessPartnerAddress?" + urlencode({"$filter": f"BusinessPartner eq '{customer}'", "$select": "BusinessPartner,AddressID,StreetName,HouseNumber,PostalCode,CityName,Country,Region,Language", "$top": "20"})),
        "role_FLCU00": get(client, BP, f"A_BusinessPartnerRole(BusinessPartner='{customer}',BusinessPartnerRole='FLCU00')"),
        "role_FLCU01": get(client, BP, f"A_BusinessPartnerRole(BusinessPartner='{customer}',BusinessPartnerRole='FLCU01')"),
        "customer_root": get(client, BP, f"A_Customer('{customer}')", "Customer,CustomerAccountGroup"),
        "sales_area": get(client, BP, f"A_CustomerSalesArea(Customer='{customer}',SalesOrganization='1010',DistributionChannel='10',Division='00')"),
        "partner_functions": get(client, BP, "A_CustSalesPartnerFunc?" + urlencode({"$filter": f"Customer eq '{customer}' and SalesOrganization eq '1010' and DistributionChannel eq '10' and Division eq '00'", "$top": "20"})),
        "tax": get(client, BP, "A_CustomerSalesAreaTax?" + urlencode({"$filter": f"Customer eq '{customer}'", "$top": "20"})),
    }

    products = {}
    for logical_id in ("T-MS101", "T-MS201", "T-D101"):
        sap_id = EXPECTED[logical_id]
        products[logical_id] = {
            "root": get(client, PRODUCT, f"A_Product('{sap_id}')", "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"),
            "sales_delivery": get(client, PRODUCT, f"A_ProductSalesDelivery(Product='{sap_id}',ProductSalesOrg='1010',ProductDistributionChnl='10')"),
            "sales_tax": get(client, PRODUCT, "A_ProductSalesTax?" + urlencode({"$filter": f"Product eq '{sap_id}'", "$top": "20"})),
        }

    output = {
        "mode": "READ_ONLY",
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mappings": mapping_state,
        "customer": customer_state,
        "products": products,
        "metadata": {
            "business_partner": compact_metadata(client, BP, ("A_BusinessPartnerRole", "A_CustomerSalesArea", "A_CustSalesPartnerFunc", "A_CustomerSalesAreaTax")),
            "product": compact_metadata(client, PRODUCT, ("A_ProductSalesDelivery", "A_ProductSalesTax")),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
