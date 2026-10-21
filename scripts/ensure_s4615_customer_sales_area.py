"""Execute only the exact approved A01 sales-area extension; dry-run default."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.s4615_customer_sales_area import ensure_sales_area_once
from src.sap_runtime.config import SapRuntimeConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    if not args.execute:
        print(json.dumps({"status": "DRY_RUN", "reason": "Use --execute for the scoped one-shot write"}))
        return 0
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
        result = ensure_sales_area_once(
            SapRuntimeConfig.from_env(),
            ROOT / "data/provisioning/s4615/C615-A01.workflow_approval.json",
            ROOT / "data/provisioning/phase5_identity_mappings.json",
            ROOT / "data/provisioning/s4615/C615-A01.workflow_checkpoint.json",
            ROOT / "data/provisioning/s4615/C615-A01.sales_area.attempt.json",
        )
    except Exception as error:
        result = {"status": "BLOCKED", "reason": str(error)}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"EXISTS", "CREATED_AND_VERIFIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
