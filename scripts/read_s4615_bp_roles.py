"""Two exact, read-only role checks for existing S4615 BP 1000000115."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    for role in ("FLCU00", "FLCU01"):
        path = (
            "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
            f"A_BusinessPartnerRole(BusinessPartner='1000000115',BusinessPartnerRole='{role}')"
        )
        print(f"{role}: HTTP {client.request('GET', path).status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
