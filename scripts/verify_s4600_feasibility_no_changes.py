"""Independent GET-only reconciliation after the feasibility simulations."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.audit_s4600_ex30_mto_candidates_readonly import bounded_read
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
baseline=json.loads((ROOT/'runtime/sap_reads/s4600_remaining_feasibility_readonly_2026-10-23.json').read_text(encoding='utf-8'))
r={'mode':'GET_ONLY_RECONCILIATION','checks':{},'sap_write_performed':False}
def read(service,entity,expression):return bounded_read(c,service,entity,{'$filter':expression,'$top':'21'})
for delivery,b in baseline['deliveries'].items():
    h=read('API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',f"DeliveryDocument eq '{delivery}'")
    keys=('OverallPickingStatus','OverallGoodsMovementStatus','ActualGoodsMovementDate')
    same=h['http_status']==200 and h['count']==1 and all(h['rows'][0].get(k)==b['header']['rows'][0].get(k) for k in keys)
    inv=read('API_BILLING_DOCUMENT_SRV','A_BillingDocumentItem',f"ReferenceSDDocument eq '{delivery}'")
    r['checks'][delivery]={'delivery_statuses_unchanged':same,'billing_absence_confirmed':inv['http_status']==200 and inv['count']==0 and not inv['has_next_page']}
for material,b in baseline['stocks'].items():
    stock=read('API_MATERIAL_STOCK_SRV','A_MatlStkInAcctMod',f"Material eq '{material}' and Plant eq 'FR10' and StorageLocation eq '0001'")
    def canonical(rows):return sorted(json.dumps({k:x[k] for k in ('Material','Plant','StorageLocation','Batch','InventorySpecialStockType','InventoryStockType','SDDocument','SDDocumentItem','MatlWrhsStkQtyInMatlBaseUnit')},sort_keys=True) for x in rows)
    same=stock['http_status']==200 and not stock['has_next_page'] and canonical(stock['rows'])==canonical(b['read']['rows'])
    r['checks']['stock_'+material]={'stock_unchanged':same}
r['status']='VERIFIED_UNCHANGED' if all(all(v.values()) for v in r['checks'].values()) else 'DRIFT_OR_UNKNOWN_REQUIRES_RECONCILIATION'
(ROOT/'runtime/sap_reads/s4600_feasibility_reconciliation_2026-10-23.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True,indent=2))
