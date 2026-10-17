"""S4615 Chapter 4 Exercise 5 exact-Book E2E orchestrator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.provisioning.phase5 import (
    S4615_SEED_PATH,
    Phase5ProvisioningEngine,
    load_backend,
    load_decisions,
    load_seed,
)
from src.sap_mapping import validate_runtime_contract
from src.training_context import PlaceholderResolver


OBJECT_ID = "S4615_CH4_EX5_SALES_ORDER_CASH_SALE"
IDENTITY_MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
EXPECTED = {
    "SalesOrderType": "BV",
    "SalesOrganization": "1010",
    "DistributionChannel": "10",
    "OrganizationDivision": "00",
    "SoldToParty": "C615-D00",
    "PurchaseOrderByCustomer": "00S4615-BV",
}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--training-user", required=True)
    mode = value.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    value.add_argument("--decision-file")
    value.add_argument("--seed-file", default=str(S4615_SEED_PATH))
    value.add_argument("--backend-factory")
    return value


def _book_payload(training_user: str) -> tuple[dict, dict]:
    objects = json.loads(
        (ROOT / "data/validated/canonical_objects.json").read_text(encoding="utf-8")
    )["objects"]
    original = next(item for item in objects if item["object_id"] == OBJECT_ID)
    resolved = PlaceholderResolver().resolve(original, training_user)
    index = {item["object_id"]: item for item in objects}
    index[OBJECT_ID] = resolved.canonical_object
    mapped = validate_runtime_contract(resolved.canonical_object, object_index=index)
    if mapped["runtime_status"] != "EXECUTION_READY":
        raise ValueError(f"Book SALES_ORDER is not EXECUTION_READY: {mapped['runtime_status']}")
    payload = mapped["payloads"][0]["body"]
    for field, expected in EXPECTED.items():
        if payload.get(field) != expected:
            raise ValueError(f"Exact Book target mismatch at {field}: {payload.get(field)!r}")
    items = payload.get("to_Item") or []
    if len(items) != 1 or any(
        items[0].get(field) != expected
        for field, expected in {
            "Material": "P615-400", "RequestedQuantity": 1, "RequestedQuantityUnit": "PC"
        }.items()
    ):
        raise ValueError("Exact Book item target mismatch")
    return payload, resolved.trace_metadata()


def _execute_sales_order(training_user: str) -> dict:
    runtime = _sales_order_runtime()
    dry = runtime.dry_run(OBJECT_ID, training_user_code=training_user)
    if dry.status.value != "DRY_RUN_OK":
        return {"status": dry.status.value, "dry_run": dry.as_dict()}
    executed = runtime.execute(
        OBJECT_ID,
        customer_reference="00S4615-BV",
        customer_purchase_order_date=None,
        training_user_code=training_user,
        allow_canonical_reference=True,
    )
    return {"status": executed.status.value, "dry_run": dry.as_dict(), "execute": executed.as_dict()}


def _sales_order_runtime():
    from dotenv import load_dotenv
    from src.sap_runtime.config import SapRuntimeConfig
    from src.sap_runtime.ledger import ExecutionLedger
    from src.sap_runtime.prechecks import ConfiguredDependencyVerifier
    from src.sap_runtime.sales_order import SalesOrderRuntime
    from src.sap_runtime.transport import UrllibSapTransport

    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.precheck_config_path is None:
        raise ValueError("SAP_PRECHECK_CONFIG is required")
    return SalesOrderRuntime(
        config=config,
        transport=UrllibSapTransport(config),
        ledger=ExecutionLedger(config.ledger_path),
        dependency_verifier=ConfiguredDependencyVerifier.from_file(
            config.precheck_config_path, client=config.client
        ),
        identity_mapping_path=IDENTITY_MAPPING_PATH,
    )


def _dry_run_sales_order(training_user: str) -> dict:
    dry = _sales_order_runtime().dry_run(OBJECT_ID, training_user_code=training_user)
    return {"status": dry.status.value, "dry_run": dry.as_dict()}


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.training_user != "00":
            raise ValueError("This one-shot is restricted to exact Book training user 00")
        payload, training_context = _book_payload(args.training_user)
        if args.execute:
            if not args.backend_factory:
                raise ValueError("--execute requires --backend-factory")
            phrase = "EXECUTE S4615 USER 00 00S4615-BV"
            if input(f"Type exactly '{phrase}' to authorize provisioning and one order: ") != phrase:
                raise ValueError("Execution confirmation failed")
        engine = Phase5ProvisioningEngine(
            backend=load_backend(args.backend_factory),
            decisions=(
                load_decisions(args.decision_file)
                if args.decision_file else load_seed(args.seed_file)
            ),
            execute=args.execute,
        )
        provisioning = engine.plan(include_book_data=True)
        blockers = list(provisioning["blockers"])
        pending = "BLOCKED_BY_PREREQUISITES" if blockers else "PENDING"
        workflow = {
            "policy": {
                "sequence": ["check", "prepare", "validate", "write", "readback"],
                "default_mode": "DRY_RUN",
                "write_gate": "--execute",
                "exists_behavior": "SKIP",
                "stop_on": [
                    "UNEXPECTED_POPUP", "TRANSPORT_REQUIRED", "UNKNOWN_MANDATORY_VALUE",
                ],
                "transport_release": "NEVER_AUTOMATIC",
                "protected_sales_order": "148",
            },
            "stages": [
                {"order": 1, "stage": "COMMON_ENV", "status": pending},
                {"order": 2, "stage": "CUSTOMER_C615_D00", "status": pending},
                {"order": 3, "stage": "PRODUCT_P615_400", "status": pending},
                {"order": 4, "stage": "PRECHECKS", "status": pending},
                {"order": 5, "stage": "ANTI_DUPLICATE_00S4615_BV", "status": pending},
                {"order": 6, "stage": "BV_CASH_SALE", "object_id": OBJECT_ID, "status": pending},
                {
                    "order": 7,
                    "stage": "VERIFY_AUTO_CREATED_DELIVERY",
                    "object_id": "S4615_CH4_EX5_OUTBOUND_DELIVERY_CASH_SALE",
                    "status": "CONTRACT_REQUIRED",
                },
                {"order": 8, "stage": "PGI", "status": "CONTRACT_REQUIRED"},
                {
                    "order": 9,
                    "stage": "BILLING_BV",
                    "object_id": "S4615_CH4_EX5_BILLING_CASH_SALE",
                    "reference": "RUNTIME_SALES_ORDER_ID",
                    "status": "CONTRACT_REQUIRED",
                },
                {"order": 10, "stage": "ACCOUNTING_READBACK", "status": "CONTRACT_REQUIRED"},
            ],
            "status": "BLOCKED_BY_PREREQUISITES" if blockers else "PENDING_SALES_ORDER",
        }
        sales_order = None
        if args.execute and not blockers:
            sales_order = _execute_sales_order(args.training_user)
            workflow["status"] = (
                "POST_SALES_ORDER_READBACK_REQUIRED"
                if sales_order["status"] == "VERIFIED"
                else "BLOCKED_SALES_ORDER"
            )
        elif args.dry_run and not blockers:
            sales_order = _dry_run_sales_order(args.training_user)
            workflow["status"] = sales_order["status"]
        result = {
            "mode": "EXECUTE" if args.execute else "DRY_RUN",
            "status": "BLOCKED" if blockers else (sales_order or {}).get("status", "READY"),
            "canonical_object_id": OBJECT_ID,
            "training_context": training_context,
            "exact_book_payload": payload,
            "provisioning": provisioning,
            "workflow": workflow,
            "sales_order_runtime": sales_order,
            "blockers": blockers,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] in {"READY", "VERIFIED", "DRY_RUN_OK"} else 2
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
