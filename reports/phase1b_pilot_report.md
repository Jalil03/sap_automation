# Phase 1B Controlled Extraction Pilot Report

## 1. Pilot scope

The pilot processed only three approved representative slices:

- S4650 Customizing: `DISTRIBUTION_CHANNEL` and two `SALES_AREA` objects.
- S4620 master data: one customer/material `PRICING_CONDITION` for PR00 with quantity scales.
- S4600 transaction chain: `SALES_ORDER -> OUTBOUND_DELIVERY -> BILLING`, with S4610 and S4615 used only as semantic references.

No full-document extraction, production validated-dataset write, SAP mapper, connector, or SAP call was performed. Source PDFs were unchanged.

## 2. Source pages and exercises used

| Course | Scenario | Primary evidence (PDF page / printed page) | Verification evidence |
|---|---|---|---|
| S4650 | Chapter 1, Exercise 1, organizational structure | 17 / 9 | Solution 1: PDF 18-19 / printed 10-11 |
| S4620 | Chapter 1, Exercise 1, PR00 customer/material scales | 21 / 13 | Solution 1: PDF 27-28 / printed 19-20 |
| S4600 | Chapter 3, Exercise 3, sales order | 57 / 47 | Solution 3: PDF 58 / printed 48 |
| S4600 | Chapter 3, Exercise 5, outbound delivery | 71 / 61 | Solution 5: PDF 72 / printed 62 |
| S4600 | Chapter 3, Exercise 7, billing | 87 / 77 | Solution 7: PDF 88 / printed 78 |
| S4610 | Outbound-delivery semantic reference | PDF 114-115 / printed 106-107 | Not used to populate scenario values |
| S4615 | Billing semantic reference | PDF 109-110 / printed 101-102 | Not used to populate scenario values |

## 3. Objects extracted

Seven unique EXTRACTED records were written: one distribution channel, two sales areas (`sales_division` 00 and 03), one PR00 pricing condition, one standard sales order, one outbound delivery, and one billing document.

Every record has a deterministic `object_id`, scenario ID, exact page provenance, lifecycle/readiness status, structured placeholders, dependencies, validation metadata, and confidence.

## 4. Objects normalized

Seven corresponding canonical records were written with `lifecycle_status: VALIDATED`. Normalization retained the source terms in lineage and applied:

- `Secteur d'activité` -> `sales_division`.
- `Organis. commerciale` -> `sales_organization`.
- `Canal distribution` -> `distribution_channel`.
- Relative dates as semantic objects rather than calendar dates.
- Unknown document numbers and values as null/unresolved, never fabricated.

## 5. Schema validation results

All 14 records (7 extracted and 7 normalized) passed their Draft 2020-12 schemas using the real `jsonschema` validator: **14 passed, 0 failed**.

Pilot evidence required two source-backed schema improvements: structured scale rows and document items, plus a distinct `planned_creation_date` for outbound delivery. The PR00 key combination and scale row contracts now validate their internal structure.

## 6. Placeholder results

Eleven placeholder occurrences remain `UNRESOLVED` with `resolved: null` because `mappings/placeholders.yaml` contains no explicit value:

| Area | Count | Effect |
|---|---:|---|
| Distribution channel | 2 | Group-specific code/description unresolved |
| Sales areas | 2 | Referenced group distribution channel unresolved |
| PR00 condition | 2 | Customer and material suffixes unresolved |
| Sales order | 4 | Customer, reference, and two materials unresolved |
| Outbound delivery | 1 | Shipping-point suffix unresolved |

All seven normalized objects are canonically valid but have `readiness_status: BLOCKED`. Billing is blocked because its identified delivery dependency is not ready.

## 7. Dependency graph

```text
S4600_CH3_EX3_SALES_ORDER_STANDARD
  -> S4600_CH3_EX5_OUTBOUND_DELIVERY_FROM_EX3
       -> S4600_CH3_EX7_BILLING_FROM_EX5
```

