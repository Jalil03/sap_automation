# S4615 functional reference discovery

**Mode:** retained repository evidence only; no SAP connection or API call was made. No SAP object was created, changed, or mapped.

## Result

No candidate can be classified as `FUNCTIONALLY_VALID_TEMPLATE` or `PARTIAL_TEMPLATE` from captured SAP readbacks. The retained same-family inspection plan explicitly says customer/product GET results were `NOT_CAPTURED` and `resolved_fields` were empty. A new SAP read would be required to verify candidate existence, views, and field values; it was not performed.

| Target | Best candidate(s) in retained evidence | Classification | Evidence and limitation |
|---|---|---|---|
| `C615-A01` | `C615-A00` (first same-family customer candidate); `C615-B00` (secondary) | `NOT_FOUND` | Listed in `data/provisioning/s4615_user00_blocker_resolution.json` as `EVIDENCE_TEMPLATE_ONLY_NEVER_SUBSTITUTE`, but both have `captured_repository_result: NOT_CAPTURED`, classification `UNKNOWN`, and no resolved fields. They are Book-family candidates, not verified SAP objects. |
| `P615-101` | `P615-100` (first same-family product candidate); `P615-200` (secondary) | `NOT_FOUND` | Listed in the same inspection record as evidence-only candidates, but GET results are `NOT_CAPTURED`, classification `UNKNOWN`, and resolved fields are empty. The requirements record explicitly warns that another product's PC association does not prove P615-101's association. |

`NOT_FOUND` here means **no candidate readback is present in the repository evidence**, not proof that the objects are absent in SAP. The latest retained environment report says `C615-A01` and `P615-101` were not created and had no verified mapping. It identifies only the excluded `C615-D00` and `P615-400` mappings as verified S4615 identities. Neither excluded object was used as a template.

The seed references customer technical template `17100002` for the D00 operation and product template `FG228` in the P400 operation. Those seed references do not provide target-specific live readbacks or prove functional equivalence for A01/P101. No values were borrowed from them.

## Values that can safely be reused

These are Book/common-environment values, not attributes inferred from a candidate:

| Value | Safe use | Source / limit |
|---|---|---|
| Customer sales area `1010/10/00` and company code `1010` | Scenario organizational context for C615-A01 | S4615 provisioning facts and retained current-state report; does not verify A01 company/sales views |
| Product sales organization `1010`, distribution channel `10`, sales division `00` | Scenario organizational context for P615-101 | Canonical S4615 sales-order records and retained current-state report; does not verify P101 product views |
| Product order unit `PC` | Preserve as the Book's order-unit requirement | S4615 canonical sales-order items and `REQ_PRODUCT_UNIT_OF_MEASURE_6A96CF240FB0`; does **not** prove base unit or an existing PC association |
| Logical IDs `C615-A01` and `P615-101` | Resolve the Book family placeholders for group 01 | Deterministic identifier substitution only; no business data inferred |

No target-specific customer or product master-data value from a functional SAP reference can safely be reused on the captured evidence.

## Remaining unresolved values

**C615-A01 customer:** BP grouping, roles, reconciliation account, payment terms, customer currency, shipping condition, delivering plant, Incoterms, account assignment group, customer pricing procedure, tax classifications, partner functions, and existence/identity of a compatible root customer with company-code and sales-area views. Name/address are intentionally outside this discovery and remain training-specific.

**P615-101 product:** material type, industry sector, base unit, product group, plant, delivering plant, item category group, tax classification, availability check, alternative units and conversion, product-specific PC association, required sales/plant views, and whether required accounting/valuation views exist.

No accounting/valuation-view readback for a candidate that avoids the known 10000287/1710/C+039 issue is present in the retained evidence. No product candidate can therefore be qualified for the requested sales order → delivery → PGI → billing flow.

## Readiness impact

- **C615-A01:** remains **MISSING/ADMIN_REQUIRED**; it cannot move to `READY` or candidate-derived `PARTIAL` based on this repository-only discovery. No compatible customer reference values were captured.
- **P615-101:** remains **MISSING/BLOCKED**; it cannot move to `READY` or candidate-derived `PARTIAL`. `PC` remains a Book requirement only, and no safe product reference or valuation evidence was captured.

## Evidence reviewed

- `data/provisioning/s4615_user00_blocker_resolution.json` — planned same-family GET inspections, each marked `NOT_CAPTURED`, with empty resolved fields.
- `data/provisioning/phase5_identity_mappings.json` — retained verified identity mappings; neither target nor eligible reference is mapped.
- `reports/sap_training_environment_current_state.md` — target status, exclusions, and common organizational setup.
- `data/requirements/training_environment_requirements.json` — target-family requirements, including the unresolved product-specific PC association.
- `config/s4615_training_seed.yaml` — D00/P400 technical-template references; not treated as proof of A01/P101 equivalence.
- `src/provisioning/sap_api_backend.py` — existing OData reads/writes inspected as code only; no backend was instantiated or executed.
