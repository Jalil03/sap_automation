"""Prepare Exercise 12 using customer material resolution; never Save."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.inspection import _visible_records,_table_record
from src.sap_gui_bridge.navigation import open_transaction,set_text
from scripts.stage_s4600_ex19_va01 import INITIAL,BODY
s=SapGuiConnection(mode=SafetyMode.PREPARE).attach();action=sys.argv[1]
prefix=str(s.raw.Id)
def mapped(k):return k.replace('/app/con[0]/ses[0]',prefix,1)
if action=='open':
    open_transaction(s,'VA01');assert str(s.raw.Info.ScreenNumber)=='101'
    for key,value in INITIAL.items():set_text(s,mapped(key),value)
    s.audit('NAVIGATE',value='Open Exercise 12 draft CS/FR10/10/1W');s.find('wnd[0]').sendVKey(0)
elif action=='header_buyer':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
    for key,value in {'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR':'1000000112',
         'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD':'5-1900',
         mapped(BODY)+'/ssubHEADER_FRAME:SAPMV45A:4440/ctxtRV45A-KETDAT':'29.10.2026'}.items():set_text(s,key,value)
    tab=s.find('wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\04');assert tab.Text=='Acheteur'
    s.audit('NAVIGATE',control_id=str(tab.Id),value='Use customer material entry as required by Book');tab.Select()
elif action=='confirm_billing_info':
    assert s.find('wnd[1]').Text=='Information'
    texts=' '.join(str(s.find('wnd[1]/usr/txtMESSTXT'+str(i)).Text) for i in (1,2))
    assert 'Modification du délai de facturation' in texts and 'facture redéterminée' in texts
    button=s.find('wnd[1]/tbar[0]/btn[0]')
    s.audit('PRESS_SAFE_BUTTON',control_id=str(button.Id),value='Acknowledge observed billing date information only')
    button.Press()
elif action=='customer_material':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
    table='wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV45A:4410/subSUBSCREEN_TC:SAPMV45A:4901/tblSAPMV45ATCTRL_U_BEST_AUFTRAG'
    assert str(s.find(table+'/ctxtVBAP-KDMAT[1,0]').Text).strip()==''
    set_text(s,table+'/ctxtVBAP-KDMAT[1,0]','K-MS-00')
    set_text(s,table+'/txtRV45A-KWMENG[3,0]','10')
    s.audit('NAVIGATE',value='Resolve material using customer number K-MS-00 only')
    s.find('wnd[0]').sendVKey(0)
elif action!='inspect':raise ValueError(action)
result={'identity':s.identity,'program':str(s.raw.Info.Program),'screen':str(s.raw.Info.ScreenNumber),'windows':[],'save_attempted':False}
for i in range(int(s.raw.Children.Count)):
    wnd=s.raw.Children(i);controls,_=_visible_records(wnd,2000)
    relevant=[c for c in controls if c['type'] in {'GuiTextField','GuiCTextField','GuiTab','GuiButton','GuiStatusbar','GuiLabel'}]
    result['windows'].append({'id':str(wnd.Id),'title':str(wnd.Text),'controls':relevant})
out=ROOT/'runtime/sap_reads/s4600_ex12_order_gui_latest.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for wnd in result['windows']:
    wnd['controls']=[{k:c.get(k) for k in ('id','text','tooltip')} for c in wnd['controls'] if c['type']!='GuiLabel' and (c.get('text') and str(c['text']).strip() or 'KDMAT' in c['id'] or 'KWMENG' in c['id'])]
print(json.dumps(result,ensure_ascii=False,indent=2))
