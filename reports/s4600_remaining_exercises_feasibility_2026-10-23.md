# S4600 — Faisabilité des 19 exercices restants

Date : **23/10/2026**. Environnement autorisé : **A4H / 600 / ABDELJ**, groupe00, adaptation FR10/10/1W.

## Périmètre et conclusion

Demande utilisateur : **tester seulement la faisabilité dans l'environnement, pour tous les exercices restants**. Aucune autorisation de création persistante n'est déduite de cette demande.

Le bilan combine les preuves live déjà acquises et les vérifications complémentaires du présent passage. Il ne revendique pas une nouvelle simulation intégrale de chaque exercice : certains ne peuvent pas être testés complètement sans créer leur prédécesseur ou effectuer une opération persistante. Ils restent explicitement **conditionnels ou non démontrés**.

**Aucun nouvel exercice n'est déclaré exécuté ou terminé. Aucune donnée de formation ou comptable n'a été modifiée dans ce passage.** Les simulations de facturation ont utilisé le TESTRUN déjà démontré, POSTING vide, sans COMMIT ; leurs contrôles indépendants n'ont trouvé aucune facture créée. Les quantités de stock et les statuts des livraisons contrôlées sont inchangés.

## Tableau exhaustif

| Ex. | Faisabilité constatée | Preuve / limite | Plus petite dépendance restante |
|---|---|---|---|
| **1** | Accès utilisateur confirmé ; parcours non testé | Capture utilisateur : Launchpad Fiori ouvert. Cela prouve l'accès, pas la création des favoris ni les préférences. L'outil navigateur n'est pas exposé dans la session. | Parcours Fiori et identité cible à vérifier ; aucune préférence changée. |
| **8** | Bloqué sur une donnée FI | Facture90000090, pièce9300000009, créance3720EUR vérifiées précédemment. Adaptation sans escompte retenue. Le compte banque/caisse FR10 reste non établi. | Compte de trésorerie validé par FI, puis contrat de simulation de paiement/rapprochement. Aucun paiement test réel. |
| **9** | Préparation technique partielle, création non démontrée de bout en bout | Routes BP partielles et proposition FR10 disponibles. Nouveau lookup ciblé T-CUS00 : zéro correspondance. Les choix de numérotation, société/compte collectif et fiscalité ne sont pas des valeurs à inventer. | Valider les valeurs de la proposition et le contrat complet. Ne pas assimiler une proposition à une création validée. |
| **10** | Conditionnel, non testé sur sa cible | L'exercice exige le client du9 et l'ajout d'un réceptionnaire, puis une commande. La cible n'est pas créée/mappée. | Client du9. Les comportements partenaires déjà observés ailleurs ne suffisent pas à clôturer ce test cible. |
| **11** | Faisabilité complète non démontrée | Nouveau lookup exact produit/ancien ID T-MS400 : zéro correspondance. La création de vues de base est prouvée historiquement, mais la copie complète des vues, textes, fiscalité et valorisation pour cette cible ne l'est pas. | Modèle et valeurs vérifiés, puis contrat complet de préparation sans sauvegarde si disponible. Aucune copie réelle d'article. |
| **13** | Conditionnel | Types PR00/PR02 présents, relus. Dans le plan d'isolation retenu, le prix doit porter sur l'objet participant, non disponible. Le type de condition présent ne prouve pas sa détermination effective dans une commande. | Objet participant du11 et vérification de l'accès/détermination ; aucun prix commun modifié. |
| **14** | Conditionnel | K007 existe et a été relu. Le barème du book est connu, mais le plan retenu exige des objets participants isolés pour ne pas affecter le client partagé. | Cible participant du9 et contrat du barème. Aucun enregistrement de remise créé pour tester. |
| **17** | Écart pédagogique démontré | Commande158 corrigée et complète. Le paramétrage réel ne bloque pas la livraison pour les deux champs manquants testés ; le refus attendu par le book n'est pas reproduit. | Accepter une adaptation pédagogique ou définir une solution isolée ; aucun customizing partagé modifié. |
| **20** | Lecture faisable, résultats différents du book | Les données et le contrôle sont accessibles. ATP de10000284/FR10 =01, et non02. | Documenter les réponses de l'environnement ou accepter une adaptation ; aucun changement d'ATP nécessaire pour simplement constater ces données. |
| **23** | Scénario du book bloqué en l'état | Lecture actuelle : ATP01, stock3170. BAPI de disponibilité en lecture seule :95 demandées et95 confirmées au30/10. Usine1020 absente. Le test BAPI ne vaut pas validation du périmètre complet de contrôle SD. | Deux usines adaptées et scénario isolé de pénurie ; ne pas consommer le stock ni changer l'ATP partagé pour un test. |
| **26** | Précontrôles favorables ; sortie comptable non simulée | Livraisons80000088–90 présentes ; stocks suffisants enFR10/0001. Fonctions PickAllItems et PostGoodsIssue présentes et routes historiquement exécutées sur80000085. Les livraisons nouvelles restent non prélevées, magasin vide. | Préparation persistante et sortie non effectuées, conformément à la demande. Aucun paramètre TESTRUN sur les fonctions OData observées ; aucune garantie nouvelle de comptabilisation pour ces cibles. |
| **27** | Simulation réellement exécutée, refus sur prérequis | Un seul TESTRUN collectif des neuf postes de80000088–90 : **VF066**, absence de sortie de marchandises. Après test : aucune facture pour ces références. | Sorties du26. Ce résultat n'est pas un défaut de facturation démontré et ne valide pas encore la ventilation ni la comptabilité collective. |
| **30** | Bloqué sur le mapping produit, en attente admin | Recherches exactes et famille T-F1 : aucun mapping. Recherche FR10 stratégie20 ou approvisionnementE : zéro résultat pour ce filtre. Aucun substitut choisi. | Numéro SAP du produit fabriqué correspondant àT-F100. Nomenclature et gamme ne peuvent pas être vérifiées sans identité. Aucun MRP. |
| **31** | Brouillon partiel validé, complétude bloquée | PrixPR00 etZPR0 et posteTAD déjà vérifiés. Nouveau lookup : pas de vue produit-usine90000133/FR10, ni commande8-600 créée. Les dates logistiques manquantes empêchent une clôture complète. | Extension article-usine avec contrat/valeurs vérifiés ; ne pas créer de valorisation pour tester. |
| **32** | Commande/livraison préparées ; suite conditionnelle | Commande163/livraison80000091 déjà créées avant ce passage. Un seul TESTRUN de leur facture : **VF066**, pas de sortie. Aucune facture persistée. La demande d'avoir et l'avoir ne sont pas encore testables sur leur prédécesseur requis. | Sortie de80000091 puis facture de référence ; pas de création de prérequis au titre de cet audit. |
| **33** | Contrat présent, test complet non permis sans écriture/prédécesseur | Fonction API **Cancel** présente, méthodePOST, paramètreBillingDocument. Aucun mode test observé sur cette fonction. L'avoir de32 n'existe pas encore. | Avoir de32. Aucune annulation de facture existante pour démontrer la faisabilité. |
| **34** | **Préparation en brouillon validée surFR10** | RE, client1000000112,10000284×3, motif103, posteREN, échéanceDN, division/pointFR10,360EUR nets ; SAP « Le document est complet ». Brouillon quitté avec Non à la sauvegarde, relecture sans retour créé. | Livraison de retour, réception et avoir non validés. La préparation positive ne prouve pas le flux complet. |
| **35** | Parcours Fiori non démontré | L'accès utilisateur au Launchpad est confirmé, mais pas le catalogue, les droits ni le parcours Analyse et résolution. Aucun nouvel outil navigateur disponible. | Parcours Fiori pilotable/observé. Pas de création volontaire d'une commande incomplète pour contourner cette limite. |
| **36** | Parcours analytique Fiori non démontré | Données de vente disponibles ; accès Launchpad confirmé par l'utilisateur. Application analytique, navigation, graphique et export du book non testés. | Accès et parcours de l'application analytique. Un agrégat API ne remplace pas la validation de l'interface demandée. |

