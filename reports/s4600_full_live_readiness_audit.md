# S4600 — audit de préparation des 36 exercices (lectures live partielles)

## Mise à jour prioritaire — S4600 seul

Le [plan d'exécution](s4600_priority_execution_plan.md) remplace l'ordre d'action historique sans modifier le compte prudent : **4 terminés, 0 READY, 22 bloqués par dépendance, 10 non vérifiés**. Une nouvelle inspection VOV8 live confirme A4H/600/ABDELJ, `SAPL080O` écran 1010, 266 lignes techniques et l'indicateur SAP `Entrée 1 / 224`. Seules 43 lignes sont visibles ; `CDCL` n'en fait pas partie et demeure donc `NOT_CHECKED`. Aucun scan d'usine, warehouse ou TVST n'a été répété.

Les vérifications SD encore ouvertes sont précisément : détermination CDCL complète, catégories poste/échéance, clés de copy control du Book, enregistrements PR00/K007 et configuration facturation/annulation. Les API de document et la présence des types de condition ne suffisent pas à les valider. La session participant `S4600-01` n'est pas disponible dans le runner ; ABDELJ n'a pas été utilisé pour ses préférences Fiori. Aucun SAP write, stock, Customizing ou FI/MM/ML.

**19 octobre 2026 — A4H / mandant 600 / ABDELJ — groupe de travail `01` — aucune écriture SAP.** L'autorisation explicite Phase 5 READ-only a permis des GET OData et lectures GUI ciblés. Les 36 énoncés du [fichier d'exercices](../data/books/S4600/S4600_EXERCISES.md) avaient déjà été analysés ; ni PDF ni FULL_CLEAN n'ont été relus. Ce complément ferme la lecture de `Z001`, mais **pas tous les contrats SD ni l'accès Fiori du participant**. Aucune écriture SAP n'a été effectuée.

## Synthèse et règle de comptage

| Classe actuelle, prudente | Exercices | Nombre |
|---|---|---:|
| `READY_TO_EXECUTE` | Aucun autre exercice complet prêt | 0 |
| `PARTIALLY_READY` | Aucun crédité sur la seule base d'une capacité SAP non vérifiée | 0 |
| `BLOCKED_BY_DEPENDENCY` | 4–8, 10, 12, 17–23, 25–27, 30, 32–35 — document prédécesseur ou usine 1010/1020 indispensable | 22 |
| `COMPLETED_AND_VERIFIED` | 2, 15, 24, 29 — réponses écrites vérifiées contre les solutions | 4 |
| `NOT_CHECKED` | 1, 3, 9, 11, 13, 14, 16, 28, 31, 36 — autre prérequis encore non vérifié | 10 |

Les cinq lignes forment une partition des **36 exercices**. `BLOCKED_BY_DEPENDENCY` signifie soit qu'un document prédécesseur n'est pas vérifié, soit qu'une usine exigée par l'exercice est absente ; un document préchargé équivalent pourrait lever la première cause après GET ciblé. `NOT_CHECKED` ne signifie jamais `MISSING`. Les lectures live confirment l'absence des usines 1010/1020 dans l'API installée, mais les identités Book des clients/articles peuvent différer de leurs numéros internes SAP. Aucun exercice transactionnel ne peut encore être annoncé exécutable sur preuve complète. Les quatre exercices conceptuels sont maintenant [répondus et vérifiés contre les solutions](s4600_conceptual_exercises_evidence.md).

## Résultats READ-only frais et portée de la preuve

Les GET ont utilisé `sap-client=600`, après contrôle local de l'identité configurée `ABDELJ`. Les trois `$metadata` (`API_BUSINESS_PARTNER`, `API_PRODUCT_SRV`, `API_PLANT_SRV`) ont répondu HTTP 200 ; les EntitySets `A_BusinessPartner`, `A_Customer`, `A_Product` et `A_Plant` sont confirmés. Aucun corps de réponse sensible, mot de passe ou en-tête d'authentification n'a été journalisé dans ce rapport.

