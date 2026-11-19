"""One approved Exercise 19 GUI save, with exact checks and OData readback."""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from scripts.stage_s4600_ex19_va01 import DOCUMENT, TABLE
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

CANDIDATE = ROOT / 'runtime/sap_reads/s4600_ex19_gui_save_candidate_2026-10-22.json'
OUTPUT = ROOT / 'runtime/sap_writes/s4600_ex19_gui_save_2026-10-22.json'
HASH = '9df8398d68ce9177b1b986a67584e5f53a02e2d7f4c85ca7adc76a574beffae7'
EXPECTED = {'system':'A4H', 'client':'600', 'user':'ABDELJ'}

def record(result):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')

def lookup(client):
    response = get(client, 'API_SALES_ORDER_SRV', 'A_SalesOrder', {
        '$filter': "PurchaseOrderByCustomer eq '6-400'", '$top':'2'})
    assert response['http_status'] == 200, response
    return response

def readback(client, result):
    found = lookup(client)
    result['after_lookup'] = found
    rows = found['rows']
    if len(rows) != 1:
        result['status'] = 'RECONCILIATION_REQUIRED'
        record(result)
        return
    header = rows[0]
    order = header['SalesOrder']
    reads = {}
    for name, entity in [('items','A_SalesOrderItem'), ('partners','A_SalesOrderItemPartner'),
                         ('header_partners','A_SalesOrderHeaderPartner'), ('schedules','A_SalesOrderScheduleLine')]:
        reads[name] = get(client, 'API_SALES_ORDER_SRV', entity, {'$filter':f"SalesOrder eq '{order}'"})
    result['readback'] = reads
    errors = []
    checks = {'SalesOrderType':'CS', 'SalesOrganization':'FR10', 'DistributionChannel':'10',
              'OrganizationDivision':'1W', 'SoldToParty':'1000000112', 'PurchaseOrderByCustomer':'6-400',
              'TransactionCurrency':'EUR'}
    for key, expected in checks.items():
        if header.get(key) != expected:
            errors.append({'field':key,'actual':header.get(key),'expected':expected})
    if Decimal(header.get('TotalNetAmount','-1')) != Decimal('870'):
        errors.append({'field':'TotalNetAmount','actual':header.get('TotalNetAmount')})
    for name, response in reads.items():
        if response['http_status'] != 200:
            errors.append({'read_error':name})
    items = reads['items'].get('rows',[])
    if len(items) != 2:
        errors.append({'item_count':len(items)})
    partners = reads['partners'].get('rows',[])
    head_partners = reads['header_partners'].get('rows',[])
    for number, material, quantity, shipto in [('10','10000282','5','1000000112'),('20','10000284','1','1000000113')]:
        matches = [r for r in items if str(r.get('SalesOrderItem','')).lstrip('0') == number]
        if len(matches) != 1 or matches[0].get('Material') != material or Decimal(matches[0].get('RequestedQuantity','-1')) != Decimal(quantity):
            errors.append({'item_mismatch':number})
        matches = [r for r in partners if str(r.get('SalesOrderItem','')).lstrip('0') == number and r.get('PartnerFunction') in {'RM','WE'}]
        if not matches:
            matches = [r for r in head_partners if r.get('PartnerFunction') in {'RM','WE'}]
        if len(matches) != 1 or matches[0].get('Customer') != shipto:
            errors.append({'shipto_mismatch':number, 'expected':shipto,'actual':matches})
    result.update(order=order, mismatches=errors, status='VERIFIED' if not errors else 'READBACK_MISMATCH')
    record(result)

