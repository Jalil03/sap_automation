"""Inspect or navigate the existing Exercise 19 draft; never persist it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.inspection import inspect_screen, _visible_records
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_gui_bridge.navigation import set_text
from scripts.stage_s4600_ex19_va01 import TABLE, DOCUMENT

def main():
    session = SapGuiConnection(mode=SafetyMode.PREPARE).attach()
    assert session.identity['transaction'] == 'VA01'
    prefix = str(session.raw.Id)
    action = sys.argv[1] if len(sys.argv) > 1 else 'inspect'
    snapshot = inspect_screen(session)
    if action == 'open20':
        assert not snapshot['popups']
        for key, expected in DOCUMENT.items():
            key = key.replace('/app/con[0]/ses[0]', prefix, 1)
            assert str(session.find(key).Text).strip() == expected, key
        item = TABLE.replace('/app/con[0]/ses[0]', prefix, 1) + '/txtVBAP-POSNR[0,1]'
        assert str(session.find(item).Text).strip() == '20'
        session.audit('NAVIGATE', control_id=item, value='Open item 20 details using F2')
        session.find(item).SetFocus()
        session.find('wnd[0]').sendVKey(2)
    elif action == 'partners':
        assert not snapshot['popups'] and snapshot['screen_number'] == '4003'
        controls, _ = _visible_records(session.find('wnd[0]'), 2000)
        tabs = [c for c in controls if c['type'] == 'GuiTab' and c['text'] == 'Partenaires']
        assert len(tabs) == 1
        session.audit('NAVIGATE', control_id=tabs[0]['id'], value='Select Partenaires tab')
        session.find(tabs[0]['id']).Select()
    elif action == 'set_shipto':
        assert not snapshot['popups'] and snapshot['screen_number'] == '4003'
        fields = snapshot['input_fields']
        assert any(c['id'].endswith('/txtVBAP-POSNR') and c['text'] == '20' for c in fields)
        role = [c for c in fields if c['id'].endswith('cmbGVS_TC_DATA-REC-PARVW[0,3]')]
        assert len(role) == 1 and session.find(role[0]['id']).Key == 'WE'
        target = role[0]['id'].rsplit('/',1)[0] + '/ctxtGVS_TC_DATA-REC-PARTNER_EXT[1,3]'
        assert str(session.find(target).Text).strip() == '1000000112'
        set_text(session, target, '1000000113')
        session.audit('NAVIGATE', value='Validate item 20 ship-to change, no persistence')
        session.find('wnd[0]').sendVKey(0)
    elif action in {'confirm_route_info', 'confirm_tax_info'}:
        assert len(snapshot['popups']) == 1
        popup = snapshot['popups'][0]
        texts = ' '.join(str(c.get('text') or '') for c in popup['input_fields'])
        assert popup['window_title'] == 'Information'
        if action == 'confirm_route_info':
            assert 'itinéraire' in texts and '1000000113 pour poste 000020' in texts
        else:
            assert texts.strip() == 'Les taxes ont été redéterminées'
        buttons = [b for b in popup['buttons'] if (b['tooltip'] or '').startswith('Continuer')]
        assert len(buttons) == 1
        session.audit('PRESS_SAFE_BUTTON', control_id=buttons[0]['id'], value='Confirm observed route information for item 20')
        session.find(buttons[0]['id']).Press()
    elif action == 'redetermine':
        assert len(snapshot['popups']) == 1
        popup = snapshot['popups'][0]
        assert popup['window_title'] == 'Adapter poste'
        assert any(c['text'] == "Redéterminer division et point d'expédition du poste ?" for c in popup['input_fields'])
        buttons = [b for b in popup['buttons'] if b['text'] == 'Redéterminer']
        assert len(buttons) == 1
        session.audit('PRESS_SAFE_BUTTON', control_id=buttons[0]['id'], value='Redetermine plant and shipping point per Book exercise 19')
        session.find(buttons[0]['id']).Press()
    elif action == 'first_item':
        assert not snapshot['popups'] and snapshot['screen_number'] == '4003'
        assert any(c['id'].endswith('PARTNER_EXT[1,3]') and c['text'] == '1000000113' for c in snapshot['input_fields'])
        buttons = [b for b in snapshot['buttons'] if b['tooltip'] == 'Premier poste']
        assert len(buttons) == 1
        session.audit('NAVIGATE', control_id=buttons[0]['id'], value='Read item 10 partners')
        session.find(buttons[0]['id']).Press()
    elif action == 'schedules':
        assert not snapshot['popups'] and snapshot['screen_number'] == '4003'
        assert any(c['id'].endswith('/txtVBAP-POSNR') and c['text'] == '10' for c in snapshot['input_fields'])
        controls, _ = _visible_records(session.find('wnd[0]'), 2000)
        tabs = [c for c in controls if c['type'] == 'GuiTab' and c['text'] == 'Échéances']
        assert len(tabs) == 1
        session.audit('NAVIGATE', control_id=tabs[0]['id'], value='Read item 10 schedule lines')
        session.find(tabs[0]['id']).Select()
    elif action == 'shipping_dates':
        assert not snapshot['popups'] and snapshot['screen_number'] == '4003'
        fields = snapshot['input_fields']
        assert any(c['id'].endswith('/txtVBAP-POSNR') and c['text'] == '10' for c in fields)
        rows = [c for c in fields if c['id'].endswith('/txtVBEP-BMENG[4,0]') and str(c['text']).strip() == '5']
        assert len(rows) == 1
        buttons = [b for b in snapshot['buttons'] if b['id'].endswith('/btnP0_EID2') and b['tooltip'] == 'Détail expéd.']
        assert len(buttons) == 1
        session.audit('NAVIGATE', control_id=buttons[0]['id'], value='Read shipping dates for confirmed quantity 5')
        session.find(rows[0]['id']).SetFocus()
        session.find(buttons[0]['id']).Press()
    elif action == 'back':
        assert not snapshot['popups'] and snapshot['screen_number'] in {'4003', '4004'}
        buttons = [b for b in snapshot['buttons'] if b['id'].endswith('/tbar[0]/btn[3]') and (b['tooltip'] or '').startswith('Retour')]
        assert len(buttons) == 1
        session.audit('BACK', control_id=buttons[0]['id'], value='Return within existing draft')
        session.find(buttons[0]['id']).Press()
    elif action != 'inspect':
        raise ValueError('Unsupported action')
    snapshot = inspect_screen(session)
    controls, truncated = _visible_records(session.find('wnd[0]'), 2000)
    result = {'identity': session.identity,
        'screen': {k:snapshot[k] for k in ('program','screen_number','window_title','status_bar','popups')},
        'tabs': [c for c in controls if c['type'] == 'GuiTab'],
        'fields': [c for c in snapshot['input_fields'] if c['text'] and str(c['text']).strip()],
        'buttons': [c for c in snapshot['buttons'] if c['type'] == 'GuiButton'],
        'truncated': truncated, 'save_attempted': False}
    output = ROOT / 'runtime/sap_reads/s4600_ex19_item_details_latest.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    checkpoint = output.with_name('s4600_ex19_' + action + '_' + str(snapshot['screen_number']) + '.json')
    checkpoint.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    if action == 'inspect' or snapshot['popups']:
        result['tabs'] = []
        result['fields'] = [c for c in result['fields'] if 'PARTNER_EXT' in c['id'] or c['id'].endswith('/txtVBAP-POSNR')]
        result['buttons'] = []
    result['tabs'] = [{'id': c['id'], 'text':c['text']} for c in result['tabs']]
    result['fields'] = [{'id':c['id'], 'text':c['text']} for c in result['fields']]
    result['buttons'] = [{'id':c['id'], 'text':c['text'], 'tooltip':c['tooltip']} for c in result['buttons']]
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
