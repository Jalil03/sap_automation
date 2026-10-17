# Phase 1B Stage 1 — S4600 extraction report

## 1. Source verification

- Logical source: `S4600`, resolved through `docs/manifests/documents.json`.
- Physical source: `docs/source/P2W_S4600_FR_Col23.pdf`.
- SHA-256: `a783e489c8e041381b1c4107d45b205511bc7c26cfcbd033ec0ca6355424f258`.
- Manifest checksum: verified.
- Parsed pages: 353 of 353.
- Detected exercise/solution pairs: 36 exercises and 36 solutions.
- Detected table markers (`Nom de zone` / `Valeur`): 107.
- No source PDF was modified. No SAP connection, SAP mapper, connector, BAPI, RFC, OData, IDoc, or GUI automation was used.

## 2. Pages and sections processed

The complete document, physical PDF pages 1–353, was parsed. Exercise start pages were 21, 39, 57, 63, 71, 79, 87, 91, 105, 111, 119, 129, 137, 141, 145, 155, 161, 179, 189, 205, 211, 215, 227, 233, 249, 253, 259, 271, 277, 283, 293, 309, 317, 323, 337, and 347. Their corresponding solution starts were also detected and reviewed.

`metadata/lineage/full/S4600/section_inventory.json` records the deterministic decision for every exercise. Exercises 2, 15, 24, 29, and 36 were theory/UI-only and produced no independent business object. Exercise 4 is `VERIFY_ONLY`: it enriches the Exercise 3 sales order and does not create a duplicate. Exercises 25–27 were not materialized because their mass-run counts and document identifiers are participant-dependent blanks.

## 3. Canonical objects found by type

| Object type | Count |
|---|---:|
| SALES_ORDER | 18 |
| OUTBOUND_DELIVERY | 7 |
| BILLING | 6 |
| MATERIAL | 4 |
| GOODS_ISSUE | 3 |
| PRICING_CONDITION | 3 |
| BUSINESS_PARTNER | 2 |
| CREDIT_MEMO_REQUEST | 1 |
| CUSTOMER_MATERIAL_INFO | 1 |
| DISTRIBUTION_CHANNEL | 1 |
| INQUIRY | 1 |
| PAYMENT_REFERENCE | 1 |
| QUOTATION | 1 |
| RETURN_ORDER | 1 |
| SALES_AREA | 1 |
| SALES_DIVISION | 1 |
| SALES_ORGANIZATION | 1 |
| SHIPPING_POINT | 1 |
| **Total** | **54** |

Classification totals are 38 `TRANSACTION`, 10 `MASTER_DATA`, 5 `CUSTOMIZING`, and 1 `REFERENCE_DATA` objects.

## 4. PRIMARY / SECONDARY / REFERENCE_ONLY handling

- `PRIMARY`: all 12 S4600 primary types with concrete source instances were represented: business partner, material, customer-material information, pricing condition, inquiry, quotation, sales order, credit memo request, return order, outbound delivery, goods issue, and billing.
- `SECONDARY`: the explicit organizational values `1010 / 10 / 00` were deduplicated into one sales organization, distribution channel, sales division, and sales area. `Z0##` became one unresolved shipping-point object. These are shared context records, not one object per mention.
- `REFERENCE_ONLY`: `PAYMENT_REFERENCE` was promoted because Exercise 8 supplies an actual payment instance and it is required by the transaction chain. Company code and plant values remain fields or dependency references. Storage location and warehouse number were not promoted to first-class objects because S4600 did not supply a qualifying independent record.

## 5. Extracted object count

54 objects were written with `lifecycle_status=EXTRACTED` to `data/extracted/full/S4600/objects.json`. Object IDs are fixed, human-readable IDs derived from course, chapter, exercise, type, and stable source key; no runtime document number was invented.

## 6. Normalized object count

54 objects were normalized and written to `data/normalized/full/S4600/objects.json`. The extracted and normalized layers have a one-to-one object inventory. Normalized keys use canonical English terms while lineage retains the French source terminology.

## 7. Schema validation results

- Valid: 54/54.
- Invalid: 0/54.
- All normalized records have `lifecycle_status=VALIDATED` because the source representation, schema, provenance, dependency encoding, and placeholder semantics validate.
- Validation used the real Draft 2020-12 schemas and the repository schema registry.

