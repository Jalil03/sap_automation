from __future__ import annotations

from copy import deepcopy
from typing import Any

from .errors import MappingContractError


def put(target: dict, sap_field: str, value: Any) -> None:
    """Add only explicit, non-null canonical values; never invent defaults."""
    if value is not None:
        target[sap_field] = deepcopy(value)


def mapped_date(value: Any, canonical_path: str, sap_field: str,
                deferred: list[dict]) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if value.get("kind") == "ABSOLUTE" and value.get("raw"):
            return value["raw"]
        deferred.append({
            "canonical_path": canonical_path,
            "sap_field": sap_field,
            "reason": "SEMANTIC_DATE_REQUIRES_RUNTIME_RESOLUTION",
            "value": deepcopy(value),
        })
        return None
    raise MappingContractError(f"Unsupported date representation at {canonical_path}")


def dependency_binding(obj: dict, target_type: str, relation: str,
                       sap_field: str, bindings: list[dict]) -> None:
    matches = [
        dep for dep in obj.get("dependencies", [])
        if dep.get("target_type") == target_type and dep.get("relation") in {relation, "REFERENCES"}
    ]
    if not matches:
        return
    dependency = matches[0]
    bindings.append({
        "sap_field": sap_field,
        "relation": dependency.get("relation"),
        "target_type": target_type,
        "target_object_id": dependency.get("target_id"),
        "dependency_status": dependency.get("status"),
        "source_phrase": dependency.get("source_phrase"),
    })


def require(body: dict, fields: tuple[str, ...], label: str) -> list[str]:
    return [f"{label}.{field}" for field in fields if body.get(field) in (None, "", [])]


def retained_nonpayload_fields(data: dict, mapped_fields: set[str]) -> list[dict]:
    """Expose meaningful canonical values intentionally excluded from a write body."""
    retained = []
    for field in sorted(set(data) - mapped_fields):
        value = data[field]
        if value not in (None, "", [], {}):
            retained.append({"canonical_path": f"data.{field}", "value": deepcopy(value)})
    return retained
