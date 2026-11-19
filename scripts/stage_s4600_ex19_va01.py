"""Stage S4600 exercise 19 header and items in VA01; never save."""

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


EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
P = "/app/con[0]/ses[0]/wnd[0]"
INITIAL = {
    P + "/usr/ctxtVBAK-AUART": "CS",
    P + "/usr/ctxtVBAK-VKORG": "FR10",
    P + "/usr/ctxtVBAK-VTWEG": "10",
    P + "/usr/ctxtVBAK-SPART": "1W",
}
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG"
DOCUMENT = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD": "6-400",
    BODY + "/ssubHEADER_FRAME:SAPMV45A:4440/ctxtRV45A-KETDAT": "29.10.2026",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "10000282",
    TABLE + "/txtRV45A-KWMENG[3,0]": "5",
    TABLE + "/ctxtRV45A-MABNR[1,1]": "10000284",
    TABLE + "/txtRV45A-KWMENG[3,1]": "1",
}
CONTINUE = P + "/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex19_va01_staged_2026-10-22.json"


def save(value: dict) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    identity = {key: session.identity[key] for key in EXPECTED}
    if identity != EXPECTED:
        raise ActionBlockedError(f"Unexpected identity: {identity!r}")
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "PREPARE_NO_SAVE",
        "operation": "STAGE_S4600_EX19_HEADER_AND_ITEMS",
        "staged": DOCUMENT,
        "item_partners_staged": False,
        "save_attempted": False,
    }
    open_transaction(session, "VA01")
    time.sleep(0.7)
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != ("VA01", "SAPMV45A", "101") or initial.get("popups"):
        evidence.update(status="BLOCKED_INITIAL_SCREEN", snapshot=initial)
        save(evidence)
        return 2
    for control_id, value in INITIAL.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(0.9)
    overview = inspect_screen(session)
    if (overview.get("transaction"), overview.get("program"), str(overview.get("screen_number"))) != ("VA01", "SAPMV45A", "4001") or overview.get("popups"):
        evidence.update(status="BLOCKED_OVERVIEW", snapshot=overview)
        save(evidence)
        return 3
    for control_id, value in DOCUMENT.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.2)
    after = inspect_screen(session)
    evidence["snapshot"] = after
    evidence["status"] = (
        "STAGED_WITH_SAP_ERROR"
        if str((after.get("status_bar") or {}).get("message_type") or "").upper() in {"E", "A"}
        else "STAGED_NO_SAVE"
    )
    save(evidence)
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "status": evidence["status"],
        "screen": {key: after.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": after.get("status_bar"),
        "popups": after.get("popups", []),
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
