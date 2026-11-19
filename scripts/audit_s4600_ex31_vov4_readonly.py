"""Read-only VOV4 verification for S4600 exercise 31 (CS + LEIS)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.navigation import open_transaction
from src.sap_gui_bridge.safety import SafetyMode
from src.provisioning.sap_gui_backend import (
    _vov4_context,
    _vov4_contract,
    _vov4_read_visible_row,
    _wait_not_busy,
)

OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex31_vov4_cs_leis_2026-10-21.json"
def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.READ).attach()
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    actual = {key: str(session.identity.get(key, "")).upper() for key in expected}
    if actual != expected:
        raise SystemExit(f"Blocked: unexpected SAP identity {actual!r}")

    open_transaction(session, "VOV4")
    contract = _vov4_contract("S4615_BV_CB04")
    _vov4_context(session, contract, screen=contract["overview_screen"])
    table = session.find(contract["table_id"])
    row_count = int(table.RowCount)
    position_button = "/app/con[0]/ses[0]/wnd[0]/usr/btnVIM_POSI_PUSH"
    document_field = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLSPO4:0300/ctxtSVALD-VALUE[0,21]"
    group_field = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLSPO4:0300/ctxtSVALD-VALUE[1,21]"
    continue_button = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
    session.audit("NAVIGATE", control_id=position_button, value="open VOV4 position dialog")
    session.find(position_button).press()
    session.audit("NAVIGATE", control_id=document_field, value="CS")
    session.find(document_field).Text = "CS"
    session.audit("NAVIGATE", control_id=group_field, value="LEIS")
    session.find(group_field).Text = "LEIS"
    session.audit("NAVIGATE", control_id=continue_button, value="position only; no save")
    session.find(continue_button).press()
    _wait_not_busy(session)
    position = int(session.find(contract["table_id"]).VerticalScrollbar.Position)
    values = _vov4_read_visible_row(session, contract, 0)
    matches = [{"row_index": position, "values": values}] if (
        values["sales_document_type"] == "CS" and values["item_category_group"] == "LEIS"
    ) else []

    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": expected,
        "mode": "STRICT_READ_ONLY_SAP_GUI",
        "transaction": "VOV4",
        "program": "SAPL080O",
        "screen_number": contract["overview_screen"],
        "target": {"sales_document_type": "CS", "item_category_group": "LEIS"},
        "row_count": row_count,
        "positioned_row": position,
        "matches": matches,
        "classification": "EXISTS" if matches else "UNKNOWN",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
