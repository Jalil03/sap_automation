"""Run BAPI quotation creation in TESTRUN mode only; never commits."""

from __future__ import annotations

import argparse
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

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

OCX = Path(r"C:\Program Files\SAP\FrontEnd\SapGui\wdtfuncs.ocx")
OUTPUT = ROOT / "runtime" / "sap_writes" / "s4600_ex28_quotation_bapi_testrun.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
PAYLOAD = {
    "header": {
        "DOC_TYPE": "AG", "SALES_ORG": "FR10", "DISTR_CHAN": "10", "DIVISION": "1W",
        "REQ_DATE_H": "20261111", "QT_VALID_F": "20261021", "QT_VALID_T": "20261101",
        "REF_DOC": "10000104",
    },
    "item": {
        "ITM_NUMBER": "000010", "TARGET_QTY": "2",
        "REF_DOC": "10000104", "REF_DOC_IT": "000010",
    },
    "partner": {"PARTN_ROLE": "AG", "PARTN_NUMB": "1000000112"},
    "TESTRUN": "X",
}


def fingerprint() -> str:
    raw = json.dumps(PAYLOAD, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def get_item(collection, key):
    try:
        values = list(collection)
    except Exception:
        values = []
    for value in values:
        if str(getattr(value, "Name", "")) == key:
            return value
    for accessor in (lambda: collection.Item(key), lambda: collection(key)):
        try:
            value = accessor()
            if value is not None:
                return value
        except Exception:
            continue
    raise RuntimeError(f"COM item not found: {key}")


def structure_dispatch(parameter):
    library = pythoncom.LoadTypeLib(str(OCX))
    iid = next(
        library.GetTypeInfo(index).GetTypeAttr()[0]
        for index in range(library.GetTypeInfoCount())
        if str(library.GetDocumentation(index)[0]) == "IStructure"
    )
    return parameter._oleobj_.QueryInterface(iid, pythoncom.IID_IDispatch)


def structure_set(raw, field: str, value: str) -> None:
    raw.InvokeTypes(
        9, 0, pythoncom.DISPATCH_PROPERTYPUT, (pythoncom.VT_EMPTY, 0),
        ((pythoncom.VT_VARIANT, 0), (pythoncom.VT_VARIANT, 0)), field, value,
    )


def structure_get(raw, field: str):
    return raw.InvokeTypes(
        9, 0, pythoncom.DISPATCH_PROPERTYGET, (pythoncom.VT_VARIANT, 0),
        ((pythoncom.VT_VARIANT, 0),), field,
    )


def table_append(table, values: dict[str, str]) -> int:
    table.AppendRow()
    row = int(table.RowCount)
    for field, value in values.items():
        table._oleobj_.InvokeTypes(
            25, 0, pythoncom.DISPATCH_PROPERTYPUT, (pythoncom.VT_EMPTY, 0),
            ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0), (pythoncom.VT_VARIANT, 0)),
            row, field, value,
        )
    return row


def table_get(table, row: int, field: str):
    return table._oleobj_.InvokeTypes(
        25, 0, pythoncom.DISPATCH_PROPERTYGET, (pythoncom.VT_VARIANT, 0),
        ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0)), row, field,
    )


def quotation_lookup(client) -> dict:
    query = urlencode({
        "$filter": "SalesOrganization eq 'FR10' and DistributionChannel eq '10' and OrganizationDivision eq '1W' and SoldToParty eq '1000000112'",
        "$top": "50",
    })
    response = client.request("GET", f"sap/opu/odata/sap/API_SALES_QUOTATION_SRV/A_SalesQuotation?{query}", headers={"Accept": "application/json"})
    rows = response.json().get("d", {}).get("results", []) if response.status == 200 else []
    return {"http_status": response.status, "count": len(rows), "numbers": [str(row.get("SalesQuotation")) for row in rows]}


