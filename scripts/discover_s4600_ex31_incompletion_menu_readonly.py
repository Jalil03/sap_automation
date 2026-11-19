"""List current VA01 menu controls relevant to incompletion; no save."""

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_service_order_incompletion_2026-10-22.json"


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    screen = inspect_screen(session)
    entries = []
    for item in screen.get("buttons", []):
        text = str(item.get("text") or "")
        if item.get("type") == "GuiMenu" and any(word in text.lower() for word in ("manqu", "incompl", "traiter", "modifier")):
            entries.append({key: item.get(key) for key in ("id", "type", "text", "changeable")})
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "READ_ONLY_NO_SAVE",
        "screen": {key: screen.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": screen.get("status_bar"), "popups": screen.get("popups", []), "menus": entries,
        "tables": screen.get("tables", []),
        "nonempty_fields": [
            {key: item.get(key) for key in ("id", "type", "text", "changeable")}
            for item in screen.get("input_fields", []) if str(item.get("text") or "").strip()
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result["output"] = str(OUTPUT.relative_to(ROOT))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
