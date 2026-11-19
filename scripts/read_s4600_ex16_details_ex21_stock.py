"""Read proposal items, BP update contract, and the stock/requirements list."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pythoncom,win32com.client,xml.etree.ElementTree as ET
from dotenv import load_dotenv
from scripts.readback_s4600_ex31_pr00_rfc import rfc_read_table,get_item,set_parameter,table_get
from scripts.testrun_s4600_ex28_quotation_bapi import structure_dispatch,structure_get
from scripts.inspect_s4600_bapi_quotation_structures_readonly import raw_structure_columns
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');pythoncom.CoInitialize()
f=win32com.client.Dispatch('SAP.Functions.Unicode');c=f.Connection
c.ApplicationServer=os.environ['SAP_APPLICATION_SERVER'];c.SystemNumber=os.environ['SAP_SYSTEM_NUMBER'];c.SystemID='A4H';c.Client=os.environ['SAP_CLIENT'];c.User=os.environ['SAP_USERNAME'];c.Password=os.environ['SAP_PASSWORD'];c.Language='FR'
r={'mode':'READ_ONLY','write_called':False}
try:
    assert c.Logon(0,True)
    assert (str(c.SystemID),str(c.Client),str(c.User).upper())==('A4H','600','ABDELJ')
    r['proposal_items']=rfc_read_table(f,'VBAP',['VBELN','POSNR','MATNR','ZMENG','ZIEME'],["VBELN = '0050000001'"])
    b=f.Add('BAPI_MATERIAL_STOCK_REQ_LIST')
    for name,value in {'MATERIAL':'10000284'.zfill(18),'PLANT':'FR10','GET_IND_LINES':'X','GET_ITEM_DETAILS':'X','GET_TOTAL_LINES':'X'}.items():set_parameter(b,name,value)
    r['stock_bapi_called']=bool(b.Call)
    ret=structure_dispatch(get_item(b.Imports,'RETURN'))
    r['stock_return']={col:structure_get(ret,col) for col in raw_structure_columns(ret)}
    r['stock_tables']={}
    if r['stock_bapi_called']:
        for name in ('MRP_IND_LINES','MRP_ITEMS','MRP_TOTAL_LINES'):
            t=get_item(b.Tables,name);columns=[str(t.ColumnName(i)) for i in range(1,int(t.ColumnCount)+1)]
            r['stock_tables'][name]={'columns':columns,'rows':[{col:table_get(t,i,col) for col in columns} for i in range(1,int(t.RowCount)+1)]}
finally:c.Logoff()
api=UrllibSapTransport(SapRuntimeConfig.from_env());md=api.request('GET','sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata');assert md.status==200
ns={'e':'http://schemas.microsoft.com/ado/2008/09/edm'};root=ET.fromstring(md.body)
r['bp_update_contract']={'set':[x.attrib for x in root.findall('.//e:EntitySet',ns) if x.get('Name')=='A_CustomerSalesArea'],'property':[]}
for entity in root.findall('.//e:EntityType',ns):
    if entity.get('Name')=='A_CustomerSalesAreaType':r['bp_update_contract']['property']=[x.attrib for x in entity.findall('e:Property',ns) if x.get('Name')=='SalesItemProposal']
r['customer']=get(api,'API_BUSINESS_PARTNER','A_CustomerSalesArea',{'$filter':"Customer eq '1000000112' and SalesOrganization eq 'FR10' and DistributionChannel eq '10' and Division eq '1W'"})
suffix=sys.argv[1] if len(sys.argv)>1 else 'before'
(ROOT/f'runtime/sap_reads/s4600_ex16_details_ex21_stock_{suffix}.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps({'file_suffix':suffix,'proposal_items':r['proposal_items'],'bp_update_contract':r['bp_update_contract'],'stock_return':r.get('stock_return'),'stock_rows':{k:v['rows'] for k,v in r['stock_tables'].items()}},indent=2))
