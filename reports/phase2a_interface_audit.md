# Phase 2A SAP Interface Audit

## Executive decision

**GO for scoped Phase 2B mapper development; NO-GO for full-scope Phase 2B or any execution.** Mapper work may proceed for the 29 object types with an evidenced interface plus the explicit `PAYMENT_REFERENCE` no-execution rule. The nine unresolved customizing types must remain excluded until an object-specific interface or an approved non-interface deployment mechanism is supplied. This audit did not connect to SAP and did not implement a mapper.

The audit covered all 39 canonical object types and all 201 validated canonical objects. Preferred-interface coverage is 30/39 types (76.9%) and 175/201 objects (87.1%), counting lookup-only and no-execution dispositions as resolved. The remaining 9 types represent 26 objects.

## Scope and evidence

The audit used only these repository-controlled inputs:

- `data/validated/canonical_objects.json`: 201 objects across 39 types; 26 `READY`, 175 `BLOCKED`.
- `inputs/sap_inventory/odata_services.xlsx`: `Data` sheet, 3,279 stored rows, including headings and blank/layout rows.
- `inputs/sap_inventory/rfc_remote_functions.xlsx`: `Data` sheet, 49,428 stored rows, including headings and blank/layout rows.
- `taxonomy/object_types.yaml`, `schemas/index.json`, and the referenced canonical schemas/contracts.

Every named candidate was accepted only after an exact technical service/version or function-name match in its source workbook. A semantic fit was also required. Generic functions such as `RFC_READ_TABLE`, broad text utilities, or names that merely contain terms such as “copy,” “output,” or “account” were rejected as evidence.

OData evidence retains both the exact technical name in the inventory and its external service name in `mappings/sap/interface_registry.yaml`. The inventory commonly records a `Z...` technical registration beside a non-`Z` external API name; the registry does not reinterpret or rename either value.

## Results summary

Preferred disposition by object type:

| Preferred classification | Types | Canonical objects | READY | BLOCKED |
|---|---:|---:|---:|---:|
| ODATA | 12 | 134 | 3 | 131 |
| STANDARD_BAPI | 5 | 13 | 0 | 13 |
| RFC_FUNCTION | 0 | 0 | 0 | 0 |
| LOOKUP_ONLY | 12 | 26 | 15 | 11 |
| NO_INTERFACE_FOUND | 9 | 26 | 8 | 18 |
| NO_EXECUTION_REQUIRED | 1 | 2 | 0 | 2 |
| **Total** | **39** | **201** | **26** | **175** |

Across preferred and alternate choices, the registry records 58 classified findings: 16 OData, 14 standard BAPI, 2 non-BAPI RFC function, 16 lookup-only, 9 no-interface, and 1 no-execution disposition.

## Preferred interface by canonical object type

“Resolved” means that the audit produced an explicit interface or no-execution disposition. It does not mean the canonical instances are downstream-ready or that runtime capability has been tested.

