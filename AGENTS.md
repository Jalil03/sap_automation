# AGENTS.md - SAP Sales Canonical Data Preparation & Phase 5 Provisioning

## Mission and boundary

This repository supports multiple phases of the SAP Sales training-data platform.

- Phase 1 transforms immutable SAP Sales PDFs into a normalized, validated, traceable canonical dataset.
- Phase 2 maps the canonical dataset to SAP-specific structures.
- Phase 3 supplies SAP connector/execution foundations.
- Phase 5 performs controlled SAP GUI provisioning, lookup, assignment, and readback operations for the authorized SAP training environment.

Phase 1 remains the default scope for canonical-data work.

Phase 5 SAP GUI provisioning is explicitly in scope when requested by the user.

Phase 5 work may use the repository's existing SAP GUI bridge, provisioning backend, discovery evidence, recorded runtime captures, tests, and execution scripts.

BAPI, RFC, OData, and IDoc integrations remain out of scope unless separately and explicitly authorized by the user.

---

## Phase 1 mandatory rules

1. Resolve S4600, S4610, S4615, S4620, and S4650 through `docs/manifests/documents.json`; preserve filenames/PDFs and verify SHA-256 checksums.

2. Never invent values. Use exactly the classifications and types in `taxonomy/object_types.yaml`.

3. Every object must conform to its schema and contain course code, source file, page, and section type provenance; add chapter/exercise when available.

4. Use `sales_division` for `secteur d'activité` and `plant` for logistical `division`; canonical `division` is forbidden.

5. Preserve `##` unless an explicit non-null mapping exists. Unresolved placeholders are allowed in every lifecycle state; a mandatory one sets `readiness_status: BLOCKED` with a structured reason.

6. Lifecycle values are RAW, EXTRACTED, NORMALIZED, VALIDATED, REJECTED. Readiness is independently READY or BLOCKED.

7. Preserve relative dates semantically. Model prior-step references as dependencies. UI actions are not business data.

8. Instructor exercise/solution pairs use `<COURSE>_CH<chapter>_EX<exercise>`. The exercise is primary; solutions add verification provenance and never a duplicate object.

9. Keep raw, extracted, normalized, validated, rejected, exports, and metadata separate. No normalized/validated object may lack provenance.

10. Prefer deterministic parsing/validation and retain original source terms in lineage.

### Phase 1 authorization

For Phase 1 work, Phase 1A allows manifest verification and foundation tests only.

Full business-object extraction requires explicit Phase 1B authorization.

This Phase 1A/1B restriction applies only to Phase 1 work and does not restrict explicitly authorized Phase 5 work.

---

# Phase 5 SAP GUI Provisioning

## Authorization

Phase 5 SAP GUI provisioning is explicitly authorized when requested by the user for the SAP training environment.

Phase 5 work may modify and use, when necessary:

- `src/sap_gui_bridge/**`
- `src/provisioning/**`
- Phase 5 execution scripts under `scripts/**`
- Phase 5 tests
- SAP GUI protocol definitions
- navigation contracts
- SafetyPolicy allowlists
- runtime discovery tooling
- Phase 4 / Phase 5 discovery evidence
- configuration and seed files related to provisioning

Existing live-proven operations must not be redesigned without evidence of a defect.

---

## Phase 5 execution model

For every Phase 5 business/configuration object, prefer the following deterministic lifecycle:

1. `LOOKUP`
2. If the target already exists:
   - validate/read back what is safely verifiable;
   - continue to the next dependency.
3. If the target is missing:
   - `PROVISION` when the GUI contract is sufficiently evidenced.
4. `READBACK`
5. Continue to the next dependency.

The normal dependency chain for the current S4615 training environment includes:

1. `COMPANY_CODE_1010`
2. `SALES_ORGANIZATION_1010`
3. `SALES_ORG_1010_TO_COMPANY_CODE_1010`
4. `DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010`
5. `DIVISION_00_TO_SALES_ORG_1010`
6. `CUSTOMER_C615_D00`
7. `PRODUCT_P615_400`

Use the seed/configuration files as the authoritative source for the exact target values and templates.

---

## Phase 5 evidence rules

Never invent SAP GUI behavior.

Before implementing a SAP GUI operation, use available repository evidence such as:

- Phase 4 discovery snapshots
- `discovery_steps.jsonl`
- discovery histories
- Phase 5 source-discovery artifacts
- recorded VBS scripts
- runtime captures
- existing navigation constants
- protocol definitions
- seed configuration
- existing tests
- previously live-proven execution paths

Do not invent:

- SAP transaction codes
- IMG node keys
- IMG node text
- table/view names
- control IDs
- control types
- item columns
- activity-dialog rows
- field mappings
- button IDs
- save behavior
- copy behavior
- transport-request behavior
- readback semantics

If required evidence genuinely does not exist, fail closed at that exact unsupported boundary.

---

## Phase 5 safety rules

Phase 5 SAP GUI actions must remain:

- deterministic
- evidence-backed
- allowlisted
- fail-closed
- scoped to the intended SAP object
- validated against the expected SAP system/session identity

Do not globally weaken `SafetyPolicy`.

When an additional action is required:

1. determine the exact primitive used by the evidenced route;
2. allow only that required primitive;
3. constrain it by transaction/control/value when possible;
4. add tests proving unrelated actions remain blocked.

Do not broadly allow all READ actions in EXECUTE mode merely for convenience.

Do not enable unrelated write primitives.

Actions such as save, text modification, creation, deletion, assignment, release, or transport handling may be enabled only where the corresponding Phase 5 operation requires them and repository/live evidence establishes the exact contract.

---

## SAP GUI navigation rules

Prefer reusable deterministic navigation primitives instead of duplicating object-specific scripts.

Reusable concepts may include:

- opening approved transactions
- SPRO / SIMG entry
- IMG tree traversal
- IMG activity opening
- activity-dialog selection
- table lookup
- vertical-scroll scanning
- positioning dialogs
- copy/create workflows
- transport handling
- save
- readback

Object-specific configuration should contain evidence-backed values such as:

- IMG path
- node keys
- node text
- item column
- activity row
- transaction
- program
- control IDs
- SAP table/view
- source template
- target value

Generic helpers must continue validating the exact caller-supplied contract.

Do not globally relax type checks, control-ID checks, transaction checks, or node validation because one SAP screen exposes a different control implementation.

---

## SAP GUI lookup rules

A lookup may return:

- `EXISTS`
- `MISSING`
- `UNKNOWN`

Return `EXISTS` only when the target is deterministically found.

Return `MISSING` only when the implementation can prove that the complete relevant dataset was inspected.

Return `UNKNOWN` when inspection is incomplete, ambiguous, interrupted, or cannot deterministically prove absence.

For scrollable SAP tables:

- use SAP-reported dynamic row counts when available;
- reacquire COM controls after scrolling when required;
- use exact evidenced cell IDs/patterns;
- do not infer absence from only currently visible rows;
- do not use stale/incomplete `table.Children` enumeration when deterministic direct cell access exists.

Scrolling a table for lookup is considered read-only when it does not modify business data.

---

## Phase 5 provisioning rules

Provision only when:

- LOOKUP establishes that the target is missing;
- the source/template is known from authoritative configuration;
- the exact GUI creation/copy workflow is evidenced;
- required controls are known;
- save behavior is evidenced;
- transport behavior is evidenced when SAP requires transport handling.

Never guess the remaining clicks of a partially captured provisioning workflow.

If only a safe prefix of the provisioning flow is evidenced:

- implement the supported deterministic portion when useful;
- fail closed before the unsupported write boundary;
- report the smallest missing runtime evidence needed.

---

## Phase 5 readback rules

After provisioning, verify as much as existing evidence safely supports.

A successful navigation or save is not by itself sufficient proof that provisioning succeeded.

Prefer independent readback of:

- target existence
- assignments
- important copied/configured fields
- relevant SAP identifiers

If only existence can currently be verified, report the operation as existing but do not claim deeper field verification.

Use explicit verification status where supported.

---

## Phase 5 acceleration rules

When Phase 5 is explicitly requested, prioritize end-to-end progress.

Do not intentionally split work into one patch per individual GUI primitive when several consecutive operations are already supported by repository evidence.

Before editing, inspect the relevant evidence for the current operation and the following Phase 5 operations.

Prefer implementing the largest safe consecutive batch possible.

