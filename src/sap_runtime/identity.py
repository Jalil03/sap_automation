"""Resolve logical canonical identities to live SAP identities at runtime only."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from .errors import PreflightBlocked


def load_verified_identity_mappings(path: str | Path) -> dict[str, str]:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    records = document.get("mappings")
    if not isinstance(records, dict):
        raise PreflightBlocked("Identity mapping store must contain a mappings object")
    resolved: dict[str, str] = {}
    for logical_id, record in records.items():
        if not isinstance(record, dict) or record.get("logical_id") != logical_id:
            raise PreflightBlocked(f"Invalid identity mapping record: {logical_id}")
        if record.get("status") != "LIVE_VERIFIED":
            continue
        sap_id = record.get("sap_id")
        if not isinstance(sap_id, str) or not sap_id:
            raise PreflightBlocked(f"Verified identity mapping lacks sap_id: {logical_id}")
        resolved[logical_id] = sap_id
    return resolved


def resolve_sales_order_payload_identities(
    payload: dict[str, Any], mappings: dict[str, str]
) -> dict[str, Any]:
    """Return a resolved payload copy; never mutate canonical/mapped input."""
    resolved = deepcopy(payload)
    sold_to = resolved.get("SoldToParty")
    if isinstance(sold_to, str) and sold_to in mappings:
        resolved["SoldToParty"] = mappings[sold_to]
    for item in resolved.get("to_Item", []):
        material = item.get("Material")
        if isinstance(material, str) and material in mappings:
            item["Material"] = mappings[material]
    return resolved
