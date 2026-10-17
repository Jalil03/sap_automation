"""Create/read back the configured Phase 5 Product root via API_PRODUCT_SRV.

Plant and sales-view extensions are intentionally not attempted until their
seed dependencies are resolved. Existing roots are always skipped.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests
import urllib3
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED = ROOT / "config" / "s4615_training_seed.yaml"


def load_operation(path: Path, operation_id: str) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))["operations"][operation_id]


def value(operation: dict[str, Any], field: str) -> Any:
    return operation["fields"][field]["value"]


def root_payload(operation: dict[str, Any]) -> dict[str, Any]:
    return {
        "Product": operation["target"]["material_id"],
        "ProductType": value(operation, "material_type"),
        "IndustrySector": value(operation, "industry_sector"),
        "BaseUnit": value(operation, "base_unit"),
        "Division": value(operation, "sales_division"),
        "ItemCategoryGroup": value(operation, "item_category_group"),
        "ProductGroup": value(operation, "product_group"),
    }


class ProductApi:
    def __init__(self) -> None:
        load_dotenv()
        self.base = os.environ["SAP_BASE_URL"].rstrip("/")
        self.client = os.environ["SAP_CLIENT"]
        self.username = os.environ["SAP_USERNAME"]
        self.auth = (self.username, os.environ["SAP_PASSWORD"])
        self.verify = os.getenv("SAP_VERIFY_SSL", os.getenv("SAP_VERIFY_TLS", "true")).lower() == "true"
        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.client != "600" or self.username.upper() != "ABDELJ":
            raise RuntimeError("Phase 5 Product execution requires client 600 / user ABDELJ")
        self.root = f"{self.base}/sap/opu/odata/sap/API_PRODUCT_SRV"
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = self.verify

    def get(self, path: str, select: str) -> requests.Response:
        return self.session.get(
            f"{self.root}/{path}", params={"sap-client": self.client, "$select": select},
            headers={"Accept": "application/json"}, timeout=30,
        )

    def fresh_get(self, path: str, select: str) -> requests.Response:
        with requests.Session() as session:
            session.auth = self.auth
            session.verify = self.verify
            return session.get(
                f"{self.root}/{path}", params={"sap-client": self.client, "$select": select},
                headers={"Accept": "application/json"}, timeout=30,
            )

    def post(self, entity_set: str, payload: dict[str, Any]) -> requests.Response:
        token_response = self.session.get(
            f"{self.root}/", params={"sap-client": self.client},
            headers={"Accept": "application/json", "X-CSRF-Token": "Fetch"}, timeout=30,
        )
        token = token_response.headers.get("X-CSRF-Token")
        if token_response.status_code != 200 or not token:
            raise RuntimeError(f"CSRF fetch failed: HTTP {token_response.status_code}")
        return self.session.post(
            f"{self.root}/{entity_set}", params={"sap-client": self.client},
            headers={"Accept": "application/json", "Content-Type": "application/json", "X-CSRF-Token": token},
            data=json.dumps(payload), timeout=30,
        )


def error(response: requests.Response) -> str:
    try:
        return " ".join(response.json()["error"]["message"]["value"].split())
    except (ValueError, KeyError, TypeError):
        return " ".join(response.text.split())[:500]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, default=DEFAULT_SEED)
    parser.add_argument("--operation", default="PRODUCT_P615_400")
    args = parser.parse_args()
    operation = load_operation(args.seed, args.operation)
    payload = root_payload(operation)
    product = payload["Product"]
    key = f"A_Product('{product}')"
    select = "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup,ProductGroup"
    api = ProductApi()
    lookup = api.get(key, select)
    status = "EXISTS"
    if lookup.status_code == 404:
        created = api.post("A_Product", payload)
        if created.status_code not in (200, 201, 204):
            raise RuntimeError(f"A_Product create HTTP {created.status_code}: {error(created)}")
        status = "CREATED"
    elif lookup.status_code != 200:
        raise RuntimeError(f"A_Product lookup HTTP {lookup.status_code}: {error(lookup)}")
    readback = api.fresh_get(key, select)
    if readback.status_code != 200:
        raise RuntimeError(f"A_Product readback HTTP {readback.status_code}: {error(readback)}")
    row = {k: v for k, v in readback.json()["d"].items() if k != "__metadata"}
    if row.get("Product") != product:
        raise RuntimeError("A_Product readback identity mismatch")
    print(json.dumps({"root": f"{status}_AND_VERIFIED", "readback": row}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
