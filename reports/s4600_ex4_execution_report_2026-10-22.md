# Rapport d'exécution S4600 — exercice 4

Date : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ  
Mode : lecture seule

## Résultat

L'exercice 4 est **terminé et vérifié** à partir de la commande client `154` créée pendant l'exercice 3.

| Question du book | Valeur vérifiée |
|---|---|
| Conditions de paiement | `0004` |
| Valeur nette totale | `3 100,00 EUR` |
| Poids brut total | `39,000 KG` |
| Livraison complète obligatoire | Non (`CompleteDeliveryIsDefined = false`) |
| Division du poste 10 | `FR10` |
| Prix unitaire poste 10 | `150,00 EUR` |
| Prix unitaire poste 20 | `80,00 EUR` |
| Date de livraison confirmée du poste 10 | `28/10/2026` |
| Quantité confirmée du poste 20 | `20 ST` |
| Réceptionnaire de facture | `1000000112` — fonction localisée `RF`, code interne `RE` |
| Statut global du processus | `C` |

Les données ont été relues directement via `API_SALES_ORDER_SRV`. Aucune donnée SAP n'a été modifiée.

## Preuve

- `runtime/sap_reads/s4600_ex4_order154_readback_2026-10-22.json`
