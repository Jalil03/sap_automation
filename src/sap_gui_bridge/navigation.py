"""Allowlisted, non-persistent SAP GUI navigation operations."""

from __future__ import annotations

import json
import re
import time
import unicodedata
from typing import Any

from .errors import ActionBlockedError
from .inspection import inspect_screen, read_tree_node_text
from .session import SapGuiSession


BLOCKED_NAVIGATION_TERMS = {
    "save",
    "sauvegarder",
    "enregistrer",
    "create",
    "creer",
    "new entries",
    "nouvelles entrees",
    "change",
    "modifier",
    "delete",
    "supprimer",
    "release",
    "liberer",
    "transport",
    "copy",
    "copier",
    "activate",
    "activer",
}
TREE_OPERATIONS = {
    "SELECT_TREE_NODE",
    "EXPAND_TREE_NODE",
    "COLLAPSE_TREE_NODE",
    "DOUBLE_CLICK_TREE_NODE",
    "OPEN_IMG_ACTIVITY",
}
FOCUS_TYPES = {
    "GuiButton",
    "GuiLabel",
    "GuiMainWindow",
    "GuiMenu",
    "GuiShell",
    "GuiTab",
    "GuiTextView",
    "GuiTree",
}
COMPANY_CODE_DISPLAY_EXCEPTION = {
    "transaction": "SIMG",
    "program": "SAPLSHI01",
    "control_id": "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell",
    "parent_text": "Comptabilité financière",
    "node_text": "Traiter, copier, supprimer, contrôler société",
    "operations": {"SELECT_TREE_NODE", "DOUBLE_CLICK_TREE_NODE", "OPEN_IMG_ACTIVITY"},
}
SALES_ORGANIZATION_DISPLAY_EXCEPTION = {
    "transaction": "SIMG",
    "program": "SAPLSHI01",
    "control_id": "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell",
    "path": (
        "Structure de l'entreprise",
        "Définition",
        "Administration des ventes (ADV)",
    ),
    "node_text": "Définir, copier, supprimer, contrôler org. commerciale",
    "operation": "OPEN_IMG_ACTIVITY",
}
DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION = {
    "transaction": "SIMG",
    "program": "SAPLSHI01",
    "control_id": "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell",
    "path": (
        "Structure de l'entreprise",
        "Définition",
        "Administration des ventes (ADV)",
    ),
    "node_text": "Définir, copier, supprimer, contrôler canal de distribution",
    "operation": "OPEN_IMG_ACTIVITY",
}
SALES_DIVISION_DISPLAY_EXCEPTION = {
    "transaction": "SIMG",
    "program": "SAPLSHI01",
    "control_id": "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell",
    "path": ("Structure de l'entreprise", "D\u00e9finition", "Logistique - donn\u00e9es g\u00e9n\u00e9rales"),
    "node_text": "D\u00e9finir, copier, supprimer, contr\u00f4ler secteur d'activit\u00e9",
    "operation": "OPEN_IMG_ACTIVITY",
}
COMPANY_CODE_TABLE_SEARCH = {
    "transaction": "V_T001",
    "program": "SAPL0ORG",
    "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001",
    "column": "BUKRS",
    "value": "1010",
}
COMPANY_CODE_TABLE_VARIANTS = (
    {
        "window_title": 'Modifier vue "Société" : synthèse',
        "table_id": COMPANY_CODE_TABLE_SEARCH["table_id"],
        "bukrs_cell_prefix": (
            f"{COMPANY_CODE_TABLE_SEARCH['table_id']}/ctxtV_T001-BUKRS[0,"
        ),
        "cell_type": "GuiCTextField",
    },
    {
        "window_title": 'Afficher vue "Société" : synthèse',
        "table_id": COMPANY_CODE_TABLE_SEARCH["table_id"],
        "bukrs_cell_prefix": (
            f"{COMPANY_CODE_TABLE_SEARCH['table_id']}/ctxtV_T001-BUKRS[0,"
        ),
        "cell_type": "GuiCTextField",
    },
)
SALES_ORGANIZATION_TABLE_SEARCH = {
    "transaction": "V_TVKO",
    "program": "SAPL0ORG",
    "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_TVKO",
    "column": "VKORG",
    "value": "1010",
}
PHASE5_ASSIGNMENT_TABLE_SEARCHES = {
    "SALES_ORG_1010_TO_COMPANY_CODE_1010": {
        "transaction": "SIMG",
        "program": "SAPLCUST_ASSIGN_SD",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLCUST_ASSIGN_SDTCTRL_V_TVKO_ASSIGN",
        "target": {"sales_organization": "1010", "company_code": "1010"},
        "fields": {
            "sales_organization": {
                "control": "ctxtV_TVKO_ASSIGN-VKORG",
                "column": "0",
                "value": "1010",
            },
            "company_code": {
                "control": "ctxtV_TVKO_ASSIGN-BUKRS",
                "column": "2",
                "value": "1010",
            },
        },
    },
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010": {
        "transaction": "SIMG",
        "program": "SAPLCUST_ASSIGN_SD",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLCUST_ASSIGN_SDTCTRL_V_TVKOV_ASSIGN",
        "target": {"distribution_channel": "10", "sales_organization": "1010"},
        "fields": {
            "sales_organization": {
                "control": "ctxtV_TVKOV_ASSIGN-VKORG",
                "column": "0",
                "value": "1010",
            },
            "distribution_channel": {
                "control": "ctxtV_TVKOV_ASSIGN-VTWEG",
                "column": "2",
                "value": "10",
            },
        },
    },
    "DIVISION_00_TO_SALES_ORG_1010": {
        "transaction": "SIMG",
        "program": "SAPLCUST_ASSIGN_SD",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLCUST_ASSIGN_SDTCTRL_V_TVKOS_ASSIGN",
        "target": {"sales_division": "00", "sales_organization": "1010"},
        "fields": {
            "sales_organization": {
                "control": "ctxtV_TVKOS_ASSIGN-VKORG",
                "column": "0",
                "value": "1010",
            },
            "sales_division": {
                "control": "ctxtV_TVKOS_ASSIGN-SPART",
                "column": "2",
                "value": "00",
            },
        },
    },
}
COMPANY_CODE_POSITION_BUTTON = {
    "id": "/app/con[0]/ses[0]/wnd[0]/usr/btnVIM_POSI_PUSH",
    "text": "Positionner.....",
}
SALES_ORGANIZATION_ACTIVITY = {
    "window_id": "/app/con[0]/ses[0]/wnd[1]",
    "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
    "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
    "row_text": "D\u00e9finir l'organisation commerciale",
    "forbidden_row_text": "Contr\u00f4ler, supprimer, copier l'organisation commerciale",
    "button_text": "S\u00e9lectionner",
}
DISTRIBUTION_CHANNEL_ACTIVITY = {
    "window_id": "/app/con[0]/ses[0]/wnd[1]",
    "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
    "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
    "row_text": "D\u00e9finir le canal de distribution",
    "forbidden_row_text": "Contr\u00f4ler, supprimer, copier le canal de distribution",
    "button_text": "S\u00e9lectionner",
}
SALES_DIVISION_ACTIVITY = {
    "window_id": "/app/con[0]/ses[0]/wnd[1]",
    "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
    "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
    "row_text": "D\u00e9finir le secteur d'activit\u00e9",
    "forbidden_row_text": "Contr\u00f4ler, supprimer, copier le secteur d'activit\u00e9",
    "button_text": "S\u00e9lectionner",
}


def open_transaction(session: SapGuiSession, transaction: str) -> None:
    code = transaction.strip().upper()
    if not code or len(code) > 20 or not code.replace("_", "").replace("/", "").isalnum():
        raise ActionBlockedError(f"Invalid transaction code: {transaction!r}")
    session.audit("OPEN_TRANSACTION", value=code)
    session.raw.StartTransaction(Transaction=code)
    session.validate_identity()


def back(session: SapGuiSession) -> None:
    session.audit("BACK", control_id="wnd[0]", value="sendVKey(3)")
    session.find("wnd[0]").sendVKey(3)
    session.validate_identity()


def close_img_info_popup(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
) -> dict[str, Any]:
    """Close only the observed read-only SAPLDSYH IMG information window."""

    expected = {
        "source": "OPEN_IMG_ACTIVITY",
        "window_id": "/app/con[0]/ses[0]/wnd[1]",
        "expected_transaction": "SIMG",
        "expected_program": "SAPLDSYH",
    }
    if params != expected:
        raise ActionBlockedError("CLOSE_IMG_INFO_POPUP context mismatch")

    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    matching = [popup for popup in popups if popup.get("id") == expected["window_id"]]
    editable_fields = [
        field
        for popup in matching
        for field in popup.get("input_fields") or []
        if field.get("changeable") is True or field.get("editable") is True
    ]
    if (
        str(before.get("transaction") or "").upper() != expected["expected_transaction"]
        or str(before.get("program") or "").upper() != expected["expected_program"]
        or len(popups) != 1
        or len(matching) != 1
        or editable_fields
    ):
        raise ActionBlockedError(
            "CLOSE_IMG_INFO_POPUP requires the single observed SAPLDSYH wnd[1] "
            "without editable/changeable input fields"
        )

    try:
        popup = session.find(expected["window_id"])
    except Exception as exc:
        raise ActionBlockedError("CLOSE_IMG_INFO_POPUP window not found") from exc
    if _control_value(popup, "Id") != expected["window_id"]:
        raise ActionBlockedError("CLOSE_IMG_INFO_POPUP window ID mismatch")

    session.audit(
        "CLOSE_IMG_INFO_POPUP",
        control_id=expected["window_id"],
        value={"source": expected["source"], "method": "sendVKey(3)"},
    )
    popup.sendVKey(3)
    session.validate_identity()
    after = _wait_for_screen(session, timeout_seconds, poll_seconds)
    remaining = {popup.get("id") for popup in after.get("popups") or []}
    if expected["window_id"] in remaining or remaining:
        raise ActionBlockedError("CLOSE_IMG_INFO_POPUP did not remove the secondary window")
    if (
        str(after.get("program") or "").upper() != "SAPLSHI01"
        or _normalized_text(after.get("window_title"))
        != "afficher guide d'implementation"
    ):
        raise ActionBlockedError(
            "CLOSE_IMG_INFO_POPUP did not return to SAPLSHI01 / Afficher guide d'implémentation"
        )
    after["closed_destination_classification"] = "READ_ONLY_DOCUMENTATION_OR_INFO"
    return after


def select_company_code_display_activity(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
) -> dict[str, Any]:
    """Choose the exact display activity in the observed SAPLDSYH selector."""

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
        raise ActionBlockedError("SELECT_COMPANY_CODE_ACTIVITY context mismatch")

    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    matching = [popup for popup in popups if popup.get("id") == expected["window_id"]]
    if (
        str(before.get("transaction") or "").upper() != expected["expected_transaction"]
        or str(before.get("program") or "").upper() != expected["expected_program"]
        or len(popups) != 1
        or len(matching) != 1
        or not _observed_exact_text(
            matching[0].get("window_title"),
            "Sélection de l'activité",
            allow_trailing_colon=True,
        )
    ):
        raise ActionBlockedError(
            "SELECT_COMPANY_CODE_ACTIVITY requires the exact observed SAPLDSYH activity-selection dialog"
        )

    popup_snapshot = matching[0]
    observed_texts = [
        str(record.get("text"))
        for record in popup_snapshot.get("controls") or []
        if record.get("text")
    ]
    for table in popup_snapshot.get("tables") or []:
        for row in table.get("visible_rows") or []:
            observed_texts.extend(
                str(value.get("text"))
                for value in row.get("values") or []
                if value.get("text")
            )
    required_rows = {
        "Copier, supprimer, contrôler société",
        expected["row_text"],
    }
    if not all(
        any(_observed_exact_text(value, expected) for value in observed_texts)
        for expected in required_rows
    ):
        raise ActionBlockedError(
            "SELECT_COMPANY_CODE_ACTIVITY observed an unknown business context"
        )

    buttons = [
        record
        for record in popup_snapshot.get("buttons") or []
        if record.get("type") == "GuiButton"
        and _observed_exact_text(record.get("text"), expected["button_text"])
    ]
    direct_rows = [
        {
            "kind": "DIRECT_CONTROL",
            "control_id": record.get("id"),
            "control_type": record.get("type"),
        }
        for record in popup_snapshot.get("controls") or []
        if _observed_exact_text(record.get("text"), expected["row_text"])
        and record.get("type") == "GuiRadioButton"
    ]
    table_rows = []
    for table in popup_snapshot.get("tables") or []:
        for row in table.get("visible_rows") or []:
            exact_values = [
                value
                for value in row.get("values") or []
                if _observed_exact_text(value.get("text"), expected["row_text"])
            ]
            if exact_values:
                table_rows.append(
                    {
                        "kind": "TABLE_ROW",
                        "control_id": table.get("id"),
                        "control_type": table.get("type"),
                        "row_index": row.get("index"),
                        "capabilities": table.get("native_capabilities") or [],
                    }
                )
    row_candidates = direct_rows + table_rows
    diagnostics = {
        "window_id": expected["window_id"],
        "controls": [
            {
                "id": record.get("id"),
                "type": record.get("type"),
                "text": record.get("text"),
            }
            for record in popup_snapshot.get("controls") or []
        ],
        "table_capabilities": [
            {
                "id": table.get("id"),
                "type": table.get("type"),
                "capabilities": table.get("native_capabilities") or [],
            }
            for table in popup_snapshot.get("tables") or []
        ],
    }
    if len(row_candidates) != 1 or len(buttons) != 1:
        raise ActionBlockedError(
            "SELECT_COMPANY_CODE_ACTIVITY row/button is not deterministic: "
            + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
        )

    chosen = row_candidates[0]
    try:
        selector = session.find(chosen["control_id"])
        button = session.find(buttons[0]["id"])
    except Exception as exc:
        raise ActionBlockedError(
            "SELECT_COMPANY_CODE_ACTIVITY observed control is no longer available"
        ) from exc
    if (
        _control_value(button, "Type") != "GuiButton"
        or not _observed_exact_text(
            _control_value(button, "Text"), expected["button_text"]
        )
        or not callable(getattr(button, "press", None))
    ):
        raise ActionBlockedError("SELECT_COMPANY_CODE_ACTIVITY button mismatch")

    session.audit(
        "SELECT_COMPANY_CODE_ACTIVITY",
        control_id=chosen["control_id"],
        control_text="approved company-code display activity selection",
        value={
            "row_text": expected["row_text"],
            "selection_kind": chosen["kind"],
            "button_id": buttons[0]["id"],
        },
    )
    if chosen["kind"] == "DIRECT_CONTROL":
        select_method = getattr(selector, "Select", None)
        if not callable(select_method):
            raise ActionBlockedError(
                "SELECT_COMPANY_CODE_ACTIVITY exact radio row has no observed Select capability"
            )
        select_method()
        selection_method = "Select"
    else:
        select_row = getattr(selector, "SelectRow", None)
        get_absolute_row = getattr(selector, "GetAbsoluteRow", None)
        if callable(select_row):
            select_row(chosen["row_index"])
            selection_method = "SelectRow"
        elif callable(get_absolute_row):
            row = get_absolute_row(chosen["row_index"])
            if not hasattr(row, "Selected"):
                raise ActionBlockedError(
                    "SELECT_COMPANY_CODE_ACTIVITY row has no observed Selected capability"
                )
            row.Selected = True
            selection_method = "GetAbsoluteRow.Selected"
        else:
            raise ActionBlockedError(
                "SELECT_COMPANY_CODE_ACTIVITY table exposes no allowlisted row-selection capability: "
                + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
            )

    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, timeout_seconds, poll_seconds)
    remaining = {popup.get("id") for popup in after.get("popups") or []}
    still_img_guide = (
        str(after.get("transaction") or "").upper() == "SIMG"
        and str(after.get("program") or "").upper() == "SAPLSHI01"
        and _normalized_text(after.get("window_title"))
        == "afficher guide d'implementation"
    )
    if expected["window_id"] in remaining or remaining or still_img_guide:
        raise ActionBlockedError(
            "SELECT_COMPANY_CODE_ACTIVITY did not reach a new screen outside the IMG guide"
        )
    after["activity_selection"] = {
        "classification": "IMG_ACTIVITY_SELECTION_DIALOG",
        "selected_row": expected["row_text"],
        "selection_method": selection_method,
        "button_id": buttons[0]["id"],
        "button_text": expected["button_text"],
    }
    return after


