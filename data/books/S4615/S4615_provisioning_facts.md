# S4615 - Provisioning Facts

## Purpose

Compact source for Codex. Use this file first. Open `S4615_full_clean.md` or a chapter file only when a required value is absent here.

**Rule:** do not adapt the Book to the current SAP system. Provision the Book's environment. Existing SAP objects are references/templates only.

## Source / course identity

- Course: `S4615 - Facturation dans SAP S/4HANA Sales`
- Course version: `12`
- Instructor-led course, duration: `2 days`
- Training user pattern: `S4615-##`
- `##` means the number assigned by the instructor/training group. Resolve it at runtime; do not modify the canonical source.
- The Book states that course data was imported via CATT and that corresponding billing documents were pre-created for some exercises. This means the training system is expected to be pre-provisioned rather than built interactively by students.

## Common organizational environment

### Confirmed by the Book

- Company Code: `1010`
- Sales Organization: `1010`
- Sales Organization `1010` is assigned to Company Code `1010`.
- Distribution Channel used throughout the exercises: `10`
- Division used throughout the main exercises: `00`
- Sales Area: `1010/10/00`
- Shipping Point used throughout the exercises: `1010`
- User defaults requested by the Book: Company Code `1010`, Shipping Point `1010`, Sales Org `1010`, Distribution Channel `10`, Division `00`.

### Chart of accounts evidence

- Chapter 2 instructor note says Company Code `1010` is assigned to chart of accounts `INT`.
- Chapter 9 contains account-determination examples using both `INT` and `YCOA` in different places. Treat this as conflicting course/instructor material; do **not** infer a single chart of accounts without live verification of the target client.

### Not specified sufficiently by the Book

The Book does **not** provide enough evidence to invent these Company Code / Sales Org fields:

- Company Code name
- Company Code city/address
- country/region
- company currency
- language
- Sales Organization description
- Sales Organization statistical currency
- other V_T001 / V_TVKO technical fields

If these do not already exist, they require a justified template/source or explicit business/config decision.

## Training master-data families

The course repeatedly uses these training families. They are better seed/reference candidates than unrelated technical pilot data.

### Customers observed

- `C615-A##`
- `C615-B##`
- `C615-C##`
- `C615-D##`
- `C615-F##`

Examples for user/group `00` appear as `C615-A00`, `C615-B00`, `C615-D00`, etc.

### Products / materials observed

- `P615-1##`
- `P615-2##`
- `P615-4##`
- `P615-5##`
- `P615-6##`
- fixed examples such as `P615-100`, `P615-200`, `P615-500`, `P615-600`
- service examples also appear in the course (for example `P-Service`, `T-D100`).

### Important seed strategy

When a Book-specific object is missing, inspect same-family siblings first, for example:

- customer target `C615-D00` -> inspect `C615-A00`, `C615-B00`, other `C615-*`
- product target `P615-400` -> inspect `P615-100`, `P615-200`, other `P615-*`

Do not substitute siblings into the Book transaction. They are source/reference evidence only.

## Golden exercise - Chapter 4 / Exercise 5 / Solution 5

### Canonical runtime target for training user `00`

| Field | Value |
|---|---|
| Training user | `S4615-00` |
| Order Type | `BV` (cash sale / vente au comptant) |
| Sales Organization | `1010` |
| Distribution Channel | `10` |
| Division | `00` |
| Sold-To Party | `C615-D00` |
| Customer Reference | `00S4615-BV` |
| Material | `P615-400` |
| Order Quantity | `1 PC` |

Canonical placeholder forms are:

- `S4615-##`
- `C615-D##`
- `##S4615-BV`
- `P615-4##`

### Golden workflow

