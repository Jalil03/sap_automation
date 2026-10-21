# S4615 — contexte Book de P615-1##

1. **Valeurs explicites :** l'exercice 3 (chapitre 3, p. 42 ; solution pp. 46–47) demande `P615-1##`, 5 pièces, organisation commerciale `1010`, puis livraison/prélèvement/sortie de marchandises au **point d'expédition `1010`**. Le support confirme séparément l'affectation de l'organisation commerciale `1010` à la **société `1010`** (chapitre 2 ; objet canonique `S4615_SHARED_COMPANY_CODE_1010`). Il ne donne **aucun code d'usine** pour P615-1##. Point d'expédition `1010` ≠ usine `1010`.
2. **`1710` :** jamais exigé pour P615-1## dans le texte Book ni dans l'objet canonique `S4615_CH3_EX3_SALES_ORDER_FAIR` (`items[0].plant=null`). La mention `1710` dans les faits de provisioning est une mise en garde contre une substitution technique, pas une donnée du Book.
3. **Intercompany :** non prévu dans ce flux Foire `ZA## → livraison → ZF##`. Le chapitre 9 traite distinctement d'un **client entreprise liée** et de détermination du compte de produits ; cela ne prescrit pas un flux inter-sociétés pour P615-1##.
4. **Non spécifié :** usine livreuse, aire de valorisation, vues/valeurs comptables et configuration Material Ledger. Le Book exige le résultat opérationnel de sortie de marchandises, pas un plant ou un schéma de valorisation précis.

Sources : `data/books/S4615/S4615_full_clean.md` (pp. 42, 46–47), `data/books/S4615/S4615_provisioning_facts.md`, `data/normalized/full/S4615/objects.json`.
