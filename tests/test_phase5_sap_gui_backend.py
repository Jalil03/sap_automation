import unittest
import uuid
from types import SimpleNamespace
from unittest.mock import Mock, patch

from src.provisioning.phase5 import Phase5ProvisioningEngine, load_seed
from src.provisioning.sap_gui_backend import (
    ASSIGNMENT_IMG_LEAVES,
    ASSIGNMENT_IMG_NODES,
    EXPECTED_TARGETS,
    _lookup_assignment,
    _lookup_sales_organization_1010,
    _save_existing_sales_organization_1010,
    _start_company_code_copy,
    _start_sales_organization_copy,
    execute_runner_action,
    SapGuiPhase5Backend,
)
from src.sap_gui_bridge.errors import ActionBlockedError, ProtocolError
from src.sap_gui_bridge.navigation import (
    COMPANY_CODE_TABLE_SEARCH,
    COMPANY_CODE_TABLE_VARIANTS,
    PHASE5_ASSIGNMENT_TABLE_SEARCHES,
    SALES_ORGANIZATION_TABLE_SEARCH,
    find_company_code_table_value,
    find_phase5_assignment_table_row,
    find_sales_organization_table_value,
)
from src.sap_gui_bridge.protocol import validate_request
from scripts.run_phase5_execute import parser as phase5_execute_parser


IDENTITY = {"system": "A4H", "client": "600", "user": "ABDELJ", "transaction": ""}


class S4615BillingBootstrapTests(unittest.TestCase):
    def test_zf01_rejects_unapproved_target_or_range_before_gui_change(self):
        session = Mock()
        base = {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"billing_type": "ZF01", "number_range": "15"}}
        for altered in ({**base, "target": {"billing_type": "ZF02"}}, {**base, "values": {"billing_type": "ZF01", "number_range": "19"}}):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, {"params": altered})
        session.find.assert_not_called()

    def test_zf01_copy_control_popup_rejects_unexpected_context(self):
        session = Mock()
        request = {"params": {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"copy_control": "NO"}}}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={"transaction": "VOFA", "program": "SAPLSPO1", "popups": [{"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Unexpected"}]}):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, request)
        session.find.assert_not_called()

    def test_zf01_pending_detail_requires_unique_visible_target(self):
        session = Mock()
        request = {"params": {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"inspect_pending": "ZF01"}}}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={"transaction": "VOFA", "program": "SAPL081F", "screen_number": "100", "popups": [], "tables": []}):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, request)
        session.find.assert_not_called()

    def test_zf01_save_rejects_wrong_number_range(self):
        session = Mock()
        request = {"params": {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"save_verified_pending": "ZF01"}}}
        snapshot = {"transaction": "VOFA", "program": "SAPL081F", "screen_number": "101", "popups": [], "input_fields": [
            {"id": "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-FKART", "text": "ZF01"},
            {"id": "/app/con[0]/ses[0]/wnd[0]/usr/txtV_TVFK-NUMKI", "text": "19"},
            {"id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtV_TVFK-VBTYP", "text": "M"},
        ]}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, request)
        session.find.assert_not_called()

    def test_zf01_transport_rejects_other_order(self):
        session = Mock()
        request = {"params": {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"confirm_transport": "A4HK908422"}}}
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Demande : ordre du Customizing", "input_fields": [
            {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-OBJ_NAME", "text": "V_TVFK"},
            {"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR", "text": "A4HK999999"},
            {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT", "text": "S4615 Training Setup"},
        ]}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={"transaction": "VOFA", "program": "SAPLSTRD", "popups": [popup]}):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, request)
        session.find.assert_not_called()

    def test_zf01_saved_info_requires_confirmed_saved_status(self):
        session = Mock()
        request = {"params": {"operation": "S4615_BILLING_TYPE_ZF01", "phase": "PROVISION", "target": {"billing_type": "ZF01"}, "values": {"close_saved_info": "ZF01"}}}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={"transaction": "VOFA", "program": "SAPMSSY0", "status_bar": {"text": ""}, "popups": [{}]}):
            with self.assertRaises(ActionBlockedError):
                execute_runner_action(session, request)
        session.find.assert_not_called()
SALES_TABLE_ID = SALES_ORGANIZATION_TABLE_SEARCH["table_id"]
COMPANY_TABLE_ID = COMPANY_CODE_TABLE_SEARCH["table_id"]


def response(result, *, identity=None, status="SUCCESS"):
    return {
        "request_id": str(uuid.uuid4()),
        "status": status,
        "sap": IDENTITY if identity is None else identity,
        "result": result,
        "error": None if status == "SUCCESS" else {"message": "blocked"},
    }


class ScriptedSender:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def __call__(self, phase, params):
        self.calls.append((phase, params))
        return self.replies.pop(0)


class FakeSalesScrollbar:
    def __init__(self, position, maximum):
        self.Maximum = maximum
        self._position = min(max(int(position), 0), maximum)
        self.visited = []

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = min(max(int(value), 0), self.Maximum)
        self.visited.append(self._position)


class FakeSalesTable:
    Id = SALES_TABLE_ID
    Type = "GuiTableControl"

    def __init__(self, raw):
        self.raw = raw
        self.RowCount = len(raw.values)
        self.VisibleRowCount = raw.visible_count
        self.VerticalScrollbar = raw.scrollbar

    @property
    def Children(self):
        raise AssertionError("Lookup must read exact cells, not table.Children")


class FakeSalesSession:
    def __init__(self, values, *, missing_rows=(), position=12):
        self.values = list(values)
        self.missing_rows = set(missing_rows)
        self.visible_count = 22
        self.scrollbar = FakeSalesScrollbar(
            position,
            max(0, len(self.values) - self.visible_count),
        )
        self.raw = type(
            "Raw",
            (),
            {
                "Busy": False,
                "Info": type("Info", (), {"Program": "SAPL0ORG"})(),
            },
        )()
        self.table_acquisitions = 0
        self.audit_events = []

    @property
    def identity(self):
        return {
            "system": "A4H",
            "client": "600",
            "user": "ABDELJ",
            "transaction": "V_TVKO",
        }

    def validate_identity(self):
        return None

    def audit(self, action, **kwargs):
        self.audit_events.append((action, kwargs))

    def find(self, control_id):
        if control_id == SALES_TABLE_ID:
            self.table_acquisitions += 1
            return FakeSalesTable(self)
        prefix = SALES_TABLE_ID + "/ctxtV_TVKO-VKORG[0,"
        if control_id.startswith(prefix) and control_id.endswith("]"):
            relative_row = int(control_id[len(prefix):-1])
            absolute_row = self.scrollbar.Position + relative_row
            if (
                absolute_row >= len(self.values)
                or absolute_row in self.missing_rows
                or relative_row >= self.visible_count
            ):
                raise KeyError(control_id)
            return type(
                "Cell",
                (),
                {
                    "Id": control_id,
                    "Type": "GuiCTextField",
                    "Text": self.values[absolute_row],
                },
            )()
        raise KeyError(control_id)


class FakeCompanyScrollbar:
    def __init__(self, maximum):
        self.Maximum = maximum
        self._position = 0
        self.visited = []

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = min(max(int(value), 0), self.Maximum)
        self.visited.append(self._position)


class FakeCompanyTable:
    Id = COMPANY_TABLE_ID
    Type = "GuiTableControl"

    def __init__(self, session):
        self.session = session
        self.RowCount = len(session.values)
        self.VisibleRowCount = session.visible_count
        self.VerticalScrollbar = session.scrollbar

    @property
    def Children(self):
        raise AssertionError("Company-code lookup must use exact direct cell IDs")


