"""Create one approved S4600 Product Basic root through controlled MM01."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


DESIGN_PATH = ROOT / "data/provisioning/s4600/product_basic_design_approval.group01.json"
APPROVAL_PATH = ROOT / "data/provisioning/s4600/product_basic_write_approval.group01.json"
CHECKPOINT_PATH = ROOT / "data/provisioning/s4600/product_basic_execution_checkpoint.group01.json"
MAPPING_PATH = ROOT / "data/provisioning/phase5_identity_mappings.json"
SERVICE = "sap/opu/odata/sap/API_PRODUCT_SRV/"
ROOT_FIELDS = "Product,ProductOldID,ProductType,IndustrySector,BaseUnit,Division"
PREFIX = "/app/con[0]/ses[0]/wnd[0]"
MATERIAL = PREFIX + "/usr/ctxtRMMG1-MATNR"
INDUSTRY = PREFIX + "/usr/cmbRMMG1-MBRSH"
MATERIAL_TYPE = PREFIX + "/usr/cmbRMMG1-MTART"
CHANGE_NUMBER = PREFIX + "/usr/ctxtRMMG1-AENNR"
REFERENCE = PREFIX + "/usr/ctxtRMMG1_REF-MATNR"
CONTINUE = PREFIX + "/tbar[0]/btn[0]"
SAVE = PREFIX + "/tbar[0]/btn[11]"
VIEW_WINDOW = PREFIX.replace("wnd[0]", "wnd[1]")
VIEW_TABLE = VIEW_WINDOW + "/usr/tblSAPLMGMMTC_VIEW"
VIEW_CONTINUE = VIEW_WINDOW + "/tbar[0]/btn[0]"
TAB1 = PREFIX + "/usr/tabsTABSPR1/tabpSP01"
BASIC1_PREFIX = TAB1 + "/ssubTABFRA1:SAPLMGMM:2004/"
BASIC1_MATERIAL = BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/ctxtRMMG1-MATNR"
BASIC1_DESCRIPTION = BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/txtMAKT-MAKTX"
BASIC1_UNIT = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-MEINS"
BASIC1_DIVISION = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-SPART"


def exact(session: Any, control_id: str, control_type: str) -> Any:
    control = session.find(control_id)
    if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != control_type:
        raise ActionBlockedError(f"MM01 control mismatch: {control_id}")
    return control


def checkpoint() -> dict[str, Any]:
    if not CHECKPOINT_PATH.exists():
        return {"workflow_id": "S4600_GROUP01_PRODUCT_BASIC", "operations": {}}
    value = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    if value.get("workflow_id") != "S4600_GROUP01_PRODUCT_BASIC" or not isinstance(value.get("operations"), dict):
        raise RuntimeError("S4600 product checkpoint mismatch")
    return value


def record(operation: str, status: str, detail: str) -> None:
    value = checkpoint()
    value["operations"][operation] = {"status": status, "detail": detail}
    temporary = CHECKPOINT_PATH.with_suffix(CHECKPOINT_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, CHECKPOINT_PATH)


def load_contract(logical_id: str) -> tuple[str, dict[str, str], str]:
    design = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))
    matches = [(name, value) for name, value in design["operations"].items()
               if value["target"]["logical_product_id"] == logical_id]
    if len(matches) != 1:
        raise RuntimeError("Product design operation mismatch")
    operation, design_op = matches[0]
    payload = design_op["payload"]
    fingerprint = design_op["target_fingerprint"]
    expected_keys = {"ProductType", "IndustrySector", "ProductDescription", "BaseUnit", "Division"}
    if set(payload) != expected_keys:
        raise RuntimeError("Approved Product Basic payload shape changed")
    approved_op = approval.get("operations", {}).get(operation, {})
    if (approval.get("workflow_id") != "S4600_GROUP01_PRODUCT_BASIC"
            or approval.get("environment") != {"system": "A4H", "client": "600", "user": "ABDELJ"}
            or approval.get("operation_scope") != "TRAINING_MASTER_DATA_PRODUCT_BASIC"
            or approval.get("approval_status") != "APPROVED"
            or approval.get("allow_write") is not True
            or not approval.get("approved_by")
            or not approval.get("authorization_evidence")
            or approved_op.get("logical_product_id") != logical_id
            or approved_op.get("target_fingerprint") != fingerprint
            or approved_op.get("allow_write") is not True
            or approved_op.get("limit") != "ONE_MM01_PRODUCT_BASIC_SAVE_ONLY"):
        raise RuntimeError("Exact PRODUCT_BASIC approval is missing")
    return operation, payload, fingerprint


def collection(client: UrllibSapTransport, entity: str, query: dict[str, str]) -> list[dict[str, Any]]:
    response = client.request("GET", SERVICE + entity + "?" + urlencode(query))
    if response.status != 200:
        raise RuntimeError(f"{entity} GET failed: HTTP {response.status}")
    rows = response.json().get("d", {}).get("results")
    if not isinstance(rows, list):
        raise RuntimeError(f"{entity} response shape unknown")
    return rows


def product(client: UrllibSapTransport, sap_id: str) -> dict[str, Any] | None:
    response = client.request("GET", SERVICE + f"A_Product('{sap_id}')?" + urlencode({"$select": ROOT_FIELDS}))
    if response.status == 404:
        return None
    if response.status != 200 or not isinstance(response.json().get("d"), dict):
        raise RuntimeError(f"A_Product readback failed: HTTP {response.status}")
    return {key: value for key, value in response.json()["d"].items() if key != "__metadata"}


def descriptions(client: UrllibSapTransport, *, sap_id: str | None = None, text: str | None = None) -> list[dict[str, Any]]:
    if (sap_id is None) == (text is None):
        raise ValueError("Use one description selector")
    selector = f"Product eq '{sap_id}'" if sap_id is not None else f"ProductDescription eq '{text.replace(chr(39), chr(39) * 2)}'"
    return collection(client, "A_ProductDescription", {
        "$filter": selector, "$select": "Product,Language,ProductDescription", "$top": "20",
    })


def expected_root(sap_id: str, payload: dict[str, str]) -> dict[str, str]:
    return {
        "Product": sap_id, "ProductType": payload["ProductType"],
        "IndustrySector": payload["IndustrySector"], "BaseUnit": payload["BaseUnit"],
        "Division": payload["Division"],
    }


def verify(client: UrllibSapTransport, sap_id: str, payload: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]] | None:
    root = product(client, sap_id)
    if root is None or any(root.get(key) != value for key, value in expected_root(sap_id, payload).items()):
        return None
    desc = descriptions(client, sap_id=sap_id)
    if not any(row.get("ProductDescription") == payload["ProductDescription"] for row in desc):
        return None
    return root, desc


def existing_mapping(logical_id: str, client: UrllibSapTransport, payload: dict[str, str]) -> str | None:
    if not MAPPING_PATH.exists():
        return None
    mappings = json.loads(MAPPING_PATH.read_text(encoding="utf-8")).get("mappings", {})
    entry = mappings.get(logical_id)
    if not entry:
        return None
    sap_id = str(entry.get("sap_id") or "")
    if entry.get("status") != "LIVE_VERIFIED" or not sap_id or verify(client, sap_id, payload) is None:
        raise RuntimeError("Existing mapping is not independently verifiable")
    return sap_id


def fresh_duplicate_check(client: UrllibSapTransport, logical_id: str, payload: dict[str, str]) -> None:
    literal = product(client, logical_id)
    aliases = collection(client, "A_Product", {
        "$filter": f"ProductOldID eq '{logical_id}'", "$select": ROOT_FIELDS, "$top": "20",
    })
    same_description = descriptions(client, text=payload["ProductDescription"])
    if literal is not None or aliases or same_description:
        raise RuntimeError("Fresh duplicate check found a candidate; creation blocked")


def prepare_mm01(payload: dict[str, str]) -> tuple[str, dict[str, Any]]:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    if any(str(session.identity.get(key, "")) != value for key, value in
           (("system", "A4H"), ("client", "600"), ("user", "ABDELJ"))):
        raise ActionBlockedError("Unexpected SAP GUI identity")
    open_transaction(session, "MM01")
    time.sleep(0.8)
    initial = inspect_screen(session)
    if (initial.get("transaction"), initial.get("program"), str(initial.get("screen_number"))) != ("MM01", "SAPLMGMM", "60") or initial.get("popups"):
        raise ActionBlockedError("MM01 initial screen mismatch")
    for control_id in (MATERIAL, CHANGE_NUMBER, REFERENCE):
        if str(getattr(exact(session, control_id, "GuiCTextField"), "Text", "") or "").strip():
            raise ActionBlockedError("MM01 initial identifier field is not blank")
    industry = exact(session, INDUSTRY, "GuiComboBox")
    product_type = exact(session, MATERIAL_TYPE, "GuiComboBox")
    session.audit("SET_TEXT", control_id=INDUSTRY, value=payload["IndustrySector"])
    industry.Key = payload["IndustrySector"]
    session.audit("SET_TEXT", control_id=MATERIAL_TYPE, value=payload["ProductType"])
    product_type.Key = payload["ProductType"]
    if str(industry.Key) != payload["IndustrySector"] or str(product_type.Key) != payload["ProductType"]:
        raise ActionBlockedError("MM01 rejected product type or industry sector")
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)
    views = inspect_screen(session)
    popups = views.get("popups") or []
    if len(popups) != 1 or popups[0].get("id") != VIEW_WINDOW:
        raise ActionBlockedError("MM01 view-selection popup mismatch")
    table = exact(session, VIEW_TABLE, "GuiTableControl")
    labels = []
    for row in (0, 1):
        label_id = VIEW_TABLE + f"/txtMSICHTAUSW-DYTXT[0,{row}]"
        labels.append(str(getattr(exact(session, label_id, "GuiTextField"), "Text", "")))
    if not labels[0].strip().endswith("base 1") or not labels[1].strip().endswith("base 2"):
        raise ActionBlockedError(f"Unexpected MM01 basic views: {labels}")
    if any(bool(getattr(table.GetAbsoluteRow(row), "Selected", False)) for row in (0, 1)):
        raise ActionBlockedError("MM01 basic views were already selected")
    session.audit("SET_TEXT", control_id=VIEW_TABLE, value={"selected_views": labels})
    table.GetAbsoluteRow(0).Selected = True
    table.GetAbsoluteRow(1).Selected = True
    press_safe_button(session, VIEW_CONTINUE)
    time.sleep(0.9)
    basic1 = inspect_screen(session)
    if (basic1.get("transaction"), basic1.get("program"), str(basic1.get("screen_number"))) != ("MM01", "SAPLMGMM", "4004") or basic1.get("popups"):
        raise ActionBlockedError("MM01 Basic Data 1 screen mismatch")
    title = str(basic1.get("window_title") or "")
    match = re.search(r"([0-9]{6,})", title)
    if match is None:
        raise ActionBlockedError("MM01 generated product number missing")
    sap_id = match.group(1)
    material = exact(session, BASIC1_MATERIAL, "GuiCTextField")
    if str(getattr(material, "Text", "")).strip() != sap_id or bool(getattr(material, "Changeable", True)):
        raise ActionBlockedError("MM01 generated product field mismatch")
    set_text(session, BASIC1_DESCRIPTION, payload["ProductDescription"])
    set_text(session, BASIC1_UNIT, payload["BaseUnit"])
    set_text(session, BASIC1_DIVISION, payload["Division"])
    press_safe_button(session, CONTINUE)
    time.sleep(0.8)
    basic2 = inspect_screen(session)
    if (basic2.get("transaction"), basic2.get("program"), str(basic2.get("screen_number"))) != ("MM01", "SAPLMGMM", "4004") or basic2.get("popups"):
        raise ActionBlockedError("MM01 Basic Data 2 validation failed")
    status = basic2.get("status_bar") or {}
    if str(status.get("message_type") or "").upper() in {"E", "A"}:
        raise ActionBlockedError(f"MM01 rejected Product Basic values: {status.get('text')}")
    return sap_id, basic2


def save_once(operation: str, sap_id: str, payload: dict[str, str]) -> dict[str, Any]:
    session = SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
    before = inspect_screen(session)
    if (before.get("transaction"), before.get("program"), str(before.get("screen_number"))) != ("MM01", "SAPLMGMM", "4004") or before.get("popups"):
        raise ActionBlockedError("MM01 pre-save screen mismatch")
    description2 = next((item for item in before.get("input_fields") or []
                         if "/tabpSP02/" in str(item.get("id")) and str(item.get("id")).endswith("/txtMAKT-MAKTX")), None)
    if description2 is None or str(description2.get("text") or "") != payload["ProductDescription"]:
        raise ActionBlockedError("MM01 Basic Data 2 description mismatch")
    tab = exact(session, TAB1, "GuiTab")
    tab.Select()
    basic1 = inspect_screen(session)
    fields = {item.get("id"): item for item in basic1.get("input_fields") or []}
    expected = {
        BASIC1_MATERIAL: sap_id, BASIC1_DESCRIPTION: payload["ProductDescription"],
        BASIC1_UNIT: payload["BaseUnit"], BASIC1_DIVISION: payload["Division"],
    }
    if any(str((fields.get(key) or {}).get("text") or "").strip() != value for key, value in expected.items()):
        raise ActionBlockedError("MM01 Basic Data 1 pre-save values mismatch")
    if (fields.get(BASIC1_MATERIAL) or {}).get("changeable") is not False:
        raise ActionBlockedError("MM01 generated product unexpectedly editable")
    save = exact(session, SAVE, "GuiButton")
    if str(getattr(save, "Text", "")) != "Sauvegarder":
        raise ActionBlockedError("MM01 exact Save control mismatch")
    record(operation, "ATTEMPTED", f"About to send one MM01 Basic Data save for generated candidate {sap_id}")
    session.audit("PHASE5_OPERATION", control_id=SAVE,
                  value={"operation": operation, "material_candidate": sap_id, "step": "save_once"})
    save.press()
    time.sleep(1.0)
    return inspect_screen(session)


def persist_mapping(logical_id: str, sap_id: str, payload: dict[str, str], fingerprint: str) -> None:
    value = json.loads(MAPPING_PATH.read_text(encoding="utf-8")) if MAPPING_PATH.exists() else {"version": 1, "mappings": {}}
    mappings = value.setdefault("mappings", {})
    prior = mappings.get(logical_id)
    if prior and prior.get("sap_id") != sap_id:
        raise RuntimeError("Identity mapping conflict")
    mappings[logical_id] = {
        "object_type": "MATERIAL", "logical_id": logical_id, "sap_id": sap_id,
        "status": "LIVE_VERIFIED", "scope": "PRODUCT_BASIC_ONLY",
        "target_fingerprint": fingerprint,
        "evidence": {"service": "API_PRODUCT_SRV", "root_readback": "EXISTS",
                     "description_readback": "EXISTS", "payload": payload},
    }
    temporary = MAPPING_PATH.with_suffix(MAPPING_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, MAPPING_PATH)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logical_id", choices=("T-D101", "T-MS101", "T-MS201"))
    args = parser.parse_args()
    operation, payload, fingerprint = load_contract(args.logical_id)
    prior = checkpoint()["operations"].get(operation)
    if prior and prior.get("status") in {"ATTEMPTED", "AMBIGUOUS", "REJECTED", "VERIFIED"}:
        raise RuntimeError(f"Prior write checkpoint requires reconciliation: {prior}")
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise RuntimeError("Only A4H/600/ABDELJ is authorized")
    client = UrllibSapTransport(config)
    mapped = existing_mapping(args.logical_id, client, payload)
    if mapped:
        record(operation, "SKIPPED_EXISTS", f"Existing LIVE_VERIFIED mapping read back as {mapped}")
        print(json.dumps({"product": args.logical_id, "result": "EXISTING", "sap_id": mapped}))
        return 0
    fresh_duplicate_check(client, args.logical_id, payload)
    sap_id, _ = prepare_mm01(payload)
    try:
        after = save_once(operation, sap_id, payload)
    except Exception as error:
        if checkpoint()["operations"].get(operation, {}).get("status") == "ATTEMPTED":
            record(operation, "AMBIGUOUS", f"SAVE path raised after checkpoint: {type(error).__name__}: {error}")
        raise
    status = after.get("status_bar") or {}
    verified = None
    read_error = None
    for _ in range(5):
        try:
            verified = verify(UrllibSapTransport(config), sap_id, payload)
        except Exception as error:
            read_error = error
        if verified is not None:
            break
        time.sleep(1.0)
    if verified is None:
        detail = f"SAVE outcome unresolved for candidate {sap_id}; status={status}; read_error={read_error}"
        record(operation, "AMBIGUOUS", detail)
        raise RuntimeError(detail)
    persist_mapping(args.logical_id, sap_id, payload, fingerprint)
    record(operation, "VERIFIED", f"MM01 Basic Data saved once and independently read back through API_PRODUCT_SRV as {sap_id}; status={status}")
    print(json.dumps({"product": args.logical_id, "result": "CREATED", "sap_id": sap_id,
                      "status_bar": status}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
