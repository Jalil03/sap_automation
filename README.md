# SAP Sales Data Platform

This repository prepares a traceable, protocol-independent canonical dataset from five SAP Sales course PDFs.

## Architecture and scope

- Phase 1 (complete): PDFs -> canonical validated dataset.
- Phase 2A (complete): offline SAP interface inventory audit.
- Phase 2B (complete, scoped): offline canonical dataset -> SAP payload mapping for the resolved writable core flow.
- Phase 2C (complete, scoped): strict local payload/runtime-contract validation and deterministic snapshots.
- Phase 3 (out of scope): SAP mapper -> connector/execution.

Phase 1 and Phase 2 never connect to SAP. PDFs are immutable and resolved by logical course name through `docs/manifests/documents.json`; original filenames are preserved. Phase 2 mapping code under `src/sap_mapping/` contains no connector or transport behavior; BLOCKED objects require explicit structural-fixture mode and are never execution-ready.

Objects use exactly `CUSTOMIZING`, `MASTER_DATA`, `TRANSACTION`, and `REFERENCE_DATA`. Every object carries strict provenance, lifecycle and readiness status, dependencies, placeholders, validation metadata, and typed business data. Unresolved mandatory placeholders remain valid but set readiness to `BLOCKED`.

French `secteur d'activité` maps to `sales_division`; logistical French `division` maps to `plant`. Instructor exercise/solution pairs share `<COURSE>_CH<chapter>_EX<exercise>`: the exercise is primary and the solution is verification provenance.

Run `python -m unittest discover -s tests -p "test_*.py"`. `scripts/ingest_documents.py` only verifies manifest sources and checksums; full extraction remains disabled.

## Golden Book offline demonstration

The S4615 chapter 4 exercise 5 Golden Book view reuses canonical object
`S4615_CH4_EX5_SALES_ORDER_CASH_SALE`, resolves training placeholders only in a
runtime copy, displays the extracted cash-sale/pro-forma workflow, the offline
SAP mapping, and seven fail-closed read-only prechecks.

```powershell
.venv\Scripts\python.exe -m src.golden_book --serve --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/`. This local view performs no SAP call and exposes
no write endpoint; SAP validation remains GET/read-only only.
