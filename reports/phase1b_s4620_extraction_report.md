# Phase 1B Stage 4 — S4620 extraction report

## 1. Outcome

**GO for a separately authorized S4650 stage.** S4620 was resolved through the manifest, checksum-verified, parsed across all 351 pages, and staged without SAP access or publication to `data/validated/`. The run produced 51 extracted and 51 normalized objects. All 102 layer records conform to the current schemas, object IDs and outputs are deterministic, and all 56 repository tests pass.

This stage stops at S4620. It did not process S4650, alter a source PDF, connect to SAP, or modify S4600/S4610/S4615 artifacts.

## 2. Source verification and scope

- Logical source: `S4620`, resolved through `docs/manifests/documents.json`.
- Physical source: `docs/source/S4620_FR_Col12_ILT_FV_Inst_A4.pdf`.
- Manifest and computed SHA-256: `8433ee1c05da24062bf849672b66bd3857e71608198b8ca127fc5a8500f2bae1`.
- Pages parsed: 351/351.
- Exercise/solution pairs detected and verified: 27/27.
- Physical exercise start pages: 19, 31, 49, 51, 57, 63, 83, 89, 93, 127, 133, 147, 151, 155, 173, 183, 189, 217, 231, 259, 281, 295, 301, 313, 317, 323, and 329.
- Physical solution start pages: 23, 32, 50, 53, 59, 66, 85, 91, 98, 129, 135, 148, 152, 156, 177, 185, 192, 223, 233, 262, 283, 297, 303, 314, 319, 325, and 330.

The parser checked every page. Canonical objects were created only for actual condition/configuration records, saved exercise datasets, explicit dependencies, and settlement results. Theory, UI navigation, reporting definitions, and out-of-coverage delivery/billing work were not promoted.

## 3. Canonical object counts

| Object type | Coverage role | Count |
|---|---|---:|
| CONDITION_TYPE | PRIMARY | 5 |
| CONDITION_TABLE | PRIMARY | 4 |
| ACCESS_SEQUENCE | PRIMARY | 2 |
| PRICING_PROCEDURE | PRIMARY | 3 |
| PRICING_PROCEDURE_DETERMINATION | PRIMARY | 3 |
| PRICING_CONDITION | PRIMARY | 11 |
| CUSTOMER_HIERARCHY | PRIMARY | 1 |
| CONDITION_CONTRACT | PRIMARY | 1 |
| SETTLEMENT_DOCUMENT | PRIMARY | 3 |
| SALES_ORDER | SECONDARY | 18 |
| COMPANY_CODE | REFERENCE_ONLY | 0 |
| **Total** |  | **51** |

Classification totals are 17 `CUSTOMIZING`, 13 `MASTER_DATA`, and 21 `TRANSACTION` objects. No company-code object was promoted because S4620 supplies no qualifying independent company-code instance or required company-code dependency.

## 4. Extracted and normalized layers

- Extracted objects: 51 with `lifecycle_status=EXTRACTED`.
- Normalized objects: 51 with `lifecycle_status=VALIDATED`.
- Extracted-to-normalized grain: one-to-one.
- Duplicate object IDs: 0.
- Solution-only duplicate objects: 0.

Canonical English field names are used in normalized data. French source terms and concise source excerpts remain in lineage. `sales_division` is used for `secteur d'activité`; forbidden canonical `division` is not used.

## 5. Pricing conditions and scales

The 11 pricing-condition records include:

- PR00 material price: 280 EUR for `P620-1##`.
- PR00 customer/material quantity scale: 1/10/100 PC at 250/240/230 EUR.
- K007 customer value scale: thresholds 100/1,000/5,000 EUR at 2/3/5 percent, with explicit `DISCOUNT` semantics.
- ZF## freight: 10 EUR for sales organization 1010, EXW, destination DE.
- Two future-year PR00 article records copied with reference and then increased by 5 percent.
- One PR00 customer/material copy from `C620-A##` to `C620-B##`.
- ZW## gross-weight scale: 0/0.5/1/2/5/10/20/30.001 KG at 8/10/12/14/16/20/30/0 EUR.
- K005 customer/article discount: -100 EUR, initially limited to one order, then 15 PC, and finally deleted after the test.
- HI02 hierarchy/material discount: 50 EUR for node `C620-ZE` and `P620-2##`.
- KA00 sales-deal discount: 10 percent for `C620-B##` and `P620-2##`.

