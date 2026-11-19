"""Read incompletion metadata/settings by RFC; never invoke a write function."""
import json,os,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
import pythoncom
import win32com.client
from scripts.readback_s4600_ex31_pr00_rfc import get_item,set_parameter,table_get,rfc_read_table

load_dotenv(ROOT/'.env')
assert os.environ['SAP_CLIENT']=='600' and os.environ['SAP_USERNAME'].upper()=='ABDELJ'
pythoncom.CoInitialize()
functions=win32com.client.Dispatch('SAP.Functions.Unicode')
c=functions.Connection
c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H'
c.Client='600';c.User='ABDELJ';c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
result={'mode':'RFC_READ_ONLY_INCOMPLETION_DIAGNOSIS','captured_at_utc':datetime.now(timezone.utc).isoformat(),'metadata':{},'reads':{},'write_called':False}
try:
    c.Logon(0,True)
    identity={'system':str(c.SystemID).upper(),'client':str(c.Client),'user':str(c.User).upper()}
    assert bool(c.IsConnected) and identity=={'system':'A4H','client':'600','user':'ABDELJ'}
    result['environment']=identity
    mode=sys.argv[1] if len(sys.argv)>1 else 'metadata'
    if mode=='fields':
        result['reads']['missing_field_settings']=rfc_read_table(functions,'TVUVF',
            ['MANDT','FEHGR','TBNAM','FDNAM','STATG','FCODE','MSGKZ'],
            ["FDNAM = 'BSTKD' OR FDNAM = 'NTGEW'"])
    elif mode=='header_assignment':
        result['reads']['header_assignment']=rfc_read_table(functions,'TVAK',['AUART','FEHGR'],["AUART = 'TA'"])
    elif mode=='item_assignment':
        result['reads']['item_assignment']=rfc_read_table(functions,'TVAP',['PSTYV','FEHGR'],["PSTYV = 'TAN'"])
    elif mode=='status_groups':
        result['reads']['status_groups']=rfc_read_table(functions,'TVUVS',
            ['MANDT','STATG','UVALL','UVVLK','UVFAK','UVPRS','UVWAK','UVPIK','UVPAK','UVGEK'],
            ["STATG = '00' OR STATG = '01' OR STATG = '04'"])
    for name in (('TVUVF','TVUVS') if mode=='metadata' else ('TVUVS',) if mode=='metadata_status' else ()):
        f=functions.Add('RFC_READ_TABLE')
        set_parameter(f,'QUERY_TABLE',name);set_parameter(f,'NO_DATA','X')
        ok=bool(f.Call)
        if not ok:
            details={}
            for key in ('Exception','ExceptionText'):
                try:
                    value=getattr(f,key);details[key]=str(value() if callable(value) else value)
                except Exception:pass
            result['metadata'][name]={'error':details}
            continue
        fields=get_item(f.Tables,'FIELDS')
        result['metadata'][name]=[{'name':table_get(fields,i,'FIELDNAME'),'type':table_get(fields,i,'TYPE'),'length':table_get(fields,i,'LENGTH')} for i in range(1,int(fields.RowCount)+1)]
    result['status']='METADATA_READ'
finally:
    try:c.Logoff()
    except Exception:pass
    suffix=sys.argv[1] if len(sys.argv)>1 else 'metadata'
    out=ROOT/('runtime/sap_reads/s4600_ex17_incompletion_'+suffix+'_2026-10-22.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
