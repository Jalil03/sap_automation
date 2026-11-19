"""Stage only evidenced exercise-28 VA11 fields and validate, without save."""

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

P = "/app/con[0]/ses[0]/wnd[0]"
INITIAL = {
    P + "/usr/ctxtVBAK-AUART": "DO",
    P + "/usr/ctxtVBAK-VKORG": "FR10",
    P + "/usr/ctxtVBAK-VTWEG": "10",
    P + "/usr/ctxtVBAK-SPART": "1W",
}
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV45A:4411"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4912/tblSAPMV45ATCTRL_U_ERF_ANGEBOT"
KNOWN = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    BODY + "/ctxtRV45A-KETDAT": "11.11.2026",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "10000283",
    TABLE + "/txtRV45A-KWMENG[3,0]": "3",
}
CONTINUE = P + "/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_va11_known_fields_2026-10-21.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    if {key: session.identity[key] for key in expected} != expected:
        raise ActionBlockedError("Unexpected SAP identity")
    open_transaction(session, "VA11")
    time.sleep(0.5)
    for control_id, value in INITIAL.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)
    overview = inspect_screen(session)
    if (overview.get("program"), str(overview.get("screen_number"))) != ("SAPMV45A", "4001"):
        raise ActionBlockedError("Unexpected VA11 overview screen")
    for control_id, value in KNOWN.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.0)
    validated = inspect_screen(session)
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in validated.get("input_fields") or []}
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "PREPARE_NO_SAVE",
        "staged": {
            "inquiry_type": "DO",
            "sales_area": "FR10/10/1W",
            "sold_to_party": "1000000112",
            "requested_delivery_date": "11.11.2026",
            "material": "10000283",
            "quantity": "3",
        },
        "intentionally_unset": {
            "binding_period_validity_end_date": "Book says end of week; exact calendar date is unresolved",
        },
        "save_attempted": False,
        "retained_known_fields": {key: fields.get(key) for key in KNOWN},
        "status_bar": validated.get("status_bar"),
        "popups": validated.get("popups", []),
        "screen": {
            "transaction": validated.get("transaction"),
            "program": validated.get("program"),
            "screen_number": validated.get("screen_number"),
            "window_title": validated.get("window_title"),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
