# Phase 3B — Runtime contrôlé de création SALES_ORDER

## Résultat

Le runtime SALES_ORDER est intégré à l’architecture existante. Il réutilise le registre, le mapper canonique, les validateurs et les contrats Phase 2/3A. Les accès SAP sont isolés derrière un transport injectable; tous les tests utilisent des doubles locaux et n’ont effectué aucune connexion SAP.

Le mode `DRY_RUN` ne peut émettre que des GET. Le mode `EXECUTE` exige un dry-run réussi pour le même SHA-256, une nouvelle référence client, une date explicite, une confirmation humaine ou CI, un nouveau contrôle anti-doublon, un jeton CSRF dynamique, puis autorise exactement un POST sans retry automatique. Un read-back header/items/partners est obligatoire après `201 Created`.

## Preuve live fournie

Le contexte live communiqué établit les éléments suivants pour le client SAP TEST 600 :

- `API_SALES_ORDER_SRV/A_SalesOrder` est accessible.
- Le POST manuel a retourné HTTP 201 et créé la commande `148`.
- La commande créée utilisait le type `CS`, la sales area `1710/10/00`, le sold-to `17100002`, la référence `TECH-PILOT-001`, l’article `FG228`, la quantité `1` et l’unité demandée `289`.
- Le read-back header, item et partenaires était cohérent; la commande a été vérifiée dans VA03.
- SAP a déterminé `CustomerPaymentTerms=0004`, `ProductionPlant=1710`, `ShippingPoint=1710`, `Route=TR0001`, `EXW`, `35.35 USD` et les partenaires DO/RF/PY/RM.

Cette preuve est enregistrée comme contexte validé fourni par l’utilisateur; le runtime et ses tests n’ont pas rejoué l’appel live. La référence `TECH-PILOT-001` est explicitement interdite à toute nouvelle exécution.

## Architecture retenue

```text
CLI
 └─ SalesOrderRuntime
     ├─ src.sap_mapping.validate_runtime_contract
     ├─ builder minimal OData V2 + schéma strict
     ├─ GET accès service
     ├─ GET préchecks master/config configurables
     ├─ GET anti-doublon exact
     ├─ ExecutionLedger SQLite
     ├─ GET CSRF (EXECUTE uniquement)
     ├─ POST unique (EXECUTE uniquement)
     └─ GET read-back header/items/partners
```

Les responsabilités sont séparées :

- `src/sap_mapping` reste purement offline et sans connecteur.
- `src/sap_runtime/config.py` charge uniquement la configuration d’environnement.
- `src/sap_runtime/transport.py` fournit le transport HTTP synchrone, la session cookie en mémoire et zéro retry.
- `src/sap_runtime/prechecks.py` exécute des sondes GET configurées par l’administrateur. Les EntitySets de lookup non prouvés ne sont pas inventés dans le code.
- `src/sap_runtime/ledger.py` gère un ledger SQLite local sans payload ni secret.
- `src/sap_runtime/sales_order.py` orchestre les gates, le POST unique et le read-back.
- `src/sap_runtime/cli.py` fournit la surface opérateur.

## Construction du payload

Le runtime commence par le payload du mapper existant, vérifie que l’objet est `EXECUTION_READY`, puis conserve uniquement les champs minimaux prouvés :

```json
{
  "SalesOrderType": "...",
  "SalesOrganization": "...",
  "DistributionChannel": "...",
  "OrganizationDivision": "...",
  "SoldToParty": "...",
  "PurchaseOrderByCustomer": "...",
  "CustomerPurchaseOrderDate": "/Date(...)/",
  "to_Item": [
    {
      "SalesOrderItem": "10",
      "Material": "...",
      "RequestedQuantity": "1",
      "RequestedQuantityUnit": "..."
    }
  ]
}
```

`Edm.Decimal` est sérialisé sous forme de chaîne décimale sans exposant. La date `YYYY-MM-DD` fournie par l’opérateur est convertie en `/Date(milliseconds UTC)/`. Le schéma runtime interdit les propriétés supplémentaires.

