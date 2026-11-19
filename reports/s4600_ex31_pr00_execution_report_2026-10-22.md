# Rapport d'exécution S4600 — exercice 31 — PR00

Date : 22/10/2026  
Environnement autorisé : A4H / mandant 600 / utilisateur ABDELJ

## Résultat

Un seul enregistrement de condition `PR00` a été sauvegardé dans SAP pour la préparation de l'exercice 31.

Valeurs autorisées et envoyées :

- client : `1000000112` ;
- article de service : `90000133` ;
- division logistique : `FR10` ;
- prix saisi : `150,00 EUR` par `1 H` ;
- validité : du `22/10/2026` au `31/12/2026`.

SAP a confirmé la sauvegarde par le message : `Les enregistrements condition ont été sauvegardés`. Une seule action de sauvegarde a été exécutée. Aucun nouvel essai de création n'a été effectué ensuite.

## Relecture indépendante

La lecture RFC sur A972 a confirmé exactement une ligne correspondant à la clé attendue :

| Champ | Valeur relue |
|---|---|
| Application | `V` |
| Type de condition | `PR00` |
| Client | `1000000112` |
| Article interne | `000000000090000133` (`90000133`) |
| Division logistique | `FR10` |
| Début de validité | `20261022` |
| Fin de validité | `20261231` |
| Numéro de condition | `0000008017` |

La clé et les dates sont donc **vérifiées**.

La relecture du montant et des unités via KONP n'a pas abouti : `RFC_READ_TABLE` retourne l'exception `TABLE_WITHOUT_DATA`. VK13 ne peut pas afficher la condition parce qu'il contrôle la présence d'une vue article pour `90000133 / FR10` et renvoie : `L'article 90000133 dans la division FR10 n'est pas géré.`

Le montant `150,00 EUR / 1 H` a bien été relu dans l'écran VK11 avant la sauvegarde, puis SAP a confirmé la sauvegarde. Cependant, selon la règle de relecture indépendante du projet, le montant reste classé **UNKNOWN en post-sauvegarde** tant qu'une autre source SAP ne l'a pas relu.

## Sécurité et périmètre

- aucune seconde création PR00 ;
- aucune modification de la fiche article ;
- aucune extension de l'article à FR10 ;
- aucune commande client créée ;
- aucune facture ni écriture FI créée ;
- aucune modification de customizing.

## Statut de l'exercice 31

La condition `PR00` est créée et sa clé est vérifiée. Toutefois, le test VA01 montre que la procédure de prix de la commande exige `ZPR0`. L'exercice 31 n'est donc pas encore exécutable.

Restent à faire :

1. obtenir une autorisation distincte pour créer la condition `ZPR0` requise ;
2. créer `ZPR0` seulement après un nouveau contrôle d'absence, puis effectuer une relecture indépendante ;
3. refaire le test VA01 sans sauvegarde pour confirmer le prix et la complétude ;
4. demander une autorisation distincte avant toute création de commande ;
5. conserver la facturation et FI sous une autorisation séparée.

## Preuves

- résultat du write : `runtime/sap_writes/s4600_ex31_pr00_vk11_result.json` ;
- relecture RFC : `runtime/sap_reads/s4600_ex31_pr00_rfc_readback_2026-10-22.json` ;
- relecture VK13 : `runtime/sap_reads/s4600_ex31_pr00_vk13_customer_plant_readback_2026-10-22.json` ;
- approbation : `data/provisioning/s4600/S4600_CH8_EX31.pr00_group00.workflow_approval.json`.

## Test de la commande de service et diagnostic ZPR0

Une commande de service a été préparée dans VA01, sans sauvegarde, avec les valeurs suivantes :

- type de commande : `CS` ;
- domaine commercial : `FR10 / 10 / 1W` ;
- donneur d'ordre : `1000000112` ;
- référence client : `8-600` ;
- article de service : `90000133` ;
- quantité : `3 H` ;
- catégorie de poste déterminée : `TAD`.

SAP a déterminé le type de condition obligatoire `ZPR0`, mais aucun prix n'a été trouvé. Le montant net est resté à `0,00 EUR` et la barre d'état a affiché : `Erreur ds déterm. prix (condition obligatoire ZPR0 manquante)`. La commande n'a pas été sauvegardée.

La définition de `ZPR0` a ensuite été relue via l'API : son accès est associé à la séquence `PR00`. La recherche exacte en VK13, en mode affichage uniquement, a utilisé la combinaison `Client/article` et les valeurs `FR10 / 10 / 1000000112 / 90000133`, valables au `22/10/2026`. SAP a répondu : `Il n'existe aucun enreg. condition pour cette sélection.`

Conclusion mise à jour : l'enregistrement `PR00` existe, mais il n'est pas le type de condition consommé par la procédure de prix de cette commande. L'exercice 31 reste bloqué par l'absence de `ZPR0`. La création de `ZPR0` constitue une nouvelle écriture, avec une clé différente de celle déjà approuvée pour `PR00`; elle nécessite donc une autorisation explicite distincte avant exécution.

Preuves complémentaires :

- commande VA01 préparée sans sauvegarde : `runtime/sap_reads/s4600_ex31_va01_service_order_staged_2026-10-22.json` ;
- définition API de ZPR0 : `runtime/sap_reads/s4600_ex31_zpr0_condition_type_2026-10-22.json` ;
- combinaisons de clés VK13 : `runtime/sap_reads/s4600_ex31_zpr0_vk13_keys_2026-10-22.json` ;
- sélection exacte et constat d'absence : `runtime/sap_reads/s4600_ex31_zpr0_customer_material_lookup_2026-10-22.json`.
