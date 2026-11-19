"""Save the verified VA01 order once and perform independent OData readback."""

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
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {
    "order_type_gui": "CS", "order_type_internal": "TA", "sales_organization": "FR10", "distribution_channel": "10", "sales_division": "1W",
    "sold_to_party": "1000000112", "reference_quotation": "20000103", "customer_reference": "8-900", "requested_delivery_date": "2026-11-11",
    "items": [{"item": "10", "material": "10000283", "quantity": "1", "unit_gui": "289", "expected_item_category": "TAN", "expected_plant": "FR10", "expected_condition": "ZPR0", "expected_unit_price_eur": "80.00"}],
    "expected_total_net_eur": "80.00",
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH8_EX28.order_group00.workflow_approval.json"
DRY_RUN = ROOT / "runtime" / "sap_reads" / "s4600_ex28_order_group00_dry_run.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex28_order_group00_result.json"
SERVICE = "sap/opu/odata/sap/API_SALES_ORDER_SRV"
P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG"
SAVE = P + "/tbar[0]/btn[11]"
GUI_EXPECTED = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD": "8-900",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR": "80,00",
    BODY + "/ssubHEADER_FRAME:SAPMV45A:4440/ctxtRV45A-KETDAT": "11.11.2026",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "10000283", TABLE + "/txtRV45A-KWMENG[3,0]": "1",
    TABLE + "/ctxtVBAP-VRKME[4,0]": "289", TABLE + "/ctxtVBAP-PSTYV[8,0]": "TAN",
    TABLE + "/ctxtVBAP-WERKS[12,0]": "FR10", TABLE + "/ctxtKOMV-KSCHL[14,0]": "ZPR0",
    TABLE + "/txtKOMV-KBETR[15,0]": "80,00", TABLE + "/txtVBAP-NETWR[20,0]": "80,00",
}


def canonical(value) -> bytes: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
def fingerprint() -> str: return hashlib.sha256(canonical(PAYLOAD)).hexdigest()
def clean(value):
    if isinstance(value, dict): return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list): return [clean(item) for item in value]
    return value
def save_result(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat(); path = RESULT if result["mode"] == "EXECUTE" else DRY_RUN; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
def rows(client, entity: str, query: dict[str, str]) -> tuple[int, list[dict]]:
    response = client.request("GET", f"{SERVICE}/{entity}?{urlencode(query)}", headers={"Accept": "application/json"}); return response.status, clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else []
def duplicate_lookup(client) -> dict:
    status, headers = rows(client, "A_SalesOrder", {"$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '8-900'", "$top": "50"})
    matches = []
    for header in headers:
        number = str(header.get("SalesOrder") or ""); item_status, items = rows(client, "A_SalesOrderItem", {"$filter": f"SalesOrder eq '{number}' and Material eq '10000283'", "$top": "10"})
        for item in items:
            if str(item.get("RequestedQuantity")) in {"1", "1.0", "1.000"}: matches.append({"header": header, "item": item, "item_http_status": item_status})
    return {"http_status": status, "candidate_headers": headers, "exact_matches": matches}
def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED" or value.get("environment") != EXPECTED or value.get("operation_scope") != "CREATE_ONE_S4600_EX28_GROUP00_ORDER_CS_VA01" or value.get("payload_sha256") != fingerprint() or value.get("constraints", {}).get("maximum_save_attempts") != 1: raise RuntimeError("Approval mismatch")
    return value
def verify_screen(mode: SafetyMode):
    session = SapGuiConnection(mode=mode).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED: raise ActionBlockedError("Unexpected SAP identity")
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VA01", "SAPMV45A", "4001") or snapshot.get("popups"): raise ActionBlockedError("Unexpected VA01 screen")
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in snapshot.get("input_fields") or []}; mismatches = {key: {"expected": value, "actual": fields.get(key)} for key, value in GUI_EXPECTED.items() if fields.get(key) != value}
    if mismatches: raise ActionBlockedError(f"VA01 pre-save mismatch: {mismatches!r}")
    return session, snapshot
