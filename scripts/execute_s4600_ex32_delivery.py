"""Prepare exercise32 delivery only, using the proven reference-order API."""
import json,sys,hashlib
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
out=ROOT/'runtime/sap_writes/s4600_ex32_delivery.json';assert not out.exists()
source=json.loads((ROOT/'runtime/sap_writes/s4600_ex32_order.json').read_text(encoding='utf-8'));assert source['status']=='VERIFIED' and source['order']=='163'
s=SapGuiConnection(mode=SafetyMode.READ).attach();s.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
q={'$filter':"ReferenceSDDocument eq '163'"};before=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',q);assert before['http_status']==200 and before['count']==0
order=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':"SalesOrder eq '163'"});assert order['http_status']==200 and order['count']==1 and order['rows'][0]['PurchaseOrderByCustomer']=='9-100'
payload={'to_DeliveryDocumentItem':{'results':[{'ReferenceSDDocument':'163'}]}}
service='sap/opu/odata/sap/API_OUTBOUND_DELIVERY_SRV';token=c.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch'}).header('X-CSRF-Token');assert token
r={'status':'ATTEMPT_RECORDED','approval_source':'User requested untreated Book exercises; exercise32 steps3-4 only','identity':s.identity,'payload':payload,'before':before,'fingerprint':hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest(),'no_pgi':True,'no_billing':True,'no_credit_memo':True}
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
persist();response=c.request('POST',service+'/A_OutbDeliveryHeader',headers={'X-CSRF-Token':token,'Content-Type':'application/json'},body=json.dumps(payload).encode());r['http_status']=response.status;persist()
if response.status!=201:r.update(status='SAP_ERROR',error=response.sanitized_sap_error());persist();raise SystemExit(str(r['error']))
r['after']=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',q);persist();assert r['after']['http_status']==200 and r['after']['count']==1
item=r['after']['rows'][0];assert item['Material']=='10000282' and Decimal(item['ActualDeliveryQuantity'])==5 and item['DeliveryDocumentItemText']==source['items']['rows'][0]['SalesOrderItemText']
delivery=item['DeliveryDocument'];r['delivery']=delivery;r['header']=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"})
assert r['header']['http_status']==200 and r['header']['count']==1 and r['header']['rows'][0]['OverallGoodsMovementStatus']=='A'
r['status']='VERIFIED';persist();print(json.dumps({'status':r['status'],'delivery':delivery,'no_pgi':True}))