def _legacy_select_sales_organization_activity(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
) -> dict[str, Any]:
    """Select one observed, non-copy Sales Organization display activity."""

    required_keys = {
        "source",
        "target",
        "window_id",
        "expected_transaction",
        "expected_program",
        "row_text",
        "button_text",
    }
    if set(params) != required_keys or any(
        params.get(key) != value
        for key, value in {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": "/app/con[0]/ses[0]/wnd[1]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "button_text": "Sélectionner",
        }.items()
    ):
        raise ActionBlockedError("SELECT_SALES_ORGANIZATION_ACTIVITY context mismatch")
    row_text = params.get("row_text")
    normalized_row = _normalized_text(row_text)
    if (
        not isinstance(row_text, str)
        or not normalized_row.startswith("traiter")
        or not (
            "organisation commerciale" in normalized_row
            or "org. commerciale" in normalized_row
        )
        or any(term in normalized_row for term in ("copier", "supprimer", "contr"))
    ):
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY row is not an allowlisted processing activity"
        )

    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    matching = [popup for popup in popups if popup.get("id") == params["window_id"]]
    if (
        str(before.get("transaction") or "").upper() != params["expected_transaction"]
        or str(before.get("program") or "").upper() != params["expected_program"]
        or len(popups) != 1
        or len(matching) != 1
        or not _observed_exact_text(
            matching[0].get("window_title"),
            "Sélection de l'activité",
            allow_trailing_colon=True,
        )
    ):
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY requires the exact SAPLDSYH activity-selection dialog"
        )

    popup_snapshot = matching[0]
    buttons = [
        record
        for record in popup_snapshot.get("buttons") or []
        if record.get("type") == "GuiButton"
        and _observed_exact_text(record.get("text"), params["button_text"])
    ]
    direct_rows = [
        {
            "kind": "DIRECT_CONTROL",
            "control_id": record.get("id"),
            "row_index": None,
        }
        for record in popup_snapshot.get("controls") or []
        if record.get("type") == "GuiRadioButton"
        and _observed_exact_text(record.get("text"), row_text)
    ]
    table_rows = []
    for table_snapshot in popup_snapshot.get("tables") or []:
        for row in table_snapshot.get("visible_rows") or []:
            if any(
                _observed_exact_text(value.get("text"), row_text)
                for value in row.get("values") or []
            ):
                table_rows.append(
                    {
                        "kind": "TABLE_ROW",
                        "control_id": table_snapshot.get("id"),
                        "row_index": row.get("index"),
                    }
                )
    row_candidates = direct_rows + table_rows
    observed_options = sorted(
        {
            str(value)
            for value in _all_popup_text_values(popup_snapshot)
            if value
        }
    )
    diagnostics = {
        "options": observed_options,
        "row_candidates": row_candidates,
        "button_ids": [button.get("id") for button in buttons],
        "controls": [
            {
                "id": record.get("id"),
                "type": record.get("type"),
                "text": record.get("text"),
            }
            for record in popup_snapshot.get("controls") or []
        ],
        "table_capabilities": [
            {
                "id": table.get("id"),
                "type": table.get("type"),
                "capabilities": table.get("native_capabilities") or [],
            }
            for table in popup_snapshot.get("tables") or []
        ],
    }
    if len(row_candidates) != 1 or len(buttons) != 1:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY row/button is not deterministic: "
            + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
        )

    chosen = row_candidates[0]
    try:
        selector = session.find(chosen["control_id"])
        button = session.find(buttons[0]["id"])
    except Exception as exc:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY observed control is unavailable"
        ) from exc
    if (
        _control_value(button, "Type") != "GuiButton"
        or not _observed_exact_text(
            _control_value(button, "Text"), params["button_text"]
        )
        or not callable(getattr(button, "press", None))
    ):
        raise ActionBlockedError("SELECT_SALES_ORGANIZATION_ACTIVITY button mismatch")

    session.audit(
        "SELECT_SALES_ORGANIZATION_ACTIVITY",
        control_id=chosen["control_id"],
        control_text="approved sales-organization display activity selection",
        value={
            "row_text": row_text,
            "selection_kind": chosen["kind"],
            "button_id": buttons[0]["id"],
        },
    )
    if chosen["kind"] == "DIRECT_CONTROL":
        select_method = getattr(selector, "Select", None)
        if not callable(select_method):
            raise ActionBlockedError(
                "SELECT_SALES_ORGANIZATION_ACTIVITY radio row has no Select capability"
            )
        select_method()
        selection_method = "Select"
    else:
        select_row = getattr(selector, "SelectRow", None)
        get_absolute_row = getattr(selector, "GetAbsoluteRow", None)
        if callable(select_row):
            select_row(chosen["row_index"])
            selection_method = "SelectRow"
        elif callable(get_absolute_row):
            row = get_absolute_row(chosen["row_index"])
            if not hasattr(row, "Selected"):
                raise ActionBlockedError(
                    "SELECT_SALES_ORGANIZATION_ACTIVITY row has no Selected capability"
                )
            row.Selected = True
            selection_method = "GetAbsoluteRow.Selected"
        else:
            raise ActionBlockedError(
                "SELECT_SALES_ORGANIZATION_ACTIVITY table has no allowlisted selection capability: "
                + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
            )

    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, timeout_seconds, poll_seconds)
    remaining = {popup.get("id") for popup in after.get("popups") or []}
    still_img_guide = (
        str(after.get("transaction") or "").upper() == "SIMG"
        and str(after.get("program") or "").upper() == "SAPLSHI01"
        and _normalized_text(after.get("window_title"))
        == "afficher guide d'implementation"
    )
    if params["window_id"] in remaining or remaining or still_img_guide:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY did not reach a new screen outside the IMG guide"
        )
    after["activity_selection"] = {
        "classification": "IMG_ACTIVITY_SELECTION_DIALOG",
        "target": "sales_organization",
        "selected_row": row_text,
        "selection_method": selection_method,
        "button_id": buttons[0]["id"],
        "button_text": params["button_text"],
    }
    return after


def select_sales_organization_activity(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
) -> dict[str, Any]:
    """Select only the exact live Sales Organization row in its exact table."""

    expected = {
        "source": "OPEN_IMG_ACTIVITY",
        "target": "sales_organization",
        "window_id": SALES_ORGANIZATION_ACTIVITY["window_id"],
        "expected_transaction": "SIMG",
        "expected_program": "SAPLDSYH",
        "table_id": SALES_ORGANIZATION_ACTIVITY["table_id"],
        "row_text": SALES_ORGANIZATION_ACTIVITY["row_text"],
        "button_id": SALES_ORGANIZATION_ACTIVITY["button_id"],
        "button_text": SALES_ORGANIZATION_ACTIVITY["button_text"],
    }
    if params != expected:
        raise ActionBlockedError("SELECT_SALES_ORGANIZATION_ACTIVITY context mismatch")

    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    matching = [popup for popup in popups if popup.get("id") == expected["window_id"]]
    if (
        str(before.get("transaction") or "").upper() != expected["expected_transaction"]
        or str(before.get("program") or "").upper() != expected["expected_program"]
        or len(popups) != 1
        or len(matching) != 1
        or not _observed_exact_text(
            matching[0].get("window_title"),
            "S\u00e9lection de l'activit\u00e9",
            allow_trailing_colon=True,
        )
    ):
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY requires the exact SAPLDSYH activity-selection dialog"
        )

    popup = matching[0]
    tables = [
        table for table in popup.get("tables") or []
        if table.get("id") == expected["table_id"]
        and table.get("type") == "GuiTableControl"
    ]
    buttons = [
        button for button in popup.get("buttons") or []
        if button.get("id") == expected["button_id"]
        and button.get("type") == "GuiButton"
        and _observed_exact_text(button.get("text"), expected["button_text"])
    ]
    observed_options: list[str] = []
    target_rows: list[int] = []
    if len(tables) == 1:
        for row in tables[0].get("visible_rows") or []:
            texts = [
                str(value.get("text")) for value in row.get("values") or []
                if value.get("text")
            ]
            observed_options.extend(texts)
            if any(_observed_exact_text(text, expected["row_text"]) for text in texts):
                target_rows.append(int(row["index"]))
    forbidden_count = sum(
        _observed_exact_text(text, SALES_ORGANIZATION_ACTIVITY["forbidden_row_text"])
        for text in observed_options
    )
    diagnostics = {
        "table_id": expected["table_id"],
        "options": observed_options,
        "target_rows": target_rows,
        "button_ids": [button.get("id") for button in buttons],
    }
    if len(tables) != 1 or len(target_rows) != 1 or len(buttons) != 1 or forbidden_count != 1:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY row/button is not deterministic: "
            + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
        )

    try:
        table = session.find(expected["table_id"])
        button = session.find(expected["button_id"])
    except Exception as exc:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY observed control is unavailable"
        ) from exc
    if (
        _control_value(button, "Type") != "GuiButton"
        or not _observed_exact_text(_control_value(button, "Text"), expected["button_text"])
        or not callable(getattr(button, "press", None))
    ):
        raise ActionBlockedError("SELECT_SALES_ORGANIZATION_ACTIVITY button mismatch")

    session.audit(
        "SELECT_SALES_ORGANIZATION_ACTIVITY",
        control_id=expected["table_id"],
        control_text="approved sales-organization display activity selection",
        value={"row_text": expected["row_text"], "button_id": expected["button_id"]},
    )
    select_row = getattr(table, "SelectRow", None)
    get_absolute_row = getattr(table, "GetAbsoluteRow", None)
    if callable(select_row):
        select_row(target_rows[0])
        selection_method = "SelectRow"
    elif callable(get_absolute_row):
        row = get_absolute_row(target_rows[0])
        if not hasattr(row, "Selected"):
            raise ActionBlockedError(
                "SELECT_SALES_ORGANIZATION_ACTIVITY row has no Selected capability"
            )
        row.Selected = True
        selection_method = "GetAbsoluteRow.Selected"
    else:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY table has no allowlisted selection capability: "
            + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True)
        )

    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, timeout_seconds, poll_seconds)
    remaining = {popup.get("id") for popup in after.get("popups") or []}
    still_img_guide = (
        str(after.get("transaction") or "").upper() == "SIMG"
        and str(after.get("program") or "").upper() == "SAPLSHI01"
        and _normalized_text(after.get("window_title")) == "afficher guide d'implementation"
    )
    if expected["window_id"] in remaining or remaining or still_img_guide:
        raise ActionBlockedError(
            "SELECT_SALES_ORGANIZATION_ACTIVITY did not reach a new screen outside the IMG guide"
        )
    after["activity_selection"] = {
        "classification": "IMG_ACTIVITY_SELECTION_DIALOG",
        "target": "sales_organization",
        "selected_row": expected["row_text"],
        "selection_method": selection_method,
        "button_id": expected["button_id"],
        "button_text": expected["button_text"],
    }
    return after


