"""Fail-closed S4615 dependency plan using the existing Phase 5 lifecycle.

The audit is offline evidence for planning, never a substitute for a fresh
LOOKUP immediately before a future SAP write. No write adapter is registered
until its exact API/BAPI/GUI contract has been proven.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .phase5 import Phase5ProvisioningEngine, ProvisioningResult, ROOT
from .customer_bp_root import prepare_bp_root
from .product_creation import prepare_material_bapi, prepare_mm01_fallback
from .s4615_customizing import READ_CONTRACTS, prepare_customizing_contract


CONTRACT_PATH = ROOT / "config/s4615_implementation.json"
OPERATION_ORDER = (
    "S4615_TRAINING_PLANT",
    "S4615_SALES_CHANNEL_PLANT",
    "S4615_PLANT_SHIPPING_POINT",
    "S4615_OVL2_DETERMINATION",
    "S4615_CUSTOMER_BP_ROOT",
    "S4615_CUSTOMER_A01",
    "S4615_PRODUCT_P101",
)
PROTECTED_IDENTITIES = {"1710", "10000287"}
FORBIDDEN_KEYS = {"material_ledger", "global_currency", "t000_mwaer"}


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if (document.get("mode") != "DRY_RUN_DEFAULT"
            or document.get("canonical_immutable") is not True
            or document.get("sap_identity") != {"system": "A4H", "client": "600", "user": "ABDELJ"}):
        raise ValueError("S4615 implementation identity or dry-run contract mismatch")
    operations = document.get("operations")
    if not isinstance(operations, list) or tuple(op.get("id") for op in operations) != OPERATION_ORDER:
        raise ValueError("S4615 operation order/allowlist mismatch")
    seen: set[str] = set()
    for op in operations:
        if (not isinstance(op.get("target"), dict) or not isinstance(op.get("values"), dict)
                or not isinstance(op.get("required_fields"), list)
                or op.get("audit_state") not in {"MISSING", "UNKNOWN"}
                or op.get("write_route", "").startswith("PROVEN")
                or any(key in FORBIDDEN_KEYS for key in op["values"])):
            raise ValueError(f"Unsafe or incomplete S4615 operation: {op.get('id')}")
        if not set(op["required_fields"]).issubset(op["values"]):
            raise ValueError(f"Required fields absent from {op['id']}")
        deps = op.get("depends_on")
        if not isinstance(deps, list) or any(dep not in seen for dep in deps):
            raise ValueError(f"S4615 dependency order invalid: {op['id']}")
        seen.add(op["id"])
    return document


def target_fingerprint(operation: str, target: dict[str, Any], values: dict[str, Any]) -> str:
    body = json.dumps({"operation": operation, "target": target, "values": values}, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def validate_write_approval(op: dict[str, Any], approval: dict[str, Any]) -> None:
    """Require explicit scoped approval; this does not establish a write route."""
    expected = {
        "system": "A4H", "client": "600", "user": "ABDELJ",
        "operation": op["id"], "target_fingerprint": target_fingerprint(op["id"], op["target"], op["values"]),
        "allow_write": True,
    }
    if any(approval.get(key) != value for key, value in expected.items()):
        raise ValueError(f"S4615 write approval does not match exact target: {op['id']}")
    if not approval.get("approved_by") or not approval.get("authorization_evidence"):
        raise ValueError(f"S4615 approver and SAP authorization evidence required: {op['id']}")
    if op["required_approval"] not in approval.get("approval_scopes", []):
        raise ValueError(f"S4615 business/FI-MM approval missing: {op['id']}")


class AuditEvidenceBackend:
    """Offline audit states for dry-run only. Never performs an SAP request."""

    writable = False

    def __init__(self, operations: list[dict[str, Any]]) -> None:
        self.states = {op["id"]: op["audit_state"] for op in operations}

    def lookup(self, operation: str, target: dict[str, Any]) -> str:
        if operation not in self.states:
            raise ValueError(f"S4615 operation is not allowlisted: {operation}")
        return self.states[operation]

    def provision(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("Historical audit evidence cannot authorize a SAP write")

    def readback(self, operation: str, target: dict[str, Any]) -> dict[str, Any] | None:
        return None


def _blocked_value(value: Any) -> bool:
    if value is None or value == "":
        return True
    if isinstance(value, str):
        return "##" in value or value.startswith("ADMIN_CONFIRMATION_REQUIRED")
    return False


def resolved_operations(
    contract: dict[str, Any], decisions: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    overrides = decisions or {}
    if not isinstance(overrides, dict) or not set(overrides).issubset(OPERATION_ORDER):
        raise ValueError("Unrecognized S4615 decision operation")
    resolved = []
    selected_plant = None
    for original in contract["operations"]:
        op = {**original, "target": dict(original["target"]), "values": dict(original["values"])}
        updates = overrides.get(op["id"], {})
        if not isinstance(updates, dict) or not set(updates).issubset(op["values"]):
            raise ValueError(f"Unrecognized S4615 decision field: {op['id']}")
        if any(key in FORBIDDEN_KEYS for key in updates):
            raise ValueError("Material Ledger and global currency changes are prohibited")
        op["values"].update(updates)
        if op["id"] == OPERATION_ORDER[0]:
            selected_plant = op["values"]["plant"]
        elif selected_plant is not None and "plant" in op["values"]:
            if op["values"]["plant"] is None:
                op["values"]["plant"] = selected_plant
            elif op["values"]["plant"] != selected_plant:
                raise ValueError(f"Plant differs from the approved training plant: {op['id']}")
        if op["values"].get("plant") in PROTECTED_IDENTITIES or op["values"].get("logical_id") in PROTECTED_IDENTITIES:
            raise ValueError("Protected cross-company/product identity cannot be a S4615 training target")
        for key, expected in op["target"].items():
            if expected is None:
                op["target"][key] = op["values"].get(key)
            elif key in op["values"] and op["values"][key] != expected:
                raise ValueError(f"Fixed S4615 target field cannot change: {op['id']}.{key}")
        resolved.append(op)
    return resolved


def build_dry_run(
    *, contract_path: Path = CONTRACT_PATH, decisions: dict[str, dict[str, Any]] | None = None,
    approvals: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    contract = load_contract(contract_path)
    operations = resolved_operations(contract, decisions)
    if approvals is not None and (not isinstance(approvals, dict) or not set(approvals).issubset(OPERATION_ORDER)):
        raise ValueError("Unrecognized S4615 approval operation")
    merged = {op["id"]: op["values"] for op in operations}

    backend = AuditEvidenceBackend(operations)
    engine = Phase5ProvisioningEngine(backend=backend, decisions=merged, execute=False)
    results: dict[str, ProvisioningResult] = {}
    steps = []
    for op in operations:
        name = op["id"]
        target = op["target"]
        result = engine.ensure_operation(
            name, target, tuple(op["required_fields"]),
            dependencies=[results[dep] for dep in op["depends_on"]],
        )
        results[name] = result
        blockers = list(result.blockers)
        missing_fields = [field for field in op["required_fields"] if _blocked_value(merged[name].get(field))]
        approval_error = "Explicit scoped approval is required"
        if approvals and name in approvals:
            try:
                validate_write_approval(op, approvals[name])
                approval_error = ""
            except ValueError as error:
                approval_error = str(error)
        for field in op["required_fields"]:
            if _blocked_value(merged[name].get(field)) and not any(
                item["code"] == "MISSING_DECISION" and item["detail"] == field for item in blockers
            ):
                blockers.append({"code": "MISSING_DECISION", "detail": field})
        blockers.extend([
            {"code": "LIVE_LOOKUP_REQUIRED", "detail": "Historical audit is not a write precheck"},
            {"code": "WRITE_CONTRACT_UNPROVEN", "detail": op["write_route"]},
        ])
        if approval_error:
            blockers.append({"code": "APPROVAL_REQUIRED", "detail": approval_error})
        step = result.as_dict()
        if name in READ_CONTRACTS:
            adapter = prepare_customizing_contract(name, {**target, **merged[name]})
        elif name == "S4615_CUSTOMER_BP_ROOT":
            adapter = prepare_bp_root(merged[name], metadata_xml=None)
        elif name == "S4615_PRODUCT_P101":
            adapter = {
                "bapi": prepare_material_bapi(merged[name]),
                "gui_fallback": prepare_mm01_fallback(),
            }
        else:
            adapter = {"interface": "API_BUSINESS_PARTNER", "status": "BLOCKED",
                       "write_route_ready": False,
                       "missing_evidence": ["generated BP ID binding", "sequential address/role/tax contracts"]}
        step.update({
            "status": "BLOCKED", "blockers": blockers, "source_evidence": op["read_evidence"],
            "preferred_interface": op["preferred_interface"],
            "depends_on": op["depends_on"], "audit_state_only": op["audit_state"],
            "target_fingerprint": target_fingerprint(name, target, merged[name]),
            "adapter": adapter,
            "readiness": {
                "DATA_READY": not missing_fields,
                "WRITE_ROUTE_READY": False,
                "EXECUTION_AUTHORIZED": not approval_error,
            },
        })
        if name == "S4615_CUSTOMER_BP_ROOT":
            evidence = op.get("sap_authorization_evidence") or {}
            identity = contract["sap_identity"]
            matching_identity = all(evidence.get(key) == identity[key] for key in ("system", "client", "user"))
            strong_profile_evidence = (
                matching_identity
                and evidence.get("source") == "USER_REPORTED_SU01D_PROFILES"
                and {"SAP_ALL", "SAP_SYSTEM"}.issubset(evidence.get("profiles") or [])
            )
            step["first_write_readiness"] = {
                "DATA_READY": not missing_fields,
                "SAP_AUTHORIZATION_PROFILE_EVIDENCED": strong_profile_evidence,
                "API_POST_SUCCESS_PROVEN": evidence.get("api_post_success_proven") is True,
                "CUSTOMER_MASTER_OWNER_APPROVED": not approval_error,
                "WRITE_ROUTE_READY": False,
                "EXECUTION_AUTHORIZED": False,
                "eligible_for_post": False,
                "missing_gate": "CUSTOMER_MASTER_OWNER_APPROVAL" if approval_error else "WRITE_ROUTE_UNPROVEN",
            }
        steps.append(step)
    return {"mode": "DRY_RUN", "status": "BLOCKED", "sap_calls": 0, "sap_writes": 0,
            "canonical_targets_immutable": True, "steps": steps}