Le runtime n’envoie pas `CustomerPaymentTerms`, `ProductionPlant`, `ShippingPoint`, `Route`, Incoterms, pricing, `to_Partner` ou `PartnerFunctionInternalCode`. SAP reste responsable de leur détermination. Le read-back les observe sans les forcer.

## Modes

### DRY RUN

Le dry-run :

1. charge l’objet canonique sans le modifier;
2. exige `EXECUTION_READY`;
3. construit et valide le payload minimal;
4. vérifie l’accès GET à `A_SalesOrder`;
5. exécute sept préchecks GET configurés : customer, material, sales organization, distribution channel, division, document type et unité;
6. vérifie le ledger;
7. exécute la recherche SAP anti-doublon;
8. écrit `DRY_RUN_OK`, `BLOCKED` ou `DUPLICATE` dans le ledger;
9. affiche le payload exact sans appeler CSRF ni POST.

### EXECUTE

L’exécution :

1. exige une nouvelle `PurchaseOrderByCustomer` et une date client explicite;
2. refuse `TECH-PILOT-001` et la référence canonique source;
3. exige un `DRY_RUN_OK` pour le même objet et le même SHA-256;
4. rejoue tous les préchecks et l’anti-doublon;
5. demande une confirmation interactive exacte, sauf approbation CI concordante;
6. récupère un jeton via GET avec `X-CSRF-Token: Fetch`;
7. inscrit `SUBMITTED` avant l’envoi;
8. effectue exactement un POST;
9. récupère l’identifiant créé;
10. relit header, items et partenaires;
11. passe à `VERIFIED` uniquement si les valeurs essentielles correspondent.

## Anti-doublon et idempotence

La recherche SAP utilise au minimum :

- `SalesOrderType`
- `SalesOrganization`
- `DistributionChannel`
- `OrganizationDivision`
- `SoldToParty`
- `PurchaseOrderByCustomer`

Tout résultat bloque le POST avec `DUPLICATE`. Le ledger bloque également un objet, correlation ID, SHA-256 ou customer reference déjà en état `SUBMITTED`, `CREATED`, `VERIFIED` ou `AMBIGUOUS`.

Le correlation ID est déterministe à partir de `canonical_object_id + payload_sha256`. Le ledger contient : identités, tentative, mode, statut, timestamps, statut HTTP, SalesOrder créée, ETag et erreur assainie. Il ne contient jamais payload, password, cookie, jeton CSRF ou Authorization header.

Il n’existe aucun retry automatique. Après timeout ou perte réseau du POST, le statut est `AMBIGUOUS`; toute nouvelle tentative est bloquée par le ledger jusqu’à réconciliation anti-doublon explicite.

## Read-back

Après HTTP 201, trois GET relisent :

- Header : SalesOrder, type, sales area, sold-to, référence/date client, payment terms, devise et montant net.
- Items : poste, article, quantité, unité externe/SAP/ISO, plant et shipping point.
- Partners : fonction externe, fonction interne et customer.

La vérification essentielle compare le type, la sales area, le sold-to, la référence/date client, chaque item, la quantité décimale et l’unité parmi les représentations external/SAP/ISO. Une divergence produit `FAILED` tout en conservant l’identifiant de la commande créée pour réconciliation; elle ne déclenche jamais un second POST.

## Sécurité

- Aucun secret hardcodé.
- `.env` et les fichiers SQLite sont ignorés par Git.
- Le transport ne journalise aucune requête ni aucun header.
- Les erreurs sont bornées et expurgent password, Authorization, cookie et CSRF.
- Le cookie jar et le jeton restent uniquement en mémoire.
- HTTPS et vérification TLS sont obligatoires par défaut.
- L’option HTTP non sécurisé nécessite une activation explicite et ne doit servir qu’à un environnement contrôlé.
- Le mode CI exige simultanément `--non-interactive-approved`, `--approval-id` et une valeur concordante dans `SAP_EXECUTION_APPROVAL_ID`.

