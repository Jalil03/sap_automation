"""Display-only lookup of V_TAUUM in A4H/600 through SM30."""

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


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_v_tauum_audit_2026-10-21.json"
TABLE_ID = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080CTCTRL_V_TAUUM"


def scan_rows(session) -> dict:
    table = session.find(TABLE_ID)
    row_count = int(table.RowCount)
    visible_count = int(table.VisibleRowCount)
    maximum = int(table.VerticalScrollbar.Maximum)
    if row_count <= 0 or row_count > 1000 or visible_count <= 0:
        raise RuntimeError("V_TAUUM table dimensions are unsafe")
    session.audit(
        "INSPECT", control_id=TABLE_ID,
        value={"operation": "full_read_only_scan", "row_count": row_count},
    )
    rows: dict[int, dict[str, str]] = {}
    positions: list[int] = []
    position = 0
    while True:
        table = session.find(TABLE_ID)
        scrollbar = table.VerticalScrollbar
        if int(scrollbar.Position) != position:
            scrollbar.Position = position
        actual = int(scrollbar.Position)
        if actual in positions:
            break
        positions.append(actual)
        for absolute in range(actual, min(actual + visible_count, row_count)):
            relative = absolute - actual
            ids = {
                "language": f"{TABLE_ID}/ctxtV_TAUUM-SPRAS[0,{relative}]",
                "source_type": f"{TABLE_ID}/ctxtV_TAUUM-AUART[1,{relative}]",
                "description": f"{TABLE_ID}/txtTVAKT-BEZEI[2,{relative}]",
                "language_type": f"{TABLE_ID}/txtV_TAUUM-AUART_SPR[3,{relative}]",
            }
            row = {key: str(getattr(session.find(control_id), "Text", "") or "").strip()
                   for key, control_id in ids.items()}
            if any(row.values()):
                rows[absolute] = row
        if actual >= maximum:
            break
        next_position = min(actual + visible_count, maximum)
        if next_position <= actual:
            break
        scrollbar.Position = next_position
        position = int(scrollbar.Position)
        if position <= actual:
            break
    return {
        "row_count": row_count,
        "rows_read": len(rows),
        "visited_scroll_positions": positions,
        "rows": [rows[index] | {"absolute_row": index} for index in sorted(rows)],
    }


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    open_transaction(session, "SM30")
    view_id = "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVIEWNAME"
    display_id = "/app/con[0]/ses[0]/wnd[0]/usr/btnSHOW_PUSH"
    set_text(session, view_id, "V_TAUUM")
    button = session.find(display_id)
    if str(getattr(button, "Text", "")).strip() != "Afficher":
        raise RuntimeError("SM30 display button contract changed")
    session.audit(
        "PRESS_SAFE_BUTTON",
        control_id=display_id,
        control_text="Afficher",
        value={"view": "V_TAUUM", "mode": "display_only"},
    )
    button.press()
    session.validate_identity()
    snapshot = inspect_screen(session)
    scan = scan_rows(session)
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "DISPLAY_ONLY_PREPARE_NO_SAVE",
        "view": "V_TAUUM",
        "snapshot": snapshot,
        "scan": scan,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "screen_number": snapshot.get("screen_number"),
        "window_title": snapshot.get("window_title"),
        "status_bar": snapshot.get("status_bar"),
        "tables": snapshot.get("tables"),
        "input_fields": snapshot.get("input_fields"),
        "popups": snapshot.get("popups"),
        "relevant_rows": [
            row for row in scan["rows"]
            if row["language"] in {"DE", "EN", "FR"}
            and ({row["source_type"], row["language_type"]} & {"CDCL", "CS", "TA", "OR"})
        ],
        "scan_summary": {key: scan[key] for key in ("row_count", "rows_read", "visited_scroll_positions")},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
