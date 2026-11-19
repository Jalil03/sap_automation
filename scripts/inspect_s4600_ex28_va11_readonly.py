"""Open VA11 in the authorized SAP GUI session and inspect the initial screen only."""

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
from src.sap_gui_bridge.navigation import open_transaction
from src.sap_gui_bridge.safety import SafetyMode

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va11_initial_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    if {key: session.identity[key] for key in expected} != expected:
        raise SystemExit(f"Blocked: unexpected identity {session.identity!r}")
    open_transaction(session, "VA11")
    snapshot = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "STRICT_READ_ONLY_SAP_GUI",
        "transaction": "VA11",
        "snapshot": snapshot,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "screen_number": snapshot.get("screen_number"),
        "window_title": snapshot.get("window_title"),
        "input_fields": snapshot.get("input_fields", []),
        "buttons": snapshot.get("buttons", []),
        "status_bar": snapshot.get("status_bar"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
