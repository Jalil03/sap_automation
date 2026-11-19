"""Create one billing document from delivery 80000085 after exact FI approval."""

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

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
DELIVERY = "80000085"
FUNCTION = "BAPI_BILLINGDOC_CREATEMULTIPLE"
OPERATION = "CREATE_AND_POST_ONE_BILLING_FROM_DELIVERY_80000085"
INPUT_ROWS = [
    {"REF_DOC": "0080000085", "REF_ITEM": "000010", "REF_DOC_CA": "J"},
    {"REF_DOC": "0080000085", "REF_ITEM": "000020", "REF_DOC_CA": "J"},
]
WORKFLOW = {
    "operation": OPERATION,
    "environment": EXPECTED,
    "function": FUNCTION,
    "parameters": {"TESTRUN": "", "POSTING": ""},
    "billingdatain": INPUT_ROWS,
    "expected_result": {
        "one_billing_document": True,
        "company_code": "FR10",
        "payer": "1000000112",
        "currency": "EUR",
        "net_amount": "3100.00",
        "tax_amount": "620.00",
        "accounting_transfer_status": "C",
    },
    "maximum_function_calls": 1,
    "no_automatic_retry": True,
}
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH3_EX7.billing_delivery80000085.workflow_approval.json"
DRY_RUN = ROOT / "runtime" / "sap_reads" / "s4600_ex7_billing_delivery80000085_dry_run.json"
RESULT = ROOT / "runtime" / "sap_writes" / "s4600_ex7_billing_delivery80000085_result.json"
TESTRUN_EVIDENCE = ROOT / "runtime" / "sap_reads" / "s4600_ex7_bapi_billing_testrun2_padded_2026-10-22.json"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def workflow_hash() -> str:
    return hashlib.sha256(canonical(WORKFLOW)).hexdigest()


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def save(result: dict) -> None:
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    path = RESULT if result["mode"] == "EXECUTE" else DRY_RUN
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    return [{field: table_get(table, row, field) for field in fields} for row in range(1, int(table.RowCount) + 1)]


def billing_lookup(client) -> dict:
    query = urlencode({"$filter": f"ReferenceSDDocument eq '{DELIVERY}'", "$top": "100"})
    response = client.request(
        "GET", f"sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV/A_BillingDocumentItem?{query}",
        headers={"Accept": "application/json"},
    )
    rows = clean(response.json().get("d", {}).get("results", [])) if response.status == 200 else []
    return {
        "http_status": response.status,
        "rows": rows,
        "error": None if response.status == 200 else response.sanitized_sap_error(),
    }


def billing_headers(client, identifiers: set[str]) -> dict:
    result = {}
    for identifier in sorted(identifiers):
        response = client.request(
            "GET", f"sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV/A_BillingDocument('{identifier}')",
            headers={"Accept": "application/json"},
        )
        result[identifier] = {
            "http_status": response.status,
            "row": clean(response.json().get("d", {})) if response.status == 200 else {},
            "error": None if response.status == 200 else response.sanitized_sap_error(),
        }
    return result


def delivery_readback(client) -> dict:
    response = client.request(
        "GET", f"sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV/A_OutbDeliveryHeader('{DELIVERY}')",
        headers={"Accept": "application/json"},
    )
    return {
        "http_status": response.status,
        "row": clean(response.json().get("d", {})) if response.status == 200 else {},
        "error": None if response.status == 200 else response.sanitized_sap_error(),
    }


