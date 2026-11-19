"""Inspect BAPI_SALESORDER_CREATEFROMDAT2 metadata without calling it."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_rfc_bapi_order_preflight_2026-10-21.json"


def names(collection) -> list[str]:
    try:
        values = list(collection)
    except Exception:
        values = []
    return [str(getattr(value, "Name", "")) for value in values]


def main() -> int:
    load_dotenv(ROOT / ".env"); pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode"); connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]; connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]; connection.SystemID = "A4H"
    connection.Client = os.environ["SAP_CLIENT"]; connection.User = os.environ["SAP_USERNAME"]; connection.Password = os.environ["SAP_PASSWORD"]; connection.Language = "F"
    if not bool(connection.Logon(0, True)):
        raise SystemExit("Blocked: RFC logon failed")
    identity = {"system": str(connection.SystemID).upper(), "client": str(connection.Client), "user": str(connection.User).upper()}
    if identity != {"system": "A4H", "client": "600", "user": "ABDELJ"}:
        raise SystemExit(f"Blocked: {identity!r}")
    bapi = functions.Add("BAPI_SALESORDER_CREATEFROMDAT2")
    result = {"mode": "RFC_METADATA_ONLY_NO_BAPI_CALL", "environment": identity, "bapi_called": False, "exports": names(bapi.Exports), "imports": names(bapi.Imports), "tables": names(bapi.Tables)}
    connection.Logoff(); OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
