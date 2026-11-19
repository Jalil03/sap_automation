# S4600 — Lot des exercices non encore traités — 22/10/2026

## Résultat

Environnement contrôlé : **A4H / 600 / ABDELJ**, groupe **00**, domaine commercial **FR10 / 10 / 1W**.

Les exercices **12, 16, 21, 22 et 25 sont exécutés et vérifiés**, selon l'adaptation FR10 retenue. L'exercice **32 est partiellement exécuté**, sans mouvement de stock ni facture.

| Exercice | Résultat vérifié | Documents / objets |
|---|---|---|
| 12 — Fiche client-article | `K-MS-00` résout bien l'article `10000282`. La désignation « Phare Premium » est reprise dans la commande et la livraison. Quantité : 10. | Fiche client-article `1000000112 / FR10 / 10 / 10000282` ; commande **159**, référence `5-1900` ; livraison **80000087**. |
| 16 — Proposition de postes | Proposition `PV`, valable du 22/10 au 31/12/2026, contenant `10000282 × 5` et `10000283 × 5`. Affectation au client vérifiée par API. La proposition est automatiquement proposée puis copiée avec ses quantités. | Proposition **50000001** ; commande **160**, référence `00-Proposition`, montant net **1 150 EUR**. |
| 21 — Transfert des besoins | Commande de 20 pièces de `10000284`. Le nouveau besoin apparaît après sauvegarde, à la date de mise à disposition du poste. | Commande **161**, référence `7-600`, montant net **2 400 EUR**. |
| 22 — Livraisons complètes / partielles | Commande de `10000282 × 10` et `10000283 × 10`. Livraison complète non exigée ; code livraison partielle vide aux deux postes. | Commande **162**, référence `7-700`, montant net **2 300 EUR**. |
| 25 — Création collective de livraisons | Une seule exécution collective, limitée aux commandes vérifiées **156, 157, 160, 161, 162**. Les neuf postes et leurs quantités sont intégralement relus par API. Aucun poste étranger au lot. | Trois livraisons : **80000088, 80000089, 80000090**. |
| 32 — Préparation uniquement | Commande de cinq pièces de `10000282` et livraison créées. Arrêt avant prélèvement, sortie de marchandises, facture, demande d'avoir et avoir. **Exercice non terminé.** | Commande **163**, référence `9-100`, montant net **750 EUR** ; livraison **80000091**. |

La création des propositions et leur reprise ont utilisé SAP GUI faute de route API d'écriture démontrée pour cette fonction. L'affectation de la proposition au client a utilisé OData PATCH. Les commandes 161, 162, 163 et les livraisons des exercices 12 et 32 ont utilisé OData. L'exercice 25 a utilisé le traitement collectif GUI VL10A, avec relecture OData. Les écrans Fiori spécifiques ne sont pas revendiqués comme testés : il s'agit des validations fonctionnelles via les routes disponibles.

## Résultats pédagogiques

### Exercice 21

- Stock initial dans FR10 : **3 170 pièces** de `10000284`.
- Avant la commande 161 : un besoin d'une pièce existe déjà pour le poste 20 de la commande 157.
- Après : nouveau besoin **20 pièces**, référence `0000000161/000010/0001`, daté du **27/10/2026**.
- Relecture indépendante de l'échéance : `MBDAT = 20261027`, `EDATU = 20261029`, quantité commandée et confirmée = 20.
- La date du besoin correspond donc à la **mise à disposition**, pas à la livraison demandée du 29/10.
- Aucun stock n'a été consommé par la création de la commande.

### Exercice 22

- En-tête : `CompleteDeliveryIsDefined = false`.
- Postes 10 et 20 : champ SAP `KZTLF` vide, relu par RFC après découverte de ses métadonnées.
- Le code de livraison complète provient des données commerciales du client. Le code livraison partielle du poste peut provenir de la fiche client-article, sinon du client.
- L'absence d'exigence de livraison complète à l'en-tête ne suffit pas à elle seule à autoriser tous les fractionnements : l'accord au poste reste à vérifier.

### Exercice 25

La commande **157** apparaît deux fois car ses postes ont des réceptionnaires différents. Le traitement collectif a également regroupé des commandes compatibles dans une livraison commune : le nombre de lignes de sélection n'est donc pas le nombre de livraisons créées.

| Livraison | Commandes sources | Quantités par article |
|---|---|---|
| **80000088** | 156 | `10000282 × 7` ; `10000283 × 8` |
| **80000089** | 157 poste 10, 160, 161, 162 | `10000282 × 20` ; `10000283 × 15` ; `10000284 × 20` |
| **80000090** | 157 poste 20 | `10000284 × 1` |

La consigne de ne pas créer de livraison pendant l'exercice 19 a été respectée lors de cet exercice. Les livraisons de la commande 157 ont été créées ensuite, dans le périmètre de l'exercice 25.

## Modifications et sécurité

