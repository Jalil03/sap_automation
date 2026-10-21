"""Thin, dry-run-by-default CLI for the evidenced customer OData extension."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.phase5 import Phase5ProvisioningEngine, S4615_SEED_PATH, load_seed
from src.provisioning.sap_api_backend import CUSTOMER, MAPPINGS_PATH, SapApiBackend


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, default=S4615_SEED_PATH)
    parser.add_argument("--operation", choices=[CUSTOMER], default=CUSTOMER)
    parser.add_argument("--mapping-store", type=Path, default=MAPPINGS_PATH)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    backend = SapApiBackend(seed_path=args.seed, mapping_path=args.mapping_store)
    engine = Phase5ProvisioningEngine(backend=backend, decisions=load_seed(args.seed), execute=args.execute)
    result = engine._ensure(args.operation).as_dict()
    if args.execute and result["status"] == "SKIPPED_EXISTS":
        result["readback"] = backend.readback(args.operation, result["target"])
        if result["readback"] is None:
            result["status"] = "BLOCKED_READBACK"
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] in {"SKIPPED_EXISTS", "PROVISIONED_VERIFIED", "WOULD_PROVISION"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
