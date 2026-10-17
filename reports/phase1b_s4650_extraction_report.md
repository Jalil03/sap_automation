# Phase 1B Stage 5 — S4650 extraction report

## 1. Outcome

**GO for Phase 1 consolidation, with the unresolved-value and return-delivery controls carried forward.** S4650 was resolved through the source manifest, checksum-verified, parsed across all 267 pages, and staged without SAP access or publication to `data/validated/`. The run produced 29 extracted and 29 normalized objects. All 58 layer records conform to the current schemas, object IDs and artifacts are deterministic, and all 66 repository tests pass.

This stage stops at S4650. It did not alter the five source PDFs, connect to SAP, implement an SAP mapper or connector, or modify S4600/S4610/S4615/S4620 artifacts.

## 2. Source verification and parsing scope

- Logical source: `S4650`, resolved through `docs/manifests/documents.json`.
- Physical source: `docs/source/S4650_FR_Col12_ILT_FV_Inst_A4.pdf`.
- Manifest and computed SHA-256: `e5601257121ad731d45297c784e25f1306cf6d8a51f215005df2b73db50efa4c`.
- Pages parsed: 267/267.
- Chapters processed: 5/5.
- Exercise/solution pairs detected and verified: 13/13.
- Physical exercise start pages: 17, 27, 53, 69, 75, 89, 109, 117, 137, 159, 177, 213, and 235.
- Physical solution start pages: 18, 29, 58, 71, 76, 90, 111, 118, 139, 161, 179, 215, and 237.

The parser inspected exercises, solutions, demonstrations, procedures, tables, and explanatory sections. Objects were created only for concrete configuration records, saved exercise datasets, explicit determination results, or dependencies useful to Phase 1. UI navigation and purely theoretical extension content were not promoted.

## 3. Canonical object counts

| Object type | Coverage role | Count |
|---|---|---:|
| SALES_ORGANIZATION | PRIMARY | 1 |
| DISTRIBUTION_CHANNEL | PRIMARY | 1 |
| SALES_DIVISION | PRIMARY | 2 |
| SALES_AREA | PRIMARY | 2 |
| SHARED_MASTER_DATA_ASSIGNMENT | PRIMARY | 1 |
| COPY_CONTROL | PRIMARY | 4 |
| TEXT_DETERMINATION | PRIMARY | 2 |
| OUTPUT_DETERMINATION | PRIMARY | 3 |
| EXTENSION_CONFIGURATION | PRIMARY, added in this stage | 2 |
| BUSINESS_PARTNER | SECONDARY | 1 |
| SALES_ORDER | SECONDARY | 7 |
| OUTBOUND_DELIVERY | SECONDARY | 3 |
| MATERIAL | SECONDARY | 0 |
| PRICING_CONDITION | SECONDARY | 0 |
| BILLING | SECONDARY | 0 |
| COMPANY_CODE | REFERENCE_ONLY | 0 |
| PLANT | REFERENCE_ONLY | 0 |
| **Total** |  | **29** |

Classification totals are 18 `CUSTOMIZING`, 1 `MASTER_DATA`, and 10 `TRANSACTION` objects.

No MATERIAL, PRICING_CONDITION, BILLING, COMPANY_CODE, or PLANT object was promoted merely because the type was mentioned. S4650 supplies no qualifying independent instance for those types. The material and plant values used in test transactions remain fields or dependencies on the qualifying transaction/configuration objects.

## 4. Organizational and shared master-data configuration

Exercise 1 produced the source-backed organizational set:

```text
SALES_ORGANIZATION 1010
  -> DISTRIBUTION_CHANNEL D# or E# (participant group determines the exact code)
    -> SALES_AREA 1010 / D# or E# / 00
    -> SALES_AREA 1010 / D# or E# / 03
```

Both sales areas retain business-area assignment rule `1`. The French `secteur d'activité` is normalized to `sales_division`. In Exercise 13, `Division chargée de la livraison` is a logistics field and is normalized to `delivering_plant`; forbidden canonical `division` is not used.

Exercise 2 creates one shared-master-data assignment from source distribution channel `10` to the participant channel for:

- pricing conditions;
- customer master data;
- material master data.

The corresponding CDCL test order depends explicitly on that assignment. The separate pricing-procedure-determination step described by the exercise is not silently promoted because that object type is outside S4650's reviewed coverage.

## 5. Copy control

Four copy-control records were normalized:

