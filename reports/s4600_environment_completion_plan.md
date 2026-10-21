# S4600 — clôture de préparation de l'environnement

**19 octobre 2026 — A4H/600 — utilisateur technique ABDELJ — participant attendu S4600-01 — groupe 01.** S4600 est le seul Book actif. Aucun write SAP, mouvement de stock, Customizing, FI/MM/ML ou changement S4615/S4650 n'a été effectué.

## 1. Composants confirmés

| Composant | État | Preuve et limite |
|---|---|---|
| Identité technique SAP GUI | `VERIFIED_PRESENT` | Runner live : A4H/600/ABDELJ, mode READ |
| Fiori Launchpad | `USER_OBSERVED_REACHABLE` | Accès navigateur signalé par l'utilisateur ; identité authentifiée et catalogues non lisibles depuis cette session d'automatisation |
| Groupe d'entraînement | `01` | Décision du projet ; résolution runtime `##→01` |
| Société / organisation commerciale / domaine commercial | `VERIFIED_PRESENT` | 1010, 1010 et 1010/10/00 selon les readbacks Phase 5 existants ; cela ne prouve pas les données S4600 |
| Types de condition | `VERIFIED_PRESENT` | PR00 avec accès PR02 ; K007 avec accès K307 |
| APIs de lecture | `VERIFIED_PRESENT` | Business Partner, Product, Plant, Warehouse, Sales Order, Outbound Delivery et Billing selon audits existants |
| Questions conceptuelles | `COMPLETED_AND_VERIFIED` | Exercices 2, 15, 24 et 29 |
| Manifeste S4600 | `STRUCTURE_READY_DATA_NOT_EXECUTION_READY` | Version 1.1 : 9 objets, classification préchargé/sortie, validations de numérotation, anti-doublon et readback |

Éléments explicitement absents : usines 1010/1020 dans `API_PLANT_SRV`, point d'expédition Z001 dans le scan TVST complet, warehouse 1010 dans l'API EWM consultée. Aucun substitut n'est proposé.

## 2. Fiori : vérification manuelle minimale

Le contrôle Chrome n'est pas connecté à cette session. Les points suivants doivent être relevés dans la session Fiori existante, sans modifier rôle, catalogue ou configuration partagée :

1. Ouvrir le menu utilisateur et relever l'identité affichée. Résultat requis : **`S4600-01`**. Si un autre utilisateur est affiché, ne pas exécuter les personnalisations de l'exercice 1.
2. Rechercher exactement les applications/tuiles suivantes et noter `AVAILABLE`, `MISSING` ou `LOAD_ERROR` :
   - Création de commandes clients VA01 ;
   - Création de livraisons sortantes – À partir des commandes client ;
   - Gestion des documents de facturation ;
   - Modification de commandes clients ;
   - Gestion des propositions des postes de vente ;
   - Gestion du partenaire ;
   - Traitement des commandes clients (Analyse et résolution) ;
   - Entrée de commandes clients – Analyse flexible.
3. Pour la tuile en erreur, conserver : titre exact, texte intégral de l'erreur, heure, URL après `#` ou intent s'il est visible, et informations techniques/app ID si le Launchpad les offre. Tester la recherche de la même application ; ne pas vider les caches, changer les rôles ou recréer la tuile.
4. Transmettre ces éléments à Basis/Fiori si l'application est absente ou échoue également depuis la recherche. Une erreur limitée à une tuile personnalisée relève de la page utilisateur ; une application absente/non autorisée relève du catalogue/rôle.

### Exercice 1

- Prérequis vérifiés : utilisateur attendu et valeurs Book connues.
- Inconnus : identité effective, trois catalogues/applications, tuile en erreur.
- Write prévu, uniquement dans `S4600-01` : groupe personnel **Mes applications favorites**, ajout des trois applications, valeurs par défaut société 1010, warehouse 1010, organisation 1010, canal 10, secteur 00.
- Gate : session participant exacte et applications disponibles ; aucun write sous ABDELJ.
- Vérification : déconnexion/reconnexion du participant, groupe/tuiles présents, valeurs par défaut relues, recherche « Modification de commandes clients » réussie.

## 3. SD et pricing encore à fermer

| Contrôle | État final de préparation |
|---|---|
| VOV8/CDCL | `NOT_CHECKED` : 43 lignes visibles sur 224 entrées SAP ; aucune absence inférée |
| Poste/échéance | `TAD` est Book-confirmed pour le service ; déterminations live non prouvées, aucun code d'échéance inventé |
| Copy control | Clés DO→OF→CDCL, CDCL→livraison→facture, commande service→facture, facture→DNC→avoir/annulation à lire ; aucun contrat objet API prouvé |
| Pricing determination | Types PR00/K007 présents ; procédure effective du client S4600 inconnue |
| Condition records | Contrat `SD_PRICING_CONDITIONRECORD_SRV` indisponible lors du dernier metadata HTTP 500 ; enregistrements/chevauchements non vérifiés |
| Billing/cancellation | APIs de documents lisibles ; paramètres de type/copie/annulation non prouvés |

