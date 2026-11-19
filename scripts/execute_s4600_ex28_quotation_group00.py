"""Save the already verified VA21 quotation once, then perform OData readback."""

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
PAYLOAD = {
    "quotation_type_gui": "OFF.", "quotation_type_internal": "AG",
    "sales_organization": "FR10", "distribution_channel": "10", "sales_division": "1W",
    "sold_to_party": "1000000112", "reference_inquiry": "10000104",
    "validity_start": "2026-10-21", "validity_end": "2026-11-01", "requested_delivery_date": "2026-11-11",
    "items": [{"item": "10", "material": "10000283", "quantity": "2", "unit_gui": "289", "expected_item_category": "AGN", "expected_plant": "FR10", "expected_condition": "ZPR0", "expected_unit_price_eur": "80.00"}],
    "expected_total_net_eur": "160.00",
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH8_EX28.quotation_group00.workflow_approval.json"
DRY_RUN = ROOT / "runtime" / "sap_reads" / "s4600_ex28_quotation_group00_dry_run.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex28_quotation_group00_result.json"
SERVICE = "sap/opu/odata/sap/API_SALES_QUOTATION_SRV"
P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV45A:4411"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4912/tblSAPMV45ATCTRL_U_ERF_ANGEBOT"
SAVE = P + "/tbar[0]/btn[11]"
GUI_EXPECTED = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR": "160,00",
    BODY + "/ctxtVBAK-ANGDT": "21.10.2026",
    BODY + "/ctxtVBAK-BNDDT": "01.11.2026",
    BODY + "/ctxtRV45A-KETDAT": "11.11.2026",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "10000283",
    TABLE + "/txtRV45A-KWMENG[3,0]": "2",
    TABLE + "/ctxtVBAP-VRKME[4,0]": "289",
    TABLE + "/ctxtVBAP-PSTYV[8,0]": "AGN",
    TABLE + "/txtVBAP-NETWR[10,0]": "160,00",
    TABLE + "/ctxtVBAP-WERKS[14,0]": "FR10",
    TABLE + "/ctxtKOMV-KSCHL[15,0]": "ZPR0",
    TABLE + "/txtKOMV-KBETR[16,0]": "80,00",
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


def save_result(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path = RESULT if result["mode"] == "EXECUTE" else DRY_RUN
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def rows(client, entity: str, query: dict[str, str]) -> tuple[int, list[dict]]:
    response = client.request("GET", f"{SERVICE}/{entity}?{urlencode(query)}", headers={"Accept": "application/json"})
    return response.status, clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else []


def duplicate_lookup(client) -> dict:
    status, headers = rows(client, "A_SalesQuotation", {
        "$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W' and SoldToParty eq '1000000112'",
        "$top": "50",
    })
    matches = []
    for header in headers:
        number = str(header.get("SalesQuotation") or "")
        item_status, items = rows(client, "A_SalesQuotationItem", {
            "$filter": f"SalesQuotation eq '{number}' and Material eq '10000283'", "$top": "10",
        })
        for item in items:
            if str(item.get("RequestedQuantity")) in {"2", "2.0", "2.000"}:
                matches.append({"header": header, "item": item, "item_http_status": item_status})
    return {"http_status": status, "candidate_headers": headers, "exact_matches": matches}


def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED" or value.get("environment") != EXPECTED:
        raise RuntimeError("Approval identity/status mismatch")
    if value.get("operation_scope") != "CREATE_ONE_S4600_EX28_GROUP00_QUOTATION_OFF_VA21":
        raise RuntimeError("Approval scope mismatch")
    if value.get("payload_sha256") != fingerprint() or value.get("constraints", {}).get("maximum_save_attempts") != 1:
        raise RuntimeError("Approval fingerprint/constraint mismatch")
    return value


def verify_current_screen(mode: SafetyMode):
    session = SapGuiConnection(mode=mode).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected SAP identity")
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != ("VA21", "SAPMV45A", "4001") or snapshot.get("popups"):
        raise ActionBlockedError("Unexpected VA21 pre-save screen")
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in snapshot.get("input_fields") or []}
    mismatches = {key: {"expected": value, "actual": fields.get(key)} for key, value in GUI_EXPECTED.items() if fields.get(key) != value}
    if mismatches:
        raise ActionBlockedError(f"VA21 pre-save mismatch: {mismatches!r}")
    return session, snapshot


def readback(client, number: str) -> dict:
    header_response = client.request("GET", f"{SERVICE}/A_SalesQuotation('{number}')", headers={"Accept": "application/json"})
    item_status, items = rows(client, "A_SalesQuotationItem", {"$filter": f"SalesQuotation eq '{number}'", "$top": "10"})
    flow_status, flow = rows(client, "A_SlsQtanPrecdgProcFlow", {"$filter": f"SalesQuotation eq '{number}'", "$top": "20"})
    return {
        "header_http_status": header_response.status,
        "header": clean(header_response.json().get("d", {})) if header_response.status == 200 else {},
        "items_http_status": item_status, "items": items,
        "preceding_flow_http_status": flow_status, "preceding_flow": flow,
    }


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--execute", action="store_true"); args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env(); identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config); duplicate = duplicate_lookup(client)
    result = {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": identity, "operation": "CREATE_ONE_S4600_EX28_GROUP00_QUOTATION_OFF_VA21", "payload": PAYLOAD, "payload_sha256": fingerprint(), "mode": "EXECUTE" if args.execute else "DRY_RUN", "duplicate_lookup": duplicate}
    if duplicate["http_status"] != 200 or duplicate["exact_matches"]:
        result["status"] = "DUPLICATE" if duplicate["exact_matches"] else "BLOCKED_LOOKUP"; save_result(result); print(json.dumps(result, ensure_ascii=False, indent=2)); return 2
    if not args.execute:
        _, snapshot = verify_current_screen(SafetyMode.READ)
        result["pre_save_status"] = snapshot.get("status_bar"); result["status"] = "DRY_RUN_OK"; save_result(result); print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    approval = load_approval(); result["approval_id"] = approval["approval_id"]
    session, before = verify_current_screen(SafetyMode.EXECUTE)
    save_control = session.find(SAVE)
    if str(getattr(save_control, "Type", "")) != "GuiButton" or str(getattr(save_control, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("Unexpected VA21 Save control")
    result["pre_save_status"] = before.get("status_bar"); result["status"] = "SUBMITTED"; result["save_attempt"] = {"status": "SUBMITTED", "control_id": SAVE}; save_result(result)
    session.audit("PHASE5_OPERATION", control_id=SAVE, value={"operation": result["operation"], "payload_sha256": fingerprint(), "step": "save_once"})
    try:
        save_control.press(); time.sleep(1.3); after = inspect_screen(session)
    except Exception as error:
        result["status"] = "AMBIGUOUS"; result["save_attempt"].update(status="AMBIGUOUS", error=f"{type(error).__name__}: {error}"); save_result(result); raise
    status = after.get("status_bar") or {}; result["post_save_status_bar"] = status
    if str(status.get("message_type") or "").upper() in {"E", "A"}:
        result["status"] = "FAILED"; result["save_attempt"]["status"] = "FAILED"; save_result(result); return 2
    message = str(status.get("text") or ""); match = re.search(r"\b(\d{6,})\b", message); number = match.group(1) if match else None
    post_lookup = duplicate_lookup(client); result["post_save_lookup"] = post_lookup
    if number is None:
        numbers = sorted({str(row["header"].get("SalesQuotation")) for row in post_lookup["exact_matches"]}); number = numbers[0] if len(numbers) == 1 else None
    if number is None:
        result["status"] = "AMBIGUOUS"; result["save_attempt"]["status"] = "AMBIGUOUS_ID"; save_result(result); return 2
    result["sales_quotation"] = number; result["readback"] = readback(client, number)
    header = result["readback"]["header"]; items = result["readback"]["items"]
    verified = (
        result["readback"]["header_http_status"] == 200 and header.get("SalesOrganization") == "FR10" and header.get("DistributionChannel") == "10" and header.get("OrganizationDivision") == "1W" and header.get("SoldToParty") == "1000000112"
        and len(items) == 1 and items[0].get("Material") == "10000283" and str(items[0].get("RequestedQuantity")) in {"2", "2.0", "2.000"}
    )
    result["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"; result["save_attempt"]["status"] = result["status"]; save_result(result)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str)); return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
