"""CLI for guarded SAP GUI status, inspection and preparation."""

from __future__ import annotations

import argparse
import json
import sys

from .connection import SapGuiConnection
from .inspection import inspect_screen
from .navigation import back, open_transaction, set_text
from .safety import SafetyMode
from .errors import SapGuiBridgeError
from .protocol import enqueue_request, wait_for_response


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m src.sap_gui_bridge")
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("inspect")
    open_cmd = sub.add_parser("open")
    open_cmd.add_argument("transaction")
    prepare = sub.add_parser("prepare")
    prepare_sub = prepare.add_subparsers(dest="prepare_action", required=True)
    set_field = prepare_sub.add_parser("set-field")
    set_field.add_argument("control_id")
    set_field.add_argument("value")
    prepare_sub.add_parser("back")
    sub.add_parser("execute")
    request = sub.add_parser("request")
    request_sub = request.add_subparsers(dest="request_action", required=True)
    request_sub.add_parser("status")
    request_sub.add_parser("inspect")
    request_sub.add_parser("inspect-bp-address")
    request_sub.add_parser("read-status-bar")
    request_sub.add_parser("read-screen")
    request_sub.add_parser("read-zf01-accounting-block")
    request_sub.add_parser("inspect-zf01-lf-new-header-form")
    request_sub.add_parser("read-f2-lf-header-options")
    request_sub.add_parser("inspect-vtflc-new-item-form")
    request_sub.add_parser("inspect-vtflc-new-target-item-form")
    request_sub.add_parser("find-zf01-lf-copy-header")
    request_sub.add_parser("display-zf01-lf-copy-header")
    request_sub.add_parser("open-billing-copy-items")
    request_sub.add_parser("display-billing-copy-tan")
    request_sub.add_parser("display-s4600-cdcl")
    request_navigate = request_sub.add_parser("navigate")
    request_navigate.add_argument("--operation", required=True)
    request_navigate.add_argument("--control-id", required=True)
    request_navigate.add_argument("--expected-type", required=True)
    request_navigate.add_argument("--expected-text")
    request_navigate.add_argument("--node-key")
    request_navigate.add_argument("--expected-transaction")
    request_navigate.add_argument("--item-column")
    request_open = request_sub.add_parser("open")
    request_open.add_argument("transaction")
    read_customizing = request_sub.add_parser("open-s4615-customizing")
    read_customizing.add_argument("transaction", choices=("SE16N", "OVL2", "OVXD"))
    inspect_customizing = request_sub.add_parser("inspect-s4615-customizing")
    inspect_customizing.add_argument("object", choices=("T001W", "T001K", "TVKWZ", "TVSWZ", "TVST", "OVL2"))
    read_table = request_sub.add_parser("read-s4615-table")
    read_table.add_argument("table", choices=("T000", "T001W", "T001K", "TVKWZ", "TVSWZ", "TVST"))
    scan_customizing = request_sub.add_parser("scan-s4615-customizing")
    scan_customizing.add_argument("object", choices=("T000", "T001W", "T001K", "TVKWZ", "TVSWZ", "TVST", "OVL2"))
    wait = sub.add_parser("wait")
    wait.add_argument("request_id")
    wait.add_argument("--timeout", type=float, default=60.0)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "request":
        if args.request_action == "status":
            action, params = "STATUS", {}
        elif args.request_action == "inspect":
            action, params = "INSPECT", {}
        elif args.request_action == "inspect-bp-address":
            action, params = "INSPECT_BP_STANDARD_ADDRESS", {}
        elif args.request_action == "read-status-bar":
            action, params = "READ_STATUS_BAR", {}
        elif args.request_action == "read-screen":
            action, params = "READ_SCREEN", {}
        elif args.request_action == "read-zf01-accounting-block":
            action, params = "READ_S4615_ZF01_ACCOUNTING_BLOCK", {}
        elif args.request_action == "inspect-zf01-lf-new-header-form":
            action, params = "INSPECT_S4615_VTFLC_NEW_HEADER_FORM", {}
        elif args.request_action == "read-f2-lf-header-options":
            action, params = "READ_S4615_F2_LF_HEADER_OPTIONS", {}
        elif args.request_action == "inspect-vtflc-new-item-form":
            action, params = "INSPECT_S4615_VTFLC_NEW_ITEM_FORM", {}
        elif args.request_action == "inspect-vtflc-new-target-item-form":
            action, params = "INSPECT_S4615_VTFLC_NEW_TARGET_ITEM_FORM", {}
        elif args.request_action in {"find-zf01-lf-copy-header", "display-zf01-lf-copy-header"}:
            action = ("FIND_S4615_ZF01_LF_COPY_HEADER" if args.request_action.startswith("find")
                      else "DISPLAY_S4615_ZF01_LF_COPY_HEADER")
            params = {
                "transaction": "VTFLC", "program": "SAPL080W",
                "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK",
                "billing_type": "ZF01", "delivery_type": "LF",
            }
            if action.startswith("DISPLAY"):
                params["detail_button_id"] = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"
        elif args.request_action == "open-billing-copy-items":
            action = "OPEN_S4650_BILLING_COPY_ITEMS"
            params = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "110",
                      "tree_id": "/app/con[0]/ses[0]/wnd[0]/shellcont/shell",
                      "node_key": "02", "node_text": "Poste", "column": "Column1"}
        elif args.request_action == "display-billing-copy-tan":
            action = "DISPLAY_S4650_BILLING_COPY_TAN"
            params = {"transaction": "VTFLC", "program": "SAPL080W", "screen": "112",
                      "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLP",
                      "item_category": "TAN", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        elif args.request_action == "display-s4600-cdcl":
            action = "DISPLAY_S4600_CDCL_REFERENCE"
            params = {"transaction": "VOV8", "program": "SAPL080O",
                      "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK",
                      "sales_order_type": "CDCL",
                      "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        elif args.request_action == "navigate":
            params = {
                "control_id": args.control_id,
                "expected_type": args.expected_type,
                "expected_text": args.expected_text,
                "navigation_operation": args.operation,
            }
            if args.node_key is not None:
                params["node_key"] = args.node_key
            if args.expected_transaction is not None:
                params["expected_transaction"] = args.expected_transaction
            if args.item_column is not None:
                params["item_column"] = args.item_column
            action = "NAVIGATE"
        elif args.request_action == "open":
            action, params = "OPEN_TRANSACTION", {"transaction": args.transaction}
        elif args.request_action == "open-s4615-customizing":
            action, params = "OPEN_S4615_CUSTOMIZING_READ", {"transaction": args.transaction}
        elif args.request_action == "inspect-s4615-customizing":
            action, params = "INSPECT_S4615_CUSTOMIZING", {"object": args.object}
        elif args.request_action == "read-s4615-table":
            action, params = "READ_S4615_CUSTOMIZING_TABLE", {"table": args.table}
        elif args.request_action == "scan-s4615-customizing":
            action, params = "SCAN_S4615_CUSTOMIZING", {"object": args.object}
        else:
            raise SapGuiBridgeError(
                f"Unsupported request action: {args.request_action!r}"
            )
        print(json.dumps(enqueue_request(action, params), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "wait":
        response = wait_for_response(args.request_id, timeout_seconds=args.timeout)
        print(json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if response.get("status") == "SUCCESS" else 2
    if args.command == "execute":
        SapGuiConnection(mode=SafetyMode.EXECUTE)
        return 2
    mode = SafetyMode.PREPARE if args.command == "prepare" else SafetyMode.READ
    session = SapGuiConnection(mode=mode).attach()
    if args.command == "status":
        output = session.status()
    elif args.command == "inspect":
        output = inspect_screen(session)
    elif args.command == "open":
        open_transaction(session, args.transaction)
        output = session.status()
    elif args.prepare_action == "set-field":
        set_text(session, args.control_id, args.value)
        output = inspect_screen(session)
    else:
        back(session)
        output = session.status()
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SapGuiBridgeError as exc:
        print(json.dumps({"status": "BLOCKED", "error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