| Object type | Canonical class | Objects | Preferred classification | Exact preferred technical name | Audit status |
|---|---|---:|---|---|---|
| ACCESS_SEQUENCE | CUSTOMIZING | 2 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| ACCOUNT_DETERMINATION | CUSTOMIZING | 1 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| BILLING | TRANSACTION | 30 | ODATA | `ZAPI_BILLING_DOCUMENT_SRV` | RESOLVED |
| BUSINESS_PARTNER | MASTER_DATA | 3 | ODATA | `ZAPI_BUSINESS_PARTNER` | RESOLVED |
| COMPANY_CODE | REFERENCE_DATA | 1 | LOOKUP_ONLY | `ZAPI_COMPANYCODE_SRV` | RESOLVED |
| CONDITION_CONTRACT | MASTER_DATA | 1 | STANDARD_BAPI | `BAPI_CONDITION_CONTRACT_CREATE` | RESOLVED |
| CONDITION_TABLE | CUSTOMIZING | 4 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| CONDITION_TYPE | CUSTOMIZING | 5 | LOOKUP_ONLY | `ZAPI_SLSPRICINGCONDITIONTYPE_SRV` | RESOLVED |
| COPY_CONTROL | CUSTOMIZING | 8 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| CREDIT_MEMO_REQUEST | TRANSACTION | 1 | ODATA | `ZAPI_CREDIT_MEMO_REQUEST_SRV` | RESOLVED |
| CUSTOMER_HIERARCHY | MASTER_DATA | 1 | STANDARD_BAPI | `BAPI_CUSTOMER_HIERARCHIE_INS` | RESOLVED |
| CUSTOMER_MATERIAL_INFO | MASTER_DATA | 1 | ODATA | `ZAPI_CUSTOMER_MATERIAL_SRV` | RESOLVED |
| DISTRIBUTION_CHANNEL | CUSTOMIZING | 2 | LOOKUP_ONLY | `ZAPI_DISTRIBUTIONCHANNEL_SRV` | RESOLVED |
| EXTENSION_CONFIGURATION | CUSTOMIZING | 2 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| GOODS_ISSUE | TRANSACTION | 4 | STANDARD_BAPI | `BAPI_GOODSMVT_CREATE` | RESOLVED |
| INBOUND_DELIVERY | TRANSACTION | 2 | ODATA | `ZAPI_INBOUND_DELIVERY_SRV` v2 | RESOLVED |
| INQUIRY | TRANSACTION | 1 | ODATA | `ZAPI_SALES_INQUIRY_SRV` | RESOLVED |
| MATERIAL | MASTER_DATA | 4 | STANDARD_BAPI | `BAPI_MATERIAL_SAVEDATA` | RESOLVED |
| OUTBOUND_DELIVERY | TRANSACTION | 21 | ODATA | `ZAPI_OUTBOUND_DELIVERY_SRV` v2 | RESOLVED |
| OUTPUT_DETERMINATION | CUSTOMIZING | 3 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| PAYMENT_REFERENCE | REFERENCE_DATA | 2 | NO_EXECUTION_REQUIRED | — | RESOLVED |
| PLANT | REFERENCE_DATA | 1 | LOOKUP_ONLY | `ZAPI_PLANT_SRV` | RESOLVED |
| PRICING_CONDITION | MASTER_DATA | 14 | ODATA | `ZSD_PRICING_CONDITIONRECORD_SRV` | RESOLVED |
| PRICING_PROCEDURE | CUSTOMIZING | 3 | LOOKUP_ONLY | `ZAPI_SLSPRICINGPROCEDURE_SRV` | RESOLVED |
| PRICING_PROCEDURE_DETERMINATION | CUSTOMIZING | 3 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| PURCHASE_ORDER_REFERENCE | REFERENCE_DATA | 2 | LOOKUP_ONLY | `ZAPI_PURCHASEORDER_PROCESS_SRV` | RESOLVED |
| QUOTATION | TRANSACTION | 1 | ODATA | `ZAPI_SALES_QUOTATION_SRV` | RESOLVED |
| RETURN_ORDER | TRANSACTION | 1 | ODATA | `ZAPI_CUSTOMER_RETURN_SRV` | RESOLVED |
| SALES_AREA | CUSTOMIZING | 3 | LOOKUP_ONLY | `BAPI_SALES_AREAS_GET` | RESOLVED |
| SALES_DIVISION | CUSTOMIZING | 2 | LOOKUP_ONLY | `ZAPI_DIVISION_SRV` | RESOLVED |
| SALES_ORDER | TRANSACTION | 57 | ODATA | `ZAPI_SALES_ORDER_SRV` | RESOLVED |
| SALES_ORGANIZATION | CUSTOMIZING | 1 | LOOKUP_ONLY | `ZAPI_SALESORGANIZATION_SRV` | RESOLVED |
| SETTLEMENT_DOCUMENT | TRANSACTION | 3 | STANDARD_BAPI | `BAPI_CONDITION_CONTRACT_SETTLE` | RESOLVED |
| SHARED_MASTER_DATA_ASSIGNMENT | CUSTOMIZING | 1 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| SHIPPING_POINT | CUSTOMIZING | 3 | LOOKUP_ONLY | `/SMERP/MM_CTSHIPPINGPOINT_GET` | RESOLVED |
| STORAGE_LOCATION | REFERENCE_DATA | 2 | LOOKUP_ONLY | `ZAPI_STORAGELOCATION_SRV` | RESOLVED |
| TEXT_DETERMINATION | CUSTOMIZING | 2 | NO_INTERFACE_FOUND | — | UNRESOLVED |
| WAREHOUSE_NUMBER | REFERENCE_DATA | 1 | LOOKUP_ONLY | `ZAPI_WAREHOUSE` | RESOLVED |
| WAREHOUSE_TASK | TRANSACTION | 2 | ODATA | `ZAPI_WAREHOUSE_ORDER_TASK` | RESOLVED |

