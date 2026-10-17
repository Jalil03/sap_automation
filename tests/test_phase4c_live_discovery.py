import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from src.sap_gui_bridge.discovery import (
    COMPANY_CODE_LEAF,
    EXPECTED_SAP,
    TREE_CONTROL_ID,
    DiscoveryBlocked,
    Phase4CDiscovery,
)
from src.sap_gui_bridge.navigation import _is_company_code_display_exception
from src.sap_gui_bridge.inspection import _tree_record

DYNAMIC_COMPANY_KEY = "09 current company leaf"

LIVE_TREE_RECORD = {
    "id": TREE_CONTROL_ID,
    "type": "GuiShell",
    "subtype": "Tree",
    "text": None,
    "tooltip": None,
    "visible": True,
    "changeable": False,
}

LIVE_IMG_FIXTURE = [
    ("01  1      1", "Guide d'implÃ©mentation SAP Customizing"),
    ("02  1      6", "Structure de l'entreprise"),
    ("03  2      1", "DÃ©finition"),
    ("04  3      1", "ComptabilitÃ© financiÃ¨re"),
    ("05  4      1", "DÃ©finir sociÃ©tÃ© S/L"),
    ("05  4      2", "DÃ©finir domaine de contrÃ´le des crÃ©dits"),
    ("05  4      3", "Traiter, copier, supprimer, contrÃ´ler sociÃ©tÃ©"),
    ("04  3      4", "Administration des ventes (ADV)"),
    ("03  2      2", "Affectation"),
]


class ObservedImgTree:
    SelectedNode = None

    def __init__(self, nodes=None):
        self.nodes = LIVE_IMG_FIXTURE if nodes is None else nodes

    def GetAllNodeKeys(self):
        return [key for key, _ in self.nodes]

    def GetNodeTextByKey(self, key):
        return dict(self.nodes)[key]

    def IsNodeExpanded(self, key):
        return False


def inspected_tree(nodes=None):
    tree = ObservedImgTree(nodes)
    session = SimpleNamespace(find=lambda control_id: tree)
    return _tree_record(session, LIVE_TREE_RECORD)


