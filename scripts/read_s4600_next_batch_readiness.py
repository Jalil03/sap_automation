"""Read-only scope for the separate FI/MM approval checkpoint."""
import json,sys
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport
load_dotenv(ROOT/'.env');cfg=SapRuntimeConfig.from_env();assert cfg.client=='600' and cfg.username.upper()=='ABDELJ';c=UrllibSapTransport(cfg)
r={'mode':'GET_ONLY','sap_write_performed':False,'deliveries':{},'stocks':{}}
for delivery in ('80000088','80000089','80000090','80000091'):
    h=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryHeader',{'$filter':f"DeliveryDocument eq '{delivery}'"})
    i=get(c,'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',{'$filter':f"DeliveryDocument eq '{delivery}'"})
    assert h['http_status']==200 and h['count']==1 and i['http_status']==200 and i['count']>0
    r['deliveries'][delivery]={'header':h,'items':i,'ready_for_pgi':h['rows'][0]['OverallPickingStatus']=='C' and h['rows'][0]['OverallGoodsMovementStatus']=='A' and all(x['StorageLocation']=='0001' for x in i['rows'])}
for material in ('10000282','10000283','10000284'):
    r['stocks'][material]=get(c,'API_MATERIAL_STOCK_SRV','A_MatlStkInAcctMod',{'$filter':f"Material eq '{material}' and Plant eq 'FR10' and StorageLocation eq '0001'"})
out=ROOT/'runtime/sap_reads/s4600_next_batch_readiness.json';out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'deliveries':{d:{'picking':v['header']['rows'][0]['OverallPickingStatus'],'goods_movement':v['header']['rows'][0]['OverallGoodsMovementStatus'],'items':[{k:x.get(k) for k in ('DeliveryDocumentItem','Material','ActualDeliveryQuantity','Plant','StorageLocation','GoodsMovementType','PickingStatus')} for x in v['items']['rows']]} for d,v in r['deliveries'].items()},'stock_rows':{m:v['rows'] for m,v in r['stocks'].items()}},ensure_ascii=True,indent=2))
