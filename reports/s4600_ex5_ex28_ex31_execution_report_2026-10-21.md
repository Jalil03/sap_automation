# Rapport d'exécution S4600 — exercices 5, 28 et 31

Date : 21/10/2026  
Environnement : **A4H / mandant 600 / ABDELJ**

## Résultat global

| Exercice | Statut | Résultat |
|---|---|---|
| 5 — livraison | **PRÉLÈVEMENT TERMINÉ** | Livraison `80000085`, deux postes sur magasin `0001`, statut de prélèvement `C`. Aucune sortie de marchandises. |
| 28 — avant-vente | **TERMINÉ ET VÉRIFIÉ** | Demande `10000104` → offre `20000103` → commande `155`, sur `FR10/10/1W`, avec readbacks OData indépendants. |
| 31 — service | **NON EXÉCUTÉ / DONNÉES MANQUANTES** | Produit `90000133` présent; prix PR00, détermination `TAD` et flux de facturation non prouvés. |

## Exercice 5

### État vérifié

- commande source : `154`;
- livraison : `80000085`;
- poste `000010` : produit `10000282`, quantité 10, division `FR10`, magasin `0001`;
- poste `000020` : produit `10000283`, quantité 20, division `FR10`, magasin `0001`;
- statut global de prélèvement : `C`;
- statut global de mouvement de marchandises : `A`;
- date réelle de mouvement : vide.

### Difficultés techniques traitées

1. Le premier PATCH du poste `000010` a réussi; le poste `000020` a d'abord été refusé avec HTTP 412 à cause d'un ETag devenu obsolète.
2. Après réconciliation, le poste `000020` a été mis à jour avec un ETag fraîchement lu.
3. `PickAllItems` a d'abord répondu HTTP 428 sans `If-Match`.
4. La route non versionnée a ensuite répondu HTTP 412 malgré l'ETag courant.
5. La route officielle `API_OUTBOUND_DELIVERY_SRV;v=2`, vérifiée par GET, a accepté `PickAllItems` avec HTTP 200.
6. Le readback final donne l'ETag `W/"'0004'"` et le statut de prélèvement `C`.

Chaque erreur a été arrêtée, enregistrée et réconciliée avant l'étape suivante. Aucun retry aveugle n'a été effectué.

### Limite restante

La sortie de marchandises n'était pas incluse dans l'autorisation. Elle doit faire l'objet d'une autorisation distincte, car elle modifie le stock et peut générer un document matériel/comptable. Avant cette opération, il faudra relire l'ETag `0004`, confirmer le statut `C`, puis contrôler ST22 et les documents créés après l'appel.

## Exercice 28

### Résultat exécuté et vérifié

- demande `DO` : `10000104`, quantité 3, total 240 EUR;
- offre `OFF.` : `20000103`, référence à la demande, quantité 2, total 160 EUR;
- commande `CS` : `155`, référence à l'offre, référence client `8-900`, quantité 1, total 80 EUR;
- domaine commercial : `FR10/10/1W`;
- client : `1000000112`;
- produit : `10000283`;
- date de livraison demandée : 11/11/2026;
- readbacks OData indépendants : **VERIFIED**.

Le connecteur RFC SAP 64 bits était déjà installé et `RFC_PING` a réussi. Les BAPI d'offre et de commande ont d'abord été testées sans persistance, conformément à la stratégie API-first. SAP retournant l'avertissement `V1 555` alors que les contrôles GUI indiquaient « Le document est complet », les sauvegardes ont été réalisées une seule fois par SAP GUI, puis vérifiées par API. Aucune dépendance supplémentaire n'a été nécessaire.

## Exercice 31

### Éléments disponibles

- produit `90000133` : `DIEN`, unité `H`, secteur `1W`, groupe `LEIS`;
- vue de vente : `FR10/10`;
- client prévu : `1000000112`;
- commande prévue : type `CS`, référence `8-600`, quantité 3 H.

### Blocages exacts

1. Aucun prix PR00 applicable à `90000133` n'est prouvé.
2. La combinaison exacte déterminant la catégorie de poste `TAD` n'a pas été relue.
3. Le contrôle de copie commande de service vers facture n'est pas prouvé.

Créer directement la commande pourrait produire un document incomplet ou incorrect. Créer PR00 sans connaître la clé PR02, la validité et l'unité exactes pourrait influencer d'autres documents. Aucune écriture n'a donc été envoyée.

### Plus petites actions nécessaires

1. Lecture GUI VOV4 de la combinaison `CS + LEIS → TAD`.
2. Lecture VK13 exhaustive des accès PR02 applicables à `90000133`.
3. Si le prix manque, validation du montant, de l'unité, de la devise et de la validité avant une autorisation VK11.
4. Création contrôlée d'une commande pilote, puis readback de la catégorie `TAD` et du prix.

## Sécurité

- Toutes les opérations live ont été limitées à A4H/600/ABDELJ.
- Aucune sortie de marchandises, facture, condition tarifaire, donnée FI/fiscale, donnée de customizing ou modification Material Ledger n'a été exécutée.
- Les écritures ont été précédées de LOOKUP et suivies de READBACK.
- Les échecs HTTP 412/428 ont été traités comme des refus avant écriture et réconciliés avant toute suite.

## Preuves principales

- `runtime/sap_writes/s4600_ex5_delivery80000085_pick_v2_result.json`
- `runtime/sap_writes/s4600_ex5_delivery80000085_pick_attempt1.json`
- `runtime/sap_writes/s4600_ex5_delivery80000085_resume_pick_result.json`
- `runtime/sap_writes/s4600_ex5_delivery80000085_pick_etag_result.json`
- `runtime/sap_writes/s4600_ex5_delivery80000085_pick_after_csrf_result.json`
- `runtime/sap_reads/s4600_delivery80000085_etags_2026-10-21.json`
- `runtime/sap_reads/s4600_ex28_inquiry_contract_2026-10-21.json`
- `runtime/sap_reads/s4600_ex28_ex31_audit_2026-10-21.json`
- `runtime/sap_writes/s4600_ex28_inquiry_group00_result.json`
- `runtime/sap_reads/s4600_ex28_va21_reference_preflight_2026-10-21.json`

## Conclusion

L'exercice 5 est terminé jusqu'au prélèvement inclus. L'exercice 28 est terminé et vérifié : demande `10000104`, offre `20000103`, commande `155`. L'exercice 31 reste bloqué par la validation de `TAD` et de PR00 avant toute commande de service.
