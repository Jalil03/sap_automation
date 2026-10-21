"""Prepared, non-writable S4615 plant/SD/LE customizing contracts."""

from __future__ import annotations

from typing import Any


READ_CONTRACTS = {
    "S4615_TRAINING_PLANT": (
        {"table": "T001W", "keys": ("WERKS",)},
        {"table": "T001K", "keys": ("BWKEY", "BUKRS")},
    ),
    "S4615_SALES_CHANNEL_PLANT": ({"table": "TVKWZ", "keys": ("VKORG", "VTWEG", "WERKS")},),
    "S4615_PLANT_SHIPPING_POINT": (
        {"table": "TVST", "keys": ("VSTEL",)},
        {"table": "TVSWZ", "keys": ("WERKS", "VSTEL")},
    ),
    "S4615_OVL2_DETERMINATION": (
        {"transaction": "OVL2", "view": "V_TVSTZ", "keys": ("VSBED", "LADGR", "WERKS", "VSTEL")},
    ),
}


def prepare_customizing_contract(operation: str, target: dict[str, Any]) -> dict[str, Any]:
    """Specify exact lookup/readback keys; never manufacture GUI write controls."""
    if operation not in READ_CONTRACTS:
        raise ValueError(f"No S4615 customizing contract for {operation}")
    required = {
        "S4615_TRAINING_PLANT": ("plant", "company_code", "valuation_area"),
        "S4615_SALES_CHANNEL_PLANT": ("sales_organization", "distribution_channel", "plant"),
        "S4615_PLANT_SHIPPING_POINT": ("plant", "shipping_point"),
        "S4615_OVL2_DETERMINATION": ("shipping_condition", "loading_group", "plant", "shipping_point"),
    }[operation]
    missing = [key for key in required if target.get(key) in (None, "")]
    if target.get("plant") == "1710":
        raise ValueError("1710 cannot be silently used for the non-intercompany training plant")
    return {
        "operation": operation, "status": "BLOCKED", "write_route_ready": False,
        "read_contract": list(READ_CONTRACTS[operation]),
        "lookup_before_write": True, "independent_readback": True,
        "missing_target_keys": missing,
        "missing_write_evidence": [
            "exact maintenance transaction and screen",
            "exact create/copy controls and writable field IDs",
            "save/transport behavior and post-save persistence contract",
            "scoped SAP authorization for A4H/600/ABDELJ",
        ],
        "forbidden": ["DELETE", "TRANSPORT_RELEASE", "MATERIAL_LEDGER_CHANGE", "GLOBAL_CURRENCY_CHANGE"],
    }
