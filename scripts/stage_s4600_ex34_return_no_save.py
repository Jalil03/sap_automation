"""Inspect the authorized RE/FR10 candidate in memory only; no Save route."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.navigation import set_text
from src.sap_gui_bridge.inspection import _visible_records
s=SapGuiConnection(mode=SafetyMode.PREPARE).attach();assert s.identity['transaction']=='VA01'
action=sys.argv[1]
if action=='initial':
    assert str(s.raw.Info.ScreenNumber)=='101' and int(s.raw.Children.Count)==1
    for field,value in {'AUART':'RE','VKORG':'FR10','VTWEG':'10','SPART':'1W'}.items():set_text(s,'wnd[0]/usr/ctxtVBAK-'+field,value)
    s.audit('NAVIGATE',value='Open RE/FR10/10/1W draft only');s.find('wnd[0]').sendVKey(0)
elif action=='header_items':
    assert str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
    assert 'Retour' in s.find('wnd[0]').Text
    table='wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG'
    values={'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR':'1000000112',table+'/ctxtRV45A-MABNR[1,0]':'10000284',table+'/txtRV45A-KWMENG[3,0]':'3'}
    for key,value in values.items():set_text(s,key,value)
    s.audit('NAVIGATE',value='Validate 3 units of10000284 for1000000112 in unsaved return draft');s.find('wnd[0]').sendVKey(0)
elif action=='reason':
    assert int(s.raw.Children.Count)==1 and str(s.raw.Info.ScreenNumber)=='4001'
    key='wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/cmbVBAK-AUGRU'
    control=s.find(key)
    matches=[str(control.Entries(i).Key) for i in range(int(control.Entries.Count)) if str(control.Entries(i).Value)=='Ecart quantité']
    assert matches==['103']
    s.audit('SET_TEXT',control_id=key,value={'key':matches[0],'label':'Ecart quantité','scope':'UNSAVED_RETURN_ONLY'})
    control.Key=matches[0]
    s.audit('NAVIGATE',value='Validate Book reason in return draft only');s.find('wnd[0]').sendVKey(0)
elif action!='inspect':raise ValueError(action)
r={'identity':s.identity,'screen':str(s.raw.Info.ScreenNumber),'save_attempted':False,'sap_write_performed':False,'windows':[]}
for i in range(int(s.raw.Children.Count)):
    w=s.raw.Children(i);controls,_=_visible_records(w,2000)
    r['windows'].append({'title':str(w.Text),'controls':[x for x in controls if x['type'] in ('GuiTextField','GuiCTextField','GuiComboBox','GuiButton','GuiTab','GuiCheckBox','GuiStatusbar') and (x.get('text') or x.get('tooltip') or any(k in x['id'] for k in ('MABNR','KWMENG','WERKS','AUGRU')))]})
out=ROOT/f'runtime/sap_reads/s4600_ex34_draft_{action}_2026-10-23.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({**r,'windows':[{**w,'controls':[x for x in w['controls'] if x.get('text') and x['type'] not in ('GuiButton','GuiTab','GuiCheckBox')]} for w in r['windows']]},ensure_ascii=True))
