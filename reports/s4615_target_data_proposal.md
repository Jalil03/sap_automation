# S4615 groupe 01 — proposition de données cibles (sans écriture SAP)

## 1. Champs prêts à proposer

| Cible | Champs | Origine |
|---|---|---|
| `C615-A01` | ID logique issu de `C615-A##` + `01` ; société `1010` ; domaine `1010/10/00` | Support/canonical et socle SAP vérifié. |
| `C615-A01` | Nom proposé `S4615 Training Customer A01` ; devise commerciale proposée `EUR` | Proposition projet conforme à la demande « European training », **pas** valeurs Book ou SAP confirmées pour ce client. |
| `C615-A01` | Rôles FLCU00/FLCU01 ; structure DO/RF/PY/RM en auto-référence vers le **futur** BP cible | Structure observée sur `17100002` ; aucune identité ni valeur US copiée. |
| `P615-101` | ID logique issu de `P615-1##` + `01` ; description `S4615 Training Product 101` ; FERT/M ; division `00` ; vente `1010/10` ; unité **de commande** `PC` | Description demandée ; support/canonical pour la vente et l'unité de commande ; FG228 pour la structure FERT/M. |

Le scénario canonique est `S4615_CH3_EX3_SALES_ORDER_FAIR` (exercice p. 41, solution p. 43). Il prévoit ZA##, client C615-A##, article P615-1## et **5 PC** ; aucun de ces `##` n'a été modifié dans le canonical. Les deux JSON sont des **propositions non exécutables**, avec provenance par champ.

## 2. Confirmation admin nécessaire

- **Client :** BP/grouping et numérotation, adresse de formation européenne réelle (pays, rue, ville, code postal, langue), compte collectif 1010, modalités de paiement, expédition/usine livreuse, Incoterms, groupe d'imputation, procédure de prix, fiscalité locale et affectations partenaires finales.
- **Produit :** numéro SAP, **BaseUnit distincte de l'unité de commande PC**, association/conversion PC, groupe produit, usine/usine livreuse, groupe de catégorie de poste, disponibilité, taxes, unités alternatives, et toutes les valeurs comptables/valorisation nécessaires au PGI. Ces champs portent `ADMIN_CONFIRMATION_REQUIRED` dans les JSON.

## 3. Blocages techniques

- La référence client `17100002` confirme la structure BP/client mais ses données `1710`, USD, Palo Alto, EXW et US/UTXJ ne sont pas réutilisables telles quelles en 1010. Le client `C615-D00` n'est pas un modèle fonctionnel pour A01.
- `FG228` possède les vues FERT/vente/usine/valorisation, mais sa BaseUnit est `289`, son alternative `/PC` n'est pas `PC`, et sa valorisation `1710` ne démontre pas qu'une nouvelle extension passera C+039. `10000217` démontre l'usage exact de PC, **sans** fournir de vue vente complète. `10000287` est exclu.
- Aucun contrat de création produit OData n'est prouvé : `A_Product` POST a déjà été rejeté par le SAP installé. La création d'adresse client OData a également échoué précédemment ; le chemin d'exécution devra être validé séparément.

## 4. Readiness finale

**C615-A01 : `BLOCKED_ADMIN_CONFIRMATION`. P615-101 : `BLOCKED_ADMIN_CONFIRMATION`.** Les fichiers définissent ce qui peut être proposé sans inventer de valeurs ; ils ne sont ni des payloads SAP, ni une autorisation de création. Aucune donnée canonique, spécification ou donnée SAP n'a été modifiée.
