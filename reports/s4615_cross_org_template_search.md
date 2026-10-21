# S4615 — références techniques inter-organisations (lecture seule)

Date : 17 octobre 2026. Système autorisé : **A4H / client 600 / ABDELJ**. Recherche bornée à **2 clients** et **9 produits** ; GET OData et métadonnées seulement. Aucun SAP write, aucun changement de mapping ou de spécification.

## 1. Meilleure référence client : `17100002`

**Classification : `FUNCTIONALLY_VALID_TEMPLATE` pour la structure client, pas pour la copie directe des valeurs d'organisation vers `1010`.**

| Élément lu | Valeur live |
|---|---|
| BP / client / grouping | `17100002` / `17100002` / `BP03` |
| Rôles BP | `FLCU00`, `FLCU01`, `UDM000` |
| Société / compte collectif / paiement | `1710` / `12100000` / `0004` |
| Domaine commercial / devise | `1710/10/00` / `USD` |
| Expédition / usine livreuse | `01` / `1710` |
| Incoterms | `EXW`, lieu `Palo Alto` |
| Groupe d'imputation / procédure de prix client | `01` / `02` |
| Taxe client | `US/UTXJ/1` |
| Fonctions partenaire | `DO`, `RF`, `PY`, `RM`, toutes pointant vers `17100002` |
| Usage transactionnel | Commandes CS `1` et `148` avec sold-to `17100002`, vente `1710/10/00` (GET ciblé). Cela prouve la prise de commande, **pas** à lui seul PGI/facturation. |

Le second client examiné, `17100050`, est un **`PARTIAL_TEMPLATE`** : BP03, FLCU00/FLCU01, quatre fonctions partenaire, société `1710`, domaine `1710/10/00`, devise `EUR`, paiement `0004`, procédure `02`. Toutefois son compte collectif `12120000`, expédition `04`, groupe d'imputation `02`, Incoterms `EXW` et taxe `US/UTXJ/1` ne démontrent pas la configuration voulue pour `C615-A01`. Aucun autre client admissible n'est ressorti de la recherche bornée EUR/10/00.

**Réutilisable sans reprendre l'identité :** le schéma de rôles FLCU00/FLCU01 et les quatre fonctions partenaire self-reference constituent une référence structurelle crédible. Les valeurs `0004`, `01`, `02` observées sur `17100002` sont des **candidats à valider**, pas des valeurs Book confirmées pour A01. Ne copier ni `17100002`, ni son compte `12100000`, ni `1710`, ni USD, ni l'adresse/Incoterms US comme valeurs finales de `C615-A01`.

## 2. Meilleure référence produit : `FG228`, partielle

**Classification : `PARTIAL_TEMPLATE`.** C'est le seul produit examiné combinant FERT, vue vente, vue usine et vues comptables/valorisation. Il est historiquement utilisé dans des commandes CS, mais ne prouve pas à lui seul la chaîne complète livraison → PGI → facture.

| Élément lu | Valeur live |
|---|---|
| Type / secteur / groupe / division | `FERT` / `M` / `L004` / `00` |
| Unité de base / unités alternatives | `289` / `289`, `/PC` ; **pas d'association exacte `PC`** |
| Vente | `1710/10`, usine livreuse `1710`, groupe de catégorie `CB04`, groupe de détermination de comptes `03` |
| Usine | `1710`, contrôle disponibilité `SP` |
| Fiscalité | Catégorie `UTXJ`, classe `1` ; aucune ligne BE/MWST prouvée par ce modèle |
| Valorisation / comptabilité | Vues `A_ProductValuation` et `A_ProductValuationAccount` présentes en `1710`, classe `7920`, devise `USD` ; `A_ProductMLAccount` présente avec rôles `10=USD` et `30=USD` |

La valorisation de `FG228` est un **état historique existant** : elle ne démontre pas qu'une nouvelle extension produit en usine `1710` passerait le blocage C+039. Son unité `/PC` ne doit jamais être substituée silencieusement à `PC`.

| Autres produits examinés | Classification | Motif décisif |
|---|---|---|
| `10000217` | `PARTIAL_TEMPLATE` | FERT, unité exacte `PC`, usine et valorisation `W110` ; **aucune vue vente** ni classification fiscale trouvée, division/groupe de poste vides. Peut documenter PC/valorisation, pas le flux commercial. |
| `10000213` | `NOT_EQUIVALENT` | FERT/PC et usine `1710`, mais pas de vue vente ni valorisation. |
| `3003`, `3007` | `NOT_EQUIVALENT` | Type `ROH` (matière première), pas de vue vente. |
| `90000029`, `90000125`, `90000126`, `90000127` | `NOT_EQUIVALENT` | Type `DIEN` (service), donc non équivalent à un article FERT destiné à livraison/PGI ; `90000029` a une vue vente `W100/10` mais pas de valorisation. |

Le produit `10000287` / `P615-400` a été exclu. Aucun des neuf produits ne fournit à lui seul un modèle **`FUNCTIONALLY_VALID_TEMPLATE`** avec unité `PC`, vente, usine, valorisation et profil logistique/facturation vérifiés.

## 3. Champs encore soumis à décision métier/admin

- **Pour `C615-A01` :** numéro SAP/groupe de numérotation à créer, nom et adresse propres au groupe 01, affectation société `1010`, compte collectif valide pour ce client, modalités de paiement, devise de vente, conditions d'expédition, usine livreuse, Incoterms, groupe d'imputation, procédure de prix, taxes et fonctions partenaire finales en `1010/10/00`. Les valeurs de `1710` sont des observations, pas une autorisation de copie inter-organisation.
- **Pour `P615-101` :** identité/numérotation, description et groupe produit, choix d'unité **`PC`** sans conversion inventée depuis `289` ou `/PC`, usine et usine livreuse compatibles avec `1010/10`, groupe de catégorie et détermination comptable, fiscalité, disponibilité, vues comptables/valorisation nécessaires au PGI, et démonstration que la nouvelle extension n'atteint pas C+039. Ne pas créer une vue de valorisation `1710` en se fondant seulement sur `FG228`.

## 4. Provisionnement possible maintenant ?

**Non, pas encore pour `C615-A01` ni `P615-101` sans décisions métier/admin complémentaires.** `17100002` réduit l'incertitude sur la structure BP/client ; `FG228` réduit l'incertitude sur la structure commerciale d'un FERT. Aucun des deux ne justifie automatiquement les valeurs propres aux cibles, et aucun produit admissible n'a prouvé le profil complet demandé en unité `PC`. Les deux cibles restent **BLOCKED** ; aucun objet SAP n'a été créé ou modifié.
