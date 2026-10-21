"""Leave the unsaved S4600 MM01 preflight without invoking Save."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import back, press_safe_button
from src.sap_gui_bridge.safety import SafetyMode


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    state = inspect_screen(session)
    popups = state.get("popups") or []
    if popups:
        popup = popups[0]
        buttons = {str(item.get("text") or "").strip(): item.get("id") for item in popup.get("buttons") or []}
        if popup.get("window_title") != "Retour" or buttons.get("Non") != "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-OPTION2":
            raise RuntimeError("Unexpected MM01 exit confirmation")
        press_safe_button(session, buttons["Non"])
        time.sleep(0.8)
    else:
        back(session)
        time.sleep(0.8)
    state = inspect_screen(session)
    print(json.dumps({
        "transaction": state.get("transaction"),
        "program": state.get("program"),
        "screen_number": state.get("screen_number"),
        "title": state.get("title"),
        "popups": state.get("popups") or [],
        "status_bar": state.get("status_bar") or {},
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
