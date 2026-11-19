# S4600 groupe 00 — audit READ-only des exercices 28 et 31

Date : 2026-10-21  
Environnement observé : A4H / mandant 600 / ABDELJ  
Mode : OData GET et réutilisation de preuves GUI d'affichage ; aucun POST, PATCH, SAVE ou document créé.

## Verdict

| Exercice | Élément | Classement | Preuve |
|---|---|---|---|
| 28 | Type français `DO` | EXISTS | Le type interne `AF` est retourné par `API_SALESORDERTYPE_SRV`; la lecture complète de `V_TAUUM` établit `FR: AF → DO`. |
| 28 | Type français `OFF.` | EXISTS | Le type interne `AG` est retourné par l'API; `V_TAUUM` établit `FR: AG → OFF.`. Le libellé Book `OF` doit donc être adapté à `OFF.` dans cette session française. |
| 28 | Type français `CS` | EXISTS | Le type interne `TA` est retourné par l'API; `V_TAUUM` établit `FR: TA → CS`. |
| 28 | API demande | EXISTS | `API_SALES_INQUIRY_SRV/$metadata` répond HTTP 200 et expose notamment `A_SalesInquiry` et ses postes/prix. |
| 28 | API offre | EXISTS | `API_SALES_QUOTATION_SRV/$metadata` répond HTTP 200 et expose notamment `A_SalesQuotation` et les flux précédents/suivants. |
| 28 | Flux de copie `DO → OFF. → CS` | UNKNOWN | Aucun document demande/offre FR10/10/1W pour `1000000112` n'est retourné. L'absence d'historique ne prouve pas l'absence du paramétrage de copie. |
| 31 | Produit `90000133` | EXISTS | Produit `DIEN`, unité `H`, secteur `1W`, groupe de catégories `LEIS`; vue vente FR10/10 présente. |
| 31 | Détermination de poste `TAD` | UNKNOWN | Le Book exige `TAD`, mais aucun poste de commande existant avec `90000133` n'est retourné et la combinaison VOV4 exacte n'a pas été relue dans ce lot. |
| 31 | PR00 de `90000133` | UNKNOWN | Aucun poste historique ne permet une lecture de `to_PricingElement`. La recherche VK13 client/article déjà faite ne retourne aucune condition, mais elle ne couvre pas toutes les combinaisons de la séquence PR02. |
| 31 | Facturation liée à la commande de service | UNKNOWN | Aucun document historique `90000133` ne permet de valider le flux commande → facture ni sa date de facturation. |

## Constats complémentaires

- Les services directs standard de demande et d'offre sont lisibles. Les alias `ZAPI_SALES_INQUIRY_SRV_0001` et `ZAPI_SALES_QUOTATION_SRV_0001` répondent HTTP 403 « aucun service trouvé ». Cela n'empêche pas les lectures via les services directs mais interdit de revendiquer les alias Z comme installés.
- Les filtres exacts renvoient zéro demande et zéro offre pour `FR10 / 10 / 1W`, client `1000000112`, au moment de l'audit.
- Le filtre exact sur les postes de commande avec article `90000133` renvoie zéro ligne. Ce résultat signifie « aucun poste observable par cette API », pas « configuration absente ».
- Le Book canonique reste inchangé. L'adaptation d'exécution groupe 00 est `DO`, `OFF.`, puis `CS`, avec client `1000000112`, article `10000283` pour l'exercice 28 et service `90000133` pour l'exercice 31.

## Blocages et plus petites actions suivantes

1. **Opération bloquée :** déclarer le flux de copie de l'exercice 28 exécutable.  
   **Preuve manquante :** lecture exacte du paramétrage `AF → AG` puis `AG → TA`, ou essai transactionnel contrôlé avec lecture des documents liés.  
   **Plus petite action :** effectuer une lecture GUI ciblée du contrôle de copie sans sauvegarde; si cette lecture reste non concluante, autoriser un pilote transactionnel distinct.

2. **Opération bloquée :** déclarer que `CS + LEIS` détermine `TAD`.  
   **Preuve manquante :** ligne exacte de détermination de catégorie de poste ou simulation non sauvegardée avec `90000133`.  
   **Plus petite action :** relire la combinaison VOV4 exacte en mode affichage.

3. **Opération bloquée :** exécuter la commande de service de l'exercice 31.  
   **Preuve manquante :** enregistrement PR00 effectif pour `90000133` sur la combinaison réellement utilisée, avec montant, devise, unité et validité.  
   **Plus petite action :** terminer VK13 sur toutes les combinaisons installées de PR02; si le prix est absent, obtenir les valeurs Book/approuvées avant toute création VK11.

4. **Opération bloquée :** facturer le service depuis la commande.  
   **Preuve manquante :** contrôle de copie commande → facture et comportement de facturation liée à la commande pour `TAD`.  
   **Plus petite action :** lecture du paramétrage exact puis test sur le document pilote, avec autorisation d'écriture séparée.

## Preuves techniques

- `runtime/sap_reads/s4600_ex28_ex31_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_v_tauum_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_pr00_vk13_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_fr10_audit_2026-10-21.json`

