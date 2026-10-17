# S4615 user 00 — final blocker resolution

No SAP live read or write was performed. The full clean book and original PDF were not read.

## Status

- Common environment: **BLOCKED_NEEDS_HUMAN_DECISION**
- Customer: **BLOCKED_NEEDS_SOURCE**
- Product: **BLOCKED_NEEDS_SOURCE**
- S4615: **BLOCKED_NOT_EXECUTION_READY**

## Exact target

`{"company_code": "1010", "customer": "C615-D00", "customer_reference": "00S4615-BV", "distribution_channel": "10", "product": "P615-400", "quantity": 1, "sales_area": "1010/10/00", "sales_division": "00", "sales_order_type": "BV", "sales_organization": "1010", "training_user": "S4615-00", "unit": "PC"}`

## Workflow

| Order | Stage | Status |
|---:|---|---|
| 1 | COMMON_ENV | BLOCKED_NEEDS_HUMAN_DECISION |
| 2 | CUSTOMER_C615_D00 | BLOCKED_NEEDS_SOURCE |
| 3 | PRODUCT_P615_400 | BLOCKED_NEEDS_SOURCE |
| 4 | PRECHECKS | PENDING_DEPENDENCIES |
| 5 | ANTI_DUPLICATE_00S4615_BV | PENDING_DEPENDENCIES |
| 6 | BV_CASH_SALE | PENDING_DEPENDENCIES |
| 7 | VERIFY_AUTO_CREATED_DELIVERY | CONTRACT_REQUIRED |
| 8 | PGI | CONTRACT_REQUIRED |
| 9 | BILLING_BV | CONTRACT_REQUIRED |
| 10 | ACCOUNTING_READBACK | CONTRACT_REQUIRED |

## Final human decisions

- Company Code 1010: approved manual creation source and name/city/country/currency/language; chart of accounts is INT from the Book.
- Sales Org 1010: approved manual creation source, description, and statistics currency.
- Customer C615-D00: approve same-family template evidence or provide grouping/name/address/roles/company-code and sales-area mandatory values.
- Product P615-400: approve same-family template evidence or provide material type/industry/base UoM/plant/sales/logistics/valuation/tax values and PC conversion if PC is not base UoM.
- Customizing transport ownership/request must be supplied; release remains manual and is never automatic.
- Delivery, PGI, BV billing, and accounting readback need live read/write contracts before execution beyond the sales-order checkpoint.

## Classified values

### source_identity

| Field | Value | Classification |
|---|---|---|
| course | `"S4615 - Facturation dans SAP S/4HANA Sales"` | BOOK_CONFIRMED |
| course_version | `"12"` | BOOK_CONFIRMED |
| training_user_template | `"S4615-##"` | BOOK_CONFIRMED |
| training_user | `"S4615-00"` | DERIVED_FROM_TRAINING_FAMILY |

### common_environment

| Field | Value | Classification |
|---|---|---|
| company_code | `"1010"` | BOOK_CONFIRMED |
| sales_organization | `"1010"` | BOOK_CONFIRMED |
| sales_org_company_assignment | `"1010->1010"` | BOOK_CONFIRMED |
| distribution_channel | `"10"` | BOOK_CONFIRMED |
| sales_division | `"00"` | BOOK_CONFIRMED |
| sales_area | `"1010/10/00"` | BOOK_CONFIRMED |
| shipping_point | `"1010"` | BOOK_CONFIRMED |
| company_code_live_state | `"MISSING"` | SAP_CONFIRMED |
| sales_organization_live_state | `"MISSING"` | SAP_CONFIRMED |
| distribution_channel_live_state | `"EXISTS"` | SAP_CONFIRMED |
| sales_division_live_state | `"EXISTS"` | SAP_CONFIRMED |
| sales_org_company_assignment_live_state | `"UNKNOWN"` | UNKNOWN |
| distribution_channel_assignment_live_state | `"UNKNOWN"` | UNKNOWN |
| division_assignment_live_state | `"UNKNOWN"` | UNKNOWN |
| company_code_name | `null` | UNKNOWN |
| company_code_city | `null` | UNKNOWN |
| company_code_country | `null` | UNKNOWN |
| company_code_currency | `null` | UNKNOWN |
| company_code_language | `null` | UNKNOWN |
| company_code_chart_of_accounts | `"INT"` | BOOK_CONFIRMED |
| sales_organization_description | `null` | UNKNOWN |
| sales_organization_statistics_currency | `null` | UNKNOWN |

### customer

