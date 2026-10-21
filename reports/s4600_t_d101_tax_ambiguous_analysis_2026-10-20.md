# S4600 — analyse READ-ONLY de la tentative fiscale T-D101

Date : 2026-10-20. Environnement : A4H / client 600 / ABDELJ.

## Verdict

La tentative `A_ProductSalesTax` pour `T-D101 / 90000132 / BE / MWST / 1` n'a produit aucune ligne fiscale visible. Le checkpoint reste `AMBIGUOUS` et interdit un retry automatique.

## Preuves

- Le produit racine existe : `DIEN / W / H / division 00 / ItemCategoryGroup LEIS`.
- `A_ProductSales` existe pour `90000132`.
- `A_ProductSalesDelivery` retourne zéro ligne pour `90000132`.
- Trois lectures fiscales séparées, dont une lecture différée et une clé exacte, retournent zéro ligne ; la clé exacte retourne HTTP 404.
- La métadonnée installée expose `A_ProductSalesTax` comme créable. Les quatre champs sont obligatoires et créables : `Product`, `Country`, `TaxCategory`, `TaxClassification`.
- `P615-400 / 10000287` prouve que `BE/MWST/1` est installé : sa ligne fiscale et sa vue commerciale `1010/10` sont lisibles.
- La documentation SAP officielle décrit `A_ProductSalesTax` comme compatible Create/Read/Update/Delete : https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/bc6b9325fedd4344a84412b2195064fa/74aa2b58a333a107e10000000a441470.html

### Vérification API exhaustive du 2026-10-20

- Liste fiscale filtrée par produit : HTTP 200, `__count=0`.
- Liste filtrée par produit/pays/catégorie/classe : HTTP 200, `__count=0`.
- Clé exacte `90000132/BE/MWST/1` : HTTP 404, transaction Gateway de cette lecture `8DC6789C69B40070E006AC6D6BEA32DC`.
- Navigation `A_Product('90000132')/to_ProductSalesTax` : HTTP 200, `__count=0`.
- Compteur direct `A_ProductSalesTax/$count` filtré : HTTP 200, valeur `0`.
- Compteur de navigation `to_ProductSalesTax/$count` : HTTP 200, valeur `0`.
- Expansion de la racine : HTTP 200, `to_ProductSalesTax.results=[]`.
- `A_ProductSales` : HTTP 200, une ligne ; classification fiscale générale vide.
- `A_ProductSalesDelivery` : HTTP 200, `__count=0`.
- Contrôle positif `10000287/BE/MWST/1` : HTTP 200, `__count=1`.

Ces chemins indépendants établissent que la taxe n'est pas persistée. Ils ne permettent pas de retrouver le statut, les en-têtes ou le corps de l'ancien POST, qui n'ont pas été conservés.

## Interprétation

Les preuves excluent une absence générale de l'entité et une incompatibilité évidente de `BE/MWST/1`. Elles ne permettent pas d'attribuer la non-persistance à une cause unique. Restent possibles : comportement spécifique à la version/backend A4H, prérequis commercial non signalé, rollback backend non exposé, ou réponse HTTP positive ne représentant pas une création persistée.

La première version de l'exécuteur n'a pas conservé le statut HTTP exact, le corps borné, l'en-tête `Location`, l'en-tête `SAP-Message` ni un identifiant de corrélation. Il est donc impossible de reconstituer cette information après coup.

## Action minimale

La recherche manuelle `/IWFND/ERROR_LOG` sur toute la journée du 2026-10-20 a été effectuée par l'utilisateur. Elle ne contient aucune entrée `API_PRODUCT_SRV` autour de la tentative. Deux entrées seulement sont visibles ; elles concernent `ZSD_PRICING_CONDITIONRECORD_SRV_0001` et confirment séparément l'absence de service/alias pour le service de conditions tarifaires. Le journal expose A4H/600, release Gateway 7.58.

Le journal d'erreurs ne permet donc pas de récupérer la réponse du POST fiscal, probablement parce que la requête n'a pas été classée comme erreur Gateway. L'action minimale devient une analyse Gateway/Basis ciblée hors de ce journal :

- UTC : autour de `2026-10-20 13:53:17` ;
- utilisateur : `ABDELJ` ;
- service : `API_PRODUCT_SRV` ;
- entité : `A_ProductSalesTax` ;
- produit : `90000132`.

Retour attendu : confirmer le statut/corps/en-têtes backend de l'appel s'ils sont encore disponibles, ou préparer une trace contrôlée pour une éventuelle nouvelle tentative séparément approuvée. Aucun nouveau POST ne doit être envoyé avant cette décision et une nouvelle approbation de reprise.

`T-MS101` et `T-MS201` n'ont pas été tentés et restent inchangés.

La lecture directe de table et l'affichage SAP GUI n'ont pas été automatisés : le bridge SE16N du projet est volontairement limité à des tables de Customizing S4615 et ne permet pas `MLAN`. Ce garde-fou n'a pas été élargi.
