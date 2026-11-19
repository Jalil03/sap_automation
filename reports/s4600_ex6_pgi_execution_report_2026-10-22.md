# S4600 — Exercice 6 — Sortie de marchandises

Date d'exécution : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ

## Résultat

Statut : `VERIFIED_PGI`

La sortie de marchandises de la livraison `80000085` a été comptabilisée par un unique appel API `PostGoodsIssue`. Aucun nouvel essai automatique n'a été effectué.

## Contrôles avant écriture

- Livraison `80000085` existante.
- Prélèvement global : `C` (terminé).
- Mouvement de marchandises global : `A` (non commencé).
- Date réelle du mouvement : vide.
- ETag relu dans la session d'écriture : `W/"'0004'"`.
- Poste `000010` : `10000282`, `FR10/0001`, quantité `10`, mouvement `601`.
- Poste `000020` : `10000283`, `FR10/0001`, quantité `20`, mouvement `601`.

## Écriture autorisée

- Fonction API : `PostGoodsIssue`.
- Paramètre : `DeliveryDocument='80000085'`.
- Réponse HTTP : `200`.
- Nombre de tentatives POST : `1`.
- Autorisation : `S4600-EX6-PGI-80000085-20261022-USER-CONFIRMED`.
- Empreinte du workflow : `92de846da77d719676d3aa3943a5a2aaee7cfe166ac0dd26561b66594d9a3078`.

## Readback indépendant

- Statut global du mouvement : `C` (terminé).
- Statut des deux postes : `C`.
- Date réelle du mouvement : 22/10/2026.
- Nouvel ETag : `W/"'0005'"`.
- Stock `10000282` sur `FR10/0001` : `3709 → 3699`, variation `-10`.
- Stock `10000283` sur `FR10/0001` : `3255 → 3235`, variation `-20`.

Le flux des deux postes référence le document matériel `4900000263`, catégorie `R`. L'API des documents matériels confirme :

- exercice `2026`, utilisateur créateur `ABDELJ`, référence `0080000085` ;
- poste matériel `1` : article `10000282`, quantité `10`, mouvement `601`, `FR10/0001` ;
- poste matériel `2` : article `10000283`, quantité `20`, mouvement `601`, `FR10/0001` ;
- aucune annulation du document matériel.

## Contrôle technique

Le contrôle ST22 effectué après la comptabilisation indique : `Aucun vidage mémoire court -comme sélectionné- disponible`. Le plantage antérieur de fractionnement comptable n'a pas été reproduit.

## Conclusion

L'exercice 6 est exécutable et terminé pour la livraison `80000085`. La sortie de marchandises, les variations de stock et le document matériel sont vérifiés indépendamment.

## Preuves

- `runtime/sap_writes/s4600_ex6_delivery80000085_pgi_result.json`
- `runtime/sap_reads/s4600_ex6_pgi_readiness_2026-10-22.json`
- `runtime/sap_reads/s4600_ex6_stock_baseline_2026-10-22.json`
- `runtime/sap_reads/s4600_ex6_post_pgi_document_flow_2026-10-22.json`
- `runtime/sap_reads/s4600_ex6_material_document_4900000263_2026-10-22.json`
- `runtime/sap_reads/s4600_ex6_st22_today_2026-10-22.json`
- `data/provisioning/s4600/S4600_CH3_EX6.delivery80000085_pgi.workflow_approval.json`
