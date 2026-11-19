"""Evidence-driven Exercise 17 draft preparation and inspection; no Save action."""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.inspection import _visible_records, _table_record
from src.sap_gui_bridge.navigation import open_transaction, set_text
from scripts.stage_s4600_ex19_va01 import INITIAL, TABLE, BODY

s=SapGuiConnection(mode=SafetyMode.PREPARE).attach()
action=sys.argv[1] if len(sys.argv)>1 else 'inspect'
prefix=str(s.raw.Id)
def mapped(key):return key.replace('/app/con[0]/ses[0]',prefix,1)
if action=='open':
    pre=json.loads((ROOT/'runtime/sap_reads/s4600_ex17_preflight_2026-10-22.json').read_text(encoding='utf-8'))
    assert pre['checks']['existing_orders']['http_status']==200
    assert pre['checks']['existing_orders']['count']==0, 'Existing blank-reference orders require reconciliation'
    assert all(pre['checks'][k]['count']==1 for k in ('customer','product'))
    open_transaction(s,'VA01')
    assert str(s.raw.Info.ScreenNumber)=='101'
    for key,value in INITIAL.items():set_text(s,mapped(key),value)
    s.audit('NAVIGATE',value='Accept evidenced CS/FR10/10/1W initial values')
    s.find('wnd[0]').sendVKey(0)
elif action=='open_change':
    saved=json.loads((ROOT/'runtime/sap_reads/s4600_ex17_initial_readback.json').read_text(encoding='utf-8'))
    assert saved['status']=='VERIFIED' and saved['order']=='158'
    open_transaction(s,'VA02')
elif action=='load_change':
    assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='102'
    set_text(s,'wnd[0]/usr/ctxtVBAK-VBELN','158')
    s.audit('NAVIGATE',value='Open existing Exercise 17 order 158 for its approved correction')
    s.find('wnd[0]').sendVKey(0)
elif action=='stage':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001'
    assert int(s.raw.Children.Count)==1
    values={
        'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR':'1000000112',
        'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD':'',
        mapped(TABLE)+'/ctxtRV45A-MABNR[1,0]':'10000283',
        mapped(TABLE)+'/txtRV45A-KWMENG[3,0]':'10'}
    for key,value in values.items():set_text(s,key,value)
elif action=='validate':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001'
    assert int(s.raw.Children.Count)==1
    s.audit('NAVIGATE',value='Validate Exercise 17 draft, no Save')
    s.find('wnd[0]').sendVKey(0)
elif action=='continue_missing_reference':
    assert s.identity['transaction'] in {'VA01','VA02'} and int(s.raw.Children.Count)==1
    status=s.find('wnd[0]/sbar')
    assert str(status.Text)=='Entrez Référence client' and str(status.MessageType)=='W'
    s.audit('NAVIGATE',value='Acknowledge missing customer reference warning required by exercise 17')
    s.find('wnd[0]').sendVKey(0)
elif action=='continue_quotes':
    assert s.find('wnd[1]').Text=='Offres en cours pour le poste'
    assert s.find('wnd[1]/usr/txtSPOP-DIAGNOSE2').Text=='10000283'
    button=s.find('wnd[1]/usr/btnSPOP-VAROPTION1')
    assert button.Text=='Suite'
    s.audit('PRESS_SAFE_BUTTON',control_id=str(button.Id),value='Continue independent order without quotation reference')
    button.Press()
elif action=='open_item_shipping':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
    item=s.find(mapped(TABLE)+'/txtVBAP-POSNR[0,0]')
    assert str(item.Text).strip()=='10'
    assert s.find(mapped(TABLE)+'/ctxtRV45A-MABNR[1,0]').Text=='10000283'
    s.audit('NAVIGATE',control_id=str(item.Id),value='Open Exercise 17 item 10 shipping data')
    item.SetFocus()
    s.find('wnd[0]').sendVKey(2)
    tab=s.find('wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03')
    assert tab.Text=='Expédition'
    tab.Select()
elif action=='clear_weight':
    assert s.identity['transaction']=='VA01' and str(s.raw.Info.ScreenNumber)=='4003' and int(s.raw.Children.Count)==1
    assert s.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4013/ctxtRV45A-MABNR').Text=='10000283'
    key='wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03/ssubSUBSCREEN_BODY:SAPMV45A:4452/txtVBAP-NTGEW'
    assert str(s.find(key).Text).strip()=='10'
    set_text(s,key,'')
    s.audit('NAVIGATE',value='Validate intentionally empty item net weight, no Save')
    s.find('wnd[0]').sendVKey(0)
