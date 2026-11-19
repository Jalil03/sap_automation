"""Display-only VK13 inspection for PR00 and product 90000133."""

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
from src.sap_gui_bridge.navigation import open_transaction, set_text
from src.sap_gui_bridge.safety import SafetyMode


OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_pr00_vk13_audit_2026-10-21.json"


def enter(session) -> None:
    window_id = "/app/con[0]/ses[0]/wnd[0]"
    session.audit("NAVIGATE", control_id=window_id, value="sendVKey(0) read-only continue")
    session.find(window_id).sendVKey(0)
    session.validate_identity()


def lookup_customer_material(session, customer: str, product: str) -> dict:
    open_transaction(session, "VK13")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRV13A-KSCHL", "PR00")
    enter(session)
    key_combination = inspect_screen(session)
    radio_id = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[0,0]"
    radio = session.find(radio_id)
    session.audit("NAVIGATE", control_id=radio_id, value="select first installed PR00 key combination")
    radio.select()
    choose_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
    choose = session.find(choose_id)
    session.audit("NAVIGATE", control_id=choose_id, value="open display selection for PR00")
    choose.press()
    session.validate_identity()
    selection = inspect_screen(session)
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF001", customer)
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF002", product)
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF003-LOW", "FR10")
    window_id = "/app/con[0]/ses[0]/wnd[0]"
    session.audit(
        "NAVIGATE", control_id=window_id,
        value={"operation": "sendVKey(8) display condition records", "customer": customer, "product": product, "division": "FR10"},
    )
    session.find(window_id).sendVKey(8)
    session.validate_identity()
    result = inspect_screen(session)
    return {
        "customer": customer,
        "product": product,
        "division": "FR10",
        "key_combination_screen": key_combination,
        "selection_screen": selection,
        "result_screen": result,
    }


def lookup_article(session, product: str) -> dict:
    open_transaction(session, "VK13")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtRV13A-KSCHL", "PR00")
    enter(session)
    radio_id = "/app/con[0]/ses[0]/wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[3,0]"
    radio = session.find(radio_id)
    session.audit("NAVIGATE", control_id=radio_id, value="select installed PR00 article key combination")
    radio.select()
    choose_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
    session.audit("NAVIGATE", control_id=choose_id, value="open article display selection for PR00")
    session.find(choose_id).press()
    session.validate_identity()
    selection = inspect_screen(session)
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF001", "FR10")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF002", "10")
    set_text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtF003-LOW", product)
    window_id = "/app/con[0]/ses[0]/wnd[0]"
    session.audit(
        "NAVIGATE", control_id=window_id,
        value={
            "operation": "sendVKey(8) display article condition records",
            "sales_organization": "FR10",
            "distribution_channel": "10",
            "product": product,
        },
    )
    session.find(window_id).sendVKey(8)
    session.validate_identity()
    return {
        "sales_organization": "FR10",
        "distribution_channel": "10",
        "product": product,
        "selection_screen": selection,
        "result_screen": inspect_screen(session),
    }


def main() -> int:
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    known_product = lookup_customer_material(session, "1000000112", "10000282")
    service_product = lookup_customer_material(session, "1000000112", "90000133")
    known_article = lookup_article(session, "10000282")
    service_article = lookup_article(session, "90000133")
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"system": "A4H", "client": "600", "user": "ABDELJ"},
        "mode": "DISPLAY_ONLY_PREPARE_NO_SAVE",
        "condition_type": "PR00",
        "lookups": {
            "known_priced_product": known_product,
            "service_product": service_product,
        },
        "article_lookups": {
            "known_priced_product": known_article,
            "service_product": service_article,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "known_priced_product_result": known_product["result_screen"],
        "service_product_result": service_product["result_screen"],
        "known_article_result": known_article["result_screen"],
        "service_article_result": service_article["result_screen"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
