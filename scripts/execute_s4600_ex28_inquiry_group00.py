"""Create one S4600 exercise-28 inquiry in VA11 with guarded readback."""

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
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {
    "inquiry_type": "DO",
    "sales_organization": "FR10",
    "distribution_channel": "10",
    "sales_division": "1W",
    "sold_to_party": "1000000112",
    "requested_delivery_date": "2026-11-11",
    "binding_period_validity_end_date": "2026-10-25",
    "items": [{"line_id": "10", "material": "10000283", "quantity": "3", "unit": "PC"}],
}
APPROVAL_PATH = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH8_EX28.inquiry_group00.workflow_approval.json"
DRY_RUN_PATH = ROOT / "runtime" / "sap_reads" / "s4600_ex28_inquiry_group00_dry_run.json"
RESULT_PATH = ROOT / "runtime" / "sap_writes" / "s4600_ex28_inquiry_group00_result.json"
SERVICE_ROOT = "sap/opu/odata/sap/API_SALES_INQUIRY_SRV"
P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV45A:4411"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4912/tblSAPMV45ATCTRL_U_ERF_ANGEBOT"
INITIAL_FIELDS = {
    P + "/usr/ctxtVBAK-AUART": "DO",
    P + "/usr/ctxtVBAK-VKORG": "FR10",
    P + "/usr/ctxtVBAK-VTWEG": "10",
    P + "/usr/ctxtVBAK-SPART": "1W",
}
DOCUMENT_FIELDS = {
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR": "1000000112",
    BODY + "/ctxtVBAK-BNDDT": "25.10.2026",
    BODY + "/ctxtRV45A-KETDAT": "11.11.2026",
    TABLE + "/ctxtRV45A-MABNR[1,0]": "10000283",
    TABLE + "/txtRV45A-KWMENG[3,0]": "3",
}
CONTINUE = P + "/tbar[0]/btn[0]"
SAVE = P + "/tbar[0]/btn[11]"


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def payload_hash() -> str:
    return hashlib.sha256(canonical(PAYLOAD)).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != "__metadata"}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def save_result(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path = RESULT_PATH if result["mode"] == "EXECUTE" else DRY_RUN_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_rows(client, entity: str, query: dict[str, str]) -> tuple[int, list[dict]]:
    response = client.request("GET", f"{SERVICE_ROOT}/{entity}?{urlencode(query)}", headers={"Accept": "application/json"})
    rows = clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else []
    return response.status, rows


def duplicate_lookup(client) -> dict:
    status, headers = get_rows(client, "A_SalesInquiry", {
        "$filter": (
            "SalesInquiryType eq 'AF' and SalesOrganization eq 'FR10' and "
            "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
            "SoldToParty eq '1000000112'"
        ),
        "$select": "SalesInquiry,SalesInquiryType,SalesOrganization,DistributionChannel,OrganizationDivision,SoldToParty,BindingPeriodValidityEndDate",
        "$top": "50",
    })
    matches = []
    for header in headers:
        number = str(header.get("SalesInquiry") or "")
        if not number:
            continue
        item_status, items = get_rows(client, "A_SalesInquiryItem", {
            "$filter": f"SalesInquiry eq '{number}' and Material eq '10000283'",
            "$select": "SalesInquiry,SalesInquiryItem,Material,RequestedQuantity,RequestedQuantityUnit",
            "$top": "10",
        })
        for item in items:
            if str(item.get("RequestedQuantity")) in {"3", "3.0", "3.000"}:
                matches.append({"header": header, "item": item, "item_http_status": item_status})
    return {"http_status": status, "candidate_headers": headers, "exact_matches": matches}


def load_approval() -> dict:
    value = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    if value.get("status") != "APPROVED" or value.get("environment") != EXPECTED:
        raise RuntimeError("Approval identity/status mismatch")
    if value.get("operation_scope") != "CREATE_ONE_S4600_EX28_GROUP00_INQUIRY_DO_VA11":
        raise RuntimeError("Approval scope mismatch")
    if value.get("payload_sha256") != payload_hash():
        raise RuntimeError("Approval fingerprint mismatch")
    constraints = value.get("constraints", {})
    if constraints.get("maximum_save_attempts") != 1:
        raise RuntimeError("Approval must limit save attempts to one")
    return value


def prepare_gui() -> dict:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if {key: session.identity[key] for key in EXPECTED} != EXPECTED:
        raise ActionBlockedError("Unexpected SAP identity")
    open_transaction(session, "VA11")
    time.sleep(0.5)
    for control_id, value in INITIAL_FIELDS.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)
    overview = inspect_screen(session)
    if (overview.get("transaction"), overview.get("program"), str(overview.get("screen_number"))) != ("VA11", "SAPMV45A", "4001"):
        raise ActionBlockedError("Unexpected VA11 overview")
    for control_id, value in DOCUMENT_FIELDS.items():
        set_text(session, control_id, value)
    press_safe_button(session, CONTINUE)
    time.sleep(1.0)
    state = inspect_screen(session)
    popups = state.get("popups") or []
    if popups:
        texts = [str(x.get("text") or "") for x in popups[0].get("input_fields") or []]
        if len(popups) != 1 or popups[0].get("window_title") != "Information" or not any("facture" in text.lower() for text in texts):
            raise ActionBlockedError("Unexpected VA11 popup")
        press_safe_button(session, "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]")
        time.sleep(0.8)
        state = inspect_screen(session)
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in state.get("input_fields") or []}
    expected = {
        **DOCUMENT_FIELDS,
        TABLE + "/ctxtVBAP-VRKME[4,0]": "289",
        TABLE + "/ctxtVBAP-PSTYV[8,0]": "AFN",
        TABLE + "/ctxtVBAP-WERKS[14,0]": "FR10",
        TABLE + "/ctxtKOMV-KSCHL[15,0]": "ZPR0",
        TABLE + "/txtKOMV-KBETR[16,0]": "80,00",
    }
    mismatches = {key: {"expected": value, "actual": fields.get(key)} for key, value in expected.items() if fields.get(key, "").strip() != value}
    if mismatches:
        raise ActionBlockedError(f"VA11 pre-save mismatch: {mismatches!r}")
    status = state.get("status_bar") or {}
    if str(status.get("message_type") or "").upper() in {"E", "A"} or state.get("popups"):
        raise ActionBlockedError(f"VA11 pre-save error: {status!r}")
    return {"screen": state, "verified_fields": expected}


