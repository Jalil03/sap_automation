"""Idempotent Phase 5 provisioning orchestration.

The engine owns ordering, value validation, check-before-create, readback and
fail-closed behavior. SAP-specific write mechanics are supplied by an explicit
backend; the repository default is evidence-only and cannot write.
"""

from __future__ import annotations

import importlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy


ROOT = Path(__file__).resolve().parents[2]
PREPARE_PATH = ROOT / "data/provisioning/phase5_prepare_1010.json"
SOURCE_ANALYSIS_PATH = ROOT / "data/provisioning/phase5_source_analysis_1010.json"
S4615_SEED_PATH = ROOT / "config/s4615_training_seed.yaml"

ALLOWED_SEED_PROVENANCE = {
    "BOOK_CONFIRMED", "PROJECT_DEFAULT", "TECHNICAL_TEMPLATE", "SAP_CONFIRMED",
}
ALLOWED_DEFERRED_RESOLUTIONS = {
    "INHERIT_ONLY_IF_SAP_REQUIRED",
    "INHERIT_MANDATORY_FROM_TECHNICAL_TEMPLATE",
    "DERIVE_1010_COMPATIBLE_DEPENDENCY",
}

COMMON_ORDER = (
    "COMPANY_CODE_1010",
    "SALES_ORGANIZATION_1010",
    "SALES_ORG_1010_TO_COMPANY_CODE_1010",
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
    "DIVISION_00_TO_SALES_ORG_1010",
)

DEFERRED_ASSIGNMENT_OPERATIONS = {
    "SALES_ORG_1010_TO_COMPANY_CODE_1010",
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
    "DIVISION_00_TO_SALES_ORG_1010",
}

REQUIRED_DECISION_FIELDS = {
    "COMPANY_CODE_1010": (
        "creation_strategy", "company_name", "city", "country", "currency", "language",
    ),
    "SALES_ORGANIZATION_1010": (
        "creation_strategy", "description", "statistics_currency",
    ),
    "CUSTOMER_C615_D00": (
        "grouping", "name", "roles", "addresses", "reconciliation_account",
        "payment_terms", "currency", "shipping_conditions", "delivering_plant",
        "incoterms", "incoterms_location", "account_assignment_group",
        "customer_pricing_procedure", "tax_classifications", "partner_functions",
    ),
    "PRODUCT_P615_400": (
        "description", "material_type", "industry_sector", "base_unit", "plants",
        "delivering_plant", "item_category_group", "tax_classification",
        "availability_check", "alternative_units",
    ),
}

# These values must be concrete before any backend may write.  Fields absent
# from this map may be explicitly set to null when SAP confirms they are
# optional for the selected creation path.
MANDATORY_NON_NULL_FIELDS = {
    "COMPANY_CODE_1010": set(REQUIRED_DECISION_FIELDS["COMPANY_CODE_1010"]),
    "SALES_ORGANIZATION_1010": {
        "creation_strategy", "description", "statistics_currency",
    },
    "CUSTOMER_C615_D00": set(REQUIRED_DECISION_FIELDS["CUSTOMER_C615_D00"]),
    "PRODUCT_P615_400": set(REQUIRED_DECISION_FIELDS["PRODUCT_P615_400"]),
}


class ProvisioningBackend(Protocol):
    """Backend contract. Implementations must never retry ambiguous writes."""

    writable: bool

    def lookup(self, operation: str, target: dict[str, Any]) -> str: ...
    def provision(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]: ...
    def readback(self, operation: str, target: dict[str, Any]) -> dict[str, Any] | None: ...


