"""Discover field contracts, then inspect bank roles and invoice assignment. No writes."""
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pythoncom
import win32com.client
from dotenv import load_dotenv
from scripts.audit_s4600_ex8_fr10_cash_account_readonly import get_item, set_parameter, table_get, rfc_read_table


@contextmanager
def connection():
    functions = win32com.client.Dispatch('SAP.Functions.Unicode')
    c = functions.Connection
    c.ApplicationServer = os.environ['SAP_APPLICATION_SERVER']
    c.SystemNumber = '23'
    c.SystemID = 'A4H'
    c.Client = os.environ['SAP_CLIENT']
    c.User = os.environ['SAP_USERNAME']
    c.Password = os.environ['SAP_PASSWORD']
    c.Language = 'FR'
    try:
        assert c.Logon(0, True) and c.IsConnected
        assert (str(c.SystemID).upper(), str(c.Client), str(c.User).upper()) == ('A4H', '600', 'ABDELJ')
        yield functions
    finally:
        if c.IsConnected:
            c.Logoff()


def main():
    load_dotenv(ROOT / '.env')
    assert os.environ['SAP_CLIENT'] == '600' and os.environ['SAP_USERNAME'].upper() == 'ABDELJ'
    result = {'captured_at_utc': datetime.now(timezone.utc).isoformat(),
              'identity': {'system': 'A4H', 'client': '600', 'user': 'ABDELJ'},
              'sap_write_performed': False, 'metadata': {}, 'reads': {}}
    pythoncom.CoInitialize()
    try:
        for table in ['T001', 'SKAT', 'SKB1', 'BSEG']:
            with connection() as functions:
                f = functions.Add('RFC_READ_TABLE')
                set_parameter(f, 'QUERY_TABLE', table)
                set_parameter(f, 'NO_DATA', 'X')
                assert bool(f.Call), 'Metadata unavailable: ' + table
                fields = get_item(f.Tables, 'FIELDS')
                result['metadata'][table] = [table_get(fields, i, 'FIELDNAME').strip()
                                             for i in range(1, int(fields.RowCount) + 1)]

        def read(name, table, fields, options):
            assert set(fields) <= set(result['metadata'][table]), 'Unverified fields'
            with connection() as functions:
                try:
                    value = rfc_read_table(functions, table, fields, options, rowcount=100)
                except RuntimeError as error:
                    function = functions.Add('RFC_READ_TABLE')
                    details = {}
                    for key in ['Exception', 'ExceptionText']:
                        try:
                            item = getattr(function, key)
                            details[key] = str(item() if callable(item) else item)
                        except Exception:
                            pass
                    value = {'classification': 'UNKNOWN', 'error': str(error), 'details': details, 'rows': []}
            result['reads'][name] = value
            return value['rows']

        company = read('company_chart', 'T001', ['BUKRS', 'KTOPL', 'WAERS'], ["BUKRS = 'FR10'"])
        assert len(company) == 1
        chart = company[0]['KTOPL']
        assert chart.isalnum()
        fields = ['BUKRS', 'SAKNR', 'MITKZ', 'XOPVW', 'WAERS', 'XINTB']
        fields += [x for x in ['HBKID', 'HKTID', 'XSPEB', 'XSPEA', 'XLOEB'] if x in result['metadata']['SKB1']]
        for account in ['0052110100', '0052110101']:
            read('account_names_' + account, 'SKAT', ['SPRAS', 'KTOPL', 'SAKNR', 'TXT20', 'TXT50'],
                 [f"KTOPL = '{chart}' AND SAKNR = '{account}'"])
            read('company_settings_' + account, 'SKB1', fields,
                 [f"BUKRS = 'FR10' AND SAKNR = '{account}'"])
        read('invoice_customer_assignment', 'BSEG',
             ['BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'KUNNR', 'WRBTR', 'ZUONR', 'SGTXT', 'AUGBL', 'AUGDT'],
             ["BUKRS = 'FR10' AND BELNR = '9300000009'", "AND GJAHR = '2026' AND KUNNR = '1000000112'"])
        result['status'] = ('PARTIAL_READ_NO_PAYMENT_TEST' if any(
            x.get('classification') == 'UNKNOWN' for x in result['reads'].values()) else 'READ_COMPLETE_NO_PAYMENT_TEST')
    finally:
        pythoncom.CoUninitialize()
        out = ROOT / 'runtime/sap_reads/s4600_bank_roles_invoice_assignment_2026-10-23.json'
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'output': str(out), 'status': result.get('status', 'INCOMPLETE'), 'reads': result['reads']}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
