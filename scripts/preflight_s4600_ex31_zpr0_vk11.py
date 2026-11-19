"""Open the evidenced ZPR0 customer/material key in VK11 without saving."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction, set_text
from src.sap_gui_bridge.safety import SafetyMode

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_vk11_preflight_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
WINDOW = "/app/con[0]/ses[0]/wnd[0]"
RADIO = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[0,0]"
CHOOSE = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    actual = {key: str(session.identity.get(key, "")).upper() for key in EXPECTED}
    if actual != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {actual!r}")

    open_transaction(session, "VK11")
    set_text(session, WINDOW + "/usr/ctxtRV13A-KSCHL", "ZPR0")
    session.find(WINDOW).sendVKey(0)
    session.validate_identity()
    key_screen = inspect_screen(session)
    radio = session.find(RADIO)
    if str(radio.Text) != "Client/article":
        raise SystemExit(f"Blocked: unexpected first key combination {radio.Text!r}")
    session.audit("NAVIGATE", control_id=RADIO, value="select evidenced ZPR0 customer/material key")
    radio.select()
    session.audit("NAVIGATE", control_id=CHOOSE, value="open VK11 entry screen; no save")
    session.find(CHOOSE).press()
    session.validate_identity()
    entry = inspect_screen(session)

    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "PREPARE_ONLY_NO_SAVE",
        "condition_type": "ZPR0",
        "key_combination": "Client/article",
        "key_combination_screen": key_screen,
        "entry_screen": entry,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "entry": {
            "title": entry.get("window_title"),
            "transaction": entry.get("transaction"),
            "program": entry.get("program"),
            "screen_number": entry.get("screen_number"),
            "input_fields": [field for field in entry.get("input_fields", []) if field.get("changeable")],
            "tables": entry.get("tables", []),
            "status_bar": entry.get("status_bar"),
            "popups": entry.get("popups", []),
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
