"""Inspect exact COM structure/table contracts for quotation BAPI; never calls it."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex28_bapi_quotation_structures_2026-10-21.json"
OCX = Path(r"C:\Program Files\SAP\FrontEnd\SapGui\wdtfuncs.ocx")


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
    except Exception as error:
        return [f"UNAVAILABLE:{type(error).__name__}:{error}"]


def signatures(value, wanted: set[str]) -> list[dict]:
    info = value._oleobj_.GetTypeInfo()
    attr = info.GetTypeAttr()
    result = []
    for index in range(attr[6]):
        desc = info.GetFuncDesc(index)
        names = [str(item) for item in info.GetNames(desc[0])]
        if names and names[0] in wanted:
            result.append({"memid": desc[0], "invkind": desc[4], "names": names, "raw": repr(desc)})
    return result


def item(collection, key):
    for accessor in (lambda: collection.Item(key), lambda: collection(key)):
        try:
            value = accessor()
            if value is not None:
                return value
        except Exception:
            continue
    raise RuntimeError(f"Cannot resolve COM collection key {key!r}")


def safe_attr(value, name):
    try:
        result = getattr(value, name)
        if callable(result):
            return "<method>"
        if isinstance(result, (str, int, float, bool)) or result is None:
            return result
        return f"<{type(result).__name__}>"
    except Exception as error:
        return f"UNAVAILABLE:{type(error).__name__}:{error}"


def describe(value) -> dict:
    names = members(value)
    return {
        "members": names,
        "selected_properties": {
            name: safe_attr(value, name)
            for name in ("Name", "Count", "ColumnCount", "RowCount", "Value", "Rows", "Columns")
            if name in names
        },
    }


def column_names(table) -> list[str]:
    return [str(table.ColumnName(index)) for index in range(1, int(table.ColumnCount) + 1)]


def ole_maps(value) -> dict:
    representation = getattr(value, "_olerepr_", None)
    return {
        "dir": sorted(name for name in dir(value) if not name.startswith("_")),
        "prop_get": sorted(str(name) for name in getattr(representation, "propMap", {}).keys()),
        "prop_put": sorted(str(name) for name in getattr(representation, "propMapPut", {}).keys()),
        "functions": sorted(str(name) for name in getattr(representation, "mapFuncs", {}).keys()),
        "default_dispatch": str(getattr(representation, "defaultDispatchName", "")),
    }


def structure_value(parameter):
    library = pythoncom.LoadTypeLib(str(OCX))
    iid = None
    for index in range(library.GetTypeInfoCount()):
        if str(library.GetDocumentation(index)[0]) == "IStructure":
            iid = library.GetTypeInfo(index).GetTypeAttr()[0]
            break
    if iid is None:
        raise RuntimeError("IStructure IID not found")
    return parameter._oleobj_.QueryInterface(iid, pythoncom.IID_IDispatch)


def raw_structure_columns(raw) -> list[str]:
    count = int(raw.InvokeTypes(3, 0, pythoncom.DISPATCH_PROPERTYGET, (pythoncom.VT_I4, 0), ()))
    return [
        str(raw.InvokeTypes(
            10,
            0,
            pythoncom.DISPATCH_PROPERTYGET,
            (pythoncom.VT_BSTR, 0),
            ((pythoncom.VT_VARIANT, 0),),
            index,
        ))
        for index in range(1, count + 1)
    ]


def main() -> int:
    load_dotenv(ROOT / ".env")
    pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode")
    connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]
    connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]
    connection.SystemID = "A4H"
    connection.Client = os.environ["SAP_CLIENT"]
    connection.User = os.environ["SAP_USERNAME"]
    connection.Password = os.environ["SAP_PASSWORD"]
    connection.Language = "FR"
    if not bool(connection.Logon(0, True)):
        raise SystemExit("Blocked: RFC logon failed")

    bapi = functions.Add("BAPI_QUOTATION_CREATEFROMDATA2")
    result: dict[str, object] = {
        "mode": "RFC_METADATA_ONLY_NO_BAPI_CALL",
        "environment": {"system": str(connection.SystemID), "client": str(connection.Client), "user": str(connection.User)},
        "bapi_called": False,
        "exports": {},
        "tables": {},
    }
    for name in ("QUOTATION_HEADER_IN", "QUOTATION_HEADER_INX", "LOGIC_SWITCH", "TESTRUN"):
        parameter = item(bapi.Exports, name)
        details = {
            "parameter": describe(parameter),
            "known_properties": {
                key: safe_attr(parameter, key)
                for key in ("Name", "Type", "SAPType", "Length", "Description", "Value", "IsStructure")
            },
        }
        is_structure = bool(getattr(parameter, "IsStructure", False))
        details["is_structure"] = is_structure
        if is_structure:
            try:
                structure = structure_value(parameter)
                details["structure"] = {
                    "columns": raw_structure_columns(structure),
                }
            except Exception as error:
                details["structure_error"] = f"{type(error).__name__}: {error}"
        try:
            details["value"] = describe(parameter.Value)
        except Exception as error:
            details["value_error"] = f"{type(error).__name__}: {error}"
        details["ole_maps"] = ole_maps(parameter)
        result["exports"][name] = details
    for name in ("QUOTATION_ITEMS_IN", "QUOTATION_ITEMS_INX", "QUOTATION_PARTNERS", "QUOTATION_SCHEDULES_IN", "QUOTATION_SCHEDULES_INX", "RETURN"):
        table = item(bapi.Tables, name)
        result["tables"][name] = {
            **describe(table),
            "columns": column_names(table),
            "signatures": signatures(table, {"AppendRow", "Cell", "Value", "RowCount", "ColumnName"}),
        }
    connection.Logoff()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
