"""Offline evidence assertions and durable checkpoint; no SAP calls."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
files=['s4600_ex12_customer_material_2026-10-22.json','s4600_ex12_order_2026-10-22.json','s4600_ex12_delivery_2026-10-22.json','s4600_ex16_proposal.json','s4600_ex16_customer_assignment.json','s4600_ex16_order.json','s4600_ex21_order.json','s4600_ex22_order.json','s4600_ex25_collective_deliveries.json','s4600_ex32_order.json','s4600_ex32_delivery.json']
records={name:read('runtime/sap_writes/'+name) for name in files}
assert all(x['status']=='VERIFIED' for x in records.values())
before=read('runtime/sap_reads/s4600_ex16_details_ex21_stock_before_normalized.json')
after=read('runtime/sap_reads/s4600_ex16_details_ex21_stock_after21.json')
assert before['stock_return']['TYPE']=='S' and after['stock_return']['TYPE']=='S'
new=[x for x in after['stock_tables']['MRP_IND_LINES']['rows'] if x['ELEMNT_DATA'].startswith('0000000161/')]
assert len(new)==1 and new[0]['REC_REQD_QTY']=='-20,000' and new[0]['SORT_DATE']=='20261027'
assert not any(x['ELEMNT_DATA'].startswith('0000000161/') for x in before['stock_tables']['MRP_IND_LINES']['rows'])
fields=read('runtime/sap_reads/s4600_ex21_22_fields_readback.json')['tables']
assert fields['VBEP']['rows'][0]['MBDAT']=='20261027' and fields['VBEP']['rows'][0]['EDATU']=='20261029'
assert all(x['KZTLF']=='' for x in fields['VBAP']['rows'])
assert records['s4600_ex22_order.json']['after']['rows'][0]['CompleteDeliveryIsDefined'] is False
scope={'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'exercise':'26','operations':['SET_STORAGE_LOCATION_0001','PICK_EXACT_DELIVERY_QUANTITIES','POST_GOODS_ISSUE'],'plant':'FR10','storage_location':'0001','goods_movement_type':'601','proposed_posting_date':'2026-10-22','deliveries':{d:[{k:x[k] for k in ('DeliveryDocumentItem','Material','ActualDeliveryQuantity')} for x in v['rows']] for d,v in records['s4600_ex25_collective_deliveries.json']['all_delivery_items'].items()},'no_billing':True,'no_customizing':True,'no_material_ledger_change':True,'exclude':['80000085','80000086','80000087','80000091']}
checkpoint={'completed_exercises':[12,16,21,22,25],'partial_exercises':{'32':{'order':'163','delivery':'80000091','stopped_before':'PICKING_PGI_BILLING_CREDIT_MEMO'}},'evidence_verified':files,'next_approval':{'status':'PENDING_USER_APPROVAL','scope':scope,'fingerprint':hashlib.sha256(json.dumps(scope,sort_keys=True,separators=(',',':')).encode()).hexdigest()},'remaining':{'13_14':'Participant objects from9/11 not yet created; do not change common prices','26':'Exact scoped picking/PGI approval required','27':'Requires26 and separate exact billing approval','32':'Prepared only; separate FI/MM and credit memo approval required','33':'Depends on32 credit memo, then exact cancellation approval','34':'Return plant1020 adaptation not verified; stock-return/credit operations need exact scope','35':'Required Fiori UI automation unavailable; do not claim backend-only equivalent'}}
(ROOT/'runtime/sap_reads/s4600_remaining_batch_checkpoint_2026-10-22.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'offline_checks':'PASS','completed_exercises':checkpoint['completed_exercises'],'partial_exercises':checkpoint['partial_exercises'],'next_approval_fingerprint':checkpoint['next_approval']['fingerprint']},ensure_ascii=True,indent=2))
