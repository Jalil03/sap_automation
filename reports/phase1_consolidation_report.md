# Phase 1 consolidation passed all publication gates

## Executive summary

Phase 1 consolidation completed successfully and the canonical dataset was published to `data/validated/canonical_objects.json`.

- Five staged normalized datasets containing 203 objects were consolidated into 201 validated objects.
- Two deterministic duplicates were merged: sales organization `1010` and sales division `00`, each preserving S4600 and S4650 provenance.
- All 201 objects conform to their current schemas; all 319 dependency edges pass integrity checks.
- 26 objects are READY and 175 are BLOCKED. BLOCKED is an expected canonical state, not a validation failure: unresolved participant values and dependencies remain explicit.
- All 13 consolidation gates and all 77 repository tests pass.
- The S4600 customer-return delivery issue remains open and unchanged.

**Recommendation: GO for Phase 2 SAP-specific mapper design, with a mandatory rule that only READY objects may be considered executable.** This is not authorization to implement Phase 2 or connect to SAP.

## 1. Scope and source verification

The consolidation loaded the staged normalized datasets for all completed courses:

| Course | Staged objects |
|---|---:|
| S4600 | 54 |
| S4610 | 21 |
| S4615 | 48 |
| S4620 | 51 |
| S4650 | 29 |
| **Total input** | **203** |

All five documents were resolved through `docs/manifests/documents.json`; their filenames and SHA-256 checksums were verified before consolidation. The normalized staged files were hashed before processing and checked again before publication. No staged dataset changed.

No source PDF was modified. No SAP, BAPI, RFC, OData, IDoc, or SAP GUI connection was attempted.

## 2. Consolidated object counts

### By classification

| Classification | Count | Share |
|---|---:|---:|
| CUSTOMIZING | 45 | 22.4% |
| MASTER_DATA | 24 | 11.9% |
| REFERENCE_DATA | 9 | 4.5% |
| TRANSACTION | 123 | 61.2% |
| **Total** | **201** | **100.0%** |

### By object type

| Object type | Count | Object type | Count |
|---|---:|---|---:|
| ACCESS_SEQUENCE | 2 | ACCOUNT_DETERMINATION | 1 |
| BILLING | 30 | BUSINESS_PARTNER | 3 |
| COMPANY_CODE | 1 | CONDITION_CONTRACT | 1 |
| CONDITION_TABLE | 4 | CONDITION_TYPE | 5 |
| COPY_CONTROL | 8 | CREDIT_MEMO_REQUEST | 1 |
| CUSTOMER_HIERARCHY | 1 | CUSTOMER_MATERIAL_INFO | 1 |
| DISTRIBUTION_CHANNEL | 2 | EXTENSION_CONFIGURATION | 2 |
| GOODS_ISSUE | 4 | INBOUND_DELIVERY | 2 |
| INQUIRY | 1 | MATERIAL | 4 |
| OUTBOUND_DELIVERY | 21 | OUTPUT_DETERMINATION | 3 |
| PAYMENT_REFERENCE | 2 | PLANT | 1 |
| PRICING_CONDITION | 14 | PRICING_PROCEDURE | 3 |
| PRICING_PROCEDURE_DETERMINATION | 3 | PURCHASE_ORDER_REFERENCE | 2 |
| QUOTATION | 1 | RETURN_ORDER | 1 |
| SALES_AREA | 3 | SALES_DIVISION | 2 |
| SALES_ORDER | 57 | SALES_ORGANIZATION | 1 |
| SETTLEMENT_DOCUMENT | 3 | SHARED_MASTER_DATA_ASSIGNMENT | 1 |
| SHIPPING_POINT | 3 | STORAGE_LOCATION | 2 |
| TEXT_DETERMINATION | 2 | WAREHOUSE_NUMBER | 1 |
| WAREHOUSE_TASK | 2 | **Total** | **201** |

## 3. Deduplication results

Deduplication was limited to stable, non-placeholder canonical business keys. Transaction descriptions, similar labels, relative references, and unresolved participant codes were not treated as identity.

### Deterministic merges

