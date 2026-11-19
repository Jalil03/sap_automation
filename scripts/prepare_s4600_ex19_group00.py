"""GET-only preflight and exact candidate payload for S4600 exercise 19."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.prepare_s4600_ex3_group00 import get, odata_date
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex19_group00_odata_preflight_2026-10-22.json"

PAYLOAD = {
    "SalesOrderType": "CS",
    "SalesOrganization": "FR10",
    "DistributionChannel": "10",
    "OrganizationDivision": "1W",
    "SoldToParty": "1000000112",
    "PurchaseOrderByCustomer": "6-400",
    "CustomerPurchaseOrderDate": odata_date("2026-10-22"),
    "RequestedDeliveryDate": odata_date("2026-10-29"),
    "to_Item": [
        {
            "SalesOrderItem": "10",
            "Material": "10000282",
            "RequestedQuantity": "5",
            "RequestedQuantityUnit": "289",
            "to_Partner": [
                {"PartnerFunction": "RM", "Customer": "1000000112"}
            ],
        },
        {
            "SalesOrderItem": "20",
            "Material": "10000284",
            "RequestedQuantity": "1",
            "RequestedQuantityUnit": "289",
            "to_Partner": [
                {"PartnerFunction": "RM", "Customer": "1000000113"}
            ],
        },
    ],
}


def fingerprint() -> str:
    raw = json.dumps(PAYLOAD, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    duplicate = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        "SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '6-400'"
    )
    checks = {
        "duplicate": get(client, "API_SALES_ORDER_SRV", "A_SalesOrder", {
            "$filter": duplicate, "$select": "SalesOrder", "$top": "2",
        }),
        "historical_item_partner_shape": get(
            client, "API_SALES_ORDER_SRV", "A_SalesOrderItemPartner", {
                "$select": "SalesOrder,SalesOrderItem,PartnerFunction,Customer",
                "$top": "50",
            },
        ),
    }
    for customer in ("1000000112", "1000000113"):
        checks[f"customer_{customer}"] = get(
            client, "API_BUSINESS_PARTNER", "A_CustomerSalesArea", {
                "$filter": (
                    f"Customer eq '{customer}' and SalesOrganization eq 'FR10' and "
                    "DistributionChannel eq '10' and Division eq '1W'"
                ),
                "$select": "Customer,CustomerPaymentTerms,SupplyingPlant,Currency,ShippingCondition",
                "$top": "1",
            },
        )
    for product in ("10000282", "10000284"):
        checks[f"product_{product}_sales"] = get(
            client, "API_PRODUCT_SRV", "A_ProductSalesDelivery", {
                "$filter": (
                    f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and "
                    "ProductDistributionChnl eq '10'"
                ),
                "$select": "Product,SupplyingPlant,ItemCategoryGroup",
                "$top": "1",
            },
        )
        checks[f"product_{product}_plant"] = get(
            client, "API_PRODUCT_SRV", "A_ProductPlant", {
                "$filter": f"Product eq '{product}' and Plant eq 'FR10'",
                "$select": "Product,Plant,AvailabilityCheckType",
                "$top": "1",
            },
        )
        checks[f"product_{product}_unit"] = get(
            client, "API_PRODUCT_SRV", "A_ProductUnitsOfMeasure", {
                "$filter": f"Product eq '{product}' and AlternativeUnit eq '289'",
                "$select": "Product,AlternativeUnit",
                "$top": "1",
            },
        )
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "operation": "PREPARE_ONE_S4600_EX19_GROUP00_SALES_ORDER",
        "candidate_payload_not_submitted": PAYLOAD,
        "payload_sha256": fingerprint(),
        "contract_status": (
            "Item-partner fields and French external partner function RM are evidenced by live metadata and readback. "
            "Deep-create behavior remains unproven until an explicitly approved one-shot POST."
        ),
        "checks": checks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "payload_sha256": evidence["payload_sha256"],
        "checks": {name: value["classification"] for name, value in checks.items()},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
