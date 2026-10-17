"""Provision one allowlisted VOV4/T184 contract through the local runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.sap_gui_backend import SapGuiPhase5Backend, _vov4_contract


OPERATION = "VOV4_ITEM_CATEGORY_DETERMINATION"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    contract = _vov4_contract(args.contract)
    backend = SapGuiPhase5Backend(timeout_seconds=60.0)
    target = {"contract_id": args.contract}
    state = backend.lookup(OPERATION, target) if args.dry_run else "PENDING_WRITE_BUFFER"
    if state == "EXISTS":
        result = {"status": "EXISTS", "contract_id": args.contract}
    elif args.dry_run:
        result = {
            "status": "WOULD_PROVISION" if state == "MISSING" else "BLOCKED",
            "state": state,
            "contract_id": args.contract,
            "target": contract["target"],
        }
    else:
        provisioned = backend.provision(
            OPERATION,
            target,
            {
                "transport_request": contract["transport_request"],
                "resume_exact_pending_row": True,
            },
        )
        result = {
            "status": "VERIFIED" if provisioned.get("accepted") else "BLOCKED",
            "contract_id": args.contract,
            "result": provisioned,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] in {"EXISTS", "WOULD_PROVISION", "VERIFIED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
