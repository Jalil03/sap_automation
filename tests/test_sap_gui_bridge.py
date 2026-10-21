import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.__main__ import parser as cli_parser
from src.sap_gui_bridge.errors import ActionBlockedError, SessionNotFoundError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import (
    display_s4650_billing_copy_header,
    find_s4650_billing_copy_header,
    open_transaction,
    press_safe_button,
    set_text,
)
from src.sap_gui_bridge.protocol import validate_request
from src.sap_gui_bridge.runner import execute_read_action
from src.sap_gui_bridge.safety import AuditLogger, SafetyMode, SafetyPolicy


class Collection:
    def __init__(self, values):
        self.values = values
        self.Count = len(values)

    def __call__(self, index):
        return self.values[index]


class Control:
    def __init__(self, control_id, control_type, text="", children=None, tooltip="", changeable=False):
        self.Id = control_id
        self.Type = control_type
        self.Text = text
        self.Tooltip = tooltip
        self.Changeable = changeable
        self.Visible = True
        self.Children = Collection(children or [])
        self.pressed = False
        self.selected = False

    def press(self):
        self.pressed = True

    def select(self):
        self.selected = True

    def sendVKey(self, key):
        self.last_key = key


class RawSession:
    def __init__(self, system="A4H", client="600", user="ABDELJ", transaction="RZ11"):
        self.Info = SimpleNamespace(SystemName=system, Client=client, User=user, Transaction=transaction)
        label = Control("wnd[0]/usr/lblTITLE", "GuiLabel", "Structure organisationnelle")
        field = Control("wnd[0]/usr/ctxtBUKRS", "GuiCTextField", "1010", changeable=True)
        button = Control("wnd[0]/usr/btnDISPLAY", "GuiButton", "Afficher")
        password = Control("wnd[0]/usr/pwdSECRET", "GuiPasswordField", "must-not-leak")
        self.root = Control("wnd[0]", "GuiMainWindow", "SAP Easy Access", [label, field, button, password])
        self.status = SimpleNamespace(Text="Ready", MessageType="S")
        self.controls = {item.Id: item for item in [self.root, label, field, button, password]}
        self.controls["wnd[0]/sbar"] = self.status

    def findById(self, control_id):
        return self.controls[control_id]

    def StartTransaction(self, Transaction):
        self.Info.Transaction = Transaction


def sap_gui(raw_sessions):
    connection = SimpleNamespace(Children=Collection(raw_sessions))
    engine = SimpleNamespace(Children=Collection([connection]))
    return SimpleNamespace(GetScriptingEngine=engine)


