import json
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.provisioning.sap_gui_backend import (
    COMPANY_CODE_IMG_LINK_COLUMN,
    COMPANY_CODE_IMG_PARENT_PATH,
    COMPANY_CODE_IMG_ROOT_TEXT,
    COMPANY_CODE_IMG_TEXT_COLUMN,
    COMPANY_CODE_IMG_LEAF_TEXT,
    COMPANY_CODE_TRANSPORT_DESCRIPTION,
    COMPANY_CODE_TRANSPORT_POPUP_TITLE,
    COMPANY_CODE_TRANSPORT_REQUEST,
    COMPANY_CODE_SAVE_CONTROL,
    COMPANY_CODE_ADDRESS_CONTINUE,
    COMPANY_CODE_ADDRESS_COUNTRY,
    COMPANY_CODE_TARGET_FIELD,
    COMPANY_CODE_TARGET_SCREEN,
    COMPANY_CODE_VBS_CONTROLS,
    _complete_company_code_target_entry,
    _complete_company_code_address_and_save,
    _open_company_code_screen_from_vbs,
    _select_company_code_template_and_open_copy,
    execute_runner_action,
)
from src.sap_gui_bridge.errors import ActionBlockedError


ROOT = Path(__file__).resolve().parents[1]


class Control:
    def __init__(self, control_id, control_type="GuiButton", *, changeable=True, text="", children=None, on_press=None):
        self.Id = control_id
        self.Type = control_type
        self.Changeable = changeable
        self.Text = text
        self.Children = Collection(children or [])
        self.on_press = on_press
        self.presses = 0
        self.selected = 0
        self.keys = []

    def press(self):
        self.presses += 1
        if self.on_press:
            self.on_press()

    def select(self):
        self.selected += 1

    def sendVKey(self, key):
        self.keys.append(key)


class Collection:
    def __init__(self, values):
        self.values = values
        self.Count = len(values)

    def __call__(self, index):
        return self.values[index]


class Session:
    def __init__(self, *, system="A4H", client="600", user="ABDELJ", transport="missing"):
        self.identity = {
            "system": system,
            "client": client,
            "user": user,
            "transaction": "V_T001",
        }
        self.raw = SimpleNamespace(Busy=False)
        copy_button = Control(
            COMPANY_CODE_VBS_CONTROLS["copy_button"],
            "GuiButton",
        )
        copy_button.Tooltip = "Copier sous...   (F6)"
        self.controls = {
            "wnd[0]": Control("wnd[0]", "GuiMainWindow", changeable=False),
            COMPANY_CODE_VBS_CONTROLS["copy_menu"]: Control(
                COMPANY_CODE_VBS_CONTROLS["copy_menu"], "GuiMenu"
            ),
            COMPANY_CODE_VBS_CONTROLS["copy_button"]: copy_button,
            COMPANY_CODE_VBS_CONTROLS["copy_source"]: Control(
                COMPANY_CODE_VBS_CONTROLS["copy_source"], "GuiCTextField"
            ),
            COMPANY_CODE_VBS_CONTROLS["copy_target"]: Control(
                COMPANY_CODE_VBS_CONTROLS["copy_target"], "GuiCTextField"
            ),
            "wnd[1]": Control(
                "wnd[1]", "GuiModalWindow", changeable=False,
                text=COMPANY_CODE_TRANSPORT_POPUP_TITLE,
            ),
            COMPANY_CODE_VBS_CONTROLS["popup_no"]: Control(
                COMPANY_CODE_VBS_CONTROLS["popup_no"]
            ),
            COMPANY_CODE_VBS_CONTROLS["popup_ack"]: Control(
                COMPANY_CODE_VBS_CONTROLS["popup_ack"]
            ),
            COMPANY_CODE_VBS_CONTROLS["number_ranges_no"]: Control(
                COMPANY_CODE_VBS_CONTROLS["number_ranges_no"]
            ),
            COMPANY_CODE_VBS_CONTROLS["transport_cancel"]: Control(
                COMPANY_CODE_VBS_CONTROLS["transport_cancel"]
            ),
        }
        if transport in {"accepted", "rejected"}:
            field = Control(
                "wnd[1]/usr/ctxtTRANSPORT-ORDER",
                "GuiCTextField",
                changeable=True,
            )
            popup = Control(
                "wnd[1]", "GuiModalWindow", changeable=False,
                text=COMPANY_CODE_TRANSPORT_POPUP_TITLE, children=[field],
            )
            self.controls["wnd[1]"] = popup
            self.transport_field = field
            validate = self.controls[COMPANY_CODE_VBS_CONTROLS["popup_ack"]]
            if transport == "accepted":
                validate.on_press = lambda: (
                    self.controls.pop("wnd[1]", None)
                    if validate.presses >= 4 else None
                )
        self.audits = []

    def audit(self, action, **kwargs):
        if (
            self.identity["system"], self.identity["client"], self.identity["user"]
        ) != ("A4H", "600", "ABDELJ"):
            raise ActionBlockedError("identity mismatch")
        self.audits.append((action, kwargs))

    def find(self, control_id):
        try:
            return self.controls[control_id]
        except KeyError as exc:
            raise ActionBlockedError(f"missing control: {control_id}") from exc


