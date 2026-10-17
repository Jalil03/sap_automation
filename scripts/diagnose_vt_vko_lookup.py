"""Read-only live diagnostic for the V_TVKO lookup table."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode


TABLE_ID = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_TVKO"


def visible_vkorg_cells(table: Any) -> list[tuple[str, str]]:
    children = table.Children
    cells = []
    for index in range(int(children.Count)):
        cell = children(index)
        control_id = str(cell.Id)
        if "V_TVKO-VKORG[" in control_id:
            cells.append((control_id, str(getattr(cell, "Text", ""))))
    if not cells:
        raise RuntimeError("No visible VKORG cells are observable in V_TVKO")
    return cells


def print_cells(label: str, cells: list[tuple[str, str]]) -> None:
    print(label)
    for control_id, text in cells:
        print(f"  {control_id}: {text!r}")


def get_vt_vko_table(session: Any) -> Any:
    try:
        table = session.find(TABLE_ID)
    except Exception as exc:
        raise RuntimeError(f"V_TVKO table control not found: {TABLE_ID}") from exc
    table_type = str(getattr(table, "Type", ""))
    if table_type != "GuiTableControl":
        raise RuntimeError(f"Expected GuiTableControl; found {table_type!r}")
    return table


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    identity = session.identity
    info = session.raw.Info
    transaction = identity["transaction"]
    program = str(getattr(info, "Program", "") or "")
    print(f"Transaction: {transaction}")
    print(f"Program: {program}")

    if transaction.upper() != "V_TVKO":
        raise RuntimeError(f"Expected transaction V_TVKO; found {transaction!r}")
    if program.upper() != "SAPL0ORG":
        raise RuntimeError(f"Expected program SAPL0ORG; found {program!r}")

    table = get_vt_vko_table(session)
    print("Table Type: GuiTableControl")
    row_count = int(table.RowCount)
    visible_row_count = int(table.VisibleRowCount)
    scrollbar = table.VerticalScrollbar
    current_position = int(scrollbar.Position)
    maximum = int(scrollbar.Maximum)
    print(f"RowCount: {row_count}")
    print(f"VisibleRowCount: {visible_row_count}")
    print(f"VerticalScrollbar.Position: {current_position}")
    print(f"VerticalScrollbar.Maximum: {maximum}")
    print_cells("Visible VKORG cells before scrolling:", visible_vkorg_cells(table))

    scrollbar.Position = maximum

    session.validate_identity()
    updated_identity = session.identity
    updated_program = str(getattr(session.raw.Info, "Program", "") or "")
    if (
        updated_identity["transaction"].upper() != "V_TVKO"
        or updated_program.upper() != "SAPL0ORG"
    ):
        raise RuntimeError(
            "SAP screen changed unexpectedly after scrollbar movement: "
            f"{updated_identity['transaction']!r}/{updated_program!r}"
        )
    table = get_vt_vko_table(session)
    scrollbar = table.VerticalScrollbar
    print(f"VerticalScrollbar.Position after scrolling: {int(scrollbar.Position)}")
    print_cells("Visible VKORG cells after scrolling:", visible_vkorg_cells(table))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"V_TVKO diagnostic failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
