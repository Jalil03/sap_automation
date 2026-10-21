"""Second, separately approved OVXD attempt for shipping point 1010 / BE."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
from src.provisioning.s4615_shipping_point_gui import (
    DESCRIPTION_ID, KEY_ID, SAVE_ID, TARGET, NEW_ENTRIES_ID,
    lookup_from_snapshot,
)
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen


OPERATION = "S4615_SHIPPING_POINT_1010_BE"
VALUES = {
    "description": "Pt expédition 1010",
    "address_country": "BE",
    "transport_request": "A4HK908422",
}
ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "data/provisioning/s4615/shipping_point_1010_be_approval.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4615/shipping_point_1010_be_checkpoint.json"
ADDRESS_ID = "/app/con[0]/ses[0]/wnd[1]/usr/ctxtADDR1_DATA-COUNTRY"
ADDRESS_CONTINUE_ID = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
TRANSPORT_ID = "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR"
TRANSPORT_CONTINUE_ID = ADDRESS_CONTINUE_ID
NEW_ENTRIES_MENU_ID = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[0]"
TABLE_ID = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPLV03BTCTRL_V_TVST"
DETAIL_MENU_ID = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[2]/menu[0]"
COUNTRY_DETAIL_ID = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVST-ALAND"


def _checkpoint() -> ExecutionCheckpoint:
    return ExecutionCheckpoint(CHECKPOINT_PATH, OPERATION)


def _exact_control(session: Any, control_id: str, kind: str) -> Any:
    control = session.find(control_id)
    if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != kind:
        raise ActionBlockedError(f"Exact OVXD control mismatch: {control_id}")
    return control


def _popup(snapshot: dict[str, Any], program: str, screen: str, title: str) -> dict[str, Any]:
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "OVXD", program, screen
    ) or len(snapshot.get("popups") or []) != 1:
        raise ActionBlockedError("Unexpected OVXD popup/context")
    popup = snapshot["popups"][0]
    if popup.get("id") != "/app/con[0]/ses[0]/wnd[1]" or popup.get("window_title") != title:
        raise ActionBlockedError("Unexpected OVXD popup identity")
    return popup


def _open_new_entries(session: Any, overview: dict[str, Any]) -> dict[str, Any]:
    """Use only the exact live-observed button or its OVXD menu equivalent."""
    buttons = {b.get("id"): b for b in overview.get("buttons", [])}
    candidate = buttons.get(NEW_ENTRIES_ID)
    if candidate and candidate.get("type") == "GuiButton" and str(candidate.get("text") or "").startswith("Nouvelles entr"):
        control = _exact_control(session, NEW_ENTRIES_ID, "GuiButton")
        session.audit("PHASE5_OPERATION", control_id=NEW_ENTRIES_ID, value={"step": "OPEN_NEW_ENTRIES"})
        control.press()
    else:
        candidate = buttons.get(NEW_ENTRIES_MENU_ID)
        if not candidate or candidate.get("type") != "GuiMenu" or not str(candidate.get("text") or "").startswith("Nouvelles entr"):
            raise ActionBlockedError("Exact OVXD New Entries control is not observed")
        control = _exact_control(session, NEW_ENTRIES_MENU_ID, "GuiMenu")
        if not str(getattr(control, "Text", "")).startswith("Nouvelles entr"):
            raise ActionBlockedError("Live OVXD New Entries menu mismatch")
        session.audit("PHASE5_OPERATION", control_id=NEW_ENTRIES_MENU_ID, value={"step": "OPEN_NEW_ENTRIES"})
        control.select()
    form = inspect_screen(session)
    if (form.get("transaction"), form.get("program"), str(form.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "510"
    ) or form.get("popups"):
        raise ActionBlockedError("OVXD did not open exact New Entries form")
    return form


def provision_once(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Stage exact fields and send one SAVE; later dialogs are separate phases."""
    if target != TARGET or values != VALUES:
        raise ActionBlockedError("Shipping point BE target or values mismatch")
    policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
    policy.authorize(OPERATION, target, values)
    checkpoint = _checkpoint()
    if checkpoint.status(OPERATION) is not None:
        raise ActionBlockedError("New shipping point attempt already recorded; no retry")
    session.validate_identity()
    overview = inspect_screen(session)
    lookup = lookup_from_snapshot(overview)
    if lookup["state"] != "MISSING":
        raise ActionBlockedError(f"Fresh shipping point lookup is {lookup['state']}")
    form = _open_new_entries(session, overview)
    fields = {field.get("id"): field for field in form.get("input_fields", [])}
    if any((fields.get(cid) or {}).get("changeable") is not True or
           str((fields.get(cid) or {}).get("text") or "").strip()
           for cid in (KEY_ID, DESCRIPTION_ID)):
        raise ActionBlockedError("OVXD target fields are not blank and editable")
    if any(field.get("changeable") is True and field.get("type") in {"GuiTextField", "GuiCTextField"}
           and str(field.get("text") or "").strip() and field.get("id") not in {KEY_ID, DESCRIPTION_ID}
           for field in form.get("input_fields", [])):
        raise ActionBlockedError("OVXD form contains unrelated input")
    for cid, value in ((KEY_ID, "1010"), (DESCRIPTION_ID, VALUES["description"])):
        control = _exact_control(session, cid, "GuiTextField")
        maximum = int(getattr(control, "MaxLength", 0))
        if maximum <= 0 or len(value) > maximum:
            raise ActionBlockedError("OVXD value exceeds field length")
        session.audit("PHASE5_OPERATION", control_id=cid, value=value)
        control.Text = value
    staged = inspect_screen(session)
    if (staged.get("transaction"), staged.get("program"), str(staged.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "510"
    ) or staged.get("popups"):
        raise ActionBlockedError("OVXD staged screen changed")
    staged_fields = {f.get("id"): f.get("text") for f in staged.get("input_fields", [])}
    if staged_fields.get(KEY_ID) != "1010" or staged_fields.get(DESCRIPTION_ID) != VALUES["description"]:
        raise ActionBlockedError("OVXD staged values mismatch")
    save = _exact_control(session, SAVE_ID, "GuiButton")
    if str(getattr(save, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("OVXD SAVE label mismatch")
    checkpoint.before_write(OPERATION)
    session.audit("PHASE5_OPERATION", control_id=SAVE_ID, value={"operation": OPERATION, "step": "SAVE_ONCE"})
    try:
        save.press()
        after = inspect_screen(session)
    except Exception:
        checkpoint.record(OPERATION, "AMBIGUOUS", detail="SAVE sent; inspect SAP before any further action")
        raise
    checkpoint.record(OPERATION, "AMBIGUOUS", detail="SAVE sent; address/transport and readback pending")
    _popup(after, "SAPLSZA1", "201", "Traiter l'adresse:  1010")
    return {"save_attempted": True, "verified": False, "post_save": after}


def confirm_address(session: Any) -> dict[str, Any]:
    """Enter only country BE in the already-observed address dialog."""
    if _checkpoint().status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("No pending shipping point BE SAVE")
    session.validate_identity()
    popup = _popup(inspect_screen(session), "SAPLSZA1", "201", "Traiter l'adresse:  1010")
    fields = {f.get("id"): f for f in popup.get("input_fields", [])}
    country = fields.get(ADDRESS_ID) or {}
    if country.get("type") != "GuiCTextField" or country.get("changeable") is not True:
        raise ActionBlockedError("Address country control not editable")
    if str(country.get("text") or "").strip() not in {"", "BE"}:
        raise ActionBlockedError("Unapproved country already present")
    for field in popup.get("input_fields", []):
        cid = str(field.get("id") or "")
        if "ADDR1_DATA-" in cid and cid != ADDRESS_ID and cid.endswith(
            ("-NAME1", "-STREET", "-POST_CODE1", "-CITY1", "-REGION")
        ) and str(field.get("text") or "").strip():
            raise ActionBlockedError("Unapproved address field is populated")
    control = _exact_control(session, ADDRESS_ID, "GuiCTextField")
    if str(getattr(control, "Text", "")).strip() != "BE":
        session.audit("PHASE5_OPERATION", control_id=ADDRESS_ID, value="BE")
        control.Text = "BE"
    staged = _popup(inspect_screen(session), "SAPLSZA1", "201", "Traiter l'adresse:  1010")
    if next((f.get("text") for f in staged.get("input_fields", []) if f.get("id") == ADDRESS_ID), None) != "BE":
        raise ActionBlockedError("Address country BE was not staged")
    observed = [b for b in staged.get("buttons", []) if b.get("id") == ADDRESS_CONTINUE_ID]
    if len(observed) != 1 or observed[0].get("type") != "GuiButton" or not str(observed[0].get("tooltip") or "").startswith("Reprendre"):
        raise ActionBlockedError("Address accept control mismatch")
    button = _exact_control(session, ADDRESS_CONTINUE_ID, "GuiButton")
    if not str(getattr(button, "Tooltip", "")).startswith("Reprendre"):
        raise ActionBlockedError("Live address accept control mismatch")
    session.audit("PHASE5_OPERATION", control_id=ADDRESS_CONTINUE_ID, value={"step": "ACCEPT_ADDRESS_BE"})
    button.press()
    after = inspect_screen(session)
    return {"address_country_staged": "BE", "verified": False, "post_address": after}


def confirm_transport(session: Any) -> dict[str, Any]:
    """Accept only the already-observed S4615 Customizing request."""
    if _checkpoint().status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("No pending shipping point BE SAVE")
    session.validate_identity()
    popup = _popup(inspect_screen(session), "SAPLSTRD", "300", "Demande : ordre du Customizing")
    fields = {f.get("id"): f.get("text") for f in popup.get("input_fields", [])}
    if (fields.get(TRANSPORT_ID), fields.get("/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-TRFUNCTN_L"),
        fields.get("/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT")) != (
        "A4HK908422", "Ordre du Customizing", "S4615 Training Setup"
    ):
        raise ActionBlockedError("Unapproved or invalid Customizing request")
    observed = [b for b in popup.get("buttons", []) if b.get("id") == TRANSPORT_CONTINUE_ID]
    if len(observed) != 1 or observed[0].get("type") != "GuiButton" or not str(observed[0].get("tooltip") or "").startswith("Suite"):
        raise ActionBlockedError("Transport continue control mismatch")
    button = _exact_control(session, TRANSPORT_CONTINUE_ID, "GuiButton")
    if not str(getattr(button, "Tooltip", "")).startswith("Suite"):
        raise ActionBlockedError("Live transport continue control mismatch")
    session.audit("PHASE5_OPERATION", control_id=TRANSPORT_CONTINUE_ID,
                  value={"step": "ACCEPT_EXISTING_REQUEST", "request": "A4HK908422"})
    button.press()
    after = inspect_screen(session)
    return {"transport_request": "A4HK908422", "verified": False, "post_transport": after}


def verify_readback(session: Any) -> dict[str, Any]:
    """Open fresh OVXD row 1010 and verify persisted country in detail."""
    if _checkpoint().status(OPERATION) != "AMBIGUOUS":
        raise ActionBlockedError("No pending shipping point BE write for readback")
    session.validate_identity()
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "500"
    ) or snapshot.get("popups"):
        raise ActionBlockedError("Fresh OVXD overview required")
    tables = [t for t in snapshot.get("tables", []) if t.get("id") == TABLE_ID]
    if len(tables) != 1:
        raise ActionBlockedError("Exact OVXD V_TVST table required")
    matches = []
    for row in tables[0].get("visible_rows") or []:
        values = {str(v.get("column")): str(v.get("text") or "").strip() for v in row.get("values", [])}
        if values.get("0") == "1010":
            matches.append((row.get("index"), values))
    if len(matches) != 1:
        raise ActionBlockedError("Shipping point 1010 not uniquely present in fresh OVXD overview")
    row_index, values = matches[0]
    if not re.fullmatch(r"Pt exp.dition 1010", values.get("1", "")):
        raise ActionBlockedError("Persisted shipping point description mismatch")
    menu = [b for b in snapshot.get("buttons", []) if b.get("id") == DETAIL_MENU_ID]
    if len(menu) != 1 or menu[0].get("type") != "GuiMenu" or not str(menu[0].get("text") or "").startswith("D") or not str(menu[0].get("text") or "").endswith("tail"):
        raise ActionBlockedError("Exact OVXD Detail menu not observed")
    table = _exact_control(session, TABLE_ID, "GuiTableControl")
    if not isinstance(row_index, int) or row_index < 0:
        raise ActionBlockedError("OVXD row index is not deterministic")
    table.GetAbsoluteRow(row_index).Selected = True
    menu_control = _exact_control(session, DETAIL_MENU_ID, "GuiMenu")
    if not str(getattr(menu_control, "Text", "")).endswith("tail"):
        raise ActionBlockedError("Live OVXD Detail menu mismatch")
    session.audit("PHASE5_OPERATION", control_id=DETAIL_MENU_ID, value={"step": "READ_ONLY_DETAIL_1010"})
    menu_control.select()
    detail = inspect_screen(session)
    if (detail.get("transaction"), detail.get("program"), str(detail.get("screen_number"))) != (
        "OVXD", "SAPLV03B", "510"
    ) or detail.get("popups"):
        raise ActionBlockedError("OVXD detail did not open readback row")
    fields = {f.get("id"): str(f.get("text") or "").strip() for f in detail.get("input_fields", [])}
    if fields.get(KEY_ID) != "1010" or fields.get(COUNTRY_DETAIL_ID) != "BE" or not re.fullmatch(
        r"Pt exp.dition 1010", fields.get(DESCRIPTION_ID, "")
    ):
        raise ActionBlockedError("Fresh OVXD detail does not confirm approved shipping point fields")
    _checkpoint().record(OPERATION, "VERIFIED", detail="Fresh SE16N TVST and OVXD detail: 1010, BE, approved description")
    return {"status": "CREATED_AND_VERIFIED", "shipping_point": "1010", "country": "BE",
            "description": VALUES["description"]}