class FakeCompanySession:
    def __init__(self, values, *, missing_rows=()):
        self.values = list(values)
        self.missing_rows = set(missing_rows)
        self.visible_count = 20
        self.scrollbar = FakeCompanyScrollbar(
            max(0, len(self.values) - self.visible_count)
        )
        self.raw = type(
            "Raw",
            (),
            {"Busy": False, "Info": type("Info", (), {"Program": "SAPL0ORG"})()},
        )()
        self.table_acquisitions = 0
        self.audit_events = []

    @property
    def identity(self):
        return {
            "system": "A4H",
            "client": "600",
            "user": "ABDELJ",
            "transaction": "V_T001",
        }

    def validate_identity(self):
        return None

    def audit(self, action, **kwargs):
        self.audit_events.append((action, kwargs))

    def find(self, control_id):
        if control_id == COMPANY_TABLE_ID:
            self.table_acquisitions += 1
            return FakeCompanyTable(self)
        prefix = f"{COMPANY_TABLE_ID}/ctxtV_T001-BUKRS[0,"
        if control_id.startswith(prefix) and control_id.endswith("]"):
            relative_row = int(control_id[len(prefix):-1])
            absolute_row = self.scrollbar.Position + relative_row
            if (
                absolute_row >= len(self.values)
                or absolute_row in self.missing_rows
                or relative_row >= self.visible_count
            ):
                raise KeyError(control_id)
            return type(
                "Cell",
                (),
                {
                    "Id": control_id,
                    "Type": "GuiCTextField",
                    "Text": self.values[absolute_row],
                },
            )()
        raise KeyError(control_id)


class FakeAssignmentScrollbar:
    def __init__(self, position, maximum):
        self.Maximum = maximum
        self._position = min(max(int(position), 0), maximum)
        self.visited = []

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        self._position = min(max(int(value), 0), self.Maximum)
        self.visited.append(self._position)


class FakeAssignmentTable:
    Type = "GuiTableControl"

    def __init__(self, session):
        self.session = session
        self.Id = session.contract["table_id"]
        self.RowCount = len(session.values)
        self.VisibleRowCount = session.visible_count
        self.VerticalScrollbar = session.scrollbar
        self.Type = session.table_type


class FakeAssignmentSession:
    def __init__(
        self,
        operation,
        values,
        *,
        missing_cells=(),
        position=0,
        visible_count=13,
        wrong_cell_type=None,
        table_id_matches=True,
        table_type="GuiTableControl",
    ):
        self.operation = operation
        self.contract = PHASE5_ASSIGNMENT_TABLE_SEARCHES[operation]
        self.values = list(values)
        self.missing_cells = set(missing_cells)
        self.wrong_cell_type = wrong_cell_type
        self.table_id_matches = table_id_matches
        self.table_type = table_type
        self.visible_count = visible_count
        self.scrollbar = FakeAssignmentScrollbar(
            position,
            max(0, len(self.values) - visible_count),
        )
        self.raw = type(
            "Raw",
            (),
            {
                "Busy": False,
                "Info": type("Info", (), {"Program": "SAPLCUST_ASSIGN_SD"})(),
            },
        )()
        self.table_acquisitions = 0
        self.audit_events = []

    @property
    def identity(self):
        return {
            "system": "A4H",
            "client": "600",
            "user": "ABDELJ",
            "transaction": getattr(self, "transaction", "SIMG"),
        }

    def validate_identity(self):
        return None

    def audit(self, action, **kwargs):
        self.audit_events.append((action, kwargs))

    def find(self, control_id):
        if control_id == self.contract["table_id"]:
            self.table_acquisitions += 1
            table = FakeAssignmentTable(self)
            if not self.table_id_matches:
                table.Id = table.Id + "/unexpected"
            return table
        for field_name, field in self.contract["fields"].items():
            prefix = (
                f"{self.contract['table_id']}/{field['control']}"
                f"[{field['column']},"
            )
            if control_id.startswith(prefix) and control_id.endswith("]"):
                relative_row = int(control_id[len(prefix):-1])
                absolute_row = self.scrollbar.Position + relative_row
                if (
                    absolute_row >= len(self.values)
                    or relative_row >= self.visible_count
                    or (field_name, absolute_row) in self.missing_cells
                ):
                    raise KeyError(control_id)
                return type(
                    "Cell",
                    (),
                    {
                        "Id": control_id,
                        "Type": (
                            "GuiTextField"
                            if self.wrong_cell_type == (field_name, absolute_row)
                            else "GuiCTextField"
                        ),
                        "Text": self.values[absolute_row][field_name],
                    },
                )()
        raise KeyError(control_id)


