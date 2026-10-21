"""Phase 5 backend for the local SAP GUI filesystem bridge.

The backend is deliberately transport-only: SAP GUI COM remains isolated in
the manually launched local runner.  Every call is one validated Phase 5
request and no failed/ambiguous request is retried.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Callable
import unicodedata

from src.sap_gui_bridge.connection import EXPECTED_CLIENT, EXPECTED_SYSTEM, EXPECTED_USER
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import (
    COMPANY_CODE_TABLE_SEARCH,
    COMPANY_CODE_TABLE_VARIANTS,
    PHASE5_ASSIGNMENT_TABLE_SEARCHES,
    SALES_ORGANIZATION_ACTIVITY,
    SALES_ORGANIZATION_DISPLAY_EXCEPTION,
    SALES_ORGANIZATION_TABLE_SEARCH,
    find_company_code_table_value,
    find_phase5_assignment_table_row,
    find_sales_organization_table_value,
    find_s4615_billing_type,
    display_s4615_f2_reference,
    find_s4615_sales_type,
    display_s4615_sales_reference,
    back,
    navigate,
    open_transaction,
    select_company_code_display_activity,
    select_sales_organization_activity,
)
from src.sap_gui_bridge.protocol import enqueue_request, wait_for_response


EXPECTED_TARGETS: dict[str, dict[str, Any]] = {
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
        "partner_id": "C615-D00", "company_code": "1010",
        "sales_area": "1010/10/00",
    },
    "PRODUCT_P615_400": {
        "material_id": "P615-400", "sales_organization": "1010",
        "distribution_channel": "10", "unit": "PC",
    },
    "VOV4_ITEM_CATEGORY_DETERMINATION": {"contract_id": "S4615_BV_CB04"},
    "ENSURE_BP_STANDARD_ADDRESS": {"logical_id": "C615-A01", "sap_id": "1000000115"},
    "S4600_T_S50A01_BP_ADDRESS": {"logical_id": "T-S50A01", "sap_id": "1000000116"},
}

VOV4_CONTRACTS_PATH = Path(__file__).resolve().parents[2] / "config" / "sap_gui_vov4_contracts.json"

EXPECTED_TEMPLATES = {
    "COMPANY_CODE_1010": "BE01",
    "SALES_ORGANIZATION_1010": "1710",
    "CUSTOMER_C615_D00": "17100002",
    "PRODUCT_P615_400": "FG228",
}
SALES_ORGANIZATION_SAVE_MENU = (
    "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[5]"
)
SALES_ORGANIZATION_OVERVIEW_TITLE = (
    'Modifier vue "Organisations commerciales" : synth\u00e8se'
)
# Exact evidenced Customizing transport-request dialog observed live after the
# Sales Organization Save (capture 7defef2f). Used only to name the boundary
# precisely; transport handling and release are never automatic.
SALES_ORGANIZATION_TRANSPORT_POPUP_TITLE = "Demande : ordre du Customizing"
SALES_ORGANIZATION_TRANSPORT_FIELD = (
    "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR"
)
SALES_ORGANIZATION_TRANSPORT_CONTINUE = (
    "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
)

# Exact controls from the recording and observed V_T001 screen. Controls
# without capture or screen evidence are intentionally not synthesized.
COMPANY_CODE_VBS_CONTROLS = {
    "easy_access_tree": "wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell",
    "img_button": "wnd[0]/tbar[1]/btn[5]",
    "img_tree": "wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell",
    "activity_table_cell": "wnd[1]/usr/tblSAPLDSYHTCODES/txtI_TSTCT-TTEXT[1,0]",
    "activity_select": "wnd[1]/tbar[0]/btn[2]",
    "copy_menu": "wnd[0]/mbar/menu[1]/menu[3]",
    "copy_button": "wnd[0]/tbar[1]/btn[6]",
    "copy_source": "wnd[1]/usr/sub:SAPLSPO4:0300/ctxtSVALD-VALUE[0,21]",
    "copy_target": "wnd[1]/usr/sub:SAPLSPO4:0300/ctxtSVALD-VALUE[1,21]",
    "popup_no": "wnd[1]/usr/btnSPOP-OPTION2",
    "popup_ack": "wnd[1]/tbar[0]/btn[0]",
    "number_ranges_no": "wnd[1]/usr/btnBUTTON_2",
    "transport_cancel": "wnd[1]/tbar[0]/btn[12]",
    "company_name": "wnd[0]/usr/txtV_T001-BUTXT",
    "currency": "wnd[0]/usr/ctxtV_T001-WAERS",
    "language": "wnd[0]/usr/ctxtV_T001-SPRAS",
}
COMPANY_CODE_IMG_ROOT_TEXT = "Guide d'implémentation SAP Customizing"
COMPANY_CODE_IMG_PARENT_PATH = (
    "Structure de l'entreprise",
    "Définition",
    "Comptabilité financière",
)
COMPANY_CODE_IMG_LEAF_TEXT = "Traiter, copier, supprimer, contrôler société"
COMPANY_CODE_IMG_TEXT_COLUMN = "TEXT"
COMPANY_CODE_IMG_LINK_COLUMN = "2"
COMPANY_CODE_IMG_TEXT_ITEM_TYPE = "2"
COMPANY_CODE_IMG_LINK_ITEM_TYPE = "5"
SALES_ORGANIZATION_IMG_NODES = (
    ("02  1      6", "Structure de l'entreprise"),
    ("03  2      1", "Définition"),
    ("04  3      4", "Administration des ventes (ADV)"),
)
SALES_ORGANIZATION_IMG_LEAF = (
    "05  4      1",
    SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
    "2",
)
ASSIGNMENT_IMG_NODES = (
    ("02  1      6", "Structure de l'entreprise"),
    ("03  2      2", "Affectation"),
    ("04  3      4", "Administration des ventes (ADV)"),
)
ASSIGNMENT_IMG_LEAVES = {
    "SALES_ORG_1010_TO_COMPANY_CODE_1010": (
        "05  4      1",
        "Affecter organisation commerciale à société",
    ),
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": (
        "05  4      2",
        "Affecter canal de distribution à organisation commerciale",
    ),
    "DIVISION_00_TO_SALES_ORG_1010": (
        "05  4      3",
        "Affecter secteur d'activité à organisation commerciale",
    ),
}
COMPANY_CODE_TRANSPORT_DESCRIPTION = "S4615 Training Setup"
COMPANY_CODE_TRANSPORT_REQUEST = "A4HK908422"
COMPANY_CODE_TRANSPORT_POPUP_TITLE = "Demande : ordre du Customizing"
COMPANY_CODE_TARGET_FIELD = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T001-BUKRS"
COMPANY_CODE_SAVE_CONTROL = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
COMPANY_CODE_SAVE_MENU = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[5]"
COMPANY_CODE_ADDRESS_CONTINUE = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
COMPANY_CODE_ADDRESS_TITLE = "Traiter l'adresse:  1010"
COMPANY_CODE_ADDRESS_COUNTRY = (
    "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY"
)
COMPANY_CODE_TEMPLATE_COUNTRY = "BE"
COMPANY_CODE_COUNTRY_REQUIRED_MESSAGE = (
    'Renseignez la zone obligatoire "Pays/Région".'
)
COMPANY_CODE_TARGET_SCREEN = {
    "transaction": "V_T001",
    "program": "SAPL0ORG",
    "screen_number": "41",
    "window_title": 'Modifier vue "SociÃ©tÃ©" : dÃ©tail ensemble de sÃ©lection',
}

COMPANY_CODE_TARGET_TITLES = {
    COMPANY_CODE_TARGET_SCREEN["window_title"],
    'Modifier vue "Soci\u00e9t\u00e9" : d\u00e9tail ensemble de s\u00e9lection',
    'Modifier vue "Soci�t�" : d�tail ensemble de s�lection',
}


def _is_company_code_target_screen(snapshot: dict[str, Any]) -> bool:
    return (
        snapshot.get("transaction") == COMPANY_CODE_TARGET_SCREEN["transaction"]
        and snapshot.get("program") == COMPANY_CODE_TARGET_SCREEN["program"]
        and str(snapshot.get("screen_number") or "").lstrip("0") == "41"
        and snapshot.get("window_title") in COMPANY_CODE_TARGET_TITLES
    )


def _wait_not_busy(session: Any, attempts: int = 100) -> None:
    import time

    for _ in range(attempts):
        if not bool(getattr(session.raw, "Busy", False)):
            return
        time.sleep(0.05)
    raise ActionBlockedError("SAP GUI remained busy")


def _press_exact(session: Any, control_id: str) -> None:
    control = session.find(control_id)
    control_type = str(getattr(control, "Type", ""))
    if control_type and control_type != "GuiButton":
        raise ActionBlockedError(f"Recorded button type mismatch: {control_id}")
    press = getattr(control, "press", None) or getattr(control, "Press", None)
    if not callable(press):
        raise ActionBlockedError(f"Recorded button is not pressable: {control_id}")
    press()
    _wait_not_busy(session)


def _vov4_contract(contract_id: str) -> dict[str, Any]:
    document = json.loads(VOV4_CONTRACTS_PATH.read_text(encoding="utf-8"))
    contract = (document.get("contracts") or {}).get(contract_id)
    if not isinstance(contract, dict) or contract.get("scope") != "S4615":
        raise ActionBlockedError(f"VOV4 contract is not allowlisted: {contract_id}")
    return contract


def _fold_sap_text(value: Any) -> str:
    """Fold accented SAP text and repair the observed UTF-8/Latin-1 mojibake."""
    text = str(value or "")
    if "Ã" in text or "Â" in text:
        try:
            text = text.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    text = unicodedata.normalize("NFKD", text)
    return "".join(char for char in text if not unicodedata.combining(char)).casefold()


def _vov4_context(session: Any, contract: dict[str, Any], *, screen: str) -> None:
    session.validate_identity()
    info = getattr(getattr(session, "raw", None), "Info", None)
    if (
        str(session.identity.get("transaction") or "").upper() != contract["transaction"]
        or str(getattr(info, "Program", "") or "").upper() != contract["program"]
        or str(getattr(info, "ScreenNumber", "") or "").lstrip("0")
        != str(screen).lstrip("0")
    ):
        raise ActionBlockedError("VOV4 transaction/program/screen contract mismatch")


def _vov4_read_visible_row(
    session: Any, contract: dict[str, Any], relative_row: int
) -> dict[str, str]:
    values: dict[str, str] = {}
    for logical_name, field in contract["fields"].items():
        control_id = (
            f"{contract['table_id']}/ctxtV_T184-{field['name']}"
            f"[{field['column']},{relative_row}]"
        )
        control = session.find(control_id)
        if str(getattr(control, "Type", "")) != "GuiCTextField":
            raise ActionBlockedError(f"VOV4 cell type mismatch: {control_id}")
        values[logical_name] = str(getattr(control, "Text", "") or "").strip()
    return values


def _scan_vov4_rows(session: Any, contract: dict[str, Any]) -> dict[str, Any]:
    """Read all T184 rows by bounded pages; never modifies a cell."""
    _vov4_context(session, contract, screen=contract["overview_screen"])
    table = session.find(contract["table_id"])
    if str(getattr(table, "Type", "")) != "GuiTableControl":
        raise ActionBlockedError("VOV4 table type mismatch")
    row_count = int(getattr(table, "RowCount", 0))
    visible_count = int(getattr(table, "VisibleRowCount", 0))
    scrollbar = getattr(table, "VerticalScrollbar", None)
    if row_count < 1 or visible_count < 1 or scrollbar is None:
        raise ActionBlockedError("VOV4 table dimensions are not observable")
    maximum = int(getattr(scrollbar, "Maximum", max(0, row_count - visible_count)))
    scrollbar.Position = 0
    _wait_not_busy(session)
    visited: set[int] = set()
    matches: dict[str, list[int]] = {"source": [], "target": []}
    stalled = False
    while True:
        table = session.find(contract["table_id"])
        scrollbar = getattr(table, "VerticalScrollbar", None)
        position = int(getattr(scrollbar, "Position", 0))
        page_rows = min(visible_count, max(0, row_count - position))
        for relative in range(page_rows):
            absolute = position + relative
            values = _vov4_read_visible_row(session, contract, relative)
            visited.add(absolute)
            for name in ("source", "target"):
                if values == contract[name]:
                    matches[name].append(absolute)
        # One exact row proves existence. A complete scan is required only
        # when proving that the target is missing.
        if matches["target"]:
            break
        if position >= maximum:
            break
        next_position = min(position + visible_count, maximum)
        scrollbar.Position = next_position
        _wait_not_busy(session)
        table = session.find(contract["table_id"])
        observed = int(getattr(table.VerticalScrollbar, "Position", position))
        if observed <= position:
            stalled = True
            break
    return {
        "row_count": row_count,
        "rows_read": len(visited),
        "complete": not stalled and len(visited) >= row_count,
        "source_rows": sorted(set(matches["source"])),
        "target_rows": sorted(set(matches["target"])),
    }


def _lookup_vov4(session: Any, contract: dict[str, Any]) -> dict[str, Any]:
    scan = _scan_vov4_rows(session, contract)
    if len(scan["target_rows"]) == 1:
        state = "EXISTS"
    elif scan["complete"] and not scan["target_rows"]:
        state = "MISSING"
    else:
        state = "UNKNOWN"
    return {"state": state, "evidence": scan}


def _vov4_copy_form_values(snapshot: dict[str, Any], contract: dict[str, Any]) -> dict[str, str]:
    observed = {item.get("id"): item for item in snapshot.get("input_fields") or []}
    values: dict[str, str] = {}
    for logical_name, field in contract["fields"].items():
        control_id = f"/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T184-{field['name']}"
        item = observed.get(control_id)
        if (
            not item
            or item.get("type") != "GuiCTextField"
            or item.get("changeable") is not True
            or item.get("visible") is not True
        ):
            raise ActionBlockedError(f"VOV4 copy-form field mismatch: {control_id}")
        values[logical_name] = str(item.get("text") or "").strip()
    return values


def _save_vov4_pending_row(
    session: Any,
    contract: dict[str, Any],
    *,
    require_copy_status: bool = True,
) -> dict[str, Any]:
    before = inspect_screen(session)
    if before.get("popups"):
        raise ActionBlockedError("VOV4 Save requires a popup-free overview")
    matching = []
    for table in before.get("tables") or []:
        if table.get("id") != contract["table_id"]:
            continue
        for row in table.get("visible_rows") or []:
            values = {
                logical: next(
                    (
                        str(value.get("text") or "").strip()
                        for value in row.get("values") or []
                        if str(value.get("column")) == str(field["column"])
                    ),
                    "",
                )
                for logical, field in contract["fields"].items()
            }
            if values == contract["target"]:
                matching.append(row)
    status_text = _fold_sap_text((before.get("status_bar") or {}).get("text"))
    if len(matching) != 1 or (require_copy_status and "entrees copi" not in status_text):
        raise ActionBlockedError("VOV4 exact unsaved copied target row is not uniquely evidenced")
    _press_exact(session, contract["save_button_id"])
    saved = inspect_screen(session)
    transport_used = None
    popups = saved.get("popups") or []
    if popups:
        if len(popups) != 1 or popups[0].get("window_title") != COMPANY_CODE_TRANSPORT_POPUP_TITLE:
            return {"unexpected_popup": True, "popup_details": popups}
        popup = popups[0]
        editable = [item for item in popup.get("input_fields") or [] if item.get("changeable") is True]
        buttons = [item for item in popup.get("buttons") or [] if item.get("id") == SALES_ORGANIZATION_TRANSPORT_CONTINUE]
        if (
            len(editable) != 1
            or editable[0].get("id") != SALES_ORGANIZATION_TRANSPORT_FIELD
            or editable[0].get("type") != "GuiCTextField"
            or len(buttons) != 1
        ):
            return {"transport_request": True, "reason": "VOV4 transport popup contract changed"}
        field = session.find(SALES_ORGANIZATION_TRANSPORT_FIELD)
        setattr(field, "Text", contract["transport_request"])
        _press_exact(session, SALES_ORGANIZATION_TRANSPORT_CONTINUE)
        saved = inspect_screen(session)
        if saved.get("popups"):
            return {"transport_request": True, "reason": "approved transport was rejected"}
        transport_used = contract["transport_request"]
    status = saved.get("status_bar") or {}
    if str(status.get("message_type") or "").upper() in {"E", "A"}:
        return {"ambiguous_save": True, "reason": str(status.get("text") or "SAP Save error")}
    open_transaction(session, "VOV4")
    readback = _lookup_vov4(session, contract)
    if readback["state"] != "EXISTS":
        return {"ambiguous_save": True, "reason": "VOV4 independent readback did not find target", "readback": readback}
    return {
        "accepted": True,
        "target": contract["target"],
        "transport_request_id": transport_used,
        "readback": readback,
    }


def _provision_vov4(
    session: Any,
    contract: dict[str, Any],
    *,
    resume_exact_pending_row: bool = False,
) -> dict[str, Any]:
    _vov4_context(session, contract, screen=contract["overview_screen"])
    current = inspect_screen(session)
    if "entrees copi" in _fold_sap_text((current.get("status_bar") or {}).get("text")):
        return _save_vov4_pending_row(session, contract)
    if resume_exact_pending_row:
        return _save_vov4_pending_row(
            session,
            contract,
            require_copy_status=False,
        )
    lookup = _lookup_vov4(session, contract)
    if lookup["state"] == "EXISTS":
        return {"accepted": True, "already_present": True, "target": contract["target"]}
    if lookup["state"] != "MISSING" or len(lookup["evidence"]["source_rows"]) != 1:
        raise ActionBlockedError("VOV4 source/target lookup is incomplete or ambiguous")
    source_row = lookup["evidence"]["source_rows"][0]
    table = session.find(contract["table_id"])
    row = table.GetAbsoluteRow(source_row)
    setattr(row, "Selected", True)
    if getattr(row, "Selected", False) is not True:
        raise ActionBlockedError("VOV4 source row selection failed")
    _press_exact(session, contract["copy_button_id"])
    copy_screen = inspect_screen(session)
    _vov4_context(session, contract, screen=contract["copy_screen"])
    if _vov4_copy_form_values(copy_screen, contract) != contract["source"]:
        raise ActionBlockedError("VOV4 copy form does not match approved source")
    target_field = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T184-AUART"
    _set_exact_text(session, target_field, contract["target"]["sales_document_type"])
    entered = inspect_screen(session)
    if _vov4_copy_form_values(entered, contract) != contract["target"]:
        raise ActionBlockedError("VOV4 copy form changed outside the approved target field")
    session.audit(
        "PHASE5_OPERATION",
        value={"operation": "VOV4_ITEM_CATEGORY_DETERMINATION", "step": "ACCEPT_COPY_FORM"},
    )
    session.find("wnd[0]").sendVKey(0)
    _wait_not_busy(session)
    return _save_vov4_pending_row(session, contract)


def _set_exact_text(session: Any, control_id: str, value: str) -> None:
    control = session.find(control_id)
    if not bool(getattr(control, "Changeable", getattr(control, "Editable", True))):
        raise ActionBlockedError(f"Recorded field is not editable: {control_id}")
    setattr(control, "Text", value)


def _company_code_provision_step(
    session: Any,
    step: str,
    control_id: str,
    action: Callable[[], Any],
    *,
    phase: str = "PROVISION",
) -> Any:
    try:
        action()
    except Exception as exc:
        identity = session.identity
        observed_transaction = str(identity.get("transaction") or "")
        observed_program = str(
            getattr(getattr(session.raw, "Info", None), "Program", "") or ""
        )
        raise ActionBlockedError(
            f"COMPANY_CODE_1010 {phase} "
            f"step={step} expected_transaction=V_T001 "
            "expected_program=SAPL0ORG "
            f"control_id={control_id} "
            f"observed_transaction={observed_transaction or 'UNKNOWN'} "
            f"observed_program={observed_program or 'UNKNOWN'} "
            f"cause={type(exc).__name__}: {exc}"
        ) from exc
    return None


def _control_children(control: Any) -> list[Any]:
    try:
        children = control.Children
        return [children(index) for index in range(int(children.Count))]
    except Exception:
        return []


def _editable_transport_fields(window: Any) -> list[Any]:
    fields: list[Any] = []
    pending = _control_children(window)
    while pending:
        control = pending.pop(0)
        pending.extend(_control_children(control))
        control_type = str(getattr(control, "Type", ""))
        editable = bool(
            getattr(control, "Changeable", False)
            or getattr(control, "Editable", False)
        )
        if control_type in {"GuiCTextField", "GuiTextField"} and editable:
            fields.append(control)
    return fields


def _reuse_company_code_transport(session: Any) -> dict[str, Any]:
    """Select the one approved unreleased request; never create or release one."""
    try:
        window = session.find("wnd[1]")
    except Exception as exc:
        return {
            "transport_request": True,
            "reason": "Customizing request popup is not observable",
        }
    if str(getattr(window, "Text", "")) != COMPANY_CODE_TRANSPORT_POPUP_TITLE:
        return {
            "unexpected_popup": True,
            "reason": f"unexpected popup at transport boundary: {getattr(window, 'Text', '')!r}",
        }
    fields = _editable_transport_fields(window)
    if len(fields) != 1:
        return {
            "transport_request": True,
            "reason": "Customizing request popup does not expose exactly one editable order field",
        }
    setattr(fields[0], "Text", COMPANY_CODE_TRANSPORT_REQUEST)
    _press_exact(session, COMPANY_CODE_VBS_CONTROLS["popup_ack"])

    try:
        follow_up = session.find("wnd[1]")
    except Exception:
        follow_up = None
    if follow_up is not None:
        follow_up_title = str(getattr(follow_up, "Text", ""))
        if follow_up_title == COMPANY_CODE_TRANSPORT_POPUP_TITLE:
            return {
                "transport_request": True,
                "request": COMPANY_CODE_TRANSPORT_REQUEST,
                "reason": "approved request was rejected or is not modifiable",
            }
        # The recording acknowledges one informational popup after transport.
        try:
            _press_exact(session, COMPANY_CODE_VBS_CONTROLS["popup_ack"])
        except Exception as exc:
            return {
                "unexpected_popup": True,
                "reason": f"unexpected post-transport popup: {type(exc).__name__}",
            }
        try:
            remaining = session.find("wnd[1]")
        except Exception:
            remaining = None
        if remaining is not None:
            return {
                "unexpected_popup": True,
                "reason": "popup remains after the recorded post-transport acknowledgement",
            }
    return {
        "accepted": True,
        "transport_request_id": COMPANY_CODE_TRANSPORT_REQUEST,
        "transport_description": COMPANY_CODE_TRANSPORT_DESCRIPTION,
        "transport_released": False,
    }


def _open_company_code_screen_from_vbs(session: Any) -> None:
    """Replay only the recorded navigation needed to reach V_T001."""
    transaction = str(session.identity.get("transaction") or "").upper()
    if transaction == "V_T001":
        return
    if transaction not in {"SPRO", "SIMG", "SMEN", "SESSION_MANAGER", ""}:
        raise ActionBlockedError(
            f"COMPANY_CODE_1010 cannot start from transaction {transaction!r}"
        )
    if transaction not in {"SPRO", "SIMG"}:
        tree = session.find(COMPANY_CODE_VBS_CONTROLS["easy_access_tree"])
        tree.SelectNode("F00012")
        tree.DoubleClickNode("F00012")
        _wait_not_busy(session)
        transaction = str(session.identity.get("transaction") or "").upper()
    if transaction == "SIMG":
        info = getattr(getattr(session, "raw", None), "Info", None)
        current_program = str(getattr(info, "Program", "") or "").upper()
        if current_program and current_program != "SAPLSHI01":
            open_transaction(session, "SPRO")
            transaction = str(session.identity.get("transaction") or "").upper()
    if transaction == "SPRO":
        _press_exact(session, COMPANY_CODE_VBS_CONTROLS["img_button"])

    def observed_img_tree() -> tuple[dict[str, Any], Any, str]:
        snapshot = inspect_screen(session)
        if (
            str(snapshot.get("transaction") or "").upper() != "SIMG"
            or str(snapshot.get("program") or "").upper() != "SAPLSHI01"
            or snapshot.get("window_title") != "Afficher guide d'implémentation"
        ):
            raise ActionBlockedError(
                "Company-code IMG navigation requires the observed "
                "SIMG / SAPLSHI01 implementation-guide screen; "
                f"observed transaction={snapshot.get('transaction')!r}, "
                f"program={snapshot.get('program')!r}, "
                f"title={snapshot.get('window_title')!r}"
            )
        tree_id = "/app/con[0]/ses[0]/" + COMPANY_CODE_VBS_CONTROLS["img_tree"]
        tree_snapshots = [
            item
            for item in snapshot.get("tree_controls", [])
            if item.get("id") == tree_id
        ]
        if (
            len(tree_snapshots) != 1
            or tree_snapshots[0].get("nodes_truncated")
            or tree_snapshots[0].get("extraction_error")
        ):
            raise ActionBlockedError(
                "Company-code IMG navigation requires one complete, "
                "readable implementation-guide tree"
            )
        nodes = tree_snapshots[0].get("nodes")
        if not isinstance(nodes, list):
            raise ActionBlockedError(
                "Company-code IMG navigation could not inspect the IMG tree nodes"
            )
        tree = session.find(COMPANY_CODE_VBS_CONTROLS["img_tree"])
        root_nodes = [
            node
            for node in nodes
            if node.get("parent_key") is None
            and node.get("text") == COMPANY_CODE_IMG_ROOT_TEXT
        ]
        if len(root_nodes) != 1 or not isinstance(root_nodes[0].get("key"), str):
            raise ActionBlockedError(
                "Company-code IMG navigation requires the exact observed "
                f"root {COMPANY_CODE_IMG_ROOT_TEXT!r}"
            )
        return tree_snapshots[0], tree, root_nodes[0]["key"]

    def exact_child(
        nodes: list[dict[str, Any]], parent_key: str, text: str
    ) -> dict[str, Any]:
        matches = [
            node
            for node in nodes
            if node.get("parent_key") == parent_key and node.get("text") == text
        ]
        if len(matches) != 1 or not isinstance(matches[0].get("key"), str):
            raise ActionBlockedError(
                "Company-code IMG path requires one exact child "
                f"{text!r} under observed parent key {parent_key!r}; "
                f"found {len(matches)}"
            )
        text_item = next(
            (
                item
                for item in matches[0].get("items", [])
                if item.get("column") == COMPANY_CODE_IMG_TEXT_COLUMN
            ),
            None,
        )
        if (
            text_item is None
            or text_item.get("type") != COMPANY_CODE_IMG_TEXT_ITEM_TYPE
            or text_item.get("text") != text
        ):
            raise ActionBlockedError(
                f"Company-code IMG node {text!r} lacks the observed "
                "TEXT/type-2 item contract"
            )
        return matches[0]

    tree_snapshot, tree, root_key = observed_img_tree()
    tree.TopNode = root_key
    parent_key = root_key
    for parent_text in COMPANY_CODE_IMG_PARENT_PATH:
        node = exact_child(tree_snapshot["nodes"], parent_key, parent_text)
        direct_children_loaded = any(
            child.get("parent_key") == node["key"]
            for child in tree_snapshot["nodes"]
        )
        if not direct_children_loaded:
            tree.ExpandNode(node["key"])
            _wait_not_busy(session)
            tree.TopNode = root_key
            tree_snapshot, tree, _ = observed_img_tree()
        parent_key = node["key"]

    leaf = exact_child(
        tree_snapshot["nodes"], parent_key, COMPANY_CODE_IMG_LEAF_TEXT
    )
    leaf_key = leaf["key"]
    link_item = next(
        (
            item
            for item in leaf.get("items", [])
            if item.get("column") == COMPANY_CODE_IMG_LINK_COLUMN
        ),
        None,
    )
    if (
        link_item is None
        or link_item.get("type") != COMPANY_CODE_IMG_LINK_ITEM_TYPE
    ):
        raise ActionBlockedError(
            "Company-code IMG leaf lacks the observed column-2/type-5 link contract"
        )
    tree.SelectItem(leaf_key, COMPANY_CODE_IMG_TEXT_COLUMN)
    tree.EnsureVisibleHorizontalItem(leaf_key, COMPANY_CODE_IMG_TEXT_COLUMN)
    tree.DoubleClickItem(leaf_key, COMPANY_CODE_IMG_TEXT_COLUMN)
    tree.SelectItem(leaf_key, COMPANY_CODE_IMG_LINK_COLUMN)
    tree.EnsureVisibleHorizontalItem(leaf_key, COMPANY_CODE_IMG_LINK_COLUMN)
    tree.ClickLink(leaf_key, COMPANY_CODE_IMG_LINK_COLUMN)
    _wait_not_busy(session)
    activity_screen = inspect_screen(session)
    expected_popup_id = "/app/con[0]/ses[0]/wnd[1]"
    popups = activity_screen.get("popups") or []
    activity_popups = [
        popup
        for popup in popups
        if popup.get("id") == expected_popup_id
        and popup.get("window_title") == "Sélection de l'activité :"
    ]
    if (
        str(activity_screen.get("transaction") or "").upper() != "SIMG"
        or str(activity_screen.get("program") or "").upper() != "SAPLDSYH"
        or len(popups) != 1
        or len(activity_popups) != 1
    ):
        raise ActionBlockedError(
            "Company-code IMG leaf did not open the observed "
            "SIMG / SAPLDSYH activity-selection dialog; "
            f"observed transaction={activity_screen.get('transaction')!r}, "
            f"program={activity_screen.get('program')!r}, "
            f"title={activity_screen.get('window_title')!r}, "
            f"popup_titles={[popup.get('window_title') for popup in popups]!r}"
        )
    select_company_code_display_activity(
        session,
        {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "company_code",
            "window_id": expected_popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "row_text": "Traiter données société",
            "button_text": "Sélectionner",
        },
    )
    if str(session.identity.get("transaction") or "").upper() != "V_T001":
        raise ActionBlockedError("Recorded IMG navigation did not reach V_T001")


def _lookup_company_code_1010(session: Any) -> dict[str, Any]:
    _open_company_code_screen_from_vbs(session)
    info = getattr(getattr(session, "raw", None), "Info", None)
    if (
        str(session.identity.get("transaction") or "").upper() == "V_T001"
        and (
            (
                str(getattr(info, "Program", "") or "").upper() == "SAPL0ORG"
                and str(getattr(info, "ScreenNumber", "") or "") in {"41", "0041"}
            )
            or (
                callable(getattr(session, "find", None))
                and callable(getattr(session, "audit", None))
            )
        )
    ):
        current = inspect_screen(session)
        saved_target = [
            field for field in current.get("input_fields") or []
            if field.get("id") == COMPANY_CODE_TARGET_FIELD
            and field.get("type") == "GuiCTextField"
            and field.get("visible") is True
            and field.get("text") == "1010"
        ]
        if (
            _is_company_code_target_screen(current)
            and len(saved_target) == 1
            and not current.get("popups")
        ):
            open_transaction(session, "SPRO")
            _open_company_code_screen_from_vbs(session)
            current = None
        pending_target = [
            field for field in (current or {}).get("input_fields") or []
            if field.get("id") == COMPANY_CODE_TARGET_FIELD
            and field.get("type") == "GuiCTextField"
            and field.get("changeable") is True
            and field.get("visible") is True
            and field.get("text") == "BE01"
        ]
        if (
            current is not None
            and _is_company_code_target_screen(current)
            and len(pending_target) == 1
            and not current.get("popups")
        ):
            return {
                "state": "MISSING",
                "evidence": {
                    "result": "CONFIRMED_NOT_FOUND",
                    "method": "PENDING_COPY_TARGET_ENTRY",
                    "source": "BE01",
                    "target": "1010",
                    "screen": dict(COMPANY_CODE_TARGET_SCREEN),
                },
            }
    snapshot = find_company_code_table_value(session, dict(COMPANY_CODE_TABLE_SEARCH))
    search = snapshot.get("table_value_search") or {}
    result = search.get("result")
    state = {
        "FOUND": "EXISTS",
        "CONFIRMED_NOT_FOUND": "MISSING",
    }.get(result, "UNKNOWN")
    return {"state": state, "evidence": search}


def _visible_input_values(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        str(field["id"]): field.get("text")
        for field in snapshot.get("input_fields") or []
        if field.get("visible") is True and isinstance(field.get("id"), str)
    }


def _post_save_state(snapshot: dict[str, Any]) -> dict[str, Any]:
    popups = snapshot.get("popups") or []
    target_field = next(
        (
            field for field in snapshot.get("input_fields") or []
            if field.get("id") == COMPANY_CODE_TARGET_FIELD
        ),
        None,
    )
    return {
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "screen_number": snapshot.get("screen_number"),
        "window_title": snapshot.get("window_title"),
        "status_bar": snapshot.get("status_bar"),
        "active_window_count": 1 + len(popups),
        "secondary_windows": popups,
        "target_field": target_field,
        "table_remains_in_edit_mode": bool(
            target_field and target_field.get("changeable") is True
        ),
        "navigated_from_target_screen": not _is_company_code_target_screen(snapshot),
    }


def _cancel_exact_company_address_dialog_for_readback(session: Any) -> bool:
    """Discard only the observed unfinished 1010 address dialog before READBACK."""
    snapshot = inspect_screen(session)
    popups = snapshot.get("popups") or []
    matches = [
        popup for popup in popups
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[1]"
        and popup.get("window_title") == "Traiter l'adresse:  1010"
    ]
    if not matches:
        return False
    pending_abort = [
        popup for popup in popups
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[2]"
        and popup.get("window_title") == "Interrompre gestion des adresses"
    ]
    if (
        snapshot.get("transaction") == "V_T001"
        and snapshot.get("program") == "SAPLSPO1"
        and len(popups) == 2
        and len(matches) == 1
        and len(pending_abort) == 1
    ):
        confirm_id = "/app/con[0]/ses[0]/wnd[2]/usr/btnSPOP-OPTION1"
        yes_buttons = [
            button for button in pending_abort[0].get("buttons") or []
            if button.get("id") == confirm_id
            and button.get("type") == "GuiButton"
            and button.get("text") == "Oui"
            and button.get("changeable") is True
        ]
        if len(yes_buttons) != 1:
            raise ActionBlockedError(
                "Company Code address-abort confirmation changed"
            )
        _press_exact(session, confirm_id)
        after_abort = inspect_screen(session)
        if after_abort.get("popups"):
            raise ActionBlockedError(
                "Company Code address dialog remained after exact abort confirmation"
            )
        return True
    if (
        snapshot.get("transaction") != "V_T001"
        or snapshot.get("program") != "SAPLSZA1"
        or len(popups) != 1
        or len(matches) != 1
    ):
        raise ActionBlockedError(
            "Company Code READBACK cannot cancel an inexact address dialog"
        )
    cancel_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[12]"
    buttons = [
        button for button in matches[0].get("buttons") or []
        if button.get("id") == cancel_id
        and button.get("type") == "GuiButton"
        and button.get("tooltip") == "Annuler   (F12)"
        and button.get("changeable") is True
    ]
    if len(buttons) != 1:
        raise ActionBlockedError(
            "Company Code address-dialog cancel control changed"
        )
    _press_exact(session, cancel_id)
    after = inspect_screen(session)
    confirmation = [
        popup for popup in after.get("popups") or []
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[2]"
        and popup.get("window_title") == "Interrompre gestion des adresses"
    ]
    if len(confirmation) == 1:
        confirm_id = "/app/con[0]/ses[0]/wnd[2]/usr/btnSPOP-OPTION1"
        yes_buttons = [
            button for button in confirmation[0].get("buttons") or []
            if button.get("id") == confirm_id
            and button.get("type") == "GuiButton"
            and button.get("text") == "Oui"
            and button.get("changeable") is True
        ]
        if len(yes_buttons) != 1:
            raise ActionBlockedError(
                "Company Code address-abort confirmation changed"
            )
        _press_exact(session, confirm_id)
        after = inspect_screen(session)
    if after.get("popups"):
        raise ActionBlockedError(
            "Company Code address dialog remained after exact Cancel"
        )
    return True


def _complete_company_code_target_entry(session: Any) -> dict[str, Any]:
    """Complete only the live-proven V_T001 screen-41 target entry."""
    before = inspect_screen(session)
    if (
        not _is_company_code_target_screen(before)
        or before.get("popups")
    ):
        raise ActionBlockedError(
            "COMPANY_CODE_1010 target entry requires exact V_T001/SAPL0ORG/0041 context"
        )
    target_fields = [
        field for field in before.get("input_fields") or []
        if field.get("id") == COMPANY_CODE_TARGET_FIELD
        and field.get("type") == "GuiCTextField"
        and field.get("changeable") is True
        and field.get("visible") is True
        and field.get("text") == "BE01"
    ]
    if len(target_fields) != 1:
        raise ActionBlockedError(
            "COMPANY_CODE_1010 exact target field is not uniquely evidenced"
        )
    before_values = _visible_input_values(before)
    target = session.find(COMPANY_CODE_TARGET_FIELD)
    if str(getattr(target, "Text", "")) != "BE01":
        raise ActionBlockedError("V_T001-BUKRS changed before target entry")
    setattr(target, "Text", "1010")
    after_entry = inspect_screen(session)
    if not _is_company_code_target_screen(after_entry):
        raise ActionBlockedError("V_T001 context changed after entering 1010")
    after_values = _visible_input_values(after_entry)
    if after_values.get(COMPANY_CODE_TARGET_FIELD) != "1010":
        raise ActionBlockedError("V_T001-BUKRS did not retain target 1010")
    unexpected_changes = {
        control_id: {"before": value, "after": after_values.get(control_id)}
        for control_id, value in before_values.items()
        if control_id != COMPANY_CODE_TARGET_FIELD
        and after_values.get(control_id) != value
    }
    if unexpected_changes:
        raise ActionBlockedError(
            f"Unrelated copied fields changed before Save: {unexpected_changes!r}"
        )
    main_window = session.find("wnd[0]")
    send_vkey = getattr(main_window, "sendVKey", None) or getattr(
        main_window, "SendVKey", None
    )
    if not callable(send_vkey):
        raise ActionBlockedError(
            "V_T001 screen 41 does not expose the evidenced target-entry confirmation"
        )
    send_vkey(0)
    _wait_not_busy(session)

    saved = inspect_screen(session)
    popups = saved.get("popups") or []
    if popups:
        return {
            "unexpected_popup": True,
            "reason": (
                "target-entry confirmation exposed the next Company Code "
                "write boundary"
            ),
            "popup_details": popups,
            "post_confirm_state": _post_save_state(saved),
        }
    message = saved.get("status_bar") or {}
    if str(message.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": "Company Code target-entry confirmation returned an error/abort status",
            "status_bar": message,
            "post_confirm_state": _post_save_state(saved),
        }
    post_save = _post_save_state(saved)
    if (
        _is_company_code_target_screen(saved)
        and (post_save.get("target_field") or {}).get("text") == "1010"
    ):
        return {
            "ambiguous_save": True,
            "reason": (
                "Target-entry confirmation returned without popup or navigation "
                "and left screen 41 editable"
            ),
            "post_confirm_state": post_save,
        }
    return {
        "accepted": True,
        "target": "1010",
        "target_entry_confirmed": True,
        "unchanged_fields_verified": True,
        "transport_released": False,
        "post_confirm_state": post_save,
    }


def _complete_company_code_address_and_save(session: Any) -> dict[str, Any]:
    """Accept the copied address, save V_T001, and reuse the approved request."""
    before = inspect_screen(session)
    popups = before.get("popups") or []
    address_popups = [
        popup for popup in popups
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[1]"
        and popup.get("window_title") == COMPANY_CODE_ADDRESS_TITLE
    ]
    error_popups = [
        popup for popup in popups
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[2]"
        and popup.get("window_title") == "Erreur"
        and COMPANY_CODE_COUNTRY_REQUIRED_MESSAGE
        in {str(field.get("text") or "") for field in popup.get("input_fields") or []}
    ]
    if len(error_popups) == 1 and len(popups) == 2 and len(address_popups) == 1:
        confirm_id = "/app/con[0]/ses[0]/wnd[2]/tbar[0]/btn[0]"
        confirm = [
            button for button in error_popups[0].get("buttons") or []
            if button.get("id") == confirm_id
            and button.get("type") == "GuiButton"
            and button.get("tooltip") in {
                "Confirmer   (Entrée)",
                "Confirmer   (EntrÃ©e)",
            }
            and button.get("changeable") is True
            and button.get("visible") is True
        ]
        if len(confirm) != 1:
            raise ActionBlockedError(
                "Company Code mandatory-country error confirmation changed"
            )
        _press_exact(session, confirm_id)
        before = inspect_screen(session)
        popups = before.get("popups") or []
        address_popups = [
            popup for popup in popups
            if popup.get("id") == "/app/con[0]/ses[0]/wnd[1]"
            and popup.get("window_title") == COMPANY_CODE_ADDRESS_TITLE
        ]
    if (
        before.get("transaction") != "V_T001"
        or before.get("program") != "SAPLSZA1"
        or str(before.get("screen_number") or "").lstrip("0") != "201"
        or len(popups) != 1
        or len(address_popups) != 1
    ):
        raise ActionBlockedError(
            "Company Code final commit requires the exact 1010 address dialog"
        )
    continue_buttons = [
        button for button in address_popups[0].get("buttons") or []
        if button.get("id") == COMPANY_CODE_ADDRESS_CONTINUE
        and button.get("type") == "GuiButton"
        and button.get("tooltip") in {
            "Reprendre   (Entrée)",
            "Reprendre   (EntrÃ©e)",
        }
        and button.get("changeable") is True
        and button.get("visible") is True
    ]
    if len(continue_buttons) != 1:
        raise ActionBlockedError("Company Code address Continue control changed")
    country_fields = [
        field for field in address_popups[0].get("input_fields") or []
        if field.get("id") == COMPANY_CODE_ADDRESS_COUNTRY
        and field.get("type") == "GuiCTextField"
        and field.get("changeable") is True
        and field.get("visible") is True
    ]
    if len(country_fields) != 1:
        raise ActionBlockedError("Company Code address country field changed")
    observed_country = str(country_fields[0].get("text") or "").strip()
    if observed_country not in {"", COMPANY_CODE_TEMPLATE_COUNTRY}:
        raise ActionBlockedError(
            f"Company Code address country is not the approved BE01 value: {observed_country!r}"
        )
    if not observed_country:
        country = session.find(COMPANY_CODE_ADDRESS_COUNTRY)
        if (
            str(getattr(country, "Type", "")) != "GuiCTextField"
            or getattr(country, "Changeable", False) is not True
        ):
            raise ActionBlockedError("Company Code live country field changed")
        setattr(country, "Text", COMPANY_CODE_TEMPLATE_COUNTRY)
        with_country = inspect_screen(session)
        country_after = [
            field for popup in with_country.get("popups") or []
            for field in popup.get("input_fields") or []
            if field.get("id") == COMPANY_CODE_ADDRESS_COUNTRY
            and str(field.get("text") or "").strip() == COMPANY_CODE_TEMPLATE_COUNTRY
        ]
        if len(country_after) != 1:
            raise ActionBlockedError("Company Code BE01 country was not retained")
    _press_exact(session, COMPANY_CODE_ADDRESS_CONTINUE)
    after_address = inspect_screen(session)
    address_status = after_address.get("status_bar") or {}
    if str(address_status.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": "Company Code address confirmation returned an error/abort status",
            "status_bar": address_status,
            "post_address_state": _post_save_state(after_address),
        }
    if after_address.get("popups"):
        return {
            "unexpected_popup": True,
            "reason": "Company Code address confirmation opened an unsupported popup",
            "popup_details": after_address.get("popups"),
            "post_address_state": _post_save_state(after_address),
        }
    if (
        after_address.get("transaction") != "V_T001"
        or after_address.get("program") != "SAPL0ORG"
        or 'Modifier vue "Soci' not in str(after_address.get("window_title") or "")
        or "synth" not in str(after_address.get("window_title") or "").casefold()
    ):
        raise ActionBlockedError(
            "Company Code address confirmation did not return to the V_T001 overview"
        )
    save_buttons = [
        button for button in after_address.get("buttons") or []
        if button.get("id") == COMPANY_CODE_SAVE_CONTROL
        and button.get("type") == "GuiButton"
        and button.get("text") == "Sauvegarder"
        and button.get("tooltip") == "Sauvegarder   (Ctrl+S)"
        and button.get("changeable") is True
        and button.get("visible") is True
    ]
    if len(save_buttons) != 1:
        raise ActionBlockedError("Company Code exact Save control changed")
    _press_exact(session, COMPANY_CODE_SAVE_CONTROL)
    after_save = inspect_screen(session)
    save_status = after_save.get("status_bar") or {}
    if str(save_status.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": "Company Code Save returned an error/abort status",
            "status_bar": save_status,
            "post_save_state": _post_save_state(after_save),
        }
    save_popups = after_save.get("popups") or []
    if save_popups:
        if (
            len(save_popups) != 1
            or save_popups[0].get("window_title")
            != COMPANY_CODE_TRANSPORT_POPUP_TITLE
        ):
            return {
                "unexpected_popup": True,
                "reason": "Company Code Save opened an unsupported popup",
                "popup_details": save_popups,
                "post_save_state": _post_save_state(after_save),
            }
        transport = _reuse_company_code_transport(session)
        if not transport.get("accepted"):
            return transport
        committed = inspect_screen(session)
    else:
        transport = {}
        committed = after_save
    committed_status = committed.get("status_bar") or {}
    if committed.get("popups"):
        return {
            "unexpected_popup": True,
            "reason": "Popup remains after Company Code final commit",
            "popup_details": committed.get("popups"),
            "post_save_state": _post_save_state(committed),
        }
    if str(committed_status.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": "Company Code final commit returned an error/abort status",
            "status_bar": committed_status,
            "post_save_state": _post_save_state(committed),
        }
    return {
        "accepted": True,
        "target": "1010",
        "address_confirmed": True,
        "save_action": COMPANY_CODE_SAVE_CONTROL,
        "transport_request_id": transport.get("transport_request_id"),
        "transport_released": False,
        "post_address_status": address_status,
        "post_save_status": committed_status,
        "post_save_state": _post_save_state(committed),
    }


def _lookup_sales_organization_1010(session: Any) -> dict[str, Any]:
    _open_sales_organization_screen(session)
    search = find_sales_organization_table_value(
        session,
        dict(SALES_ORGANIZATION_TABLE_SEARCH),
    ).get("table_value_search") or {}
    state = {
        "FOUND": "EXISTS",
        "CONFIRMED_NOT_FOUND": "MISSING",
    }.get(search.get("result"), "UNKNOWN")
    return {"state": state, "evidence": search}


def _save_existing_sales_organization_1010(session: Any) -> dict[str, Any]:
    """Save the already-copied 1010 row on the evidenced V_TVKO overview."""
    before = inspect_screen(session)
    table_id = SALES_ORGANIZATION_TABLE_SEARCH["table_id"]
    if (
        before.get("transaction") != "V_TVKO"
        or before.get("program") != "SAPL0ORG"
        or str(before.get("screen_number") or "").lstrip("0") != "240"
        or before.get("window_title") != SALES_ORGANIZATION_OVERVIEW_TITLE
        or before.get("popups")
    ):
        raise ActionBlockedError(
            "Sales Organization save requires exact V_TVKO/SAPL0ORG/0240 overview"
        )
    tables = [
        table for table in before.get("tables") or []
        if table.get("id") == table_id
        and table.get("type") == "GuiTableControl"
        and table.get("changeable") is True
    ]
    if len(tables) != 1:
        raise ActionBlockedError(
            "Sales Organization save requires one editable V_TVKO table"
        )

    code_prefix = f"{table_id}/ctxtV_TVKO-VKORG[0,"
    description_prefix = f"{table_id}/txtV_TVKO-VTEXT[1,"
    target_rows: list[tuple[str, dict[str, Any]]] = []
    for field in before.get("input_fields") or []:
        field_id = str(field.get("id") or "")
        if (
            field_id.startswith(code_prefix)
            and field_id.endswith("]")
            and field.get("visible") is True
            and field.get("type") == "GuiCTextField"
            and field.get("text") == "1010"
        ):
            row_index = field_id[len(code_prefix):-1]
            target_rows.append((row_index, field))
    if len(target_rows) != 1:
        raise ActionBlockedError(
            "Sales Organization 1010 is not uniquely visible for Save"
        )
    row_index, _ = target_rows[0]
    description_id = f"{description_prefix}{row_index}]"
    descriptions = [
        field for field in before.get("input_fields") or []
        if field.get("id") == description_id
        and field.get("type") == "GuiTextField"
        and field.get("visible") is True
        and field.get("text") == "S4615 Training"
    ]
    if len(descriptions) != 1:
        raise ActionBlockedError(
            "Sales Organization 1010 description does not match S4615 Training"
        )
    save_controls = [
        control for control in before.get("buttons") or []
        if control.get("id") == SALES_ORGANIZATION_SAVE_MENU
        and control.get("type") == "GuiMenu"
        and control.get("text") == "Sauvegarder"
        and control.get("changeable") is True
        and control.get("visible") is True
    ]
    if len(save_controls) != 1:
        raise ActionBlockedError(
            "Sales Organization exact Save menu contract changed"
        )

    save_menu = session.find(SALES_ORGANIZATION_SAVE_MENU)
    if (
        str(getattr(save_menu, "Type", "")) != "GuiMenu"
        or str(getattr(save_menu, "Text", "")) != "Sauvegarder"
        or getattr(save_menu, "Changeable", False) is not True
    ):
        raise ActionBlockedError(
            "Sales Organization exact Save menu control changed"
        )
    select_save = getattr(save_menu, "select", None) or getattr(
        save_menu, "Select", None
    )
    if not callable(select_save):
        raise ActionBlockedError(
            "Sales Organization exact Save menu action is unavailable"
        )
    select_save()
    _wait_not_busy(session)

    saved = inspect_screen(session)
    post_state = {
        "transaction": saved.get("transaction"),
        "program": saved.get("program"),
        "screen_number": saved.get("screen_number"),
        "window_title": saved.get("window_title"),
        "status_bar": saved.get("status_bar"),
        "popups": saved.get("popups") or [],
    }
    if post_state["popups"]:
        transport_dialogs = [
            popup
            for popup in post_state["popups"]
            if popup.get("window_title") == SALES_ORGANIZATION_TRANSPORT_POPUP_TITLE
            and SALES_ORGANIZATION_TRANSPORT_FIELD
            in {control.get("id") for control in popup.get("input_fields") or []}
        ]
        if len(post_state["popups"]) == 1 and len(transport_dialogs) == 1:
            popup = transport_dialogs[0]
            editable = [
                field for field in popup.get("input_fields") or []
                if field.get("changeable") is True
            ]
            continue_buttons = [
                button for button in popup.get("buttons") or []
                if button.get("id") == SALES_ORGANIZATION_TRANSPORT_CONTINUE
                and button.get("type") == "GuiButton"
                and button.get("changeable") is True
                and button.get("visible") is True
            ]
            if (
                len(editable) != 1
                or editable[0].get("id") != SALES_ORGANIZATION_TRANSPORT_FIELD
                or editable[0].get("type") != "GuiCTextField"
                or len(continue_buttons) != 1
            ):
                return {
                    "transport_request": True,
                    "reason": "Sales Organization transport popup contract changed",
                    "transport_popup": popup,
                    "post_save_state": post_state,
                }
            transport_field = session.find(SALES_ORGANIZATION_TRANSPORT_FIELD)
            if (
                str(getattr(transport_field, "Type", "")) != "GuiCTextField"
                or getattr(transport_field, "Changeable", False) is not True
            ):
                return {
                    "transport_request": True,
                    "reason": "Sales Organization transport field is not editable",
                    "transport_popup": popup,
                    "post_save_state": post_state,
                }
            setattr(transport_field, "Text", COMPANY_CODE_TRANSPORT_REQUEST)
            _press_exact(session, SALES_ORGANIZATION_TRANSPORT_CONTINUE)
            _wait_not_busy(session)
            after_transport = inspect_screen(session)
            remaining = after_transport.get("popups") or []
            if remaining:
                same_transport = [
                    item for item in remaining
                    if item.get("window_title") == SALES_ORGANIZATION_TRANSPORT_POPUP_TITLE
                ]
                if same_transport:
                    return {
                        "transport_request": True,
                        "request": COMPANY_CODE_TRANSPORT_REQUEST,
                        "reason": "approved request was rejected or is not modifiable",
                        "transport_popup": same_transport[0],
                    }
                return {
                    "unexpected_popup": True,
                    "reason": "unexpected popup after Sales Organization transport selection",
                    "popup_details": remaining,
                }
            return {
                "accepted": True,
                "target": "1010",
                "save_action": SALES_ORGANIZATION_SAVE_MENU,
                "transport_request_id": COMPANY_CODE_TRANSPORT_REQUEST,
                "transport_released": False,
                "post_save_state": {
                    "transaction": after_transport.get("transaction"),
                    "program": after_transport.get("program"),
                    "screen_number": after_transport.get("screen_number"),
                    "window_title": after_transport.get("window_title"),
                    "status_bar": after_transport.get("status_bar"),
                    "popups": [],
                },
            }
        return {
            "unexpected_popup": True,
            "reason": "Sales Organization Save opened an unverified popup",
            "popup_details": post_state["popups"],
            "post_save_state": post_state,
        }
    message = saved.get("status_bar") or {}
    if str(message.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": "Sales Organization Save returned an error/abort status",
            "status_bar": message,
            "post_save_state": post_state,
        }
    return {
        "accepted": True,
        "target": "1010",
        "save_action": SALES_ORGANIZATION_SAVE_MENU,
        "post_save_state": post_state,
    }


def _start_sales_organization_copy(
    session: Any, values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Select only live 1710 in V_TVKO and open the exact Copy destination."""
    if str(session.identity.get("transaction") or "").upper() == "V_TVKO":
        current = inspect_screen(session)
        if (
            current.get("program") == "SAPL0ORG"
            and str(current.get("screen_number") or "").lstrip("0") == "240"
            and not current.get("popups")
        ):
            lookup = _lookup_sales_organization_1010(session)
            if lookup["state"] == "EXISTS":
                return _save_existing_sales_organization_1010(session)
            if lookup["state"] == "UNKNOWN":
                raise ActionBlockedError(
                    "Sales Organization overview lookup is incomplete; Save is blocked"
                )
        popups = current.get("popups") or []
        if (
            current.get("program") == "SAPLSZA1"
            and current.get("screen_number") == "201"
            and len(popups) == 1
            and popups[0].get("window_title") == "Traiter l'adresse:  1010"
        ):
            name_id = "/app/con[0]/ses[0]/wnd[1]/usr/txtADDR1_DATA-NAME1"
            continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
            popup_fields = {
                field.get("id"): field
                for field in popups[0].get("input_fields") or []
            }
            name = popup_fields.get(name_id)
            continue_buttons = [
                button for button in popups[0].get("buttons") or []
                if button.get("id") == continue_id
                and button.get("type") == "GuiButton"
                and button.get("tooltip") == "Reprendre   (Entrée)"
                and button.get("changeable") is True
            ]
            if (
                not name
                or name.get("type") != "GuiTextField"
                or name.get("changeable") is not True
                or len(continue_buttons) != 1
            ):
                raise ActionBlockedError(
                    "Sales Organization address popup contract changed"
                )
            before_address = {
                field_id: field.get("text")
                for field_id, field in popup_fields.items()
            }
            setattr(session.find(name_id), "Text", "S4615 Training")
            changed = inspect_screen(session)
            changed_popup = (changed.get("popups") or [{}])[0]
            changed_fields = {
                field.get("id"): field.get("text")
                for field in changed_popup.get("input_fields") or []
            }
            unexpected = {
                field_id: {"before": original, "after": changed_fields.get(field_id)}
                for field_id, original in before_address.items()
                if field_id != name_id and changed_fields.get(field_id) != original
            }
            if changed_fields.get(name_id) != "S4615 Training" or unexpected:
                raise ActionBlockedError(
                    f"Sales Organization address update was not isolated: {unexpected!r}"
                )
            _press_exact(session, continue_id)
            _wait_not_busy(session)
            return {
                "provisioning_blocked": True,
                "reason": "Sales Organization address confirmed; next live boundary",
                "post_confirm_state": inspect_screen(session),
            }
        if (
            current.get("program") == "SAPMSDYP"
            and current.get("screen_number") == "10"
            and len(popups) == 1
            and popups[0].get("window_title") == "Information"
        ):
            popup_texts = {
                str(control.get("text") or "")
                for control in popups[0].get("controls") or []
            }
            continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
            continue_buttons = [
                button for button in popups[0].get("buttons") or []
                if button.get("id") == continue_id
                and button.get("type") == "GuiButton"
                and button.get("tooltip") == "Continuer   (Entrée)"
                and button.get("changeable") is True
            ]
            if (
                "AVERTISSEMENT : modification devise statistique" not in popup_texts
                or "entraîne des incohérences" not in popup_texts
                or len(continue_buttons) != 1
            ):
                raise ActionBlockedError(
                    "Sales Organization currency-warning popup contract changed"
                )
            _press_exact(session, continue_id)
            _wait_not_busy(session)
            return {
                "provisioning_blocked": True,
                "reason": "Sales Organization currency warning acknowledged; next live boundary",
                "post_confirm_state": inspect_screen(session),
            }
        if current.get("screen_number") == "245" and not current.get("popups"):
            inputs = _visible_input_values(current)
            if (
                inputs.get("/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-VKORG") != "1710"
                or inputs.get("/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-WAERS") != "USD"
            ):
                raise ActionBlockedError(
                    "Sales Organization target-entry screen contains uncommitted changes"
                )
            cancel_id = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[9]"
            cancel = session.find(cancel_id)
            if (
                str(getattr(cancel, "Type", "")) != "GuiMenu"
                or str(getattr(cancel, "Text", "")) != "Interrompre"
            ):
                raise ActionBlockedError(
                    "Sales Organization target-entry exact cancel control changed"
                )
            select_cancel = getattr(cancel, "select", None) or getattr(
                cancel, "Select", None
            )
            if not callable(select_cancel):
                raise ActionBlockedError(
                    "Sales Organization target-entry exact cancel is unavailable"
                )
            select_cancel()
            _wait_not_busy(session)
            returned = inspect_screen(session)
            if (
                returned.get("transaction") != "V_TVKO"
                or returned.get("program") != "SAPL0ORG"
                or returned.get("screen_number") != "240"
                or returned.get("popups")
            ):
                raise ActionBlockedError(
                    "Sales Organization target-entry Back did not return to overview"
                )
    _open_sales_organization_screen(session)
    snapshot = inspect_screen(session)
    table_id = SALES_ORGANIZATION_TABLE_SEARCH["table_id"]
    copy_id = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[3]"
    tables = [
        table for table in snapshot.get("tables") or []
        if table.get("id") == table_id
        and table.get("type") == "GuiTableControl"
        and table.get("changeable") is True
    ]
    copy_controls = [
        item for item in snapshot.get("buttons") or []
        if item.get("id") == copy_id
        and item.get("type") == "GuiMenu"
        and item.get("text") == "Copier sous..."
        and item.get("changeable") is True
    ]
    if (
        snapshot.get("transaction") != "V_TVKO"
        or snapshot.get("program") != "SAPL0ORG"
        or snapshot.get("screen_number") != "240"
        or len(tables) != 1
        or len(copy_controls) != 1
        or snapshot.get("popups")
    ):
        raise ActionBlockedError(
            "Sales Organization copy requires exact live V_TVKO/SAPL0ORG/0240 overview"
        )
    table = session.find(table_id)
    row_count = int(table.RowCount)
    visible_count = int(table.VisibleRowCount)
    table.VerticalScrollbar.Position = 0
    _wait_not_busy(session)
    source_row = None
    visited: set[int] = set()
    while len(visited) < row_count:
        table = session.find(table_id)
        position = int(table.VerticalScrollbar.Position)
        maximum = int(table.VerticalScrollbar.Maximum)
        for absolute_row in range(position, min(position + visible_count, row_count)):
            relative_row = absolute_row - position
            cell_id = f"{table_id}/ctxtV_TVKO-VKORG[0,{relative_row}]"
            cell = session.find(cell_id)
            if (
                str(getattr(cell, "Type", "")) != "GuiCTextField"
                or str(getattr(cell, "Id", "")) != cell_id
            ):
                raise ActionBlockedError(
                    f"Sales Organization source cell mismatch at row {absolute_row}"
                )
            if str(getattr(cell, "Text", "")).strip() == "1710":
                if source_row is not None and source_row != absolute_row:
                    raise ActionBlockedError("Sales Organization 1710 is not unique")
                source_row = absolute_row
            visited.add(absolute_row)
        if len(visited) >= row_count:
            break
        next_position = min(position + visible_count, maximum)
        if next_position <= position:
            raise ActionBlockedError("V_TVKO source scan stalled")
        table.VerticalScrollbar.Position = next_position
        _wait_not_busy(session)
    if source_row is None:
        raise ActionBlockedError("Technical template Sales Organization 1710 was not found")
    table = session.find(table_id)
    maximum = int(table.VerticalScrollbar.Maximum)
    source_position = min(source_row, maximum)
    table.VerticalScrollbar.Position = source_position
    _wait_not_busy(session)
    table = session.find(table_id)
    table.GetAbsoluteRow(source_row).Selected = True
    table.VerticalScrollbar.Position = 0
    _wait_not_busy(session)
    selected: list[int] = []
    verified: set[int] = set()
    checked_positions: set[int] = set()
    while len(verified) < row_count:
        table = session.find(table_id)
        position = int(table.VerticalScrollbar.Position)
        maximum = int(table.VerticalScrollbar.Maximum)
        if position in checked_positions:
            raise ActionBlockedError("V_TVKO selection verification stalled")
        checked_positions.add(position)
        for absolute_row in range(position, min(position + visible_count, row_count)):
            row = table.GetAbsoluteRow(absolute_row)
            if bool(row.Selected):
                selected.append(absolute_row)
            verified.add(absolute_row)
        if len(verified) >= row_count:
            break
        next_position = min(position + visible_count, maximum)
        if next_position <= position:
            raise ActionBlockedError("V_TVKO selection verification did not cover RowCount")
        table.VerticalScrollbar.Position = next_position
        _wait_not_busy(session)
    if selected != [source_row]:
        raise ActionBlockedError(
            f"Sales Organization copy selection mismatch: {selected!r}"
        )
    copy_control = session.find(copy_id)
    if (
        str(getattr(copy_control, "Type", "")) != "GuiMenu"
        or str(getattr(copy_control, "Text", "")) != "Copier sous..."
    ):
        raise ActionBlockedError("Sales Organization Copy control changed")
    select = getattr(copy_control, "select", None) or getattr(copy_control, "Select", None)
    if not callable(select):
        raise ActionBlockedError("Sales Organization Copy control is not selectable")
    select()
    _wait_not_busy(session)

    destination = inspect_screen(session)
    if values is None:
        return {
            "provisioning_blocked": True,
            "reason": "Sales Organization Copy destination requires live contract capture",
            "selected_source_row": source_row,
            "copy_destination": destination,
        }
    required = {
        "technical_template": "1710",
        "description": "S4615 Training",
        "statistics_currency": "EUR",
    }
    if any(values.get(name) != expected for name, expected in required.items()):
        raise ActionBlockedError("SALES_ORGANIZATION_1010 mandatory values mismatch")
    if (
        destination.get("transaction") != "V_TVKO"
        or destination.get("program") != "SAPL0ORG"
        or destination.get("screen_number") != "245"
        or destination.get("popups")
    ):
        raise ActionBlockedError(
            "Sales Organization target entry requires exact V_TVKO/SAPL0ORG/0245 context"
        )
    exact_fields = {
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-VKORG": "1010",
        "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVKO-VTEXT": "S4615 Training",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-WAERS": "EUR",
        # These copied 1710-specific fields are optional by project decision.
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-KUNNR": "",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-EKORG": "",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-EKGRP": "",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVKO-BSART": "",
    }
    observed = {
        field.get("id"): field
        for field in destination.get("input_fields") or []
        if field.get("visible") is True
    }
    for control_id in exact_fields:
        field = observed.get(control_id)
        if not field or field.get("changeable") is not True:
            raise ActionBlockedError(
                f"Sales Organization target field is not uniquely editable: {control_id}"
            )
    for control_id, target_value in exact_fields.items():
        setattr(session.find(control_id), "Text", target_value)

    rebate_id = "/app/con[0]/ses[0]/wnd[0]/usr/chkV_TVKO-BOAVO"
    rebate = observed.get(rebate_id)
    if rebate and rebate.get("changeable") is True:
        checkbox = session.find(rebate_id)
        if hasattr(checkbox, "Selected"):
            checkbox.Selected = False

    after_entry = inspect_screen(session)
    after_values = _visible_input_values(after_entry)
    mismatches = {
        control_id: {"expected": expected, "actual": after_values.get(control_id)}
        for control_id, expected in exact_fields.items()
        if str(after_values.get(control_id) or "") != expected
    }
    if mismatches:
        raise ActionBlockedError(
            f"Sales Organization target values were not retained: {mismatches!r}"
        )
    main_window = session.find("wnd[0]")
    send_vkey = getattr(main_window, "sendVKey", None) or getattr(
        main_window, "SendVKey", None
    )
    if not callable(send_vkey):
        raise ActionBlockedError("V_TVKO screen 245 has no target-entry confirmation")
    send_vkey(0)
    _wait_not_busy(session)
    return {
        "provisioning_blocked": True,
        "reason": "Sales Organization target entry reached the next live boundary",
        "selected_source_row": source_row,
        "target_values": exact_fields,
        "post_confirm_state": inspect_screen(session),
    }


