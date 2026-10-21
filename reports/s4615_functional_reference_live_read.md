# S4615 — recherche live READ-ONLY de références client et produit

Date : 17 octobre 2026. Environnement autorisé : A4H / mandant 600 / utilisateur ABDELJ. Méthode : quatre GET OData ciblés, sans écriture SAP, sans modification des mappings ou des spécifications. Les réponses n'ont contenu aucun candidat ; aucune lecture détaillée de vues n'était donc applicable.

## Résultat

| Famille | Requête ciblée | HTTP | Nombre SAP (`__count`) | Classification |
|---|---|---:|---:|---|
| Client | `API_BUSINESS_PARTNER/A_Customer`, clés commençant par `C615-A` ou `C615-B`, maximum 10 | 200 | 0 | `NOT_FOUND` |
| Business Partner | `API_BUSINESS_PARTNER/A_BusinessPartner`, clés commençant par `C615-A` ou `C615-B`, maximum 10 | 200 | 0 | `NOT_FOUND` |
| Produit | `API_PRODUCT_SRV/A_Product`, clés commençant par `P615-1` ou `P615-2`, maximum 10 | 200 | 0 | `NOT_FOUND` |
| Description produit | `API_PRODUCT_SRV/A_ProductDescription`, descriptions commençant par `P615-1` ou `P615-2`, maximum 10 | 200 | 0 | `NOT_FOUND` |

Les six identifiants client demandés (`C615-A00`, `C615-A01`, `C615-A02`, `C615-B00`, `C615-B01`, `C615-B02`) et les six identifiants produit demandés (`P615-100`, `P615-101`, `P615-102`, `P615-200`, `P615-201`, `P615-202`) sont tous couverts par ces préfixes. Aucun n'a été retourné dans les vues interrogées. `C615-D00` et `P615-400` / `10000287` n'ont pas été utilisés comme références.

## Meilleurs modèles et champs réutilisables

| Cible | Meilleur modèle dans le périmètre autorisé | Champs réutilisables confirmés | Préparation de la cible |
|---|---|---|---|
| `C615-A01` | **Aucun** — `NOT_FOUND` | Aucun champ de modèle client. L'existence de l'organisation `1010/10/00` ne démontre pas l'équivalence d'un client. | **Ne passe ni à READY ni à PARTIAL_TEMPLATE.** Création toujours bloquée par l'absence de source client fonctionnellement vérifiée. |
| `P615-101` | **Aucun** — `NOT_FOUND` | Aucun champ de modèle article. | **Ne passe ni à READY ni à PARTIAL_TEMPLATE.** Création toujours bloquée par l'absence de source produit fonctionnellement vérifiée. |

## Champs encore non résolus

- **Client :** numéro SAP/BP et grouping, rôles, société et compte collectif, modalités de paiement, vue `1010/10/00`, devise, condition d'expédition, usine livreuse, Incoterms, groupe d'imputation, procédure de prix client, classifications fiscales, fonctions partenaire et adresse utilisable. Aucun objet candidat n'a permis de lire ou d'hériter ces champs.
- **Produit :** numéro SAP, type de matériel, secteur industriel, unité de base et association `PC`, groupe produit, vue vente/secteur `1010/10/00`, usine, usine livreuse, groupe de catégorie de poste, classification fiscale, contrôle disponibilité, unités alternatives et présence éventuelle de vues comptables/valorisation. Aucun objet candidat n'a permis de lire ces champs.

**Portée de la conclusion :** `NOT_FOUND` concerne les clés et préfixes exacts demandés dans les quatre vues OData interrogées. Elle ne prouve pas l'absence de tous les objets portant un numéro SAP interne différent, ni celle de références d'autres familles. Aucune référence supplémentaire n'a été recherchée hors du périmètre autorisé ; aucune valeur n'a été inventée. Le flux ZA01 → LF → picking → PGI → ZF01 reste bloqué sur ses données de base groupe 01.