| Identity | Surviving object | Source objects | Result |
|---|---|---:|---|
| SALES_ORGANIZATION `1010` | `S4600_SHARED_SALES_ORGANIZATION_1010` | 2 | Merged S4600/S4650 provenance; retained explicit company code 1010 |
| SALES_DIVISION `00` | `S4600_SHARED_SALES_DIVISION_00` | 2 | Merged S4600/S4650 provenance |

- Merge groups: 2.
- Duplicate input objects removed: 2.
- Conflicting deterministic identities: 0.
- Rejected merges due to field conflicts: 0.
- Duplicate object IDs after consolidation: 0.

The surviving cross-course objects have `scenario_id=null` because they represent one canonical identity supported by multiple source scenarios. Each source scenario remains preserved in provenance and global lineage.

### Explicitly unmerged candidate

`S4600_CH3_EX5_SHIPPING_POINT_Z0-GROUP` and `S4610_CH2_EX3_SHIPPING_POINT_Z0-GROUP` share symbolic key `SHIPPING_POINT|Z0##`. They remain separate because `##` is unresolved; identical placeholder text does not prove identical deployed identity. The decision is recorded as `KEEP_SEPARATE_SYMBOLIC_PLACEHOLDER_IDENTITY`.

No transaction objects were merged without a printed, deterministic business identifier.

## 4. Provenance and global lineage

Every validated object retains:

- course code;
- original source filename;
- physical page;
- section type;
- chapter/exercise and scenario when available;
- original source term and excerpt.

`metadata/lineage/global_lineage.json` maps each validated object to all staged source object IDs and source courses. The two merged objects contain provenance from both S4600 and S4650. Unmerged objects preserve their original IDs and provenance unchanged.

The lineage artifact also records:

- source-document checksum verification;
- normalized-stage SHA-256 hashes;
- deterministic merges;
- symbolic duplicate candidates;
- cross-document dependency resolutions;
- open issues;
- publication-gate results.

## 5. READY, BLOCKED, and placeholders

| Readiness | Count | Share |
|---|---:|---:|
| READY | 26 | 12.9% |
| BLOCKED | 175 | 87.1% |

- Unresolved placeholder occurrences: 355.
- Objects containing tracked placeholders: 149, or 74.1% of the dataset.
- READY objects with blocking reasons: 0.
- READY objects with unresolved mandatory placeholders: 0.
- BLOCKED objects without a structured reason: 0.
- Non-VALIDATED objects in the published dataset: 0.

The high BLOCKED share is expected for participant course data containing `##`, omitted generated document numbers, and prior-step references. Consolidation did not treat missing participant values as null business facts or resolve them from similar-looking identifiers.

Lifecycle and readiness remain independent: all published objects are structurally `VALIDATED`, while objects that cannot safely proceed downstream remain `BLOCKED`.

## 6. Global dependency graph

| Dependency status | Count | Share |
|---|---:|---:|
| RESOLVED | 169 | 53.0% |
| UNRESOLVED | 150 | 47.0% |
| **Total** | **319** | **100.0%** |

- Graph nodes: 201.
- Resolved edges with a missing target: 0.
- Resolved edges with a target-type mismatch: 0.
- Unresolved edges carrying a fabricated target ID: 0.

Aliases produced by the two deterministic merges were applied to all dependency targets.

One new cross-document resolution was allowed:

```text
S4600_SHARED_SALES_ORGANIZATION_1010
  --ASSIGNED_TO-->
S4615_SHARED_COMPANY_CODE_1010
```

The resolution is based on the exact, non-placeholder `company_code=1010` value on the sales organization and the unique company-code object with code `1010`. No participant placeholder or inferred document number was used.

All other unresolved relationships remain explicit. Similar phrases such as “document created in the previous step,” unprinted quotation/order/delivery identifiers, and course-specific participant codes were not guessed.

## 7. Cross-document conflicts and ambiguities

### Deterministic field conflicts

None. The two merged identity groups contained compatible fields: equal values or a non-null value enriching a null field.

### Ambiguous identity

The symbolic shipping point `Z0##` appears in S4600 and S4610. Because the participant suffix is unresolved, consolidation preserves two explicit objects and records the candidate rather than silently merging it.

### Transaction identity

Course exercises frequently omit generated SAP document numbers. Similar order, delivery, and billing scenarios therefore remain separate unless an existing staged dependency already provides an exact target. Customer references alone are not globally unique enough to establish transaction identity.