| Field | Value | Classification |
|---|---|---|
| customer_template | `"C615-D##"` | BOOK_CONFIRMED |
| customer | `"C615-D00"` | DERIVED_FROM_TRAINING_FAMILY |
| customer_live_state | `"MISSING"` | SAP_CONFIRMED |
| customer_sales_area | `"1010/10/00"` | BOOK_CONFIRMED |
| incoterms | `"CFR"` | BOOK_CONFIRMED |
| incoterms_location_template | `"##"` | BOOK_CONFIRMED |
| incoterms_location | `"00"` | DERIVED_FROM_TRAINING_FAMILY |
| customer_name | `null` | UNKNOWN |
| customer_address | `null` | UNKNOWN |
| bp_grouping | `null` | UNKNOWN |
| customer_roles | `null` | UNKNOWN |
| reconciliation_account | `null` | UNKNOWN |
| payment_terms | `null` | UNKNOWN |
| customer_currency | `null` | UNKNOWN |
| shipping_conditions | `null` | UNKNOWN |
| delivering_plant | `null` | UNKNOWN |
| account_assignment_group | `null` | UNKNOWN |
| customer_pricing_procedure | `null` | UNKNOWN |
| tax_classifications | `null` | UNKNOWN |
| partner_functions | `null` | UNKNOWN |

### product

| Field | Value | Classification |
|---|---|---|
| product_template | `"P615-4##"` | BOOK_CONFIRMED |
| product | `"P615-400"` | DERIVED_FROM_TRAINING_FAMILY |
| product_live_state | `"MISSING"` | SAP_CONFIRMED |
| ordered_quantity | `1` | BOOK_CONFIRMED |
| order_unit | `"PC"` | BOOK_CONFIRMED |
| semantic_product_kind | `"bicycle / stock product"` | BOOK_CONFIRMED |
| product_description | `null` | UNKNOWN |
| material_type | `null` | UNKNOWN |
| industry_sector | `null` | UNKNOWN |
| base_unit | `null` | UNKNOWN |
| plants | `null` | UNKNOWN |
| product_delivering_plant | `null` | UNKNOWN |
| item_category_group | `null` | UNKNOWN |
| product_tax_classification | `null` | UNKNOWN |
| availability_check | `null` | UNKNOWN |
| alternative_unit_conversions | `null` | UNKNOWN |

### golden_transaction

| Field | Value | Classification |
|---|---|---|
| sales_order_type | `"BV"` | BOOK_CONFIRMED |
| customer_reference_template | `"##S4615-BV"` | BOOK_CONFIRMED |
| customer_reference | `"00S4615-BV"` | DERIVED_FROM_TRAINING_FAMILY |
| billing_type | `"BV"` | BOOK_CONFIRMED |
| cancellation_billing_type | `"SV"` | BOOK_CONFIRMED |
| output_type | `"RD03"` | BOOK_CONFIRMED |
| delivery_created_on_cash_sale_save | `true` | BOOK_CONFIRMED |
| pgi_required_before_real_billing | `true` | BOOK_CONFIRMED |
| billing_reference | `"sales_order"` | BOOK_CONFIRMED |
| billing_pricing | `"NO_NEW_PRICING_DETERMINATION"` | BOOK_CONFIRMED |
| accounting_readback | `"cash + domestic revenue + output VAT"` | BOOK_CONFIRMED |

### additional_seed_facts

| Field | Value | Classification |
|---|---|---|
| precreated_training_data_mechanism | `"CATT import"` | BOOK_CONFIRMED |
| customer_families | `["C615-A##", "C615-B##", "C615-C##", "C615-D##", "C615-F##"]` | BOOK_CONFIRMED |
| product_families | `["P615-1##", "P615-2##", "P615-4##", "P615-5##", "P615-6##"]` | BOOK_CONFIRMED |
| customer_freight_condition_type | `"KF00"` | BOOK_CONFIRMED |
| customer_freight_sales_area | `"1010/10/00"` | BOOK_CONFIRMED |
| customer_freight_incoterms | `"CFR/##"` | BOOK_CONFIRMED |
| customer_freight_rate | `"10 EUR per 1 KG"` | BOOK_CONFIRMED |
| customer_freight_required_by_golden_flow | `null` | UNKNOWN |
| standard_item_category | `"TAN"` | BOOK_CONFIRMED |
| billing_types | `["F2", "F5", "F8", "G2", "BV", "SV"]` | BOOK_CONFIRMED |
| pricing_condition_types | `["PR00", "KF00"]` | BOOK_CONFIRMED |
| account_determination_procedure | `"KOFI00"` | BOOK_CONFIRMED |
| account_determination_condition_type | `"KOFI"` | BOOK_CONFIRMED |
| account_determination_table | `"001"` | BOOK_CONFIRMED |
| revenue_account_key | `"ERL"` | BOOK_CONFIRMED |
| freight_account_key | `"ERF"` | BOOK_CONFIRMED |
| account_determination_example_gl | `"41000000"` | BOOK_CONFIRMED |
| account_determination_second_example_gl | `"49000000"` | BOOK_CONFIRMED |
| material_account_assignment_group_example | `"01"` | BOOK_CONFIRMED |
| golden_flow_account_assignment_values | `null` | UNKNOWN |
