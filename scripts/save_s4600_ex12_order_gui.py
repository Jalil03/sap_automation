"""Save the draft resolved solely from customer material K-MS-00, once."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
out=ROOT/'runtime/sap_writes/s4600_ex12_order_2026-10-22.json';assert not out.exists()
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
c=UrllibSapTransport(cfg)
query={'$filter':"SalesOrganization eq 'FR10' and SoldToParty eq '1000000112' and PurchaseOrderByCustomer eq '5-1900'",'$top':'2'}
before=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',query);assert before['http_status']==200 and before['count']==0
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach();assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
table='wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV45A:4410/subSUBSCREEN_TC:SAPMV45A:4901/tblSAPMV45ATCTRL_U_BEST_AUFTRAG'
values={table+'/ctxtVBAP-KDMAT[1,0]':'K-MS-00',table+'/ctxtRV45A-MABNR[5,0]':'10000282',table+'/txtRV45A-KWMENG[3,0]':'10',
        table+'/txtVBAP-ARKTX[6,0]':'Phare Premium',table+'/ctxtVBAP-KDMAT[1,1]':'',
        'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD':'5-1900',
        'wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV45A:4410/ctxtRV45A-KETDAT':'29.10.2026'}
for key,value in values.items():assert str(s.find(key).Text).strip()==value,key
scope={'system':'A4H','client':'600','user':'ABDELJ','type':'CS','sales_area':'FR10/10/1W','sold_to':'1000000112',
       'reference':'5-1900','requested_delivery_date':'2026-10-29','material_by_customer':'K-MS-00','resolved_material':'10000282',
       'quantity':'10','description':'Phare Premium','net_amount':'1500.00','currency':'EUR'}
digest=hashlib.sha256(json.dumps(scope,sort_keys=True,separators=(',',':')).encode()).hexdigest()
result={'status':'SAVE_ATTEMPT_RECORDED','scope':scope,'sha256':digest,'before':before,'save_attempted':True,
        'approval_source':'User: on attque les exercices qu\u0027on a pas encore fit; Book exercise 12',
        'attempted_at_utc':datetime.now(timezone.utc).isoformat()}
def save():out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save()
button=s.find('wnd[0]/tbar[0]/btn[11]');assert button.Text=='Sauvegarder'
s.audit('PHASE5_OPERATION',control_id=str(button.Id),value={'operation':'SAVE_EX12_CUSTOMER_MATERIAL_ORDER','sha256':digest});button.Press()
result['status_bar']={'text':str(s.find('wnd[0]/sbar').Text),'type':str(s.find('wnd[0]/sbar').MessageType)};save()
after=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',query);result['after']=after
assert after['http_status']==200 and after['count']==1, 'Reconcile, do not repeat save'
order=after['rows'][0]['SalesOrder'];items=get(c,'API_SALES_ORDER_SRV','A_SalesOrderItem',{'$filter':f"SalesOrder eq '{order}'"})
result.update(order=order,items=items)
ok=items['http_status']==200 and items['count']==1
if ok:
    item=items['rows'][0]
    ok=item['Material']=='10000282' and Decimal(item['RequestedQuantity'])==10 and item['SalesOrderItemText']=='Phare Premium' and item['MaterialByCustomer']=='K-MS-00'
result['status']='VERIFIED' if ok else 'READBACK_MISMATCH';save()
print(json.dumps({'status':result['status'],'order':order,'status_bar':result['status_bar']},ensure_ascii=False,indent=2))
