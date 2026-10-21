"""Read the staged, unsaved S4600 HAWA/PC MM01 preflight."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode


PREFIX = "/app/con[0]/ses[0]/wnd[0]"
TAB = PREFIX + "/usr/tabsTABSPR1/tabpSP01"
BASIC1_PREFIX = TAB + "/ssubTABFRA1:SAPLMGMM:2004/"
FIELDS = {
    "Description": BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/txtMAKT-MAKTX",
    "BaseUnit": BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-MEINS",
    "Division": BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-SPART",
}


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if session.identity.get("system") != "A4H" or session.identity.get("client") != "600" or session.identity.get("user") != "ABDELJ":
        raise ActionBlockedError("Unexpected SAP identity")
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != ("MM01", "SAPLMGMM", "4004"):
        raise ActionBlockedError("Expected the staged MM01 Basic Data screen")
    tab = session.find(TAB)
    if str(getattr(tab, "Id", "")) != TAB or str(getattr(tab, "Type", "")) != "GuiTab":
        raise ActionBlockedError("Basic Data 1 tab mismatch")
    session.audit("NAVIGATE", control_id=TAB, value="select-basic-data-1-for-readback")
    tab.Select()
    values = {}
    for name, control_id in FIELDS.items():
        control = session.find(control_id)
        if str(getattr(control, "Id", "")) != control_id:
            raise ActionBlockedError(f"Field mismatch: {name}")
        values[name] = str(getattr(control, "Text", "") or "").strip()
    state = inspect_screen(session)
    status = state.get("status_bar") or {}
    print(json.dumps({
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "transaction": state.get("transaction"),
        "program": state.get("program"),
        "screen_number": state.get("screen_number"),
        "values": values,
        "status_bar": status,
        "popup_count": len(state.get("popups") or []),
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