class EvidenceBackend:
    """Repository-evidence backend used by default; it performs no SAP calls."""

    writable = False

    def __init__(self) -> None:
        self.states = {
            "COMPANY_CODE_1010": "MISSING",
            "SALES_ORGANIZATION_1010": "MISSING",
            "SALES_ORG_1010_TO_COMPANY_CODE_1010": "UNKNOWN",
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": "UNKNOWN",
            "DIVISION_00_TO_SALES_ORG_1010": "UNKNOWN",
            "CUSTOMER_C615_D00": "MISSING",
            "PRODUCT_P615_400": "MISSING",
        }

    def lookup(self, operation: str, target: dict[str, Any]) -> str:
        return self.states.get(operation, "UNKNOWN")

    def provision(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("EvidenceBackend is READ-only")

    def readback(self, operation: str, target: dict[str, Any]) -> dict[str, Any] | None:
        return None


class RecoverableReadError(RuntimeError):
    """A backend-confirmed transient READ failure; no write was attempted."""


@dataclass
class ProvisioningResult:
    operation: str
    target: dict[str, Any]
    before_state: str
    action: str
    status: str
    checks: list[str] = field(default_factory=list)
    blockers: list[dict[str, str]] = field(default_factory=list)
    readback: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_decisions(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Decision file must be a JSON object")
    return value


def load_seed(path: str | Path = S4615_SEED_PATH) -> dict[str, Any]:
    """Load validated Phase 5 decisions from the controlled S4615 seed."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        seed = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ModuleNotFoundError as error:
            raise ValueError("Non-JSON YAML seed requires PyYAML") from error
        seed = yaml.safe_load(text)
    if not isinstance(seed, dict) or seed.get("canonical_immutable") is not True:
        raise ValueError("S4615 seed must declare canonical_immutable: true")
    if seed.get("mode") != "DRY_RUN_DEFAULT":
        raise ValueError("S4615 seed must default to DRY_RUN")
    operations = seed.get("operations")
    if not isinstance(operations, dict):
        raise ValueError("S4615 seed operations must be a mapping")
    decisions: dict[str, dict[str, Any]] = {}
    for operation, contract in operations.items():
        if operation not in {*COMMON_ORDER, "CUSTOMER_C615_D00", "PRODUCT_P615_400"}:
            raise ValueError(f"Unsupported S4615 seed operation: {operation}")
        if not isinstance(contract, dict) or not isinstance(contract.get("fields"), dict):
            raise ValueError(f"Invalid S4615 seed contract: {operation}")
        decision: dict[str, Any] = {}
        field_resolutions: dict[str, str] = {}
        for field_name, field_contract in contract["fields"].items():
            if not isinstance(field_contract, dict) or "value" not in field_contract:
                raise ValueError(f"Invalid seed field contract: {operation}.{field_name}")
            provenance = field_contract.get("provenance")
            if provenance not in ALLOWED_SEED_PROVENANCE:
                raise ValueError(f"Invalid seed provenance: {operation}.{field_name}")
            decision[field_name] = field_contract["value"]
            if field_contract.get("resolution"):
                resolution = str(field_contract["resolution"])
                if resolution not in ALLOWED_DEFERRED_RESOLUTIONS:
                    raise ValueError(f"Invalid seed resolution: {operation}.{field_name}")
                field_resolutions[field_name] = resolution
        if field_resolutions:
            decision["_field_resolutions"] = field_resolutions
        decisions[operation] = decision
    return decisions


def load_backend(factory_spec: str | None) -> ProvisioningBackend:
    if not factory_spec:
        return EvidenceBackend()
    if ":" not in factory_spec:
        raise ValueError("Backend factory must use module:function syntax")
    module_name, function_name = factory_spec.split(":", 1)
    factory = getattr(importlib.import_module(module_name), function_name)
    backend = factory()
    for member in ("lookup", "provision", "readback"):
        if not callable(getattr(backend, member, None)):
            raise ValueError(f"Provisioning backend lacks {member}()")
    if not hasattr(backend, "writable"):
        raise ValueError("Provisioning backend lacks writable safety declaration")
    return backend


def _missing(operation: str, decision: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    mandatory_non_null = MANDATORY_NON_NULL_FIELDS.get(operation, set())
    deferred = decision.get("_field_resolutions") or {}
    return [
        field
        for field in required
        if field not in decision
        or decision[field] == ""
        or (
            field in mandatory_non_null
            and decision[field] is None
            and deferred.get(field) not in ALLOWED_DEFERRED_RESOLUTIONS
        )
    ]


def _decision_errors(operation: str, decision: dict[str, Any]) -> list[str]:
    errors = []
    deferred = decision.get("_field_resolutions") or {}
    if operation == "COMPANY_CODE_1010":
        strategy = decision.get("creation_strategy")
        if strategy not in {"MANUAL_CREATE", "TECHNICAL_TEMPLATE_COPY"}:
            errors.append("unsupported company-code creation_strategy")
        if strategy == "TECHNICAL_TEMPLATE_COPY" and not decision.get("technical_template"):
            errors.append("technical_template is required for TECHNICAL_TEMPLATE_COPY")
    if operation == "SALES_ORGANIZATION_1010":
        strategy = decision.get("creation_strategy")
        if strategy not in {"MANUAL_CREATE", "TECHNICAL_TEMPLATE_COPY"}:
            errors.append("unsupported sales organization creation_strategy")
        if strategy == "TECHNICAL_TEMPLATE_COPY" and not decision.get("technical_template"):
            errors.append("technical_template is required for TECHNICAL_TEMPLATE_COPY")
    if operation == "CUSTOMER_C615_D00":
        strategy = decision.get("creation_strategy", "MANUAL_CREATE")
        if strategy not in {"MANUAL_CREATE", "TECHNICAL_TEMPLATE_COPY"}:
            errors.append("unsupported customer creation_strategy")
        if strategy == "TECHNICAL_TEMPLATE_COPY" and not decision.get("technical_template"):
            errors.append("customer technical_template is required")
        for field in ("roles", "addresses"):
            if field not in deferred and (
                not isinstance(decision.get(field), list) or not decision[field]
            ):
                errors.append(f"{field} must be a non-empty explicitly supplied list")
    if operation == "PRODUCT_P615_400":
        strategy = decision.get("creation_strategy", "MANUAL_CREATE")
        if strategy not in {"MANUAL_CREATE", "TECHNICAL_TEMPLATE_COPY"}:
            errors.append("unsupported product creation_strategy")
        if strategy == "TECHNICAL_TEMPLATE_COPY" and not decision.get("technical_template"):
            errors.append("product technical_template is required")
        if "plants" not in deferred and (
            not isinstance(decision.get("plants"), list) or not decision["plants"]
        ):
            errors.append("plants must be a non-empty explicitly supplied list")
        alternative_units = decision.get("alternative_units")
        has_pc = decision.get("base_unit") == "PC" or (
            isinstance(alternative_units, list) and "PC" in alternative_units
        )
        if not has_pc:
            errors.append("PC must be explicitly supplied as base_unit or alternative unit")
    return errors


class Phase5ProvisioningEngine:
    def __init__(
        self,
        *,
        backend: ProvisioningBackend,
        decisions: dict[str, Any] | None = None,
        execute: bool = False,
        execution_policy: TrainingExecutionPolicy | None = None,
        checkpoint: ExecutionCheckpoint | None = None,
    ) -> None:
        self.backend = backend
        self.decisions = decisions or {}
        self.execute = execute
        self.execution_policy = execution_policy
        self.checkpoint = checkpoint
        if execute and not backend.writable:
            raise ValueError("--execute requires an explicitly writable provisioning backend")
        if execution_policy is not None and checkpoint is not None and checkpoint.workflow_id != execution_policy.workflow_id:
            raise ValueError("Execution policy and checkpoint workflow mismatch")

    @staticmethod
    def _targets() -> dict[str, dict[str, Any]]:
        return {
            "COMPANY_CODE_1010": {"company_code": "1010"},
            "SALES_ORGANIZATION_1010": {"sales_organization": "1010"},
            "SALES_ORG_1010_TO_COMPANY_CODE_1010": {
                "sales_organization": "1010", "company_code": "1010",
            },
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": {
                "distribution_channel": "10", "sales_organization": "1010",
            },
            "DIVISION_00_TO_SALES_ORG_1010": {
                "sales_division": "00", "sales_organization": "1010",
            },
            "CUSTOMER_C615_D00": {
                "partner_id": "C615-D00", "company_code": "1010", "sales_area": "1010/10/00",
            },
            "PRODUCT_P615_400": {
                "material_id": "P615-400", "sales_organization": "1010",
                "distribution_channel": "10", "unit": "PC",
            },
        }

    def _ensure(
        self,
        operation: str,
        *,
        dependencies: list[ProvisioningResult] | None = None,
        target_override: dict[str, Any] | None = None,
        required_override: tuple[str, ...] | None = None,
    ) -> ProvisioningResult:
        target = target_override if target_override is not None else self._targets()[operation]
        try:
            before = self.backend.lookup(operation, target)
        except RecoverableReadError:
            # One retry is safe only when the backend certifies that this was
            # a read-only failure. Never retry provision() automatically.
            try:
                before = self.backend.lookup(operation, target)
            except Exception as error:
                return ProvisioningResult(
                    operation, target, "UNKNOWN", "STOP", "BLOCKED_LIVE_READ_REQUIRED",
                    blockers=[{"code": "LOOKUP_FAILED", "detail": str(error)}],
                )
        except Exception as error:
            if self.execution_policy is None:
                raise
            return ProvisioningResult(
                operation, target, "UNKNOWN", "STOP", "BLOCKED_LIVE_READ_REQUIRED",
                blockers=[{"code": "LOOKUP_FAILED", "detail": str(error)}],
            )
        if before not in {"EXISTS", "MISSING", "UNKNOWN"}:
            return ProvisioningResult(
                operation, target, "UNKNOWN", "STOP", "BLOCKED",
                blockers=[{"code": "INVALID_LOOKUP_STATE", "detail": str(before)}],
            )
        if before == "EXISTS":
            if self.execute and self.checkpoint is not None:
                self.checkpoint.record(operation, "SKIPPED_EXISTS")
            return ProvisioningResult(operation, target, before, "SKIP", "SKIPPED_EXISTS", checks=["check_before_create"])
        if before == "UNKNOWN" and self.execute:
            return ProvisioningResult(
                operation, target, before, "READ_CHECK_REQUIRED",
                "BLOCKED_LIVE_READ_REQUIRED",
                checks=["check_before_create"],
                blockers=[{
                    "code": "EXISTENCE_UNKNOWN",
                    "detail": "A live read must prove EXISTS or MISSING before any write.",
                }],
            )
        decision = self.decisions.get(operation, {})
        required = required_override if required_override is not None else REQUIRED_DECISION_FIELDS.get(operation, ())
        missing = _missing(operation, decision, required)
        if required_override is not None:
            missing = list(dict.fromkeys(missing + [
                name for name in required
                if decision.get(name) is None or (
                    isinstance(decision.get(name), str)
                    and ("##" in decision[name] or decision[name].startswith("ADMIN_CONFIRMATION_REQUIRED"))
                )
            ]))
        if before == "MISSING" and missing:
            return ProvisioningResult(
                operation, target, before, "PREPARE", "BLOCKED_NEEDS_VALUE",
                checks=["check_before_create"],
                blockers=[{"code": "MISSING_DECISION", "detail": field} for field in missing],
            )
        decision_errors = _decision_errors(operation, decision)
        if before == "MISSING" and decision_errors:
            return ProvisioningResult(
                operation, target, before, "PREPARE", "BLOCKED_INVALID_DECISION",
                checks=["check_before_create", "values_complete"],
                blockers=[{"code": "INVALID_DECISION", "detail": error} for error in decision_errors],
            )
        satisfied_dependencies = {"SKIPPED_EXISTS", "PROVISIONED_VERIFIED"}
        if not self.execute:
            satisfied_dependencies.update({
                "WOULD_PROVISION", "DEFERRED_READ_CHECK",
                "WOULD_PROVISION_AFTER_COMMON_ENV",
            })
        blocked_dependencies = [
            dependency.operation
            for dependency in dependencies or []
            if dependency.status not in satisfied_dependencies
        ]
        if blocked_dependencies:
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_DEPENDENCY",
                checks=["check_before_create"],
                blockers=[{
                    "code": "DEPENDENCY_BLOCKED",
                    "detail": ", ".join(blocked_dependencies),
                }],
            )
        if before == "UNKNOWN":
            if (
                not self.execute
                and operation in DEFERRED_ASSIGNMENT_OPERATIONS
                and dependencies
            ):
                return ProvisioningResult(
                    operation, target, before, "WOULD_ENSURE", "DEFERRED_READ_CHECK",
                    checks=[
                        "parents_scheduled_in_same_run",
                        "execute_live_read_required",
                        "exists_then_skip",
                        "missing_then_create",
                        "readback_required_after_create",
                    ],
                )
            return ProvisioningResult(
                operation, target, before, "READ_CHECK_REQUIRED", "BLOCKED_LIVE_READ_REQUIRED",
                checks=["check_before_create"],
                blockers=[{
                    "code": "EXISTENCE_UNKNOWN",
                    "detail": "A live read must prove EXISTS or MISSING before any write.",
                }],
            )

        if not self.execute:
            planned_status = (
                "WOULD_PROVISION_AFTER_COMMON_ENV"
                if operation in {"CUSTOMER_C615_D00", "PRODUCT_P615_400"}
                and dependencies
                else "WOULD_PROVISION"
            )
            return ProvisioningResult(
                operation, target, before, "PROVISION", planned_status,
                checks=[
                    "check_before_create", "prepare", "validate_values",
                    "write_requires_execute", "readback_required_after_write",
                ],
            )

        deferred = decision.get("_field_resolutions") or {}
        write_values = {
            key: value
            for key, value in decision.items()
            if not key.startswith("_") and not (value is None and key in deferred)
        }
        if self.execution_policy is not None:
            try:
                self.execution_policy.authorize(operation, target, write_values)
                if self.checkpoint is None:
                    raise ValueError("Autonomous execution requires a durable checkpoint")
                self.checkpoint.before_write(operation)
            except ValueError as error:
                return ProvisioningResult(
                    operation, target, before, "STOP", "BLOCKED_APPROVAL_OR_ROUTE",
                    checks=["check_before_create", "write_not_attempted"],
                    blockers=[{"code": "EXECUTION_GATE", "detail": str(error)}],
                )
        try:
            write_result = self.backend.provision(operation, target, write_values)
        except Exception as error:
            if self.execution_policy is None:
                raise
            if self.checkpoint is not None:
                self.checkpoint.record(operation, "AMBIGUOUS", detail=type(error).__name__)
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_AMBIGUOUS_WRITE",
                checks=["check_before_create", "write_attempted", "no_automatic_retry"],
                blockers=[{"code": "WRITE_OUTCOME_UNKNOWN", "detail": str(error)}],
            )
        if not isinstance(write_result, dict):
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_WRITE_RESPONSE",
                checks=["check_before_create", "write_attempted", "invalid_write_response"],
                blockers=[{
                    "code": "INVALID_WRITE_RESPONSE",
                    "detail": "Backend provision() must return a structured result.",
                }],
            )
        if write_result.get("provisioning_blocked"):
            if self.checkpoint is not None:
                self.checkpoint.record(operation, "READ_BLOCKED", detail="backend rejected write before attempt")
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_UNSUPPORTED_PROVISIONING",
                checks=["check_before_create", "write_not_attempted", "gui_contract_missing"],
                blockers=[{
                    "code": "GUI_WRITE_CONTRACT_INCOMPLETE",
                    "detail": str(write_result.get("reason") or operation),
                }],
            )
        if write_result.get("transport_request"):
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_TRANSPORT_REQUIRED",
                checks=["check_before_create", "write_attempted", "transport_not_released"],
                blockers=[{
                    "code": "TRANSPORT_REQUEST",
                    "detail": "Transport handling and release are never automatic.",
                }],
            )
        if write_result.get("unexpected_popup"):
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_UNEXPECTED_POPUP",
                checks=["check_before_create", "write_attempted", "unexpected_popup"],
                blockers=[{
                    "code": "UNEXPECTED_POPUP",
                    "detail": "Provisioning stopped before any retry.",
                }],
            )
        if write_result.get("ambiguous_save"):
            if self.checkpoint is not None:
                self.checkpoint.record(operation, "AMBIGUOUS", detail="save outcome unknown")
            return ProvisioningResult(
                operation, target, before, "STOP", "BLOCKED_AMBIGUOUS_SAVE",
                checks=["check_before_create", "write_attempted", "no_automatic_retry"],
                blockers=[{
                    "code": "AMBIGUOUS_SAVE",
                    "detail": "SAVE outcome is ambiguous; no retry or readback was attempted.",
                }],
            )
        readback = self.backend.readback(operation, target)
        if not readback:
            if self.checkpoint is not None:
                self.checkpoint.record(operation, "AMBIGUOUS", detail="independent readback failed")
            return ProvisioningResult(
                operation, target, before, "PROVISION", "BLOCKED_READBACK",
                checks=["check_before_create", "write_attempted", "readback_failed"],
                blockers=[{"code": "READBACK_FAILED", "detail": operation}],
            )
        if self.checkpoint is not None:
            self.checkpoint.record(operation, "VERIFIED")
        return ProvisioningResult(
            operation, target, before, "PROVISION", "PROVISIONED_VERIFIED",
            checks=[
                "check_before_create", "prepare", "validate_values",
                "write_once", "readback_verified",
            ],
            readback=readback,
        )

    def ensure_operation(
        self,
        operation: str,
        target: dict[str, Any],
        required_fields: tuple[str, ...],
        *,
        dependencies: list[ProvisioningResult] | None = None,
    ) -> ProvisioningResult:
        """Use the same Phase 5 lifecycle for an explicitly specified operation."""
        return self._ensure(
            operation, dependencies=dependencies,
            target_override=target, required_override=required_fields,
        )

    def ensure_company_code(self) -> ProvisioningResult:
        return self._ensure("COMPANY_CODE_1010")

    def ensure_sales_org(self, company: ProvisioningResult) -> ProvisioningResult:
        return self._ensure("SALES_ORGANIZATION_1010", dependencies=[company])

    def ensure_sales_org_company_assignment(
        self, company: ProvisioningResult, sales_org: ProvisioningResult
    ) -> ProvisioningResult:
        return self._ensure(
            "SALES_ORG_1010_TO_COMPANY_CODE_1010", dependencies=[company, sales_org]
        )

    def ensure_distribution_channel_assignment(
        self, sales_org: ProvisioningResult
    ) -> ProvisioningResult:
        return self._ensure(
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010", dependencies=[sales_org]
        )

    def ensure_division_assignment(
        self, sales_org: ProvisioningResult, channel: ProvisioningResult
    ) -> ProvisioningResult:
        return self._ensure(
            "DIVISION_00_TO_SALES_ORG_1010", dependencies=[sales_org, channel]
        )

    def ensure_common_environment(self) -> list[ProvisioningResult]:
        company = self.ensure_company_code()
        sales_org = self.ensure_sales_org(company)
        company_assignment = self.ensure_sales_org_company_assignment(company, sales_org)
        channel = self.ensure_distribution_channel_assignment(sales_org)
        division = self.ensure_division_assignment(sales_org, channel)
        return [company, sales_org, company_assignment, channel, division]

    def ensure_customer(self, common: list[ProvisioningResult]) -> ProvisioningResult:
        return self._ensure("CUSTOMER_C615_D00", dependencies=common)

    def ensure_product(self, common: list[ProvisioningResult]) -> ProvisioningResult:
        return self._ensure("PRODUCT_P615_400", dependencies=common)

    def plan(self, *, include_book_data: bool = False) -> dict[str, Any]:
        common = self.ensure_common_environment()
        book = []
        if include_book_data:
            book = [self.ensure_customer(common), self.ensure_product(common)]
        results = common + book
        blockers = [
            {"operation": result.operation, **blocker}
            for result in results
            for blocker in result.blockers
        ]
        return {
            "mode": "EXECUTE" if self.execute else "DRY_RUN",
            "canonical_targets_immutable": True,
            "results": [result.as_dict() for result in results],
            "blockers": blockers,
            "status": "READY" if not blockers else "BLOCKED",
        }
