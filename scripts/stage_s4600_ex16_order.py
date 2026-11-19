"""Exercise16 draft navigation using observed controls, no save."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.navigation import set_text
from src.sap_gui_bridge.inspection import _visible_records
s=SapGuiConnection(mode=SafetyMode.PREPARE).attach();assert s.identity['transaction']=='VA01'
action=sys.argv[1]
if action=='header':
    assert int(s.raw.Children.Count)==1
    set_text(s,'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR','1000000112')
    set_text(s,'wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD','00-Proposition')
    s.audit('NAVIGATE',value='Validate exercise16 header only');s.find('wnd[0]').sendVKey(0)
elif action!='inspect':raise ValueError(action)
r={'identity':s.identity,'windows':[],'save_attempted':False}
for i in range(int(s.raw.Children.Count)):
    w=s.raw.Children(i);controls,_=_visible_records(w,2000)
    r['windows'].append({'title':w.Text,'controls':[x for x in controls if x['type'] in ('GuiTextField','GuiCTextField','GuiButton','GuiStatusbar','GuiRadioButton','GuiCheckBox','GuiMenu') and (x.get('text') or x.get('tooltip'))]})
(ROOT/f'runtime/sap_reads/s4600_ex16_order_{action}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({**r,'windows':[{**w,'controls':[x for x in w['controls'] if x['type']!='GuiMenu' or any(k in str(x.get('text')).lower() for k in ('propos','poste'))]} for w in r['windows']]},ensure_ascii=True))
