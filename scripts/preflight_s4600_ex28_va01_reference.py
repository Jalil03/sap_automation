"""Open VA01 create-with-reference dialog for quotation 20000103; no save."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode

P = "/app/con[0]/ses[0]/wnd[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va01_reference_preflight_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    if {key: session.identity[key] for key in expected} != expected:
        raise ActionBlockedError("Unexpected identity")
    open_transaction(session, "VA01"); time.sleep(0.5)
    for control_id, value in {
        P + "/usr/ctxtVBAK-AUART": "CS", P + "/usr/ctxtVBAK-VKORG": "FR10",
        P + "/usr/ctxtVBAK-VTWEG": "10", P + "/usr/ctxtVBAK-SPART": "1W",
    }.items():
        set_text(session, control_id, value)
    press_safe_button(session, P + "/tbar[1]/btn[8]"); time.sleep(0.8)
    snapshot = inspect_screen(session)
    OUTPUT.write_text(json.dumps({"mode": "PREPARE_NO_SAVE", "environment": expected, "staged": {"order_type": "CS", "sales_area": "FR10/10/1W", "reference_quotation": "20000103"}, "save_attempted": False, "snapshot": snapshot}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"screen": {key: snapshot.get(key) for key in ("transaction", "program", "screen_number", "window_title")}, "popups": snapshot.get("popups"), "status_bar": snapshot.get("status_bar")}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
