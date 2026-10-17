import json, unittest
from pathlib import Path
from src.validation.jsonschema import validate_object
ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class PilotTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.extracted=load("data/extracted/pilot/pilot_objects.json")["objects"]
  cls.normalized=load("data/normalized/pilot/pilot_objects.json")["objects"]
 def test_inventory_and_unique_ids(self):
  self.assertEqual(len(self.normalized),7); self.assertEqual(len({o["object_id"] for o in self.normalized}),7)
  self.assertEqual({o["object_type"] for o in self.normalized},{"DISTRIBUTION_CHANNEL","SALES_AREA","PRICING_CONDITION","SALES_ORDER","OUTBOUND_DELIVERY","BILLING"})
 def test_real_schema_validation(self):
  for obj in self.extracted+self.normalized: self.assertEqual(validate_object(ROOT,obj),[],obj["object_id"])
 def test_lifecycle_and_readiness(self):
  self.assertTrue(all(o["lifecycle_status"]=="EXTRACTED" for o in self.extracted)); self.assertTrue(all(o["lifecycle_status"]=="VALIDATED" for o in self.normalized)); self.assertTrue(all(o["readiness_status"]=="BLOCKED" for o in self.normalized))
 def test_placeholder_semantics(self):
  placeholders=[p for o in self.normalized for p in o["placeholders"]]; self.assertTrue(placeholders); self.assertTrue(all(p["raw"]=="##" and p["status"]=="UNRESOLVED" and p["resolved"] is None for p in placeholders))
 def test_transaction_chain(self):
  by={o["object_type"]:o for o in self.normalized if o["classification"]=="TRANSACTION"}; self.assertEqual(by["OUTBOUND_DELIVERY"]["dependencies"][0]["target_id"],by["SALES_ORDER"]["object_id"]); self.assertEqual(by["BILLING"]["dependencies"][0]["target_id"],by["OUTBOUND_DELIVERY"]["object_id"])
 def test_pr00_scales(self):
  p=next(o for o in self.normalized if o["object_type"]=="PRICING_CONDITION"); self.assertEqual([(s["from_quantity"],s["amount"]) for s in p["data"]["scales"]],[(1,250),(10,240),(100,230)]); self.assertEqual(p["data"]["currency"],"EUR")
 def test_solution_is_verification_not_duplicate(self):
  for obj in self.normalized:
   sections=[p["section_type"] for p in obj["provenance"]]; self.assertEqual(sections.count("EXERCISE"),1); self.assertGreaterEqual(sections.count("SOLUTION"),1)
 def test_normalized_terminology_and_lineage(self):
  order=next(o for o in self.normalized if o["object_type"]=="SALES_ORDER"); self.assertIn("sales_division",order["data"]); self.assertNotIn("division",order["data"])
  lineage=load("metadata/lineage/pilot/pilot_lineage.json"); self.assertTrue(all(x["source_to_canonical"] for x in lineage)); self.assertTrue(any(x["supporting_references"] for x in lineage))
 def test_dependency_and_confidence_metadata(self):
  graph=load("metadata/dependencies/pilot/dependency_graph.json"); self.assertEqual(len(graph["edges"]),2)
  confidence=load("metadata/confidence/pilot/confidence.json")["objects"]; self.assertEqual(len(confidence),7)
if __name__=="__main__": unittest.main()
