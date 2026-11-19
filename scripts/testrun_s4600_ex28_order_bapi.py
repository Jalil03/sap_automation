"""Run sales-order creation BAPI in TESTRUN mode only; never commits."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.testrun_s4600_ex28_quotation_bapi import (
    get_item, structure_dispatch, structure_get, structure_set, table_append, table_get,
)
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

OUTPUT = ROOT / "runtime" / "sap_writes" / "s4600_ex28_order_bapi_testrun.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {
    "header": {
        "DOC_TYPE": "TA", "SALES_ORG": "FR10", "DISTR_CHAN": "10", "DIVISION": "1W",
        "REQ_DATE_H": "20261111", "PURCH_NO_C": "8-900", "REF_DOC": "20000103",
    },
    "item": {"ITM_NUMBER": "000010", "TARGET_QTY": "1", "REF_DOC": "20000103", "REF_DOC_IT": "000010"},
    "partner": {"PARTN_ROLE": "AG", "PARTN_NUMB": "1000000112"},
    "TESTRUN": "X",
}


def lookup(client) -> dict:
    query = urlencode({
        "$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '8-900'",
        "$top": "50",
    })
    response = client.request("GET", f"sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder?{query}", headers={"Accept": "application/json"})
    values = response.json().get("d", {}).get("results", []) if response.status == 200 else []
    return {"http_status": response.status, "count": len(values), "numbers": [str(row.get("SalesOrder")) for row in values]}


def main() -> int:
    load_dotenv(ROOT / ".env"); config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config); before = lookup(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": identity,
        "operation": "BAPI_SALESORDER_CREATEFROMDAT2_TESTRUN_NO_COMMIT", "payload": PAYLOAD,
        "payload_sha256": hashlib.sha256(json.dumps(PAYLOAD, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "before_lookup": before, "commit_called": False, "mode": "TESTRUN",
    }
    if before["http_status"] != 200 or before["count"]:
        result["status"] = "BLOCKED_LOOKUP"; OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8"); return 2
    pythoncom.CoInitialize(); functions = win32com.client.Dispatch("SAP.Functions.Unicode"); connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]; connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]; connection.SystemID = "A4H"
    connection.Client = config.client; connection.User = config.username; connection.Password = os.environ["SAP_PASSWORD"]; connection.Language = "F"
    if not bool(connection.Logon(0, True)):
        raise SystemExit("Blocked: RFC logon failed")
    actual = {"system": str(connection.SystemID).upper(), "client": str(connection.Client), "user": str(connection.User).upper()}
    if actual != EXPECTED:
        connection.Logoff(); raise SystemExit(f"Blocked: RFC identity mismatch {actual!r}")
    bapi = functions.Add("BAPI_SALESORDER_CREATEFROMDAT2")
    header = structure_dispatch(get_item(bapi.Exports, "ORDER_HEADER_IN")); header_x = structure_dispatch(get_item(bapi.Exports, "ORDER_HEADER_INX"))
    for field, value in PAYLOAD["header"].items():
        structure_set(header, field, value); structure_set(header_x, field, "X")
    structure_set(header_x, "UPDATEFLAG", "I")
    item_values = PAYLOAD["item"]
    item_x_values = {"ITM_NUMBER": item_values["ITM_NUMBER"], "UPDATEFLAG": "I", **{field: "X" for field in item_values if field != "ITM_NUMBER"}}
    tables = {name: get_item(bapi.Tables, name) for name in ("ORDER_ITEMS_IN", "ORDER_ITEMS_INX", "ORDER_PARTNERS", "RETURN")}
    item_row = table_append(tables["ORDER_ITEMS_IN"], item_values); table_append(tables["ORDER_ITEMS_INX"], item_x_values)
    partner_row = table_append(tables["ORDER_PARTNERS"], PAYLOAD["partner"])
    get_item(bapi.Exports, "TESTRUN").Value = "X"
    result["staged_readback"] = {
        "header": {field: structure_get(header, field) for field in PAYLOAD["header"]},
        "item": {field: table_get(tables["ORDER_ITEMS_IN"], item_row, field) for field in item_values},
        "partner": {field: table_get(tables["ORDER_PARTNERS"], partner_row, field) for field in PAYLOAD["partner"]},
    }
    result["status"] = "SUBMITTED_TESTRUN"; OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    call_ok = bool(bapi.Call); return_table = tables["RETURN"]
    messages = [{field: table_get(return_table, row, field) for field in ("TYPE", "ID", "NUMBER", "MESSAGE", "PARAMETER", "ROW", "FIELD")} for row in range(1, int(return_table.RowCount) + 1)]
    returned = str(get_item(bapi.Imports, "SALESDOCUMENT").Value or ""); connection.Logoff(); after = lookup(client)
    errors = [message for message in messages if str(message.get("TYPE", "")).upper() in {"E", "A", "X"}]
    result.update(call_ok=call_ok, return_messages=messages, returned_sales_document=returned, after_lookup=after)
    result["status"] = "TESTRUN_VALID" if call_ok and not errors and before == after else "TESTRUN_REJECTED" if errors and before == after else "AMBIGUOUS"
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"); print(json.dumps(result, ensure_ascii=False, indent=2, default=str)); return 0 if result["status"] == "TESTRUN_VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
