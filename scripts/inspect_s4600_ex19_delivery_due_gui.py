"""Navigate and inspect delivery due selection; no delivery creation controls."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.inspection import inspect_screen, _visible_records
from src.sap_gui_bridge.navigation import open_transaction
from src.sap_gui_bridge.navigation import set_text

session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
action = sys.argv[1] if len(sys.argv)>1 else 'inspect'
if action == 'open':
    saved = json.loads((ROOT/'runtime/sap_writes/s4600_ex19_gui_save_2026-10-22.json').read_text(encoding='utf-8'))
    assert saved['status'] == 'VERIFIED' and saved['order'] == '157'
    # Official SAP app documentation identifies VL10A as the delivery due list.
    open_transaction(session,'VL10A')
elif action == 'orders_tab':
    assert session.identity['transaction'] == 'VL10A' and str(session.raw.Info.ScreenNumber) == '1000'
    tab = session.find('wnd[0]/usr/tabsTABSTRIP_ORDER_CRITERIA/tabpS0S_TAB2')
    assert tab.Text == 'Commandes clients'
    session.audit('NAVIGATE',control_id=str(tab.Id),value='Narrow due-list selection to order 157')
    tab.Select()
elif action in {'select_today','select_due'}:
    assert session.identity['transaction'] == 'VL10A' and str(session.raw.Info.ScreenNumber) == '1000'
    tab=session.find('wnd[0]/usr/tabsTABSTRIP_ORDER_CRITERIA/tabpS0S_TAB2')
    assert tab.Text == 'Commandes clients'
    session.audit('NAVIGATE',control_id=str(tab.Id),value='Show order filter for exact due-list selection')
    tab.Select()
    date = '22.10.2026' if action == 'select_today' else '27.10.2026'
    order_field='wnd[0]/usr/tabsTABSTRIP_ORDER_CRITERIA/tabpS0S_TAB2/ssub%_SUBSCREEN_ORDER_CRITERIA:RVV50R10C:1020/ctxtST_VBELN-LOW'
    values={'wnd[0]/usr/ctxtST_VSTEL-LOW':'FR10','wnd[0]/usr/ctxtST_VSTEL-HIGH':'',
            'wnd[0]/usr/ctxtST_LEDAT-LOW':'22.10.2026','wnd[0]/usr/ctxtST_LEDAT-HIGH':date,
            order_field:'157',order_field.replace('-LOW','-HIGH'):''}
    for key,value in values.items():
        set_text(session,key,value)
    for key,value in values.items():
        assert str(session.find(key).Text).strip() == value
    button=session.find('wnd[0]/tbar[1]/btn[8]')
    assert button.Text == 'Exécuter'
    session.audit('PRESS_SAFE_BUTTON',control_id=str(button.Id),value={'operation':'SELECT_DUE_LIST_ONLY','order':'157','shipping_point':'FR10','from':'22.10.2026','to':date})
    button.Press()
elif action == 'back':
    assert session.identity['transaction']=='VL10A'
    button=session.find('wnd[0]/tbar[0]/btn[3]')
    assert str(button.Tooltip).startswith('Retour')
    session.audit('BACK',control_id=str(button.Id),value='Return from delivery due list to criteria')
    button.Press()
elif action != 'inspect':
    raise ValueError(action)
snapshot = inspect_screen(session)
controls,_ = _visible_records(session.find('wnd[0]'),2000)
result = {'identity':session.identity,'screen':{k:snapshot[k] for k in ('program','screen_number','window_title','status_bar','popups')},
          'fields':snapshot['input_fields'],'labels':snapshot['labels'],
          'tabs':[c for c in controls if c['type']=='GuiTab'],
          'buttons':[b for b in snapshot['buttons'] if b['type']=='GuiButton'],
          'tables':snapshot['tables'],'delivery_created':False}
out=ROOT/'runtime/sap_reads/s4600_ex19_delivery_due_gui_latest.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
out.with_name('s4600_ex19_delivery_due_'+action+'.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for key in ('fields','labels','tabs','buttons'):
    result[key]=[{k:c.get(k) for k in ('id','text','tooltip')} for c in result[key]]
print(json.dumps(result,ensure_ascii=False,indent=2))
