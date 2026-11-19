"""Save the two approved Book corrections once, then independently read them."""
import json,sys,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.readback_s4600_ex17 import readback
from scripts.stage_s4600_ex19_va01 import TABLE
from src.sap_gui_bridge.connection import SapGuiConnection
from src.sap_gui_bridge.safety import SafetyMode
OUT=ROOT/'runtime/sap_writes/s4600_ex17_correction_2026-10-22.json'
assert not OUT.exists(),'Existing correction attempt requires reconciliation'
before=readback('initial');assert before['status']=='VERIFIED' and before['order']=='158'
evidence=json.loads((ROOT/'runtime/sap_reads/s4600_ex17_gui_continue_weight_warning.json').read_text(encoding='utf-8'))
assert evidence['status_bar']=={'text':'Le document est complet','type':'S'}
s=SapGuiConnection(mode=SafetyMode.EXECUTE).attach()
assert s.identity['transaction']=='VA02' and str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
assert s.find('wnd[0]/sbar').Text=='Le document est complet'
prefix=str(s.raw.Id);table=TABLE.replace('/app/con[0]/ses[0]',prefix,1)
header='wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/'
for key,value in {header+'ctxtVBAK-VBELN':'158',header+'txtVBKD-BSTKD':'3-900',header+'txtVBAK-NETWR':'800,00',
                  table+'/ctxtRV45A-MABNR[1,0]':'10000283',table+'/txtRV45A-KWMENG[3,0]':'10'}.items():
    assert str(s.find(key).Text).strip()==value,key
s.audit('NAVIGATE',value='Verify Book net weight in corrected item before save')
s.find(table+'/txtVBAP-POSNR[0,0]').SetFocus();s.find('wnd[0]').sendVKey(2)
tab=s.find('wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03');assert tab.Text=='Expédition';tab.Select()
weightbody='wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\03/ssubSUBSCREEN_BODY:SAPMV45A:4452/'
assert str(s.find(weightbody+'txtVBAP-NTGEW').Text).strip()=='20'
assert s.find(weightbody+'ctxtVBAP-GEWEI').Text=='KG'
s.audit('BACK',value='Return to corrected order overview')
s.find('wnd[0]/tbar[0]/btn[3]').Press()
assert str(s.raw.Info.ScreenNumber)=='4001' and int(s.raw.Children.Count)==1
scope={'system':'A4H','client':'600','user':'ABDELJ','order':'158','operation':'COMPLETE_EX17_ORDER',
       'changes':{'PurchaseOrderByCustomer':'3-900','item10.ItemNetWeight':'20','item10.ItemWeightUnit':'KG'}}
digest=hashlib.sha256(json.dumps(scope,sort_keys=True,separators=(',',':')).encode()).hexdigest()
result={'status':'CORRECTION_SAVE_ATTEMPT_RECORDED','scope':scope,'sha256':digest,
        'approval_source':'User: on traite le 17; Book step 5', 'before':before,
        'attempted_at_utc':datetime.now(timezone.utc).isoformat(),'save_attempted':True}
def save():OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save()
button=s.find('wnd[0]/tbar[0]/btn[11]');assert button.Text=='Sauvegarder'
s.audit('PHASE5_OPERATION',control_id=str(button.Id),value={'operation':'SAVE_EX17_CORRECTION','sha256':digest})
button.Press()
result['save_returned']=True
result['status_bar']={'text':str(s.find('wnd[0]/sbar').Text),'type':str(s.find('wnd[0]/sbar').MessageType)}
save()
after=readback('corrected');result.update(status=after['status'],after=after);save()
print(json.dumps({'status':result['status'],'order':'158','status_bar':result['status_bar']},ensure_ascii=False,indent=2))
