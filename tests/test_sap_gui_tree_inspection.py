import unittest
from types import SimpleNamespace

from src.sap_gui_bridge.inspection import _tree_record


TREE_ID = "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell"
TREE_RECORD = {
    "id": TREE_ID,
    "type": "GuiShell",
    "subtype": "Tree",
    "text": None,
    "tooltip": None,
    "visible": True,
    "changeable": False,
}


class TreeBase:
    SelectedNode = "NODE_A"

    def __init__(self, keys=None):
        self.keys = ["NODE_A"] if keys is None else keys

    def GetAllNodeKeys(self):
        return self.keys

    def IsNodeExpanded(self, key):
        return key == "NODE_A"


class TreeWithText(TreeBase):
    def GetNodeTextByKey(self, key):
        return "Structure de l'entreprise"


class TreeWithoutTextMethod(TreeBase):
    pass


class TreeWithComFailure(TreeBase):
    def GetNodeTextByKey(self, key):
        raise RuntimeError("simulated COM failure")


class TreeWithEmptyText(TreeBase):
    def GetNodeTextByKey(self, key):
        return ""


class ColumnTreeWithText(TreeWithEmptyText):
    def GetColumnNames(self):
        return ["Hierarchy"]

    def GetItemText(self, key, column_name):
        return "Administration des ventes (ADV)"


class OrderedImgTree(TreeBase):
    def __init__(self):
        super().__init__(["01  1      1", "02  1      6", "03  2      1", "04  3      1"])

    def GetNodeTextByKey(self, key):
        return {
            "01  1      1": "Guide d'implémentation SAP",
            "02  1      6": "Structure de l'entreprise",
            "03  2      1": "Définition",
            "04  3      1": "Comptabilité financière",
        }[key]


