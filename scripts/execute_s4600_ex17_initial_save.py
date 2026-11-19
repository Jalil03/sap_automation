"""One scoped initial save of the Exercise 17 incomplete order."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from scripts.stage_s4600_ex19_va01 import TABLE,BODY
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
OUT=ROOT/'runtime/sap_writes/s4600_ex17_initial_save_2026-10-22.json'
assert not OUT.exists(), 'A save checkpoint already exists; reconcile rather than repeat'
load_dotenv(ROOT/'.env'); config=SapRuntimeConfig.from_env()
assert config.client=='600' and config.username.upper()=='ABDELJ'
before=get(UrllibSapTransport(config),'API_SALES_ORDER_SRV','A_SalesOrder',{
    '$filter':"SoldToParty eq '1000000112' and SalesOrganization eq 'FR10' and (PurchaseOrderByCustomer eq '' or PurchaseOrderByCustomer eq '3-900')",'$top':'2'})
assert before['http_status']==200 and before['count']==0
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='500' and int(s.raw.Children.Count)==1
assert 'protocole de documents incomplets' in str(s.find('wnd[0]').Text)
grid=s.find('wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell')
assert grid.RowCount==2 and {grid.GetCellValue(i,'FELD') for i in range(2)}=={'Référence client','Poids net'}
s.audit('BACK',value='Return from verified incompletion log to draft')
s.find('wnd[0]/tbar[0]/btn[3]').Press()
assert str(s.raw.Info.ScreenNumber)=='4003'
weight='wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03/ssubSUBSCREEN_BODY:SAPMV45A:4452/txtVBAP-NTGEW'
assert str(s.find(weight).Text).strip() in {'','0','0,000'}
assert s.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4013/ctxtRV45A-MABNR').Text=='10000283'
s.audit('BACK',value='Return to overview for exact before-save checks')
s.find('wnd[0]/tbar[0]/btn[3]').Press()
assert str(s.raw.Info.ScreenNumber)=='4001'
prefix=str(s.raw.Id)
def mapped(k):return k.replace('/app/con[0]/ses[0]',prefix,1)
values={'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR':'1000000112',
        'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD':'',
        'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR':'800,00',
        mapped(TABLE)+'/ctxtRV45A-MABNR[1,0]':'10000283',mapped(TABLE)+'/txtRV45A-KWMENG[3,0]':'10',
        mapped(TABLE)+'/ctxtRV45A-MABNR[1,1]':'',mapped(TABLE)+'/ctxtVBAP-WERKS[12,0]':'FR10'}
for key,value in values.items():assert str(s.find(key).Text).strip()==value,key
date=str(s.find(mapped(BODY)+'/ssubHEADER_FRAME:SAPMV45A:4440/ctxtRV45A-KETDAT').Text).strip()
scope={'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'type':'CS','sales_area':'FR10/10/1W',
       'sold_to':'1000000112','reference':'','material':'10000283','quantity':'10','unit':'289','net_weight':'0',
       'weight_unit':'KG','requested_date':date,'date_source':'SAP proposal observed in draft',
       'net_amount':'800.00','currency':'EUR'}
digest=hashlib.sha256(json.dumps(scope,sort_keys=True,separators=(',',':')).encode()).hexdigest()
result={'status':'INITIAL_SAVE_ATTEMPT_RECORDED','approval_source':'User: on traite le 17',
        'scope':scope,'sha256':digest,'before_lookup':before,'save_attempted':True,
        'attempted_at_utc':datetime.now(timezone.utc).isoformat()}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
button=s.find('wnd[0]/tbar[0]/btn[11]'); assert button.Text=='Sauvegarder'
s.audit('PHASE5_OPERATION',control_id=str(button.Id),value={'operation':'SAVE_EX17_INCOMPLETE','sha256':digest})
button.Press()
result['save_returned']=True
result['status_bar']={'text':str(s.find('wnd[0]/sbar').Text),'type':str(s.find('wnd[0]/sbar').MessageType)}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
