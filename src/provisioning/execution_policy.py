"""Opt-in Phase 5 training execution gates and resumable write checkpoints.

This module authorizes a *scope*, never an SAP capability.  The selected
backend must still implement an evidenced, fail-closed write contract.
"""

from __future__ import annotations

import json
import os
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MODES = {"AUTONOMOUS_TRAINING", "CONTROLLED_FIRST_WRITE"}
SENSITIVE_SCOPES = {"FI_MM", "TAX", "ORG_CUSTOMIZING", "MATERIAL_LEDGER"}
ROUTINE_SCOPE = "TRAINING_MASTER_DATA"
EXPECTED_ENVIRONMENT = {"system": "A4H", "client": "600", "user": "ABDELJ"}
TERMINAL_WRITE_STATES = {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}


def target_fingerprint(operation: str, target: dict[str, Any], values: dict[str, Any]) -> str:
    payload = json.dumps(
        {"operation": operation, "target": target, "values": values},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class TrainingExecutionPolicy:
    mode: str
    workflow_id: str
    environment: dict[str, str]
    approval: dict[str, Any]
    operation_scopes: dict[str, str]
    route_evidence: dict[str, str]
    sensitive_approvals: dict[str, dict[str, Any]]

    @classmethod
    def from_document(cls, value: dict[str, Any]) -> "TrainingExecutionPolicy":
        if not isinstance(value, dict):
            raise ValueError("Execution policy must be an object")
        policy = cls(
            mode=value.get("mode", ""),
            workflow_id=value.get("workflow_id", ""),
            environment=value.get("environment", {}),
            approval=value.get("approval", {}),
            operation_scopes=value.get("operation_scopes", {}),
            route_evidence=value.get("route_evidence", {}),
            sensitive_approvals=value.get("sensitive_approvals", {}),
        )
        if policy.mode not in MODES or not policy.workflow_id:
            raise ValueError("Invalid Phase 5 execution mode or workflow ID")
        if policy.environment != EXPECTED_ENVIRONMENT:
            raise ValueError("Phase 5 execution is limited to A4H/600/ABDELJ")
        if not all(isinstance(x, dict) for x in (
            policy.approval, policy.operation_scopes, policy.route_evidence,
            policy.sensitive_approvals,
        )):
            raise ValueError("Invalid execution policy mapping")
        return policy

    def authorize(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> None:
        scope = self.operation_scopes.get(operation)
        if scope not in SENSITIVE_SCOPES | {ROUTINE_SCOPE}:
            raise ValueError(f"Operation scope missing or unsupported: {operation}")
        approval = self.approval
        if (approval.get("workflow_id") != self.workflow_id
                or approval.get("environment") != EXPECTED_ENVIRONMENT
                or not approval.get("approved_by")
                or not approval.get("authorization_evidence")
                or operation not in approval.get("operations", [])
                or scope not in approval.get("scopes", [])
                or approval.get("target_fingerprints", {}).get(operation)
                != target_fingerprint(operation, target, values)):
            raise ValueError(f"Scoped workflow approval missing: {operation}")
        if scope in SENSITIVE_SCOPES:
            separate = self.sensitive_approvals.get(operation, {})
            if (separate.get("environment") != EXPECTED_ENVIRONMENT
                    or separate.get("operation") != operation
                    or separate.get("scope") != scope
                    or not separate.get("approved_by")
                    or not separate.get("authorization_evidence")):
                raise ValueError(f"Separate {scope} approval missing: {operation}")
        if not self.route_evidence.get(operation):
            raise ValueError(f"Evidenced write route missing: {operation}")


class ExecutionCheckpoint:
    """Atomic local checkpoint; an attempted write is never silently retried."""

    def __init__(self, path: str | Path, workflow_id: str):
        self.path = Path(path)
        self.workflow_id = workflow_id
        self.state: dict[str, Any] = {"workflow_id": workflow_id, "operations": {}}
        if self.path.exists():
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
            if loaded.get("workflow_id") != workflow_id or not isinstance(loaded.get("operations"), dict):
                raise ValueError("Checkpoint workflow mismatch")
            self.state = loaded

    def status(self, operation: str) -> str | None:
        return self.state["operations"].get(operation, {}).get("status")

    def record(self, operation: str, status: str, *, detail: str = "") -> None:
        if status not in TERMINAL_WRITE_STATES | {"READ_BLOCKED", "SKIPPED_EXISTS"}:
            raise ValueError("Unsupported checkpoint status")
        self.state["operations"][operation] = {"status": status, "detail": detail}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(self.state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, self.path)

    def before_write(self, operation: str) -> None:
        if self.status(operation) in TERMINAL_WRITE_STATES:
            raise ValueError(f"Prior {self.status(operation)} write checkpoint requires reconciliation: {operation}")
        self.record(operation, "ATTEMPTED")