`VALIDATED` does not mean downstream-ready. The lifecycle and readiness axes remain independent.

## 8. Placeholder summary

- Unresolved placeholder occurrences: 94.
- Objects containing at least one participant placeholder: 40.
- Placeholder token: `##`; no placeholder was resolved because `mappings/placeholders.yaml` supplies no explicit participant mapping.
- Each occurrence records `raw`, `resolved=null`, `status=UNRESOLVED`, `mandatory=true`, and an exact canonical field path.

Relative values such as `dans 1 semaine`, `Date du jour + 3 semaines`, `aujourd'hui + 14 jours`, and `Échue la semaine prochaine` remain structured relative values. No absolute dates were fabricated.

## 9. READY vs BLOCKED summary

| Readiness | Count |
|---|---:|
| READY | 4 |
| BLOCKED | 50 |

The four READY objects are the shared sales organization `1010`, distribution channel `10`, sales division `00`, and sales area `1010/10/00`. The remaining objects are correctly extracted but blocked by participant placeholders, unresolved critical source references, or propagation from a blocked dependency.

Blocking-reason occurrences are:

- `UNRESOLVED_MANDATORY_PLACEHOLDER`: 40 objects.
- `UNRESOLVED_CRITICAL_DEPENDENCY`: 24 objects.
- `DEPENDENCY_NOT_READY`: 32 objects.

These counts overlap because an object can have more than one blocking reason.

## 10. Dependency summary

- Dependency edges: 84.
- Resolved canonical edges: 38.
- Unresolved source-reference edges: 46.

Representative preserved chains include:

1. Exercise 3 `SALES_ORDER` → Exercise 5 `OUTBOUND_DELIVERY` → Exercise 6 `GOODS_ISSUE` → Exercise 7 `BILLING` → Exercise 8 `PAYMENT_REFERENCE`.
2. Exercise 28 `INQUIRY` → `QUOTATION` → `SALES_ORDER`.
3. Exercise 32 `SALES_ORDER` → `OUTBOUND_DELIVERY` → `GOODS_ISSUE` → standard `BILLING` → `CREDIT_MEMO_REQUEST` → credit-memo `BILLING` → Exercise 33 cancellation `BILLING`.
4. Exercise 34 `RETURN_ORDER` → return `OUTBOUND_DELIVERY` and credit-memo `BILLING`.

Phrases such as “document créé à l'étape précédente” are dependency evidence. They were not replaced with guessed SAP document numbers. Every `RESOLVED` edge targets an extracted object of the declared type; every unresolved edge has `target_id=null`.

## 11. Exercise/solution deduplication summary

The exercise is the primary source for every scenario. Solution sections verify or enrich the same object. No solution-only duplicate was created.

Notable enrichments include the Exercise 3 processing status, Exercise 20 material/partner values, Exercise 31 service material type and item category, and Exercise 35 completion/payment terms. Exercise 4 is explicitly recorded as `VERIFY_ONLY` against the Exercise 3 order.

## 12. Low-confidence objects

Confidence distribution is 38 HIGH, 15 MEDIUM, and 1 LOW.

The sole LOW-confidence object is `S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER`. The source creates a “livraison de retours” through an outbound-delivery application but the physical flow is a customer return. The canonical record therefore uses `OUTBOUND_DELIVERY` with `delivery_type=RETURN`, preserving the source behavior without pretending it is an ordinary outbound shipment. This interpretation must remain visible until a dedicated return-delivery type is justified across documents.

MEDIUM confidence primarily identifies objects whose source document number is intentionally blank, whose content is inherited through an explicit prior-step reference, or whose creation detail appears in solution enrichment.

## 13. Rejected or skipped candidates and reasons

- Exercises 2, 15, 24, and 29: theoretical questions, no actual record.
- Exercise 36: analytics/UI procedure, no canonical business-object instance.
- Exercises 25–27: mass delivery, goods issue, and billing runs have blank counts and blank participant-generated identifiers. Creating a guessed count or one synthetic “batch object” would violate the no-invention rule.
- Exercise 19 delivery attempt: source explicitly says not to create the delivery.
- Item proposal in Exercise 16: not in the approved taxonomy; its explicit contents enrich the sales order instead.
- MRP job, planned order, production order, and production goods receipt in Exercise 30: outside the reviewed S4600 canonical coverage.
- Accounting document and warehouse task mentions: not promoted without a complete qualifying instance.
- Return goods receipt in Exercise 34: not mislabeled as `GOODS_ISSUE`; no in-scope canonical goods-receipt type exists.