def readback(client, number: str) -> dict:
    header_response = client.request("GET", f"{SERVICE}/A_SalesOrder('{number}')", headers={"Accept": "application/json"})
    item_status, items = rows(client, "A_SalesOrderItem", {"$filter": f"SalesOrder eq '{number}'", "$top": "10"})
    flow_status, flow = rows(client, "A_SlsOrdPrecdgProcFlow", {"$filter": f"SalesOrder eq '{number}'", "$top": "20"})
    return {"header_http_status": header_response.status, "header": clean(header_response.json().get("d", {})) if header_response.status == 200 else {}, "items_http_status": item_status, "items": items, "preceding_flow_http_status": flow_status, "preceding_flow": flow}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--execute", action="store_true"); args = parser.parse_args(); load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env(); identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED: raise SystemExit(f"Blocked: {identity!r}")
    client = UrllibSapTransport(config); duplicate = duplicate_lookup(client)
    result = {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": identity, "operation": "CREATE_ONE_S4600_EX28_GROUP00_ORDER_CS_VA01", "payload": PAYLOAD, "payload_sha256": fingerprint(), "mode": "EXECUTE" if args.execute else "DRY_RUN", "duplicate_lookup": duplicate}
    if duplicate["http_status"] != 200 or duplicate["exact_matches"]: result["status"] = "DUPLICATE" if duplicate["exact_matches"] else "BLOCKED_LOOKUP"; save_result(result); return 2
    if not args.execute:
        _, snapshot = verify_screen(SafetyMode.READ); result["pre_save_status"] = snapshot.get("status_bar"); result["status"] = "DRY_RUN_OK"; save_result(result); print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    approval = load_approval(); result["approval_id"] = approval["approval_id"]; session, before = verify_screen(SafetyMode.EXECUTE); save_control = session.find(SAVE)
    if str(getattr(save_control, "Type", "")) != "GuiButton" or str(getattr(save_control, "Text", "")) != "Sauvegarder": raise ActionBlockedError("Unexpected Save control")
    result["pre_save_status"] = before.get("status_bar"); result["status"] = "SUBMITTED"; result["save_attempt"] = {"status": "SUBMITTED", "control_id": SAVE}; save_result(result)
    session.audit("PHASE5_OPERATION", control_id=SAVE, value={"operation": result["operation"], "payload_sha256": fingerprint(), "step": "save_once"})
    try: save_control.press(); time.sleep(1.3); after = inspect_screen(session)
    except Exception as error: result["status"] = "AMBIGUOUS"; result["save_attempt"].update(status="AMBIGUOUS", error=f"{type(error).__name__}: {error}"); save_result(result); raise
    status = after.get("status_bar") or {}; result["post_save_status_bar"] = status
    if str(status.get("message_type") or "").upper() in {"E", "A"}: result["status"] = "FAILED"; result["save_attempt"]["status"] = "FAILED"; save_result(result); return 2
    match = re.search(r"\b(\d{3,})\b", str(status.get("text") or "")); number = match.group(1) if match else None; post_lookup = duplicate_lookup(client); result["post_save_lookup"] = post_lookup
    if number is None:
        numbers = sorted({str(row["header"].get("SalesOrder")) for row in post_lookup["exact_matches"]}); number = numbers[0] if len(numbers) == 1 else None
    if number is None: result["status"] = "AMBIGUOUS"; result["save_attempt"]["status"] = "AMBIGUOUS_ID"; save_result(result); return 2
    result["sales_order"] = number; result["readback"] = readback(client, number); header = result["readback"]["header"]; items = result["readback"]["items"]
    verified = result["readback"]["header_http_status"] == 200 and header.get("SalesOrganization") == "FR10" and header.get("DistributionChannel") == "10" and header.get("OrganizationDivision") == "1W" and header.get("SoldToParty") == "1000000112" and header.get("PurchaseOrderByCustomer") == "8-900" and len(items) == 1 and items[0].get("Material") == "10000283" and str(items[0].get("RequestedQuantity")) in {"1", "1.0", "1.000"}
    result["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"; result["save_attempt"]["status"] = result["status"]; save_result(result); print(json.dumps(result, ensure_ascii=False, indent=2, default=str)); return 0 if verified else 2


if __name__ == "__main__": raise SystemExit(main())
