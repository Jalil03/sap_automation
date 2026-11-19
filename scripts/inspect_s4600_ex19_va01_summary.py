"""Focused read-only summary of the current Exercise 19 VA01 draft."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode


P = "/app/con[0]/ses[0]/wnd[0]"
BODY = P + "/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400"
TABLE = BODY + "/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG"
WANTED = [
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR",
    P + "/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD",
    BODY + "/ssubHEADER_FRAME:SAPMV45A:4440/ctxtRV45A-KETDAT",
]
for row in (0, 1):
    WANTED.extend([
        TABLE + f"/txtVBAP-POSNR[0,{row}]",
        TABLE + f"/ctxtRV45A-MABNR[1,{row}]",
        TABLE + f"/txtRV45A-KWMENG[3,{row}]",
        TABLE + f"/ctxtVBAP-VRKME[4,{row}]",
        TABLE + f"/ctxtVBAP-PSTYV[8,{row}]",
        TABLE + f"/ctxtVBAP-WERKS[12,{row}]",
        TABLE + f"/txtVBAP-NETWR[20,{row}]",
    ])


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    prefix = str(session.raw.Id)
    wanted = [control_id.replace(P, prefix + "/wnd[0]", 1) for control_id in WANTED]
    snapshot = inspect_screen(session)
    fields = {item.get("id"): str(item.get("text") or "").strip() for item in snapshot.get("input_fields") or []}
    controls = [
        {"id": item.get("id"), "type": item.get("type"), "text": item.get("text"), "tooltip": item.get("tooltip")}
        for item in snapshot.get("controls") or []
        if any(word in str(item.get("text") or item.get("tooltip") or "").lower() for word in ("partenaire", "poste", "détail", "detail"))
    ]
    print(json.dumps({
        "identity": session.identity,
        "screen": {key: snapshot.get(key) for key in ("transaction", "program", "screen_number", "window_title")},
        "status_bar": snapshot.get("status_bar"),
        "popups": snapshot.get("popups", []),
        "fields": {key: fields.get(key) for key in wanted},
        "candidate_controls": controls[:100],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
