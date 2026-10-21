"""Bounded, read-only duplicate search for the S4600 group-01 bootstrap.

The script never infers global absence from a negative logical-ID lookup. It
records only the exact key/alias/name searches needed by the approval manifest.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


CUSTOMERS = ("T-S50A01", "T-S50B01")
PRODUCTS = ("T-MS101", "T-MS201", "T-MS301", "T-F101", "T-D101")
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_bootstrap_group01.json"


def get(client: UrllibSapTransport, service: str, entity: str, **query: str) -> dict:
    path = f"sap/opu/odata/sap/{service}/{entity}"
    if query:
        path += "?" + urlencode(query)
    response = client.request("GET", path)
    result: dict = {"http_status": response.status}
    if response.status == 404:
        result["classification"] = "KEY_NOT_FOUND"
        return result
    if response.status != 200:
        result["classification"] = "READ_ERROR"
        result["error"] = response.sanitized_sap_error()
        return result
    payload = response.json().get("d", {})
    rows = payload.get("results") if isinstance(payload, dict) else None
    if isinstance(rows, list):
        clean = [{k: v for k, v in row.items() if k != "__metadata"} for row in rows]
        result.update(classification="ROWS_RETURNED", count=len(clean), rows=clean)
    elif isinstance(payload, dict):
        result.update(
            classification="EXACT_KEY_RETURNED",
            row={k: v for k, v in payload.items() if k != "__metadata"},
        )
    else:
        result["classification"] = "UNEXPECTED_RESPONSE_SHAPE"
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise SystemExit("S4600 audit requires A4H client 600 / user ABDELJ")
    client = UrllibSapTransport(config)
    evidence: dict = {
        "schema_version": 1,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": config.client, "user": config.username.upper()},
        "mode": "READ_ONLY",
        "scope": "S4600_GROUP01_BOOTSTRAP",
        "customers": {},
        "products": {},
        "bounded_name_searches": {},
        "interpretation_rule": "Negative logical-ID/alias searches do not prove global absence.",
    }
    for logical_id in CUSTOMERS:
        literal = logical_id.replace("'", "''")
        evidence["customers"][logical_id] = {
            "business_partner_key": get(
                client, "API_BUSINESS_PARTNER", f"A_BusinessPartner('{logical_id}')",
                **{"$select": "BusinessPartner,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1"},
            ),
            "customer_key": get(
                client, "API_BUSINESS_PARTNER", f"A_Customer('{logical_id}')",
                **{"$select": "Customer"},
            ),
            "external_id": get(
                client, "API_BUSINESS_PARTNER", "A_BusinessPartner",
                **{
                    "$filter": f"BusinessPartnerIDByExtSystem eq '{literal}'",
                    "$select": "BusinessPartner,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1",
                    "$top": "20",
                },
            ),
            "search_term": get(
                client, "API_BUSINESS_PARTNER", "A_BusinessPartner",
                **{
                    "$filter": f"SearchTerm1 eq '{literal}'",
                    "$select": "BusinessPartner,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1",
                    "$top": "20",
                },
            ),
        }
    evidence["bounded_name_searches"]["Motormarkt Heidelberg"] = get(
        client, "API_BUSINESS_PARTNER", "A_BusinessPartner",
        **{
            "$filter": "OrganizationBPName1 eq 'Motormarkt Heidelberg'",
            "$select": "BusinessPartner,BusinessPartnerIDByExtSystem,SearchTerm1,OrganizationBPName1",
            "$top": "20",
        },
    )
    for logical_id in PRODUCTS:
        literal = logical_id.replace("'", "''")
        evidence["products"][logical_id] = {
            "product_key": get(
                client, "API_PRODUCT_SRV", f"A_Product('{logical_id}')",
                **{"$select": "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup"},
            ),
            "old_id": get(
                client, "API_PRODUCT_SRV", "A_Product",
                **{
                    "$filter": f"ProductOldID eq '{literal}'",
                    "$select": "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division,ItemCategoryGroup",
                    "$top": "20",
                },
            ),
        }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "environment": evidence["environment"],
        "mode": evidence["mode"],
        "output": str(OUTPUT.relative_to(ROOT)),
        "customers": {
            key: {name: value.get("classification") for name, value in checks.items()}
            for key, checks in evidence["customers"].items()
        },
        "products": {
            key: {name: value.get("classification") for name, value in checks.items()}
            for key, checks in evidence["products"].items()
        },
        "name_search": evidence["bounded_name_searches"]["Motormarkt Heidelberg"].get("classification"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
