"""Resume a configured Phase 5 customer through proven OData entity sets.

The script is deliberately narrow: it creates missing customer company and
sales-area extensions, performs fresh-session readbacks, and persists the
logical-to-SAP identity mapping only after both extensions exist.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests
import urllib3
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED = ROOT / "config" / "s4615_training_seed.yaml"
DEFAULT_MAPPINGS = ROOT / "data" / "provisioning" / "phase5_identity_mappings.json"


def load_operation(seed_path: Path, operation_id: str) -> dict[str, Any]:
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    return seed["operations"][operation_id]


def field_value(operation: dict[str, Any], name: str) -> Any:
    return operation["fields"][name]["value"]


def customer_payloads(operation: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    target = operation["target"]
    sales_org, channel, division = target["sales_area"].split("/")
    company = {
        "Customer": target["sap_partner_id"],
        "CompanyCode": target["company_code"],
        "ReconciliationAccount": field_value(operation, "reconciliation_account"),
        "PaymentTerms": field_value(operation, "payment_terms"),
        "CustomerAccountGroup": "CUST",
    }
    sales_area = {
        "Customer": target["sap_partner_id"],
        "SalesOrganization": sales_org,
        "DistributionChannel": channel,
        "Division": division,
        "Currency": field_value(operation, "currency"),
        "CustomerAccountAssignmentGroup": field_value(operation, "account_assignment_group"),
        "CustomerPricingProcedure": field_value(operation, "customer_pricing_procedure"),
        "CustomerAccountGroup": "CUST",
        "IncotermsClassification": field_value(operation, "incoterms"),
        "IncotermsLocation1": field_value(operation, "incoterms_location"),
        "ShippingCondition": field_value(operation, "shipping_conditions"),
        "CustomerPaymentTerms": field_value(operation, "payment_terms"),
    }
    return company, sales_area


def persist_mapping(path: Path, logical_id: str, sap_id: str, evidence: dict[str, Any]) -> None:
    document = {"version": 1, "mappings": {}}
    if path.exists():
        document = json.loads(path.read_text(encoding="utf-8"))
    mappings = document.setdefault("mappings", {})
    existing = mappings.get(logical_id)
    record = {
        "object_type": "BUSINESS_PARTNER",
        "logical_id": logical_id,
        "sap_id": sap_id,
        "status": "LIVE_VERIFIED",
        "evidence": evidence,
    }
    if existing and existing.get("sap_id") != sap_id:
        raise RuntimeError(f"mapping conflict for {logical_id}")
    mappings[logical_id] = record
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SapOData:
    def __init__(self) -> None:
        load_dotenv()
        self.base = os.environ["SAP_BASE_URL"].rstrip("/")
        self.client = os.environ["SAP_CLIENT"]
        self.auth = (os.environ["SAP_USERNAME"], os.environ["SAP_PASSWORD"])
        self.verify = os.getenv("SAP_VERIFY_SSL", os.getenv("SAP_VERIFY_TLS", "true")).lower() == "true"
        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.client != "600" or os.environ["SAP_USERNAME"].upper() != "ABDELJ":
            raise RuntimeError("Phase 5 customer execution requires client 600 / user ABDELJ")
        self.root = f"{self.base}/sap/opu/odata/sap/API_BUSINESS_PARTNER"
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = self.verify

    def get(self, path: str, select: str) -> requests.Response:
        return self.session.get(
            f"{self.root}/{path}", params={"sap-client": self.client, "$select": select},
            headers={"Accept": "application/json"}, timeout=30,
        )

    def post(self, entity_set: str, payload: dict[str, Any]) -> requests.Response:
        token_response = self.session.get(
            f"{self.root}/", params={"sap-client": self.client},
            headers={"Accept": "application/json", "X-CSRF-Token": "Fetch"}, timeout=30,
        )
        token = token_response.headers.get("X-CSRF-Token")
        if token_response.status_code != 200 or not token:
            raise RuntimeError(f"CSRF fetch failed: HTTP {token_response.status_code}")
        return self.session.post(
            f"{self.root}/{entity_set}", params={"sap-client": self.client},
            headers={"Accept": "application/json", "Content-Type": "application/json", "X-CSRF-Token": token},
            data=json.dumps(payload), timeout=30,
        )

    def fresh_get(self, path: str, select: str) -> requests.Response:
        with requests.Session() as session:
            session.auth = self.auth
            session.verify = self.verify
            return session.get(
                f"{self.root}/{path}", params={"sap-client": self.client, "$select": select},
                headers={"Accept": "application/json"}, timeout=30,
            )


def sap_error(response: requests.Response) -> str:
    try:
        return " ".join(response.json()["error"]["message"]["value"].split())
    except (ValueError, KeyError, TypeError):
        return " ".join(response.text.split())[:500]


def ensure_entity(api: SapOData, entity_set: str, key: str, select: str, payload: dict[str, Any]) -> str:
    lookup = api.get(key, select)
    if lookup.status_code == 200:
        return "EXISTS"
    if lookup.status_code != 404:
        raise RuntimeError(f"{entity_set} lookup HTTP {lookup.status_code}: {sap_error(lookup)}")
    created = api.post(entity_set, payload)
    if created.status_code not in (200, 201, 204):
        raise RuntimeError(f"{entity_set} create HTTP {created.status_code}: {sap_error(created)}")
    readback = api.fresh_get(key, select)
    if readback.status_code != 200:
        raise RuntimeError(f"{entity_set} readback HTTP {readback.status_code}: {sap_error(readback)}")
    return "CREATED_AND_VERIFIED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, default=DEFAULT_SEED)
    parser.add_argument("--operation", default="CUSTOMER_C615_D00")
    parser.add_argument("--mapping-store", type=Path, default=DEFAULT_MAPPINGS)
    args = parser.parse_args()

    operation = load_operation(args.seed, args.operation)
    company, sales_area = customer_payloads(operation)
    target = operation["target"]
    sap_id = target["sap_partner_id"]
    company_key = f"A_CustomerCompany(Customer='{sap_id}',CompanyCode='{target['company_code']}')"
    sales_org, channel, division = target["sales_area"].split("/")
    sales_key = (
        f"A_CustomerSalesArea(Customer='{sap_id}',SalesOrganization='{sales_org}',"
        f"DistributionChannel='{channel}',Division='{division}')"
    )

    api = SapOData()
    company_status = ensure_entity(
        api, "A_CustomerCompany", company_key,
        "Customer,CompanyCode,ReconciliationAccount,PaymentTerms,CustomerAccountGroup", company,
    )
    sales_status = ensure_entity(
        api, "A_CustomerSalesArea", sales_key,
        "Customer,SalesOrganization,DistributionChannel,Division,Currency,IncotermsClassification", sales_area,
    )
    persist_mapping(args.mapping_store, target["partner_id"], sap_id, {
        "service": "API_BUSINESS_PARTNER",
        "company_code": target["company_code"],
        "sales_area": target["sales_area"],
        "company_readback": "EXISTS",
        "sales_area_readback": "EXISTS",
    })
    print(json.dumps({"company": company_status, "sales_area": sales_status, "mapping": "LIVE_VERIFIED"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