Quantity, value, and gross-weight scale bases remain distinct. Percent values shown unsigned in the source are retained as source values with `calculation_semantics=DISCOUNT`; no unprinted sign was fabricated.

## 6. Condition technique and pricing-procedure determination

The standard technique chain is explicit:

```text
CONDITION_TABLE 305 / 306 / 304
  -> ACCESS_SEQUENCE PR02
    -> CONDITION_TYPE PR00
      -> PRICING_PROCEDURE RVAA01
```

The participant model is also explicit:

```text
CONDITION_TABLE 7##
  -> ACCESS_SEQUENCE ZA##
    -> CONDITION_TYPE ZF## and ZW##
      -> PRICING_PROCEDURE Z##PRC
        -> PRICING_PROCEDURE_DETERMINATION 1010/10/00 + A + <YY>
```

`Z##PRC` preserves the source ordering of ZW## immediately before ZF## and the Exercise 16 exclusion comparison: group Z1##/ZW## suppresses group Z2##/ZF## under comparison procedure D.

For settlement, document schema group `0S` determines pricing procedure `A10005`. It is modeled as a separate `SETTLEMENT_DOCUMENT` determination context, rather than being forced into the sales-area key used for sales documents.

## 7. Customer hierarchy, condition contract, and settlements

The TOPCO hierarchy retains nodes `C620-ZE`, `C620-ZEW`, and participant customer `C620-A##`, plus sales area 1010/10/00. HI02 depends explicitly on that hierarchy and the related sales order depends on both.

The condition contract preserves:

- type `0S01_SALES_REBATE`;
- customer `C620-B##` and material `P620-3##` selection criteria;
- current-year relative validity;
- sales area 1010/10/00;
- RES1 at 10 EUR/PC and REA1 at -10 EUR/PC;
- annual settlement calendar AJ;
- read-only dependencies to the two Exercise 22 business-volume orders.

Three settlement documents were extracted:

| Scenario | Type | Amount | Dependency |
|---|---|---:|---|
| Exercise 24 | DELTA_ACCRUAL | 200 EUR | Condition contract |
| Exercise 25 | PARTIAL_SETTLEMENT_CREDIT | 200 EUR | Contract and delta accrual |
| Exercise 27 | FINAL_SETTLEMENT_CREDIT | 100 EUR | Contract, partial settlement, and Exercise 26 business volume |

Generated contract, accounting, credit-memo, delivery, billing, and sales-document numbers left blank in the course remain null. Canonical source-based object IDs are not presented as SAP document numbers.

## 8. Schema validation

- Normalized objects valid: 51/51.
- Extracted objects valid: 51/51.
- Invalid objects: 0.
- Validator: Draft 2020-12 schemas through the repository schema registry.

Every normalized object contains classification, deterministic object/scenario IDs, complete provenance, independent lifecycle/readiness status, dependencies, placeholders, validation metadata, confidence, and typed business data.

## 9. READY, BLOCKED, and placeholders

| Readiness | Count |
|---|---:|
| READY | 11 |
| BLOCKED | 40 |

- Placeholder occurrences: 99.
- Objects with placeholders: 38.
- All `##` tokens remain `UNRESOLVED` with `resolved=null`.
- `UNRESOLVED_MANDATORY_PLACEHOLDER`: 38 objects.
- `DEPENDENCY_NOT_READY`: 23 objects.

Counts overlap because an object can carry both a direct placeholder block and a propagated prerequisite block. `VALIDATED/BLOCKED` means the canonical extraction is structurally and semantically valid but cannot be used downstream without participant-specific values.

Relative values—including “dans une semaine,” next-year validity, today, and current-year start/end—remain semantic objects. No absolute date was fabricated.