## Configuration

Variables déclarées dans `.env.example` :

- `SAP_BASE_URL`
- `SAP_CLIENT` (`600` pour le client validé)
- `SAP_USERNAME`
- `SAP_PASSWORD`
- `SAP_TIMEOUT_SECONDS`
- `SAP_VERIFY_TLS`
- `SAP_ALLOW_INSECURE_HTTP`
- `SAP_LEDGER_PATH`
- `SAP_PRECHECK_CONFIG`
- `SAP_EXECUTION_APPROVAL_ID`

Le fichier `config/sap_sales_order_prechecks.example.json` doit être copié hors des valeurs d’exemple et complété avec les chemins GET réellement vérifiés dans le système. Le runtime refuse une configuration qui ne couvre pas les sept dépendances obligatoires. Cette approche évite d’inventer des EntitySets de master data absents des preuves live actuelles.

## Commandes

Après avoir exporté les variables d’environnement et renseigné `SAP_PRECHECK_CONFIG`, premier dry-run proposé avec une nouvelle référence :

```powershell
.venv\Scripts\python.exe -m src.sap_runtime sales-order --object S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT --dry-run --customer-reference TECH-PILOT-002 --customer-purchase-order-date 2026-10-13
```

Après un `DRY_RUN_OK` du payload strictement identique, commande d’exécution interactive :

```powershell
.venv\Scripts\python.exe -m src.sap_runtime sales-order --object S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT --execute --customer-reference TECH-PILOT-002 --customer-purchase-order-date 2026-10-13
```

La CLI demandera de saisir exactement :

```text
EXECUTE S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_SALES_ORDER_INSTALLMENT TECH-PILOT-002
```

Le runtime n’a exécuté aucune de ces commandes contre SAP pendant cette implémentation.

## Comportement en erreur

| Situation | Statut | POST |
|---|---|---:|
| Objet non EXECUTION_READY / payload invalide | `BLOCKED` | 0 |
| GET service ou précheck en échec | `BLOCKED` | 0 |
| Doublon SAP ou ledger | `DUPLICATE` | 0 |
| CSRF absent / GET CSRF non-200 | `BLOCKED` | 0 |
| HTTP 400 / 403 / 500 après POST | `FAILED` | exactement 1 |
| Timeout/perte réseau après soumission | `AMBIGUOUS` | exactement 1, aucun retry |
| HTTP 201 sans identifiant clair | `FAILED` | exactement 1 |
| Read-back différent | `FAILED` | exactement 1 |
| HTTP 201 + read-back cohérent | `VERIFIED` | exactement 1 |

## Limites et risques connus

- Le seul objet canonique `EXECUTION_READY` contient OR / 1010/10/00 / C615-A00 / P615-100, différent du pilote manuel CS / 1710/10/00 / 17100002 / FG228. Le runtime ne modifie pas ces valeurs canoniques; le premier dry-run doit donc confirmer leur existence dans TEST 600 ou bloquer.
- Les chemins de lookup master/config doivent être fournis après validation locale; ils ne sont pas déduits de noms d’interfaces vagues.
- L’authentification Basic est prise en charge par le transport actuel. Si l’environnement impose SSO, OAuth ou certificat client, un autre transport conforme au même protocole doit être ajouté.
- Le ledger est local. Une exécution distribuée nécessiterait un ledger partagé avec verrouillage transactionnel.
- La confirmation CI est un gate d’application, pas une autorisation SAP.
- Le runtime ne garantit pas l’idempotence native SAP; il fournit une protection applicative, un anti-doublon et une politique d’abandon.

## Fichiers créés ou modifiés

