"""Verify Exercise 19 evidence and absence of deliveries using GET only."""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dotenv import load_dotenv
from scripts.prepare_s4600_ex3_group00 import get, odata_date
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

load_dotenv(ROOT/'.env')
config=SapRuntimeConfig.from_env()
assert config.client=='600' and config.username.upper()=='ABDELJ'
saved=json.loads((ROOT/'runtime/sap_writes/s4600_ex19_gui_save_2026-10-22.json').read_text(encoding='utf-8'))
assert saved['status']=='VERIFIED' and saved['order']=='157' and not saved['mismatches']
today=json.loads((ROOT/'runtime/sap_reads/s4600_ex19_delivery_due_select_today.json').read_text(encoding='utf-8'))
due=json.loads((ROOT/'runtime/sap_reads/s4600_ex19_delivery_due_select_due.json').read_text(encoding='utf-8'))
assert len(today['tables'])==1 and today['tables'][0]['row_count']==0
assert len(due['tables'])==1 and due['tables'][0]['row_count']==2
rows=[{v['column']:v['text'] for v in row['values']} for row in due['tables'][0]['visible_rows']]
assert len(rows)==2 and {r['KUNWE'] for r in rows}=={'1000000112','1000000113'}
assert all(r['VBELV']=='157' and r['AMPEL'].startswith('@08') for r in rows)
assert all(row['ConfirmedDeliveryDate']==odata_date('2026-10-29') for row in saved['readback']['schedules']['rows'])
deliveries=get(UrllibSapTransport(config),'API_OUTBOUND_DELIVERY_SRV','A_OutbDeliveryItem',
               {'$filter':"ReferenceSDDocument eq '157'",'$select':'DeliveryDocument,DeliveryDocumentItem,ReferenceSDDocument','$top':'2'})
assert deliveries['http_status']==200 and deliveries['classification']=='NO_ROWS_FOR_EXACT_FILTER' and deliveries['count']==0
result={'status':'EXERCISE19_VERIFIED_COMPLETE','checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'sales_order':'157','reference':'6-400',
        'net_amount':'870.00','currency':'EUR','date_today':'2026-10-22','today_due_list_count':0,
        'material_availability_date':'2026-10-27','due_list_count_on_availability_date':2,
        'due_list_rows':rows,'linked_deliveries':deliveries,'delivery_created':False,
        'procedure_note':'VL10A is the official SAP delivery-due-list app. Only Execute selection was used.',
        'procedure_source':'https://help.sap.com/docs/SAP_S4HANA_CLOUD/aff0b3f5f46c42a2b2c0fabfc233bab2/707121e1b92f417cbbac8b9b86629262.html'}
output=ROOT/'runtime/sap_reads/s4600_ex19_final_validation_2026-10-22.json'
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
