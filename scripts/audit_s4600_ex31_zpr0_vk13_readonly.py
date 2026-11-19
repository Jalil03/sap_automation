"""Discover installed VK13 key combinations for ZPR0; no write or save."""

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
from src.sap_gui_bridge.navigation import open_transaction, set_text
from src.sap_gui_bridge.safety import SafetyMode

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
P = "/app/con[0]/ses[0]/wnd[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_vk13_keys_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError(f"Unexpected SAP identity: {session.identity!r}")
    open_transaction(session, "VK13")
    time.sleep(0.6)
    set_text(session, P + "/usr/ctxtRV13A-KSCHL", "ZPR0")
    session.audit("NAVIGATE", control_id=P, value="sendVKey(0) display ZPR0 key combinations")
    session.find(P).sendVKey(0)
    time.sleep(0.8)
    session.validate_identity()
    screen = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "DISPLAY_ONLY_NO_SAVE",
        "condition_type": "ZPR0",
        "result_screen": screen,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "screen": {key: screen.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": screen.get("status_bar"),
        "popups": screen.get("popups", []),
        "tables": screen.get("tables", []),
        "inputs": screen.get("input_fields", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