## Nouveaux contrôles de ce passage

### Livraisons et stock

Les quatre livraisons80000088–91 ont été relues (26/27 et préparation32). Toutes restent avec statuts de prélèvement et de mouvement **A**, sans facture liée.

| Article | Besoin total des quatre livraisons | Stock libre observé FR10/0001 |
|---|---:|---:|
| 10000282 | 32 | 3 699 |
| 10000283 | 23 | 3 235 |
| 10000284 | 21 | 3 170 |

Ce contrôle porte sur les quantités physiques observées, pas sur une promesse de confirmation ATP, l'absence de toute concurrence, ou la réussite d'un posting FI. Les magasins des postes restent vides ; aucune correction n'a été appliquée.

### Contrats sans mode test

Les métadonnées installées des fonctions **PickAllItems**, **PostGoodsIssue** et **Cancel** montrent des appels POST, sans paramètre de simulation observé. Elles n'ont donc pas été invoquées. Leur présence ne justifie pas un appel réel pour « tester ».

### Simulations de facturation

`BAPI_BILLINGDOC_CREATEMULTIPLE` a été appelé uniquement avec **TESTRUN=X**, **POSTING vide**, sans `BAPI_TRANSACTION_COMMIT` :

- exercice27 : neuf postes des trois livraisons, une tentative, trois retoursVF066 ;
- exercice32 : un poste de80000091, une tentative, un retourVF066 ;
- zéro succès de création, aucune facture trouvée après les deux simulations ;
- contrôles indépendants finaux : stocks et statuts inchangés, absence de factures confirmée.

