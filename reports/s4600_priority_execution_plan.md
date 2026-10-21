# S4600 — plan d'exécution prioritaire

## Complément de clôture environnement

Le [plan de clôture](s4600_environment_completion_plan.md) ajoute la procédure Fiori manuelle, la revue manifeste v1.1 et les contrats préparés des exercices 1, 13, 14 et 31. Le contrôle du navigateur n'étant pas connecté, aucune identité ou tuile n'est annoncée comme vérifiée. L'ordre reste : (1) session `S4600-01` et exercice 1 ; (2) mappings `T-*` ; (3) lectures SD exactes ; (4) PR00 exercice 13 ; (5) K007 exercice 14 ; (6) service exercice 31 lorsque ses mappings et copy control sont prouvés.

Le premier write candidat est la **personnalisation utilisateur de l'exercice 1**, exclusivement dans `S4600-01`. Le premier write de données de formation reste **PR00 exercice 13**. Aucun des deux n'est autorisé à l'exécution par cette préparation.

**État au 19 octobre 2026 — A4H/600/ABDELJ — groupe `01`.** S4600 est le seul Book actif. Ce passage est strictement READ-only : aucune création, sauvegarde, écriture de document, modification de Customizing ou opération de stock. Les Books S4615/S4650 n'ont pas été modifiés.

## Résultat exécutif

- `COMPLETED_AND_VERIFIED` : **4/36** — exercices 2, 15, 24 et 29.
- Nouvel exercice `READY` : **aucun**. Les contrôles ciblés ont réduit l'incertitude, mais aucun des 32 exercices restants ne satisfait encore toutes ses exigences.
- Plus proches sans logistique : **1, 20 et 36**, respectivement bloqués par la session participant, les mappings de données, et l'accès analytique/dataset.
- Prochain write contrôlé recommandé : **Exercice 13, enregistrement PR00**, seulement après résolution de `T-S50A01` et `T-MS101`, GET anti-doublon et preuve du contrat d'accès installé.

## Contrôles SD ciblés

| Contrôle | Exigence Book | Preuve SAP / dépôt | Résultat |
|---|---|---|---|
| Type de commande | `CDCL` dans de nombreux exercices | VOV8 live : A4H/600/ABDELJ, `SAPL080O` écran 1010, 266 lignes techniques, texte SAP `Entrée 1 / 224`. Les 43 lignes visibles ne contiennent pas CDCL. GET transactionnel CDCL : zéro commande | `NOT_CHECKED`. La vue n'a pas été parcourue entièrement ; zéro commande ne prouve pas l'absence du type |
| Catégories de poste | Ex.31 exige que le service détermine `TAD`; les autres sont déterminées par le système | `TAD` est explicite dans la solution. Aucun contrat de lecture live ne confirme sa détermination pour CDCL/T-D101 | `BOOK_CONFIRMED`, `SAP_NOT_CHECKED` |
| Catégories d'échéance | À observer dans commandes/ATP ; aucun code imposé par le Book | Aucun code inventé et aucune détermination live complète disponible | `NOT_CHECKED` |
| Pricing | Ex.13 `PR00` ; ex.14 `K007` | Types présents : PR00/accès PR02 et K007/accès K307. `SD_PRICING_CONDITIONRECORD_SRV/$metadata` a déjà répondu HTTP 500 ; pas de répétition. Procédure client S4600 inconnue | Types `VERIFIED_PRESENT`; enregistrements, clés d'accès effectives et procédure `NOT_CHECKED` |
| Copy control | DO→OF→CDCL (ex.28), CDCL→livraison→facture, commande service→facture, facture→DNC→avoir/annulation | Registre : aucune API objet dédiée. Les contrats GUI existants visent d'autres Books/clés et ne sont pas transposés | `NOT_CHECKED` |
| Facturation/annulation | Ex.7/27 facture livraison ; ex.31 facture commande ; ex.32 avoir ; ex.33 annulation | Métadonnées Billing API accessibles. Elles prouvent l'interface de lecture, pas types, copie, blocage, annulation ni transfert FI | `NOT_CHECKED` |
| Données de base 1010/10/00 | Clients `T-S50*`, articles `T-MS*`, `T-F101`, `T-D101` | Zone de vente existante d'après preuve antérieure. Clés littérales/alias/recherches bornées sans mapping ; aucune correspondance déterministe | Zone `VERIFIED_PRESENT`; identités/vues organisationnelles `UNRESOLVED` |
| Session Fiori | Ex.1 et 36 ; applications Fiori dans plusieurs exercices | Le runner expose seulement la session GUI ABDELJ. Aucune session `S4600-01` ni catalogue participant vérifié | `NOT_CHECKED`; ABDELJ ne remplace pas le participant |

Le runner courant ne possède pas de scan READ ciblé pour CDCL, catégories/échéances ou les clés de copie S4600. Cette limite appartient à notre capacité de lecture ; elle n'est pas classée comme absence SAP ou blocage administrateur.

## Ordre des 32 exercices restants

Chaque exercice apparaît une seule fois, selon son verrou principal actuel. Un verrou secondaire peut rester après levée du premier.

### A — Sans SAP write

