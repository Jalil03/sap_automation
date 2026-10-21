# S4615 — résolution ciblée des données A01/P101 (lecture seule)

Périmètre : A4H/client 600, société `1010`, domaine commercial `1010/10/00`. GET ciblés sur `API_COMPANYCODE_SRV`, `API_BUSINESS_PARTNER` et `API_PRODUCT_SRV` (HTTP 200). Aucun autre modèle fonctionnel recherché ; `1000000114` et `10000287` servent **uniquement à prouver ce que l'environnement 1010 accepte**, pas de modèles pour A01/P101. Aucun des deux JSON proposés n'a été modifié.

## 1. Valeurs résolues ou prouvées compatibles

| Champ / règle | Résultat exact et portée |
|---|---|
| Socle | `A_CompanyCode(1010)` : pays `BE`, devise `EUR`, langue `EN`, plan comptable `CABE`, exercice `K4`, statut des champs `0001`. Le domaine `1010/10/00` est déjà vérifié dans l'état Phase 5. Ces valeurs ne constituent pas une adresse client. |
| Compte collectif candidat | `A_CustomerCompany(1000000114,1010)` : compte `400000`, groupe client `CUST`, paiement `0004`. Le compte `400000` est déjà vérifié comme compte collectif client de `1010` ; **sa réutilisation pour A01 reste un choix projet**, pas une attribution automatique. |
| Options commerciales compatibles | `A_CustomerSalesArea(1000000114,1010/10/00)` : `EUR`, expédition `01`, groupe d'imputation client `01`, procédure client `02`, Incoterms `CFR/00` ; usine livreuse vide. Ces valeurs sont techniquement présentes dans cette zone, mais leur pertinence pour A01 n'est pas établie. `02` a une détermination OVKK vérifiée pour `1010/10/00 + A` vers `A17J02`. |
| Partenaires | Quatre fonctions `DO`, `RF`, `PY`, `RM` auto-référencées sont présentes sur le client existant de `1010/10/00`. Pour A01, l'ID BP restera une liaison runtime ; aucun ID d'un autre client ne doit être copié. |
| Grouping BP observé | Le BP existant de `1010` utilise `BPAB` et un numéro SAP interne. Cela prouve un chemin existant, **pas** que `C615-A01` peut être utilisé comme clé BP externe. |
| Produit : unité `PC` | Un produit déjà présent dans `1010/10` possède `BaseUnit=PC` et `AlternativeUnit=PC` à ratio `1:1` ; `PC` est donc représentable exactement. Pour P101, le choix de `BaseUnit=PC` demeure un choix projet ; si confirmé, aucune conversion vers une autre unité de base n'est requise. Ne pas confondre avec `/PC` de FG228. |
| Options produit compatibles | Un produit présent dans `1010/10` expose groupe produit `L004`, catégorie de poste `CB04`, groupe de détermination comptable `03`, disponibilité `SP`, usine livreuse/plant `1710`, fiscalité `BE/MWST=1`. Cela prouve uniquement la compatibilité observée de ces valeurs sur **cet objet**, pas leur sélection pour P101. |
| Comptabilité du produit | `A_ProductValuation` retourne zéro ligne pour ce produit de `1010/10`. Le POST BV antérieur a échoué avec `V4/210` faute de données comptables : pour le flux commande → PGI → facturation, les vues comptables/valorisation sont requises. |

## 2. Choix projet encore requis

Pour `C615-A01` : regroupement/numérotation BP (interne `BPAB` observé, clé externe `C615-A01` non prouvée) ; groupe de comptes client (`CUST` compatible) ; adresse d'entraînement exacte, y compris pays, rue, ville, code postal et langue (`BE`/`EN` ne sont confirmés que pour la société) ; décision de réutiliser `400000` ; modalités de paiement (`0004` compatible) ; condition d'expédition (`01` compatible) ; usine livreuse (vide sur le client 1010 observé) ; Incoterms et lieu (`CFR/00` compatibles mais propres à l'autre client/scénario) ; groupe d'imputation (`01` compatible) ; procédure de prix (`02` compatible avec OVKK). Les partenaires peuvent suivre la règle d'auto-référence observée, mais leurs valeurs effectives doivent être liées à l'ID SAP d'A01 après création.

Pour `P615-101` : sélectionner l'unité de base (`PC` est valide, pas imposée par l'unité de commande du Book), le groupe produit (`L004` seulement observé), la catégorie de poste (`CB04` observée, à confronter au flux `ZA01`), le groupe de détermination comptable (`03` observé) et le contrôle de disponibilité (`SP` observé). Le numéro SAP de P101 reste déterminé par la numérotation effective, sans supposer l'acceptation de l'ID logique.

## 3. Décisions réellement administrateur / métier sensible

- `C615-A01` : classification fiscale par pays. Le GET `A_CustomerSalesAreaTax` du seul client de `1010/10/00` retourne **0 ligne** ; aucune classification client cible n'est prouvée. Décision fiscale requise, pas de copie par défaut.
- `P615-101` : classification fiscale `BE/MWST` (la valeur `1` est observée sur un autre produit, sans règle générale), classe de valorisation, contrôle et détermination du prix, prix standard et devise comptable. Ces valeurs pilotent la fiscalité/comptabilité et ne découlent pas du Book ni de la seule zone commerciale.

## 4. Blocages techniques distincts

- L'affectation `1010/10 → 1710` est connue, mais `1710` dépend d'une société/valorisation différente. Il faut choisir et prouver un couple plant/usine livreuse/aire de valorisation convenant à P101 et au flux S4615 ; **ne pas reprendre `1710` par défaut**. L'usine livreuse du client 1010 existant est vide.
- Une extension comptable d'un nouveau produit à `1710` reste exposée à `C+039` (Material Ledger). Ce problème est distinct des choix de données cibles ; aucune correction ML n'a été tentée. Sans vue comptable effective, le précédent `V4/210` empêche le flux.
- Le chemin de création produit OData n'est pas prouvé (`A_Product` POST rejeté par l'installation) ; la création future exige un contrat d'exécution validé séparément. Aucun POST n'a été effectué ici.

## 5. Décompte et readiness

Décompte des **29 groupes de champs initialement marqués `ADMIN_CONFIRMATION_REQUIRED` dans les deux propositions**, non des valeurs du socle déjà prêtes :

| Cible | Règle résolue/conditionnelle | Choix projet | Décision admin/métier sensible | Blocage technique | Total |
|---|---:|---:|---:|---:|---:|
| C615-A01 | 1 (structure des partenaires) | 11 | 1 (fiscalité) | 0 | 13 |
| P615-101 | 2 (conversion et unité alternative **si** base `PC` choisie) | 5 | 5 (fiscalité et valorisation/prix) | 4 (plant, livraison, aire, vues comptables/ML) | 16 |
| **Total** | **3** | **16** | **6** | **4** | **29** |

**Readiness :** C615-A01 et P615-101 restent non exécutables. Les valeurs observées sur des objets existants sont des options prouvées compatibles, jamais des valeurs cibles inventées ou assignées implicitement.
