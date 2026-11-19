"""Stage Exercise 19 in VA01 and stop before Enter/validation; never save."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.stage_s4600_ex19_va01 import CONTINUE, DOCUMENT, EXPECTED, INITIAL
import win32com.client

from src.sap_gui_bridge.connection import SapGuiInventory
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import AuditLogger, SafetyMode, SafetyPolicy
from src.sap_gui_bridge.session import SapGuiSession


def attach_first_matching_session():
    sap_gui = win32com.client.GetObject("SAPGUI")
    engine = sap_gui.GetScriptingEngine
    connections = [engine.Children(index) for index in range(int(engine.Children.Count))]
    matches = []
    total_sessions = 0
    for connection_index, connection in enumerate(connections):
        sessions = [connection.Children(index) for index in range(int(connection.Children.Count))]
        total_sessions += len(sessions)
        for session_index, raw in enumerate(sessions):
            info = raw.Info
            if (
                str(info.SystemName).upper() == "A4H" and str(info.Client) == "600"
                and str(info.User).upper() == "ABDELJ"
            ):
                matches.append((connection_index, session_index, connection, raw))
    if not matches:
        raise ActionBlockedError("No matching A4H/600/ABDELJ session")
    connection_index, session_index, connection, raw = sorted(matches, key=lambda value: (value[0], value[1]))[0]
    wrapped = SapGuiSession(
        raw, connection,
        SapGuiInventory(connections=len(connections), sessions=total_sessions),
        SafetyPolicy(SafetyMode.PREPARE, AuditLogger(Path("logs/sap_gui_bridge/actions.jsonl"))),
    )
    wrapped.validate_identity()
    wrapped.audit("ATTACH", value={"selected_connection_index": connection_index, "selected_session_index": session_index})
    return wrapped


def main() -> int:
    session = attach_first_matching_session()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected identity")
    actual_prefix = str(session.raw.Id)
    expected_prefix = "/app/con[0]/ses[0]"
    def remap(control_id: str) -> str:
        return control_id.replace(expected_prefix, actual_prefix, 1)
    initial_values = {remap(control_id): value for control_id, value in INITIAL.items()}
    document_values = {remap(control_id): value for control_id, value in DOCUMENT.items()}
    continue_id = remap(CONTINUE)

    open_transaction(session, "VA01")
    time.sleep(0.7)
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != ("VA01", "SAPMV45A", "101") or initial.get("popups"):
        raise ActionBlockedError("Unexpected VA01 initial screen")
    for control_id, value in initial_values.items():
        set_text(session, control_id, value)
    press_safe_button(session, continue_id)
    time.sleep(0.9)
    overview = inspect_screen(session)
    if (overview.get("transaction"), overview.get("program"), str(overview.get("screen_number"))) != ("VA01", "SAPMV45A", "4001") or overview.get("popups"):
        raise ActionBlockedError("Unexpected VA01 overview")
    for control_id, value in document_values.items():
        set_text(session, control_id, value)
    observed = {control_id: str(getattr(session.find(control_id), "Text", "")).strip() for control_id in document_values}
    print(json.dumps({
        "status": "STAGED_BEFORE_VALIDATION_NO_SAVE",
        "environment": EXPECTED,
        "observed": observed,
        "validation_attempted": False,
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
