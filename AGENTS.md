# AGENTS.md — SAP Training Data & Provisioning

## 1. Mission

This repository prepares and provisions SAP training environments from the SAP Sales books.

Main scopes:

- Phase 1: extract and normalize Book data.
- Phase 2: map canonical data to SAP structures.
- Phase 3: SAP integration/runtime foundations.
- Phase 5: audit, provision, and validate the authorized SAP training environment.

Do not invent SAP or Book values.

---

## 2. Authorized SAP environment

Live SAP work is authorized only for:

- System: A4H
- Client: 600
- User: ABDELJ

Never use production systems.

---

## 3. Live SAP access policy

### READ operations

For authorized Phase 5 work, live SAP READ operations are explicitly allowed.

Allowed READ methods include:

- OData GET
- SAP GUI navigation and inspection
- read-only RFC/BAPI when supported
- table/view lookup
- metadata inspection
- independent readback

READ-ONLY discovery must not be refused because of older Phase 1/2 restrictions.

### WRITE operations

SAP writes are allowed only for explicitly authorized Phase 5 provisioning operations.

Possible write mechanisms:

- approved OData POST/PATCH
- approved SAP GUI provisioning
- approved BAPI/RFC write route when explicitly evidenced and authorized

Every write must:

1. perform LOOKUP first;
2. avoid duplicate creation;
3. use evidenced fields/contracts only;
4. stop on SAP error;
5. perform independent READBACK;
6. remain restricted to A4H client 600.

Never perform an unsupported or guessed write.

---

## 4. Phase 1 canonical-data rules

For Book extraction and canonical data:

- preserve source provenance;
- preserve `##` until an explicit mapping exists;
- never invent missing values;
- use `sales_division` for secteur d'activité;
- use `plant` for logistical division;
- keep extraction, normalization, validation, rejected data, and metadata separate;
- model dependencies explicitly;
- prefer deterministic parsing and validation.

Phase 1 restrictions apply only to Phase 1 work.

They do not prohibit explicitly authorized Phase 5 SAP access.

---

## 5. Phase 5 execution model

Preferred lifecycle:

1. LOOKUP
2. classify:
   - EXISTS
   - MISSING
   - UNKNOWN
3. PROVISION only when required and supported
4. READBACK
5. continue to the next dependency

Rules:

- EXISTS only when deterministically verified.
- MISSING only when absence is reliably proven.
- otherwise return UNKNOWN.
- fail closed when evidence is incomplete.

Do not infer absence from only visible SAP GUI rows.

---

## 6. API-first strategy

For provisioning and discovery, prefer:

1. OData / supported API
2. supported BAPI/RFC
3. SAP GUI fallback

Use SAP GUI when:
- no proven API route exists;
- the Book requires GUI validation;
- the operation is customizing-specific and only the GUI route is evidenced.

Do not redesign a live-proven route without a demonstrated reason.

---

## 7. Evidence rules

Use repository and live evidence such as:

- Book canonical data
- seed/configuration
- interface registry
- SAP metadata
- live readbacks
- SAP GUI discovery
- runtime captures
- existing tests
- previously proven execution paths

Never invent:

- transaction codes
- SAP table/view names
- control IDs
- API fields
- mappings
- save/copy behavior
- business values
- provisioning templates

If evidence is missing, report the exact missing information.

---

## 8. Master-data policy

Training objects may use:

- Book-defined values;
- verified common SAP environment values;
- values derived deterministically from placeholders;
- functionally compatible SAP reference objects when equivalence is verified.

Do not copy a reference object merely because its ID is similar.

For every derived field, preserve its source and confidence.

---

## 9. Safety

Default behavior:

- READ: allowed for authorized Phase 5 work.
- WRITE: gated.
- unsupported write: blocked.

Never globally weaken safety controls.

No CREATE / UPDATE / DELETE / SAVE unless the current Phase 5 operation explicitly requires and supports it.

---

## 10. Testing

For code changes:

- run focused tests first;
- do not run unrelated expensive tests unless needed;
- preserve existing behavior;
- test new safety boundaries;
- never use unit tests to perform live SAP writes.

Live SAP discovery should be narrow and goal-oriented.

---

## 11. Agent behavior

When Phase 5 is requested:

- proceed with authorized READ operations;
- do not confuse Phase 1 restrictions with Phase 5;
- reuse existing code before creating new infrastructure;
- prefer the smallest useful live discovery;
- avoid broad rediscovery;
- stop early when sufficient evidence is obtained;
- preserve fail-closed behavior.

If blocked, report only:

1. the exact blocked operation;
2. the exact missing evidence or capability;
3. the smallest next action required.

---

## 12. Current S4615 constraints

Known exclusions / blockers must be respected:

- `C615-D00` must not automatically be treated as a template for `C615-A01`.
- `P615-400 / 10000287` must not automatically be treated as a template for `P615-101`.
- `10000287 / valuation area 1710 / C+039` is a separate FI/CO Material Ledger issue.
- Do not automatically modify Material Ledger or global currency configuration.

Current objective:

Prepare S4615 master data and environment using API-first provisioning,
SAP GUI fallback where required, and independent readback validation.

---

## 13. Autonomous Phase 5 training execution

Two opt-in modes are available for an explicitly authorized workflow:

- `CONTROLLED_FIRST_WRITE`: an evidenced, scoped contract may perform its first
  write without a prior successful write. Record the attempt before sending it;
  never automatically repeat an ambiguous or failed write.
- `AUTONOMOUS_TRAINING`: execute routine training master-data steps within one
  recorded workflow-level approval, without asking again for every step. Resume
  from durable checkpoints and continue independent branches when one blocks.

Neither mode grants SAP authorization by itself. Before each write, verify the
actual A4H/600/ABDELJ identity, exact operation and target scope, current
absence, approved values, and an evidenced API/BAPI or GUI write contract.
An approval may be reused only for the operations and scope it names; never
infer or fabricate approval from a seed, technical access, or prior success.
Bind each approved operation to a fingerprint of its exact target and write
values; changing either requires a new scoped approval.

Routine training master-data writes may use `TRAINING_MASTER_DATA` approval.
FI/MM and reconciliation data, tax decisions, organizational/customizing
changes, and Material Ledger each require separate explicit approval for the
exact operation. Unknown accounting or tax values remain blocked. Canonical
Book data stays immutable.

Recover automatically only from a backend-certified failure that occurred
before any write (for example, a transient READ). An SAP write with an
ambiguous outcome requires reconciliation by independent READ; never blindly
retry it. Checkpoint every attempted or verified write and continue other
independent approved operations. Prefer concise progress updates and one
precise human checkpoint only when unavoidable.