| Cible | Lecture exacte du 19/10/2026 | Classification et limite |
|---|---|---|
| Usine `1010` ; usine `1020` | `API_PLANT_SRV/A_Plant('1010')` et `('1020')` : HTTP 404 chacun. Filtre `A_Plant` sur `CompanyCode eq '1010'` : HTTP 200, 0 ligne. | `CONFIRMED_MISSING` dans l'API des usines et aucune usine actuellement exposée pour la société 1010. Les affectations de valorisation, vente et expédition ne sont pas pour autant déterminées. |
| Clients `T-S50A01`, `T-S50B01` | `A_BusinessPartner` et `A_Customer` par clé littérale : HTTP 404 ; recherches exactes `SearchTerm1` et `BusinessPartnerIDByExtSystem` : HTTP 200, 0 ligne. | Clés et correspondances externes testées `CONFIRMED_NOT_FOUND` ; existence éventuelle sous un autre numéro SAP **NOT_CHECKED** faute de mapping S4600 vérifié. Ne pas réutiliser un client S4615. |
| Client `T-CUS01` | Clés littérales BP et Customer : HTTP 404. | Sortie attendue de l'exercice 9, **pas** un prérequis système manquant. |
| Articles `T-MS101/201/301`, `T-F101`, `T-D101` | `A_Product` par clé littérale : HTTP 404 ; recherches exactes `ProductOldID` : HTTP 200, 0 ligne. | Clés et anciens IDs testés `CONFIRMED_NOT_FOUND` ; autres mappings internes **NOT_CHECKED**. |
| Article `T-MS401` | `A_Product` par clé littérale : HTTP 404. | Sortie attendue de l'exercice 11, **pas** un prérequis système manquant. |
| Point `Z001` | Après une première erreur COM, reprise depuis `SESSION_MANAGER` : lecture SE16N/TVST puis scan READ complet **20/20 lignes** ; `Z001` absent. [Réponse SAP GUI](../runtime/sap_gui_responses/080efce4-7892-489d-adde-e3639695707f.json). | `CONFIRMED_MISSING` dans TVST. Le point 1010 de S4615 n'est pas substituable. Aucune création autorisée par cet audit. |
| Warehouse/EWM `1010` | `API_WAREHOUSE/$metadata` : HTTP 200, EntitySet `Warehouse`, clé `Warehouse`. `Warehouse('1010')` : HTTP 404. `API_WAREHOUSE_ORDER_TASK/$metadata` : HTTP 200, EntitySets `WarehouseOrder` et `WarehouseTask`. | Numéro `1010` `CONFIRMED_NOT_FOUND` dans **cette API EWM** ; un warehouse d'une autre technologie ou sous un autre identifiant reste `NOT_CHECKED`. Aucune tâche d'exercice créée n'était attendue. |
| Conditions PR00/K007 | `SD_PRICING_CONDITIONRECORD_SRV/$metadata` : HTTP 500. | Disponibilité du contrat de lecture et enregistrements `NOT_CHECKED` ; HTTP 500 n'est pas une preuve d'absence des conditions. |
| Participant `S4600-01`, Fiori, types SD, pricing effective et stock | Aucun contrat de lecture exact n'a fourni de résultat nouveau dans cet audit. | `NOT_CHECKED`. La session ABDELJ ne prouve pas l'accès du participant. |

Le bridge a confirmé `A4H/600/ABDELJ` en mode READ. La première erreur COM ne prouvait aucun état ; le **scan TVST complet réussi** fait foi. `VERIFIED_PRESENT` pour les API elles-mêmes n'implique pas `VERIFIED_PRESENT` pour les objets du Book. Aucun document généré par exercice n'a été qualifié à tort de configuration manquante.

## Complément ciblé : mappings, SD et Fiori

