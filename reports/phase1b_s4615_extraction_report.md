# Phase 1B Stage 3 — S4615 extraction report

## 1. Scope and source verification

Stage 3 processed S4615 only. The source was resolved through `docs/manifests/documents.json` as `docs/source/S4615_FR_Col12_ILT_FV_Inst_A4.pdf`.

- Manifest version: 12, instructor edition, French.
- Physical pages: 263 of 263 parsed.
- SHA-256: `c43431aca0d15add006a5872ac721ef7ffd16e89520195a47b47d7f98ac387d9`.
- Checksum: verified against the manifest.
- Exercise/solution pairs: 13/13 detected.
- Table markers (`Valeur de données`): 33.
- Source PDF: unchanged.
- S4600 and S4610: read-only cross-document checks only; both normalized artifact hashes remained unchanged.
- S4620: not processed.
- No SAP connection, mapper, connector, BAPI, RFC, OData, IDoc, or SAP GUI automation was used.

## 2. Complete-document processing

All physical pages 1–263 were parsed. Exercise start pages were 13, 29, 41, 61, 73, 97, 119, 137, 145, 173, 189, 213, and 235. Matching solution starts were 16, 30, 43, 63, 75, 100, 123, 139, 147, 175, 192, 216, and 238.

The deterministic decision for each exercise is stored in `metadata/lineage/full/S4615/section_inventory.json`.

- Exercise 2 is primarily navigation and organizational review; only company code 1010 was retained as a required reference.
- Exercise 8 is explicitly a simulation that is not saved; no billing instance was created.
- Exercises 1, 3–7, and 9–13 supplied qualifying billing, transaction, Customizing, or dependency instances.
- Concrete instructor demonstrations for invoice lists (pages 152–153) and installment payments (pages 199–200) were extracted.
- The appendix output-management explanation was reviewed but did not contain a concrete output-determination record.

## 3. Canonical object counts

| Object type | Coverage role | Count |
|---|---|---:|
| ACCOUNT_DETERMINATION | PRIMARY | 1 |
| COPY_CONTROL | PRIMARY | 2 |
| BILLING | PRIMARY | 24 |
| SALES_ORDER | SECONDARY | 11 |
| OUTBOUND_DELIVERY | SECONDARY | 8 |
| OUTPUT_DETERMINATION | SECONDARY | 0 |
| COMPANY_CODE | REFERENCE_ONLY | 1 |
| PAYMENT_REFERENCE | REFERENCE_ONLY | 1 |
| **Total** |  | **48** |

Classification totals are 43 `TRANSACTION`, 3 `CUSTOMIZING`, and 2 `REFERENCE_DATA` objects.

The reference-only objects were promoted only because qualifying billing/accounting objects require company-code or payment dependencies. No reference-only theory mention became a first-class record.

## 4. Extracted and normalized layers

- Extracted objects: 48, written with `lifecycle_status=EXTRACTED`.
- Normalized objects: 48, written with `lifecycle_status=VALIDATED`.
- Duplicate object IDs: 0.
- Extracted-to-normalized grain: one-to-one.

Original source terms and excerpts remain in lineage. Exercise evidence is primary; solution evidence verifies or enriches the same canonical object.

## 5. Billing and billing-subtype handling

The 24 billing objects cover the following source-backed semantics without adding taxonomy types:

- `STANDARD`: delivery- and order-related invoices, including F1, F2, and participant-specific ZF##.
- `CASH_SALE`: BV cash-sale billing with cash, revenue, and output-tax accounting semantics.
- `PRO_FORMA_INVOICE`: F5 order-related pro forma billing with no FI transfer by design.
- `CREDIT_MEMO`: a correction/credit result linked to the original F2 invoice and the RK correction request.
- `INVOICE_LIST`: one invoice list containing two demonstrated billing documents.
- `PERIODIC`: the first billed period of a maintenance-contract billing plan.
- `DOWN_PAYMENT_REQUEST`: FAZ billing for a down-payment request.
- `PARTIAL_BILLING`: first partial invoice with down-payment clearing through condition AZWR.
- `INSTALLMENT_INVOICE`: one F2 billing document with installment terms R001 and multiple FI customer entries.

