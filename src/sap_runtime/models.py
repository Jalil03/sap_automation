from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class ExecutionStatus(StrEnum):
    DRY_RUN_OK = "DRY_RUN_OK"
    BLOCKED = "BLOCKED"
    DUPLICATE = "DUPLICATE"
    SUBMITTED = "SUBMITTED"
    CREATED = "CREATED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class RuntimeResult:
    canonical_object_id: str
    correlation_id: str
    payload_sha256: str
    mode: str
    status: ExecutionStatus
    payload: dict[str, Any]
    checks: list[CheckResult] = field(default_factory=list)
    training_context: dict[str, Any] | None = None
    http_status: int | None = None
    created_sales_order_id: str | None = None
    response_etag: str | None = None
    sanitized_error: str | None = None
    read_back: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["status"] = self.status.value
        return value
