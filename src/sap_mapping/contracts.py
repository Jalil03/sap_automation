from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "schemas/sap/core_mapping_contracts.json"
PAYLOAD_SCHEMA_PATH = ROOT / "schemas/sap/payloads.schema.json"
BINDING_SCHEMA_PATH = ROOT / "schemas/sap/runtime_binding.schema.json"


@lru_cache(maxsize=1)
def mapping_contracts() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def payload_schemas() -> dict:
    return json.loads(PAYLOAD_SCHEMA_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def binding_schema() -> dict:
    return json.loads(BINDING_SCHEMA_PATH.read_text(encoding="utf-8"))
