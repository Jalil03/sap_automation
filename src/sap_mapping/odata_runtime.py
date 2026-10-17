from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse


IDENTITY_PATTERN = re.compile(r"/(?P<entity_set>A_[A-Za-z0-9_]+)\((?P<key>.*)\)$")


def load_odata_v2_results(path: str | Path) -> list[dict]:
    """Load a captured OData V2 JSON response from disk; performs no network I/O."""
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or set(value) != {"d"}:
        raise ValueError("Expected an OData V2 JSON object containing only 'd'")
    data = value["d"]
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError("Expected OData V2 collection envelope d.results")
    if not all(isinstance(item, dict) for item in data["results"]):
        raise ValueError("Every d.results entry must be an object")
    return data["results"]


def parse_entity_identity(uri: str) -> dict:
    """Parse entity-set and string key predicates from a captured entity URI."""
    path = unquote(urlparse(uri).path)
    match = IDENTITY_PATTERN.search(path)
    if not match:
        raise ValueError(f"Unrecognized OData entity URI path: {path!r}")
    raw_key = match.group("key")
    key_values: dict[str, str] = {}
    if "=" not in raw_key:
        key_values["$value"] = _odata_string(raw_key)
    else:
        for component in raw_key.split(","):
            name, raw_value = component.split("=", 1)
            key_values[name] = _odata_string(raw_value)
    return {
        "entity_set": match.group("entity_set"),
        "keys": key_values,
        "path": path,
    }


def _odata_string(value: str) -> str:
    value = value.strip()
    if len(value) < 2 or not (value.startswith("'") and value.endswith("'")):
        raise ValueError(f"Expected quoted OData string key, got {value!r}")
    return value[1:-1].replace("''", "'")
