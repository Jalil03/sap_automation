"""Open the ZPR0 customer/material VK13 selection screen; no data change."""

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
RADIO = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[0,0]"
CHOOSE = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_customer_material_selection_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError(f"Unexpected SAP identity: {session.identity!r}")
    open_transaction(session, "VK13")
    time.sleep(0.5)
    set_text(session, P + "/usr/ctxtRV13A-KSCHL", "ZPR0")
    session.find(P).sendVKey(0)
    time.sleep(0.6)
    radio = session.find(RADIO)
    if str(radio.Text) != "Client/article":
        raise ActionBlockedError(f"Unexpected key combination: {radio.Text!r}")
    session.audit("NAVIGATE", control_id=RADIO, value="select ZPR0 customer/material key")
    radio.select()
    session.audit("NAVIGATE", control_id=CHOOSE, value="open ZPR0 display selection")
    session.find(CHOOSE).press()
    time.sleep(0.7)
    session.validate_identity()
    screen = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "DISPLAY_ONLY_NO_SAVE",
        "condition_type": "ZPR0",
        "key_combination": "Client/article",
        "result_screen": screen,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "screen": {key: screen.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": screen.get("status_bar"),
        "inputs": screen.get("input_fields", []),
        "buttons": screen.get("buttons", []),
        "popups": screen.get("popups", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
