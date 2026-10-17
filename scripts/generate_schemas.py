"""Generate strict per-object Phase 1A schemas from the approved inventory."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; S={"type":["string","null"]}; N={"type":["number","null"]}; A={"type":"array","items":{"type":"string"}}; O={"type":["object","null"]}
GROUPS={
"CUSTOMIZING":{
"SALES_ORGANIZATION":["code","description","company_code"],"DISTRIBUTION_CHANNEL":["code","description","sales_organization"],"SALES_DIVISION":["code","description"],"SALES_AREA":["sales_organization","distribution_channel","sales_division"],"SHIPPING_POINT":["code","description","plant"],"CONDITION_TYPE":["code","description","calculation_type","access_sequence"],"CONDITION_TABLE":["table_id","key_fields"],"ACCESS_SEQUENCE":["code","condition_tables"],"PRICING_PROCEDURE":["code","steps"],"PRICING_PROCEDURE_DETERMINATION":["sales_organization","distribution_channel","sales_division","document_pricing_procedure","customer_pricing_procedure","pricing_procedure"],"ACCOUNT_DETERMINATION":["chart_of_accounts","account_key","general_ledger_account"],"COPY_CONTROL":["source_document_type","target_document_type","level","requirements"],"TEXT_DETERMINATION":["procedure","text_ids","access_sequence"],"OUTPUT_DETERMINATION":["procedure","output_types","channels"],"SHARED_MASTER_DATA_ASSIGNMENT":["sales_organization","source_distribution_channel","target_distribution_channel","source_sales_division","target_sales_division","scope"],"EXTENSION_CONFIGURATION":["configuration_family","configuration_key","description","target_object","settings"]},
"MASTER_DATA":{"BUSINESS_PARTNER":["partner_id","roles","name","sales_areas"],"MATERIAL":["material_id","description","base_unit","plants"],"CUSTOMER_MATERIAL_INFO":["business_partner","material","customer_material","sales_organization","distribution_channel"],"PRICING_CONDITION":["condition_type","key_combination","valid_from","valid_to","rate","currency","pricing_unit","scales"],"CUSTOMER_HIERARCHY":["hierarchy_type","nodes","valid_from","valid_to"],"CONDITION_CONTRACT":["contract_id","contract_type","business_partner","valid_from","valid_to","conditions"]},
"TRANSACTION":{"INQUIRY":["document_type","sold_to_party","valid_to","items"],"QUOTATION":["document_type","sold_to_party","valid_to","customer_reference","items"],"SALES_ORDER":["order_type","sales_organization","distribution_channel","sales_division","sold_to_party","ship_to_party","customer_reference","requested_delivery_date","items"],"CREDIT_MEMO_REQUEST":["document_type","sold_to_party","reason","reference_document","items"],"RETURN_ORDER":["document_type","sold_to_party","return_reason","reference_document","items"],"OUTBOUND_DELIVERY":["delivery_type","ship_to_party","shipping_point","planned_creation_date","planned_goods_issue_date","items"],"INBOUND_DELIVERY":["delivery_type","supplier","plant","expected_receipt_date","items"],"GOODS_ISSUE":["posting_date","movement_reference","delivery_reference","items"],"WAREHOUSE_TASK":["warehouse_number","source_bin","destination_bin","product","quantity","unit"],"BILLING":["billing_type","billing_subtype","payer","billing_date","reference_document","items","billing_plan","down_payments","installment_payments"],"SETTLEMENT_DOCUMENT":["settlement_type","condition_contract","settlement_date","amount","currency"]},
"REFERENCE_DATA":{"COMPANY_CODE":["code","description"],"PLANT":["code","description","company_code"],"STORAGE_LOCATION":["code","description","plant"],"WAREHOUSE_NUMBER":["code","description","plant_storage_locations"],"PURCHASE_ORDER_REFERENCE":["reference_id","supplier","plant","items"],"PAYMENT_REFERENCE":["reference_id","payer","billing_reference","amount","currency","payment_date"]}}
DIR={"CUSTOMIZING":"customizing","MASTER_DATA":"master_data","TRANSACTION":"transactions","REFERENCE_DATA":"reference_data"}
ARRAY_WORDS={"roles","sales_areas","plants","key_fields","condition_tables","requirements","text_ids","output_types","channels","scope","conditions","plant_storage_locations"}; OBJECT_ARRAY_WORDS={"steps","nodes","items","down_payments","installment_payments"}; NUMBER_WORDS={"rate","pricing_unit","quantity","amount"}; OBJECT_WORDS={"key_combination","billing_plan","requested_delivery_date","planned_creation_date"}
RELATIVE_VALUE={"type":["object","string","null"],"properties":{"kind":{"type":"string"},"raw":{"type":"string"},"offset":{"type":["string","null"]}},"additionalProperties":False}
SCALE_ARRAY={"type":"array","items":{"type":"object","anyOf":[{"required":["scale_basis","threshold"]},{"required":["from_quantity","quantity_unit","amount","currency"]}],"properties":{"scale_basis":{"enum":["QUANTITY","VALUE"]},"threshold":{"type":"number"},"threshold_unit":{"type":["string","null"]},"threshold_currency":{"type":["string","null"]},"amount":{"type":["number","null"]},"currency":{"type":["string","null"]},"rate":{"type":["number","null"]},"rate_unit":{"type":["string","null"]},"pricing_unit":{"type":["number","null"]},"from_quantity":{"type":["number","null"]},"quantity_unit":{"type":["string","null"]}},"additionalProperties":False}}
def prop(n): return SCALE_ARRAY if n=="scales" else {"type":"array","items":{"type":"object"}} if n in OBJECT_ARRAY_WORDS else A if n in ARRAY_WORDS else N if n in NUMBER_WORDS else O if n in OBJECT_WORDS else S
def properties_for(object_type, fields):
 props={f:prop(f) for f in fields}
 if object_type=="PRICING_CONDITION":
  props["key_combination"]={"type":["object","null"],"properties":{"sales_organization":S,"distribution_channel":S,"customer":S,"material":S,"incoterms":S,"destination_country":S,"customer_hierarchy_node":S,"promotion_reference":S,"sales_deal_reference":S},"additionalProperties":False}
  props.update({"scale_basis":S,"rate_unit":S,"calculation_semantics":S,
                "record_status":S,"source_operation":S,"adjustment_percent":N,
                "maximum_order_count":N,"maximum_quantity":N,
                "maximum_quantity_unit":S,"deletion_indicator":{"type":["boolean","null"]}})
  props["valid_from"]=RELATIVE_VALUE; props["valid_to"]=RELATIVE_VALUE
 if object_type=="SALES_ORDER":
  props.update({"payment_terms":S,"processing_status":S,"completeness_state":S,
                "pricing_elements":{"type":"array","items":{"type":"object"}}})
  props["items"]={"type":"array","items":{"type":"object","required":["line_id"],"properties":{"line_id":{"type":"string"},"material":S,"quantity":N,"unit":S,"plant":S,"ship_to_party":S,"shipping_point":S,"route":S,"net_weight":N,"net_weight_unit":S,"item_category":S},"additionalProperties":False}}
 if object_type=="BUSINESS_PARTNER":
  props.update({"grouping":S,"addresses":{"type":"array","items":{"type":"object"}},"currency":S,"shipping_conditions":S,"delivering_plant":S,"incoterms":S,"incoterms_location":S,"payment_terms":S,"account_assignment_group":S,"customer_pricing_procedure":S,"tax_classifications":{"type":"array","items":{"type":"object"}},"company_code":S,"reconciliation_account":S,"partner_functions":{"type":"array","items":{"type":"object"}},"fax_number":S})
 if object_type=="MATERIAL":
  props.update({"industry_sector":S,"material_type":S,"sales_organization":S,"distribution_channel":S,"tax_classification":S,"minimum_order_quantity":N,"minimum_order_unit":S,"sales_text":S,"availability_check":S,"delivering_plant":S,"strategy_group":S,"item_category_group":S})
 if object_type in {"INQUIRY","QUOTATION"}:
  props["valid_to"]=RELATIVE_VALUE
 if object_type in {"OUTBOUND_DELIVERY","INBOUND_DELIVERY"}:
  props["items"]={"type":"array","items":{"type":"object","properties":{"line_id":S,"material":S,"quantity":N,"unit":S,"reference_item":S,"plant":S,"storage_location":S,"warehouse_number":S,"item_category":S,"gross_weight":N,"gross_weight_unit":S},"additionalProperties":False}}
  props.update({"storage_location":S,"warehouse_number":S,"system_representations":{"type":"array","items":{"type":"object"}}})
 if object_type=="INBOUND_DELIVERY":
  props.update({"purchase_order_reference":S,"goods_receipt_status":S,"asn":S})
  props["expected_receipt_date"]=RELATIVE_VALUE
 if object_type in {"GOODS_ISSUE","BILLING"}:
  props["items"]={"type":"array","items":{"type":"object","properties":{"line_id":S,"material":S,"quantity":N,"unit":S,"reference_item":S},"additionalProperties":False}}
 if object_type=="GOODS_ISSUE": props["movement_status"]=S
 if object_type=="WAREHOUSE_TASK": props.update({"task_direction":S,"status":S,"delivery_reference":S})
 if object_type=="SHIPPING_POINT": props.update({"determination_rules":{"type":"array","items":{"type":"object"}},"working_times":S,"loading_time":S,"pick_pack_time":S})
 if object_type=="PURCHASE_ORDER_REFERENCE": props.update({"purchasing_organization":S,"purchasing_group":S,"company_code":S,"storage_location":S,"net_price":N,"currency":S,"confirmation_control":S})
 if object_type=="BILLING":
  props["billing_date"]=RELATIVE_VALUE
  props.update({"billing_status":S,"payment_terms":S,"net_value":N,"currency":S,
                "accounting_status":S,"accounting_document_type":S,
                "posting_blocked":{"type":["boolean","null"]},
                "fi_co_dependencies":{"type":"array","items":{"type":"object"}}})
  props["items"]={"type":"array","items":{"type":"object","properties":{"line_id":S,"material":S,"quantity":N,"unit":S,"reference_item":S,"net_value":N,"currency":S,"sales_division":S,"condition_values":{"type":"array","items":{"type":"object"}}},"additionalProperties":False}}
 if object_type=="ACCOUNT_DETERMINATION":
  props.update({"application":S,"condition_type":S,"account_determination_procedure":S,
                "access_sequence":S,"condition_table":S,"sales_organization":S,
                "customer_account_assignment_group":S,"material_account_assignment_group":S})
 if object_type=="COPY_CONTROL":
  props.update({"source_item_category":S,"pricing_type":S,"data_transfer_routine":S,
                "reference_number_rule":S,"assignment_number_rule":S,
                "billing_quantity_rule":S,"positive_negative_quantity":S,
                "target_item_category":S,"copy_requirement":S,
                "grouping_requirement":S,"header_data_transfer_routine":S,
                "item_data_transfer_routine":S,"document_flow_update":{"type":["boolean","null"]},
                "pricing_source":S})
 if object_type=="SALES_AREA": props["business_area_assignment_rule"]=S
 if object_type=="TEXT_DETERMINATION":
  props.update({"description":S,"level":S,"text_object":S,"source_text_object":S,
                "source_text_id":S,"assigned_document_types":A,
                "assigned_item_categories":A,"copy_reference_mode":S,
                "all_languages":{"type":["boolean","null"]},"requirement":S})
 if object_type=="OUTPUT_DETERMINATION":
  props.update({"description":S,"application_object_type":S,"framework":S,
                "access_sequence":S,"key_combinations":{"type":"array","items":{"type":"object"}},
                "condition_records":{"type":"array","items":{"type":"object"}},
                "processing_routines":{"type":"array","items":{"type":"object"}},
                "partner_role":S,"form_template":S,"print_queue":S,
                "number_of_copies":N,"send_time":S,
                "determination_rules":{"type":"array","items":{"type":"object"}}})
 if object_type=="EXTENSION_CONFIGURATION":
  props["settings"]={"type":"array","items":{"type":"object"}}
 if object_type=="PAYMENT_REFERENCE":
  props["payment_date"]=RELATIVE_VALUE
  props.update({"bank_account":S,"special_gl_indicator":S,"payment_status":S})
 if object_type=="CONDITION_TYPE":
  props.update({"reference_base":S,"group_condition":{"type":["boolean","null"]},
                "plus_minus_rule":S,"manual_entry_rule":S,
                "condition_update":{"type":["boolean","null"]},"scale_control":S,
                "copied_from_condition_type":S})
 if object_type=="CONDITION_TABLE": props["description"]=S
 if object_type=="ACCESS_SEQUENCE": props["description"]=S
 if object_type=="PRICING_PROCEDURE":
  props.update({"description":S,"exclusion_groups":{"type":"array","items":{"type":"object"}}})
 if object_type=="PRICING_PROCEDURE_DETERMINATION":
  props.update({"quick_entry_condition_type":S,"determination_context":S,
                "settlement_document_schema_group":S})
 if object_type=="CUSTOMER_HIERARCHY":
  props["sales_area"]={"type":["object","null"]}
  props["valid_from"]=RELATIVE_VALUE; props["valid_to"]=RELATIVE_VALUE
 if object_type=="CONDITION_CONTRACT":
  props["valid_from"]=RELATIVE_VALUE; props["valid_to"]=RELATIVE_VALUE
  props["conditions"]={"type":"array","items":{"type":"object"}}
  props.update({"sales_area":{"type":["object","null"]},
                "business_volume_selection_criteria":{"type":"array","items":{"type":"object"}},
                "settlement_schedule":{"type":"array","items":{"type":"object"}},
                "settlement_material":S,"contract_status":S})
 if object_type=="SETTLEMENT_DOCUMENT":
  props["settlement_date"]=RELATIVE_VALUE
  props.update({"execution_type":S,"document_id":S,"settlement_status":S,
                "business_volume":{"type":["object","null"]},
                "accounting_metadata":{"type":"array","items":{"type":"object"}}})
 return props
def main():
 idx={}
 for c,objs in GROUPS.items():
  d=ROOT/"schemas"/DIR[c]; d.mkdir(parents=True,exist_ok=True)
  for o,fields in objs.items():
   fn=o.lower()+".schema.json"; schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":o,"allOf":[{"$ref":"../common/canonical_object.schema.json"}],"type":"object","properties":{"object_type":{"const":o},"classification":{"const":c},"data":{"type":"object","properties":properties_for(o,fields),"additionalProperties":False}},"unevaluatedProperties":False}; (d/fn).write_text(json.dumps(schema,indent=2)+"\n",encoding="utf-8"); idx[o]={"classification":c,"schema":f"schemas/{DIR[c]}/{fn}"}
 (ROOT/"schemas"/"index.json").write_text(json.dumps(idx,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
