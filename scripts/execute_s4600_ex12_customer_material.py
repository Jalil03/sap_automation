"""Create one Book customer-material record through its evidenced SAP API."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
OUT=ROOT/'runtime/sap_writes/s4600_ex12_customer_material_2026-10-22.json'
payload={'SalesOrganization':'FR10','DistributionChannel':'10','Customer':'1000000112','Material':'10000282',
         'MaterialByCustomer':'K-MS-00','MaterialDescriptionByCustomer':'Phare Premium'}
query={'$filter':"SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Customer eq '1000000112' and (Material eq '10000282' or MaterialByCustomer eq 'K-MS-00')"}
assert not OUT.exists(),'Existing attempt: reconcile only'
session=SapGuiConnection(mode=SafetyMode.READ).attach();session.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
c=UrllibSapTransport(cfg)
pre=json.loads((ROOT/'runtime/sap_reads/s4600_remaining_batch_preflight_2026-10-22.json').read_text(encoding='utf-8'))
assert pre['customer_material_metadata_status']==200
fields={f['Name'] for f in pre['customer_material_fields']};assert set(payload)<=fields
before=get(c,'API_CUSTOMER_MATERIAL_SRV','A_CustomerMaterial',query)
assert before['http_status']==200 and before['count']==0
customer=get(c,'API_BUSINESS_PARTNER','A_CustomerSalesArea',{'$filter':"Customer eq '1000000112' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'"})
product=get(c,'API_PRODUCT_SRV','A_ProductSalesDelivery',{'$filter':"Product eq '10000282' and ProductSalesOrg eq 'FR10' and ProductDistributionChnl eq '10'"})
assert all(r['http_status']==200 and r['count']==1 for r in (customer,product))
service='sap/opu/odata/sap/API_CUSTOMER_MATERIAL_SRV'
token_response=c.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch','Accept':'application/json'})
token=token_response.header('X-CSRF-Token');assert token_response.status==200 and token
digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
result={'status':'ATTEMPT_RECORDED','environment':session.identity,'operation':'CREATE_ONE_EX12_CUSTOMER_MATERIAL',
        'approval_source':'User: on attque les exercices qu\u0027on a pas encore fit; S4600 group00 FR10 mapping',
        'payload':payload,'sha256':digest,'before':before,'post_attempted':True,
        'attempted_at_utc':datetime.now(timezone.utc).isoformat(),
        'contract_source':'https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/05685c9bab7b46ccb42c40ed18314f27.html'}
def save():OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save()
response=c.request('POST',service+'/A_CustomerMaterial',headers={'X-CSRF-Token':token,'Content-Type':'application/json'},body=json.dumps(payload).encode())
result['http_status']=response.status
if response.status!=201:
    result.update(status='SAP_ERROR',error=response.sanitized_sap_error());save()
    raise SystemExit(json.dumps({'status':result['status'],'error':result['error']}))
after=get(c,'API_CUSTOMER_MATERIAL_SRV','A_CustomerMaterial',query);result['after']=after
ok=after['http_status']==200 and after['count']==1 and all(after['rows'][0].get(k)==v for k,v in payload.items())
result['status']='VERIFIED' if ok else 'READBACK_MISMATCH';save()
print(json.dumps({'status':result['status'],'http_status':response.status,'payload':payload},ensure_ascii=False,indent=2))