def save(result: dict) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-testrun", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    before = quotation_lookup(client)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(), "environment": identity,
        "operation": "BAPI_QUOTATION_CREATEFROMDATA2_TESTRUN_NO_COMMIT", "payload": PAYLOAD,
        "payload_sha256": fingerprint(), "before_lookup": before, "commit_called": False,
        "mode": "TESTRUN" if args.execute_testrun else "LOCAL_STAGE_ONLY",
    }
    if before["http_status"] != 200 or before["count"]:
        result["status"] = "BLOCKED_LOOKUP"
        save(result)
        return 2

    pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode")
    connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]; connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]; connection.SystemID = "A4H"
    connection.Client = config.client; connection.User = config.username; connection.Password = os.environ["SAP_PASSWORD"]; connection.Language = "F"
    if not bool(connection.Logon(0, True)):
        raise SystemExit("Blocked: RFC logon failed")
    actual = {"system": str(connection.SystemID).upper(), "client": str(connection.Client), "user": str(connection.User).upper()}
    if actual != EXPECTED:
        connection.Logoff(); raise SystemExit(f"Blocked: RFC identity mismatch {actual!r}")

    bapi = functions.Add("BAPI_QUOTATION_CREATEFROMDATA2")
    header = structure_dispatch(get_item(bapi.Exports, "QUOTATION_HEADER_IN"))
    header_x = structure_dispatch(get_item(bapi.Exports, "QUOTATION_HEADER_INX"))
    for field, value in PAYLOAD["header"].items():
        structure_set(header, field, value); structure_set(header_x, field, "X")
    structure_set(header_x, "UPDATEFLAG", "I")
    staged = {"header": {field: structure_get(header, field) for field in PAYLOAD["header"]}}

    item_values = PAYLOAD["item"]
    item_x_values = {"ITM_NUMBER": item_values["ITM_NUMBER"], "UPDATEFLAG": "I", **{field: "X" for field in item_values if field != "ITM_NUMBER"}}
    partner_values = PAYLOAD["partner"]
    tables = {name: get_item(bapi.Tables, name) for name in ("QUOTATION_ITEMS_IN", "QUOTATION_ITEMS_INX", "QUOTATION_PARTNERS", "QUOTATION_SCHEDULES_IN", "QUOTATION_SCHEDULES_INX", "RETURN")}
    rows = {
        "item": table_append(tables["QUOTATION_ITEMS_IN"], item_values),
        "item_x": table_append(tables["QUOTATION_ITEMS_INX"], item_x_values),
        "partner": table_append(tables["QUOTATION_PARTNERS"], partner_values),
    }
    staged["tables"] = {
        "item": {field: table_get(tables["QUOTATION_ITEMS_IN"], rows["item"], field) for field in item_values},
        "partner": {field: table_get(tables["QUOTATION_PARTNERS"], rows["partner"], field) for field in partner_values},
    }
    get_item(bapi.Exports, "TESTRUN").Value = "X"
    result["staged_readback"] = staged
    if not args.execute_testrun:
        result["status"] = "LOCAL_STAGE_VERIFIED"
        connection.Logoff(); save(result); print(json.dumps(result, ensure_ascii=False, indent=2, default=str)); return 0

    result["status"] = "SUBMITTED_TESTRUN"
    save(result)
    call_ok = bool(bapi.Call)
    return_table = tables["RETURN"]
    messages = [
        {field: table_get(return_table, row, field) for field in ("TYPE", "ID", "NUMBER", "MESSAGE", "PARAMETER", "ROW", "FIELD")}
        for row in range(1, int(return_table.RowCount) + 1)
    ]
    sales_document = str(get_item(bapi.Imports, "SALESDOCUMENT").Value or "")
    connection.Logoff()
    after = quotation_lookup(client)
    result.update(call_ok=call_ok, return_messages=messages, returned_sales_document=sales_document, after_lookup=after)
    errors = [message for message in messages if str(message.get("TYPE", "")).upper() in {"E", "A", "X"}]
    unchanged = before == after
    result["status"] = "TESTRUN_VALID" if call_ok and not errors and unchanged else "TESTRUN_REJECTED" if errors and unchanged else "AMBIGUOUS"
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result["status"] == "TESTRUN_VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
