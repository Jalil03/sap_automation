# Rapport global des exercices S4600

**Situation au 23 octobre 2026**  
**Environnement : A4H / mandant 600 / utilisateur ABDELJ**  
**Groupe : 00 — domaine commercial FR10 / 10 / 1W**

## 1 Synthèse

Nous avons terminé et vérifié **17 exercices sur 36** : **13 exercices pratiques**, selon l'adaptation FR10 retenue, et **4 exercices théoriques**. Les **19 autres ne sont pas terminés**. Parmi eux, certains ont un contrôle de faisabilité positif mais limité ; d'autres restent bloqués par des données, un prédécesseur ou un parcours Fiori non vérifié.

| Classement principal | Exercices | Nombre |
|---|---|---:|
| Terminés et vérifiés | **2, 3, 4, 5, 6, 7, 12, 15, 16, 18, 19, 21, 22, 24, 25, 28, 29** | **17** |
| Faisabilité partielle vérifiée, sans clôture | **20, 26, 34** | **3** |
| Blocage de données, de contrat ou écart au book | **8, 9, 11, 17, 23, 30, 31** | **7** |
| Dépendance à un exercice ou document précédent | **10, 13, 14, 27, 32, 33** | **6** |
| Parcours Fiori non vérifiés | **1, 35, 36** | **3** |
| **Total** | **Chaque exercice figure une seule fois dans ce classement** | **36** |

**Distinction essentielle :** un brouillon accepté, une API disponible ou un stock suffisant ne prouvent pas que tout l'exercice est exécutable. Les exercices 17, 31 et 32 comportent aussi du travail déjà réalisé, détaillé ci-dessous, mais leurs blocages empêchent leur clôture.

La consigne courante est **faisabilité uniquement** : pas de nouveau document, de modification de données, de mouvement de stock ou d'écriture comptable pour poursuivre les tests. Les créations historiques restent recensées comme telles ; elles n'ont pas été répétées pendant le dernier audit.

## 2 Exercices terminés et vérifiés

Les adaptations communes sont FR10 à la place de l'organisation/usine 1010, secteur commercial 1W et prélèvement directement dans la livraison à la place du parcours EWM. Une validation fonctionnelle par API ou SAP GUI n'est pas présentée comme une validation de tous les écrans Fiori du book.

| Ex. | Sujet | Résultat et preuve principale |
|---|---|---|
| **2** | Structures organisationnelles | Réponses théoriques rédigées et comparées aux solutions du book. Pas une validation de paramétrage SAP. |
| **3** | Création de commande client | Commande **154**, client **1000000112**, référence **4-200** ; articles **10000282 × 10** et **10000283 × 20** ; net **3 100 EUR**. Création et relecture conformes. |
| **4** | Affichage de commande | Lecture de la commande **154** : conditions de paiement, montant, poids, livraison et division vérifiés. |
| **5** | Création de livraison | Livraison **80000085** créée depuis **154** ; postes et quantités relus, magasin **0001** renseigné et prélèvement vérifié. |
| **6** | Traitement des marchandises | Sur **80000085**, prélèvement contrôlé puis sortie de marchandises effectuée et relue. Mouvement **601**, document matériel **4900000263**, exercice **2026**. Parcours adapté sans EWM. |
| **7** | Facturation | Facture **90000090**, pièce comptable **9300000009**, société FR10, exercice 2026 ; **3 100 EUR nets**, **620 EUR de TVA**, **3 720 EUR bruts**. Transfert FI vérifié. |
| **12** | Fiche client-article | Fiche **K-MS-00** ; résolution vers **10000282**, désignation **Phare Premium**. Commande **159**, livraison **80000087**, quantité **10** ; désignation reprise et relue. |
| **15** | Données de base de condition | Questions théoriques traitées et comparées aux solutions du book. |
| **16** | Proposition de postes | Proposition **50000001** : **10000282 × 5**, **10000283 × 5**. Affectation au client vérifiée et copie dans la commande **160**, référence **00-Proposition**, net **1 150 EUR**. |
| **18** | Détermination automatique des données | Commande **156**, référence **6-100**, créée puis relue indépendamment ; données attendues contrôlées. |
| **19** | Ordonnancement de l'expédition et du transport | Commande **157**, référence **6-400**, net **870 EUR** ; deux réceptionnaires distincts et éligibilité à livraison aux dates testées vérifiés. Les livraisons n'ont été créées qu'ensuite, dans le 25. |
| **21** | Transfert des besoins | Commande **161**, référence **7-600**, **10000284 × 20**. Nouveau besoin MRP de **20** au **27/10/2026**, correspondant à la mise à disposition ; livraison demandée au **29/10/2026**. |
| **22** | Livraisons complètes ou partielles | Commande **162**, référence **7-700**, **10000282 × 10** et **10000283 × 10**. Livraison complète non imposée et code de livraison partielle vide aux postes, relus par API/RFC. |
| **24** | Fonctions du contrôle de disponibilité | Réponses théoriques traitées et comparées aux solutions du book. |
| **25** | Création collective de livraisons | Un traitement collectif limité à nos commandes a créé **80000088, 80000089 et 80000090**. Neuf postes relus, sans référence étrangère au lot. Pas de sortie de marchandises sur ces trois livraisons. |
| **28** | Avant-vente | Demande **10000104** → offre **20000103** → commande **155**, référence **8-900**. Documents et liens relus indépendamment. |
| **29** | Traitement des documents d'avant-vente | Réponses théoriques traitées et comparées aux solutions du book. |

