# S4615 — recherche live de modèles fonctionnels

Date : 17 octobre 2026. Environnement autorisé : **A4H / client 600 / ABDELJ**. Recherche **READ-ONLY** limitée aux vues client `1010/10/00`, société `1010` et produit vente `1010/10` (au plus dix lignes par requête). Aucun POST, PATCH, PUT, DELETE, SAVE ou changement de mapping.

## Résultat des trois GET ciblés

| Vue OData | Critère | HTTP | Total SAP | ID retourné | Décision |
|---|---|---:|---:|---|---|
| `API_BUSINESS_PARTNER/A_CustomerSalesArea` | `1010/10/00` | 200 | 1 | `1000000114` | **Exclu** : correspond à `C615-D00`, pas un modèle automatique pour `C615-A01`. |
| `API_BUSINESS_PARTNER/A_CustomerCompany` | Société `1010` | 200 | 1 | `1000000114` | Même objet exclu ; aucun autre client n'a simultanément les vues recherchées. |
| `API_PRODUCT_SRV/A_ProductSalesDelivery` | Organisation `1010`, canal `10` | 200 | 1 | `10000287` | **Exclu** : correspond à `P615-400`, affecté par le périmètre C+039 et interdit comme source. |

## Meilleurs candidats

| Cible | Meilleur candidat admissible | Classification | Champs réutilisables prouvés |
|---|---|---|---|
| `C615-A01` | **Aucun** | Aucun `FUNCTIONALLY_VALID_TEMPLATE` ni `PARTIAL_TEMPLATE` dans le périmètre ; le seul résultat est exclu, donc `NOT_EQUIVALENT` comme source automatique. | Aucun champ client spécifique. Le contexte organisationnel existant `1010/10/00` ne prouve pas les données d'un nouveau client. |
| `P615-101` | **Aucun** | Aucun `FUNCTIONALLY_VALID_TEMPLATE` ni `PARTIAL_TEMPLATE` dans le périmètre ; le seul résultat est exclu et affecté par le blocage comptable, donc `NOT_EQUIVALENT`. | Aucun champ produit spécifique. La présence de `1010/10` sur l'article exclu ne prouve pas une chaîne commande → livraison → PGI → facture utilisable pour la cible. |

Les champs détaillés demandés (rôles BP, compte collectif, paiements, expédition, Incoterms, taxes, fonctions partenaire ; ainsi que type produit, unité, usine, disponibilité, unités alternatives, valorisation) **n'ont pas été interrogés davantage** : aucun ID autorisé n'a franchi le filtre organisationnel initial. Lire ces champs sur les deux objets exclus n'aurait pas établi un modèle admissible.

## Champs restant à résoudre

- **Client `C615-A01` :** identité SAP/BP et grouping, rôles, données société et compte collectif, paiements, adresse, devise, conditions d'expédition, usine livreuse, Incoterms, groupe d'imputation, procédure de prix, taxes et fonctions partenaire.
- **Produit `P615-101` :** identité SAP, type et secteur industriel, unité de base et association `PC`, groupe produit, division, vues vente et usine, usine livreuse, groupe de catégorie de poste, taxes, contrôle de disponibilité, unités alternatives et présence de vues comptables/valorisation compatibles avec PGI et facturation.

## Décision de préparation

**NON : `C615-A01` et `P615-101` ne peuvent pas encore être construits sans valeurs de données de base fournies ou sans une autre référence fonctionnelle explicitement approuvée.** Leur readiness ne passe pas à `READY`. La recherche montre l'absence de candidat *dans les vues organisationnelles exactes interrogées* ; elle ne démontre pas qu'aucun objet d'une autre organisation ne pourrait être étendu après une analyse distincte. Aucune donnée n'a été inventée et aucun objet SAP n'a été modifié.
