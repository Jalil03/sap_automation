"""Narrow existing-returns read, using the live metadata discovered today."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
pre=json.loads((ROOT/'runtime/sap_reads/s4600_ex1_23_30_34_preflight_2026-10-23.json').read_text(encoding='utf-8'))
types=pre['metadata']['API_CUSTOMER_RETURN_SRV']['types'];sets={x['Name'] for x in pre['metadata']['API_CUSTOMER_RETURN_SRV']['sets']}
r={'mode':'GET_ONLY','sap_write_performed':False,'queries':{}}
for entity,type_name,expression,fields in [
    ('A_CustomerReturn','A_CustomerReturnType',"SalesOrganization eq 'FR10'",['CustomerReturn','CustomerReturnType','SalesOrganization','DistributionChannel','OrganizationDivision','SoldToParty','CreatedByUser','TotalNetAmount','TransactionCurrency','SDDocumentReason']),
    ('A_CustomerReturnItem','A_CustomerReturnItemType',"Material eq '10000284' and ProductionPlant eq 'FR10'",['CustomerReturn','CustomerReturnItem','CustomerReturnItemCategory','Material','RequestedQuantity','ProductionPlant','ShippingPoint','StorageLocation'])]:
    assert entity in sets and set(fields)<={x['Name'] for x in types[type_name]['properties']}
    r['queries'][entity]=get(c,'API_CUSTOMER_RETURN_SRV',entity,{'$filter':expression,'$select':','.join(fields),'$top':'5'})
r['absence_inference']='No rows means no match for this narrow query, not absence of all possible return configuration.'
(ROOT/'runtime/sap_reads/s4600_ex34_existing_returns_2026-10-23.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True,indent=2))