elif action=='incompletion_log':
    assert s.identity['transaction'] in {'VA01','VA02'} and int(s.raw.Children.Count)==1
    controls,_=_visible_records(s.find('wnd[0]'),2000)
    matches=[c for c in controls if c['type']=='GuiMenu' and c['text']=='Protocole des données manquantes']
    assert len(matches)==1
    menu=s.find(matches[0]['id'])
    assert menu.Text=='Protocole des données manquantes'
    s.audit('NAVIGATE',control_id=str(menu.Id),value='Read incompletion log before saving the Exercise 17 draft')
    menu.Select()
elif action=='complete_reference':
    assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='500'
    grid=s.find('wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell')
    assert grid.RowCount==2 and grid.GetCellValue(0,'FELD')=='Référence client'
    button=s.find('wnd[0]/tbar[1]/btn[2]');assert button.Text=='Compléter données'
    s.audit('NAVIGATE',control_id=str(grid.Id),value='Complete missing customer reference through incompletion log')
    grid.SetCurrentCell(0,'FELD')
    button.Press()
elif action=='set_reference_next':
    assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='4002'
    assert s.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4012/ctxtVBAK-VBELN').Text=='158'
    field='wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\11/ssubSUBSCREEN_BODY:SAPMV45A:4351/txtVBKD-BSTKD'
    assert str(s.find(field).Text).strip()==''
    set_text(s,field,'3-900')
    button=s.find('wnd[0]/tbar[1]/btn[5]');assert str(button.Tooltip).startswith('Traiter données suivantes')
    s.audit('NAVIGATE',control_id=str(button.Id),value='Validate Book reference 3-900 and continue incompletion correction')
    button.Press()
elif action=='complete_weight':
    assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='500'
    grid=s.find('wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell')
    assert grid.RowCount==1 and grid.GetCellValue(0,'FELD')=='Poids net'
    button=s.find('wnd[0]/tbar[1]/btn[2]');assert button.Text=='Compléter données'
    s.audit('NAVIGATE',control_id=str(grid.Id),value='Open remaining missing net weight for item 10')
    grid.SetCurrentCell(0,'FELD');button.Press()
elif action=='set_weight_next':
    assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='4003'
    assert s.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4013/ctxtRV45A-MABNR').Text=='10000283'
    field='wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03/ssubSUBSCREEN_BODY:SAPMV45A:4452/txtVBAP-NTGEW'
    assert str(s.find(field).Text).strip() in {'','0','0,000'}
    set_text(s,field,'20')
    button=s.find('wnd[0]/tbar[1]/btn[5]');assert str(button.Tooltip).startswith('Traiter données suivantes')
    s.audit('NAVIGATE',control_id=str(button.Id),value='Validate Book net weight 20 KG and continue')
    button.Press()
elif action=='continue_weight_warning':
    assert s.identity['transaction']=='VA02' and int(s.raw.Children.Count)==1
    status=s.find('wnd[0]/sbar')
    assert status.MessageType=='W' and status.Text=='Le poids brut doit être plus élevé que le poids net'
    field='wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03/ssubSUBSCREEN_BODY:SAPMV45A:4452/txtVBAP-NTGEW'
    assert str(s.find(field).Text).strip()=='20'
    s.audit('NAVIGATE',value='Acknowledge net/gross weight warning while preserving exact Book net weight 20 KG')
    s.find('wnd[0]').sendVKey(0)
elif action!='inspect':raise ValueError(action)
result={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'identity':s.identity,
        'program':str(s.raw.Info.Program),'screen_number':str(s.raw.Info.ScreenNumber),'windows':[],'save_attempted':False}
result['status_bar']={'text':str(s.find('wnd[0]/sbar').Text),'type':str(s.find('wnd[0]/sbar').MessageType)}
for idx in range(int(s.raw.Children.Count)):
    wnd=s.raw.Children(idx)
    controls,truncated=_visible_records(wnd,2000)
    # Ignore the menu bar; only form controls, tabs, labels and buttons are relevant.
    controls=[c for c in controls if c['type'] in {'GuiTextField','GuiCTextField','GuiLabel','GuiComboBox','GuiTab','GuiButton','GuiShell','GuiTableControl','GuiStatusbar'} or c['type']=='GuiMenu' and any(w in str(c.get('text') or '').lower() for w in ('incompl','protocole'))]
    tables=[_table_record(s,c) for c in controls if c.get('subtype')=='GridView' or c['type']=='GuiTableControl']
    result['windows'].append({'id':str(wnd.Id),'title':str(wnd.Text),'truncated':truncated,'controls':controls,'tables':tables})
out=ROOT/'runtime/sap_reads/s4600_ex17_gui_latest.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out.with_name('s4600_ex17_gui_'+action+'.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for wnd in result['windows']:
    wnd['controls']=[{k:c.get(k) for k in ('id','text','tooltip','changeable')} for c in wnd['controls'] if c['type'] not in {'GuiLabel'} and (c.get('text') and str(c['text']).strip() or c['type'] in {'GuiButton','GuiTableControl','GuiShell'})]
print(json.dumps(result,ensure_ascii=False,indent=2))
