"""Build only the approved Phase 1B representative pilot records."""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.validation.jsonschema import validate_object
FILES={"S4650":"S4650_FR_Col12_ILT_FV_Inst_A4.pdf","S4620":"S4620_FR_Col12_ILT_FV_Inst_A4.pdf","S4600":"P2W_S4600_FR_Col23.pdf","S4610":"S4610_FR_Col12_ILT_FV_Inst_A4.pdf","S4615":"S4615_FR_Col12_ILT_FV_Inst_A4.pdf"}
def ref(course,page,section,chapter,exercise,scenario,term): return {"course_code":course,"source_file":FILES[course],"page":page,"chapter":chapter,"exercise":exercise,"section_type":section,"scenario_id":scenario,"raw_excerpt":None,"source_term":term}
def placeholder(path): return {"raw":"##","resolved":None,"status":"UNRESOLVED","mandatory":True,"field_path":path}
def base(oid,otype,classification,sid,prov,data,placeholders=None,deps=None,reasons=None,confidence="HIGH",life="VALIDATED"):
 return {"object_id":oid,"object_type":otype,"classification":classification,"scenario_id":sid,"provenance":prov,"lifecycle_status":life,"readiness_status":"BLOCKED" if reasons else "READY","blocking_reasons":reasons or [],"dependencies":deps or [],"placeholders":placeholders or [],"validation":{"schema_valid":True,"issues":[],"confidence":confidence},"data":data}
def build(life="VALIDATED"):
 c="S4650_CH1_EX1"; p=[ref("S4650",17,"EXERCISE",1,1,c,"Canal de distribution / Organis. commerciale / Secteur d'activité"),ref("S4650",18,"SOLUTION",1,1,c,"Canal de distribution"),ref("S4650",19,"SOLUTION",1,1,c,"Organis. commerciale / Secteur d'activité")]
 miss=[{"code":"UNRESOLVED_MANDATORY_PLACEHOLDER","message":"Participant group placeholder is unresolved","field_path":"data.code"}]
 dc=base("S4650_CH1_EX1_DISTRIBUTION_CHANNEL_GROUP","DISTRIBUTION_CHANNEL","CUSTOMIZING",c,p,{"code":None,"description":"Canal groupe ##","sales_organization":"1010"},[placeholder("data.code"),placeholder("data.description")],reasons=miss,confidence="MEDIUM",life=life)
 areas=[]
 for div in ("00","03"):
  areas.append(base(f"S4650_CH1_EX1_SALES_AREA_1010_GROUP_{div}","SALES_AREA","CUSTOMIZING",c,p,{"sales_organization":"1010","distribution_channel":None,"sales_division":div},[placeholder("data.distribution_channel")],reasons=miss,confidence="MEDIUM",life=life))
 c="S4620_CH1_EX1"; p=[ref("S4620",21,"EXERCISE",1,1,c,"Organis. commerciale / Canal distribution / Client / Article / Quantité échelonnée / Montant"),ref("S4620",27,"SOLUTION",1,1,c,"Client/article / Barèmes"),ref("S4620",28,"SOLUTION",1,1,c,"Quantité échelonnée / Montant")]
 ph=[placeholder("data.key_combination.customer"),placeholder("data.key_combination.material")]
 pc=base("S4620_CH1_EX1_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL","PRICING_CONDITION","MASTER_DATA",c,p,{"condition_type":"PR00","key_combination":{"sales_organization":"1010","distribution_channel":"10","customer":"C620-A##","material":"P620-1##"},"valid_from":None,"valid_to":None,"rate":None,"currency":"EUR","pricing_unit":None,"scales":[{"from_quantity":1,"quantity_unit":"PC","amount":250,"currency":"EUR","pricing_unit":None},{"from_quantity":10,"quantity_unit":"PC","amount":240,"currency":"EUR","pricing_unit":None},{"from_quantity":100,"quantity_unit":"PC","amount":230,"currency":"EUR","pricing_unit":None}]},ph,reasons=[{"code":"UNRESOLVED_MANDATORY_PLACEHOLDER","message":"Customer and material participant placeholders are unresolved","field_path":"data.key_combination"}],confidence="HIGH",life=life)
 c="S4600_CH3_EX3"; oid="S4600_CH3_EX3_SALES_ORDER_STANDARD"; p=[ref("S4600",57,"EXERCISE",3,3,c,"Organisation commerciale / Canal distribution / Secteur d'activité / Donneur d'ordre / DateLivrSouh."),ref("S4600",58,"SOLUTION",3,3,c,"Type commande client / Article / Quantité")]
 ph=[placeholder("data.sold_to_party"),placeholder("data.customer_reference"),placeholder("data.items[0].material"),placeholder("data.items[1].material")]
 so=base(oid,"SALES_ORDER","TRANSACTION",c,p,{"order_type":"CDCL","sales_organization":"1010","distribution_channel":"10","sales_division":"00","sold_to_party":"T-S50A##","ship_to_party":None,"customer_reference":"4-2##","requested_delivery_date":{"kind":"RELATIVE","raw":"dans 1 semaine","offset":"P1W"},"items":[{"line_id":"10","material":"T-MS1##","quantity":10,"unit":None},{"line_id":"20","material":"T-MS2##","quantity":20,"unit":None}]},ph,reasons=[{"code":"UNRESOLVED_MANDATORY_PLACEHOLDER","message":"Participant-specific customer, reference, and materials are unresolved","field_path":"data"}],confidence="HIGH",life=life)
 c="S4600_CH3_EX5"; doid="S4600_CH3_EX5_OUTBOUND_DELIVERY_FROM_EX3"; dep={"relation":"CREATED_FROM","target_type":"SALES_ORDER","target_id":oid,"status":"RESOLVED","critical":True,"source_phrase":"en référence à une commande client"}
 p=[ref("S4600",71,"EXERCISE",3,5,c,"Point d'expédition / Date de création planifiée"),ref("S4600",72,"SOLUTION",3,5,c,"numéro de votre commande client")]
 dl=base(doid,"OUTBOUND_DELIVERY","TRANSACTION",c,p,{"delivery_type":None,"ship_to_party":None,"shipping_point":"Z0##","planned_creation_date":{"kind":"RELATIVE","raw":"Échue la semaine prochaine","offset":"P1W"},"planned_goods_issue_date":None,"items":[]},[placeholder("data.shipping_point")],[dep],[{"code":"UNRESOLVED_MANDATORY_PLACEHOLDER","message":"Participant shipping-point placeholder is unresolved","field_path":"data.shipping_point"}],"MEDIUM",life)
 c="S4600_CH3_EX7"; dep={"relation":"BILLED_FROM","target_type":"OUTBOUND_DELIVERY","target_id":doid,"status":"RESOLVED","critical":True,"source_phrase":"livraison sortante de la tâche précédente"}
 p=[ref("S4600",87,"EXERCISE",3,7,c,"document de facturation / livraison sortante de la tâche précédente"),ref("S4600",88,"SOLUTION",3,7,c,"Création de documents de facturation")]
 bill=base("S4600_CH3_EX7_BILLING_FROM_EX5","BILLING","TRANSACTION",c,p,{"billing_type":None,"billing_subtype":"STANDARD","payer":None,"billing_date":None,"reference_document":None,"items":[],"billing_plan":None,"down_payments":[],"installment_payments":[]},deps=[dep],reasons=[{"code":"DEPENDENCY_NOT_READY","message":"The referenced delivery is identified but remains blocked by participant placeholders","field_path":"dependencies[0]"}],confidence="MEDIUM",life=life)
 return [dc,*areas,pc,so,dl,bill]
