"""One-at-a-time customer-role provisioning for S4600 T-S50A01."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.provisioning.execution_policy import ExecutionCheckpoint, target_fingerprint
from src.provisioning.s4600_t_s50a01_bp_address import read_state as read_address_state
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


ROOT = Path(__file__).resolve().parents[2]
SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
BP = "1000000116"
LOGICAL_ID = "T-S50A01"
ROLES = ("FLCU00", "FLCU01")
OPERATIONS = {role: f"S4600_T_S50A01_{role}_ROLE" for role in ROLES}
TARGET = {"logical_id": LOGICAL_ID, "sap_id": BP}
APPROVAL_PATH = ROOT / "data/provisioning/s4600/T-S50A01.customer_roles_approval.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4600/T-S50A01.customer_roles_checkpoint.json"
ATTEMPT_DIR = ROOT / "data/provisioning/s4600"


def _payload(role: str) -> dict[str, str]:
    return {"BusinessPartner": BP, "BusinessPartnerRole": role}


def _validate_approval(role: str) -> None:
    if role not in ROLES:
        raise ValueError("Role is not allowlisted")
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))["mappings"].get(LOGICAL_ID, {})
    item = approval.get("operations", {}).get(role, {})
    expected = target_fingerprint(OPERATIONS[role], TARGET, _payload(role))
    if (
        approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
        or approval.get("existing_business_partner") != BP
        or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
        or approval.get("approval_scope") != "TRAINING_MASTER_DATA_CUSTOMER_ROLES"
        or approval.get("sequence") != ["FLCU00", "FLCU01"]
        or item.get("operation") != OPERATIONS[role]
        or item.get("execute") is not True
        or item.get("payload") != _payload(role)
        or item.get("fingerprint") != expected
        or mapping.get("sap_id") != BP
        or mapping.get("status") != "LIVE_VERIFIED"
    ):
        raise ValueError(f"Exact {role} approval or verified mapping mismatch")


def ensure_role(
    config: SapRuntimeConfig, role: str, *, execute: bool = False,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, Any]:
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is authorized")
    _validate_approval(role)
    address = read_address_state(transport_factory(config))
    if address != {"state": "EXISTS", "address_id": "1584", "current_standard": True}:
        return {"status": "BLOCKED", "reason": "Current standard address 1584 is not verified"}
    client = transport_factory(config)
    key = f"A_BusinessPartnerRole(BusinessPartner='{BP}',BusinessPartnerRole='{role}')"
    lookup = client.request("GET", SERVICE + key)
    if lookup.status == 200:
        row = lookup.json().get("d", {})
        if row.get("BusinessPartner") != BP or row.get("BusinessPartnerRole") != role:
            return {"status": "BLOCKED", "reason": "Existing role identity mismatch"}
        return {"status": "EXISTS", "role": role}
    if lookup.status != 404:
        return {"status": "BLOCKED", "reason": f"Role lookup unknown: HTTP {lookup.status}"}
    if role == "FLCU01":
        dependency = client.request(
            "GET", SERVICE + f"A_BusinessPartnerRole(BusinessPartner='{BP}',BusinessPartnerRole='FLCU00')")
        if dependency.status != 200:
            return {"status": "BLOCKED", "reason": "FLCU00 dependency is not verified"}
    metadata = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        return {"status": "BLOCKED", "reason": f"Metadata GET failed: HTTP {metadata.status}"}
    entity = inspect_creation_metadata(metadata.body, entities=("A_BusinessPartnerRole",))["A_BusinessPartnerRole"]
    mandatory = {name for name, field in entity["fields"].items() if not field["nullable"]}
    if (
        not entity["metadata_allows_create"]
        or entity["keys"] != ["BusinessPartner", "BusinessPartnerRole"]
        or mandatory != {"BusinessPartner", "BusinessPartnerRole"}
        or not all(entity["fields"][name]["creatable"] for name in mandatory)
    ):
        return {"status": "BLOCKED", "reason": "Installed role creation contract differs"}
    attempt_path = ATTEMPT_DIR / f"T-S50A01.{role}.attempt.json"
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, "S4600_T_S50A01_CUSTOMER_ROLES")
    operation = OPERATIONS[role]
    if attempt_path.exists() or checkpoint.status(operation) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        return {"status": "BLOCKED", "reason": "Previous role write attempt requires reconciliation"}
    if not execute:
        return {
            "status": "READY",
            "role": role,
            "payload": _payload(role),
            "fingerprint": target_fingerprint(operation, TARGET, _payload(role)),
        }
    token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        return {"status": "BLOCKED", "reason": f"CSRF preflight failed: HTTP {token_response.status}"}
    checkpoint.before_write(operation)
    with attempt_path.open("x", encoding="utf-8") as handle:
        json.dump({
            "operation": operation, "logical_id": LOGICAL_ID, "sap_id": BP,
            "role": role, "fingerprint": target_fingerprint(operation, TARGET, _payload(role)),
            "status": "POST_ATTEMPTED", "retry_allowed": False,
        }, handle)
    try:
        response = client.request(
            "POST", SERVICE + "A_BusinessPartnerRole",
            headers={"Content-Type": "application/json", "X-CSRF-Token": token},
            body=json.dumps(_payload(role)).encode("utf-8"),
        )
    except Exception as error:
        checkpoint.record(operation, "AMBIGUOUS", detail=type(error).__name__)
        return {"status": "BLOCKED", "reason": "POST outcome ambiguous; no retry"}
    if response.status not in {200, 201, 204}:
        evidence = response.error_evidence
        attempt_path.write_text(json.dumps({
            "operation": operation, "logical_id": LOGICAL_ID, "sap_id": BP, "role": role,
            "status": f"POST_REJECTED_HTTP_{response.status}", "sap_error": evidence,
            "retry_allowed": False,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checkpoint.record(operation, "REJECTED", detail=str(evidence.get("sap_code") if evidence else response.status))
        return {"status": "BLOCKED", "reason": f"POST rejected HTTP {response.status}", "sap_error": evidence}
    readback = transport_factory(config).request("GET", SERVICE + key)
    row = readback.json().get("d", {}) if readback.status == 200 else {}
    customer = transport_factory(config).request("GET", SERVICE + f"A_Customer('{BP}')")
    customer_row = customer.json().get("d", {}) if customer.status == 200 else {}
    if (
        row.get("BusinessPartner") != BP
        or row.get("BusinessPartnerRole") != role
        or customer_row.get("Customer") != BP
    ):
        checkpoint.record(operation, "AMBIGUOUS", detail="independent role/customer readback failed")
        return {"status": "BLOCKED", "reason": "Independent role/customer readback failed; no retry"}
    attempt_path.write_text(json.dumps({
        "operation": operation, "logical_id": LOGICAL_ID, "sap_id": BP, "role": role,
        "status": "VERIFIED", "retry_allowed": False, "customer_root": "EXISTS",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint.record(operation, "VERIFIED", detail=role)
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    approval.setdefault("verified_states", {})[role] = "EXISTS"
    APPROVAL_PATH.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    evidence = mapping["mappings"][LOGICAL_ID].setdefault("evidence", {})
    evidence[f"role_{role.lower()}_readback"] = "EXISTS"
    evidence["customer_root_readback"] = "EXISTS"
    MAPPING_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "CREATED_AND_VERIFIED", "role": role, "customer_root": "EXISTS"}
