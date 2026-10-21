# S4615 master-data readiness: C615-A01 and P615-101

## Scope and safety

This report is an offline assessment of existing Book, canonical, requirement, provisioning-code, and retained SAP-verification artifacts. It does not create or modify SAP objects and does not call SAP APIs. The generated specifications preserve the canonical source artifacts and record missing values as `null` with `source_type: MISSING`.

Group `01` resolves the Book patterns by identifier substitution only:

| Book pattern | Group | Logical target | Resolution |
|---|---:|---|---|
| `C615-A##` | `01` | `C615-A01` | Derived from the placeholder and requested group |
| `P615-1##` | `01` | `P615-101` | Derived from the placeholder and requested group |

No business attribute was inferred from that substitution.

## Readiness decision

| Object | Classification | Basis | Exact missing fields preventing creation |
|---|---|---|---|
| `C615-A01` | **ADMIN_REQUIRED** | `API_BUSINESS_PARTNER` supports customer company/sales-area extensions only for the hard-coded D00 operation and requires an existing `A_Customer` root. It does not create a BP root. There is no A01 mapping. | `existing_customer_root.sap_partner_id`; `business_partner_grouping`; `name`; `addresses`; `roles`; `reconciliation_account`; `payment_terms`; `currency`; `shipping_conditions`; `delivering_plant`; `incoterms`; `incoterms_location`; `account_assignment_group`; `customer_pricing_procedure`; `tax_classifications`; `partner_functions` |
| `P615-101` | **BLOCKED** | The existing adapter explicitly blocks product-root POST because the installed `API_PRODUCT_SRV` rejected `A_Product` POST. The backend is allowlisted only for P615-400. There is no P101 mapping. | `sap_product_id`; `description`; `material_type`; `industry_sector`; `base_unit`; `product_group`; `plants`; `delivering_plant`; `item_category_group`; `tax_classification`; `availability_check`; `alternative_units` |

The classification describes the current implementation/evidence path, not an assertion that the logical IDs do not exist in every SAP system or that another approved provisioning method is unavailable. The retained current-state report specifically says neither target was created and no target mapping exists.

## Exercise and dependency coverage

The following list includes every Book/canonical object with the exact family placeholders `C615-A##` or `P615-1##`. Exercise and solution mentions are grouped under their scenario; source field references remain visible in the canonical object IDs.

### Customer family `C615-A##` → `C615-A01`

| Scenario | Canonical objects containing the customer value | Book pages | Use |
|---|---|---:|---|
| S4615 Chapter 1 Exercise 1 | `S4615_CH1_EX1_BILLING_IMPORTED_A3` | 13, 16 | Payer for an imported billing-document reference |
| S4615 Chapter 3 Exercise 3 | `S4615_CH3_EX3_SALES_ORDER_FAIR`, `S4615_CH3_EX3_BILLING_FAIR` | 41, 43 | Sold-to and billing payer; the order also uses the P615-1## product family |
| S4615 Chapter 4 Exercise 4 | `S4615_CH4_EX4_BILLING_ORIGINAL_F2`, `S4615_CH4_EX4_BILLING_CREDIT_MEMO` | 61, 63 | Customer on original invoice/credit-memo work |
| S4615 Chapter 4 Exercise 5 | `S4615_CH4_EX5_SALES_ORDER_PRO_FORMA`, `S4615_CH4_EX5_BILLING_PRO_FORMA` | 73, 75 | Sold-to and payer; this scenario uses P615-2##, not P615-1## |
| S4615 Chapter 6 Exercise 7 | `S4615_CH6_EX7_SALES_ORDER_FIORI_APP_FINAL`, `S4615_CH6_EX7_BILLING_FIORI_APP_CANCELLED`, `S4615_CH6_EX7_BILLING_FIORI_APP_POSTED` | 121, 127–129 | Sold-to and payer across the Fiori order/billing steps |
| S4615 Chapter 10 Exercise 13 | `S4615_CH10_EX13_SALES_ORDER_POSTING_BLOCK`, `S4615_CH10_EX13_BILLING_POSTING_BLOCK`, `S4615_CH10_EX13_SALES_ORDER_FI_REFERENCE`, `S4615_CH10_EX13_BILLING_FI_REFERENCE` | 235, 238, 241 | Sold-to and payer in posting-block and FI-reference work |

