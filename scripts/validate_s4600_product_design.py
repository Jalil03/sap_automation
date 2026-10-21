"""Read-only validation of the proposed S4600 group-01 product design."""

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
DESIGNS = {
    "T-D101": {"ProductType": "DIEN", "ProductDescription": "Service de maintenance S4600", "BaseUnit": "H"},
    "T-MS101": {"ProductType": "HAWA", "ProductDescription": "Phare automobile S4600", "BaseUnit": "PC"},
    "T-MS201": {"ProductType": "HAWA", "ProductDescription": "Accessoire automobile S4600", "BaseUnit": "PC"},
}


def collection(client: UrllibSapTransport, entity: str, query: dict[str, str]) -> list[dict[str, object]]:
    response = client.request("GET", SERVICE + entity + "?" + urlencode(query))
    if response.status != 200:
        raise RuntimeError(f"{entity} GET failed: HTTP {response.status}")
    rows = response.json().get("d", {}).get("results")
    if not isinstance(rows, list):
        raise RuntimeError(f"{entity} response shape unknown")
    return rows


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is in scope")
    client = UrllibSapTransport(config)
    output: dict[str, object] = {"mode": "READ_ONLY", "targets": {}, "installed_combinations": {}}

    for logical_id, values in DESIGNS.items():
        key = client.request("GET", SERVICE + f"A_Product('{logical_id}')?" + urlencode({"$select": FIELDS}))
        aliases = collection(
            client,
            "A_Product",
            {"$filter": f"ProductOldID eq '{logical_id}'", "$select": FIELDS, "$top": "5"},
        )
        description = str(values["ProductDescription"]).replace("'", "''")
        descriptions = collection(
            client,
            "A_ProductDescription",
            {"$filter": f"ProductDescription eq '{description}'", "$select": "Product,Language,ProductDescription", "$top": "5"},
        )
        output["targets"][logical_id] = {
            "literal_key_http": key.status,
            "old_id_matches": aliases,
            "exact_description_matches": descriptions,
        }

    for label, product_type, base_unit in (
        ("DIEN_H", "DIEN", "H"),
        ("HAWA_PC", "HAWA", "PC"),
    ):
        output["installed_combinations"][label] = collection(
            client,
            "A_Product",
            {
                "$filter": f"ProductType eq '{product_type}' and BaseUnit eq '{base_unit}'",
                "$select": FIELDS,
                "$top": "10",
            },
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
