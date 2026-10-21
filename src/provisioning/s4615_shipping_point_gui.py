"""Narrow OVXD inspection contract for S4615 shipping point 1010."""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Any

from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import back
from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy


TARGET = {"shipping_point": "1010"}
TABLE_ID = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLV03BTCTRL_V_TVST"
NEW_ENTRIES_ID = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"
SAVE_ID = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
KEY_ID = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVST-VSTEL"
DESCRIPTION_ID = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVST-VTEXT"
OPERATION = "S4615_SHIPPING_POINT_1010"
VALUES = {"description": "Pt expédition 1010", "transport_request": "A4HK908422"}
ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "data/provisioning/s4615/shipping_point_1010_approval.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4615/shipping_point_1010_checkpoint.json"


def lookup_from_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Prove absence only when every SAP-reported row is visible."""
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "500"
    ) or snapshot.get("popups"):
        raise ActionBlockedError("OVXD V_TVST overview context mismatch")
    tables = [table for table in snapshot.get("tables", []) if table.get("id") == TABLE_ID]
    if len(tables) != 1:
        raise ActionBlockedError("Exact OVXD V_TVST table is not unique")
    rows = tables[0].get("visible_rows") or []
    keys = [
        str(value.get("text") or "").strip()
        for row in rows for value in row.get("values", []) if str(value.get("column")) == "0"
    ]
    keys = [key for key in keys if key]
    if "1010" in keys:
        return {"state": "EXISTS", "target": TARGET}
    position_fields = [
        field for field in snapshot.get("input_fields", [])
        if field.get("id") == "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO"
    ]
    if len(position_fields) != 1:
        return {"state": "UNKNOWN", "reason": "SAP entry total is not observed"}
    match = re.search(r"\b1\s*/\s*(\d+)\b", str(position_fields[0].get("text") or ""))
    if not match or len(keys) != int(match.group(1)) or len(set(keys)) != len(keys):
        return {"state": "UNKNOWN", "reason": "Complete unique V_TVST rows are not visible"}
    return {"state": "MISSING", "target": TARGET, "sap_total_entries": len(keys)}


def inspect_new_entry_form(session: Any) -> dict[str, Any]:
    """Open the exact unsaved New Entries form; do not enter or save data."""
    session.validate_identity()
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) == (
        "OVXD", "SAPLSZA1", "201"
    ) and len(before.get("popups") or []) == 1:
        popup = before["popups"][0]
        if popup.get("id") == "/app/con[0]/ses[0]/wnd[1]" and popup.get("window_title") == "Traiter l'adresse:  1010":
            return {"target": TARGET, "saved": False, "address_popup": popup,
                    "address_field_requirements": _field_requirements(session, popup)}
        raise ActionBlockedError("Unexpected OVXD post-save popup")
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) == (
        "OVXD", "SAPLV03B", "510"
    ) and not before.get("popups"):
        return {"target": TARGET, "saved": False, "form": before,
                "field_requirements": _field_requirements(session, before)}
    lookup = lookup_from_snapshot(before)
    if lookup["state"] != "MISSING":
        raise ActionBlockedError(f"Shipping point 1010 is not confirmed missing: {lookup['state']}")
    buttons = [button for button in before.get("buttons", []) if button.get("id") == NEW_ENTRIES_ID]
    if len(buttons) != 1 or buttons[0].get("type") != "GuiButton" or not str(buttons[0].get("text") or "").startswith("Nouvelles entr"):
        raise ActionBlockedError("Exact OVXD New Entries button mismatch")
    button = session.find(NEW_ENTRIES_ID)
    if str(getattr(button, "Id", "")) != NEW_ENTRIES_ID or str(getattr(button, "Type", "")) != "GuiButton":
        raise ActionBlockedError("Live OVXD New Entries control mismatch")
    session.audit("PHASE5_OPERATION", control_id=NEW_ENTRIES_ID, control_text="Nouvelles entrées", value={"target": "1010", "step": "open unsaved form"})
    button.press()
    session.validate_identity()
    after = inspect_screen(session)
    if (after.get("transaction"), after.get("program"), str(after.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "510"
    ) or after.get("popups"):
        raise ActionBlockedError("OVXD did not open the exact unsaved New Entries form")
    return {"target": TARGET, "saved": False, "form": after,
            "field_requirements": _field_requirements(session, after)}


def _field_requirements(session: Any, snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Read native GuiTextField.Required; unknown stays unknown."""
    result = []
    for field in snapshot.get("input_fields", []):
        control_id = str(field.get("id") or "")
        if not control_id.startswith(("/app/con[0]/ses[0]/wnd[0]/usr/", "/app/con[0]/ses[0]/wnd[1]/usr/")):
            continue
        control = session.find(control_id)
        try:
            required = bool(control.Required)
        except (AttributeError, TypeError, ValueError):
            required = None
        result.append({"id": control_id, "required": required,
                       "changeable": field.get("changeable"), "value": field.get("text")})
    return result


