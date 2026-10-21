"""Non-saving MM01 preflight for the S4600 HAWA/W/PC/00 design."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import back, open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode


PREFIX = "/app/con[0]/ses[0]/wnd[0]"
MATERIAL = PREFIX + "/usr/ctxtRMMG1-MATNR"
INDUSTRY = PREFIX + "/usr/cmbRMMG1-MBRSH"
MATERIAL_TYPE = PREFIX + "/usr/cmbRMMG1-MTART"
CHANGE_NUMBER = PREFIX + "/usr/ctxtRMMG1-AENNR"
REFERENCE = PREFIX + "/usr/ctxtRMMG1_REF-MATNR"
CONTINUE = PREFIX + "/tbar[0]/btn[0]"
VIEW_WINDOW = PREFIX.replace("wnd[0]", "wnd[1]")
VIEW_TABLE = VIEW_WINDOW + "/usr/tblSAPLMGMMTC_VIEW"
VIEW_CONTINUE = VIEW_WINDOW + "/tbar[0]/btn[0]"
BASIC1_PREFIX = PREFIX + "/usr/tabsTABSPR1/tabpSP01/ssubTABFRA1:SAPLMGMM:2004/"
BASIC1_DESCRIPTION = BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/txtMAKT-MAKTX"
BASIC1_UNIT = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-MEINS"
BASIC1_DIVISION = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-SPART"


def _exact(session, control_id: str, control_type: str):
    control = session.find(control_id)
    if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != control_type:
        raise ActionBlockedError(f"MM01 control mismatch: {control_id}")
    return control


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if session.identity != {
        "system": "A4H", "client": "600", "user": "ABDELJ", "transaction": session.identity["transaction"]
    }:
        raise ActionBlockedError("Unexpected SAP identity")
    open_transaction(session, "MM01")
    time.sleep(0.8)
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != (
        "MM01", "SAPLMGMM", "60"
    ) or initial.get("popups"):
        raise ActionBlockedError("MM01 initial screen mismatch")
    for control_id in (MATERIAL, CHANGE_NUMBER, REFERENCE):
        if str(getattr(_exact(session, control_id, "GuiCTextField"), "Text", "") or "").strip():
            raise ActionBlockedError(f"MM01 field is not blank: {control_id}")
    industry = _exact(session, INDUSTRY, "GuiComboBox")
    product_type = _exact(session, MATERIAL_TYPE, "GuiComboBox")
    session.audit("SET_TEXT", control_id=INDUSTRY, value="W")
    industry.Key = "W"
    session.audit("SET_TEXT", control_id=MATERIAL_TYPE, value="HAWA")
    product_type.Key = "HAWA"
    if str(industry.Key) != "W" or str(product_type.Key) != "HAWA":
        raise ActionBlockedError("HAWA/W was not accepted by the MM01 initial controls")
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)

    view_state = inspect_screen(session)
    popups = view_state.get("popups") or []
    if len(popups) != 1 or popups[0].get("id") != VIEW_WINDOW:
        raise ActionBlockedError("MM01 view-selection popup mismatch")
    table = _exact(session, VIEW_TABLE, "GuiTableControl")
    labels = []
    for row in (0, 1):
        label_id = VIEW_TABLE + f"/txtMSICHTAUSW-DYTXT[0,{row}]"
        label = _exact(session, label_id, "GuiTextField")
        labels.append(str(label.Text))
    if labels != ["Données de base 1", "Données de base 2"]:
        raise ActionBlockedError(f"Unexpected MM01 basic view labels: {labels}")
    if any(bool(getattr(table.GetAbsoluteRow(row), "Selected", False)) for row in (0, 1)):
        raise ActionBlockedError("MM01 basic views were already selected")
    session.audit("SET_TEXT", control_id=VIEW_TABLE, value={"selected_views": labels})
    table.GetAbsoluteRow(0).Selected = True
    table.GetAbsoluteRow(1).Selected = True
    press_safe_button(session, VIEW_CONTINUE)
    time.sleep(1.0)

    basic = inspect_screen(session)
    if (basic.get("transaction"), basic.get("program"), str(basic.get("screen_number"))) != (
        "MM01", "SAPLMGMM", "4004"
    ) or basic.get("popups"):
        raise ActionBlockedError("MM01 Basic Data 1 screen mismatch")
    set_text(session, BASIC1_DESCRIPTION, "S4600 HAWA PC preflight")
    set_text(session, BASIC1_UNIT, "PC")
    set_text(session, BASIC1_DIVISION, "00")
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)
    validated = inspect_screen(session)
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in validated.get("input_fields") or []}
    expected = {
        BASIC1_DESCRIPTION: "S4600 HAWA PC preflight",
        BASIC1_UNIT: "PC",
        BASIC1_DIVISION: "00",
    }
    status = validated.get("status_bar") or {}
    if any(fields.get(key) != value for key, value in expected.items()):
        raise ActionBlockedError("MM01 did not retain the exact HAWA/W/PC/00 preflight fields")
    if str(status.get("message_type") or status.get("type") or "").upper() in {"E", "A"}:
        raise ActionBlockedError(f"MM01 rejected the staged design: {status.get('text')}")

    # Exit the unsaved transaction. PREPARE mode prevents any SAVE control.
    back(session)
    time.sleep(0.5)
    after_back = inspect_screen(session)
    result = {
        "status": "TECHNICALLY_VALID_NO_SAVE",
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "validated": {"ProductType": "HAWA", "IndustrySector": "W", "BaseUnit": "PC", "Division": "00"},
        "save_attempted": False,
        "status_bar": status,
        "post_preflight_screen": {
            "transaction": after_back.get("transaction"),
            "program": after_back.get("program"),
            "screen_number": after_back.get("screen_number"),
            "popup_count": len(after_back.get("popups") or []),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
