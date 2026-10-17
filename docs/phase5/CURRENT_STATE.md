# Phase 5 Current State — Book 1 / S4615

Last updated: 2026-10-17. This is the current operational record from the latest live-verified state supplied for A4H.

## Environment

- SAP system/client/user: `A4H / 600 / ABDELJ`
- Current customizing transport: `A4HK908422`
- Scope: Book 1, course `S4615`

## Independent exercise pass (2026-10-17)

- Exercise 2: live READ navigation from the existing A4H/600/ABDELJ session opened `SPRO`, then the exact observed `Guide de référence SAP` button opened `SIMG` (`SAPLSHI01`, `Afficher guide d'implémentation`). The already verified `Sales Organization 1010 -> Company Code 1010` assignment supports the organizational question. Status: **PARTIAL**, because the exercise also asks for user-specific SAP GUI display settings and a Favorites entry; those were not changed or verified for the course user `S4615-##`.
- Exercise 1: the book requires a preloaded billing document found through purchase-order reference `##S4615-A3`. A targeted `API_SALES_ORDER_SRV/A_SalesOrder` GET for training user `00` returned HTTP `200` and zero rows for `PurchaseOrderByCustomer=00S4615-A3`; the source order/billing document is therefore not available through that exact reference. Do not claim that other training groups are empty.
- One additional targeted GET (HTTP `200`, zero rows) checked the exact user-`00` references `00S4615-A1`, `A3`, `A4`, `A5`, `A6`, and `A10`. The book's preloaded-document branches using these references cannot be completed for user `00` from the currently observed Sales Order data. This is not a broad system-wide absence claim.
- Exercise 5: remains **BLOCKED** by material `10000287` Accounting 1/2 extension (`C+039`); no BV Sales Order exists.
- Exercises 3, 4, 6–13: their configuration-only or display portions may be checked separately, but the book's required source documents, group-specific master data, and end-to-end result are not live-verified. No completion or SAP write is claimed in this pass.
- No SAP write was performed in this exercise pass.

## Provisioning status

| Operation | Status | Verified state |
|---|---|---|
| Company Code 1010 | EXISTS | Created from template `BE01`; live readback confirmed |
| Chart assignment 1010 → CABE | EXISTS | Assigned through `OB62`; persisted under `A4HK908422`; confirmed after re-entry |
| Sales Organization 1010 | EXISTS | Live-verified |
| Sales Org 1010 → Company Code 1010 | EXISTS | Live-verified |
| Distribution Channel 10 → Sales Org 1010 | EXISTS | Live-verified |
| Division 00 → Sales Org 1010 | EXISTS | Live-verified |
| Customer BP 1000000114 | EXISTS | Category `2`, grouping `BPAB` |
| Customer address | EXISTS | AddressID `1557`; current `XXDEFAULT`; verified after exit/re-entry |
| Customer role FLCU00 | EXISTS | Independent readback verified |
| Customer role FLCU01 | EXISTS | Independent readback verified |
| A_Customer view | EXISTS | Live-verified |
| GL account 400000 / 1010 / CABE | EXISTS | Human checkpoint live-verified: customer reconciliation account, EUR, tax `*`, sort key `001` |
| A_CustomerCompany / 1010 | EXISTS | Created through `API_BUSINESS_PARTNER` with reconciliation account `400000`; independent fresh-session readback succeeded |
| Sales Area 1010/10/00 | EXISTS | Human checkpoint verified; saved under transport `A4HK908422`; subsequent customer extension POST accepted the combination |
| A_CustomerSalesArea / 1010/10/00 | EXISTS | Created through `API_BUSINESS_PARTNER`; independent fresh-session readback succeeded |
| Product P615-400 | EXISTS | SAP material `10000287` created through MM01; independent Product API readbacks verified root, Plant `1710`, Sales `1010/10`, and BE/MWST tax data |
| Plant assignment 1010/10/1710 | EXISTS | Human checkpoint live-verified |
| S4615 cash-sale dry-run | READY | All seven dependency GETs, service access, ledger anti-duplicate, and SAP anti-duplicate checks passed with resolved SAP identities |
| Pricing determination 1010/10/00 + A + 02 | EXISTS | OVKK target `A17J02` created and verified live |
| Fiscal Year Variant 1010 | EXISTS | Targeted API readback confirmed `K4` |
| VOV4/T184 BV + CB04 | EXISTS | `BV/CB04/blank/blank → CBTA` saved and independently read back at absolute row 392 |
| S4615 BV Sales Order | BLOCKED_PRODUCT_ACCOUNTING_VIEW | Controlled POST returned SAP V4/210 for material `10000287`; no Sales Order ID was created |

