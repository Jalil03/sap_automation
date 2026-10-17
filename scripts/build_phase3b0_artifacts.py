"""Build deterministic, offline Phase 3B.0 SALES_ORDER pilot evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_mapping import validate_runtime_contract  # noqa: E402


CANONICAL_PATH = ROOT / "data/validated/canonical_objects.json"
PILOT_DIR = ROOT / "evidence/pilot"
CANDIDATE_PATH = PILOT_DIR / "sales_order_candidate.json"
PAYLOAD_PATH = PILOT_DIR / "sales_order_proposed_payload.json"
CHECKLIST_PATH = PILOT_DIR / "sales_order_dependency_checklist.json"


def rendered(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def sha256_json(value: dict) -> str:
    compact = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def select_candidate() -> tuple[dict, dict]:
    objects = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))["objects"]
    index = {obj["object_id"]: obj for obj in objects}
    eligible = []
    for obj in objects:
        if obj["object_type"] != "SALES_ORDER":
            continue
        result = validate_runtime_contract(
            obj,
            object_index=index,
            structural_fixture=obj["readiness_status"] == "BLOCKED",
        )
        if result["runtime_status"] == "EXECUTION_READY":
            eligible.append((obj, result))
    if len(eligible) != 1:
        raise RuntimeError(f"Expected exactly one EXECUTION_READY SALES_ORDER, found {len(eligible)}")
    return eligible[0]


def dependency(
    dependency_type: str,
    value: str | None,
    payload_paths: list[str],
    checks: list[str],
    *,
    mode: str = "REFERENCED_VALUE",
) -> dict:
    return {
        "type": dependency_type,
        "value": value,
        "payload_paths": payload_paths,
        "mode": mode,
        "status": "REQUIRES_LIVE_PRECHECK",
        "checks": checks,
        "on_failure": "ABORT_BEFORE_POST",
    }


def build() -> dict[Path, str]:
    candidate, result = select_candidate()
    payload = result["payloads"][0]["body"]
    payload_hash = sha256_json(payload)
    correlation_seed = f"{candidate['object_id']}|{payload_hash}"
    correlation_id = "SO-PILOT-" + hashlib.sha256(correlation_seed.encode("utf-8")).hexdigest()[:20].upper()
    data = candidate["data"]
    item = data["items"][0]

    dependencies = [
        dependency("CUSTOMER", data["sold_to_party"], ["SoldToParty", "to_Partner[0].Customer"], [
            "Customer exists and is active.",
            "Customer is extended to sales area 1010/10/00.",
            "Customer is permitted as sold-to for order type OR.",
        ]),
        dependency("PARTNER_FUNCTION", "DO", ["to_Partner[0].PartnerFunction"], [
            "External OData PartnerFunction DO is active and maps to internal AG / Donneur d'ordre.",
            "PartnerFunctionInternalCode is not sent.",
        ]),
        dependency("MATERIAL", item["material"], ["to_Item[0].Material"], [
            "Material exists and is active.",
            "Material has the required sales views for sales area 1010/10.",
            "Material is orderable for order type OR and customer C615-A00.",
        ]),
        dependency("SALES_ORGANIZATION", data["sales_organization"], ["SalesOrganization"], [
            "Sales organization exists and is active for order processing.",
        ]),
        dependency("DISTRIBUTION_CHANNEL", data["distribution_channel"], ["DistributionChannel"], [
            "Distribution channel exists and is assigned to sales organization 1010.",
        ]),
        dependency("SALES_DIVISION", data["sales_division"], ["OrganizationDivision"], [
            "Division exists and completes valid sales area 1010/10/00.",
        ]),
        dependency("SALES_DOCUMENT_TYPE", data["order_type"], ["SalesOrderType"], [
            "Document type OR exists, is creatable through this service, and is allowed for sales area 1010/10/00.",
        ]),
        dependency("UNIT_OF_MEASURE", item["unit"], ["to_Item[0].RequestedQuantityUnit"], [
            "PC is accepted by the API as an external requested-quantity unit.",
            "PC is valid for material P615-100 and quantity 10.",
        ]),
        dependency("PAYMENT_TERMS", data["payment_terms"], ["CustomerPaymentTerms"], [
            "Payment terms R001 exists and is permitted for customer/order context.",
        ]),
        dependency("PLANT", None, [], [
            "A valid plant can be determined from customer/material/sales-area configuration when ProductionPlant is omitted.",
            "Abort if plant is mandatory and cannot be determined.",
        ], mode="SYSTEM_DETERMINED_NOT_IN_PAYLOAD"),
        dependency("SHIPPING_POINT", None, [], [
            "A valid shipping point can be determined when ShippingPoint is omitted.",
            "Abort if shipping point is mandatory and cannot be determined.",
        ], mode="SYSTEM_DETERMINED_NOT_IN_PAYLOAD"),
    ]

    checklist = {
        "artifact_version": "1.0.0",
        "canonical_object_id": candidate["object_id"],
        "target": {"service": "API_SALES_ORDER_SRV", "entity_set": "A_SalesOrder"},
        "payload_sha256": payload_hash,
        "all_checks_status": "NOT_RUN",
        "dependencies": dependencies,
        "application_idempotency": {
            "canonical_object_id": candidate["object_id"],
            "migration_correlation_id": correlation_id,
            "correlation_storage": "APPLICATION_LEDGER_ONLY_NOT_SAP_PAYLOAD",
            "pre_write_duplicate_check": [
                "Reject when the ledger already has SUBMITTED, CREATED, or AMBIGUOUS for the canonical object ID, correlation ID, or payload SHA-256.",
                "Run a read-only SAP search using the source-backed fingerprint: SalesOrderType OR, SalesOrganization 1010, DistributionChannel 10, OrganizationDivision 00, SoldToParty C615-A00, PurchaseOrderByCustomer 4712, material P615-100, quantity 10, and unit PC.",
                "Abort on an exact match or on any ambiguous partial match; require human reconciliation.",
            ],
            "execution_ledger_required_fields": [
                "canonical_object_id", "migration_correlation_id", "payload_sha256", "attempt_number",
                "status", "started_at", "completed_at", "http_status", "created_sales_order_id",
                "response_etag", "sanitized_error",
            ],
            "forbidden_ledger_fields": ["csrf_token", "authorization_header", "session_cookie"],
            "safe_retry_abort_policy": [
                "Never retry blindly after a timeout, disconnect, or ambiguous response.",
                "Before every retry, rerun ledger and SAP duplicate checks.",
                "Do not retry validation errors, HTTP 4xx, authorization failures, or conflicts without correcting and reapproving the pilot.",
                "Retry a transient failure only when no order exists, the previous attempt is conclusively not committed, and a new per-session CSRF token is acquired at execution time.",
                "Allow at most one approved retry; otherwise abort for manual reconciliation.",
            ],
        },
        "acceptance_criteria": {
            "http": [
                "One authorized POST to API_SALES_ORDER_SRV/A_SalesOrder returns HTTP 201 Created.",
                "Response contains a non-empty SAP-generated SalesOrder string and no business error payload.",
                "Location and/or entity metadata identifies A_SalesOrder(<created key>); capture ETag when returned.",
            ],
            "get_reread": [
                "SalesOrder", "SalesOrderType", "SalesOrganization", "DistributionChannel",
                "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
                "CustomerPaymentTerms", "to_Partner/PartnerFunction", "to_Partner/Customer",
                "to_Item/SalesOrderItem", "to_Item/Material", "to_Item/RequestedQuantity",
                "to_Item/RequestedQuantityUnit", "to_Item/ProductionPlant", "to_Item/ShippingPoint",
            ],
            "manual_va03_or_fiori": [
                "Order exists once and has document type OR and sales area 1010/10/00.",
                "Sold-to partner is C615-A00 and the observed external DO role resolves to sold-to semantics.",
                "Item 10 contains material P615-100 and requested quantity 10 PC.",
                "Customer reference 4712 and payment terms R001 are retained.",
                "System-determined plant and shipping point are valid and no incompletion/error blocks processing.",
                "No unintended partner, pricing, schedule-line, delivery, billing, or accounting object was created.",
            ],
            "abort_failure_conditions": [
                "Any dependency pre-check is not PASS.",
                "Duplicate or ambiguous pre-existing order is found.",
                "CREATE authorization, CSRF acquisition, or explicit pilot approval is absent.",
                "Payload differs from the pinned SHA-256 or contains PartnerFunctionInternalCode, a token, or an invented field/value.",
                "Response is not HTTP 201, lacks an unambiguous created SalesOrder ID, or returns a business/validation error.",
                "Connection outcome is ambiguous, re-read does not match, or multiple orders are observed.",
            ],
        },
        "unproven": [
            "deep-insert write behavior",
            "CREATE authorization",
            "accepted write serialization",
            "transaction behavior",
            "idempotency in SAP itself",
        ],
        "current_gate": "NO_GO_UNTIL_ALL_LIVE_PRECHECKS_PASS_AND_EXECUTION_IS_EXPLICITLY_AUTHORIZED",
    }
    return {
        CANDIDATE_PATH: rendered(candidate),
        PAYLOAD_PATH: rendered(payload),
        CHECKLIST_PATH: rendered(checklist),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        stale = [
            str(path.relative_to(ROOT)) for path, value in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != value
        ]
        if stale:
            raise SystemExit(f"Phase 3B.0 artifacts are missing or stale: {stale}")
    else:
        for path, value in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
    print(json.dumps({str(path.relative_to(ROOT)): len(value) for path, value in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
