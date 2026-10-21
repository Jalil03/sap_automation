"""Read-only candidate evidence for S4600 HAWA item-category groups."""

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


def rows(client: UrllibSapTransport, entity: str, query: dict[str, str]) -> list[dict[str, object]]:
    response = client.request("GET", SERVICE + entity + "?" + urlencode(query))
    if response.status != 200:
        raise RuntimeError(f"{entity} lookup HTTP {response.status}")
    result = response.json().get("d", {}).get("results")
    if not isinstance(result, list):
        raise RuntimeError(f"{entity} response shape unknown")
    return [{key: value for key, value in item.items() if key != "__metadata"} for item in result]


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    roots = rows(client, "A_Product", {
        "$filter": "ProductType eq 'HAWA' and IndustrySector eq 'W' and ItemCategoryGroup ne ''",
        "$select": "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup",
        "$top": "50",
    })
    evidence = []
    for root in roots:
        product = str(root.get("Product") or "")
        sales = rows(client, "A_ProductSalesDelivery", {
            "$filter": f"Product eq '{product}'",
            "$select": "Product,ProductSalesOrg,ProductDistributionChnl,ItemCategoryGroup,SupplyingPlant,AccountDetnProductGroup",
            "$top": "20",
        })
        evidence.append({"root": root, "sales_delivery": sales})
    sales_candidates = rows(client, "A_ProductSalesDelivery", {
        "$filter": "ItemCategoryGroup ne ''",
        "$select": "Product,ProductSalesOrg,ProductDistributionChnl,ItemCategoryGroup,SupplyingPlant,AccountDetnProductGroup",
        "$top": "100",
    })
    for sales in sales_candidates:
        product = str(sales.get("Product") or "")
        response = client.request("GET", SERVICE + f"A_Product('{product}')?" + urlencode({
            "$select": "Product,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup",
        }))
        if response.status != 200:
            continue
        root = {key: value for key, value in response.json().get("d", {}).items() if key != "__metadata"}
        if root.get("ProductType") == "HAWA" and root.get("IndustrySector") == "W":
            evidence.append({"root": root, "sales_delivery": [sales]})
    candidates = sorted({
        str(value) for item in evidence
        for value in ([item["root"].get("ItemCategoryGroup")]
                      + [row.get("ItemCategoryGroup") for row in item["sales_delivery"]])
        if str(value or "").strip()
    })
    print(json.dumps({
        "mode": "READ_ONLY", "filter": "ProductType=HAWA, IndustrySector=W, nonblank ItemCategoryGroup",
        "candidate_item_category_groups": candidates, "examples": evidence,
        "selection_authorized": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
