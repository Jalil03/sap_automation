"""Strict read-only readiness audit for S4600 exercise 9, group 00."""

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

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex9_group00_readiness_2026-10-22.json"
BP_SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER"


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, path: str, params: dict[str, str] | None = None) -> dict:
    if params:
        path += "?" + urlencode(params)
    response = client.request("GET", path, headers={"Accept": "application/json"})
    payload = response.json().get("d", {}) if response.status == 200 else {}
    rows = payload.get("results") if isinstance(payload, dict) else None
    return {
        "http_status": response.status,
        "rows": clean(rows) if isinstance(rows, list) else None,
        "row": clean(payload) if response.status == 200 and isinstance(payload, dict) and not isinstance(rows, list) else None,
        "error_excerpt": response.body.decode("utf-8", errors="replace")[:1000] if response.status not in (200, 404) else None,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    target = "T-CUS00"
    reference = "1000000113"
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "target": {
            "logical_id": target,
            "name": "Motos et autres",
            "address": {"street": "Rue principale", "house_number": "00", "postal_code": "20111", "city": "Hambourg", "country": "DE", "region": "HH", "language": "EN"},
            "adapted_company_code": "FR10",
            "adapted_sales_area": "FR10/10/1W",
        },
        "duplicate_checks": {
            "exact_bp": get(client, f"{BP_SERVICE}/A_BusinessPartner('{target}')", {"$select": "BusinessPartner"}),
            "exact_customer": get(client, f"{BP_SERVICE}/A_Customer('{target}')", {"$select": "Customer"}),
            "external_id": get(client, f"{BP_SERVICE}/A_BusinessPartner", {"$filter": f"BusinessPartnerIDByExtSystem eq '{target}'", "$select": "BusinessPartner,BusinessPartnerIDByExtSystem", "$top": "20"}),
            "search_term": get(client, f"{BP_SERVICE}/A_BusinessPartner", {"$filter": f"SearchTerm1 eq '{target}'", "$select": "BusinessPartner,SearchTerm1", "$top": "20"}),
            "exact_name": get(client, f"{BP_SERVICE}/A_BusinessPartner", {"$filter": "OrganizationBPName1 eq 'Motos et autres'", "$select": "BusinessPartner,OrganizationBPName1", "$top": "20"}),
        },
        "bpab_samples": get(client, f"{BP_SERVICE}/A_BusinessPartner", {"$filter": "BusinessPartnerGrouping eq 'BPAB'", "$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerCategory,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1", "$top": "20"}),
        "german_fr10_reference": {
            "root": get(client, f"{BP_SERVICE}/A_BusinessPartner('{reference}')", {"$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerCategory,OrganizationBPName1,SearchTerm1"}),
            "addresses": get(client, f"{BP_SERVICE}/A_BusinessPartnerAddress", {"$filter": f"BusinessPartner eq '{reference}'", "$select": "BusinessPartner,AddressID,StreetName,HouseNumber,PostalCode,CityName,Country,Region,Language", "$top": "20"}),
            "roles": get(client, f"{BP_SERVICE}/A_BusinessPartnerRole", {"$filter": f"BusinessPartner eq '{reference}'", "$select": "BusinessPartner,BusinessPartnerRole", "$top": "20"}),
            "company": get(client, f"{BP_SERVICE}/A_CustomerCompany(Customer='{reference}',CompanyCode='FR10')", {"$select": "Customer,CompanyCode,PaymentTerms,ReconciliationAccount,CustomerAccountGroup"}),
            "sales_area": get(client, f"{BP_SERVICE}/A_CustomerSalesArea(Customer='{reference}',SalesOrganization='FR10',DistributionChannel='10',Division='1W')", {"$select": "Customer,SalesOrganization,DistributionChannel,Division,Currency,ShippingCondition,SupplyingPlant,IncotermsClassification,IncotermsLocation1,CustomerPaymentTerms,CustomerAccountAssignmentGroup,CustomerPricingProcedure,CustomerAccountGroup"}),
            "partner_functions": get(client, f"{BP_SERVICE}/A_CustSalesPartnerFunc", {"$filter": f"Customer eq '{reference}' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'", "$select": "Customer,PartnerFunction,BPCustomerNumber,DefaultPartner", "$top": "20"}),
            "sales_taxes": get(client, f"{BP_SERVICE}/A_CustomerSalesAreaTax", {"$filter": f"Customer eq '{reference}' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'", "$select": "Customer,DepartureCountry,CustomerTaxCategory,CustomerTaxClassification", "$top": "20"}),
        },
        "book_code_usage_in_fr10": {
            "company_payment_terms_zb00": get(client, f"{BP_SERVICE}/A_CustomerCompany", {"$filter": "CompanyCode eq 'FR10' and PaymentTerms eq 'ZB00'", "$select": "Customer,CompanyCode,PaymentTerms,ReconciliationAccount", "$top": "20"}),
            "sales_payment_terms_zb00": get(client, f"{BP_SERVICE}/A_CustomerSalesArea", {"$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W' and CustomerPaymentTerms eq 'ZB00'", "$select": "Customer,CustomerPaymentTerms", "$top": "20"}),
            "shipping_condition_50": get(client, f"{BP_SERVICE}/A_CustomerSalesArea", {"$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W' and ShippingCondition eq '50'", "$select": "Customer,ShippingCondition", "$top": "20"}),
            "pricing_procedure_s": get(client, f"{BP_SERVICE}/A_CustomerSalesArea", {"$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W' and CustomerPricingProcedure eq 'S'", "$select": "Customer,CustomerPricingProcedure", "$top": "20"}),
            "tax_ttx1": get(client, f"{BP_SERVICE}/A_CustomerSalesAreaTax", {"$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W' and CustomerTaxCategory eq 'TTX1'", "$select": "Customer,DepartureCountry,CustomerTaxCategory,CustomerTaxClassification", "$top": "20"}),
        },
        "book_reconciliation_account_in_fr10_chart": get(
            client,
            "sap/opu/odata/sap/API_JOURNALENTRYITEMBASIC_SRV/A_GLAccountInChartOfAccounts",
            {"$filter": "ChartOfAccounts eq 'PCOH' and (GLAccount eq '12100000' or GLAccount eq '0012100000')", "$select": "ChartOfAccounts,GLAccount,GLAccountGroup,GLAccountType", "$top": "20"},
        ),
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "duplicate_checks": evidence["duplicate_checks"],
        "bpab_samples": evidence["bpab_samples"],
        "german_fr10_reference": evidence["german_fr10_reference"],
        "book_code_usage_in_fr10": evidence["book_code_usage_in_fr10"],
        "book_reconciliation_account_in_fr10_chart": evidence["book_reconciliation_account_in_fr10_chart"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
