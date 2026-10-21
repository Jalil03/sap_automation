"""Dry-run by default; execute one approved T-S50A01 BP-root POST only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4600_t_s50a01_bp_root import (
    DEFAULT_APPROVAL_PATH,
    contract_summary,
    execute_once,
    preflight,
)
from src.sap_runtime.config import SapRuntimeConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    parser.add_argument("--approval", type=Path, default=DEFAULT_APPROVAL_PATH)
    args = parser.parse_args(argv)
    if not args.execute and not args.preflight:
        print(json.dumps(contract_summary(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    result = preflight(config=config) if args.preflight else execute_once(config=config, approval_path=args.approval)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
