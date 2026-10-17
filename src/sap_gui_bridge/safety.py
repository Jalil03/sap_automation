"""Safety policy and sanitized audit logging for SAP GUI Scripting."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import ActionBlockedError


class SafetyMode(str, Enum):
    READ = "READ"
    PREPARE = "PREPARE"
    EXECUTE = "EXECUTE"


READ_ACTIONS = {
    "ATTACH",
    "STATUS",
    "INSPECT",
    "READ_STATUS_BAR",
    "READ_SCREEN",
    "OPEN_TRANSACTION",
    "NAVIGATE",
    "OPEN_IMG_ACTIVITY",
    "BACK",
    "CLOSE_IMG_INFO_POPUP",
    "SELECT_COMPANY_CODE_ACTIVITY",
    "SELECT_SALES_ORGANIZATION_ACTIVITY",
    "SELECT_DISTRIBUTION_CHANNEL_ACTIVITY",
    "SELECT_SALES_DIVISION_ACTIVITY",
    "SCAN_S4650_DISTRIBUTION_CHANNELS",
    "SCAN_S4650_SALES_AREAS",
    "SCAN_S4650_SALES_DIVISIONS",
    "SELECT_S4650_BILLING_COPY_ACTIVITY",
    "SELECT_S4615_BILLING_TYPE_ACTIVITY",
    "FIND_S4615_BILLING_TYPE",
    "DISPLAY_S4615_F2_REFERENCE",
    "DISPLAY_S4615_ZF01",
    "FIND_S4615_SALES_TYPE",
    "DISPLAY_S4615_SALES_REFERENCE",
    "FIND_S4650_BILLING_COPY_HEADER",
    "DISPLAY_S4650_BILLING_COPY_HEADER",
    "OPEN_S4650_BILLING_COPY_ITEMS",
    "DISPLAY_S4650_BILLING_COPY_TAN",
    "LOOKUP_S4650_PRODUCT",
    "FIND_TABLE_VALUE",
    "POSITION_COMPANY_CODE_VALUE",
    "PRESS_SAFE_BUTTON",
}
PREPARE_ACTIONS = READ_ACTIONS | {"SET_TEXT"}
EXECUTE_ACTIONS = {
    "ATTACH",
    "INSPECT",
    "PHASE5_OPERATION",
    "OPEN_TRANSACTION",
    "NAVIGATE",
    "SELECT_SALES_ORGANIZATION_ACTIVITY",
    "FIND_TABLE_VALUE",
    "POSITION_COMPANY_CODE_VALUE",
    "SELECT_COMPANY_CODE_ACTIVITY",
    "SELECT_COMPANY_CODE_COPY_SOURCE",
    "FIND_S4615_BILLING_TYPE",
    "DISPLAY_S4615_F2_REFERENCE",
    "FIND_S4615_SALES_TYPE",
    "DISPLAY_S4615_SALES_REFERENCE",
    "BACK",
}
SAVE_CONTROL_IDS = {"wnd[0]/tbar[0]/btn[11]"}
BLOCKED_KEY_CHORDS = {"CTRL+S", "CONTROL+S"}
BLOCKED_METHODS = {"SAVE", "DELETE", "RELEASE", "TRANSPORT_RELEASE", "SEND_VKEY_11"}
BLOCKED_TEXT = re.compile(
    r"\b(save|sauvegarder|enregistrer|delete|supprimer|release|libérer|liberer|transport)\b",
    re.IGNORECASE,
)
SENSITIVE_CONTROL = re.compile(r"password|passwd|pwd|secret|token|credential", re.IGNORECASE)


@dataclass(frozen=True)
class AuditEvent:
    timestamp: str
    system: str
    client: str
    user: str
    transaction: str
    mode: str
    control_id: str | None
    action: str
    value: Any | None


class AuditLogger:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(event), ensure_ascii=False, sort_keys=True) + "\n")


class SafetyPolicy:
    def __init__(self, mode: SafetyMode, logger: AuditLogger) -> None:
        self.mode = SafetyMode(mode)
        self.logger = logger

    @staticmethod
    def sanitize_value(control_id: str | None, value: Any | None) -> Any | None:
        if value is None:
            return None
        if control_id and SENSITIVE_CONTROL.search(control_id):
            return "<redacted>"
        text = str(value)
        if SENSITIVE_CONTROL.search(text):
            return "<redacted>"
        return value

    def authorize(
        self,
        *,
        identity: dict[str, str],
        action: str,
        control_id: str | None = None,
        control_text: str | None = None,
        value: Any | None = None,
        key_chord: str | None = None,
    ) -> None:
        normalized_action = action.upper()
        if self.mode is SafetyMode.EXECUTE:
            if normalized_action not in EXECUTE_ACTIONS:
                raise ActionBlockedError(
                    f"Action is not allowlisted in EXECUTE: {normalized_action}"
                )
            if normalized_action == "OPEN_TRANSACTION" and value not in {"SPRO", "VOV4", "VOFA"}:
                raise ActionBlockedError(
                    "OPEN_TRANSACTION is allowlisted in EXECUTE only for SPRO, VOV4 or VOFA"
                )
            event = AuditEvent(
                timestamp=datetime.now(timezone.utc).isoformat(),
                system=identity["system"],
                client=identity["client"],
                user=identity["user"],
                transaction=identity.get("transaction", ""),
                mode=self.mode.value,
                control_id=control_id,
                action=normalized_action,
                value=self.sanitize_value(control_id, value),
            )
            self.logger.write(event)
            return
        if control_id and control_id.lower() in {item.lower() for item in SAVE_CONTROL_IDS}:
            raise ActionBlockedError(f"Blocked save control: {control_id}")
        if key_chord and key_chord.upper() in BLOCKED_KEY_CHORDS:
            raise ActionBlockedError(f"Blocked key chord: {key_chord}")
        if normalized_action in BLOCKED_METHODS:
            raise ActionBlockedError(f"Blocked action: {normalized_action}")
        if control_text and BLOCKED_TEXT.search(control_text):
            raise ActionBlockedError(f"Blocked control text: {control_text}")
        allowed = READ_ACTIONS if self.mode is SafetyMode.READ else PREPARE_ACTIONS
        if normalized_action not in allowed:
            raise ActionBlockedError(f"Action is not allowlisted in {self.mode.value}: {normalized_action}")
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            system=identity["system"],
            client=identity["client"],
            user=identity["user"],
            transaction=identity.get("transaction", ""),
            mode=self.mode.value,
            control_id=control_id,
            action=normalized_action,
            value=self.sanitize_value(control_id, value),
        )
        self.logger.write(event)
