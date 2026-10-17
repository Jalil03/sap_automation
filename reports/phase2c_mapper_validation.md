# The Core Flow Is Ready for Read-Only Metadata Validation, Not SAP Execution

## Executive summary

- Phase 2C established strict local contracts for all six Phase 2B mappers and all **138 canonical field paths** in scope. Coverage is 103 mapped, 14 intentionally ignored, 7 runtime-resolved, and 14 unsupported.
- The 129 in-scope canonical objects validate deterministically into **1 `EXECUTION_READY`**, **1 `RUNTIME_BINDING_REQUIRED`**, and **127 `BLOCKED`** results. Canonical readiness is never upgraded by the mapper.
- The representative S4615 chain now resolves as: sales order `EXECUTION_READY` → outbound delivery `RUNTIME_BINDING_REQUIRED` → billing `BLOCKED`. Billing is blocked because installment-payment content has no verified writable local field contract.
- **GO for narrowly scoped, read-only live SAP contract validation. NO-GO for connector development, writes, or Phase 3 execution.** The next authorized activity should inspect service metadata and the BAPI signature only; it must not create or change business data.

No SAP connection was made. No connector, transport, authentication, CSRF, commit, retry, or execution logic was implemented.

## Scope and source authority

Phase 2C used:

- the six Phase 2B mapper implementations under `src/sap_mapping/`;
- `mappings/sap/interface_registry.yaml` for preferred-interface identity;
- the canonical schemas and `data/validated/canonical_objects.json`;
- `schemas/sap/core_mapping_contracts.json` as the new local field-disposition contract; and
- strict local JSON Schemas for payload bodies and runtime bindings.

The contracts are deliberately labeled `LOCAL_PHASE2B_MAPPING_CONTRACT_ONLY` with `live_sap_metadata_validated: false`. They validate internal consistency; they do not claim that a live SAP system exposes these exact fields, entity sets, navigation properties, operations, or BAPI parameters.

Phase 2C added no new SAP interface capability. It formalized the existing Phase 2B targets and removed the prior non-contract `CanonicalSalesArea` fallback. A malformed sales-area value now fails deterministically rather than producing a fabricated payload field.

## Runtime states

The strict validator emits exactly three states:

| State | Meaning |
|---|---|
| `EXECUTION_READY` | Canonical object is READY, the local payload schema passes, mandatory fields are present, no unsupported populated values exist, and no runtime substitution remains. This is still not authorization to execute. |
| `RUNTIME_BINDING_REQUIRED` | The local payload is valid, but a prior SAP document identifier or semantic relative date must be resolved at runtime. |
| `BLOCKED` | Canonical readiness is BLOCKED or strict validation found placeholders, critical unresolved dependencies, missing mandatory fields, unsupported populated fields, invalid types, invalid payload fields, or invalid bindings. |

Strict validation is exposed by `validate_runtime_contract`. It returns stable structured issue codes and optionally raises `PayloadValidationError` through `raise_on_blocked=True`. Phase 2B structural mapping remains available, but only the Phase 2C result should govern any future runtime handoff.

## Full-dataset validation result

All 129 objects in the six-type writable core scope were processed offline.

| Canonical type | Objects | EXECUTION_READY | RUNTIME_BINDING_REQUIRED | BLOCKED |
|---|---:|---:|---:|---:|
| BUSINESS_PARTNER | 3 | 0 | 0 | 3 |
| MATERIAL | 4 | 0 | 0 | 4 |
| SALES_ORDER | 57 | 1 | 0 | 56 |
| PRICING_CONDITION | 14 | 0 | 0 | 14 |
| OUTBOUND_DELIVERY | 21 | 0 | 1 | 20 |
| BILLING | 30 | 0 | 0 | 30 |
| **Total** | **129** | **1** | **1** | **127** |

The high BLOCKED count is expected: 126 source objects were already canonically BLOCKED. Phase 2C also blocks the one READY billing object because it contains a populated `installment_payments` structure for which the local mapper has no verified writable field.

Issue occurrences across the structural audit are diagnostic counts, not unique objects:

| Issue code | Occurrences |
|---|---:|
| `UNRESOLVED_PLACEHOLDER` | 270 |
| `UNRESOLVED_CRITICAL_DEPENDENCY` | 58 |
| `MISSING_REQUIRED_MAPPING` | 32 |
| `PAYLOAD_SCHEMA_INVALID` | 28 |
| `MISSING_MANDATORY_FIELD` | 23 |
| `UNSUPPORTED_FIELD_POPULATED` | 23 |
| `BINDING_SCHEMA_INVALID` | 22 |
| `MISSING_RUNTIME_BINDING` | 7 |
| `UNSUPPORTED_RUNTIME_BINDING` | 3 |

Blocked fixtures may carry several issue codes at once. This is intentional and preserves all actionable defects in stable order.

## Sales-order to billing runtime contract

The representative S4615 installment-payment chain demonstrates the state model:

1. `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT`
   - state: `EXECUTION_READY`
   - local payload schema: valid
   - runtime substitutions: none
2. `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_OUTBOUND_DELIVERY_INSTALLMENT`
   - state: `RUNTIME_BINDING_REQUIRED`
   - binding: `ReferenceSDDocument` must come from the sales-order result identified by the exact canonical target ID
   - semantic selection date remains deferred rather than converted to an invented absolute date
3. `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_BILLING_INSTALLMENT`
   - state: `BLOCKED`
   - binding: `ReferenceSDDocument` points to the outbound-delivery result
   - blocker: populated `installment_payments` is unsupported by the current local write contract

