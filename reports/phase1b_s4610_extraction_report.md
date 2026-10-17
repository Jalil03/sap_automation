# Phase 1B Stage 2 — S4610 extraction report

## 1. Scope and source verification

Stage 2 processed S4610 only. The source was resolved through `docs/manifests/documents.json` as `docs/source/S4610_FR_Col12_ILT_FV_Inst_A4.pdf`.

- Manifest version: 12, instructor edition, French.
- Physical pages: 202 of 202 parsed.
- SHA-256: `a00a302c4a948f7dbd32ad952ca4dedbb94ac3c5e92d3ea03982f42cf959d6be`.
- Checksum: verified against the manifest.
- Exercise/solution pairs: 14/14 detected.
- Table markers: 44.
- Source PDF: unchanged.
- S4600: read-only cross-document checks only; its normalized artifact hash remained unchanged.
- S4615: not processed.
- No SAP connection, mapper, connector, BAPI, RFC, OData, IDoc, or SAP GUI automation was used.

## 2. Complete-document processing and section decisions

All pages 1–202 were parsed. Exercise start pages were 19, 25, 41, 65, 91, 107, 109, 127, 135, 153, 163, 169, 179, and 189; matching solution starts were 20, 26, 43, 69, 93, 108, 111, 129, 136, 155, 164, 170, 181, and 191.

The deterministic decision for every exercise is stored in `metadata/lineage/full/S4610/section_inventory.json`.

- Exercise 1: theory only; no instance.
- Exercise 2: one sparse, pre-existing outbound-delivery instance retained at LOW confidence.
- Exercises 3–4 and 7: concrete Customizing and transaction records extracted.
- Exercises 5–6: evidence enriches the Exercise 3 express shipping point; no duplicate object.
- Exercise 8: storage-location determination extracted; mass-delivery instances skipped because the source gives only “at least two” and blank identifiers.
- Exercise 9: monitor/list procedure only; no new object.
- Exercises 10–14: outbound, warehouse, goods-issue, purchase-order, and inbound chains extracted.

## 3. Object counts

| Object type | Coverage role | Count |
|---|---|---:|
| SHIPPING_POINT | PRIMARY | 2 |
| OUTBOUND_DELIVERY | PRIMARY | 3 |
| INBOUND_DELIVERY | PRIMARY | 2 |
| GOODS_ISSUE | PRIMARY | 1 |
| WAREHOUSE_TASK | PRIMARY | 2 |
| SALES_ORDER | SECONDARY | 3 |
| COPY_CONTROL | SECONDARY | 2 |
| PLANT | REFERENCE_ONLY | 1 |
| STORAGE_LOCATION | REFERENCE_ONLY | 2 |
| WAREHOUSE_NUMBER | REFERENCE_ONLY | 1 |
| PURCHASE_ORDER_REFERENCE | REFERENCE_ONLY | 2 |
| **Total** |  | **21** |

Classification totals are 11 `TRANSACTION`, 4 `CUSTOMIZING`, and 6 `REFERENCE_DATA` objects.

The reference-only records were promoted because primary delivery and warehouse dependencies require explicit plant, storage-location, warehouse, or purchase-order identities. They were not promoted merely because the terms appeared theoretically.

## 4. Extracted and normalized layers

- Extracted objects: 21, written with `lifecycle_status=EXTRACTED`.
- Normalized objects: 21, written with `lifecycle_status=VALIDATED`.
- Duplicate object IDs: 0.
- Extracted-to-normalized grain: one-to-one.

Original French source terms and excerpts remain in lineage. Canonical fields consistently distinguish logistical `plant` from sales `sales_division`.

## 5. Outbound versus inbound delivery handling

Three outbound deliveries and two inbound deliveries were retained as distinct canonical types.

