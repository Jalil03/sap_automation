from __future__ import annotations

import argparse
import json
import sys

from .config import SapRuntimeConfig
from .errors import SapRuntimeError
from .ledger import ExecutionLedger
from .models import ExecutionStatus
from .prechecks import ConfiguredDependencyVerifier
from .sales_order import SalesOrderRuntime
from .security import sanitize_error
from .transport import UrllibSapTransport


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="python -m src.sap_runtime")
    commands = root.add_subparsers(dest="command", required=True)
    sales = commands.add_parser("sales-order", help="Validate or execute one SALES_ORDER")
    sales.add_argument("--object", required=True, dest="object_id")
    mode = sales.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    sales.add_argument("--customer-reference")
    sales.add_argument("--customer-purchase-order-date", metavar="YYYY-MM-DD")
    sales.add_argument(
        "--training-user",
        metavar="00-99",
        help="Resolve ## in a detached runtime copy before mapping",
    )
    sales.add_argument(
        "--non-interactive-approved", action="store_true",
        help="CI-only: also requires --approval-id to match SAP_EXECUTION_APPROVAL_ID",
    )
    sales.add_argument("--approval-id")
    return root


def _confirmed(args: argparse.Namespace, config: SapRuntimeConfig) -> bool:
    if args.non_interactive_approved:
        return bool(
            args.approval_id
            and config.ci_approval_id
            and args.approval_id == config.ci_approval_id
        )
    phrase = f"EXECUTE {args.object_id} {args.customer_reference}"
    entered = input(f"Type exactly '{phrase}' to authorize one POST: ")
    return entered == phrase


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        config = SapRuntimeConfig.from_env()
        if config.precheck_config_path is None:
            raise SapRuntimeError("SAP_PRECHECK_CONFIG is required")
        verifier = ConfiguredDependencyVerifier.from_file(
            config.precheck_config_path, client=config.client
        )
        runtime = SalesOrderRuntime(
            config=config,
            transport=UrllibSapTransport(config),
            ledger=ExecutionLedger(config.ledger_path),
            dependency_verifier=verifier,
        )
        if args.dry_run:
            result = runtime.dry_run(
                args.object_id,
                customer_reference=args.customer_reference,
                customer_purchase_order_date=args.customer_purchase_order_date,
                training_user_code=args.training_user,
            )
        else:
            if not args.customer_reference or not args.customer_purchase_order_date:
                raise SapRuntimeError(
                    "--execute requires --customer-reference and --customer-purchase-order-date"
                )
            if not _confirmed(args, config):
                raise SapRuntimeError("Execution confirmation failed; no POST was attempted")
            result = runtime.execute(
                args.object_id,
                customer_reference=args.customer_reference,
                customer_purchase_order_date=args.customer_purchase_order_date,
                training_user_code=args.training_user,
            )
        print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0 if result.status in {ExecutionStatus.DRY_RUN_OK, ExecutionStatus.VERIFIED} else 2
    except (SapRuntimeError, OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCKED", "error": sanitize_error(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