### Terminology

- Forbidden canonical key `division`: 0 occurrences.
- `secteur d'activité` remains normalized as `sales_division`.
- Logistical French `division` remains normalized as `plant` or the more specific field already established by the source contract.
- Schema/type/classification drift: 0 detected.

## 8. Open issues

1. **S4600 customer-return delivery direction remains unresolved.** Object `S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER` remains `UNRESOLVED_CARRIED_FORWARD`. S4610, S4615, S4620, and S4650 provide no explicit evidence sufficient to resolve it.
2. **175 objects remain BLOCKED.** Phase 2 must not map these as executable records until their structured blocking reasons are resolved.
3. **150 dependencies remain unresolved.** These are retained intentionally; mapper logic must preserve or reject them according to readiness rather than inventing foreign keys.
4. **The `Z0##` cross-course candidate remains separate.** It may be reviewed only after an explicit participant mapping supplies a non-placeholder identity.

These issues do not invalidate publication because they are represented honestly, are covered by readiness/dependency metadata, and did not break a hard consistency gate.

## 9. Global consistency checks

| Gate | Result | Evidence |
|---|---|---|
| Manifest and PDF checksum verification | PASS | Five logical sources resolved and verified |
| Staged schema validation | PASS | 203/203 input objects valid |
| Input object-ID uniqueness | PASS | 0 duplicate IDs |
| Deterministic identity resolution | PASS | 2 compatible merge groups |
| Conflicting field values | PASS | 0 deterministic conflicts |
| Published schema validation | PASS | 201/201 objects valid |
| Resolved-reference integrity | PASS | 169/169 resolved edges have valid typed targets |
| Placeholder integrity | PASS | 355 occurrences tracked; no missing metadata |
| Terminology consistency | PASS | 0 forbidden `division` keys |
| Lifecycle/readiness consistency | PASS | 0 status-rule violations |
| Return-delivery issue preserved | PASS | Still unresolved; no fabricated resolution |
| Prior-stage immutability | PASS | All five normalized hashes unchanged |
| Publication gate | PASS | Validated dataset published only after prior gates passed |

## 10. Schema and test results

- Published schema-valid objects: 201/201.
- Published schema-invalid objects: 0.
- Repository tests run: 77.
- Passed: 77.
- Failed/errors: 0.
- Consolidation rerun: byte-identical for the validated dataset, global graph, and global lineage.
- Staged datasets after rerun: byte-identical to their pre-consolidation hashes.

Command:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

The consolidation tests cover counts, classifications, schema validity, complete provenance, deterministic merge behavior, symbolic non-merge behavior, placeholders/readiness, dependency integrity, exact cross-document resolution, terminology, the open return issue, publication gates, stage immutability, and deterministic reruns.

## 11. Files generated or updated

Required consolidation outputs:

- `data/validated/canonical_objects.json`
- `metadata/dependencies/global_dependency_graph.json`
- `metadata/lineage/global_lineage.json`
- `reports/phase1_consolidation_report.md`

Implementation and validation:

- `scripts/consolidate_phase1.py`
- `tests/test_phase1_consolidation.py`
- Stage 3–5 publication guards were updated so they continue to forbid course-specific publication while allowing this separately authorized global dataset.

No Phase 2 mapper or SAP connector was created.

## 12. Final GO / NO-GO for Phase 2 SAP-specific mapper

**GO for Phase 2 mapper design and implementation under a separate authorization.** The canonical contracts, classifications, provenance, dependency model, placeholder semantics, lifecycle/readiness rules, and global dataset passed every Phase 1 publication gate.

Phase 2 must enforce these entry conditions:

1. map only objects whose `readiness_status` is `READY` for execution-oriented outputs;
2. never convert unresolved `##` values into SAP keys without an explicit non-null mapping;
3. reject or quarantine unresolved critical dependencies;
4. preserve lineage back to every contributing course/page;
5. retain the unresolved S4600 return-delivery issue as a mapper exception, not a guessed direction;
6. treat the two `Z0##` objects as distinct until identity is explicitly resolved;
7. keep SAP connectivity and execution outside mapper validation.

This GO decision covers mapper readiness only. It is **NO-GO for SAP execution or connector use** until Phase 2 is separately implemented, validated, and authorized.
