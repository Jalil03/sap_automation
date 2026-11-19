# Audit lecture seule — S4600 groupe 00, exercices 9 et 11

Date : 2026-10-21  
Environnement contrôlé : A4H / mandant 600 / ABDELJ  
Mode : OData GET et preuves locales uniquement ; aucun POST, PATCH, SAVE ou DELETE.

## Verdict

| Cible | Statut | Conclusion |
|---|---|---|
| `T-CUS00` (exercice 9) | **MISSING** | Les clés exactes `A_BusinessPartner('T-CUS00')` et `A_Customer('T-CUS00')` répondent 404. Les recherches exactes par ID externe, SearchTerm1 et nom `Motos et autres` renvoient zéro ligne. Le book exige un numéro externe `T-CUS00` avec regroupement BPAB : cette sortie d'exercice n'est pas encore créée. |
| `T-MS400` (exercice 11) | **MISSING** | La clé exacte `A_Product('T-MS400')` répond 404. La recherche `ProductOldID=T-MS400` et la désignation exacte `Phare standard` renvoient zéro ligne. Cette sortie d'exercice n'est pas encore créée. |
| PR00 35 EUR de `T-MS400` | **UNKNOWN / NON EXÉCUTABLE** | PR00 existe et utilise la séquence d'accès PR02. Le service de lecture des enregistrements de condition répond HTTP 500 ; l'enregistrement exact ne peut donc pas être exclu exhaustivement. Puisque le produit cible est absent, cette condition n'est de toute façon pas utilisable actuellement. |
| Doublons potentiels | **AUCUN CANDIDAT DANS LES RECHERCHES BORNÉES** | Aucun doublon exact par les identifiants et désignations ci-dessus. Cela ne prouve pas l'absence globale d'un objet créé sous un numéro interne et avec un autre alias/texte. |

## Valeurs exactes du book, résolues pour le suffixe 00

### Exercice 9 — client `T-CUS00`

- catégorie : organisation ; regroupement `BPAB` ; numéro externe `T-CUS00` ;
- nom : `Motos et autres` ; rôles `FLCU00` et `FLCU01` ;
- adresse : Rue principale, numéro `00`, 20111 Hambourg, DE, région HH, langue EN ;
- book : société `1010`, domaine `1010/10/00`, division de livraison `1010` ;
- adaptation proposée : société `FR10`, domaine `FR10/10/1W`, division de livraison `FR10` ;
- devise EUR ; condition d'expédition `50` (`## + 50`) ; Incoterm DAP, lieu Hambourg ;
- conditions de paiement `ZB00` ; groupe d'imputation libellé `Revenus intérieurs` ; schéma client `S` ;
- taxe book : DE / TTX1 / classification 1 ; compte collectif book `12100000`.

Les valeurs FI et fiscales du book ne sont pas transposables automatiquement à FR10. Comme référence observée seulement, le client FR10 `1000000112` utilise le compte collectif `41111000`, les conditions de paiement `0002`, la condition d'expédition `01`, le groupe d'imputation `C1`, le schéma de calcul client `01` et des catégories fiscales CM/FR. Ces observations ne constituent pas une autorisation de les copier vers `T-CUS00`.

### Exercice 11 — produit `T-MS400`

- article modèle book : `T-MS100` ; mapping runtime proposé : `10000282` ;
- branche `Commerce` ; type `Prod. commercialisables` ; désignation `Phare standard` ;
- book : division/usine `1010`, organisation commerciale `1010`, canal `10` ;
- adaptation proposée : usine `FR10`, organisation commerciale `FR10`, canal `10` ;
- classification fiscale 1 ; quantité minimale de commande 10 PC ; texte ADV `Article fragile !` ;
- PR00 : 35 EUR, unité de prix 1 PC, valable dès la quantité 1.