1. Create cash-sale Sales Order `BV` in `1010/10/00` for `C615-D##` and `P615-4##`, quantity `1 PC`.
2. Saving the cash sale creates a delivery at the same time.
3. Expected save message concept: cash sale saved and delivery created.
4. Post Goods Issue on the delivery.
5. Create the real billing document using the **sales order number** as the billing reference.
6. Billing type is `BV` (cash sale).
7. Inspect accounting document.
8. Book expectation: postings include cash/petty-cash, domestic sales revenue, and output VAT; the cash-sale amount posts to a cash account rather than a customer receivable.

### BV configuration facts

- Cash sale uses Sales Order Type `BV`.
- Message/output type mentioned: `RD03` for immediate paper cash-sale invoice; the Book notes that display of RD03 may not work in the course system.
- Real billing can be created later after PGI.
- Billing Type: `BV`.
- Billing is order-related.
- No new pricing determination for the billing document: price should not differ from the printed cash-sale invoice.
- In Financial Accounting, the sale amount posts to a cash account rather than customer account.
- Cancellation billing type for cash sales: `SV`.

### Important conflict in instructor demo

One instructor/demo block near the cash-sale topic uses:

- Sales Organization `1000`
- customer `C615-D00`
- product `P615-100`

But **Exercise 5 and Solution 5 explicitly use**:

- Sales Organization `1010`
- customer `C615-D##`
- product `P615-4##`

For provisioning/execution, use the Exercise/Solution canonical values (`1010`, `C615-D##`, `P615-4##`). Do not let the instructor demo override them.

## C615-D## customer facts

Confirmed in Chapter 5 exercises/solutions:

- Sales area: `1010/10/00`
- Incoterms Part 1: `CFR`
- Incoterms Part 2: `##` (training group number)
- Therefore user `00` -> Incoterms conceptually `CFR / 00` where this exercise-specific setup is required.

The Book also instructs creating freight condition records for this customer:

- Condition Type: `KF00`
- Key combination: Incoterms Part 1 + Part 2
- Incoterms: `CFR`
- Incoterms 2: `##`
- Amount: `10 EUR`
- Per: `1 KG`

Do not assume this freight condition is required for the Chapter 4 cash-sale golden flow unless the canonical dependency graph says so.

### Customer values not supplied by the Book

The Book does not fully define the BP/customer root and all mandatory master-data fields, including for example:

- legal/name/address source
- country/language source
- BP grouping/number-range strategy
- all FI company-code data
- reconciliation account/payment terms/tax classifications where required by API/SAP validation
- partner functions not explicitly shown

These must be copied/inherited only from a justified same-training-family source or obtained from live/reference configuration.

## P615-4## product facts

Confirmed for Golden Exercise:

- Material pattern: `P615-4##`
- Quantity: `1 PC`
- It is described as a bicycle / stock product in the cash-sale exercise.
- The cash-sale process requires a delivery and PGI, so it must be logistically usable for delivery in the training sales area/plant setup.

### Product values not supplied by the Book

The Book does not fully define all product creation/extension fields, for example:

- material type
- base UoM vs alternative UoM conversions
- description
- plant extension values
- sales-org/distribution-channel extension values
- item category group
- loading/transportation fields
- valuation/accounting views
- tax classifications

Derive these from same-family `P615-*` references when technically justified. Do not invent them.

## Other S4615 workflow/config facts useful for provisioning

### Standard/logistical process

- Shipping Point `1010` is repeatedly used for delivery creation.
- Standard stocked items commonly use item category `TAN`.
- `TAN` is delivery-related for billing in standard flows.
- Standard billing type `F2` is used for delivery-related billing in several exercises.

### Billing types mentioned

- `F2` - invoice
- `F5` - pro forma for order
- `F8` - pro forma for delivery
- `BV` - cash sale billing
- `G2` - credit memo
- `S1` - invoice cancellation
- `S2` - credit memo cancellation
- `SV` - cash-sale cancellation
- custom/user-specific `ZF##` - trade-fair billing type

### Sales/document types mentioned