| Source → target | Level | Source-backed controls |
|---|---|---|
| OF → ZA## | Header | Copy requirement 002; header data-transfer routine 951 |
| ZQ## → OF | Header/item | Different customer permitted; positive/negative quantity left blank |
| ZA## → LF | Header/item | Requirements 001/101; grouping 051; header routine 001; item routine 699; target category TAN; document-flow update |
| LF → F2 | Header/item | Requirement 003; source item category TAN; pricing source/type E |

The two Exercise 4 delivery tests depend on the ZA##→LF control. The source says to use one of the previously created orders but does not uniquely identify which one, so the SALES_ORDER dependency remains unresolved rather than being guessed.

Quotation instances in Exercise 3 are not first-class S4650 objects because QUOTATION is outside the reviewed S4650 coverage. Their role is retained as an explicit unresolved dependency on the sales orders.

## 6. Text determination

Two records were extracted:

1. Exercise 6 verifies an item text determination result for text object `VBBP`, text ID `0001`, sourced from material sales text. Its provenance enriches the Exercise 3 order identified by customer reference `##-1-2.6`; no duplicate order is created.
2. Exercise 7 defines participant header-text procedure `50+##`, access sequence `90##`, text object `VBBK`, text ID `Y001`, requirement `1`, all-language handling, and assignment to order type `ZA##`.

Exercise 8 creates a reusable standard text element. It was not forced into TEXT_DETERMINATION because the source does not define a determination procedure or rule for that element.

## 7. Output determination

The three records preserve the distinction between classic NAST and new output management:

| Scenario | Framework | Output | Principal configuration |
|---|---|---|---|
| Exercise 9 | NAST | BA00 | Procedure V10000; access Z001; 1010/C650-A##; FAX; send time 3 |
| Exercise 10 | NAST | ZLD0 | Procedure V10000; access 0005; program RLE_DELNOTE; form LE_SHP_DELNOTE; shipping point 1010; LP01 |
| Exercise 11 | NEW_OUTPUT_MANAGEMENT | ORDER_CONFIRMATION_## | SALES_DOCUMENT; ZA##; partner role AG; recipient C650-B##; PRINT; LP01; one copy; form SD_SLS_ORDER_CONFIRM; immediate send |

Exercise 11 also retains the BRFplus-style determination rules for output type, recipient, channel, print options, form template, and relevance for confirmation status `C` or blank.

The Exercise 9 partner update is represented as one BUSINESS_PARTNER object with fax `123456789`. The associated order remains MEDIUM confidence because the exercise and solution are inconsistent about whether the test order was saved.

## 8. Extension-related configuration

S4650 contains explicit participant configurations that do not fit any pre-existing taxonomy type. The smallest justified model addition is `EXTENSION_CONFIGURATION`, classified as CUSTOMIZING.

Two instances were extracted:

- Exercise 12: user-specific sales-order list layout `S4650-##`, description `Groupe de mise en forme ##`, showing delivery and billing blocks and set as the initial layout.
- Exercise 13: material field-selection reference `ZM##`, copied from `ROH`, assigned to material type `YR##`, with field `MVKE-DWERK` in field-selection group `95` set to required. HAWA remains optional as the comparison case.

The following were inspected but skipped as non-instance content: extension-technology theory, instructor-only dictionary demonstrations, reserve-field explanation, VOFM concepts, user exits, customer exits, BTEs, BAdIs, and the enhancement framework. These sections describe techniques or navigation but do not provide a completed participant configuration record.

## 9. Extracted and normalized layers

- Extracted objects: 29 with `lifecycle_status=EXTRACTED`.
- Normalized objects: 29 with `lifecycle_status=VALIDATED`.
- Extracted-to-normalized grain: one-to-one.
- Duplicate object IDs: 0.
- Solution-only duplicate objects: 0.
- Rejected objects: 0; nonqualifying candidates are recorded as deterministic skips.

Every normalized object retains canonical English field names and concise source terms/excerpts in lineage. Solutions verify or enrich the exercise-primary object and never create a second canonical instance.

## 10. Schema validation

- Normalized objects valid: 29/29.
- Extracted objects valid: 29/29.
- Invalid objects: 0.
- Validator: Draft 2020-12 schemas through the repository schema registry.

Every object contains deterministic object/scenario IDs, classification, provenance, independent lifecycle/readiness states, dependencies, placeholders, validation metadata, confidence, and typed business data.

## 11. READY, BLOCKED, and placeholders

