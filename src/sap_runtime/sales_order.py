from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import date, datetime, time, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from jsonschema import Draft202012Validator

from src.sap_mapping import validate_runtime_contract
from src.training_context import PlaceholderResolver

from .config import SapRuntimeConfig
from .errors import AmbiguousTransportError, PreflightBlocked, TransportError
from .ledger import ExecutionLedger
from .identity import load_verified_identity_mappings, resolve_sales_order_payload_identities
from .models import CheckResult, ExecutionStatus, RuntimeResult
from .prechecks import DependencyVerifier
from .security import sanitize_error
from .transport import HttpResponse, SapTransport


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PATH = ROOT / "data/validated/canonical_objects.json"
WRITE_SCHEMA_PATH = ROOT / "schemas/sap/sales_order_write_runtime.schema.json"
SERVICE_ROOT = "/sap/opu/odata/sap/API_SALES_ORDER_SRV"
ENTITY_SET = "A_SalesOrder"
RESERVED_REFERENCES = frozenset({"TECH-PILOT-001"})

HEADER_READ_FIELDS = (
    "SalesOrder", "SalesOrderType", "SalesOrganization", "DistributionChannel",
    "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
    "CustomerPurchaseOrderDate", "CustomerPaymentTerms", "TransactionCurrency",
    "TotalNetAmount",
)
ITEM_READ_FIELDS = (
    "SalesOrderItem", "Material", "RequestedQuantity", "RequestedQuantityUnit",
    "RequestedQuantitySAPUnit", "RequestedQuantityISOUnit", "ProductionPlant",
    "ShippingPoint",
)
PARTNER_READ_FIELDS = ("PartnerFunction", "PartnerFunctionInternalCode", "Customer")