The dependency graph records unresolved `SOLD_TO_PARTY` edges for C615-A## from the Chapter 3 Exercise 3, Chapter 4 Exercise 5, Chapter 6 Exercise 7, and both Chapter 10 Exercise 13 sales orders. The additional payer uses above are canonical field references; they do not create extra master-data attributes.

### Product family `P615-1##` → `P615-101`

| Scenario | Canonical objects containing the material value | Book pages | Use |
|---|---|---:|---|
| S4615 Chapter 3 Exercise 3 | `S4615_CH3_EX3_SALES_ORDER_FAIR`, `S4615_CH3_EX3_OUTBOUND_DELIVERY_FAIR`, `S4615_CH3_EX3_BILLING_FAIR` | 41, 43 | Order, delivery, and billing; 5 PC |
| S4615 Chapter 5 Exercise 6 | `S4615_CH5_EX6_SALES_ORDER_FAIR_FREIGHT`, `S4615_CH5_EX6_OUTBOUND_DELIVERY_FAIR_FREIGHT`, `S4615_CH5_EX6_BILLING_FAIR_FREIGHT`, `S4615_CH5_EX6_BILLING_F1_OVERRIDE` | 97, 100 | Freight scenario and related billing work |
| S4615 Chapter 9 Exercise 12 | `S4615_CH9_EX12_SALES_ORDER_ACCOUNT_DETERMINATION_TEST`, `S4615_CH9_EX12_OUTBOUND_DELIVERY_ACCOUNT_DETERMINATION_TEST` | 213, 216 | Order and delivery; 1 PC |
| S4615 Chapter 10 Exercise 13 | `S4615_CH10_EX13_SALES_ORDER_POSTING_BLOCK`, `S4615_CH10_EX13_OUTBOUND_DELIVERY_POSTING_BLOCK`, `S4615_CH10_EX13_SALES_ORDER_FI_REFERENCE`, `S4615_CH10_EX13_OUTBOUND_DELIVERY_FI_REFERENCE` | 235, 238, 241 | Order and delivery in posting-block/FI-reference work; 1 PC |

The dependency graph records unresolved `USES_MATERIAL` edges for P615-1## from Chapter 3 Exercise 3, Chapter 5 Exercise 6, Chapter 9 Exercise 12, and both Chapter 10 Exercise 13 sales orders. The related delivery and billing objects depend on those sales orders through the canonical `CREATED_FROM`/`BILLED_FROM` relations.

`C615-A00` and `P615-100` appear as fixed group-00 examples in Chapter 8 and elsewhere. They are not group-01 targets. They were not used to populate either specification. The same applies to C615-D00 and P615-400; the requested prohibitions were observed.

## Book requirements vs API contract vs verified environment

| Area | Book/canonical requirement | Existing API implementation | Already verified |
|---|---|---|---|
| Customer identity | Customer family `C615-A##`; used as sold-to and/or payer in the scenarios above. Group 01 yields only logical ID `C615-A01`. | Current adapter accepts only operation `CUSTOMER_C615_D00`. It reads an existing `A_Customer` root and can POST only `A_CustomerCompany` and `A_CustomerSalesArea` extensions. It cannot create the BP root. | No C615-A01 mapping; current-state report says C615-A01 was not created. No target-specific root, group, address, role, or extension values are verified. |
| Customer organizational data | Sales area `1010/10/00`; company code `1010` is the common S4615 environment. | Payload keys include `Customer`, `CompanyCode`, `ReconciliationAccount`, `PaymentTerms`, `CustomerAccountGroup`, `SalesOrganization`, `DistributionChannel`, `Division`, `Currency`, `CustomerAccountAssignmentGroup`, `CustomerPricingProcedure`, `IncotermsClassification`, `IncotermsLocation1`, `ShippingCondition`, and `CustomerPaymentTerms`. The Phase 5 decision gate also requires root and additional decision fields. | Company code 1010 and sales area 1010/10/00 are verified as common environment. This does not verify A01-specific attributes. |
| Product identity | Product family `P615-1##`; group 01 yields `P615-101`. Book scenarios use order unit `PC` and require a usable product for sales/delivery flows. | Adapter supports only `PRODUCT_P615_400`. `root_payload` describes Product, ProductType, IndustrySector, BaseUnit, Division, ItemCategoryGroup, and ProductGroup, but `provision` explicitly refuses product-root creation on this API. | No P615-101 mapping or product-specific attribute evidence. The requirement for `P615-1##|PC` remains UNKNOWN; the requirement itself cautions that another product's PC association does not prove this product's association. |
| Product extension/fulfillment | The Book's canonical sales orders use `1010/10/00`; related exercises use deliveries. `PC` is an evidenced order unit, not necessarily the base unit. | Current product API path only reads/checks the product root; it does not create sales or plant views. Phase 5 product decision gate includes plants, delivering plant, tax classification, availability check, and alternative units. | Common S4615 sales organization/channel/division are verified, but no P615-101 sales/plant view, base unit, unit association, or fulfillment attribute is verified. |

