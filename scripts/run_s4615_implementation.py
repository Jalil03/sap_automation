"""Offline Phase 5 implementation plan for the S4615 plant-to-master-data chain."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4615_implementation import (
    build_dry_run, load_contract, resolved_operations, validate_write_approval,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--approvals", type=Path)
    args = parser.parse_args(argv)
    try:
        decisions = json.loads(args.decisions.read_text(encoding="utf-8")) if args.decisions else None
        approvals = json.loads(args.approvals.read_text(encoding="utf-8")) if args.approvals else None
        result = build_dry_run(decisions=decisions, approvals=approvals)
        if args.execute:
            if args.approvals is None:
                raise ValueError("--execute requires explicit scoped approvals")
            if not isinstance(approvals, dict):
                raise ValueError("Approval file must be an operation-to-approval object")
            for op in resolved_operations(load_contract(), decisions):
                validate_write_approval(op, approvals.get(op["id"], {}))
            # None of the seven SAP write contracts is established in the audit.
            # No backend-factory or write transport is attached to this CLI.
            raise ValueError("S4615 SAP write contracts are unproven; execution remains disabled")
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCKED", "sap_calls": 0, "sap_writes": 0,
                          "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
