# S4600 — Exercice 7 — Création du document de facturation

Date d'exécution : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ

## Résultat

Statut : `VERIFIED_BILLING_AND_FI_POSTING`

Une facture a été créée avec référence à la livraison `80000085` par un unique appel réel de `BAPI_BILLINGDOC_CREATEMULTIPLE`. Le transfert à la comptabilité financière a réussi.

## Documents créés

- Facture : `90000090` (valeur interne BAPI `0090000090`).
- Type de facture : `F2`.
- Pièce comptable : `9300000009`, exercice `2026`.
- Société : `FR10`.
- Client payeur : `1000000112` — HexaSole Distribution SAS.
- Date de facturation et de comptabilisation : 22/10/2026.

## Montants

- Poste 10, article `10000282`, quantité `10` : net `1500 EUR`, TVA `300 EUR`.
- Poste 20, article `10000283`, quantité `20` : net `1600 EUR`, TVA `320 EUR`.
- Total net : `3100 EUR`.
- TVA : `620 EUR`.
- Total à payer : `3720 EUR`.

## Écritures comptables vérifiées

- Compte client `41111000` : débit `3720 EUR`, client `1000000112`.
- Compte de produits `70110000` : crédit `3100 EUR`.
- Compte de TVA `44310000` : crédit `620 EUR`.

Les débits et crédits s'équilibrent à `3720 EUR`.

## Statuts

- Facture : transfert comptable `C`, comptabilisation `C`.
- Livraison `80000085` : facturation liée `C`, processus global `C` — terminé.
- Pièce comptable : `InvoiceClearingStatus=A`, donc non rapprochée avant l'encaissement, conformément à l'exercice.
- Annulation : aucune.
- ST22 après facturation : aucun dump court disponible.

## Sécurité d'exécution

- Recherche anti-doublon avant appel : aucune facture existante.
- TESTRUN accepté avant l'écriture réelle.
- Nombre d'appels BAPI réels : `1`.
- Aucun retry automatique.
- Aucune correction ou annulation automatique.
- Autorisation : `S4600-EX7-BILLING-80000085-20261022-USER-CONFIRMED`.

## Conclusion

L'exercice 7 est terminé et vérifié. La facture, ses deux postes, la pièce comptable, les comptes, le montant à payer, le transfert FI, le statut final de la livraison et ST22 ont été contrôlés indépendamment.

## Preuves

- `runtime/sap_writes/s4600_ex7_billing_delivery80000085_result.json`
- `runtime/sap_reads/s4600_ex7_billing_90000090_reconciliation_2026-10-22.json`
- `runtime/sap_reads/s4600_ex7_accounting_document_9300000009_2026-10-22.json`
- `runtime/sap_reads/s4600_ex7_st22_post_billing_2026-10-22.json`
- `runtime/sap_reads/s4600_ex7_bapi_billing_testrun2_padded_2026-10-22.json`
- `data/provisioning/s4600/S4600_CH3_EX7.billing_delivery80000085.workflow_approval.json`
