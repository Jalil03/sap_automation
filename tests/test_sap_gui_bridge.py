import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.errors import ActionBlockedError, SessionNotFoundError
from src.sap_gui_bridge.inspection import inspect_screen
from src.sap_gui_bridge.navigation import open_transaction, press_safe_button, set_text
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

    def press(self):
        self.pressed = True

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

    def test_unknown_action_and_ctrl_s_are_blocked(self):
        session, _ = self.attach(mode=SafetyMode.PREPARE)
        with self.assertRaises(ActionBlockedError):
            session.policy.authorize(identity=session.identity, action="SAVE")
        with self.assertRaises(ActionBlockedError):
            session.policy.authorize(identity=session.identity, action="PRESS_SAFE_BUTTON", key_chord="Ctrl+S")


if __name__ == "__main__":
    unittest.main()
