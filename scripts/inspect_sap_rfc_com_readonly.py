"""Inspect locally installed SAP RFC COM controls; performs no SAP call."""

from __future__ import annotations

import json

import pythoncom
import win32com.client


def type_members(value) -> list[str]:
    info = value._oleobj_.GetTypeInfo()
    attr = info.GetTypeAttr()
    names: set[str] = set()
    for index in range(attr[6]):  # cFuncs
        desc = info.GetFuncDesc(index)
        names.update(str(item) for item in info.GetNames(desc[0]) if item)
    for index in range(attr[7]):  # cVars
        desc = info.GetVarDesc(index)
        names.update(str(item) for item in info.GetNames(desc[0]) if item)
    return sorted(names)


def main() -> int:
    pythoncom.CoInitialize()
    result: dict[str, object] = {"mode": "LOCAL_COM_INSPECTION_NO_SAP_CALL"}
    for progid in ("SAP.Functions.Unicode", "SAP.LogonControl.Unicode.1", "SAP.NWRFC.Unicode.1"):
        try:
            obj = win32com.client.Dispatch(progid)
            result[progid] = {"available": True, "members": type_members(obj)}
            if progid == "SAP.Functions.Unicode":
                connection = obj.Connection
                result[progid]["connection_members"] = type_members(connection)
        except Exception as error:
            result[progid] = {"available": False, "error": f"{type(error).__name__}: {error}"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
