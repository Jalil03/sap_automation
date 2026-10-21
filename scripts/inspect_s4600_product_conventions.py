"""Targeted read-only evidence for S4600 Basic Data product candidates."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_PRODUCT_SRV/"
FIELDS = "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division"


def rows(client: UrllibSapTransport, entity: str, query: dict[str, str]) -> list[dict[str, object]]:
    response = client.request("GET", SERVICE + entity + "?" + urlencode(query))
    if response.status != 200:
        raise RuntimeError(f"{entity} lookup failed: HTTP {response.status}")
    result = response.json().get("d", {}).get("results")
    if not isinstance(result, list):
        raise RuntimeError(f"{entity} response shape is unknown")
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is in scope")
    client = UrllibSapTransport(config)
    evidence: dict[str, object] = {"mode": "READ_ONLY", "examples": {}}

    for product in ("10000289", "10000287"):
        root = client.request(
            "GET", SERVICE + f"A_Product('{product}')?" + urlencode({"$select": FIELDS})
        )
        descriptions = rows(
            client,
            "A_ProductDescription",
            {"$filter": f"Product eq '{product}'", "$select": "Product,Language,ProductDescription"},
        )
        evidence["examples"][product] = {
            "root_http": root.status,
            "root": root.json().get("d", {}) if root.status == 200 else {},
            "descriptions": descriptions,
        }

    for product_type in ("DIEN", "HAWA"):
        found = rows(
            client,
            "A_Product",
            {"$filter": f"ProductType eq '{product_type}'", "$select": FIELDS, "$top": "5"},
        )
        compact = []
        for product in found:
            product_id = str(product.get("Product") or "")
            descriptions = rows(
                client,
                "A_ProductDescription",
                {"$filter": f"Product eq '{product_id}'", "$select": "Language,ProductDescription", "$top": "3"},
            )
            compact.append({"root": product, "descriptions": descriptions})
        evidence["examples"][f"ProductType={product_type}"] = compact

    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
