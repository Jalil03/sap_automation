"""Read-only discovery of an evidenced FR10 incoming-payment cash/bank account."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex8_fr10_cash_account_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}


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


def table_append(table, values: dict[str, str]) -> None:
    table.AppendRow()
    row = int(table.RowCount)
    for field, value in values.items():
        table._oleobj_.InvokeTypes(
            25,
            0,
            pythoncom.DISPATCH_PROPERTYPUT,
            (pythoncom.VT_EMPTY, 0),
            ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0), (pythoncom.VT_VARIANT, 0)),
            row,
            field,
            value,
        )


def table_get(table, row: int, field: str) -> str:
    return str(
        table._oleobj_.InvokeTypes(
            25,
            0,
            pythoncom.DISPATCH_PROPERTYGET,
            (pythoncom.VT_VARIANT, 0),
            ((pythoncom.VT_I4, 0), (pythoncom.VT_VARIANT, 0)),
            row,
            field,
        )
        or ""
    )


def set_parameter(function, name: str, value: str) -> None:
    get_item(function.Exports, name).Value = value


def rfc_read_table(functions, table_name: str, fields: list[str], options: list[str], rowcount: int = 500) -> dict:
    function = functions.Add("RFC_READ_TABLE")
    set_parameter(function, "QUERY_TABLE", table_name)
    set_parameter(function, "DELIMITER", "|")
    set_parameter(function, "ROWSKIPS", "0")
    set_parameter(function, "ROWCOUNT", str(rowcount))
    field_table = get_item(function.Tables, "FIELDS")
    option_table = get_item(function.Tables, "OPTIONS")
    data_table = get_item(function.Tables, "DATA")
    for field in fields:
        table_append(field_table, {"FIELDNAME": field})
    for option in options:
        if len(option) > 72:
            raise RuntimeError(f"RFC_READ_TABLE option exceeds 72 characters: {option!r}")
        table_append(option_table, {"TEXT": option})
    if not bool(function.Call):
        raise RuntimeError(f"RFC_READ_TABLE failed for {table_name}")
    rows = []
    for row_number in range(1, int(data_table.RowCount) + 1):
        raw = table_get(data_table, row_number, "WA")
        values = [value.strip() for value in raw.split("|")]
        rows.append(dict(zip(fields, values)))
    return {"table": table_name, "fields": fields, "options": options, "row_count": len(rows), "rows": rows}


def save(result: dict) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    load_dotenv(ROOT / ".env")
    username = os.environ.get("SAP_USERNAME", "").upper()
    client = os.environ.get("SAP_CLIENT", "")
    password = os.environ.get("SAP_PASSWORD", "")
    if not password or username != EXPECTED["user"] or client != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")

    result: dict[str, object] = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "RFC_READ_ONLY_DISCOVERY",
        "expected_environment": EXPECTED,
        "target": {"company_code": "FR10", "document_type": "DZ", "currency": "EUR"},
        "write_function_called": False,
    }
    pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode")
    connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]
    connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]
    connection.SystemID = "A4H"
    connection.Client = client
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
            save(result)
            return 2

        result["house_bank_accounts"] = rfc_read_table(
            functions,
            "T012K",
            ["BUKRS", "HBKID", "HKTID", "BANKN", "HKONT", "WAERS"],
            ["BUKRS = 'FR10'"],
        )
        result["recent_dz_headers"] = rfc_read_table(
            functions,
            "BKPF",
            ["BUKRS", "BELNR", "GJAHR", "BLART", "BLDAT", "BUDAT", "WAERS", "STBLG"],
            ["BUKRS = 'FR10' AND BLART = 'DZ'"],
        )

        dz_lines = []
        for header in result["recent_dz_headers"]["rows"]:
            if header.get("STBLG"):
                continue
            options = [
                f"BUKRS = 'FR10' AND BELNR = '{header['BELNR']}'",
                f"AND GJAHR = '{header['GJAHR']}'",
            ]
            lines = rfc_read_table(
                functions,
                "BSEG",
                ["BUKRS", "BELNR", "GJAHR", "BUZEI", "BSCHL", "HKONT", "KUNNR", "WRBTR", "DMBTR", "AUGBL", "AUGDT"],
                options,
                rowcount=100,
            )
            dz_lines.append({"header": header, "lines": lines["rows"]})
        result["dz_documents_with_lines"] = dz_lines

        candidate_accounts = sorted(
            {
                row.get("HKONT", "")
                for item in dz_lines
                for row in item["lines"]
                if row.get("HKONT") and not row.get("KUNNR")
            }
            | {row.get("HKONT", "") for row in result["house_bank_accounts"]["rows"] if row.get("HKONT")}
        )
        result["candidate_accounts"] = candidate_accounts
        account_details = []
        for account in candidate_accounts:
            account_details.append(
                rfc_read_table(
                    functions,
                    "SKB1",
                    ["BUKRS", "SAKNR", "MITKZ", "XOPVW", "WAERS", "XINTB"],
                    [f"BUKRS = 'FR10' AND SAKNR = '{account}'"],
                    rowcount=10,
                )
            )
        result["candidate_account_company_code_details"] = account_details
        result["status"] = "READ_COMPLETE_REVIEW_REQUIRED"
        save(result)
        print(json.dumps({
            "output": str(OUTPUT.relative_to(ROOT)),
            "status": result["status"],
            "house_bank_accounts": result["house_bank_accounts"]["rows"],
            "dz_documents_with_lines": dz_lines,
            "candidate_account_company_code_details": account_details,
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        result["status"] = "READ_ERROR"
        result["error"] = f"{type(error).__name__}: {error}"
        save(result)
        print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "status": result["status"], "error": result["error"]}, ensure_ascii=False, indent=2))
        return 5
    finally:
        try:
            if bool(connection.IsConnected):
                connection.Logoff()
        except Exception:
            pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    raise SystemExit(main())
