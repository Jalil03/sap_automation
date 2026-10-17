# Phase 2B Resolved Writable Core Mapper Report

## Outcome

Phase 2B implemented deterministic, offline canonical-to-SAP payload mappers for the six authorized writable core types. The mapper package contains no SAP connection, HTTP/RFC client, credentials, transport handling, retry logic, commit handling, or execution code.

The Phase 2A registry remains the source of truth at runtime. Each mapping result embeds the registry's preferred interface record, including its exact technical name, external OData name/version when applicable, operation, and evidence basis.

## Implemented scope

| Canonical type | Preferred classification | Exact interface | Mapper output |
|---|---|---|---|
| BUSINESS_PARTNER | ODATA | `ZAPI_BUSINESS_PARTNER` / external `API_BUSINESS_PARTNER` v1 | Business-partner header, roles, addresses, customer/company-code data, sales areas, tax classifications, partner functions, and fax data |
| MATERIAL | STANDARD_BAPI | `BAPI_MATERIAL_SAVEDATA` | BAPI structures and X/update structures; deterministic request per plant context |
| SALES_ORDER | ODATA | `ZAPI_SALES_ORDER_SRV` / external `API_SALES_ORDER_SRV` v1 | Sales header, organizational data, partners, customer reference, requested date, payment terms, and items |
| PRICING_CONDITION | ODATA | `ZSD_PRICING_CONDITIONRECORD_SRV` / external `SD_PRICING_CONDITIONRECORD_SRV` v1 | Condition header, supported key-combination fields, rate/unit, validity dates, and quantity/value scales |
| OUTBOUND_DELIVERY | ODATA | `ZAPI_OUTBOUND_DELIVERY_SRV` / external `API_OUTBOUND_DELIVERY_SRV` v2 | Delivery header/items plus explicit sales-order runtime binding |
| BILLING | ODATA | `ZAPI_BILLING_DOCUMENT_SRV` / external `API_BILLING_DOCUMENT_SRV` v1 | Billing header/items plus explicit delivery/order runtime binding |

No mapper exists for `LOOKUP_ONLY`, `NO_EXECUTION_REQUIRED`, or unresolved types. Requests for types such as `COMPANY_CODE`, `PAYMENT_REFERENCE`, or `COPY_CONTROL` fail with `UnsupportedObjectTypeError`.

## Mapping contract

The entry point is `src.sap_mapping.map_canonical_object`.

Each result contains:

- canonical object/scenario identity and provenance;
- the exact preferred interface loaded from `mappings/sap/interface_registry.yaml`;
- protocol (`ODATA` or `BAPI`);
- one or more payload bodies;
- `payload_state`: `CONCRETE`, `TEMPLATE`, or `STRUCTURAL_FIXTURE`;
- `execution_ready`, which is true only for a concrete READY mapping;
- explicit `runtime_bindings` for prior-document references;
- explicit `deferred_values` for semantic relative dates;
- `missing_required_mappings`; and
- meaningful `retained_nonpayload_fields` that are deliberately kept outside the SAP write body.

Null canonical values are omitted. Values are never defaulted or invented. Relative dates remain semantic deferred values. A dependency such as “document created in the previous step” becomes a runtime binding to its canonical target object and never a fabricated SAP document number.

`execution_ready` is a mapper-level structural result only. It does not assert SAP activation, authorization, field metadata compatibility, or permission to execute.

## Readiness enforcement

- A `READY` canonical object can be mapped normally.
- A `BLOCKED` object raises `BlockedObjectError` by default.
- A `BLOCKED` object can be inspected only with `structural_fixture=True`; its output is always `STRUCTURAL_FIXTURE` and `execution_ready: false`.
- A READY result with a runtime dependency, relative-date resolution, or required-field gap is a non-executable `TEMPLATE`.

This preserves the independence of canonical lifecycle/readiness and prevents Phase 2B from bypassing Phase 1 blocking reasons.

## Validated-dataset dry run

All 129 canonical objects in the authorized six-type scope were mapped offline without exceptions under the readiness rules.