Runtime bindings are strict objects containing the target canonical ID/type, dependency relation/status, target SAP field, and original source phrase. Binding validation checks schema, declared relation/type/field combinations, target existence, and target type. It never substitutes a canonical ID as an SAP document number.

## Field-level mapping coverage

| Object type | Fields | Mapped | Intentionally ignored | Runtime-resolved | Unsupported |
|---|---:|---:|---:|---:|---:|
| BUSINESS_PARTNER | 19 | 19 | 0 | 0 | 0 |
| MATERIAL | 16 | 15 | 0 | 0 | 1 |
| SALES_ORDER | 23 | 19 | 2 | 1 | 1 |
| PRICING_CONDITION | 36 | 25 | 5 | 2 | 4 |
| OUTBOUND_DELIVERY | 19 | 12 | 1 | 2 | 4 |
| BILLING | 25 | 13 | 6 | 2 | 4 |
| **Total** | **138** | **103** | **14** | **7** | **14** |

The machine-readable report at `reports/phase2c_mapping_coverage.json` lists every canonical field path, its one and only disposition, target SAP path where mapped, and reason where ignored or unsupported. Tests compare this inventory directly with each canonical schema, including nested item, key-combination, and scale fields.

Material `sales_text`; sales-order `pricing_elements`; several pricing limit/adjustment fields; outbound-delivery gross-weight/header warehouse fields; and billing-plan/down-payment/installment structures remain unsupported. Populating one of these fields on a candidate runtime object produces `UNSUPPORTED_FIELD_POPULATED` and state `BLOCKED`.

Observed state fields—such as processing status, billing status, FI/CO evidence, and system representations—are intentionally ignored because they are not write inputs. Their classification is explicit and does not silently imply interface support.

## Strict payload validation

`schemas/sap/payloads.schema.json` defines closed local payload schemas for all six mapper outputs:

- all payload objects reject unknown properties;
- nested objects and arrays reject unknown properties;
- mapped values have explicit string, number, boolean, array, and object types;
- locally mandatory structures and fields are required;
- pricing requires either a direct rate or scale rows; and
- BAPI X/update fields accept only `X`.

`schemas/sap/runtime_binding.schema.json` similarly rejects null target IDs, unresolved binding status, unknown properties, and invalid types.

The validator also applies the canonical object schema before payload validation. Consequently, a malformed canonical quantity produces both a canonical-schema issue and a payload-schema issue, while an extra payload property is rejected by the closed SAP payload schema.

## Deterministic snapshots

`tests/snapshots/phase2c_core_payloads.json` contains stable reviewed snapshots for:

- blocked Business Partner, Material, and Pricing Condition structural fixtures;
- the READY S4615 sales order;
- the dependent READY outbound delivery; and
- the READY but runtime-blocked billing object.

Snapshots retain exact interface evidence, payload bodies, deferred values, runtime bindings, runtime state, and sorted validation issues. `scripts/build_phase2c_artifacts.py --check` fails if either the snapshots or coverage report is missing or stale.

## Deterministic failure behavior

Tests verify stable failure for:

- unresolved placeholders;
- unresolved critical dependencies;
- missing mandatory canonical fields;
- invalid canonical and payload value types;
- unknown/invented payload fields;
- populated unsupported canonical fields;
- missing or invalid runtime bindings;
- binding targets absent from the supplied canonical object index;
- attempts to map types outside the six-type writable core; and
- BLOCKED objects used outside explicit fixture mode.

Issues are sorted by code, path, and message, so unchanged inputs produce byte-stable validation and snapshots.

## Test results

Phase 2C adds 11 deterministic tests. The complete repository suite passes **107 tests**:

- 77 Phase 1 tests;
- 7 Phase 2A tests;
- 12 Phase 2B tests; and
- 11 Phase 2C tests.

No source PDF, Phase 1 staged output, canonical validated object, interface inventory, or interface registry entry was modified.

## Recommendation: GO for read-only live contract validation

**GO**, with a narrow scope, for a separately authorized read-only live SAP contract-validation phase. The purpose is to compare the local contracts with actual metadata, not to test business execution.

Allowed validation should be limited to:

- reading OData `$metadata` for the five preferred services;
- reading the installed signature/metadata for `BAPI_MATERIAL_SAVEDATA` without invoking it;
- verifying service versions, entity sets, property names/types, navigation properties, supported actions, nullability, lengths, and required fields;
- recording mismatches as contract changes with regression tests; and
- confirming that the selected technical registrations correspond to the external services recorded in the registry.

The following remain **NO-GO**:

- creating, changing, simulating, or posting SAP business data;
- invoking the BAPI or any OData action/entity mutation;
- CSRF-token acquisition for writes;
- connector/orchestration implementation;
- transaction, commit, rollback, retry, or idempotency logic; and
- Phase 3 execution work.

Read-only validation should stop and report if metadata access cannot be proven non-mutating. Phase 3 remains out of scope.

## Files generated or changed

- `schemas/sap/core_mapping_contracts.json`
- `schemas/sap/payloads.schema.json`
- `schemas/sap/runtime_binding.schema.json`
- `src/sap_mapping/contracts.py`
- `src/sap_mapping/validation.py`
- `src/sap_mapping/errors.py`
- `src/sap_mapping/__init__.py`
- `src/sap_mapping/odata.py`
- `scripts/build_phase2c_artifacts.py`
- `reports/phase2c_mapping_coverage.json`
- `tests/snapshots/phase2c_core_payloads.json`
- `tests/test_phase2c_mapper_validation.py`
- `reports/phase2c_mapper_validation.md`
- `README.md`
