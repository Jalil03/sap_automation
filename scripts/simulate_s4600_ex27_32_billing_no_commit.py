"""One proven non-persisting billing TESTRUN per independent branch; never COMMIT."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client
from dotenv import load_dotenv
from scripts.testrun_s4600_ex7_bapi_billing import get_item,set_parameter,append_row,read_rows
from scripts.audit_s4600_ex30_mto_candidates_readonly import bounded_read
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

def require_simulation_only(function):
    if str(get_item(function.Exports,'TESTRUN').Value)!='X' or str(get_item(function.Exports,'POSTING').Value or '')!='':
        raise RuntimeError('Refusing invocation without TESTRUN=X and empty POSTING')

def main():
    out=ROOT/'runtime/sap_reads/s4600_ex27_32_billing_simulation_2026-10-23.json'
    assert not out.exists(),'Existing attempt: reconcile only, never automatically repeat'
    load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
    client=UrllibSapTransport(cfg);pythoncom.CoInitialize()
    r={'captured_at':datetime.now(timezone.utc).isoformat(),'mode':'PROVEN_BAPI_TESTRUN_NO_COMMIT','authorization_source':'User requested feasibility only for remaining exercises, no persistent changes','branches':{},'persistent_write_authorized':False,'commit_called':False}
    def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    def lookup(delivery):return bounded_read(client,'API_BILLING_DOCUMENT_SRV','A_BillingDocumentItem',{'$filter':f"ReferenceSDDocument eq '{delivery}'",'$top':'21'})
    def items(delivery):return bounded_read(client,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"DeliveryDocument eq '{delivery}'",'$top':'21'})
    for ex,deliveries in [('27',['80000088','80000089','80000090']),('32',['80000091'])]:
        b={'status':'PREFLIGHT','deliveries':deliveries,'before':{},'input':[],'testrun':'X','posting':'','commit_called':False};r['branches'][ex]=b
        for delivery in deliveries:
            before=lookup(delivery);assert before['http_status']==200 and before['count']==0 and not before['has_next_page'];b['before'][delivery]=before
            source=items(delivery);assert source['http_status']==200 and source['count']>0 and not source['has_next_page']
            b['input'].extend({'REF_DOC':delivery.zfill(10),'REF_ITEM':x['DeliveryDocumentItem'],'REF_DOC_CA':'J'} for x in source['rows'])
        f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
        c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H';c.Client=cfg.client;c.User=cfg.username;c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
        try:
            assert c.Logon(0,True)
            b['identity']={'system':str(c.SystemID),'client':str(c.Client),'user':str(c.User).upper()};assert b['identity']=={'system':'A4H','client':'600','user':'ABDELJ'}
            function=f.Add('BAPI_BILLINGDOC_CREATEMULTIPLE')
            names={str(x.Name) for x in list(function.Exports)};assert {'TESTRUN','POSTING'}<=names
            set_parameter(function,'TESTRUN','X');set_parameter(function,'POSTING','')
            require_simulation_only(function)
            table=get_item(function.Tables,'BILLINGDATAIN');cols={str(table.ColumnName(i)) for i in range(1,int(table.ColumnCount)+1)};assert {'REF_DOC','REF_ITEM','REF_DOC_CA'}<=cols
            for row in b['input']:append_row(table,row)
            b['status']='TEST_ATTEMPT_RECORDED';persist()
            b['call_ok']=bool(function.Call)
            b['return']=read_rows(get_item(function.Tables,'RETURN'),['TYPE','ID','NUMBER','MESSAGE'])
            b['errors']=read_rows(get_item(function.Tables,'ERRORS'),['REF_DOC','REF_DOC_ITEM','TYPE','ID','NUMBER','MESSAGE'])
            b['success']=read_rows(get_item(function.Tables,'SUCCESS'),['REF_DOC','REF_DOC_ITEM','BILL_DOC','BILL_DOC_ITEM','NET_VALUE','TAX_VALUE','CURRENCY'])
            persist()
        finally:
            try:c.Logoff()
            except Exception:pass
        b['after']={delivery:lookup(delivery) for delivery in deliveries}
        unchanged=all(x['http_status']==200 and x['count']==0 and not x['has_next_page'] for x in b['after'].values())
        errors=[x for x in b.get('return',[])+b.get('errors',[]) if x['TYPE'] in ('E','A','X')]
        b['status']='TEST_REJECTED_NO_DOCUMENT_CREATED' if unchanged and errors else 'TEST_ACCEPTED_NO_DOCUMENT_CREATED' if unchanged and b.get('call_ok') else 'UNKNOWN_REQUIRES_RECONCILIATION'
        persist()
        assert unchanged,'Stop: independent readback differs; no automatic retry'
    print(json.dumps({ex:{k:b.get(k) for k in ('status','return','errors','success')} for ex,b in r['branches'].items()},ensure_ascii=True,indent=2))
if __name__=='__main__':main()
