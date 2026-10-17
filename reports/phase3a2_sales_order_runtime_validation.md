# Runtime evidence clears read-only SALES_ORDER development, but not writes

## Executive summary

- **GO for read-only SALES_ORDER connector development.** Four captured OData V2 GET responses confirm the external service path, root/entity-set identities, key predicates, selected runtime fields, relationship keys, JSON representations, nullable date behavior, and a root weak ETag.
- **NO-GO for a write-capable connector and NO-GO for a controlled write pilot.** GET evidence proves read behavior only. It does not prove POST/deep-insert acceptance, write authorization, transaction behavior, idempotency, partner business semantics, or accepted write representations.
- No deterministic mismatch was found between the runtime captures and Phase 3A.1 metadata. The write mapper was therefore not changed. A separate strict read-response schema was added so OData V2 GET representations cannot silently alter write assumptions.

No SAP connection or HTTP request was made. No connector was implemented, no SAP operation was executed, and canonical Phase 1 data was not modified.

## Evidence

| File | SHA-256 | Records | Runtime entity set |
|---|---|---:|---|
| `sales_order_sample.json` | `40c5ef78f97932672f62a835bbb6c2e5ce4495e1ac7bfae3d681cbb8743f3e37` | 1 | `A_SalesOrder` |
| `sales_order_partners_sample.json` | `1aabc27a657ef79e7a096f48446a2bdf8b7eaa46a5297665d80009d272cace93` | 4 | `A_SalesOrderHeaderPartner` |
| `sales_order_items_sample.json` | `b60b8ab958824b8269030d0416cf11915a6307b8f74d359a63d176f281ef648f` | 1 | `A_SalesOrderItem` |
| `sales_order_schedule_lines_sample.json` | `325f9442c7492e9db678593cd05fd2eafcfd6f8e6f4c669c81645f0f7be262b0` | 2 | `A_SalesOrderScheduleLine` |

The Phase 3A.1 metadata evidence remains pinned at SHA-256 `219aec8ef003541bb3b619c3000789a3397afc199caae85d8dc23b0ed83db5b8`.

## Runtime shape confirmed

All captures use the OData V2 collection envelope `d.results`. Their `__metadata.type` values match the metadata namespace `API_SALES_ORDER_SRV`, and all entity URIs use the consumer-facing service path `/sap/opu/odata/sap/API_SALES_ORDER_SRV/`. Nothing in the runtime evidence supports using technical Gateway registration `ZAPI_SALES_ORDER_SRV` as the HTTP service name.

### Entities and keys

| Entity | Observed key predicate | Observed JSON keys |
|---|---|---|
| Sales order | `A_SalesOrder('1')` | `SalesOrder: "1"` |
| Item | `A_SalesOrderItem(SalesOrder='1',SalesOrderItem='10')` | Item sample returns `SalesOrderItem: "10"`; parent key is retained in the URI |
| Header partner | `A_SalesOrderHeaderPartner(SalesOrder='1',PartnerFunction='<code>')` | Partner samples return the code; parent key is retained in the URI |
| Schedule line | `A_SalesOrderScheduleLine(SalesOrder='1',SalesOrderItem='10',ScheduleLine='<line>')` | `SalesOrder: "1"`, `SalesOrderItem: "10"`, lines `"1"` and `"2"` |

Keys are quoted Edm.String literals in entity URIs. The captured business keys are returned as strings and are not zero-padded beyond the values actually stored (`"1"`, `"10"`, `"1"`/`"2"`). The evidence does not establish a general padding rule for other records.

### Relationships

| Relationship | Runtime conclusion | Boundary |
|---|---|---|
| `SalesOrder → to_Partner` | RUNTIME_CONFIRMED | Metadata defines `to_Partner`; all captured header-partner keys reference sales order `"1"`. The capture is a separate collection, not an expanded navigation response. |
| `SalesOrder → to_Item` | RUNTIME_CONFIRMED | Metadata defines `to_Item`; the captured item URI contains `SalesOrder='1'`. |
| `SalesOrderItem → to_ScheduleLine` | RUNTIME_CONFIRMED | Metadata defines `to_ScheduleLine`; both schedule-line records reference order `"1"`, item `"10"`. |

This confirms readable relationship identity, not nested create or deep-insert behavior.

## Returned fields and representations

Every returned business field exists on the matching metadata entity type.

| Shape | Returned fields | Runtime representation |
|---|---|---|
| Header | `SalesOrder`, `SalesOrderType`, `SalesOrganization`, `DistributionChannel`, `OrganizationDivision`, `SoldToParty` | JSON strings |
| Item | `SalesOrderItem`, `Material`, `RequestedQuantity`, `RequestedQuantityUnit`, `ProductionPlant`, `ShippingPoint` | Strings; the `Edm.Decimal` quantity is serialized as `"1"` |
| Partner | `PartnerFunction`, `Customer` | JSON strings |
| Schedule line | `SalesOrder`, `SalesOrderItem`, `ScheduleLine`, `RequestedDeliveryDate`, `OrderQuantityUnit`, `ScheduleLineOrderQuantity` | Keys/units/decimal quantity are strings; date is OData `/Date(milliseconds)/` or JSON `null` |

Observed unit fields contain the string `"289"`. This confirms the returned value and type only. It is insufficient to infer a conversion from canonical units such as `PC`, or to claim that the write API accepts one representation instead of another.