**Les quatre exercices théoriques sont 2, 15, 24 et 29.** Les autres lignes de cette section correspondent à des contrôles ou exécutions pratiques avec des preuves SAP.

## 3 Faisabilité partielle vérifiée

Ces exercices ont un résultat favorable sur une partie du scénario. Ils ne sont pas pour autant terminés ni intégralement validés.

| Ex. | Ce qui a été vérifié | Limite restante |
|---|---|---|
| **20** | Les données de contrôle de disponibilité sont accessibles. L'article **10000284 / FR10** porte le groupe ATP **01**. | Le book attend **02**. La lecture est faisable, mais les réponses/scénarios doivent tenir compte de cet écart. Aucun groupe ATP n'a été modifié pour ce contrôle. |
| **26** | Livraisons **80000088–80000090** existantes, quantités couvertes par les stocks physiques. Fonctions **PickAllItems** et **PostGoodsIssue** présentes ; routes déjà éprouvées historiquement sur **80000085**. | Les nouvelles livraisons ne sont pas prélevées et leur magasin reste vide. Aucun mode simulation n'est démontré sur ces fonctions OData ; la sortie comptable de ces cibles n'a donc pas été testée. Sans EWM, seule l'adaptation FR10 est envisagée. |
| **34** | Brouillon de retour **RE**, client **1000000112**, article **10000284 × 3**, motif **103 — Écart quantité**. SAP détermine division et point **FR10**, poste **REN**, échéance **DN**, net **360 EUR**, et indique **Le document est complet**. | Brouillon abandonné sans sauvegarde, absence de retour confirmé par API. Livraison de retour, entrée de stock et avoir non validés. Cela prouve la préparation du retour sur FR10, pas le flux complet. |

### Stocks contrôlés pour les exercices 26 et 32

| Article | Besoin des quatre livraisons 80000088 à 80000091 | Stock libre observé en FR10 / 0001 |
|---|---:|---:|
| **10000282** | **32** | **3 699** |
| **10000283** | **23** | **3 235** |
| **10000284** | **21** | **3 170** |

Le stock physique suffisant ne constitue pas une garantie de confirmation ATP ou de comptabilisation FI. Les quantités et les statuts contrôlés sont restés inchangés après les simulations.

## 4 Blocages directs et écarts au book

| Ex. | Travail déjà réalisé | Blocage exact | Action minimale pour avancer |
|---|---|---|---|
| **8 — Encaissement** | Facture et créance de **3 720 EUR** vérifiées ; adaptation sans escompte acceptée. | Aucun compte banque/caisse FR10 approprié n'est établi. Le compte du book ne se transpose pas automatiquement au plan comptable FR10. | Obtenir du responsable FI le compte et, si nécessaire, les coordonnées de banque société ; relire ces valeurs avant toute simulation ou comptabilisation. |
| **9 — Client** | Recherche anti-doublon et proposition de valeurs FR10 préparées ; routes API partielles connues. | Numérotation, valeurs FI/fiscales et contrat complet de création restent à valider. La cible **T-CUS00** n'est pas créée/mappée. | Valider la proposition champ par champ et démontrer le contrat complet ; ne pas copier automatiquement le client de référence. |
| **11 — Article** | Recherche ciblée de **T-MS400** et examen d'un modèle technique. | Pas de cible exacte trouvée ; équivalence du modèle, vues, texte ADV, fiscalité/valorisation et contrat de copie complet non validés. | Valider un modèle et les valeurs, puis contrôler la préparation complète sans sauvegarde si la route le permet. |
| **17 — Documents incomplets** | Commande **158** créée incomplète puis corrigée : référence **3-900**, poids net **20 KG**. Document annoncé complet. | La livraison **80000086** a pu être créée avant correction. Les groupes de statut actuels des champs testés ne bloquent pas la livraison ; le refus attendu dans le book n'est pas reproduit. Écart supplémentaire : poids brut **14 KG**, inférieur au poids net demandé de **20 KG**. | Documenter l'écart pédagogique ou définir une solution isolée. Ne pas modifier globalement les procédures partagées pour cet exercice. |
| **23 — Contrôles de disponibilité** | Article et stock lus ; BAPI de disponibilité : **95 demandées, 95 confirmées au 30/10/2026**. | ATP **01** au lieu de **02**, pas de pénurie dans ce test, usine **1020 absente**. Le book demande une pénurie puis une comparaison entre deux usines. | Définir un scénario isolé et deux usines vérifiées, ou accepter une adaptation partielle. Ne pas consommer le stock partagé pour fabriquer une pénurie. |
| **30 — Fabrication sur commande** | Recherche exacte et famille **T-F1**, puis recherche de candidats FR10 en stratégie **20** ou approvisionnement **E**. | Aucun mapping vérifié de **T-F100** ; aucun résultat sous les filtres complémentaires. Impossible de rattacher une nomenclature et une gamme à une cible identifiée. | **En attente admin** : fournir le numéro SAP du produit de fabrication prévu. Aucune création de produit de remplacement ni aucun MRP. |
| **31 — Produit de service** | Service **90000133**, prix **PR00/ZPR0** et poste **TAD** vérifiés ; brouillon à **450 EUR** pour **3 H**. | Vue article-usine FR10 absente et données/dates logistiques manquantes. La tentative de sauvegarde complète n'a pas abouti ; aucune commande **8-600** créée. | Démontrer et approuver l'extension article-usine et ses valeurs nécessaires. Pas de création de valorisation pour tester. |

