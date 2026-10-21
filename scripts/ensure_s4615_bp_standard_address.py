"""Dry-run by default; one approved SAP GUI BP-address SAVE with GET readback."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4615_bp_standard_address import ensure_address
from src.sap_runtime.config import SapRuntimeConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
        result = ensure_address(SapRuntimeConfig.from_env(), execute=args.execute)
    except Exception as error:
        result = {"status": "BLOCKED", "reason": str(error)}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"EXISTS", "WOULD_CREATE", "CREATED_AND_VERIFIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