No candidate was marked `REJECTED`; non-qualifying candidates are recorded as deterministic skips with reasons.

## 14. Terminology issues

- French `division` is context-sensitive: in sales organization context it normalizes to `sales_division`; in logistics/material context it normalizes to `plant`. The source term is retained in lineage.
- `donneur d'ordre` normalizes to `sold_to_party`; `réceptionnaire` to `ship_to_party`; `point d'expédition` to `shipping_point`.
- `pièce` normalizes to unit `PC`; service hours normalize to `H` while the French wording remains in provenance.
- `livraison de retours` remains semantically ambiguous as described in Section 12.
- SAP condition `K007` is a value-basis percentage scale; it must not be normalized as a quantity/amount scale.

## 15. Coverage gaps

The current S4600 boundary intentionally does not model item proposals, production/MRP objects, accounting documents, analytical reports, generic warehouse operations, or goods receipts. These were not silently coerced into nearby object types.

The most important future review item is whether repeated evidence in later documents warrants a dedicated `RETURN_DELIVERY` and/or `GOODS_RECEIPT` type. No such taxonomy expansion is required to proceed with S4610, whose approved scope already focuses on outbound/inbound delivery, goods issue, and warehouse task objects.

## 16. Test results

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -v`

- Tests run: 26.
- Passed: 26.
- Failed/errors: 0.
- Existing foundation and pilot tests remain green.
- New tests cover stable object counts, schema validation, provenance completeness, scenario consistency, exercise/solution deduplication, placeholder preservation, terminology normalization, dependency integrity, quantity/value scale semantics, and deterministic re-run behavior.
- A second unchanged extraction produced byte-identical staged JSON artifacts and no duplicate IDs.

## 17. Files generated

Stage artifacts:

- `data/extracted/full/S4600/objects.json`
- `data/normalized/full/S4600/objects.json`
- `metadata/lineage/full/S4600/lineage.json`
- `metadata/lineage/full/S4600/section_inventory.json`
- `metadata/dependencies/full/S4600/dependency_graph.json`
- `metadata/confidence/full/S4600/confidence.json`
- `metadata/confidence/full/S4600/extraction_summary.json`

Implementation and verification:

- `scripts/extract_s4600.py`
- `tests/test_s4600_full.py`
- `reports/phase1b_s4600_extraction_report.md`

No file was written to a production validated dataset.

## 18. Required schema/taxonomy changes

The smallest justified schema changes were made and tested:

1. `PRICING_CONDITION.scales` now supports both quantity-basis amount scales and value-basis percentage scales. Existing pilot quantity-scale fields remain backward compatible.
2. `SALES_ORDER.items` gained optional `plant`, `ship_to_party`, `net_weight`, `net_weight_unit`, and `item_category`; the header gained optional payment, processing, and completeness fields.
3. `BUSINESS_PARTNER` and `MATERIAL` gained optional fields that are explicitly populated by S4600 exercises rather than being lost in lineage-only text.
4. Inquiry, quotation, billing, and payment relative dates accept structured relative values.

No taxonomy type was added. `delivery_type=RETURN` is sufficient for this staged record while its LOW-confidence semantic caveat remains explicit. A dedicated type should be added only if cross-document evidence supports it.

## 19. GO / NO-GO recommendation for Stage 2 (S4610)

**GO** for Stage 2, limited to S4610 and the existing staged-extraction controls.

The gate is supported by complete S4600 parsing, full scenario inventory, 54/54 schema-valid normalized objects, deterministic output, preserved placeholders/relative values, explicit dependency integrity, and 26/26 passing tests. Stage 2 must continue to avoid SAP connectivity and production publication, and should re-evaluate the return-delivery semantic only if S4610 supplies stronger evidence.

This recommendation does not authorize automatic Stage 2 execution. Processing stops at S4600.