def main():
    load_dotenv(ROOT / '.env')
    config = SapRuntimeConfig.from_env()
    assert config.client == '600' and config.username.upper() == 'ABDELJ'
    client = UrllibSapTransport(config)
    if len(sys.argv) > 1 and sys.argv[1] == 'readback':
        result = json.loads(OUTPUT.read_text(encoding='utf-8'))
        readback(client, result)
        print(json.dumps({k:result.get(k) for k in ('status','order','mismatches')},ensure_ascii=False))
        return
    assert len(sys.argv) > 1 and sys.argv[1] == 'execute'
    if OUTPUT.exists():
        previous = json.loads(OUTPUT.read_text(encoding='utf-8'))
        assert not previous.get('save_attempted'), 'Attempt already recorded; reconcile only'
    candidate = json.loads(CANDIDATE.read_text(encoding='utf-8'))
    actual_hash = hashlib.sha256(json.dumps(candidate['candidate'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert actual_hash == HASH == candidate['sha256']
    session = SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
    assert {k:session.identity[k] for k in EXPECTED} == EXPECTED
    assert session.identity['transaction'] == 'VA01'
    assert str(session.raw.Info.ScreenNumber) == '4001'
    assert int(session.raw.Children.Count) == 1, 'Unexpected modal'
    prefix = str(session.raw.Id)
    def mapped(key):
        return key.replace('/app/con[0]/ses[0]',prefix,1)
    def check_overview():
        for key, expected in DOCUMENT.items():
            assert str(session.find(mapped(key)).Text).strip() == expected, key
        assert str(session.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBAK-NETWR').Text).strip() == '870,00'
    check_overview()
    partner_evidence = []
    for row, number, expected in [(1,'20','1000000113'),(0,'10','1000000112')]:
        item = mapped(TABLE) + f'/txtVBAP-POSNR[0,{row}]'
        assert str(session.find(item).Text).strip() == number
        session.audit('NAVIGATE',control_id=item,value='Verify approved item partners before save')
        session.find(item).SetFocus()
        session.find('wnd[0]').sendVKey(2)
        assert str(session.raw.Info.ScreenNumber) == '4003'
        tab = 'wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\08'
        assert session.find(tab).Text == 'Partenaires'
        session.find(tab).Select()
        assert str(session.find('wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4013/txtVBAP-POSNR').Text).strip() == number
        table = tab + '/ssubSUBSCREEN_BODY:SAPMV45A:4353/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW'
        assert session.find(table + '/cmbGVS_TC_DATA-REC-PARVW[0,3]').Key == 'WE'
        actual = str(session.find(table + '/ctxtGVS_TC_DATA-REC-PARTNER_EXT[1,3]').Text).strip()
        assert actual == expected
        partner_evidence.append({'item':number,'ship_to':actual})
        session.find('wnd[0]/tbar[0]/btn[3]').Press()
        assert str(session.raw.Info.ScreenNumber) == '4001'
    check_overview()
    before = lookup(client)
    assert before['classification'] == 'NO_ROWS_FOR_EXACT_FILTER' and before['count'] == 0, before
    save_button = session.find('wnd[0]/tbar[0]/btn[11]')
    assert save_button.Text == 'Sauvegarder' and bool(save_button.Changeable)
    result = {'status':'SAVE_ATTEMPT_RECORDED', 'environment':session.identity,
              'approval':{'source':'User chat: oui et je veux qu\u0027on accelere un peu',
                          'sha256':HASH,'scope':candidate['candidate']},
              'before_lookup':before,'partner_evidence':partner_evidence,
              'attempted_at_utc':datetime.now(timezone.utc).isoformat(),'save_attempted':True}
    record(result)
    session.audit('PHASE5_OPERATION', control_id=str(save_button.Id),
                  value={'operation':'SAVE_ONE_EX19_DRAFT','sha256':HASH})
    save_button.Press()
    result['save_returned'] = True
    status = session.find('wnd[0]/sbar')
    result['status_bar'] = {'text':str(status.Text),'message_type':str(status.MessageType)}
    record(result)
    readback(client,result)
    print(json.dumps({k:result.get(k) for k in ('status','order','mismatches','status_bar')},ensure_ascii=False))

if __name__ == '__main__':
    main()