- **Mappings S4600 : aucun numéro SAP interne résolu de façon déterministe.** Aucun mapping `T-S50*`, `T-MS*`, `T-F1*` ou `T-D1*` dans les mappings/checkpoints Phase 5 S4615/S4650 consultés. Outre les clés littérales et champs externes négatifs ci-dessus, les GET bornés (10 résultats maximum) sur `A_Customer.CustomerName` et `A_BusinessPartner.OrganizationBPName1` contenant « Motormarkt », `SearchTerm1` commençant par `S4600`, `A_Product.Product` commençant par `T-MS`, ainsi que `A_ProductDescription` contenant `S4600`, `Phare` ou `Headlight`, retournent **0 candidat**. Cela confirme l'absence de correspondance par ces attributs, **pas** l'absence de tout objet sous un autre alias inconnu. Aucun client/article S4615/S4650 n'est substitué.
- **Commande `CDCL` :** VOV8 s'ouvre en READ (`SAPL080O`, écran 1010, table 266 lignes), mais le snapshot borné ne contient pas `CDCL` et le bridge installé n'expose pas de scan complet de cette table pour cette clé. `CDCL` reste `NOT_CHECKED` ; un GET `A_SalesOrder` borné sur `SalesOrderType='CDCL'` retourne 0 transaction, ce qui **ne prouve pas** l'absence du type de document. La référence Book `4-201` retourne aussi 0 commande et n'est pas traitée comme customizing manquant.
- **Postes/échéances et copy control :** aucune preuve live exacte pour les catégories requises ni les clés de copie S4600. Le registre d'interfaces classe `COPY_CONTROL` sans interface objet spécifique ; les contrats GUI existants sont ciblés sur d'autres types. État `NOT_CHECKED`, pas `CONFIRMED_MISSING`.
- **Prix :** `API_SLSPRICINGPROCEDURE_SRV/$metadata` répond 200. Les types de condition `PR00` (séquence `PR02`) et `K007` (`K307`) sont `VERIFIED_PRESENT` dans `A_SlsPricingConditionType`. La procédure `A17J02`, précédemment établie pour `1010/10/00/A/02` dans S4615, existe, mais un filtre exact ne trouve ni `PR00` ni `K007` parmi ses postes ; les premiers postes sont notamment `PCO1`/`PPR0`. **On ne connaît pas la procédure déterminée pour les clients S4600** ni leurs enregistrements de prix/remise. `SD_PRICING_CONDITIONRECORD_SRV/$metadata` répond HTTP 500 : ces enregistrements restent `NOT_CHECKED`.
- **Expédition :** `Z001` est `CONFIRMED_MISSING` dans TVST. Par conséquent aucune détermination vers ce point ne peut être déclarée utilisable, indépendamment de l'état non relu des lignes OVL2 et affectations. Pas de substitution par `1010`.
- **Facturation :** `API_OUTBOUND_DELIVERY_SRV` et `API_BILLING_DOCUMENT_SRV` répondent HTTP 200 sur `$metadata`, avec leurs EntitySets en-tête/poste ; cela ne vérifie ni le type de facture, ni la copie livraison→facture, ni la détermination comptable S4600. État `NOT_CHECKED`.
- **Fiori :** les seuls éléments du dépôt concernent des exigences de personnalisation pour `S4600-01`. Aucune session participant, attribution de catalogue ni test d'application n'est attesté. ABDELJ n'a pas été utilisé pour usurper ou simuler ce compte. Dépendance participant/Basis `NOT_CHECKED`.

## Contexte déjà vérifié, sans extrapolation vers S4600