def _canonical_json(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _payload_sha256(payload: dict) -> str:
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def _placeholder_paths(value: Any, path: str = "payload") -> list[str]:
    if isinstance(value, str):
        return [path] if "##" in value else []
    if isinstance(value, list):
        found: list[str] = []
        for index, item in enumerate(value):
            found.extend(_placeholder_paths(item, f"{path}[{index}]"))
        return found
    if isinstance(value, dict):
        found = []
        for key, item in value.items():
            found.extend(_placeholder_paths(item, f"{path}.{key}"))
        return found
    return []


def _correlation_id(object_id: str, payload_hash: str) -> str:
    value = hashlib.sha256(f"{object_id}|{payload_hash}".encode("utf-8")).hexdigest()[:20].upper()
    return f"SO-RUNTIME-{value}"


def _decimal_string(value: Any) -> str:
    try:
        decimal = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise PreflightBlocked(f"Invalid Edm.Decimal value: {value!r}") from error
    rendered = format(decimal, "f")
    return rendered.rstrip("0").rstrip(".") if "." in rendered else rendered


def _odata_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise PreflightBlocked("Customer purchase order date must be YYYY-MM-DD") from error
    instant = datetime.combine(parsed, time.min, tzinfo=timezone.utc)
    return f"/Date({int(instant.timestamp() * 1000)})/"


def _odata_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _query(path: str, **parameters: str) -> str:
    return path + "?" + urlencode(parameters, safe="$,()'/")


def _results(response: HttpResponse) -> list[dict]:
    value = response.json()
    data = value.get("d") if isinstance(value, dict) else None
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ValueError("Expected OData V2 d.results response")
    return data["results"]


class SalesOrderRuntime:
    def __init__(
        self,
        *,
        config: SapRuntimeConfig,
        transport: SapTransport,
        ledger: ExecutionLedger,
        dependency_verifier: DependencyVerifier,
        canonical_path: Path = CANONICAL_PATH,
        identity_mapping_path: Path | None = None,
    ):
        self.config = config
        self.transport = transport
        self.ledger = ledger
        self.dependency_verifier = dependency_verifier
        self.canonical_path = canonical_path
        self.identity_mapping_path = identity_mapping_path
        self._write_schema = json.loads(WRITE_SCHEMA_PATH.read_text(encoding="utf-8"))

    def _objects(self) -> tuple[list[dict], dict[str, dict]]:
        objects = json.loads(self.canonical_path.read_text(encoding="utf-8"))["objects"]
        return objects, {obj["object_id"]: obj for obj in objects}

    def _prepare_payload(
        self,
        object_id: str,
        *,
        customer_reference: str | None = None,
        customer_purchase_order_date: str | None = None,
        training_user_code: str | None = None,
    ) -> tuple[dict, dict, dict[str, Any] | None]:
        _, index = self._objects()
        obj = index.get(object_id)
        if obj is None or obj.get("object_type") != "SALES_ORDER":
            raise PreflightBlocked(f"Unknown SALES_ORDER object: {object_id}")
        training_context = None
        if training_user_code is not None:
            resolution = PlaceholderResolver().resolve(obj, training_user_code)
            obj = resolution.canonical_object
            index = dict(index)
            index[object_id] = obj
            training_context = resolution.trace_metadata()
        mapped = validate_runtime_contract(obj, object_index=index)
        if mapped["runtime_status"] != "EXECUTION_READY":
            raise PreflightBlocked(
                f"Canonical object is not EXECUTION_READY: {mapped['runtime_status']}"
            )
        source = mapped["payloads"][0]["body"]
        payload = {
            field: deepcopy(source[field])
            for field in (
                "SalesOrderType", "SalesOrganization", "DistributionChannel",
                "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
            )
            if field in source
        }
        if customer_reference is not None:
            if not customer_reference or len(customer_reference) > 35:
                raise PreflightBlocked("Customer reference must contain 1 to 35 characters")
            payload["PurchaseOrderByCustomer"] = customer_reference
        if customer_purchase_order_date is not None:
            payload["CustomerPurchaseOrderDate"] = _odata_date(customer_purchase_order_date)
        payload["to_Item"] = []
        for item in source.get("to_Item", []):
            minimal = {
                field: deepcopy(item[field])
                for field in (
                    "SalesOrderItem", "Material", "RequestedQuantity", "RequestedQuantityUnit"
                )
                if field in item
            }
            if "RequestedQuantity" in minimal:
                minimal["RequestedQuantity"] = _decimal_string(minimal["RequestedQuantity"])
            payload["to_Item"].append(minimal)
        if self.identity_mapping_path is not None:
            payload = resolve_sales_order_payload_identities(
                payload,
                load_verified_identity_mappings(self.identity_mapping_path),
            )
        placeholder_paths = _placeholder_paths(payload)
        if placeholder_paths:
            raise PreflightBlocked(
                "Runtime payload contains unresolved ## at " + ", ".join(placeholder_paths)
            )
        errors = sorted(
            Draft202012Validator(self._write_schema).iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        if errors:
            details = "; ".join(
                f"{'.'.join(map(str, error.absolute_path))}: {error.message}" for error in errors
            )
            raise PreflightBlocked(f"Runtime write payload invalid: {details}")
        return obj, payload, training_context

    def build_payload(
        self,
        object_id: str,
        *,
        customer_reference: str | None = None,
        customer_purchase_order_date: str | None = None,
        training_user_code: str | None = None,
    ) -> tuple[dict, dict]:
        """Build a payload while keeping the historical two-value public return shape."""
        obj, payload, _ = self._prepare_payload(
            object_id,
            customer_reference=customer_reference,
            customer_purchase_order_date=customer_purchase_order_date,
            training_user_code=training_user_code,
        )
        return obj, payload

    def dry_run(
        self,
        object_id: str,
        *,
        customer_reference: str | None = None,
        customer_purchase_order_date: str | None = None,
        training_user_code: str | None = None,
    ) -> RuntimeResult:
        obj, payload, training_context = self._prepare_payload(
            object_id,
            customer_reference=customer_reference,
            customer_purchase_order_date=customer_purchase_order_date,
            training_user_code=training_user_code,
        )
        return self._preflight(
            obj, payload, mode="DRY_RUN", record=True, training_context=training_context
        )

    def execute(
        self,
        object_id: str,
        *,
        customer_reference: str,
        customer_purchase_order_date: str | None,
        training_user_code: str | None = None,
        allow_canonical_reference: bool = False,
    ) -> RuntimeResult:
        obj, payload, training_context = self._prepare_payload(
            object_id,
            customer_reference=customer_reference,
            customer_purchase_order_date=customer_purchase_order_date,
            training_user_code=training_user_code,
        )
        original_reference = obj["data"].get("customer_reference")
        if customer_reference in RESERVED_REFERENCES:
            raise PreflightBlocked(f"Reserved reference must never be recreated: {customer_reference}")
        if customer_reference == original_reference and not allow_canonical_reference:
            raise PreflightBlocked("EXECUTE requires a new customer reference, not the canonical source reference")
        payload_hash = _payload_sha256(payload)
        if not self.ledger.has_successful_dry_run(object_id, payload_hash):
            raise PreflightBlocked("No successful dry-run exists for this exact payload SHA-256")

        preflight = self._preflight(
            obj, payload, mode="EXECUTE_PREFLIGHT", record=False,
            training_context=training_context,
        )
        if preflight.status != ExecutionStatus.DRY_RUN_OK:
            return preflight
        try:
            token_response = self.transport.request(
                "GET",
                _query(f"{SERVICE_ROOT}/", **{"sap-client": self.config.client}),
                headers={"X-CSRF-Token": "Fetch"},
            )
        except TransportError as error:
            return self._record_terminal(
                obj, payload, "EXECUTE", ExecutionStatus.BLOCKED,
                error=f"CSRF token fetch failed: {type(error).__name__}",
                training_context=training_context,
            )
        token = token_response.header("X-CSRF-Token")
        if token_response.status != 200 or not token:
            return self._record_terminal(
                obj, payload, "EXECUTE", ExecutionStatus.BLOCKED,
                http_status=token_response.status,
                error="CSRF token fetch did not return HTTP 200 with a token header",
                training_context=training_context,
            )

        correlation_id = _correlation_id(object_id, payload_hash)
        entry_id = self.ledger.start(
            canonical_object_id=object_id,
            correlation_id=correlation_id,
            customer_reference=payload["PurchaseOrderByCustomer"],
            payload_sha256=payload_hash,
            mode="EXECUTE",
            status=ExecutionStatus.SUBMITTED,
        )
        try:
            response = self.transport.request(
                "POST",
                _query(f"{SERVICE_ROOT}/{ENTITY_SET}", **{"sap-client": self.config.client}),
                headers={"Content-Type": "application/json", "X-CSRF-Token": token},
                body=_canonical_json(payload),
            )
        except AmbiguousTransportError as error:
            sanitized = sanitize_error(error)
            self.ledger.finish(entry_id, status=ExecutionStatus.AMBIGUOUS, sanitized_error=sanitized)
            return RuntimeResult(
                object_id, correlation_id, payload_hash, "EXECUTE", ExecutionStatus.AMBIGUOUS,
                payload, training_context=training_context, sanitized_error=sanitized,
            )

        if response.status != 201:
            sanitized = sanitize_error(response.body.decode("utf-8", errors="replace"))
            self.ledger.finish(
                entry_id, status=ExecutionStatus.FAILED,
                http_status=response.status, sanitized_error=sanitized,
            )
            return RuntimeResult(
                object_id, correlation_id, payload_hash, "EXECUTE", ExecutionStatus.FAILED,
                payload, training_context=training_context,
                http_status=response.status, sanitized_error=sanitized,
            )

        sales_order_id = self._created_sales_order_id(response)
        etag = response.header("ETag")
        if not sales_order_id:
            error = "HTTP 201 response did not contain an unambiguous SalesOrder ID"
            self.ledger.finish(
                entry_id, status=ExecutionStatus.FAILED, http_status=201,
                response_etag=etag, sanitized_error=error,
            )
            return RuntimeResult(
                object_id, correlation_id, payload_hash, "EXECUTE", ExecutionStatus.FAILED,
                payload, training_context=training_context,
                http_status=201, response_etag=etag, sanitized_error=error,
            )

        self.ledger.finish(
            entry_id, status=ExecutionStatus.CREATED, http_status=201,
            created_sales_order_id=sales_order_id, response_etag=etag,
        )
        try:
            read_back = self._read_back(sales_order_id)
            mismatches = self._read_back_mismatches(payload, read_back)
        except (TransportError, ValueError, json.JSONDecodeError) as error:
            mismatches = [f"read-back failed: {type(error).__name__}"]
            read_back = None
        if mismatches:
            error = sanitize_error("; ".join(mismatches))
            self.ledger.finish(
                entry_id, status=ExecutionStatus.FAILED, http_status=201,
                created_sales_order_id=sales_order_id, response_etag=etag,
                sanitized_error=error,
            )
            return RuntimeResult(
                object_id, correlation_id, payload_hash, "EXECUTE", ExecutionStatus.FAILED,
                payload, training_context=training_context,
                http_status=201, created_sales_order_id=sales_order_id,
                response_etag=etag, sanitized_error=error, read_back=read_back,
            )
        self.ledger.finish(
            entry_id, status=ExecutionStatus.VERIFIED, http_status=201,
            created_sales_order_id=sales_order_id, response_etag=etag,
        )
        return RuntimeResult(
            object_id, correlation_id, payload_hash, "EXECUTE", ExecutionStatus.VERIFIED,
            payload, training_context=training_context,
            http_status=201, created_sales_order_id=sales_order_id,
            response_etag=etag, read_back=read_back,
        )

    def _preflight(
        self,
        obj: dict,
        payload: dict,
        *,
        mode: str,
        record: bool,
        training_context: dict[str, Any] | None = None,
    ) -> RuntimeResult:
        object_id = obj["object_id"]
        payload_hash = _payload_sha256(payload)
        correlation_id = _correlation_id(object_id, payload_hash)
        checks: list[CheckResult] = []
        try:
            access = self.transport.request(
                "GET",
                _query(
                    f"{SERVICE_ROOT}/{ENTITY_SET}",
                    **{"$top": "1", "$select": "SalesOrder", "sap-client": self.config.client},
                ),
            )
            checks.append(CheckResult(
                "SERVICE_GET_ACCESS", "PASS" if access.status == 200 else "BLOCKED",
                f"HTTP {access.status}",
            ))
        except TransportError as error:
            checks.append(CheckResult("SERVICE_GET_ACCESS", "BLOCKED", type(error).__name__))

        checks.extend(self.dependency_verifier.verify(payload, self.transport))
        conflict = self.ledger.execution_conflict(
            canonical_object_id=object_id,
            correlation_id=correlation_id,
            payload_sha256=payload_hash,
            customer_reference=payload["PurchaseOrderByCustomer"],
        )
        checks.append(CheckResult(
            "LEDGER_DUPLICATE", "PASS" if conflict is None else "DUPLICATE",
            "no execution conflict" if conflict is None else conflict,
        ))
        duplicate = self._sap_duplicate_check(payload)
        checks.append(duplicate)

        if any(check.status == "DUPLICATE" for check in checks):
            status = ExecutionStatus.DUPLICATE
        elif any(check.status != "PASS" for check in checks):
            status = ExecutionStatus.BLOCKED
        else:
            status = ExecutionStatus.DRY_RUN_OK
        result = RuntimeResult(
            object_id, correlation_id, payload_hash, mode, status, payload,
            checks=checks, training_context=training_context,
        )
        if record:
            entry_id = self.ledger.start(
                canonical_object_id=object_id,
                correlation_id=correlation_id,
                customer_reference=payload["PurchaseOrderByCustomer"],
                payload_sha256=payload_hash,
                mode=mode,
                status=status,
            )
            self.ledger.finish(entry_id, status=status)
        return result

    def _sap_duplicate_check(self, payload: dict) -> CheckResult:
        fields = (
            "SalesOrderType", "SalesOrganization", "DistributionChannel",
            "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
        )
        expression = " and ".join(
            f"{field} eq {_odata_literal(str(payload[field]))}" for field in fields
        )
        path = _query(
            f"{SERVICE_ROOT}/{ENTITY_SET}",
            **{
                "$filter": expression,
                "$select": "SalesOrder," + ",".join(fields),
                "$top": "2",
                "sap-client": self.config.client,
            },
        )
        try:
            response = self.transport.request("GET", path)
            if response.status != 200:
                return CheckResult("SAP_DUPLICATE", "BLOCKED", f"HTTP {response.status}")
            rows = _results(response)
            if rows:
                ids = [str(row.get("SalesOrder", "<unknown>")) for row in rows]
                return CheckResult("SAP_DUPLICATE", "DUPLICATE", f"matches found: {ids}")
            return CheckResult("SAP_DUPLICATE", "PASS", "no exact SAP match")
        except (TransportError, ValueError, json.JSONDecodeError) as error:
            return CheckResult("SAP_DUPLICATE", "BLOCKED", f"check failed: {type(error).__name__}")

    def _created_sales_order_id(self, response: HttpResponse) -> str | None:
        try:
            value = response.json().get("d", {})
            if isinstance(value, dict) and value.get("SalesOrder"):
                return str(value["SalesOrder"])
        except (ValueError, json.JSONDecodeError):
            pass
        location = response.header("Location") or ""
        match = re.search(r"A_SalesOrder\('([^']+)'\)", location)
        return match.group(1) if match else None

    def _read_back(self, sales_order_id: str) -> dict[str, Any]:
        key = _odata_literal(sales_order_id)
        header_response = self.transport.request("GET", _query(
            f"{SERVICE_ROOT}/{ENTITY_SET}({key})",
            **{"$select": ",".join(HEADER_READ_FIELDS), "sap-client": self.config.client},
        ))
        item_response = self.transport.request("GET", _query(
            f"{SERVICE_ROOT}/A_SalesOrderItem",
            **{
                "$filter": f"SalesOrder eq {key}", "$select": ",".join(ITEM_READ_FIELDS),
                "sap-client": self.config.client,
            },
        ))
        partner_response = self.transport.request("GET", _query(
            f"{SERVICE_ROOT}/A_SalesOrderHeaderPartner",
            **{
                "$filter": f"SalesOrder eq {key}", "$select": ",".join(PARTNER_READ_FIELDS),
                "sap-client": self.config.client,
            },
        ))
        if any(response.status != 200 for response in (header_response, item_response, partner_response)):
            raise ValueError("One or more read-back requests did not return HTTP 200")
        header_value = header_response.json().get("d")
        if not isinstance(header_value, dict):
            raise ValueError("Header read-back is not an OData V2 entity")
        return {
            "header": header_value,
            "items": _results(item_response),
            "partners": _results(partner_response),
        }

    def _read_back_mismatches(self, payload: dict, read_back: dict[str, Any]) -> list[str]:
        mismatches = []
        header = read_back["header"]
        for field in (
            "SalesOrderType", "SalesOrganization", "DistributionChannel",
            "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer",
            "CustomerPurchaseOrderDate",
        ):
            if field in payload and header.get(field) != payload[field]:
                mismatches.append(f"header {field} expected {payload[field]!r}, got {header.get(field)!r}")
        actual_by_id = {str(item.get("SalesOrderItem")): item for item in read_back["items"]}
        for expected in payload["to_Item"]:
            actual = actual_by_id.get(expected["SalesOrderItem"])
            if actual is None:
                mismatches.append(f"missing item {expected['SalesOrderItem']}")
                continue
            for field in ("Material",):
                if actual.get(field) != expected[field]:
                    mismatches.append(f"item {expected['SalesOrderItem']} {field} mismatch")
            try:
                if Decimal(str(actual.get("RequestedQuantity"))) != Decimal(expected["RequestedQuantity"]):
                    mismatches.append(f"item {expected['SalesOrderItem']} RequestedQuantity mismatch")
            except InvalidOperation:
                mismatches.append(f"item {expected['SalesOrderItem']} RequestedQuantity invalid")
            units = {
                actual.get("RequestedQuantityUnit"), actual.get("RequestedQuantitySAPUnit"),
                actual.get("RequestedQuantityISOUnit"),
            }
            if expected["RequestedQuantityUnit"] not in units:
                mismatches.append(f"item {expected['SalesOrderItem']} unit not preserved or translated visibly")
        return mismatches

    def _record_terminal(
        self,
        obj: dict,
        payload: dict,
        mode: str,
        status: ExecutionStatus,
        *,
        http_status: int | None = None,
        error: str | None = None,
        training_context: dict[str, Any] | None = None,
    ) -> RuntimeResult:
        payload_hash = _payload_sha256(payload)
        correlation_id = _correlation_id(obj["object_id"], payload_hash)
        sanitized = sanitize_error(error) if error else None
        entry_id = self.ledger.start(
            canonical_object_id=obj["object_id"], correlation_id=correlation_id,
            customer_reference=payload["PurchaseOrderByCustomer"], payload_sha256=payload_hash,
            mode=mode, status=status,
        )
        self.ledger.finish(
            entry_id, status=status, http_status=http_status, sanitized_error=sanitized
        )
        return RuntimeResult(
            obj["object_id"], correlation_id, payload_hash, mode, status, payload,
            training_context=training_context,
            http_status=http_status, sanitized_error=sanitized,
        )
