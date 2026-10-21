"""Narrow read-only identity check for the S4600 execution-first batch."""

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


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is in scope")
    client = UrllibSapTransport(config)
    bp_service = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
    product_service = "sap/opu/odata/sap/API_PRODUCT_SRV/"
    output: dict[str, object] = {"mode": "READ_ONLY"}

    response = client.request(
        "GET",
        bp_service
        + "A_BusinessPartner('1000000116')?"
        + urlencode({"$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerCategory,OrganizationBPName1,SearchTerm1"}),
    )
    output["T-S50A01_key"] = {
        "http": response.status,
        "row": response.json().get("d", {}) if response.status == 200 else {},
    }
    query = urlencode(
        {
            "$filter": "SearchTerm1 eq 'T-S50A01'",
            "$select": "BusinessPartner,BusinessPartnerGrouping,BusinessPartnerCategory,OrganizationBPName1,SearchTerm1",
        }
    )
    response = client.request("GET", bp_service + "A_BusinessPartner?" + query)
    output["T-S50A01_marker"] = {
        "http": response.status,
        "rows": response.json().get("d", {}).get("results", []) if response.status == 200 else [],
    }

    for logical_id in ("T-D101", "T-MS101", "T-MS201"):
        select = "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division"
        literal = client.request(
            "GET",
            product_service + f"A_Product('{logical_id}')?" + urlencode({"$select": select}),
        )
        alias = client.request(
            "GET",
            product_service
            + "A_Product?"
            + urlencode({"$filter": f"ProductOldID eq '{logical_id}'", "$select": select}),
        )
        output[logical_id] = {
            "literal_http": literal.status,
            "old_id_http": alias.status,
            "old_id_rows": alias.json().get("d", {}).get("results", []) if alias.status == 200 else [],
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
