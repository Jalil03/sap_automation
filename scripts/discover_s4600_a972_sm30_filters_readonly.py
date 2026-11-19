"""Discover A972 display filters through the live-observed SM30 display route."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_a972_sm30_filter_discovery_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    open_transaction(session, "SM30")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVIEWNAME", "A972")
    radio_id = "/app/con[0]/ses[0]/wnd[0]/usr/radVIMDYNFLDS-LTD_DTA_AR"
    radio = session.find(radio_id)
    if str(radio.Text) != "Indiquer conditions":
        raise SystemExit(f"Blocked: unexpected filter radio {radio.Text!r}")
    session.audit("NAVIGATE", control_id=radio_id, value="select conditions before display")
    radio.select()
    button_id = "/app/con[0]/ses[0]/wnd[0]/usr/btnSHOW_PUSH"
    button = session.find(button_id)
    if str(button.Tooltip) != "Afficher":
        raise SystemExit(f"Blocked: unexpected display button {button.Tooltip!r}")
    session.audit("NAVIGATE", control_id=button_id, value="display A972 with conditions; read-only")
    button.press()
    session.validate_identity()
    screen = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "READ_ONLY_FILTER_DISCOVERY_NO_SAVE",
        "table": "A972",
        "result_screen": screen,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "result_screen": screen}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
