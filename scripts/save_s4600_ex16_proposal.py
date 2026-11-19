"""One-shot save of the inspected proposal, with fresh RFC lookup/readback."""
import json,os,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client
from dotenv import load_dotenv
from scripts.readback_s4600_ex31_pr00_rfc import rfc_read_table
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
out=ROOT/'runtime/sap_writes/s4600_ex16_proposal.json'
assert not out.exists(),'Existing attempt must be reconciled, not repeated'
load_dotenv(ROOT/'.env');pythoncom.CoInitialize()
f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H';c.Client=os.environ['SAP_CLIENT'];c.User=os.environ['SAP_USERNAME'];c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
r={'status':'PREFLIGHT','approval_source':'Current user: on attque les exercices qu’on a pas encore fit','source':'S4600 exercise16 pages155-160; approved FR10 group00 mapping','scope':{'type':'PV','sales_area':'FR10/10/1W','description':'Proposition poste Groupe 00','valid_from':'20261022','valid_to':'20261231','items':[['10000282','5'],['10000283','5']]}}
r['fingerprint']=hashlib.sha256(json.dumps(r['scope'],sort_keys=True).encode()).hexdigest()
def persist():out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
try:
    assert c.Logon(0,True)
    assert (str(c.SystemID),str(c.Client),str(c.User).upper())==('A4H','600','ABDELJ')
    options=["KTEXT = 'Proposition poste Groupe 00'","AND VKORG = 'FR10'"]
    fields=['VBELN','AUART','VKORG','VTWEG','SPART','KTEXT','GUEBG','GUEEN']
    r['lookup']=rfc_read_table(f,'VBAK',fields,options);assert r['lookup']['row_count']==0
    s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach();assert s.identity['transaction']=='VA51' and int(s.raw.Children.Count)==1
    for name,value in [('txtVBAK-KTEXT',r['scope']['description']),('ctxtVBAK-GUEBG','22.10.2026'),('ctxtVBAK-GUEEN','31.12.2026')]:assert s.find('wnd[0]/usr/'+name).Text==value
    table='wnd[0]/usr/tblSAPMV45ATCTRL_SORTIMENT'
    for row,(material,qty) in enumerate(r['scope']['items']):
        assert s.find(f'{table}/ctxtRV45A-MABNR[1,{row}]').Text==material
        assert s.find(f'{table}/txtVBAP-ZMENG[2,{row}]').Text.strip()==qty
    assert s.find('wnd[0]/sbar').MessageType not in ('E','A')
    b=s.find('wnd[0]/tbar[0]/btn[11]');assert b.Text=='Sauvegarder'
    r['status']='ATTEMPT_RECORDED';r['attempted_at']=datetime.now(timezone.utc).isoformat();persist()
    s.audit('PHASE5_OPERATION',control_id=str(b.Id),value='Save one Book exercise16 proposal; fingerprint '+r['fingerprint']);b.Press()
    r['sap_message']=s.find('wnd[0]/sbar').Text;r['sap_message_type']=s.find('wnd[0]/sbar').MessageType;persist()
    assert r['sap_message_type'] not in ('E','A')
    r['readback']=rfc_read_table(f,'VBAK',fields,options);assert r['readback']['row_count']==1
    h=r['readback']['rows'][0];assert (h['VKORG'],h['VTWEG'],h['SPART'],h['GUEBG'],h['GUEEN'])==('FR10','10','1W','20261022','20261231')
    r['proposal']=h['VBELN']
    r['items']=rfc_read_table(f,'VBAP',['VBELN','POSNR','MATNR','ZMENG','ZIEME'],["VBELN = '"+h['VBELN']+"'"])
    assert len(r['items']['rows'])==2
    assert [(x['MATNR'].lstrip('0'),float(x['ZMENG'])) for x in r['items']['rows']]==[('10000282',5),('10000283',5)]
    r['status']='VERIFIED';persist()
finally:c.Logoff()
print(json.dumps(r,ensure_ascii=True,indent=2))
