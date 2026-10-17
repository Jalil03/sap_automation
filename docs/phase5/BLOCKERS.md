# Active Phase 5 Blockers

Only unresolved blockers and dependencies are listed here.

## Other S4615 exercise source documents (training user 00)

- A targeted read-only `API_SALES_ORDER_SRV/A_SalesOrder` lookup returned HTTP `200` and zero rows for the exact customer references `00S4615-A1`, `00S4615-A3`, `00S4615-A4`, `00S4615-A5`, `00S4615-A6`, and `00S4615-A10`. Exercise 1's invoice-display chain and the related preloaded-document branches cannot be completed from those user-`00` references as currently observed. This does not prove absence for another group or by a different reference.
- S4615 Exercise 2 is partially verified via live read-only `SPRO` → `SIMG` navigation; its user-specific GUI preferences and Favorites entry were not changed in the `S4615-##` account.

## Product — resolved

No active Product provisioning blocker remains. `P615-400 → 10000287` is live-verified and persisted. Internal number `10000286` was never created and must not be used.

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
