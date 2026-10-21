import json
import io
import tempfile
import unittest
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from src.sap_gui_bridge.__main__ import main as bridge_cli_main
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError, DuplicateRequestError, ProtocolError, SessionNotFoundError
from src.sap_gui_bridge.navigation import (
    COMPANY_CODE_DISPLAY_EXCEPTION,
    DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION,
    SALES_ORGANIZATION_DISPLAY_EXCEPTION,
)
from src.sap_gui_bridge.protocol import enqueue_request, validate_request, write_response
from src.sap_gui_bridge.navigation import select_s4615_billing_type_activity, find_s4615_sales_type, display_s4615_sales_reference
from src.sap_gui_bridge.runner import process_request_file
from src.sap_gui_bridge.safety import SafetyMode, SafetyPolicy
from tests.test_sap_gui_bridge import Collection, Control, RawSession, sap_gui

DYNAMIC_COMPANY_PARENT_KEY = "04 dynamic parent"
DYNAMIC_COMPANY_NODE_KEY = "05 dynamic company"


class TreeControl(Control):
    def __init__(self, control_id, nodes):
        super().__init__(control_id, "GuiTree")
        self.nodes = nodes
        self.operations = []
        self.SelectedNode = None
        self.expanded = set()

    def GetAllNodeKeys(self):
        return list(self.nodes)

    def GetNodeTextByKey(self, key):
        return self.nodes[key]

    def SelectNode(self, key):
        self.operations.append(("SELECT_TREE_NODE", key))
        self.SelectedNode = key

    def ExpandNode(self, key):
        self.operations.append(("EXPAND_TREE_NODE", key))
        self.expanded.add(key)

    def CollapseNode(self, key):
        self.operations.append(("COLLAPSE_TREE_NODE", key))
        self.expanded.discard(key)

    def DoubleClickNode(self, key):
        self.operations.append(("DOUBLE_CLICK_TREE_NODE", key))

    def IsNodeExpanded(self, key):
        return key in self.expanded


class MockScrollbar:
    def __init__(self, maximum):
        self.Maximum = maximum
        self._position = 0
        self.visited = []

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = min(int(value), self.Maximum)
        self.visited.append(self._position)


class StalledScrollbar(MockScrollbar):
    @MockScrollbar.Position.setter
    def Position(self, value):
        self.visited.append(self._position)


class CompanyCodeTable:
    def __init__(self, values, visible_rows=10):
        self.Id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001"
        self.Type = "GuiTableControl"
        self.Text = "Company Codes"
        self.Tooltip = ""
        self.Changeable = False
        self.Visible = True
        self.RowCount = len(values)
        self.VisibleRowCount = visible_rows
        self.ColumnCount = 1
        self.VerticalScrollbar = MockScrollbar(max(0, len(values) - visible_rows))
        self.values = list(values)

    @property
    def Children(self):
        start = self.VerticalScrollbar.Position
        controls = []
        for relative, value in enumerate(self.values[start:start + self.VisibleRowCount]):
            controls.append(
                Control(
                    f"{self.Id}/txtV_T001-BUKRS[0,{relative}]",
                    "GuiTextField",
                    value,
                    changeable=False,
                )
            )
        return Collection(controls)


class SalesOrganizationActivityTable:
    def __init__(self, rows):
        self.Id = "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES"
        self.Type = "GuiTableControl"
        self.Text = "Sales Organization activities"
        self.Tooltip = ""
        self.Changeable = False
        self.Visible = True
        self.RowCount = len(rows)
        self.VisibleRowCount = len(rows)
        self.ColumnCount = 1
        self.rows = list(rows)
        self.selected_rows = []

    @property
    def Children(self):
        return Collection([
            Control(f"{self.Id}/txtACTIVITY[0,{index}]", "GuiTextField", text)
            for index, text in enumerate(self.rows)
        ])

    def SelectRow(self, index):
        self.selected_rows.append(index)


class LocalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.request_dir = root / "requests"
        self.response_dir = root / "responses"
        self.archive_dir = root / "archive"
        patcher = patch.multiple(
            "src.sap_gui_bridge.protocol",
            REQUEST_DIR=self.request_dir,
            RESPONSE_DIR=self.response_dir,
            ARCHIVE_DIR=self.archive_dir,
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        runner_patcher = patch.multiple(
            "src.sap_gui_bridge.runner",
            REQUEST_DIR=self.request_dir,
            ARCHIVE_DIR=self.archive_dir,
        )
        runner_patcher.start()
        self.addCleanup(runner_patcher.stop)

    def request(self, action="STATUS", params=None, request_id=None):
        return enqueue_request(action, params or {}, request_id=request_id)

    def factory(self, raw=None):
        raw = raw or RawSession()
        return lambda: SapGuiConnection(
            mode=SafetyMode.READ,
            get_object=lambda _: sap_gui([raw]),
            log_path=Path(self.tmp.name) / "audit.jsonl",
        )

    def navigation_raw(self, **kwargs):
        raw = RawSession(transaction="SPRO", **kwargs)
        raw.Busy = False
        button = Control(
            "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]",
            "GuiButton",
            "Guide de référence SAP",
        )
        tree = TreeControl(
            "/app/con[0]/ses[0]/wnd[0]/usr/cntlIMG/shellcont/shell",
            {"ROOT": "Structure de l'entreprise", "SALES": "Commercial"},
        )
        raw.root.Children = Collection([button, tree])
        raw.controls[button.Id] = button
        raw.controls[tree.Id] = tree
        return raw, button, tree

    def sales_organization_img_raw(self):
        raw, _, tree = self.navigation_raw()
        raw.controls.pop(tree.Id)
        tree.Id = SALES_ORGANIZATION_DISPLAY_EXCEPTION["control_id"]
        tree.Type = "GuiShell"
        tree.SubType = "Tree"
        tree.nodes = {
            "02  1      6": "Structure de l'entreprise",
            "03  2      1": "Définition",
            "04  3      4": "Administration des ventes (ADV)",
            "05  4      1": SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
        }
        raw.Info.Transaction = "SIMG"
        raw.Info.Program = "SAPLSHI01"
        raw.root.Text = "Afficher guide d'implémentation"
        raw.controls[tree.Id] = tree
        tree.GetColumnNames = lambda: ["1", "2", "3", "4", "5", "6", "8", "TEXT"]
        tree.GetItemText = lambda key, column: tree.nodes[key]
        tree.GetItemType = lambda key, column: "2" if column in {"8", "TEXT"} else "5"
        return raw, tree

    def distribution_channel_img_raw(self):
        raw, _, tree = self.navigation_raw()
        raw.controls.pop(tree.Id)
        tree.Id = DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION["control_id"]
        tree.Type = "GuiShell"
        tree.SubType = "Tree"
        tree.nodes = {
            "02  1      6": "Structure de l'entreprise",
            "03  2      1": "Définition",
            "04  3      4": "Administration des ventes (ADV)",
            "05  4      2": DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION["node_text"],
        }
        raw.Info.Transaction = "SIMG"
        raw.Info.Program = "SAPLSHI01"
        raw.root.Text = "Afficher guide d'implémentation"
        raw.controls[tree.Id] = tree
        tree.GetColumnNames = lambda: ["1", "2", "3", "4", "5", "6", "8", "TEXT"]
        tree.GetItemText = lambda key, column: tree.nodes[key]
        tree.GetItemType = lambda key, column: "2" if column in {"8", "TEXT"} else "5"
        return raw, tree

    @staticmethod
    def navigation_params(control, operation, expected_text=None, node_key=None):
        params = {
            "control_id": control.Id,
            "expected_type": control.Type,
            "expected_text": expected_text,
            "navigation_operation": operation,
        }
        if node_key is not None:
            params["node_key"] = node_key
        return params

    def process(self, raw, action, params=None):
        queued = self.request(action, params)
        path = self.request_dir / f"{queued['request_id']}.json"
        return process_request_file(path, self.factory(raw))

    def test_malformed_request(self):
        request_id = str(uuid.uuid4())
        self.request_dir.mkdir(parents=True)
        path = self.request_dir / f"{request_id}.json"
        path.write_text("{bad", encoding="utf-8")
        response = process_request_file(path, self.factory())
        self.assertEqual("ERROR", response["status"])
        self.assertTrue((self.archive_dir / f"{request_id}.json").exists())

    def test_request_filename_must_match_payload_id(self):
        filename_id = str(uuid.uuid4())
        payload_id = str(uuid.uuid4())
        self.request_dir.mkdir(parents=True)
        path = self.request_dir / f"{filename_id}.json"
        path.write_text(json.dumps({"request_id": payload_id, "mode": "READ", "action": "STATUS", "params": {}}), encoding="utf-8")
        response = process_request_file(path, self.factory())
        self.assertEqual("ERROR", response["status"])

    def test_unsupported_and_write_actions_are_blocked(self):
        for action in ("SAVE", "CREATE", "MODIFY", "POST", "PATCH", "PUT", "DELETE", "RELEASE", "TRANSPORT"):
            with self.subTest(action=action), self.assertRaises(ProtocolError):
                validate_request({"request_id": str(uuid.uuid4()), "mode": "READ", "action": action, "params": {}})

    def test_non_read_mode_is_blocked(self):
        with self.assertRaises(ProtocolError):
            validate_request({"request_id": str(uuid.uuid4()), "mode": "PREPARE", "action": "STATUS", "params": {}})

    def test_wrong_system_client_and_user_fail_closed(self):
        for field, value in (("system", "OTHER"), ("client", "100"), ("user", "OTHER")):
            with self.subTest(field=field):
                kwargs = {field: value}
                queued = self.request(request_id=str(uuid.uuid4()))
                path = self.request_dir / f"{queued['request_id']}.json"
                response = process_request_file(path, self.factory(RawSession(**kwargs)))
                self.assertEqual("ERROR", response["status"])
                self.assertEqual("SessionNotFoundError", response["error"]["type"])

    def test_duplicate_request_is_rejected(self):
        request_id = str(uuid.uuid4())
        self.request(request_id=request_id)
        with self.assertRaises(DuplicateRequestError):
            self.request(request_id=request_id)

    def test_success_response_and_request_archive(self):
        queued = self.request()
        request_path = self.request_dir / f"{queued['request_id']}.json"
        response = process_request_file(request_path, self.factory())
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("A4H", response["sap"]["system"])
        response_path = self.response_dir / f"{queued['request_id']}.json"
        self.assertTrue(response_path.exists())
        self.assertEqual(response, json.loads(response_path.read_text(encoding="utf-8")))
        self.assertTrue((self.archive_dir / f"{queued['request_id']}.json").exists())
        self.assertFalse(request_path.exists())

    def test_open_transaction_is_limited_to_spro(self):
        with self.assertRaises(ProtocolError):
            self.request("OPEN_TRANSACTION", {"transaction": "SE16"})
        queued = self.request("OPEN_TRANSACTION", {"transaction": "SPRO"})
        path = self.request_dir / f"{queued['request_id']}.json"
        response = process_request_file(path, self.factory())
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("SPRO", response["sap"]["transaction"])

    def test_dedicated_back_action_is_read_only_and_does_not_use_navigate_contract(self):
        raw = RawSession(transaction="SIMG")
        response = self.process(raw, "BACK", {})
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual(3, raw.root.last_key)
        self.assertEqual("SIMG", response["result"]["transaction"])

    def test_close_sapldsyh_info_popup_returns_to_img(self):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'implémentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        read_only_field = Control(
            f"{popup_id}/usr/txtDISPLAY",
            "GuiTextField",
            "display-only documentation",
            changeable=False,
        )
        popup = Control(
            popup_id,
            "GuiModalWindow",
            "Information",
            children=[read_only_field],
        )
        raw.controls["wnd[1]"] = popup
        raw.controls[popup_id] = popup

        def close_with_back(key):
            popup.last_key = key
            raw.controls.pop("wnd[1]")
            raw.controls.pop(popup_id)
            raw.Info.Program = "SAPLSHI01"

        popup.sendVKey = close_with_back
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
        }
        response = self.process(raw, "CLOSE_IMG_INFO_POPUP", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual(3, popup.last_key)
        self.assertEqual("SAPLSHI01", response["result"]["program"])
        self.assertEqual("Afficher guide d'implémentation", response["result"]["window_title"])
        self.assertEqual([], response["result"]["popups"])
        self.assertEqual(
            "READ_ONLY_DOCUMENTATION_OR_INFO",
            response["result"]["closed_destination_classification"],
        )

    def test_close_sapldsyh_info_popup_blocks_editable_field(self):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'implémentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        editable_field = Control(
            f"{popup_id}/usr/txtEDITABLE",
            "GuiTextField",
            "editable",
            changeable=True,
        )
        popup = Control(
            popup_id,
            "GuiModalWindow",
            "Information",
            children=[editable_field],
        )
        raw.controls["wnd[1]"] = popup
        raw.controls[popup_id] = popup
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
        }

        response = self.process(raw, "CLOSE_IMG_INFO_POPUP", params)

        self.assertEqual("ERROR", response["status"])
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertIn("editable/changeable", response["error"]["message"])
        self.assertFalse(hasattr(popup, "last_key"))

    def test_close_img_info_popup_contract_is_exact(self):
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "window_id": "/app/con[0]/ses[0]/wnd[2]",
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
        }
        with self.assertRaises(ProtocolError):
            self.request("CLOSE_IMG_INFO_POPUP", params)

    def _company_code_activity_dialog(self, *, duplicate_row=False, duplicate_button=False):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'implémentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        copy_row = Control(
            f"{popup_id}/usr/radCOPY",
            "GuiRadioButton",
            "Copier, supprimer, contr\ufffdler soci\ufffdt\ufffd",
        )
        display_row = Control(
            f"{popup_id}/usr/radDISPLAY",
            "GuiRadioButton",
            "Traiter donn\ufffdes soci\ufffdt\ufffd",
        )
        copy_row.selected = False
        display_row.selected = False
        copy_row.Select = lambda: setattr(copy_row, "selected", True)
        display_row.Select = lambda: setattr(display_row, "selected", True)
        rows = [copy_row, display_row]
        if duplicate_row:
            duplicate = Control(
                f"{popup_id}/usr/radDISPLAY2",
                "GuiRadioButton",
                "Traiter donn\ufffdes soci\ufffdt\ufffd",
            )
            duplicate.Select = lambda: setattr(duplicate, "selected", True)
            rows.append(duplicate)
        select_button = Control(
            f"{popup_id}/tbar[0]/btn[0]",
            "GuiButton",
            "S\ufffdlectionner",
        )
        buttons = [select_button]
        if duplicate_button:
            buttons.append(
                Control(
                    f"{popup_id}/usr/btnSELECT2",
                    "GuiButton",
                    "S\ufffdlectionner",
                )
            )
        popup = Control(
            popup_id,
            "GuiModalWindow",
            "S\ufffdlection de l'activit\ufffd :",
            children=rows + buttons,
        )
        raw.controls["wnd[1]"] = popup
        for control in [popup, *rows, *buttons]:
            raw.controls[control.Id] = control

        def open_selected_activity():
            select_button.pressed = True
            raw.controls.pop("wnd[1]")
            raw.controls.pop(popup_id)
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue de customizing"

        select_button.press = open_selected_activity
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "company_code",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "row_text": "Traiter données société",
            "button_text": "Sélectionner",
        }
        return raw, copy_row, display_row, select_button, params

    def test_company_code_activity_selects_exact_display_row_and_button(self):
        raw, copy_row, display_row, select_button, params = (
            self._company_code_activity_dialog()
        )

        response = self.process(raw, "SELECT_COMPANY_CODE_ACTIVITY", params)

        self.assertEqual("SUCCESS", response["status"])
        self.assertFalse(copy_row.selected)
        self.assertTrue(display_row.selected)
        self.assertTrue(select_button.pressed)
        self.assertEqual("SAPLSVIM", response["result"]["program"])
        self.assertEqual("Afficher vue de customizing", response["result"]["window_title"])
        self.assertEqual([], response["result"]["popups"])
        self.assertEqual(
            "IMG_ACTIVITY_SELECTION_DIALOG",
            response["result"]["activity_selection"]["classification"],
        )

    def test_company_code_activity_ambiguous_row_or_button_is_blocked(self):
        for option in ("duplicate_row", "duplicate_button"):
            with self.subTest(option=option):
                raw, copy_row, display_row, select_button, params = (
                    self._company_code_activity_dialog(**{option: True})
                )
                response = self.process(raw, "SELECT_COMPANY_CODE_ACTIVITY", params)
                self.assertEqual("ERROR", response["status"])
                self.assertEqual("ActionBlockedError", response["error"]["type"])
                self.assertIn("not deterministic", response["error"]["message"])
                self.assertFalse(copy_row.selected)
                self.assertFalse(display_row.selected)
                self.assertFalse(select_button.pressed)

    def _company_code_table_raw(self, *, include_1010):
        raw = RawSession(transaction="V_T001")
        raw.Info.Program = "SAPL0ORG"
        raw.root.Text = "Afficher vue société"
        values = [f"{2000 + index:04d}" for index in range(112)]
        if include_1010:
            values[105] = "1010"
        table = CompanyCodeTable(values)
        raw.root.Children = Collection([table])
        raw.controls[table.Id] = table
        original_find = raw.findById
        raw.table_acquisitions = 0

        def counted_find(control_id):
            if control_id == table.Id:
                raw.table_acquisitions += 1
            return original_find(control_id)

        raw.findById = counted_find
        params = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "table_id": table.Id,
            "column": "BUKRS",
            "value": "1010",
        }
        return raw, table, params

    def test_find_table_value_reads_scroll_pages_and_finds_1010(self):
        raw, table, params = self._company_code_table_raw(include_1010=True)
        response = self.process(raw, "FIND_TABLE_VALUE", params)
        search = response["result"]["table_value_search"]
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("FOUND", search["result"])
        self.assertEqual(105, search["found_row"])
        self.assertGreater(len(table.VerticalScrollbar.visited), 1)
        self.assertGreater(raw.table_acquisitions, len(table.VerticalScrollbar.visited))
        self.assertEqual("1010", table.values[105])

    def test_find_table_value_stalled_scrollbar_stops_safely(self):
        raw, table, params = self._company_code_table_raw(include_1010=True)
        table.VerticalScrollbar = StalledScrollbar(102)
        response = self.process(raw, "FIND_TABLE_VALUE", params)
        search = response["result"]["table_value_search"]
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("UNKNOWN", search["result"])
        self.assertIn("positioning button is unavailable", search["reason"])

    def test_find_table_value_position_fallback_is_read_only(self):
        raw, table, params = self._company_code_table_raw(include_1010=True)
        before = list(table.values)
        table.VerticalScrollbar = StalledScrollbar(102)
        position_button = Control(
            "/app/con[0]/ses[0]/wnd[0]/usr/btnVIM_POSI_PUSH",
            "GuiButton",
            "Positionner.....",
        )
        raw.controls[position_button.Id] = position_button

        def open_position_dialog():
            popup_id = "/app/con[0]/ses[0]/wnd[1]"
            criterion = Control(
                f"{popup_id}/usr/ctxtVIM_POSI",
                "GuiCTextField",
                "",
                changeable=True,
            )
            confirm = Control(
                f"{popup_id}/tbar[0]/btn[0]",
                "GuiButton",
                "Suite",
            )
            popup = Control(
                popup_id,
                "GuiModalWindow",
                "Positionner",
                children=[criterion, confirm],
            )
            raw.controls["wnd[1]"] = popup
            for control in [popup, criterion, confirm]:
                raw.controls[control.Id] = control

            def confirm_position():
                self.assertEqual("1010", criterion.Text)
                table.VerticalScrollbar._position = 102
                raw.controls.pop("wnd[1]")
                raw.controls.pop(popup_id)

            confirm.press = confirm_position

        position_button.press = open_position_dialog
        response = self.process(raw, "FIND_TABLE_VALUE", params)
        search = response["result"]["table_value_search"]
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("FOUND", search["result"])
        self.assertEqual("POSITION_DIALOG", search["method"])
        self.assertEqual(before, table.values)

    def test_find_table_value_confirms_absence_after_all_112_rows(self):
        raw, table, params = self._company_code_table_raw(include_1010=False)
        before = list(table.values)
        response = self.process(raw, "FIND_TABLE_VALUE", params)
        search = response["result"]["table_value_search"]
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("CONFIRMED_NOT_FOUND", search["result"])
        self.assertEqual(112, search["rows_read"])
        self.assertEqual(before, table.values)

    def test_sales_organization_leaf_exception_is_exact_and_navigation_only(self):
        raw, tree = self.sales_organization_img_raw()

        def click_link(key, column):
            tree.operations.append(("CLICK_LINK", key, column))
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue organisation commerciale"

        tree.ClickLink = click_link
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
            node_key="05  4      1",
        )
        params["item_column"] = "2"
        params["expected_transaction"] = "SIMG"
        self.assertEqual("GuiShell", params["expected_type"])
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual([("CLICK_LINK", "05  4      1", "2")], tree.operations)
        self.assertEqual("2", response["result"]["img_activity_open"]["item_column"])

    def test_distribution_channel_leaf_exception_is_exact_and_navigation_only(self):
        raw, tree = self.distribution_channel_img_raw()

        def click_link(key, column):
            tree.operations.append(("CLICK_LINK", key, column))
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue canal de distribution"

        tree.ClickLink = click_link
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION["node_text"],
            node_key="05  4      2",
        )
        params["item_column"] = "2"
        params["expected_transaction"] = "SIMG"
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual([("CLICK_LINK", "05  4      2", "2")], tree.operations)
        self.assertEqual("2", response["result"]["img_activity_open"]["item_column"])

    def test_distribution_channel_exception_rejects_wrong_path(self):
        raw, tree = self.distribution_channel_img_raw()
        tree.nodes["04  3      4"] = "Comptabilité financière"
        tree.ClickLink = lambda key, column: tree.operations.append(
            ("CLICK_LINK", key, column)
        )
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=DISTRIBUTION_CHANNEL_DISPLAY_EXCEPTION["node_text"],
            node_key="05  4      2",
        )
        params["item_column"] = "2"
        params["expected_transaction"] = "SIMG"
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("ERROR", response["status"])
        self.assertIn("blocked write term", response["error"]["message"])
        self.assertEqual([], tree.operations)

    def test_sales_organization_img_leaf_rejects_unobserved_item_column(self):
        raw, tree = self.sales_organization_img_raw()
        tree.ClickLink = lambda key, column: tree.operations.append(
            ("CLICK_LINK", key, column)
        )
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
            node_key="05  4      1",
        )
        params["item_column"] = "UNOBSERVED"
        params["expected_transaction"] = "SIMG"

        response = self.process(raw, "NAVIGATE", params)

        self.assertEqual("ERROR", response["status"])
        self.assertIn(
            "item column is not backed by observed tree capabilities",
            response["error"]["message"],
        )
        self.assertEqual([], tree.operations)

    def test_sales_organization_img_tree_rejects_wrong_control_id(self):
        raw, tree = self.sales_organization_img_raw()
        params = self.navigation_params(
            tree,
            "EXPAND_TREE_NODE",
            expected_text="Structure de l'entreprise",
            node_key="02  1      6",
        )
        params["control_id"] = tree.Id + "/unexpected"

        response = self.process(raw, "NAVIGATE", params)

        self.assertEqual("ERROR", response["status"])
        self.assertIn("NAVIGATE control not found", response["error"]["message"])
        self.assertEqual([], tree.operations)

    def test_sales_organization_img_tree_rejects_unexpected_type(self):
        raw, tree = self.sales_organization_img_raw()
        tree.Type = "GuiTree"
        params = self.navigation_params(
            tree,
            "EXPAND_TREE_NODE",
            expected_text="Structure de l'entreprise",
            node_key="02  1      6",
        )
        params["expected_type"] = "GuiShell"

        response = self.process(raw, "NAVIGATE", params)

        self.assertEqual("ERROR", response["status"])
        self.assertIn("NAVIGATE control type mismatch", response["error"]["message"])
        self.assertEqual([], tree.operations)

    def test_sales_organization_exception_rejects_wrong_observed_path(self):
        raw, _, tree = self.navigation_raw()
        old_id = tree.Id
        tree.Id = SALES_ORGANIZATION_DISPLAY_EXCEPTION["control_id"]
        tree.Type = "GuiShell"
        tree.SubType = "Tree"
        tree.nodes = {
            "02 root": "Structure de l'entreprise",
            "03 definition": "Définition",
            "04 wrong": "Comptabilité financière",
            "05 leaf": SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
        }
        raw.Info.Transaction = "SIMG"
        raw.Info.Program = "SAPLSHI01"
        raw.controls.pop(old_id)
        raw.controls[tree.Id] = tree
        tree.GetColumnNames = lambda: ["ACTION"]
        tree.GetItemText = lambda key, column: tree.nodes[key]
        tree.GetItemType = lambda key, column: "5"
        tree.ClickLink = lambda key, column: None
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=SALES_ORGANIZATION_DISPLAY_EXCEPTION["node_text"],
            node_key="05 leaf",
        )
        params["expected_transaction"] = "SIMG"
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("ERROR", response["status"])
        self.assertEqual("ActionBlockedError", response["error"]["type"])

    def _legacy_sales_organization_activity_dialog(self, *, duplicate=False):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'implémentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        copy_row = Control(
            f"{popup_id}/usr/radCOPY",
            "GuiRadioButton",
            "Copier organisation commerciale",
        )
        display_row = Control(
            f"{popup_id}/usr/radDISPLAY",
            "GuiRadioButton",
            "Traiter organisation commerciale",
        )
        copy_row.selected = False
        display_row.selected = False
        copy_row.Select = lambda: setattr(copy_row, "selected", True)
        display_row.Select = lambda: setattr(display_row, "selected", True)
        rows = [copy_row, display_row]
        if duplicate:
            duplicate_row = Control(
                f"{popup_id}/usr/radDISPLAY2",
                "GuiRadioButton",
                "Traiter organisation commerciale",
            )
            duplicate_row.Select = lambda: setattr(duplicate_row, "selected", True)
            rows.append(duplicate_row)
        select_button = Control(
            f"{popup_id}/tbar[0]/btn[2]",
            "GuiButton",
            "S\ufffdlectionner",
        )
        popup = Control(
            popup_id,
            "GuiModalWindow",
            "S\ufffdlection de l'activit\ufffd :",
            children=rows + [select_button],
        )
        raw.controls["wnd[1]"] = popup
        for control in [popup, *rows, select_button]:
            raw.controls[control.Id] = control

        def open_activity():
            select_button.pressed = True
            raw.controls.pop("wnd[1]")
            raw.controls.pop(popup_id)
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue organisation commerciale"

        select_button.press = open_activity
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "row_text": "Traiter organisation commerciale",
            "button_text": "Sélectionner",
        }
        return raw, copy_row, display_row, select_button, params

    def _sales_organization_activity_dialog(self, *, duplicate=False):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'impl\u00e9mentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        rows = [
            "D\u00e9finir l'organisation commerciale",
            "Contr\u00f4ler, supprimer, copier l'organisation commerciale",
        ]
        if duplicate:
            rows.insert(1, "D\u00e9finir l'organisation commerciale")
        table = SalesOrganizationActivityTable(rows)
        select_button = Control(
            f"{popup_id}/tbar[0]/btn[2]", "GuiButton", "S\u00e9lectionner"
        )
        popup = Control(
            popup_id,
            "GuiModalWindow",
            "S\u00e9lection de l'activit\u00e9 :",
            children=[table, select_button],
        )
        raw.controls["wnd[1]"] = popup
        for control in [popup, table, select_button]:
            raw.controls[control.Id] = control

        def open_activity():
            select_button.pressed = True
            raw.controls.pop("wnd[1]")
            raw.controls.pop(popup_id)
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue organisation commerciale"

        select_button.press = open_activity
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "sales_organization",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "table_id": table.Id,
            "row_text": "D\u00e9finir l'organisation commerciale",
            "button_id": select_button.Id,
            "button_text": "S\u00e9lectionner",
        }
        return raw, table, select_button, params

    def test_sales_organization_activity_selects_only_exact_processing_row(self):
        raw, table, select_button, params = (
            self._sales_organization_activity_dialog()
        )
        response = self.process(raw, "SELECT_SALES_ORGANIZATION_ACTIVITY", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual([0], table.selected_rows)
        self.assertNotIn(1, table.selected_rows)
        self.assertTrue(select_button.pressed)
        self.assertEqual("SAPLSVIM", response["result"]["program"])

    def test_sales_organization_activity_ambiguous_row_is_blocked(self):
        raw, table, select_button, params = (
            self._sales_organization_activity_dialog(duplicate=True)
        )
        response = self.process(raw, "SELECT_SALES_ORGANIZATION_ACTIVITY", params)
        self.assertEqual("ERROR", response["status"])
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertEqual([], table.selected_rows)
        self.assertFalse(select_button.pressed)

    def _distribution_channel_activity_dialog(self, *, duplicate=False):
        raw = RawSession(transaction="SIMG")
        raw.Info.Program = "SAPLDSYH"
        raw.root.Text = "Afficher guide d'impl\u00e9mentation"
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        rows = [
            "D\u00e9finir le canal de distribution",
            "Contr\u00f4ler, supprimer, copier le canal de distribution",
        ]
        if duplicate:
            rows.insert(1, "D\u00e9finir le canal de distribution")
        table = SalesOrganizationActivityTable(rows)
        select_button = Control(f"{popup_id}/tbar[0]/btn[2]", "GuiButton", "S\u00e9lectionner")
        popup = Control(popup_id, "GuiModalWindow", "S\u00e9lection de l'activit\u00e9 :", children=[table, select_button])
        raw.controls["wnd[1]"] = popup
        for control in [popup, table, select_button]:
            raw.controls[control.Id] = control

        def open_activity():
            select_button.pressed = True
            raw.controls.pop("wnd[1]")
            raw.controls.pop(popup_id)
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue canal de distribution"

        select_button.press = open_activity
        params = {
            "source": "OPEN_IMG_ACTIVITY",
            "target": "distribution_channel",
            "window_id": popup_id,
            "expected_transaction": "SIMG",
            "expected_program": "SAPLDSYH",
            "table_id": table.Id,
            "row_text": "D\u00e9finir le canal de distribution",
            "button_id": select_button.Id,
            "button_text": "S\u00e9lectionner",
        }
        return raw, table, select_button, params

    def test_distribution_channel_activity_selects_only_exact_definition_row(self):
        raw, table, select_button, params = self._distribution_channel_activity_dialog()
        response = self.process(raw, "SELECT_DISTRIBUTION_CHANNEL_ACTIVITY", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual([0], table.selected_rows)
        self.assertNotIn(1, table.selected_rows)
        self.assertTrue(select_button.pressed)

    def test_distribution_channel_activity_ambiguous_row_is_blocked(self):
        raw, table, select_button, params = self._distribution_channel_activity_dialog(duplicate=True)
        response = self.process(raw, "SELECT_DISTRIBUTION_CHANNEL_ACTIVITY", params)
        self.assertEqual("ERROR", response["status"])
        self.assertEqual([], table.selected_rows)
        self.assertFalse(select_button.pressed)

    def test_sales_organization_resolver_reads_only_exact_table_rows(self):
        raw, table, select_button, params = self._sales_organization_activity_dialog()
        table.rows[0] = "Autre activit\u00e9"
        popup = raw.controls["wnd[1]"]
        misleading = Control(
            "/app/con[0]/ses[0]/wnd[1]/usr/lblMISLEADING",
            "GuiLabel",
            "D\u00e9finir l'organisation commerciale",
        )
        popup.Children = Collection([table, misleading, select_button])
        raw.controls[misleading.Id] = misleading
        response = self.process(raw, "SELECT_SALES_ORGANIZATION_ACTIVITY", params)
        self.assertEqual("ERROR", response["status"])
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertEqual([], table.selected_rows)
        self.assertFalse(select_button.pressed)

    def test_safe_button_navigation(self):
        raw, button, _ = self.navigation_raw()
        params = self.navigation_params(
            button, "PRESS_SAFE_BUTTON", expected_text="Guide de référence SAP"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertTrue(button.pressed)
        self.assertIn("GuiTree", response["result"]["visible_control_types"])

    def test_tree_expand_select_collapse_and_double_click(self):
        for operation in (
            "EXPAND_TREE_NODE",
            "SELECT_TREE_NODE",
            "COLLAPSE_TREE_NODE",
            "DOUBLE_CLICK_TREE_NODE",
        ):
            with self.subTest(operation=operation):
                raw, _, tree = self.navigation_raw()
                params = self.navigation_params(
                    tree, operation, expected_text="Commercial", node_key="SALES"
                )
                response = self.process(raw, "NAVIGATE", params)
                self.assertEqual("SUCCESS", response["status"])
                self.assertEqual([(operation, "SALES")], tree.operations)

    def test_tree_navigation_reuses_native_column_text_fallback(self):
        raw, _, tree = self.navigation_raw()
        tree.GetNodeTextByKey = lambda key: ""
        tree.GetColumnNames = lambda: ["Hierarchy"]
        tree.GetItemText = lambda key, column: "Commercial"
        params = self.navigation_params(
            tree,
            "SELECT_TREE_NODE",
            expected_text="Commercial",
            node_key="SALES",
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual([("SELECT_TREE_NODE", "SALES")], tree.operations)

    def test_exact_company_code_sensitive_leaf_is_read_only_allowlisted(self):
        raw, _, tree = self.navigation_raw()
        old_id = tree.Id
        tree.Id = COMPANY_CODE_DISPLAY_EXCEPTION["control_id"]
        tree.Type = "GuiShell"
        tree.SubType = "Tree"
        tree.nodes = {
            DYNAMIC_COMPANY_PARENT_KEY: COMPANY_CODE_DISPLAY_EXCEPTION["parent_text"],
            DYNAMIC_COMPANY_NODE_KEY: COMPANY_CODE_DISPLAY_EXCEPTION["node_text"],
        }
        raw.Info.Transaction = "SIMG"
        raw.Info.Program = "SAPLSHI01"
        raw.controls.pop(old_id)
        raw.controls[tree.Id] = tree
        params = self.navigation_params(
            tree,
            "DOUBLE_CLICK_TREE_NODE",
            expected_text=COMPANY_CODE_DISPLAY_EXCEPTION["node_text"],
            node_key=DYNAMIC_COMPANY_NODE_KEY,
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual(
            [("DOUBLE_CLICK_TREE_NODE", DYNAMIC_COMPANY_NODE_KEY)],
            tree.operations,
        )
        self.assertEqual("NO_OBSERVED_EFFECT", response["result"]["navigation_outcome"])

    def test_com_success_with_unchanged_screen_is_no_observed_effect(self):
        raw, _, tree = self.navigation_raw()
        params = self.navigation_params(
            tree, "DOUBLE_CLICK_TREE_NODE", expected_text="Commercial", node_key="SALES"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["status"])
        self.assertEqual("NO_OBSERVED_EFFECT", response["result"]["navigation_outcome"])
        self.assertFalse(response["result"]["navigation_effect"]["observed"])

    def test_expand_without_state_or_descendant_change_is_no_observed_effect(self):
        raw, _, tree = self.navigation_raw()
        tree.ExpandNode = lambda key: tree.operations.append(("EXPAND_TREE_NODE", key))
        params = self.navigation_params(
            tree, "EXPAND_TREE_NODE", expected_text="Commercial", node_key="SALES"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("NO_OBSERVED_EFFECT", response["result"]["navigation_outcome"])
        self.assertEqual(0, response["result"]["navigation_effect"]["descendant_count_after"])

    def test_expand_adding_descendant_is_success(self):
        raw, _, tree = self.navigation_raw()
        tree.nodes = {"01 root": "Root", "02 branch": "Branch"}

        def expand(key):
            tree.operations.append(("EXPAND_TREE_NODE", key))
            tree.nodes["03 child"] = "Child"

        tree.ExpandNode = expand
        params = self.navigation_params(
            tree, "EXPAND_TREE_NODE", expected_text="Branch", node_key="02 branch"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertEqual(1, response["result"]["navigation_effect"]["descendant_count_after"])
        self.assertEqual(["03 child"], response["result"]["navigation_effect"]["new_node_keys"])

    def test_expand_with_loaded_direct_child_is_idempotent(self):
        raw, _, tree = self.navigation_raw()
        tree.nodes = {"01 root": "Root", "02 branch": "Branch", "03 child": "Child"}
        params = self.navigation_params(
            tree, "EXPAND_TREE_NODE", expected_text="Branch", node_key="02 branch"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("ALREADY_EXPANDED", response["result"]["navigation_outcome"])
        self.assertEqual([], tree.operations)
        self.assertTrue(response["result"]["navigation_effect"]["already_expanded"])

    def _img_activity_raw(self):
        raw, _, tree = self.navigation_raw()
        old_id = tree.Id
        tree.Id = COMPANY_CODE_DISPLAY_EXCEPTION["control_id"]
        tree.Type = "GuiShell"
        tree.SubType = "Tree"
        tree.nodes = {
            DYNAMIC_COMPANY_PARENT_KEY: COMPANY_CODE_DISPLAY_EXCEPTION["parent_text"],
            DYNAMIC_COMPANY_NODE_KEY: COMPANY_CODE_DISPLAY_EXCEPTION["node_text"],
        }
        raw.Info.Transaction = "SIMG"
        raw.Info.Program = "SAPLSHI01"
        raw.root.Text = "Afficher guide d'implÃ©mentation"
        raw.controls.pop(old_id)
        raw.controls[tree.Id] = tree
        tree.GetColumnNames = lambda: ["ACTION"]
        tree.GetItemText = lambda key, column: COMPANY_CODE_DISPLAY_EXCEPTION["node_text"]
        tree.GetItemType = lambda key, column: "5"
        return raw, tree

    def _open_img_params(self, tree):
        params = self.navigation_params(
            tree,
            "OPEN_IMG_ACTIVITY",
            expected_text=COMPANY_CODE_DISPLAY_EXCEPTION["node_text"],
            node_key=DYNAMIC_COMPANY_NODE_KEY,
        )
        params["expected_transaction"] = "SIMG"
        return params

    def test_img_activity_open_transaction_change_is_success(self):
        raw, tree = self._img_activity_raw()

        def open_activity(key, column):
            tree.operations.append(("CLICK_LINK", key, column))
            raw.Info.Transaction = "OX02"

        tree.ClickLink = open_activity
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertTrue(response["result"]["navigation_effect"]["transaction_changed"])
        self.assertEqual("ClickLink", response["result"]["chosen_native_method"])

    def test_img_activity_open_program_and_title_change_is_success(self):
        raw, tree = self._img_activity_raw()

        def open_activity(key, column):
            tree.operations.append(("CLICK_LINK", key, column))
            raw.Info.Program = "SAPLSVIM"
            raw.root.Text = "Afficher vue de customizing"

        tree.ClickLink = open_activity
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        effect = response["result"]["navigation_effect"]
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertTrue(effect["program_changed"])
        self.assertTrue(effect["window_changed"])

    def test_open_img_activity_uses_click_link_for_observed_type_5(self):
        raw, tree = self._img_activity_raw()
        tree.GetColumnNames = lambda: ["Hierarchy"]
        tree.GetItemText = lambda key, column: COMPANY_CODE_DISPLAY_EXCEPTION["node_text"]
        tree.GetItemType = lambda key, column: "5"

        def click_link(key, column):
            tree.operations.append(("CLICK_LINK", key, column))
            raw.root.Text = "Afficher vue de customizing"

        tree.ClickLink = click_link
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertEqual("ClickLink", response["result"]["chosen_native_method"])
        self.assertEqual("Hierarchy", response["result"]["img_activity_open"]["item_column"])

    def test_open_img_activity_uses_double_click_item_for_type_5_when_link_unavailable(self):
        raw, tree = self._img_activity_raw()

        def double_click_item(key, column):
            tree.operations.append(("DOUBLE_CLICK_ITEM", key, column))
            raw.Info.Program = "SAPMSSY0"
            raw.root.Text = "Afficher hypertexte"

        tree.DoubleClickItem = double_click_item
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertEqual("DoubleClickItem", response["result"]["chosen_native_method"])
        self.assertEqual([("DOUBLE_CLICK_ITEM", DYNAMIC_COMPANY_NODE_KEY, "ACTION")], tree.operations)

    def test_open_img_activity_uses_press_button_for_observed_type_4(self):
        raw, tree = self._img_activity_raw()
        tree.GetItemType = lambda key, column: "4"

        def press_button(key, column):
            tree.operations.append(("PRESS_BUTTON", key, column))
            raw.Info.Program = "SAPLSVIM"

        tree.PressButton = press_button
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        self.assertEqual("SUCCESS", response["result"]["navigation_outcome"])
        self.assertEqual("PressButton", response["result"]["chosen_native_method"])

    def test_open_img_activity_refuses_type_2_as_primary_method(self):
        raw, tree = self._img_activity_raw()
        tree.GetItemType = lambda key, column: "2"
        tree.DoubleClickItem = lambda key, column: tree.operations.append(
            ("DOUBLE_CLICK_ITEM", key, column)
        )
        response = self.process(raw, "NAVIGATE", self._open_img_params(tree))
        self.assertEqual("ERROR", response["status"])
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertEqual([], tree.operations)

    def test_open_img_activity_protocol_requires_simg(self):
        raw, tree = self._img_activity_raw()
        params = self._open_img_params(tree)
        params["expected_transaction"] = "SPRO"
        with self.assertRaises(ProtocolError):
            self.request("NAVIGATE", params)

    def test_navigation_blocks_exact_control_mismatch(self):
        raw, button, _ = self.navigation_raw()
        params = self.navigation_params(button, "PRESS_SAFE_BUTTON")
        button.Id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[6]"
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertFalse(button.pressed)

    def test_navigation_blocks_text_mismatch(self):
        raw, button, _ = self.navigation_raw()
        params = self.navigation_params(
            button, "PRESS_SAFE_BUTTON", expected_text="Unexpected"
        )
        response = self.process(raw, "NAVIGATE", params)
        self.assertEqual("ActionBlockedError", response["error"]["type"])
        self.assertFalse(button.pressed)

    def test_navigation_blocks_write_related_text(self):
        for blocked_text in ("Save", "New Entries", "Change", "Delete"):
            with self.subTest(blocked_text=blocked_text):
                raw, button, _ = self.navigation_raw()
                button.Text = blocked_text
                params = self.navigation_params(
                    button, "PRESS_SAFE_BUTTON", expected_text=blocked_text
                )
                response = self.process(raw, "NAVIGATE", params)
                self.assertEqual("ActionBlockedError", response["error"]["type"])
                self.assertFalse(button.pressed)

    def test_navigation_protocol_blocks_set_text_and_send_vkey_zero(self):
        raw, button, _ = self.navigation_raw()
        for operation in ("SET_TEXT", "ENTER", "SEND_VKEY_0", "session.sendVKey(0)"):
            with self.subTest(operation=operation), self.assertRaises(ProtocolError):
                self.request(
                    "NAVIGATE",
                    self.navigation_params(button, operation),
                )

    def test_navigation_blocks_wrong_system_client_or_user(self):
        for field, value in (("system", "OTHER"), ("client", "100"), ("user", "OTHER")):
            with self.subTest(field=field):
                raw, button, _ = self.navigation_raw(**{field: value})
                params = self.navigation_params(button, "PRESS_SAFE_BUTTON")
                response = self.process(raw, "NAVIGATE", params)
                self.assertEqual("SessionNotFoundError", response["error"]["type"])
                self.assertFalse(button.pressed)

    def test_navigation_loop_inspect_navigate_inspect_responses(self):
        raw, button, tree = self.navigation_raw()
        before = self.process(raw, "INSPECT")
        self.assertEqual("SUCCESS", before["status"])
        self.assertEqual("Commercial", before["result"]["tree_controls"][0]["nodes"][1]["text"])

        params = self.navigation_params(
            tree,
            "SELECT_TREE_NODE",
            expected_text="Commercial",
            node_key="SALES",
        )
        navigated = self.process(raw, "NAVIGATE", params)
        self.assertEqual("SUCCESS", navigated["status"])

        after = self.process(raw, "INSPECT")
        self.assertEqual("SUCCESS", after["status"])
        self.assertEqual("SPRO", after["result"]["transaction"])

    def test_response_duplicate_is_rejected(self):
        request_id = str(uuid.uuid4())
        payload = {"request_id": request_id, "status": "ERROR", "sap": None, "result": None, "error": {"type": "X", "message": "x"}}
        write_response(payload)
        with self.assertRaises(DuplicateRequestError):
            write_response(payload)

    def test_request_cli_layer_does_not_import_live_connection(self):
        import src.sap_gui_bridge.protocol as protocol
        source = Path(protocol.__file__).read_text(encoding="utf-8")
        self.assertNotIn("SapGuiConnection", source)
        self.assertNotIn("win32com", source)


class RequestCliDispatchTests(unittest.TestCase):
    def assert_request_dispatch(self, argv, expected_action, expected_params):
        queued = {"request_id": str(uuid.uuid4()), "status": "QUEUED"}
        with patch(
            "src.sap_gui_bridge.__main__.enqueue_request", return_value=queued
        ) as mocked_enqueue, redirect_stdout(io.StringIO()):
            self.assertEqual(0, bridge_cli_main(argv))
        mocked_enqueue.assert_called_once_with(expected_action, expected_params)

    def test_request_status_dispatches_without_transaction(self):
        self.assert_request_dispatch(["request", "status"], "STATUS", {})

    def test_request_inspect_dispatches_without_transaction(self):
        self.assert_request_dispatch(["request", "inspect"], "INSPECT", {})

    def test_request_open_dispatches_with_transaction(self):
        self.assert_request_dispatch(
            ["request", "open", "SPRO"],
            "OPEN_TRANSACTION",
            {"transaction": "SPRO"},
        )

    def test_request_navigate_dispatches_exact_contract(self):
        self.assert_request_dispatch(
            [
                "request",
                "navigate",
                "--operation",
                "DOUBLE_CLICK_TREE_NODE",
                "--control-id",
                "/app/con[0]/ses[0]/wnd[0]/usr/tree",
                "--expected-type",
                "GuiTree",
                "--expected-text",
                "Commercial",
                "--node-key",
                "SALES",
            ],
            "NAVIGATE",
            {
                "control_id": "/app/con[0]/ses[0]/wnd[0]/usr/tree",
                "expected_type": "GuiTree",
                "expected_text": "Commercial",
                "navigation_operation": "DOUBLE_CLICK_TREE_NODE",
                "node_key": "SALES",
            },
        )

    def test_request_open_requires_transaction(self):
        with patch("src.sap_gui_bridge.__main__.enqueue_request") as mocked_enqueue:
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                bridge_cli_main(["request", "open"])
        self.assertEqual(2, raised.exception.code)
        mocked_enqueue.assert_not_called()

    def test_request_rejects_invalid_action(self):
        with patch("src.sap_gui_bridge.__main__.enqueue_request") as mocked_enqueue:
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                bridge_cli_main(["request", "invalid"])
        self.assertEqual(2, raised.exception.code)
        mocked_enqueue.assert_not_called()


class S4615BillingTypeActivityTests(unittest.TestCase):
    expected = {
        "source": "OPEN_IMG_ACTIVITY",
        "window_id": "/app/con[0]/ses[0]/wnd[1]",
        "transaction": "SIMG",
        "program": "SAPLDSYH",
        "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
        "row_text": "Définir types de documents de facturation pour les ventes",
        "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
        "button_text": "Sélectionner",
    }

    def test_protocol_accepts_only_observed_activity(self):
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "SELECT_S4615_BILLING_TYPE_ACTIVITY", "params": self.expected}
        self.assertEqual(self.expected, validate_request(request)["params"])
        request["params"] = {**self.expected, "row_text": "Contrôler options du Customizing pour types de document de facturation"}
        with self.assertRaises(ProtocolError):
            validate_request(request)

    def test_billing_type_lookup_accepts_only_exact_target(self):
        params = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "ZF01"}
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "FIND_S4615_BILLING_TYPE", "params": params}
        self.assertEqual(params, validate_request(request)["params"])
        request["params"] = {**params, "billing_type": "F2"}
        with self.assertRaises(ProtocolError):
            validate_request(request)

    def test_f2_display_rejects_other_reference(self):
        params = {"transaction": "VOFA", "program": "SAPL081F", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL081FTCTRL_V_TVFK", "billing_type": "F2", "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "DISPLAY_S4615_F2_REFERENCE", "params": params}
        self.assertEqual(params, validate_request(request)["params"])
        request["params"] = {**params, "billing_type": "ZF1"}
        with self.assertRaises(ProtocolError):
            validate_request(request)

    def test_za01_lookup_rejects_other_sales_type(self):
        params = {"transaction": "VOV8", "program": "SAPL080O", "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "sales_order_type": "ZA01"}
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "FIND_S4615_SALES_TYPE", "params": params}
        self.assertEqual(params, validate_request(request)["params"])
        request["params"] = {**params, "sales_order_type": "ZA02"}
        with self.assertRaises(ProtocolError):
            validate_request(request)

    def test_vov8_partial_scan_preserves_observed_reference_and_does_not_claim_absence(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK"
        params = {"transaction": "VOV8", "program": "SAPL080O", "table_id": table_id, "sales_order_type": "ZA01"}
        table = Mock(Type="GuiTableControl", RowCount=3, VisibleRowCount=3)
        table.VerticalScrollbar.Position = 0
        table.VerticalScrollbar.Maximum = 0
        session = Mock(identity={"transaction": "VOV8"})
        session.raw.Info.Program = "SAPL080O"
        def find(control_id):
            if control_id == table_id:
                return table
            if control_id.endswith("AUART[0,0]"):
                return Mock(Id=control_id, Type="GuiTextField", Text="OR")
            if control_id.endswith("BEZEI[1,0]"):
                return Mock(Id=control_id, Type="GuiTextField", Text="Commande standard")
            if control_id.endswith("AUART[0,1]"):
                return Mock(Id=control_id, Type="GuiCTextField", Text="CS")
            raise AssertionError(control_id)
        session.find.side_effect = find
        result = find_s4615_sales_type(session, params)["sales_type_search"]
        self.assertEqual("UNKNOWN", result["result"])
        self.assertEqual([{"sales_order_type": "OR", "description": "Commande standard", "row": 0}], result["related_types"])
        self.assertEqual(1, result["read_error"]["absolute_row"])

    def test_vov8_reference_display_allows_scoped_s4615_and_s4600_targets(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"
        params = {"transaction": "VOV8", "program": "SAPL080O", "table_id": table_id, "sales_order_type": "CS", "detail_button_id": button_id}
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "DISPLAY_S4615_SALES_REFERENCE", "params": params}
        self.assertEqual(params, validate_request(request)["params"])
        self.assertEqual("ZA01", validate_request({**request, "params": {**params, "sales_order_type": "ZA01"}})["params"]["sales_order_type"])
        SafetyPolicy(SafetyMode.READ, Mock()).authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ", "transaction": "VOV8"}, action="DISPLAY_S4615_SALES_REFERENCE")
        cdcl_params = {**params, "sales_order_type": "CDCL"}
        cdcl_request = {**request, "action": "DISPLAY_S4600_CDCL_REFERENCE", "params": cdcl_params}
        self.assertEqual(cdcl_params, validate_request(cdcl_request)["params"])
        SafetyPolicy(SafetyMode.READ, Mock()).authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ", "transaction": "VOV8"}, action="DISPLAY_S4600_CDCL_REFERENCE")
        with self.assertRaises(ProtocolError):
            validate_request({**request, "params": {**params, "sales_order_type": "OR"}})
        table = Mock(Type="GuiTableControl", RowCount=2, VisibleRowCount=2)
        table.VerticalScrollbar.Position = 0
        table.VerticalScrollbar.Maximum = 0
        prior_row = Mock(Selected=True)
        target_row = Mock(Selected=False)
        table.GetAbsoluteRow.side_effect = lambda index: [prior_row, target_row][index]
        button = Mock(Id=button_id, Type="GuiButton", Tooltip="Détail   (Ctrl+Maj+F2)")
        session = Mock(identity={"transaction": "VOV8"})
        session.raw.Info.Program = "SAPL080O"
        def find(control_id):
            if control_id == table_id:
                return table
            if control_id == f"{table_id}/txtV_TVAK-AUART[0,0]":
                return Mock(Id=control_id, Type="GuiTextField", Text="BV")
            if control_id == f"{table_id}/txtV_TVAK-AUART[0,1]":
                return Mock(Id=control_id, Type="GuiTextField", Text="CS")
            if control_id == button_id:
                return button
            raise AssertionError(control_id)
        session.find.side_effect = find
        detail = {"transaction": "VOV8", "program": "SAPL080O", "screen_number": "1011", "popups": [], "input_fields": [{"id": "/usr/txtV_TVAK-AUART", "text": "CS"}]}
        with patch("src.sap_gui_bridge.navigation._wait_for_screen", return_value=detail):
            result = display_s4615_sales_reference(session, params)
        self.assertEqual("CS", result["reference"])
        self.assertFalse(prior_row.Selected)
        self.assertTrue(target_row.Selected)
        button.press.assert_called_once_with()
        with patch("src.sap_gui_bridge.navigation._wait_for_screen", return_value={**detail, "input_fields": [{"id": "/usr/txtV_TVAK-AUART", "text": "BV"}]}):
            with self.assertRaisesRegex(ActionBlockedError, "did not open the selected"):
                display_s4615_sales_reference(session, params)

    def test_vov8_cdcl_complete_scan_can_confirm_absence(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"
        params = {"transaction": "VOV8", "program": "SAPL080O", "table_id": table_id,
                  "sales_order_type": "CDCL", "detail_button_id": button_id}
        table = Mock(Type="GuiTableControl", RowCount=1, VisibleRowCount=1)
        table.VerticalScrollbar.Position = 0
        table.VerticalScrollbar.Maximum = 0
        table.GetAbsoluteRow.return_value = Mock(Selected=False)
        session = Mock(identity={"transaction": "VOV8"})
        session.raw.Info.Program = "SAPL080O"
        def find(control_id):
            if control_id == table_id:
                return table
            if control_id.endswith("AUART[0,0]"):
                return Mock(Id=control_id, Type="GuiTextField", Text="OR")
            raise AssertionError(control_id)
        session.find.side_effect = find
        result = display_s4615_sales_reference(session, params)
        self.assertEqual("CONFIRMED_NOT_FOUND", result["result"])
        self.assertEqual(1, result["rows_read"])

    def test_selects_exact_row_and_button(self):
        table = Mock()
        button = Mock(Type="GuiButton", Text="Sélectionner")
        session = Mock()
        session.find.side_effect = [table, button]
        before = {
            "transaction": "SIMG", "program": "SAPLDSYH",
            "popups": [{
                "id": self.expected["window_id"], "window_title": "Sélection de l'activité :",
                "tables": [{"id": self.expected["table_id"], "type": "GuiTableControl", "visible_rows": [
                    {"index": 0, "values": [{"column": "1", "text": self.expected["row_text"]}]},
                    {"index": 1, "values": [{"column": "1", "text": "Contrôler options du Customizing pour types de document de facturation"}]},
                ]}],
                "buttons": [{"id": self.expected["button_id"], "type": "GuiButton", "text": "Sélectionner"}],
            }],
        }
        with patch("src.sap_gui_bridge.navigation.inspect_screen", return_value=before), patch("src.sap_gui_bridge.navigation._wait_for_screen", return_value={"popups": [], "transaction": "SIMG"}):
            result = select_s4615_billing_type_activity(session, self.expected)
        table.SelectRow.assert_called_once_with(0)
        button.press.assert_called_once_with()
        self.assertEqual("billing_type", result["activity_selection"]["target"])

    def test_wrong_or_ambiguous_row_is_blocked(self):
        session = Mock()
        before = {"transaction": "SIMG", "program": "SAPLDSYH", "popups": [{
            "id": self.expected["window_id"], "window_title": "Sélection de l'activité :",
            "tables": [{"id": self.expected["table_id"], "type": "GuiTableControl", "visible_rows": [
                {"index": 0, "values": [{"text": "Contrôler options du Customizing pour types de document de facturation"}]}
            ]}],
            "buttons": [{"id": self.expected["button_id"], "type": "GuiButton", "text": "Sélectionner"}],
        }]}
        with patch("src.sap_gui_bridge.navigation.inspect_screen", return_value=before):
            with self.assertRaises(ActionBlockedError):
                select_s4615_billing_type_activity(session, self.expected)
        session.find.assert_not_called()


if __name__ == "__main__":
    unittest.main()
