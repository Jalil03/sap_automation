"""Assign the verified Book proposal to the exact customer sales area once."""
import json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
out=ROOT/'runtime/sap_writes/s4600_ex16_customer_assignment.json';assert not out.exists()
head=json.loads((ROOT/'runtime/sap_reads/s4600_batch16_21_rfc_preflight.json').read_text())['proposal_lookup']
detail=json.loads((ROOT/'runtime/sap_reads/s4600_ex16_details_ex21_stock_before.json').read_text())
assert head['row_count']==1 and head['rows'][0]['VBELN']=='0050000001'
assert [(x['MATNR'].lstrip('0'),float(x['ZMENG'])) for x in detail['proposal_items']['rows']]==[('10000282',5),('10000283',5)]
sap='{http://www.sap.com/Protocols/SAPData}'
assert detail['bp_update_contract']['set'][0].get(sap+'updatable')!='false'
assert detail['bp_update_contract']['property'][0].get(sap+'updatable')!='false'
s=SapGuiConnection(mode=SafetyMode.READ).attach();s.validate_identity()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
service='sap/opu/odata/sap/API_BUSINESS_PARTNER'
target="A_CustomerSalesArea(Customer='1000000112',SalesOrganization='FR10',DistributionChannel='10',Division='1W')"
q={'$filter':"Customer eq '1000000112' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'"}
before=get(c,'API_BUSINESS_PARTNER','A_CustomerSalesArea',q);assert before['http_status']==200 and before['count']==1 and before['rows'][0]['SalesItemProposal']==''
payload={'SalesItemProposal':'0050000001'}
token=c.request('GET',service+'/',headers={'X-CSRF-Token':'Fetch'}).header('X-CSRF-Token');assert token
r={'status':'ATTEMPT_RECORDED','approval_source':'User requested execution of untreated Book exercises; exercise16 step3','identity':s.identity,'target':target,'payload':payload,'before':before,'fingerprint':hashlib.sha256(json.dumps({'target':target,'payload':payload},sort_keys=True).encode()).hexdigest()}
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
persist();response=c.request('PATCH',service+'/'+target,headers={'X-CSRF-Token':token,'Content-Type':'application/json'},body=json.dumps(payload).encode())
r['http_status']=response.status;persist()
if response.status not in (200,204):r.update(status='SAP_ERROR',error=response.sanitized_sap_error());persist();raise SystemExit(str(r['error']))
r['after']=get(c,'API_BUSINESS_PARTNER','A_CustomerSalesArea',q)
assert r['after']['http_status']==200 and r['after']['count']==1 and r['after']['rows'][0]['SalesItemProposal'].lstrip('0')=='50000001'
r['status']='VERIFIED';persist()
p=ROOT/'runtime/sap_writes/s4600_ex16_proposal.json';record=json.loads(p.read_text(encoding='utf-8'));record.update(status='VERIFIED',proposal='0050000001',independent_header_readback=head,independent_items_readback=detail['proposal_items']);p.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':r['status'],'target':target,'payload':payload,'http_status':response.status}))
