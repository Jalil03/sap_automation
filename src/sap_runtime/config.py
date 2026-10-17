from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .errors import ConfigurationError


@dataclass(frozen=True)
class SapRuntimeConfig:
    base_url: str
    client: str
    username: str
    password: str
    timeout_seconds: float = 30.0
    verify_tls: bool = True
    ledger_path: Path = Path("var/sap_runtime/execution_ledger.sqlite3")
    precheck_config_path: Path | None = None
    ci_approval_id: str | None = None

    @classmethod
    def from_env(cls) -> "SapRuntimeConfig":
        required = ["SAP_BASE_URL", "SAP_CLIENT", "SAP_USERNAME", "SAP_PASSWORD"]
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise ConfigurationError(f"Missing environment variables: {', '.join(missing)}")
        base_url = os.environ["SAP_BASE_URL"].rstrip("/")
        parsed = urlparse(base_url)
        allow_insecure = os.environ.get("SAP_ALLOW_INSECURE_HTTP", "false").lower() == "true"
        if parsed.scheme != "https" and not allow_insecure:
            raise ConfigurationError("SAP_BASE_URL must use HTTPS unless SAP_ALLOW_INSECURE_HTTP=true")
        client = os.environ["SAP_CLIENT"]
        if not (client.isdigit() and len(client) == 3):
            raise ConfigurationError("SAP_CLIENT must contain exactly three digits")
        precheck = os.environ.get("SAP_PRECHECK_CONFIG")
        return cls(
            base_url=base_url,
            client=client,
            username=os.environ["SAP_USERNAME"],
            password=os.environ["SAP_PASSWORD"],
            timeout_seconds=float(os.environ.get("SAP_TIMEOUT_SECONDS", "30")),
            verify_tls=os.environ.get(
                "SAP_VERIFY_TLS", os.environ.get("SAP_VERIFY_SSL", "true")
            ).lower() == "true",
            ledger_path=Path(os.environ.get("SAP_LEDGER_PATH", "var/sap_runtime/execution_ledger.sqlite3")),
            precheck_config_path=Path(precheck) if precheck else None,
            ci_approval_id=os.environ.get("SAP_EXECUTION_APPROVAL_ID"),
        )
