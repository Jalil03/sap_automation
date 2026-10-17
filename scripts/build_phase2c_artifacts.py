"""Build deterministic Phase 2C coverage and representative payload snapshots."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_mapping import validate_runtime_contract  # noqa: E402
from src.sap_mapping.contracts import mapping_contracts  # noqa: E402

CANONICAL_PATH = ROOT / "data/validated/canonical_objects.json"
COVERAGE_PATH = ROOT / "reports/phase2c_mapping_coverage.json"
SNAPSHOT_PATH = ROOT / "tests/snapshots/phase2c_core_payloads.json"

REPRESENTATIVE_IDS = [
    "S4600_CH4_EX9_BUSINESS_PARTNER_T-CUS-GROUP",
    "S4600_CH4_EX11_MATERIAL_T-MS4-GROUP",
    "S4600_CH4_EX13_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL",
    "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT",
    "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_OUTBOUND_DELIVERY_INSTALLMENT",
    "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_BILLING_INSTALLMENT",
]


def canonical_objects() -> list[dict]:
    return json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))["objects"]


def build_coverage() -> dict:
    contracts = mapping_contracts()
    objects = canonical_objects()
    scoped = set(contracts["objects"])
    counts = Counter(obj["object_type"] for obj in objects if obj["object_type"] in scoped)
    result = {
        "contract_version": contracts["contract_version"],
        "authority": contracts["authority"],
        "live_sap_metadata_validated": False,
        "object_types": {},
    }
    for object_type in sorted(scoped):
        contract = contracts["objects"][object_type]
        disposition_counts = Counter(
            entry["disposition"] for entry in contract["fields"].values()
        )
        result["object_types"][object_type] = {
            "canonical_object_count": counts[object_type],
            "interface": contract["interface"],
            "protocol": contract["protocol"],
            "field_count": len(contract["fields"]),
            "disposition_counts": {
                disposition: disposition_counts.get(disposition, 0)
                for disposition in contracts["dispositions"]
            },
            "fields": contract["fields"],
            "mandatory_paths": contract["mandatory_paths"],
            "runtime_bindings": contract["runtime_bindings"],
        }
    result["totals"] = {
        "canonical_object_count": sum(counts.values()),
        "field_count": sum(item["field_count"] for item in result["object_types"].values()),
        "disposition_counts": {
            disposition: sum(
                item["disposition_counts"][disposition]
                for item in result["object_types"].values()
            )
            for disposition in contracts["dispositions"]
        },
    }
    return result


def build_snapshots() -> dict:
    objects = canonical_objects()
    index = {obj["object_id"]: obj for obj in objects}
    snapshots = []
    for object_id in REPRESENTATIVE_IDS:
        obj = index[object_id]
        result = validate_runtime_contract(
            obj,
            object_index=index,
            structural_fixture=obj["readiness_status"] == "BLOCKED",
        )
        snapshots.append({
            "object_id": result["object_id"],
            "object_type": result["object_type"],
            "runtime_status": result["runtime_status"],
            "interface": result["interface"],
            "payloads": result["payloads"],
            "runtime_bindings": result["runtime_bindings"],
            "deferred_values": result["deferred_values"],
            "contract_validation": result["contract_validation"],
        })
    return {
        "snapshot_version": "1.0.0",
        "source": "data/validated/canonical_objects.json",
        "snapshots": snapshots,
    }


def rendered(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {COVERAGE_PATH: rendered(build_coverage()), SNAPSHOT_PATH: rendered(build_snapshots())}
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, value in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != value]
        if stale:
            raise SystemExit(f"Phase 2C artifacts are missing or stale: {stale}")
    else:
        for path, value in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
    print(json.dumps({str(path.relative_to(ROOT)): len(value) for path, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
