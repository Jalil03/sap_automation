"""List matching SAP GUI sessions without selecting or modifying one."""

from __future__ import annotations

import json

import win32com.client


def children(parent):
    collection = parent.Children
    return [collection(index) for index in range(int(collection.Count))]


def main() -> int:
    sap_gui = win32com.client.GetObject("SAPGUI")
    engine = sap_gui.GetScriptingEngine
    result = []
    for connection_index, connection in enumerate(children(engine)):
        for session_index, session in enumerate(children(connection)):
            info = session.Info
            if str(info.SystemName).upper() != "A4H" or str(info.Client) != "600" or str(info.User).upper() != "ABDELJ":
                continue
            window = session.FindById("wnd[0]")
            result.append({
                "connection_index": connection_index,
                "session_index": session_index,
                "system": str(info.SystemName),
                "client": str(info.Client),
                "user": str(info.User),
                "transaction": str(info.Transaction),
                "program": str(info.Program),
                "screen_number": str(info.ScreenNumber),
                "window_title": str(window.Text),
                "busy": bool(session.Busy),
            })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
