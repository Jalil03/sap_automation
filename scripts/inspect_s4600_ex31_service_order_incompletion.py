"""Return from the incomplete-save popup and inspect the VA01 incompletion log; never save."""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
MODIFY = "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-VAROPTION2"
MENU = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[12]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_service_order_incompletion_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected identity")
    before = inspect_screen(session)
    popups = before.get("popups") or []
    if len(popups) != 1 or popups[0].get("window_title") != "Sauvegarder document incomplet":
        raise ActionBlockedError("Expected the incomplete-document popup")
    button = session.find(MODIFY)
    if str(getattr(button, "Text", "")) != "Modifier":
        raise ActionBlockedError("Unexpected popup button")
    session.audit("NAVIGATE", control_id=MODIFY, value="return to document without save")
    button.press()
    time.sleep(0.8)
    overview = inspect_screen(session)
    if overview.get("transaction") != "VA01" or overview.get("popups"):
        raise ActionBlockedError("Did not return to VA01 overview")
    menu = session.find(MENU)
    menu_text = str(getattr(menu, "Text", ""))
    if str(getattr(menu, "Type", "")) != "GuiMenu" or "manquant" not in menu_text.lower():
        raise ActionBlockedError(f"Unexpected incompletion menu {menu_text!r}")
    session.audit("NAVIGATE", control_id=MENU, value="open incompletion log without save")
    menu.Select()
    time.sleep(1.0)
    log = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "READ_ONLY_NO_SAVE",
        "save_attempted_before_inspection": True,
        "popup_choice": "MODIFY_NO_SAVE",
        "save_completed": False,
        "incompletion_log": log,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "screen": {key: log.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": log.get("status_bar"),
        "popups": log.get("popups", []),
        "tables": log.get("tables", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