class Phase5SapGuiBackendTests(unittest.TestCase):
    def backend(self, replies):
        sender = ScriptedSender(replies)
        return SapGuiPhase5Backend(sender=sender), sender

    def test_protocol_whitelists_only_exact_phase5_operations(self):
        payload = {
            "request_id": str(uuid.uuid4()),
            "mode": "EXECUTE",
            "action": "PHASE5_OPERATION",
            "params": {
                "operation": "COMPANY_CODE_1010",
                "phase": "LOOKUP",
                "target": EXPECTED_TARGETS["COMPANY_CODE_1010"],
                "values": {},
            },
        }
        self.assertEqual("EXECUTE", validate_request(payload)["mode"])
        payload["params"]["operation"] = "DELETE_ANYTHING"
        with self.assertRaises(ProtocolError):
            validate_request(payload)

    def test_copy_dialog_inspection_phase_is_company_code_only_and_read_only(self):
        payload = {
            "request_id": str(uuid.uuid4()),
            "mode": "EXECUTE",
            "action": "PHASE5_OPERATION",
            "params": {
                "operation": "COMPANY_CODE_1010",
                "phase": "COPY_DIALOG_INSPECT",
                "target": EXPECTED_TARGETS["COMPANY_CODE_1010"],
                "values": {},
            },
        }
        self.assertEqual(
            "COPY_DIALOG_INSPECT",
            validate_request(payload)["params"]["phase"],
        )
        payload["params"]["operation"] = "SALES_ORGANIZATION_1010"
        with self.assertRaisesRegex(ProtocolError, "only allowlisted"):
            validate_request(payload)
        payload["params"]["operation"] = "COMPANY_CODE_1010"
        payload["params"]["values"] = {"company_name": "must be empty"}
        with self.assertRaisesRegex(ProtocolError, "does not accept write values"):
            validate_request(payload)

    def test_read_exists_skips_without_provision(self):
        backend, sender = self.backend([response({"state": "EXISTS"})])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("SKIPPED_EXISTS", result.status)
        self.assertEqual(["LOOKUP"], [call[0] for call in sender.calls])

    def test_read_missing_provisions_once_then_reads_back(self):
        target = EXPECTED_TARGETS["COMPANY_CODE_1010"]
        backend, sender = self.backend([
            response({"state": "MISSING"}),
            response({"accepted": True}),
            response({"verified": True, "object": target}),
        ])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("PROVISIONED_VERIFIED", result.status)
        self.assertEqual(
            ["LOOKUP", "PROVISION", "READBACK"],
            [call[0] for call in sender.calls],
        )

    def test_transport_stops_before_readback(self):
        backend, sender = self.backend([
            response({"state": "MISSING"}),
            response({"transport_request": True}),
        ])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_TRANSPORT_REQUIRED", result.status)
        self.assertEqual(["LOOKUP", "PROVISION"], [call[0] for call in sender.calls])

    def test_unexpected_popup_stops_before_readback(self):
        backend, sender = self.backend([
            response({"state": "MISSING"}),
            response({"unexpected_popup": True}),
        ])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_UNEXPECTED_POPUP", result.status)
        self.assertEqual(["LOOKUP", "PROVISION"], [call[0] for call in sender.calls])

    def test_ambiguous_save_stops_without_retry_or_readback(self):
        backend, sender = self.backend([
            response({"state": "MISSING"}),
            response({"ambiguous_save": True}),
        ])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_AMBIGUOUS_SAVE", result.status)
        self.assertEqual(["LOOKUP", "PROVISION"], [call[0] for call in sender.calls])

    def test_missing_write_outcome_is_treated_as_ambiguous(self):
        backend, sender = self.backend([
            response({"state": "MISSING"}),
            response({}),
        ])
        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).ensure_company_code()
        self.assertEqual("BLOCKED_AMBIGUOUS_SAVE", result.status)
        self.assertEqual(["LOOKUP", "PROVISION"], [call[0] for call in sender.calls])

    def test_wrong_identity_is_rejected(self):
        backend, _ = self.backend([
            response(
                {"state": "EXISTS"},
                identity={"system": "A4H", "client": "500", "user": "ABDELJ"},
            )
        ])
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            backend.lookup("COMPANY_CODE_1010", EXPECTED_TARGETS["COMPANY_CODE_1010"])

    def test_runner_error_is_reported_before_identity_validation(self):
        backend, _ = self.backend([
            response({}, identity={}, status="ERROR"),
        ])

        with self.assertRaisesRegex(RuntimeError, "blocked"):
            backend.lookup("COMPANY_CODE_1010", EXPECTED_TARGETS["COMPANY_CODE_1010"])

    def test_target_and_template_are_exact(self):
        backend, _ = self.backend([])
        with self.assertRaises(ValueError):
            backend.lookup("COMPANY_CODE_1010", {"company_code": "1710"})
        with self.assertRaises(ValueError):
            backend.provision(
                "COMPANY_CODE_1010",
                EXPECTED_TARGETS["COMPANY_CODE_1010"],
                {"technical_template": "1710"},
            )

    def _sales_org_request(self, phase, values=None, target=None):
        return {
            "params": {
                "operation": "SALES_ORGANIZATION_1010",
                "phase": phase,
                "target": (
                    EXPECTED_TARGETS["SALES_ORGANIZATION_1010"]
                    if target is None
                    else target
                ),
                "values": values or {},
            }
        }

    def _run_sales_org_lookup(self, session):
        return find_sales_organization_table_value(
            session, dict(SALES_ORGANIZATION_TABLE_SEARCH)
        )

    def test_company_code_scan_covers_131_runtime_rows_across_overlapping_pages(self):
        values = [f"{2000 + index:04d}" for index in range(131)]
        values[130] = "1010"
        session = FakeCompanySession(values)

        with patch(
            "src.sap_gui_bridge.navigation.inspect_screen",
            return_value={
                "transaction": "V_T001",
                "program": "SAPL0ORG",
                "window_title": 'Afficher vue "Société" : synthèse',
                "tables": [{"id": COMPANY_TABLE_ID, "type": "GuiTableControl"}],
            },
        ):
            result = find_company_code_table_value(
                session, dict(COMPANY_CODE_TABLE_SEARCH)
            )["table_value_search"]

        self.assertEqual("FOUND", result["result"])
        self.assertEqual(131, result["row_count"])
        self.assertEqual(131, result["rows_read"])
        self.assertEqual(130, result["found_row"])
        self.assertEqual(
            [0, 20, 40, 60, 80, 100, 111],
            result["visited_scroll_positions"],
        )
        self.assertGreater(session.table_acquisitions, 7)

    def test_company_code_scan_confirms_missing_only_after_all_runtime_rows(self):
        values = [f"{2000 + index:04d}" for index in range(131)]
        session = FakeCompanySession(values)

        with patch(
            "src.sap_gui_bridge.navigation._position_company_code_1010",
            side_effect=AssertionError("fallback must not run after complete scan"),
        ), patch(
            "src.sap_gui_bridge.navigation.inspect_screen",
            return_value={
                "transaction": "V_T001",
                "program": "SAPL0ORG",
                "window_title": 'Modifier vue "Société" : synthèse',
                "tables": [{"id": COMPANY_TABLE_ID, "type": "GuiTableControl"}],
            },
        ):
            result = find_company_code_table_value(
                session, dict(COMPANY_CODE_TABLE_SEARCH)
            )["table_value_search"]

        self.assertEqual("CONFIRMED_NOT_FOUND", result["result"])
        self.assertEqual(131, result["row_count"])
        self.assertEqual(131, result["rows_read"])
        self.assertEqual(
            [0, 20, 40, 60, 80, 100, 111],
            result["visited_scroll_positions"],
        )

    def test_company_code_scan_keeps_unknown_when_a_runtime_row_is_unreadable(self):
        values = [f"{2000 + index:04d}" for index in range(131)]
        session = FakeCompanySession(values, missing_rows={45})

        with patch(
            "src.sap_gui_bridge.navigation._position_company_code_1010",
            return_value=("UNKNOWN", None, "positioning did not find target"),
        ) as fallback, patch(
            "src.sap_gui_bridge.navigation.inspect_screen",
            return_value={
                "transaction": "V_T001",
                "program": "SAPL0ORG",
                "window_title": 'Afficher vue "Société" : synthèse',
                "tables": [{"id": COMPANY_TABLE_ID, "type": "GuiTableControl"}],
            },
        ):
            result = find_company_code_table_value(
                session, dict(COMPANY_CODE_TABLE_SEARCH)
            )["table_value_search"]

        self.assertEqual("UNKNOWN", result["result"])
        self.assertLess(result["rows_read"], result["row_count"])
        self.assertEqual("POSITION_DIALOG", result["method"])
        fallback.assert_called_once()

    def test_company_code_scan_accepts_only_evidenced_display_and_maintenance_variants(self):
        values = [f"{2000 + index:04d}" for index in range(131)]
        self.assertEqual(2, len(COMPANY_CODE_TABLE_VARIANTS))
        for variant in COMPANY_CODE_TABLE_VARIANTS:
            with self.subTest(window_title=variant["window_title"]):
                session = FakeCompanySession(values)
                with patch(
                    "src.sap_gui_bridge.navigation.inspect_screen",
                    return_value={
                        "transaction": "V_T001",
                        "program": "SAPL0ORG",
                        "window_title": variant["window_title"],
                        "tables": [{
                            "id": variant["table_id"],
                            "type": "GuiTableControl",
                        }],
                    },
                ):
                    result = find_company_code_table_value(
                        session, dict(COMPANY_CODE_TABLE_SEARCH)
                    )["table_value_search"]

                self.assertEqual("CONFIRMED_NOT_FOUND", result["result"])
                self.assertEqual(131, result["rows_read"])

    def test_company_code_scan_rejects_unobserved_v001_title(self):
        session = FakeCompanySession(["1000"])
        with patch(
            "src.sap_gui_bridge.navigation.inspect_screen",
            return_value={
                "transaction": "V_T001",
                "program": "SAPL0ORG",
                "window_title": 'Afficher vue "Organisation" : synthèse',
                "tables": [{"id": COMPANY_TABLE_ID, "type": "GuiTableControl"}],
            },
        ):
            with self.assertRaisesRegex(ActionBlockedError, "exact evidenced"):
                find_company_code_table_value(
                    session, dict(COMPANY_CODE_TABLE_SEARCH)
                )

    def test_company_code_provision_reports_first_missing_copy_control(self):
        class ProvisionSession:
            identity = {"transaction": "V_T001"}
            raw = type(
                "Raw",
                (),
                {"Info": type("Info", (), {"Program": "SAPL0ORG"})()},
            )()

            def __init__(self):
                self.requested_ids = []

            def find(self, control_id):
                self.requested_ids.append(control_id)
                raise RuntimeError("The control could not be found by id.")

        session = ProvisionSession()
        with patch(
            "src.provisioning.sap_gui_backend._open_company_code_screen_from_vbs"
        ), patch(
            "src.provisioning.sap_gui_backend._lookup_company_code_1010",
            return_value={"state": "MISSING", "evidence": {}},
        ), patch(
            "src.provisioning.sap_gui_backend._select_company_code_template_and_open_copy",
            side_effect=ActionBlockedError("copy control unavailable"),
        ):
            with self.assertRaises(ActionBlockedError) as raised:
                _start_company_code_copy(session)

        message = str(raised.exception)
        self.assertIn("copy control unavailable", message)
        self.assertEqual([], session.requested_ids)

    def test_sales_org_lookup_finds_1010_by_direct_cell_ids_after_scroll(self):
        values = [f"{2000 + index:04d}" for index in range(34)]
        values[27] = "1010"
        session = FakeSalesSession(values)

        result = self._run_sales_org_lookup(session)["table_value_search"]

        self.assertEqual("FOUND", result["result"])
        self.assertEqual(27, result["found_row"])
        self.assertEqual(34, result["rows_read"])
        self.assertEqual([0, 12], result["visited_scroll_positions"])
        self.assertGreater(session.table_acquisitions, 2)
        self.assertEqual(
            ["FIND_TABLE_VALUE"],
            [action for action, _ in session.audit_events],
        )

    def test_sales_org_lookup_confirms_missing_only_after_all_rows(self):
        values = [f"{2000 + index:04d}" for index in range(34)]
        session = FakeSalesSession(values)

        result = self._run_sales_org_lookup(session)["table_value_search"]

        self.assertEqual("CONFIRMED_NOT_FOUND", result["result"])
        self.assertEqual(34, result["rows_read"])
        self.assertEqual([0, 12], result["visited_scroll_positions"])

    def test_sales_org_lookup_returns_unknown_for_unreadable_cell(self):
        values = [f"{2000 + index:04d}" for index in range(34)]
        session = FakeSalesSession(values, missing_rows={5})

        result = self._run_sales_org_lookup(session)["table_value_search"]

        self.assertEqual("UNKNOWN", result["result"])
        self.assertEqual(5, result["rows_read"])
        self.assertIn("not deterministically readable", result["reason"])

    def test_sales_org_phase_routes_lookup_to_scanner(self):
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()
        with patch(
            "src.provisioning.sap_gui_backend._lookup_sales_organization_1010",
            return_value={"state": "EXISTS", "evidence": {}},
        ) as lookup:
            result = execute_runner_action(
                session, self._sales_org_request("LOOKUP")
            )

        self.assertEqual("EXISTS", result["state"])
        lookup.assert_called_once_with(session)

    def test_sales_org_lookup_maps_found_missing_and_unknown(self):
        session = type(
            "Session", (), {"identity": {"transaction": "V_TVKO"}}
        )()
        for result_name, expected_state in (
            ("FOUND", "EXISTS"),
            ("CONFIRMED_NOT_FOUND", "MISSING"),
            ("UNKNOWN", "UNKNOWN"),
        ):
            with self.subTest(result=result_name):
                with patch(
                    "src.provisioning.sap_gui_backend.find_sales_organization_table_value",
                    return_value={"table_value_search": {"result": result_name}},
                ):
                    result = _lookup_sales_organization_1010(session)
                self.assertEqual(expected_state, result["state"])

    def test_company_code_lookup_to_sales_org_lookup_navigates_and_scans(self):
        class IntegratedSession:
            def __init__(self):
                self.transaction = "V_T001"
                self.audit_events = []

            @property
            def identity(self):
                return {"transaction": self.transaction}

            def audit(self, action, **kwargs):
                self.audit_events.append((action, kwargs))

        session = IntegratedSession()
        navigation_calls = []
        company_search = {
            "table_value_search": {"result": "FOUND", "found_value": "1010"}
        }
        sales_search = {
            "table_value_search": {
                "result": "FOUND",
                "found_value": "1010",
                "found_row": 27,
                "rows_read": 34,
            }
        }

        def open_transaction(_session, transaction):
            self.assertIs(_session, session)
            self.assertEqual("SPRO", transaction)
            session.transaction = transaction

        def press_exact(_session, control_id):
            self.assertEqual("wnd[0]/tbar[1]/btn[5]", control_id)
            session.transaction = "SIMG"

        def navigate(_session, params):
            navigation_calls.append(params)
            return {}

        def select_activity(_session, params):
            self.assertEqual("sales_organization", params["target"])
            session.transaction = "V_TVKO"
            return {}

        with (
            patch(
                "src.provisioning.sap_gui_backend.find_company_code_table_value",
                return_value=company_search,
            ),
            patch(
                "src.provisioning.sap_gui_backend.open_transaction",
                side_effect=open_transaction,
            ),
            patch(
                "src.provisioning.sap_gui_backend._press_exact",
                side_effect=press_exact,
            ),
            patch(
                "src.provisioning.sap_gui_backend.navigate",
                side_effect=navigate,
            ),
            patch(
                "src.provisioning.sap_gui_backend.select_sales_organization_activity",
                side_effect=select_activity,
            ),
            patch(
                "src.provisioning.sap_gui_backend.find_sales_organization_table_value",
                side_effect=lambda current_session, params: (
                    self.assertEqual("V_TVKO", current_session.identity["transaction"])
                    or sales_search
                ),
            ),
        ):
            company_result = execute_runner_action(
                session,
                {
                    "params": {
                        "operation": "COMPANY_CODE_1010",
                        "phase": "LOOKUP",
                        "target": EXPECTED_TARGETS["COMPANY_CODE_1010"],
                        "values": {},
                    }
                },
            )
            self.assertEqual("EXISTS", company_result["state"])
            self.assertEqual("V_T001", session.identity["transaction"])

            sales_result = execute_runner_action(
                session, self._sales_org_request("LOOKUP")
            )

        self.assertEqual("EXISTS", sales_result["state"])
        self.assertEqual(4, len(navigation_calls))
        self.assertEqual(
            ["EXPAND_TREE_NODE", "EXPAND_TREE_NODE", "EXPAND_TREE_NODE", "OPEN_IMG_ACTIVITY"],
            [call["navigation_operation"] for call in navigation_calls],
        )
        self.assertEqual(
            ["GuiShell"] * 4,
            [call["expected_type"] for call in navigation_calls],
        )
        self.assertEqual("05  4      1", navigation_calls[-1]["node_key"])
        self.assertEqual("2", navigation_calls[-1]["item_column"])

    def test_sales_org_lookup_rejects_unsupported_starting_transaction(self):
        session = type(
            "Session", (), {"identity": {"transaction": "VA01"}}
        )()

        with self.assertRaisesRegex(
            ActionBlockedError, "cannot start from transaction 'VA01'"
        ):
            _lookup_sales_organization_1010(session)

    def test_sales_org_provision_opens_only_live_copy_boundary(self):
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()

        with patch(
            "src.provisioning.sap_gui_backend._start_sales_organization_copy",
            return_value={"provisioning_blocked": True, "reason": "capture"},
        ) as start_copy:
            result = execute_runner_action(
                session,
                self._sales_org_request(
                    "PROVISION", values={"technical_template": "1710"}
                ),
            )
        start_copy.assert_called_once_with(session, {"technical_template": "1710"})
        self.assertTrue(result["provisioning_blocked"])

    @staticmethod
    def _sales_org_pending_save_snapshot(*, popups=None):
        return {
            "transaction": "V_TVKO",
            "program": "SAPL0ORG",
            "screen_number": "240",
            "window_title": 'Modifier vue "Organisations commerciales" : synth\u00e8se',
            "status_bar": {"text": "", "message_type": "S"},
            "popups": popups or [],
            "tables": [
                {
                    "id": SALES_TABLE_ID,
                    "type": "GuiTableControl",
                    "changeable": True,
                }
            ],
            "input_fields": [
                {
                    "id": f"{SALES_TABLE_ID}/ctxtV_TVKO-VKORG[0,0]",
                    "type": "GuiCTextField",
                    "text": "1010",
                    "visible": True,
                },
                {
                    "id": f"{SALES_TABLE_ID}/txtV_TVKO-VTEXT[1,0]",
                    "type": "GuiTextField",
                    "text": "S4615 Training",
                    "visible": True,
                },
            ],
            "buttons": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[5]",
                    "type": "GuiMenu",
                    "text": "Sauvegarder",
                    "changeable": True,
                    "visible": True,
                }
            ],
        }

    def test_sales_org_existing_target_is_saved_without_recopying(self):
        snapshot = self._sales_org_pending_save_snapshot()
        saved_snapshot = self._sales_org_pending_save_snapshot()
        selected = []
        menu = SimpleNamespace(
            Type="GuiMenu",
            Text="Sauvegarder",
            Changeable=True,
            select=lambda: selected.append(True),
        )
        session = SimpleNamespace(
            identity={"transaction": "V_TVKO"},
            raw=SimpleNamespace(Busy=False),
            find=lambda control_id: menu,
        )

        with (
            patch(
                "src.provisioning.sap_gui_backend.inspect_screen",
                side_effect=[snapshot, snapshot, saved_snapshot],
            ),
            patch(
                "src.provisioning.sap_gui_backend._lookup_sales_organization_1010",
                return_value={"state": "EXISTS", "evidence": {"result": "FOUND"}},
            ) as lookup,
            patch(
                "src.provisioning.sap_gui_backend._open_sales_organization_screen"
            ) as open_screen,
        ):
            result = _start_sales_organization_copy(
                session, {"technical_template": "1710"}
            )

        self.assertTrue(result["accepted"])
        self.assertEqual("1010", result["target"])
        self.assertEqual(
            "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[5]",
            result["save_action"],
        )
        self.assertEqual([True], selected)
        lookup.assert_called_once_with(session)
        open_screen.assert_not_called()

    def test_sales_org_save_fails_closed_on_unverified_popup(self):
        snapshot = self._sales_org_pending_save_snapshot()
        popup_snapshot = self._sales_org_pending_save_snapshot(
            popups=[{"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Unknown"}]
        )
        menu = SimpleNamespace(
            Type="GuiMenu",
            Text="Sauvegarder",
            Changeable=True,
            select=lambda: None,
        )
        session = SimpleNamespace(
            raw=SimpleNamespace(Busy=False),
            find=lambda control_id: menu,
        )

        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[snapshot, popup_snapshot],
        ):
            result = _save_existing_sales_organization_1010(session)

        self.assertTrue(result["unexpected_popup"])
        self.assertEqual("Unknown", result["popup_details"][0]["window_title"])

    def test_sales_org_save_reuses_exact_approved_transport_request(self):
        snapshot = self._sales_org_pending_save_snapshot()
        transport_popup = {
            "id": "/app/con[0]/ses[0]/wnd[1]",
            "window_title": "Demande : ordre du Customizing",
            "input_fields": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR",
                    "type": "GuiCTextField",
                    "changeable": True,
                },
                {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT"},
            ],
            "buttons": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]",
                    "type": "GuiButton",
                    "changeable": True,
                    "visible": True,
                }
            ],
        }
        transport_snapshot = self._sales_org_pending_save_snapshot(
            popups=[transport_popup]
        )
        menu = SimpleNamespace(
            Type="GuiMenu",
            Text="Sauvegarder",
            Changeable=True,
            select=lambda: None,
        )
        transport_field = SimpleNamespace(
            Type="GuiCTextField", Changeable=True, Text=""
        )
        session = SimpleNamespace(
            raw=SimpleNamespace(Busy=False),
            find=lambda control_id: (
                transport_field
                if control_id.endswith("ctxtKO008-TRKORR")
                else menu
            ),
        )

        with (
            patch(
                "src.provisioning.sap_gui_backend.inspect_screen",
                side_effect=[snapshot, transport_snapshot, snapshot],
            ),
            patch("src.provisioning.sap_gui_backend._press_exact") as press,
        ):
            result = _save_existing_sales_organization_1010(session)

        self.assertTrue(result["accepted"])
        self.assertEqual("A4HK908422", result["transport_request_id"])
        self.assertEqual("A4HK908422", transport_field.Text)
        press.assert_called_once_with(
            session, "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
        )

    def test_sales_org_save_transport_popup_without_field_is_unexpected(self):
        snapshot = self._sales_org_pending_save_snapshot()
        lookalike_popup = {
            "id": "/app/con[0]/ses[0]/wnd[1]",
            "window_title": "Demande : ordre du Customizing",
            "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtOTHER"}],
        }
        lookalike_snapshot = self._sales_org_pending_save_snapshot(
            popups=[lookalike_popup]
        )
        menu = SimpleNamespace(
            Type="GuiMenu",
            Text="Sauvegarder",
            Changeable=True,
            select=lambda: None,
        )
        session = SimpleNamespace(
            raw=SimpleNamespace(Busy=False),
            find=lambda control_id: menu,
        )

        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[snapshot, lookalike_snapshot],
        ):
            result = _save_existing_sales_organization_1010(session)

        self.assertTrue(result["unexpected_popup"])
        self.assertNotIn("transport_request", result)

    def test_sales_org_save_transport_popup_with_extra_popup_is_unexpected(self):
        snapshot = self._sales_org_pending_save_snapshot()
        transport_popup = {
            "id": "/app/con[0]/ses[0]/wnd[1]",
            "window_title": "Demande : ordre du Customizing",
            "input_fields": [
                {"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR"},
            ],
        }
        extra_popup = {"id": "/app/con[0]/ses[0]/wnd[2]", "window_title": "Extra"}
        mixed_snapshot = self._sales_org_pending_save_snapshot(
            popups=[transport_popup, extra_popup]
        )
        menu = SimpleNamespace(
            Type="GuiMenu",
            Text="Sauvegarder",
            Changeable=True,
            select=lambda: None,
        )
        session = SimpleNamespace(
            raw=SimpleNamespace(Busy=False),
            find=lambda control_id: menu,
        )

        with patch(
            "src.provisioning.sap_gui_backend.inspect_screen",
            side_effect=[snapshot, mixed_snapshot],
        ):
            result = _save_existing_sales_organization_1010(session)

        self.assertTrue(result["unexpected_popup"])
        self.assertNotIn("transport_request", result)

    def test_sales_org_provision_rejects_unexpected_template(self):
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()

        with self.assertRaisesRegex(
            ActionBlockedError, "technical template mismatch"
        ):
            execute_runner_action(
                session,
                self._sales_org_request(
                    "PROVISION", values={"technical_template": "BE01"}
                ),
            )

    def test_sales_org_readback_verifies_existence_only_scope(self):
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()
        with patch(
            "src.provisioning.sap_gui_backend._lookup_sales_organization_1010",
            return_value={
                "state": "EXISTS",
                "evidence": {"result": "FOUND", "found_row": 27},
            },
        ):
            result = execute_runner_action(
                session, self._sales_org_request("READBACK")
            )

        self.assertTrue(result["verified"])
        self.assertEqual("EXISTS", result["state"])
        self.assertEqual("EXISTENCE", result["verification_scope"])
        self.assertEqual(
            {"sales_organization": "1010"},
            EXPECTED_TARGETS["SALES_ORGANIZATION_1010"],
        )
        self.assertEqual({"sales_organization": "1010"}, result["object"])
        self.assertEqual({"result": "FOUND", "found_row": 27}, result["evidence"])
        self.assertIsNone(result["reason"])

    def test_sales_org_readback_is_not_verified_when_lookup_is_not_exists(self):
        for state, reason_fragment in (
            ("MISSING", "not confirmed"),
            ("UNKNOWN", "not confirmed"),
        ):
            with self.subTest(state=state):
                session = type(
                    "Session", (), {"audit": lambda self, *a, **k: None}
                )()
                with patch(
                    "src.provisioning.sap_gui_backend._lookup_sales_organization_1010",
                    return_value={"state": state, "evidence": {}},
                ):
                    result = execute_runner_action(
                        session, self._sales_org_request("READBACK")
                    )

                self.assertFalse(result["verified"])
                self.assertEqual(state, result["state"])
                self.assertIsNone(result["verification_scope"])
                self.assertIsNone(result["object"])
                self.assertIn(reason_fragment, result["reason"])

    def test_sales_org_readback_engine_reaches_provisioned_verified(self):
        # End-to-end: LOOKUP=MISSING, PROVISION=accepted, READBACK=EXISTS must
        # reach PROVISIONED_VERIFIED through the real SapGuiPhase5Backend.
        from src.provisioning.sap_gui_backend import SapGuiPhase5Backend

        responses = {
            "LOOKUP": response({"state": "MISSING"}),
            "PROVISION": response(
                {
                    "accepted": True,
                    "target": "1010",
                    "save_action": "/app/con[0]/ses[0]/wnd[0]/mbar/menu[0]/menu[5]",
                }
            ),
            "READBACK": response(
                {
                    "verified": True,
                    "state": "EXISTS",
                    "object": {"sales_organization": "1010"},
                }
            ),
        }
        calls = []

        def sender(phase, params):
            calls.append((params["operation"], phase))
            return responses[phase]

        backend = SapGuiPhase5Backend(sender=sender)
        engine = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        )
        company = engine.ensure_company_code()
        self.assertEqual("PROVISIONED_VERIFIED", company.status)
        result = engine.ensure_sales_org(company)
        self.assertEqual("PROVISIONED_VERIFIED", result.status)
        sales_org_calls = [
            phase for operation, phase in calls if operation == "SALES_ORGANIZATION_1010"
        ]
        self.assertEqual(["LOOKUP", "PROVISION", "READBACK"], sales_org_calls)

    def _assignment_request(self, operation, phase, values=None):
        return {
            "params": {
                "operation": operation,
                "phase": phase,
                "target": EXPECTED_TARGETS[operation],
                "values": values or {},
            }
        }

    @staticmethod
    def _assignment_rows(operation, count=34):
        fields = PHASE5_ASSIGNMENT_TABLE_SEARCHES[operation]["fields"]
        rows = [
            {
                name: f"{field['value']}-other-{index}"
                for name, field in fields.items()
            }
            for index in range(count)
        ]
        return rows

    def test_assignment_lookup_scans_exact_tuple_across_scrolled_pages(self):
        for operation, contract in PHASE5_ASSIGNMENT_TABLE_SEARCHES.items():
            with self.subTest(operation=operation):
                values = self._assignment_rows(operation)
                values[27] = {
                    name: field["value"]
                    for name, field in contract["fields"].items()
                }
                session = FakeAssignmentSession(operation, values, position=8)

                result = find_phase5_assignment_table_row(
                    session, operation, EXPECTED_TARGETS[operation]
                )["table_row_search"]

                self.assertEqual("FOUND", result["result"])
                self.assertEqual(27, result["found_row"])
                self.assertEqual(34, result["rows_read"])
                self.assertEqual([0, 13, 21], result["visited_scroll_positions"])
                self.assertGreater(session.table_acquisitions, 3)
                self.assertEqual(
                    ["FIND_TABLE_VALUE"],
                    [action for action, _ in session.audit_events],
                )

    def test_assignment_lookup_confirms_missing_only_after_complete_scan(self):
        operation = "SALES_ORG_1010_TO_COMPANY_CODE_1010"
        session = FakeAssignmentSession(operation, self._assignment_rows(operation))

        result = find_phase5_assignment_table_row(
            session, operation, EXPECTED_TARGETS[operation]
        )["table_row_search"]

        self.assertEqual("CONFIRMED_NOT_FOUND", result["result"])
        self.assertEqual(34, result["rows_read"])
        self.assertEqual([0, 13, 21], result["visited_scroll_positions"])

    def test_assignment_lookup_returns_unknown_for_unreadable_cell(self):
        operation = "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010"
        session = FakeAssignmentSession(
            operation,
            self._assignment_rows(operation),
            missing_cells={("distribution_channel", 5)},
        )

        result = find_phase5_assignment_table_row(
            session, operation, EXPECTED_TARGETS[operation]
        )["table_row_search"]

        self.assertEqual("UNKNOWN", result["result"])
        self.assertEqual(5, result["rows_read"])
        self.assertIn("not deterministically readable", result["reason"])

    def test_assignment_lookup_rejects_wrong_target_and_screen_identity(self):
        operation = "DIVISION_00_TO_SALES_ORG_1010"
        session = FakeAssignmentSession(operation, self._assignment_rows(operation))

        with self.assertRaisesRegex(ActionBlockedError, "context mismatch"):
            find_phase5_assignment_table_row(
                session, operation, {"sales_division": "01", "sales_organization": "1010"}
            )

        session.raw.Info.Program = "SAPL0ORG"
        with self.assertRaisesRegex(ActionBlockedError, "exact SIMG"):
            find_phase5_assignment_table_row(
                session, operation, EXPECTED_TARGETS[operation]
            )

        session.raw.Info.Program = "SAPLCUST_ASSIGN_SD"
        session.transaction = "VA01"
        with self.assertRaisesRegex(ActionBlockedError, "exact SIMG"):
            find_phase5_assignment_table_row(
                session, operation, EXPECTED_TARGETS[operation]
            )

    def test_assignment_lookup_returns_unknown_for_wrong_control_id_or_type(self):
        operation = "SALES_ORG_1010_TO_COMPANY_CODE_1010"
        rows = self._assignment_rows(operation)
        for options in (
            {"table_id_matches": False},
            {"table_type": "GuiShell"},
            {"wrong_cell_type": ("company_code", 0)},
        ):
            with self.subTest(options=options):
                session = FakeAssignmentSession(operation, rows, **options)

                result = find_phase5_assignment_table_row(
                    session, operation, EXPECTED_TARGETS[operation]
                )["table_row_search"]

                self.assertEqual("UNKNOWN", result["result"])
                self.assertTrue(result["reason"])

    def test_assignment_lookup_routes_through_captured_img_nodes(self):
        class IntegratedSession:
            def __init__(self):
                self.transaction = "V_TVKO"
                self.raw = type(
                    "Raw",
                    (),
                    {
                        "Info": type("Info", (), {"Program": "SAPL0ORG"})(),
                    },
                )()
                self.navigation_calls = []

            @property
            def identity(self):
                return {"transaction": self.transaction}

            def audit(self, *args, **kwargs):
                return None

        session = IntegratedSession()

        def open_transaction(current, transaction):
            self.assertIs(current, session)
            self.assertEqual("SPRO", transaction)
            session.transaction = "SPRO"

        def press_exact(current, control_id):
            self.assertIs(current, session)
            self.assertEqual("wnd[0]/tbar[1]/btn[5]", control_id)
            session.transaction = "SIMG"
            session.raw.Info.Program = "SAPLSHI01"

        def navigate(current, params):
            self.assertIs(current, session)
            session.navigation_calls.append(params)
            if params["navigation_operation"] == "OPEN_IMG_ACTIVITY":
                session.raw.Info.Program = "SAPLCUST_ASSIGN_SD"
            return {}

        operation = "SALES_ORG_1010_TO_COMPANY_CODE_1010"
        with (
            patch("src.provisioning.sap_gui_backend.open_transaction", side_effect=open_transaction),
            patch("src.provisioning.sap_gui_backend._press_exact", side_effect=press_exact),
            patch("src.provisioning.sap_gui_backend.navigate", side_effect=navigate),
            patch(
                "src.provisioning.sap_gui_backend.find_phase5_assignment_table_row",
                return_value={
                    "table_row_search": {
                        "result": "FOUND",
                        "found_row": 2,
                    }
                },
            ) as scan,
        ):
            result = _lookup_assignment(session, operation)

        self.assertEqual("EXISTS", result["state"])
        scan.assert_called_once_with(session, operation, EXPECTED_TARGETS[operation])
        self.assertEqual(4, len(session.navigation_calls))
        self.assertEqual(
            ["EXPAND_TREE_NODE", "EXPAND_TREE_NODE", "EXPAND_TREE_NODE", "OPEN_IMG_ACTIVITY"],
            [call["navigation_operation"] for call in session.navigation_calls],
        )
        self.assertEqual(ASSIGNMENT_IMG_NODES, tuple(
            (call["node_key"], call["expected_text"])
            for call in session.navigation_calls[:3]
        ))
        leaf_key, leaf_text = ASSIGNMENT_IMG_LEAVES[operation]
        self.assertEqual(leaf_key, session.navigation_calls[-1]["node_key"])
        self.assertEqual(leaf_text, session.navigation_calls[-1]["expected_text"])
        self.assertEqual("2", session.navigation_calls[-1]["item_column"])

    def test_assignment_readback_verifies_only_a_found_pair(self):
        operation = "DIVISION_00_TO_SALES_ORG_1010"
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()
        with patch(
            "src.provisioning.sap_gui_backend._lookup_assignment",
            return_value={"state": "EXISTS", "evidence": {"found_row": 4}},
        ):
            result = execute_runner_action(
                session, self._assignment_request(operation, "READBACK")
            )

        self.assertTrue(result["verified"])
        self.assertEqual(EXPECTED_TARGETS[operation], result["object"])
        self.assertEqual({"found_row": 4}, result["evidence"])

    def test_za01_copy_probe_requires_absence_and_observed_cs_contract(self):
        params = {"operation": "S4615_SALES_TYPE_ZA01", "phase": "COPY_DIALOG_INSPECT", "target": {"sales_order_type": "ZA01"}, "values": {}}
        session = Mock()
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK"
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[6]"
        table = Mock(Id=table_id, Type="GuiTableControl")
        button = Mock(Id=button_id, Type="GuiButton", Tooltip="Copier sous...   (F6)")
        session.find.side_effect = lambda control_id: table if control_id == table_id else button if control_id == button_id else None
        observed = {"txtV_TVAK-AUART": "CS", "txtV_TVAK-BEZEI": "Cmde client standard", "ctxtV_TVAK-VBTYP": "C", "ctxtV_TVAK-LFARV": "LF", "ctxtV_TVAK-FKARV": "F2", "ctxtV_TVAK-FKARA": "F2"}
        detail = {"input_fields": [{"id": f"/usr/{key}", "text": value} for key, value in observed.items()]}
        overview = {"transaction": "VOV8", "program": "SAPL080O", "screen_number": "1010", "window_title": 'Modifier vue "Gestion des types de commande client" : synthèse'}
        with patch("src.provisioning.sap_gui_backend.find_s4615_sales_type", return_value={"sales_type_search": {"result": "CONFIRMED_NOT_FOUND"}}), patch("src.provisioning.sap_gui_backend.display_s4615_sales_reference", return_value={"source_row": 190, "snapshot": detail}), patch("src.provisioning.sap_gui_backend.back"), patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[overview, {"window_title": "copy form"}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, {"params": params})
        self.assertEqual("CS", result["source"])
        self.assertFalse(result["saved"])
        button.press.assert_called_once_with()
        table.GetAbsoluteRow.assert_called_once_with(190)
        with patch("src.provisioning.sap_gui_backend.find_s4615_sales_type", return_value={"sales_type_search": {"result": "UNKNOWN"}}):
            with self.assertRaisesRegex(ActionBlockedError, "confirmed absence"):
                execute_runner_action(session, {"params": params})

    def test_za01_unsaved_fields_change_only_the_four_approved_values(self):
        values = {"sales_order_type": "ZA01", "description": "cde Foire 01", "delivery_billing_type": "ZF01", "order_billing_type": "ZF01"}
        request = {"params": {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": values}}
        base = "/app/con[0]/ses[0]/wnd[0]/usr/"
        source = {"txtV_TVAK-AUART": ("GuiTextField", "CS", "ZA01"), "txtV_TVAK-BEZEI": ("GuiTextField", "Cmde client standard", "cde Foire 01"), "ctxtV_TVAK-FKARV": ("GuiCTextField", "F2", "ZF01"), "ctxtV_TVAK-FKARA": ("GuiCTextField", "F2", "ZF01")}
        controls = {base + key: Mock(Id=base + key, Type=kind, Text=before) for key, (kind, before, _) in source.items()}
        session = Mock()
        session.find.side_effect = lambda control_id: controls[control_id]
        snapshot = {"transaction": "VOV8", "program": "SAPL080O", "screen_number": "1011", "window_title": 'Modifier vue "Gestion des types de commande client" : détail ensemble', "popups": [], "status_bar": {"text": "Indiquez les entrées cibles."}, "input_fields": [{"id": base + key, "type": kind, "text": before, "changeable": True} for key, (kind, before, _) in source.items()]}
        def inspect(_):
            if all(control.Text == before for key, (_, before, _) in source.items() for control in [controls[base + key]]):
                return snapshot
            return {**snapshot, "input_fields": [{"id": control_id, "text": control.Text} for control_id, control in controls.items()]}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=inspect):
            result = execute_runner_action(session, request)
        self.assertFalse(result["saved"])
        self.assertEqual({key: after for key, (_, _, after) in source.items()}, {key: controls[base + key].Text for key in source})
        with self.assertRaisesRegex(ActionBlockedError, "four Book-confirmed"):
            execute_runner_action(session, {"params": {**request["params"], "values": {**values, "extra": "1"}}})

    def test_za01_enter_requires_exact_unsaved_target_and_never_saves(self):
        base = "/app/con[0]/ses[0]/wnd[0]/usr/"
        values = {"txtV_TVAK-AUART": "ZA01", "txtV_TVAK-BEZEI": "cde Foire 01", "ctxtV_TVAK-FKARV": "ZF01", "ctxtV_TVAK-FKARA": "ZF01"}
        snapshot = {"transaction": "VOV8", "program": "SAPL080O", "screen_number": "1011", "window_title": 'Modifier vue "Gestion des types de commande client" : détail ensemble', "popups": [], "status_bar": {"text": "Indiquez les entrées cibles."}, "input_fields": [{"id": base + key, "text": value} for key, value in values.items()]}
        request = {"params": {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": {"confirm_target": "ZA01"}}}
        window_id = "/app/con[0]/ses[0]/wnd[0]"
        window = Mock(Id=window_id, Type="GuiMainWindow")
        session = Mock()
        session.find.return_value = window
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[snapshot, {"popups": []}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, request)
        self.assertFalse(result["saved"])
        window.sendVKey.assert_called_once_with(0)
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={**snapshot, "input_fields": [{"id": base + "txtV_TVAK-AUART", "text": "CS"}]}):
            with self.assertRaisesRegex(ActionBlockedError, "exact observed unsaved"):
                execute_runner_action(session, request)

    def test_za01_copy_control_yes_requires_exact_group_specific_popup(self):
        button_id = "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-OPTION1"
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Entrées dépendantes pour pilotage copies", "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-DIAGNOSE1", "text": "Type doc. de vente : ZA01 -cde Foire 01 -"}, {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-TEXTLINE1", "text": "L'entrée concerne-t-elle aussi le pilotage copies ?"}], "buttons": [{"id": button_id, "type": "GuiButton", "text": "Oui"}]}
        snapshot = {"transaction": "VOV8", "program": "SAPLSPO1", "screen_number": "300", "popups": [popup]}
        params = {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": {"copy_control": "YES"}}
        button = Mock(Id=button_id, Type="GuiButton", Text="Oui")
        session = Mock()
        session.find.return_value = button
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[snapshot, {"popups": []}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, {"params": params})
        self.assertEqual("COPIED_FROM_CS", result["copy_control"])
        self.assertFalse(result["saved"])
        button.press.assert_called_once_with()
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={**snapshot, "popups": [{**popup, "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtSPOP-DIAGNOSE1", "text": "Type doc. de vente : OTHER -"}]}]}):
            with self.assertRaisesRegex(ActionBlockedError, "content mismatch"):
                execute_runner_action(session, {"params": params})

    def test_za01_save_requires_exact_pending_row_and_evidenced_button(self):
        button_id = "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"
        snapshot = {"transaction": "VOV8", "program": "SAPL080O", "screen_number": "1010", "popups": [], "status_bar": {"text": "Nombre d'entrées copiées (traductions y compris) : 1"}, "tables": [{"id": "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL080OTCTRL_V_TVAK", "visible_rows": [{"values": [{"column": "0", "text": "ZA01"}, {"column": "1", "text": "cde Foire 01"}]}]}], "buttons": [{"id": button_id, "type": "GuiButton", "text": "Sauvegarder"}]}
        request = {"params": {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": {"save_pending": "ZA01"}}}
        button = Mock(Id=button_id, Type="GuiButton", Text="Sauvegarder")
        session = Mock()
        session.find.return_value = button
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[snapshot, {"status_bar": {"text": "saved"}}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, request)
        self.assertFalse(result["verified"])
        button.press.assert_called_once_with()
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={**snapshot, "tables": []}):
            with self.assertRaisesRegex(ActionBlockedError, "exact pending"):
                execute_runner_action(session, request)

    def test_za01_transport_reuses_only_approved_request(self):
        button_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Demande : ordre du Customizing", "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR", "text": "A4HK908422"}, {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-OBJ_NAME", "text": "V_TVAK"}, {"id": "/app/con[0]/ses[0]/wnd[1]/usr/txtKO008-AS4TEXT", "text": "S4615 Training Setup"}], "buttons": [{"id": button_id, "type": "GuiButton", "tooltip": "Suite   (Entrée)"}]}
        snapshot = {"transaction": "VOV8", "program": "SAPLSTRD", "screen_number": "300", "popups": [popup]}
        request = {"params": {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": {"confirm_transport": "A4HK908422"}}}
        button = Mock(Id=button_id, Type="GuiButton", Tooltip="Suite   (Entrée)")
        session = Mock()
        session.find.return_value = button
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[snapshot, {"popups": []}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, request)
        self.assertFalse(result["verified"])
        button.press.assert_called_once_with()
        bad_popup = {**popup, "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[1]/usr/ctxtKO008-TRKORR", "text": "OTHER"}]}
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={**snapshot, "popups": [bad_popup]}):
            with self.assertRaisesRegex(ActionBlockedError, "request, object"):
                execute_runner_action(session, request)

    def test_za01_saved_information_is_closed_only_after_confirmed_save(self):
        button_id = "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]"
        labels = ["T184", "TVAKZ", "TVASP", "TVCPA", "TVCPF", "TVCPL"]
        popup = {"id": "/app/con[0]/ses[0]/wnd[1]", "window_title": "Gestion des vues de table : écran initial", "input_fields": [], "labels": [{"text": value} for value in labels], "buttons": [{"id": button_id, "type": "GuiButton", "tooltip": "Weiter   (Entrée)"}]}
        snapshot = {"transaction": "VOV8", "program": "SAPMSSY0", "status_bar": {"text": "Données sauvegardées"}, "popups": [popup]}
        request = {"params": {"operation": "S4615_SALES_TYPE_ZA01", "phase": "PROVISION", "target": {"sales_order_type": "ZA01"}, "values": {"close_saved_info": "ZA01"}}}
        button = Mock(Id=button_id, Type="GuiButton", Tooltip="Weiter   (Entrée)")
        session = Mock()
        session.find.return_value = button
        with patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[snapshot, {"popups": []}]), patch("src.provisioning.sap_gui_backend._wait_not_busy"):
            result = execute_runner_action(session, request)
        self.assertFalse(result["verified"])
        button.press.assert_called_once_with()
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value={**snapshot, "status_bar": {"text": ""}}):
            with self.assertRaisesRegex(ActionBlockedError, "post-save state"):
                execute_runner_action(session, request)

    def test_assignment_write_uses_only_exact_existing_row_contract(self):
        operation = "SALES_ORG_1010_TO_COMPANY_CODE_1010"
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()

        with patch(
            "src.provisioning.sap_gui_backend._provision_assignment_existing_row",
            return_value={"accepted": True, "target": EXPECTED_TARGETS[operation]},
        ) as provision:
            result = execute_runner_action(
                session, self._assignment_request(operation, "PROVISION")
            )

        self.assertTrue(result["accepted"])
        provision.assert_called_once_with(session, operation)

    def test_engine_continues_after_assignment_write_contract_blockers(self):
        responses = [
            response({"state": "EXISTS"}),
            response({"state": "EXISTS"}),
            response({"state": "MISSING"}),
            response({
                "provisioning_blocked": True,
                "reason": "assignment add-row/save/transport contract missing",
            }),
            response({"state": "EXISTS"}),
            response({"state": "MISSING"}),
            response({
                "provisioning_blocked": True,
                "reason": "division add-row/save/transport contract missing",
            }),
            response({"state": "UNKNOWN", "reason": "no customer GUI lookup contract"}),
            response({"state": "UNKNOWN", "reason": "no product GUI lookup contract"}),
        ]
        backend, sender = self.backend(responses)

        result = Phase5ProvisioningEngine(
            backend=backend, decisions=load_seed(), execute=True
        ).plan(include_book_data=True)

        self.assertEqual(
            [
                "COMPANY_CODE_1010",
                "SALES_ORGANIZATION_1010",
                "SALES_ORG_1010_TO_COMPANY_CODE_1010",
                "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
                "DIVISION_00_TO_SALES_ORG_1010",
                "CUSTOMER_C615_D00",
                "PRODUCT_P615_400",
            ],
            [item["operation"] for item in result["results"]],
        )
        self.assertEqual("BLOCKED_UNSUPPORTED_PROVISIONING", result["results"][2]["status"])
        self.assertEqual("SKIPPED_EXISTS", result["results"][3]["status"])
        self.assertEqual("BLOCKED_UNSUPPORTED_PROVISIONING", result["results"][4]["status"])
        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", result["results"][5]["status"])
        self.assertEqual("BLOCKED_LIVE_READ_REQUIRED", result["results"][6]["status"])
        self.assertEqual(9, len(sender.calls))
        self.assertEqual(
            ["LOOKUP", "LOOKUP", "LOOKUP", "PROVISION", "LOOKUP",
             "LOOKUP", "PROVISION", "LOOKUP", "LOOKUP"],
            [phase for phase, _ in sender.calls],
        )

    def test_customer_and_product_fail_closed_without_gui_contracts(self):
        session = type("Session", (), {"audit": lambda self, *args, **kwargs: None})()
        for operation in ("CUSTOMER_C615_D00", "PRODUCT_P615_400"):
            with self.subTest(operation=operation):
                result = execute_runner_action(
                    session,
                    {
                        "params": {
                            "operation": operation,
                            "phase": "LOOKUP",
                            "target": EXPECTED_TARGETS[operation],
                            "values": {},
                        }
                    },
                )
                self.assertEqual("UNKNOWN", result["state"])
                self.assertIn("no captured SAP GUI object lookup", result["reason"])

    def test_execute_script_exposes_book_data_as_explicit_opt_in(self):
        arguments = phase5_execute_parser().parse_args(["--include-book-data"])
        self.assertTrue(arguments.include_book_data)
        self.assertFalse(phase5_execute_parser().parse_args([]).include_book_data)


if __name__ == "__main__":
    unittest.main()
