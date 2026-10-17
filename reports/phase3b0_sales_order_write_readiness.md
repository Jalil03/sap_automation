# The SALES_ORDER pilot payload is prepared, but live pre-checks still block execution

## Executive summary

- The only `EXECUTION_READY` candidate is `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT`, sourced from S4615 chapter 8, page 200.
- Its exact proposed deep-insert body targets `API_SALES_ORDER_SRV/A_SalesOrder` and contains 7 header fields, one external sold-to partner row, and one item. It contains no CSRF token, credentials, SAP-generated order ID, inferred ship-to/bill-to/payer, plant, shipping point, date, schedule line, pricing row, or internal partner code.
- The payload passes the current strict local contract and every emitted field is present and creatable in metadata. Runtime evidence confirms the service/entity names, read-side item/partner relationships, field names, and GET representations—but not POST/deep-insert behavior.
- **NO-GO for the write pilot now.** All 11 SAP dependency/configuration checks are still unexecuted. The gate may be reconsidered only after every check passes, duplicate checks are clear, CREATE authorization is explicitly confirmed, and the individual pilot execution is separately authorized.

No SAP connection or HTTP request was made. No token was captured or stored, no production connector was implemented, and no write occurred.

## Candidate selection

Re-evaluating all 57 canonical SALES_ORDER objects through the current runtime contract produced:

| Runtime status | Count |
|---|---:|
| `EXECUTION_READY` | 1 |
| `BLOCKED` | 56 |

Selected object:

| Attribute | Value |
|---|---|
| Canonical object ID | `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT` |
| Scenario | `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS` |
| Source | `S4615_FR_Col12_ILT_FV_Inst_A4.pdf`, page 200, demonstration |
| Confidence | HIGH |
| Canonical readiness | READY |
| Mapper runtime status | EXECUTION_READY |
| Placeholders | None |
| Critical unresolved dependencies | None |

Its two canonical dependencies—customer `C615-A00` and material `P615-100`—are noncritical at canonical extraction time but become mandatory live pre-checks before a write.

## Exact proposed request

Target: `API_SALES_ORDER_SRV` / `A_SalesOrder`

```json
{
  "CustomerPaymentTerms": "R001",
  "DistributionChannel": "10",
  "OrganizationDivision": "00",
  "PurchaseOrderByCustomer": "4712",
  "SalesOrderType": "OR",
  "SalesOrganization": "1010",
  "SoldToParty": "C615-A00",
  "to_Item": [
    {
      "Material": "P615-100",
      "RequestedQuantity": 10,
      "RequestedQuantityUnit": "PC",
      "SalesOrderItem": "10"
    }
  ],
  "to_Partner": [
    {
      "Customer": "C615-A00",
      "PartnerFunction": "DO"
    }
  ]
}
```

Canonical JSON SHA-256: `fee6311451a3cfb8d0e09501f86c5596e4fcec46f272fcc88376d36a28605c33`.

The provided partner evidence establishes external `DO` → internal `AG` → *Donneur d'ordre*. The payload therefore writes `PartnerFunction: "DO"`. It does not write `AG` or `PartnerFunctionInternalCode`; metadata marks `PartnerFunctionInternalCode` non-creatable and non-updatable. The other evidenced mappings (`RM`/`WE`, `RF`/`RE`, `PY`/`RG`) are not emitted because the canonical candidate contains no corresponding partner values.

## Field validation

| Payload path | Value | Metadata / contract | Runtime evidence | Write conclusion |
|---|---|---|---|---|
| `SalesOrderType` | `OR` | `Edm.String`, MaxLength 4, creatable; mapped | Field name/string confirmed | Value requires live document-type pre-check |
| `SalesOrganization` | `1010` | `Edm.String`, MaxLength 4, creatable; mapped | Field name/string confirmed | Requires live existence/configuration check |
| `DistributionChannel` | `10` | `Edm.String`, MaxLength 2, creatable; mapped | Field/value representation confirmed | Requires assignment check |
| `OrganizationDivision` | `00` | `Edm.String`, MaxLength 2, creatable; mapped | Field/value representation confirmed | Requires valid 1010/10/00 sales-area check |
| `SoldToParty` | `C615-A00` | `Edm.String`, MaxLength 10, creatable; mapped | Field name/string confirmed | Customer value requires live check |
| `PurchaseOrderByCustomer` | `4712` | `Edm.String`, MaxLength 35, creatable; mapped | Not selected in runtime sample | Metadata/contract valid; exact write remains unproven |
| `CustomerPaymentTerms` | `R001` | `Edm.String`, MaxLength 4, creatable; mapped | Not selected in runtime sample | Terms require live configuration check |
| `to_Partner` | one row | Navigation to header partners, multiplicity `*` | Read relationship confirmed | Nested POST remains unproven |
| `to_Partner[0].PartnerFunction` | `DO` | `Edm.String`, MaxLength 2, non-null, creatable | `DO` observed at runtime; supplied mapping identifies sold-to semantics | External code is correct for proposal; live write still unproven |
| `to_Partner[0].Customer` | `C615-A00` | `Edm.String`, MaxLength 10, creatable | Customer field/string confirmed | Value requires live check |
| `to_Item` | one row | Navigation to items, multiplicity `*` | Read relationship confirmed | Nested POST remains unproven |
| `to_Item[0].SalesOrderItem` | `10` | `Edm.String`, MaxLength 6, non-null, creatable | Key/field value `"10"` observed | Proposed format compatible; POST unproven |
| `to_Item[0].Material` | `P615-100` | `Edm.String`, MaxLength 40, creatable | Field/string confirmed | Material requires live check |
| `to_Item[0].RequestedQuantity` | `10` | `Edm.Decimal(15,3)`, creatable; local write schema uses number | GET serializes decimal as string | Accepted POST serialization remains unproven |
| `to_Item[0].RequestedQuantityUnit` | `PC` | `Edm.String`, MaxLength 3, creatable | GET returned string `"289"` for another record | `PC` requires live API/material-unit pre-check; no conversion inferred |

