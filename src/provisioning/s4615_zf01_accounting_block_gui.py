"""One approved VOFA change: ZF01 accounting block false -> true."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen


OPERATION = "S4615_ZF01_ACCOUNTING_BLOCK"
TARGET = {"billing_type": "ZF01"}
VALUES = {"rfbfk": True, "transport": "A4HK908422"}
ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "data/provisioning/s4615/zf01_accounting_block_approval.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4615/zf01_accounting_block_checkpoint.json"
FIELD_ID = "/app/con[0]/ses[0]/wnd[0]/usr/chkV_TVFK-RFBFK"
SAVE_ID = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
KEY_ID = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART"


def _authorize() -> None:
    document = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    TrainingExecutionPolicy.from_document(document).authorize(OPERATION, TARGET, VALUES)


def _checkpoint() -> ExecutionCheckpoint:
    return ExecutionCheckpoint(CHECKPOINT_PATH, OPERATION)


def _detail(session: Any) -> dict[str, Any]:
    session.validate_identity()
    snapshot = inspect_screen(session)
    if ((snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number")))
            != ("VOFA", "SAPL081F", "101") or snapshot.get("popups")):
        raise ActionBlockedError("ZF01 accounting block requires exact VOFA detail without popup")
    fields = {field.get("id"): field for field in snapshot.get("input_fields", [])}
    if str((fields.get(KEY_ID) or {}).get("text") or "").strip() != "ZF01":
        raise ActionBlockedError("VOFA detail is not ZF01")
    observed = [button for button in snapshot.get("input_fields", [])
                if button.get("id") == FIELD_ID and button.get("type") == "GuiCheckBox"
                and button.get("text") == "Blocage comptabil." and button.get("changeable") is True]
    if len(observed) != 1:
        raise ActionBlockedError("ZF01 accounting block is not the exact editable control")
    return snapshot


def _checkbox(session: Any):
    control = session.find(FIELD_ID)
    if (str(getattr(control, "Id", "")) != FIELD_ID
            or str(getattr(control, "Type", "")) != "GuiCheckBox"
            or str(getattr(control, "Text", "")).strip() != "Blocage comptabil."
            or getattr(control, "Selected", None) not in (True, False, -1, 0, 1)):
        raise ActionBlockedError("ZF01 accounting-block live control mismatch")
    return control


def _other_controls(session: Any, snapshot: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for field in snapshot.get("input_fields", []):
        control_id = field.get("id")
        if control_id and control_id != FIELD_ID:
            values[control_id] = field.get("text")
    for button in snapshot.get("input_fields", []):
        control_id = button.get("id")
        if button.get("type") == "GuiCheckBox" and control_id != FIELD_ID:
            control = session.find(control_id)
            if (str(getattr(control, "Id", "")) != control_id
                    or str(getattr(control, "Type", "")) != "GuiCheckBox"
                    or getattr(control, "Selected", None) not in (True, False, -1, 0, 1)):
                raise ActionBlockedError("VOFA unrelated checkbox state unavailable")
            values[control_id] = bool(control.Selected)
    return values


def save_once(session: Any) -> dict[str, Any]:
    """Fresh lookup, exact toggle, one Save, then stop for transport/readback."""
    _authorize()
    checkpoint = _checkpoint()
    if checkpoint.status(OPERATION) is not None:
        raise ActionBlockedError("ZF01 accounting block already attempted; no automatic retry")
    before = _detail(session)
    field = _checkbox(session)
    if bool(field.Selected):
        checkpoint.record(OPERATION, "SKIPPED_EXISTS", detail="ZF01 RFBFK already true; no Save")
        return {"state": "EXISTS", "saved": False}
    frozen = _other_controls(session, before)
    save_observed = [button for button in before.get("buttons", [])
                     if button.get("id") == SAVE_ID and button.get("type") == "GuiButton"
                     and button.get("text") == "Sauvegarder"]
    if len(save_observed) != 1:
        raise ActionBlockedError("VOFA Save button not observed")
    save = session.find(SAVE_ID)
    if (str(getattr(save, "Id", "")) != SAVE_ID
            or str(getattr(save, "Type", "")) != "GuiButton"
            or str(getattr(save, "Text", "")) != "Sauvegarder"
            or not callable(getattr(save, "press", None))):
        raise ActionBlockedError("VOFA live Save control mismatch")
    checkpoint.before_write(OPERATION)
    try:
        session.audit("PHASE5_OPERATION", control_id=FIELD_ID,
                      value={"target": "ZF01", "field": "RFBFK", "from": False, "to": True})
        field.Selected = True
        staged = _detail(session)
        if not bool(_checkbox(session).Selected) or _other_controls(session, staged) != frozen:
            raise ActionBlockedError("VOFA unrelated value changed while staging RFBFK")
        session.audit("PHASE5_OPERATION", control_id=SAVE_ID,
                      value={"target": "ZF01", "field": "RFBFK", "step": "SAVE_ONCE"})
        save.press()
        session.validate_identity()
        after = inspect_screen(session)
    except Exception:
        checkpoint.record(OPERATION, "AMBIGUOUS", detail="Toggle or Save attempted; reconcile before any retry")
        raise
    checkpoint.record(OPERATION, "AMBIGUOUS", detail="Save sent; transport and independent readback pending")
    return {"save_attempted": True, "verified": False, "post_save": after}


def confirm_transport(session: Any) -> dict[str, Any]:
    """Continue only the previously observed V_TVFK transport popup."""
    _authorize()
    checkpoint = _checkpoint()
    if checkpoint.status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("VOFA transport requires prior Save attempt")
    if checkpoint.status("TRANSPORT_CONTINUE") is not None:
        raise ActionBlockedError("VOFA transport Continue already attempted; no automatic retry")
    session.validate_identity()
    snapshot = inspect_screen(session)
    popups = snapshot.get("popups") or []
    if (snapshot.get("transaction"), snapshot.get("program")) != ("VOFA", "SAPLSTRD") or len(popups) != 1:
        raise ActionBlockedError("VOFA exact transport popup not observed")
    popup = popups[0]
    prefix = "/app/con[0]/ses[0]/wnd[1]"
    fields = {field.get("id"): str(field.get("text") or "").strip()
              for field in popup.get("input_fields", [])}
    if (popup.get("id") != prefix or popup.get("window_title") != "Demande : ordre du Customizing"
            or fields.get(prefix + "/usr/txtKO008-OBJ_NAME") != "V_TVFK"
            or fields.get(prefix + "/usr/ctxtKO008-TRKORR") != "A4HK908422"
            or fields.get(prefix + "/usr/txtKO008-AS4TEXT") != "S4615 Training Setup"):
        raise ActionBlockedError("VOFA transport target or request mismatch")
    button_id = prefix + "/tbar[0]/btn[0]"
    observed = [button for button in popup.get("buttons", []) if button.get("id") == button_id
                and button.get("type") == "GuiButton" and str(button.get("tooltip") or "").startswith("Suite")]
    if len(observed) != 1:
        raise ActionBlockedError("VOFA transport Continue button mismatch")
    button = session.find(button_id)
    if (str(getattr(button, "Id", "")) != button_id or str(getattr(button, "Type", "")) != "GuiButton"
            or not str(getattr(button, "Tooltip", "")).startswith("Suite")):
        raise ActionBlockedError("VOFA live transport Continue mismatch")
    session.audit("PHASE5_OPERATION", control_id=button_id,
                  value={"target": "ZF01", "transport": "A4HK908422"})
    checkpoint.before_write("TRANSPORT_CONTINUE")
    try:
        button.press()
        session.validate_identity()
        after = inspect_screen(session)
    except Exception:
        checkpoint.record("TRANSPORT_CONTINUE", "AMBIGUOUS", detail="Transport Continue sent; reconcile")
        raise
    checkpoint.record("TRANSPORT_CONTINUE", "VERIFIED", detail="Exact V_TVFK transport Continue sent")
    return {"transport_confirmed": "A4HK908422", "verified": False,
            "post_transport": after}


def verify_readback(session: Any) -> dict[str, Any]:
    """Caller must leave/re-enter VOFA and reopen ZF01 before invoking."""
    _authorize()
    if _checkpoint().status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("VOFA readback requires prior Save attempt")
    _detail(session)
    if not bool(_checkbox(session).Selected):
        raise ActionBlockedError("ZF01 RFBFK is not persisted true")
    _checkpoint().record(OPERATION, "VERIFIED", detail="Fresh VOFA re-entry: ZF01 RFBFK=true")
    return {"result": "CREATED_AND_VERIFIED", "billing_type": "ZF01", "RFBFK": True}