def load_approval() -> dict:
    value = json.loads(APPROVAL.read_text(encoding="utf-8"))
    constraints = value.get("constraints", {})
    if (
        value.get("status") != "APPROVED"
        or value.get("environment") != EXPECTED
        or value.get("operation_scope") != OPERATION
        or value.get("workflow_sha256") != workflow_hash()
        or constraints.get("maximum_function_calls") != 1
        or constraints.get("no_automatic_retry") is not True
        or constraints.get("independent_readback_required") is not True
    ):
        raise RuntimeError("Exact billing/FI workflow approval does not match")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--print-fingerprint", action="store_true")
    args = parser.parse_args()
    if args.print_fingerprint:
        print(workflow_hash())
        return 0
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    tested = json.loads(TESTRUN_EVIDENCE.read_text(encoding="utf-8"))
    if tested.get("status") != "TESTRUN_ACCEPTED_NO_DOCUMENT_CREATED" or tested.get("billingdatain") != INPUT_ROWS:
        raise SystemExit("Blocked: successful exact TESTRUN evidence is missing")
    if RESULT.exists() and json.loads(RESULT.read_text(encoding="utf-8")).get("attempts"):
        raise SystemExit("Blocked: a real billing attempt is already recorded; reconcile instead of retrying")
    transport = UrllibSapTransport(config)
    before = billing_lookup(transport)
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "operation": OPERATION,
        "workflow": WORKFLOW,
        "workflow_sha256": workflow_hash(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "duplicate_lookup": before,
        "attempts": [],
    }
    if before["http_status"] != 200 or before["rows"]:
        result["status"] = "BLOCKED_DUPLICATE_OR_UNKNOWN"
        save(result)
        return 2
    if not args.execute:
        result["status"] = "DRY_RUN_OK"
        save(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval = load_approval()
    result["approval_id"] = approval["approval_id"]
    username = os.environ.get("SAP_USERNAME", "").upper()
    client_number = os.environ.get("SAP_CLIENT", "")
    password = os.environ.get("SAP_PASSWORD", "")
    if not password or username != EXPECTED["user"] or client_number != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")
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
    call_error = None
    try:
        logged_on = bool(connection.Logon(0, True))
        actual = {
            "system": str(connection.SystemID).upper(),
            "client": str(connection.Client),
            "user": str(connection.User).upper(),
        }
        result["rfc_identity"] = {**actual, "logon_return": logged_on, "is_connected": bool(connection.IsConnected)}
        if not bool(connection.IsConnected) or actual != EXPECTED:
            result["status"] = "BLOCKED_RFC_IDENTITY"
            save(result)
            return 2
        function = functions.Add(FUNCTION)
        set_parameter(function, "TESTRUN", "")
        set_parameter(function, "POSTING", "")
        input_table = get_item(function.Tables, "BILLINGDATAIN")
        for values in INPUT_ROWS:
            append_row(input_table, values)
        attempt = {
            "operation": FUNCTION,
            "status": "SUBMITTED",
            "attempt_number": 1,
            "input": INPUT_ROWS,
            "testrun": "",
            "posting": "",
            "separate_bapi_transaction_commit_called": False,
        }
        result["attempts"].append(attempt)
        result["status"] = "SUBMITTED"
        save(result)
        try:
            attempt["function_call_return"] = bool(function.Call)
        except Exception as error:
            call_error = f"{type(error).__name__}: RFC outcome unknown"
            attempt["status"] = "AMBIGUOUS_NO_RETRY"
        if call_error is None:
            attempt["return"] = read_rows(
                get_item(function.Tables, "RETURN"),
                ["TYPE", "ID", "NUMBER", "MESSAGE", "MESSAGE_V1", "MESSAGE_V2", "MESSAGE_V3", "MESSAGE_V4"],
            )
            attempt["errors"] = read_rows(
                get_item(function.Tables, "ERRORS"),
                ["REF_DOC", "REF_DOC_ITEM", "TYPE", "ID", "NUMBER", "MESSAGE", "MESSAGE_V1", "MESSAGE_V2"],
            )
            attempt["success"] = read_rows(
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
    identifiers = {str(row.get("BillingDocument")) for row in after["rows"] if row.get("BillingDocument")}
    headers = billing_headers(transport, identifiers)
    delivery = delivery_readback(transport)
    result["independent_readback"] = {"billing_items": after, "billing_headers": headers, "delivery": delivery}
    if call_error:
        result["attempts"][0]["error"] = call_error
        result["status"] = "AMBIGUOUS_RECONCILED_DOCUMENT_FOUND" if identifiers else "AMBIGUOUS_NO_DOCUMENT_FOUND_NO_RETRY"
        save(result)
        return 2
    messages = result["attempts"][0].get("return", []) + result["attempts"][0].get("errors", [])
    if any(row.get("TYPE") in {"E", "A"} for row in messages):
        result["attempts"][0]["status"] = "FAILED_NO_RETRY"
        result["status"] = "FAILED"
        save(result)
        return 2
    verified = False
    if len(identifiers) == 1:
        identifier = next(iter(identifiers))
        header = headers.get(identifier, {}).get("row", {})
        item_numbers = {str(row.get("BillingDocumentItem")) for row in after["rows"]}
        verified = (
            headers[identifier]["http_status"] == 200
            and item_numbers == {"000010", "000020"}
            and header.get("CompanyCode") == "FR10"
            and header.get("PayerParty") == "1000000112"
            and header.get("TransactionCurrency") == "EUR"
            and header.get("TotalNetAmount") == "3100.00"
            and header.get("TaxAmount") == "620.00"
            and bool(header.get("AccountingDocument"))
            and header.get("AccountingPostingStatus") == "C"
            and header.get("AccountingTransferStatus") == "C"
            and delivery["row"].get("OverallDelivReltdBillgStatus") == "C"
        )
    result["status"] = "VERIFIED_BILLING_AND_FI_POSTING" if verified else "CREATED_READBACK_NOT_FULLY_VERIFIED"
    result["attempts"][0]["status"] = result["status"]
    save(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
