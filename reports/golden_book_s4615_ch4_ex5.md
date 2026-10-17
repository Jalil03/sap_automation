# Golden Book Scenario — S4615, chapitre 4, exercice 5

## Résultat

La vue de démonstration locale réutilise l'objet canonique existant `S4615_CH4_EX5_SALES_ORDER_CASH_SALE`. Aucun nouvel objet métier n'a été créé et `data/validated/canonical_objects.json` n'a pas été modifié.

Pour le training user `07` :

- résolution des placeholders : **PASS**;
- validation et mapping local SALES_ORDER : **EXECUTION_READY**;
- prechecks SAP : **7 × NEEDS_LIVE_VALIDATION**;
- résultat final : **BLOCKED** jusqu'à validation GET/read-only des références SAP.

Aucun appel SAP, aucune requête POST et aucun `--execute` n'ont été réalisés.

## Ancrage source

| Élément | Valeur |
|---|---|
| Support | `S4615_FR_Col12_ILT_FV_Inst_A4.pdf` |
| Cours | `S4615` |
| Chapitre | 4 — Types de documents de facturation spéciaux |
| Exercice / solution | 5 — Créer une facture de vente au comptant et une facture pro forma |
| Page exercice | 73 |
| Page solution | 75 |
| Scenario ID | `S4615_CH4_EX5` |
| Canonical object ID principal | `S4615_CH4_EX5_SALES_ORDER_CASH_SALE` |

## Données source et runtime 07

| Champ | Book immuable | Runtime 07 |
|---|---|---|
| Training user | `S4615-##` | `S4615-07` |
| Sales Order Type | `BV` | `BV` |
| Sales Organization | `1010` | `1010` |
| Distribution Channel | `10` | `10` |
| Organization Division | `00` | `00` |
| Sold-To Party | `C615-D##` | `C615-D07` |
| Customer Reference | `##S4615-BV` | `07S4615-BV` |
| Material | `P615-4##` | `P615-407` |
| Quantity | `1` | `1` |
| Unit | `PC` | `PC` |

La résolution est effectuée sur une copie profonde. Les templates originaux et la provenance du canonique restent inchangés.

## Workflow extrait

Le scénario complet comporte cinq objets canoniques existants et quatre dépendances résolues :

```text
Vente au comptant
S4615_CH4_EX5_SALES_ORDER_CASH_SALE
  → S4615_CH4_EX5_OUTBOUND_DELIVERY_CASH_SALE
  → S4615_CH4_EX5_BILLING_CASH_SALE

Pro forma
S4615_CH4_EX5_SALES_ORDER_PRO_FORMA
  → S4615_CH4_EX5_BILLING_PRO_FORMA
```

La facture comptant BV dépend explicitement de la commande et de la livraison créée avec la commande. La facture pro forma F5 dépend de la commande avant livraison et conserve le statut FI `NOT_APPLICABLE_PRO_FORMA` extrait du support.

## Mapping SAP offline

| Contrat | Valeur |
|---|---|
| Protocole | OData V2 |
| Service externe | `API_SALES_ORDER_SRV` |
| Enregistrement technique | `ZAPI_SALES_ORDER_SRV` |
| EntitySet | `A_SalesOrder` |
| Statut contrat local | `EXECUTION_READY` |
| Payload envoyé | Non |

La vue affiche les correspondances canoniques vers `SalesOrderType`, `SalesOrganization`, `DistributionChannel`, `OrganizationDivision`, `SoldToParty`, `PurchaseOrderByCustomer`, `to_Partner`, `to_Item`, `Material`, `RequestedQuantity` et `RequestedQuantityUnit`. Elle expose un aperçu offline du mapper, sans exécution.

Aucune donnée du pilote technique `148` ou de la référence `TECH-PILOT-001` n'est utilisée.

## Prechecks SAP pour le runtime 07

| Precheck | Valeur résolue | Service | EntitySet proposé | Statut |
|---|---|---|---|---|
| CUSTOMER | `C615-D07` | `API_BUSINESS_PARTNER` | `A_Customer` | `NEEDS_LIVE_VALIDATION` |
| MATERIAL | `P615-407` | `API_PRODUCT_SRV` | `A_Product` | `NEEDS_LIVE_VALIDATION` |
| SALES_ORGANIZATION | `1010` | `API_SALESORGANIZATION_SRV` | `A_SalesOrganization` | `NEEDS_LIVE_VALIDATION` |
| DISTRIBUTION_CHANNEL | `10` | `API_DISTRIBUTIONCHANNEL_SRV` | `A_DistributionChannel` | `NEEDS_LIVE_VALIDATION` |
| ORGANIZATION_DIVISION | `00` | `API_DIVISION_SRV` | `A_Division` | `NEEDS_LIVE_VALIDATION` |
| SALES_ORDER_TYPE | `BV` | `API_SALESORDERTYPE_SRV` | `A_SalesOrderType` | `NEEDS_LIVE_VALIDATION` |
| UNIT_OF_MEASURE | `PC` | Non confirmé | Non confirmé | `NEEDS_LIVE_VALIDATION` |

Les EntitySets proposés ne sont pas activés. Même une observation positive injectée dans le modèle ne peut pas produire `PASS` tant que le contrat du lookup n'est pas marqué `CONFIRMED` avec des métadonnées et un chemin GET vérifiés. Une future réponse GET vide produit `BLOCKED`; une interface indisponible produit également `BLOCKED`.

## Vue locale

Commande de lancement :

```powershell
.venv\Scripts\python.exe -m src.golden_book --serve --host 127.0.0.1 --port 8765
```

Puis ouvrir `http://127.0.0.1:8765/`. Le sélecteur propose `00` à `99` et recharge uniquement l'API locale en GET. Le serveur refuse toute méthode POST avec `405 Method Not Allowed`.

La page et l'API ont été vérifiées localement avec HTTP 200. L'API a retourné le bon canonical object ID, sept prechecks, `EXECUTION_READY` local et `BLOCKED` global. La prévisualisation visuelle intégrée n'était pas disponible dans l'environnement; le DOM, les ressources et l'API ont été vérifiés déterministiquement par les tests.

## Validation

- Tests Golden Book : **12 passés**.
- Tests ciblés Golden Book + Training Context + Phase 3B : **39 passés**.
- Suite complète du dépôt : **172 passés**.
- Connexions SAP : **0**.
- POST SAP/réseau : **0**.
- `--execute` : **0**.

## Conditions restantes pour une validation live read-only

1. Capturer le `$metadata` des six services inventoriés et identifier un service déterministe pour les unités.
2. Confirmer chaque EntitySet, propriété filtrable, clé, type EDM et nom de service externe.
3. Mettre les contrats vérifiés à `CONFIRMED` dans la configuration des prechecks.
4. Exécuter exclusivement des GET sur le client cible pour les sept valeurs résolues de l'utilisateur `07`.
5. Conserver les réponses assainies comme preuves locales, avec statut HTTP et correspondance exacte.
6. Marquer chaque contrôle `PASS` seulement si la valeur exacte est trouvée; sinon conserver `BLOCKED` avec `NOT_FOUND` ou `INTERFACE_UNAVAILABLE`.

La validation live read-only est donc **NO-GO** tant que les contrats GET restent non confirmés. La vue Golden Book offline est prête pour validation fonctionnelle client.