- Outbound deliveries depend on sales orders and, where explicit, shipping points and picking storage locations.
- Inbound deliveries depend on purchase-order references, plant `1010`, storage location `101D`, and warehouse `1010`.
- LE and EWM document numbers are modeled as system representations of one canonical business delivery per scenario. They are not duplicate canonical objects.
- Exercise 12's additional EWM outbound-delivery document enriches the Exercise 10 outbound delivery rather than creating a second business delivery.
- Exercise 13's LE and EWM inbound identifiers likewise remain one canonical inbound delivery.

## 6. Schema validation

- Normalized objects valid: 21/21.
- Normalized objects invalid: 0.
- Extracted objects valid: 21/21.
- Validator: Draft 2020-12 schemas through the repository schema registry.

Every object includes classification, scenario ID, provenance, lifecycle, readiness, placeholders, dependencies, validation metadata, and canonical data.

## 7. READY and BLOCKED

| Readiness | Count |
|---|---:|
| READY | 4 |
| BLOCKED | 17 |

The READY objects are plant `1010`, storage locations `101C` and `101D`, and warehouse number `1010`.

Blocking-reason occurrences are:

- `UNRESOLVED_MANDATORY_PLACEHOLDER`: 13 objects.
- `UNRESOLVED_CRITICAL_DEPENDENCY`: 6 objects.
- `DEPENDENCY_NOT_READY`: 9 objects.

Counts overlap because an object can have several blocking reasons. `VALIDATED/BLOCKED` is intentional: the extraction is valid while participant-specific values or prerequisite identities remain unresolved.

## 8. Placeholder results

- Placeholder occurrences: 42.
- Objects with placeholders: 13.
- Resolution status: all remain `UNRESOLVED` with `resolved=null`.
- Explicit mapping used: none; `mappings/placeholders.yaml` contains no applicable participant assignment.

Examples include `Y0##`, `Z0##`, `ZA##`, `ZL##`, `C610-A##`, `P610-2##`, `Z##`, and `S4610-##-1`. No suffix or participant number was invented.

Relative values such as `Date du lendemain`, `Surlendemain`, and `dans 1 semaine` remain structured relative values rather than fabricated calendar dates.

## 9. Dependency results

- Total dependency edges: 43.
- Resolved canonical edges: 32.
- Unresolved source-reference edges: 11.

Unresolved edges comprise one unidentified prior sales order, five business-partner references, and five material references. Their source phrases remain attached and their target IDs are null.

Representative resolved chains are:

1. Exercise 4 `SALES_ORDER` → express `OUTBOUND_DELIVERY` with copy-control evidence.
2. Exercise 10 `SALES_ORDER` → `OUTBOUND_DELIVERY` → Exercise 11 `WAREHOUSE_TASK` → Exercise 12 `GOODS_ISSUE`.
3. Exercise 13 `PURCHASE_ORDER_REFERENCE` → `INBOUND_DELIVERY`.
4. Exercise 14 `PURCHASE_ORDER_REFERENCE` → `INBOUND_DELIVERY` → inbound `WAREHOUSE_TASK`.
5. `SHIPPING_POINT` → `PLANT`; warehouse and delivery objects → `STORAGE_LOCATION` / `WAREHOUSE_NUMBER`.

Every resolved dependency targets an extracted object of the declared canonical type.

## 10. Shipping point, plant, storage, and warehouse findings

- `Z0##`: existing standard shipping point assigned to plant `1010`.
- `Y0##`: copied from `Z0##`, assigned to plant `1010`, described as the express Hamburg shipping point.
- Express determination evidence: shipping condition `50+##`, loading group `0004`, plant `1010`, proposed point `Y0##`, alternative point `Z0##`.
- Scheduling evidence for `Y0##`: working time `2-SHIFT`, loading time `PT2H30M`, and pick/pack time `PT2H30M`.
- Storage-location determination: `Y0## / 1010 / blank or 70 → 101C`.
- Inbound purchasing storage location: `101D` at plant `1010`.
- Warehouse number: `1010`, linked to the documented plant/storage-location combinations.

