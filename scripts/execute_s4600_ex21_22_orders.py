"""One evidenced OData order per requested exercise, no posting or retries."""
import json,sys,hashlib
from pathlib import Path
from decimal import Decimal
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get,odata_date
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
ex=sys.argv[1];assert ex in ('21','22','32')
reference={'21':'7-600','22':'7-700','32':'9-100'}[ex]
items={'21':[('10000284','20')],'22':[('10000282','10'),('10000283','10')],'32':[('10000282','5')]}[ex]
out=ROOT/f'runtime/sap_writes/s4600_ex{ex}_order.json';assert not out.exists(),'Reconcile existing attempt; never blindly repeat'
if ex=='21':
    baseline=json.loads((ROOT/'runtime/sap_reads/s4600_ex16_details_ex21_stock_before_normalized.json').read_text())
    assert baseline['stock_return']['TYPE']=='S' and baseline['stock_tables']['MRP_IND_LINES']['rows']
payload={'SalesOrderType':'CS','SalesOrganization':'FR10','DistributionChannel':'10','OrganizationDivision':'1W','SoldToParty':'1000000112','PurchaseOrderByCustomer':reference,'RequestedDeliveryDate':odata_date('2026-10-29'),'to_Item':[{'SalesOrderItem':str(i*10),'Material':m,'RequestedQuantity':qty,'RequestedQuantityUnit':'289'} for i,(m,qty) in enumerate(items,1)]}
s=SapGuiConnection(mode=SafetyMode.READ).attach();s.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
q={'$filter':f"SalesOrganization eq 'FR10' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '{reference}'"}
before=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',q);assert before['http_status']==200 and before['count']==0
customer=get(c,'API_BUSINESS_PARTNER','A_CustomerSalesArea',{'$filter':"Customer eq '1000000112' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'"});assert customer['http_status']==200 and customer['count']==1
assert customer['rows'][0]['SupplyingPlant']=='FR10'
plant_evidence={}
for material,_ in items:
    product=get(c,'API_PRODUCT_SRV','A_ProductSalesDelivery',{'$filter':f"Product eq '{material}' and ProductSalesOrg eq 'FR10' and ProductDistributionChnl eq '10'"})
    assert product['http_status']==200 and product['count']==1
    if product['rows'][0]['SupplyingPlant']=='':
        proven=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '157' and Material eq '{material}'"})
        assert proven['http_status']==200 and proven['count']==1 and proven['rows'][0]['ProductionPlant']=='FR10'
        plant_evidence[material]={'source':'Customer supplying plant, independently corroborated by existing order157 item','readback':proven}
    else:assert product['rows'][0]['SupplyingPlant']=='FR10'
service='sap/opu/odata/sap/API_SALES_ORDER_SRV'
token=c.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch'}).header('X-CSRF-Token');assert token
r={'status':'ATTEMPT_RECORDED','approval_source':'User requested execution of untreated Book exercises','book_source':f'S4600 exercise{ex}; immutable canonical Book; approved group00/FR10 mappings','identity':s.identity,'payload':payload,'fingerprint':hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'before':before,'plant_evidence':plant_evidence,'attempted_at':datetime.now(timezone.utc).isoformat(),'no_posting':True}
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
persist();response=c.request('POST',service+'/A_SalesOrder',headers={'X-CSRF-Token':token,'Content-Type':'application/json'},body=json.dumps(payload).encode());r['http_status']=response.status;persist()
if response.status!=201:r.update(status='SAP_ERROR',error=response.sanitized_sap_error());persist();raise SystemExit(str(r['error']))
r['after']=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',q);persist();assert r['after']['http_status']==200 and r['after']['count']==1
h=r['after']['rows'][0];order=h['SalesOrder'];r['order']=order
assert (h['SalesOrderType'],h['DistributionChannel'],h['OrganizationDivision'])==('CS','10','1W')
assert h['RequestedDeliveryDate']==payload['RequestedDeliveryDate']
r['items']=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{order}'"});persist();assert r['items']['http_status']==200 and r['items']['count']==len(items)
assert [(x['Material'],Decimal(x['RequestedQuantity'])) for x in r['items']['rows']]==[(m,Decimal(qty)) for m,qty in items]
assert all(x['ProductionPlant']=='FR10' for x in r['items']['rows'])
r['schedule_lines']=get(c,'API_SALES_ORDER_SRV','A_SalesOrderScheduleLine',{'$filter':f"SalesOrder eq '{order}'"})
r['status']='VERIFIED';persist()
print(json.dumps({'status':r['status'],'exercise':ex,'order':order,'net':h['TotalNetAmount'],'schedule_lines':r['schedule_lines'],'complete_delivery':h.get('CompleteDeliveryIsDefined'),'partial_delivery':[x.get('PartialDeliveryIsAllowed') for x in r['items']['rows']]},ensure_ascii=True))
