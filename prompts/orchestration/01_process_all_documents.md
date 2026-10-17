Process all PDFs in `docs/source/` according to `AGENTS.md` and the repository skills.

Goal: produce a protocol-independent canonical dataset only. Do not connect to SAP.

For every source document:
1. register the document in `docs/manifests/documents.json`;
2. extract relevant exercises/tables/field-value structures into `data/extracted/`;
3. classify objects using `taxonomy/object_types.yaml`;
4. normalize them to the schemas in `schemas/` and write to `data/normalized/`;
5. build dependencies and placeholder metadata;
6. validate and place records in `data/validated/` or `data/rejected/`; represent unresolved operational concerns through `readiness_status: BLOCKED` and structured reasons;
7. generate JSON and CSV exports under `data/exports/`;
8. generate coverage, lineage, unresolved-placeholder, duplicate, and validation reports under `metadata/`.

Every important value must remain traceable to its source PDF/page.
Never invent values to make a record pass validation.
