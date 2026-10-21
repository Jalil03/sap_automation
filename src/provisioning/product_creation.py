"""Offline BAPI/MM01 route assessment for a new S4615 training product."""

from __future__ import annotations

from typing import Any

from src.sap_mapping.bapi import map_material


def prepare_material_bapi(
    values: dict[str, Any], *, installed_signature: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Reuse the Phase 2 mapper but never claim a complete accounting create."""
    required = (
        "sap_material_id", "material_type", "industry_sector", "base_unit",
        "sales_organization", "distribution_channel", "plant",
        "valuation_class", "price_control", "price_determination",
        "standard_price", "valuation_currency",
    )
    missing = [name for name in required if values.get(name) in (None, "", "ADMIN_CONFIRMATION_REQUIRED")]
    if values.get("plant") == "1710" or values.get("sap_material_id") == "10000287":
        raise ValueError("Protected valuation area/material cannot be used as target")
    blockers = []
    if missing:
        blockers.append({"code": "DATA_REQUIRED", "fields": missing})
    if installed_signature is None:
        blockers.append({"code": "INSTALLED_BAPI_SIGNATURE_REQUIRED", "function": "BAPI_MATERIAL_SAVEDATA"})
    else:
        params = installed_signature.get("parameters")
        if not isinstance(params, dict) or not {"HEADDATA", "CLIENTDATA", "SALESDATA", "PLANTDATA"}.issubset(params):
            blockers.append({"code": "INSTALLED_BAPI_SIGNATURE_INCOMPLETE"})
    # The current Phase 2 mapper has no valuation/accounting structures and
    # therefore cannot create a PGI-ready FERT, even with all values supplied.
    blockers.extend([
        {"code": "VALUATION_MAPPER_CONTRACT_REQUIRED"},
        {"code": "RFC_COMMIT_AND_READBACK_CONTRACT_REQUIRED"},
    ])
    payloads = []
    if not missing:
        material = {"data": {
            "material_id": values["sap_material_id"],
            "material_type": values["material_type"],
            "industry_sector": values["industry_sector"],
            "base_unit": values["base_unit"],
            "sales_organization": values["sales_organization"],
            "distribution_channel": values["distribution_channel"],
            "plants": [values["plant"]],
            "description": values.get("description"),
            "delivering_plant": values.get("delivering_plant"),
            "item_category_group": values.get("item_category_group"),
            "availability_check": values.get("availability_check"),
        }}
        payloads, _, _, mapping_missing = map_material(material)
        if mapping_missing:
            blockers.append({"code": "BAPI_MAPPING_INCOMPLETE", "fields": mapping_missing})
    return {"interface": "BAPI_MATERIAL_SAVEDATA", "status": "BLOCKED",
            "write_route_ready": False, "payloads": payloads, "blockers": blockers}


def prepare_mm01_fallback(*, captured_contract: dict[str, Any] | None = None) -> dict[str, Any]:
    required = ("lookup_controls", "create_controls", "plant_view_controls",
                "accounting_view_controls", "save_controls", "readback_controls")
    missing = [name for name in required if not (captured_contract or {}).get(name)]
    return {"interface": "MM01", "status": "BLOCKED", "write_route_ready": False,
            "missing_evidence": missing or ["live transition/commit behavior not validated"]}