## Customer identity and mapping

- Logical Book ID: `C615-D00`
- SAP Business Partner key: `1000000114`
- Logical mapping: `C615-D00 → 1000000114`
- Mapping status: **LIVE_VERIFIED** and persisted in `data/provisioning/phase5_identity_mappings.json`.
- Grouping `BPAB` uses internal number range `BP` (`1000000000..1999999999`); do not use `C615-D00` as the SAP BP key.

## Latest verified readbacks

- Company Code service returned `1010 → CABE`; `BE01 → CABE`.
- BP address `1557` has current `XXDEFAULT` usage. Read fields include `West Chester Pike 3999`, `Newtown Square, PA 19073`, `US`, language `EN`, time zone `EST`.
- Both customer roles and the `A_Customer` view exist.
- `A_CustomerCompany` for `1000000114/1010` exists after an independent readback; reconciliation account is `400000`.
- `A_CustomerSalesArea` for `1000000114/1010/10/00` exists after an independent readback.

## Active blocker and next dependency

The Customer and Product dependency chains are complete and live-verified. Runtime identity resolution now transforms only the execution copy (`C615-D00 → 1000000114`, `P615-400 → 10000287`) while preserving canonical values. The exact cash-sale dry-run passed all ten checks. The next unresolved dependency is live pricing-procedure determination for Sales Area `1010/10/00`, document pricing procedure `A`, and the customer's current pricing procedure `02`.

The first controlled BV POST returned HTTP `400` with SAP message V1/212, `Aucun schéma de calcul n'a pu être déterminé`, parameters `1010 10 00 / A / 02`. No Sales Order ID was returned and the runtime ledger records the attempt as failed; it must not be blindly retried. A subsequent human OVKK lookup positioned past the target to Sales Organization `140C`, deterministically confirming that the exact `1010/10/00 + A + 02` row is missing.

The previously proposed source `1010/10/00 + A + 1 → RVAA01` is **disproved live**: OVKK positioning found no exact row and moved to Sales Organization `140C`. It is not an approved source and must not be copied.

The approved live OVKK source row is `1710/10/00 + A + 02 → A17J02`. A direct read-only OVKK observation confirmed all five source keys and the assigned pricing procedure; no changes were made. This agrees with the supporting live evidence: customer `17100002` has customer pricing procedure `02` in `1710/10/00`, and existing `CS` orders `1` and `148` prove that context has operated.

The target `1010/10/00 + A + 02 → A17J02` now exists and was verified live. A subsequent exact dry-run passed all ten checks. The single controlled POST was then rejected with HTTP `400`, SAP `KI 268`: `Déterminez tout d'abord une version d'exercice pour la société 1010`. No Sales Order ID was created.

A fresh read-only `API_COMPANYCODE_SRV` comparison proved the exact cause at that point: Company Code `1010` had an empty `FiscalYearVariant`, while its approved technical copy template `BE01` had `FiscalYearVariant=K4`.

That dependency is now resolved: a targeted API GET confirmed `1010.FiscalYearVariant=K4`. The following exact dry-run passed all ten checks, but the controlled POST returned HTTP `400`, SAP V1/320: `Type de poste non défini (table T184 BV CB04  )`. No Sales Order ID was created.

Targeted read-only evidence found no existing `BV` orders. The proven technical cash-sale context has orders `1` and `148` with document type `CS`, material `FG228`, item-category group `CB04`, and actual item category `CBTA`. A direct read-only VOV4/T184 observation then confirmed the exact source row `CS/CB04/blank/blank → CBTA`; no changes were made. The approved target is therefore `BV/CB04/blank/blank → CBTA`, changing only the sales-document type.

The approved VOV4 target `BV/CB04/blank/blank → CBTA` is now persisted. The reusable allowlisted GUI contract saved the exact prepared row and an independent VOV4 scan found the target at absolute row `392` among `3642` rows. SAP did not request a new transport during this save. The next action is the controlled Sales Order dry-run and, only if it passes, one POST.

