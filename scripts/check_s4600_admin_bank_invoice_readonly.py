"""Narrow read-only reconciliation of the administrator's FR10 bank update."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pythoncom
import win32com.client
from dotenv import load_dotenv
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from scripts.audit_s4600_ex30_mto_candidates_readonly import bounded_read
from scripts.audit_s4600_ex8_fr10_cash_account_readonly import rfc_read_table

EXPECTED = {'system': 'A4H', 'client': '600', 'user': 'ABDELJ'}


def read_table(table, fields, options):
    # Separate connections prevent COM RFC_READ_TABLE parameter accumulation.
    functions = win32com.client.Dispatch('SAP.Functions.Unicode')
    connection = functions.Connection
    connection.ApplicationServer = os.environ['SAP_APPLICATION_SERVER']
    connection.SystemNumber = os.environ['SAP_SYSTEM_NUMBER']
    connection.SystemID = 'A4H'
    connection.Client = os.environ['SAP_CLIENT']
    connection.User = os.environ['SAP_USERNAME']
    connection.Password = os.environ['SAP_PASSWORD']
    connection.Language = 'FR'
    try:
        assert connection.Logon(0, True)
        identity = {'system': str(connection.SystemID).upper(),
                    'client': str(connection.Client), 'user': str(connection.User).upper()}
        assert identity == EXPECTED and connection.IsConnected
        return {'identity': identity, **rfc_read_table(functions, table, fields, options, rowcount=100)}
    finally:
        if connection.IsConnected:
            connection.Logoff()


def main():
    load_dotenv(ROOT / '.env')
    cfg = SapRuntimeConfig.from_env()
    assert cfg.client == '600' and cfg.username.upper() == 'ABDELJ'
    result = {'captured_at_utc': datetime.now(timezone.utc).isoformat(),
              'mode': 'READ_ONLY', 'sap_write_performed': False, 'checks': {}}
    checks = result['checks']
    transport = UrllibSapTransport(cfg)
    checks['bank_api'] = bounded_read(transport, 'API_BANKACCOUNT_SRV', 'A_BankAccountName', {
        '$filter': "CompanyCode eq 'FR10'",
        '$select': 'BankAccountInternalID,BankAccountCurrency,CompanyCode,BankAccountDescription', '$top': '21'})
    response = transport.request('GET', "sap/opu/odata/sap/API_BILLING_DOCUMENT_SRV/A_BillingDocument('90000090')",
                                 headers={'Accept': 'application/json'})
    header = response.json().get('d', {}) if response.status == 200 else {}
    checks['invoice'] = {'http_status': response.status, 'header': {key: header.get(key) for key in [
        'BillingDocument', 'CompanyCode', 'AccountingDocument', 'FiscalYear', 'SoldToParty',
        'TotalGrossAmount', 'TotalNetAmount', 'TaxAmount', 'TransactionCurrency',
        'InvoiceClearingStatus', 'BillingDocumentIsCancelled', 'AccountingPostingStatus']}}
    pythoncom.CoInitialize()
    try:
        tasks = [
            ('house_bank_accounts', 'T012K', ['BUKRS', 'HBKID', 'HKTID', 'HKONT', 'WAERS'], ["BUKRS = 'FR10'"]),
            ('gl_account', 'SKB1', ['BUKRS', 'SAKNR', 'MITKZ', 'XOPVW', 'WAERS', 'XINTB'],
             ["BUKRS = 'FR10' AND SAKNR = '0052110101'"]),
            ('invoice_accounting_lines', 'BSEG', ['BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'HKONT', 'KUNNR', 'WRBTR', 'AUGBL', 'AUGDT'],
             ["BUKRS = 'FR10' AND BELNR = '9300000009'", "AND GJAHR = '2026'"]),
        ]
        for name, table, fields, options in tasks:
            try:
                checks[name] = read_table(table, fields, options)
            except Exception as error:
                checks[name] = {'classification': 'UNKNOWN', 'error': type(error).__name__ + ': ' + str(error)}
    finally:
        pythoncom.CoUninitialize()
    out = ROOT / 'runtime/sap_reads/s4600_fr10_bank_invoice_check_2026-10-23.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
