"""Structured, read-only snapshots of the current SAP GUI screen."""

from __future__ import annotations

import re
from typing import Any

from .session import SapGuiSession


PASSWORD_TYPES = {"GuiPasswordField"}
FIELD_TYPES = {"GuiTextField", "GuiCTextField", "GuiPasswordField", "GuiComboBox", "GuiCheckBox", "GuiRadioButton"}
LABEL_TYPES = {"GuiLabel", "GuiTextView"}
BUTTON_TYPES = {"GuiButton", "GuiMenu"}
TABLE_TYPES = {"GuiGridView", "GuiTableControl", "GuiShell"}
TREE_TYPES = {"GuiTree"}
TREE_NATIVE_METHODS = (
    "DoubleClickNode",
    "SelectNode",
    "ExpandNode",
    "CollapseNode",
    "SelectItem",
    "DoubleClickItem",
    "PressButton",
    "ClickLink",
    "GetItemType",
    "GetItemText",
    "GetItemTooltip",
    "GetItemIcon",
    "GetColumnNames",
    "GetNodeType",
    "GetNodeLevel",
    "GetParent",
    "GetParentNode",
    "GetSubNodes",
    "IsFolder",
    "IsNodeExpanded",
)
TABLE_NATIVE_METHODS = (
    "GetAbsoluteRow",
    "GetCellValue",
    "SelectRow",
    "SetCurrentCell",
)