class DiscoveryClient:
    def __init__(
        self,
        *,
        company_key=None,
        company_text=None,
        company_parent="FI",
        duplicate_financial_under_definition=False,
        popup=None,
        omit_sales=False,
        no_effect_nodes=None,
    ):
        self.transaction = "SIMG"
        self.expanded = set()
        self.counter = 0
        self.actions = []
        self.popup = popup
        self.omit_sales = omit_sales
        self.no_effect_nodes = set(no_effect_nodes or [])
        self.nodes = [
            ("IMGROOT", "Guide d'implémentation SAP", None),
            ("ROOT", "Structure de l'entreprise", "IMGROOT"),
            ("DEF", "Définition", "ROOT"),
            ("FI", "Comptabilité financière", "DEF"),
            ("SD", "Administration des ventes (ADV)", "DEF"),
            ("ASSIGN", "Affectation", "ROOT"),
            (company_key or DYNAMIC_COMPANY_KEY, company_text or COMPANY_CODE_LEAF["text"], company_parent),
            (
                "SALES_DEF",
                "Définir, copier, supprimer, contrôler org. commerciale",
                "SD",
            ),
            ("SO_CC", "Affecter organisation commerciale à société", "ASSIGN"),
            ("DC_SO", "Affecter canal de distribution à organisation commerciale", "ASSIGN"),
            ("DIV_SO", "Affecter secteur d'activité à organisation commerciale", "ASSIGN"),
            ("FI_TOP", "Comptabilité financière", "IMGROOT"),
        ]
        if duplicate_financial_under_definition:
            self.nodes.append(("FI_DUP", "Comptabilité financière", "DEF"))
        if omit_sales:
            self.nodes = [item for item in self.nodes if item[0] != "SALES_DEF"]

    def _status(self):
        return {**EXPECTED_SAP, "transaction": self.transaction}

    def _spro(self):
        return {
            "transaction": "SPRO",
            "program": "SAPLS_IMG_TOOL_5",
            "window_title": "Customizing : traitement de projet",
            "status_bar": {"text": "", "message_type": ""},
            "popups": [],
            "tree_controls": [],
            "buttons": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]",
                    "type": "GuiButton",
                    "text": "Guide de référence SAP",
                    "tooltip": "Afficher guide de référence SAP",
                }
            ],
            "labels": [],
            "input_fields": [],
            "tables": [],
        }

    def _img(self):
        popup = [self.popup] if self.popup else []
        return {
            "transaction": "SIMG",
            "program": "SAPLSHI01",
            "window_title": "Afficher guide d'implémentation",
            "status_bar": {"text": "", "message_type": ""},
            "popups": popup,
            "tree_controls": [
                {
                    "id": TREE_CONTROL_ID,
                    "type": "GuiShell",
                    "subtype": "Tree",
                    "columns": ["ACTIVITY_LINK"],
                    "native_capabilities": ["ClickLink", "ExpandNode", "SelectNode"],
                    "nodes": [
                        {
                            "key": key,
                            "text": text,
                            "parent_key": parent_key,
                            "level": None,
                            "expanded": key in self.expanded,
                            "selected": False,
                            "extraction_error": None,
                            "expandable": True,
                            "items": [
                                {
                                    "column": "ACTIVITY_LINK",
                                    "type": "5",
                                    "text": text,
                                    "tooltip": None,
                                    "icon": None,
                                }
                            ],
                        }
                        for key, text, parent_key in self.nodes
                    ],
                }
            ],
            "control_ids": [TREE_CONTROL_ID],
            "buttons": [],
            "labels": [],
            "input_fields": [],
            "tables": [],
        }

    def _maintenance(self):
        return {
            "transaction": "SIMG",
            "program": "SAPLSVIM",
            "window_title": "Afficher vue de customizing",
            "status_bar": {"text": "", "message_type": ""},
            "popups": [],
            "tree_controls": [],
            "buttons": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[0]/tbar[1]/btn[5]",
                    "type": "GuiButton",
                    "text": "Nouvelles entrées",
                    "tooltip": None,
                }
            ],
            "labels": [{"id": "lbl1010", "type": "GuiLabel", "text": "1010"}],
            "input_fields": [],
            "tables": [{"id": "tblVIEW", "text": "Maintenance view"}],
        }

    def exchange(self, action, params):
        self.counter += 1
        self.actions.append((action, params))
        request_id = f"request-{self.counter}"
        if action == "STATUS":
            result = self._status()
        elif action == "OPEN_TRANSACTION":
            self.transaction = "SPRO"
            result = self._status()
        elif action == "INSPECT":
            if self.transaction == "SPRO":
                result = self._spro()
            elif self.transaction == "SIMG":
                result = self._img()
            else:
                result = self._maintenance()
        elif action == "NAVIGATE":
            operation = params["navigation_operation"]
            observed = True
            if operation == "PRESS_SAFE_BUTTON":
                self.transaction = "SIMG"
                result = self._img()
            elif operation == "EXPAND_TREE_NODE":
                if params["node_key"] not in self.no_effect_nodes:
                    self.expanded.add(params["node_key"])
                else:
                    observed = False
                result = self._img()
            elif operation == "SELECT_TREE_NODE":
                observed = params["node_key"] not in self.no_effect_nodes
                result = self._img()
            elif operation in {"DOUBLE_CLICK_TREE_NODE", "OPEN_IMG_ACTIVITY"}:
                if params["node_key"] in self.no_effect_nodes:
                    observed = False
                    result = self._img()
                else:
                    self.transaction = "MAINTENANCE"
                    result = self._maintenance()
            else:
                raise AssertionError(operation)
            result["navigation_outcome"] = "SUCCESS" if observed else "NO_OBSERVED_EFFECT"
            result["navigation_effect"] = {"observed": observed}
            if operation == "OPEN_IMG_ACTIVITY":
                result["chosen_native_method"] = "DoubleClickNode"
                result["img_activity_open"] = {
                    "node_metadata": {},
                    "chosen_native_method": "DoubleClickNode",
                }
        else:
            raise AssertionError(action)
        return request_id, {
            "status": "SUCCESS",
            "sap": self._status(),
            "result": result,
            "error": None,
        }


