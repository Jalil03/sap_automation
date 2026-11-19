"""Open the live-observed Extended Table Management menu entry; no data change."""

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
from src.sap_gui_bridge.safety import SafetyMode

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_extended_table_management_discovery_2026-10-22.json"
MENU_ID = "/app/con[0]/ses[0]/wnd[0]/mbar/menu[4]/menu[3]/menu[3]/menu[0]"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    menu = session.find(MENU_ID)
    observed = {"text": str(menu.Text), "type": str(menu.Type), "changeable": bool(menu.Changeable)}
    if observed["text"] != "Gestion étendue des tables" or observed["type"] != "GuiMenu":
        raise SystemExit(f"Blocked: unexpected live menu contract {observed!r}")
    session.audit("NAVIGATE", control_id=MENU_ID, value="open observed extended table management read-only route")
    menu.select()
    session.validate_identity()
    screen = inspect_screen(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "READ_ONLY_DISCOVERY_NO_SAVE",
        "observed_menu": observed,
        "result_screen": screen,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "result_screen": screen}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
