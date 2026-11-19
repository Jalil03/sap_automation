"""Narrow SAP GUI READ audit for S4600 order types and recent ABAP dumps."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import (
    back,
    display_s4615_sales_reference,
    find_s4615_sales_type,
    open_transaction,
)
from src.sap_gui_bridge.safety import SafetyMode


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_gui_audit_2026-10-21.json"


def field_map(snapshot: dict) -> dict[str, str]:
    return {
        item["id"]: str(item.get("text") or "").strip()
        for item in snapshot.get("input_fields", [])
    }


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    if session.identity != {
        "system": "A4H", "client": "600", "user": "ABDELJ", "transaction": session.identity["transaction"]
    }:
        raise RuntimeError(f"Unexpected SAP identity: {session.identity}")

    open_transaction(session, "ST22")
    st22_initial = inspect_screen(session)
    st22_fields = field_map(st22_initial)
    today_button_id = "/app/con[0]/ses[0]/wnd[0]/usr/btnTODAY"
    today_button = session.find(today_button_id)
    session.audit(
        "PRESS_SAFE_BUTTON",
        control_id=today_button_id,
        control_text=str(getattr(today_button, "Text", "")),
        value="read today's dump overview",
    )
    today_button.press()
    session.validate_identity()
    st22_today = inspect_screen(session)

    open_transaction(session, "ST22")
    yesterday_button_id = "/app/con[0]/ses[0]/wnd[0]/usr/btnYESTERD"
    yesterday_button = session.find(yesterday_button_id)
    session.audit(
        "PRESS_SAFE_BUTTON",
        control_id=yesterday_button_id,
        control_text=str(getattr(yesterday_button, "Text", "")),
        value="read yesterday's dump overview",
    )
    yesterday_button.press()
    session.validate_identity()
    st22_yesterday = inspect_screen(session)

    open_transaction(session, "VOV8")
    vov8_initial = inspect_screen(session)
    search = find_s4615_sales_type(session, {
        "transaction": "VOV8",
        "program": "SAPL080O",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK",
        "sales_order_type": "ZA01",
    })
    cs_detail = display_s4615_sales_reference(session, {
        "transaction": "VOV8",
        "program": "SAPL080O",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK",
        "sales_order_type": "CS",
        "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]",
    })
    back(session)
    cdcl = display_s4615_sales_reference(session, {
        "transaction": "VOV8",
        "program": "SAPL080O",
        "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK",
        "sales_order_type": "CDCL",
        "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]",
    })

    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "STRICT_READ_ONLY_SAP_GUI",
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "st22": {
            "selection_date": st22_fields.get("/app/con[0]/ses[0]/wnd[0]/usr/ctxtS_DATUM-LOW"),
            "today_count_text": st22_fields.get("/app/con[0]/ses[0]/wnd[0]/usr/txtTOD_NUM"),
            "yesterday_count_text": st22_fields.get("/app/con[0]/ses[0]/wnd[0]/usr/txtYED_NUM"),
            "today_overview": st22_today,
            "yesterday_overview": st22_yesterday,
        },
        "vov8": {
            "initial": {
                "transaction": vov8_initial.get("transaction"),
                "program": vov8_initial.get("program"),
                "screen_number": vov8_initial.get("screen_number"),
                "window_title": vov8_initial.get("window_title"),
            },
            "full_scan": search,
            "cs_detail": cs_detail,
            "cdcl_scan": cdcl,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "output": str(OUTPUT.relative_to(ROOT)),
        "environment": evidence["environment"],
        "st22": {
            "selection_date": evidence["st22"]["selection_date"],
            "today_count_text": evidence["st22"]["today_count_text"],
            "yesterday_count_text": evidence["st22"]["yesterday_count_text"],
            "overview_tables": st22_today.get("tables", []),
            "yesterday_overview_tables": st22_yesterday.get("tables", []),
        },
        "sales_type_search": search.get("sales_type_search"),
        "cs_fields": field_map(cs_detail.get("snapshot", {})),
        "cdcl": cdcl,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
