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
from .s4615_scan import scan_s4615_customizing


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


def _read_s4615_zf01_accounting_block(session) -> dict[str, Any]:
    """Read only the live VOFA/ZF01 accounting-block checkbox state."""
    session.validate_identity()
    snapshot = inspect_screen(session)
    field_id = "/app/con[0]/ses[0]/wnd[0]/usr/chkV_TVFK-RFBFK"
    header_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART"
    if ((snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")))
            != ("VOFA", "SAPL081F", "101") or snapshot.get("popups")):
        raise ActionBlockedError("ZF01 accounting-block read requires exact VOFA detail without popup")
    header = session.find(header_id)
    field = session.find(field_id)
    if (str(getattr(header, "Id", "")) != header_id
            or str(getattr(header, "Text", "")) != "ZF01"
            or str(getattr(field, "Id", "")) != field_id
            or str(getattr(field, "Type", "")) != "GuiCheckBox"
            or str(getattr(field, "Text", "")).strip() != "Blocage comptabil."):
        raise ActionBlockedError("ZF01 accounting-block controls do not match live evidence")
    selected = getattr(field, "Selected", None)
    if selected not in (True, False, -1, 0, 1):
        raise ActionBlockedError("ZF01 accounting-block Selected state unavailable")
    session.audit("READ_S4615_ZF01_ACCOUNTING_BLOCK", control_id=field_id, value=bool(selected))
    return {"billing_type": "ZF01", "field": "V_TVFK-RFBFK", "selected": bool(selected),
            "transaction": "VOFA", "program": "SAPL081F", "screen": "101"}


def _inspect_s4615_vtflc_new_header_form(session) -> dict[str, Any]:
    """Open only the empty VTFLC header form; never enter values or save."""
    session.validate_identity()
    before = inspect_screen(session)
    table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK"
    button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"
    if ((before.get("transaction"), before.get("program"), str(before.get("screen_number")))
            != ("VTFLC", "SAPL080W", "110") or before.get("popups")
            or not any(item.get("id") == table_id and item.get("type") == "GuiTableControl"
                       for item in before.get("tables", []))):
        raise ActionBlockedError("VTFLC new-header inspection requires exact header summary")
    button = session.find(button_id)
    tooltip = str(getattr(button, "Tooltip", ""))
    if (str(getattr(button, "Id", "")) != button_id
            or str(getattr(button, "Type", "")) != "GuiButton"
            or not tooltip.startswith("Nouvelles entr") or "(F5)" not in tooltip
            or not callable(getattr(button, "press", None))):
        raise ActionBlockedError("VTFLC New Entries button differs from observed control")
    session.audit("INSPECT_S4615_VTFLC_NEW_HEADER_FORM", control_id=button_id,
                  control_text="Nouvelles entrées", value="navigation_only")
    button.press()
    session.validate_identity()
    after = inspect_screen(session)
    if after.get("popups") or after.get("transaction") != "VTFLC":
        raise ActionBlockedError("VTFLC new-header navigation reached unexpected destination")
    return after


def _read_s4615_f2_lf_header_options(session) -> dict[str, Any]:
    """Read installed F2/LF header condition and item-number flag only."""
    session.validate_identity()
    snapshot = inspect_screen(session)
    if ((snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")))
            != ("VTFLC", "SAPL080W", "111") or snapshot.get("popups")):
        raise ActionBlockedError("F2/LF options require exact VTFLC header detail")
    prefix = "/app/con[0]/ses[0]/wnd[0]/usr/"
    fixed = {
        "billing_type": (prefix + "ctxtV_TVCPFLK-FKARN", "F2"),
        "delivery_type": (prefix + "ctxtV_TVCPFLK-LFARV", "LF"),
        "copy_requirement": (prefix + "ctxtV_TVCPFLK-GRBED", None),
        "copy_requirement_label": (prefix + "txtTEXT_BEDI", None),
        "copy_item_number": (prefix + "chkV_TVCPFLK-POSVO", None),
    }
    controls = {}
    for name, (control_id, expected_value) in fixed.items():
        control = session.find(control_id)
        if str(getattr(control, "Id", "")) != control_id:
            raise ActionBlockedError(f"F2/LF {name} control ID mismatch")
        if expected_value is not None and str(getattr(control, "Text", "")).strip() != expected_value:
            raise ActionBlockedError(f"F2/LF {name} value mismatch")
        controls[name] = control
    if str(getattr(controls["copy_item_number"], "Type", "")) != "GuiCheckBox":
        raise ActionBlockedError("F2/LF copy-item-number type mismatch")
    selected = getattr(controls["copy_item_number"], "Selected", None)
    if selected not in (True, False, -1, 0, 1):
        raise ActionBlockedError("F2/LF copy-item-number state unavailable")
    session.audit("READ_S4615_F2_LF_HEADER_OPTIONS", value="read_only")
    return {"billing_type": "F2", "delivery_type": "LF",
            "copy_requirement": str(getattr(controls["copy_requirement"], "Text", "")).strip(),
            "copy_requirement_label": str(getattr(controls["copy_requirement_label"], "Text", "")).strip(),
            "copy_item_number": bool(selected)}


def _inspect_s4615_vtflc_new_item_form(session, *, parent: str = "F2") -> dict[str, Any]:
    """Open a blank item form under the observed F2/LF reference; no writes."""
    session.validate_identity()
    before = inspect_screen(session)
    prefix = "/app/con[0]/ses[0]/wnd[0]"
    table_id = prefix + "/usr/tblSAPL080WTCTRL_V_TVCPFLP"
    button_id = prefix + "/tbar[1]/btn[5]"
    if ((before.get("transaction"), before.get("program"), str(before.get("screen_number")))
            != ("VTFLC", "SAPL080W", "112") or before.get("popups")
            or not any(item.get("id") == table_id and item.get("type") == "GuiTableControl"
                       for item in before.get("tables", []))):
        raise ActionBlockedError("VTFLC new-item inspection requires exact item summary")
    if parent not in {"F2", "ZF01"}:
        raise ActionBlockedError("VTFLC new-item parent is not allowlisted")
    for field, expected in (("FKARN", parent), ("LFARV", "LF")):
        control_id = prefix + "/usr/ctxtV_TVCPFLP-" + field
        control = session.find(control_id)
        if (str(getattr(control, "Id", "")) != control_id
                or str(getattr(control, "Text", "")).strip() != expected):
            raise ActionBlockedError("VTFLC new-item parent mismatch")
    button = session.find(button_id)
    tooltip = str(getattr(button, "Tooltip", ""))
    if (str(getattr(button, "Id", "")) != button_id
            or str(getattr(button, "Type", "")) != "GuiButton"
            or not tooltip.startswith("Nouvelles entr") or "(F5)" not in tooltip
            or not callable(getattr(button, "press", None))):
        raise ActionBlockedError("VTFLC new-item button differs from observed control")
    session.audit("INSPECT_S4615_VTFLC_NEW_ITEM_FORM", control_id=button_id,
                  control_text="Nouvelles entrées", value="navigation_only")
    button.press()
    session.validate_identity()
    after = inspect_screen(session)
    if (after.get("popups") or after.get("transaction") != "VTFLC"
            or after.get("program") != "SAPL080W"
            or str(after.get("screen_number")) != "113"):
        raise ActionBlockedError("VTFLC new-item navigation reached unexpected destination")
    fields = {field.get("id"): str(field.get("text") or "").strip()
              for field in after.get("input_fields", [])}
    if (fields.get(prefix + "/usr/ctxtV_TVCPFLP-FKARN") != parent
            or fields.get(prefix + "/usr/ctxtV_TVCPFLP-LFARV") != "LF"):
        raise ActionBlockedError("VTFLC new-item form parent changed")
    return after


def execute_read_action(session, request: dict[str, Any]) -> Any:
    action = request["action"]
    if action == "READ_PHASE5_TRANSPORT_OVERVIEW":
        session.audit(action)
        before = inspect_screen(session)
        if (before["transaction"], before["program"], before["screen_number"]) != ("SE09", "RDDM0001", "100") or before["popups"]:
            raise ActionBlockedError("Transport read requires exact SE09 overview without popups")
        prefix = "/app/con[0]/ses[0]/wnd[0]/usr/subCOMMONSUBSCREEN:RDDM0001:0220"
        user = session.find(prefix + "/ctxtTRDYSE01CM-USERNAME")
        button = session.find(prefix + "/btn%_AUTOTEXT028")
        if (str(getattr(user, "Type", "")) != "GuiCTextField"
                or str(getattr(user, "Text", "")) != "ABDELJ"
                or str(getattr(button, "Type", "")) != "GuiButton"
                or str(getattr(button, "Text", "")).strip() != "Afficher"):
            raise ActionBlockedError("SE09 transport display control mismatch")
        button.press()  # Observed SE09 display-only button; no release or save.
        session.validate_identity()
        return inspect_screen(session)
    if action == "READ_PHASE5_CHANGE_LOG":
        table = request["params"]["table"]
        date = request["params"]["date"]
        session.audit(action, value=table)
        before = inspect_screen(session)
        if (before["transaction"], before["program"], before["screen_number"]) != ("SCU3", "RSVTPROT", "1000") or before["popups"]:
            raise ActionBlockedError("Change-log read requires the exact SCU3 selection screen without popups")
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        field = session.find(prefix + "/usr/ctxtCUSOBJ-LOW")
        tables_radio = session.find(prefix + "/usr/radTABFIRST")
        start = session.find(prefix + "/usr/ctxtDBEG")
        end = session.find(prefix + "/usr/ctxtDEND")
        execute = session.find(prefix + "/tbar[1]/btn[8]")
        if (str(getattr(field, "Type", "")) != "GuiCTextField"
                or str(getattr(tables_radio, "Type", "")) != "GuiRadioButton"
                or (str(getattr(start, "Text", "")), str(getattr(end, "Text", ""))) not in {
                    ("12.10.2026", "18.10.2026"),
                    ("16.10.2026", "16.10.2026"),
                    ("14.10.2026", "14.10.2026"),
                }
                or str(getattr(execute, "Type", "")) != "GuiButton"
                or not str(getattr(execute, "Text", "")).startswith(("Exécuter", "ExÃ©cuter"))):
            raise ActionBlockedError("SCU3 selection control mismatch")
        tables_radio.select()  # Select table-log search mode, not business data.
        field.Text = table  # Read-only SCU3 search criterion.
        start.Text = date
        end.Text = date
        execute.press()  # Exact observed SCU3 Execute (F8), not a Save.
        session.validate_identity()
        return inspect_screen(session)
    if action == "INSPECT_BP_STANDARD_ADDRESS":
        from src.provisioning.s4615_bp_address_gui import inspect_form
        session.audit(action)
        return inspect_form(session)
    if action == "INSPECT_S4600_T_S50A01_BP_ADDRESS":
        from src.provisioning.s4600_t_s50a01_bp_address_gui import inspect_form
        session.audit(action)
        return inspect_form(session)
    if action == "POSITION_S4600_T_S50A01_BP":
        from src.provisioning.s4600_t_s50a01_bp_address_gui import position_search
        return position_search(session)
    if action == "OPEN_S4600_T_S50A01_BP":
        from src.provisioning.s4600_t_s50a01_bp_address_gui import open_exact_partner
        return open_exact_partner(session)
    if action == "CONFIRM_OPEN_S4600_T_S50A01_BP":
        from src.provisioning.s4600_t_s50a01_bp_address_gui import confirm_open_exact_partner
        return confirm_open_exact_partner(session)
    if action == "STATUS":
        return session.status()
    if action == "INSPECT":
        return inspect_screen(session)
    if action == "READ_STATUS_BAR":
        return _status_bar(session)
    if action == "READ_SCREEN":
        return _read_screen(session)
    if action == "READ_S4615_ZF01_ACCOUNTING_BLOCK":
        return _read_s4615_zf01_accounting_block(session)
    if action == "INSPECT_S4615_VTFLC_NEW_HEADER_FORM":
        return _inspect_s4615_vtflc_new_header_form(session)
    if action == "READ_S4615_F2_LF_HEADER_OPTIONS":
        return _read_s4615_f2_lf_header_options(session)
    if action == "INSPECT_S4615_VTFLC_NEW_ITEM_FORM":
        return _inspect_s4615_vtflc_new_item_form(session)
    if action == "INSPECT_S4615_VTFLC_NEW_TARGET_ITEM_FORM":
        return _inspect_s4615_vtflc_new_item_form(session, parent="ZF01")
    if action == "OPEN_TRANSACTION":
        open_transaction(session, request["params"]["transaction"])
        return session.status()
    if action == "OPEN_S4615_CUSTOMIZING_READ":
        transaction = request["params"]["transaction"]
        session.audit(action, value=transaction)
        open_transaction(session, transaction)
        return inspect_screen(session)
    if action == "INSPECT_S4615_CUSTOMIZING":
        target = request["params"]["object"]
        transaction = "OVL2" if target == "OVL2" else "SE16N"
        session.audit(action, value=target)
        snapshot = inspect_screen(session)
        if snapshot["transaction"] != transaction or snapshot["popups"]:
            raise ActionBlockedError("S4615 inspection requires the exact read-only transaction without popups")
        if target != "OVL2":
            observed = [snapshot["window_title"]] + [
                str(field.get("text") or "") for field in snapshot["input_fields"] + snapshot["labels"]
            ]
            if target not in observed and not any(target in value.split() for value in observed):
                raise ActionBlockedError(f"S4615 inspection cannot prove the current SE16N table is {target}")
        return {
            "object": target,
            "transaction": snapshot["transaction"],
            "program": snapshot["program"],
            "screen_number": snapshot["screen_number"],
            "window_title": snapshot["window_title"],
            "status_bar": snapshot["status_bar"],
            "tables": snapshot["tables"],
            "truncated": snapshot["truncated"],
            "complete_dataset_proven": False,
        }
    if action == "READ_S4615_CUSTOMIZING_TABLE":
        table = request["params"]["table"]
        session.audit(action, value=table)
        open_transaction(session, "SE16N")
        before = inspect_screen(session)
        if (before["transaction"] != "SE16N" or before["program"] != "SAPLSE16N"
                or before["screen_number"] != "120" or before["popups"]):
            raise ActionBlockedError("S4615 table read requires exact SE16N/SAPLSE16N/120 without popup")
        field_id = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtGD-TAB"
        edit_id = "/app/con[0]/ses[0]/wnd[0]/usr/chkGD-EDIT"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[8]"
        menu_id = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[0]/menu[0]"
        field = session.find(field_id)
        edit = session.find(edit_id)
        if str(getattr(edit, "Type", "")) == "GuiCheckBox" and getattr(edit, "Selected", None) in (True, -1):
            edit.Selected = False  # Exact SE16N display-mode flag; no business data is changed.
            field = session.find(field_id)
            edit = session.find(edit_id)
        try:
            execute_control = session.find(menu_id)
            execute_kind = "menu"
        except Exception:
            execute_control = session.find(button_id)
            execute_kind = "button"
        if (str(getattr(field, "Type", "")) != "GuiCTextField"
                or str(getattr(edit, "Type", "")) != "GuiCheckBox"
                or getattr(edit, "Selected", None) not in (False, 0)
                or (execute_kind == "button" and (
                    str(getattr(execute_control, "Type", "")) != "GuiButton"
                    or not str(getattr(execute_control, "Tooltip", "")).casefold().startswith("en ligne")))
                or (execute_kind == "menu" and (
                    str(getattr(execute_control, "Type", "")) != "GuiMenu"
                    or str(getattr(execute_control, "Text", "")).casefold() != "en ligne"))):
            raise ActionBlockedError(
                "S4615 SE16N read control mismatch: "
                f"field_type={getattr(field, 'Type', None)!r}, "
                f"edit_type={getattr(edit, 'Type', None)!r}, "
                f"edit_selected={getattr(edit, 'Selected', None)!r}, "
                f"execute_kind={execute_kind!r}, "
                f"execute_type={getattr(execute_control, 'Type', None)!r}, "
                f"execute_label={getattr(execute_control, 'Text' if execute_kind == 'menu' else 'Tooltip', None)!r}"
            )
        current = str(getattr(field, "Text", "") or "")
        if current and current not in {"T000", "T001W", "T001K", "TVKWZ", "TVSWZ", "TVST"}:
            raise ActionBlockedError("S4615 SE16N table field contains an unrelated value")
        field.Text = table  # Exact SE16N search criterion only; never a business-data field.
        if execute_kind == "button":
            execute_control.press()  # Exact observed read-only En ligne (F8).
        else:
            execute_control.select()  # Exact observed read-only En ligne menu.
        session.validate_identity()
        after = inspect_screen(session)
        return {
            "table": table,
            "transaction": after["transaction"],
            "program": after["program"],
            "screen_number": after["screen_number"],
            "window_title": after["window_title"],
            "status_bar": after["status_bar"],
            "popups": after["popups"],
            "input_fields": after["input_fields"],
            "labels": after["labels"],
            "tables": after["tables"],
            "truncated": after["truncated"],
            "complete_dataset_proven": False,
        }
    if action == "SCAN_S4615_CUSTOMIZING":
        return scan_s4615_customizing(session, request["params"]["object"])
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
    if action == "DISPLAY_S4600_CDCL_REFERENCE":
        return display_s4615_sales_reference(session, request["params"])
    if action == "FIND_S4650_BILLING_COPY_HEADER":
        return find_s4650_billing_copy_header(session, request["params"])
    if action == "FIND_S4615_ZF01_LF_COPY_HEADER":
        return find_s4650_billing_copy_header(session, request["params"])
    if action == "DISPLAY_S4650_BILLING_COPY_HEADER":
        return display_s4650_billing_copy_header(session, request["params"])
    if action == "DISPLAY_S4615_ZF01_LF_COPY_HEADER":
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
