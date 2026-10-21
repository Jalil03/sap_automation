# Audit final strictement READ-ONLY — S4600 Book 00 et S4615

**Date de référence :** 20 octobre 2026  
**Environnement contrôlé :** A4H / client 600 / utilisateur ABDELJ  
**Mode :** GET OData ciblés et lecture de preuves locales uniquement. Aucun POST, PATCH, PUT, DELETE, Save SAP, correction, relance d'écriture échouée ou changement de Customizing n'a été exécuté pendant cet audit.

## A. Résumé exécutif

SAP LIVE était accessible. Les GET du 20 octobre confirment directement l'identité et l'état courant des cinq objets principaux de chaque périmètre, les vues associées, les sociétés/usines et les références de commandes du Book.

- **S4600 :** `T-S50A01 → 1000000116`, `T-D101 → 90000132`, `T-MS101 → 60000445` et `T-MS201 → 60000446` existent. Ce sont uniquement une racine BP et trois racines produit. Le BP n'a ni adresse, ni rôle FLCU00/FLCU01, ni racine client, ni société 1010, ni zone `1010/10/00`, ni partenaires, ni fiscalité. Les trois produits n'ont aucune vue Sales Delivery, Sales Tax, usine, comptabilité ou valorisation. `LEIS/H` est bien observé sur la racine de T-D101 ; `NORM` n'est enregistré ni sur T-MS101 ni sur T-MS201.
- **Tentatives S4600 :** l'extension T-D101 est restée `AMBIGUOUS`, mais le readback frais confirme qu'aucune vue commerciale n'existe. T-MS101 a été rejeté par `MG/172` pour fiscalité incomplète. T-MS201 n'a pas été envoyé. Il est donc inexact de dire que les trois extensions ont échoué de la même manière.
- **S4615 :** `C615-A01 → 1000000115` et `C615-D00 → 1000000114` existent avec adresse, rôles client, société 1010 et zone `1010/10/00`; aucune classification fiscale client n'est exposée. `P615-101 → 10000289` est une racine FERT/M/PC/00 sans vente, taxe, usine ou valorisation. `P615-400 → 10000287` a vente `1010/10`, fiscalité BE/MWST/1, usine 1710 et ATP `SP`, mais aucune vue de valorisation/comptabilité/ML.
- **Organisation :** société 1010 = BE/EUR/**CABE** ; société 1710 = US/USD/YCOA. Les usines 1010 et 1020 répondent 404 ; l'usine 1710 existe et appartient à la société 1710. Le point d'expédition 1010 existe selon checkpoint SAP GUI vérifié, mais les audits exhaustifs historiques ne trouvent ni TVSWZ vers ce point ni règle OVL2 utilisable. Le warehouse 1010 répond 404 dans l'API interrogée.
- **SD :** CDCL est absent du scan complet VOV8 266/266. PR00, K007 et PPSV existent comme types de condition ; le service des enregistrements de conditions reste en erreur HTTP 500 faute d'alias. `ZA01`, `ZF01`, le copy control `ZF01←LF/TAN` et `RFBFK=true` sont vérifiés par relecture/checkpoint, mais aucune chaîne transactionnelle n'a validé leur fonctionnement métier.
- **Exercices :** seuls les exercices conceptuels S4600 2, 15, 24 et 29 ont une réponse historique vérifiée. Aucun exercice transactionnel S4600 et aucun des 13 exercices S4615 n'est terminé. Les tests automatisés et les configurations vérifiées ne sont pas comptés comme exercices métier.
- **Références S4615 :** les recherches LIVE exactes de toutes les références groupe 01 demandées retournent zéro commande. La chaîne `01S6415-PB` est exactement celle imprimée dans le Book ; elle est probablement une coquille pour `01S4615-PB`, mais les deux variantes ont été testées et aucune n'existe.

**Verdict : `MAIL_À_CORRIGER`.** Les identités des objets sont confirmées, mais les affirmations sur les extensions fiscales, la fonctionnalité du copy control et la priorité des exercices 3 doivent être nuancées comme indiqué en sections F et G.

## Méthode, hiérarchie et limites des preuves

1. Un GET SAP LIVE exact prévaut sur un mapping et sur une ancienne section de rapport.
2. Un checkpoint avec relecture indépendante prouve l'état de la clé configurée, pas un processus métier complet.
3. Un mapping seul ne prouve pas l'existence ; tous les mappings déclarés existants ci-dessous ont été relus en LIVE.
4. Un résultat 404 sur un identifiant logique et zéro résultat sur un alias testé ne prouvent pas l'absence sous tout numéro interne : les objets sans mapping restent `UNKNOWN`.
5. Aucun PDF binaire n'a été interprété isolément : les objectifs et valeurs viennent des extractions Markdown issues des PDF, [S4600_EXERCISES.md](../data/books/S4600/S4600_EXERCISES.md) et [S4615_full_clean.md](../data/books/S4615/S4615_full_clean.md).
6. Les preuves LIVE ont été obtenues par le script GET-only [audit_final_s4600_s4615_readonly.py](../scripts/audit_final_s4600_s4615_readonly.py). Le script n'écrit ni dans SAP ni dans un fichier.

### Nature des valeurs

- **Valeurs exactes du Book :** identifiants à `##`, quantités, références de commande, types de documents/conditions, organisations et étapes décrites dans les deux extractions.
- **Valeurs du nouveau dataset approuvé, non issues du Book :** descriptions françaises de T-D101/T-MS101/T-MS201, types DIEN/HAWA, secteurs W, unités H/PC et propositions LEIS/NORM. Leur approbation autorise le dataset nommé, pas une généralisation à d'autres objets.
- **Valeurs installées observées :** numéros internes, rôles/vues réellement retournés, CABE/YCOA, PR00/K007/PPSV, ZA01/ZF01, LF/TAN, RFBFK et les codes exposés par les objets existants.
- **Hypothèses ou projets non persistés :** NORM sur MS101/MS201, les objets supplémentaires sans mapping et tout paramètre FI/taxe/usine non relu. Ils ne sont jamais présentés comme faits SAP.

## 1. Vérification des objets S4600

| Objet | État LIVE | Complétude vérifiée | Conclusion |
|---|---|---|---|
| T-S50A01 / 1000000116 | Racine BP 200, BPAB, catégorie 2, nom et SearchTerm1 exacts | Adresse 0 ; rôles 0 ; A_Customer 404 ; société 1010 404 ; `1010/10/00` 404 ; partenaires 0 ; taxes 0 | **EXISTANT_INCOMPLET — BP_ROOT_ONLY** |
| T-D101 / 90000132 | DIEN/W/H/00, description FR exacte, racine `ItemCategoryGroup=LEIS` | Sales Delivery 0 ; Sales Tax 0 ; usine 0 ; valorisation 0 | **EXISTANT_INCOMPLET — PRODUCT_BASIC_ONLY** |
| T-MS101 / 60000445 | HAWA/W/PC/00, description FR exacte | `ItemCategoryGroup` racine vide ; Sales Delivery 0 ; Sales Tax 0 ; usine/valorisation 0 | **EXISTANT_INCOMPLET — PRODUCT_BASIC_ONLY** |
| T-MS201 / 60000446 | HAWA/W/PC/00, description FR exacte | Identique à T-MS101 ; aucune valeur NORM persistée | **EXISTANT_INCOMPLET — PRODUCT_BASIC_ONLY** |
| T-S50B01 | Clé littérale 404 et SearchTerm1 exact 0 ligne | Aucun mapping interne vérifié | **UNKNOWN**, seulement prévu comme donnée préchargée |
| T-MS301 | Clé littérale 404 et ProductOldID exact 0 ligne | Aucun mapping interne vérifié | **UNKNOWN**, seulement prévu |
| T-F101 | Clé littérale 404 et ProductOldID exact 0 ligne | Aucun mapping interne vérifié | **UNKNOWN**, seulement prévu |
| T-CUS01 | Clé littérale 404 et SearchTerm1 exact 0 ligne | Sortie à créer pendant l'exercice 9, pas donnée préchargée | **NOT_CREATED_BY_PROJECT / UNKNOWN hors alias testés** |
| T-MS401 | Clé littérale 404 et ProductOldID exact 0 ligne | Sortie à créer pendant l'exercice 11 | **NOT_CREATED_BY_PROJECT / UNKNOWN hors alias testés** |

### Tentatives d'extension S4600

| Opération | Preuve | État réel |
|---|---|---|
| T-D101 Sales `1010/10`, LEIS | Checkpoint `AMBIGUOUS`; POST au résultat ambigu ; GET LIVE frais : 0 Sales Delivery et 0 taxe | **Non créée.** Ne pas relancer sans réconciliation/autorisation ; l'absence courante est désormais relue. |
| T-MS101 Sales `1010/10`, NORM | HTTP 400 SAP `MG/172`, « classification des taxes … incomplète » ; GET LIVE : 0 vue | **REJECTED**, aucune extension créée. |
| T-MS201 Sales `1010/10`, NORM | Non exécuté après le rejet déterministe et la fiscalité vide | **NOT_ATTEMPTED**, aucune extension créée. |
| T-S50A01 extension client | Aucune tentative d'extension validée ; GET LIVE montre uniquement la racine | **NOT_ATTEMPTED/NOT_CREATED**. |

Les trois approbations PRODUCT_SALES existent dans le projet, mais une décision approuvée ne constitue ni une donnée du Book ni une vue SAP persistée. `LEIS`, `NORM` et les descriptions françaises des trois nouveaux produits sont des valeurs de dataset de formation approuvées ; elles ne doivent pas être présentées comme des valeurs textuelles originales du Book.

### Configuration S4600

| Élément | Verdict | Preuve/limite |
|---|---|---|
| Domaine `1010/10/00` | Présent dans les clients S4615 relus | Ne prouve pas un client S4600 utilisable. |
| CDCL | **MISSING confirmé** | Scan GUI VOV8 complet 266/266, [trace](../runtime/sap_gui_responses/f7e192f0-8c62-4374-9fdd-56b6d1f4f03c.json). |
| PR00 / K007 | Types présents | LIVE : PR00/PR02 et K007/K307. Les enregistrements S4600 et leur applicabilité ne sont pas vérifiés. |
| Service condition records | **Bloqué** | LIVE `$metadata` HTTP 500 : aucun alias pour `ZSD_PRICING_CONDITIONRECORD_SRV_0001`/ABDELJ ; route directe HTTP 403/service non trouvé. |
| Usines 1010 / 1020 | **MISSING dans API_PLANT** | LIVE 404 ; audit historique complet ne trouve aucune usine de société 1010. |
| Point Z001 | **MISSING confirmé** | Scan TVST historique 20/20. Le point S4615 `1010` n'est pas un substitut. |
| Warehouse/EWM 1010 | Non disponible dans la route testée | LIVE Warehouse('1010') 404 ; ne prouve pas l'absence de tout objet EWM autrement exposé. |
| ATP 02 | **NOT_TESTED** | Le Book l'exige pour T-MS301/1010/1020 ; article et deux usines non disponibles. |
| MTO | **NOT_TESTED/BLOCKED** | T-F101, vues MRP3, stratégie 20, BOM/gamme, usine et droits PP non vérifiés. |

## B. Matrice S4600 complète et corrigée

Tous les identifiants `##` sont résolus en `01` uniquement lorsque le Book le demande. `Préexistants` désigne les objets effectivement relus, pas leur aptitude transactionnelle.

| Ex. | Objectif exact / jeu Book groupe 01 | Mapping/préexistants | Dépendance ou blocage confirmé | Test minimum après correction / critère de succès | Statut / preuve |
|---:|---|---|---|---|---|
| 1 | Utiliser le FLP sous `S4600-01`, favoris et valeurs 1010/10/00/warehouse 1010 | Aucun mapping requis | Session/catalogues participant non vérifiés | Connexion S4600-01, ouvrir les 3 apps et relire les préférences | **NOT_TESTED** — Book/historique |
| 2 | Décrire société, org. commerciale, canal, secteur, usine, magasin, point et warehouse | 1010/10/00 partiellement observé | Aucun pour la réponse conceptuelle | Comparer chaque réponse au corrigé | **VERIFIED_READY** — réponse conceptuelle vérifiée |
| 3 | Créer CDCL, T-S50A01, T-MS101×10, T-MS201×20, réf. `4-201`, J+7 | 1000000116, 60000445, 60000446 | CDCL absent ; client sans SD ; produits sans vente/taxe/usine | Créer une commande sans erreur et relire ID, postes, prix et ATP | **BLOCKED** — Book + LIVE |
| 4 | Afficher la commande de 3 et ses paiement/valeur/poids/prix/échéances/partenaires/statut | Aucun document | Dépend de 3 | Afficher le numéro créé et contrôler tous les champs | **BLOCKED** — Book |
| 5 | Créer livraison de 3 via Z001 ; quantités, magasin, statuts, stock T-MS101/1010 | Aucun document | 3 ; Z001 et usine 1010 manquent ; pas de vue usine/stock | Livraison créée et relue avec déterminations exactes | **BLOCKED** — Book + audit |
| 6 | Traiter tâches warehouse 1010, prélèvement et PGI | Aucun | 5 ; warehouse/EWM/stock non prouvés | Tâche confirmée, PGI et stock/flux relus | **BLOCKED** |
| 7 | Facturer la livraison et contrôler transfert FI | Aucun | 6 ; copy/pricing/FI | Facture et document comptable relus | **BLOCKED** |
| 8 | Encaisser en DZ, société 1010, banque 11100000, EUR, T-S50A01 | BP root seulement | 7 ; client FI et autorisation FI absents | Encaissement/lettrage et solde relus | **BLOCKED** |
| 9 | Créer T-CUS01 : BPAB, FLCU00/01, Hambourg DE, société 1010, compte 12100000, zone, DE/TTX1=1, partenaires | Aucun | Sortie d'exercice ; FI/taxe/anti-doublon à valider | Création puis readback racine, adresse, rôles, société, SD, taxe, partenaires | **BLOCKED** |
| 10 | Ajouter T-S50A01 réceptionnaire de T-CUS01 ; CDCL/T-MS201×2, réf. `5-901` | T-S50A01 root ; T-MS201 root | 9, CDCL et vues SD | Partenaire et commande relus | **BLOCKED** |
| 11 | Créer T-MS401 depuis T-MS101, texte « Article fragile ! », prix 35 EUR, commande test | T-MS101 basic only | Sortie d'exercice ; référence sans vues ; prix/service conditions bloqué | Produit, texte, condition et commande relus | **BLOCKED** |
| 12 | Fiche infos T-S50A01/T-MS101, n° K-MS-01, commande/livraison Z001 | Deux racines seulement | Client/article SD, Z001 et logistique | Description client visible dans livraison relue | **BLOCKED** |
| 13 | PR00 T-S50A01/T-MS101 : 1→53, 10→51, 20→49 EUR/PC | Type PR00 présent | Service condition records HTTP 500 ; client/article non commerciaux | Lire/écrire condition autorisée puis commande à 51 | **BLOCKED** |
| 14 | K007 T-S50A01 : 100→−1 %, 500→−2 %, 1000→−3 % | Type K007 présent | Même service bloqué ; client SD absent | Condition et remise de commande relues | **BLOCKED** |
| 15 | Expliquer contexte des données de condition | Aucun | Aucun pour le conceptuel | Réponses concordantes au corrigé | **VERIFIED_READY** — historique conceptuel |
| 16 | Proposition de postes PV, T-MS101/201×5, affectation T-S50A01 et copie commande | Racines présentes | App/contrat PV et données SD absents | Proposition et commande copiée relues | **BLOCKED** |
| 17 | CDCL incomplet T-MS201, corriger référence/poids, livrer Z001 | Racines seulement | CDCL/Z001/SD/logistique | Incomplétude puis correction et livraison démontrées | **BLOCKED** |
| 18 | Commande T-S50B01 avec T-MS101/201 ; lire usine, point, itinéraire | Produits basic ; B01 non résolu | Client B01, vues usine/vente et règles expédition | Déterminations exactes visibles dans commande | **BLOCKED** |
| 19 | T-S50A01 + T-MS101/301, réceptionnaire B01 ; dates/route/livraison | A01 root, MS101 basic | B01/MS301 non résolus, usine/Z001 | Dates/route et résultat livraison relus | **BLOCKED** |
| 20 | Lire ATP T-MS301/1010 et usine proposée chez B01 | Aucun mapping MS301/B01 | Objets/usine absents | Afficher vues ATP et proposition usine | **BLOCKED** |
| 21 | Stock/besoins T-MS301/1010 avant/après CDCL×20 | Aucun | 20, CDCL, stock/MRP | Besoin de commande visible dans couverture | **BLOCKED** |
| 22 | T-S50A01 + T-MS101/201×10 ; livraison complète/partielle | Racines seulement | Données SD/ATP absentes | Options et confirmation ATP observées | **BLOCKED** |
| 23 | ATP groupe 02 T-MS301, usines 1010/1020, commande ×95 | Aucun | Article, deux usines, stock et ATP 02 manquent | Résultat ATP multi-usines conforme au Book | **BLOCKED** |
| 24 | Expliquer ATP, livraisons partielles et ordonnancement | Aucun | Aucun pour conceptuel | Réponses comparées au corrigé | **VERIFIED_READY** — historique conceptuel |
| 25 | Création collective des livraisons groupe 01 via Z001 | Aucun document | Commandes amont + Z001/usine | Liste collective crée les livraisons attendues | **BLOCKED** |
| 26 | Tâches magasin collectives A01/B01 et PGI | Aucun | 25 + EWM/stock | Tâches/PGI/flux relus | **BLOCKED** |
| 27 | Facturation collective, simulation, ventilation, journal | Aucun | 26 + billing/FI | Documents et journal relus | **BLOCKED** |
| 28 | Demande DO → offre OF → CDCL pour A01/MS201 | Deux racines | Types/copy control S4600, SD client/article, CDCL | Flux DO/OF/commande et statuts de référence relus | **BLOCKED** |
| 29 | Expliquer traitement avant-vente | Aucun | Aucun pour conceptuel | Réponses concordantes | **VERIFIED_READY** — historique conceptuel |
| 30 | MTO T-F101/1010, stratégie 20, MRP, ordre planifié→fabrication | T-F101 non résolu | Usine/PP/BOM/gamme/MRP3 non vérifiés | Chaîne MRP et ordre de fabrication relue | **BLOCKED** |
| 31 | Vente T-D101×3 H à T-S50A01, facture liée à commande | 90000132 + 1000000116 roots | Client sans SD ; produit sans Sales Delivery/taxe ; CDCL absent | Commande service puis facture order-related relues sans livraison | **BLOCKED** |
| 32 | Commande A01/MS101, livraison Z001, PGI, facture, demande d'avoir DNC×3 | Deux racines | Logistique/FI/type DNC/copy | Chaîne complète et avoir relus | **BLOCKED** |
| 33 | Annuler l'avoir de 32 | Aucun | 32 | Document d'annulation et FI relus | **BLOCKED** |
| 34 | Retour RE A01/MS301×3, usine 1020, entrée et avoir | A01 root ; MS301 non résolu | Usine 1020 404, produit/logistique absents | Retour, réception et avoir relus | **BLOCKED** |
| 35 | CDCL incomplet A01/MS101, corriger via app puis livrer | Racines seulement | App/catalogue, CDCL et logistique | Incomplétude corrigée et livraison relue | **BLOCKED** |
| 36 | Analyse flexible entrées de commandes EUR/mois/client, graphique/export | Aucun dataset de commandes groupe 01 | App/droits/session et données non vérifiés | Filtre, total, graphique et export concordants | **NOT_TESTED** |

## 2. Vérification des objets et configurations S4615

| Objet | État LIVE | Complétude / limite |
|---|---|---|
| C615-A01 / 1000000115 | Racine, adresse 1581 Bruxelles/BE, FLCU00/FLCU01, client CUST, société 1010, zone `1010/10/00`, partenaires DO/RF/PY/RM | Compte collectif 400000, paiement 0004 ; **taxes client vides**. |
| C615-D00 / 1000000114 | Racine, adresse 1557 US, FLCU00/FLCU01, société 1010, zone `1010/10/00`, partenaires | Taxes client vides ; objet groupe 00, jamais substituer à A01. |
| P615-101 / 10000289 | FERT/M/PC/00, description FR | Aucune vente, taxe, usine, valorisation ou ML : **BASIC_ROOT_ONLY**. |
| P615-400 / 10000287 | FERT/M/PC/00 ; vente 1010/10, CB04, usine livreuse 1710 ; taxes BE/MWST/1 et US/UTXJ/1 ; usine 1710, ATP SP | Aucune A_ProductValuation, ValuationAccount ou MLAccount. C+039 a arrêté MM01 avant Save. Objet groupe 00, exclu comme modèle P101. |
| C615-B01/C01/E01/F01 | Clé littérale 404 + SearchTerm1 exact vide ; aucun mapping | **UNKNOWN**, prévus dans manifeste seulement. |
| P615-201/501/601 | Clé littérale 404 + ProductOldID exact vide ; aucun mapping | **UNKNOWN**, prévus seulement. |

### Configuration S4615

| Élément | Verdict strict |
|---|---|
| Organisation `1010/10/00` | Présente et relue sur A01/D00. |
| Usine 1010 | Absente dans API et audits T001W/T001K ; aucune aire 1010 rattachée à société 1010. |
| Point d'expédition 1010 | **Présent**, checkpoint OVXD/TVST vérifié avec adresse BE. |
| TVKWZ / TVSWZ / OVL2 | Audit historique : 1010/10 pointe seulement vers 1710 ; aucune TVSWZ vers point 1010 ; aucune chaîne OVL2 exploitable prouvée. |
| C+039 | **Confirmé sur l'extension Accounting 1/2 de 10000287/aire 1710, avant Save.** La causalité première reste `INCONCLUSIVE`; aucune correction dans cet audit. |
| ZA01 | Créé depuis CS, relu avec LF et valeurs de facturation ZF01 ; présence vérifiée, fonctionnement transactionnel non testé. |
| ZF01 | Créé depuis F2, relu ; `RFBFK=true` selon checkpoint le plus récent. |
| ZF01←LF/TAN | Header et item présents et relus ; pricing H et routines 003. **Pas fonctionnellement validé** faute de livraison/facture réelles. |
| BV | Exigence du Book et tentative de commande connue, rejetée V4/210 faute de comptabilité produit. Existence/configuration globale du type non relue dans ce passage. |
| F5 | Book exige Pro Forma for Order ; recherche de documents F5 = 0. Cela ne prouve ni présence ni absence du type/configuration. |
| WV / WVN | Valeurs exactes du Book pour contrat/maintenance ; installation/détermination non vérifiées. |
| FAZ | Valeur exacte du Book pour demande d'acompte ; installation et fonctionnement non vérifiés. |
| AM | Valeur Book du calendrier mensuel ; zéro affectation trouvée dans A_CustomerSalesArea et règles du calendrier non vérifiées. |
| PPSV | Type présent LIVE, accès PPPV ; calcul M attesté historiquement. Aucun montant/validité/contrat groupe 01. |
| CABE / YCOA | LIVE : société 1010 utilise CABE ; 1710 utilise YCOA. YCOA ne doit pas être appliqué par défaut au flux 1010. |

## C. Matrice S4615 complète et corrigée

| Ex. | Objectif exact / jeu Book groupe 01 | Mapping/préexistants | Blocage confirmé | Test minimum après correction / critère de succès | Statut / preuve |
|---:|---|---|---|---|---|
| 1 | Afficher facture issue de la commande réf. `01S4615-A3`, flux et pièce comptable, client C615-A01 | A01=1000000115 | Référence LIVE 0 commande ; aucune facture/chaîne | Retrouver ordre/livraison/facture et rapprocher FI | **BLOCKED** — Book + LIVE |
| 2 | Personnaliser session `S4615-01`, clés/listes/favori SPRO et lire interface FI-SD | Org 1010→1010 connue | Seule session ABDELJ disponible ; préférences participant non testées | Exécuter sous S4615-01 et relire préférences/favori | **PARTIAL** — navigation SPRO seulement |
| 3 | Définir ZF01/ZA01 puis ZA01 A01/P101, réf. `01S4615-A1`, LF, picking, PGI, ZF01 | ZA01/ZF01, A01, P101 root, point 1010 | P101 sans vente/usine/valorisation ; usine/stock manquants ; réf. 0 | Chaîne complète et statuts/documents relus | **PARTIAL** — config/master partiels |
| 4 | Réclamation sur facture réf. `01S4615-A4`, correction de facture | A01 existe | Référence 0 et facture source absente | Créer/identifier source puis débit/crédit et FI | **BLOCKED** |
| 5 | Vente au comptant BV D01/P615-401 réf. `01S4615-BV`; pro forma F5 A01/P615-201 réf. `01S4615-PF` | D00=1000000114 et P400=10000287, mais groupe 00 | B01/P201 absents ; P400 interdit comme substitut et C+039 ; références 0 | Tester séparément BV et F5 avec données 01 valides | **BLOCKED** |
| 6 | Tester flux de données sur livraison `01S4615-A5`; pricing type H | Copy control ZF01←LF/TAN vérifié | Réf. 0 ; aucune livraison/P101 logistique | Facturer livraison source et vérifier prix avant/après H | **PARTIAL** — configuration seule |
| 7 | Facturation via VF04, client C615-B01/P615-201, calendrier AM | Aucun mapping | Objets, trois livraisons, AM non vérifiés | VF04 avant/après AM ; regroupement mensuel conforme | **BLOCKED** |
| 8 | Analyser regroupement/ventilation pour C615-C01 | Aucun mapping | Client/livraisons absents | Simulation VF04 avec analyse des critères | **BLOCKED** |
| 9 | Ventilation de facture, ordre réf. `01S4615-A10`, C615-C01 ; routine 3 | Copy control routine 003 vérifié | Réf. 0, C01/livraisons absents | Deux résultats de facturation attendus et journal d'analyse | **PARTIAL** — configuration seule |
| 10 | Contrat WV, C615-E01, réf. Book `01S6415-PB`, P615-501, item WVN, plan 02, PPSV | PPSV présent | E01/P501/WV/WVN/plan non vérifiés ; les deux variantes de réf. = 0 | Contrat, plan, dates et facturation order-related conformes | **BLOCKED** |
| 11 | Acompte facultatif : C615-F01, réf. `01S4615-AZ`, P615-601, FAZ, paiement | Aucun mapping | Client/produit/type/paramétrage FI absents ; réf. 0 | Demande FAZ, paiement et postes client relus | **BLOCKED** |
| 12 | Détermination comptes : C615-B01, groupe 81, compte 49000000 ; nouvelle réf. `01S4615-KO` et facture antérieure `01S4615-A6` | Aucun mapping | Client/sources absents ; deux filtres exacts = 0 ; changement FI/customizing requis | Facture après réglage approuvé et compte exact relu | **BLOCKED** |
| 13 | Bloquer transfert FI de ZF01, ZA01→LF→PGI→ZF01, réf. `01S4615-BS`, puis libérer ; seconde chaîne Book `01S4615-Réf` | RFBFK=true, ZA01/ZF01/A01/P101 root | Références 0 ; P101/logistique/stock/FI absents | Facture bloquée sans FI, puis libération et pièce FI | **PARTIAL** — réglage seul |

**Totaux S4615 :** exercice métier terminé `0/13`; `PARTIAL 5/13` (2, 3, 6, 9, 13); `BLOCKED 8/13`. Les références `01S4615-A1/A3/A4/A5/A6/A10/BV/PF/BS/AZ/KO/Réf`, `01S6415-PB` et la variante `01S4615-PB` ont toutes retourné HTTP 200 avec zéro commande.

## D. Inventaire des travaux réellement effectués

### Créations/objets SAP attribuables au projet et relus

| Périmètre | Objet | Réalité vérifiée |
|---|---|---|
| S4600 | BP 1000000116 | Racine BP créée et relue ; aucune extension client. |
| S4600 | Produits 90000132, 60000445, 60000446 | Racines Basic Data créées et relues ; aucune vue commerciale/usine/valorisation. |
| S4615 | BP/client 1000000115 | Racine, adresse, rôles et extensions 1010/1010-10-00 relues ; fiscalité vide. |
| S4615 | Produit 10000289 | Basic Data 1/2 seulement, relu. |
| S4615 | Point d'expédition 1010 | Création et relecture checkpointées. |
| S4615 | ZA01 et ZF01 | Créations/configurations relues ; transport A4HK908422 cité dans les checkpoints historiques. |
| S4615 | Copy control ZF01←LF/TAN | Créé et relu ; ne prouve pas le flux. |
| S4615 | ZF01 RFBFK=true | Modifié et relu ; ne prouve pas le blocage/libération en transaction. |

`C615-D00/1000000114` et `P615-400/10000287` existent et sont relus, mais l'inventaire disponible ne permet pas d'attribuer sans réserve chaque étape de leur création au workflow courant. Ils sont donc présentés comme **objets existants**, pas comme créations nouvellement revendiquées par cet audit.

### Échecs, inspections, scripts et tests

- **Écritures échouées/ambiguës historiques :** T-D101 Sales ambigu puis vue absente ; T-MS101 Sales rejet MG/172 ; T-MS201 non tenté ; Accounting 1/2 P615-400 arrêté par C+039 avant Save ; BV Sales Order rejeté V4/210, sans commande.
- **Configurations seulement inspectées :** CDCL/VOV8, TVST Z001, T001W/T001K/TVKWZ/TVSWZ/OVL2, sociétés/plants, PR00/K007/PPSV, calendrier AM, documents F5/F8 et références Book. Inspection n'équivaut pas à installation.
- **Automatisations développées :** contrats OData/GUI, anti-doublon, readback, checkpoints, scripts de provisioning BP/Product/Sales, bridge SAP GUI à routes bornées et le script GET-only de cet audit. Un script ne prouve pas qu'une fonction est installée dans SAP.
- **Tests techniques :** tests unitaires/bridge et lectures metadata/GET historiques. Ils valident le code ou un contrat, jamais la fin d'un exercice métier.
- **Exercices réellement exécutés :** S4600 2, 15, 24, 29 uniquement comme réponses conceptuelles vérifiées ; aucun exercice transactionnel S4600 ; aucun exercice S4615 complet.
- **Rapports/checkpoints clés :** [mappings](../data/provisioning/phase5_identity_mappings.json), [checkpoint Sales S4600](../data/provisioning/s4600/product_sales_execution_checkpoint.group01.json), [progress S4600](../data/books/S4600/S4600_PROGRESS.md), [progress S4615](../books/S4615/S4615_PROGRESS.md), [copy control](../data/provisioning/s4615/vtflc_zf01_lf_tan_checkpoint.json), [RFBFK](../data/provisioning/s4615/zf01_accounting_block_checkpoint.json), [point 1010](../data/provisioning/s4615/shipping_point_1010_be_checkpoint.json), [audit C+039](sap_c039_attribution.md), [audit usine](s4615_plant_customizing_audit.md) et [inventaire des changements](sap_all_changes_inventory.md).

## E. Interventions nécessaires

| Propriétaire | Action minimale demandée | Débloque |
|---|---|---|
| SAP SD/Basis | Restaurer/importer officiellement CDCL et prouver ses déterminations/copy controls ; ne pas substituer OR | S4600 3 et chaîne aval |
| Gateway/Basis | Enregistrer l'alias de `ZSD_PRICING_CONDITIONRECORD_SRV_0001` pour ABDELJ/A4H-600 ; metadata 200 et lecture/création scoped | S4600 13–14 |
| Training Data + Tax Owner | Définir/valider les fiscalités exactes S4600 client/produits ; ne pas déduire BE/MWST/1 de P400 | Extensions S4600, MG/172 |
| SD Customer Master | Compléter T-S50A01 : adresse, FLCU00/FLCU01, A_Customer, société et zone, partenaires, fiscalité selon valeurs approuvées | Exercices S4600 commerciaux |
| MM/Product + Tax | Compléter Sales Delivery/Tax des trois produits S4600, puis vues usine uniquement après décision organisationnelle | S4600 3/31 et autres |
| Org + FI/MM | Décider/créer une usine 1010 compatible société 1010/EUR, aire de valorisation et comptes ; séparément, usine 1020 si Book maintenu | S4600 logistique/ATP et S4615 logistique |
| SD/LE | Après l'usine : TVKWZ, TVSWZ et OVL2 exacts vers point 1010 ; pour S4600, créer/restaurer Z001 séparément | Livraison/PGI |
| EWM | Confirmer warehouse 1010, intégration et tâches | S4600 6/26 |
| FI/CO Material Ledger | Diagnostiquer C+039 sur 1710 avec historique ML/SCU3/transport ; aucune modification globale improvisée | Branche BV/P615-400 uniquement |
| S4615 Data Owners | Fournir/créer B01/C01/E01/F01 et P201/P501/P601 avec valeurs Book et décisions FI/taxe | S4615 5, 7–12 |
| SD Billing | Vérifier installation BV/F5/WV/WVN/FAZ/AM et leurs déterminations ; ne pas conclure depuis les seuls codes du Book | S4615 5, 7, 10, 11 |
| Fiori/Basis | Session/rôles `S4600-01` et `S4615-01`, applications commandes, VF04/billing et analytics | Exercices UI/analytics |

## F. Corrections à appliquer au mail avant envoi

1. Remplacer « les extensions commerciales sont bloquées par les données fiscales » par une formulation différenciée : **MS101 est rejeté MG/172 ; D101 a eu un résultat ambigu mais sa vue est absente au readback ; MS201 n'a pas été tenté.**
2. Préciser que les trois produits S4600 existent **en Basic Data seulement** et que T-S50A01 existe **en BP root seulement**.
3. Dire que le copy control `ZF01←LF/TAN` et `RFBFK=true` sont **présents et relus**, mais **non validés par une chaîne métier**.
4. Présenter CABE comme plan de comptes de la société 1010 et YCOA comme celui de 1710 ; ne pas écrire « incompatibilité YCOA » comme défaut général sans préciser le mélange organisationnel 1010/1710.
5. Indiquer que C+039 a été observée exactement sur P615-400/10000287, aire 1710, avant Save, mais que sa cause initiale n'est pas attribuée avec certitude.
6. Ne pas déclarer les références Book « absentes de SAP » au sens global : dire « zéro commande retournée par filtre exact PurchaseOrderByCustomer ».
7. Ne pas présenter les exercices 3 comme exécutables maintenant. Ils sont de bons **tests d'intégration futurs après correction**, pas les prochaines actions immédiates.
8. Mentionner la coquille probable `##S6415-PB` telle qu'imprimée et l'absence de résultat pour les variantes 01S6415-PB et 01S4615-PB.

## G. Audit des affirmations du mail

| AFFIRMATION | VERDICT | PREUVE | FORMULATION RECOMMANDÉE |
|---|---|---|---|
| Le BP S4600 1000000116 existe. | **CONFIRMÉ** | GET LIVE racine 200, identité/nature/nom/SearchTerm exacts | « Le BP racine T-S50A01/1000000116 existe ; aucune extension client ni adresse n'est présente. » |
| Les produits S4600 90000132, 60000445, 60000446 existent. | **CONFIRMÉ** | GET LIVE A_Product + descriptions 200 | « Les trois racines produit existent en Basic Data uniquement ; aucune vue vente/taxe/usine/valorisation. » |
| Les extensions commerciales sont bloquées par les données fiscales. | **À NUANCER** | MS101 MG/172 ; D101 ambigu puis 0 vue ; MS201 non tenté ; taxes vides pour tous | « La fiscalité vide bloque explicitement MS101 ; D101 reste non créé après résultat ambigu et MS201 n'a pas été tenté. » |
| Le client S4600 manque de données SD. | **CONFIRMÉ** | Adresse/rôles vides ; A_Customer, société et Sales Area 404 | « T-S50A01 est BP_ROOT_ONLY et ne peut pas encore servir de client SD. » |
| Les clients S4615 1000000115 et 1000000114 existent. | **CONFIRMÉ** | GET LIVE racines, rôles, société et Sales Area 200 | « A01 et D00 existent comme clients ; leurs classifications fiscales client sont vides. » |
| Les articles S4615 10000289 et 10000287 existent. | **CONFIRMÉ** | GET LIVE racines 200 | « P101 existe en Basic Data only ; P400 a vente/usine 1710 mais aucune valorisation. » |
| C+039 concerne bien P615-400. | **CONFIRMÉ** | Checkpoint/log MM01 10000287/1710, avant Save ; vues de valorisation encore vides | « C+039 a été observée lors de l'extension Accounting 1/2 de P615-400/10000287 en 1710 ; causalité première non prouvée. » |
| Le copy control ZF01 depuis LF/TAN est présent. | **CONFIRMÉ** | Checkpoint HEADER/ITEM VERIFIED et relectures VTFLC | « Le paramétrage ZF01←LF/TAN est présent et relu ; son fonctionnement métier n'a pas été testé. » |
| CABE est le plan comptable pertinent. | **CONFIRMÉ** pour société 1010 | GET LIVE A_CompanyCode(1010)=CABE ; 1710=YCOA | « CABE est le plan de comptes de la société 1010 ; YCOA appartient à 1710 et n'est pas un substitut. » |
| Les exercices 3 de S4600 et S4615 sont les tests prioritaires. | **À NUANCER** | Les deux concentrent les chaînes principales, mais sont actuellement bloqués par master data/config/logistique | « Après correction des prérequis, les exercices 3 constituent les premiers tests d'intégration recommandés ; ils ne sont pas exécutables actuellement. » |

## Verdict final

# MAIL_À_CORRIGER

Le mail peut être envoyé après application des huit corrections de la section F, surtout la distinction entre racine et extension, la différenciation des trois tentatives PRODUCT_SALES, et la réserve « configuration présente ≠ fonctionnalité métier validée ».

