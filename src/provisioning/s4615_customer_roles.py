"""One-shot, scoped FLCU00/FLCU01 role provisioning for the existing S4615 BP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.provisioning.execution_policy import ExecutionCheckpoint, target_fingerprint
from src.provisioning.s4615_bp_standard_address import read_state
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
ROLES = ("FLCU00", "FLCU01")
WORKFLOW_ID = "S4615_CUSTOMER_A01"


def ensure_roles_once(
    config: SapRuntimeConfig,
    approval_path: Path,
    mapping_path: Path,
    attempt_dir: Path,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, str]:
    if config.client != "600" or config.username != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is approved")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    if (approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("existing_business_partner") != "1000000115"
            or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
            or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])):
        raise ValueError("Scoped customer master approval mismatch")
    mappings = json.loads(mapping_path.read_text(encoding="utf-8"))["mappings"]
    mapped = mappings.get("C615-A01", {})
    if mapped.get("status") != "LIVE_VERIFIED" or mapped.get("sap_id") != "1000000115":
        raise ValueError("Verified C615-A01 mapping mismatch")
    for role in ROLES:
        if f"{role}_ROLE" not in approval.get("approved_scope", []):
            raise ValueError(f"{role} is not in scoped approval")
        if approval.get("step_authorizations", {}).get(f"{role}_ROLE", {}).get("execute") is not True:
            raise ValueError(f"{role} lacks explicit step execution approval")
    client = transport_factory(config)
    metadata = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        raise RuntimeError(f"BP metadata GET failed: HTTP {metadata.status}")
    entity = inspect_creation_metadata(metadata.body, entities=("A_BusinessPartnerRole",))["A_BusinessPartnerRole"]
    if (not entity["metadata_allows_create"] or entity["keys"] != ["BusinessPartner", "BusinessPartnerRole"]
            or {name for name, field in entity["fields"].items() if not field["nullable"]}
            != {"BusinessPartner", "BusinessPartnerRole"}
            or not all(entity["fields"][name]["creatable"] for name in entity["keys"])):
        raise RuntimeError("Installed role creation contract is not proven")
    result = {}
    for role in ROLES:
        key = f"A_BusinessPartnerRole(BusinessPartner='1000000115',BusinessPartnerRole='{role}')"
        attempt_path = attempt_dir / f"C615-A01.{role}.attempt.json"
        precheck = client.request("GET", SERVICE + key)
        if precheck.status == 200:
            row = precheck.json().get("d", {})
            if row.get("BusinessPartner") != "1000000115" or row.get("BusinessPartnerRole") != role:
                raise RuntimeError(f"{role} exists with unexpected values")
            result[role] = "EXISTS"
            continue
        if precheck.status != 404:
            raise RuntimeError(f"{role} lookup unknown: HTTP {precheck.status}")
        if attempt_path.exists():
            raise RuntimeError(f"{role} prior write attempt exists; no automatic retry")
        token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
        token = token_response.header("X-CSRF-Token")
        if token_response.status != 200 or not token:
            raise RuntimeError(f"{role} CSRF preflight failed: HTTP {token_response.status}")
        attempt_dir.mkdir(parents=True, exist_ok=True)
        with attempt_path.open("x", encoding="utf-8") as marker:
            json.dump({"logical_id": "C615-A01", "sap_id": "1000000115", "role": role,
                       "status": "POST_ATTEMPTED", "retry_allowed": False}, marker)
        payload = {"BusinessPartner": "1000000115", "BusinessPartnerRole": role}
        response = client.request("POST", SERVICE + "A_BusinessPartnerRole",
                                  headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                                  body=json.dumps(payload).encode("utf-8"))
        if response.status not in (200, 201, 204):
            attempt_path.write_text(json.dumps({"logical_id": "C615-A01", "sap_id": "1000000115",
                                                "role": role, "status": f"POST_REJECTED_HTTP_{response.status}",
                                                "sap_error": response.error_evidence,
                                                "retry_allowed": False}) + "\n", encoding="utf-8")
            raise RuntimeError(f"{role} POST failed: HTTP {response.status}; no automatic retry")
        readback = transport_factory(config).request("GET", SERVICE + key)
        row = readback.json().get("d", {}) if readback.status == 200 else {}
        if row.get("BusinessPartner") != "1000000115" or row.get("BusinessPartnerRole") != role:
            raise RuntimeError(f"{role} independent readback failed; no automatic retry")
        attempt_path.write_text(json.dumps({"logical_id": "C615-A01", "sap_id": "1000000115",
                                            "role": role, "status": "VERIFIED", "retry_allowed": False}) + "\n",
                                encoding="utf-8")
        result[role] = "CREATED"
    return result


def ensure_roles_after_verified_address(
    config: SapRuntimeConfig,
    approval_path: Path,
    mapping_path: Path,
    attempt_dir: Path,
    checkpoint_path: Path,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, dict[str, Any]]:
    """Reconcile FSBP_ECC025 once, then execute independent approved role steps.

    The old rejected FLCU00 marker is retained. A distinct post-address marker
    is used for the corrected contract. Ambiguous writes are never retried.
    """
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is approved")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))["mappings"].get("C615-A01", {})
    if (approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("existing_business_partner") != "1000000115"
            or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
            or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])
            or approval.get("proposed_values", {}).get("roles") != list(ROLES)
            or mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != "1000000115"):
        raise ValueError("Exact C615-A01 workflow approval or BP mapping mismatch")
    for role in ROLES:
        if (f"{role}_ROLE" not in approval.get("approved_scope", [])
                or approval.get("step_authorizations", {}).get(f"{role}_ROLE", {}).get("execute") is not True):
            raise ValueError(f"Exact {role} workflow step is not approved")
        operation = f"ENSURE_{role}_ROLE_AFTER_ADDRESS" if role == "FLCU00" else "ENSURE_FLCU01_ROLE"
        expected_fingerprint = target_fingerprint(
            operation, {"logical_id": "C615-A01", "sap_id": "1000000115"},
            {"BusinessPartner": "1000000115", "BusinessPartnerRole": role})
        if approval.get("role_target_fingerprints", {}).get(role) != expected_fingerprint:
            raise ValueError(f"Exact {role} target/value approval fingerprint mismatch")
    address = read_state(transport_factory(config))
    if address != {"state": "EXISTS", "address_id": "1581", "current_standard": True}:
        raise RuntimeError("Current standard address 1581 is not independently verified")
    if (approval.get("verified_step_states", {}).get("BP_ADDRESS") != "EXISTS_CURRENT_XXDEFAULT"
            or approval.get("address_evidence", {}).get("verified_address_id") != "1581"):
        raise ValueError("Recorded address checkpoint mismatch")
    metadata = transport_factory(config).request(
        "GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        raise RuntimeError(f"BP role metadata GET failed: HTTP {metadata.status}")
    entity = inspect_creation_metadata(metadata.body, entities=("A_BusinessPartnerRole",))["A_BusinessPartnerRole"]
    if (not entity["metadata_allows_create"]
            or entity["keys"] != ["BusinessPartner", "BusinessPartnerRole"]
            or {name for name, field in entity["fields"].items() if not field["nullable"]}
            != {"BusinessPartner", "BusinessPartnerRole"}
            or not all(entity["fields"][name]["creatable"] for name in entity["keys"])):
        raise RuntimeError("Installed A_BusinessPartnerRole creation contract is not proven")

    checkpoint = ExecutionCheckpoint(checkpoint_path, WORKFLOW_ID)
    result: dict[str, dict[str, Any]] = {}
    for role in ROLES:
        operation = f"ENSURE_{role}_ROLE_AFTER_ADDRESS" if role == "FLCU00" else "ENSURE_FLCU01_ROLE"
        key = f"A_BusinessPartnerRole(BusinessPartner='1000000115',BusinessPartnerRole='{role}')"
        client = transport_factory(config)
        precheck = client.request("GET", SERVICE + key)
        if precheck.status == 200:
            row = precheck.json().get("d", {})
            if row.get("BusinessPartner") != "1000000115" or row.get("BusinessPartnerRole") != role:
                result[role] = {"status": "BLOCKED", "reason": "Existing role identity mismatch"}
                continue
            checkpoint.record(operation, "SKIPPED_EXISTS")
            result[role] = {"status": "EXISTS"}
            continue
        if precheck.status != 404:
            result[role] = {"status": "BLOCKED", "reason": f"Role lookup unknown: HTTP {precheck.status}"}
            continue
        if role == "FLCU00":
            prior_path = attempt_dir / "C615-A01.FLCU00.attempt.json"
            if not prior_path.exists():
                result[role] = {"status": "BLOCKED", "reason": "Prior FLCU00 attempt record missing"}
                continue
            prior = json.loads(prior_path.read_text(encoding="utf-8"))
            if (prior.get("logical_id") != "C615-A01" or prior.get("sap_id") != "1000000115"
                    or prior.get("role") != "FLCU00"
                    or prior.get("status") != "POST_REJECTED_HTTP_400"
                    or prior.get("independent_readback_http") != 404
                    or prior.get("retry_allowed") is not False
                    or not str(approval.get("address_evidence", {}).get("role_error", "")).startswith("FSBP_ECC025")):
                result[role] = {"status": "BLOCKED", "reason": "Prior deterministic FSBP_ECC025 failure not proven"}
                continue
            marker = attempt_dir / "C615-A01.FLCU00.after_address.attempt.json"
        else:
            marker = attempt_dir / "C615-A01.FLCU01.attempt.json"
        if marker.exists():
            previous = json.loads(marker.read_text(encoding="utf-8"))
            lock_released = approval.get("lock_release_evidence", {})
            if (previous.get("logical_id") != "C615-A01"
                    or previous.get("sap_id") != "1000000115"
                    or previous.get("role") != role
                    or previous.get("status") != "POST_REJECTED_HTTP_400"
                    or previous.get("sap_error", {}).get("sap_code") != "R1/084"
                    or previous.get("retry_allowed") is not False
                    or checkpoint.status(operation) != "REJECTED"
                    or lock_released.get("bp_id") != "1000000115"
                    or lock_released.get("user_reported_exit") is not True):
                result[role] = {"status": "BLOCKED", "reason": "Previous role write attempt requires reconciliation"}
                continue
            operation = f"ENSURE_{role}_ROLE_AFTER_LOCK_RELEASE"
            expected_fingerprint = target_fingerprint(
                operation, {"logical_id": "C615-A01", "sap_id": "1000000115"},
                {"BusinessPartner": "1000000115", "BusinessPartnerRole": role})
            if approval.get("role_lock_recovery_fingerprints", {}).get(role) != expected_fingerprint:
                result[role] = {"status": "BLOCKED", "reason": "Lock-recovery target/value approval mismatch"}
                continue
            marker = attempt_dir / f"C615-A01.{role}.after_lock_release.attempt.json"
        if marker.exists() or checkpoint.status(operation) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
            result[role] = {"status": "BLOCKED", "reason": "Previous role write attempt requires reconciliation"}
            continue
        token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
        token = token_response.header("X-CSRF-Token")
        if token_response.status != 200 or not token:
            result[role] = {"status": "BLOCKED", "reason": f"CSRF preflight failed: HTTP {token_response.status}"}
            continue
        attempt_dir.mkdir(parents=True, exist_ok=True)
        checkpoint.before_write(operation)
        with marker.open("x", encoding="utf-8") as handle:
            json.dump({"logical_id": "C615-A01", "sap_id": "1000000115", "role": role,
                       "status": "POST_ATTEMPTED", "retry_allowed": False,
                       "address_id": "1581", "reconciles": "FSBP_ECC025" if role == "FLCU00" else None}, handle)
        payload = {"BusinessPartner": "1000000115", "BusinessPartnerRole": role}
        try:
            response = client.request("POST", SERVICE + "A_BusinessPartnerRole",
                                      headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                                      body=json.dumps(payload).encode("utf-8"))
        except Exception as error:
            checkpoint.record(operation, "AMBIGUOUS", detail=type(error).__name__)
            result[role] = {"status": "BLOCKED", "reason": "POST outcome ambiguous; no retry"}
            continue
        if response.status not in (200, 201, 204):
            evidence = response.error_evidence
            marker.write_text(json.dumps({"logical_id": "C615-A01", "sap_id": "1000000115",
                                          "role": role, "status": f"POST_REJECTED_HTTP_{response.status}",
                                          "sap_error": evidence, "retry_allowed": False}) + "\n", encoding="utf-8")
            checkpoint.record(operation, "REJECTED", detail=str(evidence.get("sap_code") if evidence else response.status))
            result[role] = {"status": "BLOCKED", "reason": f"POST rejected HTTP {response.status}",
                            "sap_error": evidence}
            continue
        try:
            readback = transport_factory(config).request("GET", SERVICE + key)
            row = readback.json().get("d", {}) if readback.status == 200 else {}
        except Exception:
            checkpoint.record(operation, "AMBIGUOUS", detail="independent role readback unavailable")
            result[role] = {"status": "BLOCKED", "reason": "Independent role readback unavailable; no retry"}
            continue
        if row.get("BusinessPartner") != "1000000115" or row.get("BusinessPartnerRole") != role:
            checkpoint.record(operation, "AMBIGUOUS", detail="independent role readback failed")
            result[role] = {"status": "BLOCKED", "reason": "Independent role readback failed; no retry"}
            continue
        marker.write_text(json.dumps({"logical_id": "C615-A01", "sap_id": "1000000115",
                                      "role": role, "status": "VERIFIED", "retry_allowed": False,
                                      "address_id": "1581"}) + "\n", encoding="utf-8")
        checkpoint.record(operation, "VERIFIED", detail=role)
        approval.setdefault("verified_step_states", {})[f"{role}_ROLE"] = "EXISTS"
        approval_path.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result[role] = {"status": "CREATED_AND_VERIFIED"}
    return result
