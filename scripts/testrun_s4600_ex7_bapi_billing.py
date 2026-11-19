"""Run one non-persisting TESTRUN of the installed billing BAPI."""

from __future__ import annotations

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

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_bapi_billing_testrun2_padded_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
FUNCTION = "BAPI_BILLINGDOC_CREATEMULTIPLE"
DELIVERY = "80000085"
TEST_INPUT = [
    {"REF_DOC": "0080000085", "REF_ITEM": "000010", "REF_DOC_CA": "J"},
    {"REF_DOC": "0080000085", "REF_ITEM": "000020", "REF_DOC_CA": "J"},
]


def get_item(collection, key):
    try:
        for value in list(collection):
            if str(getattr(value, "Name", "")).upper() == key.upper():
                return value
    except Exception:
        pass
    for accessor in (lambda: collection.Item(key), lambda: collection(key)):
        try:
            value = accessor()
            if value is not None:
                return value
        except Exception:
            continue
    raise RuntimeError(f"COM item not found: {key}")


def set_parameter(function, name: str, value: str) -> None:
    get_item(function.Exports, name).Value = value


def table_set(table, row: int, field: str, value: str) -> None:
    table._oleobj_.InvokeTypes(
        25, 0, pythoncom.DISPATCH_PROPERTYPUT, (pythoncom.VT_EMPTY, 0),
        ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0), (pythoncom.VT_VARIANT, 0)),
        row, field, value,
    )


def table_get(table, row: int, field: str) -> str:
    return str(table._oleobj_.InvokeTypes(
        25, 0, pythoncom.DISPATCH_PROPERTYGET, (pythoncom.VT_VARIANT, 0),
        ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0)), row, field,
    ) or "")


def append_row(table, values: dict[str, str]) -> None:
    table.AppendRow()
    row = int(table.RowCount)
    for field, value in values.items():
        table_set(table, row, field, value)


def read_rows(table, fields: list[str]) -> list[dict[str, str]]:
    return [
        {field: table_get(table, row, field) for field in fields}
        for row in range(1, int(table.RowCount) + 1)
    ]


def billing_lookup(client) -> dict:
    query = urlencode({"$filter": f"ReferenceSDDocument eq '{DELIVERY}'", "$top": "100"})
    response = client.request(
        "GET", f"sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV/A_BillingDocumentItem?{query}",
        headers={"Accept": "application/json"},
    )
    return {
        "http_status": response.status,
        "rows": response.json().get("d", {}).get("results", []) if response.status == 200 else [],
        "error": None if response.status == 200 else response.sanitized_sap_error(),
    }


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit("Blocked: the second and final TESTRUN is already recorded")
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    username = os.environ.get("SAP_USERNAME", "").upper()
    client_number = os.environ.get("SAP_CLIENT", "")
    password = os.environ.get("SAP_PASSWORD", "")
    if not password or username != EXPECTED["user"] or client_number != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")
    transport = UrllibSapTransport(config)
    before = billing_lookup(transport)
    if before["http_status"] != 200 or before["rows"]:
        raise SystemExit("Blocked: exact pre-test billing absence not proven")
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "BAPI_TESTRUN_NO_COMMIT",
        "expected_environment": EXPECTED,
        "function": FUNCTION,
        "attempt_sequence": 2,
        "authorization": "Explicit user confirmation for one final padded-reference TESTRUN",
        "testrun": "X",
        "posting": "",
        "billingdatain": TEST_INPUT,
        "before_lookup": before,
        "bapi_transaction_commit_called": False,
    }
    pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode")
    connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]
    connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]
    connection.SystemID = "A4H"
    connection.Client = client_number
    connection.User = username
    connection.Password = password
    connection.Language = "FR"
    try:
        logged_on = bool(connection.Logon(0, True))
        actual = {
            "system": str(connection.SystemID).upper(),
            "client": str(connection.Client),
            "user": str(connection.User).upper(),
        }
        result["identity"] = {**actual, "logon_return": logged_on, "is_connected": bool(connection.IsConnected)}
        if not bool(connection.IsConnected) or actual != EXPECTED:
            result["status"] = "BLOCKED_IDENTITY"
            return 2
        function = functions.Add(FUNCTION)
        set_parameter(function, "TESTRUN", "X")
        set_parameter(function, "POSTING", "")
        input_table = get_item(function.Tables, "BILLINGDATAIN")
        for values in TEST_INPUT:
            append_row(input_table, values)
        result["function_call_attempts"] = 1
        result["function_call_return"] = bool(function.Call)
        result["return"] = read_rows(
            get_item(function.Tables, "RETURN"),
            ["TYPE", "ID", "NUMBER", "MESSAGE", "MESSAGE_V1", "MESSAGE_V2", "MESSAGE_V3", "MESSAGE_V4"],
        )
        result["errors"] = read_rows(
            get_item(function.Tables, "ERRORS"),
            ["REF_DOC", "REF_DOC_ITEM", "TYPE", "ID", "NUMBER", "MESSAGE", "MESSAGE_V1", "MESSAGE_V2"],
        )
        result["success"] = read_rows(
            get_item(function.Tables, "SUCCESS"),
            ["REF_DOC", "REF_DOC_ITEM", "BILL_DOC", "BILL_DOC_ITEM", "NET_VALUE", "TAX_VALUE", "CURRENCY"],
        )
    finally:
        try:
            if bool(connection.IsConnected):
                connection.Logoff()
        except Exception:
            pass
    after = billing_lookup(transport)
    result["after_lookup"] = after
    if after["http_status"] != 200 or after["rows"]:
        result["status"] = "SAFETY_VIOLATION_PERSISTED_DOCUMENT_DETECTED"
        exit_code = 2
    elif any(row.get("TYPE") in {"E", "A"} for row in result.get("return", []) + result.get("errors", [])):
        result["status"] = "TESTRUN_REJECTED"
        exit_code = 2
    else:
        result["status"] = "TESTRUN_ACCEPTED_NO_DOCUMENT_CREATED"
        exit_code = 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
