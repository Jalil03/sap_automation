# Phase 1A Foundation Hardening Report

## Outcome

Phase 1A foundation hardening is complete. The five immutable source PDFs resolve by logical course code through the manifest and pass SHA-256 verification. No business objects were extracted and no SAP integration was added.

## Files changed

- Governance and documentation: `AGENTS.md`, `README.md`, relevant repository skills, and the orchestration prompt.
- Source inventory: `docs/manifests/documents.json`, `config/project.yaml`, `scripts/ingest_documents.py`, and `src/ingestion/manifest.py`.
- Taxonomy and terminology: all files under `taxonomy/`, plus `mappings/field_aliases.yaml` and `mappings/normalization_rules.yaml`.
- Canonical coverage: `mappings/document_to_object.yaml` with PRIMARY, SECONDARY, and REFERENCE_ONLY relationships.
- Common contracts: canonical object, source reference, dependency, placeholder, validation, and blocking-reason schemas under `schemas/common/`.
- Object contracts: 38 generated schemas under `schemas/customizing/`, `schemas/master_data/`, `schemas/transactions/`, and `schemas/reference_data/`, indexed by `schemas/index.json`. Obsolete organizational/division and generic delivery schemas were removed.
- Deterministic policies: `src/placeholders/policy.py` and `src/extraction/scenarios.py`.
- Reproducibility and tests: `scripts/generate_schemas.py` and `tests/test_foundation.py`.

## Canonical object inventory

| Classification | Count | Objects |
|---|---:|---|
| CUSTOMIZING | 15 | SALES_ORGANIZATION, DISTRIBUTION_CHANNEL, SALES_DIVISION, SALES_AREA, SHIPPING_POINT, CONDITION_TYPE, CONDITION_TABLE, ACCESS_SEQUENCE, PRICING_PROCEDURE, PRICING_PROCEDURE_DETERMINATION, ACCOUNT_DETERMINATION, COPY_CONTROL, TEXT_DETERMINATION, OUTPUT_DETERMINATION, SHARED_MASTER_DATA_ASSIGNMENT |
| MASTER_DATA | 6 | BUSINESS_PARTNER, MATERIAL, CUSTOMER_MATERIAL_INFO, PRICING_CONDITION, CUSTOMER_HIERARCHY, CONDITION_CONTRACT |
| TRANSACTION | 11 | INQUIRY, QUOTATION, SALES_ORDER, CREDIT_MEMO_REQUEST, RETURN_ORDER, OUTBOUND_DELIVERY, INBOUND_DELIVERY, GOODS_ISSUE, WAREHOUSE_TASK, BILLING, SETTLEMENT_DOCUMENT |
| REFERENCE_DATA | 6 | COMPANY_CODE, PLANT, STORAGE_LOCATION, WAREHOUSE_NUMBER, PURCHASE_ORDER_REFERENCE, PAYMENT_REFERENCE |

`PRO_FORMA_INVOICE` and `INVOICE_LIST` are controlled BILLING subtypes. Billing plans, down payments, and installment payments are nested BILLING structures.

## Taxonomy and schema coverage

The taxonomy contains exactly four top-level classifications and 38 object types. Every type has one indexed schema with enforced `object_type` and `classification` constants and meaningful, source-supported optional business fields. All objects inherit common requirements for provenance, lifecycle, readiness, blocking reasons, dependencies, placeholders, and validation metadata.

The ambiguous canonical `division` field was removed. `sales_division` represents French `secteur d'activité`; `plant` represents the logistical French term `division`. Original terms remain available in source lineage.

## Policy behavior

- Lifecycle: RAW, EXTRACTED, NORMALIZED, VALIDATED, REJECTED.
- Readiness: READY or BLOCKED.
- Unresolved placeholders remain valid in all lifecycle states. Mandatory unresolved placeholders create `UNRESOLVED_MANDATORY_PLACEHOLDER` blocking reasons.
- Scenario IDs use `<COURSE>_CH<chapter>_EX<exercise>`. Exercises are primary; matching solutions are verification provenance and do not create another object.

## Test results

Command: `python -m unittest discover -s tests -p "test_*.py" -v`

Result: **8 tests passed, 0 failed**. Coverage includes source resolution and checksum verification, schema JSON/reference validity, taxonomy-to-schema completeness, constants, provenance, lifecycle/readiness enums, placeholder resolution, terminology disambiguation, exercise/solution deduplication, and coverage-matrix validity.

The manifest-only ingestion check also resolved and verified all five source documents successfully.

## Unresolved design questions

- Extraction evidence may justify additional optional business fields; additions must remain source-backed and backward compatible.
- EWM storage types, sections, and bins remain nested/reference attributes rather than top-level objects unless Phase 1B evidence requires promotion.
- Billing subtype vocabulary may need expansion beyond STANDARD, PRO_FORMA_INVOICE, and INVOICE_LIST based on extracted exercises.

## Recommendation

**GO for Phase 1B extraction**, provided it begins with a small representative pilot and retains the schema, provenance, placeholder, readiness, and deduplication gates implemented here. Phase 2 mapping and Phase 3 SAP connectivity remain explicitly out of scope.