**Limite de recherche pour le 30 :** les résultats nuls ne prouvent pas qu'aucun produit de fabrication n'existe dans tout SAP. Ils prouvent qu'aucune correspondance exploitable n'a été identifiée dans les sources et filtres contrôlés.

## 5 Exercices en attente de leurs prédécesseurs

| Ex. | Vérification réalisée | Dépendance ou résultat bloquant |
|---|---|---|
| **10 — Données partenaire** | Exigences lues ; comportement des partenaires observé dans d'autres scénarios, pas sur cette cible. | Attend le client participant du **9** pour ajouter un réceptionnaire et créer sa commande. |
| **13 — Prix de vente** | Type **PR00** et séquence **PR02** présents. | Le plan validé réserve les prix aux objets participants isolés, notamment l'article du **11**. L'existence du type de condition ne prouve pas sa détermination dans la commande cible. |
| **14 — Remise** | Type **K007** présent et barème du book connu. | Attend une cible participant isolée, notamment le client du **9**, et la vérification du contrat de barème. Aucune remise n'a été appliquée au client partagé pour tester. |
| **27 — Facturation collective** | **Simulation réellement exécutée**, une tentative sur les neuf postes des livraisons **80000088–80000090**. | Refus **VF066 — aucune sortie de marchandises enregistrée**. Attend le **26**. Aucune facture créée ; ventilation et comptabilisation collective non validées. |
| **32 — Demande d'avoir** | Commande **163**, référence **9-100**, et livraison **80000091** déjà créées ; net commande **750 EUR**. Simulation de facture effectuée une fois. | Même refus **VF066** : sortie de marchandises absente. Sans facture source, demande d'avoir puis avoir ne sont pas encore validés. **Exercice partiellement exécuté**, non terminé. |
| **33 — Annulation de facture** | Fonction API **Cancel** disponible, mais sans mode test observé. | Attend l'avoir de l'exercice **32**. Aucune facture existante n'a été annulée pour tester ; la fonction disponible n'est pas une preuve du flux comptable complet. |

Les simulations des 27 et 32 ont utilisé **TESTRUN = X**, **POSTING vide**, sans **COMMIT**. La relecture indépendante a confirmé l'absence de factures créées. **VF066 identifie un prédécesseur manquant ; ce n'est pas la preuve d'un défaut du système de facturation.**

## 6 Parcours Fiori non encore vérifiés

L'utilisateur a fourni une capture montrant son **accès effectif au Launchpad Fiori**. Il ne faut donc pas présenter cette situation comme une absence d'accès à Fiori. La limite concerne la validation des applications et des actions précises du book.

| Ex. | Ce qui est établi | Ce qui reste à vérifier |
|---|---|---|
| **1 — Navigation et personnalisation** | Launchpad accessible ; exercice laissé de côté à la demande de l'utilisateur. | Compte cible, création du groupe de favoris, ajout des trois applications et valeurs personnelles adaptées. Aucune personnalisation n'est déclarée exécutée. |
| **35 — Analyse et résolution des commandes** | Données de vente disponibles et accès général Fiori confirmé. | Application, catalogue/droits et parcours complet d'identification/résolution d'une commande incomplète. Ne pas créer une commande incomplète uniquement pour contourner l'absence de validation de l'interface. |
| **36 — Analyse des ventes** | Données commerciales disponibles et accès général Fiori confirmé. | Application analytique, filtres, navigation, graphique et export demandés. Une lecture ou un calcul API ne remplace pas le parcours Fiori. |

