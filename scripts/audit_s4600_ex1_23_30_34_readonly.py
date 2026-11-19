"""Narrow GET-only checks for the four newly requested Book exercises."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
s=SapGuiConnection(mode=SafetyMode.READ).attach();s.validate_identity();c=UrllibSapTransport(cfg)
r={'captured_at':datetime.now(timezone.utc).isoformat(),'environment':s.identity,'mode':'GET_ONLY','sap_write_performed':False,'metadata':{},'checks':{}}
ns={'e':'http://schemas.microsoft.com/ado/2008/09/edm'}
for service in ('API_PRODUCT_SRV','API_CUSTOMER_RETURN_SRV'):
    response=c.request('GET','sap/opu/odata/sap/'+service+'/$metadata')
    md={'http_status':response.status};r['metadata'][service]=md
    if response.status==200:
        root=ET.fromstring(response.body);md['sets']=[x.attrib for x in root.findall('.//e:EntitySet',ns)]
        md['types']={x.get('Name'):{'keys':[y.get('Name') for y in x.findall('e:Key/e:PropertyRef',ns)],'properties':[y.attrib for y in x.findall('e:Property',ns)]} for x in root.findall('.//e:EntityType',ns)}
    else:md['error']=response.sanitized_sap_error()
for plant in ('FR10','1020'):
    response=c.request('GET',f"sap/opu/odata/sap/API_PLANT_SRV/A_Plant('{plant}')",headers={'Accept':'application/json'})
    r['checks']['plant_'+plant]={'http_status':response.status,'row':response.json().get('d',{}) if response.status==200 else None,'error':None if response.status==200 else response.sanitized_sap_error()}
r['checks']['ex23_material_plants']=get(c,'API_PRODUCT_SRV','A_ProductPlant',{'$filter':"Product eq '10000284'",'$select':'Product,Plant,AvailabilityCheckType','$top':'100'})
r['checks']['ex23_stock']=get(c,'API_MATERIAL_STOCK_SRV','A_MatlStkInAcctMod',{'$filter':"Material eq '10000284' and Plant eq 'FR10'"})
r['checks']['ex30_literal']=get(c,'API_PRODUCT_SRV','A_Product',{'$filter':"Product eq 'T-F100'"})
r['checks']['ex30_oldid']=get(c,'API_PRODUCT_SRV','A_Product',{'$filter':"ProductOldID eq 'T-F100'",'$top':'10'})
for ex,ref,customer in (('23','7-300','1000000113'),('30','8-900','1000000112')):
    rows=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':f"SalesOrganization eq 'FR10' and SoldToParty eq '{customer}' and PurchaseOrderByCustomer eq '{ref}'"})
    r['checks']['ex'+ex+'_orders']=rows
    for row in rows.get('rows',[]):r['checks']['order_'+row['SalesOrder']+'_items']=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':"SalesOrder eq '"+row['SalesOrder']+"'"})
response=c.request('GET',"sap/opu/odata/sap/API_SALESORDERTYPE_SRV/A_SalesOrderType('RE')",headers={'Accept':'application/json'})
r['checks']['return_type_RE']={'http_status':response.status,'row':response.json().get('d',{}) if response.status==200 else None}
out=ROOT/'runtime/sap_reads/s4600_ex1_23_30_34_preflight_2026-10-23.json'
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'metadata':{k:{'http_status':v['http_status'],'sets':[x['Name'] for x in v.get('sets',[]) if k!='API_PRODUCT_SRV' or 'Supply' in x['Name']]} for k,v in r['metadata'].items()},'checks':r['checks']},ensure_ascii=True,indent=2))