## 11. Exercise/solution deduplication

Exercise evidence is primary. Solution evidence verifies or enriches the same scenario.

- Shipping-point evidence from Exercises 5, 6, and 8 enriches the Exercise 3 `Y0##` object.
- Exercise 12's EWM delivery representation enriches the Exercise 10 outbound delivery.
- LE/EWM inbound representations in Exercises 13 and 14 do not produce duplicate inbound-delivery objects.
- All 21 normalized objects have exercise and solution provenance.

## 12. Confidence summary

| Confidence | Count |
|---|---:|
| HIGH | 15 |
| MEDIUM | 5 |
| LOW | 1 |

The sole LOW-confidence object is the existing outbound delivery in Exercise 2. The exercise proves that a delivery exists and is linked to a sales order with customer purchase-order reference `S4610`, but its delivery number, shipping point, weight, and arrival date are participant/system results left blank. It is retained as a real instance with an unresolved sales-order dependency rather than populated with guesses.

MEDIUM confidence primarily covers sparse prior-step documents, warehouse tasks whose generated identifiers are blank, and one pre-existing copy-control relationship verified rather than newly configured.

## 13. Skipped or rejected candidates

- Exercise 1 delivery theory: no first-class instance.
- Route `Expr##` and route-determination entries: explicit configuration evidence exists, but `ROUTE` is not an approved canonical type. The route remains on the sales-order item and in lineage.
- Delivery/item category configuration: retained in copy-control requirements and transaction line attributes; no unsupported new type was created.
- Exercise 8 mass outbound deliveries: the source states “at least two” and supplies no IDs, so neither a guessed count nor a synthetic batch delivery was created.
- Exercise 9 monitor output: UI/list procedure only.
- Goods receipt in Exercise 14: represented as `goods_receipt_status=POSTED` on the inbound delivery; it was not mislabeled as `GOODS_ISSUE`.
- Warehouse orders mentioned around tasks: not promoted without a separate complete canonical instance.

No object was written with `lifecycle_status=REJECTED`; non-qualifying candidates are recorded as skips with reasons.

## 14. Contradictions and ambiguities

### Exercise 13 wording

The scenario introduction says a “livraison sortante” is created after the purchase order. The exercise title, numbered tasks, solution, goods-receipt process, and LE/EWM navigation consistently create a `livraison entrante`. The canonical object follows the repeated operational evidence and is `INBOUND_DELIVERY`. The contradictory introductory wording remains documented rather than silently treated as authoritative.

### Purchase-order field layout

Some solution tables are visually misaligned in text extraction. Values were reconciled against the exercise table and surrounding instructions. Unspecified net price remains null in Exercise 13; Exercise 14's solution explicitly supplies `52`, with currency still null.

### S4600 return-delivery issue

The S4600 LOW-confidence customer-return delivery remains unresolved. S4610 page 21 explicitly lists `Retours fournisseur` as a delivery-document scenario, but this does not establish whether the S4600 customer-return delivery should be canonical inbound, outbound, or a dedicated return-delivery type. No S4600 file or status was changed.

## 15. Cross-document checks against S4600

- S4600 normalized artifact SHA-256 was recorded before and after the read-only check and remained identical.
- `SHIPPING_POINT.code=Z0##` creates a potential S4600/S4610 entity match.
- The match remains `POTENTIAL_MATCH_UNRESOLVED_PLACEHOLDER`; unresolved participant suffixes prevent declaring global identity.
- No S4610 dependency was silently linked to an S4600 object solely by a placeholder-bearing display value.

## 16. Data-quality assessment

