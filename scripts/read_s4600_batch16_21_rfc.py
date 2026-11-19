"""Narrow read-only proposal lookup and stock/requirements BAPI metadata."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client
from dotenv import load_dotenv
from scripts.readback_s4600_ex31_pr00_rfc import rfc_read_table
load_dotenv(ROOT/'.env');pythoncom.CoInitialize()
f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H'
c.Client=os.environ['SAP_CLIENT'];c.User=os.environ['SAP_USERNAME'];c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
r={'write_called':False}
try:
    assert c.Logon(0,True)
    r['identity']={'system':str(c.SystemID),'client':str(c.Client),'user':str(c.User).upper()}
    assert r['identity']=={'system':'A4H','client':'600','user':'ABDELJ'}
    r['proposal_lookup']=rfc_read_table(f,'VBAK',['VBELN','AUART','VKORG','VTWEG','SPART','KTEXT','GUEBG','GUEEN'],["KTEXT = 'Proposition poste Groupe 00'","AND VKORG = 'FR10'"])
    b=f.Add('BAPI_MATERIAL_STOCK_REQ_LIST')
    r['bapi_metadata']={key:[str(x.Name) for x in list(getattr(b,key))] for key in ('Exports','Imports','Tables')}
finally:
    c.Logoff()
    (ROOT/'runtime/sap_reads/s4600_batch16_21_rfc_preflight.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
