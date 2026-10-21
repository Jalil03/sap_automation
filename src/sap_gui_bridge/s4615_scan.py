"""Bounded, read-only scans of allowlisted S4615 customizing views."""

from __future__ import annotations

import time
from typing import Any

from .errors import ActionBlockedError
from .inspection import inspect_screen


GRID_ID = "/app/con[0]/ses[0]/wnd[0]/shellcont/shell"
OVL2_ID = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0VVWTCTRL_V_TVSTZ"
KEYS = {
    "T000": ("MANDT",),
    "T001W": ("WERKS",),
    "T001K": ("BWKEY",),
    "TVKWZ": ("VKORG", "VTWEG", "WERKS"),
    "TVSWZ": ("WERKS", "VSTEL"),
    "TVST": ("VSTEL",),
    "OVL2": ("VSBED", "LADGR", "WERKS"),
}
OVL2_COLUMNS = ("VSBED", "LADGR", "WERKS", "VSTEL") + tuple(f"VSTE{i}" for i in range(1, 12)) + ("ERNAM",)
GRID_COLUMNS = {
    "T000": ("MANDT", "MWAER"),
    "T001W": ("WERKS", "BWKEY", "VSTEL", "LAND1"),
    "T001K": ("BWKEY", "BUKRS"),
    "TVKWZ": ("VKORG", "VTWEG", "WERKS"),
    "TVSWZ": ("WERKS", "VSTEL"),
    "TVST": ("VSTEL",),
}


def _view(snapshot: dict[str, Any], target: str) -> dict[str, Any]:
    expected = ("OVL2", "SAPL0VVW", "1234", OVL2_ID, "GuiTableControl") if target == "OVL2" else (
        "SE16N", "SAPLSE16N", "200", GRID_ID, "GuiShell"
    )
    transaction, program, screen, control_id, control_type = expected
    tables = [item for item in snapshot.get("tables", []) if item.get("id") == control_id]
    if (snapshot.get("transaction") != transaction or snapshot.get("program") != program
            or snapshot.get("screen_number") != screen or snapshot.get("popups")
            or snapshot.get("truncated") or len(tables) != 1
            or tables[0].get("type") != control_type):
        raise ActionBlockedError(f"S4615 {target} scan requires the exact observed display screen")
    if target != "OVL2":
        if target not in str(snapshot.get("window_title") or ""):
            raise ActionBlockedError(f"S4615 {target} scan title mismatch")
        names = [str(field.get("text") or "") for field in snapshot.get("input_fields", [])
                 if str(field.get("id") or "").endswith("/txtGD-TAB")]
        if names != [target] or tables[0].get("subtype") != "GridView":
            raise ActionBlockedError(f"S4615 {target} scan table identity mismatch")
    return tables[0]


def _normalized_row(row: dict[str, Any], target: str) -> dict[str, str]:
    values = {str(item["column"]): str(item["text"]).strip() for item in row.get("values", [])}
    if target == "OVL2":
        return {name: values[str(index)] for index, name in enumerate(OVL2_COLUMNS)
                if values.get(str(index))}
    return values


