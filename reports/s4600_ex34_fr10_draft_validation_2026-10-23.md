# S4600 exercice 34 — validation du brouillon FR10

Date : 23/10/2026. Environnement : **A4H / 600 / ABDELJ**.

Autorisation utilisateur : vérifier **sans sauvegarde** le retour de trois pièces de `10000284`, client `1000000112`, sur FR10 à la place de 1020. Cette autorisation ne couvre pas la création persistante du retour, une entrée de stock, un avoir ou un changement de paramétrage.

## Résultat

**Préparation du document de retour validée en mémoire. Exercice 34 non terminé.**

| Donnée | Valeur observée dans SAP |
|---|---|
| Type | RE — Créer Retours |
| Domaine commercial | FR10 / 10 / 1W |
| Donneur d'ordre et réceptionnaire | 1000000112 — HexaSole Distribution SAS |
| Article | 10000284 — Rubber Outsole Pair |
| Quantité | 3, unité externe SAP 289 |
| Motif du book | Code **103**, libellé observé **Ecart quantité** |
| Division déterminée automatiquement | **FR10**, KC FR Paris |
| Point d'expédition déterminé automatiquement | **FR10** |
| Catégorie de poste | **REN** |
| Catégorie d'échéance | **DN** |
| Quantité de l'échéance / confirmée | **3 / 3** |
| Date proposée par SAP | **23/10/2026** — le book ne prescrit pas une autre date pour ce retour |
| Prix déterminé par SAP | **120 EUR**, condition **ZPR0** |
| Montant net | **360 EUR** |
| Blocage de facturation | **Crtle avoir**, conservé ; aucune tentative de suppression |
| Contrôle de complétude | Message SAP **Le document est complet** |

Les prix, les données client/article et le paramétrage n'ont pas été modifiés. La division FR10 a été déterminée par SAP ; elle n'a pas été forcée sur un poste qui aurait proposé une autre usine.

## Messages rencontrés

- SAP a demandé le motif de commande. Le code 103 a été choisi après lecture des libellés de la liste, en accord avec le book ; aucun code n'a été inventé.
- L'avertissement « Veuillez vérifier la date de la facture: 23.10.2026 » a été confirmé dans le brouillon, conformément à la consigne du book. La date n'a pas été changée arbitrairement.
- Après ces validations : pas de message bloquant, prix et données logistiques déterminés, document complet selon SAP.

## Fermeture et contrôle indépendant

Le dialogue « Voulez-vous sauvegarder vos données ? » a reçu **Non**. Retour à **SAP Easy Access**, transaction `SESSION_MANAGER`, une seule fenêtre. Le brouillon a été abandonné sans sauvegarde.

Relecture OData indépendante après fermeture :

- `A_CustomerReturn`, filtre `SalesOrganization = FR10` : HTTP 200, zéro correspondance.
- `A_CustomerReturnItem`, article `10000284`, usine `FR10` : HTTP 200, zéro correspondance.

**Aucun numéro de retour ou de livraison créé ; aucun mouvement de stock, aucune facture ni aucun avoir.**

## Limite et prochaine autorisation

La validation prouve la détermination du **document de retour en brouillon** sur FR10. Elle ne prouve pas encore sa sauvegarde, le contrôle de copie vers la livraison de retour, le mouvement de réception, le type de stock résultant ou la création de l'avoir. Il serait incorrect de déclarer le flux complet validé.

Prochaine étape possible, sur autorisation distincte : créer **un seul retour RE**, FR10/10/1W, client `1000000112`, article `10000284 × 3`, motif `103`, en conservant le blocage d'avoir ; effectuer un nouveau lookup et une relecture indépendante. Cette étape n'inclut pas d'entrée de stock ou d'avoir. Avant une écriture API, le contrat de création RE doit être démontré ; l'existence des métadonnées ne suffit pas.

## Route et preuves

L'API de retours est disponible, mais aucun mode de simulation non persistante n'est démontré. Le test a donc utilisé le pont SAP GUI existant en mode **PREPARE**, sans route de sauvegarde dans le script. La compétence Computer Use a été lue ; son outil d'exécution n'étant pas exposé, le contrôle SAP ciblé existant a été utilisé pour ce brouillon. Aucun réglage de sécurité Windows ou SAP n'a été modifié.

- `scripts/stage_s4600_ex34_return_no_save.py` : saisie et lecture du brouillon, sans SAVE.
- `runtime/sap_reads/s4600_ex34_draft_initial_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_draft_header_items_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_draft_reason_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_draft_inspect_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_item_details_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_shipping_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_schedules_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_incompletion_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_draft_exit_2026-10-23.json`.
- `runtime/sap_reads/s4600_ex34_existing_returns_2026-10-23.json` : relecture après fermeture.