LIVE_IMG_NODES = [
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


class LiveImgTree(TreeBase):
    def __init__(self, nodes=None):
        self.nodes = LIVE_IMG_NODES if nodes is None else nodes
        super().__init__([key for key, _ in self.nodes])

    def GetNodeTextByKey(self, key):
        return dict(self.nodes)[key]


class NativeHierarchyTree(LiveImgTree):
    def GetNodeLevel(self, key):
        return int(key.strip().split(maxsplit=1)[0])

    def GetParent(self, key):
        parents = {
            "01  1      1": None,
            "02  1      6": "01  1      1",
            "03  2      1": "02  1      6",
            "04  3      1": "03  2      1",
            "05  4      1": "04  3      1",
            "05  4      2": "04  3      1",
            "05  4      3": "04  3      1",
            "04  3      4": "03  2      1",
            "03  2      2": "02  1      6",
        }
        return parents[key]


class MetadataImgTree(TreeBase):
    SelectedNode = "02 branch"
    FocusedItem = "Hierarchy"

    def __init__(self):
        super().__init__(["01 root", "02 branch"])

    def GetNodeTextByKey(self, key):
        return {"01 root": "IMG", "02 branch": "Activity"}[key]

    def GetColumnNames(self):
        return ["Hierarchy"]

    def GetItemType(self, key, column):
        return "Text"

    def GetItemText(self, key, column):
        return self.GetNodeTextByKey(key)

    def GetItemTooltip(self, key, column):
        return "Open activity" if key == "02 branch" else ""

    def GetItemIcon(self, key, column):
        return "@5D@"

    def GetNodeType(self, key):
        return "Folder" if key == "01 root" else "Leaf"

    def IsFolder(self, key):
        return key == "01 root"

    def GetSubNodes(self, key):
        return ["02 branch"] if key == "01 root" else []

    def DoubleClickItem(self, key, column):
        pass


class TreeInspectionTests(unittest.TestCase):
    def inspect_tree(self, tree):
        session = SimpleNamespace(find=lambda control_id: tree)
        return _tree_record(session, TREE_RECORD)

    def test_node_text_is_returned_by_native_key_method(self):
        result = self.inspect_tree(TreeWithText())
        self.assertEqual("Structure de l'entreprise", result["nodes"][0]["text"])
        self.assertEqual("GetNodeTextByKey", result["nodes"][0]["text_extraction_method"])
        self.assertIsNone(result["nodes"][0]["extraction_error"])
        self.assertTrue(result["nodes"][0]["expanded"])
        self.assertTrue(result["nodes"][0]["selected"])

    def test_unavailable_get_node_text_is_reported_without_invention(self):
        result = self.inspect_tree(TreeWithoutTextMethod())
        node = result["nodes"][0]
        self.assertIsNone(node["text"])
        self.assertIn("GetNodeTextByKey unavailable", node["extraction_error"])

    def test_com_exception_on_one_node_is_reported(self):
        result = self.inspect_tree(TreeWithComFailure())
        node = result["nodes"][0]
        self.assertIsNone(node["text"])
        self.assertIn("GetNodeTextByKey failed (RuntimeError)", node["extraction_error"])

    def test_node_without_text_is_null(self):
        result = self.inspect_tree(TreeWithEmptyText())
        node = result["nodes"][0]
        self.assertIsNone(node["text"])
        self.assertIn("GetNodeTextByKey returned no text", node["extraction_error"])

    def test_empty_key_list_returns_empty_nodes(self):
        result = self.inspect_tree(TreeWithText(keys=[]))
        self.assertEqual([], result["nodes"])
        self.assertFalse(result["nodes_truncated"])
        self.assertIsNone(result["extraction_error"])

    def test_observed_native_column_tree_api_is_used_as_fallback(self):
        result = self.inspect_tree(ColumnTreeWithText())
        node = result["nodes"][0]
        self.assertEqual("Administration des ventes (ADV)", node["text"])
        self.assertEqual("GetItemText:Hierarchy", node["text_extraction_method"])
        self.assertIsNone(node["extraction_error"])

    def test_parent_relationship_is_reconstructed_from_observed_level_and_order(self):
        result = self.inspect_tree(OrderedImgTree())
        nodes = {node["key"]: node for node in result["nodes"]}
        self.assertIsNone(nodes["01  1      1"]["parent_key"])
        self.assertEqual("01  1      1", nodes["02  1      6"]["parent_key"])
        self.assertEqual("02  1      6", nodes["03  2      1"]["parent_key"])
        self.assertEqual("03  2      1", nodes["04  3      1"]["parent_key"])
        self.assertEqual(4, nodes["04  3      1"]["level"])
        self.assertEqual("OBSERVED_KEY_LEVEL_AND_ORDER", nodes["04  3      1"]["hierarchy_method"])

    def test_exact_live_img_sequence_reconstructs_expected_parents(self):
        result = self.inspect_tree(LiveImgTree())
        nodes = {node["text"]: node for node in result["nodes"]}
        self.assertEqual("02  1      6", nodes["DÃ©finition"]["parent_key"])
        self.assertEqual("03  2      1", nodes["ComptabilitÃ© financiÃ¨re"]["parent_key"])
        self.assertEqual(
            "04  3      1",
            nodes["Traiter, copier, supprimer, contrÃ´ler sociÃ©tÃ©"]["parent_key"],
        )
        self.assertEqual("03  2      1", nodes["Administration des ventes (ADV)"]["parent_key"])
        self.assertEqual("02  1      6", nodes["Affectation"]["parent_key"])
        self.assertEqual([1, 2, 3, 4, 5, 5, 5, 4, 3], [node["level"] for node in result["nodes"]])
        self.assertTrue(all(node["hierarchy_error"] is None for node in result["nodes"]))

    def test_same_level_siblings_share_the_last_parent(self):
        result = self.inspect_tree(LiveImgTree())
        nodes = {node["key"]: node for node in result["nodes"]}
        for key in ("05  4      1", "05  4      2", "05  4      3"):
            self.assertEqual("04  3      1", nodes[key]["parent_key"])

    def test_deep_to_shallower_level_replaces_deeper_stack_entries(self):
        result = self.inspect_tree(LiveImgTree())
        nodes = {node["key"]: node for node in result["nodes"]}
        self.assertEqual("03  2      1", nodes["04  3      4"]["parent_key"])
        self.assertEqual("02  1      6", nodes["03  2      2"]["parent_key"])

    def test_root_has_no_parent(self):
        node = self.inspect_tree(LiveImgTree())["nodes"][0]
        self.assertEqual(1, node["level"])
        self.assertIsNone(node["parent_key"])
        self.assertIsNone(node["hierarchy_error"])

    def test_malformed_key_fails_closed(self):
        result = self.inspect_tree(LiveImgTree([("NOT_A_LEVEL", "Malformed")]))
        node = result["nodes"][0]
        self.assertIsNone(node["level"])
        self.assertIsNone(node["parent_key"])
        self.assertIn("not observable", node["hierarchy_error"])

    def test_invalid_level_jump_fails_closed(self):
        result = self.inspect_tree(
            LiveImgTree([("01 root", "Root"), ("03 child", "Impossible child")])
        )
        node = result["nodes"][1]
        self.assertEqual(3, node["level"])
        self.assertIsNone(node["parent_key"])
        self.assertEqual("invalid observed level jump 1->3", node["hierarchy_error"])

    def test_observable_native_hierarchy_api_has_priority(self):
        result = self.inspect_tree(NativeHierarchyTree())
        nodes = {node["key"]: node for node in result["nodes"]}
        self.assertEqual("02  1      6", nodes["03  2      1"]["parent_key"])
        self.assertEqual("NATIVE_GETPARENT", nodes["03  2      1"]["hierarchy_method"])

    def test_tree_item_metadata_and_native_capabilities_are_observed(self):
        result = self.inspect_tree(MetadataImgTree())
        self.assertEqual(["Hierarchy"], result["columns"])
        self.assertIn("DoubleClickItem", result["native_capabilities"])
        self.assertEqual("02 branch", result["selected_node"])
        self.assertEqual("Hierarchy", result["focused_item"])
        root, activity = result["nodes"]
        self.assertEqual(1, root["children_count"])
        self.assertEqual(["02 branch"], root["children_keys"])
        self.assertTrue(root["expandable"])
        self.assertEqual("Leaf", activity["node_type"])
        self.assertEqual("Open activity", activity["items"][0]["tooltip"])
        self.assertEqual("@5D@", activity["items"][0]["icon"])


if __name__ == "__main__":
    unittest.main()
