"""Read-only VK13 reconciliation for PR00, bounded by customer and material."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_pr00_vk13_customer_plant_readback_2026-10-22.json"


def enter(session) -> None:
    window_id = "/app/con[0]/ses[0]/wnd[0]"
    session.audit("NAVIGATE", control_id=window_id, value="sendVKey(0) read-only continue")
    session.find(window_id).sendVKey(0)
    session.validate_identity()


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    open_transaction(session, "VK13")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRV13A-KSCHL", "PR00")
    enter(session)
    radio_id = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[0,0]"
    session.audit("NAVIGATE", control_id=radio_id, value="select proven customer/material/plant key")
    session.find(radio_id).select()
    choose_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
    session.audit("NAVIGATE", control_id=choose_id, value="open display-only PR00 selection")
    session.find(choose_id).press()
    session.validate_identity()
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF001", "1000000112")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF002", "90000133")
    # F003 (plant) intentionally remains blank to avoid product/plant validation;
    # the displayed result must independently prove the saved FR10 key.
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF003-LOW", "")
    window_id = "/app/con[0]/ses[0]/wnd[0]"
    session.audit(
        "NAVIGATE",
        control_id=window_id,
        value={"operation": "sendVKey(8) display condition records", "customer": "1000000112", "material": "90000133"},
    )
    session.find(window_id).sendVKey(8)
    session.validate_identity()
    screen = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "DISPLAY_ONLY_PREPARE_NO_SAVE",
        "condition_type": "PR00",
        "selection": {"customer": "1000000112", "material": "90000133", "plant": ""},
        "result_screen": screen,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "result_screen": screen}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