| Priorité | Exercice | Action | Verrou exact |
|---:|---:|---|---|
| 1 | 1 | Vérifier puis réaliser navigation, favoris et valeurs par défaut Fiori | Session autorisée `S4600-01` et catalogues non disponibles |
| 2 | 20 | Afficher ATP/usines de T-MS301 et données de T-S50B01 | Mappings internes et vues organisationnelles non résolus |
| 3 | 36 | Exécuter l'analyse flexible et vérifier filtre/graphique/export | Catalogue analytique participant et dataset de commandes non prouvés |

### B — Avec writes de données de formation autorisés et contrôlés

| Ordre | Exercices | Write normal de l'exercice | Conditions avant exécution |
|---:|---|---|---|
| 1 | 13 | Créer PR00 avec échelle 1/10/20 = 53/51/49 EUR/PC | Mappings T-S50A01/T-MS101, accès installé, anti-doublon |
| 2 | 14 | Créer K007 avec échelle de valeur 100/500/1000 = −1/−2/−3 % | Mapping client, accès K007, anti-doublon |
| 3 | 9 | Créer T-CUS01 | BPAB/numérotation, compte 12100000 et taxe DE/TTX1=1 validés et approuvés |
| 4 | 11 | Créer T-MS401 à partir d'une référence fonctionnellement valide | T-MS101 résolu, type/unité/vues et implications valorisation validés |
| 5 | 12, 16 | Créer fiche client-article puis proposition de postes | Clients/articles résolus, applications/contrats de write prouvés |
| 6 | 17, 18, 19, 22, 28, 31, 35 | Créer les documents propres à chaque exercice | CDCL/catégories/copie et master data ; Z001 seulement pour les résultats de livraison |

`T-CUS01` et `T-MS401` sont des **sorties** des exercices 9 et 11, pas des prérequis administrateur à fournir. Les documents de vente des exercices ne doivent pas être précréés comme configuration.

### C — Décisions/objets administrateur indispensables

| Exercices | Dépendance administrateur principale |
|---|---|
| 3 | Mappings/vues client-articles et CDCL/pricing ; la commande ne devient READY qu'après validation complète |
| 21 | Usine 1010, vues MRP/stock et transfert des besoins |
| 23 | Usines 1010 et 1020, valorisation, stock et ATP 02 |
| 30 | Usine 1010, vues MRP, nomenclature/gamme et autorisations PP |
| 32 | Usine/point/stock, PGI, billing/FI et chaîne d'avoir |
| 34 | Usine 1020, retour, mouvement MM, stock et billing/FI |

### D — Dépendances sur exercices antérieurs

| Chaîne | Exercices | Dépendance |
|---|---|---|
| Commande initiale | 4 | commande de l'exercice 3 |
| Order-to-cash | 5 → 6 → 7 → 8 | commande 3, puis livraison, prélèvement/PGI, facture, encaissement |
| Partenaire | 10 | client créé en 9 |
| Traitements collectifs | 25 → 26 → 27 | commandes éligibles, livraisons, prélèvement/PGI, échéancier de factures |
| Annulation | 33 | avoir réellement créé dans l'exercice 32 |

## Responsabilités et blocages minimaux

### Notre équipe

- Ajouter ou utiliser un contrat READ ciblé pour le scan complet CDCL, catégories/échéances et copy control ; ne jamais interpréter une fenêtre visible comme la table entière.
- Résoudre les identités logiques `T-*` à partir d'une source de formation fiable ; préparer les writes des exercices 9, 11, 13, 14 et 16 avec anti-doublon/readback.
- Exécuter ensuite les documents dans l'ordre des dépendances et conserver les numéros réels.

### Participant / Basis-Fiori

- Fournir une session autorisée `S4600-01` et vérifier catalogues/apps des exercices 1 et 36. Les personnalisations doivent rester dans cette session, jamais dans ABDELJ.

### Administrateur SAP SD/LE/EWM/FI-MM

- Décider/provisionner les usines 1010/1020 et leur contexte société/valorisation.
- Créer/affecter le point d'expédition `Z001` selon les valeurs du Book et la détermination installée.
- Établir le warehouse/EWM 1010, emplacements, intégration et stock de formation.
- Confirmer les prérequis de compte/taxe pour T-CUS01 et de valorisation pour les articles créés.
- Confirmer la configuration SD installée si notre contrat READ ciblé ne peut pas l'exposer.

## Cinq premières actions exécutables

1. Ouvrir une session **S4600-01** autorisée et vérifier catalogues/Fiori ; si conforme, réaliser et vérifier entièrement l'exercice 1.
2. Obtenir le mapping approuvé des objets préchargés `T-S50A01`, `T-S50B01`, `T-MS101/201/301`, `T-F101`, `T-D101`, puis faire des GET ciblés des vues requises.
3. Exécuter un scan READ complet de VOV8 pour `CDCL`, puis des déterminations poste/échéance et copy control uniquement pour les clés du Book.
4. Vérifier les enregistrements PR00/K007 exacts et leurs doublons avec un contrat de lecture fonctionnel.
5. Si les actions 2–4 valident T-S50A01/T-MS101 et le pricing, soumettre puis exécuter le write contrôlé **PR00 de l'exercice 13** ; readback indépendant avant la commande test.

## Décision

**NO-GO pour un exercice SAP complet immédiat sous ABDELJ.** **GO pour les travaux ciblés ci-dessus** : session participant, résolution des mappings, scans SD exacts et préparation du PR00. Aucun blocage S4615, S4650 ou C+039 n'est introduit dans ce plan S4600.
