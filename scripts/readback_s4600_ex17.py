"""Independent GET-only Exercise 17 document reconciliation."""
import json,sys
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

def readback(phase='initial'):
    load_dotenv(ROOT/'.env'); cfg=SapRuntimeConfig.from_env()
    assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
    client=UrllibSapTransport(cfg)
    if phase=='initial':
        headers=get(client,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':"SoldToParty eq '1000000112' and SalesOrganization eq 'FR10' and PurchaseOrderByCustomer eq ''",'$top':'2'})
    else:
        previous=json.loads((ROOT/'runtime/sap_reads/s4600_ex17_initial_readback.json').read_text(encoding='utf-8'))
        headers=get(client,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':"SalesOrder eq '"+previous['order']+"'"})
    assert headers['http_status']==200 and headers['count']==1,headers
    h=headers['rows'][0]; number=h['SalesOrder']
    items=get(client,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{number}'"})
    schedules=get(client,'API_SALES_ORDER_SRV','A_SalesOrderScheduleLine',{'$filter':f"SalesOrder eq '{number}'"})
    deliveries=get(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"ReferenceSDDocument eq '{number}'"})
    expected_ref='' if phase=='initial' else '3-900'
    expected_weight='0' if phase=='initial' else '20'
    errors=[]
    for key,expected in {'SalesOrderType':'CS','SalesOrganization':'FR10','DistributionChannel':'10','OrganizationDivision':'1W','SoldToParty':'1000000112','PurchaseOrderByCustomer':expected_ref}.items():
        if h.get(key)!=expected:errors.append({'field':key,'actual':h.get(key),'expected':expected})
    if items['http_status']!=200 or items.get('count')!=1:errors.append({'error':'item_readback'})
    else:
        item=items['rows'][0]
        if item.get('Material')!='10000283' or Decimal(item.get('RequestedQuantity','-1'))!=10:errors.append({'error':'item_mismatch'})
        if Decimal(item.get('ItemNetWeight','-1'))!=Decimal(expected_weight):errors.append({'error':'weight_mismatch','actual':item.get('ItemNetWeight')})
    result={'status':'VERIFIED' if not errors else 'MISMATCH','phase':phase,'order':number,
            'header':headers,'items':items,'schedules':schedules,'deliveries':deliveries,'mismatches':errors}
    out=ROOT/('runtime/sap_reads/s4600_ex17_'+phase+'_readback.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'phase':phase,'status':result['status'],'order':number,'mismatches':errors,
                      'header_status':{k:v for k,v in h.items() if 'Status' in k},
                      'item_status':[{k:v for k,v in i.items() if 'Status' in k or 'Weight' in k} for i in items.get('rows',[])]},ensure_ascii=False,indent=2))
    return result
if __name__=='__main__':readback(sys.argv[1] if len(sys.argv)>1 else 'initial')
