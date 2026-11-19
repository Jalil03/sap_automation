"""Stage the exact VA11 initial data for S4600 exercise 28, without saving."""

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
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode

PREFIX = "/app/con[0]/ses[0]/wnd[0]"
FIELDS = {
    PREFIX + "/usr/ctxtVBAK-AUART": "DO",
    PREFIX + "/usr/ctxtVBAK-VKORG": "FR10",
    PREFIX + "/usr/ctxtVBAK-VTWEG": "10",
    PREFIX + "/usr/ctxtVBAK-SPART": "1W",
}
CONTINUE = PREFIX + "/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va11_group00_preflight_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected_identity = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    if {key: session.identity[key] for key in expected_identity} != expected_identity:
        raise ActionBlockedError(f"Unexpected SAP identity: {session.identity!r}")
    open_transaction(session, "VA11")
    time.sleep(0.6)
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != ("VA11", "SAPMV45A", "101"):
        raise ActionBlockedError("Unexpected VA11 initial screen")
    if initial.get("popups"):
        raise ActionBlockedError("Unexpected popup on VA11 initial screen")
    for control_id, value in FIELDS.items():
        control = session.find(control_id)
        if str(getattr(control, "Type", "")) != "GuiCTextField":
            raise ActionBlockedError(f"Unexpected control type: {control_id}")
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.0)
    overview = inspect_screen(session)
    status = overview.get("status_bar") or {}
    if str(status.get("message_type") or status.get("type") or "").upper() in {"E", "A"}:
        raise ActionBlockedError(f"VA11 rejected initial values: {status.get('text')}")
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected_identity,
        "mode": "PREPARE_NO_SAVE",
        "staged_initial_values": {"inquiry_type": "DO", "sales_organization": "FR10", "distribution_channel": "10", "sales_division": "1W"},
        "save_attempted": False,
        "initial": initial,
        "overview": overview,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "staged_initial_values": evidence["staged_initial_values"],
        "overview": {
            "transaction": overview.get("transaction"),
            "program": overview.get("program"),
            "screen_number": overview.get("screen_number"),
            "window_title": overview.get("window_title"),
            "status_bar": status,
            "input_fields": overview.get("input_fields", []),
            "tables": overview.get("tables", []),
            "popups": overview.get("popups", []),
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
