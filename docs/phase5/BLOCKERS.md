# Active Phase 5 Blockers

Only unresolved blockers and dependencies are listed here.

## C615-A01 customer extensions

- BP `1000000115` now has current standard address `1581` with `XXDEFAULT`, independently verified. FSBP_ECC025's missing-address prerequisite is resolved.
- Current standard address `1581`, FLCU00, FLCU01, and `A_Customer` root are independently verified. The prior FSBP_ECC025 and R1/084 errors were reconciled with distinct one-shot recovery attempts after the user released the edit lock. Do not recreate the BP or roles.
- `A_CustomerSalesArea(1000000115,1010/10/00)` was created and independently verified with the user's exact approved commercial values. A targeted GET confirmed all four required self-referencing partner functions already exist; no partner POST was issued.
- `A_CustomerCompany(1000000115,1010)` was created after explicit scoped FI approval and independently verified with account `400000` and terms `0004`. All core C615-A01 customer extensions are verified; do not recreate them. Targeted tax GETs returned 0 rows for A01 and area `1010/10/00`. Tax is optional for the installed sales-area creation contract, but any tax-classification write or S4615 billing tax claim needs a proven value and separate tax decision.

## Other S4615 exercise source documents (training user 00)

- A targeted read-only `API_SALES_ORDER_SRV/A_SalesOrder` lookup returned HTTP `200` and zero rows for the exact customer references `00S4615-A1`, `00S4615-A3`, `00S4615-A4`, `00S4615-A5`, `00S4615-A6`, and `00S4615-A10`. Exercise 1's invoice-display chain and the related preloaded-document branches cannot be completed from those user-`00` references as currently observed. This does not prove absence for another group or by a different reference.
- S4615 Exercise 2 is partially verified via live read-only `SPRO` → `SIMG` navigation; its user-specific GUI preferences and Favorites entry were not changed in the `S4615-##` account.

## Product — resolved

No active Product provisioning blocker remains for the separate `P615-400 → 10000287` mapping. Internal number `10000286` was never created and must not be used.

For group-01 product `P615-101`, the Basic Data 1/2 root now exists as SAP material `10000289` and is independently verified through API_PRODUCT_SRV. The remaining blocker is the sales/plant/valuation extension: no 1010-compatible plant/valuation has been approved; `1710` and material `10000287` remain excluded. No sales, plant, accounting, or valuation view was created. The Basic Data root must not be recreated.

## Sales Order — Product accounting view

- **Dry-run:** `DRY_RUN_OK`; service access, seven dependencies, ledger duplicate check, and exact SAP duplicate check all passed.
- **Runtime identities:** `SoldToParty=1000000114`, `Material=10000287`; canonical Book values remain unchanged.
- **Pricing blocker resolved:** OVKK target `1010/10/00 + A + 02 → A17J02` exists and is live-verified.
- **Fiscal-year blocker resolved:** Targeted API readback confirms `1010.FiscalYearVariant=K4`.
- **Previous controlled write result:** The exact dry-run passed all ten checks; the single POST returned HTTP `400`, SAP V1/320 (`Type de poste non défini (table T184 BV CB04  )`). No Sales Order ID was created.
- **Item-category blocker resolved:** `BV/CB04/blank/blank → CBTA` is saved and independently read back in VOV4/T184 at absolute row `392`.
- **Latest controlled write result:** All ten dry-run checks passed, then the single POST returned HTTP `400`, SAP V4/210 (`Aucune donnée de comptabilité gérée pr l'article 10000287`). No Sales Order ID was created.
- **Confirmed missing data:** Product `10000287` has no row in `A_ProductValuation`, `A_ProductValuationAccount`, `A_ProductValuationCosting`, or `A_ProductMLAccount`.
- **Approved template evidence:** FG228 valuation area `1710`, valuation class `7920`, price control `S`, price determination control `2`, price unit `1`, standard price `27.19`, currency `USD`.
- **FINSC blocker resolved:** Independent `SE16N` readback confirms `FINSC_001A` row `1710/30` with Source Currency Type `10`, Exchange Rate Type `M`, Translation Date Type `2`, and real-time conversion enabled. The change is assigned to `A4HK908422`.
- **Current MM01 blocker:** SAP C+039, `Les devises du ledger articles ont été modifiées`, occurs after selecting only Accounting 1/2 for `10000287`, target/reference plant `1710`, and reference material `FG228`. SAP's long text says the current currency/type configuration for valuation area `1710` differs from its Material Ledger productive-startup configuration. The accounting fields are not reached and no material save was attempted.
- **Exact unsupported boundary:** the required Material Ledger follow-up after changing currency configuration is not captured or authorized. Do not guess an initialization/migration transaction and do not alter other company-code or global currency settings.
- **Read-only candidate evidence:** There are no existing `BV` orders. Existing `CS` orders `1` and `148` use material `FG228`; API reads prove `FG228.ItemCategoryGroup=CB04` and both order items have `SalesOrderItemCategory=CBTA`.
- **Approved live source:** Direct read-only VOV4/T184 observation confirmed `CS/CB04/blank/blank → CBTA`; no changes were made.
- **Required action:** an SAP FI/CO Material Ledger administrator must restore or reconcile valuation area `1710` currency configuration with the productive-startup configuration (type `30` must be `USD`) using the SAP-supported procedure, without changing unrelated company codes. Confirm that MM01 no longer raises C+039; then retry the same Accounting 1/2 extension and verify `A_ProductValuation` before another Sales Order POST.

### S4615 logistics 1010 (separate from 1710/C+039)

- **Shipping point 1010:** The first OVXD Save exposed mandatory address country. Address and transport were cancelled; fresh OVXD plus independent SE16N `TVST` confirm `1010` is still absent. The first attempt is terminal `REJECTED`, not automatically retryable. Proposed `BE` follows company 1010's Belgian context but was not in the original write fingerprint. Obtain a new exact scoped approval for `BE` (and any optional address values) before a new controlled attempt; do not treat the maintenance buffer as persisted evidence.
- **Plant 1010 and dependents:** No plant was created. Company/valuation assignment, EUR-compatible valuation, FERT valuation class, price control/initial price, stock/PGI account determination, plant write contract and scoped FI/MM approval remain unresolved. TVKWZ, TVSWZ, OVL2 and material `10000289` extensions must wait for the verified plant and approved configuration. Do not reuse 1710 settings or alter Material Ledger/global currencies.