def _get(control: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(control, name)
    except Exception:
        return default


def _child_controls(control: Any) -> list[Any]:
    children = _get(control, "Children")
    if children is None:
        return []
    try:
        return [children(index) for index in range(int(children.Count))]
    except Exception:
        return []


def _visible_records(root: Any, max_controls: int) -> tuple[list[dict[str, Any]], bool]:
    stack = [root]
    controls: list[dict[str, Any]] = []
    while stack and len(controls) < max_controls:
        control = stack.pop()
        record = _control_record(control)
        if record["visible"]:
            controls.append(record)
        stack.extend(reversed(_child_controls(control)))
    return controls, bool(stack)


def _table_visible_rows(control: Any, max_rows: int = 100) -> list[dict[str, Any]]:
    rows: dict[int, list[dict[str, Any]]] = {}
    get_cell_value = _callable_member(control, "GetCellValue")
    row_count = _get(control, "RowCount")
    columns = _collection_values(_get(control, "ColumnOrder"), 100)
    if get_cell_value is not None and isinstance(row_count, int) and columns:
        for row_index in range(min(row_count, max_rows)):
            values = []
            for column in columns:
                try:
                    value = get_cell_value(row_index, column)
                except Exception:
                    continue
                if value not in (None, ""):
                    values.append({"column": str(column), "text": str(value)})
            if values:
                rows[row_index] = values
    else:
        for record in _visible_records(control, max_controls=1000)[0]:
            match = re.search(r"\[(\d+),(\d+)\]$", record.get("id") or "")
            if match is None or not record.get("text"):
                continue
            column_index, row_index = (int(value) for value in match.groups())
            rows.setdefault(row_index, []).append(
                {"column": str(column_index), "text": record["text"]}
            )
    return [
        {"index": index, "values": rows[index]}
        for index in sorted(rows)
    ]


def _table_record(session: SapGuiSession, record: dict[str, Any]) -> dict[str, Any]:
    try:
        control = session.find(record["id"])
    except Exception:
        return record
    return {
        **record,
        "row_count": _get(control, "RowCount"),
        "column_count": _get(control, "ColumnCount"),
        "native_capabilities": [
            name for name in TABLE_NATIVE_METHODS if _callable_member(control, name) is not None
        ],
        "visible_rows": _table_visible_rows(control),
    }


def _control_record(control: Any) -> dict[str, Any]:
    control_type = str(_get(control, "Type", type(control).__name__))
    control_id = str(_get(control, "Id", ""))
    text = None if control_type in PASSWORD_TYPES else _get(control, "Text")
    return {
        "id": control_id,
        "type": control_type,
        "subtype": str(_get(control, "SubType", "") or "") or None,
        "text": str(text) if text not in (None, "") else None,
        "tooltip": str(_get(control, "Tooltip", "") or "") or None,
        "visible": bool(_get(control, "Visible", True)),
        "changeable": bool(_get(control, "Changeable", False)),
    }


def _collection_values(collection: Any, max_items: int) -> list[Any]:
    if collection is None:
        return []
    if isinstance(collection, (list, tuple)):
        return list(collection[:max_items])
    try:
        return [collection(index) for index in range(min(int(collection.Count), max_items))]
    except Exception:
        try:
            return list(collection)[:max_items]
        except Exception:
            return []


def _callable_member(control: Any, name: str) -> Any | None:
    try:
        if not hasattr(control, name):
            return None
        member = getattr(control, name)
    except Exception:
        return None
    return member if callable(member) else None


def _node_state(control: Any, key: str) -> tuple[bool | None, bool | None]:
    expanded = None
    is_expanded = _callable_member(control, "IsNodeExpanded")
    if is_expanded is not None:
        try:
            expanded = bool(is_expanded(key))
        except Exception:
            expanded = None

    selected = None
    try:
        selected_node = getattr(control, "SelectedNode")
        if selected_node is not None:
            selected = str(selected_node) == key
    except Exception:
        selected = None
    return expanded, selected


def _protected_native_value(control: Any, method_name: str, *args: Any) -> Any:
    method = _callable_member(control, method_name)
    if method is None:
        return None
    try:
        return method(*args)
    except Exception:
        return None


def _tree_node_metadata(
    control: Any,
    key: str,
    columns: list[str],
) -> dict[str, Any]:
    subnodes_value = _protected_native_value(control, "GetSubNodes", key)
    children = (
        [str(value) for value in _collection_values(subnodes_value, 500)]
        if subnodes_value is not None
        else None
    )
    node_type = _protected_native_value(control, "GetNodeType", key)
    expandable = _protected_native_value(control, "IsFolder", key)
    items = []
    for column in columns:
        item = {"column": column, "type": None, "text": None, "tooltip": None, "icon": None}
        for field, method_name in (
            ("type", "GetItemType"),
            ("text", "GetItemText"),
            ("tooltip", "GetItemTooltip"),
            ("icon", "GetItemIcon"),
        ):
            value = _protected_native_value(control, method_name, key, column)
            item[field] = str(value) if value not in (None, "") else None
        items.append(item)
    return {
        "node_type": str(node_type) if node_type not in (None, "") else None,
        "expandable": bool(expandable) if expandable is not None else None,
        "children_count": len(children) if children is not None else None,
        "children_keys": children,
        "items": items,
    }


def _observed_key_level(key: str) -> int | None:
    """Return the first numeric key token without relying on fixed spacing."""
    try:
        token = str(key).strip().split(maxsplit=1)[0]
    except (AttributeError, IndexError):
        return None
    return int(token) if token.isdecimal() else None


def _native_node_level(control: Any, key: str) -> int | None:
    """Read a node level only when the live COM object exposes the native API."""
    method = _callable_member(control, "GetNodeLevel")
    if method is None:
        return None
    try:
        value = method(key)
        return int(value) if value is not None else None
    except Exception:
        return None


def _native_parent_key(control: Any, key: str) -> tuple[str | None, str | None]:
    """Try only observable SAP tree parent APIs, returning the method used."""
    for method_name in ("GetParent", "GetParentNode"):
        method = _callable_member(control, method_name)
        if method is None:
            continue
        try:
            value = method(key)
        except Exception:
            continue
        return (str(value) if value not in (None, "") else None), method_name
    return None, None


def _enrich_node_hierarchy(control: Any, nodes: list[dict[str, Any]]) -> None:
    observed_keys = {node["key"] for node in nodes}
    stack: dict[int, str] = {}
    root_level: int | None = None
    previous_valid_level: int | None = None

    for index, node in enumerate(nodes):
        key = node["key"]
        observed_level = _observed_key_level(key)
        native_level = _native_node_level(control, key)
        level = native_level if native_level is not None else observed_level
        node.update(
            {
                "order_index": index,
                "level": level,
                "parent_key": None,
                "hierarchy_method": None,
                "hierarchy_error": None,
            }
        )

        if level is None:
            node["hierarchy_error"] = "node level is not observable from key or native API"
            continue

        if root_level is None:
            root_level = level

        if level < root_level:
            node["hierarchy_error"] = (
                f"observed level {level} is above root level {root_level}"
            )
            continue

        if previous_valid_level is not None and level > previous_valid_level + 1:
            node["hierarchy_error"] = (
                f"invalid observed level jump {previous_valid_level}->{level}"
            )
            continue

        native_parent, native_method = _native_parent_key(control, key)
        if native_method is not None:
            native_valid = (
                (level == root_level and native_parent is None)
                or (
                    level != root_level
                    and native_parent in observed_keys
                    and stack.get(level - 1) == native_parent
                )
            )
            if native_valid:
                node["parent_key"] = native_parent
                node["hierarchy_method"] = f"NATIVE_{native_method.upper()}"
            elif native_parent is not None:
                node["hierarchy_error"] = (
                    f"native {native_method} parent {native_parent!r} is inconsistent "
                    f"with observed level/order"
                )
                continue

        if node["hierarchy_method"] is None:
            if level == root_level:
                node["hierarchy_method"] = (
                    "NATIVE_LEVEL_AND_ORDER"
                    if native_level is not None
                    else "OBSERVED_KEY_LEVEL_AND_ORDER"
                )
            else:
                parent_key = stack.get(level - 1)
                if parent_key is None:
                    node["hierarchy_error"] = f"missing observed parent at level {level - 1}"
                    continue
                node["parent_key"] = parent_key
                node["hierarchy_method"] = (
                    "NATIVE_LEVEL_AND_ORDER"
                    if native_level is not None
                    else "OBSERVED_KEY_LEVEL_AND_ORDER"
                )

        for stacked_level in [value for value in stack if value > level]:
            del stack[stacked_level]
        stack[level] = key
        previous_valid_level = level


def read_tree_node_text(control: Any, key: str) -> tuple[str | None, str | None, str | None]:
    errors: list[str] = []
    get_node_text = _callable_member(control, "GetNodeTextByKey")
    if get_node_text is None:
        errors.append("GetNodeTextByKey unavailable")
    else:
        try:
            value = get_node_text(key)
            text = str(value) if value not in (None, "") else None
            if text is not None:
                return text, "GetNodeTextByKey", None
            errors.append("GetNodeTextByKey returned no text")
        except Exception as exc:
            errors.append(f"GetNodeTextByKey failed ({type(exc).__name__})")

    # Column trees may expose node labels as native item text.  Use this only
    # when both native APIs are actually exposed; never guess an item/column.
    get_column_names = _callable_member(control, "GetColumnNames")
    get_item_text = _callable_member(control, "GetItemText")
    if get_column_names is not None and get_item_text is not None:
        try:
            column_names = _collection_values(get_column_names(), 100)
        except Exception as exc:
            errors.append(f"GetColumnNames failed ({type(exc).__name__})")
        else:
            if not column_names:
                errors.append("GetColumnNames returned no columns")
            for column_name in column_names:
                try:
                    value = get_item_text(key, column_name)
                    text = str(value) if value not in (None, "") else None
                    if text is not None:
                        return text, f"GetItemText:{column_name}", None
                except Exception as exc:
                    errors.append(
                        f"GetItemText failed for observed column {column_name!r} ({type(exc).__name__})"
                    )
    else:
        errors.append("native column-tree text API unavailable")

    return None, None, "; ".join(errors)


def _tree_record(session: SapGuiSession, record: dict[str, Any], max_nodes: int = 500) -> dict[str, Any]:
    enriched = dict(record)
    enriched["nodes"] = []
    enriched["nodes_truncated"] = False
    enriched["extraction_error"] = None
    enriched["columns"] = []
    enriched["native_capabilities"] = []
    enriched["selected_node"] = None
    enriched["focused_item"] = None
    try:
        control = session.find(record["id"])
        enriched["native_capabilities"] = [
            name for name in TREE_NATIVE_METHODS if _callable_member(control, name) is not None
        ]
        get_column_names = _callable_member(control, "GetColumnNames")
        if get_column_names is not None:
            try:
                enriched["columns"] = [
                    str(value) for value in _collection_values(get_column_names(), 100)
                ]
            except Exception:
                enriched["columns"] = []
        selected_node = _get(control, "SelectedNode")
        focused_item = _get(control, "FocusedItem")
        enriched["selected_node"] = (
            str(selected_node) if selected_node not in (None, "") else None
        )
        enriched["focused_item"] = (
            str(focused_item) if focused_item not in (None, "") else None
        )
        get_all_node_keys = _callable_member(control, "GetAllNodeKeys")
        if get_all_node_keys is None:
            enriched["extraction_error"] = "GetAllNodeKeys unavailable"
            return enriched
        keys = _collection_values(get_all_node_keys(), max_nodes + 1)
        enriched["nodes_truncated"] = len(keys) > max_nodes
        for key in keys[:max_nodes]:
            key = str(key)
            text, extraction_method, extraction_error = read_tree_node_text(control, key)
            expanded, selected = _node_state(control, key)
            enriched["nodes"].append(
                {
                    "key": key,
                    "text": text,
                    "expanded": expanded,
                    "selected": selected,
                    "text_extraction_method": extraction_method,
                    "extraction_error": extraction_error,
                    **_tree_node_metadata(control, key, enriched["columns"]),
                }
            )
        _enrich_node_hierarchy(control, enriched["nodes"])
    except Exception as exc:
        enriched["extraction_error"] = f"tree extraction failed ({type(exc).__name__})"
    return enriched


def inspect_screen(session: SapGuiSession, max_controls: int = 2000) -> dict[str, Any]:
    session.audit("INSPECT")
    root = session.find("wnd[0]")
    controls, truncated = _visible_records(root, max_controls)

    def select(types: set[str]) -> list[dict[str, Any]]:
        return [record for record in controls if record["type"] in types]

    status_bar = None
    try:
        status_control = session.find("wnd[0]/sbar")
        status_bar = {
            "text": str(_get(status_control, "Text", "")),
            "message_type": str(_get(status_control, "MessageType", "")),
        }
    except Exception:
        status_bar = {"text": "", "message_type": ""}

    tables = [_table_record(session, record) for record in select(TABLE_TYPES)]

    tree_records = [
        record
        for record in controls
        if record["type"] in TREE_TYPES
        or (record["type"] == "GuiShell" and "tree" in str(record["subtype"] or "").casefold())
    ]

    popups = []
    for index in range(1, 6):
        try:
            popup_root = session.find(f"wnd[{index}]")
        except Exception:
            continue
        popup_controls, popup_truncated = _visible_records(popup_root, max_controls=500)
        popup_tables = [
            _table_record(session, record)
            for record in popup_controls
            if record["type"] in TABLE_TYPES
        ]
        popups.append(
            {
                "id": str(_get(popup_root, "Id", f"wnd[{index}]")),
                "window_title": str(_get(popup_root, "Text", "")),
                "buttons": [
                    record for record in popup_controls if record["type"] in BUTTON_TYPES
                ],
                "input_fields": [
                    record for record in popup_controls if record["type"] in FIELD_TYPES
                ],
                "labels": [
                    record for record in popup_controls if record["type"] in LABEL_TYPES
                ],
                "tables": popup_tables,
                "controls": popup_controls,
                "control_ids": [
                    record["id"] for record in popup_controls if record["id"]
                ],
                "truncated": popup_truncated,
            }
        )

    info = _get(session.raw, "Info")

    return {
        "window_title": str(_get(root, "Text", "")),
        "transaction": session.identity["transaction"],
        "program": str(_get(info, "Program", "") or "") or None,
        "screen_number": str(_get(info, "ScreenNumber", "") or "") or None,
        "status_bar": status_bar,
        "popups": popups,
        "visible_control_types": sorted({record["type"] for record in controls}),
        "tree_controls": [_tree_record(session, record) for record in tree_records],
        "input_fields": select(FIELD_TYPES),
        "labels": select(LABEL_TYPES),
        "buttons": select(BUTTON_TYPES),
        "tables": tables,
        "control_ids": [record["id"] for record in controls if record["id"]],
        "truncated": truncated,
    }
