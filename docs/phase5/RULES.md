# Phase 5 Execution Rules

1. Treat live SAP readbacks as the source of truth. Repository seeds and Book-derived facts supply intended target values, not proof of live existence.
2. Perform an exact `LOOKUP` before every write. Skip existing objects; never recreate an object already verified as `EXISTS`.
3. Perform an independent readback after every write before moving to the next dependency.
4. Fail closed when a control, field, value, route, or write/readback contract is unknown or unproven.
5. Prefer interfaces in this order:
   1. Proven OData/API contract
   2. Proven BAPI/RFC contract
   3. Proven SAP GUI automation contract
   4. Minimal human-assisted discovery, only when unavoidable
6. Never guess SAP fields, accounts, plants, identifiers, or required values. Use only live evidence and the applicable Book seed/configuration/mapping.
7. Stop on the first unexpected SAP write error. Preserve the original SAP error and do not retry with a guessed value or alternate unproven route.
8. Do not reuse failed or unproven routes. A route may be reconsidered only after new evidence establishes a corrected contract.
9. Use only SAP system `A4H`, client `600`, user `ABDELJ`; never target production.
10. Update `CURRENT_STATE.md` after every meaningful live state change.
11. Resolve Book-specific values from the seed/configuration/mapping for that Book; do not substitute unrelated template values without evidence.
12. Keep logical Book identifiers separate from generated SAP identifiers and preserve their mappings in project state.
13. Do not hardcode `C615-D00`, `1000000114`, `1010`, `10`, or `00` in generic business logic; such values belong only in Book-specific configuration, fixtures, or tests.
14. If human intervention is required, request exactly one precise action at a time.
