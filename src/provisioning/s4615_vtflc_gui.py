"""Exact, fail-closed GUI contract for S4615 ZF01 <- LF / TAN copy control.

This module never exposes arbitrary table maintenance. Each step is bound to
the observed VTFLC screen and the user's approved values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen


ROOT = "/app/con[0]/ses[0]/wnd[0]"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OPERATION = "S4615_VTFLC_ZF01_LF_TAN"
TARGET = {"billing_type": "ZF01", "delivery_type": "LF", "item_category": "TAN"}
HEADER = {"FKARN": "ZF01", "LFARV": "LF", "GRBED": "003",
          "ORDNR_FI": "E", "XBLNR_FI": "B"}
ITEM = {"PSTYV": "TAN", "GRBED": "004", "FKMGK": "G",
        "GRURP": "3", "PLMIN": "+", "KNPRS": "H", "PFKUR": "",
        "PRSQU": "E"}
APPROVED_VALUES = {"header": {**HEADER, "POSVO": True},
                   "item": {**ITEM, "KVPRS": "UNCHANGED"},
                   "transport": "A4HK908422"}
APPROVAL_PATH = PROJECT_ROOT / "data/provisioning/s4615/vtflc_zf01_lf_tan_approval.json"
CHECKPOINT_PATH = PROJECT_ROOT / "data/provisioning/s4615/vtflc_zf01_lf_tan_checkpoint.json"


def _authorize() -> None:
    policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
    policy.authorize(OPERATION, TARGET, APPROVED_VALUES)


def _checkpoint() -> ExecutionCheckpoint:
    return ExecutionCheckpoint(CHECKPOINT_PATH, OPERATION)


def _screen(session: Any, number: str) -> dict[str, Any]:
    session.validate_identity()
    snap = inspect_screen(session)
    if ((snap.get("transaction"), snap.get("program"), str(snap.get("screen_number")))
            != ("VTFLC", "SAPL080W", number) or snap.get("popups")):
        raise ActionBlockedError(f"VTFLC expected SAPL080W/{number} without popup")
    return snap


def _field(session: Any, suffix: str, name: str, expected: str | None = None):
    control_id = f"{ROOT}/usr/ctxtV_TVCPFL{suffix}-{name}"
    control = session.find(control_id)
    if (str(getattr(control, "Id", "")) != control_id
            or str(getattr(control, "Type", "")) != "GuiCTextField"):
        raise ActionBlockedError(f"VTFLC field {name} control mismatch")
    if expected is not None and str(getattr(control, "Text", "")).strip() != expected:
        raise ActionBlockedError(f"VTFLC field {name} value mismatch")
    return control


def _checkbox(session: Any, suffix: str, name: str):
    control_id = f"{ROOT}/usr/chkV_TVCPFL{suffix}-{name}"
    control = session.find(control_id)
    if (str(getattr(control, "Id", "")) != control_id
            or str(getattr(control, "Type", "")) != "GuiCheckBox"
            or getattr(control, "Selected", None) not in (True, False, -1, 0, 1)):
        raise ActionBlockedError(f"VTFLC checkbox {name} mismatch")
    return control


def prepare_header(session: Any) -> dict[str, Any]:
    _authorize()
    if _checkpoint().status("HEADER") is not None:
        raise ActionBlockedError("VTFLC header has a prior write checkpoint")
    _screen(session, "111")
    for name in HEADER:
        _field(session, "K", name, "")
    posvo = _checkbox(session, "K", "POSVO")
    if bool(posvo.Selected):
        raise ActionBlockedError("VTFLC new-header POSVO was not initially blank")
    for name, value in HEADER.items():
        control = _field(session, "K", name, "")
        session.audit("PHASE5_OPERATION", control_id=control.Id,
                      value={"field": name, "value": value, "saved": False})
        control.Text = value
    session.audit("PHASE5_OPERATION", control_id=posvo.Id,
                  value={"field": "POSVO", "value": True, "saved": False})
    posvo.Selected = True
    for name, value in HEADER.items():
        _field(session, "K", name, value)
    if not bool(_checkbox(session, "K", "POSVO").Selected):
        raise ActionBlockedError("VTFLC header POSVO did not retain value")
    return {"target": "ZF01<-LF", "prepared": True, "saved": False}


def prepare_item(session: Any) -> dict[str, Any]:
    _authorize()
    if _checkpoint().status("HEADER") != "VERIFIED" or _checkpoint().status("ITEM") is not None:
        raise ActionBlockedError("VTFLC item requires verified header and no prior item write")
    _screen(session, "113")
    for name, expected in (("FKARN", "ZF01"), ("LFARV", "LF")):
        _field(session, "P", name, expected)
    for name in ITEM:
        _field(session, "P", name, "")
    kvprs = _checkbox(session, "P", "KVPRS")
    original_kvprs = bool(kvprs.Selected)
    for name, value in ITEM.items():
        if value == "":
            continue
        control = _field(session, "P", name, "")
        session.audit("PHASE5_OPERATION", control_id=control.Id,
                      value={"field": name, "value": value, "saved": False})
        control.Text = value
    for name, value in ITEM.items():
        _field(session, "P", name, value)
    if bool(_checkbox(session, "P", "KVPRS").Selected) != original_kvprs:
        raise ActionBlockedError("VTFLC item KVPRS changed unexpectedly")
    return {"target": "ZF01<-LF/TAN", "prepared": True, "saved": False,
            "kvprs_unchanged": True}


def save_once(session: Any, kind: str) -> dict[str, Any]:
    _authorize()
    if kind not in {"header", "item"}:
        raise ActionBlockedError("VTFLC save kind is not allowlisted")
    checkpoint = _checkpoint()
    checkpoint_key = kind.upper()
    if checkpoint.status(checkpoint_key) is not None:
        raise ActionBlockedError("VTFLC write already attempted; reconcile before retry")
    if kind == "item" and checkpoint.status("HEADER") != "VERIFIED":
        raise ActionBlockedError("VTFLC item requires verified persisted header")
    _screen(session, "111" if kind == "header" else "113")
    suffix, fields = ("K", HEADER) if kind == "header" else ("P", ITEM)
    if kind == "item":
        for name, expected in (("FKARN", "ZF01"), ("LFARV", "LF")):
            _field(session, suffix, name, expected)
    for name, expected in fields.items():
        _field(session, suffix, name, expected)
    if kind == "header" and not bool(_checkbox(session, "K", "POSVO").Selected):
        raise ActionBlockedError("VTFLC header POSVO mismatch before save")
    _checkbox(session, "P", "KVPRS") if kind == "item" else None
    control_id = f"{ROOT}/tbar[0]/btn[11]"
    button = session.find(control_id)
    if (str(getattr(button, "Id", "")) != control_id
            or str(getattr(button, "Type", "")) != "GuiButton"
            or str(getattr(button, "Text", "")) != "Sauvegarder"
            or not callable(getattr(button, "press", None))):
        raise ActionBlockedError("VTFLC Save control does not match live evidence")
    session.audit("PHASE5_OPERATION", control_id=control_id,
                  value={"target": f"ZF01<-LF/{kind}", "step": "one_save"})
    checkpoint.before_write(checkpoint_key)
    try:
        button.press()
        session.validate_identity()
        post_save = inspect_screen(session)
    except Exception:
        checkpoint.record(checkpoint_key, "AMBIGUOUS", detail="Save sent; reconcile from SAP before retry")
        raise
    checkpoint.record(checkpoint_key, "AMBIGUOUS", detail="Save sent; transport and fresh readback pending")
    return {"target": f"ZF01<-LF/{kind}", "save_attempted": True,
            "post_save": post_save, "verified": False}


def confirm_transport(session: Any, kind: str) -> dict[str, Any]:
    """Continue only the observed V_TVCPFL popup on the approved request."""
    _authorize()
    if kind not in {"header", "item"} or _checkpoint().status(kind.upper()) != "AMBIGUOUS":
        raise ActionBlockedError("VTFLC transport requires an attempted matching Save")
    session.validate_identity()
    snap = inspect_screen(session)
    popups = snap.get("popups") or []
    if ((snap.get("transaction"), snap.get("program"), str(snap.get("screen_number")))
            != ("VTFLC", "SAPLSTRD", "300") or len(popups) != 1):
        raise ActionBlockedError("VTFLC exact Customizing transport popup not observed")
    popup = popups[0]
    fields = {f.get("id"): str(f.get("text") or "").strip()
              for f in popup.get("input_fields", [])}
    prefix = "/app/con[0]/ses[0]/wnd[1]"
    if (popup.get("id") != prefix
            or popup.get("window_title") != "Demande : ordre du Customizing"
            or fields.get(prefix + "/usr/txtKO008-OBJ_NAME") != "V_TVCPFL"
            or fields.get(prefix + "/usr/ctxtKO008-TRKORR") != "A4HK908422"
            or fields.get(prefix + "/usr/txtKO008-AS4TEXT") != "S4615 Training Setup"):
        raise ActionBlockedError("VTFLC transport object, request or description mismatch")
    button_id = prefix + "/tbar[0]/btn[0]"
    observed = [b for b in popup.get("buttons", []) if b.get("id") == button_id
                and b.get("type") == "GuiButton"
                and str(b.get("tooltip") or "").startswith("Suite")]
    if len(observed) != 1:
        raise ActionBlockedError("VTFLC transport Continue button not observed")
    button = session.find(button_id)
    if (str(getattr(button, "Id", "")) != button_id
            or str(getattr(button, "Type", "")) != "GuiButton"
            or not str(getattr(button, "Tooltip", "")).startswith("Suite")):
        raise ActionBlockedError("VTFLC live transport Continue control mismatch")
    session.audit("PHASE5_OPERATION", control_id=button_id,
                  value={"target": f"ZF01<-LF/{kind}", "transport": "A4HK908422"})
    button.press()
    session.validate_identity()
    return {"transport_confirmed": "A4HK908422", "post_transport": inspect_screen(session),
            "verified": False}


def verify_header(session: Any) -> dict[str, Any]:
    """Verify exact header fields after a caller-led fresh VTFLC re-entry."""
    _authorize()
    if _checkpoint().status("HEADER") != "AMBIGUOUS":
        raise ActionBlockedError("VTFLC header readback requires a prior Save attempt")
    _screen(session, "111")
    for name, expected in HEADER.items():
        _field(session, "K", name, expected)
    if not bool(_checkbox(session, "K", "POSVO").Selected):
        raise ActionBlockedError("VTFLC persisted POSVO is not selected")
    _checkpoint().record("HEADER", "VERIFIED", detail="Fresh VTFLC re-entry, exact header values observed")
    return {"result": "CREATED_AND_VERIFIED", "header": {**HEADER, "POSVO": True}}


def verify_item(session: Any) -> dict[str, Any]:
    """Verify the exact TAN row after caller-led fresh VTFLC re-entry."""
    _authorize()
    if (_checkpoint().status("HEADER") != "VERIFIED"
            or _checkpoint().status("ITEM") != "AMBIGUOUS"):
        raise ActionBlockedError("VTFLC item readback requires verified header and attempted item Save")
    _screen(session, "113")
    for name, expected in (("FKARN", "ZF01"), ("LFARV", "LF")):
        _field(session, "P", name, expected)
    for name, expected in ITEM.items():
        _field(session, "P", name, "003" if name == "GRURP" else expected)
    kvprs = bool(_checkbox(session, "P", "KVPRS").Selected)
    _checkpoint().record("ITEM", "VERIFIED", detail="Fresh VTFLC re-entry, exact TAN values observed")
    return {"result": "CREATED_AND_VERIFIED", "item": {**ITEM, "GRURP": "003", "KVPRS": kvprs}}
