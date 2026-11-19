# Vérification S4600 sur FR10 — 21/10/2026

## Périmètre et sécurité

- Système vérifié : A4H
- Mandant : 600
- Utilisateur : ABDELJ
- Opérations effectuées : lectures OData et affichages SAP GUI uniquement
- Aucune création, modification, sauvegarde, sortie de marchandises ou écriture comptable n'a été exécutée.

## Verdict

La route FR10 / 10 / 1W est techniquement crédible et déjà utilisée, mais le déploiement pédagogique n'est pas encore prêt sans réserves. Le parcours historique commande → livraison → sortie de marchandises → facture → pièce comptable est prouvé pour plusieurs documents. Quatre points doivent toutefois être fermés avant le lancement : le prix PR00 du service, un nouveau test contrôlé de sortie de marchandises, la stratégie d'unicité des conditions participants et les écarts de fiches produits.

## Résultats

| Contrôle | Statut | Résultat |
|---|---|---|
| Identité SAP | EXISTS | A4H / 600 / ABDELJ vérifié avant les lectures GUI. |
| Société et division FR10 | EXISTS | Société FR10 et division logistique FR10 présentes. |
| Domaine commercial FR10 / 10 / 1W | EXISTS | Données commerciales présentes pour les clients proposés. |
| Clients 1000000112 et 1000000113 | EXISTS | Rôles FLCU00/FLCU01, société FR10, domaine commercial FR10/10/1W, devise EUR et fonctions partenaires observés. |
| Produits 10000282 et 10000283 | EXISTS_WITH_GAPS | Vues vente FR10/10, division 1W, division logistique FR10, magasin 0001 et valorisation FR10 présents. Les descriptions françaises sont « CARBURANT BRUT(Essence) », incompatibles avec les articles attendus. |
| Produit 10000284 | EXISTS_WITH_GAPS | Même socle que les deux produits précédents, mais la division de livraison est vide dans la vue vente-livraison. Des commandes historiques ont néanmoins déterminé FR10 et ont été livrées. |
| Service 90000133 | EXISTS_WITH_GAPS | DIEN, unité H, division 1W, groupe LEIS et vue vente FR10/10 présents. Classifications fiscales FR et CM observées. Aucun prix PR00 n'a pu être prouvé de manière exhaustive. |
| Type de commande | CONFIRMED | Dans V_TAUUM : TA → OR en anglais, TA → CS en français. Aucun code CDCL trouvé. En français, OR correspond à RA (ordre de réparation), donc le contexte de langue est déterminant. |
| Offre | CONFIRMED | Dans V_TAUUM : AG → OFF. en français. |
| Cycle FR10 | CONFIRMED_HISTORICALLY | 14 commandes FR10/10/1W et 13 livraisons au point d'expédition FR10 observées. Plusieurs chaînes complètes aboutissent à une pièce comptable, notamment les factures 90000081, 90000084 et 90000089. D'autres factures observées ne sont pas comptabilisées en FI. |
| Prix historiques des articles | CONFIRMED_HISTORICALLY | Les documents observés corroborent 150 EUR pour 10000282, 80 EUR pour 10000283 et 120 EUR pour 10000284. Cela ne prouve pas à lui seul l'état actuel de toutes les fiches de condition. |
| Dump SAPLGLT2 | NO_RECURRENCE_OBSERVED | ST22 montre SAPLGLT2 en mandants 400 et 600 le 20/10, dont le dernier en 600 à 07:43:15. Aucun SAPLGLT2 ultérieur n'a été observé sur les 20–21/10. La régénération du code n'est pas directement prouvée. |
| Nouveau test de sortie de marchandises | NOT_EXECUTED | Il s'agit d'une écriture logistique/comptable. Aucune autorisation ciblée ni livraison de test n'a été fournie. |

## Point critique sur les objets participants

Le book canonique indique :

- exercice 11 : PR00 sur `T-MS4##`, 35 EUR ;
- exercice 12 : référence article client `K-MS-##` pour `T-S50A## / T-MS1##` ;
- exercice 13 : PR00 sur `T-S50A## / T-MS1##`, avec 1 = 53 EUR, 10 = 51 EUR et 20 = 49 EUR ;
- exercice 14 : K007 sur `T-S50A##`, avec les seuils 100 = -1 %, 500 = -2 % et 1 000 = -3 %.

La proposition reçue affirme que les exercices 13–14 porteront sur `T-CUS##`, `T-MS4##` et `K-MS-##`. Ce n'est pas ce que contient le book canonique. Si `T-S50A##` et `T-MS1##` sont remplacés pour tous par les objets partagés 1000000112 et 10000282, les participants peuvent écraser les mêmes conditions PR00/K007.

Le dépôt possède bien un résolveur déterministe `##` : codes `00` à `99`, `00` réservé au formateur, remplacement dans une copie runtime et blocage si un placeholder exécutable subsiste. Ses 11 tests ciblés passent. Cela garantit la transformation logicielle, mais pas l'attribution organisationnelle d'un code distinct à chaque participant ni l'existence des objets correspondants dans SAP.

## Conditions avant GO

1. Choisir explicitement la pédagogie des exercices 13–14 : conserver les clés du book avec des objets réellement distincts par participant, ou documenter une adaptation vers `T-CUS## / T-MS4##`.
2. Vérifier toutes les clés d'accès PR00 de 90000133 puis, si le prix est réellement absent, définir le montant, la devise, l'unité de prix, la période de validité et la combinaison de clés avant toute création VK11.
3. Corriger ou accepter formellement les descriptions françaises erronées des produits 10000282–10000284.
4. Décider si la division de livraison vide de 10000284 doit être complétée ou si la détermination démontrée par le flux est la règle retenue.
5. Autoriser séparément un test contrôlé de sortie de marchandises sur une livraison dédiée, puis vérifier ST22, le document matériel et la pièce comptable en lecture indépendante.
6. Affecter un suffixe unique à chaque participant et vérifier l'absence des objets avant les exercices de création.

## Preuves techniques

- `runtime/sap_reads/s4600_fr10_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_gui_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_v_tauum_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_pr00_vk13_audit_2026-10-21.json`
- `data/validated/canonical_objects.json`
- `src/training_context/placeholder_resolver.py`
- `tests/test_training_context.py`
