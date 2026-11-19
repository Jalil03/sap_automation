"""Join independent RFC evidence and update the local diagnosis, no SAP call."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
READS=ROOT/'runtime/sap_reads'
def evidence(mode):
    return json.loads((READS/f's4600_ex17_incompletion_{mode}_2026-10-22.json').read_text(encoding='utf-8'))
header=evidence('header_assignment')['reads']['header_assignment']['rows']
item=evidence('item_assignment')['reads']['item_assignment']['rows']
fields=evidence('fields')['reads']['missing_field_settings']['rows']
groups=evidence('status_groups')['reads']['status_groups']['rows']
assert len(header)==len(item)==1 and header[0]=={'AUART':'TA','FEHGR':'11'} and item[0]=={'PSTYV':'TAN','FEHGR':'20'}
joined=[]
for procedure,table,field in [('11','VBKD','BSTKD'),('20','VBAP','NTGEW')]:
    matches=[r for r in fields if r['FEHGR']==procedure and r['TBNAM']==table and r['FDNAM']==field]
    assert len(matches)==1 and matches[0]['MANDT']=='600'
    group=[r for r in groups if r['STATG']==matches[0]['STATG']]
    assert len(group)==1 and group[0]['MANDT']=='600' and group[0]['UVVLK']==''
    joined.append({'procedure':procedure,'table':table,'field':field,'status_group':matches[0]['STATG'],
                   'generally_incomplete':group[0]['UVALL']=='X','blocks_delivery':False})
result={'status':'DIAGNOSIS_VERIFIED_CURRENT_CONFIGURATION_DOES_NOT_BLOCK_DELIVERY',
        'environment':{'system':'A4H','client':'600','user':'ABDELJ'},'evidence_join':joined,
        'conclusion':'The two missing fields are not configured to set delivery incompletion. Observed delivery creation is consistent with current configuration; an API bypass is not established.',
        'limitation':'The settings were read after the test; no historical customizing snapshot is available to rule out intervening changes.',
        'sap_writes':False,'new_delivery':False,
        'source':'https://help.sap.com/docs/signavio-process-insights/administration-guide/be4b0a35f6d048eb979899f569509c78.html'}
(READS/'s4600_ex17_diagnosis_conclusion_2026-10-22.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
final_path=READS/'s4600_ex17_final_validation_2026-10-22.json'
final=json.loads(final_path.read_text(encoding='utf-8'))
final['root_cause']=result['conclusion'];final['configuration_diagnosis']=result
final_path.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