Ces lacunes restent **team-owned** tant qu'une lecture ciblée ou une preuve administrateur peut les fermer. Elles ne sont pas reclassées comme objets SAP manquants.

## 4. Revue du manifeste et données de base

### Données supposées préchargées par le Book

`T-S50A01`, `T-S50B01`, `T-MS101`, `T-MS201`, `T-MS301`, `T-F101`, `T-D101`. Aucune correspondance SAP déterministe n'est trouvée. Une clé littérale absente n'autorise pas leur recréation : obtenir un mapping approuvé ou un scope bootstrap séparé.

### Sorties à créer dans leur exercice

`T-CUS01` (exercice 9) et `T-MS401` (exercice 11). Ils ne doivent pas être demandés à l'administrateur comme prérequis préchargés.

La version 1.1 du [manifeste](../data/provisioning/s4600/master_data_manifest.group01.json) contient les Book values, dépendances, décisions manquantes, règles de numérotation, GET anti-doublon et readbacks par type. Aucun champ FI, taxe, usine, valorisation ou unité de base n'est inventé.

## 5. Branches préparées

### Exercice 13 — PR00

- Confirmé : PR00 présent ; clé Book client/article T-S50A01/T-MS101, 1010/10 ; échelles 1→53, 10→51, 20→49 EUR/PC.
- Inconnus : IDs SAP des deux masters, combinaison d'accès réellement installée, condition existante/chevauchante et contrat de lecture/écriture opérationnel.
- Write prévu : **un** enregistrement PR00 pour la clé installée et l'intervalle Book, avec ses trois échelles ; aucune autre condition.
- Gate : approbation `CONDITION_RECORDS`, identités vérifiées, GET anti-doublon et payload/GUI contract exact.
- Vérification : GET/relecture indépendante de l'ID, clé, validité, monnaie, unité et trois échelles ; puis commande test du Book.

### Exercice 14 — K007

- Confirmé : K007 présent ; client T-S50A01 ; échelles de valeur 100→−1 %, 500→−2 %, 1000→−3 %.
- Inconnus : ID client, combinaison d'accès, devise/validité exactes selon l'écran Book et éventuel doublon.
- Write prévu : un enregistrement K007 avec les trois échelles, sans toucher au pricing global.
- Gate/readback : mêmes contrôles que PR00, séparés par une empreinte de valeurs propre.

### Exercice 31 — vente de service sans PGI

- Confirmé par le Book : T-D101 préchargé, type DIEN, groupe de catégories LEIS, unité de commande H ; poste `TAD` déterminé ; facturation liée à la commande, sans chaîne physique/PGI.
- Inconnus : mapping SAP de T-D101/T-S50A01, base unit/description, prix/taxe, CDCL→TAD, copy control commande→facture et comportement billing installé. Le Book demande une vue usine 1010 ; elle ne sera pas omise sans décision explicite d'équivalence.
- Writes prévus : commande CDCL de 3 heures puis facture liée à la commande. Aucun delivery, PGI ou stock. Création du service seulement sous scope bootstrap distinct si la donnée préchargée est définitivement indisponible.
- Gate : master mappings, pricing/tax non sensibles validés ou approuvés, transaction write scope et copy control prouvé.
- Vérification : GET commande/poste TAD et flux commande→facture, sans document de livraison/PGI.

## 6. Propriété des tâches restantes

### Notre équipe

- Obtenir l'évidence Fiori manuelle et diagnostiquer la tuile.
- Fermer les lectures CDCL, déterminations et copy control avec un contrat strictement READ.
- Résoudre les mappings S4600, valider le manifeste et préparer les fingerprints exacts des writes.

### Administrateurs

- Usines 1010/1020 et affectations ; Z001 et détermination ; warehouse/EWM 1010.
- Valorisation FI/MM, comptes, stock initial et opérations sensibles.
- Autorisations/catalogues du participant et correction de l'application Fiori si le rôle ou le contenu partagé est en cause.

## 7. GO / NO-GO

- **GO conditionnel — exercice 1** : premier write candidat, mais seulement après preuve que la session est `S4600-01` et que les applications existent. Il s'agit uniquement de personnalisation utilisateur.
- **NO-GO actuel — PR00/K007 et documents transactionnels** : mappings, accès/doublons et contrats SD ne sont pas encore complètement prouvés.
- **NO-GO — logistique/stock** jusqu'aux décisions administrateur.

Premier write de données de formation après la personnalisation : **PR00 exercice 13**, sous les gates exacts décrits ci-dessus.
