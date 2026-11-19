"""Inspect the installed billing BAPI interface without calling it."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_bapi_billing_preflight_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
FUNCTION = "BAPI_BILLINGDOC_CREATEMULTIPLE"


def members(value) -> list[str]:
    try:
        info = value._oleobj_.GetTypeInfo()
        attr = info.GetTypeAttr()
        names: set[str] = set()
        for index in range(attr[6]):
            desc = info.GetFuncDesc(index)
            names.update(str(item) for item in info.GetNames(desc[0]) if item)
        for index in range(attr[7]):
            desc = info.GetVarDesc(index)
            names.update(str(item) for item in info.GetNames(desc[0]) if item)
        return sorted(names)
    except Exception:
        return []


def collection_items(collection):
    try:
        values = list(collection)
        if values:
            return values
    except Exception:
        pass
    values = []
    for index in range(1, int(collection.Count) + 1):
        for accessor in (lambda: collection.Item(index), lambda: collection(index)):
            try:
                item = accessor()
                if item is not None:
                    values.append(item)
                    break
            except Exception:
                continue
    return values


def describe_collection(collection) -> list[dict]:
    result = []
    for index, item in enumerate(collection_items(collection), 1):
        entry = {
            "index": index,
            "name": str(getattr(item, "Name", "") or index),
            "members": members(item),
        }
        for attribute in ("Type", "ColumnCount", "RowCount"):
            try:
                entry[attribute] = str(getattr(item, attribute))
            except Exception:
                pass
        try:
            entry["columns"] = [str(getattr(column, "Name", "") or column) for column in collection_items(item.Columns)]
        except Exception:
            entry["columns"] = []
        result.append(entry)
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    username = os.environ.get("SAP_USERNAME", "").upper()
    client = os.environ.get("SAP_CLIENT", "")
    password = os.environ.get("SAP_PASSWORD", "")
    if not password or username != EXPECTED["user"] or client != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "RFC_READ_ONLY_FUNCTION_INTERFACE_INSPECTION",
        "expected_environment": EXPECTED,
        "function": FUNCTION,
        "function_called": False,
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
            return 2
        bapi = functions.Add(FUNCTION)
        result["function_available"] = bapi is not None
        result["function_members"] = members(bapi)
        for name in ("Exports", "Imports", "Tables", "Changing"):
            try:
                result[name.lower()] = describe_collection(getattr(bapi, name))
            except Exception as error:
                result[name.lower()] = {"unavailable": f"{type(error).__name__}: {error}"}
        result["status"] = "AVAILABLE_NOT_CALLED"
        return 0
    finally:
        try:
            if bool(connection.IsConnected):
                connection.Logoff()
        finally:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
