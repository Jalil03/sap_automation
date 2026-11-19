"""Two distinct Book delivery tests, once per verified source state."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.readback_s4600_ex17 import readback
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode

phase=sys.argv[1];assert phase in {'initial','corrected'}
out=ROOT/('runtime/sap_writes/s4600_ex17_delivery_'+phase+'.json')
assert not out.exists(),'Attempt already recorded; independent reconciliation required'
state=readback(phase);assert state['status']=='VERIFIED'
assert state['order']=='158' and state['deliveries']['http_status']==200 and state['deliveries']['count']==0
session=SapGuiConnection(mode=SafetyMode.READ).attach();session.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
client=UrllibSapTransport(cfg)
payload={'to_DeliveryDocumentItem':{'results':[{'ReferenceSDDocument':'158'}]}}
scope={'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'phase':phase,'payload':payload,
       'source_reference':state['header']['rows'][0]['PurchaseOrderByCustomer'],
       'source_net_weight':state['items']['rows'][0]['ItemNetWeight'],'maximum_post_attempts':1}
digest=hashlib.sha256(json.dumps(scope,sort_keys=True,separators=(',',':')).encode()).hexdigest()
service='sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV'
token_response=client.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch','Accept':'application/json'})
token=token_response.header('X-CSRF-Token');assert token_response.status==200 and token
result={'status':'ATTEMPT_RECORDED','phase':phase,'approval_source':'User: on traite le 17; Book steps 3 and 6',
        'scope':scope,'sha256':digest,'attempted_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_preflight':state,'post_attempted':True}
def save():out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
save()
try:
    response=client.request('POST',service+'/A_OutbDeliveryHeader',
        headers={'X-CSRF-Token':token,'Content-Type':'application/json'},
        body=json.dumps(payload,separators=(',',':')).encode())
    result['http_status']=response.status
    if response.status==201:result['response']=response.json()
    else:result['error']=response.sanitized_sap_error()
except Exception as error:
    result['status']='AMBIGUOUS_RECONCILIATION_REQUIRED';result['error_type']=type(error).__name__
    save();raise
linked=get(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':"ReferenceSDDocument eq '158'"})
result['linked_deliveries_after']=linked
if response.status!=201:
    result['status']='EXPECTED_REJECTION_VERIFIED' if phase=='initial' and linked['http_status']==200 and linked['count']==0 else 'REJECTED'
else:
    rows=linked.get('rows',[])
    if linked['http_status']==200 and len(rows)==1:
        item=rows[0]; delivery=item['DeliveryDocument']
        header=get(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"})
        result.update(delivery=delivery,header_readback=header)
        ok=item['ReferenceSDDocument']=='158' and item['Material']=='10000283' and Decimal(item['ActualDeliveryQuantity'])==10
        ok=ok and header['http_status']==200 and header['count']==1 and header['rows'][0]['ShippingPoint']=='FR10'
        result['status']='DELIVERY_VERIFIED' if ok else 'READBACK_MISMATCH'
    else:result['status']='RECONCILIATION_REQUIRED'
save()
print(json.dumps({k:result.get(k) for k in ('status','phase','http_status','error','delivery')},ensure_ascii=False,indent=2))