| Type | Objects |
|---|---:|
| BUSINESS_PARTNER | 3 |
| MATERIAL | 4 |
| SALES_ORDER | 57 |
| PRICING_CONDITION | 14 |
| OUTBOUND_DELIVERY | 21 |
| BILLING | 30 |
| **Total** | **129** |

Output states were:

- 126 `STRUCTURAL_FIXTURE` results for BLOCKED canonical objects;
- 1 `CONCRETE` result for the READY S4615 installment-payment sales order; and
- 2 `TEMPLATE` results for its READY outbound delivery and billing document.

The delivery and billing records remain templates because their SAP document identifiers must be supplied by results of earlier flow steps. The mapper records those bindings but does not resolve or execute them. The delivery also retains its relative scheduling date for future runtime resolution.

Across the full structural dry run, 44 objects contained explicit runtime document bindings and 63 contained semantic deferred values. Twenty-six fixture mappings exposed missing fields required by their mapper contracts; this is expected for BLOCKED source objects and does not change their canonical validation state.

## BAPI/OData separation

OData field mapping is isolated in `src/sap_mapping/odata.py`. BAPI structure mapping is isolated in `src/sap_mapping/bapi.py`. Registry resolution, common value handling, and orchestration-free dispatch are separate modules.

There is deliberately no connector module. The code imports no HTTP, socket, SAP GUI, RFC client, or SAP SDK package. BAPI output is data only; it does not invoke the function or issue a commit.

## Data preservation and known limits

- Original canonical objects are not mutated.
- Provenance is copied into every mapping result.
- Business-state fields that are not SAP write inputs—such as processing status, billing status, FI/CO evidence, system representations, and pricing source-operation metadata—are retained explicitly outside the payload instead of silently discarded.
- The Phase 2A workbooks establish exact interface names but do not contain OData entity metadata or BAPI parameter definitions. Phase 2B therefore establishes the offline field contract; service metadata/function signatures must be independently validated before any Phase 3 connector is considered.
- OData navigation/deep-insert support, service activation, authorizations, accepted date formats, and transaction behavior were not tested.
- Material descriptions may require language-specific BAPI handling when runtime signature validation is performed; no language value is inferred.
- Pricing-condition entity-set/condition-table routing must be confirmed against actual service metadata. No condition table is invented from a key combination.
- The Phase 2A registry field `mapper_implemented: false` is retained as historical audit metadata describing the state when that registry was generated; it is not rewritten by Phase 2B.
- The open S4600 return-delivery issue is outside this mapper scope and remains unchanged.

## Tests

Phase 2B adds deterministic tests covering:

- exact six-type scope;
- preferred registry interface selection;
- OData and BAPI dispatch;
- Business Partner deep structures;
- Material plant contexts and X/update flags;
- Sales Order item mapping;
- pricing quantity scales;
- prior-document binding without identifier fabrication;
- BLOCKED fixture enforcement;
- rejection of lookup/no-execution/unresolved types;
- deterministic output and input immutability;
- explicit retention of non-payload business state; and
- absence of connector/network code.

The focused Phase 2B suite passes 12 tests. The complete repository suite passes 96 tests.

## Phase 3 gate

Phase 2B core mapper development is complete for the authorized scope. **Phase 3 is NO-GO at this point** and was not started.

Before Phase 3, a separate authorization and technical validation must confirm:

1. OData service metadata, entity sets, navigation properties, actions, and v1/v2 compatibility;
2. the installed `BAPI_MATERIAL_SAVEDATA` signature and language/plant semantics;
3. authentication, authorization, CSRF, transaction, idempotency, retry, and commit policies;
4. runtime substitution of dependency bindings and relative dates;
5. a policy that only concrete `execution_ready: true` results can reach a connector; and
6. non-production integration tests with rollback and audit controls.

No SAP connection or transport/execution code was created.

## Files changed

- `src/sap_mapping/__init__.py`
- `src/sap_mapping/errors.py`
- `src/sap_mapping/registry.py`
- `src/sap_mapping/common.py`
- `src/sap_mapping/odata.py`
- `src/sap_mapping/bapi.py`
- `src/sap_mapping/core.py`
- `tests/test_phase2b_core_mappers.py`
- `reports/phase2b_core_mapper_report.md`
- `README.md`
