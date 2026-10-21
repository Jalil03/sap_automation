"""Narrow, non-persistent MM01 preparation for the P615-101 basic root.

Only the live-observed initial screen is supported. This module deliberately
has no SAVE operation; subsequent screens require their own observed contract.
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Any

from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.inspection import inspect_screen


PREFIX = "/app/con[0]/ses[0]/wnd[0]"
MATERIAL = PREFIX + "/usr/ctxtRMMG1-MATNR"
INDUSTRY = PREFIX + "/usr/cmbRMMG1-MBRSH"
MATERIAL_TYPE = PREFIX + "/usr/cmbRMMG1-MTART"
CHANGE_NUMBER = PREFIX + "/usr/ctxtRMMG1-AENNR"
REFERENCE = PREFIX + "/usr/ctxtRMMG1_REF-MATNR"
CONTINUE = PREFIX + "/tbar[0]/btn[0]"
VIEW_TABLE = PREFIX.replace("wnd[0]", "wnd[1]") + "/usr/tblSAPLMGMMTC_VIEW"
VIEW_CONTINUE = PREFIX.replace("wnd[0]", "wnd[1]") + "/tbar[0]/btn[0]"
TARGET = {"logical_product_id": "P615-101"}
VALUES = {"industry_sector": "M", "material_type": "FERT"}
VIEW_VALUES = {"views": ["BASIC_DATA_1", "BASIC_DATA_2"]}
BASIC1_VALUES = {"description": "S4615 Training Product 101", "base_unit": "PC", "division": "00"}
BASIC1_PREFIX = PREFIX + "/usr/tabsTABSPR1/tabpSP01/ssubTABFRA1:SAPLMGMM:2004/"
BASIC1_MATERIAL = BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/ctxtRMMG1-MATNR"
BASIC1_DESCRIPTION = BASIC1_PREFIX + "subSUB1:SAPLMGD1:1002/txtMAKT-MAKTX"
BASIC1_UNIT = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-MEINS"
BASIC1_DIVISION = BASIC1_PREFIX + "subSUB2:SAPLMGD1:2001/ctxtMARA-SPART"
ROOT_VALUES = {"description": "S4615 Training Product 101", "material_type": "FERT",
               "industry_sector": "M", "base_unit": "PC", "division": "00"}
APPROVAL_PATH = Path(__file__).resolve().parents[2] / "data/provisioning/s4615/P615-101.basic_root_approval.json"
CHECKPOINT_PATH = Path(__file__).resolve().parents[2] / "data/provisioning/s4615/P615-101.basic_root_checkpoint.json"


def _assert_identity(session: Any) -> None:
    if any(str(session.identity.get(key, "")) != expected for key, expected in (
        ("system", "A4H"), ("client", "600"), ("user", "ABDELJ")
    )):
        raise ActionBlockedError("MM01 P615-101 requires A4H/600/ABDELJ")


def prepare_initial_screen(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Enter only approved initial MM01 values, then inspect the next screen."""
    if target != TARGET or values != VALUES:
        raise ActionBlockedError("MM01 P615-101 initial target or values mismatch")
    _assert_identity(session)
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "MM01", "SAPLMGMM", "60"
    ) or snapshot.get("popups"):
        raise ActionBlockedError("MM01 initial screen context mismatch")

    def exact(control_id: str, control_type: str) -> Any:
        control = session.find(control_id)
        if str(getattr(control, "Id", "")) != control_id or str(getattr(control, "Type", "")) != control_type:
            raise ActionBlockedError(f"MM01 control mismatch: {control_id}")
        return control

    for control_id in (MATERIAL, CHANGE_NUMBER, REFERENCE):
        field = exact(control_id, "GuiCTextField")
        if str(getattr(field, "Text", "") or "").strip():
            raise ActionBlockedError(f"MM01 initial field is not blank: {control_id}")
    industry = exact(INDUSTRY, "GuiComboBox")
    material_type = exact(MATERIAL_TYPE, "GuiComboBox")
    button = exact(CONTINUE, "GuiButton")
    if str(getattr(button, "Text", "")) != "Suite":
        raise ActionBlockedError("MM01 exact Continue button text mismatch")

    industry.Key = "M"
    material_type.Key = "FERT"
    if str(getattr(industry, "Key", "")) != "M" or str(getattr(material_type, "Key", "")) != "FERT":
        raise ActionBlockedError("MM01 selected industry or material type not confirmed")
    session.audit("PHASE5_OPERATION", control_id=CONTINUE, value={"operation": "S4615_PRODUCT_P101_BASIC_ROOT", "stage": "initial"})
    button.press()
    return {"stage": "INITIAL_PREPARED", "saved": False, "screen": inspect_screen(session)}


