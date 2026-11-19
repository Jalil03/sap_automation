"""Dismiss the known VA11 information popup and inspect derived values, no save."""

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
from src.sap_gui_bridge.navigation import press_safe_button
from src.sap_gui_bridge.safety import SafetyMode

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va11_derived_values_2026-10-21.json"
CONTINUE = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    if {key: session.identity[key] for key in expected} != expected:
        raise ActionBlockedError("Unexpected SAP identity")
    before = inspect_screen(session)
    popups = before.get("popups") or []
    if len(popups) != 1 or popups[0].get("window_title") != "Information":
        raise ActionBlockedError("Expected exact VA11 information popup")
    texts = [str(x.get("text") or "") for x in popups[0].get("input_fields") or []]
    if not any("facture" in text.lower() for text in texts):
        raise ActionBlockedError("Unexpected information popup content")
    press_safe_button(session, CONTINUE)
    time.sleep(1.0)
    after = inspect_screen(session)
    fields = [
        item for item in after.get("input_fields") or []
        if item.get("text") not in (None, "")
    ]
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "PREPARE_NO_SAVE",
        "popup_dismissed": True,
        "save_attempted": False,
        "screen": {
            "transaction": after.get("transaction"),
            "program": after.get("program"),
            "screen_number": after.get("screen_number"),
            "window_title": after.get("window_title"),
        },
        "status_bar": after.get("status_bar"),
        "popups": after.get("popups", []),
        "non_empty_fields": fields,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
