"""One-shot A01 sales-area extension; no tax or FI write is implied."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.customer_bp_root import inspect_creation_metadata
from src.provisioning.execution_policy import ExecutionCheckpoint, target_fingerprint
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
ENTITY = "A_CustomerSalesArea"
KEY = "A_CustomerSalesArea(Customer='1000000115',SalesOrganization='1010',DistributionChannel='10',Division='00')"
OPERATION = "ENSURE_C615_A01_SALES_AREA_1010_10_00"
TARGET = {"logical_id": "C615-A01", "sap_id": "1000000115", "sales_area": "1010/10/00"}
PAYLOAD = {
    "Customer": "1000000115", "SalesOrganization": "1010", "DistributionChannel": "10",
    "Division": "00", "Currency": "EUR", "ShippingCondition": "01",
    "CustomerPricingProcedure": "02", "CustomerAccountAssignmentGroup": "01",
    "IncotermsClassification": "CFR", "IncotermsLocation1": "Bruxelles",
    "CustomerPaymentTerms": "0004",
}


def _matches(row: dict[str, Any]) -> bool:
    return all(row.get(field) == value for field, value in PAYLOAD.items())


def ensure_sales_area_once(
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
            or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
            or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])
            or "CUSTOMER_SALES_AREA_1010_10_00" not in approval.get("approved_scope", [])
            or approval.get("step_authorizations", {}).get("CUSTOMER_SALES_AREA_1010_10_00", {}).get("execute") is not True
            or approval.get("sales_area_approved_payload") != PAYLOAD
            or approval.get("sales_area_target_fingerprint") != target_fingerprint(OPERATION, TARGET, PAYLOAD)
            or mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != "1000000115"
            or approval.get("verified_step_states", {}).get("FLCU01_ROLE") != "EXISTS"):
        raise ValueError("Exact A01 sales-area approval, values or verified mapping missing")
    checkpoint = ExecutionCheckpoint(checkpoint_path, "S4615_CUSTOMER_A01")
    client = transport_factory(config)
    precheck = client.request("GET", SERVICE + KEY)
    if precheck.status == 200:
        row = precheck.json().get("d", {})
        if not _matches(row):
            return {"status": "BLOCKED", "reason": "Existing sales-area values conflict with approved target"}
        checkpoint.record(OPERATION, "SKIPPED_EXISTS")
        return {"status": "EXISTS"}
    if precheck.status != 404:
        return {"status": "BLOCKED", "reason": f"Sales-area lookup unknown: HTTP {precheck.status}"}
    if attempt_path.exists() or checkpoint.status(OPERATION) in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        return {"status": "BLOCKED", "reason": "Prior sales-area write attempt requires reconciliation"}
    metadata = client.request("GET", SERVICE + "$metadata", headers={"Accept": "application/xml"})
    if metadata.status != 200:
        return {"status": "BLOCKED", "reason": f"Metadata GET failed: HTTP {metadata.status}"}
    entity = inspect_creation_metadata(metadata.body, entities=(ENTITY,))[ENTITY]
    mandatory = {name for name, field in entity["fields"].items() if not field["nullable"]}
    if (not entity["metadata_allows_create"]
            or mandatory != {"Customer", "SalesOrganization", "DistributionChannel", "Division"}):
        return {"status": "BLOCKED", "reason": "Installed sales-area create contract differs"}
    for name, value in PAYLOAD.items():
        field = entity["fields"].get(name)
        if (not field or not field["creatable"] or field["edm_type"] != "Edm.String"
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
        error = response.error_evidence
        attempt_path.write_text(json.dumps({"operation": OPERATION, "target": TARGET,
                                            "status": f"POST_REJECTED_HTTP_{response.status}",
                                            "sap_error": error, "retry_allowed": False}) + "\n", encoding="utf-8")
        checkpoint.record(OPERATION, "REJECTED", detail=str(error.get("sap_code") if error else response.status))
        return {"status": "BLOCKED", "reason": f"POST rejected HTTP {response.status}", "sap_error": error}
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
    checkpoint.record(OPERATION, "VERIFIED", detail="1010/10/00")
    approval.setdefault("verified_step_states", {})["CUSTOMER_SALES_AREA_1010_10_00"] = "EXISTS"
    approval_path.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "CREATED_AND_VERIFIED"}