def _open_assignment_screen(session: Any, operation: str) -> None:
    """Navigate only the captured IMG route for the three assignment views."""
    transaction = str(session.identity.get("transaction") or "").upper()
    search = PHASE5_ASSIGNMENT_TABLE_SEARCHES[operation]
    if transaction not in {"SESSION_MANAGER", "V_T001", "V_TVKO", "SPRO", "SIMG"}:
        raise ActionBlockedError(
            f"{operation} cannot start from transaction {transaction!r}"
        )
    if transaction != "SPRO":
        open_transaction(session, "SPRO")
    if str(session.identity.get("transaction") or "").upper() != "SPRO":
        raise ActionBlockedError("Recorded assignment navigation did not reach SPRO")

    _press_exact(session, COMPANY_CODE_VBS_CONTROLS["img_button"])
    if str(session.identity.get("transaction") or "").upper() != "SIMG":
        raise ActionBlockedError("Recorded assignment navigation did not reach SIMG")

    tree_id = SALES_ORGANIZATION_DISPLAY_EXCEPTION["control_id"]
    for node_key, node_text in ASSIGNMENT_IMG_NODES:
        navigate(
            session,
            {
                "navigation_operation": "EXPAND_TREE_NODE",
                "control_id": tree_id,
                "expected_type": "GuiShell",
                "expected_text": node_text,
                "node_key": node_key,
                "expected_transaction": "SIMG",
            },
        )
    leaf_key, leaf_text = ASSIGNMENT_IMG_LEAVES[operation]
    navigate(
        session,
        {
            "navigation_operation": "OPEN_IMG_ACTIVITY",
            "control_id": tree_id,
            "expected_type": "GuiShell",
            "expected_text": leaf_text,
            "node_key": leaf_key,
            "item_column": "2",
            "expected_transaction": "SIMG",
        },
    )
    if (
        str(session.identity.get("transaction") or "").upper() != "SIMG"
        or str(getattr(session.raw.Info, "Program", "") or "").upper()
        != search["program"]
    ):
        raise ActionBlockedError(
            f"Recorded IMG activity did not reach the {operation} table"
        )


