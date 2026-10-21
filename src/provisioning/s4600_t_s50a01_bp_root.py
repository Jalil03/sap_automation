"""One-shot BP root contract for S4600 T-S50A01.

No customer roles, address, company-code, sales-area, tax, FI, plant, or stock
data is part of this operation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from src.provisioning.customer_bp_root import (
    assess_bp_root_identity_readback,
    capture_generated_bp_id,
    generated_bp_readback_keys,
    prepare_bp_root,
)
from src.provisioning.sap_api_backend import persist_mapping
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


ROOT = Path(__file__).resolve().parents[2]
OPERATION = "S4600_T_S50A01_BP_ROOT"
TARGET = {"logical_id": "T-S50A01", "sap_partner_id": None}
VALUES = {
    "logical_id": "T-S50A01",
    "business_partner": None,
    "bp_grouping": "BPAB",
    "bp_category": "2",
    "training_name": "Motormarkt Heidelberg",
    "duplicate_key": "T-S50A01",
}
PAYLOAD = {
    "BusinessPartnerGrouping": "BPAB",
    "BusinessPartnerCategory": "2",
    "OrganizationBPName1": "Motormarkt Heidelberg",
    "SearchTerm1": "T-S50A01",
}
REQUIRED_SCOPES = {
    "TRAINING_DATA_OWNER_NEW_DATASET",
    "CUSTOMER_MASTER_OWNER",
    "TRAINING_MASTER_DATA_BP_ROOT",
}
DEFAULT_APPROVAL_PATH = ROOT / "data/provisioning/s4600/T-S50A01.bp_root_approval.json"
DEFAULT_ATTEMPT_PATH = ROOT / "data/provisioning/s4600/T-S50A01.bp_root_attempt.json"
DEFAULT_MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"


def target_fingerprint() -> str:
    canonical = json.dumps(
        {"operation": OPERATION, "target": TARGET, "payload": PAYLOAD},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def contract_summary() -> dict[str, Any]:
    return {
        "operation": OPERATION,
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "target": TARGET,
        "payload": PAYLOAD,
        "target_fingerprint": target_fingerprint(),
        "required_approval_scopes": sorted(REQUIRED_SCOPES),
        "limit": "ONE_BP_ROOT_POST_ONLY",
        "excluded": [
            "address", "roles", "customer root", "company code", "sales area",
            "partner functions", "tax", "FI/MM", "plant", "valuation", "stock",
        ],
    }


def preflight(
    *,
    config: SapRuntimeConfig,
    attempt_path: Path = DEFAULT_ATTEMPT_PATH,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, Any]:
    """Perform only fresh metadata and anti-duplicate GETs; never fetch CSRF or POST."""
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("T-S50A01 requires A4H client 600 / ABDELJ")
    if Path(attempt_path).exists():
        raise RuntimeError("T-S50A01 has a prior attempt requiring reconciliation")
    mappings = json.loads(Path(mapping_path).read_text(encoding="utf-8")).get("mappings", {})
    if TARGET["logical_id"] in mappings:
        raise RuntimeError("T-S50A01 already has an identity mapping")
    service = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
    client = transport_factory(config)
    metadata = client.request("GET", service + "$metadata?sap-client=600", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        raise RuntimeError(f"BP metadata GET failed: HTTP {metadata.status}")
    prepared = prepare_bp_root(VALUES, metadata.body)
    if prepared.get("status") != "PAYLOAD_PREPARED" or prepared.get("payload") != PAYLOAD:
        raise RuntimeError("Installed metadata does not validate the exact T-S50A01 payload")
    filters = {
        "literal_key": "BusinessPartner eq 'T-S50A01'",
        "external_id": "BusinessPartnerIDByExtSystem eq 'T-S50A01'",
        "search_term": "SearchTerm1 eq 'T-S50A01'",
        "exact_name": "OrganizationBPName1 eq 'Motormarkt Heidelberg'",
    }
    checks = {}
    for label, filter_value in filters.items():
        query = urlencode({"sap-client": "600", "$filter": filter_value, "$select": "BusinessPartner", "$top": "2"})
        response = client.request("GET", service + "A_BusinessPartner?" + query)
        if response.status != 200:
            raise RuntimeError(f"Fresh duplicate {label} GET failed: HTTP {response.status}")
        data = response.json().get("d")
        rows = data.get("results") if isinstance(data, dict) else None
        if not isinstance(rows, list):
            raise RuntimeError(f"Fresh duplicate {label} response shape is unverified")
        if rows:
            raise RuntimeError(f"Fresh duplicate {label} found; no POST")
        checks[label] = "ZERO_ROWS"
    return {
        "status": "WRITE_CONTRACT_READY_AWAITING_APPROVAL",
        "environment": {"system": "A4H", "client": config.client, "user": config.username.upper()},
        "payload": PAYLOAD,
        "metadata": "VALIDATED",
        "duplicate_checks": checks,
        "configuration_evidence": "BPAB/category 2 already accepted by A4H/600 for an internally numbered organization BP",
        "target_fingerprint": target_fingerprint(),
        "sap_write_attempted": False,
    }


def _validate_approval(document: dict[str, Any]) -> None:
    approval = document.get(OPERATION)
    if not isinstance(approval, dict):
        raise ValueError("Exact T-S50A01 approval is missing")
    if (approval.get("system"), str(approval.get("client")), str(approval.get("user", "")).upper()) != (
        "A4H", "600", "ABDELJ"
    ):
        raise ValueError("Approval environment mismatch")
    if approval.get("operation") != OPERATION or approval.get("allow_write") is not True:
        raise ValueError("Approval does not authorize the exact BP-root write")
    if approval.get("target_fingerprint") != target_fingerprint():
        raise ValueError("Approval target/value fingerprint mismatch")
    if approval.get("limit") != "ONE_BP_ROOT_POST_ONLY":
        raise ValueError("Approval must limit execution to one BP-root POST")
    if not REQUIRED_SCOPES.issubset(set(approval.get("approval_scopes") or [])):
        raise ValueError("Required new-dataset/customer-master/training scopes are missing")
    if not str(approval.get("approved_by") or "").strip():
        raise ValueError("Approval owner evidence is missing")


def execute_once(
    *,
    config: SapRuntimeConfig,
    approval_path: Path = DEFAULT_APPROVAL_PATH,
    attempt_path: Path = DEFAULT_ATTEMPT_PATH,
    mapping_path: Path = DEFAULT_MAPPING_PATH,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, Any]:
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("T-S50A01 requires A4H client 600 / ABDELJ")
    approval = json.loads(Path(approval_path).read_text(encoding="utf-8"))
    _validate_approval(approval)
    if Path(attempt_path).exists():
        raise RuntimeError("T-S50A01 POST was already attempted; reconcile instead of retrying")
    mappings = json.loads(Path(mapping_path).read_text(encoding="utf-8")).get("mappings", {})
    if TARGET["logical_id"] in mappings:
        raise RuntimeError("T-S50A01 already has an identity mapping")

    service = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
    client = transport_factory(config)
    metadata = client.request("GET", service + "$metadata?sap-client=600", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        raise RuntimeError(f"BP metadata GET failed: HTTP {metadata.status}")
    prepared = prepare_bp_root(VALUES, metadata.body)
    if prepared.get("status") != "PAYLOAD_PREPARED" or prepared.get("payload") != PAYLOAD:
        raise RuntimeError("Installed metadata does not validate the exact T-S50A01 payload")

    filters = {
        "literal_key": "BusinessPartner eq 'T-S50A01'",
        "external_id": "BusinessPartnerIDByExtSystem eq 'T-S50A01'",
        "search_term": "SearchTerm1 eq 'T-S50A01'",
        "exact_name": "OrganizationBPName1 eq 'Motormarkt Heidelberg'",
    }
    for label, filter_value in filters.items():
        query = urlencode({"sap-client": "600", "$filter": filter_value, "$select": "BusinessPartner", "$top": "2"})
        response = client.request("GET", service + "A_BusinessPartner?" + query)
        if response.status != 200:
            raise RuntimeError(f"Fresh duplicate {label} GET failed: HTTP {response.status}")
        data = response.json().get("d")
        rows = data.get("results") if isinstance(data, dict) else None
        if not isinstance(rows, list):
            raise RuntimeError(f"Fresh duplicate {label} response shape is unverified")
        if rows:
            raise RuntimeError(f"Fresh duplicate {label} found; no POST")

    csrf = client.request("GET", service + "?sap-client=600", headers={"X-CSRF-Token": "Fetch"})
    token = csrf.header("X-CSRF-Token")
    if csrf.status != 200 or not token:
        raise RuntimeError(f"BP CSRF/session preflight failed: HTTP {csrf.status}")

    attempt_path = Path(attempt_path)
    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    with attempt_path.open("x", encoding="utf-8") as handle:
        json.dump(
            {"operation": OPERATION, "logical_id": "T-S50A01", "status": "POST_ATTEMPTED",
             "target_fingerprint": target_fingerprint(), "post_count_limit": 1},
            handle,
            sort_keys=True,
        )
        handle.write("\n")

    response = client.request(
        "POST",
        service + "A_BusinessPartner?sap-client=600",
        headers={"Content-Type": "application/json", "X-CSRF-Token": token},
        body=json.dumps(PAYLOAD, separators=(",", ":")).encode("utf-8"),
    )
    sap_id = capture_generated_bp_id(response)

    readback_client = transport_factory(config)
    key = generated_bp_readback_keys(sap_id)["root"]
    query = urlencode({"sap-client": "600", "$select": "BusinessPartner," + ",".join(PAYLOAD)})
    readback = readback_client.request("GET", service + key + "?" + query)
    assessment = assess_bp_root_identity_readback(readback, sap_id, PAYLOAD, metadata.body)
    if not assessment.get("verified"):
        raise RuntimeError("T-S50A01 independent readback failed; do not retry POST")

    persist_mapping(
        Path(mapping_path),
        "T-S50A01",
        sap_id,
        {
            "service": "API_BUSINESS_PARTNER",
            "entity_set": "A_BusinessPartner",
            "root_readback": "EXISTS",
            "scope": "BP_ROOT_ONLY",
            "target_fingerprint": target_fingerprint(),
            "verified_fields": assessment.get("verified_fields", []),
        },
    )
    attempt_path.write_text(
        json.dumps(
            {"operation": OPERATION, "logical_id": "T-S50A01", "sap_id": sap_id,
             "status": "VERIFIED", "post_count": 1, "target_fingerprint": target_fingerprint()},
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    return {"status": "VERIFIED", "logical_id": "T-S50A01", "sap_id": sap_id, "scope": "BP_ROOT_ONLY"}