The registry contains the alternate evidence omitted from this compact table. Examples include `BAPI_SALESORDER_CREATEFROMDAT2`, `BAPI_OUTB_DELIVERY_CREATE_SLS`, `BAPI_BILLINGDOC_CREATEMULTIPLE`, `BAPI_CUSTOMERRETURN_CREATE`, `BAPI_BUPA_CREATE_FROM_DATA`, `API_PRODUCT_SRV` through technical service `ZAPI_PRODUCT_SRV`, `/SCWM/TO_CREATE`, and `WB2R_SETTLEMENT_RFC`.

## Unresolved object types

No sufficiently specific interface was found for:

- `ACCESS_SEQUENCE` — 2 objects
- `ACCOUNT_DETERMINATION` — 1 object
- `CONDITION_TABLE` — 4 objects
- `COPY_CONTROL` — 8 objects
- `EXTENSION_CONFIGURATION` — 2 objects
- `OUTPUT_DETERMINATION` — 3 objects
- `PRICING_PROCEDURE_DETERMINATION` — 3 objects
- `SHARED_MASTER_DATA_ASSIGNMENT` — 1 object
- `TEXT_DETERMINATION` — 2 objects

These are all customizing types. They must not be mapped to generic RFC utilities on name similarity. Before they enter Phase 2B, the owner must provide one of: an exact supported API/function, an approved customizing transport/deployment route, or an explicit policy that they are validation-only and require no direct execution.

`PAYMENT_REFERENCE` is deliberately `NO_EXECUTION_REQUIRED`. It represents the reference/dependency captured from source material, not authorization to create a payment request or FI posting. The payment-related names in the RFC inventory therefore are not candidates for this object.

## Selection rationale and constraints

- OData is preferred where an object-specific process API is present. Delivery v2 is preferred over v1 because both exact versions appear in the inventory and v2 is the later registered version; Phase 2B must still verify its entity/action coverage before mapping.
- Standard BAPIs are preferred where their operation is more specific than a broader OData document concept: material maintenance, goods movement for goods issue, customer hierarchy maintenance, condition-contract maintenance, and condition-contract settlement.
- Organizational units and reference data are `LOOKUP_ONLY`. Their interfaces may validate values and resolve keys but must not be treated as permission to alter customizing.
- `SHIPPING_POINT` has only the exact specialized lookup `/SMERP/MM_CTSHIPPINGPOINT_GET`; its namespace and runtime availability require confirmation before reliance.
- The presence of a name in an inventory proves registration/listing only. It does not prove authorization, activation, entity shape, method support, transaction behavior, or fitness for a specific canonical field set.
- The 175 `BLOCKED` canonical objects remain blocked. Interface availability does not override unresolved placeholders, dependencies, or Phase 1 readiness policy.
- The open S4600 return-delivery ambiguity is unchanged. `API_CUSTOMER_RETURN_SRV` is an interface candidate for `RETURN_ORDER`; it is not evidence resolving the disputed return-delivery interpretation.

## Validation and deterministic controls

The audit builder validates that:

1. canonical data, taxonomy, and schema index cover the same 39 types;
2. schema classifications match canonical classifications and all indexed schema files exist;
3. every named OData technical name/version and external name matches an inventory row exactly;
4. every named BAPI/RFC function matches the RFC inventory exactly;
5. each preferred interface is one of the recorded candidates;
6. candidate classifications use only the six values requested for Phase 2A;
7. rerunning against unchanged inputs produces byte-identical registry content; and
8. the registry records that no SAP connection and no mapper implementation occurred.

Phase 2A added seven deterministic tests. They all pass. The full repository suite passes **84 tests** in total (77 existing Phase 1 tests plus 7 Phase 2A tests).

## Phase 2B entry conditions

Scoped Phase 2B may begin for the resolved subset under these gates:

1. develop mapper contracts only; preserve `READY`/`BLOCKED` and never submit blocked objects;
2. validate actual service metadata/function signatures, supported operations, mandatory fields, and version compatibility before coding field mappings;
3. keep lookup-only types non-mutating;
4. keep `PAYMENT_REFERENCE` as a no-op/reference mapping;
5. exclude the nine unresolved customizing types from executable scope; and
6. retain all canonical provenance and dependency controls.

Full-scope Phase 2B remains **NO-GO** until the nine customizing gaps have an approved disposition. SAP connectivity and execution remain outside this audit and were not attempted.

## Files generated

- `mappings/sap/interface_registry.yaml`
- `reports/phase2a_interface_audit.md`
- `scripts/audit_sap_interfaces.py`
- `tests/test_phase2a_interface_audit.py`
