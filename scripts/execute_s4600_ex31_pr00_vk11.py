"""Save exactly one approved S4600 exercise 31 PR00 condition in VK11."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.safety import SafetyMode

TABLE = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY"
OUTPUT = ROOT / "runtime" / "sap_writes" / "s4600_ex31_pr00_vk11_result.json"
APPROVAL = ROOT / "data" / "provisioning" / "s4600" / "S4600_CH8_EX31.pr00_group00.workflow_approval.json"
LOOKUP = ROOT / "runtime" / "sap_reads" / "s4600_pr00_vk13_audit_2026-10-21.json"
OPERATION = "CREATE_ONE_S4600_EX31_PR00_CUSTOMER_MATERIAL_PLANT_VK11"
PAYLOAD = {
    "condition_type": "PR00",
    "key_combination": "CUSTOMER_MATERIAL_PLANT",
    "customer": "1000000112",
    "material": "90000133",
    "plant": "FR10",
    "rate": "150.00",
    "currency": "EUR",
    "pricing_unit": "1",
    "quantity_unit": "H",
    "valid_from": "2026-10-22",
    "valid_to": "2026-12-31",
}


def fingerprint() -> str:
    raw = json.dumps(PAYLOAD, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def text(session, control_id: str) -> str:
    return str(getattr(session.find(control_id), "Text", "") or "").strip()


def validate_screen(session) -> dict:
    expected = {"system": "A4H", "client": "600", "user": "ABDELJ"}
    actual = {key: str(session.identity.get(key, "")).upper() for key in expected}
    if actual != expected or session.identity.get("transaction") != "VK11":
        raise SystemExit(f"Blocked: unexpected SAP context {session.identity!r}")
    info = session.raw.Info
    if str(info.Program).upper() != "SAPMV13A" or str(info.ScreenNumber).lstrip("0") != "1972":
        raise SystemExit("Blocked: VK11 quick-entry contract changed")
    observed = {
        "customer": text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-KUNNR"),
        "material": text(session, "/app/con[0]/ses[0]/wnd[0]/usr/ctxtKOMG-MATNR"),
        "plant": text(session, f"{TABLE}/ctxtKOMG-WERKS[0,0]"),
        "rate": text(session, f"{TABLE}/txtKONP-KBETR[4,0]").replace(" ", "").replace(",", "."),
        "currency": text(session, f"{TABLE}/ctxtKONP-KONWA[5,0]"),
        "pricing_unit": text(session, f"{TABLE}/txtKONP-KPEIN[6,0]"),
        "quantity_unit": text(session, f"{TABLE}/ctxtKONP-KMEIN[7,0]"),
        "valid_from": text(session, f"{TABLE}/ctxtRV13A-DATAB[10,0]"),
        "valid_to": text(session, f"{TABLE}/ctxtRV13A-DATBI[11,0]"),
    }
    expected_screen = {
        "customer": "1000000112", "material": "90000133", "plant": "FR10",
        "rate": "150.00", "currency": "EUR", "pricing_unit": "1", "quantity_unit": "H",
        "valid_from": "22.10.2026", "valid_to": "31.12.2026",
    }
    if observed != expected_screen:
        raise SystemExit(f"Blocked: staged VK11 values changed: {observed!r}")
    return {"environment": actual, "observed": observed}


def validate_lookup() -> dict:
    data = json.loads(LOOKUP.read_text(encoding="utf-8"))
    if not str(data.get("captured_at_utc", "")).startswith("2026-10-22"):
        raise SystemExit("Blocked: PR00 lookup is not from 2026-10-22")
    statuses = {
        "customer_material_plant": data["lookups"]["service_product"]["result_screen"]["status_bar"]["text"],
        "material": data["article_lookups"]["service_product"]["result_screen"]["status_bar"]["text"],
    }
    if not all("aucun enreg" in str(value).lower() for value in statuses.values()):
        raise SystemExit(f"Blocked: duplicate lookup is not deterministically empty: {statuses!r}")
    return {"captured_at_utc": data["captured_at_utc"], "statuses": statuses}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    session = SapGuiConnection(mode=SafetyMode.EXECUTE if args.execute else SafetyMode.PREPARE).attach()
    screen = validate_screen(session)
    lookup = validate_lookup()
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": screen["environment"],
        "operation": OPERATION,
        "payload": PAYLOAD,
        "payload_sha256": fingerprint(),
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "duplicate_lookup": lookup,
        "staged_values": screen["observed"],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if not args.execute:
        result["status"] = "DRY_RUN_OK"
        OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
    if approval.get("status") != "APPROVED" or approval.get("operation_scope") != OPERATION:
        raise SystemExit("Blocked: approval status or scope mismatch")
    if approval.get("payload_sha256") != fingerprint():
        raise SystemExit("Blocked: approval payload fingerprint mismatch")
    if approval.get("environment") != screen["environment"]:
        raise SystemExit("Blocked: approval environment mismatch")
    result.update(status="ATTEMPT_RECORDED", approval_id=approval.get("approval_id"), save_attempts=0)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save_id = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
    session.audit(
        "PHASE5_OPERATION",
        control_id=save_id,
        value={"operation": OPERATION, "payload_sha256": fingerprint(), "step": "save_once"},
    )
    session.find(save_id).press()
    result["save_attempts"] = 1
    session.validate_identity()
    snapshot = inspect_screen(session)
    result["post_save"] = {
        "transaction": snapshot.get("transaction"),
        "program": snapshot.get("program"),
        "screen_number": snapshot.get("screen_number"),
        "status_bar": snapshot.get("status_bar"),
        "popups": snapshot.get("popups"),
    }
    message_type = str((snapshot.get("status_bar") or {}).get("message_type") or "")
    if snapshot.get("popups") or message_type in {"E", "A"}:
        result["status"] = "AMBIGUOUS_OR_FAILED_NO_RETRY"
    else:
        result["status"] = "SAVED_PENDING_INDEPENDENT_READBACK"
    result["checkpointed_at_utc"] = datetime.now(timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "SAVED_PENDING_INDEPENDENT_READBACK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
