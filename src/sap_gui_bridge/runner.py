"""One-at-a-time processor used by the manually launched Windows runner."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from .connection import SapGuiConnection
from .errors import ActionBlockedError, ProtocolError, SapGuiBridgeError
from .inspection import inspect_screen
from .navigation import (
    back,
    close_img_info_popup,
    find_company_code_table_value,
    navigate,
    open_transaction,
    select_company_code_display_activity,
    select_sales_organization_activity,
    select_distribution_channel_activity,
    select_sales_division_activity,
    scan_s4650_distribution_channels,
    scan_s4650_sales_areas,
    scan_s4650_sales_divisions,
    select_s4650_billing_copy_activity,
    select_s4615_billing_type_activity,
    find_s4615_billing_type,
    display_s4615_f2_reference,
    find_s4615_sales_type,
    display_s4615_sales_reference,
    find_s4650_billing_copy_header,
    display_s4650_billing_copy_header,
    open_s4650_billing_copy_items,
    display_s4650_billing_copy_tan,
    lookup_s4650_product,
)
from .protocol import (
    ARCHIVE_DIR,
    REQUEST_DIR,
    archive_request,
    ensure_runtime_dirs,
    validate_request,
    write_response,
)
from .safety import SafetyMode


def _status_bar(session) -> dict[str, str]:
    session.audit("READ_STATUS_BAR")
    control = session.find("wnd[0]/sbar")
    return {
        "text": str(getattr(control, "Text", "")),
        "message_type": str(getattr(control, "MessageType", "")),
    }


def _read_screen(session) -> dict[str, Any]:
    session.audit("READ_SCREEN")
    snapshot = inspect_screen(session)
    return {
        "window_title": snapshot["window_title"],
        "transaction": snapshot["transaction"],
        "status_bar": snapshot["status_bar"],
        "control_ids": snapshot["control_ids"],
        "truncated": snapshot["truncated"],
    }


def execute_read_action(session, request: dict[str, Any]) -> Any:
    action = request["action"]
    if action == "STATUS":
        return session.status()
    if action == "INSPECT":
        return inspect_screen(session)
    if action == "READ_STATUS_BAR":
        return _status_bar(session)
    if action == "READ_SCREEN":
        return _read_screen(session)
    if action == "OPEN_TRANSACTION":
        open_transaction(session, request["params"]["transaction"])
        return session.status()
    if action == "NAVIGATE":
        return navigate(session, request["params"])
    if action == "BACK":
        back(session)
        return inspect_screen(session)
    if action == "CLOSE_IMG_INFO_POPUP":
        return close_img_info_popup(session, request["params"])
    if action == "SELECT_COMPANY_CODE_ACTIVITY":
        return select_company_code_display_activity(session, request["params"])
    if action == "FIND_TABLE_VALUE":
        return find_company_code_table_value(session, request["params"])
    if action == "SELECT_SALES_ORGANIZATION_ACTIVITY":
        return select_sales_organization_activity(session, request["params"])
    if action == "SELECT_DISTRIBUTION_CHANNEL_ACTIVITY":
        return select_distribution_channel_activity(session, request["params"])
    if action == "SELECT_SALES_DIVISION_ACTIVITY":
        return select_sales_division_activity(session, request["params"])
    if action == "SCAN_S4650_DISTRIBUTION_CHANNELS":
        return scan_s4650_distribution_channels(session, request["params"])
    if action == "SCAN_S4650_SALES_AREAS":
        return scan_s4650_sales_areas(session, request["params"])
    if action == "SCAN_S4650_SALES_DIVISIONS":
        return scan_s4650_sales_divisions(session, request["params"])
    if action == "SELECT_S4650_BILLING_COPY_ACTIVITY":
        return select_s4650_billing_copy_activity(session, request["params"])
    if action == "SELECT_S4615_BILLING_TYPE_ACTIVITY":
        return select_s4615_billing_type_activity(session, request["params"])
    if action == "FIND_S4615_BILLING_TYPE":
        return find_s4615_billing_type(session, request["params"])
    if action == "DISPLAY_S4615_F2_REFERENCE":
        return display_s4615_f2_reference(session, request["params"])
    if action == "DISPLAY_S4615_ZF01":
        return display_s4615_f2_reference(session, request["params"])
    if action == "FIND_S4615_SALES_TYPE":
        return find_s4615_sales_type(session, request["params"])
    if action == "DISPLAY_S4615_SALES_REFERENCE":
        return display_s4615_sales_reference(session, request["params"])
    if action == "FIND_S4650_BILLING_COPY_HEADER":
        return find_s4650_billing_copy_header(session, request["params"])
    if action == "DISPLAY_S4650_BILLING_COPY_HEADER":
        return display_s4650_billing_copy_header(session, request["params"])
    if action == "OPEN_S4650_BILLING_COPY_ITEMS":
        return open_s4650_billing_copy_items(session, request["params"])
    if action == "DISPLAY_S4650_BILLING_COPY_TAN":
        return display_s4650_billing_copy_tan(session, request["params"])
    if action == "LOOKUP_S4650_PRODUCT":
        return lookup_s4650_product(session, request["params"])
    raise AssertionError(f"unreachable action after validation: {action}")


def execute_phase5_action(session, request: dict[str, Any]) -> Any:
    """Validate the EXECUTE envelope and fail closed without an exact GUI contract.

    The Phase4 evidence identifies the write boundaries, but it does not record
    the complete deterministic control sequence for copy/create, field override,
    SAVE, transport handling, and readback for all seven objects.  Calling a
    generic transaction or COM method here would violate the Phase5 whitelist.
    """
    session.audit(
        "PHASE5_OPERATION",
        value={
            "operation": request["params"]["operation"],
            "phase": request["params"]["phase"],
        },
    )
    raise ActionBlockedError(
        "Phase5 operation has no complete captured SAP GUI control contract; "
        "generic transaction execution is forbidden"
    )


def _error_response(request_id: str, exc: Exception) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "status": "ERROR",
        "sap": None,
        "result": None,
        "error": {"type": type(exc).__name__, "message": str(exc)},
    }


def process_request_file(
    request_path: Path,
    connection_factory: Callable[[], SapGuiConnection] | None = None,
    execute_handler: Callable[[Any, dict[str, Any]], Any] | None = None,
) -> dict[str, Any]:
    execute_handler = execute_handler or execute_phase5_action
    fallback_id = None
    try:
        fallback_id = str(uuid.UUID(request_path.stem))
    except ValueError:
        fallback_id = str(uuid.uuid5(uuid.NAMESPACE_URL, request_path.name))
    try:
        raw = json.loads(request_path.read_text(encoding="utf-8"))
        request = validate_request(raw)
        request_id = request["request_id"]
        if request_path.stem != request_id:
            raise ProtocolError("request filename must match request_id")
        mode = SafetyMode(request["mode"])
        connection = (
            connection_factory()
            if connection_factory is not None
            else SapGuiConnection(mode=mode)
        )
        session = connection.attach()
        if session.policy.mode is not mode:
            raise ProtocolError("runner connection mode does not match request mode")
        result = (
            execute_read_action(session, request)
            if mode is SafetyMode.READ
            else execute_handler(session, request)
        )
        response = {
            "request_id": request_id,
            "status": "SUCCESS",
            "sap": session.identity,
            "result": result,
            "error": None,
        }
    except Exception as exc:
        request_id = fallback_id
        if isinstance(locals().get("raw"), dict):
            candidate = raw.get("request_id")
            try:
                request_id = str(uuid.UUID(str(candidate)))
            except (ValueError, TypeError, AttributeError):
                pass
        response = _error_response(request_id, exc)

    try:
        write_response(response)
    except Exception as exc:
        if not isinstance(exc, SapGuiBridgeError):
            raise
    finally:
        archive_request(request_path, response["request_id"])
    return response


def run_forever(
    poll_seconds: float = 0.5,
    execute_handler: Callable[[Any, dict[str, Any]], Any] | None = None,
) -> None:
    ensure_runtime_dirs()
    print(
        "SAP GUI local runner active (READ plus strict Phase5 EXECUTE whitelist). "
        "Press Ctrl+C to stop.",
        flush=True,
    )
    try:
        while True:
            requests = sorted(REQUEST_DIR.glob("*.json"), key=lambda path: path.name)
            if requests:
                response = process_request_file(
                    requests[0], execute_handler=execute_handler
                )
                print(json.dumps({"request_id": response["request_id"], "status": response["status"]}), flush=True)
            else:
                time.sleep(poll_seconds)
    except KeyboardInterrupt:
        print("SAP GUI local runner stopped.", flush=True)
