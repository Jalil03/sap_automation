"""Open and inspect the VA21 incompletion log; never save or edit."""

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
from src.sap_gui_bridge.safety import SafetyMode

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
MENU = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[12]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va21_incompletion_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected SAP identity")
    before = inspect_screen(session)
    if before.get("transaction") != "VA21" or before.get("popups"):
        raise ActionBlockedError("Expected VA21 quotation overview")
    control = session.find(MENU)
    text = str(getattr(control, "Text", ""))
    if str(getattr(control, "Type", "")) != "GuiMenu" or "donn" not in text.lower() or "manquant" not in text.lower():
        raise ActionBlockedError("Unexpected incompletion menu")
    session.audit("NAVIGATE", control_id=MENU, control_text=text, value={"operation": "SELECT_INCOMPLETION_LOG"})
    control.Select()
    time.sleep(1.0)
    after = inspect_screen(session)
    evidence = {"mode": "READ_ONLY", "environment": EXPECTED, "save_attempted": False, "snapshot": after}
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "screen": {key: after.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": after.get("status_bar"), "popups": after.get("popups"),
        "tables": after.get("tables"), "input_fields": after.get("input_fields"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
