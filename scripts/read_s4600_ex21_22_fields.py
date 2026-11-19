"""Read live DDIC field metadata, then exercise-specific schedule/partial data."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client
from dotenv import load_dotenv
from scripts.readback_s4600_ex31_pr00_rfc import get_item,set_parameter,table_get,rfc_read_table
load_dotenv(ROOT/'.env');pythoncom.CoInitialize()
mode=sys.argv[1];assert mode in ('metadata','readback')
r={'mode':'RFC_READ_ONLY','tables':{}}
for name in ('VBAP','VBEP'):
    f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
    c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H';c.Client=os.environ['SAP_CLIENT'];c.User=os.environ['SAP_USERNAME'];c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
    try:
        assert c.Logon(0,True)
        assert (str(c.SystemID),str(c.Client),str(c.User).upper())==('A4H','600','ABDELJ')
        if mode=='metadata':
            b=f.Add('RFC_READ_TABLE');set_parameter(b,'QUERY_TABLE',name);set_parameter(b,'NO_DATA','X');assert bool(b.Call)
            t=get_item(b.Tables,'FIELDS');r['tables'][name]=[{k:table_get(t,i,k) for k in ('FIELDNAME','TYPE','LENGTH','FIELDTEXT')} for i in range(1,int(t.RowCount)+1)]
        else:
            md=json.loads((ROOT/'runtime/sap_reads/s4600_ex21_22_fields_metadata.json').read_text())['tables'][name]
            fields={'VBAP':['VBELN','POSNR','MATNR','KZTLF'],'VBEP':['VBELN','POSNR','ETENR','EDATU','MBDAT','WMENG','BMENG']}[name]
            assert set(fields)<={x['FIELDNAME'] for x in md}
            order='162' if name=='VBAP' else '161'
            r['tables'][name]=rfc_read_table(f,name,fields,["VBELN = '"+order.zfill(10)+"'"])
    finally:c.Logoff()
(ROOT/f'runtime/sap_reads/s4600_ex21_22_fields_{mode}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r if mode=='readback' else {'mode':mode,'fields':{k:[x for x in v if x['FIELDNAME'] in ('KZTLF','MBDAT','EDATU','WMENG','BMENG')] for k,v in r['tables'].items()}},ensure_ascii=True))