| Readiness | Count |
|---|---:|
| READY | 4 |
| BLOCKED | 25 |

- Placeholder occurrences: 50.
- Objects with literal `##` placeholders: 19.
- `UNRESOLVED_MANDATORY_PLACEHOLDER`: 19 objects.
- `UNRESOLVED_CRITICAL_DEPENDENCY`: 5 objects.
- `DEPENDENCY_NOT_READY`: 14 objects.

Counts overlap because an object can carry a direct placeholder and inherit a blocked prerequisite. All literal `##` values remain `UNRESOLVED` with `resolved=null`. `VALIDATED/BLOCKED` means the extraction is structurally and semantically valid but cannot be used downstream without participant-specific resolution.

The exact Exercise 1 channel is also unresolved: the source selects a D- or E-series code by participant group but does not state the group. It is retained as the semantic expression `D# or E#`, with MEDIUM confidence, rather than being fabricated.

Relative values such as “dans une semaine,” “aujourd'hui + 2 semaines,” and “fin de la semaine prochaine” remain semantic objects. No absolute date was invented.

## 12. Dependency summary

- Dependency edges: 39.
- Resolved canonical edges: 20.
- Unresolved source-reference edges: 19.
- Resolved edges passed target-existence and target-type checks.

Principal chains include:

```text
SALES_ORGANIZATION + DISTRIBUTION_CHANNEL + SALES_DIVISION
  -> SALES_AREA

DISTRIBUTION_CHANNEL
  -> SHARED_MASTER_DATA_ASSIGNMENT
    -> SALES_ORDER

COPY_CONTROL
  -> SALES_ORDER / OUTBOUND_DELIVERY

TEXT_DETERMINATION
  -> SALES_ORDER

OUTPUT_DETERMINATION
  -> SALES_ORDER
    -> OUTBOUND_DELIVERY
```

Course-local BUSINESS_PARTNER and MATERIAL references that lack an independently qualifying S4650 object remain noncritical unresolved dependencies. Prior-step quotation/order references that are necessary but not uniquely identifiable remain critical and BLOCKED.

## 13. Confidence summary

| Confidence | Count |
|---|---:|
| HIGH | 23 |
| MEDIUM | 6 |
| LOW | 0 |

MEDIUM-confidence objects and reasons:

- Participant distribution channel: the group-dependent D/E code is not uniquely resolvable.
- ZQ##→OF copy control: the source gives the behavioral settings but not every technical routine key.
- Different-customer Exercise 3 order: the final copied quantity is not printed.
- Two Exercise 4 deliveries: “one of the orders created previously” does not identify the source order.
- Exercise 9 BA00 test order: save status is contradictory between exercise/solution instructions.

There are no LOW-confidence objects.

## 14. Skipped or rejected candidates

- Instructor demonstrations in Chapters 1, 3, and 4 were treated as verification/reference when they repeated participant scenarios; they were not duplicated as exercise objects.
- Exercise 3 quotation records are outside S4650 coverage and remain dependencies.
- Exercise 8 standard text is not a text-determination rule.
- The pricing-procedure-determination action in Exercise 2 is outside S4650's reviewed coverage.
- Chapter 5 conceptual descriptions and UI-only demonstrations are not completed business/configuration records.
- Assessment questions and answers are knowledge checks, not canonical data.

No object received `lifecycle_status=REJECTED`; all skip decisions are preserved in `metadata/lineage/full/S4650/section_inventory.json`.

## 15. Data-quality issues and terminology

| Finding | Severity | Confidence | Control |
|---|---|---|---|
| Exact D/E participant channel is group-dependent | Medium | High | Preserve `D# or E#`; do not select a code |
| Exercise 4 does not identify which prior order feeds each delivery | Medium | High | Keep critical dependencies unresolved |
| Exercise 9 save status is inconsistent | Medium | High | Use `TESTED_SAVE_STATUS_AMBIGUOUS`; confidence MEDIUM |
| Exercise 11 prints `ORDER_CONFIRMATION_# #` in a few lines | Low | High | Normalize to the repeated intended `ORDER_CONFIRMATION_##`; retain source evidence |
| Exercise 3 customer-reference punctuation varies (`##-1-1,4` / `##-1-1.4`) | Low | High | Use canonical dot notation and retain provenance |
| Generated SAP document numbers are not printed | Medium | High | Keep them absent; canonical IDs are not presented as SAP numbers |
| French “division” is context-sensitive | High | High | Use `sales_division` for `secteur d'activité`; `delivering_plant` for `Division chargée de la livraison` |

