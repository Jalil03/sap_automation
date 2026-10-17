from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any

from .errors import UnresolvedPlaceholderError
from .user_context import TrainingUserContext


PLACEHOLDER = "##"
_PATH_PART = re.compile(r"([^.[\]]+)|\[(\d+)\]")


@dataclass(frozen=True)
class PlaceholderResolution:
    field_path: str
    original_template: str
    resolved_value: str
    replacements: int


@dataclass(frozen=True)
class ResolvedTrainingObject:
    canonical_object: dict[str, Any]
    training_user_code: str
    training_user_role: str
    placeholders_resolved: tuple[PlaceholderResolution, ...]

    def trace_metadata(self) -> dict[str, Any]:
        return {
            "training_user_code": self.training_user_code,
            "training_user_role": self.training_user_role,
            "placeholders_resolved": [asdict(item) for item in self.placeholders_resolved],
        }


class PlaceholderResolver:
    """Resolve book placeholders in a detached runtime copy of canonical data."""

    def resolve(
        self, canonical_object: dict[str, Any], training_user_code: str
    ) -> ResolvedTrainingObject:
        context = TrainingUserContext(training_user_code)
        runtime_object = deepcopy(canonical_object)
        resolutions: list[PlaceholderResolution] = []

        if not isinstance(runtime_object, dict):
            raise TypeError("canonical_object must be a dictionary")

        # Only canonical data is executable. Provenance and raw placeholder templates
        # remain untouched in the runtime copy for traceability.
        runtime_object["data"] = self._resolve_node(
            runtime_object.get("data", {}),
            "data",
            context.training_user_code,
            resolutions,
        )
        self._synchronize_placeholder_metadata(runtime_object)
        self._synchronize_readiness(runtime_object)

        remaining = self._find_remaining(runtime_object.get("data", {}), "data")
        if remaining:
            raise UnresolvedPlaceholderError(
                "Executable placeholder remains after resolution at " + ", ".join(remaining)
            )

        return ResolvedTrainingObject(
            canonical_object=runtime_object,
            training_user_code=context.training_user_code,
            training_user_role=context.role,
            placeholders_resolved=tuple(resolutions),
        )

    def _resolve_node(
        self,
        value: Any,
        path: str,
        code: str,
        resolutions: list[PlaceholderResolution],
    ) -> Any:
        if isinstance(value, str):
            count = value.count(PLACEHOLDER)
            if not count:
                return value
            resolved = value.replace(PLACEHOLDER, code)
            resolutions.append(PlaceholderResolution(path, value, resolved, count))
            return resolved
        if isinstance(value, list):
            return [
                self._resolve_node(item, f"{path}[{index}]", code, resolutions)
                for index, item in enumerate(value)
            ]
        if isinstance(value, dict):
            # Canonical field names are contracts, not templates. A placeholder in a
            # key is deliberately left visible so the final executable check blocks.
            return {
                key: self._resolve_node(item, f"{path}.{key}", code, resolutions)
                for key, item in value.items()
            }
        return value

    @staticmethod
    def _value_at_path(root: dict[str, Any], path: str | None) -> Any:
        if not path:
            return None
        value: Any = root
        for match in _PATH_PART.finditer(path):
            key, index = match.groups()
            if key is not None:
                if not isinstance(value, dict) or key not in value:
                    return None
                value = value[key]
            else:
                if not isinstance(value, list) or int(index) >= len(value):
                    return None
                value = value[int(index)]
        return value

    def _synchronize_placeholder_metadata(self, runtime_object: dict[str, Any]) -> None:
        for placeholder in runtime_object.get("placeholders", []):
            if placeholder.get("status") != "UNRESOLVED":
                continue
            value = self._value_at_path(runtime_object, placeholder.get("field_path"))
            if value is not None and PLACEHOLDER not in str(value):
                placeholder["status"] = "RESOLVED"
                placeholder["resolved"] = value

    @staticmethod
    def _synchronize_readiness(runtime_object: dict[str, Any]) -> None:
        if any(
            placeholder.get("status") == "UNRESOLVED" and placeholder.get("mandatory")
            for placeholder in runtime_object.get("placeholders", [])
        ):
            return
        reasons = [
            reason
            for reason in runtime_object.get("blocking_reasons", [])
            if reason.get("code") != "UNRESOLVED_MANDATORY_PLACEHOLDER"
        ]
        runtime_object["blocking_reasons"] = reasons
        if runtime_object.get("readiness_status") == "BLOCKED" and not reasons:
            runtime_object["readiness_status"] = "READY"

    def _find_remaining(self, value: Any, path: str) -> list[str]:
        if isinstance(value, str):
            return [path] if PLACEHOLDER in value else []
        if isinstance(value, list):
            found: list[str] = []
            for index, item in enumerate(value):
                found.extend(self._find_remaining(item, f"{path}[{index}]"))
            return found
        if isinstance(value, dict):
            found = []
            for key, item in value.items():
                key_path = f"{path}.{key}"
                if isinstance(key, str) and PLACEHOLDER in key:
                    found.append(key_path)
                found.extend(self._find_remaining(item, key_path))
            return found
        return []