| Finding | Evidence | Severity | Confidence | Impact / control |
|---|---|---|---|---|
| Participant values unresolved | 42 occurrences across 13 objects | Medium | High | Correctly blocks readiness; resolve only through explicit mapping |
| Sparse existing delivery | Exercise 2 has blank result fields | Medium | High | LOW-confidence object retained without invented attributes |
| Mass-run cardinality unavailable | Exercise 8 says at least two, IDs blank | Medium | High | Candidate instances skipped |
| Unresolved entity parents | 11 dependency edges lack extractable parent IDs | Medium | High | Null targets and source phrases preserved |
| Exercise 13 directional wording conflict | Introduction says outbound; tasks/solution say inbound | Medium | High | Repeated operational evidence controls classification |
| Return-delivery taxonomy ambiguity | S4610 covers supplier return only | Medium | High | S4600 issue carried forward unchanged |
| LE/EWM duplicate risk | Two document representations per delivery | High if unhandled | High | Canonical dedup stores system representations on one object |

Grain, key uniqueness, completeness, validity, dependency integrity, schema drift, and deterministic output were tested. Temporal freshness and distribution drift are not applicable to this static training-document extraction.

## 17. Schema and taxonomy changes

The smallest source-justified schema changes were applied:

1. Delivery items now support optional plant, storage location, warehouse number, item category, and weight fields.
2. Outbound and inbound deliveries can retain storage/warehouse context and LE/EWM system representations.
3. Inbound delivery supports purchase-order reference, ASN, and goods-receipt status.
4. Warehouse task supports direction, confirmation status, and delivery reference.
5. Goods issue supports movement status.
6. Shipping point supports source-backed determination rules and scheduling values.
7. Purchase-order reference supports purchasing organization/group, company code, storage location, price, currency, and confirmation control.
8. Sales-order items support shipping point and route.

All additions are optional and backward compatible with the pilot and S4600 objects. No taxonomy object type was added. In particular, no `RETURN_DELIVERY`, `ROUTE`, or `GOODS_RECEIPT` type was introduced without sufficient cross-document evidence.

## 18. Test results

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -v`

- Tests run: 36.
- Passed: 36.
- Failed/errors: 0.
- Foundation, pilot, and S4600 regression tests remain green.
- Stage 2 tests cover stable counts, unique IDs, schema compliance, provenance, scenario consistency, placeholders, READY/BLOCKED, outbound/inbound separation, LE/EWM deduplication, plant/storage/warehouse integrity, purchase-order dependencies, dependency referential integrity, skipped candidates, cross-document checks, S4600 immutability, and byte-identical deterministic reruns.

## 19. Files generated

Stage artifacts:

- `data/extracted/full/S4610/objects.json`
- `data/normalized/full/S4610/objects.json`
- `metadata/lineage/full/S4610/lineage.json`
- `metadata/lineage/full/S4610/section_inventory.json`
- `metadata/lineage/full/S4610/cross_document_checks.json`
- `metadata/dependencies/full/S4610/dependency_graph.json`
- `metadata/confidence/full/S4610/confidence.json`
- `metadata/confidence/full/S4610/extraction_summary.json`

Implementation and verification:

- `scripts/extract_s4610.py`
- `tests/test_s4610_full.py`
- Updated generated schemas and `scripts/generate_schemas.py`
- `reports/phase1b_s4610_extraction_report.md`

Nothing was published under `data/validated/`.

## 20. GO / NO-GO recommendation for S4615

**GO** for a separately authorized S4615 stage.

The recommendation is supported by complete S4610 parsing, 21/21 schema-valid normalized objects, deterministic output, explicit outbound/inbound separation, correct reference-data promotion, dependency integrity, LE/EWM deduplication, and 36/36 passing tests.

The following controls must carry into S4615:

- Keep the S4600 return-delivery issue open unless S4615 provides explicit directional evidence.
- Treat S4610 delivery objects as read-only dependency candidates.
- Preserve participant placeholders and prior-step references.
- Do not publish to `data/validated/` and do not connect to SAP.

This report does not authorize automatic S4615 extraction. Stage 2 stops at S4610.
