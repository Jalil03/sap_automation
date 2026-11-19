"""Targeted API-first discovery for the remaining authorized Book exercises."""
import json,sys
from pathlib import Path
from datetime import datetime,timezone
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env()
assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
c=UrllibSapTransport(cfg)
result={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'mode':'GET_ONLY','checks':{}}
md=c.request('GET','sap/opu/odata/sap/API_CUSTOMER_MATERIAL_SRV/$metadata')
result['customer_material_metadata_status']=md.status
if md.status==200:
    out=ROOT/'runtime/sap_reads/s4600_customer_material_metadata_2026-10-22.xml';out.write_bytes(md.body)
    ns={'e':'http://schemas.microsoft.com/ado/2008/09/edm'};sap='{http://www.sap.com/Protocols/SAPData}'
    root=ET.fromstring(md.body)
    result['customer_material_sets']=[dict(n.attrib) for n in root.findall('.//e:EntitySet',ns)]
    result['customer_material_fields']=[dict(n.attrib) for n in root.findall(".//e:EntityType[@Name='A_CustomerMaterialType']/e:Property",ns)]
    result['checks']['customer_material']=get(c,'API_CUSTOMER_MATERIAL_SRV','A_CustomerMaterial',{
        '$filter':"SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Customer eq '1000000112' and Material eq '10000282'"})
for ex,reference in [('12','5-1900'),('13','5-2300'),('14','5-2400'),('16','00-Proposition'),('21','7-600'),('22','7-700')]:
    result['checks']['order_'+ex]=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':f"SalesOrganization eq 'FR10' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '{reference}'",'$select':'SalesOrder,PurchaseOrderByCustomer','$top':'2'})
out=ROOT/'runtime/sap_reads/s4600_remaining_batch_preflight_2026-10-22.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
