"""Exact, one-shot SAP GUI contract for T-S50A01's first BP address."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.provisioning.s4615_bp_address_gui import (
    ADDRESS_PREFIX, FIELD_IDS, FIELD_TYPES, HEADER, SAVE_ID, _entries,
)


ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "data/provisioning/s4600/T-S50A01.bp_address_approval.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
ATTEMPT_PATH = ROOT / "data/provisioning/s4600/T-S50A01.bp_address_attempt.json"
BP = "1000000116"
OPERATION = "S4600_T_S50A01_BP_ADDRESS"
FINGERPRINT = "60af943bd3ce670d8c4b3ae0b372e301615fcfe20cbd91a6b7b3ee23fbac8f1d"
TARGET = {"logical_id": "T-S50A01", "sap_id": BP}
ADDRESS = {
    "StreetName": "1 Schulungsstrasse S4600",
    "PostalCode": "69115",
    "CityName": "Heidelberg",
    "Country": "DE",
    "Language": "EN",
}
SEARCH_FIELD_ID = (
    "/app/con[0]/ses[0]/wnd[0]/usr/"
    "subSCREEN_3000_RESIZING_AREA:SAPLBUS_LOCATOR:2240/"
    "subSCREEN_1010_LEFT_AREA:SAPLBUS_LOCATOR:3100/"
    "tabsGS_SCREEN_3100_TABSTRIP/tabpBUS_LOCATOR_TAB_02/"
    "ssubSCREEN_3100_TABSTRIP_AREA:SAPLBUS_LOCATOR:3202/"
    "subSCREEN_3200_SEARCH_AREA:SAPLBUS_LOCATOR:3211/"
    "subSCREEN_3200_SEARCH_FIELDS_AREA:SAPLBUPA_DIALOG_SEARCH:2100/"
    "txtBUS_JOEL_SEARCH-PARTNER_NUMBER"
)
SEARCH_GO_ID = (
    "/app/con[0]/ses[0]/wnd[0]/usr/"
    "subSCREEN_3000_RESIZING_AREA:SAPLBUS_LOCATOR:2240/"
    "subSCREEN_1010_LEFT_AREA:SAPLBUS_LOCATOR:3100/"
    "tabsGS_SCREEN_3100_TABSTRIP/tabpBUS_LOCATOR_TAB_02/"
    "ssubSCREEN_3100_TABSTRIP_AREA:SAPLBUS_LOCATOR:3202/"
    "subSCREEN_3200_SEARCH_AREA:SAPLBUS_LOCATOR:3211/"
    "subSCREEN_3200_SEARCH_BUTTON_AREA:SAPLBUS_LOCATOR:3240/"
    "btnBUS_LOCA_SRCH01-GO"
)
RESULT_TABLE_ID = (
    "/app/con[0]/ses[0]/wnd[0]/usr/"
    "subSCREEN_3000_RESIZING_AREA:SAPLBUS_LOCATOR:2240/"
    "subSCREEN_1010_LEFT_AREA:SAPLBUS_LOCATOR:3100/"
    "tabsGS_SCREEN_3100_TABSTRIP/tabpBUS_LOCATOR_TAB_02/"
    "ssubSCREEN_3100_TABSTRIP_AREA:SAPLBUS_LOCATOR:3202/"
    "subSCREEN_3200_SEARCH_AREA:SAPLBUS_LOCATOR:3211/"
    "subSCREEN_3200_RESULT_AREA:SAPLBUPA_DIALOG_JOEL:1060/"
    "ssubSCREEN_1060_RESULT_AREA:SAPLBUPA_DIALOG_JOEL:1080/"
    "cntlSCREEN_1080_CONTAINER/shellcont/shell"
)
OPEN_PARTNER_ID = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[17]"
OPEN_NUMBER_ID = "/app/con[0]/ses[0]/wnd[1]/usr/ctxtBUS_JOEL_MAIN-OPEN_NUMBER"
OPEN_CONFIRM_ID = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"


def position_search(session: Any) -> dict[str, Any]:
    """Run the exact read-only BP-number search for 1000000116."""
    session.validate_identity()
    snapshot = inspect_screen(session)
    if (
        snapshot.get("transaction") != "BP"
        or snapshot.get("program") != "SAPLBUS_LOCATOR"
        or str(snapshot.get("screen_number")) != "3000"
        or snapshot.get("window_title") != "Traiter partenaire"
        or snapshot.get("popups")
        or snapshot.get("truncated")
    ):
        raise ActionBlockedError("T-S50A01 search requires the exact BP locator screen")
    fields = {field.get("id"): field for field in snapshot.get("input_fields", [])}
    field_info = fields.get(SEARCH_FIELD_ID, {})
    if field_info.get("type") != "GuiTextField" or field_info.get("changeable") is not True:
        raise ActionBlockedError("Exact BP partner-number search field not observed")
    buttons = {button.get("id"): button for button in snapshot.get("buttons", [])}
    button_info = buttons.get(SEARCH_GO_ID, {})
    if button_info.get("type") != "GuiButton" or button_info.get("text") != "Lancer":
        raise ActionBlockedError("Exact BP search button not observed")
    field = session.find(SEARCH_FIELD_ID)
    if str(getattr(field, "Id", "")) != SEARCH_FIELD_ID or str(getattr(field, "Type", "")) != "GuiTextField":
        raise ActionBlockedError("Live BP search field mismatch")
    field.Text = BP
    if str(field.Text).strip() != BP:
        raise ActionBlockedError("BP search field did not retain exact target")
    button = session.find(SEARCH_GO_ID)
    if str(getattr(button, "Id", "")) != SEARCH_GO_ID or str(getattr(button, "Type", "")) != "GuiButton":
        raise ActionBlockedError("Live BP search button mismatch")
    session.audit("POSITION_S4600_T_S50A01_BP", control_id=SEARCH_GO_ID, value={"bp": BP})
    button.press()
    session.validate_identity()
    return inspect_screen(session)


def open_exact_partner(session: Any) -> dict[str, Any]:
    """Open only the single exact T-S50A01 search result."""
    session.validate_identity()
    snapshot = inspect_screen(session)
    if (
        snapshot.get("transaction") != "BP"
        or snapshot.get("program") != "SAPLBUS_LOCATOR"
        or str(snapshot.get("screen_number")) != "3000"
        or snapshot.get("window_title") != "Traiter partenaire"
        or snapshot.get("popups")
        or snapshot.get("truncated")
        or snapshot.get("status_bar", {}).get("message_type") != "S"
    ):
        raise ActionBlockedError("Exact T-S50A01 BP search-result screen is not active")
    tables = {table.get("id"): table for table in snapshot.get("tables", [])}
    table_info = tables.get(RESULT_TABLE_ID, {})
    rows = table_info.get("visible_rows") or []
    values = {cell.get("column"): cell.get("text") for cell in rows[0].get("values", [])} if len(rows) == 1 else {}
    if (
        table_info.get("type") != "GuiShell"
        or table_info.get("subtype") != "GridView"
        or table_info.get("row_count") != 1
        or values.get("PARTNER") != BP
        or values.get("DESCRIPTION") != "Motormarkt Heidelberg"
    ):
        raise ActionBlockedError("Single exact T-S50A01 BP search result not proven")
    buttons = {button.get("id"): button for button in snapshot.get("buttons", [])}
    open_info = buttons.get(OPEN_PARTNER_ID, {})
    if open_info.get("type") != "GuiButton" or not str(open_info.get("tooltip") or "").startswith("Ouvrir PRTN."):
        raise ActionBlockedError("Exact Open Partner control not observed")
    table = session.find(RESULT_TABLE_ID)
    if str(getattr(table, "Id", "")) != RESULT_TABLE_ID or str(getattr(table, "Type", "")) != "GuiShell":
        raise ActionBlockedError("Live BP result table mismatch")
    table.SetCurrentCell(0, "PARTNER")
    button = session.find(OPEN_PARTNER_ID)
    if str(getattr(button, "Id", "")) != OPEN_PARTNER_ID or str(getattr(button, "Type", "")) != "GuiButton":
        raise ActionBlockedError("Live Open Partner control mismatch")
    session.audit("OPEN_S4600_T_S50A01_BP", control_id=OPEN_PARTNER_ID, value={"bp": BP})
    button.press()
    session.validate_identity()
    return inspect_screen(session)


def confirm_open_exact_partner(session: Any) -> dict[str, Any]:
    """Enter only 1000000116 in the observed Open Partners dialog."""
    session.validate_identity()
    snapshot = inspect_screen(session)
    popups = snapshot.get("popups") or []
    if (
        snapshot.get("transaction") != "BP"
        or snapshot.get("program") != "SAPLBUPA_DIALOG_JOEL"
        or str(snapshot.get("screen_number")) != "1600"
        or len(popups) != 1
        or popups[0].get("window_title") != "Ouvrir partenaires"
        or popups[0].get("truncated")
    ):
        raise ActionBlockedError("Exact Open Partners dialog is not active")
    popup = popups[0]
    fields = {field.get("id"): field for field in popup.get("input_fields", [])}
    field_info = fields.get(OPEN_NUMBER_ID, {})
    buttons = {button.get("id"): button for button in popup.get("buttons", [])}
    confirm_info = buttons.get(OPEN_CONFIRM_ID, {})
    if (
        field_info.get("type") != "GuiCTextField"
        or field_info.get("changeable") is not True
        or str(field_info.get("text") or "").strip()
        or confirm_info.get("type") != "GuiButton"
        or not str(confirm_info.get("tooltip") or "").startswith("Entr")
    ):
        raise ActionBlockedError("Open Partners controls do not match the observed empty dialog")
    field = session.find(OPEN_NUMBER_ID)
    field.Text = BP
    if str(field.Text).strip() != BP:
        raise ActionBlockedError("Open Partners field did not retain exact BP")
    button = session.find(OPEN_CONFIRM_ID)
    if str(getattr(button, "Id", "")) != OPEN_CONFIRM_ID or str(getattr(button, "Type", "")) != "GuiButton":
        raise ActionBlockedError("Live Open Partners confirm control mismatch")
    session.audit("CONFIRM_OPEN_S4600_T_S50A01_BP", control_id=OPEN_CONFIRM_ID, value={"bp": BP})
    button.press()
    session.validate_identity()
    return inspect_screen(session)


def _approved() -> None:
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))["mappings"].get("T-S50A01", {})
    approved_address = {
        key: approval.get("proposed_values", {}).get("address", {}).get(key)
        for key in ADDRESS
    }
    if (
        approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
        or approval.get("operation") != OPERATION
        or approval.get("existing_business_partner") != BP
        or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
        or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])
        or "TRAINING_MASTER_DATA_BP_ADDRESS" not in approval.get("approval_scopes_evidenced", [])
        or approval.get("approved_scope") != ["BP_ADDRESS"]
        or approval.get("step_authorizations", {}).get("BP_ADDRESS", {}).get("execute") is not True
        or approval.get("target_fingerprint") != FINGERPRINT
        or approved_address != ADDRESS
        or mapping.get("sap_id") != BP
        or mapping.get("status") != "LIVE_VERIFIED"
    ):
        raise ActionBlockedError("Existing BP mapping or exact T-S50A01 BP_ADDRESS approval mismatch")


def inspect_form(session: Any) -> dict[str, Any]:
    session.validate_identity()
    snapshot = inspect_screen(session)
    if (
        snapshot.get("transaction") != "BP"
        or snapshot.get("program") != "SAPLBUS_LOCATOR"
        or str(snapshot.get("screen_number")) != "3000"
        or snapshot.get("window_title") != f"Modifier Organisation : {BP}"
        or snapshot.get("popups")
        or snapshot.get("truncated")
    ):
        raise ActionBlockedError("Expected exact BP change screen for existing 1000000116")
    fields = {field.get("id"): field for field in snapshot.get("input_fields", [])}
    if str(fields.get(HEADER, {}).get("text") or "").strip() != BP:
        raise ActionBlockedError("BP header identity mismatch")
    observed: dict[str, dict[str, Any]] = {}
    for name, control_id in FIELD_IDS.items():
        field = fields.get(control_id, {})
        if field.get("type") != FIELD_TYPES[name] or field.get("changeable") is not True:
            raise ActionBlockedError(f"BP address field unavailable or not editable: {name}")
        observed[name] = {"id": control_id, "value": str(field.get("text") or "").strip()}
    if not any(
        button.get("id") == SAVE_ID
        and button.get("type") == "GuiButton"
        and button.get("text") == "Sauvegarder"
        for button in snapshot.get("buttons", [])
    ):
        raise ActionBlockedError("Exact BP Save control not observed")
    combo = session.find(FIELD_IDS["Language"])
    if str(getattr(combo, "Id", "")) != FIELD_IDS["Language"] or str(getattr(combo, "Type", "")) != "GuiComboBox":
        raise ActionBlockedError("Live BP address language combo mismatch")
    choices = _entries(combo)
    english = [
        choice for choice in choices
        if choice["key"].upper() == "EN" or choice["value"].strip().casefold() in {"english", "anglais"}
    ]
    return {
        "bp": BP,
        "fields": observed,
        "language_choices": choices,
        "english_key": english[0]["key"] if len(english) == 1 else None,
        "save_id": SAVE_ID,
    }


def save_once(session: Any, target: dict[str, str], values: dict[str, str]) -> dict[str, Any]:
    if target != TARGET or values != ADDRESS:
        raise ActionBlockedError("T-S50A01 BP address target or approved values mismatch")
    _approved()
    if ATTEMPT_PATH.exists():
        raise ActionBlockedError("Prior T-S50A01 BP address write attempt exists; reconcile before retry")
    form = inspect_form(session)
    if any(item["value"] for item in form["fields"].values()):
        raise ActionBlockedError("T-S50A01 BP address form is not blank; do not overwrite")
    language_key = form["english_key"]
    if not language_key:
        raise ActionBlockedError("English language option not deterministically observed")
    for name in ("StreetName", "PostalCode", "CityName", "Country"):
        control = session.find(FIELD_IDS[name])
        if (
            str(getattr(control, "Id", "")) != FIELD_IDS[name]
            or str(getattr(control, "Type", "")) != FIELD_TYPES[name]
            or not bool(getattr(control, "Changeable", False))
        ):
            raise ActionBlockedError(f"Live BP address field mismatch: {name}")
        control.Text = values[name]
        if str(control.Text).strip() != values[name]:
            raise ActionBlockedError(f"BP address field did not retain value: {name}")
    language = session.find(FIELD_IDS["Language"])
    language.Key = language_key
    if str(language.Key) != language_key:
        raise ActionBlockedError("BP address language selection did not retain English")
    prepared = inspect_form(session)
    if any(
        prepared["fields"][name]["value"] != values[name]
        for name in ("StreetName", "PostalCode", "CityName", "Country")
    ):
        raise ActionBlockedError("BP address form changed unexpectedly before Save")
    button = session.find(SAVE_ID)
    if (
        str(getattr(button, "Id", "")) != SAVE_ID
        or str(getattr(button, "Type", "")) != "GuiButton"
        or str(getattr(button, "Text", "")) != "Sauvegarder"
    ):
        raise ActionBlockedError("Live BP Save control mismatch")
    ATTEMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ATTEMPT_PATH.open("x", encoding="utf-8") as marker:
        json.dump({
            "operation": OPERATION,
            "logical_id": "T-S50A01",
            "sap_id": BP,
            "target_fingerprint": FINGERPRINT,
            "status": "SAVE_ATTEMPTED",
            "retry_allowed": False,
        }, marker)
    session.audit("PHASE5_OPERATION", control_id=SAVE_ID, value={"operation": OPERATION, "bp": BP})
    button.press()
    snapshot = inspect_screen(session)
    return {
        "save_attempted": True,
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "window_title": snapshot.get("window_title"),
        "status_bar": snapshot.get("status_bar"),
        "popups": snapshot.get("popups"),
    }