- `src/sap_runtime/__init__.py`
- `src/sap_runtime/__main__.py`
- `src/sap_runtime/cli.py`
- `src/sap_runtime/config.py`
- `src/sap_runtime/errors.py`
- `src/sap_runtime/ledger.py`
- `src/sap_runtime/models.py`
- `src/sap_runtime/prechecks.py`
- `src/sap_runtime/sales_order.py`
- `src/sap_runtime/security.py`
- `src/sap_runtime/transport.py`
- `schemas/sap/sales_order_write_runtime.schema.json`
- `config/sap_sales_order_prechecks.example.json`
- `tests/test_phase3b_sales_order_runtime.py`
- `.env.example`
- `.gitignore`
- `reports/phase3b_sales_order_runtime.md`

## Tests

Les tests couvrent le builder minimal, sérialisation decimal/date, statuts, dry-run sans POST, préchecks, anti-doublon, CSRF mocké, HTTP 201, 400, 403, 500, timeout/AMBIGUOUS, absence de retry, mismatch read-back, références interdites, confirmation interactive/CI et absence de secrets dans les erreurs/ledger.

Résultats : **14 tests runtime ciblés passés**; **147 tests passés** sur la suite complète du dépôt.

## Mise à jour — audit des prechecks et contexte utilisateur de formation

Cette mise à jour a été réalisée entièrement hors ligne. Aucun appel SAP, aucune requête HTTP et aucun `POST` n'ont été exécutés. Le fichier `data/validated/canonical_objects.json` est resté inchangé.

### Audit des sept prechecks

Les inventaires locaux confirment les noms externes/techniques de six services. Ils ne contiennent cependant ni les EntitySets, ni les propriétés de clé, ni une réponse GET permettant de valider les chemins. Les EntitySets et filtres ci-dessous sont donc des **propositions inactives**, jamais présentées comme des contrats prouvés. Le metadata local `API_SALES_ORDER_SRV.metadata.xml` confirme les champs du payload Sales Order, mais pas les contrats des services de lookup.

| Precheck | Donnée canonique | Service SAP inventorié | EntitySet attendu | Filtre/clé proposé | Résultat attendu | Si absent | Si interface indisponible | Statut |
|---|---|---|---|---|---|---|---|---|
| `CUSTOMER` | `data.sold_to_party` | `API_BUSINESS_PARTNER` (`ZAPI_BUSINESS_PARTNER`) | `A_Customer` non confirmé | `Customer eq '{CUSTOMER}'` | HTTP 200 et ligne `Customer` exacte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `MATERIAL` | `data.items[].material` | `API_PRODUCT_SRV` (`ZAPI_PRODUCT_SRV`) | `A_Product` non confirmé | `Product eq '{MATERIAL}'` | HTTP 200 et ligne exacte pour chaque article distinct | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `SALES_ORGANIZATION` | `data.sales_organization` | `API_SALESORGANIZATION_SRV` (`ZAPI_SALESORGANIZATION_SRV`) | `A_SalesOrganization` non confirmé | `SalesOrganization eq '{SALES_ORGANIZATION}'` | HTTP 200 et ligne exacte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `DISTRIBUTION_CHANNEL` | `data.distribution_channel` | `API_DISTRIBUTIONCHANNEL_SRV` (`ZAPI_DISTRIBUTIONCHANNEL_SRV`) | `A_DistributionChannel` non confirmé | `DistributionChannel eq '{DISTRIBUTION_CHANNEL}'` | HTTP 200 et ligne exacte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `ORGANIZATION_DIVISION` | `data.sales_division` | `API_DIVISION_SRV` (`ZAPI_DIVISION_SRV`) | `A_Division` non confirmé | `Division eq '{ORGANIZATION_DIVISION}'` | HTTP 200 et ligne exacte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `SALES_ORDER_TYPE` | `data.order_type` | `API_SALESORDERTYPE_SRV` (`ZAPI_SALESORDERTYPE_SRV`) | `A_SalesOrderType` non confirmé | `SalesOrderType eq '{SALES_ORDER_TYPE}'` | HTTP 200 et ligne exacte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |
| `UNIT_OF_MEASURE` | `data.items[].unit` | aucun service déterministe sélectionné | non confirmé | non confirmé | lookup exact pour chaque unité distincte | `BLOCKED` | `BLOCKED` | `NEEDS_LIVE_VALIDATION` |

