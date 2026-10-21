"""Narrow Phase 5 OData backend for the live-proven customer and product routes.

The customer route extends an *existing* Business Partner. Product root create
is deliberately blocked: the installed API_PRODUCT_SRV rejected A_Product POST.
No constructor, import, or dry-run performs an SAP request.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from src.provisioning.phase5 import Phase5ProvisioningEngine, S4615_SEED_PATH
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError, TransportError
from src.sap_runtime.transport import HttpResponse, SapTransport, UrllibSapTransport


ROOT = Path(__file__).resolve().parents[2]
MAPPINGS_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
REGISTRY_PATH = ROOT / "mappings/sap/interface_registry.yaml"
CUSTOMER = "CUSTOMER_C615_D00"
PRODUCT = "PRODUCT_P615_400"
API_OPERATIONS = frozenset({CUSTOMER, PRODUCT})
CUSTOMER_SELECT = "Customer,CompanyCode,ReconciliationAccount,PaymentTerms,CustomerAccountGroup"
SALES_SELECT = "Customer,SalesOrganization,DistributionChannel,Division,Currency,IncotermsClassification"
PRODUCT_SELECT = "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup,ProductGroup"


def load_operation(seed_path: Path, operation_id: str) -> dict[str, Any]:
    seed = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    if seed.get("canonical_immutable") is not True or operation_id not in API_OPERATIONS:
        raise ValueError("Unsupported or mutable Phase 5 seed operation")
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
    sales = {
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
    return company, sales


def root_payload(operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "Product": operation["target"]["material_id"],
        "ProductType": field_value(operation, "material_type"),
        "IndustrySector": field_value(operation, "industry_sector"),
        "BaseUnit": field_value(operation, "base_unit"),
        "Division": field_value(operation, "sales_division"),
        "ItemCategoryGroup": field_value(operation, "item_category_group"),
        "ProductGroup": field_value(operation, "product_group"),
    }


def persist_mapping(
    path: Path, logical_id: str, sap_id: str, evidence: dict[str, Any],
    *, object_type: str = "BUSINESS_PARTNER",
) -> None:
    document = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"version": 1, "mappings": {}}
    mappings = document.setdefault("mappings", {})
    existing = mappings.get(logical_id)
    if existing and existing.get("sap_id") != sap_id:
        raise RuntimeError(f"mapping conflict for {logical_id}")
    if existing and existing.get("status") == "LIVE_VERIFIED":
        return  # Preserve richer pre-existing verification evidence.
    mappings[logical_id] = {
        "object_type": object_type, "logical_id": logical_id,
        "sap_id": sap_id, "status": "LIVE_VERIFIED", "evidence": evidence,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _registry_service(path: Path, object_type: str, expected: str) -> str:
    # The registry is JSON-compatible YAML. Never substitute a technical Z name
    # for the consumer-facing OData service.
    registry = json.loads(path.read_text(encoding="utf-8"))
    entries = registry["object_types"]
    candidates = entries[object_type]["candidates"]
    if not any(c.get("classification") == "ODATA" and c.get("external_name") == expected for c in candidates):
        raise ValueError(f"{object_type} OData service is not evidenced in interface registry")
    return expected


def _odata_row(response: HttpResponse, entity: str) -> dict[str, Any] | None:
    if response.status == 404:
        return None
    if response.status != 200:
        raise RuntimeError(f"{entity} GET failed: HTTP {response.status}")
    data = response.json().get("d")
    if not isinstance(data, dict):
        raise RuntimeError(f"{entity} GET response shape is unverified")
    return {key: value for key, value in data.items() if key != "__metadata"}


class SapApiBackend:
    """ProvisioningBackend adapter; only the customer extension route can POST."""

    writable = True

    def __init__(
        self, *, config: SapRuntimeConfig | None = None,
        transport: SapTransport | None = None,
        transport_factory: Any = UrllibSapTransport,
        seed_path: Path = S4615_SEED_PATH,
        mapping_path: Path = MAPPINGS_PATH,
        registry_path: Path = REGISTRY_PATH,
    ) -> None:
        self.config = config
        self.transport = transport
        self.transport_factory = transport_factory
        self.seed_path = Path(seed_path)
        self.mapping_path = Path(mapping_path)
        self.registry_path = Path(registry_path)

    def _client(self, *, fresh: bool = False) -> SapTransport:
        if self.config is None:
            from dotenv import load_dotenv
            load_dotenv()
            self.config = SapRuntimeConfig.from_env()
        if self.config.client != "600" or self.config.username.upper() != "ABDELJ":
            raise ValueError("Phase 5 API backend requires client 600 / user ABDELJ")
        if fresh:
            return self.transport_factory(self.config)
        if self.transport is None:
            self.transport = self.transport_factory(self.config)
        return self.transport

    def _contract(self, operation: str, target: dict[str, Any]) -> dict[str, Any]:
        if operation not in API_OPERATIONS:
            raise ValueError(f"No API route for {operation}")
        expected = Phase5ProvisioningEngine._targets()[operation]
        if target != expected:
            raise ValueError(f"Phase 5 API target mismatch for {operation}")
        contract = load_operation(self.seed_path, operation)
        for key, value in target.items():
            if contract["target"].get(key) != value:
                raise ValueError(f"Phase 5 seed target mismatch: {key}")
        _registry_service(self.registry_path, "BUSINESS_PARTNER" if operation == CUSTOMER else "MATERIAL",
                          "API_BUSINESS_PARTNER" if operation == CUSTOMER else "API_PRODUCT_SRV")
        return contract

    def _mapped_id(self, logical_id: str, seeded_id: str | None = None) -> str:
        if not self.mapping_path.exists():
            return seeded_id or logical_id
        mappings = json.loads(self.mapping_path.read_text(encoding="utf-8")).get("mappings", {})
        record = mappings.get(logical_id)
        if record:
            if record.get("status") != "LIVE_VERIFIED" or not record.get("sap_id"):
                raise RuntimeError("Unverified logical-to-SAP mapping")
            if seeded_id and record["sap_id"] != seeded_id:
                raise RuntimeError("Logical-to-SAP mapping conflicts with seed")
            return str(record["sap_id"])
        return seeded_id or logical_id

    def _get(self, service: str, key: str, select: str, *, fresh: bool = False) -> dict[str, Any] | None:
        query = urlencode({"sap-client": "600", "$select": select})
        path = f"sap/opu/odata/sap/{service}/{key}?{query}"
        response = self._client(fresh=fresh).request("GET", path)
        return _odata_row(response, key)

    @staticmethod
    def _customer_keys(sap_id: str, company: str, area: str) -> tuple[str, str]:
        sales_org, channel, division = area.split("/")
        return (
            f"A_CustomerCompany(Customer='{sap_id}',CompanyCode='{company}')",
            f"A_CustomerSalesArea(Customer='{sap_id}',SalesOrganization='{sales_org}',"
            f"DistributionChannel='{channel}',Division='{division}')",
        )

    def _customer_rows(self, contract: dict[str, Any], *, fresh: bool = False) -> tuple[dict | None, dict | None, dict | None]:
        target = contract["target"]
        sap_id = self._mapped_id(target["partner_id"], target["sap_partner_id"])
        root = self._get("API_BUSINESS_PARTNER", f"A_Customer('{sap_id}')", "Customer", fresh=fresh)
        if root is None:
            return None, None, None
        company_key, sales_key = self._customer_keys(sap_id, target["company_code"], target["sales_area"])
        company = self._get("API_BUSINESS_PARTNER", company_key, CUSTOMER_SELECT, fresh=fresh)
        sales = self._get("API_BUSINESS_PARTNER", sales_key, SALES_SELECT, fresh=fresh)
        return root, company, sales

    def lookup(self, operation: str, target: dict[str, Any]) -> str:
        contract = self._contract(operation, target)
        if operation == CUSTOMER:
            root, company, sales = self._customer_rows(contract)
            if root is None:
                return "UNKNOWN"  # BP creation is not part of this proven route.
            sap_id = contract["target"]["sap_partner_id"]
            if root.get("Customer") != sap_id:
                return "UNKNOWN"
            expected_company, expected_sales = customer_payloads(contract)
            if company is not None and any(company.get(key) != expected_company[key] for key in
                                           ("Customer", "CompanyCode", "ReconciliationAccount")):
                return "UNKNOWN"
            if sales is not None and any(sales.get(key) != expected_sales[key] for key in
                                         ("Customer", "SalesOrganization", "DistributionChannel",
                                          "Division", "Currency", "IncotermsClassification")):
                return "UNKNOWN"
            if company is None or sales is None:
                return "MISSING"
            return "EXISTS"
        product = self._mapped_id(target["material_id"])
        root = self._get("API_PRODUCT_SRV", f"A_Product('{product}')", PRODUCT_SELECT)
        if root is None:
            return "MISSING"
        expected = root_payload(contract)
        matched = root.get("Product") == product and all(
            root.get(field) == expected[field] for field in ("ProductType", "IndustrySector", "BaseUnit", "Division")
        )
        if not matched:
            return "UNKNOWN"
        return "EXISTS"

    def _post(self, service: str, entity: str, payload: dict[str, Any]) -> None:
        client = self._client()
        base = f"sap/opu/odata/sap/{service}/"
        token_response = client.request("GET", base + "?sap-client=600", headers={"X-CSRF-Token": "Fetch"})
        token = token_response.header("X-CSRF-Token")
        if token_response.status != 200 or not token:
            raise RuntimeError(f"CSRF preflight failed: HTTP {token_response.status}")
        try:
            response = client.request(
                "POST", base + entity + "?sap-client=600",
                headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                body=json.dumps(payload).encode("utf-8"),
            )
        except (AmbiguousTransportError, TransportError) as error:
            raise RuntimeError("Ambiguous OData POST outcome; do not retry automatically") from error
        if response.status not in {200, 201, 204}:
            raise RuntimeError(f"{entity} POST failed: HTTP {response.status}; do not retry automatically")

    def provision(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
        contract = self._contract(operation, target)
        if operation == PRODUCT:
            return {"provisioning_blocked": True, "reason": "A_Product POST is not creatable on the installed API_PRODUCT_SRV"}
        if self.lookup(operation, target) != "MISSING":
            return {"provisioning_blocked": True, "reason": "Customer extensions require a fresh MISSING lookup and existing A_Customer root"}
        company_payload, sales_payload = customer_payloads(contract)
        for field, expected in {
            "reconciliation_account": company_payload["ReconciliationAccount"],
            "payment_terms": company_payload["PaymentTerms"],
            "currency": sales_payload["Currency"],
            "account_assignment_group": sales_payload["CustomerAccountAssignmentGroup"],
            "customer_pricing_procedure": sales_payload["CustomerPricingProcedure"],
            "incoterms": sales_payload["IncotermsClassification"],
            "incoterms_location": sales_payload["IncotermsLocation1"],
            "shipping_conditions": sales_payload["ShippingCondition"],
        }.items():
            if values.get(field) != expected:
                raise ValueError(f"Customer decision mismatch: {field}")
        sap_id = contract["target"]["sap_partner_id"]
        company_key, sales_key = self._customer_keys(sap_id, target["company_code"], target["sales_area"])
        # Each entity is independently looked up immediately before its single POST.
        for entity, key, select, payload in (
            ("A_CustomerCompany", company_key, CUSTOMER_SELECT, company_payload),
            ("A_CustomerSalesArea", sales_key, SALES_SELECT, sales_payload),
        ):
            if self._get("API_BUSINESS_PARTNER", key, select) is not None:
                continue
            self._post("API_BUSINESS_PARTNER", entity, payload)
            if self._get("API_BUSINESS_PARTNER", key, select, fresh=True) is None:
                raise RuntimeError(f"{entity} fresh-session readback failed; do not retry")
        return {"accepted": True, "service": "API_BUSINESS_PARTNER"}

    def readback(self, operation: str, target: dict[str, Any]) -> dict[str, Any] | None:
        contract = self._contract(operation, target)
        if operation == CUSTOMER:
            root, company, sales = self._customer_rows(contract, fresh=True)
            sap_id = contract["target"]["sap_partner_id"]
            if not (root and company and sales):
                return None
            if (root.get("Customer"), company.get("Customer"), company.get("CompanyCode"),
                sales.get("Customer"), sales.get("SalesOrganization"),
                sales.get("DistributionChannel"), sales.get("Division")) != (
                sap_id, sap_id, target["company_code"], sap_id, *target["sales_area"].split("/")):
                return None
            expected_company, expected_sales = customer_payloads(contract)
            if (company.get("ReconciliationAccount") != expected_company["ReconciliationAccount"]
                or sales.get("Currency") != expected_sales["Currency"]
                or sales.get("IncotermsClassification") != expected_sales["IncotermsClassification"]):
                return None
            persist_mapping(self.mapping_path, target["partner_id"], sap_id, {
                "service": "API_BUSINESS_PARTNER", "company_code": target["company_code"],
                "sales_area": target["sales_area"], "company_readback": "EXISTS", "sales_area_readback": "EXISTS",
            })
            return {"partner_id": target["partner_id"], "sap_partner_id": sap_id,
                    "company_code": target["company_code"], "sales_area": target["sales_area"]}
        product = self._mapped_id(target["material_id"])
        row = self._get("API_PRODUCT_SRV", f"A_Product('{product}')", PRODUCT_SELECT, fresh=True)
        if not row or row.get("Product") != product:
            return None
        expected = root_payload(contract)
        if any(row.get(field) != expected[field] for field in ("ProductType", "IndustrySector", "BaseUnit", "Division")):
            return None
        persist_mapping(self.mapping_path, target["material_id"], product,
                        {"service": "API_PRODUCT_SRV", "root_readback": "EXISTS"}, object_type="MATERIAL")
        return {"material_id": target["material_id"], "sap_product_id": product, "root": row}


def create_backend() -> SapApiBackend:
    return SapApiBackend()
