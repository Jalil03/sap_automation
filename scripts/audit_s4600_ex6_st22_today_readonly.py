"""Read today's ST22 overview before an exercise 6 PGI; no SAP write."""

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
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction
from src.sap_gui_bridge.safety import SafetyMode

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex6_st22_today_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise SystemExit(f"Blocked: {session.identity!r}")
    open_transaction(session, "ST22")
    time.sleep(0.6)
    initial = inspect_screen(session)
    button_id = "/app/con[0]/ses[0]/wnd[0]/usr/btnTODAY"
    button = session.find(button_id)
    session.audit("PRESS_SAFE_BUTTON", control_id=button_id, value="read today's dump overview")
    button.press()
    time.sleep(0.8)
    session.validate_identity()
    overview = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "STRICT_READ_ONLY_SAP_GUI",
        "initial": initial,
        "today_overview": overview,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "initial_status": initial.get("status_bar"),
        "overview_screen": {key: overview.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": overview.get("status_bar"),
        "popups": overview.get("popups", []),
        "tables": overview.get("tables", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