Quality checks cover source freshness/immutability, key uniqueness, missingness, duplicates, schema drift, referential integrity, placeholder behavior, exercise/solution duplication, terminology, and deterministic reruns.

## 16. Cross-document checks and S4600 return issue

Prior normalized hashes remained unchanged:

- S4600: `4b5b38be6c9a291db6ffbe010a87e8f73d670f25e346d23da0a157881d519319`.
- S4610: `8e4a94dea69465af58c89b8c661dfa8ec41b719799d24e59cc588e413f661889`.
- S4615: `a571a6d4794c1aadf4271a9e189dc3b092a129e65bc622022ac4c6f027345695`.
- S4620: `40fc22acca1c462cfae84a276aa3ccd5b1707e6b98f5503a3cec7c4f86b88113`.

S4650 supplies no exact identifier joining a prior staged object, so no cross-course dependency was guessed.

S4650's copy-control exercises cover ordinary quotation→order→delivery→billing flows. They provide no explicit directional evidence for `S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER`. The customer-return delivery issue remains `UNRESOLVED_CARRIED_FORWARD`, and no S4600 artifact was modified.

## 17. Schema and taxonomy changes

The smallest source-justified changes were made:

1. Added CUSTOMIZING type `EXTENSION_CONFIGURATION`, with configuration family/key, description, target object, and structured settings. Added it to S4650 PRIMARY coverage.
2. Extended SALES_AREA with `business_area_assignment_rule`.
3. Extended COPY_CONTROL with distinct header/item requirements and data-transfer routines, grouping, target item category, document-flow update, and pricing source.
4. Extended TEXT_DETERMINATION with level, text object/source, assignments, reference-copy mode, language handling, and requirement.
5. Extended OUTPUT_DETERMINATION with application object, framework, access sequence, key combinations, condition records, routines, partner/form/print settings, send time, and structured determination rules.
6. Extended BUSINESS_PARTNER with `fax_number` for the explicit Exercise 9 update.

All additions are backward-compatible. No prior object was reclassified or rewritten.

## 18. Test results

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`

- Tests run: 66.
- Passed: 66.
- Failed/errors: 0.
- All foundation, pilot, and Stages 1–4 regression tests remain green.
- Stage 5 tests cover stable counts, schema/lifecycle validation, provenance, scenario consistency, exercise/solution deduplication, placeholders/readiness, organization/shared-data semantics, copy control, text/output frameworks, extension configuration, terminology, dependency integrity, relative values, prior-stage immutability, the carried return issue, publication prevention, and byte-identical deterministic reruns.

## 19. Files generated

Stage artifacts:

- `data/extracted/full/S4650/objects.json`
- `data/normalized/full/S4650/objects.json`
- `metadata/lineage/full/S4650/lineage.json`
- `metadata/lineage/full/S4650/section_inventory.json`
- `metadata/lineage/full/S4650/cross_document_checks.json`
- `metadata/dependencies/full/S4650/dependency_graph.json`
- `metadata/confidence/full/S4650/confidence.json`
- `metadata/confidence/full/S4650/extraction_summary.json`

Implementation, model, and verification:

- `scripts/extract_s4650.py`
- `tests/test_s4650_full.py`
- `tests/test_s4620_full.py` (obsolete “S4650 must not exist” guard removed)
- `taxonomy/object_types.yaml`
- `mappings/document_to_object.yaml`
- `scripts/generate_schemas.py`
- `schemas/customizing/extension_configuration.schema.json`
- affected regenerated schemas and `schemas/index.json`
- `reports/phase1b_s4650_extraction_report.md`

Nothing was published under `data/validated/`; only the pre-existing `.gitkeep` remains.

## 20. GO / NO-GO for Phase 1 consolidation

**GO for Phase 1 consolidation.** The five staged sources now have deterministic, schema-valid artifacts and cross-document immutability evidence. Consolidation should remain a separate authorized activity and must:

1. preserve the 25 S4650 BLOCKED objects until participant placeholders or critical references are explicitly resolved;
2. keep the S4600 customer-return delivery issue open;
3. reconcile cross-course duplicates by source identity and semantics, not by similar labels alone;
4. revalidate the newly added `EXTENSION_CONFIGURATION` type across the consolidated registry;
5. run a full dependency, provenance, schema, and deterministic-publication gate before anything enters `data/validated/`.

Stage 5 itself does not publish or begin consolidation.
