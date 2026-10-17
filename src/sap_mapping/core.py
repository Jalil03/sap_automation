from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from .bapi import BAPI_MAPPERS
from .common import retained_nonpayload_fields
from .errors import BlockedObjectError, MappingContractError, UnsupportedObjectTypeError
from .odata import ODATA_MAPPERS
from .registry import WRITABLE_CORE, preferred_interface

MAPPING_VERSION = "1.0.0"

MAPPED_TOP_LEVEL_FIELDS = {
    "BUSINESS_PARTNER": {
        "partner_id", "roles", "name", "sales_areas", "grouping", "addresses", "currency",
        "shipping_conditions", "delivering_plant", "incoterms", "incoterms_location",
        "payment_terms", "account_assignment_group", "customer_pricing_procedure",
        "tax_classifications", "company_code", "reconciliation_account", "partner_functions",
        "fax_number",
    },
    "MATERIAL": {
        "material_id", "description", "base_unit", "plants", "industry_sector", "material_type",
        "sales_organization", "distribution_channel", "tax_classification",
        "minimum_order_quantity", "minimum_order_unit", "availability_check", "delivering_plant",
        "strategy_group", "item_category_group",
    },
    "SALES_ORDER": {
        "order_type", "sales_organization", "distribution_channel", "sales_division",
        "sold_to_party", "ship_to_party", "customer_reference", "requested_delivery_date",
        "items", "payment_terms",
    },
    "PRICING_CONDITION": {
        "condition_type", "key_combination", "valid_from", "valid_to", "rate", "currency",
        "pricing_unit", "scales", "rate_unit", "calculation_semantics", "deletion_indicator",
    },
    "OUTBOUND_DELIVERY": {
        "delivery_type", "ship_to_party", "shipping_point", "planned_creation_date",
        "planned_goods_issue_date", "items",
    },
    "BILLING": {
        "billing_type", "payer", "billing_date", "reference_document", "items", "payment_terms",
        "net_value", "currency",
    },
}


def supported_object_types() -> tuple[str, ...]:
    return tuple(sorted(WRITABLE_CORE))


def _validate_canonical(obj: dict[str, Any]) -> None:
    required = ("object_id", "object_type", "readiness_status", "data", "provenance")
    missing = [field for field in required if field not in obj]
    if missing:
        raise MappingContractError(f"Canonical object missing fields: {missing}")
    if obj["readiness_status"] not in {"READY", "BLOCKED"}:
        raise MappingContractError(f"Unsupported readiness status: {obj['readiness_status']}")


def map_canonical_object(obj: dict[str, Any], *, structural_fixture: bool = False) -> dict:
    """Map one canonical object without network, transport, or execution behavior.

    BLOCKED objects require explicit ``structural_fixture=True`` and can never be
    marked execution-ready. Runtime dependency/date bindings remain outside the
    SAP payload body and must be resolved by a future Phase 3 orchestration layer.
    """
    _validate_canonical(obj)
    object_type = obj["object_type"]
    if object_type not in WRITABLE_CORE:
        raise UnsupportedObjectTypeError(f"No Phase 2B writable-core mapper for {object_type}")
    if obj["readiness_status"] == "BLOCKED" and not structural_fixture:
        raise BlockedObjectError(
            f"{obj['object_id']} is BLOCKED; use structural_fixture=True for non-executable testing"
        )

    interface = deepcopy(preferred_interface(object_type))
    if object_type == "SALES_ORDER" and interface.get("external_name"):
        # Phase 3A.1 live metadata identifies the external namespace. Keep the
        # Gateway registration as evidence, but never present it as the
        # consumer endpoint service name.
        interface["consumer_service_name"] = interface["external_name"]
        interface["technical_registration_name"] = interface["exact_name"]
    if interface["classification"] == "ODATA":
        mapper = ODATA_MAPPERS.get(object_type)
        protocol = "ODATA"
    elif interface["classification"] == "STANDARD_BAPI":
        mapper = BAPI_MAPPERS.get(object_type)
        protocol = "BAPI"
    else:
        mapper = None
        protocol = interface["classification"]
    if mapper is None:
        raise MappingContractError(
            f"No {interface['classification']} mapper matches registry preference for {object_type}"
        )

    payloads, bindings, deferred, missing = mapper(obj)
    is_fixture = obj["readiness_status"] == "BLOCKED"
    payload_state = "STRUCTURAL_FIXTURE" if is_fixture else (
        "TEMPLATE" if bindings or deferred or missing else "CONCRETE"
    )
    result = {
        "mapping_version": MAPPING_VERSION,
        "object_id": obj["object_id"],
        "object_type": object_type,
        "scenario_id": obj.get("scenario_id"),
        "canonical_readiness_status": obj["readiness_status"],
        "structural_fixture": is_fixture,
        "execution_ready": payload_state == "CONCRETE",
        "payload_state": payload_state,
        "protocol": protocol,
        "interface": interface,
        "payloads": payloads,
        "runtime_bindings": bindings,
        "deferred_values": deferred,
        "missing_required_mappings": missing,
        "retained_nonpayload_fields": retained_nonpayload_fields(
            obj["data"], MAPPED_TOP_LEVEL_FIELDS[object_type]
        ),
        "provenance": deepcopy(obj["provenance"]),
    }
    # A deterministic round trip also rejects unserializable accidental values.
    json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False)
    return result
