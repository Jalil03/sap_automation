"""Bounded MTO identity discovery; GET only, never assign a candidate mapping."""
from __future__ import annotations
import json,sys
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode

def bounded_read(client,service,entity,query):
    assert int(query.get('$top','21'))<=21
    response=client.request('GET','sap/opu/odata/sap/'+service+'/'+entity+'?'+urlencode(query),headers={'Accept':'application/json'})
    result={'request':{'service':service,'entity':entity,**query},'http_status':response.status}
    if response.status!=200:return {**result,'classification':'UNKNOWN_READ_ERROR','error':response.sanitized_sap_error()}
    data=response.json().get('d',{});rows=data.get('results',[])
    result.update(rows=[{k:v for k,v in x.items() if k!='__metadata'} for x in rows],count=len(rows),has_next_page=bool(data.get('__next')))
    result['classification']='BOUNDED_MATCHES_NOT_AUTOMATIC_MAPPING' if rows else 'NO_MATCH_FOR_EXACT_FILTER'
    return result

def main():
    load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ'
    session=SapGuiConnection(mode=SafetyMode.READ).attach();session.validate_identity();client=UrllibSapTransport(cfg)
    metadata=json.loads((ROOT/'runtime/sap_reads/s4600_ex1_23_30_34_preflight_2026-10-23.json').read_text(encoding='utf-8'))['metadata']['API_PRODUCT_SRV']['types']
    fields=['Product','Plant','PlanningStrategyGroup','ProcurementType','MRPType','MRPResponsible','LotSizingProcedure','BaseUnit','InHouseProductionTime']
    assert set(fields)<={x['Name'] for x in metadata['A_ProductSupplyPlanningType']['properties']}
    r={'captured_at':datetime.now(timezone.utc).isoformat(),'environment':session.identity,'mode':'GET_ONLY','sap_write_performed':False,'logical_target':'T-F100','mapping_status':'UNKNOWN','checks':{}}
    r['checks']['logical_family']=bounded_read(client,'API_PRODUCT_SRV','A_Product',{'$filter':"startswith(Product,'T-F1') or startswith(ProductOldID,'T-F1')",'$select':'Product,ProductOldID,ProductType,BaseUnit,Division','$top':'21'})
    r['checks']['fr10_manufacturing_candidates']=bounded_read(client,'API_PRODUCT_SRV','A_ProductSupplyPlanning',{'$filter':"Plant eq 'FR10' and (PlanningStrategyGroup eq '20' or ProcurementType eq 'E')",'$select':','.join(fields),'$top':'21'})
    candidates=r['checks']['fr10_manufacturing_candidates'].get('rows',[])
    r['candidate_details']={}
    # Technical candidates are not Book equivalents. Keep reads bounded to five.
    for row in candidates[:5]:
        product=row['Product'];assert "'" not in product
        r['candidate_details'][product]={
            'root':bounded_read(client,'API_PRODUCT_SRV','A_Product',{'$filter':f"Product eq '{product}'",'$select':'Product,ProductOldID,ProductType,BaseUnit,Division','$top':'2'}),
            'description':bounded_read(client,'API_PRODUCT_SRV','A_ProductDescription',{'$filter':f"Product eq '{product}'",'$select':'Product,Language,ProductDescription','$top':'5'}),
            'sales':bounded_read(client,'API_PRODUCT_SRV','A_ProductSalesDelivery',{'$filter':f"Product eq '{product}' and ProductSalesOrg eq 'FR10' and ProductDistributionChnl eq '10'",'$select':'Product,ProductSalesOrg,ProductDistributionChnl,ItemCategoryGroup,SupplyingPlant','$top':'2'})}
    out=ROOT/'runtime/sap_reads/s4600_ex30_mto_candidates_2026-10-23.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