def _lookup_assignment(session: Any, operation: str) -> dict[str, Any]:
    target = EXPECTED_TARGETS[operation]
    _open_assignment_screen(session, operation)
    search = find_phase5_assignment_table_row(session, operation, target)[
        "table_row_search"
    ]
    state = {
        "FOUND": "EXISTS",
        "CONFIRMED_NOT_FOUND": "MISSING",
    }.get(search.get("result"), "UNKNOWN")
    return {"state": state, "evidence": search}


def _provision_assignment_existing_row(session: Any, operation: str) -> dict[str, Any]:
    """Fill an evidenced existing row or one exact New Entries row."""
    search = PHASE5_ASSIGNMENT_TABLE_SEARCHES[operation]
    fields = search["fields"]
    anchor_name = "sales_organization"
    value_name = next(name for name in fields if name != anchor_name)
    anchor = fields[anchor_name]
    value = fields[value_name]
    new_entries_screen = {
        "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": "2",
        "DIVISION_00_TO_SALES_ORG_1010": "3",
    }.get(operation)

    info = getattr(getattr(session, "raw", None), "Info", None)
    in_new_entries = (
        str(session.identity.get("transaction") or "").upper() == "SIMG"
        and str(getattr(info, "Program", "") or "").upper() == search["program"]
        and new_entries_screen is not None
        and str(getattr(info, "ScreenNumber", "") or "").lstrip("0")
        == new_entries_screen
    )
    if not in_new_entries:
        _open_assignment_screen(session, operation)
    before = inspect_screen(session)
    table_id = search["table_id"]
    if (
        before.get("transaction") != "SIMG"
        or before.get("program") != search["program"]
        or before.get("popups")
        or len([
            table for table in before.get("tables") or []
            if table.get("id") == table_id
            and table.get("type") == "GuiTableControl"
            and table.get("changeable") is True
        ]) != 1
    ):
        raise ActionBlockedError(f"{operation} requires its exact live assignment table")

    anchor_prefix = f"{table_id}/{anchor['control']}[{anchor['column']},"
    anchor_rows = []
    if not in_new_entries:
        for field in before.get("input_fields") or []:
            field_id = str(field.get("id") or "")
            if (
                field_id.startswith(anchor_prefix)
                and field_id.endswith("]")
                and field.get("type") == "GuiCTextField"
                and field.get("visible") is True
                and str(field.get("text") or "").strip() == anchor["value"]
            ):
                anchor_rows.append(field_id[len(anchor_prefix):-1])
    if not in_new_entries and not anchor_rows:
        new_entries_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"
        new_entries = [
            button for button in before.get("buttons") or []
            if button.get("id") == new_entries_id
            and button.get("type") == "GuiButton"
            and button.get("text") == "Nouvelles entrées"
            and button.get("tooltip") == "Nouvelles entrées   (F5)"
            and button.get("changeable") is True
            and button.get("visible") is True
        ]
        if len(new_entries) != 1:
            raise ActionBlockedError(
                f"{operation} has no 1010 row and exact New Entries is unavailable"
            )
        _press_exact(session, new_entries_id)
        before = inspect_screen(session)
        in_new_entries = True
    if in_new_entries:
        if (
            new_entries_screen is None
            or str(before.get("screen_number") or "").lstrip("0")
            != new_entries_screen
            or not str(before.get("window_title") or "").startswith("Nouvelles entr")
        ):
            raise ActionBlockedError(
                f"{operation} exact New Entries screen contract changed"
            )
        row = "0"
        anchor_id = f"{table_id}/{anchor['control']}[{anchor['column']},{row}]"
        value_id = f"{table_id}/{value['control']}[{value['column']},{row}]"
        expected_entry_fields = {
            anchor_id: anchor["value"],
            value_id: value["value"],
        }
        observed = {
            field.get("id"): field
            for field in before.get("input_fields") or []
            if field.get("id") in expected_entry_fields
        }
        if set(observed) != set(expected_entry_fields) or any(
            field.get("type") != "GuiCTextField"
            or field.get("changeable") is not True
            or field.get("visible") is not True
            or str(field.get("text") or "").strip()
            for field in observed.values()
        ):
            raise ActionBlockedError(
                f"{operation} exact blank New Entries row is unavailable"
            )
        for control_id, target_value in expected_entry_fields.items():
            control = session.find(control_id)
            if (
                str(getattr(control, "Type", "")) != "GuiCTextField"
                or getattr(control, "Changeable", False) is not True
                or str(getattr(control, "Text", "") or "").strip()
            ):
                raise ActionBlockedError(
                    f"{operation} live New Entries field changed: {control_id}"
                )
            setattr(control, "Text", target_value)
        entered = inspect_screen(session)
        entered_values = _visible_input_values(entered)
        if any(
            entered_values.get(control_id) != target_value
            for control_id, target_value in expected_entry_fields.items()
        ):
            raise ActionBlockedError(
                f"{operation} New Entries values were not retained"
            )
        entered_control_id: Any = sorted(expected_entry_fields)
    elif len(anchor_rows) != 1:
        raise ActionBlockedError(
            f"{operation} Sales Organization 1010 row is not uniquely visible"
        )
    else:
        row = anchor_rows[0]
        value_id = f"{table_id}/{value['control']}[{value['column']},{row}]"
        candidates = [
            field for field in before.get("input_fields") or []
            if field.get("id") == value_id
            and field.get("type") == "GuiCTextField"
            and field.get("visible") is True
            and field.get("changeable") is True
        ]
        if len(candidates) != 1:
            raise ActionBlockedError(f"{operation} exact target assignment cell is unavailable")
        existing = str(candidates[0].get("text") or "").strip()
        if existing not in {"", value["value"]}:
            raise ActionBlockedError(
                f"{operation} target cell contains conflicting value {existing!r}"
            )
        if existing == value["value"]:
            return {"accepted": True, "target": EXPECTED_TARGETS[operation], "already_present": True}

        control = session.find(value_id)
        if (
            str(getattr(control, "Type", "")) != "GuiCTextField"
            or getattr(control, "Changeable", False) is not True
        ):
            raise ActionBlockedError(f"{operation} live target cell contract changed")
        setattr(control, "Text", value["value"])
        entered = inspect_screen(session)
        entered_values = _visible_input_values(entered)
        if entered_values.get(value_id) != value["value"]:
            raise ActionBlockedError(f"{operation} target value was not retained")
        entered_control_id = value_id

    exact_save_id = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
    save_buttons = [
        button for button in entered.get("buttons") or []
        if button.get("id") == exact_save_id
        and button.get("type") == "GuiButton"
        and button.get("text") == "Sauvegarder"
        and button.get("changeable") is True
        and button.get("visible") is True
    ]
    if len(save_buttons) != 1:
        return {
            "provisioning_blocked": True,
            "reason": f"{operation} exact Save control is not evidenced after entry",
            "entered_control_id": entered_control_id,
        }
    _press_exact(session, exact_save_id)
    _wait_not_busy(session)
    saved = inspect_screen(session)
    popups = saved.get("popups") or []
    transport_used = None
    if popups:
        if (
            len(popups) != 1
            or popups[0].get("window_title") != SALES_ORGANIZATION_TRANSPORT_POPUP_TITLE
        ):
            return {
                "unexpected_popup": True,
                "reason": f"{operation} Save opened an unverified popup",
                "popup_details": popups,
            }
        popup = popups[0]
        editable = [
            field for field in popup.get("input_fields") or []
            if field.get("changeable") is True
        ]
        if (
            len(editable) != 1
            or editable[0].get("id") != SALES_ORGANIZATION_TRANSPORT_FIELD
            or editable[0].get("type") != "GuiCTextField"
        ):
            return {
                "transport_request": True,
                "reason": f"{operation} transport popup contract changed",
            }
        transport = session.find(SALES_ORGANIZATION_TRANSPORT_FIELD)
        setattr(transport, "Text", COMPANY_CODE_TRANSPORT_REQUEST)
        _press_exact(session, SALES_ORGANIZATION_TRANSPORT_CONTINUE)
        _wait_not_busy(session)
        after_transport = inspect_screen(session)
        if after_transport.get("popups"):
            return {
                "transport_request": True,
                "reason": f"{operation} transport request was rejected or not modifiable",
                "popup_details": after_transport.get("popups"),
            }
        saved = after_transport
        transport_used = COMPANY_CODE_TRANSPORT_REQUEST
    message = saved.get("status_bar") or {}
    if str(message.get("message_type") or "").upper() in {"E", "A"}:
        return {
            "ambiguous_save": True,
            "reason": f"{operation} Save returned an error/abort status",
            "status_bar": message,
        }
    return {
        "accepted": True,
        "target": EXPECTED_TARGETS[operation],
        "transport_request_id": transport_used,
        "transport_released": False,
    }


