"""Exact, one-shot SAP GUI contract for C615-A01's first BP address.

The runner owns COM. This module never opens a session or guesses an AddressID.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen


ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "data/provisioning/s4615/C615-A01.workflow_approval.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
ATTEMPT_PATH = ROOT / "data/provisioning/s4615/C615-A01.bp_address_attempt.json"
BP = "1000000115"
TARGET = {"logical_id": "C615-A01", "sap_id": BP}
ADDRESS = {
    "StreetName": "1 Rue de la Formation S4615",
    "PostalCode": "1000",
    "CityName": "Bruxelles",
    "Country": "BE",
    "Language": "EN",
}
HEADER = (
    "/app/con[0]/ses[0]/wnd[0]/usr/"
    "subSCREEN_3000_RESIZING_AREA:SAPLBUS_LOCATOR:2000/"
    "subSCREEN_1010_RIGHT_AREA:SAPLBUPA_DIALOG_JOEL:1000/"
    "subSCREEN_1000_HEADER_AREA:SAPLBUPA_DIALOG_JOEL:1510/"
    "ctxtBUS_JOEL_MAIN-CHANGE_NUMBER"
)
ADDRESS_PREFIX = (
    "/app/con[0]/ses[0]/wnd[0]/usr/"
    "subSCREEN_3000_RESIZING_AREA:SAPLBUS_LOCATOR:2000/"
    "subSCREEN_1010_RIGHT_AREA:SAPLBUPA_DIALOG_JOEL:1000/"
    "ssubSCREEN_1000_WORKAREA_AREA:SAPLBUPA_DIALOG_JOEL:1100/"
    "ssubSCREEN_1100_MAIN_AREA:SAPLBUPA_DIALOG_JOEL:1101/"
    "tabsGS_SCREEN_1100_TABSTRIP/tabpSCREEN_1100_TAB_01/"
    "ssubSCREEN_1100_TABSTRIP_AREA:SAPLBUSS:0028/"
    "ssubGENSUB:SAPLBUSS:7016/subA05P01:SAPLBUA0:0400/"
    "subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/"
)
FIELD_IDS = {
    "StreetName": ADDRESS_PREFIX + "txtADDR1_DATA-STREET",
    "PostalCode": ADDRESS_PREFIX + "txtADDR1_DATA-POST_CODE1",
    "CityName": ADDRESS_PREFIX + "txtADDR1_DATA-CITY1",
    "Country": ADDRESS_PREFIX + "ctxtADDR1_DATA-COUNTRY",
    "Language": ADDRESS_PREFIX + "cmbADDR1_DATA-LANGU",
}
FIELD_TYPES = {
    "StreetName": "GuiTextField", "PostalCode": "GuiTextField",
    "CityName": "GuiTextField", "Country": "GuiCTextField",
    "Language": "GuiComboBox",
}
SAVE_ID = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"


def _entries(combo: Any) -> list[dict[str, str]]:
    try:
        entries = combo.Entries
        count = int(entries.Count)
        if count < 1 or count > 100:
            return []
        result = []
        for index in range(count):
            entry = entries(index) if callable(entries) else entries.Item(index)
            result.append({"key": str(entry.Key), "value": str(entry.Value)})
        return result
    except Exception:
        return []


def _approved() -> None:
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))["mappings"].get("C615-A01", {})
    if (approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("existing_business_partner") != BP
            or approval.get("approved_by") != "REQUESTING_USER_SELF_ATTESTED"
            or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])
            or "BP_ADDRESS" not in approval.get("approved_scope", [])
            or approval.get("step_authorizations", {}).get("BP_ADDRESS", {}).get("execute") is not True
            or {key: approval.get("proposed_values", {}).get("address", {}).get(key) for key in ADDRESS} != ADDRESS
            or mapping.get("sap_id") != BP or mapping.get("status") != "LIVE_VERIFIED"):
        raise ActionBlockedError("Existing BP mapping or exact BP_ADDRESS workflow approval mismatch")


def inspect_form(session: Any) -> dict[str, Any]:
    session.validate_identity()
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction") != "BP"
            or snapshot.get("program") != "SAPLBUS_LOCATOR"
            or str(snapshot.get("screen_number")) != "3000"
            or snapshot.get("window_title") != f"Modifier Organisation : {BP}"
            or snapshot.get("popups") or snapshot.get("truncated")):
        raise ActionBlockedError("Expected exact BP change screen for existing 1000000115")
    fields = {field.get("id"): field for field in snapshot.get("input_fields", [])}
    if str(fields.get(HEADER, {}).get("text") or "").strip() != BP:
        raise ActionBlockedError("BP header identity mismatch")
    observed: dict[str, dict[str, Any]] = {}
    for name, control_id in FIELD_IDS.items():
        field = fields.get(control_id, {})
        if field.get("type") != FIELD_TYPES[name] or field.get("changeable") is not True:
            raise ActionBlockedError(f"BP address field unavailable or not editable: {name}")
        observed[name] = {"id": control_id, "value": str(field.get("text") or "").strip()}
    if not any(button.get("id") == SAVE_ID and button.get("type") == "GuiButton"
               and button.get("text") == "Sauvegarder" for button in snapshot.get("buttons", [])):
        raise ActionBlockedError("Exact BP Save control not observed")
    combo = session.find(FIELD_IDS["Language"])
    if str(getattr(combo, "Id", "")) != FIELD_IDS["Language"] or str(getattr(combo, "Type", "")) != "GuiComboBox":
        raise ActionBlockedError("Live BP address language combo mismatch")
    choices = _entries(combo)
    english = [choice for choice in choices if choice["key"].upper() == "EN"
               or choice["value"].strip().casefold() in {"english", "anglais"}]
    return {"bp": BP, "fields": observed, "language_choices": choices,
            "english_key": english[0]["key"] if len(english) == 1 else None,
            "save_id": SAVE_ID}


def save_once(session: Any, target: dict[str, str], values: dict[str, str]) -> dict[str, Any]:
    if target != TARGET or values != ADDRESS:
        raise ActionBlockedError("BP address target or approved values mismatch")
    _approved()
    if ATTEMPT_PATH.exists():
        raise ActionBlockedError("Prior BP address write attempt exists; reconcile before retry")
    form = inspect_form(session)
    if any(item["value"] for item in form["fields"].values()):
        raise ActionBlockedError("BP address form is not blank; do not overwrite")
    language_key = form["english_key"]
    if not language_key:
        raise ActionBlockedError("English language option not deterministically observed")
    for name in ("StreetName", "PostalCode", "CityName", "Country"):
        control = session.find(FIELD_IDS[name])
        if (str(getattr(control, "Id", "")) != FIELD_IDS[name]
                or str(getattr(control, "Type", "")) != FIELD_TYPES[name]
                or not bool(getattr(control, "Changeable", False))):
            raise ActionBlockedError(f"Live BP address field mismatch: {name}")
        control.Text = values[name]
        if str(control.Text).strip() != values[name]:
            raise ActionBlockedError(f"BP address field did not retain value: {name}")
    language = session.find(FIELD_IDS["Language"])
    language.Key = language_key
    if str(language.Key) != language_key:
        raise ActionBlockedError("BP address language selection did not retain English")
    prepared = inspect_form(session)
    if any(prepared["fields"][name]["value"] != values[name]
           for name in ("StreetName", "PostalCode", "CityName", "Country")):
        raise ActionBlockedError("BP address form changed unexpectedly before Save")
    button = session.find(SAVE_ID)
    if str(getattr(button, "Id", "")) != SAVE_ID or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("Live BP Save control mismatch")
    ATTEMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ATTEMPT_PATH.open("x", encoding="utf-8") as marker:
        json.dump({"operation": "ENSURE_BP_STANDARD_ADDRESS", "logical_id": "C615-A01",
                   "sap_id": BP, "status": "SAVE_ATTEMPTED", "retry_allowed": False}, marker)
    session.audit("PHASE5_OPERATION", control_id=SAVE_ID, value={"operation": "ENSURE_BP_STANDARD_ADDRESS", "bp": BP})
    button.press()
    snapshot = inspect_screen(session)
    return {"save_attempted": True, "transaction": snapshot.get("transaction"),
            "program": snapshot.get("program"), "window_title": snapshot.get("window_title"),
            "status_bar": snapshot.get("status_bar"), "popups": snapshot.get("popups")}
