"""Stage the approved S4600 exercise 31 ZPR0 condition in VK11; never save."""

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
from src.sap_gui_bridge.navigation import set_text
from src.sap_gui_bridge.safety import SafetyMode

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_zpr0_vk11_staged_2026-10-22.json"
TABLE = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {
    "condition_type": "ZPR0",
    "key_combination": "CUSTOMER_MATERIAL",
    "sales_organization": "FR10",
    "distribution_channel": "10",
    "customer": "1000000112",
    "material": "90000133",
    "rate": "150.00",
    "currency": "EUR",
    "pricing_unit": "1",
    "quantity_unit": "H",
    "valid_from": "2026-10-22",
    "valid_to": "2026-12-31",
}


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    actual = {key: str(session.identity.get(key, "")).upper() for key in EXPECTED}
    info = session.raw.Info
    if actual != EXPECTED or session.identity.get("transaction") != "VK11":
        raise SystemExit(f"Blocked: unexpected SAP context {session.identity!r}")
    if str(info.Program).upper() != "SAPMV13A" or str(info.ScreenNumber).lstrip("0") != "1005":
        raise SystemExit("Blocked: ZPR0 VK11 customer/material contract changed")

    fields = {
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-VKORG": "FR10",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-VTWEG": "10",
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-KUNNR": "1000000112",
        f"{TABLE}/ctxtKOMG-MATNR[0,0]": "90000133",
        f"{TABLE}/txtKONP-KBETR[2,0]": "150",
        f"{TABLE}/ctxtKONP-KONWA[3,0]": "EUR",
        f"{TABLE}/txtKONP-KPEIN[4,0]": "1",
        f"{TABLE}/ctxtKONP-KMEIN[5,0]": "H",
        f"{TABLE}/ctxtRV13A-DATAB[8,0]": "22.10.2026",
        f"{TABLE}/ctxtRV13A-DATBI[9,0]": "31.12.2026",
    }
    for control_id, value in fields.items():
        set_text(session, control_id, value)
    window = "/app/con[0]/ses[0]/wnd[0]"
    session.audit("NAVIGATE", control_id=window, value="validate staged ZPR0 without save")
    session.find(window).sendVKey(0)
    session.validate_identity()
    snapshot = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": EXPECTED,
        "mode": "PREPARE_ONLY_NO_SAVE",
        "payload": PAYLOAD,
        "screen": snapshot,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "payload": PAYLOAD,
        "screen": {
            "transaction": snapshot.get("transaction"),
            "program": snapshot.get("program"),
            "screen_number": snapshot.get("screen_number"),
            "status_bar": snapshot.get("status_bar"),
            "popups": snapshot.get("popups", []),
            "selected_fields": [f for f in snapshot.get("input_fields", []) if f.get("id") in fields],
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