class Phase4CLiveDiscoveryTests(unittest.TestCase):
    def run_discovery(self, client):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name) / "phase4c"
        discovery = Phase4CDiscovery(client, output)
        return discovery.run(), output

    def test_nominal_read_only_discovery(self):
        summary, _ = self.run_discovery(DiscoveryClient())
        self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", summary["status"])
        self.assertEqual("FOUND", summary["targets"]["company_code"]["status"])
        self.assertEqual("FOUND", summary["targets"]["sales_organization"]["status"])
        self.assertEqual("DISCOVERED", summary["targets"]["division_assignment"]["status"])

    def test_duplicate_text_in_different_branches_is_not_ambiguous(self):
        summary, _ = self.run_discovery(DiscoveryClient())
        company_path = summary["targets"]["company_code"]["img_path"]
        self.assertEqual("FI", company_path[2]["key"])
        self.assertEqual("Comptabilité financière", company_path[2]["text"])

    def test_duplicate_text_under_same_parent_is_blocked(self):
        summary, output = self.run_discovery(
            DiscoveryClient(duplicate_financial_under_definition=True)
        )
        self.assertEqual("PARTIAL", summary["status"])
        self.assertIn("expected one direct child", summary["blockers"][0])
        steps = [
            json.loads(line)
            for line in (output / "discovery_steps.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        diagnostic = next(
            step
            for step in steps
            if step.get("action") == "RESOLVE_IMG_NODE"
            and step.get("requested_text") == "Comptabilité financière"
        )
        self.assertEqual(2, len([item for item in diagnostic["candidate_children"] if item["text"] == "Comptabilité financière"]))

    def test_unique_direct_child_resolution_records_parent_and_selected_key(self):
        _, output = self.run_discovery(DiscoveryClient())
        steps = [
            json.loads(line)
            for line in (output / "discovery_steps.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        financial = next(
            step
            for step in steps
            if step.get("requested_text") == "Comptabilité financière"
            and step.get("parent_key") == "DEF"
        )
        self.assertEqual("FI", financial["selected_key"])
        self.assertEqual("DIRECT_CHILD", financial["resolution"])

    def test_live_fixture_direct_child_resolution_uses_reconstructed_parent(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            discovery = Phase4CDiscovery(DiscoveryClient(), output)
            tree = inspected_tree()
            selected = discovery._resolve_direct_child(
                "company_code", tree, "02  1      6", "DÃ©finition"
            )
        self.assertEqual("03  2      1", selected["key"])

    def test_live_fixture_complete_company_path_and_duplicate_other_branch(self):
        duplicate_other_branch = LIVE_IMG_FIXTURE + [("02  1      7", "DÃ©finition")]
        tree = inspected_tree(duplicate_other_branch)
        labels = (
            ("01  1      1", "Structure de l'entreprise", "02  1      6"),
            ("02  1      6", "DÃ©finition", "03  2      1"),
            ("03  2      1", "ComptabilitÃ© financiÃ¨re", "04  3      1"),
            (
                "04  3      1",
                "Traiter, copier, supprimer, contrÃ´ler sociÃ©tÃ©",
                "05  4      3",
            ),
        )
        for parent_key, text, expected_key in labels:
            matches = [
                node
                for node in Phase4CDiscovery._children(tree, parent_key)
                if node.get("text") == text
            ]
            self.assertEqual([expected_key], [node["key"] for node in matches])

    def test_wrong_parent_is_blocked(self):
        summary, _ = self.run_discovery(DiscoveryClient(company_parent="ASSIGN"))
        self.assertEqual("PARTIAL", summary["status"])
        self.assertIn("expected one direct child", summary["blockers"][0])

    def test_missing_direct_child_is_blocked(self):
        client = DiscoveryClient()
        client.nodes = [item for item in client.nodes if item[0] != "FI"]
        summary, _ = self.run_discovery(client)
        self.assertEqual("PARTIAL", summary["status"])
        self.assertIn("expected one direct child", summary["blockers"][0])

    def test_resume_from_simg_reuses_current_screen(self):
        client = DiscoveryClient()
        summary, _ = self.run_discovery(client)
        self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", summary["status"])
        first_actions = [action for action, _ in client.actions[:3]]
        self.assertEqual(["STATUS", "STATUS", "INSPECT"], first_actions)

    def test_company_code_path_traversal_is_hierarchical(self):
        summary, _ = self.run_discovery(DiscoveryClient())
        path = summary["targets"]["company_code"]["img_path"]
        self.assertEqual(
            ["ROOT", "DEF", "FI", DYNAMIC_COMPANY_KEY],
            [item["key"] for item in path],
        )

    def test_company_code_leaf_read_only_exception_is_exact(self):
        session = SimpleNamespace(identity={"transaction": "SIMG"})
        snapshot = DiscoveryClient()._img()
        self.assertTrue(
            _is_company_code_display_exception(
                session,
                "DOUBLE_CLICK_TREE_NODE",
                TREE_CONTROL_ID,
                DYNAMIC_COMPANY_KEY,
                COMPANY_CODE_LEAF["text"],
                snapshot,
            )
        )
        self.assertTrue(
            _is_company_code_display_exception(
                session,
                "OPEN_IMG_ACTIVITY",
                TREE_CONTROL_ID,
                DYNAMIC_COMPANY_KEY,
                COMPANY_CODE_LEAF["text"],
                snapshot,
            )
        )

    def test_company_code_exception_rejects_key_not_observed_in_current_snapshot(self):
        session = SimpleNamespace(identity={"transaction": "SIMG"})
        snapshot = DiscoveryClient()._img()
        self.assertFalse(
            _is_company_code_display_exception(
                session,
                "DOUBLE_CLICK_TREE_NODE",
                TREE_CONTROL_ID,
                "wrong",
                COMPANY_CODE_LEAF["text"],
                snapshot,
            )
        )

    def test_company_code_dynamic_observed_key_is_accepted_without_historical_key(self):
        fresh_key = "11 newly observed company leaf"
        summary, _ = self.run_discovery(DiscoveryClient(company_key=fresh_key))
        self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", summary["status"])
        self.assertEqual(fresh_key, summary["targets"]["company_code"]["node"]["key"])

    def test_company_code_node_text_mismatch_fails_closed(self):
        summary, _ = self.run_discovery(DiscoveryClient(company_text="Unexpected"))
        self.assertEqual("PARTIAL", summary["status"])
        self.assertIn("expected one direct child", summary["blockers"][0])

    def test_unexpected_popup_fails_closed(self):
        popup = {"window_title": "Information inattendue", "buttons": []}
        summary, _ = self.run_discovery(DiscoveryClient(popup=popup))
        self.assertEqual("BLOCKED", summary["status"])
        self.assertIn("unexpected popup", summary["blockers"][0])

    def test_write_boundary_is_detected_without_pressing_it(self):
        summary, _ = self.run_discovery(DiscoveryClient())
        boundary = summary["targets"]["company_code"]["first_write_action"]
        self.assertEqual("write-capable controls or context observed", boundary["reason"])
        self.assertIn("Nouvelles entrées", boundary["controls"][0]["text"])

    def test_transport_popup_fails_closed(self):
        popup = {"window_title": "Demande de transport", "buttons": []}
        summary, _ = self.run_discovery(DiscoveryClient(popup=popup))
        self.assertEqual("BLOCKED", summary["status"])
        self.assertIn("transport popup", summary["blockers"][0])

    def test_partial_discovery_preserves_completed_target(self):
        summary, _ = self.run_discovery(DiscoveryClient(omit_sales=True))
        self.assertEqual("PARTIAL", summary["status"])
        self.assertEqual("FOUND", summary["targets"]["company_code"]["status"])
        self.assertEqual("BLOCKED", summary["targets"]["sales_organization"]["status"])

    def test_one_target_no_effect_does_not_stop_later_targets(self):
        summary, _ = self.run_discovery(
            DiscoveryClient(no_effect_nodes={DYNAMIC_COMPANY_KEY})
        )
        self.assertEqual("PARTIAL", summary["status"])
        self.assertEqual("BLOCKED", summary["targets"]["company_code"]["status"])
        self.assertNotEqual("not processed", summary["targets"]["sales_organization"]["blocker"])
        self.assertIn("NO_OBSERVED_EFFECT", summary["targets"]["company_code"]["blocker"])

    def test_loaded_direct_children_skip_expand_request(self):
        client = DiscoveryClient()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            discovery = Phase4CDiscovery(client, output)
            snapshot = client._img()
            root = next(
                node
                for node in snapshot["tree_controls"][0]["nodes"]
                if node["key"] == "ROOT"
            )
            result = discovery._expand_node("company_code", snapshot, root)
        self.assertIs(snapshot, result)
        self.assertFalse(any(action == "NAVIGATE" for action, _ in client.actions))

    def test_type_5_probe_backs_out_of_documentation_then_opens_maintenance(self):
        class ProbeClient(DiscoveryClient):
            def _img(self):
                snapshot = super()._img()
                node = next(
                    item
                    for item in snapshot["tree_controls"][0]["nodes"]
                    if item["key"] == DYNAMIC_COMPANY_KEY
                )
                node["items"] = [
                    {"column": "DOC", "type": "5", "text": "Documentation"},
                    {"column": "INFO", "type": "5", "text": "Information"},
                    {"column": "MAINT", "type": "5", "text": "Activity"},
                ]
                snapshot["tree_controls"][0]["columns"] = ["DOC", "INFO", "MAINT"]
                return snapshot

            def exchange(self, action, params):
                if action == "NAVIGATE" and params["navigation_operation"] == "OPEN_IMG_ACTIVITY":
                    self.actions.append((action, params))
                    if params["item_column"] == "DOC":
                        result = {
                            "transaction": "SIMG",
                            "program": "SAPMSSY0",
                            "window_title": "Afficher hypertexte",
                            "status_bar": {"text": "", "message_type": ""},
                            "popups": [],
                            "tree_controls": [],
                            "buttons": [],
                            "labels": [],
                            "input_fields": [],
                            "tables": [],
                            "control_ids": [],
                            "navigation_outcome": "SUCCESS",
                            "navigation_effect": {"observed": True},
                        }
                    elif params["item_column"] == "INFO":
                        result = {
                            "transaction": "SIMG",
                            "program": "SAPLDSYH",
                            "window_title": "Afficher guide d'implémentation",
                            "status_bar": {"text": "", "message_type": ""},
                            "popups": [
                                {
                                    "id": "/app/con[0]/ses[0]/wnd[1]",
                                    "window_title": "S\ufffdlection de l'activit\ufffd :",
                                    "buttons": [
                                        {
                                            "id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[0]",
                                            "type": "GuiButton",
                                            "text": "S\ufffdlectionner",
                                        }
                                    ],
                                    "input_fields": [],
                                    "labels": [
                                        {
                                            "id": "copy",
                                            "type": "GuiLabel",
                                            "text": "Copier, supprimer, contr\ufffdler soci\ufffdt\ufffd",
                                        },
                                        {
                                            "id": "display",
                                            "type": "GuiLabel",
                                            "text": "Traiter donn\ufffdes soci\ufffdt\ufffd",
                                        },
                                    ],
                                    "control_ids": [],
                                    "truncated": False,
                                }
                            ],
                            "tree_controls": [],
                            "buttons": [],
                            "labels": [],
                            "input_fields": [],
                            "tables": [],
                            "control_ids": [],
                            "navigation_outcome": "SUCCESS",
                            "navigation_effect": {"observed": True},
                        }
                    else:
                        result = self._maintenance()
                        result["navigation_outcome"] = "SUCCESS"
                        result["navigation_effect"] = {"observed": True}
                    return "probe-open", {
                        "status": "SUCCESS",
                        "sap": self._status(),
                        "result": result,
                        "error": None,
                    }
                if action == "BACK":
                    self.actions.append((action, params))
                    result = self._img()
                    return "probe-back", {
                        "status": "SUCCESS",
                        "sap": self._status(),
                        "result": result,
                        "error": None,
                    }
                if action == "SELECT_COMPANY_CODE_ACTIVITY":
                    self.actions.append((action, params))
                    result = self._maintenance()
                    result["activity_selection"] = {
                        "classification": "IMG_ACTIVITY_SELECTION_DIALOG",
                        "selected_row": "Traiter données société",
                        "button_text": "Sélectionner",
                    }
                    return "probe-select-activity", {
                        "status": "SUCCESS",
                        "sap": self._status(),
                        "result": result,
                        "error": None,
                    }
                return super().exchange(action, params)

        client = ProbeClient()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "snapshots").mkdir()
            discovery = Phase4CDiscovery(client, output)
            snapshot = client._img()
            leaf = next(
                node
                for node in snapshot["tree_controls"][0]["nodes"]
                if node["key"] == DYNAMIC_COMPANY_KEY
            )
            result = discovery._open_img_activity("company_code", snapshot, leaf)
        self.assertEqual("SAPLSVIM", result["program"])
        operations = [
            params["navigation_operation"] if action == "NAVIGATE" else action
            for action, params in client.actions
        ]
        self.assertEqual(
            [
                "OPEN_IMG_ACTIVITY",
                "BACK",
                "OPEN_IMG_ACTIVITY",
                "SELECT_COMPANY_CODE_ACTIVITY",
            ],
            operations,
        )
        self.assertNotIn("CLOSE_IMG_INFO_POPUP", operations)

    def test_live_encoded_activity_selection_is_not_documentation_info(self):
        snapshot = {
            "transaction": "SIMG",
            "program": "SAPLDSYH",
            "popups": [
                {
                    "id": "/app/con[0]/ses[0]/wnd[1]",
                    "window_title": "S\ufffdlection de l'activit\ufffd :",
                    "buttons": [{"text": "S\ufffdlectionner"}],
                    "input_fields": [
                        {"text": "Copier, supprimer, contr\ufffdler soci\ufffdt\ufffd"},
                        {"text": "Traiter donn\ufffdes soci\ufffdt\ufffd"},
                    ],
                }
            ],
        }
        self.assertTrue(Phase4CDiscovery._is_img_activity_selection_dialog(snapshot))
        self.assertFalse(Phase4CDiscovery._is_secondary_documentation_info(snapshot))

    def test_unknown_secondary_popup_remains_blocked(self):
        class UnknownPopupClient(DiscoveryClient):
            def _img(self):
                snapshot = super()._img()
                node = next(
                    item
                    for item in snapshot["tree_controls"][0]["nodes"]
                    if item["key"] == DYNAMIC_COMPANY_KEY
                )
                node["items"] = [{"column": "UNKNOWN", "type": "5", "text": ""}]
                snapshot["tree_controls"][0]["columns"] = ["UNKNOWN"]
                return snapshot

            def exchange(self, action, params):
                if action == "NAVIGATE" and params["navigation_operation"] == "OPEN_IMG_ACTIVITY":
                    self.actions.append((action, params))
                    result = {
                        "transaction": "SIMG",
                        "program": "SAPLUNKNOWN",
                        "window_title": "Unclassified destination",
                        "status_bar": {"text": "", "message_type": ""},
                        "popups": [
                            {
                                "id": "/app/con[0]/ses[0]/wnd[1]",
                                "window_title": "Mystery",
                                "buttons": [],
                                "input_fields": [],
                                "labels": [],
                                "control_ids": [],
                                "truncated": False,
                            }
                        ],
                        "tree_controls": [],
                        "buttons": [],
                        "labels": [],
                        "input_fields": [],
                        "tables": [],
                        "control_ids": [],
                        "navigation_outcome": "SUCCESS",
                        "navigation_effect": {"observed": True},
                    }
                    return "unknown-popup", {
                        "status": "SUCCESS",
                        "sap": self._status(),
                        "result": result,
                        "error": None,
                    }
                return super().exchange(action, params)

        client = UnknownPopupClient()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "snapshots").mkdir()
            discovery = Phase4CDiscovery(client, output)
            snapshot = client._img()
            leaf = next(
                node
                for node in snapshot["tree_controls"][0]["nodes"]
                if node["key"] == DYNAMIC_COMPANY_KEY
            )
            with self.assertRaisesRegex(DiscoveryBlocked, "unknown destination"):
                discovery._open_img_activity("company_code", snapshot, leaf)

    def test_recursive_semantic_resolution_uses_fresh_post_expand_snapshot(self):
        class DynamicBranchClient(DiscoveryClient):
            def __init__(self):
                super().__init__()
                self.nodes = [
                    ("IMGROOT", "Guide d'implÃ©mentation SAP", None),
                    ("BRANCH", "Dossier ADV", "IMGROOT"),
                ]

            def exchange(self, action, params):
                if (
                    action == "NAVIGATE"
                    and params["navigation_operation"] == "EXPAND_TREE_NODE"
                    and params["node_key"] == "BRANCH"
                ):
                    self.nodes.append(
                        (
                            "TARGET",
                            "DÃ©finir organisation commerciale",
                            "BRANCH",
                        )
                    )
                return super().exchange(action, params)

        client = DynamicBranchClient()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "snapshots").mkdir()
            discovery = Phase4CDiscovery(client, output)
            snapshot = client._img()
            snapshot, chain = discovery._resolve_semantic_branch(
                "sales_organization",
                snapshot,
                "IMGROOT",
                ("organisation commerciale",),
                max_depth=4,
            )
            steps = [
                json.loads(line)
                for line in (output / "discovery_steps.jsonl").read_text(encoding="utf-8").splitlines()
            ]
        self.assertEqual(["BRANCH", "TARGET"], [node["key"] for node in chain])
        observed = next(step for step in steps if step.get("action") == "OBSERVE_DIRECT_CHILDREN")
        self.assertEqual(
            [{"key": "TARGET", "text": "DÃ©finir organisation commerciale", "parent_key": "BRANCH"}],
            observed["children"],
        )

    def test_assignment_resolution_prefers_exact_adv_child(self):
        client = DiscoveryClient()
        client.nodes.append(("ASSIGN_ADV", "Administration des ventes (ADV)", "ASSIGN"))
        client.nodes = [
            (key, text, "ASSIGN_ADV" if key in {"SO_CC", "DC_SO", "DIV_SO"} else parent)
            for key, text, parent in client.nodes
        ]
        summary, _ = self.run_discovery(client)
        path = summary["targets"]["sales_org_company_assignment"]["img_path"]
        self.assertIn("ASSIGN_ADV", [node["key"] for node in path])
        self.assertEqual("DISCOVERED", summary["targets"]["sales_org_company_assignment"]["status"])

    def test_org_alias_matches_organisation_only_in_normalized_exact_resolution(self):
        client = DiscoveryClient()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            discovery = Phase4CDiscovery(client, output)
            snapshot = client._img()
            _, chain = discovery._resolve_preferred_leaf(
                "sales_organization",
                snapshot,
                "SD",
                "Définir, copier, supprimer, contrôler organisation commerciale",
                ("definir", "organisation commerciale"),
            )
        self.assertEqual(["SALES_DEF"], [node["key"] for node in chain])

    def test_distribution_exact_direct_child_wins_over_semantic_lookalike(self):
        client = DiscoveryClient()
        client.nodes.append(
            (
                "DC_LOOKALIKE",
                "Affectation d'organisation commerciale - Canal de distribution - Division",
                "ASSIGN",
            )
        )
        summary, _ = self.run_discovery(client)
        target = summary["targets"]["distribution_channel_assignment"]
        self.assertEqual("DISCOVERED", target["status"])
        self.assertEqual("DC_SO", target["node"]["key"])

    def test_generic_simg_menus_are_not_write_boundaries_and_values_are_unknown(self):
        snapshot = DiscoveryClient()._img()
        snapshot["buttons"] = [
            {"id": "menu1", "type": "GuiMenu", "text": "Transport", "tooltip": None},
            {"id": "menu2", "type": "GuiMenu", "text": "Supprimer transaction", "tooltip": None},
        ]
        self.assertIsNone(Phase4CDiscovery._write_boundary(snapshot))
        evidence = Phase4CDiscovery._screen_evidence(snapshot)
        self.assertEqual("UNKNOWN", evidence["value_1010_observed"])
        self.assertEqual("UNKNOWN", evidence["transport_observed"])

    def test_overlapping_raw_reads_do_not_inflate_completeness_logic(self):
        snapshot = {
            "input_fields": [{
                "id": "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO",
                "text": "Entr\u00e9e 7 / 112",
            }],
            "table_value_search": {
                "result": "UNKNOWN",
                "row_count": 131,
                "rows_read": 131,
                "unique_rows_read": 111,
                "found_row": None,
            },
        }
        classified = Phase4CDiscovery._classify_company_code_table_search(snapshot)
        self.assertEqual("UNKNOWN", classified["result"])
        self.assertEqual(111, classified["unique_rows_read"])
        self.assertEqual(112, classified["sap_total_entries"])

    def test_sap_total_and_complete_unique_scan_confirm_target_absent(self):
        snapshot = {
            "input_fields": [{
                "id": "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO",
                "text": "Entr\u00e9e 7 / 112",
            }],
            "table_value_search": {
                "result": "UNKNOWN",
                "row_count": 131,
                "rows_read": 112,
                "found_row": None,
            },
        }
        evidence = Phase4CDiscovery._screen_evidence(snapshot)
        self.assertEqual("CONFIRMED_NOT_FOUND", evidence["value_1010_observed"])
        self.assertEqual(
            "CONFIRMED_NOT_FOUND", evidence["table_value_search"]["result"]
        )

    def test_incomplete_unique_scan_remains_unknown(self):
        snapshot = {
            "input_fields": [{
                "id": "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO",
                "text": "Entr\u00e9e 7 / 112",
            }],
            "table_value_search": {
                "result": "UNKNOWN",
                "row_count": 131,
                "rows_read": 111,
                "found_row": None,
            },
        }
        evidence = Phase4CDiscovery._screen_evidence(snapshot)
        self.assertEqual("UNKNOWN", evidence["value_1010_observed"])

    def test_output_bundle_is_generated(self):
        summary, output = self.run_discovery(DiscoveryClient())
        self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", summary["status"])
        self.assertTrue((output / "discovery_summary.json").exists())
        self.assertTrue((output / "discovery_report.md").exists())
        self.assertTrue((output / "discovery_steps.jsonl").exists())
        self.assertTrue(any((output / "snapshots").glob("*.json")))
        stored = json.loads((output / "discovery_summary.json").read_text(encoding="utf-8"))
        self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", stored["status"])

    def test_existing_output_makes_resume_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "phase4c"
            output.mkdir()
            (output / "discovery_summary.json").write_text("{}", encoding="utf-8")
            discovery = Phase4CDiscovery(DiscoveryClient(), output)
            with self.assertRaises(DiscoveryBlocked):
                discovery.run()

    def test_explicit_restart_archives_previous_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "phase4c"
            output.mkdir()
            (output / "discovery_summary.json").write_text(
                '{"status":"BLOCKED"}', encoding="utf-8"
            )
            discovery = Phase4CDiscovery(
                DiscoveryClient(), output, archive_existing=True
            )
            summary = discovery.run()
            self.assertEqual("COMPLETE/PARTIAL_READY_FOR_PREPARE", summary["status"])
            archived = list((output / "history").glob("*/discovery_summary.json"))
            self.assertEqual(1, len(archived))
            self.assertEqual(
                "BLOCKED",
                json.loads(archived[0].read_text(encoding="utf-8"))["status"],
            )


if __name__ == "__main__":
    unittest.main()
