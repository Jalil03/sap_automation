"""Create one approved S4600 A_ProductSalesDelivery extension."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.provisioning.execution_policy import ExecutionCheckpoint, target_fingerprint
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.errors import AmbiguousTransportError, TransportError
from src.sap_runtime.transport import UrllibSapTransport


APPROVAL_PATH = ROOT / "data/provisioning/s4600/product_sales_write_approval.group01.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4600/product_sales_execution_checkpoint.group01.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
SERVICE = "sap/opu/odata/sap/API_PRODUCT_SRV/"
ENTITY = "A_ProductSalesDelivery"
ROOT_SELECT = "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"
SALES_SELECT = "Product,ProductSalesOrg,ProductDistributionChnl,ItemCategoryGroup,SupplyingPlant,AccountDetnProductGroup"
EXPECTED_ROOTS = {
    "T-D101": {"sap_id": "90000132", "ProductType": "DIEN", "IndustrySector": "W", "BaseUnit": "H", "Division": "00"},
    "T-MS101": {"sap_id": "60000445", "ProductType": "HAWA", "IndustrySector": "W", "BaseUnit": "PC", "Division": "00"},
    "T-MS201": {"sap_id": "60000446", "ProductType": "HAWA", "IndustrySector": "W", "BaseUnit": "PC", "Division": "00"},
}


def operation_for(logical_id: str) -> str:
    suffix = logical_id.replace("-", "_")
    return f"S4600_PRODUCT_{suffix}_SALES_1010_10"


def load_approved(logical_id: str) -> tuple[str, dict[str, str], dict[str, str], str]:
    document = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    operation = operation_for(logical_id)
    entry = document.get("operations", {}).get(operation, {})
    target = entry.get("target", {})
    payload = entry.get("payload", {})
    fingerprint = entry.get("target_fingerprint", "")
    if (document.get("workflow_id") != "S4600_GROUP01_PRODUCT_SALES"
            or document.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or document.get("operation_scope") != "TRAINING_MASTER_DATA_PRODUCT_SALES"
            or document.get("approval_status") != "APPROVED"
            or document.get("allow_write") is not True
            or not document.get("approved_by")
            or not document.get("authorization_evidence")
            or entry.get("allow_write") is not True
            or entry.get("limit") != "ONE_A_PRODUCT_SALES_DELIVERY_POST_ONLY"
            or target != {"logical_product_id": logical_id,
                          "sap_id": EXPECTED_ROOTS[logical_id]["sap_id"], "sales_area": "1010/10"}
            or set(payload) != {"Product", "ProductSalesOrg", "ProductDistributionChnl", "ItemCategoryGroup"}
            or payload.get("Product") != target.get("sap_id")
            or payload.get("ProductSalesOrg") != "1010"
            or payload.get("ProductDistributionChnl") != "10"
            or payload.get("ItemCategoryGroup") not in ({"LEIS"} if logical_id == "T-D101" else {"NORM"})
            or fingerprint != target_fingerprint(operation, target, payload)):
        raise RuntimeError("Exact PRODUCT_SALES approval, payload or fingerprint mismatch")
    return operation, target, payload, fingerprint


def exact_key(sap_id: str) -> str:
    return f"{ENTITY}(Product='{sap_id}',ProductSalesOrg='1010',ProductDistributionChnl='10')"


def get_row(client: UrllibSapTransport, resource: str, select: str) -> dict[str, Any] | None:
    response = client.request("GET", SERVICE + resource + "?" + urlencode({"$select": select}))
    if response.status == 404:
        return None
    if response.status != 200 or not isinstance(response.json().get("d"), dict):
        raise RuntimeError(f"{resource} read failed: HTTP {response.status}")
    return {key: value for key, value in response.json()["d"].items() if key != "__metadata"}


def tax_rows(client: UrllibSapTransport, sap_id: str) -> list[dict[str, Any]]:
    response = client.request("GET", SERVICE + "A_ProductSalesTax?" + urlencode({
        "$filter": f"Product eq '{sap_id}'", "$select": "Product,Country,TaxCategory,TaxClassification", "$top": "100",
    }))
    if response.status != 200:
        raise RuntimeError(f"Product tax read failed: HTTP {response.status}")
    rows = response.json().get("d", {}).get("results")
    if not isinstance(rows, list):
        raise RuntimeError("Product tax response shape unknown")
    return [{key: value for key, value in row.items() if key != "__metadata"} for row in rows]


def matches(row: dict[str, Any], payload: dict[str, str]) -> bool:
    return all(row.get(field) == value for field, value in payload.items())


def validate_root_and_mapping(client: UrllibSapTransport, logical_id: str) -> None:
    expected = EXPECTED_ROOTS[logical_id]
    mappings = json.loads(MAPPING_PATH.read_text(encoding="utf-8")).get("mappings", {})
    mapping = mappings.get(logical_id, {})
    if mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != expected["sap_id"]:
        raise RuntimeError("LIVE_VERIFIED identity mapping mismatch")
    root = get_row(client, f"A_Product('{expected['sap_id']}')", ROOT_SELECT)
    if root is None or any(root.get(field) != value for field, value in expected.items() if field != "sap_id"):
        raise RuntimeError("Product root independent validation mismatch")


def validate_metadata(client: UrllibSapTransport, payload: dict[str, str]) -> None:
    response = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if response.status != 200:
        raise RuntimeError(f"Product metadata HTTP {response.status}")
    entity = inspect_creation_metadata(response.body, entities=(ENTITY,))[ENTITY]
    mandatory = {name for name, spec in entity["fields"].items() if not spec["nullable"]}
    if (entity["metadata_allows_create"] is not True
            or entity["keys"] != ["Product", "ProductSalesOrg", "ProductDistributionChnl"]
            or mandatory != {"Product", "ProductSalesOrg", "ProductDistributionChnl"}):
        raise RuntimeError("Installed A_ProductSalesDelivery create contract changed")
    for field, value in payload.items():
        spec = entity["fields"].get(field)
        if not spec or spec["creatable"] is not True or spec["edm_type"] != "Edm.String":
            raise RuntimeError(f"Unproven sales payload field: {field}")
        if spec["max_length"] and spec["max_length"].isdigit() and len(value) > int(spec["max_length"]):
            raise RuntimeError(f"Sales payload exceeds field length: {field}")


def persist_mapping(logical_id: str, sap_id: str, payload: dict[str, str], fingerprint: str) -> None:
    document = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    entry = document.get("mappings", {}).get(logical_id, {})
    if entry.get("status") != "LIVE_VERIFIED" or entry.get("sap_id") != sap_id:
        raise RuntimeError("Mapping changed before sales evidence persistence")
    entry.setdefault("sales_extensions", {})["1010/10"] = {
        "status": "LIVE_VERIFIED", "entity": ENTITY,
        "payload": payload, "target_fingerprint": fingerprint,
        "tax_modified": False,
    }
    temporary = MAPPING_PATH.with_suffix(MAPPING_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, MAPPING_PATH)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logical_id", choices=tuple(EXPECTED_ROOTS))
    args = parser.parse_args()
    operation, target, payload, fingerprint = load_approved(args.logical_id)
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, "S4600_GROUP01_PRODUCT_SALES")
    if checkpoint.status(operation) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        raise RuntimeError(f"Prior {checkpoint.status(operation)} checkpoint requires reconciliation")
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    validate_root_and_mapping(client, args.logical_id)
    validate_metadata(client, payload)
    tax_before = tax_rows(client, target["sap_id"])
    key = exact_key(target["sap_id"])
    existing = get_row(client, key, SALES_SELECT)
    if existing is not None:
        if not matches(existing, payload):
            raise RuntimeError("Existing sales extension conflicts with approved payload")
        if str(existing.get("SupplyingPlant") or ""):
            raise RuntimeError("Existing sales extension contains an unapproved plant")
        persist_mapping(args.logical_id, target["sap_id"], payload, fingerprint)
        checkpoint.record(operation, "SKIPPED_EXISTS", detail=f"Exact 1010/10 sales extension exists for {target['sap_id']}")
        print(json.dumps({"product": args.logical_id, "result": "EXISTING", "sap_id": target["sap_id"]}))
        return 0
    token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        raise RuntimeError(f"CSRF preflight failed: HTTP {token_response.status}")
    checkpoint.before_write(operation)
    try:
        response = client.request("POST", SERVICE + ENTITY,
                                  headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                                  body=json.dumps(payload).encode("utf-8"))
    except (AmbiguousTransportError, TransportError) as error:
        checkpoint.record(operation, "AMBIGUOUS", detail=type(error).__name__)
        raise RuntimeError("Sales-extension POST outcome ambiguous; do not retry") from error
    if response.status not in {200, 201, 204}:
        evidence = response.error_evidence
        checkpoint.record(operation, "REJECTED", detail=json.dumps(evidence, sort_keys=True))
        raise RuntimeError(f"Sales-extension POST rejected HTTP {response.status}: {evidence}")
    try:
        fresh = UrllibSapTransport(config)
        readback = get_row(fresh, key, SALES_SELECT)
        tax_after = tax_rows(fresh, target["sap_id"])
    except Exception as error:
        checkpoint.record(operation, "AMBIGUOUS", detail=f"Independent readback unavailable: {type(error).__name__}")
        raise RuntimeError("Independent readback unavailable; do not retry") from error
    if readback is None or not matches(readback, payload):
        checkpoint.record(operation, "AMBIGUOUS", detail="Independent sales readback mismatch")
        raise RuntimeError("Independent sales readback mismatch; do not retry")
    if str(readback.get("SupplyingPlant") or ""):
        checkpoint.record(operation, "AMBIGUOUS", detail="Unexpected unapproved SupplyingPlant default")
        raise RuntimeError("SAP persisted an unapproved plant default; stop")
    if tax_after != tax_before:
        checkpoint.record(operation, "AMBIGUOUS", detail="Product tax state changed unexpectedly")
        raise RuntimeError("Product tax state changed unexpectedly; stop")
    persist_mapping(args.logical_id, target["sap_id"], payload, fingerprint)
    checkpoint.record(operation, "VERIFIED", detail=f"A_ProductSalesDelivery 1010/10 independently verified for {target['sap_id']}; product tax unchanged")
    print(json.dumps({"product": args.logical_id, "result": "CREATED", "sap_id": target["sap_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
