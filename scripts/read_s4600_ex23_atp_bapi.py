"""Read-only ATP query for Book exercise23; no order or reservation creation."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client
from dotenv import load_dotenv
from scripts.readback_s4600_ex31_pr00_rfc import get_item,set_parameter,table_get,table_append
from scripts.testrun_s4600_ex28_quotation_bapi import structure_dispatch,structure_get
from scripts.inspect_s4600_bapi_quotation_structures_readonly import raw_structure_columns
load_dotenv(ROOT/'.env');pythoncom.CoInitialize()
f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H';c.Client=os.environ['SAP_CLIENT'];c.User=os.environ['SAP_USERNAME'];c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
r={'mode':'READ_ONLY_BAPI','sap_write_performed':False,'target':{'material':'10000284','plant':'FR10','requested_quantity':'95','requested_date':'20261030','date_source':'Book next week, client date2026-10-23'},'bapi':'BAPI_MATERIAL_AVAILABILITY'}
try:
    assert c.Logon(0,True)
    r['identity']={'system':str(c.SystemID),'client':str(c.Client),'user':str(c.User).upper()};assert r['identity']=={'system':'A4H','client':'600','user':'ABDELJ'}
    b=f.Add(r['bapi']);r['metadata']={key:[str(x.Name) for x in list(getattr(b,key))] for key in ('Exports','Imports','Tables')}
    inputs={'MATERIAL':'10000284'.zfill(18),'PLANT':'FR10','UNIT':'ST'}
    assert set(inputs)<=set(r['metadata']['Exports'])
    r['observed_default_check_rule']=str(get_item(b.Exports,'CHECK_RULE').Value or '')
    for name,value in inputs.items():set_parameter(b,name,value)
    table=get_item(b.Tables,'WMDVSX');columns=[str(table.ColumnName(i)) for i in range(1,int(table.ColumnCount)+1)]
    r['input_columns']=columns;assert {'REQ_DATE','REQ_QTY'}<=set(columns)
    table_append(table,{'REQ_DATE':'20261030','REQ_QTY':'95'})
    r['called']=bool(b.Call)
    ret=structure_dispatch(get_item(b.Imports,'RETURN'));r['return']={col:structure_get(ret,col) for col in raw_structure_columns(ret)}
    result=get_item(b.Tables,'WMDVEX');cols=[str(result.ColumnName(i)) for i in range(1,int(result.ColumnCount)+1)]
    r['output_columns']=cols;r['rows']=[{col:table_get(result,i,col) for col in cols} for i in range(1,int(result.RowCount)+1)]
finally:c.Logoff()
(ROOT/'runtime/sap_reads/s4600_ex23_atp_bapi_2026-10-23.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True,indent=2))
