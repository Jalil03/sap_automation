"""Preflight or execute one approved T-S50A01 customer role."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4600_t_s50a01_customer_roles import ensure_role
from src.sap_runtime.config import SapRuntimeConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("FLCU00", "FLCU01"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    load_dotenv(ROOT / ".env")
    result = ensure_role(SapRuntimeConfig.from_env(), args.role, execute=args.execute)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"READY", "EXISTS", "CREATED_AND_VERIFIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
