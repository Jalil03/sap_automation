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
    request_sub.add_parser("read-status-bar")
    request_sub.add_parser("read-screen")
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
        elif args.request_action == "read-status-bar":
            action, params = "READ_STATUS_BAR", {}
        elif args.request_action == "read-screen":
            action, params = "READ_SCREEN", {}
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
