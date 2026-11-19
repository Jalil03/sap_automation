"""Copy quotation 20000103 into VA01 and inspect the order draft; never save."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
POPUP = "/app/con[0]/ses[0]/wnd[1]"
REFERENCE = POPUP + "/usr/tabsMYTABSTRIP/tabpRANG/ssubSUB1:SAPLV45C:0301/ctxtLV45C-VBELN"
COPY = POPUP + "/tbar[0]/btn[5]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va01_copied_reference_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected identity")
    before = inspect_screen(session)
    if before.get("transaction") != "VA01" or len(before.get("popups") or []) != 1:
        raise ActionBlockedError("Expected VA01 reference popup")
    set_text(session, REFERENCE, "20000103"); press_safe_button(session, COPY); time.sleep(1.2)
    after = inspect_screen(session)
    OUTPUT.write_text(json.dumps({"mode": "PREPARE_NO_SAVE", "environment": EXPECTED, "reference_quotation": "20000103", "save_attempted": False, "snapshot": after}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"screen": {key: after.get(key) for key in ("transaction", "program", "screen_number", "window_title")}, "popups": after.get("popups"), "status_bar": after.get("status_bar"), "tables": after.get("tables")}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