Billing identifiers left blank in the course remain null. Relative dates such as `dans une semaine`, `date du jour + 10 jours`, `fin du mois`, and `dernier jour du mois` remain semantic relative values.

## 6. Billing references and dependency graph

- Dependency edges: 66.
- Resolved canonical edges: 34.
- Unresolved source-reference edges: 32.
- Critical unresolved edges: 10.

Unresolved edges by target type are 11 business partners, 11 materials, 5 outbound deliveries, 3 sales orders, 1 credit-memo request, and 1 sales-contract reference. Business-partner and material edges are noncritical context; prior-document references required to use a billing object are critical.

Representative chains are:

1. Exercise 3 fair order → outbound delivery → ZF## billing, controlled by the shared fair-billing copy-control record.
2. Exercise 5 cash-sale order → automatically created delivery → BV billing.
3. Exercise 5 standard order → F5 pro forma billing, with FI transfer explicitly not applicable.
4. Exercise 6 fair order → outbound delivery → ZF## billing with freight re-determination type H.
5. Exercise 7 order → delivery → month-end billing.
6. Exercise 11 order → FAZ down-payment request → payment reference → first partial billing.
7. Exercise 12 order → delivery → billing → account-determination record → G/L account 49000000.
8. Exercise 13 two fair orders → deliveries → ZF## billings → manual FI release.

No missing SAP document number was fabricated.

## 7. Invoice-list and pro-forma findings

The invoice-list demonstration creates two source billing records for purchase-order references `00S4615-A11` and `00S4615-A12`, both paid by `C615-GC00`, followed by one canonical `BILLING` object with subtype `INVOICE_LIST`. Its two `CONTAINS` dependencies are explicit and resolved.

The pro forma exercise creates one `BILLING` object with type F5 and subtype `PRO_FORMA_INVOICE`. Its `accounting_status` is `NOT_APPLICABLE_PRO_FORMA`, matching the explicit source statement that no accounting document is created and no data is sent to FI.

## 8. Billing plans, down payments, and installments

- Periodic billing: one first-period billing object retains plan type 02, item category WVN, date category 01, monthly quantity calculation rule M, and billed status C.
- Down payment: the FAZ request, posted payment reference, first partial billing, and AZWR clearing semantics are preserved. The explicit tax-inclusive payment amount is 33000; currency is null because the source does not specify it.
- Installments: one billing document retains payment terms R001 and the source rule that a single billing document produces multiple FI customer entries. The number and percentages of installments remain unset because the source does not provide them.

No billing-plan, down-payment, or installment-payment taxonomy type was added; all remain nested BILLING structures as required by the foundation model.

## 9. Account determination and FI/CO metadata

Exercise 12 produced one `ACCOUNT_DETERMINATION` object with:

- application V;
- condition type KOFI;
- procedure KOFI00 and access sequence KOFI;
- condition table 001;
- chart of accounts YCOA;
- sales organization 1010;
- customer account-assignment group `80+##`;
- material account-assignment group 01;
- account key ERL;
- G/L account 49000000.

Qualifying billing objects retain explicit FI/CO dependency metadata: posted, blocked pending manual release, no accounting entry, pro-forma not applicable, down-payment posting/clearing, invoice-list reference replacement, or multiple installment receivable items. No FI or CO document identifier was invented.

## 10. Schema validation

- Normalized objects valid: 48/48.
- Normalized objects invalid: 0/48.
- Extracted objects valid: 48/48.
- Validator: Draft 2020-12 schemas through the repository schema registry.

Every object includes classification, scenario ID, provenance, lifecycle/readiness, structured placeholders, dependencies, validation metadata, confidence, and canonical business data.

## 11. READY and BLOCKED

| Readiness | Count |
|---|---:|
| READY | 5 |
| BLOCKED | 43 |

Blocking-reason occurrences are:

- `UNRESOLVED_MANDATORY_PLACEHOLDER`: 39 objects.
- `UNRESOLVED_CRITICAL_DEPENDENCY`: 10 objects.
- `DEPENDENCY_NOT_READY`: 22 objects.

Counts overlap because an object can have multiple reasons. `VALIDATED/BLOCKED` means the extraction is structurally and semantically valid while participant-specific or prerequisite data prevents downstream use.

## 12. Placeholder results

- Placeholder occurrences: 70.
- Objects with placeholders: 39.
- Resolution status: all remain `UNRESOLVED` with `resolved=null`.
- Explicit mapping used: none; `mappings/placeholders.yaml` supplies no participant assignment.

Examples include `C615-A##`, `P615-1##`, `ZA##`, `ZF##`, `##S4615-KO`, `##S4615-Réf`, and the account-assignment expression `80+##`. No group number was inferred.

## 13. Exercise/solution deduplication

- Each exercise-primary object has one deterministic object ID.
- Solution sections add verification or enrichment provenance and never create a duplicate object.
- The fair-billing copy-control object is enriched across Exercises 3, 6, 9, and 13 because all four sections configure the same ZF##/LF relationship.
- The invoice-list and installment datasets are demonstrations rather than exercise/solution pairs and are explicitly labeled `DEMONSTRATION`.
- The Exercise 8 simulated invoice is not duplicated as a saved billing object.

## 14. Confidence summary

| Confidence | Count |
|---|---:|
| HIGH | 39 |
| MEDIUM | 7 |
| LOW | 2 |

The two LOW-confidence records are the two Exercise 9 split invoices. The source proves that two F1 invoices were created and saved but leaves both delivery and billing identifiers blank. They are retained as separate, source-counted instances with unresolved delivery dependencies.

MEDIUM confidence covers pre-imported billings whose identifiers or source delivery numbers are blank, the month-end invoice with a relative date, and the two invoice-list source billings whose purchase-order references are explicit but generated billing identifiers are not.

## 15. Skipped and rejected candidates

- Exercise 2 UI/navigation steps: not business data.
- Exercise 7 initial batch of three pre-existing due-list invoices: known aggregate count, but indistinguishable source deliveries and blank identifiers; no synthetic objects were created.
- Exercise 8 grouped-invoice simulation: explicitly not saved.
- External billing document requests: no approved EBDR canonical type and no completed source instance.
- Appendix output management: theoretical BRFplus/NAST explanation only; no concrete `OUTPUT_DETERMINATION` record.
- Generic FI/CO posting examples: retained as semantic context, not independent accounting objects.
- Billing-type configuration has no standalone taxonomy type; it is retained on BILLING and COPY_CONTROL records.

No object was written with `lifecycle_status=REJECTED`; nonqualifying candidates are deterministic skips with documented reasons.

## 16. Contradictions, ambiguities, and data-quality findings

| Finding | Evidence | Severity | Confidence | Control |
|---|---|---|---|---|
| Participant values unresolved | 70 occurrences across 39 objects | Medium | High | Preserve placeholders and block readiness |
| Generated document identifiers blank | Multiple exercise result fields | Medium | High | Use null IDs and canonical source-based object IDs |
| Exercise 9 split invoices indistinguishable | Two invoices saved; source delivery IDs blank | Medium | High | LOW confidence and unresolved delivery dependencies |
| Exercise 7 initial batch lacks stable grain | Three invoices cancelled, but source records are not distinguishable | Medium | High | Skip batch instances rather than invent ordinal identities |
| Down-payment currency absent | Amount 33000 is explicit, currency is not | Medium | High | Retain amount and null currency |
| Installment breakdown absent | R001 and multiple FI entries are explicit; count/percentages are not | Low | High | Retain empty schedule details |
| Pro forma accounting semantics differ from standard billing | Explicitly no FI transfer | High if conflated | High | Dedicated controlled BILLING subtype and accounting status |
| Copy-control settings accumulate over exercises | H, routine 3, B, and E are configured successively | Medium | High | One enriched relationship with complete provenance |

