"""Record the verified GUI candidate for a scoped final save approval; no SAP call."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
candidate = {
    'environment': {'system': 'A4H', 'client': '600', 'user': 'ABDELJ'},
    'operation': 'SAVE_ONE_EXISTING_VA01_DRAFT_S4600_EX19_GROUP00',
    'header': {'sales_order_type': 'CS', 'sales_organization': 'FR10',
               'distribution_channel': '10', 'sales_division': '1W',
               'sold_to_party': '1000000112', 'customer_reference': '6-400',
               'requested_delivery_date': '2026-10-29'},
    'items': [
        {'item': '10', 'material': '10000282', 'quantity': '5',
         'unit': '289', 'ship_to_party': '1000000112'},
        {'item': '20', 'material': '10000284', 'quantity': '1',
         'unit': '289', 'ship_to_party': '1000000113'},
    ],
    'expected_net_amount': '870.00', 'currency': 'EUR',
    'delivery_creation_authorized': False,
}
fingerprint = hashlib.sha256(json.dumps(candidate, ensure_ascii=False, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
record = {'status': 'AWAITING_EXACT_FINAL_SAVE_APPROVAL', 'candidate': candidate,
          'sha256': fingerprint, 'save_attempted': False,
          'item10_shipping_dates': {'delivery': '2026-10-29', 'goods_issue': '2026-10-29',
              'loading': '2026-10-28', 'transport_planning': '2026-10-28',
              'material_availability': '2026-10-27'}}
output = ROOT / 'runtime/sap_reads/s4600_ex19_gui_save_candidate_2026-10-22.json'
output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status':record['status'], 'sha256':fingerprint, 'path':str(output)}))
