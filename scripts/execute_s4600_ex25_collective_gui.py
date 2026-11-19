"""Single scoped collective delivery creation; no picking, PGI or billing."""
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
out=ROOT/'runtime/sap_writes/s4600_ex25_collective_deliveries.json';assert not out.exists(),'Reconcile only after any attempt'
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach();assert s.identity['transaction']=='VL10A' and int(s.raw.Children.Count)==1
g=s.find('wnd[0]/usr/cntlGRID1/shellcont/shell');assert int(g.RowCount)==6
observed=[(str(g.GetCellValue(i,'VBELV')),str(g.GetCellValue(i,'KUNWE'))) for i in range(6)]
expected=[('160','1000000112'),('157','1000000112'),('157','1000000113'),('161','1000000112'),('162','1000000112'),('156','1000000113')];assert observed==expected
orders=['156','157','160','161','162'];before={};source_items={}
for order in orders:
    before[order]=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"ReferenceSDDocument eq '{order}'"});assert before[order]['http_status']==200 and before[order]['count']==0
    source_items[order]=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{order}'"});assert source_items[order]['http_status']==200 and source_items[order]['count']>0
scope={'operation':'CREATE_COLLECTIVE_OUTBOUND_DELIVERIES_ONLY','orders':orders,'source_items':source_items,'shipping_point':'FR10','from':'2026-10-19','to':'2026-11-01','maximum_deliveries':6,'excluded_orders_already_delivered':['158','159'],'no_pgi':True,'no_billing':True}
r={'status':'ATTEMPT_RECORDED','approval_source':'User requested execution of untreated Book exercises; exercise25 collective delivery creation','scope':scope,'identity':s.identity,'before':before,'fingerprint':hashlib.sha256(json.dumps(scope,sort_keys=True).encode()).hexdigest(),'attempted_at':datetime.now(timezone.utc).isoformat()}
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
mark=s.find('wnd[0]/tbar[1]/btn[5]');assert str(mark.Tooltip).startswith('Marquer tout')
s.audit('PHASE5_OPERATION',control_id=str(mark.Id),value='Select only six rows independently verified above');mark.Press()
assert str(g.SelectedRows)=='0-5',str(g.SelectedRows)
button=s.find('wnd[0]/tbar[1]/btn[19]');assert button.Text=='Arrière-plan' and 'Créer livraisons' in button.Tooltip
persist();s.audit('PHASE5_OPERATION',control_id=str(button.Id),value={'operation':'EX25_COLLECTIVE_CREATE','fingerprint':r['fingerprint']});button.Press()
r['status']='SUBMITTED_REQUIRES_INDEPENDENT_READBACK';r['message']=s.find('wnd[0]/sbar').Text;r['message_type']=s.find('wnd[0]/sbar').MessageType;persist()
print(json.dumps({'status':r['status'],'message':r['message'],'message_type':r['message_type']},ensure_ascii=True))
