"""Validate the staged Exercise 19 VA01 draft with Enter; never save."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.stage_s4600_ex19_va01 import DOCUMENT, EXPECTED
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected identity")
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VA01", "SAPMV45A", "4001") or snapshot.get("popups"):
        raise ActionBlockedError("Expected staged VA01 overview without popup")
    prefix = str(session.raw.Id)
    values = {
        control_id.replace("/app/con[0]/ses[0]", prefix, 1): value
        for control_id, value in DOCUMENT.items()
    }
    mismatches = {
        control_id: {"expected": value, "actual": str(getattr(session.find(control_id), "Text", "")).strip()}
        for control_id, value in values.items()
        if str(getattr(session.find(control_id), "Text", "")).strip() != value
    }
    if mismatches:
        raise ActionBlockedError(f"Staged values changed: {mismatches!r}")
    session.audit("NAVIGATE", control_id=prefix + "/wnd[0]", value={"operation": "sendVKey(0)", "save": False})
    session.find(prefix + "/wnd[0]").sendVKey(0)
    print(json.dumps({"status": "VALIDATION_RETURNED", "save_attempted": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
