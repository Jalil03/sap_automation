"""Stage the approved S4600 exercise 31 PR00 condition in VK11; never save."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_pr00_vk11_staged_2026-10-22.json"
TABLE = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY"

PAYLOAD = {
    "condition_type": "PR00",
    "customer": "1000000112",
    "material": "90000133",
    "plant": "FR10",
    "rate": "150.00",
    "currency": "EUR",
    "pricing_unit": "1",
    "quantity_unit": "H",
    "valid_from": "2026-10-22",
    "valid_to": "2026-12-31",
}


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    actual = {key: str(session.identity.get(key, "")).upper() for key in expected}
    if actual != expected or session.identity.get("transaction") != "VK11":
        raise SystemExit(f"Blocked: unexpected SAP context {session.identity!r}")
    info = session.raw.Info
    if str(info.Program).upper() != "SAPMV13A" or str(info.ScreenNumber).lstrip("0") != "1972":
        raise SystemExit("Blocked: VK11 quick-entry contract changed")

    fields = {
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-KUNNR": PAYLOAD["customer"],
        "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-MATNR": PAYLOAD["material"],
        f"{TABLE}/ctxtKOMG-WERKS[0,0]": PAYLOAD["plant"],
        f"{TABLE}/txtKONP-KBETR[4,0]": "150",
        f"{TABLE}/ctxtKONP-KONWA[5,0]": PAYLOAD["currency"],
        f"{TABLE}/txtKONP-KPEIN[6,0]": PAYLOAD["pricing_unit"],
        f"{TABLE}/ctxtKONP-KMEIN[7,0]": PAYLOAD["quantity_unit"],
        f"{TABLE}/ctxtRV13A-DATAB[10,0]": "22.10.2026",
        f"{TABLE}/ctxtRV13A-DATBI[11,0]": "31.12.2026",
    }
    for control_id, value in fields.items():
        set_text(session, control_id, value)

    window = "/app/con[0]/ses[0]/wnd[0]"
    session.audit("NAVIGATE", control_id=window, value="validate staged PR00 without save")
    session.find(window).sendVKey(0)
    session.validate_identity()
    snapshot = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "PREPARE_ONLY_NO_SAVE",
        "payload": PAYLOAD,
        "screen": snapshot,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    selected = [
        field for field in snapshot.get("input_fields", [])
        if field.get("id") in fields
    ]
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "environment": expected,
        "payload": PAYLOAD,
        "screen": {
            "title": snapshot.get("window_title"),
            "transaction": snapshot.get("transaction"),
            "program": snapshot.get("program"),
            "screen_number": snapshot.get("screen_number"),
            "status_bar": snapshot.get("status_bar"),
            "popups": snapshot.get("popups"),
            "selected_fields": selected,
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
