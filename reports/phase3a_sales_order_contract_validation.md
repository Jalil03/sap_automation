# Phase 3A.1 — SALES_ORDER live contract validation

## Outcome

**NO-GO for an executable SALES_ORDER connector.** The corrected mapper is structurally compatible with the locally captured live metadata for its supported header and item properties, but OData V2 metadata does not prove deep-insert execution behavior. Ship-to partner-function semantics also remain unverified. No SAP connection, HTTP request, connector, or data mutation was performed.

## Evidence and service identification

| Evidence | Result |
|---|---|
| File | `evidence/sap_live/odata/API_SALES_ORDER_SRV.metadata.xml` |
| SHA-256 | `219aec8ef003541bb3b619c3000789a3397afc199caae85d8dc23b0ed83db5b8` |
| Size | 286,853 bytes |
| OData version | 2.0 |
| Schema namespace / consumer-facing service | `API_SALES_ORDER_SRV` |
| Technical Gateway registration from registry | `ZAPI_SALES_ORDER_SRV` |
| Technical name present in metadata | No |
| Root entity set | `A_SalesOrder` → `API_SALES_ORDER_SRV.A_SalesOrderType` |
| Complete parse inventory | 22 entity types, 22 entity sets, 54 associations |

The live metadata deterministically identifies `API_SALES_ORDER_SRV`, not `ZAPI_SALES_ORDER_SRV`, as its namespace. The Phase 2 contract now names `API_SALES_ORDER_SRV` as the consumer interface and retains `ZAPI_SALES_ORDER_SRV` separately as `technical_registration`. SALES_ORDER mapper results likewise expose `consumer_service_name: API_SALES_ORDER_SRV` separately from `technical_registration_name: ZAPI_SALES_ORDER_SRV`. The technical registration name is not an evidenced HTTP endpoint.

## CRUD capabilities

The five relevant entity sets contain no explicit `sap:creatable`, `sap:updatable`, or `sap:deletable` restriction. Under the SAP OData V2 annotation default, the metadata therefore does not disable create, update, or delete. This is metadata-level permission only; it is not proof that a particular user, system configuration, payload shape, or deep insert will execute successfully.

| Entity set | Entity type | Create | Update | Delete |
|---|---|---:|---:|---:|
| `A_SalesOrder` | `A_SalesOrderType` | metadata-default allowed | metadata-default allowed | metadata-default allowed |
| `A_SalesOrderItem` | `A_SalesOrderItemType` | metadata-default allowed | metadata-default allowed | metadata-default allowed |
| `A_SalesOrderHeaderPartner` | `A_SalesOrderHeaderPartnerType` | metadata-default allowed | metadata-default allowed | metadata-default allowed |
| `A_SalesOrderItemPartner` | `A_SalesOrderItemPartnerType` | metadata-default allowed | metadata-default allowed | metadata-default allowed |
| `A_SalesOrderScheduleLine` | `A_SalesOrderScheduleLineType` | metadata-default allowed | metadata-default allowed | metadata-default allowed |

No POST, PATCH, or DELETE was attempted.

## Navigation and deep structure

The root exposes `to_Item` (`A_SalesOrderItemType`, `*`) and `to_Partner` (`A_SalesOrderHeaderPartnerType`, `*`). Items expose `to_Partner` (`A_SalesOrderItemPartnerType`, `*`) and `to_ScheduleLine` (`A_SalesOrderScheduleLineType`, `*`). The schedule-line type exposes writable metadata fields including `ScheduleLine`, `RequestedDeliveryDate`, `OrderQuantityUnit`, and `ScheduleLineOrderQuantity`.

These navigation targets and cardinalities are a structural **MATCH**. Whether the service accepts a nested create through those navigation properties is **NOT_VERIFIED** because this OData V2 document has no deterministic deep-insert capability declaration. The current mapper continues to produce `to_Item`; a future connector must not treat this report as execution proof.

## Field-by-field assessment

This table covers all 23 current canonical SALES_ORDER mapping-contract fields. `MISMATCH` records the pre-validation Phase 2 mapping that was deterministically contradicted and has now been corrected.

