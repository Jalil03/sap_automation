"""Save the proposal-derived exercise16 draft once and independently read it."""
import json,sys,hashlib
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from scripts.stage_s4600_ex19_va01 import TABLE
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
out=ROOT/'runtime/sap_writes/s4600_ex16_order.json';assert not out.exists()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
q={'$filter':"SalesOrganization eq 'FR10' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '00-Proposition'"}
before=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',q);assert before['http_status']==200 and before['count']==0
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach();assert s.identity['transaction']=='VA01' and int(s.raw.Children.Count)==1
table=TABLE.replace('/app/con[0]/ses[0]',str(s.raw.Id),1)
for row,material in enumerate(('10000282','10000283')):
    assert s.find(f'{table}/ctxtRV45A-MABNR[1,{row}]').Text==material
    assert s.find(f'{table}/txtRV45A-KWMENG[3,{row}]').Text.strip()=='5'
assert s.find(f'{table}/ctxtRV45A-MABNR[1,2]').Text.strip()==''
assert s.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD').Text=='00-Proposition'
assert s.find('wnd[0]/sbar').MessageType not in ('E','A')
scope={'reference':'00-Proposition','customer':'1000000112','sales_area':'FR10/10/1W','proposal':'0050000001','items':[['10000282','5'],['10000283','5']],'date_source':'SAP default; Book does not prescribe delivery date'}
r={'status':'ATTEMPT_RECORDED','approval_source':'User requested untreated Book exercises; exercise16 step5','scope':scope,'fingerprint':hashlib.sha256(json.dumps(scope,sort_keys=True).encode()).hexdigest(),'before':before}
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
persist();b=s.find('wnd[0]/tbar[0]/btn[11]');assert b.Text=='Sauvegarder';s.audit('PHASE5_OPERATION',control_id=str(b.Id),value={'operation':'SAVE_EX16_ORDER','fingerprint':r['fingerprint']});b.Press()
r['message']=s.find('wnd[0]/sbar').Text;persist()
r['after']=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',q);assert r['after']['http_status']==200 and r['after']['count']==1
order=r['after']['rows'][0]['SalesOrder'];r['order']=order
r['items']=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{order}'"})
assert r['items']['http_status']==200 and r['items']['count']==2
assert [(x['Material'],Decimal(x['RequestedQuantity'])) for x in r['items']['rows']]==[('10000282',5),('10000283',5)]
r['status']='VERIFIED';persist();print(json.dumps({'status':r['status'],'order':order,'message':r['message']},ensure_ascii=True))
