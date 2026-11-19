# S4600 exercice 31 — lecture de préparation et analyse de risque

Date : 21/10/2026  
Environnement : **A4H / mandant 600 / ABDELJ**  
Mode : **lecture seule, aucune sauvegarde SAP**

## Verdict

L'exercice 31 est **partiellement prêt** et sa difficulté est **moyenne**. La commande de service est techniquement proche d'être exécutable, mais elle ne doit pas encore être sauvegardée : aucun prix `PR00` applicable à `90000133` n'est installé dans les deux clés vérifiées. Le contrôle de facturation commande → facture reste également à prouver avant la création d'une facture.

## Résultats vérifiés

| Contrôle | Résultat |
|---|---|
| Produit | `90000133` existe |
| Type / unité / secteur | `DIEN` / `H` / `1W` |
| Vue commerciale | `FR10/10` existe |
| Groupe de catégories de poste | `LEIS` |
| Détermination VOV4 | `CS + LEIS + usage vide + poste supérieur vide → TAD` |
| Catégorie manuelle autorisée | `TAW` |
| Historique de commandes pour ce produit | Aucun poste trouvé par filtre exact |
| PR00 client `1000000112` + produit `90000133` + division `FR10` | Aucun enregistrement actif au 21/10/2026 |
| PR00 article `FR10/10` + produit `90000133` | Aucun enregistrement actif au 21/10/2026 |
| Contrôle de copie commande → facture | Non encore prouvé |

Le Book demande une commande `CS`, client `1000000112`, référence `8-600`, produit `90000133`, quantité `3 H`, puis une facture directement liée à la commande, sans livraison ni sortie de marchandises.

## Risques

| Action | Risque | Motif |
|---|---|---|
| Lectures effectuées | **Nul** | GET OData et affichages VK13/VOV4, sans sauvegarde |
| Création ciblée de PR00 | **Faible à moyen** | Ne modifie ni stock ni FI immédiatement, mais influence la valorisation commerciale des futures commandes correspondant à la clé et à la validité |
| Création de la commande pilote | **Faible à moyen** | Document persistant; aucun mouvement de stock attendu avec `TAD`, mais le prix et la complétude doivent être contrôlés avant sauvegarde |
| Création de la facture | **Moyen à élevé** | Peut produire une pièce comptable; nécessite un contrôle de copie et une autorisation spécifique |

## Données manquantes avant PR00

Le Book ne fournit pas le prix du service. Avant toute création VK11, il faut donc confirmer explicitement :

- montant du service;
- devise, normalement EUR mais à valider;
- unité de prix et unité de quantité, probablement par `1 H` mais à valider;
- combinaison de clés retenue : article `FR10/10/90000133` ou client/article;
- dates de validité.

Ces valeurs ne doivent pas être inventées.

## Plus petit plan sûr

1. Obtenir la décision métier sur les valeurs exactes de `PR00`.
2. Créer un seul enregistrement VK11 avec recherche anti-doublon et readback VK13.
3. Préparer une commande `CS` sans sauvegarde et vérifier `TAD`, le prix, la complétude et l'absence de livraison.
4. Sauvegarder une seule commande après autorisation ciblée et effectuer le readback OData.
5. Vérifier la facturation proposée; ne créer la facture qu'après une autorisation séparée couvrant l'impact comptable.

## Preuves

- `runtime/sap_reads/s4600_ex28_ex31_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_pr00_vk13_audit_2026-10-21.json`
- `runtime/sap_reads/s4600_ex31_vov4_cs_leis_2026-10-21.json`

## Conclusion

Le paramétrage `TAD` ne nécessite aucune création : il existe déjà. L'exercice est plutôt facile techniquement, mais il reste bloqué par une décision métier sur le prix et par la validation prudente du flux de facturation.
