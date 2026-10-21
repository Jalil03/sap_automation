"""One-shot S4615 BP standard-address workflow around the local GUI runner."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlencode

from src.provisioning.execution_policy import ExecutionCheckpoint
from src.provisioning.s4615_bp_address_gui import (
    ADDRESS, APPROVAL_PATH, ATTEMPT_PATH, BP, MAPPING_PATH, TARGET,
)
from src.sap_gui_bridge.protocol import enqueue_request, wait_for_response
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


SERVICE = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
CHECKPOINT_PATH = APPROVAL_PATH.with_name("C615-A01.workflow_checkpoint.json")
WORKFLOW_ID = "S4615_CUSTOMER_A01"


def _rows(client: Any, entity: str) -> list[dict[str, Any]]:
    query = urlencode({"$filter": f"BusinessPartner eq '{BP}'", "$format": "json"})
    response = client.request("GET", f"{SERVICE}{entity}?{query}")
    if response.status != 200:
        raise RuntimeError(f"{entity} lookup unknown: HTTP {response.status}")
    value = response.json().get("d", {}).get("results")
    if not isinstance(value, list):
        raise RuntimeError(f"{entity} response shape unknown")
    return value


def _date(value: Any):
    if value is None:
        return None
    if isinstance(value, str):
        match = re.fullmatch(r"/Date\((-?\d+)(?:[+-]\d{4})?\)/", value)
        try:
            parsed = (datetime(1970, 1, 1, tzinfo=timezone.utc)
                      + timedelta(milliseconds=int(match.group(1)))
                      if match else datetime.fromisoformat(value.replace("Z", "+00:00")))
            return parsed.date()
        except (ValueError, OverflowError, OSError):
            return None
    return None


def read_state(client: Any, *, today: datetime | None = None) -> dict[str, Any]:
    """One focused existence check: address plus XXDEFAULT usage for this BP."""
    now = today or datetime.now(timezone.utc)
    addresses = _rows(client, "A_BusinessPartnerAddress")
    usages = _rows(client, "A_BuPaAddressUsage")
    if not addresses and not usages:
        return {"state": "MISSING", "address_id": None}
    if len(addresses) != 1:
        return {"state": "UNKNOWN", "reason": "Unexpected address count", "address_id": None}
    row = addresses[0]
    address_id = row.get("AddressID")
    if not address_id or row.get("BusinessPartner") != BP:
        return {"state": "UNKNOWN", "reason": "Address identity unverified", "address_id": None}
    expected = {key: row.get(key) for key in ADDRESS}
    if expected != ADDRESS:
        return {"state": "UNKNOWN", "reason": "Existing address differs from approved values",
                "address_id": str(address_id)}
    standard = [usage for usage in usages if usage.get("AddressID") == address_id
                and usage.get("AddressUsage") == "XXDEFAULT"]
    if len(standard) != 1:
        return {"state": "UNKNOWN", "reason": "Current XXDEFAULT not proven",
                "address_id": str(address_id)}
    usage = standard[0]
    # OData V2 dates are represented as /Date(milliseconds)/. A missing or
    # unknown validity field cannot prove that the default usage is current.
    start = usage.get("ValidityStartDate")
    end = usage.get("ValidityEndDate")
    start_date = _date(start)
    end_date = _date(end)
    if start_date is None or end_date is None or not (start_date <= now.date() <= end_date):
        return {"state": "UNKNOWN", "reason": "XXDEFAULT validity not proven",
                "address_id": str(address_id)}
    return {"state": "EXISTS", "address_id": str(address_id), "current_standard": True}


def _approved_step() -> None:
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))["mappings"].get("C615-A01", {})
    if (approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("existing_business_partner") != BP
            or "CUSTOMER_MASTER_OWNER" not in approval.get("approval_scopes_evidenced", [])
            or approval.get("step_authorizations", {}).get("BP_ADDRESS", {}).get("execute") is not True
            or {key: approval.get("proposed_values", {}).get("address", {}).get(key) for key in ADDRESS} != ADDRESS
            or mapping.get("status") != "LIVE_VERIFIED" or mapping.get("sap_id") != BP):
        raise ValueError("Existing BP mapping or scoped address approval is not valid")


def _request(action: str, params: dict[str, Any], mode: str,
             sender: Callable[..., dict[str, Any]], waiter: Callable[..., dict[str, Any]]) -> dict[str, Any]:
    queued = sender(action, params, mode=mode)
    response = waiter(queued["request_id"], timeout_seconds=60)
    if response.get("status") != "SUCCESS":
        error = response.get("error") or {}
        raise RuntimeError(str(error.get("message") or f"Runner {action} failed"))
    if response.get("sap", {}).get("system") != "A4H" or str(response.get("sap", {}).get("client")) != "600" or response.get("sap", {}).get("user") != "ABDELJ":
        raise RuntimeError("SAP GUI runner identity mismatch")
    return response.get("result") or {}


def ensure_address(
    config: SapRuntimeConfig, *, execute: bool = False,
    transport_factory: Any = UrllibSapTransport,
    sender: Callable[..., dict[str, Any]] = enqueue_request,
    waiter: Callable[..., dict[str, Any]] = wait_for_response,
) -> dict[str, Any]:
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("Only A4H/600/ABDELJ is authorized")
    _approved_step()
    before = read_state(transport_factory(config))
    if before["state"] == "EXISTS":
        return {"status": "EXISTS", "address_id": before["address_id"]}
    if before["state"] != "MISSING":
        return {"status": "BLOCKED", "reason": before.get("reason", "Address state unknown")}
    form = _request("INSPECT_BP_STANDARD_ADDRESS", {}, "READ", sender, waiter)
    if form.get("bp") != BP or not form.get("english_key") or any(
        item.get("value") for item in form.get("fields", {}).values()
    ):
        return {"status": "BLOCKED", "reason": "Exact empty BP form or EN option not proven"}
    if not execute:
        return {"status": "WOULD_CREATE", "address_id": None}
    if ATTEMPT_PATH.exists():
        return {"status": "BLOCKED", "reason": "Previous address attempt requires reconciliation"}
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, WORKFLOW_ID)
    checkpoint.before_write("ENSURE_BP_STANDARD_ADDRESS")
    try:
        result = _request("PHASE5_OPERATION", {
            "operation": "ENSURE_BP_STANDARD_ADDRESS", "phase": "PROVISION",
            "target": TARGET, "values": ADDRESS,
        }, "EXECUTE", sender, waiter)
    except Exception:
        checkpoint.record("ENSURE_BP_STANDARD_ADDRESS", "AMBIGUOUS", detail="runner outcome unknown")
        raise
    if result.get("save_attempted") is not True:
        checkpoint.record("ENSURE_BP_STANDARD_ADDRESS", "AMBIGUOUS", detail="SAVE not confirmed")
        return {"status": "BLOCKED", "reason": "Runner did not confirm one SAVE"}
    after = read_state(transport_factory(config))
    if after["state"] != "EXISTS":
        checkpoint.record("ENSURE_BP_STANDARD_ADDRESS", "AMBIGUOUS", detail="independent address readback failed")
        return {"status": "BLOCKED", "reason": after.get("reason", "Independent address readback failed")}
    checkpoint.record("ENSURE_BP_STANDARD_ADDRESS", "VERIFIED", detail=after["address_id"])
    if ATTEMPT_PATH.exists():
        attempt = json.loads(ATTEMPT_PATH.read_text(encoding="utf-8"))
        attempt.update(status="VERIFIED", address_id=after["address_id"])
        ATTEMPT_PATH.write_text(json.dumps(attempt, indent=2) + "\n", encoding="utf-8")
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    approval.setdefault("verified_step_states", {})["BP_ADDRESS"] = "EXISTS_CURRENT_XXDEFAULT"
    approval.setdefault("address_evidence", {})["verified_address_id"] = after["address_id"]
    APPROVAL_PATH.write_text(json.dumps(approval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "CREATED_AND_VERIFIED", "address_id": after["address_id"]}
