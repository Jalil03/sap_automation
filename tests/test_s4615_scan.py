import unittest
from unittest.mock import patch

from src.sap_gui_bridge.errors import ActionBlockedError
from src.sap_gui_bridge.protocol import validate_request
from src.sap_gui_bridge.s4615_scan import GRID_ID, OVL2_ID, scan_s4615_customizing


class Grid:
    Id = GRID_ID
    RowCount = 3
    VisibleRowCount = 2
    FirstVisibleRow = 0

    def GetCellValue(self, index, column):
        return {"WERKS": f"{index:04d}", "BWKEY": f"{index:04d}",
                "VSTEL": "1010", "LAND1": "BE"}.get(column, "")


class Scrollbar:
    Position = 0
    Maximum = 1


class Table:
    Id = OVL2_ID
    RowCount = 3
    VisibleRowCount = 2

    def __init__(self):
        self.VerticalScrollbar = Scrollbar()


class Session:
    def __init__(self, control):
        self.control = control
        self.find_count = 0
        self.actions = []

    def find(self, control_id):
        self.find_count += 1
        assert control_id == self.control.Id
        return self.control

    def audit(self, action, **kwargs):
        self.actions.append(action)


def grid_snapshot(grid, target="T001W"):
    rows = []
    for index in range(grid.FirstVisibleRow, min(grid.FirstVisibleRow + grid.VisibleRowCount, grid.RowCount)):
        rows.append({"index": index, "values": [{"column": "WERKS", "text": f"{index:04d}"}]})
    return {
        "transaction": "SE16N", "program": "SAPLSE16N", "screen_number": "200",
        "window_title": f"{target} : entries", "popups": [], "truncated": False,
        "input_fields": [{"id": "/app/con[0]/ses[0]/wnd[0]/usr/txtGD-TAB", "text": target}],
        "tables": [{"id": GRID_ID, "type": "GuiShell", "subtype": "GridView", "visible_rows": rows}],
    }


def ovl2_snapshot(table):
    rows = []
    for relative in range(min(table.VisibleRowCount, table.RowCount - table.VerticalScrollbar.Position)):
        absolute = table.VerticalScrollbar.Position + relative
        rows.append({"index": relative, "values": [
            {"column": "0", "text": "01"}, {"column": "1", "text": "0001"},
            {"column": "2", "text": f"{absolute:04d}"}, {"column": "3", "text": "1010"},
        ]})
    return {
        "transaction": "OVL2", "program": "SAPL0VVW", "screen_number": "1234",
        "window_title": "Shipping determination", "popups": [], "truncated": False,
        "tables": [{"id": OVL2_ID, "type": "GuiTableControl", "visible_rows": rows}],
    }


class S4615ScanTests(unittest.TestCase):
    def test_grid_reads_all_absolute_rows_and_reacquires(self):
        grid = Grid()
        session = Session(grid)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: grid_snapshot(grid)):
            result = scan_s4615_customizing(session, "T001W")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual([0, 1, 2], [row["index"] for row in result["rows"]])
        self.assertGreater(session.find_count, 2)
        self.assertEqual([], result["visited_scroll_positions"])

    def test_grid_blank_rows_do_not_hide_later_populated_rows(self):
        grid = Grid()
        grid.RowCount = 4
        original = grid.GetCellValue
        grid.GetCellValue = lambda index, column: "" if index == 2 else original(index, column)
        session = Session(grid)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: grid_snapshot(grid)):
            result = scan_s4615_customizing(session, "T001W")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual([0, 1, 3], [row["index"] for row in result["rows"]])
        self.assertEqual(1, result["blank_slots"])

    def test_shipping_point_scan_uses_exact_tvst_key(self):
        grid = Grid()
        grid.GetCellValue = lambda index, column: "1010" if column == "VSTEL" and index == 1 else ""
        session = Session(grid)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: grid_snapshot(grid, "TVST")):
            result = scan_s4615_customizing(session, "TVST")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual([{"index": 1, "VSTEL": "1010"}], result["rows"])

    def test_tvst_is_read_only_allowlisted(self):
        request = {"request_id": "123e4567-e89b-12d3-a456-426614174000", "mode": "READ",
                   "action": "SCAN_S4615_CUSTOMIZING", "params": {"object": "TVST"}}
        self.assertEqual("TVST", validate_request(request)["params"]["object"])
        request["mode"] = "EXECUTE"
        with self.assertRaises(Exception):
            validate_request(request)

    def test_t000_scan_reads_client_currency_without_write(self):
        grid = Grid()
        grid.RowCount = 1
        grid.VisibleRowCount = 1
        grid.GetCellValue = lambda index, column: {"MANDT": "600", "MWAER": "USD"}.get(column, "")
        session = Session(grid)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: grid_snapshot(grid, "T000")):
            result = scan_s4615_customizing(session, "T000")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual([{"index": 0, "MANDT": "600", "MWAER": "USD"}], result["rows"])
        self.assertEqual(["SCAN_S4615_CUSTOMIZING"], session.actions)

    def test_ovl2_scroll_reads_all_rows(self):
        table = Table()
        session = Session(table)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: ovl2_snapshot(table)):
            result = scan_s4615_customizing(session, "OVL2")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual("1010", result["rows"][2]["VSTEL"])

    def test_ovl2_blank_template_slots_are_counted_separately(self):
        table = Table()
        session = Session(table)
        def snapshot(_):
            value = ovl2_snapshot(table)
            for row in value["tables"][0]["visible_rows"]:
                if table.VerticalScrollbar.Position + row["index"] == 2:
                    row["values"] = []
            return value
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=snapshot):
            result = scan_s4615_customizing(session, "OVL2")
        self.assertEqual("COMPLETE", result["result"])
        self.assertEqual(3, result["slots_inspected"])
        self.assertEqual(2, result["rows_read"])
        self.assertEqual(1, result["blank_slots"])

    def test_wrong_screen_and_unrelated_object_fail_closed(self):
        grid = Grid()
        session = Session(grid)
        with patch("src.sap_gui_bridge.s4615_scan.inspect_screen", side_effect=lambda _: grid_snapshot(grid, "T000")):
            with self.assertRaises(ActionBlockedError):
                scan_s4615_customizing(session, "T001W")
        with self.assertRaises(ActionBlockedError):
            scan_s4615_customizing(session, "UNKNOWN")

    def test_protocol_rejects_scan_in_execute(self):
        request = {"request_id": "123e4567-e89b-12d3-a456-426614174000", "mode": "EXECUTE",
                   "action": "SCAN_S4615_CUSTOMIZING", "params": {"object": "TVKWZ"}}
        with self.assertRaises(Exception):
            validate_request(request)


if __name__ == "__main__":
    unittest.main()