That dry-run passed all ten checks. The single controlled POST then returned HTTP `400`, SAP V4/210: `Aucune donnée de comptabilité gérée pr l'article 10000287`. No Sales Order ID was created. Targeted Product API GETs prove that `10000287` has no `A_ProductValuation`, `A_ProductValuationAccount`, `A_ProductValuationCosting`, or `A_ProductMLAccount` row. The approved template FG228 has valuation-area `1710`, valuation class `7920`, price control `S`, price determination control `2`, price unit `1`, standard price `27.19`, and currency `USD`. Product accounting-view extension is the next dependency; the Sales Order must not be retried before a fresh valuation readback succeeds.

The human accounting-view extension stopped before Save with SAP message C+899: `Missing currency translation rule for currency and valuation type 30`. A read-only GUI snapshot confirms transaction `MM01`, program `SAPMSDYP`, screen `10`, material `10000287`, and plant `1710`. Targeted API reads prove plant `1710` belongs to Company Code `1710`; FG228 has Material Ledger currency roles `10=USD` and `30=USD`, while `10000287` has no Material Ledger rows. The missing customizing belongs to `FINSC_LEDGER`, view **Currency Conversion Settings for Company Codes**, table `FINSC_001A`; ledger/company-code currency assignment is held in `FINSC_LD_CMP`. The exact source-currency/exchange-rate/date rule is not exposed by the proven APIs and must not be guessed.

The FINSC dependency is now resolved for the exact stored rule. Live GUI maintenance saved Company Code `1710`, Currency Type `30`, Source Currency Type `10`, Exchange Rate Type `M`, Translation Date Type `2` (Posting Date), with real-time conversion enabled, under transport `A4HK908422`. An independent `SE16N` readback of `FINSC_001A` confirmed `1710/30/10/M/2` and `NOREALTIMECONV` blank. `WAERS` is not stored in `FINSC_001A`; the maintenance UI derives and displays it separately.

The subsequent MM01 retry selected only Accounting 1 and Accounting 2 for material `10000287`, target plant `1710`, reference material `FG228`, and reference plant `1710`. Before reaching the accounting fields, SAP stopped with message **C+039**, `Les devises du ledger articles ont été modifiées`. SAP's long text states that the current currency/type configuration for valuation area `1710` differs from the configuration used at Material Ledger productive startup, and therefore postings are blocked to preserve consistency. The long text contains no maintained procedure. No material save was attempted. This is now the sole active boundary before the accounting extension and Sales Order retry.

## Product state

Logical Product `P615-400` is represented by live SAP material `10000287`. The Book unit remains `PC`; it was not replaced with template-specific `289` or `/PC`.

The attempted minimal `A_Product` POST used the explicit target ID and Book unit, but SAP returned HTTP 400 `L'opération Créer n'est pas autorisée pour l'entité.` No Product row was created. OData create is therefore conclusively unavailable on this installed service. No live RFC connector is installed and the SAP GUI Product operation has no captured lookup/create/readback contract.

The prior manual SAP GUI attempt used generated material `10000286` but never persisted it. It must not be used or mapped.

The previously external BE/MWST dependency is resolved by the successfully created material itself: independent readback proves `BE/MWST/1` on `10000287`. This is evidence for this exact material only, not a general default for future products.

The abandoned internal number `10000286` was never persisted. A subsequent controlled MM01 creation succeeded as SAP material `10000287`. Independent fresh-session `API_PRODUCT_SRV` readbacks verify: root `FERT/M`, base unit `PC`, division `00`, item category group `CB04`, product group `L004`; Plant `1710` with availability check `SP`; Sales Organization/Distribution Channel `1010/10` with delivering plant `1710`, account-determination product group `03`, and item category group `CB04`; and Product tax `BE/MWST/1`. The logical mapping `P615-400 → 10000287` is persisted as `LIVE_VERIFIED` in `data/provisioning/phase5_identity_mappings.json`.

## DO NOT REDO

- Do not recreate Company Code 1010, Sales Organization 1010, or their verified assignments.
- Do not recreate BP `1000000114`, its address `1557`, roles FLCU00/FLCU01, or the `A_Customer` root.
- Do not reassign the already verified `1010 → CABE` chart mapping.
- Do not recreate `C615-D00` as a BP key or create a duplicate BP.
