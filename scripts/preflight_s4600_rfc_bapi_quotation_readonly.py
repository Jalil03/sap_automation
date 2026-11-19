"""Prove the installed RFC route and inspect quotation BAPI metadata; no write call."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_rfc_bapi_quotation_preflight_2026-10-21.json"
EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}


def members(value) -> list[str]:
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


def collection_names(collection) -> list[str]:
    result = []
    try:
        values = list(collection)
    except Exception:
        values = []
    if not values:
        for index in range(1, int(collection.Count) + 1):
            item = None
            for accessor in (
                lambda: collection.Item(index),
                lambda: collection(index),
            ):
                try:
                    item = accessor()
                    if item is not None:
                        break
                except Exception:
                    continue
            if item is None:
                raise RuntimeError(f"Unable to read collection item {index}")
            values.append(item)
    for index, item in enumerate(values, 1):
        result.append(str(getattr(item, "Name", "") or getattr(item, "name", "") or index))
    return result


def main() -> int:
    load_dotenv(ROOT / ".env")
    password = os.environ.get("SAP_PASSWORD")
    username = os.environ.get("SAP_USERNAME", "").upper()
    client = os.environ.get("SAP_CLIENT", "")
    if not password or username != EXPECTED["user"] or client != EXPECTED["client"]:
        raise SystemExit("Blocked: incomplete or unexpected RFC identity")

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

    evidence: dict[str, object] = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "RFC_READ_ONLY_PING_AND_METADATA",
        "expected_environment": EXPECTED,
        "write_bapi_called": False,
    }
    logged_on = bool(connection.Logon(0, True))
    evidence["logon"] = {
        "success": logged_on,
        "system": str(connection.SystemID).upper(),
        "client": str(connection.Client),
        "user": str(connection.User).upper(),
        "is_connected": bool(connection.IsConnected),
        "sap_release": str(connection.SAPRelease),
        "last_error": str(connection.LastError or ""),
    }
    actual = {key: evidence["logon"][key] for key in EXPECTED}
    if not logged_on or actual != EXPECTED:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(f"Blocked: RFC identity/logon mismatch {actual!r}")

    ping = functions.Add("RFC_PING")
    evidence["rfc_ping"] = {"success": bool(ping.Call)}

    bapi = functions.Add("BAPI_QUOTATION_CREATEFROMDATA2")
    metadata: dict[str, object] = {"function": "BAPI_QUOTATION_CREATEFROMDATA2"}
    for name in ("Exports", "Imports", "Tables", "Changing"):
        try:
            collection = getattr(bapi, name)
            metadata[name.lower()] = collection_names(collection)
        except Exception as error:
            metadata[name.lower()] = {"unavailable": f"{type(error).__name__}: {error}"}
    evidence["bapi_metadata"] = metadata
    connection.Logoff()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