The stored edge direction is from the dependent object to its predecessor: delivery `CREATED_FROM` sales order, then billing `BILLED_FROM` delivery. Both target identities are deterministically resolved; no SAP document number was invented.

## 8. Exercise/solution deduplication

Seven exercise-primary objects contain 7 EXERCISE provenance references and 11 SOLUTION verification references. Object IDs remain unique and no solution generated a second object. The two sales-area records are intentional separate business objects for sales divisions 00 and 03, not duplicates.

## 9. Confidence summary

| Confidence | Objects | Rationale |
|---|---:|---|
| HIGH | 2 | PR00 scales and sales-order fields are explicit in source tables |
| MEDIUM | 5 | Group-dependent Customizing values, blank delivery detail cells, or sparse billing fields |
| LOW | 0 | None |

## 10. Data-quality issues

| Finding | Evidence | Severity | Confidence | Impact/remediation |
|---|---|---|---|---|
| Participant identity is absent | 11 unresolved `##` occurrences | Medium | High | Correctly blocks readiness; supply an explicit mapping later if authorized |
| Distribution-channel code cannot be selected | S4650 provides a group-number lookup but no participant group | Medium | High | Keep code null and both sales areas blocked |
| PR00 validity is only “default” | No explicit dates in the exercise | Low | High | Keep `valid_from`/`valid_to` null |
| Sales-order units are absent | Quantities 10/20 are explicit, units are not | Low | High | Keep item units null |
| Delivery detail table is blank | Item quantities/storage locations are participant results | Medium | High | Keep delivery items empty; do not copy order items silently |
| Billing identifiers/date/payer are not supplied | Exercise asks the participant to create/note the result | Medium | High | Preserve nulls and the delivery dependency |

There is no temporal history in this seven-record pilot, so freshness, trend, and distribution-drift checks are not applicable.

## 11. Ambiguous fields or terminology

- The delivery exercise field is `Date de création planifiée`; it is normalized as `planned_creation_date`, not `planned_goods_issue_date`.
- The PR00 table shows scale quantity unit `PC` and amount currency `EUR`, but no explicit numeric pricing unit. `pricing_unit` remains null.
- S4610 and S4615 describe delivery/billing semantics but do not prove the S4600 scenario values; they are stored only as semantic references.
- S4600 is cataloged as a participant edition but includes solution pages. Deduplication therefore operates on section type rather than edition label alone.

## 12. Files generated

- `data/extracted/pilot/pilot_objects.json`
- `data/normalized/pilot/pilot_objects.json`
- `metadata/lineage/pilot/pilot_lineage.json`
- `metadata/dependencies/pilot/dependency_graph.json`
- `metadata/confidence/pilot/confidence.json`
- `reports/phase1b_pilot_report.md`
- `scripts/build_pilot.py`
- `src/validation/jsonschema.py`
- `tests/test_pilot.py`

The schema generator and affected pricing-condition, sales-order, outbound-delivery, and billing contracts were updated to support the observed structures.

## 13. Test results

Command: `.venv/Scripts/python.exe -m unittest discover -s tests -p "test_*.py" -v`

Result: **17 passed, 0 failed** (8 foundation tests and 9 pilot tests). Checks cover real schema validation, inventory/key uniqueness, lifecycle/readiness, placeholders, PR00 scales, normalized terminology, lineage, dependencies, confidence metadata, and exercise/solution deduplication.

## 14. Recommendation

**GO for staged full Phase 1B extraction.** The canonical foundation handled real Customizing, master-data, and transaction-chain evidence without invented identifiers, duplicate solution objects, or schema failures. Full extraction should proceed course-by-course with the same validation gates and must retain `BLOCKED` readiness for unresolved participant values.

This recommendation does not authorize Phase 2 mapping, Phase 3 SAP connectivity, or writing pilot records into the production validated dataset.