def _open_sales_organization_screen(session: Any) -> None:
    """Follow the captured V_T001/SPRO/IMG route to the Sales Org lookup."""
    transaction = str(session.identity.get("transaction") or "").upper()
    if transaction == "V_TVKO":
        return
    if transaction not in {"SESSION_MANAGER", "V_T001", "SPRO", "SIMG"}:
        raise ActionBlockedError(
            f"SALES_ORGANIZATION_1010 cannot start from transaction {transaction!r}"
        )
    if transaction in {"SESSION_MANAGER", "V_T001"}:
        open_transaction(session, "SPRO")
        transaction = str(session.identity.get("transaction") or "").upper()
        if transaction != "SPRO":
            raise ActionBlockedError("Recorded navigation did not reach SPRO")
    if transaction == "SPRO":
        _press_exact(session, COMPANY_CODE_VBS_CONTROLS["img_button"])
        transaction = str(session.identity.get("transaction") or "").upper()
        if transaction != "SIMG":
            raise ActionBlockedError("Recorded navigation did not reach SIMG")

    tree_id = SALES_ORGANIZATION_DISPLAY_EXCEPTION["control_id"]
    for node_key, node_text in SALES_ORGANIZATION_IMG_NODES:
        navigate(
            session,
            {
                "navigation_operation": "EXPAND_TREE_NODE",
                "control_id": tree_id,
                "expected_type": "GuiShell",
                "expected_text": node_text,
                "node_key": node_key,
                "expected_transaction": "SIMG",
            },
        )
    leaf_key, leaf_text, item_column = SALES_ORGANIZATION_IMG_LEAF
    navigate(
        session,
        {
            "navigation_operation": "OPEN_IMG_ACTIVITY",
            "control_id": tree_id,
            "expected_type": "GuiShell",
            "expected_text": leaf_text,
            "node_key": leaf_key,
            "item_column": item_column,
            "expected_transaction": "SIMG",
        },
    )
    select_sales_organization_activity(
        session,
        {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": SALES_ORGANIZATION_ACTIVITY["window_id"],
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "table_id": SALES_ORGANIZATION_ACTIVITY["table_id"],
            "row_text": SALES_ORGANIZATION_ACTIVITY["row_text"],
            "button_id": SALES_ORGANIZATION_ACTIVITY["button_id"],
            "button_text": SALES_ORGANIZATION_ACTIVITY["button_text"],
        },
    )
    if str(session.identity.get("transaction") or "").upper() != "V_TVKO":
        raise ActionBlockedError("Recorded IMG navigation did not reach V_TVKO")