Les noms `API_ET_UNITOFMEASURE_SRV` et `API_EXSTXUNITOFMEASURE_SRV` existent dans l'inventaire, mais leur nom seul ne prouve pas qu'ils constituent le lookup générique requis. Ils restent des candidats rejetés pour activation automatique.

Le fichier `config/sap_sales_order_prechecks.example.json` porte désormais tout le contrat documentaire : chemins canoniques/payload, service, EntitySet attendu, filtre, résultat, comportements d'échec, preuve et statut. Le runtime applique une politique fail-closed :

- une sonde `NEEDS_LIVE_VALIDATION` retourne `BLOCKED` sans émettre de requête;
- seule une sonde explicitement passée à `CONFIRMED` avec un `path_template` absolu peut effectuer un GET;
- une réponse vide, non-2xx, invalide ou une interface indisponible retourne `BLOCKED`;
- tous les articles et toutes les unités distinctes sont vérifiés, pas seulement le premier poste;
- les noms techniques `Z...` documentent l'enregistrement Gateway, tandis que les chemins HTTP proposés utilisent les noms externes `API_...`.

### Training User Context et résolution des placeholders

Le nouveau paquet `src/training_context` centralise la validation et la résolution :

- `TrainingUserContext` n'accepte que des chaînes à deux chiffres, de `00` à `99`; `00` est classé `INSTRUCTOR`, `01`–`99` `PARTICIPANT`;
- `PlaceholderResolver` effectue une copie profonde, résout récursivement les chaînes dans `data` au sein des dictionnaires/listes imbriqués et ne modifie jamais l'objet source;
- les métadonnées runtime contiennent `training_user_code`, `training_user_role`, les chemins résolus, `original_template`, la valeur résolue et le nombre de remplacements;
- les entrées `placeholders` de la copie runtime passent à `RESOLVED`; seuls les blocages dus aux placeholders résolus sont retirés;
- un `##` restant dans les données exécutables, dans une clé exécutable ou dans le payload final bloque déterministiquement le traitement;
- un objet sans placeholder reste sémantiquement identique, tout en étant retourné sous forme de copie.

L'ordre d'exécution est désormais :

```text
canonical object immuable
→ TrainingUserContext / PlaceholderResolver (copie runtime)
→ validation canonique et contrat Phase 2C
→ mapper SALES_ORDER
→ garde-fou final anti-##
→ prechecks
→ dry-run
→ execute
```

La CLI accepte par exemple :

```powershell
.venv\Scripts\python.exe -m src.sap_runtime sales-order --object <OBJECT_ID> --dry-run --training-user 07
```

L'option est transmise avant la validation et le mapping. Si l'objet ne contient aucun `##`, le payload reste inchangé. Le résultat runtime expose la traçabilité dans `training_context`. La présente mise à jour n'a lancé ni cette commande contre SAP, ni aucun `--execute`.

### Fichiers de cette mise à jour

- `src/training_context/__init__.py`
- `src/training_context/errors.py`
- `src/training_context/user_context.py`
- `src/training_context/placeholder_resolver.py`
- `src/sap_runtime/cli.py`
- `src/sap_runtime/models.py`
- `src/sap_runtime/prechecks.py`
- `src/sap_runtime/sales_order.py`
- `config/sap_sales_order_prechecks.example.json`
- `tests/test_training_context.py`
- `tests/test_phase3b_sales_order_runtime.py`
- `reports/phase3b_sales_order_runtime.md`

### Tests de la mise à jour

- Tests ciblés Training Context + Phase 3B runtime : **27 passés**.
- Suite complète : **160 passés**.
- Tests avec connexion SAP : **0**.
- POST SAP/réseau effectués : **0** (les branches d'exécution sont couvertes exclusivement par des doubles locaux).
