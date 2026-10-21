"""Create one exactly approved S4600 A_ProductSalesTax row."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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


APPROVAL_PATH = ROOT / "data/provisioning/s4600/product_tax_write_approval.group01.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4600/product_tax_execution_checkpoint.group01.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
LEDGER_PATH = ROOT / "data/provisioning/training_change_ledger.group01.json"
SERVICE = "sap/opu/odata/sap/API_PRODUCT_SRV/"
ENTITY = "A_ProductSalesTax"
SELECT = "Product,Country,TaxCategory,TaxClassification"
EXPECTED_ROOTS = {
    "T-D101": {"sap_id": "90000132", "ProductType": "DIEN", "IndustrySector": "W", "BaseUnit": "H", "Division": "00"},
    "T-MS101": {"sap_id": "60000445", "ProductType": "HAWA", "IndustrySector": "W", "BaseUnit": "PC", "Division": "00"},
    "T-MS201": {"sap_id": "60000446", "ProductType": "HAWA", "IndustrySector": "W", "BaseUnit": "PC", "Division": "00"},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def operation_for(logical_id: str) -> str:
    return f"S4600_PRODUCT_{logical_id.replace('-', '_')}_TAX_BE_MWST_1"


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_ledger(event: dict[str, Any]) -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger["events"].append(event)
    ledger["current_summary"]["latest_event_id"] = event["event_id"]
    if event.get("sap_write"):
        ledger["current_summary"]["sap_writes_since_bootstrap_launch"] += 1
    atomic_json(LEDGER_PATH, ledger)


def load_approved(logical_id: str) -> tuple[str, dict[str, str], dict[str, str], str]:
    document = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    operation = operation_for(logical_id)
    entry = document.get("operations", {}).get(operation, {})
    target, payload = entry.get("target", {}), entry.get("payload", {})
    fingerprint = entry.get("target_fingerprint", "")
    expected_id = EXPECTED_ROOTS[logical_id]["sap_id"]
    if (document.get("workflow_id") != "S4600_GROUP01_PRODUCT_TAX"
            or document.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or document.get("operation_scope") != "TRAINING_MASTER_DATA_PRODUCT_TAX"
            or document.get("sensitive_scope") != "TAX"
            or document.get("approval_status") != "APPROVED"
            or document.get("allow_write") is not True
            or not document.get("approved_by")
            or not document.get("authorization_evidence")
            or entry.get("allow_write") is not True
            or entry.get("limit") != "ONE_A_PRODUCT_SALES_TAX_POST_ONLY"
            or target != {"logical_product_id": logical_id, "sap_id": expected_id, "tax_key": "BE/MWST"}
            or payload != {"Product": expected_id, "Country": "BE", "TaxCategory": "MWST", "TaxClassification": "1"}
            or fingerprint != target_fingerprint(operation, target, payload)):
        raise RuntimeError("Exact PRODUCT_TAX approval, payload or fingerprint mismatch")
    return operation, target, payload, fingerprint


def tax_rows(client: UrllibSapTransport, sap_id: str) -> list[dict[str, Any]]:
    response = client.request("GET", SERVICE + ENTITY + "?" + urlencode({
        "$filter": f"Product eq '{sap_id}' and Country eq 'BE' and TaxCategory eq 'MWST'",
        "$select": SELECT,
        "$top": "20",
    }))
    if response.status != 200:
        raise RuntimeError(f"Exact product-tax lookup failed: HTTP {response.status}")
    rows = response.json().get("d", {}).get("results")
    if not isinstance(rows, list):
        raise RuntimeError("Product-tax response shape unknown")
    return [{key: value for key, value in row.items() if key != "__metadata"} for row in rows]


def validate_root_and_mapping(client: UrllibSapTransport, logical_id: str) -> None:
    expected = EXPECTED_ROOTS[logical_id]
    mappings = json.loads(MAPPING_PATH.read_text(encoding="utf-8")).get("mappings", {})
    mapping = mappings.get(logical_id, {})
    if mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != expected["sap_id"]:
        raise RuntimeError("LIVE_VERIFIED identity mapping mismatch")
    response = client.request("GET", SERVICE + f"A_Product('{expected['sap_id']}')?" + urlencode({
        "$select": "Product,ProductType,IndustrySector,BaseUnit,Division",
    }))
    root = response.json().get("d", {}) if response.status == 200 else {}
    if any(root.get(field) != value for field, value in expected.items() if field != "sap_id"):
        raise RuntimeError("Product root independent validation mismatch")


def validate_metadata(client: UrllibSapTransport, payload: dict[str, str]) -> None:
    response = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if response.status != 200:
        raise RuntimeError(f"Product metadata HTTP {response.status}")
    entity = inspect_creation_metadata(response.body, entities=(ENTITY,))[ENTITY]
    mandatory = {name for name, spec in entity["fields"].items() if not spec["nullable"]}
    expected_fields = {"Product", "Country", "TaxCategory", "TaxClassification"}
    if (entity["metadata_allows_create"] is not True
            or set(entity["keys"]) != expected_fields
            or mandatory != expected_fields):
        raise RuntimeError("Installed A_ProductSalesTax create contract changed")
    for field, value in payload.items():
        spec = entity["fields"].get(field)
        if not spec or spec["creatable"] is not True or spec["edm_type"] != "Edm.String":
            raise RuntimeError(f"Unproven tax payload field: {field}")
        if spec["max_length"] and spec["max_length"].isdigit() and len(value) > int(spec["max_length"]):
            raise RuntimeError(f"Tax payload exceeds field length: {field}")


def persist_mapping(logical_id: str, payload: dict[str, str], fingerprint: str) -> None:
    document = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    entry = document.get("mappings", {}).get(logical_id, {})
    if entry.get("status") != "LIVE_VERIFIED" or entry.get("sap_id") != payload["Product"]:
        raise RuntimeError("Mapping changed before tax evidence persistence")
    entry.setdefault("tax_extensions", {})["BE/MWST"] = {
        "status": "LIVE_VERIFIED",
        "entity": ENTITY,
        "payload": payload,
        "target_fingerprint": fingerprint,
    }
    atomic_json(MAPPING_PATH, document)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logical_id", choices=tuple(EXPECTED_ROOTS))
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    operation, target, payload, fingerprint = load_approved(args.logical_id)
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, "S4600_GROUP01_PRODUCT_TAX")
    if checkpoint.status(operation) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        raise RuntimeError(f"Prior {checkpoint.status(operation)} checkpoint requires reconciliation")
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    validate_root_and_mapping(client, args.logical_id)
    validate_metadata(client, payload)
    existing = tax_rows(client, target["sap_id"])
    if existing:
        if len(existing) != 1 or existing[0] != payload:
            raise RuntimeError("Existing BE/MWST tax row conflicts with approved payload")
        persist_mapping(args.logical_id, payload, fingerprint)
        checkpoint.record(operation, "SKIPPED_EXISTS", detail="Exact BE/MWST/1 tax row exists")
        print(json.dumps({"product": args.logical_id, "result": "EXISTING", "sap_id": target["sap_id"]}))
        return 0
    if args.preflight_only:
        print(json.dumps({"product": args.logical_id, "result": "READY", "sap_id": target["sap_id"]}))
        return 0
    token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        raise RuntimeError(f"CSRF preflight failed: HTTP {token_response.status}")
    event_prefix = f"SAP-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}-{args.logical_id}"
    append_ledger({
        "event_id": event_prefix + "-ATTEMPT",
        "occurred_at_utc": utc_now(),
        "event_type": "SAP_WRITE_ATTEMPT",
        "book": "S4600",
        "operation": operation,
        "target": target,
        "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
        "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX",
        "target_fingerprint": fingerprint,
        "before_state": [],
        "sap_result": "NOT_SENT_YET",
        "readback_state": "PENDING",
        "evidence": str(APPROVAL_PATH.relative_to(ROOT)),
        "sap_write": False,
    })
    checkpoint.before_write(operation)
    try:
        response = client.request(
            "POST", SERVICE + ENTITY,
            headers={"Content-Type": "application/json", "X-CSRF-Token": token},
            body=json.dumps(payload).encode("utf-8"),
        )
    except (AmbiguousTransportError, TransportError) as error:
        checkpoint.record(operation, "AMBIGUOUS", detail=type(error).__name__)
        append_ledger({
            "event_id": event_prefix + "-AMBIGUOUS", "occurred_at_utc": utc_now(),
            "event_type": "SAP_WRITE_RESULT", "book": "S4600", "operation": operation,
            "target": target, "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
            "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX", "target_fingerprint": fingerprint,
            "before_state": [], "sap_result": "AMBIGUOUS_TRANSPORT", "readback_state": "NOT_AVAILABLE",
            "evidence": type(error).__name__, "sap_write": True,
        })
        raise RuntimeError("Product-tax POST outcome ambiguous; do not retry") from error
    if response.status not in {200, 201, 204}:
        evidence = response.error_evidence
        checkpoint.record(operation, "REJECTED", detail=json.dumps(evidence, sort_keys=True))
        append_ledger({
            "event_id": event_prefix + "-REJECTED", "occurred_at_utc": utc_now(),
            "event_type": "SAP_WRITE_RESULT", "book": "S4600", "operation": operation,
            "target": target, "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
            "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX", "target_fingerprint": fingerprint,
            "before_state": [], "sap_result": {"status": response.status, "error": evidence},
            "readback_state": "NOT_PERFORMED_AFTER_CERTIFIED_REJECTION", "evidence": evidence,
            "sap_write": True,
        })
        raise RuntimeError(f"Product-tax POST rejected HTTP {response.status}: {evidence}")
    try:
        readback = tax_rows(UrllibSapTransport(config), target["sap_id"])
    except Exception as error:
        checkpoint.record(operation, "AMBIGUOUS", detail=f"Independent readback unavailable: {type(error).__name__}")
        append_ledger({
            "event_id": event_prefix + "-AMBIGUOUS", "occurred_at_utc": utc_now(),
            "event_type": "SAP_WRITE_RESULT", "book": "S4600", "operation": operation,
            "target": target, "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
            "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX", "target_fingerprint": fingerprint,
            "before_state": [], "sap_result": {"status": response.status},
            "readback_state": f"UNAVAILABLE:{type(error).__name__}", "evidence": str(CHECKPOINT_PATH.relative_to(ROOT)),
            "sap_write": True,
        })
        raise RuntimeError("Independent product-tax readback unavailable; do not retry") from error
    if len(readback) != 1 or readback[0] != payload:
        checkpoint.record(operation, "AMBIGUOUS", detail="Independent product-tax readback mismatch")
        append_ledger({
            "event_id": event_prefix + "-AMBIGUOUS", "occurred_at_utc": utc_now(),
            "event_type": "SAP_WRITE_RESULT", "book": "S4600", "operation": operation,
            "target": target, "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
            "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX", "target_fingerprint": fingerprint,
            "before_state": [], "sap_result": {"status": response.status},
            "readback_state": readback, "evidence": str(CHECKPOINT_PATH.relative_to(ROOT)),
            "sap_write": True,
        })
        raise RuntimeError("Independent product-tax readback mismatch; do not retry")
    persist_mapping(args.logical_id, payload, fingerprint)
    checkpoint.record(operation, "VERIFIED", detail="A_ProductSalesTax BE/MWST/1 independently verified")
    append_ledger({
        "event_id": event_prefix + "-VERIFIED", "occurred_at_utc": utc_now(),
        "event_type": "SAP_WRITE_RESULT", "book": "S4600", "operation": operation,
        "target": target, "interface": "API_PRODUCT_SRV/A_ProductSalesTax",
        "approval_scope": "TRAINING_MASTER_DATA_PRODUCT_TAX/TAX", "target_fingerprint": fingerprint,
        "before_state": [], "sap_result": {"status": response.status},
        "readback_state": readback, "evidence": str(CHECKPOINT_PATH.relative_to(ROOT)),
        "sap_write": True,
    })
    print(json.dumps({"product": args.logical_id, "result": "CREATED", "sap_id": target["sap_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