def scan_s4615_customizing(session: Any, target: str) -> dict[str, Any]:
    if target not in KEYS:
        raise ActionBlockedError("S4615 scan target is not allowlisted")
    session.audit("SCAN_S4615_CUSTOMIZING", value=target)
    initial = inspect_screen(session)
    table_record = _view(initial, target)
    control_id = OVL2_ID if target == "OVL2" else GRID_ID
    try:
        table = session.find(control_id)
        row_count = int(table.RowCount)
        visible_count = int(table.VisibleRowCount)
        if target == "OVL2":
            position = int(table.VerticalScrollbar.Position)
            maximum = int(table.VerticalScrollbar.Maximum)
        else:
            position = int(table.FirstVisibleRow)
            maximum = max(0, row_count - visible_count)
    except Exception as exc:
        raise ActionBlockedError(f"S4615 {target} scroll dimensions unavailable ({type(exc).__name__})") from exc
    if not (0 <= row_count <= 500 and 0 < visible_count <= 100 and 0 <= position <= maximum):
        raise ActionBlockedError(f"S4615 {target} scroll dimensions unsafe")

    if target != "OVL2":
        # GridView.GetCellValue uses absolute row indexes. The generic screen
        # snapshot is intentionally capped at 100 rows, even after scrolling.
        rows = []
        blank_slots = 0
        reason = None
        for index in range(row_count):
            try:
                grid = session.find(control_id)
                if str(grid.Id) != control_id or int(grid.RowCount) != row_count:
                    raise ValueError("grid identity changed")
                value = {column: str(grid.GetCellValue(index, column)).strip()
                         for column in GRID_COLUMNS[target]}
                if not any(value.values()):
                    blank_slots += 1
                    continue
                if any(not value[key] for key in KEYS[target]):
                    raise ValueError("partial mandatory key")
                rows.append({"index": index, **value})
            except Exception as exc:
                reason = f"absolute grid row {index} unreadable ({type(exc).__name__})"
                break
        complete = len(rows) + blank_slots == row_count
        return {
            "object": target,
            "result": "COMPLETE" if complete else "UNKNOWN",
            "row_count": row_count,
            "rows_read": len(rows),
            "slots_inspected": len(rows) + blank_slots,
            "blank_slots": blank_slots,
            "visited_scroll_positions": [],
            "incomplete_reason": None if complete else reason,
            "rows": rows,
            "source_table_id": table_record["id"],
        }

    observed: dict[int, dict[str, str]] = {}
    inspected_slots: set[int] = set()
    positions: list[int] = []
    reason: str | None = None
    for _ in range(50):
        try:
            table = session.find(control_id)  # COM controls are reacquired after every scroll.
            if (str(table.Id) != control_id or int(table.RowCount) != row_count
                    or int(table.VisibleRowCount) != visible_count):
                raise ValueError("table identity/dimensions changed")
            current = int(table.VerticalScrollbar.Position) if target == "OVL2" else int(table.FirstVisibleRow)
            if current in positions or not 0 <= current <= maximum:
                reason = "scroll position stalled or invalid"
                break
            positions.append(current)
            snapshot = inspect_screen(session)
            page = _view(snapshot, target)
            if target == "OVL2":
                # SAP GuiTableControl may include blank template slots in RowCount.
                # The snapshot omits blank rows, but the bounded viewport still
                # establishes that those slots were inspected.
                inspected_slots.update(range(current, min(current + visible_count, row_count)))
            for row in page.get("visible_rows", []):
                relative = int(row["index"])
                absolute = current + relative if target == "OVL2" else relative
                if not 0 <= absolute < row_count:
                    continue
                value = _normalized_row(row, target)
                if any(not value.get(key) for key in KEYS[target]):
                    continue
                if absolute in observed and observed[absolute] != value:
                    reason = f"row changed during scan at {absolute}"
                    break
                observed[absolute] = value
            if reason or len(observed) == row_count or (target == "OVL2" and len(inspected_slots) == row_count):
                break
            next_position = min(current + visible_count, maximum)
            if next_position <= current:
                reason = "scroll reached end before all rows were readable"
                break
            if target == "OVL2":
                table.VerticalScrollbar.Position = next_position
            else:
                table.FirstVisibleRow = next_position
            time.sleep(0.08)
            table = session.find(control_id)
            actual = int(table.VerticalScrollbar.Position) if target == "OVL2" else int(table.FirstVisibleRow)
            if actual <= current or actual > next_position:
                reason = f"unpredictable scroll {current}->{actual}"
                break
        except Exception as exc:
            reason = f"read-only scroll failed ({type(exc).__name__})"
            break
    complete = (len(observed) == row_count and set(observed) == set(range(row_count))) or (
        target == "OVL2" and inspected_slots == set(range(row_count))
    )
    return {
        "object": target,
        "result": "COMPLETE" if complete else "UNKNOWN",
        "row_count": row_count,
        "rows_read": len(observed),
        "slots_inspected": len(inspected_slots) if target == "OVL2" else len(observed),
        "blank_slots": len(inspected_slots - set(observed)) if target == "OVL2" else 0,
        "visited_scroll_positions": positions,
        "incomplete_reason": None if complete else reason or "not every absolute row was readable",
        "rows": [{"index": index, **observed[index]} for index in sorted(observed)],
        "source_table_id": table_record["id"],
    }
