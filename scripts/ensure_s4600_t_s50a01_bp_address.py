"""Preflight or execute the approved T-S50A01 standard-address workflow."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4600_t_s50a01_bp_address import ensure_address
from src.sap_runtime.config import SapRuntimeConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    load_dotenv(ROOT / ".env")
    result = ensure_address(SapRuntimeConfig.from_env(), execute=args.execute)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
