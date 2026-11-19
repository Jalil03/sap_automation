# Rapport d'exécution S4600 — exercice 31 — ZPR0

Date : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ

## Résultat

La condition de prix obligatoire `ZPR0` a été créée et vérifiée pour l'exercice 31.

Clé et valeur sauvegardées :

- organisation commerciale : `FR10` ;
- canal de distribution : `10` ;
- client : `1000000112` ;
- article de service : `90000133` ;
- prix : `150,00 EUR` par `1 H` ;
- validité : du `22/10/2026` au `31/12/2026`.

La combinaison installée dans SAP est `Client/article`. Elle ne contient pas la division logistique.

## Contrôles de sécurité

Avant la sauvegarde, VK13 a confirmé l'absence de condition pour la clé exacte. Les valeurs préparées ont été comparées à l'empreinte de l'autorisation `S4600-EX31-ZPR0-GROUP00-20261022`.

Une seule sauvegarde a été déclenchée. SAP a répondu : `Les enregistrements condition ont été sauvegardés`. Aucun nouvel essai de création n'a été effectué.

Aucune commande, livraison, facture ou écriture comptable n'a été sauvegardée. Aucun customizing n'a été modifié.

## Relecture indépendante

La relecture VK13 en mode affichage a retrouvé une seule ligne visible avec :

- article `90000133` — `Prestation de service S4600 (T-D1##)` ;
- montant `150,00 EUR` ;
- unité de prix `1 H` ;
- validité `22.10.2026–31.12.2026`.

Le statut de l'écriture est donc `SAVED_AND_INDEPENDENTLY_VERIFIED`.

## Validation fonctionnelle VA01

La commande de service a été préparée sans sauvegarde avec :

- type de commande `CS` ;
- domaine commercial `FR10 / 10 / 1W` ;
- client `1000000112` ;
- référence client `8-600` ;
- article `90000133` ;
- quantité `3 H`.

SAP a déterminé :

- catégorie de poste `TAD` ;
- condition `ZPR0` à `150,00 EUR` ;
- valeur nette du poste `450,00 EUR` ;
- valeur nette de l'en-tête `450,00 EUR` ;
- aucun message d'erreur.

La commande n'a pas été sauvegardée.

## Conclusion

Le blocage de prix de l'exercice 31 est levé. L'environnement permet maintenant de préparer correctement la commande de service de l'exercice.

La création effective d'une commande reste une opération distincte et nécessite une autorisation dédiée. La facturation et la comptabilité restent également hors du périmètre de cette autorisation.

## Tentative contrôlée de création de la commande

La création a ensuite été autorisée et préparée avec les valeurs validées. Le contrôle anti-doublon OData a confirmé qu'aucune commande `8-600` n'existait.

Lors de la sauvegarde, SAP a ouvert la fenêtre `Sauvegarder document incomplet`. La sauvegarde n'a pas été confirmée. Le journal d'incomplétude contient :

- division logistique du poste 10 ;
- date de chargement ;
- date de mise à disposition article ;
- date de planification du transport ;
- date de sortie de marchandises.

Une relecture OData indépendante a confirmé qu'aucune commande n'a été créée. La fiche `90000133` possède la vue commerciale `FR10/10`, mais aucune vue article-division `FR10` et aucune valorisation. Les exemples `TAD` existants relus dans le système possèdent tous une division logistique.

La commande est donc classée `BLOCKED_INCOMPLETE_PRODUCT_PLANT_VIEW_NO_ORDER_CREATED`. Aucune sauvegarde incomplète, extension article, valorisation ou modification de customizing n'a été effectuée.

Le blocage de prix reste levé, mais l'exercice 31 n'est pas entièrement exécutable tant que la dépendance article-division n'est pas résolue par un contrat et des valeurs prouvés.

## Preuves

- approbation : `data/provisioning/s4600/S4600_CH8_EX31.zpr0_group00.workflow_approval.json` ;
- préflight VK11 : `runtime/sap_reads/s4600_ex31_zpr0_vk11_preflight_2026-10-22.json` ;
- préparation VK11 : `runtime/sap_reads/s4600_ex31_zpr0_vk11_staged_2026-10-22.json` ;
- résultat de sauvegarde : `runtime/sap_writes/s4600_ex31_zpr0_vk11_result.json` ;
- relecture VK13 : `runtime/sap_reads/s4600_ex31_zpr0_customer_material_lookup_2026-10-22.json` ;
- validation VA01 sans sauvegarde : `runtime/sap_reads/s4600_ex31_va01_service_order_staged_2026-10-22.json`.
- résultat de la tentative contrôlée : `runtime/sap_writes/s4600_ex31_service_order_result.json` ;
- journal d'incomplétude : `runtime/sap_reads/s4600_ex31_service_order_incompletion_2026-10-22.json` ;
- réconciliation OData et exemples TAD : `runtime/sap_reads/s4600_ex31_service_order_incomplete_reconciliation_2026-10-22.json`.
