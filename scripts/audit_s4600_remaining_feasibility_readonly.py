"""Current GET-only checks; never invoke persistent SAP actions."""
from __future__ import annotations
import json,sys
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.audit_s4600_ex30_mto_candidates_readonly import bounded_read
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode

def main():
    load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
    s=SapGuiConnection(mode=SafetyMode.READ).attach();s.validate_identity();c=UrllibSapTransport(cfg)
    r={'captured_at':datetime.now(timezone.utc).isoformat(),'environment':s.identity,'mode':'GET_ONLY_FEASIBILITY','sap_write_performed':False,'deliveries':{},'stocks':{},'contracts':{},'checks':{}}
    def read(service,entity,query):return bounded_read(c,service,entity,{**query,'$top':'21'})
    totals={}
    for delivery in ('80000088','80000089','80000090','80000091'):
        h=read('API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"})
        items=read('API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"DeliveryDocument eq '{delivery}'"})
        inv=read('API_BILLING_DOCUMENT_SRV','A_BillingDocumentItem',{'$filter':f"ReferenceSDDocument eq '{delivery}'"})
        r['deliveries'][delivery]={'header':h,'items':items,'billing':inv}
        if items['http_status']==200:
            for item in items['rows']:totals[item['Material']]=totals.get(item['Material'],Decimal(0))+Decimal(item['ActualDeliveryQuantity'])
    for material,qty in totals.items():
        stock=read('API_MATERIAL_STOCK_SRV','A_MatlStkInAcctMod',{'$filter':f"Material eq '{material}' and Plant eq 'FR10' and StorageLocation eq '0001'"})
        r['stocks'][material]={'read':stock,'required_for_four_deliveries':str(qty)}
        if stock['http_status']==200 and not stock.get('has_next_page'):
            available=sum((Decimal(x['MatlWrhsStkQtyInMatlBaseUnit']) for x in stock['rows'] if x['InventoryStockType']=='01' and x['InventorySpecialStockType']==''),Decimal(0))
            r['stocks'][material].update(unrestricted_quantity=str(available),physical_quantity_sufficient=available>=qty)
    ns={'e':'http://schemas.microsoft.com/ado/2008/09/edm'}
    for service in ('API_OUTBOUND_DELIVERY_SRV;v=2','API_BILLING_DOCUMENT_SRV'):
        response=c.request('GET','sap/opu/odata/sap/'+service+'/$metadata')
        md={'http_status':response.status,'functions':[]};r['contracts'][service]=md
        if response.status==200:
            root=ET.fromstring(response.body)
            for f in root.findall('.//e:FunctionImport',ns):
                md['functions'].append({'attributes':f.attrib,'parameters':[p.attrib for p in f.findall('e:Parameter',ns)]})
        else:md['error']=response.sanitized_sap_error()
    r['checks']['service_product_plant']=read('API_PRODUCT_SRV','A_ProductPlant',{'$filter':"Product eq '90000133' and Plant eq 'FR10'"})
    r['checks']['service_order']=read('API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':"SalesOrganization eq 'FR10' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '8-600'"})
    r['checks']['participant_product']=read('API_PRODUCT_SRV','A_Product',{'$filter':"Product eq 'T-MS400' or ProductOldID eq 'T-MS400'"})
    r['checks']['participant_customer']=read('API_BUSINESS_PARTNER','A_BusinessPartner',{'$filter':"BusinessPartner eq 'T-CUS00' or BusinessPartnerIDByExtSystem eq 'T-CUS00' or SearchTerm1 eq 'T-CUS00'"})
    for code in ('PR00','K007'):
        r['checks']['condition_'+code]=read('API_SLSPRICINGPROCEDURE_SRV','A_SlsPricingConditionType',{'$filter':f"ConditionType eq '{code}'",'$select':'ConditionType,AccessSequence'})
    r['checks']['invoice_90000090']=read('API_BILLING_DOCUMENT_SRV','A_BillingDocument',{'$filter':"BillingDocument eq '90000090'"})
    out=ROOT/'runtime/sap_reads/s4600_remaining_feasibility_readonly_2026-10-23.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'stocks':{k:{n:v for n,v in val.items() if n!='read'} for k,val in r['stocks'].items()},'deliveries':{k:{'header_status':v['header']['http_status'],'picking':v['header'].get('rows',[{}])[0].get('OverallPickingStatus'),'goods_movement':v['header'].get('rows',[{}])[0].get('OverallGoodsMovementStatus'),'items_count':v['items'].get('count'),'invoice_count':v['billing'].get('count')} for k,v in r['deliveries'].items()},'checks':{k:{n:v.get(n) for n in ('http_status','count','classification')} for k,v in r['checks'].items()},'functions':{k:[f['attributes']['Name'] for f in v['functions']] for k,v in r['contracts'].items()}},ensure_ascii=True,indent=2))
if __name__=='__main__':main()
