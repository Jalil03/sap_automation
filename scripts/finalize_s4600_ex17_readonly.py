"""Read-only closeout with an explicit Book-vs-runtime discrepancy."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env()
assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
client=UrllibSapTransport(cfg)
corrected=json.loads((ROOT/'runtime/sap_writes/s4600_ex17_correction_2026-10-22.json').read_text(encoding='utf-8'))
assert corrected['status']=='VERIFIED' and corrected['status_bar']['type']=='S'
linked=get(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':"ReferenceSDDocument eq '158'"})
assert linked['http_status']==200 and linked['count']==1 and linked['rows'][0]['DeliveryDocument']=='80000086'
header=get(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':"DeliveryDocument eq '80000086'"})
assert header['http_status']==200 and header['count']==1
assert header['rows'][0]['OverallGoodsMovementStatus']=='A'
result={'status':'ORDER_CORRECTED_VERIFIED_BOOK_DELIVERY_BLOCK_NOT_REPRODUCED',
        'captured_at_utc':datetime.now(timezone.utc).isoformat(),'order':'158','delivery':'80000086',
        'reference':'3-900','net_weight_kg':'20','net_amount_eur':'800.00',
        'initial_incompletion_fields':['Référence client','Poids net'],
        'initial_delivery_test':{'expected':'REJECTED_INCOMPLETE','observed':'HTTP_201_DELIVERY_CREATED'},
        'correction_status':'VERIFIED','second_delivery_attempted':False,
        'second_delivery_reason':'The only source item was already fully referenced by delivery 80000086; no duplicate creation.',
        'goods_issue_posted':False,'delivery_header':header,'delivery_items':linked,
        'pedagogical_gap':'The refusal-before-correction sequence from Book steps 3 and 6 was not reproduced with the OData route.',
        'root_cause':'Originally unverified; see subsequent RFC diagnosis of TVAK/TVAP -> TVUVF -> TVUVS. Current procedures 11/20 assign BSTKD to status group 01 and NTGEW to 00, both with delivery incompletion flag UVVLK blank.',
        'weight_note':'Book correction sets order net weight 20 KG; source order gross weight remains 14 KG. SAP warning was acknowledged. Existing delivery retains original net weight 0 KG; no extra update was authorized or performed.'}
out=ROOT/'runtime/sap_reads/s4600_ex17_final_validation_2026-10-22.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'delivery_header','delivery_items'}},ensure_ascii=False,indent=2))
