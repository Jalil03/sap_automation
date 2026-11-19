"""Independently reconcile the single S4600 exercise 31 PR00 write by RFC reads."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_pr00_rfc_readback_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
TARGET = {
    "condition_type": "PR00",
    "customer": "1000000112",
    "material": "90000133",
    "plant": "FR10",
    "rate": "150.00",
    "currency": "EUR",
    "pricing_unit": "1",
    "quantity_unit": "H",
    "valid_from": "20261022",
    "valid_to": "20261231",
}


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


def rfc_read_table(functions, table_name: str, fields: list[str], options: list[str]) -> dict:
    function = functions.Add("RFC_READ_TABLE")
    set_parameter(function, "QUERY_TABLE", table_name)
    set_parameter(function, "DELIMITER", "|")
    set_parameter(function, "ROWSKIPS", "0")
    set_parameter(function, "ROWCOUNT", "100")
    field_table = get_item(function.Tables, "FIELDS")
    option_table = get_item(function.Tables, "OPTIONS")
    data_table = get_item(function.Tables, "DATA")
    for field in fields:
        table_append(field_table, {"FIELDNAME": field})
    for option in options:
        if len(option) > 72:
            raise RuntimeError(f"RFC_READ_TABLE option exceeds 72 characters: {option!r}")
        table_append(option_table, {"TEXT": option})
    called = bool(function.Call)
    if not called:
        details = []
        for name in ("Exception", "ExceptionText"):
            try:
                value = getattr(function, name)
                details.append(f"{name}={value() if callable(value) else value}")
            except Exception:
                continue
        suffix = f" ({'; '.join(details)})" if details else ""
        raise RuntimeError(f"RFC_READ_TABLE failed for {table_name}{suffix}")
    rows = []
    for row_number in range(1, int(data_table.RowCount) + 1):
        raw = table_get(data_table, row_number, "WA")
        values = [value.strip() for value in raw.split("|")]
        rows.append(dict(zip(fields, values)))
    return {"table": table_name, "fields": fields, "options": options, "row_count": len(rows), "rows": rows}


def normalized_identifier(value: str) -> str:
    stripped = value.strip().lstrip("0")
    return stripped or "0"


def normalized_number(value: str) -> str:
    text = value.strip().replace(" ", "").replace(",", ".")
    try:
        return f"{float(text):.2f}"
    except ValueError:
        return text


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
        "mode": "RFC_READ_ONLY_INDEPENDENT_READBACK",
        "expected_environment": EXPECTED,
        "target": TARGET,
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
        connected = bool(connection.IsConnected)
        result["identity"] = {**actual, "logon_return": logged_on, "is_connected": connected}
        if not logged_on:
            try:
                result["identity"]["logon_error"] = str(connection.LastError())
            except Exception as logon_error:
                result["identity"]["logon_error"] = f"UNAVAILABLE:{type(logon_error).__name__}:{logon_error}"
        if not connected or actual != EXPECTED:
            result["status"] = "BLOCKED_IDENTITY"
            save(result)
            return 2

        ping = functions.Add("RFC_PING")
        ping_ok = bool(ping.Call)
        result["rfc_ping"] = {"success": ping_ok}
        if not ping_ok:
            result["status"] = "BLOCKED_RFC_PING"
            save(result)
            return 2

        a972 = rfc_read_table(
            functions,
            "A972",
            ["KAPPL", "KSCHL", "KUNNR", "MATNR", "WERKS", "DATAB", "DATBI", "KNUMH"],
            ["KAPPL = 'V' AND KSCHL = 'PR00'", "AND KUNNR = '1000000112'", "AND WERKS = 'FR10'"],
        )
        result["a972"] = a972
        matches = [
            row
            for row in a972["rows"]
            if row["KSCHL"] == TARGET["condition_type"]
            and row["KUNNR"] == TARGET["customer"]
            and normalized_identifier(row["MATNR"]) == TARGET["material"]
            and row["WERKS"] == TARGET["plant"]
            and row["DATAB"] == TARGET["valid_from"]
            and row["DATBI"] == TARGET["valid_to"]
        ]
        result["exact_a972_matches"] = matches
        if len(matches) != 1:
            result["status"] = "UNKNOWN_NOT_EXACTLY_ONE_A972_MATCH"
            save(result)
            return 3

        condition_number = matches[0]["KNUMH"]
        konp = rfc_read_table(
            functions,
            "KONP",
            ["KNUMH", "KBETR", "KONWA", "KPEIN", "KMEIN"],
            [f"KNUMH = '{condition_number}'"],
        )
        result["konp"] = konp
        exact = [
            row
            for row in konp["rows"]
            if normalized_number(row["KBETR"]) == TARGET["rate"]
            and row["KONWA"] == TARGET["currency"]
            and normalized_identifier(row["KPEIN"]) == TARGET["pricing_unit"]
            and row["KMEIN"] == TARGET["quantity_unit"]
        ]
        result["exact_konp_matches"] = exact
        result["status"] = "VERIFIED" if len(exact) == 1 else "UNKNOWN_KONP_VALUE_MISMATCH"
        save(result)
        return 0 if result["status"] == "VERIFIED" else 4
    except Exception as error:
        result["status"] = "READBACK_ERROR"
        result["error"] = f"{type(error).__name__}: {error}"
        try:
            result["connection_last_error"] = str(connection.LastError())
        except Exception as last_error:
            result["connection_last_error"] = f"UNAVAILABLE:{type(last_error).__name__}:{last_error}"
        save(result)
        return 5
    finally:
        try:
            if connection.IsConnected:
                connection.Logoff()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