A later unsupported operation must not prevent implementation of earlier operations whose contracts are already sufficiently evidenced.

When useful, summarize readiness as:

| Operation | LOOKUP | PROVISION | READBACK | Implement now |
|---|---|---|---|---|

Then implement all safely supported consecutive operations.

Do not ask the user to perform a new live SAP run after every small internal code change.

Prefer this cycle:

1. inspect evidence for a batch;
2. implement the largest safe batch;
3. run focused tests;
4. perform one live SAP run;
5. inspect the first real runtime boundary;
6. continue from there.

---

## Live-proven behavior

Treat a flow that has successfully executed against the authorized live SAP training session as stronger evidence than an unexecuted assumption.

Do not redesign live-proven flows unless:

- a regression is demonstrated;
- newer runtime evidence invalidates the existing contract; or
- the user explicitly requests redesign.

If code is changed while the SAP GUI local runner is running, remember that the existing Python process may still have old modules loaded.

After SAP GUI bridge/provisioning changes, restart the local runner before evaluating a new live run.

---

## Error handling

Preserve the original SAP/runner error whenever possible.

Runner error responses must be evaluated before success-only SAP identity assertions so that real execution failures are not incorrectly replaced by generic identity-mismatch errors.

Fail-closed errors should identify the exact unsupported boundary whenever possible.

Avoid converting a specific actionable SAP GUI error into a vague generic failure.

---

## Testing requirements

Every Phase 5 patch must include focused automated tests where practical.

Tests should cover:

- successful evidenced route
- wrong control ID
- wrong control type
- wrong transaction/program
- unsupported starting transaction
- wrong/unobserved node or activity
- incomplete lookup
- blocked unrelated write actions
- success/error response handling
- any newly allowlisted SafetyPolicy primitive

Existing unrelated behavior must remain unchanged.

Before requesting another live SAP run:

- run the relevant Phase 5 backend tests;
- run SAP GUI bridge/runner tests;
- check syntax/static diagnostics;
- confirm the expected call chain.

---

## Agent behavior for Phase 5

When the user explicitly requests Phase 5 work:

- do not refuse merely because Phase 1 is the repository's default data-preparation scope;
- Phase 5 SAP GUI provisioning is explicitly authorized by this file;
- inspect evidence first;
- implement rather than only describing a possible solution when the evidence is sufficient;
- preserve strict fail-closed behavior;
- work in the largest safe batch practical;
- do not repeatedly request evidence already present in the repository;
- do not repeatedly ask the user to rerun SAP for internal issues that can be caught through repository inspection or tests.

If progress is blocked by genuinely missing runtime evidence, report:

1. the exact unsupported operation;
2. the exact missing property/control/transition;
3. the smallest live capture necessary to establish it.

Do not block unrelated Phase 5 operations that can already be implemented safely.

---

## Out-of-scope interfaces

Unless the user separately and explicitly authorizes them, do not use:

- BAPI
- RFC
- OData
- IDoc

SAP GUI automation through the repository's controlled Phase 5 framework is explicitly permitted for authorized Phase 5 work.

## Phase 5 live SAP provisioning authorization

For the authorized SAP training environment:

- System: A4H
- Client: 600
- User: ABDELJ

Phase 5 live provisioning is explicitly authorized.

Allowed operations:
- read-only SAP/OData lookups
- OData POST/PATCH required for Phase 5 provisioning
- SAP GUI provisioning already covered by the Phase 5 bridge
- Customer / Business Partner provisioning
- Product / Material provisioning
- Company Code / Sales Organization / assignments provisioning
- independent post-write readback
- persistence of logical-to-SAP identifier mappings

Current authorized Customer continuation:
- existing BP: 1000000114
- logical book customer ID: C615-D00
- do NOT create another BP
- FLCU00 / FLCU01 roles may be added
- A_CustomerCompany for CompanyCode 1010 may be created
- A_CustomerSalesArea for 1010/10/00 may be created

Safety requirements:
- LOOKUP before every write
- no duplicate master-data creation
- stop on SAP error
- use only evidenced metadata/fields
- independent readback after every write
- no production systems
- authorization applies only to A4H client 600 training environment

This Phase 5 authorization overrides earlier Phase 1-only restrictions for the
specific provisioning operations above.