def select_distribution_channel_activity(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
    activity: dict[str, str] = DISTRIBUTION_CHANNEL_ACTIVITY,
    target: str = "distribution_channel",
) -> dict[str, Any]:
    """Select only the exact live distribution-channel definition row."""

    expected = {
        "source": "OPEN_IMG_ACTIVITY",
        "target": target,
        "window_id": activity["window_id"],
        "expected_transaction": "SIMG",
        "expected_program": "SAPLDSYH",
        "table_id": activity["table_id"],
        "row_text": activity["row_text"],
        "button_id": activity["button_id"],
        "button_text": activity["button_text"],
    }
    if params != expected:
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY context mismatch")

    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    matching = [popup for popup in popups if popup.get("id") == expected["window_id"]]
    if (
        str(before.get("transaction") or "").upper() != expected["expected_transaction"]
        or str(before.get("program") or "").upper() != expected["expected_program"]
        or len(popups) != 1
        or len(matching) != 1
        or not _observed_exact_text(matching[0].get("window_title"), "S\u00e9lection de l'activit\u00e9", allow_trailing_colon=True)
    ):
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY requires the exact SAPLDSYH selector")

    popup = matching[0]
    tables = [table for table in popup.get("tables") or [] if table.get("id") == expected["table_id"] and table.get("type") == "GuiTableControl"]
    buttons = [button for button in popup.get("buttons") or [] if button.get("id") == expected["button_id"] and button.get("type") == "GuiButton" and _observed_exact_text(button.get("text"), expected["button_text"])]
    options: list[str] = []
    target_rows: list[int] = []
    if len(tables) == 1:
        for row in tables[0].get("visible_rows") or []:
            texts = [str(value.get("text")) for value in row.get("values") or [] if value.get("text")]
            options.extend(texts)
            if any(_observed_exact_text(text, expected["row_text"]) for text in texts):
                target_rows.append(int(row["index"]))
    forbidden_count = sum(_observed_exact_text(text, activity["forbidden_row_text"]) for text in options)
    diagnostics = {"table_id": expected["table_id"], "options": options, "target_rows": target_rows, "button_ids": [button.get("id") for button in buttons]}
    if len(tables) != 1 or len(target_rows) != 1 or len(buttons) != 1 or forbidden_count != 1:
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY row/button is not deterministic: " + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True))

    table = session.find(expected["table_id"])
    button = session.find(expected["button_id"])
    if _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Text"), expected["button_text"]) or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY button mismatch")
    session.audit("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY", control_id=expected["table_id"], control_text="approved distribution-channel definition activity", value={"row_text": expected["row_text"], "button_id": expected["button_id"]})
    select_row = getattr(table, "SelectRow", None)
    get_absolute_row = getattr(table, "GetAbsoluteRow", None)
    if callable(select_row):
        select_row(target_rows[0])
        selection_method = "SelectRow"
    elif callable(get_absolute_row):
        row = get_absolute_row(target_rows[0])
        if not hasattr(row, "Selected"):
            raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY row has no Selected capability")
        row.Selected = True
        selection_method = "GetAbsoluteRow.Selected"
    else:
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY table has no allowlisted selection capability")
    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, timeout_seconds, poll_seconds)
    remaining = {popup.get("id") for popup in after.get("popups") or []}
    if expected["window_id"] in remaining or remaining:
        raise ActionBlockedError("SELECT_DISTRIBUTION_CHANNEL_ACTIVITY did not leave the selector")
    after["activity_selection"] = {"classification": "IMG_ACTIVITY_SELECTION_DIALOG", "target": target, "selected_row": expected["row_text"], "selection_method": selection_method, "button_id": expected["button_id"], "button_text": expected["button_text"]}
    return after


def select_sales_division_activity(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    return select_distribution_channel_activity(session, params, activity=SALES_DIVISION_ACTIVITY, target="sales_division")


def select_s4650_billing_copy_activity(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    """Open only the observed delivery-to-billing copy-control activity."""
    expected = {"source": "OPEN_IMG_ACTIVITY", "window_id": "/app/con[0]/ses[0]/wnd[1]", "transaction": "SIMG", "program": "SAPLDSYH", "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES", "row_text": "D\u00e9finir pilotage copie pour document de livraison vers document facturation", "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]", "button_text": "S\u00e9lectionner"}
    if params != expected:
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    if str(before.get("transaction") or "").upper() != "SIMG" or str(before.get("program") or "").upper() != "SAPLDSYH" or len(popups) != 1 or popups[0].get("id") != expected["window_id"] or not _observed_exact_text(popups[0].get("window_title"), "S\u00e9lection de l'activit\u00e9", allow_trailing_colon=True):
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY requires exact IMG activity popup")
    popup = popups[0]
    tables = [t for t in popup.get("tables") or [] if t.get("id") == expected["table_id"] and t.get("type") == "GuiTableControl"]
    buttons = [b for b in popup.get("buttons") or [] if b.get("id") == expected["button_id"] and b.get("type") == "GuiButton" and _observed_exact_text(b.get("text"), expected["button_text"])]
    matches = []
    if len(tables) == 1:
        for row in tables[0].get("visible_rows") or []:
            if any(_observed_exact_text(v.get("text"), expected["row_text"]) for v in row.get("values") or []):
                matches.append(int(row["index"]))
    if len(tables) != 1 or len(buttons) != 1 or len(matches) != 1:
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY row/button is ambiguous")
    table = session.find(expected["table_id"])
    button = session.find(expected["button_id"])
    if _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Text"), expected["button_text"]) or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY button mismatch")
    session.audit("SELECT_S4650_BILLING_COPY_ACTIVITY", control_id=expected["table_id"], control_text=expected["row_text"], value={"row": matches[0]})
    select_row = getattr(table, "SelectRow", None)
    get_row = getattr(table, "GetAbsoluteRow", None)
    if callable(select_row):
        select_row(matches[0])
    elif callable(get_row) and hasattr(get_row(matches[0]), "Selected"):
        get_row(matches[0]).Selected = True
    else:
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY has no observed row selection capability")
    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, 10.0, 0.1)
    if after.get("popups"):
        raise ActionBlockedError("SELECT_S4650_BILLING_COPY_ACTIVITY destination has an unexpected popup")
    after["activity_selection"] = {"target": "delivery_to_billing", "selected_row": expected["row_text"]}
    return after


def select_s4615_billing_type_activity(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    """Open only the live-observed S4615 billing-type definition activity."""
    expected = {"source": "OPEN_IMG_ACTIVITY", "window_id": "/app/con[0]/ses[0]/wnd[1]", "transaction": "SIMG", "program": "SAPLDSYH", "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES", "row_text": "Définir types de documents de facturation pour les ventes", "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]", "button_text": "Sélectionner"}
    if params != expected:
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    popups = before.get("popups") or []
    if (str(before.get("transaction") or "").upper() != "SIMG" or str(before.get("program") or "").upper() != "SAPLDSYH" or len(popups) != 1 or popups[0].get("id") != expected["window_id"] or not _observed_exact_text(popups[0].get("window_title"), "Sélection de l'activité", allow_trailing_colon=True)):
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY requires exact IMG activity popup")
    popup = popups[0]
    tables = [t for t in popup.get("tables") or [] if t.get("id") == expected["table_id"] and t.get("type") == "GuiTableControl"]
    buttons = [b for b in popup.get("buttons") or [] if b.get("id") == expected["button_id"] and b.get("type") == "GuiButton" and _observed_exact_text(b.get("text"), expected["button_text"])]
    matches = []
    if len(tables) == 1:
        for row in tables[0].get("visible_rows") or []:
            if any(_observed_exact_text(v.get("text"), expected["row_text"]) for v in row.get("values") or []):
                matches.append(int(row["index"]))
    if len(tables) != 1 or len(buttons) != 1 or len(matches) != 1:
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY row/button is ambiguous")
    table = session.find(expected["table_id"])
    button = session.find(expected["button_id"])
    if _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Text"), expected["button_text"]) or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY button mismatch")
    select_row = getattr(table, "SelectRow", None)
    get_row = getattr(table, "GetAbsoluteRow", None)
    if not callable(select_row) and not callable(get_row):
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY has no observed row selection capability")
    session.audit("SELECT_S4615_BILLING_TYPE_ACTIVITY", control_id=expected["table_id"], control_text=expected["row_text"], value={"row": matches[0]})
    if callable(select_row):
        select_row(matches[0])
    elif hasattr(get_row(matches[0]), "Selected"):
        get_row(matches[0]).Selected = True
    else:
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY row is not selectable")
    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, 10.0, 0.1)
    if after.get("popups"):
        raise ActionBlockedError("SELECT_S4615_BILLING_TYPE_ACTIVITY destination has an unexpected popup")
    after["activity_selection"] = {"target": "billing_type", "selected_row": expected["row_text"]}
    return after


def _collection_controls(collection: Any) -> list[Any]:
    try:
        return [collection(index) for index in range(int(collection.Count))]
    except Exception:
        try:
            return list(collection)
        except Exception:
            return []


def _company_code_cells(table: Any, position: int, row_count: int) -> tuple[dict[int, str], str | None]:
    cells_by_row: dict[int, list[Any]] = {}
    for cell in _collection_controls(getattr(table, "Children", None)):
        control_id = _control_value(cell, "Id")
        if "BUKRS[" not in control_id.upper():
            continue
        match = re.search(r"\[\d+,(\d+)\]$", control_id)
        if match is not None:
            cells_by_row.setdefault(int(match.group(1)), []).append(cell)
    if not cells_by_row:
        return {}, "BUKRS cells are not observable on a visible table page"
    values: dict[int, str] = {}
    for relative_row, cells in cells_by_row.items():
        absolute_row = position + relative_row
        if absolute_row >= row_count:
            continue
        if len(cells) != 1:
            return values, f"BUKRS cell is ambiguous at absolute row {absolute_row}"
        values[absolute_row] = _control_value(cells[0], "Text")
    return values, None


def _wait_while_busy(session: SapGuiSession, timeout_seconds: float, poll_seconds: float) -> None:
    deadline = time.monotonic() + timeout_seconds
    while bool(getattr(session.raw, "Busy", False)):
        if time.monotonic() >= deadline:
            raise TimeoutError("SAP GUI operation did not finish")
        time.sleep(poll_seconds)


def _position_company_code_1010(
    session: SapGuiSession,
    expected: dict[str, str],
    *,
    timeout_seconds: float,
    poll_seconds: float,
) -> tuple[str, int | None, str]:
    """Use only the exact V_T001 positioning dialog as a read-only fallback."""
    try:
        button = session.find(COMPANY_CODE_POSITION_BUTTON["id"])
    except Exception:
        return "UNKNOWN", None, "exact V_T001 positioning button is unavailable"
    if (
        _control_value(button, "Type") != "GuiButton"
        or not _observed_exact_text(
            _control_value(button, "Text"), COMPANY_CODE_POSITION_BUTTON["text"]
        )
        or not callable(getattr(button, "press", None))
    ):
        return "UNKNOWN", None, "exact V_T001 positioning button does not match live control"

    session.audit(
        "POSITION_COMPANY_CODE_VALUE",
        control_id=COMPANY_CODE_POSITION_BUTTON["id"],
        control_text="approved read-only V_T001 positioning search",
        value={"column": expected["column"], "search_value": expected["value"]},
    )
    button.press()
    _wait_while_busy(session, timeout_seconds, poll_seconds)
    positioned = inspect_screen(session)
    popups = positioned.get("popups") or []
    if len(popups) != 1 or popups[0].get("id") != "/app/con[0]/ses[0]/wnd[1]":
        return "UNKNOWN", None, "V_T001 positioning dialog was not uniquely observable"
    popup = popups[0]
    editable = [
        field for field in popup.get("input_fields") or []
        if field.get("type") in {"GuiTextField", "GuiCTextField"}
        and field.get("changeable") is True
    ]
    allowed_confirm_text = {"suite", "continuer", "positionner", "rechercher", "ok"}
    confirms = [
        candidate for candidate in popup.get("buttons") or []
        if candidate.get("type") == "GuiButton"
        and (
            _normalized_text(candidate.get("text")).strip(" .:") in allowed_confirm_text
            or _normalized_text(candidate.get("tooltip")).split("(", 1)[0].strip(" .:")
            in allowed_confirm_text
        )
    ]
    if len(editable) != 1 or len(confirms) != 1:
        return "UNKNOWN", None, "V_T001 positioning criterion/button is not deterministic"
    try:
        field = session.find(editable[0]["id"])
        confirm = session.find(confirms[0]["id"])
    except Exception:
        return "UNKNOWN", None, "V_T001 positioning controls could not be reacquired"
    if not bool(getattr(field, "Changeable", False)) or not hasattr(field, "Text"):
        return "UNKNOWN", None, "V_T001 positioning criterion is not editable"
    session.audit(
        "POSITION_COMPANY_CODE_VALUE",
        control_id=editable[0]["id"],
        control_text="read-only V_T001 positioning criterion",
        value={"column": expected["column"], "search_value": expected["value"]},
    )
    field.Text = expected["value"]
    if not callable(getattr(confirm, "press", None)):
        return "UNKNOWN", None, "V_T001 positioning confirmation has no press capability"
    confirm.press()
    _wait_while_busy(session, timeout_seconds, poll_seconds)
    after = inspect_screen(session)
    try:
        table = session.find(expected["table_id"])
        scrollbar = getattr(table, "VerticalScrollbar")
        position = int(getattr(scrollbar, "Position"))
        row_count = int(getattr(table, "RowCount"))
        values, error = _company_code_cells(table, position, row_count)
    except Exception as exc:
        return "UNKNOWN", None, f"positioned table could not be read ({type(exc).__name__})"
    for row, value in values.items():
        if value == expected["value"]:
            return "FOUND", row, "found through exact V_T001 positioning dialog"
    observed_message = " ".join(
        [str((after.get("status_bar") or {}).get("text") or "")]
        + [str(value) for popup in after.get("popups") or [] for value in _all_popup_text_values(popup)]
    )
    normalized_message = _normalized_text(observed_message)
    no_entry_markers = (
        "aucune entree",
        "aucune donnee",
        "no entries",
        "not found",
    )
    if any(marker in normalized_message for marker in no_entry_markers):
        return "CONFIRMED_NOT_FOUND", None, "SAP reported no matching V_T001 entry"
    return "UNKNOWN", None, error or "positioning completed but 1010 was not deterministically visible"


