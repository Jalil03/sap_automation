"""Stage exercise-28 quotation values in the current VA21 draft; never save."""

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
P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV45A:4411"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4912/tblSAPMV45ATCTRL_U_ERF_ANGEBOT"
FIELDS = {
    BODY + "/ctxtVBAK-BNDDT": "01.11.2026",
    TABLE + "/txtRV45A-KWMENG[3,0]": "2",
}
CONTINUE = P + "/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va21_offer_staged_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected SAP identity")
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != ("VA21", "SAPMV45A", "4001") or before.get("popups"):
        raise ActionBlockedError("Expected the current VA21 quotation overview")
    for control_id, value in FIELDS.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.0)
    after = inspect_screen(session)
    if after.get("popups"):
        popup = after["popups"][0]
        texts = " ".join(str(item.get("text") or "") for item in popup.get("input_fields") or [])
        if len(after["popups"]) == 1 and popup.get("window_title") == "Information" and "facture" in texts.lower():
            press_safe_button(session, "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]")
            time.sleep(0.8)
            after = inspect_screen(session)
        else:
            raise ActionBlockedError("Unexpected popup after VA21 recalculation")
    evidence = {"mode": "PREPARE_NO_SAVE", "environment": EXPECTED, "staged": FIELDS, "save_attempted": False, "snapshot": after}
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = {item.get("id"): item.get("text") for item in after.get("input_fields") or []}
    print(json.dumps({
        "screen": {key: after.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": after.get("status_bar"), "popups": after.get("popups"),
        "validity_end": fields.get(BODY + "/ctxtVBAK-BNDDT"),
        "quantity": fields.get(TABLE + "/txtRV45A-KWMENG[3,0]"),
        "header_net_value": fields.get(P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR"),
        "item_net_value": fields.get(TABLE + "/txtVBAP-NETWR[10,0]"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