def prepare_basic_views(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Select only the two observed Basic Data views; never select org/accounting views."""
    if target != TARGET or values != VIEW_VALUES:
        raise ActionBlockedError("MM01 P615-101 basic-view target or values mismatch")
    _assert_identity(session)
    snapshot = inspect_screen(session)
    popups = snapshot.get("popups") or []
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "MM01", "SAPLMGMM", "70"
    ) or len(popups) != 1 or popups[0].get("id") != PREFIX.replace("wnd[0]", "wnd[1]") or popups[0].get("window_title") != "Sélection des vues":
        raise ActionBlockedError("MM01 view-selection context mismatch")
    table = session.find(VIEW_TABLE)
    if str(getattr(table, "Id", "")) != VIEW_TABLE or str(getattr(table, "Type", "")) != "GuiTableControl":
        raise ActionBlockedError("MM01 view table mismatch")
    for row, label in ((0, "Données de base 1"), (1, "Données de base 2")):
        label_id = VIEW_TABLE + f"/txtMSICHTAUSW-DYTXT[0,{row}]"
        control = session.find(label_id)
        if str(getattr(control, "Id", "")) != label_id or str(getattr(control, "Type", "")) != "GuiTextField" or str(getattr(control, "Text", "")) != label:
            raise ActionBlockedError(f"MM01 basic-view label mismatch at row {row}")
    button = session.find(VIEW_CONTINUE)
    if (str(getattr(button, "Id", "")) != VIEW_CONTINUE
            or str(getattr(button, "Type", "")) != "GuiButton"
            or not str(getattr(button, "Tooltip", "")).startswith("Suite")):
        raise ActionBlockedError("MM01 view Continue button mismatch")
    view_tables = [item for item in popups[0].get("tables", []) if item.get("id") == VIEW_TABLE]
    if len(view_tables) != 1 or len(view_tables[0].get("visible_rows") or []) < 2:
        raise ActionBlockedError("MM01 basic views are not both visible")
    visible_count = len(view_tables[0]["visible_rows"])
    # This SAP table rejects GetAbsoluteRow for unloaded rows. No SAVE is
    # permitted at this stage; the next screen is inspected before continuing.
    if any(bool(getattr(table.GetAbsoluteRow(index), "Selected", False)) for index in range(visible_count)):
        raise ActionBlockedError("MM01 view selection already contains marked rows")
    table.GetAbsoluteRow(0).Selected = True
    table.GetAbsoluteRow(1).Selected = True
    if not (table.GetAbsoluteRow(0).Selected and table.GetAbsoluteRow(1).Selected):
        raise ActionBlockedError("MM01 basic views could not be confirmed selected")
    session.audit("PHASE5_OPERATION", control_id=VIEW_CONTINUE, value={"operation": "S4615_PRODUCT_P101_BASIC_ROOT", "stage": "basic views"})
    button.press()
    return {"stage": "BASIC_VIEWS_PREPARED", "saved": False, "screen": inspect_screen(session)}


def prepare_basic_data_1(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Stage only user-approved Basic Data 1 fields; no navigation or SAVE."""
    if target != TARGET or values != BASIC1_VALUES:
        raise ActionBlockedError("MM01 P615-101 Basic Data 1 target or values mismatch")
    _assert_identity(session)
    snapshot = inspect_screen(session)
    if (snapshot.get("transaction"), snapshot.get("program"), str(snapshot.get("screen_number"))) != (
        "MM01", "SAPLMGMM", "4004"
    ) or snapshot.get("popups"):
        raise ActionBlockedError("MM01 Basic Data 1 screen mismatch")
    title_match = re.fullmatch(r"Créer article ([0-9]+) \(Produit fini\)", str(snapshot.get("window_title") or ""))
    if title_match is None:
        raise ActionBlockedError("MM01 generated material title mismatch")
    inputs = {item.get("id"): item for item in snapshot.get("input_fields") or []}
    material = inputs.get(BASIC1_MATERIAL)
    if material is None or str(material.get("text") or "").strip() != title_match.group(1) or material.get("changeable") is not False:
        raise ActionBlockedError("MM01 generated material field mismatch")
    updates = ((BASIC1_DESCRIPTION, "GuiTextField", values["description"]),
               (BASIC1_UNIT, "GuiCTextField", values["base_unit"]),
               (BASIC1_DIVISION, "GuiCTextField", values["division"]))
    controls = []
    pending = []
    for control_id, control_type, value in updates:
        item = inputs.get(control_id)
        control = session.find(control_id)
        if (item is None or str(getattr(control, "Id", "")) != control_id
                or str(getattr(control, "Type", "")) != control_type):
            raise ActionBlockedError(f"MM01 Basic Data 1 field mismatch: {control_id}")
        current = str(item.get("text") or "").strip()
        if current and current != value:
            raise ActionBlockedError(f"MM01 Basic Data 1 unexpected value: {control_id}")
        if current == value:
            continue
        if item.get("changeable") is True:
            controls.append((control, value))
        elif control_id == BASIC1_DESCRIPTION:
            raise ActionBlockedError("MM01 mandatory description is not editable")
        else:
            pending.append(control_id)
    if not controls and pending:
        raise ActionBlockedError("MM01 Basic Data 1 has no currently editable approved field")
    for control, value in controls:
        control.Text = value
    if any(str(getattr(control, "Text", "")) != value for control, value in controls):
        raise ActionBlockedError("MM01 Basic Data 1 staged value mismatch")
    session.audit("PHASE5_OPERATION", value={"operation": "S4615_PRODUCT_P101_BASIC_ROOT", "stage": "basic data 1", "material_candidate": title_match.group(1)})
    return {"stage": "BASIC_DATA_1_PREPARED", "saved": False,
            "material_candidate": title_match.group(1), "pending_fields": pending,
            "screen": inspect_screen(session)}


def save_basic_root_once(session: Any, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """One controlled MM01 SAVE; independent API readback is required afterward."""
    if target != TARGET or values != ROOT_VALUES:
        raise ActionBlockedError("MM01 P615-101 root SAVE target or values mismatch")
    _assert_identity(session)
    from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy
    policy = TrainingExecutionPolicy.from_document(json.loads(APPROVAL_PATH.read_text(encoding="utf-8")))
    policy.authorize("S4615_PRODUCT_P101_BASIC_ROOT", target, values)
    checkpoint = ExecutionCheckpoint(CHECKPOINT_PATH, policy.workflow_id)
    if checkpoint.status("S4615_PRODUCT_P101_BASIC_ROOT") is not None:
        raise ActionBlockedError("Prior P615-101 root SAVE checkpoint requires reconciliation")

    before = inspect_screen(session)
    title_match = re.fullmatch(r"Créer article ([0-9]+) \(Produit fini\)", str(before.get("window_title") or ""))
    if ((before.get("transaction"), before.get("program"), str(before.get("screen_number")))
            != ("MM01", "SAPLMGMM", "4004") or before.get("popups") or title_match is None):
        raise ActionBlockedError("MM01 P615-101 root SAVE screen mismatch")
    material_id = title_match.group(1)
    basic2_fields = {item.get("id"): item for item in before.get("input_fields") or []}
    basic2_description = next((item for control_id, item in basic2_fields.items()
                               if control_id.endswith("/txtMAKT-MAKTX") and "/tabpSP02/" in control_id), None)
    if basic2_description is None or str(basic2_description.get("text") or "") != ROOT_VALUES["description"]:
        raise ActionBlockedError("MM01 Basic Data 2 description mismatch")
    if any(item.get("changeable") is True and item.get("type") in {"GuiTextField", "GuiCTextField", "GuiComboBox"}
           and str(item.get("text") or "").strip() and item is not basic2_description
           for item in basic2_fields.values()):
        raise ActionBlockedError("MM01 Basic Data 2 contains unapproved field values")
    tab_id = PREFIX + "/usr/tabsTABSPR1/tabpSP01"
    tab = session.find(tab_id)
    if str(getattr(tab, "Id", "")) != tab_id or str(getattr(tab, "Type", "")) != "GuiTab" or str(getattr(tab, "Text", "")) != " Données de base 1":
        raise ActionBlockedError("MM01 exact Basic Data 1 tab mismatch")
    tab.Select()
    basic1 = inspect_screen(session)
    if (basic1.get("transaction"), basic1.get("program"), str(basic1.get("screen_number"))) != ("MM01", "SAPLMGMM", "4004") or basic1.get("popups"):
        raise ActionBlockedError("MM01 Basic Data 1 pre-save context mismatch")
    fields = {item.get("id"): item for item in basic1.get("input_fields") or []}
    expected = {BASIC1_MATERIAL: material_id, BASIC1_DESCRIPTION: ROOT_VALUES["description"],
                BASIC1_UNIT: ROOT_VALUES["base_unit"], BASIC1_DIVISION: ROOT_VALUES["division"]}
    if any(str((fields.get(control_id) or {}).get("text") or "").strip() != value for control_id, value in expected.items()):
        raise ActionBlockedError("MM01 Basic Data 1 pre-save values mismatch")
    if fields[BASIC1_MATERIAL].get("changeable") is not False:
        raise ActionBlockedError("MM01 generated material number is unexpectedly editable")
    if any(item.get("changeable") is True and item.get("type") in {"GuiTextField", "GuiCTextField", "GuiComboBox"}
           and str(item.get("text") or "").strip() and item.get("id") not in expected
           for item in fields.values()):
        raise ActionBlockedError("MM01 Basic Data 1 contains unapproved field values")
    save_id = PREFIX + "/tbar[0]/btn[11]"
    save = session.find(save_id)
    if (str(getattr(save, "Id", "")) != save_id
            or str(getattr(save, "Type", "")) != "GuiButton"
            or str(getattr(save, "Text", "")) != "Sauvegarder"):
        raise ActionBlockedError("MM01 exact SAVE button mismatch")
    checkpoint.before_write("S4615_PRODUCT_P101_BASIC_ROOT")
    session.audit("PHASE5_OPERATION", control_id=save_id, value={"operation": "S4615_PRODUCT_P101_BASIC_ROOT", "material_candidate": material_id, "step": "save_once"})
    save.press()
    after = inspect_screen(session)
    checkpoint.record("S4615_PRODUCT_P101_BASIC_ROOT", "AMBIGUOUS", detail="SAVE sent; independent A_Product readback required")
    return {"material_candidate": material_id, "saved_attempted": True, "verified": False,
            "screen": after}
