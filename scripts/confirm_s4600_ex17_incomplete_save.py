"""Confirm only the observed, approved incomplete-document save dialog once."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from scripts.readback_s4600_ex17 import readback
out=ROOT/'runtime/sap_writes/s4600_ex17_initial_save_2026-10-22.json'
result=json.loads(out.read_text(encoding='utf-8'))
assert result['save_attempted'] and not result.get('confirmation_attempted')
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
assert s.identity['transaction']=='VA01' and s.find('wnd[1]').Text=='Sauvegarder document incomplet'
assert s.find('wnd[1]/usr/txtSPOP-TEXTLINE1').Text=='Document incomplet'
button=s.find('wnd[1]/usr/btnSPOP-VAROPTION1');assert button.Text=='Sauvegarder'
result['confirmation_attempted']=True
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
s.audit('PHASE5_OPERATION',control_id=str(button.Id),value={'operation':'CONFIRM_EX17_INCOMPLETE_SAVE','sha256':result['sha256']})
button.Press()
result['status_bar']={'text':str(s.find('wnd[0]/sbar').Text),'type':str(s.find('wnd[0]/sbar').MessageType)}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
verified=readback('initial')
result.update(status=verified['status'],order=verified['order'])
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
