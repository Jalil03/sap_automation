"""Inspect the current authorized SAP GUI screen without navigation or changes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    snapshot = inspect_screen(session)
    print(json.dumps({
        "identity": session.identity,
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "screen_number": snapshot.get("screen_number"),
        "window_title": snapshot.get("window_title"),
        "popups": snapshot.get("popups", []),
        "input_fields": snapshot.get("input_fields", []),
        "status_bar": snapshot.get("status_bar"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