def find_company_code_table_value(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.05,
) -> dict[str, Any]:
    """Scan V_T001 read-only, reacquiring COM controls after every scroll."""
    expected = dict(COMPANY_CODE_TABLE_SEARCH)
    if params != expected:
        raise ActionBlockedError("FIND_TABLE_VALUE context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    window_title = str(before.get("window_title") or "")
    variant = next(
        (
            item
            for item in COMPANY_CODE_TABLE_VARIANTS
            if _normalized_text(window_title)
            == _normalized_text(item["window_title"])
        ),
        None,
    )
    tables = [table for table in before.get("tables") or [] if table.get("id") == expected["table_id"]]
    if (
        str(before.get("transaction") or "").upper() != expected["transaction"]
        or str(before.get("program") or "").upper() != expected["program"]
        or variant is None
        or len(tables) != 1
        or tables[0].get("type") != "GuiTableControl"
    ):
        raise ActionBlockedError(
            "FIND_TABLE_VALUE requires an exact evidenced V_T001/SAPL0ORG "
            "company-code table variant"
        )
    try:
        initial_table = session.find(expected["table_id"])
        row_count = int(getattr(initial_table, "RowCount"))
        visible_count = int(getattr(initial_table, "VisibleRowCount"))
    except Exception as exc:
        raise ActionBlockedError(
            "FIND_TABLE_VALUE table dimensions are not observable"
        ) from exc
    if row_count < 0 or row_count > 10000 or visible_count <= 0:
        raise ActionBlockedError("FIND_TABLE_VALUE table dimensions are unsafe")

    session.audit(
        "FIND_TABLE_VALUE",
        control_id=expected["table_id"],
        control_text="read-only company code table scan",
        value={"column": expected["column"], "value": expected["value"], "row_count": row_count},
    )
    observed_rows: dict[int, str] = {}
    visited_positions: set[int] = set()
    found_row: int | None = None
    reason: str | None = None
    try:
        table = session.find(expected["table_id"])
        scrollbar = getattr(table, "VerticalScrollbar")
        position = int(getattr(scrollbar, "Position"))
        if (
            int(getattr(table, "RowCount")) != row_count
            or int(getattr(table, "VisibleRowCount")) != visible_count
        ):
            reason = "V_T001 table dimensions changed before lookup"
        elif position != 0:
            scrollbar.Position = 0
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = getattr(table, "VerticalScrollbar")
            position = int(getattr(scrollbar, "Position"))
            if position != 0:
                reason = "V_T001 scrollbar did not return to row zero"
    except Exception as exc:
        reason = f"vertical scrollbar reset failed ({type(exc).__name__})"

    while reason is None and len(observed_rows) < row_count:
        try:
            table = session.find(expected["table_id"])
            if (
                _control_value(table, "Id") != expected["table_id"]
                or _control_value(table, "Type") != "GuiTableControl"
                or int(getattr(table, "RowCount")) != row_count
                or int(getattr(table, "VisibleRowCount")) != visible_count
            ):
                raise ValueError("V_T001 table identity or dimensions changed")
            scrollbar = getattr(table, "VerticalScrollbar")
            position = int(getattr(scrollbar, "Position"))
            maximum = int(getattr(scrollbar, "Maximum"))
        except Exception as exc:
            reason = f"table/scrollbar reacquisition failed ({type(exc).__name__})"
            break
        if position < 0 or position > maximum or position in visited_positions:
            reason = f"vertical scrollbar position is invalid or repeated: {position}"
            break
        visited_positions.add(position)
        end_row = min(position + visible_count, row_count)
        for absolute_row in range(position, end_row):
            relative_row = absolute_row - position
            control_id = f"{variant['bukrs_cell_prefix']}{relative_row}]"
            try:
                cell = session.find(control_id)
                if (
                    _control_value(cell, "Id") != control_id
                    or _control_value(cell, "Type") != variant["cell_type"]
                ):
                    raise ValueError("BUKRS cell control ID/type mismatch")
                value = str(_control_value(cell, "Text") or "").strip()
            except Exception as exc:
                reason = (
                    f"BUKRS cell is not deterministically readable at row "
                    f"{absolute_row} ({type(exc).__name__})"
                )
                break
            previous_value = observed_rows.get(absolute_row)
            if previous_value is not None and previous_value != value:
                reason = f"BUKRS value changed during lookup at row {absolute_row}"
                break
            observed_rows[absolute_row] = value
            if value == expected["value"]:
                found_row = absolute_row
                break
        if reason is not None or found_row is not None:
            break
        if len(observed_rows) == row_count or position >= maximum:
            break
        next_position = min(position + visible_count, maximum)
        if next_position <= position:
            reason = f"vertical scrollbar stalled at position {position}"
            break
        try:
            scrollbar.Position = next_position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = getattr(table, "VerticalScrollbar")
            actual_position = int(getattr(scrollbar, "Position"))
        except Exception as exc:
            reason = f"vertical scrollbar traversal failed ({type(exc).__name__})"
            break
        if (
            actual_position <= position
            or actual_position > position + visible_count
            or actual_position > maximum
        ):
            reason = (
                f"vertical scrollbar moved unpredictably from {position} "
                f"to {actual_position}"
            )
            break

    method = "SCROLL_SCAN"
    if found_row is not None:
        result = "FOUND"
    elif reason is None and len(observed_rows) == row_count and all(
        row in observed_rows for row in range(row_count)
    ):
        result = "CONFIRMED_NOT_FOUND"
    else:
        method = "POSITION_DIALOG"
        result, fallback_row, fallback_reason = _position_company_code_1010(
            session,
            expected,
            timeout_seconds=timeout_seconds,
            poll_seconds=poll_seconds,
        )
        if fallback_row is not None:
            found_row = fallback_row
        reason = fallback_reason if result != "FOUND" else None

    session.validate_identity()
    after = inspect_screen(session)
    after["table_value_search"] = {
        "result": result,
        "method": method,
        "transaction": expected["transaction"],
        "program": expected["program"],
        "table_id": expected["table_id"],
        "column": expected["column"],
        "value": expected["value"],
        "row_count": row_count,
        "rows_read": len(observed_rows),
        "found_row": found_row,
        "visited_scroll_positions": sorted(visited_positions),
        "reason": reason,
    }
    return after


def scan_s4650_distribution_channels(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.05,
) -> dict[str, Any]:
    """Read every V_TVTW key to determine the first free S4650 group code."""
    expected = {
        "transaction": "V_TVTW",
        "program": "SAPL0ORGCORE",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGCORETCTRL_V_TVTW",
    }
    if params != expected:
        raise ActionBlockedError("SCAN_S4650_DISTRIBUTION_CHANNELS context mismatch")
    session.validate_identity()
    identity = session.identity
    if str(identity.get("transaction") or "").upper() != expected["transaction"] or str(getattr(session.raw.Info, "Program", "") or "").upper() != expected["program"]:
        raise ActionBlockedError("SCAN_S4650_DISTRIBUTION_CHANNELS requires exact V_TVTW/SAPL0ORGCORE")
    try:
        table = session.find(expected["table_id"])
        row_count = int(table.RowCount)
        visible_count = int(table.VisibleRowCount)
        maximum = int(table.VerticalScrollbar.Maximum)
    except Exception as exc:
        raise ActionBlockedError("V_TVTW dimensions are not observable") from exc
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("V_TVTW dimensions are unsafe")
    session.audit("SCAN_S4650_DISTRIBUTION_CHANNELS", control_id=expected["table_id"], control_text="read-only full V_TVTW key scan", value={"row_count": row_count})
    observed: dict[int, str] = {}
    positions: list[int] = []
    position = 0
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            cell_id = f"{expected['table_id']}/ctxtV_TVTW-VTWEG[0,{relative_row}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Type") != "GuiCTextField":
                raise ActionBlockedError(f"V_TVTW key cell mismatch at row {absolute_row}")
            observed[absolute_row] = str(_control_value(cell, "Text") or "").strip()
        if len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    codes = sorted({value for value in observed.values() if value})
    candidates = [(f"{i:02d}", f"D{i % 10}") for i in range(1, 11)] + [(f"{i:02d}", f"E{i % 10}") for i in range(11, 21)]
    first_free = next(({"group": group, "distribution_channel": code} for group, code in candidates if code not in codes), None) if complete else None
    session.validate_identity()
    return {"distribution_channel_scan": {"result": "COMPLETE" if complete else "UNKNOWN", "row_count": row_count, "rows_read": len(observed), "visited_scroll_positions": positions, "existing_codes": codes, "first_free": first_free}}


