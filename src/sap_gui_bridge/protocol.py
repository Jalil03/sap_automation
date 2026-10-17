"""Filesystem request/response protocol for the manually launched local runner."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import DuplicateRequestError, ProtocolError, ResponseTimeoutError


ROOT = Path(__file__).resolve().parents[2]
REQUEST_DIR = ROOT / "runtime" / "sap_gui_requests"
RESPONSE_DIR = ROOT / "runtime" / "sap_gui_responses"
ARCHIVE_DIR = ROOT / "runtime" / "sap_gui_archive"

READ_ACTIONS = {
    "STATUS",
    "INSPECT",
    "READ_STATUS_BAR",
    "READ_SCREEN",
    "OPEN_TRANSACTION",
    "NAVIGATE",
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
}
EXECUTE_ACTIONS = {"PHASE5_OPERATION"}
ALLOWED_ACTIONS = READ_ACTIONS | EXECUTE_ACTIONS
PHASE5_OPERATIONS = {
    "COMPANY_CODE_1010",
    "SALES_ORGANIZATION_1010",
    "SALES_ORG_1010_TO_COMPANY_CODE_1010",
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
    "DIVISION_00_TO_SALES_ORG_1010",
    "CUSTOMER_C615_D00",
    "PRODUCT_P615_400",
    "VOV4_ITEM_CATEGORY_DETERMINATION",
    "S4615_BILLING_TYPE_ZF01",
    "S4615_SALES_TYPE_ZA01",
}
PHASE5_PHASES = {"LOOKUP", "PROVISION", "READBACK", "COPY_DIALOG_INSPECT"}
ALLOWED_TRANSACTIONS = {"SPRO", "MM02", "VOFA", "VOV8"}
NAVIGATION_OPERATIONS = {
    "PRESS_SAFE_BUTTON",
    "SELECT_TREE_NODE",
    "EXPAND_TREE_NODE",
    "COLLAPSE_TREE_NODE",
    "DOUBLE_CLICK_TREE_NODE",
    "OPEN_IMG_ACTIVITY",
    "SELECT_TAB",
    "FOCUS_CONTROL",
    "BACK",
}
TREE_NAVIGATION_OPERATIONS = {
    "SELECT_TREE_NODE",
    "EXPAND_TREE_NODE",
    "COLLAPSE_TREE_NODE",
    "DOUBLE_CLICK_TREE_NODE",
    "OPEN_IMG_ACTIVITY",
}
FORBIDDEN_TERMS = {
    "SAVE", "CTRL+S", "CONTROL+S", "DELETE", "RELEASE", "TRANSPORT",
    "CREATE", "MODIFY", "POST", "PATCH", "PUT", "ENTER",
}


def ensure_runtime_dirs() -> None:
    for directory in (REQUEST_DIR, RESPONSE_DIR, ARCHIVE_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def normalize_request_id(value: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ProtocolError("request_id must be a canonical UUID") from exc
    canonical = str(parsed)
    if str(value).lower() != canonical:
        raise ProtocolError("request_id must use canonical UUID formatting")
    return canonical


def validate_request(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != {"request_id", "mode", "action", "params"}:
        raise ProtocolError("request must contain exactly request_id, mode, action and params")
    request_id = normalize_request_id(payload["request_id"])
    mode = str(payload["mode"]).upper()
    if mode not in {"READ", "EXECUTE"}:
        raise ProtocolError("mode must be READ or EXECUTE")
    action = str(payload["action"]).upper()
    allowed_actions = READ_ACTIONS if mode == "READ" else EXECUTE_ACTIONS
    if action in FORBIDDEN_TERMS or action not in allowed_actions:
        raise ProtocolError(f"unsupported or forbidden action: {action}")
    params = payload["params"]
    if not isinstance(params, dict):
        raise ProtocolError("params must be an object")
    if action == "PHASE5_OPERATION":
        if set(params) != {"operation", "phase", "target", "values"}:
            raise ProtocolError(
                "PHASE5_OPERATION requires exactly operation, phase, target and values"
            )
        operation = str(params["operation"]).upper()
        phase = str(params["phase"]).upper()
        target = params["target"]
        values = params["values"]
        if operation not in PHASE5_OPERATIONS:
            raise ProtocolError(f"Phase5 operation is not allowlisted: {operation}")
        if phase not in PHASE5_PHASES:
            raise ProtocolError(f"unsupported Phase5 phase: {phase}")
        if not isinstance(target, dict) or not target:
            raise ProtocolError("Phase5 target must be a non-empty object")
        if not isinstance(values, dict):
            raise ProtocolError("Phase5 values must be an object")
        if phase != "PROVISION" and values:
            raise ProtocolError(f"{phase} does not accept write values")
        if phase == "COPY_DIALOG_INSPECT" and operation not in {"COMPANY_CODE_1010", "S4615_BILLING_TYPE_ZF01", "S4615_SALES_TYPE_ZA01"}:
            raise ProtocolError(
                "COPY_DIALOG_INSPECT is only allowlisted for COMPANY_CODE_1010 or S4615_BILLING_TYPE_ZF01"
            )
        params = {
            "operation": operation,
            "phase": phase,
            "target": target,
            "values": values,
        }
    elif action == "OPEN_TRANSACTION":
        if set(params) != {"transaction"}:
            raise ProtocolError("OPEN_TRANSACTION requires exactly params.transaction")
        transaction = str(params["transaction"]).upper()
        if transaction not in ALLOWED_TRANSACTIONS:
            raise ProtocolError(f"transaction is not allowlisted: {transaction}")
        params = {"transaction": transaction}
    elif action == "NAVIGATE":
        required = {"control_id", "expected_type", "expected_text", "navigation_operation"}
        allowed = required | {"node_key", "expected_transaction", "item_column"}
        if not required.issubset(params) or not set(params).issubset(allowed):
            raise ProtocolError(
                "NAVIGATE requires control_id, expected_type, expected_text and navigation_operation; only node_key is optional"
            )
        operation = str(params["navigation_operation"]).upper()
        if operation not in NAVIGATION_OPERATIONS:
            raise ProtocolError(f"unsupported navigation operation: {operation}")
        control_id = params["control_id"]
        expected_type = params["expected_type"]
        expected_text = params["expected_text"]
        if not isinstance(control_id, str) or not control_id.strip():
            raise ProtocolError("NAVIGATE control_id must be a non-empty string")
        if not isinstance(expected_type, str) or not expected_type.strip():
            raise ProtocolError("NAVIGATE expected_type must be a non-empty string")
        if expected_text is not None and not isinstance(expected_text, str):
            raise ProtocolError("NAVIGATE expected_text must be a string or null")
        node_key = params.get("node_key")
        if operation in TREE_NAVIGATION_OPERATIONS:
            if not isinstance(node_key, str) or not node_key:
                raise ProtocolError(f"{operation} requires a non-empty node_key")
        elif "node_key" in params:
            raise ProtocolError(f"{operation} does not accept node_key")
        expected_transaction = params.get("expected_transaction")
        item_column = params.get("item_column")
        if operation == "OPEN_IMG_ACTIVITY":
            if expected_transaction != "SIMG":
                raise ProtocolError("OPEN_IMG_ACTIVITY requires expected_transaction='SIMG'")
            if item_column is not None and (
                not isinstance(item_column, str) or not item_column
            ):
                raise ProtocolError("OPEN_IMG_ACTIVITY item_column must be a non-empty string or null")
        elif "expected_transaction" in params or "item_column" in params:
            raise ProtocolError(
                f"{operation} does not accept expected_transaction or item_column"
            )
        params = {
            "control_id": control_id,
            "expected_type": expected_type,
            "expected_text": expected_text,
            "navigation_operation": operation,
            **({"node_key": node_key} if node_key is not None else {}),
            **(
                {"expected_transaction": expected_transaction}
                if operation == "OPEN_IMG_ACTIVITY"
                else {}
            ),
            **({"item_column": item_column} if item_column is not None else {}),
        }
    elif action == "CLOSE_IMG_INFO_POPUP":
        expected = {
            "source": "OPEN_IMG_ACTIVITY",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
        }
        if params != expected:
            raise ProtocolError(
                "CLOSE_IMG_INFO_POPUP is restricted to the observed "
                "OPEN_IMG_ACTIVITY SAPLDSYH wnd[1] context"
            )
        params = dict(expected)
    elif action == "SELECT_COMPANY_CODE_ACTIVITY":
        expected = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "company_code",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "row_text": "Traiter données société",
            "button_text": "Sélectionner",
        }
        if params != expected:
            raise ProtocolError(
                "SELECT_COMPANY_CODE_ACTIVITY is restricted to the exact observed company-code activity selector"
            )
        params = dict(expected)
    elif action == "FIND_TABLE_VALUE":
        expected = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001",
            "column": "BUKRS",
            "value": "1010",
        }
        if params != expected:
            raise ProtocolError(
                "FIND_TABLE_VALUE is restricted to the exact V_T001/SAPL0ORG BUKRS=1010 lookup"
            )
        params = dict(expected)
    elif action == "SELECT_SALES_ORGANIZATION_ACTIVITY":
        expected = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
            "row_text": "D\u00e9finir l'organisation commerciale",
            "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
            "button_text": "S\u00e9lectionner",
        }
        if params != expected:
            raise ProtocolError(
                "SELECT_SALES_ORGANIZATION_ACTIVITY requires the exact observed Sales Organization table row and button"
            )
        params = dict(expected)
    elif action == "SELECT_DISTRIBUTION_CHANNEL_ACTIVITY":
        expected = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "distribution_channel",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
            "row_text": "D\u00e9finir le canal de distribution",
            "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
            "button_text": "S\u00e9lectionner",
        }
        if params != expected:
            raise ProtocolError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY requires the exact observed distribution-channel definition row and button")
        params = dict(expected)
    elif action == "SELECT_SALES_DIVISION_ACTIVITY":
        expected = {"source": "OPEN_IMG_ACTIVITY", "target": "sales_division", "window_id": "/app/con[0]/ses[0]/wnd[1]", "expected_transaction": "SIMG", "expected_program": "SAPLDSYH", "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES", "row_text": "D\u00e9finir le secteur d'activit\u00e9", "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]", "button_text": "S\u00e9lectionner"}
        if params != expected:
            raise ProtocolError("SELECT_SALES_DIVISION_ACTIVITY requires the exact observed definition row and button")
        params = dict(expected)
    elif action == "SCAN_S4650_DISTRIBUTION_CHANNELS":
        expected = {
            "transaction": "V_TVTW",
            "program": "SAPL0ORGCORE",
            "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGCORETCTRL_V_TVTW",
        }
        if params != expected:
            raise ProtocolError("SCAN_S4650_DISTRIBUTION_CHANNELS is restricted to the exact live V_TVTW table")
        params = dict(expected)
    elif action == "SCAN_S4650_SALES_AREAS":
        expected = {"transaction": "SIMG", "program": "SAPLCUST_ASSIGN_SD", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLCUST_ASSIGN_SDTCTRL_V_TVTA_ASSIGN", "sales_organization": "1010", "distribution_channel": "D1", "divisions": ["00", "03"]}
        if params != expected:
            raise ProtocolError("SCAN_S4650_SALES_AREAS requires the exact observed target and table")
        params = dict(expected)
    elif action == "SCAN_S4650_SALES_DIVISIONS":
        expected = {"transaction": "V_TSPA", "program": "SAPL0ORGCORE", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGCORETCTRL_V_TSPA", "values": ["00", "03"]}
        if params != expected:
            raise ProtocolError("SCAN_S4650_SALES_DIVISIONS requires exact observed V_TSPA target and table")
        params = dict(expected)
    elif action == "SELECT_S4650_BILLING_COPY_ACTIVITY":
        expected = {"source": "OPEN_IMG_ACTIVITY", "window_id": "/app/con[0]/ses[0]/wnd[1]", "transaction": "SIMG", "program": "SAPLDSYH", "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES", "row_text": "D\u00e9finir pilotage copie pour document de livraison vers document facturation", "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]", "button_text": "S\u00e9lectionner"}
        if params != expected:
            raise ProtocolError("SELECT_S4650_BILLING_COPY_ACTIVITY requires exact observed delivery-to-billing row")
        params = dict(expected)
    elif action == "SELECT_S4615_BILLING_TYPE_ACTIVITY":
        expected = {"source": "OPEN_IMG_ACTIVITY", "window_id": "/app/con[0]/ses[0]/wnd[1]", "transaction": "SIMG", "program": "SAPLDSYH", "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES", "row_text": "Définir types de documents de facturation pour les ventes", "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]", "button_text": "Sélectionner"}
        if params != expected:
            raise ProtocolError("SELECT_S4615_BILLING_TYPE_ACTIVITY requires the exact observed billing-type row")
        params = dict(expected)
    elif action == "FIND_S4615_BILLING_TYPE":
        expected = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "ZF01"}
        if params != expected:
            raise ProtocolError("FIND_S4615_BILLING_TYPE requires exact VOFA ZF01 target")
        params = dict(expected)
    elif action == "DISPLAY_S4615_F2_REFERENCE":
        expected = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "F2", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        if params != expected:
            raise ProtocolError("DISPLAY_S4615_F2_REFERENCE requires exact VOFA F2 display contract")
        params = dict(expected)
    elif action == "DISPLAY_S4615_ZF01":
        expected = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "ZF01", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        if params != expected:
            raise ProtocolError("DISPLAY_S4615_ZF01 requires exact VOFA ZF01 display contract")
        params = dict(expected)
    elif action == "FIND_S4615_SALES_TYPE":
        expected = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": "ZA01"}
        if params != expected:
            raise ProtocolError("FIND_S4615_SALES_TYPE requires exact VOV8 ZA01 target")
        params = dict(expected)
    elif action == "DISPLAY_S4615_SALES_REFERENCE":
        expected = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": params.get("sales_order_type"), "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        if expected["sales_order_type"] not in {"CS", "BV", "ZA01"} or params != expected:
            raise ProtocolError("DISPLAY_S4615_SALES_REFERENCE requires exact VOV8 CS/BV/ZA01 display contract")
        params = dict(expected)
    elif action == "FIND_S4650_BILLING_COPY_HEADER":
        expected = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK", "billing_type": "F2", "delivery_type": "LF"}
        if params != expected:
            raise ProtocolError("FIND_S4650_BILLING_COPY_HEADER requires exact VTFLC F2/LF target")
        params = dict(expected)
    elif action == "DISPLAY_S4650_BILLING_COPY_HEADER":
        expected = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK", "billing_type": "F2", "delivery_type": "LF", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        if params != expected:
            raise ProtocolError("DISPLAY_S4650_BILLING_COPY_HEADER requires exact F2/LF detail contract")
        params = dict(expected)
    elif action == "OPEN_S4650_BILLING_COPY_ITEMS":
        expected = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "110", "tree_id": "/app/con[0]/ses[0]/wnd[0]/shellcont/shell", "node_key": "02", "node_text": "Poste", "column": "Column1"}
        if params != expected:
            raise ProtocolError("OPEN_S4650_BILLING_COPY_ITEMS requires exact VTFLC Poste tree contract")
        params = dict(expected)
    elif action == "DISPLAY_S4650_BILLING_COPY_TAN":
        expected = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "112", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLP", "item_category": "TAN", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        if params != expected:
            raise ProtocolError("DISPLAY_S4650_BILLING_COPY_TAN requires exact VTFLC TAN target")
        params = dict(expected)
    elif action == "LOOKUP_S4650_PRODUCT":
        expected = {"transaction": "MM02", "program": "SAPLMGMM", "screen": "60", "material": "P650-101", "field_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRMMG1-MATNR", "views_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"}
        if params != expected:
            raise ProtocolError("LOOKUP_S4650_PRODUCT requires exact book material and MM02 controls")
        params = dict(expected)
    elif action == "_LEGACY_SELECT_SALES_ORGANIZATION_ACTIVITY":
        required = {
            "source",
            "target",
            "window_id",
            "expected_transaction",
            "expected_program",
            "row_text",
            "button_text",
        }
        fixed = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "button_text": "Sélectionner",
        }
        row_text = params.get("row_text")
        normalized_row = str(row_text or "").casefold()
        if (
            set(params) != required
            or any(params.get(key) != value for key, value in fixed.items())
            or not isinstance(row_text, str)
            or not normalized_row.startswith("traiter")
            or not (
                "organisation commerciale" in normalized_row
                or "org. commerciale" in normalized_row
            )
            or any(term in normalized_row for term in ("copier", "supprimer", "contr"))
        ):
            raise ProtocolError(
                "SELECT_SALES_ORGANIZATION_ACTIVITY requires one exact observed non-copy processing row"
            )
        params = {**fixed, "row_text": row_text}
    elif params:
        raise ProtocolError(f"{action} does not accept params")
    return {"request_id": request_id, "mode": mode, "action": action, "params": params}


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def request_paths(request_id: str) -> tuple[Path, Path, Path]:
    request_id = normalize_request_id(request_id)
    return (
        REQUEST_DIR / f"{request_id}.json",
        RESPONSE_DIR / f"{request_id}.json",
        ARCHIVE_DIR / f"{request_id}.json",
    )


def enqueue_request(
    action: str,
    params: dict[str, Any] | None = None,
    request_id: str | None = None,
    *,
    mode: str = "READ",
) -> dict[str, Any]:
    ensure_runtime_dirs()
    payload = validate_request(
        {
            "request_id": request_id or str(uuid.uuid4()),
            "mode": mode,
            "action": action,
            "params": params or {},
        }
    )
    request_path, response_path, archive_path = request_paths(payload["request_id"])
    if request_path.exists() or response_path.exists() or archive_path.exists():
        raise DuplicateRequestError(f"request_id already exists: {payload['request_id']}")
    _atomic_json(request_path, payload)
    try:
        display_path = request_path.relative_to(ROOT)
    except ValueError:  # Supports isolated temporary directories in tests.
        display_path = request_path
    return {"request_id": payload["request_id"], "request_path": str(display_path).replace("\\", "/")}


def read_response(request_id: str) -> dict[str, Any] | None:
    _, response_path, _ = request_paths(request_id)
    if not response_path.exists():
        return None
    try:
        payload = json.loads(response_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(f"invalid response file for {request_id}") from exc
    if not isinstance(payload, dict) or payload.get("request_id") != request_id:
        raise ProtocolError("response request_id mismatch")
    return payload


def wait_for_response(request_id: str, timeout_seconds: float = 60.0, poll_seconds: float = 0.25) -> dict[str, Any]:
    request_id = normalize_request_id(request_id)
    if timeout_seconds < 0 or timeout_seconds > 60:
        raise ProtocolError("timeout must be between 0 and 60 seconds")
    deadline = time.monotonic() + timeout_seconds
    while True:
        response = read_response(request_id)
        if response is not None:
            return response
        if time.monotonic() >= deadline:
            raise ResponseTimeoutError(f"no response for {request_id} within {timeout_seconds:g}s")
        time.sleep(min(poll_seconds, max(0.0, deadline - time.monotonic())))


def write_response(payload: dict[str, Any]) -> Path:
    ensure_runtime_dirs()
    request_id = normalize_request_id(payload.get("request_id"))
    required = {"request_id", "status", "sap", "result", "error"}
    if set(payload) != required or payload["status"] not in {"SUCCESS", "ERROR"}:
        raise ProtocolError("invalid response payload")
    _, response_path, _ = request_paths(request_id)
    if response_path.exists():
        raise DuplicateRequestError(f"response already exists: {request_id}")
    _atomic_json(response_path, payload)
    return response_path


def archive_request(request_path: Path, request_id: str) -> Path:
    ensure_runtime_dirs()
    request_id = normalize_request_id(request_id)
    resolved = request_path.resolve()
    if resolved.parent != REQUEST_DIR.resolve():
        raise ProtocolError("request archive source is outside the request directory")
    archive_path = ARCHIVE_DIR / f"{request_id}.json"
    if archive_path.exists():
        suffix = uuid.uuid5(uuid.NAMESPACE_URL, request_path.read_text(encoding="utf-8", errors="replace")).hex[:12]
        archive_path = ARCHIVE_DIR / f"{request_id}.duplicate.{suffix}.json"
    request_path.replace(archive_path)
    return archive_path
