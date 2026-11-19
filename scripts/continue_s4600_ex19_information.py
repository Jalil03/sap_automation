"""Dismiss only the known VA01 billing-date information popup; never save."""

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
from src.sap_gui_bridge.navigation import press_safe_button
from src.sap_gui_bridge.safety import SafetyMode


EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
BUTTON_SUFFIX = "/wnd[1]/tbar[0]/btn[0]"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected identity")
    before = inspect_screen(session)
    popups = before.get("popups") or []
    if before.get("transaction") != "VA01" or len(popups) != 1:
        raise ActionBlockedError("Expected exactly one VA01 popup")
    popup = popups[0]
    text = " ".join(str(field.get("text") or "") for field in popup.get("input_fields") or [])
    if popup.get("window_title") != "Information" or "facture" not in text.lower():
        raise ActionBlockedError(f"Unexpected popup: {popup.get('window_title')!r} {text!r}")
    press_safe_button(session, str(session.raw.Id) + BUTTON_SUFFIX)
    time.sleep(1.2)
    after = inspect_screen(session)
    print(json.dumps({
        "screen": {key: after.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": after.get("status_bar"),
        "popups": after.get("popups", []),
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