Key uniqueness, completeness, domain validity, exercise/solution duplication, dependency integrity, schema drift, and deterministic output were tested. Temporal freshness and distribution drift are not applicable to this static training-document extraction.

## 17. Cross-document checks and S4600 return issue

- S4600 normalized artifact SHA-256 remained `4b5b38be6c9a291db6ffbe010a87e8f73d670f25e346d23da0a157881d519319`.
- S4610 normalized artifact SHA-256 remained `8e4a94dea69465af58c89b8c661dfa8ec41b719799d24e59cc588e413f661889`.
- S4615 contains no explicit identifier that joins a staged S4600 or S4610 object; no cross-course dependency was guessed.
- S4615 supplies no explicit directional evidence for `S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER`.
- The S4600 customer-return delivery issue remains `UNRESOLVED_CARRIED_FORWARD`; no S4600 file was modified.

## 18. Schema and taxonomy changes

The smallest source-justified, backward-compatible schema additions were made:

1. `BILLING` now supports billing/accounting status, payment terms, net value/currency, posting-block state, and structured FI/CO dependency metadata.
2. Billing items can retain net value, currency, sales division, and source condition values.
3. `ACCOUNT_DETERMINATION` now supports application, condition type, procedure, access sequence, condition table, sales organization, and customer/material account-assignment groups.
4. `COPY_CONTROL` now supports source item category, pricing type, data-transfer routine, reference/assignment rules, billing-quantity rule, and positive/negative quantity semantics.
5. `PAYMENT_REFERENCE` now supports bank account, special G/L indicator, and payment status.

No taxonomy type was added. Invoice lists and pro forma documents remain BILLING subtypes; billing plans, down payments, and installment payments remain nested structures.

## 19. Test results

Command: `.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`

- Tests run: 46.
- Passed after the publication-guard correction: 46.
- Failed/errors: 0.
- Foundation, pilot, S4600, and S4610 regression tests remain green.
- Stage 3 tests cover stable counts, unique IDs, schema compliance, lifecycle, provenance, exercise/solution deduplication, placeholders, READY/BLOCKED semantics, billing subtypes, FI/CO metadata, invoice-list containment, billing plans, down payments, installments, account determination, copy control, relative dates, dependency integrity, prior-stage immutability, return-issue carry-forward, production-publication prevention, and byte-identical deterministic reruns.

## 20. Files generated

Stage artifacts:

- `data/extracted/full/S4615/objects.json`
- `data/normalized/full/S4615/objects.json`
- `metadata/lineage/full/S4615/lineage.json`
- `metadata/lineage/full/S4615/section_inventory.json`
- `metadata/lineage/full/S4615/cross_document_checks.json`
- `metadata/dependencies/full/S4615/dependency_graph.json`
- `metadata/confidence/full/S4615/confidence.json`
- `metadata/confidence/full/S4615/extraction_summary.json`

Implementation and verification:

- `scripts/extract_s4615.py`
- `tests/test_s4615_full.py`
- Updated generated schemas and `scripts/generate_schemas.py`
- `reports/phase1b_s4615_extraction_report.md`

Nothing was published under `data/validated/`; the pre-existing `.gitkeep` is unchanged.

## 21. GO / NO-GO recommendation for S4620

**GO** for a separately authorized S4620 stage.

The gate is supported by complete S4615 parsing, 48/48 schema-valid normalized objects, deterministic output, explicit billing subtype semantics, preserved FI/CO relationships, tested invoice-list and special-billing structures, dependency integrity, and 46/46 passing tests.

Controls to carry into S4620:

- Treat all S4600/S4610/S4615 staged artifacts as read-only dependency candidates.
- Preserve participant placeholders and relative dates.
- Keep condition records distinct from billing condition snapshots.
- Do not publish to `data/validated/` and do not connect to SAP.
- Keep the S4600 return-delivery issue open unless S4620 provides explicit directional evidence.

This report does not authorize automatic S4620 extraction. Stage 3 stops at S4615.
