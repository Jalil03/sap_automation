"""Read the installed SAP RFC ActiveX type library; no SAP connection."""

from __future__ import annotations

import json
from pathlib import Path

import pythoncom

ROOT = Path(__file__).resolve().parents[1]
OCX = Path(r"C:\Program Files\SAP\FrontEnd\SapGui\wdtfuncs.ocx")
OUTPUT = ROOT / "runtime" / "sap_reads" / "sap_rfc_activex_typelib_2026-10-21.json"


def main() -> int:
    library = pythoncom.LoadTypeLib(str(OCX))
    types = []
    for type_index in range(library.GetTypeInfoCount()):
        info = library.GetTypeInfo(type_index)
        attr = info.GetTypeAttr()
        type_name = str(library.GetDocumentation(type_index)[0])
        functions = []
        for function_index in range(attr[6]):
            desc = info.GetFuncDesc(function_index)
            names = [str(value) for value in info.GetNames(desc[0])]
            functions.append({"memid": desc[0], "invkind": desc[4], "names": names})
        variables = []
        for variable_index in range(attr[7]):
            desc = info.GetVarDesc(variable_index)
            variables.append({"memid": desc[0], "names": [str(value) for value in info.GetNames(desc[0])]})
        if any(token in type_name.lower() for token in ("param", "field", "struct", "function", "table")):
            types.append({"name": type_name, "typekind": attr[5], "functions": functions, "variables": variables})
    result = {"mode": "LOCAL_TYPELIB_READ_ONLY", "source": str(OCX), "types": types}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
