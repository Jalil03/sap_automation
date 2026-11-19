"""Independently reconcile the single collective attempt; never writes SAP."""
import json,sys
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
out=ROOT/'runtime/sap_writes/s4600_ex25_collective_deliveries.json';r=json.loads(out.read_text(encoding='utf-8'))
assert r['status'] in ('SUBMITTED_REQUIRES_INDEPENDENT_READBACK','READBACK_INCOMPLETE','VERIFIED')
r['after']={};deliveries=set();ok=True
for order in r['scope']['orders']:
    read=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"ReferenceSDDocument eq '{order}'"});r['after'][order]=read
    if read['http_status']!=200:ok=False;continue
    expected={x['SalesOrderItem'].lstrip('0'):(x['Material'],Decimal(x['RequestedQuantity'])) for x in r['scope']['source_items'][order]['rows']}
    actual={x['ReferenceSDDocumentItem'].lstrip('0'):(x['Material'],Decimal(x['ActualDeliveryQuantity'])) for x in read['rows']}
    ok=ok and actual==expected and len(read['rows'])==len(expected)
    deliveries.update(x['DeliveryDocument'] for x in read['rows'])
r['headers']={};r['all_delivery_items']={}
for delivery in sorted(deliveries):
    h=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"});r['headers'][delivery]=h
    ok=ok and h['http_status']==200 and h['count']==1 and h['rows'][0]['ShippingPoint']=='FR10' and h['rows'][0]['OverallGoodsMovementStatus']=='A'
    all_items=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"DeliveryDocument eq '{delivery}'"});r['all_delivery_items'][delivery]=all_items
    ok=ok and all_items['http_status']==200 and all(x['ReferenceSDDocument'] in r['scope']['orders'] for x in all_items['rows'])
r['deliveries']=sorted(deliveries);r['status']='VERIFIED' if ok and 0<len(deliveries)<=6 else 'READBACK_INCOMPLETE'
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':r['status'],'deliveries':r['deliveries'],'order_items':{k:[{n:x.get(n) for n in ('DeliveryDocument','DeliveryDocumentItem','ReferenceSDDocument','ReferenceSDDocumentItem','Material','ActualDeliveryQuantity')} for x in v['rows']] for k,v in r['after'].items()}},ensure_ascii=True,indent=2))
