# Phase 4B — Golden Book S4615 CH4 EX5 minimal provisioning

## Conclusion

**BLOCKED.** Le premier write nécessaire serait le customizing de l’organisation commerciale `1010`, confirmée absente. Aucun contrat writable local ne couvre cette opération : le registre ne fournit qu’un lookup. Le customer `C615-D00` et le product `P615-400` sont également absents au niveau testé, mais les preuves conservées ne permettent pas encore de choisir création complète ou extension.

Aucune connexion SAP et aucune écriture n’ont été effectuées. Le canonical est inchangé.

## Périmètre et comptages

- Requirements : **13** — 9 directs, 4 transitifs.
- États : **3 EXISTS**, **3 MISSING**, **7 UNKNOWN**.
- Risque : **10 HIGH RISK**.
- Nature : **6 customizing**, **6 master data**, **1 transactionnel**.
- Frontière : commande Cash Sale BV sélectionnée et prérequis; branche pro forma exclue car elle n’est pas une dépendance du canonical sélectionné.

## Requirements minimaux

| Requirement | Type | Template | Runtime 00 | Direct/transitif | SAP | Layer | Write capability |
|---|---|---|---|---|---|---|---|
| `REQ_DISTRIBUTION_CHANNEL_9411C41EC990` | DISTRIBUTION_CHANNEL | `10` | `10` | DIRECT | EXISTS | EXISTING | UNKNOWN |
| `REQ_SALES_DIVISION_12DB1A50F04D` | SALES_DIVISION | `00` | `00` | DIRECT | EXISTS | EXISTING | UNKNOWN |
| `REQ_SALES_ORDER_TYPE_FD17CC7ED649` | SALES_ORDER_TYPE | `BV` | `BV` | DIRECT | EXISTS | EXISTING | UNKNOWN |
| `REQ_COMPANY_CODE_8131EAD50CED` | COMPANY_CODE | `1010` | `1010` | TRANSITIVE | UNKNOWN | GLOBAL_CUSTOMIZING | MANUAL_CUSTOMIZING_REQUIRED |
| `REQ_SALES_ORGANIZATION_017B33085362` | SALES_ORGANIZATION | `1010` | `1010` | DIRECT | MISSING | GLOBAL_CUSTOMIZING | MANUAL_CUSTOMIZING_REQUIRED |
| `REQ_SALES_AREA_2D070605D0FF` | SALES_AREA | `1010/10/00` | `1010/10/00` | TRANSITIVE | UNKNOWN | SALES_AREA_CUSTOMIZING | MANUAL_CUSTOMIZING_REQUIRED |
| `REQ_BUSINESS_PARTNER_7BE3434D7102` | BUSINESS_PARTNER | `C615-D##` | `C615-D00` | DIRECT | MISSING | MASTER_DATA_CREATE | ODATA_CREATE_SUPPORTED |
| `REQ_MATERIAL_67C49094879C` | MATERIAL | `P615-4##` | `P615-400` | DIRECT | MISSING | MASTER_DATA_CREATE | BAPI_SUPPORTED |
| `REQ_CUSTOMER_SALES_AREA_EXTENSION_09190AA5FDD8` | CUSTOMER_SALES_AREA_EXTENSION | `C615-D##|1010/10/00` | `C615-D00|1010/10/00` | TRANSITIVE | UNKNOWN | MASTER_DATA_EXTEND | ODATA_UPDATE_SUPPORTED |
| `REQ_PRODUCT_SALES_AREA_EXTENSION_D237B2C0DF76` | PRODUCT_SALES_AREA_EXTENSION | `P615-4##|1010/10` | `P615-400|1010/10` | TRANSITIVE | UNKNOWN | MASTER_DATA_EXTEND | BAPI_SUPPORTED |
| `REQ_PRODUCT_UNIT_OF_MEASURE_3FF2FF2DA869` | PRODUCT_UNIT_OF_MEASURE | `P615-4##|PC` | `P615-400|PC` | DIRECT | UNKNOWN | MASTER_DATA_EXTEND | UNKNOWN |
| `REQ_UNIT_OF_MEASURE_8CF4FF8ED738` | UNIT_OF_MEASURE | `PC` | `PC` | DIRECT | UNKNOWN | UNKNOWN | UNKNOWN |
| `REQ_SALES_ORDER_8347DE8AC9E6` | SALES_ORDER | `S4615_CH4_EX5_SALES_ORDER_CASH_SALE` | `S4615_CH4_EX5_SALES_ORDER_CASH_SALE` | DIRECT | UNKNOWN | TRANSACTIONAL_RUNTIME | ODATA_CREATE_SUPPORTED |

## A. Minimal blockers

1. `SalesOrganization 1010` est MISSING et doit précéder toute donnée de base liée à 1010/10/00.
2. L’existence du `CompanyCode 1010` et du sales area exact `1010/10/00` reste à confirmer.
3. `C615-D00` est MISSING, mais root BP versus extension customer/sales area n’est pas distingué.
4. `P615-400` est MISSING, mais root product versus extension sales/plant n’est pas distingué.
5. `P615-400 + PC` reste UNKNOWN; `FG228 + PC` ne constitue pas une preuve transférable.
6. Le deep insert `A_SalesOrder` reste metadata-compatible mais non démontré en write.