### Exact API boundary

- `API_BUSINESS_PARTNER`: the code-generated payloads describe customer **extensions**, not Business Partner root creation. The customer route requires an existing `A_Customer` root. The route also enforces an operation/target allowlist limited to `CUSTOMER_C615_D00`; C615-A01 is not accepted.
- `API_PRODUCT_SRV`: the code can construct a product-root payload for readback/contract tests, but `SapApiBackend.provision` returns a blocked result for products instead of sending `A_Product` POST. P615-101 is not an accepted operation.
- `CustomerAccountGroup: CUST` is a literal in the current customer payload, not an independently verified A01 business value. It is marked `DERIVED` in the spec and still requires compatibility verification.
- For P615-101, the Book's `PC` order-unit requirement is preserved separately from `BaseUnit`. The spec does not assert that PC is the material's base unit or that the product-unit association already exists.

## Target-specific missing data

### C615-A01

The target's known Book-level values are its logical ID, group `01`, company code `1010`, and sales area `1010/10/00`. These do not supply the following missing fields:

- **Root / identity:** existing SAP customer ID and `A_Customer` root, Business Partner grouping, name, address(es), customer roles.
- **Company-code extension:** reconciliation account and payment terms.
- **Sales-area extension:** currency, shipping conditions, customer account assignment group, customer pricing procedure, Incoterms classification/location, and customer payment terms (same underlying `payment_terms` decision as the company view).
- **Phase 5 decision gate:** delivering plant, tax classifications, and partner functions.

The `CUST` account-group string in the API payload is known only as an implementation constant; it does not close the missing Business Partner root/grouping gap.

### P615-101

The target's known Book-level values are logical ID P615-101, group `01`, sales organization/channel `1010/10`, sales division `00`, and order unit `PC`. The following remain missing:

- **Identity/root contract:** SAP product mapping/readback identity; the adapter's create route is blocked.
- **Root payload / Phase 5 decision gate:** description, material type, industry sector, base unit, item-category group, product group, plants, delivering plant, tax classification, availability check, and alternative-unit definition.
- **Scenario qualification (separate from root creation fields):** product-specific PC unit association and evidence of sales/plant views adequate for the Book's order/delivery scenarios. `product_unit_of_measure_association` is missing; the requirements artifact explicitly warns that PC for another product does not prove this association.

Accounting/valuation-view requirements cannot be resolved from the existing API root payload or the target-specific artifacts; the P615-400 values were not used to fill that gap.

## Sources

- Book and canonical data: [S4615_full_clean.md](../data/books/S4615/S4615_full_clean.md), [S4615_provisioning_facts.md](../data/books/S4615/S4615_provisioning_facts.md), [extracted objects](../data/extracted/full/S4615/objects.json), [normalized objects](../data/normalized/full/S4615/objects.json), [dependency graph](../metadata/dependencies/full/S4615/dependency_graph.json).
- Readiness and seed evidence: [training environment requirements](../data/requirements/training_environment_requirements.json), [training seed](../config/s4615_training_seed.yaml), [identity mappings](../data/provisioning/phase5_identity_mappings.json), [current environment status](./sap_training_environment_current_state.md).
- API contract evidence: [OData backend](../src/provisioning/sap_api_backend.py), [Phase 5 validation contract](../src/provisioning/phase5.py), [interface registry](../mappings/sap/interface_registry.yaml).

The field-level records and source references are in [C615-A01.spec.json](../data/provisioning/s4615/C615-A01.spec.json) and [P615-101.spec.json](../data/provisioning/s4615/P615-101.spec.json).
