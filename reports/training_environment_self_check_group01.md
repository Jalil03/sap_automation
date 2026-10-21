# Précontrôle autonome de l'environnement S4600/S4615 — groupe 01

Date : 20 octobre 2026  
Environnement : A4H / client 600 / ABDELJ  
Mode : READ-ONLY

## Conclusion

Nous pouvons éviter une phase de questions/réponses avec l'administrateur. Les preuves du projet et les lectures SAP permettent déjà de classer les principaux prérequis. Aucun package officiel de cours n'est identifié dans le dépôt ou les traces de transports ; cette information n'est plus un préalable bloquant. Nous poursuivons le bootstrap incrémental et transmettrons plus tard un ticket unique contenant seulement les opérations administrateur confirmées nécessaires.

## Contrôles déjà réalisés sans administrateur

| Prérequis | Résultat autonome | Action |
|---|---|---|
| Société 1010 | Présente, BE/EUR/CABE | Réutiliser |
| Zone commerciale 1010/10/00 | Présente et relue sur des clients existants | Réutiliser |
| Usine 1010 | Absente : API 404 et audit complet T001W/T001K | À créer/configurer par Org + FI/MM |
| Usine 1020 | Absente : API 404 | À créer seulement si le scénario S4600 officiel la maintient |
| Usine 1710 | Présente mais société 1710, USD/YCOA | Ne pas substituer à 1010 |
| Point d'expédition 1010 | Présent et vérifié | Conserver |
| Point Z001 | Absent après scan TVST 20/20 | Restaurer pour S4600 |
| TVKWZ | 1010/10 pointe uniquement vers 1710 dans l'audit | Nouvelle affectation nécessaire après création de 1010 |
| TVSWZ | Aucun lien vers point 1010 | À configurer après l'usine |
| OVL2 | Aucune chaîne cible exploitable prouvée | À configurer après les valeurs expédition approuvées |
| CDCL | Absent après scan VOV8 complet 266/266 | Restaurer depuis la définition officielle du cours |
| ZA01/ZF01 | Présents et vérifiés | Conserver |
| ZF01←LF/TAN | Présent et relu | Conserver ; test métier ultérieur |
| ZF01 RFBFK | `true`, relu | Conserver |
| PR00/K007/PPSV | Types présents | Les enregistrements d'exercice ne sont pas précréés |
| Service conditions | Metadata HTTP 500, alias manquant | Activation Gateway nécessaire |
| Warehouse 1010 | 404 dans la route API testée | EWM/Basis doit fournir la cible officielle |
| Utilisateurs participants | Sessions S4600-01/S4615-01 non disponibles dans les preuves | Basis doit fournir rôles/catalogues et accès |
| Transport A4HK908422 | Transport de changements du projet, non package officiel de cours | Ne pas le présenter comme baseline SAP officielle |
| Package officiel | Aucun package vérifié dans dépôt/traces | Non bloquant ; continuer le bootstrap incrémental |

## Contrôles master data déjà réalisés

| Domaine | Résultat |
|---|---|
| T-S50A01 | BP root vérifié ; aucune adresse, rôle ou extension client |
| T-D101/T-MS101/T-MS201 | Basic Data vérifiées ; aucune vue Sales/Tax/Plant/Valuation |
| T-S50B01/T-MS301/T-F101 | Aucun mapping déterministe ; absence globale non prouvée |
| C615-A01 | Client 1010/1010-10-00 vérifié ; fiscalité vide |
| P615-101 | Basic Data seulement |
| C615-B01/C01/E01/F01 et P615-201/501/601 | Aucun mapping déterministe |
| Fiscalité de référence | BE/MWST/1 observé uniquement sur P615-400 ; ce n'est pas une règle générale ni une décision pour les autres produits |

## Ce que nous pouvons encore faire seuls

1. Construire les payloads racine/SD à partir des valeurs exactes du Book et des décisions déjà approuvées.
2. Vérifier metadata, champs obligatoires, numérotation, anti-doublon et readback.
3. Préparer les fingerprints et approbations par objet.
4. Créer ou étendre les objets ne nécessitant ni FI/MM, ni fiscalité inconnue, ni usine.
5. Maintenir mappings, checkpoints et preuves.

## Décisions irréductibles, sans les confondre avec des contrôles techniques

Ces points ne peuvent pas être déduits par une lecture SAP :

- classification fiscale à utiliser pour chaque nouveau client/produit ;
- valeurs client obligatoires non définies par le Book ;
- définition métier officielle de CDCL/Z001 si aucune source de référence n'est fournie ;
- conception de l'usine/valorisation 1010 et 1020 ;
- stock initial et comptes FI/MM ;
- traitement FI/CO Material Ledger de C+039.

Ils seront regroupés en un seul dossier de décision. Aucun échange administrateur séparé ne sera demandé pour les contrôles déjà conclus ci-dessus.

## Prochaine étape interne

Préparer un premier lot sans écriture SAP :

1. payload final de l'extension client T-S50A01 avec champs manquants explicitement nuls ;
2. payloads Sales Delivery de T-D101/T-MS101/T-MS201 avec bloc fiscal explicite ;
3. fiches de création proposées pour T-S50B01/T-MS301/T-F101 sans valeurs inventées ;
4. dossier unique administrateur avec les opérations organisationnelles déjà démontrées nécessaires.