def save_once(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """One OVXD SAVE attempt; transport and independent readback remain separate."""
    if target != TARGET or values != VALUES:
        raise ActionBlockedError("Shipping point 1010 target or approved values mismatch")
    policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
    policy.authorize(OPERATION, target, values)
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, policy.workflow_id)
    if checkpoint.status(OPERATION) is not None:
        raise ActionBlockedError("Prior shipping point SAVE checkpoint requires reconciliation")
    session.validate_identity()
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) == (
        "OVXD", "SAPLV03B", "510"
    ) and not initial.get("popups"):
        if any(str(field.get("text") or "").strip() for field in initial.get("input_fields", [])
               if field.get("id") in {KEY_ID, DESCRIPTION_ID}):
            raise ActionBlockedError("OVXD form already contains unverified input")
        back(session)
        initial = inspect_screen(session)
    lookup = lookup_from_snapshot(initial)
    if lookup["state"] != "MISSING":
        raise ActionBlockedError(f"Fresh shipping point lookup is {lookup['state']}")
    form = inspect_new_entry_form(session)["form"]
    fields = {field.get("id"): field for field in form.get("input_fields", [])}
    for control_id in (KEY_ID, DESCRIPTION_ID):
        if (fields.get(control_id) or {}).get("changeable") is not True or fields[control_id].get("text"):
            raise ActionBlockedError("OVXD target field is not blank and editable")
    if any(field.get("changeable") is True and field.get("type") in {"GuiTextField", "GuiCTextField"}
           and str(field.get("text") or "").strip() and field.get("id") not in {KEY_ID, DESCRIPTION_ID}
           for field in form.get("input_fields", [])):
        raise ActionBlockedError("OVXD form contains unapproved non-target input")
    for control_id, value in ((KEY_ID, "1010"), (DESCRIPTION_ID, VALUES["description"])):
        control = session.find(control_id)
        if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != "GuiTextField":
            raise ActionBlockedError("Live OVXD field control mismatch")
        max_length = int(getattr(control, "MaxLength", 0))
        if max_length <= 0 or len(value) > max_length:
            raise ActionBlockedError("OVXD target value exceeds unverified field length")
        session.audit("PHASE5_OPERATION", control_id=control_id, value=value)
        control.Text = value
    staged = inspect_screen(session)
    if (staged.get("transaction"), staged.get("program"), str(staged.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "510"
    ) or staged.get("popups"):
        raise ActionBlockedError("OVXD context changed while staging shipping point")
    staged_fields = {field.get("id"): field for field in staged.get("input_fields", [])}
    if (staged_fields.get(KEY_ID) or {}).get("text") != "1010" or (
        staged_fields.get(DESCRIPTION_ID) or {}
    ).get("text") != VALUES["description"]:
        raise ActionBlockedError("OVXD staged target values mismatch")
    if any(field.get("changeable") is True and field.get("type") in {"GuiTextField", "GuiCTextField"}
           and str(field.get("text") or "").strip() and field.get("id") not in {KEY_ID, DESCRIPTION_ID}
           for field in staged.get("input_fields", [])):
        raise ActionBlockedError("OVXD staged unrelated field changed")
    save = session.find(SAVE_ID)
    if str(getattr(save, "Id", "")) != SAVE_ID or str(getattr(save, "Type", "")) != "GuiButton" or str(getattr(save, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("Exact OVXD SAVE control mismatch")
    checkpoint.before_write(OPERATION)
    session.audit("PHASE5_OPERATION", control_id=SAVE_ID, value={"target": "1010", "step": "save_once"})
    try:
        save.press()
        after = inspect_screen(session)
    except Exception:
        checkpoint.record(OPERATION, "AMBIGUOUS", detail="SAVE sent; SAP outcome unknown")
        raise
    checkpoint.record(OPERATION, "AMBIGUOUS", detail="SAVE sent; transport/readback reconciliation required")
    return {"target": TARGET, "save_attempted": True, "verified": False, "post_save": after}


def cancel_empty_address_popup(session: Any) -> dict[str, Any]:
    """Cancel only the observed untouched address popup; never retry SAVE."""
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, OPERATION)
    if checkpoint.status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("Shipping address reconciliation requires prior ambiguous SAVE")
    session.validate_identity()
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != (
        "OVXD", "SAPLSZA1", "201"
    ) or len(before.get("popups") or []) != 1:
        raise ActionBlockedError("Exact OVXD shipping address popup is not active")
    popup = before["popups"][0]
    if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != "Traiter l'adresse:  1010":
        raise ActionBlockedError("Shipping address popup identity mismatch")
    sensitive_suffixes = ("-NAME1", "-STREET", "-POST_CODE1", "-CITY1", "-COUNTRY", "-REGION")
    if any(str(field.get("text") or "").strip() for field in popup.get("input_fields", [])
           if str(field.get("id") or "").endswith(sensitive_suffixes)
           and "ADDR1_DATA-" in str(field.get("id") or "")):
        raise ActionBlockedError("Shipping address popup contains entered address data")
    button_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[12]"
    observed = [button for button in popup.get("buttons", []) if button.get("id") == button_id]
    if not any(button.get("type") == "GuiButton" and str(button.get("tooltip") or "").startswith("Annuler") for button in observed):
        raise ActionBlockedError("Exact address Cancel button not evidenced")
    button = session.find(button_id)
    if str(getattr(button, "Id", "")) != button_id or str(getattr(button, "Type", "")) != "GuiButton" or not str(getattr(button, "Tooltip", "")).startswith("Annuler"):
        raise ActionBlockedError("Live address Cancel button mismatch")
    session.audit("PHASE5_OPERATION", control_id=button_id, value={"target": "1010", "step": "cancel_empty_address"})
    button.press()
    after = inspect_screen(session)
    return {"target": TARGET, "address_popup_cancelled": True, "verified": False, "post_cancel": after}


def confirm_discard_address(session: Any) -> dict[str, Any]:
    """Confirm only SAP's exact discard-address dialog; no SAVE or retry."""
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, OPERATION)
    if checkpoint.status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("Address discard requires prior ambiguous SAVE")
    session.validate_identity()
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != (
        "OVXD", "SAPLSPO1", "200"
    ) or len(before.get("popups") or []) != 2:
        raise ActionBlockedError("Exact OVXD address-discard confirmation is not active")
    address, confirm = before["popups"]
    if (address.get("id"), address.get("window_title"), confirm.get("id"), confirm.get("window_title")) != (
        "/app/con[0]/ses[0]/wnd[1]", "Traiter l'adresse:  1010",
        "/app/con[0]/ses[0]/wnd[2]", "Interrompre gestion des adresses"
    ):
        raise ActionBlockedError("Address-discard window identity mismatch")
    if not any("seront perdues" in str(field.get("text") or "") for field in confirm.get("input_fields", [])):
        raise ActionBlockedError("SAP does not confirm address data will be discarded")
    if any(str(field.get("text") or "").strip() for field in address.get("input_fields", [])
           if "ADDR1_DATA-" in str(field.get("id") or "")
           and str(field.get("id") or "").endswith(("-NAME1", "-STREET", "-POST_CODE1", "-CITY1", "-COUNTRY", "-REGION"))):
        raise ActionBlockedError("Address data is no longer empty")
    button_id = "/app/con[0]/ses[0]/wnd[2]/usr/btnSPOP-OPTION1"
    buttons = [button for button in confirm.get("buttons", []) if button.get("id") == button_id]
    if len(buttons) != 1 or buttons[0].get("text") != "Oui" or buttons[0].get("type") != "GuiButton":
        raise ActionBlockedError("Exact address-discard Yes control mismatch")
    button = session.find(button_id)
    if str(getattr(button, "Id", "")) != button_id or str(getattr(button, "Type", "")) != "GuiButton" or str(getattr(button, "Text", "")) != "Oui":
        raise ActionBlockedError("Live address-discard Yes button mismatch")
    session.audit("PHASE5_OPERATION", control_id=button_id, value={"target": "1010", "step": "discard_empty_address"})
    button.press()
    after = inspect_screen(session)
    return {"target": TARGET, "address_discard_confirmed": True, "verified": False, "post_discard": after}
