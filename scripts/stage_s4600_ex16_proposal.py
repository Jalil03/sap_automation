"""Stage evidenced Book exercise 16 proposal fields; no save."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.navigation import set_text
from src.sap_gui_bridge.inspection import _visible_records
s=SapGuiConnection(mode=SafetyMode.PREPARE).attach()
assert s.identity['transaction']=='VA51' and s.find('wnd[0]').Text.startswith('Créer Poste par défaut')
values={'wnd[0]/usr/txtVBAK-KTEXT':'Proposition poste Groupe 00','wnd[0]/usr/ctxtVBAK-GUEBG':'22.10.2026','wnd[0]/usr/ctxtVBAK-GUEEN':'31.12.2026'}
table='wnd[0]/usr/tblSAPMV45ATCTRL_SORTIMENT'
for row,material in enumerate(('10000282','10000283')):
    values[f'{table}/ctxtRV45A-MABNR[1,{row}]']=material
    values[f'{table}/txtVBAP-ZMENG[2,{row}]']='5'
for key,value in values.items():set_text(s,key,value)
s.audit('NAVIGATE',value='Validate Book proposal group00 without save');s.find('wnd[0]').sendVKey(0)
r={'identity':s.identity,'windows':[],'save_attempted':False}
for i in range(int(s.raw.Children.Count)):
    w=s.raw.Children(i);controls,_=_visible_records(w,2000)
    r['windows'].append({'title':w.Text,'controls':[x for x in controls if x['type'] in ('GuiTextField','GuiCTextField','GuiStatusbar','GuiButton') and (x.get('text') or x['type']=='GuiStatusbar')]})
(ROOT/'runtime/sap_reads/s4600_ex16_proposal_staged.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True))
