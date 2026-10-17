from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from jsonschema import Draft202012Validator

from src.validation.jsonschema import validate_object

from .contracts import ROOT, binding_schema, mapping_contracts, payload_schemas
from .core import map_canonical_object
from .errors import PayloadValidationError

RUNTIME_STATUSES = frozenset({"EXECUTION_READY", "RUNTIME_BINDING_REQUIRED", "BLOCKED"})


def _issue(code: str, path: str, message: str) -> dict:
    return {"code": code, "path": path, "message": message}


def _values_at(data: Any, path: str) -> list[Any]:
    """Return values for a canonical data path containing optional [] segments."""
    values = [data]
    for segment in path.split("."):
        is_array = segment.endswith("[]")
        key = segment[:-2] if is_array else segment
        next_values = []
        for value in values:
            if not isinstance(value, dict) or key not in value:
                continue
            child = value[key]
            if is_array:
                if isinstance(child, list):
                    next_values.extend(child)
                else:
                    next_values.append(child)
            else:
                next_values.append(child)
        values = next_values
    return values


def _populated(values: list[Any]) -> bool:
    return any(value not in (None, "", [], {}) for value in values)


def _schema_issues(schema: dict, value: Any, code: str, prefix: str) -> list[dict]:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    return [
        _issue(
            code,
            ".".join([prefix, *map(str, error.absolute_path)]).rstrip("."),
            error.message,
        )
        for error in errors
    ]


def validate_payload_body(object_type: str, body: dict, *, raise_on_error: bool = False) -> list[dict]:
    """Validate one mapper body against its strict local object-specific schema."""
    document = payload_schemas()
    if object_type not in document["$defs"]:
        issues = [_issue(
            "PAYLOAD_SCHEMA_NOT_FOUND", "body", f"No local payload schema exists for {object_type}."
        )]
    else:
        schema = {
            "$schema": document["$schema"],
            "$ref": f"#/$defs/{object_type}",
            "$defs": document["$defs"],
        }
        issues = _schema_issues(schema, body, "PAYLOAD_SCHEMA_INVALID", "body")
    if issues and raise_on_error:
        raise PayloadValidationError(json.dumps(issues, sort_keys=True, ensure_ascii=False))
    return issues