All fields pass the local Phase 3B.0 payload schema. This is structural evidence, not a claim that SAP will accept the POST.

## Dependency pre-checks

Every entry currently has status `REQUIRES_LIVE_PRECHECK` and failure action `ABORT_BEFORE_POST`.

| Dependency | Proposed value | Required check |
|---|---|---|
| Customer | `C615-A00` | Exists, active, extended to 1010/10/00, allowed as sold-to for OR |
| Partner function | `DO` | Active external function and observed mapping to internal AG / sold-to; internal field omitted |
| Material | `P615-100` | Exists, active, correct sales views, orderable for customer/context |
| Sales organization | `1010` | Exists and supports order processing |
| Distribution channel | `10` | Assigned to sales organization 1010 |
| Division | `00` | Completes valid sales area 1010/10/00 |
| Document type | `OR` | Exists, allowed for sales area, and creatable through service |
| Unit | `PC` | Accepted as external API unit and valid for material/quantity |
| Payment terms | `R001` | Exists and is permitted for customer/order context |
| Plant | omitted | Valid plant must be determinable; abort if explicit plant is required |
| Shipping point | omitted | Valid shipping point must be determinable; abort if explicit point is required |

The customer reference `4712` is payload data, not master/configuration identity. It is included in duplicate detection and post-create verification.

## Application-side idempotency

| Control | Definition |
|---|---|
| Canonical identity | `S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT` |
| Migration/correlation ID | `SO-PILOT-49B1BBA4FA3FE33DD3B3` |
| Payload identity | SHA-256 `fee6311451a3cfb8d0e09501f86c5596e4fcec46f272fcc88376d36a28605c33` |
| Correlation placement | Application execution ledger only; not inserted into an unevidenced SAP field |

Before any POST, the application must reject a ledger match in `SUBMITTED`, `CREATED`, or `AMBIGUOUS` state and perform a read-only SAP duplicate search using the full source-backed fingerprint: order type, sales area, sold-to, customer reference, material, quantity, and unit. Exact or ambiguous matches require abort and human reconciliation.

The execution ledger must record object/correlation/payload identities, attempt number, status, timestamps, HTTP status, created order ID, response ETag, and sanitized error. It must never persist CSRF tokens, authorization headers, or session cookies.

Retries are prohibited after ambiguous outcomes until a read-only reconciliation proves that no order exists. Validation errors, authorization errors, other HTTP 4xx responses, and conflicts are not retryable without correction and reapproval. A transient retry is allowed at most once, only after duplicate checks are clear, the prior attempt is conclusively uncommitted, and a fresh session token is acquired at execution time.

## Controlled-pilot acceptance criteria

### HTTP response

- Exactly one authorized POST returns `201 Created`.
- The response contains one non-empty SAP-generated `SalesOrder` ID and no business error payload.
- `Location` and/or entity metadata identifies `A_SalesOrder(<created key>)`; capture a returned ETag if present.

### GET re-read

Re-read the created order and verify order ID/type, sales area, sold-to, customer reference, payment terms, partner function/customer, item number/material/quantity/unit, and any SAP-determined plant and shipping point.

### VA03/Fiori verification

- Exactly one order exists with type OR and sales area 1010/10/00.
- Sold-to is C615-A00 and external role DO resolves to sold-to semantics.
- Item 10 is P615-100 for 10 PC.
- Customer reference 4712 and terms R001 are retained.
- Determined plant/shipping point are valid and the order is not blocked by incompletion/error.
- No unintended partner, schedule, pricing, delivery, billing, or accounting object was created.

### Abort/failure conditions

Abort before or during the pilot if any dependency check is not PASS; a duplicate/ambiguous order exists; CREATE authorization, token acquisition, or explicit execution approval is absent; the payload hash differs; a token/internal partner code/invented field appears; the response is not an unambiguous `201`; the connection outcome is ambiguous; re-read differs; or multiple orders are observed.

## What remains unproven

- Deep-insert write behavior for `to_Item` and `to_Partner`.
- CREATE authorization for the intended execution identity.
- Accepted write serialization, especially `Edm.Decimal`, dates, and external units.
- Transaction and rollback behavior.
- Idempotency in SAP itself.

The user-provided evidence that the service returns HTTP 200 and an authenticated browser can fetch a CSRF token reduces reachability/session uncertainty. It does not prove any of the five items above, and no real token is stored or required by these artifacts.

## Test results

Targeted suite: **49 tests passed**. Full repository suite: **133 tests passed**.

## Files generated or changed

- `evidence/pilot/sales_order_candidate.json`
- `evidence/pilot/sales_order_proposed_payload.json`
- `evidence/pilot/sales_order_dependency_checklist.json`
- `scripts/build_phase3b0_artifacts.py`
- `src/sap_mapping/odata.py`
- `schemas/sap/core_mapping_contracts.json`
- `schemas/sap/payloads.schema.json`
- `tests/test_phase3b0_sales_order_write_readiness.py`
- `tests/snapshots/phase2c_core_payloads.json`
- `reports/phase2c_mapping_coverage.json`
- `reports/phase3b0_sales_order_write_readiness.md`

## Gate recommendation

**NO-GO for one controlled SALES_ORDER write pilot at the current evidence state.** The candidate and payload are ready for review, but execution must remain disabled until all 11 live dependency/configuration checks pass, the duplicate search is clear, CREATE authorization is explicitly confirmed, and the exact single pilot is separately authorized. This preparation does not authorize a SAP connection or write.