## B. Exact provisioning order

### Layer 0 — EXISTING prerequisites

- `REQ_DISTRIBUTION_CHANNEL_9411C41EC990`
- `REQ_SALES_DIVISION_12DB1A50F04D`
- `REQ_SALES_ORDER_TYPE_FD17CC7ED649`

### Layer 1 — Global / organizational customizing

- `REQ_COMPANY_CODE_8131EAD50CED`
- `REQ_SALES_ORGANIZATION_017B33085362`

### Layer 2 — Sales-area customizing

- `REQ_SALES_AREA_2D070605D0FF`

### Layer 3 — Customer / product root master data

- `REQ_BUSINESS_PARTNER_7BE3434D7102`
- `REQ_MATERIAL_67C49094879C`

### Layer 4 — Master-data extensions and product-specific unit

- `REQ_CUSTOMER_SALES_AREA_EXTENSION_09190AA5FDD8`
- `REQ_PRODUCT_SALES_AREA_EXTENSION_D237B2C0DF76`
- `REQ_PRODUCT_UNIT_OF_MEASURE_3FF2FF2DA869`

### Layer 5 — Read-only runtime qualification checks

- `CHECK_CUSTOMER_ROOT_VS_EXTENSION`
- `CHECK_PRODUCT_ROOT_VS_EXTENSION`
- `CHECK_SALES_AREA`
- `CHECK_PRODUCT_UOM`
- `CHECK_DUPLICATE_ORDER`

### Layer 6 — Sales Order BV runtime creation

- `REQ_SALES_ORDER_8347DE8AC9E6`

### Layer 7 — Downstream outcome observation

- `OBSERVE_AUTO_OUTBOUND_DELIVERY`
- `OBSERVE_CASH_SALE_BILLING`

## C. Automatisation possible avec les interfaces existantes

- SALES_ORDER : `API_SALES_ORDER_SRV/A_SalesOrder`, contrat mapper et metadata locale disponibles; l’exécution write reste non prouvée.
- BUSINESS_PARTNER : `API_BUSINESS_PARTNER` est inventorié en MAINTAIN et le mapper couvre les sales areas; metadata write locale absente.
- MATERIAL : `BAPI_MATERIAL_SAVEDATA` est un candidat exact; les attributs obligatoires de création ne figurent pas dans ce scénario.
- Product UoM : `A_ProductUnitsOfMeasure` est utilisable en GET avec les clés Product + AlternativeUnit; aucune capacité write n’est prouvée.

## D. Customizing SAP probable

`1010`, son affectation au company code, l’affectation du canal `10`, du secteur `00` et le sales area `1010/10/00` relèvent du customizing. Les interfaces locales correspondantes sont lookup-only : le plan ne prétend pas pouvoir les créer automatiquement.

Le plant, l’affectation plant↔sales organization, le shipping point, la shipping determination et le pricing sont `MAY_BE_REQUIRED`, car le canonical exact ne fournit aucune valeur permettant de les provisionner sans invention.

## E. Vérifications GET restantes

Le script `scripts/browser_checks_s4615_ch4_ex5.js` charge d’abord le `$metadata` de chaque service. Il n’émet le GET de données que si l’EntitySet et les propriétés attendues sont réellement présents. Pour le sales area, aucun endpoint navigateur exact n’est prouvé : le résultat reste `NEEDS_LIVE_VALIDATION` au lieu de deviner une API.

## F. Premier point nécessitant une écriture SAP

Le premier write serait **la création/configuration de Sales Organization 1010**. Il est explicitement hors autorisation dans cette phase et nécessite vraisemblablement du customizing manuel ou un transport SAP gouverné.

## Customer C615-D00

Décision : **C — impossible à déterminer sans live check**. Si le BP root existe, les vues minimales connues sont le rôle/customer entity et la sales-area view `1010/10/00`. Pour la facturation aval, une company-code view `1010` peut être nécessaire, mais le scénario ne fournit pas assez d’éléments pour la déclarer certaine ni pour fabriquer ses attributs.

## Product P615-400

Décision : **C — impossible à déterminer sans live check**. Les besoins connus sont le root product/material, la vue ventes `1010/10` et l’association product-specific `P615-400 + PC`. Une extension plant est seulement potentielle. `PC` n’est jamais converti en `289`.

## G. Fichiers

- `data/requirements/golden_book_s4615_ch4_ex5_provisioning.json`
- `reports/phase4b_golden_book_s4615_provisioning.md`
- `scripts/browser_checks_s4615_ch4_ex5.js`
- `scripts/build_golden_book_provisioning.py`
- `tests/test_phase4b_golden_book_provisioning.py`

## H. Tests

Les tests vérifient la fermeture, la résolution `00`, l’absence de mutation canonical, le DAG, les statuts live, les décisions customer/product et le caractère GET-only du script navigateur.
