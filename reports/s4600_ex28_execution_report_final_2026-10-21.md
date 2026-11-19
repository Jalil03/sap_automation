# Rapport final d'exécution — S4600 exercice 28, groupe 00

Date : 21/10/2026  
Environnement : **A4H / mandant 600 / utilisateur ABDELJ**

## Résultat

Statut : **TERMINÉ ET VÉRIFIÉ**

| Étape | Document | Données principales | Vérification |
|---|---:|---|---|
| Demande `DO` | `10000104` | Client `1000000112`, article `10000283`, quantité 3, total 240 EUR | Readback OData vérifié |
| Offre `OFF.` | `20000103` | Référence demande `10000104`, quantité 2, total 160 EUR | Readback OData et référence vérifiés |
| Commande `CS` | `155` | Référence offre `20000103`, référence client `8-900`, quantité 1, total 80 EUR | Readback OData en-tête et poste vérifié |

Le flux a été exécuté sur `FR10/10/1W`. La date de livraison demandée est le `11/11/2026`.

## Stratégie API/BAPI et fallback

Le connecteur RFC SAP 64 bits était déjà présent. `RFC_PING` a réussi vers A4H/600 avec ABDELJ; aucune dépendance supplémentaire n'a donc été installée.

Les métadonnées de `BAPI_QUOTATION_CREATEFROMDATA2` et `BAPI_SALESORDER_CREATEFROMDAT2` ont été inspectées. Les appels en `TESTRUN` ont été exécutés sans persistance : les données métier étaient acceptées, mais SAP retournait l'avertissement `V1 555` indiquant un document incomplet. Comme les journaux d'incomplétude VA21 et VA01 indiquaient au contraire « Le document est complet », aucune écriture BAPI ambiguë n'a été envoyée.

Le fallback SAP GUI prévalidé a donc été utilisé pour une sauvegarde unique de chaque document. Chaque sauvegarde a été précédée d'un contrôle d'absence de doublon et suivie d'une lecture OData indépendante.

## Contrôle final de la commande 155

- type : `CS`;
- organisation / canal / secteur : `FR10/10/1W`;
- donneur d'ordre : `1000000112`;
- référence client : `8-900`;
- référence au document précédent : offre `20000103`, catégorie `B`;
- poste 10 : article `10000283`, quantité 1 PC, catégorie `TAN`;
- division et point d'expédition : `FR10`;
- montant net : 80 EUR;
- quantité confirmée : 1 PC;
- résultat du workflow : `VERIFIED`.

L'endpoint OData spécialisé du flux précédent a répondu HTTP 404. Cela n'invalide pas le contrôle : l'en-tête et le poste relus par `API_SALES_ORDER_SRV` portent tous deux explicitement la référence `20000103`.

## Sécurité et périmètre

- Une seule sauvegarde autorisée et exécutée par document.
- Aucun doublon détecté avant les créations.
- Aucune livraison, sortie de marchandises, facture, écriture FI, modification fiscale, condition tarifaire ou modification de customizing n'a été réalisée dans ce flux.
- Aucun retry aveugle n'a été effectué.

## Preuves principales

- `runtime/sap_writes/s4600_ex28_inquiry_group00_result.json`
- `runtime/sap_writes/s4600_ex28_quotation_group00_result.json`
- `runtime/sap_writes/s4600_ex28_order_group00_result.json`
- `runtime/sap_writes/s4600_ex28_quotation_bapi_testrun.json`
- `runtime/sap_writes/s4600_ex28_order_bapi_testrun.json`
- `runtime/sap_reads/s4600_ex28_va21_incompletion_2026-10-21.json`
- `runtime/sap_reads/s4600_ex28_va01_incompletion_2026-10-21.json`

## Conclusion

L'exercice 28 du groupe 00 est exécutable dans l'environnement FR10 et son instance de validation est terminée : demande `10000104` → offre `20000103` → commande `155`.
