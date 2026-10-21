# S4600 + S4615 — avancement sûr, 19 octobre 2026

Périmètre : A4H/600/ABDELJ, lectures SAP uniquement. Aucun POST, Save, mouvement de stock, transport ou changement FI/MM/ML. Sources : Markdown des Books, canonique immuable, checkpoints et audits existants. Aucun PDF relu. Les résultats GET ci-dessous sont ceux de cette session ; les preuves GUI historiques sont explicitement distinguées.

## Résultats des exercices

| Book | Terminés et vérifiés | Partiels | Bloqués par dépendance | Non vérifiés | Exécutables immédiatement en SAP |
|---|---:|---:|---:|---:|---:|
| S4600 | 4/36 : 2, 15, 24, 29 | 0 | 22 | 10 | 0 démontré |
| S4615 | 0/13 | 5 : 2, 3, 6, 9, 13 | 8 | 0 | 0 démontré |

Les [24 réponses conceptuelles S4600](s4600_conceptual_exercises_evidence.md) reprennent les questions exactes et sont comparées aux solutions pages 42–43, 146, 234 et 278. Elles satisfont ces quatre exercices écrits sans SAP. Les documents transactionnels produits par les autres exercices sont des dépendances de séquence, pas des configurations manquantes.

## Lectures ciblées et limites

Requêtes GET sous `/sap/opu/odata/sap/`, client 600 ; seules les propriétés utiles sont rapportées, aucun secret. `[]` signifie aucune ligne répondant au filtre, jamais absence d'un type de document ou d'un calendrier.

| Sujet | Preuve réutilisée ou lecture du 19/10 | Conclusion exacte |
|---|---|---|
| S4600 CDCL | Audit existant : commandes filtrées CDCL, HTTP 200/0 ; VOV8 seulement 43 lignes visibles sur 266 | NOT_CHECKED pour la configuration CDCL ; aucune nouvelle recherche exhaustive, aucune absence inférée |
| Catégories de postes/échéances | Book et manifestes : notamment DIEN/LEIS pour le service ; aucun contrat de lecture installé permettant de vérifier toutes les déterminations cibles | NOT_CHECKED ; présence d'une valeur Book ≠ entrée de détermination installée |
| Copy control S4600 | Preuve ZF01/LF/TAN spécifique S4615, non transposable aux clés S4600 | NOT_CHECKED pour les clés S4600 |
| Prix S4600 | Audit précédent : PR00 et K007 présents ; service `SD_PRICING_CONDITIONRECORD_SRV/$metadata` HTTP 500 | Types présents, enregistrements client/article et validité non vérifiés ; appel échoué non répété |
| Clé comptable | `API_SLSPRICINGPROCEDURE_SRV/A_SlsPricingProcedureItem`, filtre `ConditionType eq 'PR00'`, sélection procédure/type/`AccountKeyForGLAccount`, top 10 : HTTP 200 ; ERL notamment dans ADAA01, ADBOS1, BVRBTI, CHBACK, GRVAA1, GT7000, ICAA01, J1NA01 | ERL existe dans ces schémas ; ne prouve ni le schéma déterminé pour le scénario ni le compte général cible |
| Facturation S4600 | Métadonnées facturation déjà accessibles ; pas de nouvelle preuve des paramètres de types/copy-control S4600 | NOT_CHECKED, ne pas confondre API disponible et configuration validée |
| Calendrier S4615 | Métadonnées BP : `A_CustomerSalesArea` expose `InvoiceDate` et `InvoiceListSchedule`. GET filtré 1010/10/00 + `InvoiceDate eq 'AM'`, top 3 : HTTP 200/0 | Aucune affectation AM dans ce résultat ; définition/calendrier AM non vérifiés. Book ex7 exige AM pour B01 |
| Pro forma | `API_BILLING_DOCUMENT_SRV/A_BillingDocument`, filtre `BillingDocumentType eq 'F5'`, puis F8, top 1 : chacun HTTP 200/0 | Aucun document observé ; pas de conclusion sur existence/configuration F5/F8. Book ex5 demande F5 sur commande |
| Groupement | Même GET, filtre type F1, top 1 : HTTP 200 ; facture 90000054, organisation CI10, société XCI1, AccountingDocument vide, PostingStatus A, TransferStatus B | F1 observé hors contexte cible ; aucune preuve du regroupement C615-C01. Ex8 attend simulation de deux livraisons → une facture/quatre postes ; ex9 split |
| Facturation périodique | `API_SLSPRICINGPROCEDURE_SRV/A_SlsPricingConditionType`, filtre PPSV : HTTP 200 ; usage A, application V, accès PPPV, calcul M | PPSV et son calcul M confirmés ; montant, validité et données du contrat groupe01 restent à établir |
| S4615 copy control et blocage comptable | Checkpoints existants et [progression](../books/S4615/S4615_PROGRESS.md) : ZF01←LF/TAN vérifié ; RFBFK=true après réouverture | Préparation ex6/9/13 acquise, pas leur validation transactionnelle |
| Z001 | Lecture GUI historique complète TVST 20/20 : [réponse](../runtime/sap_gui_responses/080efce4-7892-489d-adde-e3639695707f.json) | CONFIRMED_MISSING ; pas de nouvelle lecture |

Les contrôles GUI restants ne sont pas exposés par les contrats ciblés actuels (CDCL, catégories/échéances, calendrier et détails F1/F5/F8). La compétence Windows `computer-use` exige `node_repl` avec `@oai/sky`, outil absent de cette session. Aucun contournement COM ni élargissement de permissions n'a été effectué. Ces lacunes sont des capacités de lecture de notre équipe, pas automatiquement des incidents administrateur.

## Préparation locale, sans création

- [Manifeste S4600](../data/provisioning/s4600/master_data_manifest.group01.json) : 9 objets, trois clients et six articles. T-CUS01 et T-MS401 sont des résultats d'exercices, pas des objets à recréer avant ces exercices.
- [Manifeste S4615](../data/provisioning/s4615/additional_master_data_manifest.group01.json) : 7 objets, B01/C01/E01/F01 et P615-201/501/601.
- Templates `##` préservés, groupe 01 résolu localement, sources/dépendances/approbations explicites. Aucun nouvel identifiant SAP inventé, aucune nouvelle correspondance persistée.
- Choix fiscaux, comptes, unité de base, usine et valorisation non prouvés restent indéterminés. L'unité de commande PC n'impose pas une unité de base PC.

## Suite ciblée

1. Obtenir les décisions et accès du [paquet administrateur](s4600_s4615_admin_request.md), sans réparer automatiquement C+039.
2. Avec la session participant autorisée, terminer les préférences/Favoris S4615 ex2 et les tâches Fiori S4600 concernées ; jamais dans ABDELJ à sa place.
3. Fermer les lectures SD restantes avec un contrat ciblé ou une preuve administrateur ; confirmer les mappings T-* avant toute création.
4. Après décisions et approbations exactes, préparer les clients/articles des manifestes ; préserver les exercices de création T-CUS01/T-MS401.
5. Exécuter les branches pro forma/service/périodique lorsqu'elles disposent de leurs propres données, sans exiger arbitrairement un PGI. Réserver livraison/PGI/facturation aux prérequis logistiques et comptables effectivement validés.
