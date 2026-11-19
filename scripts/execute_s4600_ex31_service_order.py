"""Save one approved S4600 exercise 31 service order and independently read it back."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OPERATION = "CREATE_ONE_S4600_EX31_GROUP00_SERVICE_ORDER_CS_VA01"
PAYLOAD = {
    "order_type_gui": "CS",
    "sales_organization": "FR10",
    "distribution_channel": "10",
    "sales_division": "1W",
    "sold_to_party": "1000000112",
    "customer_reference": "8-600",
    "material": "90000133",
    "quantity": "3",
    "quantity_unit": "H",
    "expected_item_category": "TAD",
    "expected_condition_type": "ZPR0",
    "expected_unit_price_eur": "150.00",
    "expected_total_net_eur": "450.00",
    "requested_delivery_date": "SYSTEM_DEFAULT_NOT_SET_BY_BOOK",
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH8_EX31.service_order_group00.workflow_approval.json"
DRY_RUN = ROOT / "runtime" / "sap_reads" / "s4600_ex31_service_order_dry_run.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex31_service_order_result.json"
SERVICE = "sap/opu/odata/sap/API_SALES_ORDER_SRV"
P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG"
SAVE = P + "/tbar[0]/btn[11]"
GUI_EXPECTED = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD": "8-600",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR": "450,00",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "90000133",
    TABLE + "/txtRV45A-KWMENG[3,0]": "3",
    TABLE + "/ctxtVBAP-VRKME[4,0]": "H",
    TABLE + "/ctxtVBAP-PSTYV[8,0]": "TAD",
    TABLE + "/ctxtVBAP-WERKS[12,0]": "",
    TABLE + "/ctxtKOMV-KSCHL[14,0]": "ZPR0",
    TABLE + "/txtKOMV-KBETR[15,0]": "150,00",
    TABLE + "/txtVBAP-NETWR[20,0]": "450,00",
}


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def fingerprint() -> str:
    return hashlib.sha256(canonical(PAYLOAD)).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def checkpoint(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path = RESULT if result["mode"] == "EXECUTE" else DRY_RUN
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def rows(client, entity: str, query: dict[str, str]) -> tuple[int, list[dict]]:
    response = client.request("GET", f"{SERVICE}/{entity}?{urlencode(query)}", headers={"Accept": "application/json"})
    if response.status != 200:
        return response.status, []
    return response.status, clean(response.json().get("d", {}).get("results", []))


def duplicate_lookup(client) -> dict:
    expression = (
        "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and "
        "OrganizationDivision eq '1W' and SoldToParty eq '1000000112' and "
        "PurchaseOrderByCustomer eq '8-600'"
    )
    status, headers = rows(client, "A_SalesOrder", {"$filter": expression, "$top": "50"})
    matches = []
    for header in headers:
        number = str(header.get("SalesOrder") or "")
        item_status, items = rows(client, "A_SalesOrderItem", {
            "$filter": f"SalesOrder eq '{number}' and Material eq '90000133'", "$top": "10"
        })
        for item in items:
            if str(item.get("RequestedQuantity")) in {"3", "3.0", "3.000"}:
                matches.append({"header": header, "item": item, "item_http_status": item_status})
    return {"http_status": status, "candidate_headers": headers, "exact_matches": matches}


def verify_screen(mode: SafetyMode):
    session = SapGuiConnection(mode=mode).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected SAP identity")
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VA01", "SAPMV45A", "4001"):
        raise ActionBlockedError("Unexpected VA01 screen")
    if snapshot.get("popups"):
        raise ActionBlockedError("Unexpected popup before save")
    status = snapshot.get("status_bar") or {}
    if str(status.get("message_type") or "").upper() in {"E", "A"}:
        raise ActionBlockedError(f"SAP error before save: {status!r}")
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in snapshot.get("input_fields") or []}
    mismatches = {key: {"expected": value, "actual": fields.get(key)} for key, value in GUI_EXPECTED.items() if fields.get(key) != value}
    if mismatches:
        raise ActionBlockedError(f"VA01 pre-save mismatch: {mismatches!r}")
    return session, snapshot


def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    if (
        value.get("status") != "APPROVED" or value.get("environment") != EXPECTED
        or value.get("operation_scope") != OPERATION or value.get("payload_sha256") != fingerprint()
        or value.get("constraints", {}).get("maximum_save_attempts") != 1
    ):
        raise RuntimeError("Approval mismatch")
    return value


def readback(client, number: str) -> dict:
    header_response = client.request("GET", f"{SERVICE}/A_SalesOrder('{number}')", headers={"Accept": "application/json"})
    item_status, items = rows(client, "A_SalesOrderItem", {"$filter": f"SalesOrder eq '{number}'", "$top": "10"})
    return {
        "header_http_status": header_response.status,
        "header": clean(header_response.json().get("d", {})) if header_response.status == 200 else {},
        "items_http_status": item_status,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: {identity!r}")
    client = UrllibSapTransport(config)
    duplicate = duplicate_lookup(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": identity,
        "operation": OPERATION, "payload": PAYLOAD, "payload_sha256": fingerprint(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN", "duplicate_lookup": duplicate,
    }
    if duplicate["http_status"] != 200 or duplicate["exact_matches"]:
        result["status"] = "DUPLICATE" if duplicate["exact_matches"] else "BLOCKED_LOOKUP"
        checkpoint(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    if not args.execute:
        _, snapshot = verify_screen(SafetyMode.READ)
        result["pre_save_status"] = snapshot.get("status_bar")
        result["status"] = "DRY_RUN_OK"
        checkpoint(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval = load_approval()
    result["approval_id"] = approval["approval_id"]
    session, before = verify_screen(SafetyMode.EXECUTE)
    save_control = session.find(SAVE)
    if str(getattr(save_control, "Type", "")) != "GuiButton" or str(getattr(save_control, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("Unexpected Save control")
    result["pre_save_status"] = before.get("status_bar")
    result["status"] = "SUBMITTED"
    result["save_attempt"] = {"status": "SUBMITTED", "control_id": SAVE, "attempts": 1}
    checkpoint(result)
    session.audit("PHASE5_OPERATION", control_id=SAVE, value={
        "operation": OPERATION, "payload_sha256": fingerprint(), "step": "save_once"
    })
    try:
        save_control.press()
        time.sleep(1.5)
        after = inspect_screen(session)
    except Exception as error:
        result["status"] = "AMBIGUOUS_NO_RETRY"
        result["save_attempt"].update(status="AMBIGUOUS_NO_RETRY", error=f"{type(error).__name__}: {error}")
        checkpoint(result)
        raise
    status = after.get("status_bar") or {}
    result["post_save_status_bar"] = status
    if after.get("popups") or str(status.get("message_type") or "").upper() in {"E", "A"}:
        result["status"] = "FAILED_OR_AMBIGUOUS_NO_RETRY"
        result["save_attempt"]["status"] = result["status"]
        checkpoint(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    match = re.search(r"\b(\d{3,})\b", str(status.get("text") or ""))
    number = match.group(1) if match else None
    post_lookup = duplicate_lookup(client)
    result["post_save_lookup"] = post_lookup
    if number is None:
        numbers = sorted({str(row["header"].get("SalesOrder")) for row in post_lookup["exact_matches"]})
        number = numbers[0] if len(numbers) == 1 else None
    if number is None:
        result["status"] = "AMBIGUOUS_ID_NO_RETRY"
        result["save_attempt"]["status"] = result["status"]
        checkpoint(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    result["sales_order"] = number
    result["readback"] = readback(client, number)
    header = result["readback"]["header"]
    items = result["readback"]["items"]
    verified = (
        result["readback"]["header_http_status"] == 200
        and header.get("SalesOrganization") == "FR10"
        and header.get("DistributionChannel") == "10"
        and header.get("OrganizationDivision") == "1W"
        and header.get("SoldToParty") == "1000000112"
        and header.get("PurchaseOrderByCustomer") == "8-600"
        and len(items) == 1
        and items[0].get("Material") == "90000133"
        and str(items[0].get("RequestedQuantity")) in {"3", "3.0", "3.000"}
        and str(items[0].get("NetAmount")) in {"450", "450.0", "450.00"}
    )
    result["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"
    result["save_attempt"]["status"] = result["status"]
    checkpoint(result)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
