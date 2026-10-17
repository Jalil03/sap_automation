import json, re, unittest
from pathlib import Path
from scripts.generate_schemas import GROUPS
from src.ingestion.manifest import load_manifest, resolve_document
from src.placeholders.policy import evaluate_placeholders
from src.extraction.scenarios import scenario_id, merge_scenario_sections
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def test_manifest(self):
  docs=load_manifest(ROOT); self.assertEqual(len(docs),5)
  for d in docs: self.assertEqual(resolve_document(ROOT,d["logical_name"]).name,d["actual_filename"])
 def test_schema_inventory_constants(self):
  idx=json.loads((ROOT/"schemas/index.json").read_text()); expected={o:c for c,g in GROUPS.items() for o in g}; self.assertEqual({o:v["classification"] for o,v in idx.items()},expected)
  for o,v in idx.items():
   s=json.loads((ROOT/v["schema"]).read_text()); self.assertEqual(s["properties"]["object_type"]["const"],o); self.assertEqual(s["properties"]["classification"]["const"],v["classification"])
 def test_provenance_statuses(self):
  base=json.loads((ROOT/"schemas/common/canonical_object.schema.json").read_text()); self.assertTrue({"provenance","lifecycle_status","readiness_status","dependencies","placeholders","validation"}<=set(base["required"])); self.assertEqual(base["properties"]["lifecycle_status"]["enum"],["RAW","EXTRACTED","NORMALIZED","VALIDATED","REJECTED"]); self.assertEqual(base["properties"]["readiness_status"]["enum"],["READY","BLOCKED"])
  src=json.loads((ROOT/"schemas/common/source_ref.schema.json").read_text()); self.assertEqual(set(src["required"]),{"course_code","source_file","page","section_type"}); self.assertNotIn("NEEDS_REVIEW",(ROOT/"taxonomy/classifications.yaml").read_text())
 def test_all_schema_json_and_refs(self):
  for path in (ROOT/"schemas").rglob("*.json"):
   doc=json.loads(path.read_text(encoding="utf-8")); self.assertEqual(doc.get("$schema"),"https://json-schema.org/draft/2020-12/schema") if path.name!="index.json" else None
   for ref in re.findall(r'"\$ref"\s*:\s*"([^"]+)"',path.read_text(encoding="utf-8")):
    if ref.startswith("#/"): continue
    self.assertTrue((path.parent/ref.split("#",1)[0]).resolve().is_file(),f"Missing ref {ref} from {path}")
 def test_placeholders(self):
  p={"raw":"##","mandatory":True,"field_path":"data.id"}; self.assertEqual(evaluate_placeholders([p],{"##":None})["readiness_status"],"BLOCKED"); self.assertEqual(evaluate_placeholders([p],{"##":"42"})["readiness_status"],"READY")
 def test_terminology(self):
  a=(ROOT/"mappings/field_aliases.yaml").read_text(encoding="utf-8"); self.assertRegex(a,r"sales_division:.*secteur d'activité"); self.assertRegex(a,r"plant:.*division"); self.assertNotRegex(a,r"(?m)^\s+division:")
 def test_deduplication(self):
  sid=scenario_id("S4610",3,4); parts=[{"scenario_id":sid,"section_type":"EXERCISE"},{"scenario_id":sid,"section_type":"SOLUTION"}]; self.assertEqual(len(merge_scenario_sections(parts)),1)
 def test_coverage(self):
  m=json.loads((ROOT/"mappings/document_to_object.yaml").read_text())["documents"]; objects={o for g in GROUPS.values() for o in g}; self.assertEqual(set(m),{"S4600","S4610","S4615","S4620","S4650"})
  for r in m.values(): self.assertEqual(set(r),{"PRIMARY","SECONDARY","REFERENCE_ONLY"}); self.assertFalse(set(sum(r.values(),[]))-objects)
if __name__=="__main__": unittest.main()
