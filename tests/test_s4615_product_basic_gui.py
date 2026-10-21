import unittest
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.provisioning.s4615_product_basic_gui import (
    BASIC1_DESCRIPTION, BASIC1_DIVISION, BASIC1_MATERIAL, BASIC1_UNIT, BASIC1_VALUES,
    ROOT_VALUES, APPROVAL_PATH,
    CHANGE_NUMBER, CONTINUE, INDUSTRY, MATERIAL, MATERIAL_TYPE,
    REFERENCE, TARGET, VALUES, VIEW_CONTINUE, VIEW_TABLE, VIEW_VALUES,
    prepare_basic_data_1, prepare_basic_views, prepare_initial_screen, save_basic_root_once,
)
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.navigation import _is_mm01_basic_tab_exception
from src.sap_gui_bridge.protocol import ProtocolError, validate_request


class Control:
    def __init__(self, control_id, control_type, text="", key=""):
        self.Id, self.Type, self.Text, self.Key = control_id, control_type, text, key
        self.pressed = False

    def press(self):
        self.pressed = True

    def Select(self):
        self.pressed = True


class Table(Control):
    def __init__(self):
        super().__init__(VIEW_TABLE, "GuiTableControl")
        self.RowCount = 50
        self.rows = [SimpleNamespace(Selected=False) for _ in range(3)]

    def GetAbsoluteRow(self, index):
        return self.rows[index]


class Session:
    def __init__(self):
        self.identity = {"system": "A4H", "client": "600", "user": "ABDELJ"}
        self.controls = {
            MATERIAL: Control(MATERIAL, "GuiCTextField"),
            CHANGE_NUMBER: Control(CHANGE_NUMBER, "GuiCTextField"),
            REFERENCE: Control(REFERENCE, "GuiCTextField"),
            INDUSTRY: Control(INDUSTRY, "GuiComboBox"),
            MATERIAL_TYPE: Control(MATERIAL_TYPE, "GuiComboBox"),
            CONTINUE: Control(CONTINUE, "GuiButton", "Suite"),
            VIEW_TABLE: Table(),
            VIEW_TABLE + "/txtMSICHTAUSW-DYTXT[0,0]": Control(VIEW_TABLE + "/txtMSICHTAUSW-DYTXT[0,0]", "GuiTextField", "Données de base 1"),
            VIEW_TABLE + "/txtMSICHTAUSW-DYTXT[0,1]": Control(VIEW_TABLE + "/txtMSICHTAUSW-DYTXT[0,1]", "GuiTextField", "Données de base 2"),
            VIEW_CONTINUE: Control(VIEW_CONTINUE, "GuiButton"),
            BASIC1_MATERIAL: Control(BASIC1_MATERIAL, "GuiCTextField", "10000289"),
            BASIC1_DESCRIPTION: Control(BASIC1_DESCRIPTION, "GuiTextField"),
            BASIC1_UNIT: Control(BASIC1_UNIT, "GuiCTextField"),
            BASIC1_DIVISION: Control(BASIC1_DIVISION, "GuiCTextField"),
            "/app/con[0]/ses[0]/wnd[0]/usr/tabsTABSPR1/tabpSP01": Control("/app/con[0]/ses[0]/wnd[0]/usr/tabsTABSPR1/tabpSP01", "GuiTab", " Données de base 1"),
            "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]": Control("/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]", "GuiButton", "Sauvegarder"),
        }
        self.controls[VIEW_CONTINUE].Tooltip = "Suite   (Entrée)"
        self.audits = []

    def find(self, control_id):
        return self.controls[control_id]

    def audit(self, *args, **kwargs):
        self.audits.append((args, kwargs))


INITIAL = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "60", "popups": []}
NEXT = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "7", "popups": []}
VIEWS = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "70",
         "popups": [{"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Sélection des vues",
                     "tables": [{"id": VIEW_TABLE, "visible_rows": [{"index": 0}, {"index": 1}, {"index": 2}]}]}]}
BASIC1 = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "4004",
          "window_title": "Créer article 10000289 (Produit fini)", "popups": [],
          "input_fields": [{"id": BASIC1_MATERIAL, "text": "10000289", "changeable": False},
                           {"id": BASIC1_DESCRIPTION, "text": "", "changeable": True},
                           {"id": BASIC1_UNIT, "text": "", "changeable": True},
                           {"id": BASIC1_DIVISION, "text": "", "changeable": True}]}
BASIC1_READY = {**BASIC1, "input_fields": [
    {**item, "text": ({BASIC1_MATERIAL: "10000289", BASIC1_DESCRIPTION: ROOT_VALUES["description"],
                      BASIC1_UNIT: "PC", BASIC1_DIVISION: "00"})[item["id"]],
     "type": "GuiCTextField" if item["id"] != BASIC1_DESCRIPTION else "GuiTextField"}
    for item in BASIC1["input_fields"]]}