def scan_s4650_sales_areas(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    """Read the exact live sales-area table for the two Exercise 1 keys."""
    expected = {"transaction": "SIMG", "program": "SAPLCUST_ASSIGN_SD", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLCUST_ASSIGN_SDTCTRL_V_TVTA_ASSIGN", "sales_organization": "1010", "distribution_channel": "D1", "divisions": ["00", "03"]}
    if params != expected:
        raise ActionBlockedError("SCAN_S4650_SALES_AREAS context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != expected["transaction"] or str(getattr(session.raw.Info, "Program", "") or "").upper() != expected["program"]:
        raise ActionBlockedError("SCAN_S4650_SALES_AREAS requires exact IMG sales-area view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("SCAN_S4650_SALES_AREAS table type mismatch")
    row_count = int(table.RowCount)
    visible_count = int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("SCAN_S4650_SALES_AREAS dimensions are unsafe")
    session.audit("SCAN_S4650_SALES_AREAS", control_id=expected["table_id"], control_text="read-only exact sales-area scan", value={"row_count": row_count, "target": "1010/D1/00,03"})
    observed: dict[int, tuple[str, str, str]] = {}
    positions: list[int] = []
    position = 0
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            values = []
            for column, field in ((0, "VKORG"), (2, "VTWEG"), (4, "SPART")):
                cell_id = f"{expected['table_id']}/ctxtV_TVTA_ASSIGN-{field}[{column},{relative_row}]"
                cell = session.find(cell_id)
                if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiCTextField":
                    raise ActionBlockedError(f"Sales-area {field} cell mismatch at row {absolute_row}")
                values.append(str(_control_value(cell, "Text") or "").strip())
            observed[absolute_row] = tuple(values)
        if len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    targets = {f"1010/D1/{division}": next((row for row, values in observed.items() if values == ("1010", "D1", division)), None) for division in expected["divisions"]}
    return {"sales_area_scan": {"result": "COMPLETE" if complete else "UNKNOWN", "row_count": row_count, "rows_read": len(observed), "visited_scroll_positions": positions, "sales_org_1010_observed": any(values[0] == "1010" for values in observed.values()), "target_rows": targets}}


def scan_s4650_sales_divisions(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    expected = {"transaction": "V_TSPA", "program": "SAPL0ORGCORE", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGCORETCTRL_V_TSPA", "values": ["00", "03"]}
    if params != expected:
        raise ActionBlockedError("SCAN_S4650_SALES_DIVISIONS context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != expected["transaction"] or str(getattr(session.raw.Info, "Program", "") or "").upper() != expected["program"]:
        raise ActionBlockedError("SCAN_S4650_SALES_DIVISIONS requires exact V_TSPA view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("SCAN_S4650_SALES_DIVISIONS table type mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("SCAN_S4650_SALES_DIVISIONS dimensions are unsafe")
    session.audit("SCAN_S4650_SALES_DIVISIONS", control_id=expected["table_id"], control_text="read-only V_TSPA key scan", value={"row_count": row_count, "values": expected["values"]})
    observed: dict[int, str] = {}
    positions: list[int] = []
    position = 0
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            cell_id = f"{expected['table_id']}/ctxtV_TSPA-SPART[0,{relative_row}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiCTextField":
                raise ActionBlockedError(f"V_TSPA SPART cell mismatch at row {absolute_row}")
            observed[absolute_row] = str(_control_value(cell, "Text") or "").strip()
        if len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    return {"sales_division_scan": {"result": "COMPLETE" if complete else "UNKNOWN", "row_count": row_count, "rows_read": len(observed), "visited_scroll_positions": positions, "target_rows": {value: next((row for row, observed_value in observed.items() if observed_value == value), None) for value in expected["values"]}}}


def find_s4615_billing_type(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    expected = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "ZF01"}
    if params != expected:
        raise ActionBlockedError("FIND_S4615_BILLING_TYPE context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != "VOFA" or str(getattr(session.raw.Info, "Program", "") or "").upper() != "SAPL081F":
        raise ActionBlockedError("FIND_S4615_BILLING_TYPE requires exact VOFA view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("FIND_S4615_BILLING_TYPE table type mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("FIND_S4615_BILLING_TYPE dimensions are unsafe")
    session.audit("FIND_S4615_BILLING_TYPE", control_id=expected["table_id"], control_text="read-only VOFA ZF01 lookup", value={"row_count": row_count})
    observed: dict[int, str] = {}
    positions: list[int] = []
    found_row = None
    reference_rows: list[dict[str, str]] = []
    position = 0
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            cell_id = f"{expected['table_id']}/txtV_TVFK-FKART[0,{relative_row}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiTextField":
                raise ActionBlockedError(f"VOFA billing type cell mismatch at row {absolute_row}")
            value = str(_control_value(cell, "Text") or "").strip()
            observed[absolute_row] = value
            if value.startswith("ZF"):
                description_id = f"{expected['table_id']}/txtV_TVFK-VTEXT[1,{relative_row}]"
                description_cell = session.find(description_id)
                if _control_value(description_cell, "Id") != description_id or _control_value(description_cell, "Type") != "GuiTextField":
                    raise ActionBlockedError(f"VOFA billing description cell mismatch at row {absolute_row}")
                reference_rows.append({"billing_type": value, "description": str(_control_value(description_cell, "Text") or "").strip()})
            if value == "ZF01":
                found_row = absolute_row
        if len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    return {"billing_type_search": {"result": "FOUND" if found_row is not None else "CONFIRMED_NOT_FOUND" if complete else "UNKNOWN", "found_row": found_row, "row_count": row_count, "rows_read": len(observed), "visited_scroll_positions": positions, "reference_rows": reference_rows}}


def find_s4615_sales_type(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    expected = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": "ZA01"}
    if params != expected:
        raise ActionBlockedError("FIND_S4615_SALES_TYPE context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != "VOV8" or str(getattr(session.raw.Info, "Program", "") or "").upper() != "SAPL080O":
        raise ActionBlockedError("FIND_S4615_SALES_TYPE requires exact VOV8 view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("FIND_S4615_SALES_TYPE table type mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("FIND_S4615_SALES_TYPE dimensions are unsafe")
    session.audit("FIND_S4615_SALES_TYPE", control_id=expected["table_id"], control_text="read-only VOV8 ZA01 lookup", value={"row_count": row_count})
    observed: dict[int, str] = {}
    related: list[dict[str, str]] = []
    positions: list[int] = []
    found_row = None
    position = 0
    read_error = None
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative = absolute_row - actual
            cell_id = f"{expected['table_id']}/txtV_TVAK-AUART[0,{relative}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiTextField":
                read_error = {"absolute_row": absolute_row, "expected_id": cell_id, "observed_id": _control_value(cell, "Id"), "observed_type": _control_value(cell, "Type")}
                break
            value = str(_control_value(cell, "Text") or "").strip()
            observed[absolute_row] = value
            if value.startswith("ZA") or value in {"OR", "TA", "CS", "BV"}:
                description_id = f"{expected['table_id']}/txtV_TVAK-BEZEI[1,{relative}]"
                description_cell = session.find(description_id)
                if _control_value(description_cell, "Id") != description_id or _control_value(description_cell, "Type") != "GuiTextField":
                    read_error = {"absolute_row": absolute_row, "expected_id": description_id, "observed_id": _control_value(description_cell, "Id"), "observed_type": _control_value(description_cell, "Type")}
                    break
                related.append({"sales_order_type": value, "description": str(_control_value(description_cell, "Text") or "").strip(), "row": absolute_row})
            if value == "ZA01":
                found_row = absolute_row
        if read_error is not None:
            break
        if len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    return {"sales_type_search": {"result": "FOUND" if found_row is not None else "CONFIRMED_NOT_FOUND" if complete else "UNKNOWN", "found_row": found_row, "row_count": row_count, "rows_read": len(observed), "related_types": related, "read_error": read_error}}


def display_s4615_sales_reference(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    target = params.get("sales_order_type")
    expected = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": target, "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
    if target not in {"CS", "BV", "ZA01", "CDCL"} or params != expected:
        raise ActionBlockedError("VOV8 sales reference contract mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != "VOV8" or str(getattr(session.raw.Info, "Program", "") or "").upper() != "SAPL080O":
        raise ActionBlockedError("VOV8 sales reference requires exact overview")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("VOV8 sales reference table mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("VOV8 sales reference dimensions are unsafe")
    maximum = int(table.VerticalScrollbar.Maximum)
    position = 0
    visited: set[int] = set()
    found = None
    found_position = None
    selected_rows: list[int] = []
    scanned_rows: set[int] = set()
    while True:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in visited:
            break
        visited.add(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            row = table.GetAbsoluteRow(absolute_row)
            if bool(row.Selected):
                row.Selected = False
                selected_rows.append(absolute_row)
            cell_id = f"{expected['table_id']}/txtV_TVAK-AUART[0,{absolute_row - actual}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiTextField":
                raise ActionBlockedError("VOV8 sales reference key cell mismatch")
            scanned_rows.add(absolute_row)
            if str(_control_value(cell, "Text") or "").strip() == target:
                if found is not None and found != absolute_row:
                    raise ActionBlockedError("VOV8 sales reference key is duplicated")
                found = absolute_row
                found_position = actual
        if actual >= maximum:
            break
        position = min(actual + visible_count, maximum)
    if len(scanned_rows) != row_count:
        raise ActionBlockedError("VOV8 sales reference selection scan incomplete")
    if found is None or found_position is None:
        if target == "CDCL":
            session.audit("DISPLAY_S4600_CDCL_REFERENCE", control_id=expected["table_id"], control_text="read-only complete VOV8 scan", value={"reference": target, "result": "CONFIRMED_NOT_FOUND", "row_count": row_count, "rows_read": len(scanned_rows), "visited_scroll_positions": sorted(visited)})
            return {"reference": target, "result": "CONFIRMED_NOT_FOUND", "row_count": row_count,
                    "rows_read": len(scanned_rows), "visited_scroll_positions": sorted(visited)}
        raise ActionBlockedError(f"VOV8 sales reference {target} not found")
    table = session.find(expected["table_id"])
    if int(table.VerticalScrollbar.Position) != found_position:
        table.VerticalScrollbar.Position = found_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
    if int(table.VerticalScrollbar.Position) != found_position:
        raise ActionBlockedError("VOV8 sales reference could not return to target page")
    cell_id = f"{expected['table_id']}/txtV_TVAK-AUART[0,{found - found_position}]"
    cell = session.find(cell_id)
    if _control_value(cell, "Id") != cell_id or str(_control_value(cell, "Text") or "").strip() != target:
        raise ActionBlockedError("VOV8 sales reference target changed before selection")
    table.GetAbsoluteRow(found).Selected = True
    button = session.find(expected["detail_button_id"])
    if _control_value(button, "Id") != expected["detail_button_id"] or _control_value(button, "Type") != "GuiButton" or "Détail" not in str(_control_value(button, "Tooltip") or ""):
        raise ActionBlockedError("VOV8 sales reference detail button mismatch")
    audit_action = "DISPLAY_S4600_CDCL_REFERENCE" if target == "CDCL" else "DISPLAY_S4615_SALES_REFERENCE"
    session.audit(audit_action, control_id=expected["detail_button_id"], control_text="Détail", value={"reference": target, "row": found, "cleared_selection_rows": selected_rows})
    button.press()
    snapshot = _wait_for_screen(session, timeout_seconds, poll_seconds)
    if snapshot.get("popups"):
        raise ActionBlockedError("VOV8 sales reference opened unexpected popup")
    fields = {field.get("id", "").rsplit("/", 1)[-1]: field.get("text") for field in snapshot.get("input_fields", [])}
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")), fields.get("txtV_TVAK-AUART")) != ("VOV8", "SAPL080O", "1011", target):
        raise ActionBlockedError("VOV8 detail did not open the selected sales reference")
    return {"reference": target, "source_row": found, "snapshot": snapshot}


def display_s4615_f2_reference(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    target = str(params.get("billing_type") or "")
    if target not in {"F2", "ZF01"}:
        raise ActionBlockedError("VOFA billing detail target is not allowlisted")
    expected = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": target, "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
    if params != expected:
        raise ActionBlockedError("DISPLAY_S4615_F2_REFERENCE context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != "VOFA" or str(getattr(session.raw.Info, "Program", "") or "").upper() != "SAPL081F":
        raise ActionBlockedError("DISPLAY_S4615_F2_REFERENCE requires exact VOFA view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("DISPLAY_S4615_F2_REFERENCE table mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("DISPLAY_S4615_F2_REFERENCE dimensions are unsafe")
    found = None
    position = 0
    visited = set()
    while True:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in visited:
            break
        visited.add(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            cell_id = f"{expected['table_id']}/txtV_TVFK-FKART[0,{absolute_row - actual}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiTextField":
                raise ActionBlockedError("VOFA reference cell mismatch")
            if str(_control_value(cell, "Text") or "").strip() == target:
                found = absolute_row
                break
        if found is not None or actual >= maximum:
            break
        position = min(actual + visible_count, maximum)
    if found is None:
        raise ActionBlockedError(f"{target} billing type not found in VOFA")
    table = session.find(expected["table_id"])
    row = table.GetAbsoluteRow(found)
    row.Selected = True
    button = session.find(expected["detail_button_id"])
    if _control_value(button, "Id") != expected["detail_button_id"] or _control_value(button, "Type") != "GuiButton" or "Détail" not in str(_control_value(button, "Tooltip") or ""):
        raise ActionBlockedError("VOFA F2 detail button mismatch")
    session.audit("DISPLAY_S4615_F2_REFERENCE" if target == "F2" else "DISPLAY_S4615_ZF01", control_id=expected["detail_button_id"], control_text="Détail", value={"billing_type": target, "row": found})
    button.press()
    snapshot = _wait_for_screen(session, timeout_seconds, poll_seconds)
    if snapshot.get("popups"):
        raise ActionBlockedError("VOFA F2 detail opened an unexpected popup")
    return {"reference": target, "source_row": found, "snapshot": snapshot}


def find_s4650_billing_copy_header(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    expected = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK", "billing_type": "F2", "delivery_type": "LF"}
    if params.get("billing_type") == "ZF01":
        expected = {**expected, "billing_type": "ZF01"}
    if params != expected:
        raise ActionBlockedError("FIND_BILLING_COPY_HEADER context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != expected["transaction"] or str(getattr(session.raw.Info, "Program", "") or "").upper() != expected["program"]:
        raise ActionBlockedError("FIND_S4650_BILLING_COPY_HEADER requires exact VTFLC header view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("FIND_S4650_BILLING_COPY_HEADER table type mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("FIND_S4650_BILLING_COPY_HEADER dimensions are unsafe")
    session.audit("FIND_S4615_ZF01_LF_COPY_HEADER" if expected["billing_type"] == "ZF01" else "FIND_S4650_BILLING_COPY_HEADER", control_id=expected["table_id"], control_text="read-only exact VTFLC header lookup", value={"row_count": row_count})
    observed: dict[int, tuple[str, str]] = {}
    positions: list[int] = []
    position = 0
    found_row = None
    while len(observed) < row_count:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            values = []
            for column, field in ((0, "FKARN"), (2, "LFARV")):
                cell_id = f"{expected['table_id']}/ctxtV_TVCPFLK-{field}[{column},{relative_row}]"
                cell = session.find(cell_id)
                if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiCTextField":
                    raise ActionBlockedError(f"VTFLC {field} cell mismatch at row {absolute_row}")
                values.append(str(_control_value(cell, "Text") or "").strip())
            observed[absolute_row] = tuple(values)
            if observed[absolute_row] == (expected["billing_type"], "LF"):
                found_row = absolute_row
                break
        if found_row is not None or len(observed) >= row_count or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    complete = len(observed) == row_count and all(index in observed for index in range(row_count))
    return {"billing_copy_header_search": {"result": "FOUND" if found_row is not None else "CONFIRMED_NOT_FOUND" if complete else "UNKNOWN", "found_row": found_row, "row_count": row_count, "rows_read": len(observed), "visited_scroll_positions": positions}}


def display_s4650_billing_copy_header(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    expected = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK", "billing_type": "F2", "delivery_type": "LF", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
    if params.get("billing_type") == "ZF01":
        expected = {**expected, "billing_type": "ZF01"}
    if params != expected:
        raise ActionBlockedError("DISPLAY_BILLING_COPY_HEADER context mismatch")
    session.validate_identity()
    if str(session.identity.get("transaction") or "").upper() != "VTFLC" or str(getattr(session.raw.Info, "Program", "") or "").upper() != "SAPL080W":
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER requires VTFLC header view")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER table mismatch")
    position, visible_count = int(table.VerticalScrollbar.Position), int(table.VisibleRowCount)
    matches = []
    for relative_row in range(visible_count):
        values = []
        for column, field in ((0, "FKARN"), (2, "LFARV")):
            cell_id = f"{expected['table_id']}/ctxtV_TVCPFLK-{field}[{column},{relative_row}]"
            try:
                cell = session.find(cell_id)
            except Exception:
                continue
            values.append(str(_control_value(cell, "Text") or "").strip())
        if values == [expected["billing_type"], "LF"]:
            matches.append(position + relative_row)
    if len(matches) != 1:
        raise ActionBlockedError("DISPLAY_BILLING_COPY_HEADER exact row is not unique and visible")
    button = session.find(expected["detail_button_id"])
    if _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Tooltip"), "D\u00e9tail   (Ctrl+Maj+F2)") or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER detail button mismatch")
    get_row = getattr(table, "GetAbsoluteRow", None)
    if not callable(get_row):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER row-selection capability missing")
    row = get_row(matches[0])
    if not hasattr(row, "Selected"):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER selected property missing")
    session.audit("DISPLAY_S4615_ZF01_LF_COPY_HEADER" if expected["billing_type"] == "ZF01" else "DISPLAY_S4650_BILLING_COPY_HEADER", control_id=expected["table_id"], control_text="read-only exact billing copy header detail", value={"row": matches[0]})
    row.Selected = True
    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, 10.0, 0.1)
    if after.get("popups"):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_HEADER unexpected popup")
    return after


def open_s4650_billing_copy_items(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    expected = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "110", "tree_id": "/app/con[0]/ses[0]/wnd[0]/shellcont/shell", "node_key": "02", "node_text": "Poste", "column": "Column1"}
    if params != expected:
        raise ActionBlockedError("OPEN_S4650_BILLING_COPY_ITEMS context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    if str(before.get("transaction") or "").upper() != "VTFLC" or str(before.get("program") or "").upper() != "SAPL080W" or str(before.get("screen_number") or "") != "110":
        raise ActionBlockedError("OPEN_S4650_BILLING_COPY_ITEMS requires VTFLC header summary")
    trees = [tree for tree in before.get("tree_controls") or [] if tree.get("id") == expected["tree_id"] and tree.get("type") == "GuiShell" and tree.get("subtype") == "Tree"]
    nodes = [node for tree in trees for node in tree.get("nodes") or [] if node.get("key") == "02" and node.get("text") == "Poste" and node.get("parent_key") == "01"]
    if len(trees) != 1 or len(nodes) != 1 or not any(item.get("column") == "Column1" and item.get("text") == "Poste" for item in nodes[0].get("items") or []) or "DoubleClickItem" not in trees[0].get("native_capabilities", []):
        raise ActionBlockedError("OPEN_S4650_BILLING_COPY_ITEMS exact observed tree contract missing")
    tree = session.find(expected["tree_id"])
    if not callable(getattr(tree, "DoubleClickItem", None)):
        raise ActionBlockedError("OPEN_S4650_BILLING_COPY_ITEMS native method missing")
    session.audit("OPEN_S4650_BILLING_COPY_ITEMS", control_id=expected["tree_id"], control_text="read-only VTFLC Poste navigation", value={"node_key": "02", "column": "Column1"})
    tree.DoubleClickItem("02", "Column1")
    session.validate_identity()
    after = _wait_for_screen(session, 10.0, 0.1)
    if after.get("popups"):
        raise ActionBlockedError("OPEN_S4650_BILLING_COPY_ITEMS unexpected popup")
    return after


def display_s4650_billing_copy_tan(session: SapGuiSession, params: dict[str, Any], *, timeout_seconds: float = 10.0, poll_seconds: float = 0.05) -> dict[str, Any]:
    expected = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "112", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLP", "item_category": "TAN", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
    if params != expected:
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    if str(before.get("transaction") or "").upper() != "VTFLC" or str(before.get("program") or "").upper() != "SAPL080W" or str(before.get("screen_number") or "") != "112":
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN requires exact item summary")
    table = session.find(expected["table_id"])
    if _control_value(table, "Type") != "GuiTableControl":
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN table mismatch")
    row_count, visible_count = int(table.RowCount), int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count < 0 or row_count > 1000 or visible_count <= 0:
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN dimensions unsafe")
    session.audit("DISPLAY_S4650_BILLING_COPY_TAN", control_id=expected["table_id"], control_text="read-only TAN item detail", value={"row_count": row_count})
    positions: set[int] = set()
    position = 0
    found_row = None
    while True:
        table = session.find(expected["table_id"])
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.add(actual)
        for absolute_row in range(actual, min(actual + visible_count, row_count)):
            relative_row = absolute_row - actual
            cell_id = f"{expected['table_id']}/ctxtV_TVCPFLP-PSTYV[0,{relative_row}]"
            cell = session.find(cell_id)
            if _control_value(cell, "Id") != cell_id or _control_value(cell, "Type") != "GuiCTextField":
                raise ActionBlockedError(f"DISPLAY_S4650_BILLING_COPY_TAN cell mismatch at row {absolute_row}")
            if str(_control_value(cell, "Text") or "").strip() == "TAN":
                found_row = absolute_row
                break
        if found_row is not None or actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        _wait_while_busy(session, timeout_seconds, poll_seconds)
        table = session.find(expected["table_id"])
        new_position = int(table.VerticalScrollbar.Position)
        if new_position <= actual:
            break
        position = new_position
    if found_row is None:
        return {"billing_copy_tan_search": {"result": "UNKNOWN", "row_count": row_count, "visited_scroll_positions": sorted(positions)}}
    button = session.find(expected["detail_button_id"])
    if _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Tooltip"), "D\u00e9tail   (Ctrl+Maj+F2)") or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN detail button mismatch")
    table = session.find(expected["table_id"])
    get_row = getattr(table, "GetAbsoluteRow", None)
    if not callable(get_row):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN row-selection capability missing")
    row = get_row(found_row)
    if not hasattr(row, "Selected"):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN Selected property missing")
    row.Selected = True
    button.press()
    session.validate_identity()
    after = _wait_for_screen(session, 10.0, 0.1)
    if after.get("popups"):
        raise ActionBlockedError("DISPLAY_S4650_BILLING_COPY_TAN unexpected popup")
    after["billing_copy_tan_search"] = {"result": "FOUND", "found_row": found_row, "row_count": row_count, "visited_scroll_positions": sorted(positions)}
    return after


def lookup_s4650_product(session: SapGuiSession, params: dict[str, Any]) -> dict[str, Any]:
    expected = {"transaction": "MM02", "program": "SAPLMGMM", "screen": "60", "material": "P650-101", "field_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRMMG1-MATNR", "views_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"}
    if params != expected:
        raise ActionBlockedError("LOOKUP_S4650_PRODUCT context mismatch")
    session.validate_identity()
    before = inspect_screen(session)
    if str(before.get("transaction") or "").upper() != "MM02" or str(before.get("program") or "").upper() != "SAPLMGMM" or str(before.get("screen_number") or "") != "60" or before.get("popups"):
        raise ActionBlockedError("LOOKUP_S4650_PRODUCT requires exact MM02 initial screen")
    field = session.find(expected["field_id"])
    button = session.find(expected["views_button_id"])
    if _control_value(field, "Type") != "GuiCTextField" or not bool(getattr(field, "Changeable", False)) or _control_value(button, "Type") != "GuiButton" or not _observed_exact_text(_control_value(button, "Text"), "S\u00e9lection des vues") or not callable(getattr(button, "press", None)):
        raise ActionBlockedError("LOOKUP_S4650_PRODUCT lookup controls mismatch")
    session.audit("LOOKUP_S4650_PRODUCT", control_id=expected["field_id"], control_text="MM02 material search criterion", value={"material": expected["material"]})
    field.Text = expected["material"]
    button.press()
    session.validate_identity()
    return _wait_for_screen(session, 10.0, 0.1)


def _sales_organization_cells(
    session: SapGuiSession,
    position: int,
    row_count: int,
    visible_count: int,
) -> tuple[dict[int, str], str | None]:
    values: dict[int, str] = {}
    end_row = min(position + visible_count, row_count)
    for absolute_row in range(position, end_row):
        relative_row = absolute_row - position
        control_id = (
            f"{SALES_ORGANIZATION_TABLE_SEARCH['table_id']}"
            f"/ctxtV_TVKO-VKORG[0,{relative_row}]"
        )
        try:
            cell = session.find(control_id)
            if (
                _control_value(cell, "Id") != control_id
                or _control_value(cell, "Type") != "GuiCTextField"
            ):
                return values, f"VKORG cell control mismatch at row {absolute_row}"
            values[absolute_row] = _control_value(cell, "Text").strip()
        except Exception as exc:
            return values, (
                f"VKORG cell is not deterministically readable at row {absolute_row} "
                f"({type(exc).__name__})"
            )
    return values, None


def find_sales_organization_table_value(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.05,
) -> dict[str, Any]:
    """Scan V_TVKO read-only using observed VKORG cell IDs and the table scrollbar."""
    expected = dict(SALES_ORGANIZATION_TABLE_SEARCH)
    if params != expected:
        raise ActionBlockedError("FIND_SALES_ORGANIZATION_VALUE context mismatch")
    session.validate_identity()
    identity = session.identity
    program = str(getattr(session.raw.Info, "Program", "") or "")
    if (
        str(identity.get("transaction") or "").upper() != expected["transaction"]
        or program.upper() != expected["program"]
    ):
        raise ActionBlockedError(
            "FIND_SALES_ORGANIZATION_VALUE requires the exact V_TVKO/SAPL0ORG table"
        )

    try:
        table = session.find(expected["table_id"])
        if str(getattr(table, "Type", "")) != "GuiTableControl":
            raise ValueError("table type mismatch")
        row_count = int(table.RowCount)
        visible_count = int(table.VisibleRowCount)
        scrollbar = table.VerticalScrollbar
        maximum = int(scrollbar.Maximum)
        position = int(scrollbar.Position)
    except Exception as exc:
        return {
            "table_value_search": {
                "result": "UNKNOWN",
                "transaction": expected["transaction"],
                "program": expected["program"],
                "table_id": expected["table_id"],
                "column": expected["column"],
                "value": expected["value"],
                "row_count": None,
                "rows_read": 0,
                "found_row": None,
                "visited_scroll_positions": [],
                "reason": (
                    "table dimensions/scrollbar are not observable "
                    f"({type(exc).__name__})"
                ),
            }
        }
    if row_count < 0 or row_count > 10000 or visible_count <= 0 or maximum < 0:
        return {
            "table_value_search": {
                "result": "UNKNOWN",
                "transaction": expected["transaction"],
                "program": expected["program"],
                "table_id": expected["table_id"],
                "column": expected["column"],
                "value": expected["value"],
                "row_count": row_count,
                "rows_read": 0,
                "found_row": None,
                "visited_scroll_positions": [],
                "reason": "table dimensions/scrollbar are outside safe bounds",
            }
        }

    session.audit(
        "FIND_TABLE_VALUE",
        control_id=expected["table_id"],
        control_text="read-only Sales Organization table scan",
        value={
            "column": expected["column"],
            "value": expected["value"],
            "row_count": row_count,
        },
    )
    observed_rows: dict[int, str] = {}
    visited_positions: set[int] = set()
    found_row: int | None = None
    reason: str | None = None

    if position != 0:
        try:
            scrollbar.Position = 0
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
            position = int(scrollbar.Position)
        except Exception as exc:
            reason = f"vertical scrollbar reset failed ({type(exc).__name__})"
        if reason is None and position != 0:
            reason = "vertical scrollbar did not return to row zero"

    while reason is None:
        try:
            table = session.find(expected["table_id"])
            if str(getattr(table, "Type", "")) != "GuiTableControl":
                raise ValueError("table type changed")
            current_row_count = int(table.RowCount)
            current_visible_count = int(table.VisibleRowCount)
            scrollbar = table.VerticalScrollbar
            position = int(scrollbar.Position)
            current_maximum = int(scrollbar.Maximum)
        except Exception as exc:
            reason = f"table/scrollbar reacquisition failed ({type(exc).__name__})"
            break
        if (
            current_row_count != row_count
            or current_visible_count != visible_count
            or current_maximum != maximum
        ):
            reason = "V_TVKO table dimensions changed during lookup"
            break
        if position < 0 or position > maximum or position in visited_positions:
            reason = f"vertical scrollbar position is invalid or repeated: {position}"
            break
        visited_positions.add(position)
        page_values, page_error = _sales_organization_cells(
            session, position, row_count, visible_count
        )
        for row, value in page_values.items():
            if row in observed_rows and observed_rows[row] != value:
                page_error = f"VKORG value changed during lookup at row {row}"
                break
            observed_rows[row] = value
        if page_error:
            reason = page_error
            break
        matches = [
            row for row, value in page_values.items()
            if value == expected["value"]
        ]
        if matches:
            found_row = matches[0]
            break
        if len(observed_rows) == row_count:
            break
        if position >= maximum:
            reason = "scrollbar reached its maximum before all VKORG rows were covered"
            break

        next_position = min(position + visible_count, maximum)
        if next_position <= position:
            reason = f"vertical scrollbar stalled at position {position}"
            break
        try:
            scrollbar.Position = next_position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            # Discard the old table and scrollbar immediately after every move.
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
            actual_position = int(scrollbar.Position)
        except Exception as exc:
            reason = f"vertical scrollbar traversal failed ({type(exc).__name__})"
            break
        if (
            actual_position <= position
            or actual_position > position + visible_count
            or actual_position > maximum
        ):
            reason = f"vertical scrollbar moved unpredictably from {position} to {actual_position}"
            break

    result = (
        "FOUND"
        if found_row is not None
        else "CONFIRMED_NOT_FOUND"
        if reason is None
        and len(observed_rows) == row_count
        and all(row in observed_rows for row in range(row_count))
        else "UNKNOWN"
    )
    if result == "UNKNOWN" and reason is None:
        reason = f"only {len(observed_rows)} of {row_count} VKORG rows were covered"

    session.validate_identity()
    after_identity = session.identity
    after_program = str(getattr(session.raw.Info, "Program", "") or "")
    if (
        str(after_identity.get("transaction") or "").upper() != expected["transaction"]
        or after_program.upper() != expected["program"]
    ):
        result = "UNKNOWN"
        found_row = None
        reason = "SAP transaction/program changed during Sales Organization lookup"
    search = {
        "result": result,
        "transaction": expected["transaction"],
        "program": expected["program"],
        "table_id": expected["table_id"],
        "column": expected["column"],
        "value": expected["value"],
        "row_count": row_count,
        "rows_read": len(observed_rows),
        "found_row": found_row,
        "visited_scroll_positions": sorted(visited_positions),
        "reason": reason,
    }
    return {"table_value_search": search}


def find_phase5_assignment_table_row(
    session: SapGuiSession,
    operation: str,
    target: dict[str, str],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.05,
) -> dict[str, Any]:
    """Find an exact Phase 5 assignment tuple in its captured SAP GUI table."""
    expected = PHASE5_ASSIGNMENT_TABLE_SEARCHES.get(operation)
    if expected is None or target != expected["target"]:
        raise ActionBlockedError("FIND_PHASE5_ASSIGNMENT_ROW context mismatch")

    session.validate_identity()
    identity = session.identity
    program = str(getattr(session.raw.Info, "Program", "") or "")
    if (
        str(identity.get("transaction") or "").upper() != expected["transaction"]
        or program.upper() != expected["program"]
    ):
        raise ActionBlockedError(
            "FIND_PHASE5_ASSIGNMENT_ROW requires the exact SIMG/"
            "SAPLCUST_ASSIGN_SD assignment screen"
        )

    def unknown(reason: str, *, row_count: int | None = None) -> dict[str, Any]:
        return {
            "table_row_search": {
                "result": "UNKNOWN",
                "transaction": expected["transaction"],
                "program": expected["program"],
                "table_id": expected["table_id"],
                "values": {
                    name: field["value"]
                    for name, field in expected["fields"].items()
                },
                "row_count": row_count,
                "rows_read": 0,
                "found_row": None,
                "visited_scroll_positions": [],
                "reason": reason,
            }
        }

    try:
        table = session.find(expected["table_id"])
        if _control_value(table, "Id") != expected["table_id"]:
            raise ValueError("table ID mismatch")
        if _control_value(table, "Type") != "GuiTableControl":
            raise ValueError("table type mismatch")
        row_count = int(table.RowCount)
        visible_count = int(table.VisibleRowCount)
        scrollbar = table.VerticalScrollbar
        maximum = int(scrollbar.Maximum)
        position = int(scrollbar.Position)
    except Exception as exc:
        return unknown(
            f"table dimensions/scrollbar are not observable ({type(exc).__name__})"
        )
    if row_count < 0 or row_count > 10000 or visible_count <= 0 or maximum < 0:
        return unknown(
            "table dimensions/scrollbar are outside safe bounds",
            row_count=row_count,
        )

    session.audit(
        "FIND_TABLE_VALUE",
        control_id=expected["table_id"],
        control_text="read-only Phase 5 assignment table scan",
        value={
            "operation": operation,
            "values": {
                name: field["value"]
                for name, field in expected["fields"].items()
            },
            "row_count": row_count,
        },
    )
    observed_rows: dict[int, dict[str, str]] = {}
    visited_positions: set[int] = set()
    found_row: int | None = None
    reason: str | None = None

    if position != 0:
        try:
            scrollbar.Position = 0
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
            position = int(scrollbar.Position)
        except Exception as exc:
            reason = f"vertical scrollbar reset failed ({type(exc).__name__})"
        if reason is None and position != 0:
            reason = "vertical scrollbar did not return to row zero"

    while reason is None:
        try:
            table = session.find(expected["table_id"])
            if (
                _control_value(table, "Id") != expected["table_id"]
                or _control_value(table, "Type") != "GuiTableControl"
            ):
                raise ValueError("table identity/type changed")
            current_row_count = int(table.RowCount)
            current_visible_count = int(table.VisibleRowCount)
            scrollbar = table.VerticalScrollbar
            position = int(scrollbar.Position)
            current_maximum = int(scrollbar.Maximum)
        except Exception as exc:
            reason = f"table/scrollbar reacquisition failed ({type(exc).__name__})"
            break
        if (
            current_row_count != row_count
            or current_visible_count != visible_count
            or current_maximum != maximum
        ):
            reason = "assignment table dimensions changed during lookup"
            break
        if position < 0 or position > maximum or position in visited_positions:
            reason = f"vertical scrollbar position is invalid or repeated: {position}"
            break
        visited_positions.add(position)

        page_rows: dict[int, dict[str, str]] = {}
        end_row = min(position + visible_count, row_count)
        for absolute_row in range(position, end_row):
            relative_row = absolute_row - position
            row_values: dict[str, str] = {}
            for field_name, field in expected["fields"].items():
                control_id = (
                    f"{expected['table_id']}/{field['control']}"
                    f"[{field['column']},{relative_row}]"
                )
                try:
                    cell = session.find(control_id)
                    if (
                        _control_value(cell, "Id") != control_id
                        or _control_value(cell, "Type") != "GuiCTextField"
                    ):
                        raise ValueError("cell control ID/type mismatch")
                    row_values[field_name] = str(
                        _control_value(cell, "Text") or ""
                    ).strip()
                except Exception as exc:
                    reason = (
                        f"{field_name} cell is not deterministically readable "
                        f"at row {absolute_row} ({type(exc).__name__})"
                    )
                    break
            if reason is not None:
                break
            page_rows[absolute_row] = row_values
            if absolute_row in observed_rows and observed_rows[absolute_row] != row_values:
                reason = (
                    f"assignment values changed during lookup at row {absolute_row}"
                )
                break
            observed_rows[absolute_row] = row_values
        if reason is not None:
            break

        matches = [
            row
            for row, values in page_rows.items()
            if all(
                values[field_name] == field["value"]
                for field_name, field in expected["fields"].items()
            )
        ]
        if matches:
            found_row = matches[0]
            break
        if len(observed_rows) == row_count:
            break
        if position >= maximum:
            reason = "scrollbar reached its maximum before all assignment rows were covered"
            break

        next_position = min(position + visible_count, maximum)
        if next_position <= position:
            reason = f"vertical scrollbar stalled at position {position}"
            break
        try:
            scrollbar.Position = next_position
            _wait_while_busy(session, timeout_seconds, poll_seconds)
            table = session.find(expected["table_id"])
            scrollbar = table.VerticalScrollbar
            actual_position = int(scrollbar.Position)
        except Exception as exc:
            reason = f"vertical scrollbar traversal failed ({type(exc).__name__})"
            break
        if (
            actual_position <= position
            or actual_position > position + visible_count
            or actual_position > maximum
        ):
            reason = (
                f"vertical scrollbar moved unpredictably from {position} "
                f"to {actual_position}"
            )
            break

    result = (
        "FOUND"
        if found_row is not None
        else "CONFIRMED_NOT_FOUND"
        if reason is None
        and len(observed_rows) == row_count
        and all(row in observed_rows for row in range(row_count))
        else "UNKNOWN"
    )
    if result == "UNKNOWN" and reason is None:
        reason = (
            f"only {len(observed_rows)} of {row_count} assignment rows were covered"
        )

    session.validate_identity()
    after_identity = session.identity
    after_program = str(getattr(session.raw.Info, "Program", "") or "")
    if (
        str(after_identity.get("transaction") or "").upper()
        != expected["transaction"]
        or after_program.upper() != expected["program"]
    ):
        result = "UNKNOWN"
        found_row = None
        reason = "SAP transaction/program changed during assignment lookup"

    return {
        "table_row_search": {
            "result": result,
            "transaction": expected["transaction"],
            "program": expected["program"],
            "table_id": expected["table_id"],
            "values": {
                name: field["value"]
                for name, field in expected["fields"].items()
            },
            "row_count": row_count,
            "rows_read": len(observed_rows),
            "found_row": found_row,
            "visited_scroll_positions": sorted(visited_positions),
            "reason": reason,
        }
    }


def _normalized_text(value: Any) -> str:
    decomposed = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in decomposed if not unicodedata.combining(char)).casefold()


def _observed_exact_text(
    observed: Any,
    expected: str,
    *,
    allow_trailing_colon: bool = False,
) -> bool:
    actual = _normalized_text(observed).strip()
    wanted = _normalized_text(expected).strip()
    if allow_trailing_colon:
        actual = actual.rstrip(" :")
    pattern = re.escape(actual).replace("\ufffd", ".")
    return re.fullmatch(pattern, wanted) is not None


def _all_popup_text_values(popup: dict[str, Any]) -> list[str]:
    values = [
        str(record.get("text"))
        for record in popup.get("controls") or []
        if record.get("text")
    ]
    for table in popup.get("tables") or []:
        for row in table.get("visible_rows") or []:
            values.extend(
                str(value.get("text"))
                for value in row.get("values") or []
                if value.get("text")
            )
    return values


def _assert_safe_context(*values: Any) -> None:
    for value in values:
        normalized = _normalized_text(value)
        blocked = next((term for term in BLOCKED_NAVIGATION_TERMS if term in normalized), None)
        if blocked:
            raise ActionBlockedError(
                f"Navigation context contains blocked write term: {blocked!r}"
            )


def _control_value(control: Any, name: str) -> str:
    try:
        return str(getattr(control, name) or "")
    except Exception:
        return ""


def _is_tree(control: Any, control_type: str) -> bool:
    if control_type == "GuiTree":
        return True
    subtype = _control_value(control, "SubType")
    return control_type == "GuiShell" and "tree" in subtype.casefold()


def _is_mm01_basic_tab_exception(operation: str, control_id: str, tab_text: str, snapshot: dict[str, Any]) -> bool:
    """Allow only the observed Basic Data 2 tab despite MM01's 'Créer' title."""
    return (
        operation == "SELECT_TAB"
        and control_id == "/app/con[0]/ses[0]/wnd[0]/usr/tabsTABSPR1/tabpSP02"
        and tab_text == " Données de base 2"
        and (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")))
        == ("MM01", "SAPLMGMM", "4004")
        and not snapshot.get("popups")
    )


def _is_company_code_display_exception(
    session: SapGuiSession,
    operation: str,
    control_id: str,
    node_key: str | None,
    node_text: str,
    snapshot: dict[str, Any] | None = None,
) -> bool:
    approved = COMPANY_CODE_DISPLAY_EXCEPTION
    if snapshot is None or node_key is None:
        return False
    trees = [
        tree
        for tree in snapshot.get("tree_controls", [])
        if tree.get("id") == control_id
    ]
    if len(trees) != 1:
        return False
    nodes = trees[0].get("nodes", [])
    current = [node for node in nodes if node.get("key") == node_key]
    if len(current) != 1 or current[0].get("text") != approved["node_text"]:
        return False
    parents = [
        node for node in nodes if node.get("key") == current[0].get("parent_key")
    ]
    return (
        str(session.identity.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("program", "")).upper() == approved["program"]
        and control_id == approved["control_id"]
        and node_text == approved["node_text"]
        and len(parents) == 1
        and parents[0].get("text") == approved["parent_text"]
        and operation in approved["operations"]
    )


def _is_sales_organization_display_exception(
    session: SapGuiSession,
    operation: str,
    control_id: str,
    node_key: str | None,
    node_text: str,
    snapshot: dict[str, Any] | None = None,
) -> bool:
    approved = SALES_ORGANIZATION_DISPLAY_EXCEPTION
    if snapshot is None or node_key is None:
        return False
    trees = [
        tree
        for tree in snapshot.get("tree_controls", [])
        if tree.get("id") == control_id
    ]
    if len(trees) != 1:
        return False
    nodes = trees[0].get("nodes", [])
    by_key = {node.get("key"): node for node in nodes if node.get("key")}
    current = by_key.get(node_key)
    if current is None or current.get("text") != approved["node_text"]:
        return False
    observed_path = []
    parent_key = current.get("parent_key")
    while parent_key is not None and len(observed_path) < len(approved["path"]):
        parent = by_key.get(parent_key)
        if parent is None:
            return False
        observed_path.append(parent.get("text"))
        parent_key = parent.get("parent_key")
    observed_path.reverse()
    return (
        str(session.identity.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("program", "")).upper() == approved["program"]
        and control_id == approved["control_id"]
        and node_text == approved["node_text"]
        and tuple(observed_path) == approved["path"]
        and operation == approved["operation"]
    )


def _is_distribution_channel_display_exception(
    session: SapGuiSession,
    operation: str,
    control_id: str,
    node_key: str | None,
    node_text: str,
    snapshot: dict[str, Any] | None = None,
) -> bool:
    approved = DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION
    if snapshot is None or node_key is None:
        return False
    trees = [
        tree
        for tree in snapshot.get("tree_controls", [])
        if tree.get("id") == control_id
    ]
    if len(trees) != 1:
        return False
    nodes = trees[0].get("nodes", [])
    by_key = {node.get("key"): node for node in nodes if node.get("key")}
    current = by_key.get(node_key)
    if current is None or current.get("text") != approved["node_text"]:
        return False
    observed_path = []
    parent_key = current.get("parent_key")
    while parent_key is not None and len(observed_path) < len(approved["path"]):
        parent = by_key.get(parent_key)
        if parent is None:
            return False
        observed_path.append(parent.get("text"))
        parent_key = parent.get("parent_key")
    observed_path.reverse()
    return (
        str(session.identity.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("transaction", "")).upper() == approved["transaction"]
        and str(snapshot.get("program", "")).upper() == approved["program"]
        and control_id == approved["control_id"]
        and node_text == approved["node_text"]
        and tuple(observed_path) == approved["path"]
        and operation == approved["operation"]
    )


def _is_sales_division_display_exception(session: SapGuiSession, operation: str, control_id: str, node_key: str | None, node_text: str, snapshot: dict[str, Any] | None = None) -> bool:
    approved = SALES_DIVISION_DISPLAY_EXCEPTION
    if snapshot is None or node_key is None:
        return False
    trees = [tree for tree in snapshot.get("tree_controls", []) if tree.get("id") == control_id]
    if len(trees) != 1:
        return False
    by_key = {node.get("key"): node for node in trees[0].get("nodes", []) if node.get("key")}
    current = by_key.get(node_key)
    if current is None or current.get("text") != approved["node_text"]:
        return False
    observed_path = []
    parent_key = current.get("parent_key")
    while parent_key is not None and len(observed_path) < len(approved["path"]):
        parent = by_key.get(parent_key)
        if parent is None:
            return False
        observed_path.append(parent.get("text"))
        parent_key = parent.get("parent_key")
    observed_path.reverse()
    return (str(session.identity.get("transaction", "")).upper() == approved["transaction"] and str(snapshot.get("transaction", "")).upper() == approved["transaction"] and str(snapshot.get("program", "")).upper() == approved["program"] and control_id == approved["control_id"] and node_text == approved["node_text"] and tuple(observed_path) == approved["path"] and operation == approved["operation"])


def _wait_for_screen(
    session: SapGuiSession,
    timeout_seconds: float,
    poll_seconds: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while bool(getattr(session.raw, "Busy", False)):
        if time.monotonic() >= deadline:
            raise ActionBlockedError("NAVIGATE screen did not finish loading")
        time.sleep(poll_seconds)
    try:
        return inspect_screen(session)
    except Exception as exc:
        raise ActionBlockedError("NAVIGATE resulting screen is not readable") from exc


def _tree_from_snapshot(snapshot: dict[str, Any], control_id: str) -> dict[str, Any] | None:
    return next(
        (tree for tree in snapshot.get("tree_controls", []) if tree.get("id") == control_id),
        None,
    )


def _descendant_keys(tree: dict[str, Any] | None, node_key: str | None) -> set[str]:
    if tree is None or node_key is None:
        return set()
    nodes = tree.get("nodes", [])
    children: dict[str | None, list[str]] = {}
    for node in nodes:
        children.setdefault(node.get("parent_key"), []).append(node.get("key"))
    descendants: set[str] = set()
    pending = list(children.get(node_key, []))
    while pending:
        key = pending.pop()
        if key in descendants or key is None:
            continue
        descendants.add(key)
        pending.extend(children.get(key, []))
    return descendants


def _direct_children_loaded(tree: dict[str, Any] | None, node_key: str | None) -> bool:
    if tree is None or node_key is None:
        return False
    if any(node.get("parent_key") == node_key for node in tree.get("nodes", [])):
        return True
    node = next(
        (item for item in tree.get("nodes", []) if item.get("key") == node_key),
        {},
    )
    return bool(node.get("children_count"))


def _user_area_signature(snapshot: dict[str, Any]) -> tuple[Any, ...]:
    return (
        tuple(sorted(value for value in snapshot.get("control_ids", []) if "/usr/" in value)),
        tuple(
            sorted(
                (
                    str(item.get("id") or ""),
                    str(item.get("text") or ""),
                    bool(item.get("changeable")),
                )
                for section in ("labels", "input_fields", "tables", "buttons")
                for item in snapshot.get(section, [])
                if item.get("type") != "GuiMenu"
            )
        ),
    )


def _navigation_effect(
    before: dict[str, Any],
    after: dict[str, Any],
    operation: str,
    control_id: str,
    node_key: str | None,
) -> dict[str, Any]:
    before_tree = _tree_from_snapshot(before, control_id)
    after_tree = _tree_from_snapshot(after, control_id)
    before_nodes = {node.get("key") for node in (before_tree or {}).get("nodes", [])}
    after_nodes = {node.get("key") for node in (after_tree or {}).get("nodes", [])}
    before_descendants = _descendant_keys(before_tree, node_key)
    after_descendants = _descendant_keys(after_tree, node_key)
    before_node = next(
        (node for node in (before_tree or {}).get("nodes", []) if node.get("key") == node_key),
        {},
    )
    after_node = next(
        (node for node in (after_tree or {}).get("nodes", []) if node.get("key") == node_key),
        {},
    )
    transaction_changed = before.get("transaction") != after.get("transaction")
    program_changed = before.get("program") != after.get("program")
    window_changed = before.get("window_title") != after.get("window_title")
    before_windows = {popup.get("id") for popup in before.get("popups", [])}
    after_windows = {popup.get("id") for popup in after.get("popups", [])}
    new_windows = sorted(value for value in after_windows - before_windows if value)
    expanded_changed = before_node.get("expanded") is not True and after_node.get("expanded") is True
    selected_changed = before_node.get("selected") is not True and after_node.get("selected") is True
    user_area_changed = _user_area_signature(before) != _user_area_signature(after)
    tree_disappeared = before_tree is not None and after_tree is None
    screen_changed = any(
        (
            transaction_changed,
            program_changed,
            window_changed,
            bool(new_windows),
            user_area_changed,
            tree_disappeared,
        )
    )
    descendants_increased = len(after_descendants) > len(before_descendants)
    if operation == "EXPAND_TREE_NODE":
        observed = expanded_changed or descendants_increased
    elif operation == "COLLAPSE_TREE_NODE":
        observed = before_node.get("expanded") is True and after_node.get("expanded") is False
    elif operation == "SELECT_TREE_NODE":
        observed = selected_changed
    elif operation == "OPEN_IMG_ACTIVITY":
        observed = screen_changed
    elif operation == "DOUBLE_CLICK_TREE_NODE":
        observed = screen_changed or expanded_changed or descendants_increased
    else:
        observed = screen_changed or selected_changed
    return {
        "observed": observed,
        "transaction_changed": transaction_changed,
        "program_changed": program_changed,
        "window_changed": window_changed,
        "user_area_signature_changed": user_area_changed,
        "tree_disappeared": tree_disappeared,
        "tree_node_count_before": len(before_nodes),
        "tree_node_count_after": len(after_nodes),
        "descendant_count_before": len(before_descendants),
        "descendant_count_after": len(after_descendants),
        "new_node_keys": sorted(value for value in after_nodes - before_nodes if value),
        "new_windows": new_windows,
        "expanded_changed": expanded_changed,
        "selected_changed": selected_changed,
    }


def _node_metadata(snapshot: dict[str, Any], control_id: str, node_key: str) -> dict[str, Any]:
    tree = _tree_from_snapshot(snapshot, control_id) or {}
    node = next(
        (item for item in tree.get("nodes", []) if item.get("key") == node_key),
        {},
    )
    return {
        "columns": tree.get("columns", []),
        "native_capabilities": tree.get("native_capabilities", []),
        "selected_node": tree.get("selected_node"),
        "focused_item": tree.get("focused_item"),
        "node": node,
    }


def navigate(
    session: SapGuiSession,
    params: dict[str, Any],
    *,
    timeout_seconds: float = 10.0,
    poll_seconds: float = 0.1,
) -> dict[str, Any]:
    """Perform one explicitly allowlisted navigation operation and re-inspect."""

    session.validate_identity()
    operation = params["navigation_operation"]
    control_id = params["control_id"]
    expected_type = params["expected_type"]
    expected_text = params["expected_text"]
    node_key = params.get("node_key")
    item_column = params.get("item_column")
    expected_transaction = params.get("expected_transaction")

    before = inspect_screen(session)

    try:
        control = session.find(control_id)
    except Exception as exc:
        raise ActionBlockedError(f"NAVIGATE control not found: {control_id}") from exc

    actual_id = _control_value(control, "Id")
    actual_type = _control_value(control, "Type")
    actual_text = _control_value(control, "Text")
    tooltip = _control_value(control, "Tooltip")
    if actual_id != control_id:
        raise ActionBlockedError(f"NAVIGATE control ID mismatch: {actual_id!r}")
    if actual_type != expected_type:
        raise ActionBlockedError(
            f"NAVIGATE control type mismatch: expected {expected_type!r}, got {actual_type!r}"
        )
    if expected_transaction is not None and str(session.identity.get("transaction", "")).upper() != expected_transaction:
        raise ActionBlockedError(
            f"NAVIGATE transaction mismatch: expected {expected_transaction!r}"
        )

    root = session.find("wnd[0]")
    window_title = _control_value(root, "Text")
    status_text = _control_value(session.find("wnd[0]/sbar"), "Text")
    comparison_text = actual_text or tooltip
    if operation in TREE_OPERATIONS:
        if not _is_tree(control, actual_type):
            raise ActionBlockedError(f"{operation} requires a tree control")
        comparison_text, _, extraction_error = read_tree_node_text(control, node_key)
        if comparison_text is None:
            raise ActionBlockedError(
                f"Tree node text is not verifiable for {node_key!r}: {extraction_error}"
            )
    if expected_text is not None and comparison_text != expected_text:
        raise ActionBlockedError(
            f"NAVIGATE text mismatch: expected {expected_text!r}, got {comparison_text!r}"
        )

    company_code_display_exception = _is_company_code_display_exception(
        session, operation, control_id, node_key, comparison_text, before
    )
    sales_organization_display_exception = _is_sales_organization_display_exception(
        session, operation, control_id, node_key, comparison_text, before
    )
    distribution_channel_display_exception = _is_distribution_channel_display_exception(
        session, operation, control_id, node_key, comparison_text, before
    )
    sales_division_display_exception = _is_sales_division_display_exception(
        session, operation, control_id, node_key, comparison_text, before
    )
    mm01_basic_tab_exception = _is_mm01_basic_tab_exception(operation, control_id, comparison_text, before)
    vtflc_item_display_exception = (
        operation in {"SELECT_TREE_NODE", "DOUBLE_CLICK_TREE_NODE"}
        and control_id == "/app/con[0]/ses[0]/wnd[0]/shellcont/shell"
        and node_key == "02"
        and comparison_text == "Poste"
        and str(before.get("transaction") or "").upper() == "VTFLC"
        and str(before.get("program") or "").upper() == "SAPL080W"
        and str(before.get("screen_number") or "") == "110"
        and any(tree.get("id") == control_id and any(node.get("key") == "02" and node.get("text") == "Poste" for node in tree.get("nodes") or []) for tree in before.get("tree_controls") or [])
    )
    read_only_exception = (
        "COMPANY_CODE_DISPLAY"
        if company_code_display_exception
        else (
            "SALES_ORGANIZATION_DISPLAY"
            if sales_organization_display_exception
            else (
                "DISTRIBUTION_CHANNEL_DISPLAY"
                if distribution_channel_display_exception
                else ("SALES_DIVISION_DISPLAY" if sales_division_display_exception else ("VTFLC_ITEM_DISPLAY" if vtflc_item_display_exception else None))
            )
        )
    )
    if mm01_basic_tab_exception:
        _assert_safe_context(actual_text, comparison_text, tooltip, status_text)
    elif vtflc_item_display_exception:
        _assert_safe_context(actual_text, tooltip, status_text)
    elif read_only_exception:
        _assert_safe_context(actual_text, tooltip, window_title, status_text)
    else:
        _assert_safe_context(actual_text, comparison_text, tooltip, window_title, status_text)
    session.audit(
        "NAVIGATE",
        control_id=control_id,
        control_text=(
            "approved read-only IMG display activity"
            if read_only_exception
            else " ".join(filter(None, (comparison_text, tooltip)))
        ),
        value={
            "operation": operation,
            "node_key": node_key,
            "node_text": comparison_text,
            "read_only_exception": read_only_exception,
        },
    )

    chosen_native_method = None
    metadata = _node_metadata(before, control_id, node_key) if node_key else None
    already_expanded = False

    if operation == "PRESS_SAFE_BUTTON":
        if actual_type != "GuiButton":
            raise ActionBlockedError("PRESS_SAFE_BUTTON requires GuiButton")
        if expected_text is None or not comparison_text:
            raise ActionBlockedError(
                "PRESS_SAFE_BUTTON requires an observed expected_text"
            )
        control.press()
        chosen_native_method = "Press"
    elif operation == "SELECT_TREE_NODE":
        control.SelectNode(node_key)
        chosen_native_method = "SelectNode"
    elif operation == "EXPAND_TREE_NODE":
        if _direct_children_loaded(_tree_from_snapshot(before, control_id), node_key):
            already_expanded = True
        else:
            control.ExpandNode(node_key)
            chosen_native_method = "ExpandNode"
    elif operation == "COLLAPSE_TREE_NODE":
        control.CollapseNode(node_key)
        chosen_native_method = "CollapseNode"
    elif operation == "DOUBLE_CLICK_TREE_NODE":
        control.DoubleClickNode(node_key)
        chosen_native_method = "DoubleClickNode"
    elif operation == "OPEN_IMG_ACTIVITY":
        capabilities = set((metadata or {}).get("native_capabilities", []))
        columns = list((metadata or {}).get("columns", []))
        items = ((metadata or {}).get("node") or {}).get("items", [])
        if item_column is not None:
            item = next((value for value in items if value.get("column") == item_column), None)
            if item_column not in columns or item is None:
                raise ActionBlockedError(
                    "OPEN_IMG_ACTIVITY item column is not backed by observed tree capabilities"
                )
            item_type = str(item.get("type") or "")
            if item_type == "4" and "PressButton" in capabilities:
                control.PressButton(node_key, item_column)
                chosen_native_method = "PressButton"
            elif item_type == "5" and "ClickLink" in capabilities:
                control.ClickLink(node_key, item_column)
                chosen_native_method = "ClickLink"
            elif item_type == "5" and "DoubleClickItem" in capabilities:
                control.DoubleClickItem(node_key, item_column)
                chosen_native_method = "DoubleClickItem"
            elif item_type == "2":
                raise ActionBlockedError(
                    "OPEN_IMG_ACTIVITY refuses item type 2 as the primary open method"
                )
            else:
                raise ActionBlockedError(
                    f"OPEN_IMG_ACTIVITY has no observed safe method for item type {item_type!r}"
                )
        else:
            supported = [
                item
                for item in items
                if (
                    str(item.get("type") or "") == "4"
                    and "PressButton" in capabilities
                )
                or (
                    str(item.get("type") or "") == "5"
                    and (
                        "ClickLink" in capabilities
                        or "DoubleClickItem" in capabilities
                    )
                )
            ]
            if len(supported) != 1:
                raise ActionBlockedError(
                    "OPEN_IMG_ACTIVITY requires one explicit observed type 4/5 item column"
                )
            item_column = supported[0]["column"]
            if str(supported[0].get("type")) == "4":
                control.PressButton(node_key, item_column)
                chosen_native_method = "PressButton"
            else:
                if "ClickLink" in capabilities:
                    control.ClickLink(node_key, item_column)
                    chosen_native_method = "ClickLink"
                else:
                    control.DoubleClickItem(node_key, item_column)
                    chosen_native_method = "DoubleClickItem"
    elif operation == "SELECT_TAB":
        if actual_type != "GuiTab":
            raise ActionBlockedError("SELECT_TAB requires GuiTab")
        control.Select()
    elif operation == "FOCUS_CONTROL":
        if actual_type not in FOCUS_TYPES:
            raise ActionBlockedError(f"FOCUS_CONTROL is blocked for {actual_type}")
        control.SetFocus()
    elif operation == "BACK":
        if actual_type != "GuiMainWindow" or control_id not in {
            "wnd[0]",
            "/app/con[0]/ses[0]/wnd[0]",
        }:
            raise ActionBlockedError("BACK requires the main window control")
        control.sendVKey(3)
    else:
        raise ActionBlockedError(f"Unsupported navigation operation: {operation}")

    session.validate_identity()
    after = before if already_expanded else _wait_for_screen(session, timeout_seconds, poll_seconds)
    effect = _navigation_effect(before, after, operation, control_id, node_key)
    if already_expanded:
        effect["observed"] = True
        effect["already_expanded"] = True
        after["navigation_outcome"] = "ALREADY_EXPANDED"
    else:
        after["navigation_outcome"] = "SUCCESS" if effect["observed"] else "NO_OBSERVED_EFFECT"
    after["navigation_effect"] = effect
    after["chosen_native_method"] = chosen_native_method
    if operation == "OPEN_IMG_ACTIVITY":
        after["img_activity_open"] = {
            "node_metadata": metadata,
            "item_column": item_column,
            "chosen_native_method": chosen_native_method,
            "screen_signature_before": {
                "transaction": before.get("transaction"),
                "program": before.get("program"),
                "window_title": before.get("window_title"),
            },
            "screen_signature_after": {
                "transaction": after.get("transaction"),
                "program": after.get("program"),
                "window_title": after.get("window_title"),
            },
        }
    return after


def press_safe_button(session: SapGuiSession, control_id: str) -> None:
    control = session.find(control_id)
    text = str(getattr(control, "Text", "") or getattr(control, "Tooltip", ""))
    session.audit("PRESS_SAFE_BUTTON", control_id=control_id, control_text=text)
    control.press()
    session.validate_identity()


def set_text(session: SapGuiSession, control_id: str, value: str) -> None:
    if session.policy.mode.value != "PREPARE":
        raise ActionBlockedError("Field entry requires PREPARE mode")
    control = session.find(control_id)
    text = str(getattr(control, "Text", "") or getattr(control, "Tooltip", ""))
    session.audit("SET_TEXT", control_id=control_id, control_text=text, value=value)
    control.Text = value
    session.validate_identity()