- `BV` - cash sale
- `CDLC` / course text sometimes also shows `CDCL` in explanatory material
- `ZA##` - group-specific trade-fair sales order
- `RK` - invoice correction request
- `RE` - return
- `G2` - credit memo request in course examples
- `OR` appears in instructor examples

Preserve exact canonical type from the target exercise; do not normalize inconsistent course labels globally.

## Pricing / copy-control facts

- Pricing condition `PR00` appears repeatedly.
- Freight condition `KF00` is used in Chapter 5.
- Copy control is an explicit dependency for several later exercises.
- For trade-fair scenario `ZF##` / `LF` / `TAN`, the Book instructs pricing type `H` to redetermine freight conditions.
- `TAN` is a recurring item category in delivery-related flows.

These later-exercise settings must not be forced into the Golden cash-sale scenario unless its dependency graph requires them.

## Account determination facts

Course examples include:

- Pricing procedure example: `RVAA01`
- `PR00` -> account key `ERL`
- `KF00` -> account key `ERF` (and a course note also mentions `K007` -> `ERS`)
- Account determination procedure: `KOFI00`
- Account determination type/access sequence: `KOFI`
- Condition table `001` is used in the account-determination exercise.
- Sales Org `1010` is part of the key.
- Material account assignment group example: `01`
- Existing sales revenue example: G/L `41000000`
- Exercise creates new G/L assignment example: `49000000`

Caution: chapter 9 contains inconsistent chart-of-accounts examples (`INT` and `YCOA`). Verify live rather than inventing the target value.

## Pre-existing-data assumptions from the Book

The course is not a system-install/setup guide. Many exercises explicitly assume data and configuration already exist, for example:

- CATT-imported course data and pre-created documents
- `1010/10/00`
- training users `S4615-##`
- customer families `C615-*`
- product families `P615-*`
- custom group-specific document types such as `ZA##` / `ZF##`

Therefore absence of these in client 600 is an environment-provisioning problem, not a reason to substitute unrelated current SAP data.

## Minimal provisioning target for Golden S4615 user 00

### Common environment

- Ensure Company Code `1010`
- Ensure Sales Organization `1010`
- Ensure Sales Org `1010` -> Company Code `1010`
- Ensure Distribution Channel `10` is usable with Sales Org `1010`
- Ensure Division `00` is usable with Sales Org `1010`
- Ensure Sales Area `1010/10/00`
- Ensure required plant/shipping-point linkage discovered by runtime checks; Book evidence strongly uses Shipping Point `1010`

### Book master data

- Ensure customer `C615-D00`
- Ensure customer role/company/sales-area extensions for `1010/10/00`
- Ensure material `P615-400`
- Ensure material sales/logistics extensions required by cash sale
- Ensure quantity `1 PC` is valid

### Transactional readiness

- `BV` must be valid in `1010/10/00`
- cash-sale save must create a delivery
- PGI must be possible
- order-related `BV` billing must be possible after PGI
- FI posting must be possible

## Explicit non-goals / forbidden substitutions

Do **not** substitute Golden Book values with pilot values such as:

- Sales Org `1710`
- product `FG228`
- order type `CS`

Do not modify existing Sales Order `148` created by the technical pilot.

## Unknowns that still require live/reference evidence

If these remain missing after inspecting same-family training records, keep them as consolidated blockers rather than inventing values:

1. Company Code `1010` detailed creation fields/source strategy.
2. Sales Organization `1010` detailed creation fields/source strategy.
3. Exact customer creation/extension template values for `C615-D00`.
4. Exact material creation/extension template values for `P615-400`.
5. Writable transport/customizing handling contract for live changes.
6. Live write/readback contracts for delivery/PGI/billing if not already validated.

## Codex reading policy

Use this order:

1. `S4615_provisioning_facts.md`
2. relevant chapter file only if a field is missing
3. `S4615_full_clean.md` only as last resort
4. original PDF only for visual verification of a table/figure that text extraction cannot resolve

This avoids repeatedly consuming context on the full 263-page PDF.