## 10. Dependency summary

- Dependency edges: 87.
- Resolved canonical edges: 44.
- Unresolved source-reference edges: 43.
- Resolved edges were checked for both target existence and target type.

Unresolved edges are noncritical references to course-local business partners/materials or copied source condition records for which S4620 does not supply a canonical identifier. Critical pricing, procedure, hierarchy, contract, and settlement chains are resolved to staged S4620 objects.

The source’s delivery and billing steps in Exercises 6, 20, 22, and 26 were not silently promoted: those types are outside S4620’s reviewed coverage, and generated identifiers are blank. Their relevant semantics are retained in skip evidence and settlement lineage.

## 11. Exercise/solution deduplication

The exercise is the primary evidence for every scenario. Solutions verify and enrich the same object IDs.

- Exercise 13 enriches the two Exercise 12 future condition records with the explicit 5 percent adjustment; it creates no duplicate.
- Exercises 15 and 16 enrich the Exercise 9 ZF##/Z##PRC model with gross-weight and exclusion behavior.
- Exercise 10 and 11 reporting definitions are deterministic skips.
- The optional instructor demonstration on pages 332–334 is not a second condition contract.

The complete decision and object list for every exercise is stored in `metadata/lineage/full/S4620/section_inventory.json`.

## 12. Confidence summary

| Confidence | Count |
|---|---:|
| HIGH | 48 |
| MEDIUM | 3 |
| LOW | 0 |

The two future PR00 records are MEDIUM because their creation and 5 percent adjustment are explicit but their copied base rates are not printed. KA00 is MEDIUM because the solution prints `P620-2#` once while the exercise and surrounding scenario use `P620-2##`; the exercise-primary value was retained.

## 13. Skipped and rejected candidates

- Exercise 1’s initial order was explicitly abandoned without saving after a missing-price error.
- Exercise 3 contains terminology questions but no additional instance.
- Exercise 6 F1/F2 copy-control and billing records are outside S4620 coverage; the billing identifier is blank.
- Exercises 10–11 define condition-list reporting menus/variants, not canonical condition records.
- Exercise 20 promotion and sales-deal headers have no approved taxonomy type; KA00 and the qualifying order are retained.
- Exercises 20, 22, and 26 delivery/billing operations are outside S4620 coverage and have blank generated identifiers.
- The optional English instructor demonstration on pages 332–334 is explicitly advisory, not a completed participant dataset.

No object has `lifecycle_status=REJECTED`; nonqualifying candidates are recorded as skips with reasons.

## 14. Contradictions, ambiguities, and data-quality findings

| Finding | Severity | Confidence | Control |
|---|---|---|---|
| Participant values unresolved | Medium | High | Preserve all 99 placeholders and block affected objects |
| Generated document identifiers blank | Medium | High | Keep null and use canonical source-based IDs only |
| Exercise 21 prose shows `10010 /10/00`, while its table and solution use 1010/10/00 | Medium | High | Use the repeated tabular/solution value 1010 and record the contradiction |
| KA00 solution prints `P620-2#` once; exercise uses `P620-2##` | Medium | High | Exercise-primary value retained; object confidence MEDIUM |
| Exercise 23 displays REA1 as 10, while solution explicitly states it is -10 EUR | Medium | High | Solution enrichment supplies the unambiguous negative settlement rate |
| Exercise 17 asks for 100 EUR but the solution’s entered discount is -100 | Medium | High | Retain -100 and `DISCOUNT` semantics with both sections in provenance |
| Future copied PR00 base rates are not printed | Medium | High | Keep rates null; retain relative validity and 5 percent adjustment |
| Exercise 5 header-condition currency is not supplied | Low | High | Keep currency null |
| Settlement business volume 5,360 has no printed currency | Low | High | Preserve the value and keep its currency null |

Key uniqueness, missingness, duplicates, schema drift, referential integrity, placeholder behavior, relative values, and deterministic reruns were tested. Freshness and distribution drift are not applicable to this immutable course-document extraction.

## 15. Cross-document checks and S4600 return issue