def _start_company_code_copy(session: Any) -> dict[str, Any]:
    """Select BE01 or resume the already-proven screen-41 target entry."""
    info = getattr(getattr(session, "raw", None), "Info", None)
    if (
        str(session.identity.get("transaction") or "").upper() == "V_T001"
        and str(getattr(info, "Program", "") or "").upper()
        in {"SAPLSZA1", "SAPLSPO1", "SAPMSDYP"}
    ):
        current = inspect_screen(session)
        current_popups = current.get("popups") or []
        if (
            any(
                popup.get("window_title") == COMPANY_CODE_ADDRESS_TITLE
                for popup in current_popups
            )
        ):
            return _complete_company_code_address_and_save(session)
    _open_company_code_screen_from_vbs(session)
    lookup = _lookup_company_code_1010(session)
    if lookup.get("state") != "MISSING":
        raise ActionBlockedError(
            "Company-code copy requires a fresh LOOKUP=MISSING; "
            f"observed {lookup.get('state')!r}"
        )
    if (lookup.get("evidence") or {}).get("method") == "PENDING_COPY_TARGET_ENTRY":
        return _complete_company_code_target_entry(session)
    popup = _select_company_code_template_and_open_copy(session, phase="PROVISION")
    if popup.get("destination") == "TARGET_ENTRY_SCREEN":
        return _complete_company_code_target_entry(session)
    return {
        "provisioning_blocked": True,
        "reason": (
            "Copy popup is open; its live field contract must be verified "
            "before entering source or target values"
        ),
        "copy_popup": popup,
    }