def provision_request(operation="COMPANY_CODE_1010"):
    return {
        "params": {
            "operation": operation,
            "phase": "PROVISION",
            "target": {"company_code": "1010"},
            "values": {
                "technical_template": "BE01",
                "company_name": "S4615 Training Company",
                "currency": "EUR",
                "language": "EN",
                "chart_of_accounts": "INT",
            },
        }
    }


class CompanyCodeVbsBackendTests(unittest.TestCase):
    def test_address_continue_then_exact_save_and_transport_commit(self):
        session = Session()
        session.controls[COMPANY_CODE_ADDRESS_CONTINUE] = Control(
            COMPANY_CODE_ADDRESS_CONTINUE
        )
        session.controls[COMPANY_CODE_SAVE_CONTROL] = Control(
            COMPANY_CODE_SAVE_CONTROL
        )
        session.controls[COMPANY_CODE_ADDRESS_COUNTRY] = Control(
            COMPANY_CODE_ADDRESS_COUNTRY, "GuiCTextField", text=""
        )
        address = {
            "transaction": "V_T001",
            "program": "SAPLSZA1",
            "screen_number": "201",
            "window_title": 'Modifier vue "Société" : détail ensemble de sélection',
            "status_bar": {"message_type": "", "text": ""},
            "input_fields": [],
            "popups": [{
                "id": "/app/con[0]/ses[0]/wnd[1]",
                "window_title": "Traiter l'adresse:  1010",
                "buttons": [{
                    "id": COMPANY_CODE_ADDRESS_CONTINUE,
                    "type": "GuiButton",
                    "tooltip": "Reprendre   (Entrée)",
                    "changeable": True,
                    "visible": True,
                }],
                "input_fields": [{
                    "id": COMPANY_CODE_ADDRESS_COUNTRY,
                    "type": "GuiCTextField",
                    "text": "",
                    "changeable": True,
                    "visible": True,
                }],
            }],
        }
        address_with_country = {
            **address,
            "popups": [{
                **address["popups"][0],
                "input_fields": [{
                    "id": COMPANY_CODE_ADDRESS_COUNTRY,
                    "type": "GuiCTextField",
                    "text": "BE",
                    "changeable": True,
                    "visible": True,
                }],
            }],
        }
        overview = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "screen_number": "40",
            "window_title": 'Modifier vue "Société" : synthèse',
            "status_bar": {"message_type": "S", "text": ""},
            "input_fields": [],
            "popups": [],
            "buttons": [{
                "id": COMPANY_CODE_SAVE_CONTROL,
                "type": "GuiButton",
                "text": "Sauvegarder",
                "tooltip": "Sauvegarder   (Ctrl+S)",
                "changeable": True,
                "visible": True,
            }],
        }
        transport = {
            **overview,
            "popups": [{
                "id": "/app/con[0]/ses[0]/wnd[1]",
                "window_title": COMPANY_CODE_TRANSPORT_POPUP_TITLE,
            }],
        }
        committed = {
            **overview,
            "status_bar": {"message_type": "S", "text": "Données sauvegardées"},
        }
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[address, address_with_country, overview, transport, committed],
        ), patch(
            "src.provisioning.sap_gui_backend._reuse_company_code_transport",
            return_value={
                "accepted": True,
                "transport_request_id": "A4HK908422",
            },
        ):
            result = _complete_company_code_address_and_save(session)
        self.assertTrue(result["accepted"])
        self.assertEqual("A4HK908422", result["transport_request_id"])
        self.assertEqual("BE", session.controls[COMPANY_CODE_ADDRESS_COUNTRY].Text)
        self.assertEqual(1, session.controls[COMPANY_CODE_ADDRESS_CONTINUE].presses)
        self.assertEqual(1, session.controls[COMPANY_CODE_SAVE_CONTROL].presses)

    @staticmethod
    def _img_snapshot():
        def node(key, parent_key, text, *, link_type=None):
            items = [
                {"column": "TEXT", "text": text, "type": "2"},
            ]
            if link_type is not None:
                items.append(
                    {"column": "2", "text": None, "type": link_type}
                )
            return {
                "key": key,
                "parent_key": parent_key,
                "text": text,
                "items": items,
            }

        root = "01  1      1"
        structure = "02  1      6"
        definition = "03  2      1"
        accounting = "04  3      1"
        adv = "04  3      4"
        return {
            "transaction": "SIMG",
            "program": "SAPLSHI01",
            "window_title": "Afficher guide d'implémentation",
            "tree_controls": [
                {
                    "id": (
                        "/app/con[0]/ses[0]/"
                        + COMPANY_CODE_VBS_CONTROLS["img_tree"]
                    ),
                    "nodes_truncated": False,
                    "extraction_error": None,
                    "nodes": [
                        node(root, None, COMPANY_CODE_IMG_ROOT_TEXT),
                        node(structure, root, COMPANY_CODE_IMG_PARENT_PATH[0]),
                        node(definition, structure, COMPANY_CODE_IMG_PARENT_PATH[1]),
                        node(accounting, definition, COMPANY_CODE_IMG_PARENT_PATH[2]),
                        node(
                            "05  5      3",
                            accounting,
                            COMPANY_CODE_IMG_LEAF_TEXT,
                            link_type="5",
                        ),
                        node(adv, definition, "Administration des ventes (ADV)"),
                        node(
                            "05  4      3",
                            adv,
                            "Gérer agence commerciale",
                            link_type="5",
                        ),
                    ],
                }
            ],
        }

    @staticmethod
    def _activity_dialog_snapshot():
        popup_id = "/app/con[0]/ses[0]/wnd[1]"
        return {
            "transaction": "SIMG",
            "program": "SAPLDSYH",
            "popups": [
                {
                    "id": popup_id,
                    "window_title": "Sélection de l'activité :",
                    "controls": [
                        {"text": "Copier, supprimer, contrôler société"},
                        {"text": "Traiter données société"},
                    ],
                    "tables": [
                        {
                            "visible_rows": [
                                {
                                    "values": [
                                        {
                                            "column": "1",
                                            "text": "Copier, supprimer, contrôler société",
                                        }
                                    ]
                                },
                                {
                                    "values": [
                                        {
                                            "column": "1",
                                            "text": "Traiter données société",
                                        }
                                    ]
                                },
                            ]
                        }
                    ],
                }
            ],
        }

    def test_company_code_navigation_resolves_full_exact_img_path(self):
        events = []

        class Tree:
            def ExpandNode(self, node_key):
                events.append(("expand", node_key))

            @property
            def TopNode(self):
                return None

            @TopNode.setter
            def TopNode(self, node_key):
                events.append(("top", node_key))

            def SelectItem(self, node_key, column):
                events.append(("select", node_key, column))

            def EnsureVisibleHorizontalItem(self, node_key, column):
                events.append(("ensure", node_key, column))

            def DoubleClickItem(self, node_key, column):
                events.append(("double_click", node_key, column))

            def ClickLink(self, node_key, column):
                events.append(("click_link", node_key, column))

        class NavigationSession:
            identity = {"transaction": "SIMG"}
            raw = SimpleNamespace(Busy=False)

            def find(self, control_id):
                self.assert_control_id = control_id
                return tree

        session = NavigationSession()
        tree = Tree()
        img_snapshot = self._img_snapshot()
        inspect_results = [img_snapshot, self._activity_dialog_snapshot()]

        def select_activity(actual_session, params):
            self.assertEqual(session, actual_session)
            self.assertEqual("company_code", params["target"])
            events.append(("select_company_activity", params["row_text"]))
            actual_session.identity["transaction"] = "V_T001"

        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=inspect_results,
        ), patch(
            "src.provisioning.sap_gui_backend.select_company_code_display_activity",
            side_effect=select_activity,
        ):
            _open_company_code_screen_from_vbs(session)

        expected_keys = (
            "01  1      1",
            "02  1      6",
            "03  2      1",
            "04  3      1",
        )
        expected_events = [("top", expected_keys[0])]
        expected_events.extend(
            [
                ("select", "05  5      3", COMPANY_CODE_IMG_TEXT_COLUMN),
                ("ensure", "05  5      3", COMPANY_CODE_IMG_TEXT_COLUMN),
                ("double_click", "05  5      3", COMPANY_CODE_IMG_TEXT_COLUMN),
                ("select", "05  5      3", COMPANY_CODE_IMG_LINK_COLUMN),
                ("ensure", "05  5      3", COMPANY_CODE_IMG_LINK_COLUMN),
                ("click_link", "05  5      3", COMPANY_CODE_IMG_LINK_COLUMN),
                ("select_company_activity", "Traiter données société"),
            ]
        )
        self.assertEqual(
            COMPANY_CODE_VBS_CONTROLS["img_tree"],
            session.assert_control_id,
        )
        self.assertEqual(expected_events, events)

    def test_company_code_navigation_blocks_if_exact_leaf_is_on_wrong_path(self):
        tree_snapshot = self._img_snapshot()
        nodes = tree_snapshot["tree_controls"][0]["nodes"]
        company_leaf = next(
            node for node in nodes if node["text"] == COMPANY_CODE_IMG_LEAF_TEXT
        )
        company_leaf["parent_key"] = "04  3      4"
        tree_snapshot["tree_controls"][0]["nodes"] = [
            node
            for node in nodes
            if node["key"] != "04  3      1"
        ]

        class Tree:
            def ExpandNode(self, node_key):
                pass

            @property
            def TopNode(self):
                return None

            @TopNode.setter
            def TopNode(self, node_key):
                pass

        class NavigationSession:
            identity = {"transaction": "SIMG"}
            raw = SimpleNamespace(Busy=False)

            def find(self, control_id):
                return tree

        tree = Tree()
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            return_value=tree_snapshot,
        ), patch(
            "src.provisioning.sap_gui_backend.select_company_code_display_activity"
        ) as select_activity:
            with self.assertRaisesRegex(
                ActionBlockedError, "one exact child"
            ):
                _open_company_code_screen_from_vbs(NavigationSession())

        select_activity.assert_not_called()

    def test_company_code_navigation_stops_when_leaf_opens_vtbur(self):
        events = []

        class Tree:
            def ExpandNode(self, node_key):
                events.append(("expand", node_key))

            @property
            def TopNode(self):
                return None

            @TopNode.setter
            def TopNode(self, node_key):
                events.append(("top", node_key))

            def SelectItem(self, node_key, column):
                events.append(("select", node_key, column))

            def EnsureVisibleHorizontalItem(self, node_key, column):
                events.append(("ensure", node_key, column))

            def DoubleClickItem(self, node_key, column):
                events.append(("double_click", node_key, column))

            def ClickLink(self, node_key, column):
                events.append(("click_link", node_key, column))

        class NavigationSession:
            identity = {"transaction": "SIMG"}
            raw = SimpleNamespace(Busy=False)

            def find(self, control_id):
                return tree

        tree = Tree()
        wrong_screen = {
            "transaction": "SIMG",
            "program": "SAPL0ORG",
            "window_title": 'Modifier vue "Agences commerciales" : synthèse',
            "popups": [],
            "tables": [
                {
                    "id": (
                        "/app/con[0]/ses[0]/wnd[0]/usr/"
                        "tblSAPL0ORGTCTRL_V_TVBUR"
                    )
                }
            ],
        }
        inspect_results = [self._img_snapshot()] * 4 + [wrong_screen]
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=inspect_results,
        ), patch(
            "src.provisioning.sap_gui_backend.select_company_code_display_activity"
        ) as select_activity:
            with self.assertRaisesRegex(
                ActionBlockedError, "did not open the observed"
            ):
                _open_company_code_screen_from_vbs(NavigationSession())

        select_activity.assert_not_called()

    def test_all_automation_control_ids_are_recorded_or_captured_readback_fields(self):
        vbs = (ROOT / "runtime/captures/company_code_1010.vbs").read_text(
            encoding="utf-8"
        )
        recorded = set(re.findall(r'findById\("([^"]+)"\)', vbs))
        snapshot = json.loads(
            (ROOT / "runtime/sap_discovery/phase4c/snapshots/007_company_code.json")
            .read_text(encoding="utf-8")
        )
        captured_navigation = {
            button["id"].removeprefix("/app/con[0]/ses[0]/")
            for button in snapshot["buttons"]
            if button.get("text") == "Copier sous..."
            and button.get("type") == "GuiMenu"
        }
        captured_navigation.update(
            button["id"].removeprefix("/app/con[0]/ses[0]/")
            for button in snapshot["buttons"]
            if button.get("tooltip") == "Copier sous...   (F6)"
            and button.get("type") == "GuiButton"
        )
        captured_readback = {
            "wnd[0]/usr/txtV_T001-BUTXT",
            "wnd[0]/usr/ctxtV_T001-WAERS",
            "wnd[0]/usr/ctxtV_T001-SPRAS",
        }
        self.assertTrue(
            set(COMPANY_CODE_VBS_CONTROLS.values())
            <= recorded | captured_navigation | captured_readback
        )

    def test_copy_uses_exact_values_and_reuses_transport(self):
        session = Session(transport="accepted")
        with patch(
            "src.provisioning.sap_gui_backend._open_company_code_screen_from_vbs"
        ), patch(
            "src.provisioning.sap_gui_backend._lookup_company_code_1010",
            return_value={"state": "MISSING", "evidence": {}},
        ) as lookup, patch(
            "src.provisioning.sap_gui_backend._select_company_code_template_and_open_copy",
            return_value={
                "destination": "TARGET_ENTRY_SCREEN",
                "screen": {"screen_number": "41"},
                "target_entry_control": {
                    "id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T001-BUKRS",
                    "type": "GuiCTextField",
                    "text": "BE01",
                    "changeable": True,
                },
                "selected_source_row": 15,
            },
        ) as copy:
            with patch(
                "src.provisioning.sap_gui_backend._complete_company_code_target_entry",
                return_value={"accepted": True, "saved": True},
            ) as complete:
                result = execute_runner_action(session, provision_request())
        lookup.assert_called_once_with(session)
        copy.assert_called_once_with(session, phase="PROVISION")
        complete.assert_called_once_with(session)
        self.assertTrue(result["accepted"])
        self.assertEqual("", session.controls[COMPANY_CODE_VBS_CONTROLS["copy_source"]].Text)
        self.assertEqual("", session.controls[COMPANY_CODE_VBS_CONTROLS["copy_target"]].Text)

    def test_live_screen_41_changes_only_bukrs_and_uses_exact_save(self):
        session = Session()
        target = Control(COMPANY_CODE_TARGET_FIELD, "GuiCTextField", text="BE01")
        name_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_T001-BUTXT"
        name = Control(name_id, "GuiTextField", text="Template Company")
        save = Control(COMPANY_CODE_SAVE_CONTROL, "GuiButton")
        session.controls.update({
            COMPANY_CODE_TARGET_FIELD: target,
            name_id: name,
            COMPANY_CODE_SAVE_CONTROL: save,
        })
        base = {
            **COMPANY_CODE_TARGET_SCREEN,
            "popups": [],
            "buttons": [{
                "id": COMPANY_CODE_SAVE_CONTROL,
                "type": "GuiButton",
                "changeable": True,
            }],
            "status_bar": {"message_type": "S", "text": ""},
        }
        before = {
            **base,
            "input_fields": [
                {"id": COMPANY_CODE_TARGET_FIELD, "type": "GuiCTextField", "text": "BE01", "changeable": True, "visible": True},
                {"id": name_id, "type": "GuiTextField", "text": "Template Company", "changeable": True, "visible": True},
            ],
        }
        after_entry = {
            **base,
            "input_fields": [
                {"id": COMPANY_CODE_TARGET_FIELD, "type": "GuiCTextField", "text": "1010", "changeable": True, "visible": True},
                {"id": name_id, "type": "GuiTextField", "text": "Template Company", "changeable": True, "visible": True},
            ],
        }
        saved = {**after_entry, "buttons": [], "status_bar": {"message_type": "S", "text": "Saved"}}
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[before, after_entry, saved],
        ):
            result = _complete_company_code_target_entry(session)
        self.assertTrue(result["ambiguous_save"])
        self.assertEqual(1, result["post_confirm_state"]["active_window_count"])
        self.assertTrue(result["post_confirm_state"]["table_remains_in_edit_mode"])
        self.assertFalse(result["post_confirm_state"]["navigated_from_target_screen"])
        self.assertEqual("1010", target.Text)
        self.assertEqual("Template Company", name.Text)
        self.assertEqual([0], session.controls["wnd[0]"].keys)
        self.assertEqual(0, save.presses)

    @staticmethod
    def _copy_source_session(
        codes=("XCM1", "BE01", "YN01", "ZA01"),
        *,
        initially_selected=(),
        select_extra_row=None,
    ):
        class Row:
            def __init__(self, selected=False, on_select=None):
                self._selected = selected
                self.on_select = on_select

            @property
            def Selected(self):
                return self._selected

            @Selected.setter
            def Selected(self, value):
                self._selected = bool(value)
                if value and self.on_select:
                    self.on_select()

        class Scrollbar:
            def __init__(self, maximum):
                self.Maximum = maximum
                self._position = 0

            @property
            def Position(self):
                return self._position

            @Position.setter
            def Position(self, value):
                self._position = min(max(0, value), self.Maximum)

        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001"
        rows = [Row(index in initially_selected) for index in range(len(codes))]
        if select_extra_row is not None:
            rows[codes.index("BE01")].on_select = lambda: setattr(
                rows[select_extra_row], "Selected", True
            )
        table = SimpleNamespace(
            Id=table_id,
            Type="GuiTableControl",
            RowCount=len(codes),
            VisibleRowCount=len(codes),
            VerticalScrollbar=Scrollbar(0),
            GetAbsoluteRow=lambda index: rows[index],
        )
        prefix = table_id + "/ctxtV_T001-BUKRS[0,"
        cells = {
            f"{prefix}{index}]": SimpleNamespace(
                Id=f"{prefix}{index}]",
                Type="GuiCTextField",
                Text=code,
            )
            for index, code in enumerate(codes)
        }
        button = Control(COMPANY_CODE_VBS_CONTROLS["copy_button"], "GuiButton")
        button.Tooltip = "Copier sous...   (F6)"
        session = Session()
        session.controls.update(cells)
        session.controls[table_id] = table
        session.controls[COMPANY_CODE_VBS_CONTROLS["copy_button"]] = button
        session.copy_rows = rows
        session.copy_button = button
        session.copy_table_id = table_id
        session.copy_prefix = prefix
        return session

    @staticmethod
    def _copy_source_snapshots(session, *, popup=None):
        before = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "window_title": 'Modifier vue "Société" : synthèse',
            "tables": [{
                "id": session.copy_table_id,
                "type": "GuiTableControl",
            }],
            "buttons": [{
                "id": "/app/con[0]/ses[0]/" + COMPANY_CODE_VBS_CONTROLS["copy_button"],
                "type": "GuiButton",
                "tooltip": "Copier sous...   (F6)",
                "changeable": True,
            }],
            "popups": [],
        }
        after = {**before, "popups": [popup] if popup else []}
        return before, after

    def test_copy_to_screen_41_returns_target_control_without_editing(self):
        session = self._copy_source_session()
        before, _ = self._copy_source_snapshots(session)
        target_control = {
            "id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_T001-BUKRS",
            "type": "GuiCTextField",
            "text": "BE01",
            "tooltip": None,
            "visible": True,
            "changeable": True,
        }
        screen_41 = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "screen_number": "41",
            "window_title": 'Modifier vue "Société" : détail ensemble de sélection',
            "status_bar": {"message_type": "S", "text": "Indiquez les entrées cibles."},
            "input_fields": [
                target_control,
                {
                    "id": "/app/con[0]/ses[0]/wnd[0]/usr/txtV_T001-BUTXT",
                    "type": "GuiTextField",
                    "text": "Country Template BE",
                    "visible": True,
                    "changeable": True,
                },
            ],
            "popups": [],
        }
        session.copy_button.on_press = lambda: self.assertEqual(
            [False, True, False, False],
            [row.Selected for row in session.copy_rows],
        )
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[before, screen_41],
        ):
            result = _select_company_code_template_and_open_copy(
                session, phase="PROVISION"
            )
        self.assertEqual("TARGET_ENTRY_SCREEN", result["destination"])
        self.assertEqual(1, result["selected_source_row"])
        self.assertEqual(target_control, result["target_entry_control"])
        self.assertTrue(result["stopped_before_target_entry"])
        self.assertEqual(1, session.copy_button.presses)
        self.assertEqual("", session.controls[COMPANY_CODE_VBS_CONTROLS["copy_source"]].Text)
        self.assertEqual("", session.controls[COMPANY_CODE_VBS_CONTROLS["copy_target"]].Text)

    def test_be01_found_and_selected_before_copy(self):
        session = self._copy_source_session()
        popup = {
            "id": "/app/con[0]/ses[0]/wnd[1]",
            "window_title": "Company code copy",
            "controls": [],
            "control_ids": [],
            "buttons": [],
            "input_fields": [],
        }
        before, after = self._copy_source_snapshots(session, popup=popup)
        session.copy_button.on_press = lambda: self.assertEqual(
            [False, True, False, False],
            [row.Selected for row in session.copy_rows],
        )
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[before, after],
        ):
            result = _select_company_code_template_and_open_copy(
                session, phase="COPY_DIALOG_INSPECT"
            )
        self.assertEqual(1, result["selected_source_row"])
        self.assertEqual(1, session.copy_button.presses)
        self.assertEqual(
            [False, True, False, False],
            [row.Selected for row in session.copy_rows],
        )

    def test_missing_be01_fails_closed_without_copy(self):
        session = self._copy_source_session(codes=("XCM1", "YN01", "ZA01"))
        before, _ = self._copy_source_snapshots(session)
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            return_value=before,
        ), self.assertRaisesRegex(ActionBlockedError, "BE01 row is missing or ambiguous"):
            _select_company_code_template_and_open_copy(
                session, phase="COPY_DIALOG_INSPECT"
            )
        self.assertEqual(0, session.copy_button.presses)
        self.assertFalse(any(row.Selected for row in session.copy_rows))

    def test_preselected_rows_fail_closed_without_copy(self):
        session = self._copy_source_session(initially_selected=(0, 2))
        before, _ = self._copy_source_snapshots(session)
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            return_value=before,
        ), self.assertRaisesRegex(ActionBlockedError, "preselected rows"):
            _select_company_code_template_and_open_copy(
                session, phase="COPY_DIALOG_INSPECT"
            )
        self.assertEqual(0, session.copy_button.presses)

    def test_exact_preselected_be01_row_is_verified_before_copy(self):
        session = self._copy_source_session(initially_selected=(1,))
        popup = {
            "id": "/app/con[0]/ses[0]/wnd[1]",
            "window_title": "Company code copy",
            "controls": [],
            "control_ids": [],
            "buttons": [],
            "input_fields": [],
        }
        before, after = self._copy_source_snapshots(session, popup=popup)
        session.copy_button.on_press = lambda: self.assertEqual(
            [False, True, False, False],
            [row.Selected for row in session.copy_rows],
        )
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[before, after],
        ):
            result = _select_company_code_template_and_open_copy(
                session, phase="COPY_DIALOG_INSPECT"
            )
        self.assertEqual(1, result["selected_source_row"])
        self.assertEqual(1, session.copy_button.presses)

    def test_unintended_multiple_selection_fails_before_copy(self):
        session = self._copy_source_session(select_extra_row=2)
        before, _ = self._copy_source_snapshots(session)
        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            return_value=before,
        ), self.assertRaisesRegex(ActionBlockedError, "selection verification failed"):
            _select_company_code_template_and_open_copy(
                session, phase="COPY_DIALOG_INSPECT"
            )
        self.assertEqual(0, session.copy_button.presses)

    def test_copy_dialog_inspection_requires_live_copy_button_contract(self):
        class DiagnosticSession:
            identity = {
                "system": "A4H",
                "client": "600",
                "user": "ABDELJ",
                "transaction": "V_T001",
            }
            raw = SimpleNamespace(
                Busy=False,
                Info=SimpleNamespace(Program="SAPL0ORG"),
            )

            def __init__(self):
                self.requested_controls = []

            def audit(self, action, **kwargs):
                pass

            def find(self, control_id):
                self.requested_controls.append(control_id)
                raise AssertionError("Must not click an unverified copy control")

        request = {
            "params": {
                "operation": "COMPANY_CODE_1010",
                "phase": "COPY_DIALOG_INSPECT",
                "target": {"company_code": "1010"},
                "values": {},
            }
        }
        session = DiagnosticSession()
        wrong_action = {
            "transaction": "V_T001",
            "program": "SAPL0ORG",
            "buttons": [],
            "popups": [],
        }
        with patch(
            "src.provisioning.sap_gui_backend._lookup_company_code_1010",
            return_value={"state": "MISSING", "evidence": {}},
        ) as lookup, patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            return_value=wrong_action,
        ) as inspect:
            with self.assertRaisesRegex(
                ActionBlockedError,
                "Company-code template copy requires",
            ):
                execute_runner_action(session, request)

        lookup.assert_called_once_with(session)
        inspect.assert_called_once_with(session)
        self.assertEqual(
            [],
            session.requested_controls,
        )

    def test_copy_dialog_inspection_requires_missing_lookup(self):
        class DiagnosticSession:
            identity = {"transaction": "V_T001"}
            raw = SimpleNamespace(Info=SimpleNamespace(Program="SAPL0ORG"))

            def audit(self, action, **kwargs):
                pass

            def find(self, control_id):
                raise AssertionError("Copy menu must not open when LOOKUP exists")

        request = {
            "params": {
                "operation": "COMPANY_CODE_1010",
                "phase": "COPY_DIALOG_INSPECT",
                "target": {"company_code": "1010"},
                "values": {},
            }
        }
        with patch(
            "src.provisioning.sap_gui_backend._lookup_company_code_1010",
            return_value={"state": "EXISTS", "evidence": {}},
        ):
            with self.assertRaisesRegex(ActionBlockedError, "live MISSING lookup"):
                execute_runner_action(DiagnosticSession(), request)

    def test_non_recorded_operation_is_blocked(self):
        with self.assertRaises(ActionBlockedError):
            execute_runner_action(Session(), provision_request("UNALLOWLISTED_OPERATION"))

    def test_wrong_identity_is_blocked(self):
        with self.assertRaises(ActionBlockedError):
            execute_runner_action(Session(client="500"), provision_request())


if __name__ == "__main__":
    unittest.main()