def save_once(result: dict) -> dict:
    session = SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != ("VA11", "SAPMV45A", "4001") or before.get("popups"):
        raise ActionBlockedError("Unexpected VA11 pre-save screen")
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in before.get("input_fields") or []}
    if any(fields.get(key, "").strip() != value for key, value in DOCUMENT_FIELDS.items()):
        raise ActionBlockedError("VA11 exact target values changed before save")
    save = session.find(SAVE)
    if str(getattr(save, "Type", "")) != "GuiButton" or str(getattr(save, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("VA11 exact Save control mismatch")
    result["status"] = "SUBMITTED"
    result["save_attempt"] = {"status": "SUBMITTED", "control_id": SAVE}
    save_result(result)
    session.audit("PHASE5_OPERATION", control_id=SAVE, value={"operation": "CREATE_ONE_S4600_EX28_GROUP00_INQUIRY_DO_VA11", "payload_sha256": payload_hash(), "step": "save_once"})
    save.press()
    time.sleep(1.2)
    return inspect_screen(session)


def readback(client, number: str) -> dict:
    header_response = client.request("GET", f"{SERVICE_ROOT}/A_SalesInquiry('{number}')", headers={"Accept": "application/json"})
    item_status, items = get_rows(client, "A_SalesInquiryItem", {
        "$filter": f"SalesInquiry eq '{number}'",
        "$select": "SalesInquiry,SalesInquiryItem,SalesInquiryItemCategory,Material,RequestedQuantity,RequestedQuantityUnit,NetAmount,TransactionCurrency",
        "$top": "10",
    })
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
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    duplicate = duplicate_lookup(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": "CREATE_ONE_S4600_EX28_GROUP00_INQUIRY_DO_VA11",
        "payload": PAYLOAD,
        "payload_sha256": payload_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "duplicate_lookup": duplicate,
    }
    if duplicate["http_status"] != 200 or duplicate["exact_matches"]:
        result["status"] = "DUPLICATE" if duplicate["exact_matches"] else "BLOCKED_LOOKUP"
        save_result(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    if not args.execute:
        result["status"] = "DRY_RUN_OK"
        save_result(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    approval = load_approval()
    result["approval_id"] = approval["approval_id"]
    prepared = prepare_gui()
    result["pre_save_verification"] = {"verified_fields": prepared["verified_fields"]}
    save_result(result)
    try:
        after = save_once(result)
    except Exception as error:
        result["status"] = "AMBIGUOUS"
        result["save_attempt"]["status"] = "AMBIGUOUS"
        result["save_attempt"]["error"] = f"{type(error).__name__}: {error}"
        save_result(result)
        raise
    status = after.get("status_bar") or {}
    result["post_save_status_bar"] = status
    message = str(status.get("text") or "")
    if str(status.get("message_type") or "").upper() in {"E", "A"}:
        result["status"] = "FAILED"
        result["save_attempt"]["status"] = "FAILED"
        save_result(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    match = re.search(r"\b(\d{6,})\b", message)
    number = match.group(1) if match else None
    if number is None:
        post_lookup = duplicate_lookup(client)
        result["post_save_lookup"] = post_lookup
        numbers = sorted({str(row["header"].get("SalesInquiry")) for row in post_lookup["exact_matches"]})
        number = numbers[0] if len(numbers) == 1 else None
    if number is None:
        result["status"] = "AMBIGUOUS"
        result["save_attempt"]["status"] = "AMBIGUOUS_ID"
        save_result(result)
        return 2
    result["sales_inquiry"] = number
    result["readback"] = readback(client, number)
    header = result["readback"]["header"]
    items = result["readback"]["items"]
    verified = (
        result["readback"]["header_http_status"] == 200
        and header.get("SalesInquiryType") == "DO"
        and header.get("SalesOrganization") == "FR10"
        and header.get("DistributionChannel") == "10"
        and header.get("OrganizationDivision") == "1W"
        and header.get("SoldToParty") == "1000000112"
        and len(items) == 1
        and items[0].get("Material") == "10000283"
        and str(items[0].get("RequestedQuantity")) in {"3", "3.0", "3.000"}
    )
    result["save_attempt"]["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"
    result["status"] = "VERIFIED" if verified else "READBACK_MISMATCH"
    save_result(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