class SapGuiBridgeTests(unittest.TestCase):
    def test_s4615_vtflc_new_item_form_requires_exact_parent_and_no_save(self):
        payload = {"request_id": str(uuid.uuid4()), "mode": "READ",
                   "action": "INSPECT_S4615_VTFLC_NEW_ITEM_FORM", "params": {}}
        self.assertEqual({}, validate_request(payload)["params"])
        with self.assertRaises(Exception):
            validate_request({**payload, "mode": "EXECUTE"})
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        button_id = prefix + "/tbar[1]/btn[5]"
        table_id = prefix + "/usr/tblSAPL080WTCTRL_V_TVCPFLP"
        button = Control(button_id, "GuiButton", tooltip="Nouvelles entrées   (F5)")
        billing = Control(prefix + "/usr/ctxtV_TVCPFLP-FKARN", "GuiCTextField", "F2")
        delivery = Control(prefix + "/usr/ctxtV_TVCPFLP-LFARV", "GuiCTextField", "LF")
        controls = {button_id: button, billing.Id: billing, delivery.Id: delivery}
        session = SimpleNamespace(validate_identity=lambda: None,
                                  find=lambda control_id: controls[control_id],
                                  audit=lambda *args, **kwargs: None)
        before = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "112",
                  "popups": [], "tables": [{"id": table_id, "type": "GuiTableControl"}]}
        after = {"transaction": "VTFLC", "program": "SAPL080W", "popups": [], "screen_number": "113",
                 "input_fields": [{"id": billing.Id, "text": "F2"},
                                  {"id": delivery.Id, "text": "LF"}]}
        with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
            self.assertEqual(after, execute_read_action(session, payload))
        self.assertTrue(button.pressed)
        button.pressed = False
        delivery.Text = "ZLF"
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=before):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, payload)
        self.assertFalse(button.pressed)

    def test_s4615_new_target_item_form_accepts_only_observed_zf01_parent(self):
        payload = {"request_id": str(uuid.uuid4()), "mode": "READ",
                   "action": "INSPECT_S4615_VTFLC_NEW_TARGET_ITEM_FORM", "params": {}}
        self.assertEqual({}, validate_request(payload)["params"])
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        button_id = prefix + "/tbar[1]/btn[5]"
        table_id = prefix + "/usr/tblSAPL080WTCTRL_V_TVCPFLP"
        button = Control(button_id, "GuiButton", tooltip="Nouvelles entrÃ©es   (F5)")
        billing = Control(prefix + "/usr/ctxtV_TVCPFLP-FKARN", "GuiCTextField", "ZF01")
        delivery = Control(prefix + "/usr/ctxtV_TVCPFLP-LFARV", "GuiCTextField", "LF")
        controls = {button_id: button, billing.Id: billing, delivery.Id: delivery}
        session = SimpleNamespace(validate_identity=lambda: None, find=lambda cid: controls[cid],
                                  audit=lambda *args, **kwargs: None)
        before = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "112",
                  "popups": [], "tables": [{"id": table_id, "type": "GuiTableControl"}]}
        after = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "113",
                 "popups": [], "input_fields": [{"id": billing.Id, "text": "ZF01"},
                                               {"id": delivery.Id, "text": "LF"}]}
        with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
            self.assertEqual(after, execute_read_action(session, payload))
        self.assertTrue(button.pressed)

    def test_s4615_f2_lf_header_options_are_read_only_and_exact(self):
        payload = {"request_id": str(uuid.uuid4()), "mode": "READ",
                   "action": "READ_S4615_F2_LF_HEADER_OPTIONS", "params": {}}
        self.assertEqual({}, validate_request(payload)["params"])
        with self.assertRaises(Exception):
            validate_request({**payload, "mode": "EXECUTE"})
        self.assertEqual("read-f2-lf-header-options",
                         cli_parser().parse_args(["request", "read-f2-lf-header-options"]).request_action)
        prefix = "/app/con[0]/ses[0]/wnd[0]/usr/"
        controls = {
            prefix + "ctxtV_TVCPFLK-FKARN": Control(prefix + "ctxtV_TVCPFLK-FKARN", "GuiCTextField", "F2"),
            prefix + "ctxtV_TVCPFLK-LFARV": Control(prefix + "ctxtV_TVCPFLK-LFARV", "GuiCTextField", "LF"),
            prefix + "ctxtV_TVCPFLK-GRBED": Control(prefix + "ctxtV_TVCPFLK-GRBED", "GuiCTextField", "003"),
            prefix + "txtTEXT_BEDI": Control(prefix + "txtTEXT_BEDI", "GuiTextField", "Header/delivery-related"),
            prefix + "chkV_TVCPFLK-POSVO": Control(prefix + "chkV_TVCPFLK-POSVO", "GuiCheckBox", "Copy item number"),
        }
        controls[prefix + "chkV_TVCPFLK-POSVO"].Selected = False
        session = SimpleNamespace(validate_identity=lambda: None,
                                  find=lambda control_id: controls[control_id],
                                  audit=lambda *args, **kwargs: None)
        snapshot = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "111", "popups": []}
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
            result = execute_read_action(session, payload)
        self.assertEqual("003", result["copy_requirement"])
        self.assertFalse(result["copy_item_number"])
        self.assertFalse(any(control.pressed or control.selected for control in controls.values()))
        controls[prefix + "ctxtV_TVCPFLK-FKARN"].Text = "ZF01"
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, payload)

    def test_s4615_vtflc_new_header_form_protocol_and_read_only_gate(self):
        self.assertEqual("inspect-zf01-lf-new-header-form",
                         cli_parser().parse_args(["request", "inspect-zf01-lf-new-header-form"]).request_action)
        payload = {"request_id": str(uuid.uuid4()), "mode": "READ",
                   "action": "INSPECT_S4615_VTFLC_NEW_HEADER_FORM", "params": {}}
        self.assertEqual({}, validate_request(payload)["params"])
        with self.assertRaises(Exception):
            validate_request({**payload, "params": {"billing_type": "F2"}})
        with self.assertRaises(Exception):
            validate_request({**payload, "mode": "EXECUTE"})

    def test_s4615_vtflc_new_header_form_only_presses_exact_button(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"
        before = {"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "110",
                  "popups": [], "tables": [{"id": table_id, "type": "GuiTableControl"}]}
        after = {"transaction": "VTFLC", "popups": [], "screen_number": "100"}
        for tooltip, should_press in (("Nouvelles entrées   (F5)", True),
                                      ("Sauvegarder   (Ctrl+S)", False)):
            with self.subTest(tooltip=tooltip):
                button = Control(button_id, "GuiButton", tooltip=tooltip)
                events = []
                session = SimpleNamespace(validate_identity=lambda: None,
                                          find=lambda control_id: button if control_id == button_id else None,
                                          audit=lambda *args, **kwargs: events.append((args, kwargs)))
                with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
                    if should_press:
                        result = execute_read_action(session, {"action": "INSPECT_S4615_VTFLC_NEW_HEADER_FORM", "params": {}})
                        self.assertEqual(after, result)
                    else:
                        with self.assertRaises(ActionBlockedError):
                            execute_read_action(session, {"action": "INSPECT_S4615_VTFLC_NEW_HEADER_FORM", "params": {}})
                self.assertEqual(should_press, button.pressed)
                self.assertEqual(int(should_press), len(events))

    def test_s4615_vtflc_new_header_form_blocks_wrong_screen(self):
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]"
        button = Control(button_id, "GuiButton", tooltip="Nouvelles entrées   (F5)")
        session = SimpleNamespace(validate_identity=lambda: None,
                                  find=lambda control_id: button, audit=lambda *args, **kwargs: None)
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value={"transaction": "VTFLC", "program": "SAPL080W", "screen_number": "111", "popups": [], "tables": []}):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, {"action": "INSPECT_S4615_VTFLC_NEW_HEADER_FORM", "params": {}})
        self.assertFalse(button.pressed)

    def test_s4615_zf01_lf_copy_header_protocol_is_exact(self):
        for command in ("read-zf01-accounting-block", "find-zf01-lf-copy-header",
                        "display-zf01-lf-copy-header", "open-billing-copy-items",
                        "display-billing-copy-tan"):
            self.assertEqual(command, cli_parser().parse_args(["request", command]).request_action)
        params = {"transaction": "VTFLC", "program": "SAPL080W",
                  "table_id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK",
                  "billing_type": "ZF01", "delivery_type": "LF"}
        request = validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                                    "action": "FIND_S4615_ZF01_LF_COPY_HEADER", "params": params})
        self.assertEqual(params, request["params"])
        with self.assertRaises(Exception):
            validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                              "action": "FIND_S4615_ZF01_LF_COPY_HEADER",
                              "params": {**params, "billing_type": "F2"}})
        detail = {**params, "detail_button_id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"}
        self.assertEqual(detail, validate_request({"request_id": str(uuid.uuid4()),
                         "mode": "READ", "action": "DISPLAY_S4615_ZF01_LF_COPY_HEADER",
                         "params": detail})["params"])

    def test_s4615_zf01_lf_copy_header_finds_exact_row_only(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK"
        params = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": table_id,
                  "billing_type": "ZF01", "delivery_type": "LF"}
        scrollbar = SimpleNamespace(Position=0, Maximum=0)
        table = SimpleNamespace(Type="GuiTableControl", RowCount=2, VisibleRowCount=2,
                                VerticalScrollbar=scrollbar)
        cells = {}
        for index, pair in enumerate((("F2", "LF"), ("ZF01", "LF"))):
            for column, field, value in ((0, "FKARN", pair[0]), (2, "LFARV", pair[1])):
                control_id = f"{table_id}/ctxtV_TVCPFLK-{field}[{column},{index}]"
                cells[control_id] = SimpleNamespace(Id=control_id, Type="GuiCTextField", Text=value)
        session = SimpleNamespace(identity={"transaction": "VTFLC"},
                                  raw=SimpleNamespace(Info=SimpleNamespace(Program="SAPL080W")),
                                  validate_identity=lambda: None,
                                  find=lambda control_id: table if control_id == table_id else cells[control_id],
                                  audit=lambda *args, **kwargs: None)
        result = find_s4650_billing_copy_header(session, params)
        self.assertEqual("FOUND", result["billing_copy_header_search"]["result"])
        self.assertEqual(1, result["billing_copy_header_search"]["found_row"])
        with self.assertRaises(ActionBlockedError):
            find_s4650_billing_copy_header(session, {**params, "delivery_type": "XX"})

    def test_s4615_zf01_lf_copy_header_detail_is_navigation_only(self):
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080WTCTRL_V_TVCPFLK"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[38]"
        params = {"transaction": "VTFLC", "program": "SAPL080W", "table_id": table_id,
                  "billing_type": "ZF01", "delivery_type": "LF", "detail_button_id": button_id}
        row = SimpleNamespace(Selected=False)
        table = SimpleNamespace(Type="GuiTableControl", VisibleRowCount=1,
                                VerticalScrollbar=SimpleNamespace(Position=0),
                                GetAbsoluteRow=lambda index: row)
        cells = {}
        for column, field, value in ((0, "FKARN", "ZF01"), (2, "LFARV", "LF")):
            control_id = f"{table_id}/ctxtV_TVCPFLK-{field}[{column},0]"
            cells[control_id] = SimpleNamespace(Id=control_id, Type="GuiCTextField", Text=value)
        button = Control(button_id, "GuiButton", tooltip="Détail   (Ctrl+Maj+F2)")
        session = SimpleNamespace(identity={"transaction": "VTFLC"},
                                  raw=SimpleNamespace(Info=SimpleNamespace(Program="SAPL080W")),
                                  validate_identity=lambda: None,
                                  find=lambda control_id: table if control_id == table_id else button if control_id == button_id else cells[control_id],
                                  audit=lambda *args, **kwargs: None)
        with patch("src.sap_gui_bridge.navigation._wait_for_screen", return_value={"popups": []}):
            result = display_s4650_billing_copy_header(session, params)
        self.assertEqual([], result["popups"])
        self.assertTrue(row.Selected)
        self.assertTrue(button.pressed)

    def test_s4615_copy_control_transaction_is_read_only(self):
        request = validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                                    "action": "OPEN_TRANSACTION", "params": {"transaction": "VTFLC"}})
        self.assertEqual("VTFLC", request["params"]["transaction"])
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))
            with self.assertRaises(ActionBlockedError):
                policy.authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                                 action="OPEN_TRANSACTION", value="VTFLC")

    def test_zf01_accounting_block_reads_selected_without_mutation(self):
        field_id = "/app/con[0]/ses[0]/wnd[0]/usr/chkV_TVFK-RFBFK"
        header_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART"
        for state in (False, True):
            with self.subTest(state=state):
                header = SimpleNamespace(Id=header_id, Text="ZF01")
                field = SimpleNamespace(Id=field_id, Type="GuiCheckBox",
                                        Text="Blocage comptabil.", Selected=state)
                events = []
                session = SimpleNamespace(validate_identity=lambda: None,
                                          find=lambda control_id: {header_id: header, field_id: field}[control_id],
                                          audit=lambda *args, **kwargs: events.append((args, kwargs)))
                snapshot = {"transaction": "VOFA", "program": "SAPL081F",
                            "screen_number": "101", "popups": []}
                with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
                    result = execute_read_action(session, {"action": "READ_S4615_ZF01_ACCOUNTING_BLOCK", "params": {}})
                self.assertEqual(state, result["selected"])
                self.assertEqual(state, field.Selected)
                self.assertEqual(1, len(events))

    def test_zf01_accounting_block_fails_closed_on_mismatch(self):
        field_id = "/app/con[0]/ses[0]/wnd[0]/usr/chkV_TVFK-RFBFK"
        header_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART"
        header = SimpleNamespace(Id=header_id, Text="F2")
        field = SimpleNamespace(Id=field_id, Type="GuiCheckBox",
                                Text="Blocage comptabil.", Selected=True)
        session = SimpleNamespace(validate_identity=lambda: None,
                                  find=lambda control_id: {header_id: header, field_id: field}[control_id],
                                  audit=lambda *args, **kwargs: self.fail("must not audit a mismatched read"))
        snapshot = {"transaction": "VOFA", "program": "SAPL081F",
                    "screen_number": "101", "popups": []}
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, {"action": "READ_S4615_ZF01_ACCOUNTING_BLOCK", "params": {}})

    def test_change_log_query_is_read_only_and_narrow(self):
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "READ_PHASE5_CHANGE_LOG", "params": {"table": "FINSC_001A", "date": "16.10.2026"}}
        self.assertEqual("FINSC_001A", validate_request(request)["params"]["table"])
        request["params"] = {"table": "T000", "date": "14.10.2026"}
        self.assertEqual("T000", validate_request(request)["params"]["table"])
        request["params"] = {"table": "T001", "date": "14.10.2026"}
        with self.assertRaises(Exception):
            validate_request(request)
        request["mode"] = "EXECUTE"
        with self.assertRaises(Exception):
            validate_request(request)

    def test_transport_overview_read_is_not_executable(self):
        request = {"request_id": str(uuid.uuid4()), "mode": "READ", "action": "READ_PHASE5_TRANSPORT_OVERVIEW", "params": {}}
        self.assertEqual({}, validate_request(request)["params"])
        request["mode"] = "EXECUTE"
        with self.assertRaises(Exception):
            validate_request(request)

    def attach(self, raw=None, mode=SafetyMode.READ):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / "audit.jsonl"
        raw = raw or RawSession()
        return SapGuiConnection(mode=mode, get_object=lambda _: sap_gui([raw]), log_path=path).attach(), path

    def test_attach_status_and_expected_identity(self):
        session, _ = self.attach()
        self.assertEqual(
            {"system": "A4H", "client": "600", "user": "ABDELJ", "transaction": "RZ11", "connections": 1, "sessions": 1, "mode": "READ"},
            session.status(),
        )

    def test_default_attach_contract_never_opens_a_connection(self):
        # The injected callable is invoked only for the active SAPGUI object;
        # no OpenConnection/Dispatch method is part of the bridge contract.
        calls = []
        raw = RawSession()
        bridge = SapGuiConnection(get_object=lambda name: calls.append(name) or sap_gui([raw]))
        bridge.attach()
        self.assertEqual(["SAPGUI"], calls)

    def test_bridge_surface_has_no_open_connection_method(self):
        import src.sap_gui_bridge.connection as connection
        source = Path(connection.__file__).read_text(encoding="utf-8")
        self.assertNotIn(".OpenConnection(", source)
        self.assertNotIn("Dispatch(", source)

    def test_wrong_identity_fails_closed(self):
        with self.assertRaises(SessionNotFoundError):
            self.attach(RawSession(system="OTHER"))

    def test_ambiguous_matching_sessions_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            bridge = SapGuiConnection(get_object=lambda _: sap_gui([RawSession(), RawSession()]), log_path=Path(tmp) / "a.jsonl")
            with self.assertRaises(SessionNotFoundError):
                bridge.attach()

    def test_execute_allows_only_phase5_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))
            with self.assertRaises(ActionBlockedError):
                policy.authorize(
                    identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                    action="SAVE",
                )

    def test_execute_allows_exact_sales_org_lookup_route_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))
            identity = {"system": "A4H", "client": "600", "user": "ABDELJ"}
            route_actions = (
                ("PHASE5_OPERATION", None),
                ("OPEN_TRANSACTION", "SPRO"),
                ("NAVIGATE", {"operation": "EXPAND_TREE_NODE"}),
                ("NAVIGATE", {"operation": "OPEN_IMG_ACTIVITY"}),
                ("SELECT_SALES_ORGANIZATION_ACTIVITY", None),
                ("SELECT_COMPANY_CODE_COPY_SOURCE", None),
                ("FIND_TABLE_VALUE", None),
            )

            for action, value in route_actions:
                with self.subTest(action=action, value=value):
                    policy.authorize(identity=identity, action=action, value=value)

    def test_execute_open_transaction_is_restricted_to_spro_and_vov4(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))

            for transaction in ("SPRO", "VOV4"):
                policy.authorize(
                    identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                    action="OPEN_TRANSACTION",
                    value=transaction,
                )

            with self.assertRaisesRegex(ActionBlockedError, "only for SPRO"):
                policy.authorize(
                    identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                    action="OPEN_TRANSACTION",
                    value="VA01",
                )

    def test_mm01_navigation_is_read_only(self):
        request = validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                                    "action": "OPEN_TRANSACTION", "params": {"transaction": "MM01"}})
        self.assertEqual("MM01", request["params"]["transaction"])
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "audit.jsonl"))
            with self.assertRaises(ActionBlockedError):
                policy.authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                                 action="OPEN_TRANSACTION", value="MM01")

    def test_execute_keeps_unrelated_write_actions_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))

            for action in ("SET_TEXT", "SAVE", "DELETE", "RELEASE"):
                with self.subTest(action=action):
                    with self.assertRaises(ActionBlockedError):
                        policy.authorize(
                            identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                            action=action,
                        )

    def test_read_mode_cannot_set_text(self):
        session, _ = self.attach()
        with self.assertRaises(ActionBlockedError):
            set_text(session, "wnd[0]/usr/ctxtBUKRS", "2000")

    def test_prepare_sets_text_without_save(self):
        session, _ = self.attach(mode=SafetyMode.PREPARE)
        set_text(session, "wnd[0]/usr/ctxtBUKRS", "1010")
        self.assertEqual("1010", session.find("wnd[0]/usr/ctxtBUKRS").Text)

    def test_save_control_and_save_text_are_blocked(self):
        session, _ = self.attach(mode=SafetyMode.PREPARE)
        session.raw.controls["wnd[0]/tbar[0]/btn[11]"] = Control("wnd[0]/tbar[0]/btn[11]", "GuiButton", "Save")
        with self.assertRaises(ActionBlockedError):
            press_safe_button(session, "wnd[0]/tbar[0]/btn[11]")
        session.raw.controls["wnd[0]/usr/btnSAVE"] = Control("wnd[0]/usr/btnSAVE", "GuiButton", "Enregistrer")
        with self.assertRaises(ActionBlockedError):
            press_safe_button(session, "wnd[0]/usr/btnSAVE")

    def test_inspection_is_structured_and_redacts_password(self):
        session, _ = self.attach()
        snapshot = inspect_screen(session)
        self.assertEqual("SAP Easy Access", snapshot["window_title"])
        self.assertEqual("RZ11", snapshot["transaction"])
        secret = next(row for row in snapshot["input_fields"] if row["type"] == "GuiPasswordField")
        self.assertIsNone(secret["text"])
        self.assertIn("wnd[0]/usr/btnDISPLAY", snapshot["control_ids"])

    def test_open_transaction_is_allowlisted_and_logged(self):
        session, path = self.attach()
        open_transaction(session, "SPRO")
        self.assertEqual("SPRO", session.identity["transaction"])
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual("OPEN_TRANSACTION", events[-1]["action"])
        self.assertNotIn("password", path.read_text(encoding="utf-8").lower())

    def test_gateway_error_log_open_is_read_only_only(self):
        request = validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                                    "action": "OPEN_TRANSACTION",
                                    "params": {"transaction": "/IWFND/ERROR_LOG"}})
        self.assertEqual("/IWFND/ERROR_LOG", request["params"]["transaction"])
        with tempfile.TemporaryDirectory() as tmp:
            policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))
            with self.assertRaises(ActionBlockedError):
                policy.authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                                 action="OPEN_TRANSACTION", value="/IWFND/ERROR_LOG")

    def test_change_audit_transactions_are_read_only_only(self):
        for transaction in ("SCU3", "SE09"):
            request = validate_request({"request_id": str(uuid.uuid4()), "mode": "READ",
                                        "action": "OPEN_TRANSACTION", "params": {"transaction": transaction}})
            self.assertEqual(transaction, request["params"]["transaction"])
            with tempfile.TemporaryDirectory() as tmp:
                policy = SafetyPolicy(SafetyMode.EXECUTE, AuditLogger(Path(tmp) / "a.jsonl"))
                with self.assertRaises(ActionBlockedError):
                    policy.authorize(identity={"system": "A4H", "client": "600", "user": "ABDELJ"},
                                     action="OPEN_TRANSACTION", value=transaction)

    def test_unknown_action_and_ctrl_s_are_blocked(self):
        session, _ = self.attach(mode=SafetyMode.PREPARE)
        with self.assertRaises(ActionBlockedError):
            session.policy.authorize(identity=session.identity, action="SAVE")
        with self.assertRaises(ActionBlockedError):
            session.policy.authorize(identity=session.identity, action="PRESS_SAFE_BUTTON", key_chord="Ctrl+S")

    def test_s4615_customizing_read_protocol_is_narrow(self):
        def request(action, params, mode="READ"):
            return validate_request({"request_id": str(uuid.uuid4()), "mode": mode, "action": action, "params": params})

        self.assertEqual("SE16N", request("OPEN_S4615_CUSTOMIZING_READ", {"transaction": "SE16N"})["params"]["transaction"])
        self.assertEqual("OVXD", request("OPEN_S4615_CUSTOMIZING_READ", {"transaction": "OVXD"})["params"]["transaction"])
        self.assertEqual("T001W", request("INSPECT_S4615_CUSTOMIZING", {"object": "T001W"})["params"]["object"])
        for action, params in (
            ("OPEN_S4615_CUSTOMIZING_READ", {"transaction": "SM30"}),
            ("INSPECT_S4615_CUSTOMIZING", {"object": "T000"}),
            ("INSPECT_S4615_CUSTOMIZING", {"object": "T001W", "value": "1010"}),
        ):
            with self.subTest(action=action, params=params), self.assertRaises(Exception):
                request(action, params)
        with self.assertRaises(Exception):
            request("INSPECT_S4615_CUSTOMIZING", {"object": "T001W"}, mode="EXECUTE")
        self.assertEqual("TVKWZ", request("READ_S4615_CUSTOMIZING_TABLE", {"table": "TVKWZ"})["params"]["table"])
        self.assertEqual("T000", request("READ_S4615_CUSTOMIZING_TABLE", {"table": "T000"})["params"]["table"])
        self.assertEqual("T000", request("SCAN_S4615_CUSTOMIZING", {"object": "T000"})["params"]["object"])
        with self.assertRaises(Exception):
            request("READ_S4615_CUSTOMIZING_TABLE", {"table": "T001W"}, mode="EXECUTE")

    def test_s4615_customizing_inspection_reads_only_confirmed_screen(self):
        session, _ = self.attach(RawSession(transaction="SE16N"))
        snapshot = {
            "transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "100",
            "window_title": "Data Browser", "status_bar": {"text": "", "message_type": ""},
            "popups": [], "input_fields": [{"text": "T001W"}], "labels": [],
            "tables": [{"visible_rows": [{"index": 0, "values": [{"column": "WERKS", "text": "1710"}]}]}],
            "truncated": False,
        }
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
            result = execute_read_action(session, {"action": "INSPECT_S4615_CUSTOMIZING", "params": {"object": "T001W"}})
        self.assertEqual("T001W", result["object"])
        self.assertFalse(result["complete_dataset_proven"])
        self.assertEqual("1710", result["tables"][0]["visible_rows"][0]["values"][0]["text"])
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, {"action": "INSPECT_S4615_CUSTOMIZING", "params": {"object": "TVKWZ"}})
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value={**snapshot, "popups": [{"window_title": "Unknown"}]}):
            with self.assertRaises(ActionBlockedError):
                execute_read_action(session, {"action": "INSPECT_S4615_CUSTOMIZING", "params": {"object": "T001W"}})

    def test_s4615_customizing_read_open_does_not_enable_writes(self):
        session, _ = self.attach()
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value={"transaction": "SE16N"}):
            result = execute_read_action(session, {"action": "OPEN_S4615_CUSTOMIZING_READ", "params": {"transaction": "SE16N"}})
        self.assertEqual("SE16N", result["transaction"])
        self.assertEqual("SE16N", session.identity["transaction"])
        with self.assertRaises(ActionBlockedError):
            session.audit("SET_TEXT")
        with self.assertRaises(ActionBlockedError):
            session.audit("SAVE")

    def test_s4615_shipping_point_open_remains_read_only(self):
        session, _ = self.attach()
        with patch("src.sap_gui_bridge.runner.inspect_screen", return_value={"transaction": "OVXD"}):
            result = execute_read_action(session, {"action": "OPEN_S4615_CUSTOMIZING_READ", "params": {"transaction": "OVXD"}})
        self.assertEqual("OVXD", result["transaction"])
        with self.assertRaises(ActionBlockedError):
            session.audit("SAVE")

    def test_s4615_se16n_read_uses_only_observed_search_controls(self):
        session, _ = self.attach()
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        field = Control(prefix + "/usr/ctxtGD-TAB", "GuiCTextField")
        edit = Control(prefix + "/usr/chkGD-EDIT", "GuiCheckBox")
        edit.Selected = False
        button = Control(prefix + "/tbar[1]/btn[8]", "GuiButton", tooltip="En ligne   (F8)")
        session.raw.controls.update({item.Id: item for item in (field, edit, button)})
        before = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "120", "popups": []}
        after = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "100", "window_title": "Results", "status_bar": {}, "popups": [], "input_fields": [], "labels": [], "tables": [], "truncated": False}
        with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
            result = execute_read_action(session, {"action": "READ_S4615_CUSTOMIZING_TABLE", "params": {"table": "T001W"}})
        self.assertEqual("T001W", field.Text)
        self.assertTrue(button.pressed)
        self.assertFalse(result["complete_dataset_proven"])

    def test_s4615_se16n_read_disables_manage_entries_before_lookup(self):
        session, _ = self.attach()
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        field = Control(prefix + "/usr/ctxtGD-TAB", "GuiCTextField")
        edit = Control(prefix + "/usr/chkGD-EDIT", "GuiCheckBox")
        edit.Selected = True
        button = Control(prefix + "/tbar[1]/btn[8]", "GuiButton", tooltip="En ligne   (F8)")
        session.raw.controls.update({item.Id: item for item in (field, edit, button)})
        before = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "120", "popups": []}
        after = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "200", "window_title": "T001W", "status_bar": {}, "popups": [], "input_fields": [], "labels": [], "tables": [], "truncated": False}
        with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
            execute_read_action(session, {"action": "READ_S4615_CUSTOMIZING_TABLE", "params": {"table": "T001W"}})
        self.assertFalse(edit.Selected)
        self.assertEqual("T001W", field.Text)
        self.assertTrue(button.pressed)

    def test_s4615_se16n_read_uses_exact_online_menu_when_button_hidden(self):
        session, _ = self.attach()
        prefix = "/app/con[0]/ses[0]/wnd[0]"
        field = Control(prefix + "/usr/ctxtGD-TAB", "GuiCTextField")
        edit = Control(prefix + "/usr/chkGD-EDIT", "GuiCheckBox")
        edit.Selected = 0
        menu = Control(prefix + "/mbar/menu[0]/menu[0]/menu[0]", "GuiMenu", "En ligne")
        session.raw.controls.update({item.Id: item for item in (field, edit, menu)})
        before = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "120", "popups": []}
        after = {"transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "200", "window_title": "T001W", "status_bar": {}, "popups": [], "input_fields": [], "labels": [], "tables": [], "truncated": False}
        with patch("src.sap_gui_bridge.runner.inspect_screen", side_effect=[before, after]):
            result = execute_read_action(session, {"action": "READ_S4615_CUSTOMIZING_TABLE", "params": {"table": "T001W"}})
        self.assertEqual("T001W", field.Text)
        self.assertTrue(menu.selected)
        self.assertFalse(result["complete_dataset_proven"])


if __name__ == "__main__":
    unittest.main()