- S4600 normalized SHA-256 remained `4b5b38be6c9a291db6ffbe010a87e8f73d670f25e346d23da0a157881d519319`.
- S4610 normalized SHA-256 remained `8e4a94dea69465af58c89b8c661dfa8ec41b719799d24e59cc588e413f661889`.
- S4615 normalized SHA-256 remained `a571a6d4794c1aadf4271a9e189dc3b092a129e65bc622022ac4c6f027345695`.
- S4620 supplies no explicit identifier joining a prior staged object; no cross-course link was guessed.
- S4620 supplies no directional evidence for `S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER`.
- The customer-return delivery issue remains `UNRESOLVED_CARRIED_FORWARD`; no S4600 file was modified.

## 16. Schema and taxonomy changes

The smallest source-justified, backward-compatible schema additions were made:

1. `PRICING_CONDITION` supports extended condition keys, semantic relative validity, percentage units, source operations, adjustments, cumulative limits, record status, and deletion state.
2. `CONDITION_TYPE` supports reference base, group-condition, manual/sign/update, scale-control, and copied-from attributes.
3. `CONDITION_TABLE` and `ACCESS_SEQUENCE` support descriptions.
4. `PRICING_PROCEDURE` supports descriptions and structured exclusion groups.
5. `PRICING_PROCEDURE_DETERMINATION` supports quick-entry conditions and settlement-document determination context/group.
6. `SALES_ORDER` supports source pricing elements without turning document snapshots into reusable condition records.
7. `CUSTOMER_HIERARCHY`, `CONDITION_CONTRACT`, and `SETTLEMENT_DOCUMENT` support the source’s structured hierarchy, selection, schedule, business-volume, execution, and accounting metadata.

No taxonomy type was added or reclassified. Promotion and sales-deal headers were not forced into `CONDITION_CONTRACT`, and billing price snapshots were not converted into `PRICING_CONDITION` records.

## 17. Test results

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`

- Tests run: 56.
- Passed: 56.
- Failed/errors: 0.
- Foundation, pilot, S4600, S4610, and S4615 regression tests remain green.
- Stage 4 tests cover stable counts, schema validation, provenance, scenario consistency, exercise/solution deduplication, placeholder/readiness semantics, all three scale bases, condition-technique chains, pricing-procedure determination, hierarchy, condition contract, settlements, relative dates, dependency integrity, prior-stage immutability, the carried return issue, publication prevention, S4650 non-start, and byte-identical deterministic reruns.

## 18. Files generated

Stage artifacts:

- `data/extracted/full/S4620/objects.json`
- `data/normalized/full/S4620/objects.json`
- `metadata/lineage/full/S4620/lineage.json`
- `metadata/lineage/full/S4620/section_inventory.json`
- `metadata/lineage/full/S4620/cross_document_checks.json`
- `metadata/dependencies/full/S4620/dependency_graph.json`
- `metadata/confidence/full/S4620/confidence.json`
- `metadata/confidence/full/S4620/extraction_summary.json`

Implementation and verification:

- `scripts/extract_s4620.py`
- `tests/test_s4620_full.py`
- `scripts/generate_schemas.py` and affected generated schemas
- `reports/phase1b_s4620_extraction_report.md`

Nothing was published under `data/validated/`; only the pre-existing `.gitkeep` remains.

## 19. GO / NO-GO for S4650

**GO**, but only under a separate explicit authorization.

The gate is supported by complete-document parsing, 51/51 schema-valid normalized objects, 44 resolved dependency edges, preserved placeholders and relative values, explicit treatment of all requested pricing and settlement types, documented skips/ambiguities, prior-stage immutability, deterministic outputs, and 56/56 passing tests.

Controls to carry into S4650:

- retain the reviewed coverage roles;
- preserve `##` and readiness independence;
- keep exercise-primary/solution-verification deduplication;
- distinguish reusable condition records from document pricing snapshots;
- do not publish to `data/validated/`;
- do not connect to SAP;
- keep the S4600 return-delivery issue open unless S4650 provides explicit evidence.

This report does not authorize automatic S4650 extraction.
