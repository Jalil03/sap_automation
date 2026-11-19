"""Exact VK13 lookup for the ZPR0 customer/material key; no write."""

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
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_customer_material_lookup_2026-10-22.json"
VALUES = {
    P + "/usr/ctxtF001": "FR10",
    P + "/usr/ctxtF002": "10",
    P + "/usr/ctxtF003": "1000000112",
    P + "/usr/ctxtF004-LOW": "90000133",
    P + "/usr/ctxtSEL_DATE": "22.10.2026",
}


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
    radio.select()
    session.find(CHOOSE).press()
    time.sleep(0.6)
    selection = inspect_screen(session)
    if (selection.get("transaction"), selection.get("program"), str(selection.get("screen_number"))) != ("VK13", "RV13A005", "1000"):
        raise ActionBlockedError("Unexpected ZPR0 customer/material selection screen")
    for control_id, value in VALUES.items():
        set_text(session, control_id, value)
    session.audit("NAVIGATE", control_id=P, value={"operation": "sendVKey(8) display exact ZPR0 customer/material", "values": VALUES})
    session.find(P).sendVKey(8)
    time.sleep(0.8)
    session.validate_identity()
    result = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "DISPLAY_ONLY_NO_SAVE",
        "condition_type": "ZPR0",
        "key_combination": "Client/article",
        "selection": {"sales_organization": "FR10", "distribution_channel": "10", "customer": "1000000112", "material": "90000133", "valid_on": "2026-10-22"},
        "result_screen": result,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "screen": {key: result.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": result.get("status_bar"),
        "popups": result.get("popups", []),
        "tables": result.get("tables", []),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