The root record contains a weak ETag in `__metadata.etag`. No child capture contains an ETag. That absence is **NOT_VERIFIED** as a general child-entity rule because the samples may reflect selection or endpoint behavior rather than a universal contract.

## Partner behavior

The observed `PartnerFunction` codes are `RM`, `DO`, `RF`, and `PY`; all four records contain `Customer: "17100002"`. Their business meanings are **NOT_VERIFIED**. Neither the metadata nor the supplied GET captures provides a deterministic code-to-role definition, so none was assigned to sold-to, ship-to, bill-to, payer, or another canonical semantic.

Consequently, the Phase 3A.1 decision remains unchanged: header/item canonical `ship_to_party` is not written through `to_Partner` until partner-function semantics and write behavior are separately evidenced.

## Metadata/runtime assumption matrix

| Assumption group | Classification | Result |
|---|---|---|
| External service name, root set/type | RUNTIME_CONFIRMED | Runtime URIs/types use `API_SALES_ORDER_SRV` and `A_SalesOrder`. |
| Root, item, partner, and schedule key formatting | RUNTIME_CONFIRMED | Quoted string predicates and named composite keys observed. |
| Order→partner, order→item, item→schedule identity | RUNTIME_CONFIRMED | Metadata navigation plus matching captured keys. |
| Selected header/item/partner/schedule fields | RUNTIME_CONFIRMED | Names exactly match metadata. |
| Decimal, unit, date, and null GET representations | RUNTIME_CONFIRMED | Decimal/unit strings, `/Date(...)` string, and JSON null observed. |
| Root ETag | RUNTIME_CONFIRMED | Weak ETag observed. |
| Overall metadata/runtime field consistency | MATCH | No returned field, type, or null contradicted metadata. |
| Deep-insert and entity write capability | METADATA_ONLY | Navigation and non-disabled metadata capabilities exist; GETs add no write proof. |
| Child ETag behavior | NOT_VERIFIED | No child ETag observed; general behavior cannot be inferred. |
| Meanings of RM/DO/RF/PY | NOT_VERIFIED | Codes observed without semantic definitions. |
| Accepted POST quantity/date/unit representation | NOT_VERIFIED | GET serialization is not a POST contract. |
| Write authorization, transaction behavior, idempotency | NOT_VERIFIED | No write operation occurred. |

The machine-readable matrix contains 30 assumptions: **19 RUNTIME_CONFIRMED, 1 MATCH, 2 METADATA_ONLY, 8 NOT_VERIFIED, 0 MISMATCH**.

## Contract and mapper impact

No mapper field or write-payload contract was changed because the GET captures prove no deterministic write mismatch. In particular:

- The mapper's numeric `RequestedQuantity` write value was not changed to a string merely because GET serializes `Edm.Decimal` as a string.
- The mapper's date handling was not changed to `/Date(...)` because the response representation does not prove the accepted POST representation.
- No unit translation from canonical values to observed code `"289"` was invented.
- No partner code was mapped to a canonical business role.

A new strict read-response schema validates the four capture types separately. The core mapping contract now records `CAPTURED_GET_RESPONSES_ONLY` runtime validation, and its version is `1.2.0`. Phase 2C snapshots and coverage were regenerated deterministically for the version change.

## Remaining blockers

- POST and deep-insert payload acceptance is untested.
- Write authorization and CSRF behavior are untested.
- Partner-function business meanings and the correct writable partner structure are unverified.
- Accepted write representations for decimals, dates, and unit codes are unverified.
- Transaction boundaries, rollback behavior, duplicate prevention, and idempotency are unverified.
- The evidence covers one order, one item, four header partners, and two schedule lines; it does not establish behavior for all optional fields or record variations.

## Tests

The Phase 3A.2 tests pin all four evidence hashes and record counts; validate their strict OData V2 envelopes; reconcile entity types and returned fields with metadata; parse entity keys; verify relationship identity; check partner codes without semantic inference; check decimal/date/null/unit/ETag representations; enforce the 30-entry classification matrix; and verify that GET serialization did not alter the write mapper.

Targeted suite: **39 tests passed**. Full repository suite: **123 tests passed**.

## Files changed

- `src/sap_mapping/odata_runtime.py`
- `schemas/sap/core_mapping_contracts.json`
- `schemas/sap/sales_order_runtime_response.schema.json`
- `schemas/sap/sales_order_runtime_evidence_contract.json`
- `tests/test_phase3a2_sales_order_runtime.py`
- `tests/snapshots/phase2c_core_payloads.json`
- `reports/phase2c_mapping_coverage.json`
- `reports/phase3a2_sales_order_runtime_validation.md`

## Recommendations

1. **Read-only SALES_ORDER connector development: GO.** The captured GET contract is sufficient to implement offline response parsing and read-only request construction against the evidenced external service/entity paths, subject to later environment-specific authentication and connectivity configuration.
2. **Write-capable SALES_ORDER connector development: NO-GO.** Metadata plus GET captures do not establish a safe executable write contract.
3. **Controlled write pilot readiness: NO-GO.** Require explicit non-production authorization and deterministic evidence for POST/deep insert, partner roles, write serialization, CSRF/authentication, transaction handling, and idempotency before a pilot.