def _select_company_code_template_and_open_copy(
    session: Any, *, phase: str
) -> dict[str, Any]:
    """Select exactly one live BE01 row and inspect the result of Copy."""
    expected_transaction = "V_T001"
    expected_program = "SAPL0ORG"
    table_id = COMPANY_CODE_TABLE_SEARCH["table_id"]
    button_id = COMPANY_CODE_VBS_CONTROLS["copy_button"]
    expected_button_id = "/app/con[0]/ses[0]/" + button_id
    snapshot = inspect_screen(session)
    variant = next(
        (
            item
            for item in COMPANY_CODE_TABLE_VARIANTS
            if item.get("window_title") == snapshot.get("window_title")
        ),
        None,
    )
    tables = [
        item for item in snapshot.get("tables") or []
        if item.get("id") == table_id and item.get("type") == "GuiTableControl"
    ]
    copy_buttons = [
        item for item in snapshot.get("buttons") or []
        if item.get("id") == expected_button_id
        and item.get("type") == "GuiButton"
        and " ".join(str(item.get("tooltip") or "").split())
        == "Copier sous... (F6)"
        and item.get("changeable") is True
    ]
    if (
        str(snapshot.get("transaction") or "").upper() != expected_transaction
        or str(snapshot.get("program") or "").upper() != expected_program
        or variant is None
        or len(tables) != 1
        or len(copy_buttons) != 1
        or snapshot.get("popups")
    ):
        raise ActionBlockedError(
            "Company-code template copy requires the exact live V_T001 "
            "table and Copy button contract"
        )

    try:
        table = session.find(table_id)
        row_count = int(table.RowCount)
        visible_rows = int(table.VisibleRowCount)
        scrollbar = table.VerticalScrollbar
        position = int(scrollbar.Position)
        maximum = int(scrollbar.Maximum)
    except Exception as exc:
        raise ActionBlockedError(
            f"Company-code template table dimensions/scrollbar unavailable: {exc}"
        ) from exc
    if row_count <= 0 or row_count > 10000 or visible_rows <= 0:
        raise ActionBlockedError("Company-code template table dimensions are unsafe")

    try:
        if position != 0:
            scrollbar.Position = 0
            _wait_not_busy(session)
        found_rows: list[int] = []
        covered: set[int] = set()
        visited: set[int] = set()
        selected_before: list[int] = []
        while len(covered) < row_count:
            table = session.find(table_id)
            scrollbar = table.VerticalScrollbar
            get_absolute_row = getattr(table, "GetAbsoluteRow", None)
            position = int(scrollbar.Position)
            maximum = int(scrollbar.Maximum)
            if (
                int(table.RowCount) != row_count
                or int(table.VisibleRowCount) != visible_rows
                or not callable(get_absolute_row)
                or position < 0
                or position > maximum
                or position in visited
            ):
                raise ActionBlockedError(
                    f"Company-code template scan position/dimensions invalid at {position}"
                )
            visited.add(position)
            for absolute_row in range(
                position, min(position + visible_rows, row_count)
            ):
                relative_row = absolute_row - position
                cell_id = f"{variant['bukrs_cell_prefix']}{relative_row}]"
                cell = session.find(cell_id)
                if (
                    str(getattr(cell, "Id", "")) != cell_id
                    or str(getattr(cell, "Type", "")) != "GuiCTextField"
                ):
                    raise ActionBlockedError(
                        f"Company-code BUKRS cell contract mismatch at row {absolute_row}"
                    )
                if str(getattr(cell, "Text", "") or "").strip() == "BE01":
                    found_rows.append(absolute_row)
                try:
                    row = get_absolute_row(absolute_row)
                    if not hasattr(row, "Selected"):
                        raise ActionBlockedError(
                            "V_T001 visible row does not expose Selected state"
                        )
                    if bool(row.Selected):
                        selected_before.append(absolute_row)
                except ActionBlockedError:
                    raise
                except Exception as exc:
                    raise ActionBlockedError(
                        "V_T001 GetAbsoluteRow(absolute-index selection) failed for visible "
                        f"row {absolute_row}: {exc}"
                    ) from exc
                covered.add(absolute_row)
            if len(covered) == row_count:
                break
            next_position = min(position + visible_rows, maximum)
            if next_position <= position:
                raise ActionBlockedError(
                    "Company-code template scan stalled before covering RowCount"
                )
            scrollbar.Position = next_position
            _wait_not_busy(session)
            moved_table = session.find(table_id)
            moved_position = int(moved_table.VerticalScrollbar.Position)
            if moved_position <= position or moved_position > position + visible_rows:
                raise ActionBlockedError(
                    "Company-code template scan moved unpredictably: "
                    f"{position} -> {moved_position}"
                )
    except ActionBlockedError:
        raise
    except Exception as exc:
        raise ActionBlockedError(
            f"Company-code template scan failed before selection: {exc}"
        ) from exc

    if len(covered) != row_count or len(found_rows) != 1:
        raise ActionBlockedError(
            "Company-code template BE01 row is missing or ambiguous: "
            f"matches={found_rows!r}, covered={len(covered)}, row_count={row_count}"
        )
    source_row = found_rows[0]
    try:
        if selected_before and selected_before != [source_row]:
            raise ActionBlockedError(
                f"Refusing copy with preselected rows: {selected_before!r}"
            )
        get_absolute_row = getattr(table, "GetAbsoluteRow", None)
        if not callable(get_absolute_row):
            raise ActionBlockedError("V_T001 GetAbsoluteRow capability disappeared")
        if not selected_before:
            session.audit(
                "SELECT_COMPANY_CODE_COPY_SOURCE",
                control_id=table_id,
                control_text="live BUKRS row selection",
                value={"company_code": "BE01", "row_index": source_row},
            )
            table = session.find(table_id)
            scrollbar = table.VerticalScrollbar
            scrollbar.Position = source_row
            _wait_not_busy(session)
            table = session.find(table_id)
            scrollbar = table.VerticalScrollbar
            source_position = int(scrollbar.Position)
            relative_row = source_row - source_position
            if relative_row < 0 or relative_row >= int(table.VisibleRowCount):
                raise ActionBlockedError(
                    f"BE01 row {source_row} is not visible after positioning"
                )
            source_cell_id = f"{variant['bukrs_cell_prefix']}{relative_row}]"
            source_cell = session.find(source_cell_id)
            if str(getattr(source_cell, "Text", "") or "").strip() != "BE01":
                raise ActionBlockedError(
                    "BE01 row changed while positioning for selection"
                )
            get_absolute_row = getattr(table, "GetAbsoluteRow", None)
            if not callable(get_absolute_row):
                raise ActionBlockedError("V_T001 GetAbsoluteRow capability disappeared")
            source = get_absolute_row(source_row)
            if not hasattr(source, "Selected") or bool(source.Selected):
                raise ActionBlockedError(
                    "BE01 visible row is not in a selectable, unselected state"
                )
            source.Selected = True

        table = session.find(table_id)
        table.VerticalScrollbar.Position = 0
        _wait_not_busy(session)
        table = session.find(table_id)
        if int(table.VerticalScrollbar.Position) != 0:
            raise ActionBlockedError(
                "V_T001 selection verification could not return to row zero"
            )
        selected_after = []
        verified: set[int] = set()
        checked_positions: set[int] = set()
        while len(verified) < row_count:
            table = session.find(table_id)
            scrollbar = table.VerticalScrollbar
            position = int(scrollbar.Position)
            maximum = int(scrollbar.Maximum)
            if position in checked_positions or position < 0 or position > maximum:
                raise ActionBlockedError(
                    f"V_T001 selection verification stalled at {position}"
                )
            checked_positions.add(position)
            for absolute_row in range(position, min(position + visible_rows, row_count)):
                row = table.GetAbsoluteRow(absolute_row)
                if bool(row.Selected):
                    selected_after.append(absolute_row)
                verified.add(absolute_row)
            if len(verified) == row_count:
                break
            next_position = min(position + visible_rows, maximum)
            if next_position <= position:
                raise ActionBlockedError(
                    "V_T001 selection verification did not cover RowCount"
                )
            scrollbar.Position = next_position
            _wait_not_busy(session)
        if selected_after != [source_row]:
            raise ActionBlockedError(
                "V_T001 selection verification failed: "
                f"expected={[source_row]!r}, observed={selected_after!r}"
            )
    except ActionBlockedError:
        raise
    except Exception as exc:
        raise ActionBlockedError(
            f"Company-code BE01 row selection failed closed: {exc}"
        ) from exc

    def press_copy() -> None:
        button = session.find(button_id)
        if (
            str(getattr(button, "Type", "")) != "GuiButton"
            or " ".join(str(getattr(button, "Tooltip", "") or "").split())
            != "Copier sous... (F6)"
        ):
            raise ActionBlockedError(
                f"Live Company Code copy button contract changed: {button_id}"
            )
        if selected_after != [source_row]:
            raise ActionBlockedError(
                "Copy button not invoked because BE01 was not the sole "
                f"verified selection: {selected_after!r}"
            )
        press = getattr(button, "press", None) or getattr(button, "Press", None)
        if not callable(press):
            raise ActionBlockedError("Live Company Code copy button is not pressable")
        press()
        _wait_not_busy(session)

    _company_code_provision_step(
        session,
        "press_copy_after_verified_BE01_selection",
        button_id,
        press_copy,
        phase=phase,
    )
    after = inspect_screen(session)
    popups = [
        item for item in after.get("popups") or []
        if item.get("id") == "/app/con[0]/ses[0]/wnd[1]"
    ]
    if len(popups) == 1 and len(after.get("popups") or []) == 1:
        return {
            "destination": "POPUP",
            "window_title": popups[0].get("window_title"),
            "program": str(
                getattr(getattr(session.raw, "Info", None), "Program", "") or ""
            ) or None,
            "screen_number": str(
                getattr(getattr(session.raw, "Info", None), "ScreenNumber", "") or ""
            ) or None,
            "controls": popups[0].get("controls", []),
            "control_ids": popups[0].get("control_ids", []),
            "buttons": popups[0].get("buttons", []),
            "input_fields": popups[0].get("input_fields", []),
            "selected_source_row": source_row,
        }

    target_fields = [
        field for field in after.get("input_fields") or []
        if field.get("id") == "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T001-BUKRS"
        and field.get("type") == "GuiCTextField"
        and field.get("changeable") is True
        and field.get("visible") is True
        and field.get("text") == "BE01"
    ]
    if (
        not after.get("popups")
        and str(after.get("transaction") or "").upper() == expected_transaction
        and str(after.get("program") or "").upper() == expected_program
        and after.get("screen_number") == "41"
        and after.get("window_title")
        == 'Modifier vue "Société" : détail ensemble de sélection'
        and len(target_fields) == 1
    ):
        return {
            "destination": "TARGET_ENTRY_SCREEN",
            "screen": {
                "transaction": after.get("transaction"),
                "program": after.get("program"),
                "screen_number": after.get("screen_number"),
                "window_title": after.get("window_title"),
                "status_bar": after.get("status_bar"),
            },
            "target_entry_control": target_fields[0],
            "selected_source_row": source_row,
            "stopped_before_target_entry": True,
        }

    if len(popups) != 1 or len(after.get("popups") or []) != 1:
        raise ActionBlockedError(
            "Copy action did not open exactly one wnd[1] after selecting "
            f"BE01 row {source_row}; popup_ids="
            f"{[item.get('id') for item in after.get('popups') or []]!r}, "
            f"status={after.get('status_bar')!r}"
        )
    raise ActionBlockedError("Copy action reached an unsupported SAP screen")


def _inspect_company_code_copy_dialog(session: Any) -> dict[str, Any]:
    """Open the live copy action and inspect wnd[1] without entering values."""
    lookup = _lookup_company_code_1010(session)
    if lookup.get("state") != "MISSING":
        raise ActionBlockedError(
            "Company-code copy dialog inspection requires a live MISSING lookup; "
            f"observed {lookup.get('state')!r}"
        )
    if str(session.identity.get("transaction") or "").upper() != "V_T001":
        raise ActionBlockedError(
            "Company-code copy dialog inspection requires transaction V_T001"
        )
    copy_popup = _select_company_code_template_and_open_copy(
        session, phase="COPY_DIALOG_INSPECT"
    )
    if copy_popup.get("destination") == "TARGET_ENTRY_SCREEN":
        return {
            "state": "MISSING",
            "stopped_before_field_entry": True,
            "selected_source_row": copy_popup["selected_source_row"],
            "screen": copy_popup["screen"],
            "target_entry_control": copy_popup["target_entry_control"],
        }
    return {
        "state": "MISSING",
        "stopped_before_field_entry": True,
        "selected_source_row": copy_popup["selected_source_row"],
        "wnd1": copy_popup,
    }


