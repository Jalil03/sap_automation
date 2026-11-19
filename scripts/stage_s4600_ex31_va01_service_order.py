"""Stage the S4600 exercise 31 service order in VA01; never save."""

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
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD": "8-600",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "90000133",
    TABLE + "/txtRV45A-KWMENG[3,0]": "3",
}
CONTINUE = P + "/tbar[0]/btn[0]"
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_va01_service_order_staged_2026-10-22.json"


def save_evidence(payload: dict) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError(f"Unexpected SAP identity: {session.identity!r}")

    evidence: dict[str, object] = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "PREPARE_NO_SAVE",
        "staged": {
            "order_type_gui": "CS",
            "sales_area": "FR10/10/1W",
            "sold_to_party": "1000000112",
            "customer_reference": "8-600",
            "material": "90000133",
            "quantity": "3",
            "expected_unit": "H",
            "expected_item_category": "TAD",
        },
        "intentionally_unset": {"requested_delivery_date": "not provided by the Book"},
        "save_attempted": False,
    }

    open_transaction(session, "VA01")
    time.sleep(0.6)
    initial = inspect_screen(session)
    evidence["initial_screen"] = initial
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != ("VA01", "SAPMV45A", "101"):
        evidence["status"] = "BLOCKED_UNEXPECTED_INITIAL_SCREEN"
        save_evidence(evidence)
        return 2
    if initial.get("popups"):
        evidence["status"] = "BLOCKED_INITIAL_POPUP"
        save_evidence(evidence)
        return 2

    for control_id, value in INITIAL.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(0.9)
    overview = inspect_screen(session)
    evidence["overview_before_document_values"] = overview
    if (overview.get("transaction"), overview.get("program"), str(overview.get("screen_number"))) != ("VA01", "SAPMV45A", "4001") or overview.get("popups"):
        evidence["status"] = "BLOCKED_BEFORE_DOCUMENT_ENTRY"
        save_evidence(evidence)
        return 3

    for control_id, value in DOCUMENT.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.2)
    validated = inspect_screen(session)
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in validated.get("input_fields") or []}
    evidence["validated_screen"] = validated
    evidence["observed"] = {
        "sold_to_party": fields.get(next(iter(DOCUMENT))),
        "customer_reference": fields.get(P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD"),
        "material": fields.get(TABLE + "/ctxtRV45A-MABNR[1,0]"),
        "quantity": fields.get(TABLE + "/txtRV45A-KWMENG[3,0]"),
        "unit": fields.get(TABLE + "/ctxtVBAP-VRKME[4,0]"),
        "item_category": fields.get(TABLE + "/ctxtVBAP-PSTYV[8,0]"),
        "plant": fields.get(TABLE + "/ctxtVBAP-WERKS[12,0]"),
        "condition_type": fields.get(TABLE + "/ctxtKOMV-KSCHL[14,0]"),
        "condition_rate": fields.get(TABLE + "/txtKOMV-KBETR[15,0]"),
        "item_net_value": fields.get(TABLE + "/txtVBAP-NETWR[20,0]"),
        "header_net_value": fields.get(P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR"),
    }
    status = validated.get("status_bar") or {}
    message_type = str(status.get("message_type") or status.get("type") or "").upper()
    evidence["status"] = "STAGED_WITH_SAP_ERROR" if message_type in {"E", "A"} else "STAGED_NO_SAVE"
    save_evidence(evidence)
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "status": evidence["status"],
        "screen": {key: validated.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": status,
        "popups": validated.get("popups", []),
        "observed": evidence["observed"],
        "save_attempted": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
