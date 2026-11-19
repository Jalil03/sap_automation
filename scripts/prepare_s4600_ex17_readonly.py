"""GET-only preflight for the Exercise 17 incomplete order lifecycle."""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env')
config=SapRuntimeConfig.from_env()
assert config.client=='600' and config.username.upper()=='ABDELJ'
client=UrllibSapTransport(config)
checks={}
checks['existing_orders']=get(client,'API_SALES_ORDER_SRV','A_SalesOrder',{
    '$filter':"SoldToParty eq '1000000112' and SalesOrganization eq 'FR10' and (PurchaseOrderByCustomer eq '3-900' or PurchaseOrderByCustomer eq '')",'$top':'100'})
assert checks['existing_orders']['http_status']==200 and checks['existing_orders']['count']<100
for header in checks['existing_orders']['rows']:
    number=header['SalesOrder']
    checks['items_'+number]=get(client,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{number}'"})
checks['customer']=get(client,'API_BUSINESS_PARTNER','A_CustomerSalesArea',{
    '$filter':"Customer eq '1000000112' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'"})
checks['product']=get(client,'API_PRODUCT_SRV','A_ProductSalesDelivery',{
    '$filter':"Product eq '10000283' and ProductSalesOrg eq 'FR10' and ProductDistributionChnl eq '10'"})
result={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'mode':'GET_ONLY','checks':checks}
output=ROOT/'runtime/sap_reads/s4600_ex17_preflight_2026-10-22.json'
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