def write():
 outs={"data/extracted/pilot/pilot_objects.json":build("EXTRACTED"),"data/normalized/pilot/pilot_objects.json":build()}
 for rel,data in outs.items():
  path=ROOT/rel; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps({"objects":data},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 normalized=outs["data/normalized/pilot/pilot_objects.json"]
 for obj in normalized:
  errs=validate_object(ROOT,obj)
  if errs: raise ValueError({obj["object_id"]:errs})
 supporting={"OUTBOUND_DELIVERY":[{"course_code":"S4610","source_file":FILES["S4610"],"pages":[114,115],"relation":"SEMANTIC_REFERENCE","topic":"Traitement des livraisons sortantes"}],"BILLING":[{"course_code":"S4615","source_file":FILES["S4615"],"pages":[109,110],"relation":"SEMANTIC_REFERENCE","topic":"Création de documents de facturation"}]}
 lineage=[{"object_id":o["object_id"],"scenario_id":o["scenario_id"],"source_to_canonical":[{"source_term":r["source_term"],"section_type":r["section_type"],"page":r["page"]} for r in o["provenance"]],"supporting_references":supporting.get(o["object_type"],[])} for o in normalized]
 graph={"nodes":[o["object_id"] for o in normalized],"edges":[{"source":o["object_id"],"target":d["target_id"],"relation":d["relation"],"status":d["status"]} for o in normalized for d in o["dependencies"]]}
 confidence={"objects":[{"object_id":o["object_id"],"confidence":o["validation"]["confidence"],"readiness_status":o["readiness_status"]} for o in normalized]}
 for rel,data in [("metadata/lineage/pilot/pilot_lineage.json",lineage),("metadata/dependencies/pilot/dependency_graph.json",graph),("metadata/confidence/pilot/confidence.json",confidence)]:
  path=ROOT/rel; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if __name__=="__main__": write()
