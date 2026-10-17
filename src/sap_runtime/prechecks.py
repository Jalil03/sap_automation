from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

from .errors import ConfigurationError, TransportError
from .models import CheckResult
from .transport import SapTransport


REQUIRED_PROBES = frozenset({
    "CUSTOMER",
    "MATERIAL",
    "SALES_ORGANIZATION",
    "DISTRIBUTION_CHANNEL",
    "ORGANIZATION_DIVISION",
    "SALES_ORDER_TYPE",
    "UNIT_OF_MEASURE",
})


class DependencyVerifier(Protocol):
    def verify(self, payload: dict[str, Any], transport: SapTransport) -> list[CheckResult]: ...


def payload_context(payload: dict[str, Any]) -> dict[str, str]:
    item = payload["to_Item"][0]
    values = {
        "CUSTOMER": payload["SoldToParty"],
        "MATERIAL": item["Material"],
        "SALES_ORGANIZATION": payload["SalesOrganization"],
        "DISTRIBUTION_CHANNEL": payload["DistributionChannel"],
        "ORGANIZATION_DIVISION": payload["OrganizationDivision"],
        "SALES_ORDER_TYPE": payload["SalesOrderType"],
        "UNIT_OF_MEASURE": item["RequestedQuantityUnit"],
    }
    return {name: quote(str(value).replace("'", "''"), safe="") for name, value in values.items()}


class ConfiguredDependencyVerifier:
    """Run administrator-supplied read-only OData probes for referenced values."""

    def __init__(self, probes: list[dict[str, Any]], *, client: str):
        names = {probe.get("name") for probe in probes}
        missing = sorted(REQUIRED_PROBES - names)
        if missing:
            raise ConfigurationError(f"Precheck configuration is missing probes: {', '.join(missing)}")
        if len(probes) != len(REQUIRED_PROBES):
            raise ConfigurationError("Precheck configuration must define each of the seven probes once")
        for probe in probes:
            if probe["name"] not in REQUIRED_PROBES:
                raise ConfigurationError(f"Unsupported precheck name: {probe['name']}")
            status = probe.get("status", "CONFIRMED")
            if status not in {"CONFIRMED", "NEEDS_LIVE_VALIDATION"}:
                raise ConfigurationError(f"Unsupported precheck status: {status}")
            path = probe.get("path_template")
            if status == "CONFIRMED" and (not isinstance(path, str) or not path.startswith("/")):
                raise ConfigurationError(
                    "A CONFIRMED precheck requires an absolute-relative path_template"
                )
        self.probes = sorted(probes, key=lambda item: item["name"])
        self.client = client

    @classmethod
    def from_file(cls, path: str | Path, *, client: str) -> "ConfiguredDependencyVerifier":
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(value, dict) or not isinstance(value.get("probes"), list):
            raise ConfigurationError("Precheck file must contain a probes array")
        return cls(value["probes"], client=client)

    def verify(self, payload: dict[str, Any], transport: SapTransport) -> list[CheckResult]:
        context = payload_context(payload)
        results = []
        for probe in self.probes:
            name = probe["name"]
            if probe.get("status", "CONFIRMED") == "NEEDS_LIVE_VALIDATION":
                results.append(CheckResult(
                    name=f"DEPENDENCY_{name}",
                    status="BLOCKED",
                    detail="lookup contract is NEEDS_LIVE_VALIDATION; no request attempted",
                ))
                continue
            values = _probe_values(payload, name)
            statuses: list[tuple[int | None, bool]] = []
            try:
                for value in values:
                    item_context = dict(context)
                    item_context[name] = quote(str(value).replace("'", "''"), safe="")
                    path = probe["path_template"].format_map(item_context)
                    response = transport.request("GET", _with_client(path, self.client))
                    statuses.append((response.status, _odata_has_value(response.json())))
                valid = bool(statuses) and all(
                    status is not None and 200 <= status < 300 and found
                    for status, found in statuses
                )
                rendered = ", ".join(f"HTTP {status}" for status, _ in statuses)
                results.append(CheckResult(
                    name=f"DEPENDENCY_{name}",
                    status="PASS" if valid else "BLOCKED",
                    detail=f"{len(statuses)} read-only probe(s) returned {rendered}",
                ))
            except (TransportError, ValueError, json.JSONDecodeError, KeyError) as error:
                results.append(CheckResult(
                    name=f"DEPENDENCY_{name}",
                    status="BLOCKED",
                    detail=f"read-only probe failed: {type(error).__name__}",
                ))
        return results


def _probe_values(payload: dict[str, Any], name: str) -> list[str]:
    if name == "MATERIAL":
        values = [item.get("Material") for item in payload.get("to_Item", [])]
    elif name == "UNIT_OF_MEASURE":
        values = [item.get("RequestedQuantityUnit") for item in payload.get("to_Item", [])]
    else:
        reverse = {
            "CUSTOMER": "SoldToParty",
            "SALES_ORGANIZATION": "SalesOrganization",
            "DISTRIBUTION_CHANNEL": "DistributionChannel",
            "ORGANIZATION_DIVISION": "OrganizationDivision",
            "SALES_ORDER_TYPE": "SalesOrderType",
        }
        values = [payload.get(reverse[name])]
    return list(dict.fromkeys(str(value) for value in values if value not in (None, "")))


def _odata_has_value(value: dict) -> bool:
    data = value.get("d") if isinstance(value, dict) else None
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        return bool(data["results"])
    return isinstance(data, dict) and bool(data)


def _with_client(path: str, client: str) -> str:
    parts = urlsplit(path)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.setdefault("sap-client", client)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