Le pilotage navigateur requis n'est pas disponible dans la session d'automatisation actuelle. Un parcours manuel guidé reste une possibilité ; l'indisponibilité de cet outil n'est pas un blocage SAP démontré.

## 7 Points à transmettre à l administrateur ou au formateur

1. **Exercice 30** : communiquer le produit SAP correspondant à **T-F100**, avec ses données de fabrication prévues sur FR10.
2. **Exercice 8** : communiquer le compte de trésorerie FR10 et les données de banque société nécessaires au paiement/rapprochement.
3. **Exercice 9** : valider la numérotation du nouveau client et les valeurs FI/fiscales de la proposition FR10.
4. **Exercice 11** : valider le modèle article et les données nécessaires à la création complète des vues demandées.
5. **Exercice 31** : définir les données de la vue article-usine du service et les éventuelles exigences comptables, sans modification globale de valorisation.
6. **Exercices 17, 20 et 23** : décider quelles différences par rapport au book sont acceptées et lesquelles doivent être reproduites dans un scénario isolé.

Ces points sont des demandes d'information ou de décision. **Le présent rapport n'autorise aucune modification de paramétrage, de fiscalité, de ledger, de devises ou de Material Ledger.**

## 8 Principaux documents déjà présents

| Scénario | Documents |
|---|---|
| Cycle initial des exercices 3 à 7 | Commande **154** → livraison **80000085** → document matériel **4900000263** → facture **90000090** → pièce FI **9300000009**. |
| Avant-vente 28 | Demande **10000104** → offre **20000103** → commande **155**. |
| Détermination et ordonnancement 18–19 | Commandes **156** et **157**. |
| Incomplétude 17 | Commande **158**, livraison **80000086** sans sortie de marchandises. |
| Client-article 12 | Fiche **K-MS-00**, commande **159**, livraison **80000087** sans sortie. |
| Proposition 16 | Proposition **50000001**, commande **160**. |
| Besoins et livraisons partielles 21–22 | Commandes **161** et **162**. |
| Création collective 25 | Livraisons **80000088, 80000089, 80000090**, non prélevées et sans sortie. |
| Préparation de l'avoir 32 | Commande **163**, livraison **80000091**, sans sortie ni facture. |

Le brouillon de retour 34 n'a produit **aucun numéro de retour**. Les créations historiques ne sont pas annulées ou rejouées pendant les contrôles de faisabilité.

## 9 Sources et portée des vérifications

Les preuves d'exécution et de faisabilité sont conservées dans les rapports et journaux du projet. Les sources principales de cette synthèse sont :

- [Exercices conceptuels 2 15 24 29](s4600_conceptual_exercises_evidence.md).
- [Affichage de commande 4](s4600_ex4_execution_report_2026-10-22.md), [marchandises 6](s4600_ex6_pgi_execution_report_2026-10-22.md), [facturation 7](s4600_ex7_billing_execution_report_2026-10-22.md).
- [Lot 12 16 21 22 25 et préparation 32](s4600_remaining_batch_execution_2026-10-22.md).
- [Exercices 17 18 19 20 et 36](s4600_ex17_18_19_20_36_progress_2026-10-22.md).
- [Avant vente 28](s4600_ex28_execution_report_final_2026-10-21.md).
- [Préparation 8](s4600_ex8_payment_readiness_report_2026-10-22.md), [préparation 9](s4600_ex9_group00_readiness_report_2026-10-22.md), [audit 9 et 11](s4600_group00_ex9_ex11_readonly_audit_2026-10-21.md).
- [Service 31](s4600_ex31_zpr0_execution_report_2026-10-22.md).
- [Recherche fabrication 30](s4600_ex30_mto_identity_check_2026-10-23.md).
- [Brouillon de retour 34](s4600_ex34_fr10_draft_validation_2026-10-23.md).
- [Bilan des 19 faisabilités](s4600_remaining_exercises_feasibility_2026-10-23.md).
- [Réconciliation indépendante après simulations](../runtime/sap_reads/s4600_feasibility_reconciliation_2026-10-23.json).

**Conclusion : 17 exercices terminés ; 19 non terminés avec un état documenté.** Les contrôles positifs limités sont conservés sans les transformer en validations intégrales. La poursuite reste limitée aux lectures et aux simulations non persistantes démontrées, selon la consigne actuelle.