def validate_runtime_contract(
    obj: dict,
    *,
    object_index: dict[str, dict] | None = None,
    structural_fixture: bool = False,
    raise_on_blocked: bool = False,
) -> dict:
    """Map and strictly validate one object against the local Phase 2C contracts.

    This is offline validation only. A valid local payload is not evidence that a
    live service exposes the same metadata or permits the operation.
    """
    mapped = map_canonical_object(obj, structural_fixture=structural_fixture)
    object_type = obj["object_type"]
    contract = mapping_contracts()["objects"][object_type]
    issues = []

    for error in validate_object(ROOT, obj):
        issues.append(_issue("CANONICAL_SCHEMA_INVALID", error["path"], error["message"]))

    for index, placeholder in enumerate(obj.get("placeholders", [])):
        if placeholder.get("status") == "UNRESOLVED":
            issues.append(_issue(
                "UNRESOLVED_PLACEHOLDER",
                f"placeholders.{index}",
                f"Unresolved placeholder {placeholder.get('raw')!r} cannot enter a writable payload.",
            ))

    for index, dependency in enumerate(obj.get("dependencies", [])):
        if dependency.get("critical") and dependency.get("status") != "RESOLVED":
            issues.append(_issue(
                "UNRESOLVED_CRITICAL_DEPENDENCY",
                f"dependencies.{index}",
                f"Critical dependency to {dependency.get('target_type')} is unresolved.",
            ))

    for path in contract["mandatory_paths"]:
        if not _populated(_values_at(obj["data"], path)):
            issues.append(_issue(
                "MISSING_MANDATORY_FIELD", f"data.{path}", "Mandatory local mapping value is absent."
            ))

    for path, field_contract in contract["fields"].items():
        if field_contract["disposition"] == "UNSUPPORTED" and _populated(_values_at(obj["data"], path)):
            issues.append(_issue(
                "UNSUPPORTED_FIELD_POPULATED",
                f"data.{path}",
                field_contract.get("reason", "No local writable target field is defined."),
            ))

    for missing_path in mapped["missing_required_mappings"]:
        issues.append(_issue(
            "MISSING_REQUIRED_MAPPING", missing_path, "Phase 2B mapper could not populate a required target field."
        ))

    for index, payload in enumerate(mapped["payloads"]):
        body_issues = validate_payload_body(object_type, payload.get("body"))
        for item in body_issues:
            item = dict(item)
            item["path"] = item["path"].replace("body", f"payloads.{index}.body", 1)
            issues.append(item)
        if mapped["protocol"] == "BAPI":
            plant_context = payload.get("plant_context")
            if plant_context is not None and not isinstance(plant_context, str):
                issues.append(_issue(
                    "PAYLOAD_SCHEMA_INVALID", f"payloads.{index}.plant_context",
                    "Plant context must be a string or null.",
                ))

    expected_bindings = {
        (item["relation"], item["target_type"], item["sap_field"])
        for item in contract["runtime_bindings"]
    }
    for index, binding in enumerate(mapped["runtime_bindings"]):
        issues.extend(_schema_issues(
            binding_schema(), binding, "BINDING_SCHEMA_INVALID", f"runtime_bindings.{index}"
        ))
        signature = (binding.get("relation"), binding.get("target_type"), binding.get("sap_field"))
        if signature not in expected_bindings:
            issues.append(_issue(
                "UNSUPPORTED_RUNTIME_BINDING", f"runtime_bindings.{index}",
                f"Binding {signature!r} is not declared by the local mapping contract.",
            ))
        target_id = binding.get("target_object_id")
        if object_index is not None and target_id:
            target = object_index.get(target_id)
            if target is None:
                issues.append(_issue(
                    "BINDING_TARGET_NOT_FOUND", f"runtime_bindings.{index}.target_object_id",
                    f"Canonical target {target_id!r} is not present in the supplied object index.",
                ))
            elif target.get("object_type") != binding.get("target_type"):
                issues.append(_issue(
                    "BINDING_TARGET_TYPE_MISMATCH", f"runtime_bindings.{index}.target_type",
                    f"Target is {target.get('object_type')}, expected {binding.get('target_type')}.",
                ))

    # A document with no concrete reference must expose one of its declared bindings.
    if contract["runtime_bindings"]:
        body_has_reference = any(
            payload.get("body", {}).get("ReferenceSDDocument") for payload in mapped["payloads"]
        )
        if not body_has_reference and not mapped["runtime_bindings"]:
            issues.append(_issue(
                "MISSING_RUNTIME_BINDING", "runtime_bindings",
                "Neither a concrete reference document nor a declared runtime binding is present.",
            ))

    issues = sorted(issues, key=lambda item: (item["code"], item["path"], item["message"]))
    if obj["readiness_status"] == "BLOCKED" or issues:
        runtime_status = "BLOCKED"
    elif mapped["runtime_bindings"] or mapped["deferred_values"]:
        runtime_status = "RUNTIME_BINDING_REQUIRED"
    else:
        runtime_status = "EXECUTION_READY"

    result = deepcopy(mapped)
    result["runtime_status"] = runtime_status
    result["execution_ready"] = runtime_status == "EXECUTION_READY"
    result["contract_validation"] = {
        "contract_version": mapping_contracts()["contract_version"],
        "local_contract_valid": not issues,
        "live_sap_metadata_validated": (
            contract.get("live_metadata_validation", {}).get("status") == "VALIDATED"
        ),
        "issues": issues,
    }
    json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False)
    if runtime_status == "BLOCKED" and raise_on_blocked:
        raise PayloadValidationError(json.dumps(issues, sort_keys=True, ensure_ascii=False))
    return result
