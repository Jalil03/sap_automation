"""Read-only readiness inspection for T-S50A01 customer extensions."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
BP = "1000000116"
REFERENCE_BP = "1000000115"
EDM = "http://schemas.microsoft.com/ado/2008/09/edm"
CANDIDATE_ENTITIES = (
    "A_BusinessPartnerAddress",
    "A_BuPaAddressUsage",
    "A_BusinessPartnerRole",
    "A_Customer",
    "A_CustomerCompany",
    "A_CustomerSalesArea",
    "A_CustSalesPartnerFunc",
    "A_CustomerSalesAreaTax",
)


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Read inspection is restricted to A4H/600/ABDELJ")
    client = UrllibSapTransport(config)
    metadata_response = client.request(
        "GET", SERVICE + "$metadata", headers={"Accept": "application/xml"}
    )
    if metadata_response.status != 200:
        raise RuntimeError(f"Metadata unavailable: HTTP {metadata_response.status}")
    root = ET.fromstring(metadata_response.body)
    installed = {
        node.get("Name")
        for node in root.iter()
        if node.tag == f"{{{EDM}}}EntitySet" and node.get("Name")
    }
    result: dict[str, object] = {
        "environment": {"system": "A4H", "client": config.client, "user": config.username},
        "mode": "READ_ONLY",
        "logical_id": "T-S50A01",
        "sap_id": BP,
        "metadata_http_status": metadata_response.status,
        "entities": {},
    }

    paths = {
        "root": f"A_BusinessPartner('{BP}')",
        "customer": f"A_Customer('{BP}')",
        "company_1010": f"A_CustomerCompany(Customer='{BP}',CompanyCode='1010')",
        "sales_area_1010_10_00": (
            f"A_CustomerSalesArea(Customer='{BP}',SalesOrganization='1010',"
            "DistributionChannel='10',Division='00')"
        ),
    }
    for name, path in paths.items():
        response = client.request("GET", SERVICE + path)
        raw = response.json().get("d", {}) if response.status == 200 else {}
        row = {
            key: raw.get(key)
            for key in (
                "BusinessPartner", "Customer", "BusinessPartnerCategory",
                "BusinessPartnerGrouping", "OrganizationBPName1", "SearchTerm1",
                "CompanyCode", "SalesOrganization", "DistributionChannel", "Division",
            )
            if key in raw
        }
        result["entities"][name] = {"http_status": response.status, "row": row}

    filters = {
        "addresses": ("A_BusinessPartnerAddress", f"BusinessPartner eq '{BP}'"),
        "address_usages": ("A_BuPaAddressUsage", f"BusinessPartner eq '{BP}'"),
        "roles": ("A_BusinessPartnerRole", f"BusinessPartner eq '{BP}'"),
        "partner_functions": ("A_CustSalesPartnerFunc", f"Customer eq '{BP}'"),
        "tax": ("A_CustomerSalesAreaTax", f"Customer eq '{BP}'"),
    }
    for name, (entity, filter_text) in filters.items():
        if entity not in installed:
            result["entities"][name] = {"state": "ENTITY_NOT_INSTALLED", "entity": entity}
            continue
        query = urlencode({"$filter": filter_text, "$format": "json"})
        response = client.request("GET", f"{SERVICE}{entity}?{query}")
        rows = response.json().get("d", {}).get("results", []) if response.status == 200 else []
        result["entities"][name] = {
            "entity": entity,
            "http_status": response.status,
            "count": len(rows) if isinstance(rows, list) else None,
            "rows": rows if isinstance(rows, list) else [],
        }

    reference: dict[str, object] = {}
    reference_paths = {
        "company_1010": f"A_CustomerCompany(Customer='{REFERENCE_BP}',CompanyCode='1010')",
        "sales_area_1010_10_00": (
            f"A_CustomerSalesArea(Customer='{REFERENCE_BP}',SalesOrganization='1010',"
            "DistributionChannel='10',Division='00')"
        ),
    }
    for name, path in reference_paths.items():
        response = client.request("GET", SERVICE + path)
        raw = response.json().get("d", {}) if response.status == 200 else {}
        keep = {
            "Customer", "CompanyCode", "ReconciliationAccount", "PaymentTerms",
            "CustomerAccountGroup", "SalesOrganization", "DistributionChannel", "Division",
            "Currency", "ShippingCondition", "SupplyingPlant", "CustomerPricingProcedure",
            "CustomerAccountAssignmentGroup", "IncotermsClassification", "IncotermsLocation1",
            "CustomerPaymentTerms",
        }
        reference[name] = {
            "http_status": response.status,
            "row": {key: value for key, value in raw.items() if key in keep},
        }
    for name, entity in {
        "roles": "A_BusinessPartnerRole",
        "addresses": "A_BusinessPartnerAddress",
        "partner_functions": "A_CustSalesPartnerFunc",
        "tax": "A_CustomerSalesAreaTax",
    }.items():
        field = "BusinessPartner" if entity.startswith("A_BusinessPartner") else "Customer"
        query = urlencode({"$filter": f"{field} eq '{REFERENCE_BP}'", "$format": "json"})
        response = client.request("GET", f"{SERVICE}{entity}?{query}")
        rows = response.json().get("d", {}).get("results", []) if response.status == 200 else []
        reference[name] = {"http_status": response.status, "rows": rows}
    result["verified_environment_reference_1000000115"] = reference

    creatable = tuple(entity for entity in CANDIDATE_ENTITIES if entity in installed)
    raw_contracts = inspect_creation_metadata(metadata_response.body, entities=creatable)
    result["contracts"] = {
        entity: {
            "metadata_allows_create": contract["metadata_allows_create"],
            "keys": contract["keys"],
            "mandatory_fields": [
                name for name, field in contract["fields"].items() if not field["nullable"]
            ],
            "selected_creatable_fields": {
                name: field["creatable"]
                for name, field in contract["fields"].items()
                if name in {
                    "StreetName", "HouseNumber", "PostalCode", "CityName", "Country",
                    "Region", "Language", "BusinessPartnerRole", "ReconciliationAccount",
                    "PaymentTerms", "Currency", "ShippingCondition", "SupplyingPlant",
                    "CustomerPricingProcedure", "CustomerAccountAssignmentGroup",
                    "IncotermsClassification", "IncotermsLocation1", "CustomerPaymentTerms",
                    "BPCustomerNumber", "DefaultPartner", "CustomerTaxClassification",
                }
            },
        }
        for entity, contract in raw_contracts.items()
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
