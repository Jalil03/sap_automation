"""Exact owned-order due-list selection only; no delivery creation."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.navigation import open_transaction,set_text
from src.sap_gui_bridge.inspection import inspect_screen
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
r={'mode':'READ_ONLY_SELECTION','delivery_created':False,'sources':{}}
refs={'156':'6-100','157':'6-400','158':'3-900','159':'5-1900','160':'00-Proposition','161':'7-600','162':'7-700'}
for order,ref in refs.items():
    a=get(c,'API_SALES_ORDER_SRV','A_SalesOrder',{'$filter':f"SalesOrder eq '{order}'"});assert a['http_status']==200 and a['count']==1
    h=a['rows'][0];assert h['PurchaseOrderByCustomer']==ref and h['SalesOrganization']=='FR10' and h['CreatedByUser']=='ABDELJ'
    r['sources'][order]={'reference':ref,'sold_to':h['SoldToParty']}
s=SapGuiConnection(mode=SafetyMode.PREPARE).attach();open_transaction(s,'VL10A')
tab=s.find('wnd[0]/usr/tabsTABSTRIP_ORDER_CRITERIA/tabpS0S_TAB2');assert tab.Text=='Commandes clients';s.audit('NAVIGATE',value='Restrict collective run to verified owned order interval156-162');tab.Select()
field='wnd[0]/usr/tabsTABSTRIP_ORDER_CRITERIA/tabpS0S_TAB2/ssub%_SUBSCREEN_ORDER_CRITERIA:RVV50R10C:1020/ctxtST_VBELN-LOW'
values={'wnd[0]/usr/ctxtST_VSTEL-LOW':'FR10','wnd[0]/usr/ctxtST_VSTEL-HIGH':'','wnd[0]/usr/ctxtST_LEDAT-LOW':'19.10.2026','wnd[0]/usr/ctxtST_LEDAT-HIGH':'01.11.2026',field:'156',field.replace('-LOW','-HIGH'):'162'}
for key,value in values.items():set_text(s,key,value)
for key,value in values.items():assert s.find(key).Text.strip()==value
b=s.find('wnd[0]/tbar[1]/btn[8]');assert b.Text=='Exécuter';s.audit('PRESS_SAFE_BUTTON',control_id=str(b.Id),value='Display exact due list only, no creation');b.Press()
r['snapshot']=inspect_screen(s)
(ROOT/'runtime/sap_reads/s4600_ex25_collective_due_selection.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'sources':r['sources'],'status':r['snapshot']['status_bar'],'tables':r['snapshot']['tables'],'buttons':[x for x in r['snapshot']['buttons'] if x['type']=='GuiButton']},ensure_ascii=True))