| Canonical field | Phase 2 target / behavior | Classification | Live evidence and disposition |
|---|---|---|---|
| `order_type` | `SalesOrderType` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `sales_organization` | `SalesOrganization` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `distribution_channel` | `DistributionChannel` | MATCH | `Edm.String`, MaxLength 2, nullable, creatable/updatable |
| `sales_division` | `OrganizationDivision` | MATCH | `Edm.String`, MaxLength 2, nullable, creatable/updatable |
| `sold_to_party` | `SoldToParty` | MATCH | `Edm.String`, MaxLength 10, nullable, creatable/updatable |
| `ship_to_party` | formerly `ShipToParty` | MISMATCH | No header property. `to_Partner` exists, but partner-function semantics/deep insert are unverified; now unsupported. |
| `customer_reference` | `PurchaseOrderByCustomer` | MATCH | `Edm.String`, MaxLength 35, nullable, creatable/updatable |
| `requested_delivery_date` | `RequestedDeliveryDate` | RUNTIME_ONLY | `Edm.DateTime`, nullable, creatable/updatable; semantic relative dates still require runtime resolution. |
| `items[].line_id` | `to_Item[].SalesOrderItem` | MATCH | `Edm.String`, MaxLength 6, non-null, creatable/updatable |
| `items[].material` | `to_Item[].Material` | MATCH | `Edm.String`, MaxLength 40, nullable, creatable/updatable |
| `items[].quantity` | `to_Item[].RequestedQuantity` | MATCH | `Edm.Decimal(15,3)`, nullable, creatable/updatable |
| `items[].unit` | `to_Item[].RequestedQuantityUnit` | MATCH | `Edm.String`, MaxLength 3, nullable, creatable/updatable |
| `items[].plant` | `to_Item[].ProductionPlant` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `items[].ship_to_party` | formerly `to_Item[].ShipToParty` | MISMATCH | No item property. Item `to_Partner` exists; semantics/deep insert unverified; now unsupported. |
| `items[].shipping_point` | `to_Item[].ShippingPoint` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `items[].route` | formerly `to_Item[].Route` | MISMATCH | `Route` is absent from `A_SalesOrderItemType`; now unsupported. |
| `items[].net_weight` | formerly `to_Item[].NetWeight` | MISMATCH | Live field is `ItemNetWeight`, explicitly non-creatable/non-updatable; now unsupported. |
| `items[].net_weight_unit` | formerly `to_Item[].WeightUnit` | MISMATCH | Live field is `ItemWeightUnit`, explicitly non-creatable/non-updatable; now unsupported. |
| `items[].item_category` | `to_Item[].SalesOrderItemCategory` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `payment_terms` | `CustomerPaymentTerms` | MATCH | `Edm.String`, MaxLength 4, nullable, creatable/updatable |
| `processing_status` | intentionally ignored | NOT_VERIFIED | Observed canonical state was not equated to a writable status property. |
| `completeness_state` | intentionally ignored | NOT_VERIFIED | Observed canonical state was not equated to a writable status property. |
| `pricing_elements` | unsupported | NOT_VERIFIED | `to_PricingElement` exists, but writable nested behavior is not proven. |

Summary: **14 MATCH, 5 MISMATCH, 3 NOT_VERIFIED, 1 RUNTIME_ONLY**.

## Corrected mappings and validation contracts

Five invalid write claims were removed from `src/sap_mapping/odata.py`: header/item `ShipToParty`, item `Route`, `NetWeight`, and `WeightUnit`. The corresponding canonical fields are now `UNSUPPORTED` with evidence-specific reasons. This makes populated values fail deterministically instead of being silently dropped into invalid SAP fields.

The SALES_ORDER payload schema now rejects those removed fields and enforces live `MaxLength` facets for supported strings. It continues to enforce local mandatory payload fields, which are stricter than metadata nullability and represent the repository's create contract rather than a claim about all SAP operations.

The representative READY snapshot remains payload-identical because it does not populate any removed field. Its contract version and live-validation flag changed. Mapping coverage changed from 19 mapped / 1 unsupported to **14 mapped / 6 unsupported** for SALES_ORDER; the remaining dispositions are 2 intentionally ignored and 1 runtime-resolved.

## Unresolved and runtime-only items

- Deep insert through `A_SalesOrder/to_Item` is structurally present but not execution-verified.
- Header and item ship-to values require a verified partner-function mapping and proof that `to_Partner` is accepted in the intended write operation. No partner code was guessed.
- Relative requested-delivery dates remain runtime-resolved; no absolute date was fabricated.
- Schedule-line entities and fields are verified structurally, but the current canonical mapper does not claim or emit schedule-line deep inserts.
- Authorization, CSRF handling, endpoint base path, service activation, business validation, and live write behavior are outside this evidence file and remain untested.

## Automated test results

The new metadata tests parse the entire XML and pin its SHA-256, byte count, complete entity/entity-set/association counts, service identity, root entity set, CRUD annotations, field facets, navigation targets/cardinalities, all 23 field classifications, mapper exclusions, unsupported-field blocking, and payload `MaxLength` enforcement.

Targeted suite result: **30 tests passed** (`tests.test_phase3a_sales_order_metadata`, Phase 2C mapper validation, and Phase 2B core mapper regression). Full repository suite result: **114 tests passed**.

## Files changed

- `src/sap_mapping/odata_metadata.py`
- `src/sap_mapping/core.py`
- `src/sap_mapping/odata.py`
- `src/sap_mapping/validation.py`
- `schemas/sap/core_mapping_contracts.json`
- `schemas/sap/payloads.schema.json`
- `schemas/sap/sales_order_live_metadata_contract.json`
- `tests/test_phase3a_sales_order_metadata.py`
- `tests/test_phase2c_mapper_validation.py`
- `tests/snapshots/phase2c_core_payloads.json`
- `reports/phase2c_mapping_coverage.json`
- `reports/phase3a_sales_order_contract_validation.md`

## Gate

**NO-GO for SALES_ORDER connector development that can execute writes.** Proceed only after read-only runtime discovery confirms the actual service URL/activation and a controlled non-production validation establishes the accepted create/deep-insert shape, including partner-function semantics. The supported offline mapper subset is now internally consistent with the captured metadata, but metadata alone is not sufficient execution evidence.
