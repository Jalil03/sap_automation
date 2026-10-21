"""One scoped, checkpointed FI customer-company extension for S4615 A01."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
ENTITY = "A_CustomerCompany"
KEY = "A_CustomerCompany(Customer='1000000115',CompanyCode='1010')"
OPERATION = "ENSURE_C615_A01_COMPANY_1010"
TARGET = {"logical_id": "C615-A01", "sap_id": "1000000115", "company_code": "1010"}
PAYLOAD = {"Customer": "1000000115", "CompanyCode": "1010",
           "ReconciliationAccount": "400000", "PaymentTerms": "0004"}


def _matches(row: dict[str, Any]) -> bool:
    return all(row.get(name) == value for name, value in PAYLOAD.items())


def ensure_company_once(
    config: SapRuntimeConfig, approval_path: Path, mapping_path: Path,
    checkpoint_path: Path, attempt_path: Path,
    transport_factory: Any = UrllibSapTransport,
) -> dict[str, Any]:
    if config.client != "600" or config.username != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is approved")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))["mappings"].get("C615-A01", {})
    if (approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("existing_business_partner") != "1000000115"
            or approval.get("step_authorizations", {}).get("CUSTOMER_COMPANY_1010", {}).get("execute") is not True
            or approval.get("proposed_values", {}).get("reconciliation_account", {}).get("value") != "400000"
            or approval.get("proposed_values", {}).get("payment_terms", {}).get("value") != "0004"
            or mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != "1000000115"
            or approval.get("verified_step_states", {}).get("CUSTOMER_SALES_AREA_1010_10_00") != "EXISTS"
            or approval.get("verified_step_states", {}).get("FLCU00_ROLE") != "EXISTS"):
        raise ValueError("A01 FI approval, values, mapping or prerequisites mismatch")
    TrainingExecutionPolicy.from_document(approval.get("company_extension_policy", {})).authorize(
        OPERATION, TARGET, PAYLOAD)
    checkpoint = ExecutionCheckpoint(checkpoint_path, "S4615_CUSTOMER_A01")
    client = transport_factory(config)
    precheck = client.request("GET", SERVICE + KEY)
    if precheck.status == 200:
        if not _matches(precheck.json().get("d", {})):
            return {"status": "BLOCKED", "reason": "Existing company values conflict with approved target"}
        checkpoint.record(OPERATION, "SKIPPED_EXISTS")
        return {"status": "EXISTS"}
    if precheck.status != 404:
        return {"status": "BLOCKED", "reason": f"Company lookup unknown: HTTP {precheck.status}"}
    if attempt_path.exists() or checkpoint.status(OPERATION) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        return {"status": "BLOCKED", "reason": "Previous company write attempt requires reconciliation"}
    metadata = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        return {"status": "BLOCKED", "reason": f"Metadata GET failed: HTTP {metadata.status}"}
    entity = inspect_creation_metadata(metadata.body, entities=(ENTITY,))[ENTITY]
    mandatory = {name for name, field in entity["fields"].items() if not field["nullable"]}
    if (not entity["metadata_allows_create"] or entity["keys"] != ["Customer", "CompanyCode"]
            or mandatory != {"Customer", "CompanyCode"}):
        return {"status": "BLOCKED", "reason": "Installed company-create contract differs"}
    for name, value in PAYLOAD.items():
        field = entity["fields"].get(name)
        if (not field or field["edm_type"] != "Edm.String" or not field["creatable"]
                or (field["max_length"] and field["max_length"].isdigit()
                    and len(value) > int(field["max_length"]))):
            return {"status": "BLOCKED", "reason": f"Unproven payload field: {name}"}
    token_response = client.request("GET", SERVICE, headers={"X-CSRF-Token": "Fetch"})
    token = token_response.header("X-CSRF-Token")
    if token_response.status != 200 or not token:
        return {"status": "BLOCKED", "reason": f"CSRF preflight failed: HTTP {token_response.status}"}
    checkpoint.before_write(OPERATION)
    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    with attempt_path.open("x", encoding="utf-8") as handle:
        json.dump({"operation": OPERATION, "target": TARGET, "status": "POST_ATTEMPTED",
                   "retry_allowed": False}, handle)
    try:
        response = client.request("POST", SERVICE + ENTITY,
                                  headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                                  body=json.dumps(PAYLOAD).encode("utf-8"))
    except Exception as error:
        checkpoint.record(OPERATION, "AMBIGUOUS", detail=type(error).__name__)
        return {"status": "BLOCKED", "reason": "POST outcome ambiguous; no retry"}
    if response.status not in {200, 201, 204}:
        evidence = response.error_evidence
        attempt_path.write_text(json.dumps({"operation": OPERATION, "target": TARGET,
                                            "status": f"POST_REJECTED_HTTP_{response.status}",
                                            "sap_error": evidence, "retry_allowed": False}) + "\n", encoding="utf-8")
        checkpoint.record(OPERATION, "REJECTED", detail=str(evidence.get("sap_code") if evidence else response.status))
        return {"status": "BLOCKED", "reason": f"POST rejected HTTP {response.status}", "sap_error": evidence}
    try:
        readback = transport_factory(config).request("GET", SERVICE + KEY)
        row = readback.json().get("d", {}) if readback.status == 200 else {}
    except Exception:
        row = {}
    if not _matches(row):
        checkpoint.record(OPERATION, "AMBIGUOUS", detail="independent readback mismatch")
        return {"status": "BLOCKED", "reason": "Independent readback mismatch; no retry"}
    attempt_path.write_text(json.dumps({"operation": OPERATION, "target": TARGET,
                                        "status": "VERIFIED", "retry_allowed": False}) + "\n", encoding="utf-8")
    checkpoint.record(OPERATION, "VERIFIED", detail="1010/400000/0004")
    approval.setdefault("verified_step_states", {})["CUSTOMER_COMPANY_1010"] = "EXISTS"
    approval_path.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "CREATED_AND_VERIFIED"}
