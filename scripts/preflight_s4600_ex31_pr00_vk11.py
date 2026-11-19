"""Open the evidenced PR00 customer/material key in VK11 without saving."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_pr00_vk11_preflight_2026-10-22.json"


def enter(session) -> None:
    window = "/app/con[0]/ses[0]/wnd[0]"
    session.audit("NAVIGATE", control_id=window, value="continue without save")
    session.find(window).sendVKey(0)
    session.validate_identity()


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    actual = {key: str(session.identity.get(key, "")).upper() for key in expected}
    if actual != expected:
        raise SystemExit(f"Blocked: unexpected SAP identity {actual!r}")

    open_transaction(session, "VK11")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRV13A-KSCHL", "PR00")
    enter(session)
    key_screen = inspect_screen(session)
    radio_id = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[0,0]"
    choose_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
    session.audit("NAVIGATE", control_id=radio_id, value="select evidenced PR00 customer/material key")
    session.find(radio_id).select()
    session.audit("NAVIGATE", control_id=choose_id, value="open VK11 selection; no save")
    session.find(choose_id).press()
    session.validate_identity()
    selection = inspect_screen(session)

    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "PREPARE_ONLY_NO_SAVE",
        "condition_type": "PR00",
        "key_combination_screen": key_screen,
        "selection_screen": selection,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "selection": {
            "title": selection.get("window_title"),
            "transaction": selection.get("transaction"),
            "program": selection.get("program"),
            "screen_number": selection.get("screen_number"),
            "input_fields": selection.get("input_fields", []),
            "tables": selection.get("tables", []),
            "status_bar": selection.get("status_bar"),
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
