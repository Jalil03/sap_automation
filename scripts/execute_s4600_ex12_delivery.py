"""Create and read back the single Exercise 12 delivery; never post goods issue."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
out=ROOT/'runtime/sap_writes/s4600_ex12_delivery_2026-10-22.json';assert not out.exists()
source=json.loads((ROOT/'runtime/sap_writes/s4600_ex12_order_2026-10-22.json').read_text(encoding='utf-8'))
assert source['status']=='VERIFIED' and source['order']=='159'
session=SapGuiConnection(mode=SafetyMode.READ).attach();session.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
c=UrllibSapTransport(cfg);query={'$filter':"ReferenceSDDocument eq '159'"}
before=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',query);assert before['http_status']==200 and before['count']==0
order=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':"SalesOrder eq '159'"});assert order['http_status']==200 and order['count']==1 and order['rows'][0]['PurchaseOrderByCustomer']=='5-1900'
payload={'to_DeliveryDocumentItem':{'results':[{'ReferenceSDDocument':'159'}]}}
digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
service='sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV'
token_response=c.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch','Accept':'application/json'})
token=token_response.header('X-CSRF-Token');assert token_response.status==200 and token
result={'status':'ATTEMPT_RECORDED','approval_source':'User: on attque les exercices qu\u0027on a pas encore fit; Book exercise 12 step 4',
        'environment':session.identity,'payload':payload,'sha256':digest,'post_attempted':True,'before':before,
        'attempted_at_utc':datetime.now(timezone.utc).isoformat()}
def save():out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save()
response=c.request('POST',service+'/A_OutbDeliveryHeader',headers={'X-CSRF-Token':token,'Content-Type':'application/json'},body=json.dumps(payload).encode())
result['http_status']=response.status
if response.status!=201:
    result.update(status='SAP_ERROR',error=response.sanitized_sap_error());save();raise SystemExit(json.dumps(result['error']))
after=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',query);result['after']=after
assert after['http_status']==200 and after['count']==1,'Readback requires reconciliation; do not retry'
item=after['rows'][0];delivery=item['DeliveryDocument']
header=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"})
ok=item['Material']=='10000282' and Decimal(item['ActualDeliveryQuantity'])==10 and item['DeliveryDocumentItemText']=='Phare Premium'
ok=ok and header['http_status']==200 and header['count']==1 and header['rows'][0]['OverallGoodsMovementStatus']=='A'
result.update(status='VERIFIED' if ok else 'READBACK_MISMATCH',delivery=delivery,header=header);save()
print(json.dumps({'status':result['status'],'delivery':delivery,'description':item['DeliveryDocumentItemText'],'goods_issue_posted':False},ensure_ascii=False,indent=2))
