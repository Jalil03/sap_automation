# S4600 exercice 30 — recherche du produit à fabriquer

Date : 23/10/2026. Identité vérifiée : **A4H / 600 / ABDELJ**.

## Résultat

**Exercice non exécutable à ce stade : mapping de T-F100 inconnu.** Aucun objet SAP n'a été créé ou modifié.

Les recherches existantes du 23/10 sur l'identifiant exact `T-F100` et `ProductOldID = T-F100` n'avaient donné aucune correspondance. Le manifeste et les données canoniques ne donnent pas de numéro SAP vérifié ; la désignation et l'unité du produit à fabriquer ne sont pas spécifiées dans l'objet canonique. Ces valeurs ne doivent pas être inventées.

## Recherche complémentaire live

| Lecture OData | Résultat |
|---|---|
| Produits dont l'identifiant ou l'ancien identifiant commence par `T-F1` | HTTP200, zéro correspondance, pas de page suivante. |
| Planification produit en FR10 avec stratégie `20` ou type d'approvisionnement `E` | HTTP200, zéro correspondance, pas de page suivante. |

Ce résultat ne signifie pas qu'aucune fabrication n'est possible dans tout le système. Il porte uniquement sur ces filtres : il n'exclut pas un produit sous un autre identifiant, une autre stratégie ou un autre mode d'approvisionnement. Il ne prouve pas non plus l'absence universelle de nomenclatures ou de gammes. Aucune équivalence avec les articles commerciaux existants n'a été déduite.

## Contrôles qui restent impossibles sans produit identifié

- stratégie de planification applicable et comportement fabrication sur commande ;
- nomenclature et composants ;
- gamme, postes de travail et données de production ;
- version de fabrication si nécessaire au processus installé ;
- vues commerciales FR10/10 et données de valorisation ;
- conversion d'ordre planifié, lancement, entrée de marchandises et livraison du stock individuel.

La référence `8-900` existe déjà pour la commande **155**, issue du scénario avant-vente28. Sa présence ne constitue pas une exécution du30. Aucun document n'a été modifié, réutilisé ou renommé pour contourner cette collision de référence.

## Plus petite suite requise

Obtenir auprès de l'administrateur/formateur **le numéro SAP du produit correspondant à T-F100**, préparé pour la fabrication sur commande en **FR10**. Il sera ensuite possible de lire et vérifier sa stratégie20, sa nomenclature et sa gamme.

Si aucun produit n'est prévu, la préparation d'un jeu de données PP complet représente un périmètre distinct à définir et autoriser. Le seul passage d'un article commercial en stratégie20 ne valide pas ce scénario. Aucun lancement MRP ni changement de stratégie ne doit être entrepris sur la base de la présente vérification.

## Preuves et sécurité

- `runtime/sap_reads/s4600_ex30_mto_candidates_2026-10-23.json` : identité, requêtes, résultats et absence de pagination.
- `runtime/sap_reads/s4600_ex1_23_30_34_preflight_2026-10-23.json` : recherches exactes et commande155.
- `data/provisioning/s4600/master_data_manifest.group01.json` : absence de mapping antérieure ; ce manifeste historique groupe01 n'est pas utilisé comme mapping du groupe00.
- `data/normalized/full/S4600/objects.json` : objet canonique `S4600_CH8_EX30_MATERIAL_T-F1-GROUP`, inchangé.
- `scripts/audit_s4600_ex30_mto_candidates_readonly.py` : appels GET uniquement, lecture bornée, aucune affectation automatique de candidat.
- `tests/test_s4600_ex30_readonly_discovery.py` : contrôles hors ligne de la route GET, de la borne de lecture, de la pagination et du classement UNKNOWN en cas d'erreur.

**Zéro modification de stratégie, nomenclature, gamme, job MRP, ordre de fabrication, stock, comptabilité ou Material Ledger.**