La simulation ne constitue pas une preuve de future comptabilisation FI ni d'une création d'avoir. Aucun essai automatique n'a suivi les refus. Les branches indépendantes ont été poursuivies sans contourner le prérequis de sortie.

## Interprétation à retenir

« Faisable en brouillon », « précontrôles favorables », « route disponible », « dépendance manquante » et « exercice exécuté » sont des états différents. **Aucune conclusion “tout est faisable” n'est justifiée.** Le résultat le plus favorable sans création nouvelle est le brouillon34 ; le26 a des précontrôles favorables mais sa sortie ne peut pas être garantie sans un test non persistant supplémentaire démontré ou une exécution séparément autorisée.

Le mode **faisabilité uniquement** reste la consigne courante : ne pas réutiliser les anciennes demandes d'autorisation pour lancer les écritures restantes. Les dossiers en attente admin, notamment30, restent inchangés.

## Preuves et vérification

Nouvelles preuves :

- `runtime/sap_reads/s4600_remaining_feasibility_readonly_2026-10-23.json` : lectures, métadonnées, stocks, prérequis et documents.
- `runtime/sap_reads/s4600_ex27_32_billing_simulation_2026-10-23.json` : tentatives et retours TESTRUN, lectures avant/après.
- `runtime/sap_reads/s4600_feasibility_reconciliation_2026-10-23.json` : **VERIFIED_UNCHANGED** sur les états contrôlés.
- `tests/test_s4600_feasibility_simulation_guards.py` : quatre tests hors ligne PASS ; aucun appel live dans ces tests.

Preuves antérieures réutilisées sans redécouverte inutile : rapports8/9/11/17/20/23/30/31 et `reports/s4600_ex34_fr10_draft_validation_2026-10-23.md`. Les conclusions historiques sont distinguées des nouvelles lectures. La confirmation de l'accès Fiori repose sur la capture utilisateur, pas sur un test automatisé des applications.
