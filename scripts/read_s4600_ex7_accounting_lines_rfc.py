"""Read the exact FI line items for exercise 7; no write function is called."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

from readback_s4600_ex31_pr00_rfc import rfc_read_table

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_accounting_document_9300000009_2026-10-22.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
TARGET = {"company_code": "FR10", "fiscal_year": "2026", "accounting_document": "9300000009"}


def main() -> int:
    load_dotenv(ROOT / ".env")
    username = os.environ.get("SAP_USERNAME", "").upper()
    client = os.environ.get("SAP_CLIENT", "")
    password = os.environ.get("SAP_PASSWORD", "")
    if not password or username != EXPECTED["user"] or client != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "RFC_READ_ONLY_ACCOUNTING_DOCUMENT_LINES",
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
        result["identity"] = {**actual, "logon_return": logged_on, "is_connected": bool(connection.IsConnected)}
        if not bool(connection.IsConnected) or actual != EXPECTED:
            result["status"] = "BLOCKED_IDENTITY"
            return 2
        result["line_items"] = rfc_read_table(
            functions,
            "BSEG",
            [
                "BUKRS", "BELNR", "GJAHR", "BUZEI", "BSCHL", "SHKZG", "HKONT", "KUNNR",
                "WRBTR", "DMBTR", "SGTXT", "ZTERM", "ZFBDT", "ZBD1T", "ZBD1P", "SKFBT", "WSKTO"
            ],
            ["BUKRS = 'FR10' AND BELNR = '9300000009'", "AND GJAHR = '2026'"],
        )
        result["status"] = "VERIFIED" if result["line_items"]["row_count"] > 0 else "UNKNOWN_NO_LINES"
        return 0 if result["status"] == "VERIFIED" else 2
    except Exception as error:
        result["status"] = "UNKNOWN_READ_FAILED"
        result["error"] = f"{type(error).__name__}: {error}"
        return 2
    finally:
        try:
            if bool(connection.IsConnected):
                connection.Logoff()
        except Exception:
            pass
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
