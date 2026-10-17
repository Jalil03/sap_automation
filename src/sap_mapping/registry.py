from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .errors import MappingContractError, UnsupportedObjectTypeError

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "mappings/sap/interface_registry.yaml"
WRITABLE_CORE = frozenset({
    "BUSINESS_PARTNER",
    "MATERIAL",
    "SALES_ORDER",
    "PRICING_CONDITION",
    "OUTBOUND_DELIVERY",
    "BILLING",
})
WRITABLE_CLASSES = frozenset({"ODATA", "STANDARD_BAPI", "RFC_FUNCTION"})


@lru_cache(maxsize=1)
def load_registry() -> dict:
    # Phase 2A emits YAML 1.2 using its JSON-compatible deterministic form.
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def preferred_interface(object_type: str) -> dict:
    if object_type not in WRITABLE_CORE:
        raise UnsupportedObjectTypeError(f"No Phase 2B writable-core mapper for {object_type}")
    entry = load_registry()["object_types"].get(object_type)
    if not entry:
        raise MappingContractError(f"{object_type} is absent from the interface registry")
    preferred = entry["preferred_interface"]
    if entry["resolution"] != "RESOLVED" or preferred["classification"] not in WRITABLE_CLASSES:
        raise MappingContractError(
            f"{object_type} preferred interface is not writable: {preferred['classification']}"
        )
    return preferred
