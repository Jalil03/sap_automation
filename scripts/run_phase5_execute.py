"""Phase 5 common-environment provisioning entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.phase5 import Phase5ProvisioningEngine, load_backend, load_decisions, load_seed


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    mode = value.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    source = value.add_mutually_exclusive_group()
    source.add_argument("--decision-file")
    source.add_argument("--seed-file")
    value.add_argument("--backend-factory", help="Explicit module:function SAP backend factory")
    value.add_argument(
        "--include-book-data",
        action="store_true",
        help="Also run LOOKUP/PROVISION/READBACK checks for the S4615 customer and product",
    )
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.execute:
            if not (args.decision_file or args.seed_file) or not args.backend_factory:
                raise ValueError("--execute requires --decision-file/--seed-file and --backend-factory")
            phrase = (
                "EXECUTE PHASE5 S4615 1010 INCLUDING BOOK DATA"
                if args.include_book_data
                else "EXECUTE PHASE5 COMMON 1010"
            )
            if input(f"Type exactly '{phrase}' to authorize provisioning: ") != phrase:
                raise ValueError("Execution confirmation failed")
        engine = Phase5ProvisioningEngine(
            backend=load_backend(args.backend_factory),
            decisions=(
                load_seed(args.seed_file) if args.seed_file
                else load_decisions(args.decision_file)
            ),
            execute=args.execute,
        )
        result = engine.plan(include_book_data=args.include_book_data)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] == "READY" else 2
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