- Les [états Phase 5](../docs/phase5/CURRENT_STATE.md) et [captures d'autres Books](s4615_plant_customizing_audit.md) établissaient `1010` société/organisation commerciale, `1010/10/00`, les affectations commerciales et le point d'expédition **1010**. Ces observations antérieures ne prouvent ni les données `T-*` de S4600 ni leur état **aujourd'hui**.
- L'audit antérieur `T001W/T001K` n'avait trouvé **aucune usine rattachée à la société 1010** ; `1710` appartenait à la société 1710. Le GET frais `API_PLANT_SRV` confirme maintenant `1010` et `1020` non trouvées et zéro usine exposée pour la société 1010.
- Le point d'expédition S4615 `1010` ne remplace pas le point **`Z0## → Z001`** exigé par S4600. La division commerciale `00` ne remplace pas une usine ou un emplacement de stockage ; le « numéro de magasin 1010 » du Book est un objet warehouse/EWM distinct.
- `C615-A01`, `P615-101`, `ZA01` et `ZF01` sont S4615, pas des remplaçants des clients `T-S50*` ni des articles `T-MS*`. Le problème `C+039` documenté pour l'aire **1710** n'est pas une preuve que tout mouvement de stock S4600 échouerait.
- Le [suivi S4650](../books/S4650/S4650_PROGRESS.md) signalait la division commerciale **03** absente le 17/10 ; S4600 utilise surtout `00`, donc ce constat n'est pas un blocage S4600 par défaut.

## Matrice complète des exercices

La colonne « État » ci-dessous conserve la **classification documentaire initiale** pour tracer les dépendances ; la table de synthèse ci-dessus est la **classification actuelle**. Les exercices 2, 15, 24 et 29 sont clos par réponse écrite. Les exercices 12, 17–23, 30, 32, 34 et 35 passent de `NOT_CHECKED` à `BLOCKED_BY_DEPENDENCY` à cause de l'absence vérifiée de l'usine 1010/1020 nécessaire à leur résultat complet.

Abréviations : `A` équipe formation/SD ; `B` admin, FI-MM, Basis, EWM ou PP ; `C` document prédécesseur à créer par un exercice ; `D` contrat d'automatisation/Fiori non prouvé. « Écriture » décrit **l'exercice futur**, non cet audit. Toutes les clés `##` restent dans le Book ; ici le groupe 01 donne `T-S50A01`, `T-S50B01`, `T-CUS01`, `T-MS101/201/301/401`, `T-F101`, `T-D101`, `Z001` et `S4600-01` lorsque ces modèles sont utilisés.

| # | Exigence du Book, objet/clé et résultat à vérifier | Application ou route indiquée ; dépendance SD/MM/FI/PP/EWM | État / responsabilité / écriture future | Prochain contrôle ciblé |
|---:|---|---|---|---|
| 1 | `S4600-01` : groupe Fiori « Mes applications favorites », trois applications, valeurs par défaut société/warehouse/org `1010`, canal `10`, secteur `00` ; recherche Modifier commandes | FLP, catalogues et personnalisation utilisateur ; Basis/Fiori | `NOT_CHECKED` B/D ; oui, préférences personnelles | Session participant et catalogues exacts, pas paramètres ABDELJ |
| 2 | Nommer société, organisation commerciale, canal, secteur, usine, emplacement, point d'expédition et warehouse ; expliquer leurs affectations | Questions conceptuelles ; valeurs 1010 vérifiées auparavant mais sans besoin de write | `READY_TO_EXECUTE` A ; non | Répondre aux questions du Book, conserver distinction secteur/usine |
| 3 | Commande `CDCL`, `T-S50A01`, `T-MS101`×10 et `T-MS201`×20, référence `4-201`, date J+7 ; ID de commande | VA01/Fiori ; client, ventes article, prix, ATP et org `1010/10/00` | `NOT_CHECKED` A/B/D ; oui | GET exact client/articles et type CDCL, puis disponibilité et prix |
| 4 | Afficher la commande de 3 : paiement, valeur, poids, prix, échéances, partenaires et statut | Affichage commande/flux ; dépend **3** | `BLOCKED` C ; non | Numéro de commande de 3 ou équivalent préchargé démontré |
| 5 | Livraison de la commande de 3 avec `Z001`, quantités, emplacement, statuts et stock `T-MS101/1010` | Création livraison, usine/point/emplacement, stock ; dépend **3** | `BLOCKED` C+B ; oui | Commande éligible, puis GET exact `Z001`/usine/stock |
| 6 | Tâches du warehouse `1010`, confirmation de prélèvement, PGI, stock et flux livraison | Application tâches magasin/EWM, mouvement MM ; dépend **5** | `BLOCKED` C+B/D ; oui | Livraison de 5, intégration EWM/warehouse et stock |
| 7 | Facture de la livraison, transfert FI automatique, comptes et statut | Facturation SD/FI ; dépend **6** | `BLOCKED` C+B ; oui | Livraison PGI, copie vers facture et détermination FI |
| 8 | Encaissement de la facture : `DZ`, société `1010`, banque `11100000`, EUR, client `T-S50A01`, escompte | Écriture et lettrage FI ; dépend **7** | `BLOCKED` C+B ; oui | Facture et montant exact ; compte/droits FI validés |
| 9 | Créer BP externe `T-CUS01`, BPAB, FLCU00/FLCU01, adresse DE/Hambourg, société 1010, compte collectif `12100000`, zone 1010/10/00, taxe DE/TTX1=1, partenaires | BP et extensions FI/SD ; données Book explicites, mais tax/compte/numérotation à valider | `NOT_CHECKED` A+B ; oui | GET exact doublon, metadata BP, compte 12100000 et taxe installée |
| 10 | Ajouter `T-S50A01` comme réceptionnaire de `T-CUS01`, puis commande `CDCL`/`T-MS201`×2, référence `5-901` | BP partenaires et VA01 ; dépend **9** | `BLOCKED` C+A ; oui | BP de 9, partenaire T-S50A01 et produit T-MS201 |
| 11 | Créer `T-MS401` à partir de `T-MS101`, texte ADV « Article fragile ! », prix 35 EUR, puis commande de test | MM01/données commerciales, condition prix, VA01 ; `T-MS401` est **sortie normale de l'exercice** | `NOT_CHECKED` A+B ; oui | GET de la référence T-MS101, vues/org et mode numérotation |
| 12 | Fiche infos client-article `T-S50A01/T-MS101`, numéro `K-MS-01`, commande puis livraison `Z001` ; description client dans livraison | Données de base SD, VA01, livraison ; client/article et logistique | `NOT_CHECKED` A+B ; oui | GET client/article, route fiche infos et point Z001 |
| 13 | PR00 client/article `T-S50A01/T-MS101` : 1→53, 10→51, 20→49 EUR/PC ; commande et prix 51 | Condition de prix, échelles quantité, VA01 | `NOT_CHECKED` A/D ; oui | Accès PR00/clé et doublon de condition, client/article |
| 14 | K007 `T-S50A01` : valeur 100→−1 %, 500→−2 %, 1000→−3 % ; commande et remise | Condition et échelles de valeur, VA01 | `NOT_CHECKED` A/D ; oui | Accès K007, doublon et pricing de la commande |
| 15 | Expliquer quatre classes de conditions, prix par canal et modification manuelle | Questions de détermination du prix | `READY_TO_EXECUTE` A ; non | Rédiger les réponses étayées par la solution Book |
| 16 | Proposition de postes `PV` pour groupe 01, `T-MS101/201`×5 ; affecter à `T-S50A01`, copier vers commande | Application propositions Fiori, BP, VA01 | `NOT_CHECKED` A/D ; oui | Existence PV, application et client/articles exacts |
| 17 | Commande `CDCL` volontairement incomplète (`T-MS201`), corriger référence/poids puis livraison `Z001` | VA01, contrôle d'incomplétude, livraison | `NOT_CHECKED` A+B/D ; oui | Client/article et schéma d'incomplétude, point Z001 |
| 18 | Commande `T-S50B01` avec T-MS101/201 ; lire détermination usine, point et itinéraire | VA01, données client/article et détermination expédition | `NOT_CHECKED` A+B ; oui | GET master sales/plant et règles expédition exactes |
| 19 | Commande T-S50A01 avec T-MS101/301, réceptionnaire T-S50B01 ; dates/route, puis tentative livraison | VA01, ordonnancement et détermination de route, Z001 | `NOT_CHECKED` A+B ; oui | Clients/articles, règles de route/temps et usine |
| 20 | Lire contrôle ATP de `T-MS301` en usine 1010 et usine proposée chez `T-S50B01` | Affichage article/BP, ATP ; lecture seule | `NOT_CHECKED` A+B ; non | GET exact vues ATP et client, pas besoin d'ordre préalable |
| 21 | Stock/besoins `T-MS301/1010` avant/après commande `CDCL`×20 | Couverture/MRP, transfert des besoins | `NOT_CHECKED` A+B ; oui | Vues usine/MRP, stock et configuration transfert des besoins |
| 22 | Commande T-S50A01, T-MS101/201×10 ; analyser livraison complète/partielle | VA01, master client/article et ATP | `NOT_CHECKED` A+B ; oui | Données et codes de livraison/ATP exacts |
| 23 | Contrôler ATP `T-MS301` groupe `02` en usines 1010 **et 1020**, stock/appros puis commande ×95 | VA01/ATP, deux usines, stock et périmètre de contrôle | `NOT_CHECKED` A+B ; oui | GET deux usines, vues article, stock et règle ATP 02 |
| 24 | Expliquer interaction ATP, livraisons partielles et ordonnancement | Questions conceptuelles | `READY_TO_EXECUTE` A ; non | Répondre sur la base de la solution Book |
| 25 | Création collective des livraisons du groupe 01 via `Z001` | App livraison collective ; commandes éligibles, usine/point ; dépend des commandes antérieures | `BLOCKED` C+B/D ; oui | Constituer liste d'ordres non livrés après 3/10/… |
| 26 | Tâches magasin collectives pour T-S50A01/B01, puis PGI | EWM/warehouse 1010, stock ; dépend **25** | `BLOCKED` C+B/D ; oui | Livraisons 25, warehouse/tâches et stock |
| 27 | VF04/facturation collective des livraisons, simulation/ventilation et journal | SD billing/FI ; dépend **26** | `BLOCKED` C+B/D ; oui | Livraisons éligibles et configuration billing/copie |
| 28 | Demande `DO` → offre `OF` → commande `CDCL` pour T-S50A01/T-MS201, avec statut de référence | VA01/Fiori avant-vente, copie entre documents | `NOT_CHECKED` A/D ; oui | Client/article, types DO/OF et copy control exact |
| 29 | Expliquer demande/offre, pricing et ATP | Questions conceptuelles | `READY_TO_EXECUTE` A ; non | Répondre avec la solution Book |
| 30 | MTO `T-F101/1010` : stratégie 20, commande, MRP, conversion ordre planifié→ordre de fabrication | PP/MRP, nomenclature/gamme annoncées préchargées dans le Book | `NOT_CHECKED` B+A/D ; oui | GET exact T-F101, vues MRP3, BOM/gamme et droits PP |
| 31 | Service `T-D101`, commande T-S50A01×3 heures et facture liée à commande | Vente de service, produit DIEN et item non livrable ; potentiellement **indépendant du PGI** | `NOT_CHECKED` A+B/D ; oui | GET exact produit/service, client, type de poste et copie commande→facture |
| 32 | Commande T-S50A01/T-MS101, livraison `Z001`, PGI, facture, demande d'avoir `DNC` pour 3 pièces | Chaîne SD/MM/FI et réclamation ; documents créés **dans l'exercice** | `NOT_CHECKED` A+B/D ; oui | Client/article, logistique puis DNC/motif/copie |
| 33 | Annuler l'avoir créé en **32**, afficher document d'annulation | Application Gestion des documents de facturation ; dépend **32** | `BLOCKED` C+B ; oui | Avoir réel de 32 et règles d'annulation FI |
| 34 | Retour `RE` de T-S50A01/T-MS301×3 en **usine 1020**, livraison retour, entrée marchandises, avoir | Retour SD/MM, stock 1020, comptabilisation | `NOT_CHECKED` A+B/D ; oui | Client/article, usine 1020 et contrat retour/copie |
| 35 | Commande `CDCL` T-S50A01/T-MS101 volontairement incomplète, correction via application puis livraison | Fiori Sales Order Processing, incomplétude/point | `NOT_CHECKED` A+D/B ; oui | Application/catalogue et master/config exacts |
| 36 | Analyse flexible des entrées de commandes en EUR, mois courant, client, graphique/export | Application analytique Fiori, droits et dataset de commandes | `NOT_CHECKED` B/D ; non côté SAP | Accès application et présence de données pertinentes |

Les transactions/applications nommées dans la matrice proviennent des énoncés/solutions compactes du Book ; leur **disponibilité dans A4H/600 n'est pas confirmée**. Les résultats attendus des exercices sont les ID et statuts affichés, les montants/échelles ou les effets fonctionnels mentionnés, **non des numéros SAP inventés**.

## Graphe de dépendances et contrôles live à terminer

```text
S4600-01 + Fiori/catalogues ──────────────────────────────── ex. 1, 16, 35, 36
1010/10/00 + T-S50A01/B01 + T-MS101/201/301 + CDCL ────── ex. 3, 9–14, 17–23, 28, 31–32, 34–35
usine 1010 + vues/stock + Z001 + détermination shipping ── ex. 5–6, 12, 17–19, 23, 25–27, 32
warehouse 1010/EWM + stock/PGI ───────────────────────────── ex. 6, 26, 32
ex. 3 → 4 → 5 → 6 → 7 → 8
commandes antérieures → 25 → 26 → 27
ex. 9 → 10       ex. 32 → 33
usine 1020 + stock/retours ───────────────────────────────── ex. 23, 34
T-F101 + MRP/BOM/gamme ───────────────────────────────────── ex. 30
T-D101 + copie commande→facture ──────────────────────────── ex. 31
```

**Contrôles READ-only restant à terminer**, après les GET ciblés ci-dessus :

1. Participant `S4600-01` et FLP : authentification, groupe/pages, catalogues et applications exactes ; ne pas tester la personnalisation sur ABDELJ.
2. Org : usines **1010 et 1020** absentes dans `API_PLANT_SRV`, point **Z001** absent après scan TVST complet ; restent à vérifier les affectations vente→usine, valorisation, emplacements et le mode exact de gestion du warehouse/EWM 1010.
3. Master groupe 01 : après les recherches négatives sur IDs littéraux/externes, obtenir les correspondances logiques→SAP éventuelles, puis vérifier rôles, extensions, prix/taxe, vues vente/usine/MRP/valorisation, unités et stock. `T-CUS01` et `T-MS401` sont des **sorties à créer par les exercices 9/11**, pas des prérequis système présumés manquants.
4. Customizing ciblé : `CDCL`, `DO`, `OF`, `PV`, `DNC`, `RE`, catégories poste/échéance, copie commande→livraison→facture, PR00/K007, incomplétude, partenaires, ATP/besoins, route, retours, facturation/annulation. Vérifier uniquement les clés qu'utilisent les exercices.
5. Documents exacts et équivalents de formation : inquiry/offre/commandes/livraisons/factures et pièces FI liés au groupe 01, sans qualifier les **sorties normales** des exercices de « configuration absente ».

Les blocages live confirmés sont **l'absence d'usines 1010 et 1020** dans `API_PLANT_SRV`, de toute usine exposée pour la société 1010, du point `Z001` dans TVST et du warehouse `1010` dans `API_WAREHOUSE`. Les autres entrées sont des **risques/prérequis à confirmer**, pas des absences SAP prouvées. En particulier, un 404 sur la clé littérale d'un article ou client ne ferme pas la possibilité d'un ID SAP interne.

## Décisions, responsabilités et ordre d'exécution

- **Notre équipe (A) :** répondre aux exercices théoriques 2, 15, 24, 29 ; préparer les données propres au groupe et les conditions PR00/K007 après contrôle de doublon ; créer seulement les documents de l'exercice concerné lorsque ses prérequis sont validés. Pas de remplacement par des objets S4615.
- **Admin/Basis/FI-MM/EWM/PP (B) :** session/catalogues `S4600-01` ; usine 1010 et 1020/valorisation et comptes si nécessaires ; entrepôt 1010/EWM, stock initial, configuration MRP/BOM/gamme, paiement FI et retours. Regrouper ces décisions après les GET ciblés, pas à partir de l'ancienne absence seule.
- **Dépendance (C) :** exécuter les chaînes 3→8, 9→10, commandes→25→27 et 32→33 dans cet ordre. Une commande, livraison ou facture produite par l'exercice précédent n'est pas une donnée de base système manquante.
- **Automatisation (D) :** disponibilité Fiori/analytics, EWM et routes de lecture/write exactes à vérifier ; ne pas inventer un service ni un control ID. Aucun adaptateur supplémentaire n'a été codé pendant cet audit.

**Prochaines actions :** (1) demander au propriétaire des données de formation le mapping SAP des objets `T-*` ; (2) obtenir une décision admin sur usines 1010/1020, `Z001` et EWM ; (3) compléter la lecture ciblée de `CDCL`, des catégories et des copies SD ; (4) vérifier la procédure de prix réellement déterminée et les enregistrements de condition ; (5) vérifier une session autorisée du participant `S4600-01` pour Fiori. Les exercices conceptuels 2, 15, 24, 29 sont déjà clos par [preuve écrite](s4600_conceptual_exercises_evidence.md).

**Opérations suspendues :** toutes les écritures SAP ; toute modification FI/MM, Material Ledger, FINSC/T000/devises ou transport ; PGI/stock tant que usine, valorisation, EWM et stock ne sont pas prouvés ; et toute création de documents S4600 sur des identifiants non vérifiés.

## Références et limites de preuve

Sources principales : [exercices S4600](../data/books/S4600/S4600_EXERCISES.md), [suivi S4600](../data/books/S4600/S4600_PROGRESS.md). Sources SAP antérieures : [état Phase 5](../docs/phase5/CURRENT_STATE.md), [audit plant 1010](s4615_plant_customizing_audit.md), [inventaire des changements](sap_all_changes_inventory.md), [mappings vérifiés](../data/provisioning/phase5_identity_mappings.json). Sources live de cet audit : GET `$metadata` et clés/filtres exacts des trois API nommées dans le tableau ; réponse du bridge `STATUS` A4H/600/ABDELJ en mode READ ; erreur COM du GET GUI TVST. Les anciens rapports ne sont pas présentés comme un GET frais du 19/10/2026.