def execute_runner_action(session: Any, request: dict[str, Any]) -> dict[str, Any]:
    """Run recorded Phase 5 operations and fail closed on unsupported GUI flows."""
    session.audit(
        "PHASE5_OPERATION",
        value={
            "operation": request["params"]["operation"],
            "phase": request["params"]["phase"],
        },
    )
    params = request["params"]
    operation = params["operation"]
    phase = params["phase"]
    if operation == "S4615_ZF01_ACCOUNTING_BLOCK":
        from .s4615_zf01_accounting_block_gui import (
            TARGET as ZF01_TARGET, VALUES as ZF01_VALUES,
            save_once, confirm_transport, verify_readback,
        )
        if params["target"] != ZF01_TARGET:
            raise ActionBlockedError("ZF01 accounting-block target mismatch")
        if phase == "PROVISION" and params["values"] == ZF01_VALUES:
            return save_once(session)
        if phase == "PROVISION" and params["values"] == {"confirm_transport": "A4HK908422"}:
            return confirm_transport(session)
        if phase == "READBACK" and params["values"] == {}:
            return verify_readback(session)
        raise ActionBlockedError("ZF01 accounting-block phase or values not allowlisted")
    if operation == "S4615_VTFLC_ZF01_LF_TAN":
        from .s4615_vtflc_gui import prepare_header, prepare_item, save_once, confirm_transport, verify_header, verify_item
        if params["target"] != {"billing_type": "ZF01", "delivery_type": "LF", "item_category": "TAN"}:
            raise ActionBlockedError("S4615 VTFLC target mismatch")
        if phase != "PROVISION":
            raise ActionBlockedError("S4615 VTFLC supports only exact provision steps")
        values = params["values"]
        if values == {"step": "prepare_header"}:
            return prepare_header(session)
        if values == {"step": "save_header"}:
            return save_once(session, "header")
        if values == {"step": "prepare_item"}:
            return prepare_item(session)
        if values == {"step": "save_item"}:
            return save_once(session, "item")
        if values == {"step": "confirm_transport_header"}:
            return confirm_transport(session, "header")
        if values == {"step": "confirm_transport_item"}:
            return confirm_transport(session, "item")
        if values == {"step": "verify_header"}:
            return verify_header(session)
        if values == {"step": "verify_item"}:
            return verify_item(session)
        raise ActionBlockedError("S4615 VTFLC write step is not allowlisted")
    if operation == "S4615_SHIPPING_POINT_1010_BE":
        from .s4615_shipping_point_be_gui import (
            TARGET as SHIPPING_TARGET, provision_once, confirm_address, confirm_transport,
            verify_readback,
        )
        if params["target"] != SHIPPING_TARGET:
            raise ActionBlockedError("Shipping point BE target mismatch")
        if phase == "LOOKUP" and params["values"] == {}:
            from .s4615_shipping_point_gui import lookup_from_snapshot
            return lookup_from_snapshot(inspect_screen(session))
        if phase == "PROVISION":
            return provision_once(session, params["target"], params["values"])
        if phase == "RECONCILE" and params["values"] == {}:
            return confirm_address(session)
        if phase == "RECONCILE_CONFIRM" and params["values"] == {}:
            return confirm_transport(session)
        if phase == "READBACK" and params["values"] == {}:
            return verify_readback(session)
        raise ActionBlockedError("Unsupported shipping point BE phase or values")
    if operation == "S4615_SHIPPING_POINT_1010":
        from .s4615_shipping_point_gui import TARGET, inspect_new_entry_form, lookup_from_snapshot, save_once, cancel_empty_address_popup, confirm_discard_address
        if params["target"] != TARGET:
            raise ActionBlockedError("Shipping point 1010 target mismatch")
        if phase == "LOOKUP":
            if params["values"] != {}:
                raise ActionBlockedError("Shipping point 1010 LOOKUP takes no values")
            return lookup_from_snapshot(inspect_screen(session))
        if phase == "FORM_INSPECT":
            if params["values"] != {}:
                raise ActionBlockedError("Shipping point 1010 FORM_INSPECT takes no values")
            return inspect_new_entry_form(session)
        if phase == "PROVISION":
            return save_once(session, params["target"], params["values"])
        if phase == "RECONCILE":
            if params["values"] != {}:
                raise ActionBlockedError("Shipping point 1010 RECONCILE takes no values")
            return cancel_empty_address_popup(session)
        if phase == "RECONCILE_CONFIRM":
            if params["values"] != {}:
                raise ActionBlockedError("Shipping point 1010 RECONCILE_CONFIRM takes no values")
            return confirm_discard_address(session)
        raise ActionBlockedError("Shipping point 1010 write contract is not yet evidenced")
    if operation == "S4615_PRODUCT_P101_BASIC_ROOT":
        from .s4615_product_basic_gui import prepare_basic_data_1, prepare_basic_views, prepare_initial_screen, save_basic_root_once
        if phase == "MM01_INITIAL_PREPARE":
            return prepare_initial_screen(session, params["target"], params["values"])
        if phase == "MM01_VIEWS_PREPARE":
            return prepare_basic_views(session, params["target"], params["values"])
        if phase == "MM01_BASIC1_PREPARE":
            return prepare_basic_data_1(session, params["target"], params["values"])
        if phase == "PROVISION":
            return save_basic_root_once(session, params["target"], params["values"])
        raise ActionBlockedError("P615-101 root SAVE is unsupported until the remaining MM01 screens are evidenced")
    if operation == "ENSURE_BP_STANDARD_ADDRESS":
        from .s4615_bp_address_gui import TARGET, save_once
        if params["target"] != TARGET or phase != "PROVISION":
            raise ActionBlockedError("BP standard address only supports exact one-shot PROVISION")
        return save_once(session, params["target"], params["values"])
    if operation == "S4600_T_S50A01_BP_ADDRESS":
        from .s4600_t_s50a01_bp_address_gui import TARGET, save_once
        if params["target"] != TARGET or phase != "PROVISION":
            raise ActionBlockedError("T-S50A01 BP address only supports exact one-shot PROVISION")
        return save_once(session, params["target"], params["values"])
    if operation == "S4615_SALES_TYPE_ZA01":
        if params["target"] != {"sales_order_type": "ZA01"}:
            raise ActionBlockedError("ZA01 target mismatch")
        if phase == "PROVISION":
            if params["values"] == {"close_saved_info": "ZA01"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program"), snapshot.get("status_bar", {}).get("text")) != ("VOV8", "SAPMSSY0", "Données sauvegardées") or len(popups) != 1:
                    raise ActionBlockedError("ZA01 saved-information close requires exact post-save state")
                popup = popups[0]
                labels = {label.get("text") for label in popup.get("labels", [])}
                continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Gestion des vues de table : écran initial" or popup.get("input_fields") or not {"T184", "TVAKZ", "TVASP", "TVCPA", "TVCPF", "TVCPL"}.issubset(labels) or not any(button.get("id") == continue_id and button.get("type") == "GuiButton" and button.get("tooltip") == "Weiter   (Entrée)" for button in popup.get("buttons", [])):
                    raise ActionBlockedError("ZA01 saved transport-information popup mismatch")
                button = session.find(continue_id)
                if str(getattr(button, "Id", "")) != continue_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Tooltip", "")) != "Weiter   (Entrée)":
                    raise ActionBlockedError("ZA01 saved-information Continue button mismatch")
                session.audit("PHASE5_OPERATION", control_id=continue_id, value={"target": "ZA01", "step": "close saved transport information"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZA01", "post_info": inspect_screen(session), "verified": False}
            if params["values"] == {"confirm_transport": "A4HK908422"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOV8", "SAPLSTRD", "300") or len(popups) != 1:
                    raise ActionBlockedError("ZA01 transport confirmation requires exact VOV8 Customizing request")
                popup = popups[0]
                fields = {field.get("id"): str(field.get("text") or "").strip() for field in popup.get("input_fields", [])}
                request_id = "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR"
                object_id = "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-OBJ_NAME"
                description_id = "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT"
                continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Demande : ordre du Customizing" or fields.get(request_id) != "A4HK908422" or fields.get(object_id) != "V_TVAK" or fields.get(description_id) != "S4615 Training Setup" or not any(button.get("id") == continue_id and button.get("type") == "GuiButton" and button.get("tooltip") == "Suite   (Entrée)" for button in popup.get("buttons", [])):
                    raise ActionBlockedError("ZA01 transport request, object or Continue button mismatch")
                button = session.find(continue_id)
                if str(getattr(button, "Id", "")) != continue_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Tooltip", "")) != "Suite   (Entrée)":
                    raise ActionBlockedError("ZA01 live transport Continue control mismatch")
                session.audit("PHASE5_OPERATION", control_id=continue_id, value={"target": "ZA01", "transport_request": "A4HK908422", "step": "confirm existing unreleased request"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZA01", "transport_request": "A4HK908422", "post_transport": inspect_screen(session), "verified": False}
            if params["values"] == {"save_pending": "ZA01"}:
                snapshot = inspect_screen(session)
                table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK"
                rows = [row for table in snapshot.get("tables", []) if table.get("id") == table_id for row in table.get("visible_rows", []) if any(value.get("column") == "0" and value.get("text") == "ZA01" for value in row.get("values", []))]
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOV8", "SAPL080O", "1010") or snapshot.get("popups") or snapshot.get("status_bar", {}).get("text") != "Nombre d'entrées copiées (traductions y compris) : 1" or len(rows) != 1 or not any(value.get("column") == "1" and value.get("text") == "cde Foire 01" for value in rows[0].get("values", [])):
                    raise ActionBlockedError("ZA01 Save requires the exact pending copied overview row")
                save_id = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
                if not any(button.get("id") == save_id and button.get("type") == "GuiButton" and button.get("text") == "Sauvegarder" for button in snapshot.get("buttons", [])):
                    raise ActionBlockedError("ZA01 exact Save button not observed")
                button = session.find(save_id)
                if str(getattr(button, "Id", "")) != save_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Sauvegarder":
                    raise ActionBlockedError("ZA01 live Save button mismatch")
                session.audit("PHASE5_OPERATION", control_id=save_id, value={"target": "ZA01", "step": "save exact pending sales document type"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZA01", "post_save": inspect_screen(session), "verified": False}
            if params["values"] == {"copy_control": "YES"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOV8", "SAPLSPO1", "300") or len(popups) != 1:
                    raise ActionBlockedError("ZA01 copy-control decision requires exact VOV8 popup")
                popup = popups[0]
                fields = {field.get("id"): field.get("text") for field in popup.get("input_fields", [])}
                diagnose = "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-DIAGNOSE1"
                question = "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-TEXTLINE1"
                yes_id = "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-OPTION1"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Entrées dépendantes pour pilotage copies" or fields.get(diagnose) != "Type doc. de vente : ZA01 -cde Foire 01 -" or fields.get(question) != "L'entrée concerne-t-elle aussi le pilotage copies ?" or not any(button.get("id") == yes_id and button.get("type") == "GuiButton" and button.get("text") == "Oui" for button in popup.get("buttons", [])):
                    raise ActionBlockedError("ZA01 copy-control popup content mismatch")
                button = session.find(yes_id)
                if str(getattr(button, "Id", "")) != yes_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Oui":
                    raise ActionBlockedError("ZA01 live copy-control Yes button mismatch")
                session.audit("PHASE5_OPERATION", control_id=yes_id, value={"target": "ZA01", "copy_control": "YES", "saved": False})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZA01", "copy_control": "COPIED_FROM_CS", "post_decision": inspect_screen(session), "saved": False}
            if params["values"] == {"confirm_target": "ZA01"}:
                snapshot = inspect_screen(session)
                expected = {"/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVAK-AUART": "ZA01", "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVAK-BEZEI": "cde Foire 01", "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVAK-FKARV": "ZF01", "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVAK-FKARA": "ZF01"}
                fields = {field.get("id"): field.get("text") for field in snapshot.get("input_fields", [])}
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")), snapshot.get("window_title")) != ("VOV8", "SAPL080O", "1011", 'Modifier vue "Gestion des types de commande client" : détail ensemble') or snapshot.get("popups") or snapshot.get("status_bar", {}).get("text") != "Indiquez les entrées cibles." or any(fields.get(key) != value for key, value in expected.items()):
                    raise ActionBlockedError("ZA01 Enter requires exact observed unsaved copy target")
                window_id = "/app/con[0]/ses[0]/wnd[0]"
                window = session.find(window_id)
                if str(getattr(window, "Id", "")) != window_id or str(getattr(window, "Type", "")) != "GuiMainWindow":
                    raise ActionBlockedError("ZA01 copy target main window mismatch")
                session.audit("PHASE5_OPERATION", control_id=window_id, value={"target": "ZA01", "step": "confirm copy target with Enter", "saved": False})
                window.sendVKey(0)
                _wait_not_busy(session)
                return {"target": "ZA01", "post_confirm": inspect_screen(session), "saved": False}
            expected_values = {"sales_order_type": "ZA01", "description": "cde Foire 01", "delivery_billing_type": "ZF01", "order_billing_type": "ZF01"}
            if params["values"] != expected_values:
                raise ActionBlockedError("ZA01 permits only the four Book-confirmed target fields")
            snapshot = inspect_screen(session)
            if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")), snapshot.get("window_title")) != ("VOV8", "SAPL080O", "1011", 'Modifier vue "Gestion des types de commande client" : détail ensemble') or snapshot.get("popups") or snapshot.get("status_bar", {}).get("text") != "Indiquez les entrées cibles.":
                raise ActionBlockedError("ZA01 target fields require exact unsaved VOV8 copy form")
            original = {field.get("id"): field for field in snapshot.get("input_fields", [])}
            changes = (
                ("/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVAK-AUART", "GuiTextField", "CS", "ZA01"),
                ("/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVAK-BEZEI", "GuiTextField", "Cmde client standard", "cde Foire 01"),
                ("/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVAK-FKARV", "GuiCTextField", "F2", "ZF01"),
                ("/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVAK-FKARA", "GuiCTextField", "F2", "ZF01"),
            )
            if any(original.get(control_id, {}).get("type") != control_type or original.get(control_id, {}).get("text") != before or original.get(control_id, {}).get("changeable") is not True for control_id, control_type, before, _ in changes):
                raise ActionBlockedError("ZA01 copy form does not contain the exact editable CS source fields")
            for control_id, control_type, _, after in changes:
                control = session.find(control_id)
                if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != control_type:
                    raise ActionBlockedError("ZA01 target control mismatch")
                session.audit("PHASE5_OPERATION", control_id=control_id, value={"target": "ZA01", "value": after, "saved": False})
                control.Text = after
            entered = inspect_screen(session)
            fields = {field.get("id"): field.get("text") for field in entered.get("input_fields", [])}
            if any(fields.get(control_id) != after for control_id, _, _, after in changes):
                raise ActionBlockedError("ZA01 unsaved target fields did not reflect exact values")
            return {"target": "ZA01", "entered": entered, "saved": False}
        if params["values"] != {} or phase != "COPY_DIALOG_INSPECT":
            raise ActionBlockedError("ZA01 phase or values are not evidenced")
        contract = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": "ZA01"}
        lookup = find_s4615_sales_type(session, contract)["sales_type_search"]
        if lookup["result"] != "CONFIRMED_NOT_FOUND":
            raise ActionBlockedError(f"ZA01 copy requires confirmed absence, got {lookup['result']}")
        reference = display_s4615_sales_reference(session, {**contract, "sales_order_type": "CS", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"})
        fields = {field["id"].rsplit("/", 1)[-1]: field.get("text") for field in reference["snapshot"].get("input_fields", [])}
        required = {"txtV_TVAK-AUART": "CS", "txtV_TVAK-BEZEI": "Cmde client standard", "ctxtV_TVAK-VBTYP": "C", "ctxtV_TVAK-LFARV": "LF", "ctxtV_TVAK-FKARV": "F2", "ctxtV_TVAK-FKARA": "F2"}
        if any(fields.get(key) != value for key, value in required.items()):
            raise ActionBlockedError("CS is not the observed standard order/delivery/billing reference")
        back(session)
        overview = inspect_screen(session)
        if (overview.get("transaction"), overview.get("program"), str(overview.get("screen_number"))) != ("VOV8", "SAPL080O", "1010") or "synthèse" not in str(overview.get("window_title") or ""):
            raise ActionBlockedError("VOV8 did not return to the sales-type overview")
        table = session.find(contract["table_id"])
        if str(getattr(table, "Id", "")) != contract["table_id"] or str(getattr(table, "Type", "")) != "GuiTableControl":
            raise ActionBlockedError("VOV8 source table mismatch after return")
        table.GetAbsoluteRow(reference["source_row"]).Selected = True
        copy_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[6]"
        button = session.find(copy_id)
        if str(getattr(button, "Id", "")) != copy_id or str(getattr(button, "Type", "")) != "GuiButton" or "Copier sous" not in str(getattr(button, "Tooltip", "")):
            raise ActionBlockedError("VOV8 exact Copy under button mismatch")
        session.audit("PHASE5_OPERATION", control_id=copy_id, control_text="Copier sous", value={"source": "CS", "target": "ZA01", "step": "open unsaved copy form"})
        button.press()
        _wait_not_busy(session)
        return {"source": "CS", "target": "ZA01", "copy_form": inspect_screen(session), "saved": False}
    if operation == "S4615_BILLING_TYPE_ZF01":
        if params["target"] != {"billing_type": "ZF01"}:
            raise ActionBlockedError("S4615 ZF01 target mismatch")
        if phase == "PROVISION":
            if params["values"] == {"close_saved_info": "ZF01"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program")) != ("VOFA", "SAPMSSY0") or snapshot.get("status_bar", {}).get("text") != "Données sauvegardées" or len(popups) != 1:
                    raise ActionBlockedError("ZF01 post-save information requires exact saved VOFA state")
                popup = popups[0]
                label_values = {label.get("text") for label in popup.get("labels", [])}
                continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Gestion des vues de table : écran initial" or popup.get("input_fields") or "TVFSP" not in label_values or "Entrées associées aux nouveaux objets" not in label_values:
                    raise ActionBlockedError("ZF01 post-save transport information popup mismatch")
                observed = [button for button in popup.get("buttons", []) if button.get("id") == continue_id and button.get("type") == "GuiButton" and "Weiter" in str(button.get("tooltip") or "")]
                if len(observed) != 1:
                    raise ActionBlockedError("ZF01 post-save Continue button mismatch")
                button = session.find(continue_id)
                if str(getattr(button, "Id", "")) != continue_id or str(getattr(button, "Type", "")) != "GuiButton" or "Weiter" not in str(getattr(button, "Tooltip", "")):
                    raise ActionBlockedError("ZF01 live post-save Continue button mismatch")
                session.audit("PHASE5_OPERATION", control_id=continue_id, value={"target": "ZF01", "step": "close saved transport information"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZF01", "post_info": inspect_screen(session), "verified": False}
            if params["values"] == {"confirm_transport": "A4HK908422"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program")) != ("VOFA", "SAPLSTRD") or len(popups) != 1:
                    raise ActionBlockedError("ZF01 transport requires exact VOFA Customizing request popup")
                popup = popups[0]
                fields = {field["id"]: str(field.get("text") or "").strip() for field in popup.get("input_fields", [])}
                expected_fields = {
                    "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-OBJ_NAME": "V_TVFK",
                    "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR": "A4HK908422",
                    "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT": "S4615 Training Setup",
                }
                continue_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Demande : ordre du Customizing" or any(fields.get(key) != value for key, value in expected_fields.items()):
                    raise ActionBlockedError("ZF01 transport request or V_TVFK object mismatch")
                observed = [button for button in popup.get("buttons", []) if button.get("id") == continue_id and button.get("type") == "GuiButton" and "Suite" in str(button.get("tooltip") or "")]
                if len(observed) != 1:
                    raise ActionBlockedError("ZF01 transport Continue control mismatch")
                button = session.find(continue_id)
                if str(getattr(button, "Id", "")) != continue_id or str(getattr(button, "Type", "")) != "GuiButton" or "Suite" not in str(getattr(button, "Tooltip", "")):
                    raise ActionBlockedError("ZF01 live transport Continue control mismatch")
                session.audit("PHASE5_OPERATION", control_id=continue_id, value={"target": "ZF01", "transport_request": "A4HK908422", "step": "confirm existing unreleased request"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZF01", "transport_request": "A4HK908422", "post_transport": inspect_screen(session), "verified": False}
            if params["values"] == {"save_verified_pending": "ZF01"}:
                snapshot = inspect_screen(session)
                fields = {field["id"]: field.get("text") for field in snapshot.get("input_fields", [])}
                expected_fields = {
                    "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART": "ZF01",
                    "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-NUMKI": "15",
                    "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVFK-VBTYP": "M",
                }
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOFA", "SAPL081F", "101") or snapshot.get("popups") or any(fields.get(key) != value for key, value in expected_fields.items()):
                    raise ActionBlockedError("ZF01 Save requires exact pending billing type, number range 15 and invoice category M")
                save_id = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
                observed = [button for button in snapshot.get("buttons", []) if button.get("id") == save_id and button.get("type") == "GuiButton" and button.get("text") == "Sauvegarder"]
                if len(observed) != 1:
                    raise ActionBlockedError("ZF01 exact Save control not observed")
                button = session.find(save_id)
                if str(getattr(button, "Id", "")) != save_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Sauvegarder":
                    raise ActionBlockedError("ZF01 live Save control mismatch")
                session.audit("PHASE5_OPERATION", control_id=save_id, value={"target": "ZF01", "step": "save only verified billing type"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZF01", "post_save": inspect_screen(session), "verified": False}
            if params["values"] == {"inspect_pending": "ZF01"}:
                snapshot = inspect_screen(session)
                table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK"
                detail_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"
                matches = [row for table in snapshot.get("tables", []) if table.get("id") == table_id for row in table.get("visible_rows", []) if any(value.get("column") == "0" and value.get("text") == "ZF01" for value in row.get("values", []))]
                if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOFA", "SAPL081F", "100") or snapshot.get("popups") or len(matches) != 1:
                    raise ActionBlockedError("ZF01 pending row is not uniquely visible in exact VOFA overview")
                table = session.find(table_id)
                if str(getattr(table, "Type", "")) != "GuiTableControl":
                    raise ActionBlockedError("ZF01 pending table type mismatch")
                absolute = int(table.VerticalScrollbar.Position) + int(matches[0]["index"])
                table.GetAbsoluteRow(absolute).Selected = True
                button = session.find(detail_id)
                if str(getattr(button, "Id", "")) != detail_id or str(getattr(button, "Type", "")) != "GuiButton" or "Détail" not in str(getattr(button, "Tooltip", "")):
                    raise ActionBlockedError("ZF01 detail control mismatch")
                session.audit("PHASE5_OPERATION", control_id=detail_id, value={"target": "ZF01", "step": "inspect unsaved detail"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZF01", "pending_detail": inspect_screen(session), "saved": False}
            if params["values"] == {"copy_control": "NO"}:
                snapshot = inspect_screen(session)
                popups = snapshot.get("popups") or []
                if (snapshot.get("transaction"), snapshot.get("program")) != ("VOFA", "SAPLSPO1") or len(popups) != 1:
                    raise ActionBlockedError("ZF01 copy-control decision requires exact VOFA SAPLSPO1 popup")
                popup = popups[0]
                fields = {field["id"]: field.get("text") for field in popup.get("input_fields", [])}
                diagnose = "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-DIAGNOSE1"
                question = "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-TEXTLINE1"
                no_id = "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-OPTION2"
                if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Entrées dépendantes pour pilotage copies" or fields.get(diagnose) != "type fact.: ZF01 -Facture -" or fields.get(question) != "L'entrée concerne-t-elle aussi le pilotage copies ?":
                    raise ActionBlockedError("ZF01 copy-control popup content mismatch")
                observed_no = [button for button in popup.get("buttons", []) if button.get("id") == no_id and button.get("type") == "GuiButton" and button.get("text") == "Non"]
                if len(observed_no) != 1:
                    raise ActionBlockedError("ZF01 copy-control No button mismatch")
                button = session.find(no_id)
                if str(getattr(button, "Id", "")) != no_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Non":
                    raise ActionBlockedError("ZF01 live copy-control No button mismatch")
                session.audit("PHASE5_OPERATION", control_id=no_id, value={"target": "ZF01", "copy_control": "NO"})
                button.press()
                _wait_not_busy(session)
                return {"target": "ZF01", "copy_control": "NOT_COPIED", "post_decision": inspect_screen(session), "saved": False}
            if params["values"] != {"billing_type": "ZF01", "number_range": "15"}:
                raise ActionBlockedError("S4615 ZF01 allows only target key and Book number range 15")
            snapshot = inspect_screen(session)
            fields = {field["id"]: field for field in snapshot.get("input_fields", [])}
            key_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART"
            range_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-NUMKI"
            if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VOFA", "SAPL081F", "101") or snapshot.get("popups"):
                raise ActionBlockedError("S4615 ZF01 requires exact unsaved VOFA copy target screen")
            if fields.get(key_id, {}).get("text") != "F2" or fields.get(range_id, {}).get("text") != "19" or not fields.get(key_id, {}).get("changeable") or not fields.get(range_id, {}).get("changeable"):
                raise ActionBlockedError("S4615 ZF01 copy target fields are not the observed F2 template")
            if "Indiquez les entrées cibles" not in str(snapshot.get("status_bar", {}).get("text") or ""):
                raise ActionBlockedError("S4615 ZF01 copy target prompt mismatch")
            for control_id, value in ((key_id, "ZF01"), (range_id, "15")):
                control = session.find(control_id)
                if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != "GuiTextField":
                    raise ActionBlockedError("S4615 ZF01 target input control mismatch")
                session.audit("PHASE5_OPERATION", control_id=control_id, value={"target": "ZF01", "value": value})
                control.Text = value
            after_entry = inspect_screen(session)
            entered = {field["id"]: field.get("text") for field in after_entry.get("input_fields", [])}
            if entered.get(key_id) != "ZF01" or entered.get(range_id) != "15":
                raise ActionBlockedError("S4615 ZF01 target entry did not reflect exact requested values")
            session.audit("PHASE5_OPERATION", control_id="/app/con[0]/ses[0]/wnd[0]", value={"target": "ZF01", "step": "confirm copy target with Enter"})
            session.find("/app/con[0]/ses[0]/wnd[0]").sendVKey(0)
            _wait_not_busy(session)
            return {"target": "ZF01", "number_range": "15", "post_confirm": inspect_screen(session), "saved": False}
        if phase != "COPY_DIALOG_INSPECT" or params["values"] != {}:
            raise ActionBlockedError("S4615 ZF01 unsupported phase or values")
        contract = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "ZF01"}
        lookup = find_s4615_billing_type(session, contract)["billing_type_search"]
        if lookup["result"] != "CONFIRMED_NOT_FOUND":
            raise ActionBlockedError(f"ZF01 copy requires confirmed absence, got {lookup['result']}")
        reference = display_s4615_f2_reference(session, {**contract, "billing_type": "F2", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"})
        fields = {field["id"].rsplit("/", 1)[-1]: field.get("text") for field in reference["snapshot"].get("input_fields", [])}
        if fields.get("txtV_TVFK-FKART") != "F2" or fields.get("txtV_TVFK-VTEXT") != "Facture" or fields.get("ctxtV_TVFK-VBTYP") != "M":
            raise ActionBlockedError("F2 is not the expected standard invoice reference")
        back(session)
        overview = inspect_screen(session)
        if overview.get("transaction") != "VOFA" or overview.get("program") != "SAPL081F" or "synthèse" not in str(overview.get("window_title") or ""):
            raise ActionBlockedError("VOFA did not return to billing-type overview")
        table = session.find(contract["table_id"])
        row = table.GetAbsoluteRow(reference["source_row"])
        row.Selected = True
        copy_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[6]"
        copy_button = session.find(copy_id)
        if str(getattr(copy_button, "Id", "")) != copy_id or str(getattr(copy_button, "Type", "")) != "GuiButton" or "Copier sous" not in str(getattr(copy_button, "Tooltip", "")):
            raise ActionBlockedError("VOFA exact Copy under button mismatch")
        session.audit("PHASE5_OPERATION", control_id=copy_id, control_text="Copier sous", value={"source": "F2", "target": "ZF01", "step": "open unsaved copy form"})
        copy_button.press()
        _wait_not_busy(session)
        return {"source": "F2", "target": "ZF01", "copy_form": inspect_screen(session)}
    if operation == "VOV4_ITEM_CATEGORY_DETERMINATION":
        contract_id = str((params.get("target") or {}).get("contract_id") or "")
        contract = _vov4_contract(contract_id)
        if params["target"] != {"contract_id": contract_id}:
            raise ActionBlockedError("VOV4 target must contain only the allowlisted contract_id")
        if phase == "LOOKUP":
            if params["values"]:
                raise ActionBlockedError("VOV4 LOOKUP does not accept write values")
            return _lookup_vov4(session, contract)
        if phase == "PROVISION":
            allowed_values = {
                "transport_request": contract["transport_request"],
                "resume_exact_pending_row": True,
            }
            if params["values"] not in (
                {"transport_request": contract["transport_request"]},
                allowed_values,
            ):
                raise ActionBlockedError("VOV4 transport/value contract mismatch")
            return _provision_vov4(
                session,
                contract,
                resume_exact_pending_row=params["values"].get(
                    "resume_exact_pending_row", False
                ),
            )
        if phase == "READBACK":
            if params["values"]:
                raise ActionBlockedError("VOV4 READBACK does not accept write values")
            open_transaction(session, "VOV4")
            lookup = _lookup_vov4(session, contract)
            return {
                "verified": lookup["state"] == "EXISTS",
                "state": lookup["state"],
                "object": contract["target"] if lookup["state"] == "EXISTS" else None,
                "evidence": lookup["evidence"],
            }
        raise ActionBlockedError(f"Unsupported VOV4 phase: {phase}")
    if phase == "COPY_DIALOG_INSPECT":
        if (
            operation != "COMPANY_CODE_1010"
            or params["target"] != EXPECTED_TARGETS["COMPANY_CODE_1010"]
            or params["values"] != {}
        ):
            raise ActionBlockedError(
                "COPY_DIALOG_INSPECT requires the exact COMPANY_CODE_1010 "
                "target and empty values"
            )
        return _inspect_company_code_copy_dialog(session)
    if operation in PHASE5_ASSIGNMENT_TABLE_SEARCHES:
        if params["target"] != EXPECTED_TARGETS[operation]:
            raise ActionBlockedError(f"{operation} target mismatch")
        if phase == "LOOKUP":
            return _lookup_assignment(session, operation)
        if phase == "PROVISION":
            return _provision_assignment_existing_row(session, operation)
        if phase == "READBACK":
            lookup = _lookup_assignment(session, operation)
            exists = lookup["state"] == "EXISTS"
            return {
                "verified": exists,
                "state": lookup["state"],
                "object": EXPECTED_TARGETS[operation] if exists else None,
                "evidence": lookup["evidence"],
                "reason": None if exists else "assignment tuple was not verified",
            }
        raise ActionBlockedError(f"Unsupported {operation} phase: {phase}")
    if operation in {"CUSTOMER_C615_D00", "PRODUCT_P615_400"}:
        reason = (
            f"{operation} has no captured SAP GUI object lookup, creation, "
            "or independent readback screen/control contract"
        )
        if params["phase"] == "LOOKUP":
            return {"state": "UNKNOWN", "reason": reason}
        if params["phase"] == "PROVISION":
            return {"provisioning_blocked": True, "reason": reason}
        return {"verified": False, "state": "UNKNOWN", "reason": reason}
    if operation == "SALES_ORGANIZATION_1010":
        if params["target"] != EXPECTED_TARGETS["SALES_ORGANIZATION_1010"]:
            raise ActionBlockedError("SALES_ORGANIZATION_1010 target mismatch")
        if phase == "LOOKUP":
            return _lookup_sales_organization_1010(session)
        if phase == "PROVISION":
            if params["values"].get("technical_template") != EXPECTED_TEMPLATES[
                "SALES_ORGANIZATION_1010"
            ]:
                raise ActionBlockedError(
                    "SALES_ORGANIZATION_1010 technical template mismatch"
                )
            return _start_sales_organization_copy(session, params["values"])
        if phase == "READBACK":
            lookup = _lookup_sales_organization_1010(session)
            exists = lookup["state"] == "EXISTS"
            return {
                "verified": exists,
                "state": lookup["state"],
                "verification_scope": "EXISTENCE" if exists else None,
                "object": EXPECTED_TARGETS["SALES_ORGANIZATION_1010"] if exists else None,
                "evidence": lookup.get("evidence"),
                "reason": (
                    None
                    if exists
                    else (
                        "Sales Organization 1010 was not confirmed by independent "
                        "V_TVKO lookup"
                    )
                ),
            }
        raise ActionBlockedError(
            f"Unsupported SALES_ORGANIZATION_1010 phase: {phase}"
        )
    if operation != "COMPANY_CODE_1010":
        raise ActionBlockedError("Phase5 operation has no recorded SAP GUI script")
    if params["target"] != EXPECTED_TARGETS["COMPANY_CODE_1010"]:
        raise ActionBlockedError("COMPANY_CODE_1010 target mismatch")
    if phase == "LOOKUP":
        return _lookup_company_code_1010(session)
    if phase == "PROVISION":
        values = params["values"]
        required = {
            "technical_template": "BE01",
            "company_name": "S4615 Training Company",
            "currency": "EUR",
            "language": "EN",
            "chart_of_accounts": "INT",
        }
        if any(values.get(key) != value for key, value in required.items()):
            raise ActionBlockedError("COMPANY_CODE_1010 mandatory values mismatch")
        try:
            return _start_company_code_copy(session)
        except ActionBlockedError as exc:
            return {"unexpected_popup": True, "reason": str(exc)}
    if phase == "READBACK":
        current = inspect_screen(session)
        if current.get("popups"):
            return {
                "verified": False,
                "state": "UNKNOWN",
                "object": None,
                "evidence": {"post_save_state": _post_save_state(current)},
                "reason": "Company Code readback requires a popup-free committed state",
            }
        # A V_T001 maintenance buffer is not persistence evidence. Leave the
        # view completely and re-enter it before scanning T001.
        open_transaction(session, "SPRO")
        lookup = _lookup_company_code_1010(session)
        exists = lookup["state"] == "EXISTS"
        return {
            "verified": exists,
            "state": lookup["state"],
            "object": EXPECTED_TARGETS["COMPANY_CODE_1010"] if exists else None,
            "evidence": lookup.get("evidence"),
            "reason": None if exists else "Company Code 1010 was not found by independent lookup",
        }
    raise ActionBlockedError(f"Unsupported COMPANY_CODE_1010 phase: {phase}")


def _contains_protected_sales_order(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            str(key).casefold() in {"sales_order", "salesorder"}
            and str(item) == "148"
            or _contains_protected_sales_order(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_protected_sales_order(item) for item in value)
    return False


class SapGuiPhase5Backend:
    """Synchronous adapter implementing ``ProvisioningBackend`` exactly."""

    writable = True

    def __init__(
        self,
        *,
        timeout_seconds: float = 60.0,
        sender: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self._sender = sender or self._filesystem_send

    def _filesystem_send(self, phase: str, params: dict[str, Any]) -> dict[str, Any]:
        queued = enqueue_request(
            "PHASE5_OPERATION",
            {**params, "phase": phase},
            mode="EXECUTE",
        )
        return wait_for_response(
            queued["request_id"], timeout_seconds=self.timeout_seconds
        )

    @staticmethod
    def _validate_call(
        operation: str,
        target: dict[str, Any],
        values: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        operation = str(operation).upper()
        expected = EXPECTED_TARGETS.get(operation)
        if expected is None:
            raise ValueError(f"Phase5 operation is not allowlisted: {operation}")
        if target != expected:
            raise ValueError(f"Phase5 target mismatch for {operation}")
        safe_values = deepcopy(values or {})
        if _contains_protected_sales_order(safe_values):
            raise ValueError("Sales Order 148 is protected")
        template = EXPECTED_TEMPLATES.get(operation)
        if template and safe_values and safe_values.get("technical_template") != template:
            raise ValueError(f"Technical template mismatch for {operation}")
        return operation, deepcopy(expected), safe_values

    def _call(
        self,
        phase: str,
        operation: str,
        target: dict[str, Any],
        values: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        operation, target, values = self._validate_call(operation, target, values)
        response = self._sender(
            phase,
            {"operation": operation, "target": target, "values": values},
        )
        if not isinstance(response, dict):
            raise RuntimeError("SAP GUI runner returned a non-object response")
        if response.get("status") != "SUCCESS":
            error = response.get("error") or {}
            raise RuntimeError(str(error.get("message") or "SAP GUI runner failed"))
        sap = response.get("sap")
        expected_identity = {
            "system": EXPECTED_SYSTEM,
            "client": EXPECTED_CLIENT,
            "user": EXPECTED_USER,
        }
        actual_identity = {
            "system": str((sap or {}).get("system", "")).upper(),
            "client": str((sap or {}).get("client", "")),
            "user": str((sap or {}).get("user", "")).upper(),
        }
        if actual_identity != expected_identity:
            raise RuntimeError("SAP GUI runner identity mismatch")
        result = response.get("result")
        if not isinstance(result, dict):
            raise RuntimeError("SAP GUI runner result must be an object")
        return result

    def lookup(self, operation: str, target: dict[str, Any]) -> str:
        result = self._call("LOOKUP", operation, target)
        state = result.get("state")
        if state not in {"EXISTS", "MISSING", "UNKNOWN"}:
            raise RuntimeError(f"Invalid SAP lookup state: {state}")
        return state

    def provision(
        self,
        operation: str,
        target: dict[str, Any],
        values: dict[str, Any],
    ) -> dict[str, Any]:
        result = self._call("PROVISION", operation, target, values)
        terminal_flags = {
            "accepted", "transport_request", "unexpected_popup", "ambiguous_save",
            "provisioning_blocked",
        }
        if not any(flag in result for flag in terminal_flags):
            return {
                "ambiguous_save": True,
                "reason": "runner returned no deterministic write outcome",
            }
        return result

    def readback(
        self, operation: str, target: dict[str, Any]
    ) -> dict[str, Any] | None:
        result = self._call("READBACK", operation, target)
        return result.get("object") if result.get("verified") is True else None


def create_backend() -> SapGuiPhase5Backend:
    return SapGuiPhase5Backend()