Le modèle runtime `10000282` existe avec type `ZOH`, branche `1`, secteur `1W`, vue vente FR10/10, usine et magasin FR10/0001 et valorisation FR10. Sa désignation anglaise est toutefois `Shoes Laces` et sa désignation française actuelle `CARBURANT BRUT(Essence)`. Il est donc techniquement exploitable comme référence de structure, mais il n'est pas sémantiquement équivalent au phare du book sans décision pédagogique explicite.

## Routes établies et limites

### Client

- Lecture/readback : `API_BUSINESS_PARTNER` est opérationnelle.
- Création racine : `A_BusinessPartner` POST avec capture d'un numéro SAP interne est prouvé dans le même environnement, sous approbation ciblée.
- Limite : le comportement de numéro externe littéral `T-CUS00` n'est pas prouvé ; BPAB a été observé avec numérotation interne.
- Extensions client : des contrats partiels existent pour rôles, société et domaine commercial, mais le contrat complet spécifique à `T-CUS00` avec adresse, partenaires, FI et fiscalité FR10 n'est pas validé.
- Route manuelle : le book prévoit la création via l'application Partenaire ; aucun contrat GUI complet et cible-spécifique n'est conservé pour une création automatisée sûre.

### Produit et prix

- Lecture/readback produit : `API_PRODUCT_SRV` est opérationnelle.
- Création OData produit : `A_Product` POST n'est pas supporté par le service installé.
- Création GUI : MM01 Basic Data 1/2 avec numéro SAP généré et readback OData est prouvé dans le même environnement. Le contrat complet de copie de `10000282` avec vues vente/usine, taxe, quantité minimale et texte ADV n'est pas encore prouvé pour `T-MS400`.
- Prix : VK13 est une route d'affichage installée ; PR00/PR02 est confirmé. L'API `SD_PRICING_CONDITIONRECORD_SRV` n'est pas disponible (HTTP 500). Aucun contrat de création VK11 cible-spécifique n'est autorisé dans cet audit.

## Blocages exacts avant exécution

1. **Exercice 9 — opération bloquée :** création complète de `T-CUS00`.  
   **Évidence manquante :** décision sur numéro externe littéral versus numéro SAP interne mappé ; codes FR10 approuvés pour conditions de paiement, condition d'expédition, groupe d'imputation et schéma client ; décision fiscale exacte ; compte collectif FR10 validé ; contrat adresse/partenaires et approbations `TRAINING_MASTER_DATA`, FI et taxe.  
   **Plus petite action :** valider la fiche cible FR10 champ par champ, puis préparer une empreinte de write unique et un readback indépendant.

2. **Exercice 11 — opération bloquée :** création complète de `T-MS400`.  
   **Évidence manquante :** acceptation de `10000282` comme référence malgré l'écart sémantique ; mode de numérotation ; contrat MM01 couvrant toutes les vues requises, le texte ADV et la quantité minimale ; décisions taxe/valorisation ; approbations correspondantes.  
   **Plus petite action :** approuver le modèle et les valeurs exactes, puis effectuer un préflight MM01 sans sauvegarde pour le contrat cible.

3. **PR00 — opération bloquée :** création/validation du prix 35 EUR.  
   **Évidence manquante :** produit SAP créé/mappé ; clé d'accès installée exacte pour l'article ; preuve anti-doublon sur toutes les combinaisons pertinentes ; validité ; contrat VK11 et approbation `CONDITION_RECORDS`.  
   **Plus petite action :** après création/readback du produit, exécuter un lookup VK13 sur toutes les clés PR00 applicables, puis préparer le write VK11 exact.

## Preuves

- `runtime/sap_reads/s4600_ex9_ex11_group00_2026-10-21.json`
- `data/books/S4600/S4600_EXERCISES.md`, pages 105–110 et 119–125
- `runtime/sap_reads/s4600_fr10_audit_2026-10-21.json`
- `data/provisioning/s4600/bootstrap_execution_manifest.group01.json` (routes techniques déjà établies dans le même environnement)
- `src/provisioning/s4600_t_s50a01_bp_root.py`
- `scripts/execute_s4600_product_basic.py`