BASIC2_READY = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "4004",
                "window_title": "Créer article 10000289 (Produit fini)", "popups": [],
                "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[0]/usr/tabsTABSPR1/tabpSP02/txtMAKT-MAKTX",
                                  "text": ROOT_VALUES["description"], "type": "GuiTextField", "changeable": True}]}


class Mm01BasicRootTests(unittest.TestCase):
    def test_initial_screen_only_sets_approved_values_and_does_not_save(self):
        session = Session()
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[INITIAL, NEXT]):
            result = prepare_initial_screen(session, TARGET, VALUES)
        self.assertEqual("M", session.controls[INDUSTRY].Key)
        self.assertEqual("FERT", session.controls[MATERIAL_TYPE].Key)
        self.assertEqual("", session.controls[MATERIAL].Text)
        self.assertTrue(session.controls[CONTINUE].pressed)
        self.assertFalse(result["saved"])

    def test_wrong_target_or_values_block_before_gui_action(self):
        session = Session()
        for target, values in (({"logical_product_id": "P615-102"}, VALUES), (TARGET, {"industry_sector": "M", "material_type": "HALB"})):
            with self.assertRaises(ActionBlockedError):
                prepare_initial_screen(session, target, values)
        self.assertFalse(session.controls[CONTINUE].pressed)

    def test_existing_material_or_reference_blocks(self):
        for field in (MATERIAL, CHANGE_NUMBER, REFERENCE):
            session = Session()
            session.controls[field].Text = "something"
            with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value=INITIAL):
                with self.assertRaises(ActionBlockedError):
                    prepare_initial_screen(session, TARGET, VALUES)
            self.assertFalse(session.controls[CONTINUE].pressed)

    def test_unexpected_screen_or_button_blocks(self):
        session = Session()
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value={**INITIAL, "screen_number": "61"}):
            with self.assertRaises(ActionBlockedError):
                prepare_initial_screen(session, TARGET, VALUES)
        session.controls[CONTINUE].Text = "Sauvegarder"
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value=INITIAL):
            with self.assertRaises(ActionBlockedError):
                prepare_initial_screen(session, TARGET, VALUES)

    def test_wrong_sap_identity_blocks(self):
        session = Session()
        session.identity["client"] = "100"
        with self.assertRaises(ActionBlockedError):
            prepare_initial_screen(session, TARGET, VALUES)
        self.assertFalse(session.controls[CONTINUE].pressed)

    def test_protocol_limits_stage_to_exact_operation(self):
        import uuid
        request = {"request_id": str(uuid.uuid4()), "mode": "EXECUTE", "action": "PHASE5_OPERATION",
                   "params": {"operation": "S4615_PRODUCT_P101_BASIC_ROOT", "phase": "MM01_INITIAL_PREPARE", "target": TARGET, "values": VALUES}}
        validate_request(request)
        request["params"]["operation"] = "PRODUCT_P615_400"
        with self.assertRaises(ProtocolError):
            validate_request(request)

    def test_selects_only_basic_data_views_without_save(self):
        session = Session()
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[VIEWS, NEXT]):
            result = prepare_basic_views(session, TARGET, VIEW_VALUES)
        self.assertTrue(session.controls[VIEW_TABLE].rows[0].Selected)
        self.assertTrue(session.controls[VIEW_TABLE].rows[1].Selected)
        self.assertFalse(session.controls[VIEW_TABLE].rows[2].Selected)
        self.assertTrue(session.controls[VIEW_CONTINUE].pressed)
        self.assertFalse(result["saved"])

    def test_preselected_or_wrong_view_blocks(self):
        session = Session()
        session.controls[VIEW_TABLE].rows[2].Selected = True
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value=VIEWS):
            with self.assertRaises(ActionBlockedError):
                prepare_basic_views(session, TARGET, VIEW_VALUES)
        self.assertFalse(session.controls[VIEW_CONTINUE].pressed)
        session.controls[VIEW_TABLE].rows[2].Selected = False
        session.controls[VIEW_TABLE + "/txtMSICHTAUSW-DYTXT[0,1]"].Text = "Comptabilité 1"
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value=VIEWS):
            with self.assertRaises(ActionBlockedError):
                prepare_basic_views(session, TARGET, VIEW_VALUES)
        self.assertFalse(session.controls[VIEW_CONTINUE].pressed)

    def test_mm01_tab_exception_is_exact_and_read_only(self):
        screen = {"transaction": "MM01", "program": "SAPLMGMM", "screen_number": "4004", "popups": []}
        tab = "/app/con[0]/ses[0]/wnd[0]/usr/tabsTABSPR1/tabpSP02"
        self.assertTrue(_is_mm01_basic_tab_exception("SELECT_TAB", tab, " Données de base 2", screen))
        self.assertFalse(_is_mm01_basic_tab_exception("PRESS_SAFE_BUTTON", tab, " Données de base 2", screen))
        self.assertFalse(_is_mm01_basic_tab_exception("SELECT_TAB", tab, "Comptabilité 1", screen))
        self.assertFalse(_is_mm01_basic_tab_exception("SELECT_TAB", tab, " Données de base 2", {**screen, "screen_number": "4005"}))

    def test_basic_data_1_sets_only_approved_fields_without_save(self):
        session = Session()
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[BASIC1, BASIC1]):
            result = prepare_basic_data_1(session, TARGET, BASIC1_VALUES)
        self.assertEqual("S4615 Training Product 101", session.controls[BASIC1_DESCRIPTION].Text)
        self.assertEqual("PC", session.controls[BASIC1_UNIT].Text)
        self.assertEqual("00", session.controls[BASIC1_DIVISION].Text)
        self.assertEqual("10000289", result["material_candidate"])
        self.assertFalse(result["saved"])

    def test_basic_data_1_rejects_unapproved_values_or_prefilled_fields(self):
        session = Session()
        with self.assertRaises(ActionBlockedError):
            prepare_basic_data_1(session, TARGET, {**BASIC1_VALUES, "base_unit": "EA"})
        session.controls[BASIC1_DESCRIPTION].Text = "other"
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", return_value={**BASIC1, "input_fields": [{**x, "text": "other"} if x["id"] == BASIC1_DESCRIPTION else x for x in BASIC1["input_fields"]]}):
            with self.assertRaises(ActionBlockedError):
                prepare_basic_data_1(session, TARGET, BASIC1_VALUES)

    def test_basic_data_1_stages_description_when_other_fields_are_disabled(self):
        session = Session()
        blocked = {**BASIC1, "input_fields": [
            {**item, "changeable": False} if item["id"] in {BASIC1_UNIT, BASIC1_DIVISION} else item
            for item in BASIC1["input_fields"]]}
        with patch("src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[blocked, blocked]):
            result = prepare_basic_data_1(session, TARGET, BASIC1_VALUES)
        self.assertEqual("S4615 Training Product 101", session.controls[BASIC1_DESCRIPTION].Text)
        self.assertEqual("", session.controls[BASIC1_UNIT].Text)
        self.assertEqual("", session.controls[BASIC1_DIVISION].Text)
        self.assertEqual([BASIC1_UNIT, BASIC1_DIVISION], result["pending_fields"])
        self.assertFalse(result["saved"])

    def test_exact_save_is_checkpointed_once_and_requires_readback(self):
        session = Session()
        with tempfile.TemporaryDirectory() as folder:
            with patch("src.provisioning.s4615_product_basic_gui.CHECKPOINT_PATH", Path(folder) / "checkpoint.json"), patch(
                "src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[BASIC2_READY, BASIC1_READY, BASIC1_READY]
            ):
                result = save_basic_root_once(session, TARGET, ROOT_VALUES)
            self.assertTrue(session.controls["/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"].pressed)
            self.assertTrue(result["saved_attempted"])
            self.assertFalse(result["verified"])
            self.assertEqual("AMBIGUOUS", json.loads((Path(folder) / "checkpoint.json").read_text())["operations"]["S4615_PRODUCT_P101_BASIC_ROOT"]["status"])
            with patch("src.provisioning.s4615_product_basic_gui.CHECKPOINT_PATH", Path(folder) / "checkpoint.json"):
                with self.assertRaises(ActionBlockedError):
                    save_basic_root_once(session, TARGET, ROOT_VALUES)

    def test_save_rejects_changed_values_before_checkpoint(self):
        session = Session()
        with self.assertRaises(ActionBlockedError):
            save_basic_root_once(session, TARGET, {**ROOT_VALUES, "base_unit": "EA"})
        with tempfile.TemporaryDirectory() as folder:
            bad = {**BASIC1_READY, "input_fields": [{**item, "text": "EA"} if item["id"] == BASIC1_UNIT else item for item in BASIC1_READY["input_fields"]]}
            with patch("src.provisioning.s4615_product_basic_gui.CHECKPOINT_PATH", Path(folder) / "checkpoint.json"), patch(
                "src.provisioning.s4615_product_basic_gui.inspect_screen", side_effect=[BASIC2_READY, bad]
            ):
                with self.assertRaises(ActionBlockedError):
                    save_basic_root_once(session, TARGET, ROOT_VALUES)
            self.assertFalse((Path(folder) / "checkpoint.json").exists())


if __name__ == "__main__":
    unittest.main()
