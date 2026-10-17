import unittest
import uuid
from types import SimpleNamespace
from unittest.mock import patch

from src.provisioning.sap_gui_backend import (
    _lookup_vov4,
    _save_vov4_pending_row,
    _vov4_contract,
)
from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.protocol import validate_request


class Scrollbar:
    def __init__(self, maximum, stalled=False):
        self.Maximum = maximum
        self._position = 0
        self.stalled = stalled

    @property
    def Position(self):
        return self._position

    @Position.setter
    def Position(self, value):
        if not self.stalled:
            self._position = min(max(int(value), 0), self.Maximum)


class Table:
    Type = "GuiTableControl"

    def __init__(self, session):
        self.session = session
        self.RowCount = len(session.rows)
        self.VisibleRowCount = 2
        self.VerticalScrollbar = session.scrollbar


class Cell:
    Type = "GuiCTextField"

    def __init__(self, text):
        self.Text = text


class Session:
    def __init__(self, rows, stalled=False):
        self.rows = rows
        self.scrollbar = Scrollbar(max(0, len(rows) - 2), stalled=stalled)
        self.identity = {
            "system": "A4H", "client": "600", "user": "ABDELJ", "transaction": "VOV4"
        }
        self.raw = SimpleNamespace(
            Busy=False,
            Info=SimpleNamespace(Program="SAPL080O", ScreenNumber="1002"),
        )

    def validate_identity(self):
        return None

    def find(self, control_id):
        contract = _vov4_contract("S4615_BV_CB04")
        if control_id == contract["table_id"]:
            return Table(self)
        for logical, field in contract["fields"].items():
            prefix = f"{contract['table_id']}/ctxtV_T184-{field['name']}[{field['column']},"
            if control_id.startswith(prefix) and control_id.endswith("]"):
                relative = int(control_id[len(prefix):-1])
                absolute = self.scrollbar.Position + relative
                if absolute >= len(self.rows):
                    raise KeyError(control_id)
                return Cell(self.rows[absolute][logical])
        raise KeyError(control_id)


def visible_snapshot(contract, rows, *, status="Nombre d'entrées copiées : 1"):
    visible_rows = []
    for index, row in enumerate(rows):
        visible_rows.append({
            "index": index,
            "values": [
                {"column": str(field["column"]), "text": row[logical]}
                for logical, field in contract["fields"].items()
                if row[logical]
            ],
        })
    return {
        "popups": [],
        "status_bar": {"message_type": "S", "text": status},
        "tables": [{"id": contract["table_id"], "visible_rows": visible_rows}],
    }


class Vov4ContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = _vov4_contract("S4615_BV_CB04")

    def test_lookup_exists(self):
        result = _lookup_vov4(Session([self.contract["source"], self.contract["target"]]), self.contract)
        self.assertEqual("EXISTS", result["state"])
        self.assertEqual([1], result["evidence"]["target_rows"])

    def test_live_mojibake_pending_status_is_detected(self):
        session = SimpleNamespace()
        before = visible_snapshot(
            self.contract,
            [self.contract["target"]],
            status="Nombre d'entrÃ©es copiÃ©es : 1",
        )
        saved = {
            "popups": [],
            "status_bar": {"message_type": "S", "text": "Données sauvegardées"},
        }
        with (
            patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[before, saved]),
            patch("src.provisioning.sap_gui_backend._press_exact"),
            patch("src.provisioning.sap_gui_backend.open_transaction"),
            patch(
                "src.provisioning.sap_gui_backend._lookup_vov4",
                return_value={"state": "EXISTS", "evidence": {}},
            ),
        ):
            result = _save_vov4_pending_row(session, self.contract)
        self.assertTrue(result["accepted"])

    def test_complete_lookup_missing(self):
        result = _lookup_vov4(Session([self.contract["source"], self.contract["source"]]), self.contract)
        self.assertEqual("MISSING", result["state"])

    def test_incomplete_lookup_is_unknown(self):
        rows = [self.contract["source"], self.contract["source"], self.contract["source"]]
        result = _lookup_vov4(Session(rows, stalled=True), self.contract)
        self.assertEqual("UNKNOWN", result["state"])

    def test_exact_pending_row_save_requires_independent_readback(self):
        session = SimpleNamespace()
        before = visible_snapshot(self.contract, [self.contract["target"]])
        saved = {"popups": [], "status_bar": {"message_type": "S", "text": "Données sauvegardées"}}
        with (
            patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[before, saved]),
            patch("src.provisioning.sap_gui_backend._press_exact") as pressed,
            patch("src.provisioning.sap_gui_backend.open_transaction") as reopened,
            patch("src.provisioning.sap_gui_backend._lookup_vov4", return_value={"state": "EXISTS", "evidence": {"complete": True}}),
        ):
            result = _save_vov4_pending_row(session, self.contract)
        self.assertTrue(result["accepted"])
        pressed.assert_called_once_with(session, self.contract["save_button_id"])
        reopened.assert_called_once_with(session, "VOV4")

    def test_ambiguous_pending_rows_fail_closed(self):
        snapshot = visible_snapshot(self.contract, [self.contract["target"], self.contract["target"]])
        with patch("src.provisioning.sap_gui_backend.inspect_screen", return_value=snapshot):
            with self.assertRaises(ActionBlockedError):
                _save_vov4_pending_row(SimpleNamespace(), self.contract)

    def test_explicit_resume_accepts_only_one_exact_visible_target(self):
        session = SimpleNamespace()
        before = visible_snapshot(
            self.contract,
            [self.contract["target"]],
            status="",
        )
        saved = {"popups": [], "status_bar": {"message_type": "S", "text": "Saved"}}
        with (
            patch("src.provisioning.sap_gui_backend.inspect_screen", side_effect=[before, saved]),
            patch("src.provisioning.sap_gui_backend._press_exact") as pressed,
            patch("src.provisioning.sap_gui_backend.open_transaction"),
            patch(
                "src.provisioning.sap_gui_backend._lookup_vov4",
                return_value={"state": "EXISTS", "evidence": {}},
            ),
        ):
            result = _save_vov4_pending_row(
                session,
                self.contract,
                require_copy_status=False,
            )
        self.assertTrue(result["accepted"])
        pressed.assert_called_once_with(session, self.contract["save_button_id"])

    def test_protocol_allows_only_allowlisted_vov4_operation(self):
        request = validate_request({
            "request_id": str(uuid.uuid4()),
            "mode": "EXECUTE",
            "action": "PHASE5_OPERATION",
            "params": {
                "operation": "VOV4_ITEM_CATEGORY_DETERMINATION",
                "phase": "PROVISION",
                "target": {"contract_id": "S4615_BV_CB04"},
                "values": {"transport_request": "A4HK908422"},
            },
        })
        self.assertEqual("VOV4_ITEM_CATEGORY_DETERMINATION", request["params"]["operation"])


if __name__ == "__main__":
    unittest.main()