- Fiche client-article `K-MS-00` créée pour le couple client/article indiqué au book.
- **Modification persistante du client commun `1000000112` :** sa proposition de postes par défaut, auparavant vide, est maintenant **50000001**, uniquement dans FR10/10/1W. Cette affectation était explicitement demandée par l'exercice 16.
- Aucun prix ni remise des objets communs n'a été modifié dans ce lot.
- Aucune modification de paramétrage organisationnel, fiscal, de ledger, de devises ou de Material Ledger.
- Aucun prélèvement, aucune sortie ou entrée de marchandises, aucune facture, aucun avoir ni annulation comptable dans ce lot.
- Les livraisons nouvelles restent non prélevées, sans sortie de marchandises. Le magasin est encore vide ; le stock de référence existe en **FR10 / 0001**.
- Les livraisons déjà présentes 80000085, 80000086 et 80000087 n'ont pas été réexécutées dans le traitement collectif.
- Chaque écriture a été précédée d'un contrôle et d'un enregistrement de son périmètre/empreinte. Les succès ont fait l'objet d'une relecture indépendante.

## Incidents techniques réconciliés

- Après la sauvegarde de la proposition, la première relecture RFC a échoué (`OPTION_NOT_VALID`, réutilisation d'une instance de fonction avec paramètres cumulés). Une **nouvelle connexion en lecture seule** a retrouvé la proposition et ses deux postes. La sauvegarde n'a pas été répétée.
- La première lecture BAPI de stock avec identifiant article externe n'a pas fourni de lignes exploitables. L'identifiant interne SAP à 18 caractères a donné un retour de succès et l'état dynamique complet ; une liste vide n'a pas été traitée comme une absence.
- La vue commerciale de `10000284` n'indique pas de division de livraison. FR10 est néanmoins vérifié sur le client et sur le poste existant de la commande 157 ; les nouveaux postes ont été relus en FR10. Aucune fiche article n'a été corrigée inutilement.
- La première comparaison des livraisons utilisait des formats différents de numéros de poste (`10` / `000010`). La normalisation a été corrigée et une nouvelle **lecture seule** a confirmé les neuf postes. La création collective n'a pas été répétée.

## Exercices du lot encore ouverts

| Exercice | Blocage / dépendance exacte | Plus petite suite |
|---|---|---|
| **13–14** | Le plan validé réserve les prix/remises aux objets participants des exercices 9 et 11, non créés. | Débloquer ces objets ou approuver un autre périmètre isolé ; ne pas modifier les prix partagés par défaut. |
| **26** | Trois livraisons prêtes pour préparation, mais magasin et prélèvement non renseignés. La sortie 601 consomme le stock et génère des pièces comptables : autorisation FI/MM exacte requise. | Autoriser uniquement la préparation et les sorties des livraisons 80000088–80000090, FR10/0001, quantités du tableau, date proposée 22/10/2026. |
| **27** | Sorties de marchandises du 26 non effectuées ; simulation/ventilation puis facturation collective restent à exécuter. | Après 26, vérifier les cibles et obtenir l'autorisation exacte de facturation ; aucune facture n'est créée ici. |
| **32** | Commande/livraison préparées, mais étapes stock et financières non autorisées dans ce périmètre exact. | Autorisation distincte pour 80000091, puis contrôles de facturation et du contrat d'avoir pour trois pièces endommagées. |
| **33** | L'avoir de l'exercice 32 n'existe pas encore. | Terminer 32, identifier l'avoir exact, puis autoriser son annulation comptable. |
| **34** | Le book exige la division 1020 pour le retour ; sa substitution n'est pas fonctionnellement vérifiée. Les opérations d'entrée de stock/avoir nécessitent aussi une autorisation exacte. | Vérifier et décider l'adaptation de la division de retour avant de créer le document. Ne pas supposer FR10 automatiquement. |
| **35** | L'exercice exige l'application Fiori Analyse et résolution. Le pilotage du navigateur requis n'est pas disponible dans cette session. | Rendre cette application pilotable ; ne pas créer une commande volontairement incomplète en prétendant avoir validé le parcours Fiori. |

Les exercices déjà laissés de côté (dont 9, 11, 17, 20 et 31) ne sont pas déclarés débloqués par ce lot. Leurs constats précédents restent applicables.

## Contrôles et preuves

- Compilation Python des scripts concernés : **PASS**.
- Vérifications hors ligne de onze journaux d'exécution, du delta MRP et des accords de livraison : **PASS**. Ce n'est pas une suite complète de tests de non-régression ; aucun test unitaire n'a exécuté d'écriture SAP.
- Point de reprise : `runtime/sap_reads/s4600_remaining_batch_checkpoint_2026-10-22.json`.
- Empreinte du périmètre **proposé, non approuvé** pour 26 : `70c0f7529e90bdd014f54c772b2360521f90ff039c8d872195590c68ee91a070`.
- Journaux : `runtime/sap_writes/s4600_ex12_*.json`, `s4600_ex16_*.json`, `s4600_ex21_order.json`, `s4600_ex22_order.json`, `s4600_ex25_collective_deliveries.json`, `s4600_ex32_order.json`, `s4600_ex32_delivery.json`.
- Relectures : `runtime/sap_reads/s4600_ex16_details_ex21_stock_before_normalized.json`, `s4600_ex16_details_ex21_stock_after21.json`, `s4600_ex21_22_fields_readback.json`, `s4600_ex25_collective_due_selection.json`, `s4600_next_batch_readiness.json`.
