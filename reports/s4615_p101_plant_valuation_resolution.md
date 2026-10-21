# S4615 P615-101 — usine et valorisation (A4H/600, lecture seule)

## Conclusion

| Élément | Résultat |
|---|---|
| Usine recommandée | **Aucune usine sûre prouvée** pour un nouveau FERT destiné à `1010/10`. `1710` est la seule usine **déjà prouvée affectée** à `1010/10`, mais elle n'est pas recommandable pour une nouvelle extension comptable tant que C+039 subsiste. L'exhaustivité des affectations `1010/10 → usine` n'est pas prouvée par l'API. |
| Usine livreuse | **À déterminer** ; `1710` est observée sur un produit de `1010/10`, sans preuve qu'elle soit sûre pour P615-101. |
| Société cible / société de l'usine disponible | `1010` = `BE`/`EUR`/plan `CABE` ; usine `1710` = société `1710`, `US`/`USD`/plan `YCOA`. |
| Aire de valorisation | **À déterminer** ; `1710` est la seule aire associée à l'usine candidate vérifiée, pas une aire EUR de société 1010. Aucune ligne de valorisation d'aire `1010` n'est retournée. |
| Dry-run readiness | **BLOCKED** pour une proposition d'usine/valorisation exécutable et pour le flux complet vente → livraison → PGI → facture. Aucune valeur plant/valuation ne doit être inscrite par défaut dans P615-101. |

## Preuves ciblées

- GET `API_PLANT_SRV/A_Plant` : usine `1710` rattachée à la société `1710` ; aucune usine retournée pour `Plant=1010` ou `CompanyCode=1010`. GET `API_COMPANYCODE_SRV/A_CompanyCode` : `1010=BE/EUR/CABE`, `1710=US/USD/YCOA`.
- L'affectation `1010/10 → 1710` est déjà vérifiée dans `docs/phase5/CURRENT_STATE.md`. GET `API_PRODUCT_SRV/A_ProductSalesDelivery` limité à `1010/10` : seul produit retourné `10000287`, `SupplyingPlant=1710`. Cela démontre une compatibilité commerciale observée, **pas** la santé de la valorisation ni l'exhaustivité des affectations d'usines.
- GET `A_ProductValuation` pour l'aire `1010` : **0 ligne retournée** ; pour l'aire `1710` avec `BaseUnit=PC` : deux lignes (`90000125`, `90000126`), toutes deux `DIEN`/secteur `C`, classe `3200`, prix standard `0.00 USD` — **pas des FERT sains**. Aucun exemple FERT valorisé en `PC` n'a été établi par cette recherche ciblée.
- `FG228` est un FERT existant avec vente `1710/10`, usine `1710`, valorisation `1710`, classe `7920`, prix standard `27.19 USD`, mais `BaseUnit=289`. C'est une valorisation historique, non une preuve qu'une nouvelle extension `PC` en `1710` sera acceptée.
- Les lignes `A_ProductMLAccount` de produits historiques en `1710` montrent les rôles `10/30` en `USD`. Elles ne prouvent pas la santé actuelle du Material Ledger. La tentative documentée d'ajout des vues comptables pour `10000287` en `1710` a échoué sur **C+039** avant sauvegarde ; le POST de commande précédent avait échoué sur **V4/210** faute de données comptables. La capacité de PGI/facturation de P615-101 reste non prouvée.

## Décisions FI/MM restantes

1. Choisir une usine réellement affectée à `1010/10` et une aire de valorisation cohérente avec l'objectif EUR/société 1010 ; aucune usine 1010 n'est actuellement attestée par `A_Plant`.
2. Si `1710` devait être retenue malgré la préférence EUR/1010, faire valider explicitement le flux inter-sociétés, la devise USD et la résolution du C+039 **avant** toute extension comptable. Ne pas extrapoler de FG228.
3. Pour l'aire approuvée, valider classe de valorisation, contrôle/détermination du prix, prix standard et devise, ainsi que les vues comptables/ML nécessaires au PGI ; ces valeurs ne sont pas déductibles du seul Book ou des exemples consultés.

Aucun POST, aucune modification SAP, aucune modification des jeux proposés ou du Material Ledger.
