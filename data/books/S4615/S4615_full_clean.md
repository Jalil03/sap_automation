# S4615 - Facturation dans SAP S/4HANA Sales

> Conversion Markdown nettoyée du support SAP fourni. Les en-têtes/pieds de page répétitifs et mentions de copyright ont été retirés. Les numéros de page PDF sont conservés pour traçabilité.


## PDF page 1

S4615
Facturation dans SAP S/4HANA
Sales
.
.
SUPPORT DE COURS DE L'ANIMATEUR
COURS AVEC INSTRUCTEUR
.
Version du cours : 12
Durée du cours : 2 Jours
Numéro d'article : 50151550


## PDF page 2

Copyrights et marques SAP
© 2019 SAP SE ou société affiliée SAP. Tous droits réservés.
Toute reproduction ou communication de la présente publication, même partielle,
par quelque procédé et à quelque fin que ce soit, est interdite sans l'autorisation
expresse et préalable de SAP SE ou d'une société affiliée SAP.
Les informations contenues dans le présent document peuvent être modifiées sans
préavis. Certains logiciels commercialisés par SAP SE et ses distributeurs
contiennent des composants logiciels qui sont la propriété d'éditeurs tiers. Les
spécifications des produits peuvent varier d’un pays à l’autre.
Les informations du présent document sont fournies par SAP SE ou par une société
affiliée SAP uniquement à titre informatif, sans engagement ni garantie d'aucune
sorte. SAP SE ou ses sociétés affiliées ne pourront en aucun cas être tenues
responsables des erreurs ou omissions relatives à ces informations. Les seules
garanties fournies pour les produits et les services de SAP ou d'une société affiliée
SAP sont celles énoncées expressément à titre de garantie accompagnant, le cas
échéant, lesdits produits et services. Aucune des informations contenues dans le
présent document ne saurait constituer une garantie supplémentaire.
En particulier, SAP SE ou ses sociétés affiliées ne sont en aucun cas tenues de se
livrer aux activités citées dans le présent document ou toute autre présentation, ni de
développer ou de mettre sur le marché quelque fonctionnalité mentionnée dans les
présentes. Le présent document ou toute présentation liée, ainsi que la stratégie et
les futurs développements, produits, orientations de plate-forme et fonctionnalités
éventuels de SAP SE ou de ses sociétés affiliées peuvent être modifiés par SAP ou
par ses sociétés affiliées à tout moment et pour quelque raison que ce soit, sans
préavis. Les informations contenues dans le présent document ne constituent en
aucun cas un engagement, une promesse ou une obligation juridique de livrer un
quelconque matériel, code ou fonctionnalité. Toutes les prévisions mentionnées sont
soumises à certains risques et comportent une part d'incertitude pouvant entraîner
des résultats substantiellement différents des attentes. Il est recommandé au lecteur
de ne pas placer une confiance exagérée dans lesdites prévisions et de ne pas
prendre de décision d'achat en fonction de ces dernières.
SAP et tous les autres produits et services SAP mentionnés dans le présent
document, ainsi que leurs logos respectifs, sont des marques commerciales ou des
marques déposées de SAP SE (ou d'une société affiliée SAP) en Allemagne ainsi que
dans d'autres pays. Tous les autres noms de produits et de services mentionnés sont
des marques commerciales ou des marques déposées de leurs entreprises
respectives. Consultez http://global12.sap.com/corporate-en/legal/copyright/
index.epx pour obtenir des informations complémentaires sur les marques déposées.


## PDF page 3

Conventions typographiques
Le français de France est le standard utilisé dans ce manuel.
Les conventions typographiques décrites ci-après sont également utilisées.
Ces informations apparaissent dans la présentation de l'animateur.
Démonstration
Procédure
Avertissement ou Attention
Astuce
Informations connexes ou supplémentaires
Invitation à la discussion
Contrôle d'interface utilisateur
Exemple de texte
Titre de fenêtre
Exemple de texte


## PDF page 5

Sommaire :
Vue d'ensemble du cours
Chapitre 1: Documents de facturation dans l'Administration des ventes
Sujet: Intégration de documents de facturation dans
l'Administration des ventes
50 Minutes
Exercice 1: Afficher un document de facturation
20 Minutes
Chapitre 2: Entités organisationnelles
Sujet: Définition d'entités organisationnelles
30 Minutes
Exercice 2: Personnaliser des aspects des entités
organisationnelles
10 Minutes
Chapitre 3: Processus de facturation
Sujet: Contrôle du processus de facturation
50 Minutes
Exercice 3: Définition d'un nouveau type de document de
facturation
20 Minutes
Chapitre 4: Types de documents de facturation spéciaux
Sujet: Création de documents de facturation dans la gestion des
réclamations
55 Minutes
Exercice 4: Créer des documents de facturation dans la gestion
des réclamations
15 Minutes
Sujet: Création de factures pro forma et de vente au comptant
30 Minutes
Exercice 5: Créer une facture de vente au comptant et une
facture pro forma
10 Minutes
Chapitre 5: Flux de données
Sujet: Configuration du flux de données pour les documents de
facturation
70 Minutes
Exercice 6: Configuration du flux de données pour les
documents de facturation
25 Minutes
Chapitre 6: Création de documents de facturation
Sujet: Création de documents de facturation de différentes façons
50 Minutes
Exercice 7: Créer des documents de facturation de différentes
façons
30 Minutes


## PDF page 6

Chapitre 7: Méthodes de facturation
Sujet: Analyse du regroupement et de la ventilation de factures
60 Minutes
Exercice 8: Analyser le regroupement et la ventilation de
factures
10 Minutes
Exercice 9: Interprétation des raisons incitant à ventiler une
facture
10 Minutes
Sujet: Définition de relevés de factures
20 Minutes
Sujet: Facturation convergente omnicanal
40 Minutes
Chapitre 8: Processus de gestion spécifiques
Sujet: Définir des calendriers de facturation
45 Minutes
Exercice 10: Définir des calendriers de facturation
25 Minutes
Sujet: Traitement des acomptes
50 Minutes
Exercice 11: Traitement des acomptes (exercice facultatif)
25 Minutes
Sujet: Traitement des versements échelonnés
10 Minutes
Chapitre 9: Détermination des comptes
Sujet: Définition de la détermination des comptes
70 Minutes
Exercice 12: Définir la détermination des comptes
30 Minutes
Chapitre
10:
Interface entre l'Administration des ventes et la Comptabilité
financière
Sujet: Ajustement de l'interface entre l'Administration des ventes et
la Comptabilité financière
70 Minutes
Exercice 13: Ajustement de l'interface entre l'Administration des
ventes et la Comptabilité financière
20 Minutes
Chapitre 11:Annexe
Sujet: Informations supplémentaires sur la gestion des messages,
les informations techniques et les principes comptables de base
10 Minutes


## PDF page 7

Vue d'ensemble du cours
PUBLIC CONCERNÉ
Ce cours s'adresse aux participants suivants :
●
Consultant applicatif
●
Responsable de processus de gestion/Responsable d'équipe/Utilisateur de référence


## PDF page 9

CHAPITRE 1
Documents de facturation dans
l'Administration des ventes
Sujet 1
Intégration de documents de facturation dans l'Administration des ventes
Exercice 1: Afficher un document de facturation
OBJECTIFS DU CHAPITRE
●
Intégrer des documents de facturation dans le processus de l'Administration des ventes


## PDF page 10

Chapitre 1
Sujet 1
Intégration de documents de facturation dans
l'Administration des ventes
VUE D'ENSEMBLE DU SUJET
Ce sujet vous offre une vue d'ensemble des documents de facturation. Il explique la structure
de ces documents et la façon d'accéder aux données qu'ils contiennent.
Give participants a rough summary to remind them of the Sales and Distribution (SD)
process.
Exemple de gestion
Après enregistrement et livraison des commandes clients, vous voulez maintenant facturer à
vos clients les services fournis. Pour cette raison, vous devez disposer des connaissances
suivantes :
●
connaître l'intégration du document de facturation à la chaîne de processus de
l'Administration des ventes ;
●
connaître le transfert des données de l'Administration des ventes vers la Comptabilité
financière ;
●
connaître la structure d'un document de facturation ;
●
connaître l'accès aux différentes informations contenues dans le document de facturation.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Intégrer des documents de facturation dans le processus de l'Administration des ventes
Intégration des documents de facturation


## PDF page 11

Figure 1: Intégration des documents de facturation
Perform a system demonstration of the SD process with the following data:
●
Customer: 2140
●
Purchase order number: 4711
●
Material: M-06 (10 pieces)
●
Material: M-07 (10 pieces)
●
Material: M-08 (10 pieces)
Le document de facturation correspond à la dernière fonction de la chaîne de processus de
l'Administration des ventes.
Il a plusieurs incidences sur les différents domaines du système.
Un aspect important de la facturation concerne l'interface avec la Comptabilité financière. Elle
permet de créer automatiquement des documents dans les applications Comptabilité
financière et Contrôle de gestion lors de la création de document de facturation.
Structure d'un document de facturation
Sujet: Intégration de documents de facturation dans l'Administration des ventes


## PDF page 12

Figure 2: Structure d'un document de facturation
Perform the following system demonstration:
1. Call up the billing document you created earlier (transaction VF02).
2. Go to the header, item, and overview screens and display the key data (terms of
payment, preceding document, and posting status).
3. Go from the billing document directly to the automatically created accounting document
and give quick explanations for the postings made.
Account determination and transfer of fields will be presented in detail in separate units.
Tous les documents de facturation possèdent la même structure. Ils se composent d'un en-
tête et de plusieurs postes.
L'en-tête comprend les données générales suivantes valables pour l'ensemble du
document de facturation :
●
Numéro de client du payeur
●
Date de facture
●
Valeur nette de l'ensemble du document de facturation
Les postes comprennent les données suivantes significatives pour chaque poste
individuel :
●
Numéro d'article
●
Quantité facturée
●
Valeur nette des postes individuels
Chapitre 1: Documents de facturation dans l'Administration des ventes


## PDF page 13

Chapitre 1
Exercice 1
Afficher un document de facturation
Afficher un document de facturation
Exemple de gestion
En tant que commercial de votre entreprise, vous devez fournir à votre chef de service des
informations concernant une facture générée automatiquement pour un client donné. Vous
devez donc savoir comment afficher un document de facturation.
Repérez des informations dans un document de facturation et accédez à une pièce
comptable générée automatiquement.
Votre chef de service souhaite obtenir des informations spécifiques sur un document de
facturation donné. La seule information qui vous a été transmise est le numéro de la
commande d'achat ##S4615-A3 de la commande client standard (CDCL), sur laquelle est
basé le document de facturation. Vous voulez donc faire référence au document de
facturation à l'aide de la commande client standard (CDCL) créée avec le numéro de la
commande d'achat ##S4615-A3.
Commencez par vous familiariser avec la barre de lancement SAP Fiori.
Data for this course was imported through CATT and corresponding documents were
created for billing.
Remarque :
Dans les exercices de cette formation, lorsqu’une valeur contient ##, remplacez
ces caractères par le numéro que vous a attribué l'animateur.
1. Lancez la barre de lancement SAP Fiori depuis le menu d'applications Microsoft Windows.
Utilisez l'utilisateur S4615-## et le mot de passe fournis par l'animateur.
2. Vérifiez une facture client. La seule information dont vous disposez est le numéro de
référence client ou le numéro de commande d'achat ##S4615-A3. Déterminez le numéro
de facture via le flux de documents de la commande client. Notez le numéro de la facture.
3. Quelle livraison a servi de référence à la création de ce document de facturation ?


## PDF page 14

Astuce :
Vérifiez le poste de facture.
4. Vérifiez le statut de comptabilisation du document de facturation.
Astuce :
Vérifiez l'en-tête de la facture.
5. Quelles sont les conditions de paiement pour ce client ?
6. Quel est le prix (condition de prix PR00) pour l'article du premier poste ?
7. À quel secteur d'activité l'article du premier poste appartient-il ?
Afficher la pièce comptable :
Votre supérieur souhaite également obtenir des informations relatives à la pièce comptable.
1. Comment pouvez-vous accéder directement à cette pièce comptable à partir du
document de facturation ?
2. Visualisez le statut de traitement global dans le flux de documents.
Quel est le statut indiqué et pourquoi ?
3. Vous souhaitez obtenir la synthèse des documents de facturation établies ces deux
dernières semaines pour votre client C615-A##. Accédez au groupe de vignettes
Documents de facturation (Billing Documents) et appelez l'application Gestion des
documents de facturation. Affichez les détails du premier document de facturation
apparaissant dans la liste.
Chapitre 1: Documents de facturation dans l'Administration des ventes


## PDF page 15

4. Définissez des valeurs par défaut pour votre utilisateur et ajoutez des valeurs pour le
processus de vente. Ne modifiez pas les valeurs par défaut existantes.
Accédez à
 vos données utilisateur et sélectionnez
Options.
Vous souhaitez définir des valeurs par défaut pour les paramètres Société : 1010, Point
d'expéd. : 1010, Organisation commerciale : 1010, Canal de distribution : 10 et Secteur
d’activité : 00.
Sujet: Intégration de documents de facturation dans l'Administration des ventes


## PDF page 16

Chapitre 1
Solution 1
Afficher un document de facturation
Afficher un document de facturation
Exemple de gestion
En tant que commercial de votre entreprise, vous devez fournir à votre chef de service des
informations concernant une facture générée automatiquement pour un client donné. Vous
devez donc savoir comment afficher un document de facturation.
Repérez des informations dans un document de facturation et accédez à une pièce
comptable générée automatiquement.
Votre chef de service souhaite obtenir des informations spécifiques sur un document de
facturation donné. La seule information qui vous a été transmise est le numéro de la
commande d'achat ##S4615-A3 de la commande client standard (CDCL), sur laquelle est
basé le document de facturation. Vous voulez donc faire référence au document de
facturation à l'aide de la commande client standard (CDCL) créée avec le numéro de la
commande d'achat ##S4615-A3.
Commencez par vous familiariser avec la barre de lancement SAP Fiori.
Data for this course was imported through CATT and corresponding documents were
created for billing.
Remarque :
Dans les exercices de cette formation, lorsqu’une valeur contient ##, remplacez
ces caractères par le numéro que vous a attribué l'animateur.
1. Lancez la barre de lancement SAP Fiori depuis le menu d'applications Microsoft Windows.
Utilisez l'utilisateur S4615-## et le mot de passe fournis par l'animateur.
a) Sélectionnez Microsoft Windows
 et, pour afficher le menu d’applications, cliquez
sur
. Recherchez la barre de lancement SAP Fiori.
b) Pour lancer la barre de lancement SAP Fiori, cliquez sur l'entrée correspondante dans
la liste des applications.
c) Pour vous connecter, utilisez l'utilisateur S4615-## et le mot de passe fournis.
2. Vérifiez une facture client. La seule information dont vous disposez est le numéro de
référence client ou le numéro de commande d'achat ##S4615-A3. Déterminez le numéro
de facture via le flux de documents de la commande client. Notez le numéro de la facture.
a) Sélectionnez le groupe de vignettes Ventes (Sales) et lancez l'application Modifier
commande client.


## PDF page 17

b) Appuyez sur la touche d'aide à la recherche (F4) dans la zone Commande client. Dans
la zone de Critère de recherche, saisissez ##S4615-A3 dans la zone N° commande
d'achat et cliquez sur Rechercher. Confirmez votre saisie et sélectionnez le document
dans la liste.
c) Dans la commande, cliquez sur le bouton Afficher flux doc.
d) Sélectionnez la Facture, puis cliquez sur le bouton Afficher document.
3. Quelle livraison a servi de référence à la création de ce document de facturation ?
Astuce :
Vérifiez le poste de facture.
a) Sélectionnez un poste puis cliquez sur l'icône Afficher détails du poste ou sélectionnez
Plus → Saut → Poste → Sélectionner (les détails du poste s'afficheront).
b) Dans la page d'onglet Détails du poste, dans la zone d'écran Données de facture, les
informations significatives sont affichées dans la zone Modèle document.
c) Revenez à l'écran précédent en cliquant sur Retour.
4. Vérifiez le statut de comptabilisation du document de facturation.
Astuce :
Vérifiez l'en-tête de la facture.
a) Cliquez sur Plus → Saut → En-tête → En-tête.
b) Dans la page d'onglet Détail en-tête, dans la zone d'écran Données de comptabilité, la
zone Statut de comptabilisation affiche les informations suivantes :
La pièce comptable a été créée.
5. Quelles sont les conditions de paiement pour ce client ?
a) Les conditions de paiement sont affichées dans la page d'onglet Détail en-tête, dans la
zone d'écran Données de prix.
b) Revenez à l'écran précédent.
6. Quel est le prix (condition de prix PR00) pour l'article du premier poste ?
Sujet: Intégration de documents de facturation dans l'Administration des ventes


## PDF page 18

a) Sélectionnez le premier poste puis Plus → Saut → Poste → Conditions du poste.
b) Le prix (condition de prix PR00) pour l'article du premier poste s'affiche dans la page
d'onglet Conditions. Il s'élève à 1 400 EUR.
7. À quel secteur d'activité l'article du premier poste appartient-il ?
a) Sélectionnez la page d'onglet Détails du poste. La zone d'écran Données de facture
vous permet de visualiser le secteur d'activité. L'article du premier poste appartient au
secteur d'activité 03 (Motos).
b) Revenez à l'écran précédent.
Afficher la pièce comptable :
Votre supérieur souhaite également obtenir des informations relatives à la pièce comptable.
1. Comment pouvez-vous accéder directement à cette pièce comptable à partir du
document de facturation ?
a) Dans le document de facturation, sélectionnez Gestion comptable. Dans la Liste des
pièces en gestion comptable, sélectionnez Pièce comptable et cliquez sur Afficher la
pièce.
b) Revenez au document de facturation en cliquant sur Terminer.
2. Visualisez le statut de traitement global dans le flux de documents.
Quel est le statut indiqué et pourquoi ?
a) Sélectionnez Afficher flux de documents. Le statut de traitement global du document
de facturation est FI : liquidé, la pièce comptable ayant déjà été créée. Vous pouvez
également vérifier ce statut dans la synthèse des statuts.
b) Sélectionnez Facture et cliquez sur le bouton Synthèse des statuts. Le système affiche
le message suivant :
Statut de comptabil : Comptabilisé RF
En d'autres termes, les données ont été transférées en Comptabilité financière.
c) Le processus de traitement global de la pièce comptable est Non rapproché, aucun
encaissement n'ayant encore été effectué pour cette créance. Pour revenir au
document de facturation, cliquez sur Terminer.
3. Vous souhaitez obtenir la synthèse des documents de facturation établies ces deux
dernières semaines pour votre client C615-A##. Accédez au groupe de vignettes
Documents de facturation (Billing Documents) et appelez l'application Gestion des
Chapitre 1: Documents de facturation dans l'Administration des ventes


## PDF page 19

documents de facturation. Affichez les détails du premier document de facturation
apparaissant dans la liste.
a) Accédez au groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Gestion des documents de facturation.
b) Dans la zone Donneur d'ordre, saisissez votre client C615-A##. Dans la zone Date de
facturation du - au, sélectionnez la période correspondant aux deux dernières
semaines à compter de la date du jour.
c) Sélectionnez le premier document de facturation et cliquez sur Afficher afin
d'afficher les détails du document de facturation.
4. Définissez des valeurs par défaut pour votre utilisateur et ajoutez des valeurs pour le
processus de vente. Ne modifiez pas les valeurs par défaut existantes.
Accédez à
 vos données utilisateur et sélectionnez
Options.
Vous souhaitez définir des valeurs par défaut pour les paramètres Société : 1010, Point
d'expéd. : 1010, Organisation commerciale : 1010, Canal de distribution : 10 et Secteur
d’activité : 00.
a) Accédez à
 vos données utilisateur et sélectionnez
Options.
b) Sélectionnez
Valeurs standard. Saisissez les valeurs par défaut indiquées sans
modifier les valeurs par défaut existantes.
c) Cliquez sur Sauvegarder.
Sujet: Intégration de documents de facturation dans l'Administration des ventes


## PDF page 20

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Intégrer des documents de facturation dans le processus de l'Administration des ventes
Chapitre 1: Documents de facturation dans l'Administration des ventes


## PDF page 21

Chapitre 1
Évaluation des connaissances
1.
Parmi les éléments suivants, lesquels retrouve-t-on dans la structure d'un document de
facturation ?
Sélectionnez les réponses correctes.
A En-tête
B Échéance
C Synthèse
D Poste
2. Quelles informations sont indiquées au niveau de l'en-tête du document de facturation ?
Sélectionnez les réponses correctes.
A Payeur
B Quantité facturée
C Date de facture
D Réceptionnaire


## PDF page 22

Chapitre 1
Évaluation des connaissances - Réponses
1.
Parmi les éléments suivants, lesquels retrouve-t-on dans la structure d'un document de
facturation ?
Sélectionnez les réponses correctes.
A En-tête
B Échéance
C Synthèse
D Poste
2. Quelles informations sont indiquées au niveau de l'en-tête du document de facturation ?
Sélectionnez les réponses correctes.
A Payeur
B Quantité facturée
C Date de facture
D Réceptionnaire


## PDF page 23

CHAPITRE 2
Entités organisationnelles
Sujet 1
Définition d'entités organisationnelles
Exercice 2: Personnaliser des aspects des entités organisationnelles
OBJECTIFS DU CHAPITRE
●
Définir des entités organisationnelles


## PDF page 24

Chapitre 2
Sujet 1
Définition d'entités organisationnelles
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux entités organisationnelles responsables de la facturation et de la
comptabilité.
Exemple de gestion
Vous devez modifier plusieurs options du Customizing afin d'effectuer des modifications
propres à l'entreprise. La première étape consiste à examiner les entités organisationnelles
de l'Administration des ventes et de la Comptabilité financière. Vous devrez ensuite apporter
les modifications correspondantes dans les options de définition et d'affectation du
Customizing. Pour cette raison, vous devez disposer des connaissances suivantes :
●
connaître les entités organisationnelles de l'Administration des ventes et de la
Comptabilité financière et l'affectation de ces entités organisationnelles à d'autres entités.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Définir des entités organisationnelles
Customizing des entités organisationnelles
Définissez votre structure organisationnelle avec minutie et cohérence, en vous assurant de
prendre en compte tous les domaines de votre entreprise.
Essayez de définir votre structure organisationnelle de manière efficace. Vous réduirez ainsi
la charge de travail, par exemple, lors de la gestion des données de base. Vous disposez de
plusieurs options d'analyse.


## PDF page 25

Affectation des entités organisationnelles
Figure 3: Affectation d'organisations commerciales et de divisions
Display the required definitions and assignments in Customizing.
Define the company code and sales organization using the following Customizing paths:
●
Enterprise Structure →  Definition →  Financial Accounting →  Define company
Use company code 1010.
●
Enterprise Structure →  Definition →  Sales and Distribution →  Define, copy, delete,
check sales organization
Use sales organization 1010.
Display the assignment of sales organizations to company codes using the following
Customizing path:
Enterprise Structure →  Assignment →  Sales and Distribution →  Assign sales organization
to company code
Sales organization 1010 is assigned to company code 1010.
La société représente une entreprise indépendante au sens juridique, pour laquelle il est
possible de définir des comptes à des fins de reporting externe.
Les organisations commerciales et les divisions ne sont affectées qu'à une seule société.
Pour chaque organisation commerciale, le système détermine les divisions possibles en
fonction du canal de distribution afin qu'elle puisse vendre des marchandises provenant de
plusieurs divisions. Vous pouvez également affecter une division à plusieurs organisations
commerciales. Elles pourront toutes vendre des articles de cette division.
Sujet: Définition d'entités organisationnelles


## PDF page 26

Dans la commande client, le système détermine automatiquement une division chargée de la
livraison sur la base d'une règle de priorité.
Une organisation commerciale peut également vendre des marchandises provenant d'une
division affectée à une société autre que celle dont elle dépend elle-même (vente inter-
sociétés).
Le fait de combiner l'organisation commerciale avec le canal de distribution permet de
différentier l'organisation des ventes. Par exemple, le canal de distribution (vente directe)
utilisé par une organisation commerciale autorisera la vente de produits issus de certaines
divisions. Cela ne sera pas le cas si associé à d'autres organisations commerciales.
Organisation dans la Gestion comptable
Figure 4: Organisation dans la Gestion comptable
Chaque société définie dans le système SAP utilise des comptes généraux appartenant à un
seul plan comptable. Dans un plan comptable, les comptes généraux sont définis de manière
unique. Vous pouvez nommer le plan comptable selon vos impératifs spécifiques.
Dans la comptabilité financière, vous créez, sauvegardez, traitez et comptabilisez les
opérations commerciales au niveau de la société. Vous pouvez créer plusieurs sociétés dans
chaque mandant afin de gérer la comptabilité de plusieurs entreprises indépendantes. Vous
devez créer au minimum une société.
L'organisation commerciale appartenant à une seule société, le système détermine
automatiquement cette société lorsque vous saisissez l'organisation commerciale dans la
commande client.
Show how a company code is assigned to a chart of accounts (you do not need to necessarily
show this, since it is part of Financial Accounting).
Chapitre 2: Entités organisationnelles


## PDF page 27

In Customizing for Financial Accounting (New) under General Ledger Accounting (New) →
Master Data →  G/L Accounts →  Preparations →  Assign Company Code to Chart of
Accounts, show that company code 1010 is assigned to chart of accounts INT.
Sujet: Définition d'entités organisationnelles


## PDF page 28

Chapitre 2: Entités organisationnelles


## PDF page 29

Chapitre 2
Exercice 2
Personnaliser des aspects des entités
organisationnelles
Exemple de gestion
Vous souhaitez découvrir le système backend SAP et la navigation via SAP GUI.
En outre, vous souhaitez accéder au Customizing et récapituler l'affectation
organisationnelle.
1. Connectez-vous au système backend SAP. Les informations système, à savoir l'utilisateur
S4615-## et le mot de passe, vous seront fournis par l'animateur. Veillez à bien utiliser
le menu SAP
.
2. Ajustez vous-même SAP GUI.
Pour le menu SAP, rendez les codes de transaction visibles à l'utilisateur.
Dans la barre de menus, sélectionnez Autres fonctions →  Options, puis cochez Affichage
des noms techniques.
3. En tant que personne devant réaliser le Customizing dans le système SAP, il est important
de connaître les valeurs techniques de l'option du Customizing. Assurez-vous donc que
les clés techniques sont affichées dans la liste déroulante. Vérifiez et si nécessaire
personnalisez la mise en forme locale en conséquence.
Cliquez sur
Ajuster m.en.f locale et vérifiez les options sous Options → Conception
interaction → Visualisation 1, en vérifiant que les zones : Afficher clés dans zones des listes
déroulantes et : Trier par clés ds zones listes déroulantes pour saisie au clavier plus efficace
soient activées.
4. Familiarisez-vous avec le Customizing SAP.
Commencez par créer une entrée pour le Customizing SAP dans votre menu Favoris. Vous
pourrez ainsi accéder plus facilement au Customizing SAP par la suite. Pour ce faire, vous
avez le choix entre deux méthodes : vous pouvez insérer le code de transaction du
Customizing SPRO directement dans votre menu Favoris ou utiliser le bouton Ajouter aux
favoris dans le menu SAP.
Vous trouverez l'entrée du Customizing dans l'écran du Menu SAP, sous le chemin de
menus suivant : Outils → Customizing → IMG → Traitement de projet (code de transaction
SPRO).
5. Consultez les divers aspects des options organisationnelles dans le Customizing.
Où définissez-vous l'interface entre la Finance et l'Administration des ventes ?
Quelle société est affectée à l'organisation commerciale 1010 ?
Remarque :
N'apportez Pas la moindre modification aux options du Customizing.


## PDF page 30

Chapitre 2
Solution 2
Personnaliser des aspects des entités
organisationnelles
Exemple de gestion
Vous souhaitez découvrir le système backend SAP et la navigation via SAP GUI.
En outre, vous souhaitez accéder au Customizing et récapituler l'affectation
organisationnelle.
1. Connectez-vous au système backend SAP. Les informations système, à savoir l'utilisateur
S4615-## et le mot de passe, vous seront fournis par l'animateur. Veillez à bien utiliser
le menu SAP
.
a) Connectez-vous au système backend SAP à l'aide des informations fournies.
b) Si nécessaire, passez du Menu utilisateur au Menu SAP. Pour ce faire, sélectionnez
Menu → Menu SAP ou cliquez sur le bouton
 Menu SAP.
2. Ajustez vous-même SAP GUI.
Pour le menu SAP, rendez les codes de transaction visibles à l'utilisateur.
Dans la barre de menus, sélectionnez Autres fonctions →  Options, puis cochez Affichage
des noms techniques.
a) Dans la barre de menus, sélectionnez Autres fonctions →  Options, puis cochez
Affichage des noms techniques et cliquez sur
 Suite (Entrée).
3. En tant que personne devant réaliser le Customizing dans le système SAP, il est important
de connaître les valeurs techniques de l'option du Customizing. Assurez-vous donc que
les clés techniques sont affichées dans la liste déroulante. Vérifiez et si nécessaire
personnalisez la mise en forme locale en conséquence.
Cliquez sur
Ajuster m.en.f locale et vérifiez les options sous Options → Conception
interaction → Visualisation 1, en vérifiant que les zones : Afficher clés dans zones des listes
déroulantes et : Trier par clés ds zones listes déroulantes pour saisie au clavier plus efficace
soient activées.
a) Procédez comme indiqué : cliquez sur
 Ajuster m.en.f locale.
b) Vérifiez les options et accédez à Options → Conception interaction → Visualisation 1.
c) Dans l'onglet : Visualisation 1 dans la zone : Pilotages, si nécessaire, sélectionnez les
zones : Afficher clés dans zones des listes déroulantes et : Trier par clés ds zones listes
déroulantes pour saisie au clavier plus efficace.
d) Sélectionnez Reprendre et OK.
4. Familiarisez-vous avec le Customizing SAP.


## PDF page 31

Commencez par créer une entrée pour le Customizing SAP dans votre menu Favoris. Vous
pourrez ainsi accéder plus facilement au Customizing SAP par la suite. Pour ce faire, vous
avez le choix entre deux méthodes : vous pouvez insérer le code de transaction du
Customizing SPRO directement dans votre menu Favoris ou utiliser le bouton Ajouter aux
favoris dans le menu SAP.
Vous trouverez l'entrée du Customizing dans l'écran du Menu SAP, sous le chemin de
menus suivant : Outils → Customizing → IMG → Traitement de projet (code de transaction
SPRO).
a) Dans la barre de menus, sélectionnez Favoris → Ajouter transaction, puis saisissez le
code de transaction SPRO.
b) CDLC
c) Dans le Menu SAP, ouvrez le chemin de menus :
Outils → Customizing → IMG → Traitement de projet (code de transaction SAP SPRO),
puis cliquez sur le bouton
 AJOUTER AUX FAVORIS.
5. Consultez les divers aspects des options organisationnelles dans le Customizing.
Où définissez-vous l'interface entre la Finance et l'Administration des ventes ?
Quelle société est affectée à l'organisation commerciale 1010 ?
Remarque :
N'apportez Pas la moindre modification aux options du Customizing.
a) Vous définissez l'interface entre la Finance et l'Administration des ventes lorsque vous
configurez l'affectation de l'organisation commerciale à la société. En règle générale,
une organisation commerciale est affectée à une seule société, c’est pourquoi
l'Administration des ventes doit réaliser l'affectation.
b) Utilisez le menu Favoris pour appeler le Customizing SAP (code de transaction SAP
SPRO) et cliquez sur le bouton
 Guide de référence SAP.
c) Dans le Guide d'implémentation (IMG) du Customizing SAP, sélectionnez : Structure
de l'entreprise → Affectation → Administration des ventes (ADV) → Affecter
organisation commerciale à société et cliquez sur
 Activité IMG.
d) Dans la liste, recherchez l'entrée pour l'organisation commerciale 1010. Elle est
affectée à la société : 1010
e) Quittez le Customizing sans sauvegarder. Enfin, cliquez sur le bouton
(Terminer).
Sujet: Définition d'entités organisationnelles


## PDF page 32

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Définir des entités organisationnelles
Chapitre 2: Entités organisationnelles


## PDF page 33

CHAPITRE 3
Processus de facturation
Sujet 1
Contrôle du processus de facturation
Exercice 3: Définition d'un nouveau type de document de facturation
OBJECTIFS DU CHAPITRE
●
Contrôler le processus de facturation


## PDF page 34

Chapitre 3
Sujet 1
Contrôle du processus de facturation
VUE D'ENSEMBLE DU SUJET
L'objectif de ce sujet est de vous familiariser avec les principaux éléments de contrôle de la
facturation, dont le type de document de facturation. Vous découvrirez également quelles
sont les interactions existant entre le type de poste et la facturation.
Exemple de gestion
Dans votre entreprise, la facturation de certaines opérations commerciales s'effectue à partir
d'une commande client et d'autres à partir d'une livraison. Vous voulez également définir un
type de document de facturation distinct pour les ventes effectuées lors de foires dont les
numéros proviennent d'un intervalle de tranches de numéros particulier. Il s'agira du type de
document de facturation par défaut pour les commandes clients enregistrées lors d'une foire.
Pour cette raison, vous devez disposer des connaissances suivantes :
●
connaître les différentes opérations commerciales dans le contexte de la facturation et des
types de document de facturation ;
●
connaître l'importance du type de poste dans le cadre de la facturation.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Contrôler le processus de facturation


## PDF page 35

Types de document de facturation
Figure 5: Types de document de facturation
The Customizing path for defining billing types is Sales and Distribution →  Billing →  Billing
Documents →  Define Billing Types .
Perform the following activities:
1. Demonstrate the different billing types available in the system.
2. Describe a few control options for the billing type by choosing billing type F2 as an
example.
Le type de document de facturation est déterminant pour l'ensemble du document de
facturation.
Les types de document de facturation vous permettent de prendre en compte la totalité des
opérations commerciales durant le traitement de la facturation.
Le tableau suivant énumère les types de document de facturation disponibles dans le
système SAP :
Type de document de facturation
Description
F2
Facture
F8
Facture pro forma
BV
Vente au comptant
G2
Avoir
Sujet: Contrôle du processus de facturation


## PDF page 36

Type de document de facturation
Description
L2
Note de débit
RE
Retours
Facturation interne
IG
Facturation interne (avoir)
S1
Annulation de facture
S2
Annulation avoir
LR
Relevé de factures
LG
Liste des avoirs
Contrôles du type de document de facturation
Figure 6: Contrôles du type de document de facturation
Vous pouvez créer de nouveaux types de document de facturation ou modifier des types
existants dans le système standard pour satisfaire les impératifs spécifiques de votre
entreprise.
De nombreux paramètres de contrôle du type de document de facturation affectent le
traitement ultérieur dans le module Comptabilité financière (blocage de comptabilisation ou
détermination des comptes).
De nouvelles zones du type de document de facturation vous permettent de représenter des
caractéristiques spéciales de l'interface Administration des ventes ou Comptabilité
financière. Citons le type de pièce, l'écriture négative, la relation succursale/centrale, les
avoirs avec délai de validité.
Chapitre 3: Processus de facturation


## PDF page 37

Pertinence du type de poste
Figure 7: Type de document de facturation par défaut
Demonstration
Perform the following demonstrations:
●
In Customizing, demonstrate the importance of various item categories within billing,
such as item category TAN (delivery-related) and item category TAD (order-related).
●
Show how the default billing type is created. Use the sales document type SO as an
example.
●
In Customizing, configure billing type ZF20 with order type ZA20.
●
In Customizing, change the number range of the trade fair billing type ZF20 to the number
range interval 15, so that the numbers of the trade fair billing documents start with 7 and
can therefore be immediately recognized.
●
Assign the trade fair billing type ZF20 of the trade fair order type ZA20 as the default
billing type. This trade fair billing type ZF20 is to be used for order-related and delivery-
related billing items.
Au niveau du Customizing du type de poste, vous pouvez spécifier si la facturation doit se
référer à une livraison ou à une commande client.
Le système propose un type de document de facturation par défaut approprié d'après le
paramétrage du type de document de vente d'origine. Dans le cadre d'une facturation basée
sur une livraison, vous facturez une commande client standard (type de commande client
CDCL) en vous basant sur le type de document de facturation F2.
Lors de la création de documents de facturation, vous pouvez modifier le type de document
de facturation par défaut en entrant le type souhaité dans les données par défaut.
Sujet: Contrôle du processus de facturation


## PDF page 38

Factures créées à partir d'une livraison
Figure 8: Factures créées à partir d'une livraison
Vous pouvez créer une facture en référence à une commande client ou à une livraison.
Si vous voulez vous assurer que les marchandises sont expédiées avant de créer la facture,
créez cette dernière en vous basant sur la livraison. Exemple : la livraison d'un tapis.
Une facture peut faire simultanément référence à une commande client et à une livraison.
Vous pouvez par exemple créer une seule facture pour des marchandises (le tapis) et pour un
service (la pose du tapis) si vous avez autorisé ce paramétrage.
Chapitre 3: Processus de facturation


## PDF page 39

Factures créées à partir d'une commande client
Figure 9: Factures créées à partir d'une commande client
Si vous voulez facturer un client pour une prestation de services, vous créez normalement
une facture se référant à la commande client concernée. Les livraisons sont en effet rarement
créées pour des services tels que la pose d'un tapis.
Comment créer un document de facturation
1. Display in Customizing the billing-relevance of different item categories TAN and TAD.
Use product P615-100 as an example for item category TAN and product T-D100 as an
example for item category TAD.
1. Create a sales order with the customer reference 00S4615-A0.
Use the following data:
Field
Data Value
Order Type
OR (credit memo request)
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
Enter product P615-100 with quantity 10 (item category TAN) and product T-D100 with
10 hours (item category TAD).
Sujet: Contrôle du processus de facturation


## PDF page 40

2. Optional - when in doubt leave it out
3. Do the delivery, picking and PGO (post good issue) for the TAN item category.
4. In order to bill both items at the same time - note the delivery number AND note the
order number.
5. If you want to bill both items at the same time - go to the sales order and adjust the Req.
Del. Date so it is the same as the POG date (should be today’s day)
6. Go to Sales and Distribution  → Billing  → Billing document → Create (transaction code
VF01).
7. Change the Default Data choose Billing Type Invoice F1
8. Create an invoice with reference to the delivery and the sales order.
One billing document with both items - with item category TAN and TAD.
Chapitre 3: Processus de facturation


## PDF page 41

Chapitre 3
Exercice 3
Définition d'un nouveau type de document de
facturation
Exemple de gestion
Vous devez créer le document de facturation d'une livraison déjà effectuée. Vous êtes
également chargé de définir un nouveau type de document de facturation dans l'entreprise
pour les commandes clients prises à l'occasion d'une foire. Il s'agira du type de document de
facturation par défaut pour la facturation lors du traitement de commandes clients prises à
l'occasion d'une foire pour la facturation. Vous devez donc savoir comment définir un
nouveau type de document de facturation.
Définition d'un nouveau type de document de facturation
Vous allez modifier les options du Customizing. Pour cela, utilisez SAP GUI dans le système
backend pour cet exercice.
Créez d'abord un document de facturation à partir d'une livraison déjà effectuée.
1. Dans le système backend, utilisez le Menu SAP et appelez la commande avec le numéro
de commande d'achat ##S4615-A1. Affichez le flux de documents de la commande client
et notez le numéro de livraison.
Vous le trouverez dans le menu SAP : Logistique → Administration des ventes
(ADV) → Vente → Commande client → Afficher
Notez le numéro de livraison. Numéro de livraison : ____________________________
Créez une facture pour cette livraison.
2. Affichez la facture.
De quel type est-elle ?
3. À quel type de document correspond la commande client qui se trouve au début du
processus ?
4. Revenez au document de facturation.


## PDF page 42

Définissez le type de poste associé à ces postes puis notez leur mode de facturation.
5. Recherchez ces aspects dans le Customizing. Appelez le Customizing SAP à l'aide de
votre menu Favoris.
Définissez le type de facture Foire ZF##
Configurez le type de facture Foire déjà existant en utilisant les données indiquées dans les
sous-tâches suivantes.
1. Affichez le type de document de facturation Foire ZF## que vous a fourni le système.
2. Recherchez la tranche de numéros appropriée et affectez-la aux factures de type Foire.
Ces numéros doivent être compris entre 70000000 et 74999999.
3. Votre nouveau type de document de facturation ZF## doit être le type par défaut en cas
de facturation créée à partir d'une commande ou d'une livraison si votre type de
document de vente ZA## est utilisé. Affectez cette valeur par défaut dans le Customizing.
Testez vos options du Customizing en réalisant l'ensemble du processus de vente à l'aide
de votre commande de type Foire.
Afin de tester vos options, ouvrez une nouvelle fenêtre SAP GUI en cliquant sur
.
Dans le menu SAP, créez une commande client en utilisant les données suivantes :
Zone
Valeur de données
Type de commande
ZA## (cde Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. client
S4615-ZF##
Article
P615-1##
Quantité d'ordre
5 pces
Pour créer la livraison, utilisez le point d'expédition 1010, exécutez les étapes nécessaires
pour le prélèvement et enregistrez la sortie de marchandises.
Astuce :
Normalement, votre système utilisera automatiquement votre document de
facturation Foire ## (ZF##) et votre facture commencera par le
nombre 7000.
Chapitre 3: Processus de facturation


## PDF page 43

Chapitre 3
Solution 3
Définition d'un nouveau type de document de
facturation
Exemple de gestion
Vous devez créer le document de facturation d'une livraison déjà effectuée. Vous êtes
également chargé de définir un nouveau type de document de facturation dans l'entreprise
pour les commandes clients prises à l'occasion d'une foire. Il s'agira du type de document de
facturation par défaut pour la facturation lors du traitement de commandes clients prises à
l'occasion d'une foire pour la facturation. Vous devez donc savoir comment définir un
nouveau type de document de facturation.
Définition d'un nouveau type de document de facturation
Vous allez modifier les options du Customizing. Pour cela, utilisez SAP GUI dans le système
backend pour cet exercice.
Créez d'abord un document de facturation à partir d'une livraison déjà effectuée.
1. Dans le système backend, utilisez le Menu SAP et appelez la commande avec le numéro
de commande d'achat ##S4615-A1. Affichez le flux de documents de la commande client
et notez le numéro de livraison.
Vous le trouverez dans le menu SAP : Logistique → Administration des ventes
(ADV) → Vente → Commande client → Afficher
Notez le numéro de livraison. Numéro de livraison : ____________________________
Créez une facture pour cette livraison.
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Vente → Commande client →  Afficher.
b) Appuyez sur la touche d'aide à la recherche (F4) dans la zone Commande client. Dans
Documents de vente par numéro de commande chez client, saisissez ##S4615-A1
dans la zone Nº de commande d'achat. Confirmez votre saisie et sélectionnez le
document dans la liste.
c) Accédez au flux de documents en sélectionnant Environnement →  Afficher flux doc.
Notez le numéro de livraison et quittez la transaction.
d) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Facturation →  Facture →  Créer;
e) Saisissez le numéro de la livraison comme document à facturer, puis exécutez le
programme.
f)
 Sauvegardez le document.
2. Affichez la facture.


## PDF page 44

De quel type est-elle ?
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Afficher.
b) La barre de titre affiche le type de document de facturation. Il s'agit du type F2
(Facture F2).
3. À quel type de document correspond la commande client qui se trouve au début du
processus ?
a) Sélectionnez Environnement → Afficher flux doc, puis affichez le document de
commande, sélectionnez la commande et sélectionnez Afficher document.
b) Sélectionnez Saut → En-tête → Ventes.
c) Dans Ventes, la valeur de la zone Type commande cl est CDCL (Commande client
standard).
4. Revenez au document de facturation.
Définissez le type de poste associé à ces postes puis notez leur mode de facturation.
a) Revenez au document de facturation.
b) Sélectionnez un poste et cliquez sur
 Afficher détails du poste. La valeur pour la
zone Type de poste est TAN (Poste standard). Dans le système standard, le type de
poste TAN sert pour les postes d'articles gérés en stock. Pour ces derniers, la
facturation est effectuée à partir de la livraison.
5. Recherchez ces aspects dans le Customizing. Appelez le Customizing SAP à l'aide de
votre menu Favoris.
a) Utilisez le menu Favoris et sélectionnez l'entrée Customizing (code de transaction
SPRO).
b) Accédez au Customizing et cliquez sur le bouton
 Guide de référence SAP.
c) Dans le Customizing, sélectionnez Guide d'implémentation : Administration des ventes
(ADV) → Vente → Documents de vente → Poste de document de vente → Définir les
types de poste
d) Sélectionnez le type de poste TAN et cliquez sur le bouton
 (Détail).
e) Dans la zone d'écran Données commerciales, la valeur pour la zone Pertinence facture
est A (facture créée à partir d'une livraison).
Chapitre 3: Processus de facturation


## PDF page 45

f) Revenez en arrière et sélectionnez Administration des ventes
(ADV) → Vente → Documents de vente → En-tête du document de vente → Définir les
types de document de vente.
g) Sélectionnez le type de document de vente CDCL, puis cliquez sur
 (Détail).
h) Dans la zone d'écran Facturation, la valeur pour la zone TypeFact à p. livr. est F2
(Facture F2).
Définissez le type de facture Foire ZF##
Configurez le type de facture Foire déjà existant en utilisant les données indiquées dans les
sous-tâches suivantes.
1. Affichez le type de document de facturation Foire ZF## que vous a fourni le système.
a) Dans le Customizing, sélectionnez Guide d'implémentation : Administration des ventes
(ADV) → Facturation → Factures → Définir les types de facture.
b) Sélectionnez l'activité Définir les types de facture et cliquez sur le bouton
Sélectionner.
c) Cliquez sur le bouton
 Positionner et saisissez le type de document de facturation
ZF##.
d) Sélectionnez le type de document de facturation ZF##, puis cliquez sur
 Détail.
Recherchez la zone Affectation de tranche de numéros (Tr.interne numéros). Vous ne
savez pas quelle tranche de numéros est nécessaire et devez donc la rechercher.
2. Recherchez la tranche de numéros appropriée et affectez-la aux factures de type Foire.
Ces numéros doivent être compris entre 70000000 et 74999999.
a) Dans le Customizing, sélectionnez Guide d'implémentation : Administration des ventes
(ADV) → Facturation → Factures → Définir les tranches de numéros pour les factures.
b) Cliquez sur le bouton
 Interv. (Afficher intervalles). L'intervalle 15 se base sur la
tranche indiquée.
c) Pour affecter l'intervalle 15 à votre type de document de facturation Foire ZF##,
appelez-la de nouveau dans le Customizing, en sélectionnant Guide d'implémentation :
Administration des ventes (ADV) → Facturation → Factures → Définir les types de
facture.
d) Sélectionnez l'activité Définir les types de facture et cliquez sur le bouton
Sélectionner.
e) Cliquez sur le bouton
 Positionner et saisissez le type de document de facturation
ZF##.
f) Sélectionnez le type de document de facturation ZF##, puis cliquez sur
 Détail.
g) Dans la zone Tr.interne numéros, saisissez 15 et sauvegardez vos entrées.
3. Votre nouveau type de document de facturation ZF## doit être le type par défaut en cas
de facturation créée à partir d'une commande ou d'une livraison si votre type de
document de vente ZA## est utilisé. Affectez cette valeur par défaut dans le Customizing.
Sujet: Contrôle du processus de facturation


## PDF page 46

Testez vos options du Customizing en réalisant l'ensemble du processus de vente à l'aide
de votre commande de type Foire.
Afin de tester vos options, ouvrez une nouvelle fenêtre SAP GUI en cliquant sur
.
Dans le menu SAP, créez une commande client en utilisant les données suivantes :
Zone
Valeur de données
Type de commande
ZA## (cde Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. client
S4615-ZF##
Article
P615-1##
Quantité d'ordre
5 pces
Pour créer la livraison, utilisez le point d'expédition 1010, exécutez les étapes nécessaires
pour le prélèvement et enregistrez la sortie de marchandises.
Astuce :
Normalement, votre système utilisera automatiquement votre document de
facturation Foire ## (ZF##) et votre facture commencera par le
nombre 7000.
a) Dans le Customizing, sélectionnez Guide d'implémentation : Administration des ventes
(ADV) → Vente → Documents de vente → En-tête du document de vente → Définir les
types de document de vente.
b) Sélectionnez le type de document de vente ZA##, puis cliquez sur
 (Détail).
c) Dans la zone d'écran Facturation, saisissez ZF## dans les zones TypeFact. à p. livr. et
T.Fact. en fct cde.
d) Afin de tester vos options, ouvrez une nouvelle fenêtre SAP GUI en cliquant sur
.
e) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.
f) Saisissez le type de commande ZA##, l'organisation commerciale 1010, le canal de
distribution 10 et le secteur d'activité 00, puis confirmez votre saisie.
g) Saisissez les autres détails comme indiqué dans la tâche et enfin, sauvegardez (bouton
) votre commande.
Donneur d'ordre
C615-A##
Réf. client
S4615-ZF##
Chapitre 3: Processus de facturation


## PDF page 47

Article
P615-1##
Quantité d'ordre
5 pces
h) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Expédition et transport → Livraison sortante → Créer → Document
individuel → Avec référence à la commande client.
i) Saisissez le point d'expédition 1010 et la date de sélection <10 jours à compter de la
date du jour>. Confirmez votre saisie.
j) Accédez à l’onglet Prélèvement d’articles et entrez la quantité de prélèvement 5 dans
la zone Qté prélevée.
k) Cliquez ensuite sur le bouton : Enreg. sortie march.
l) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes →
Facturation  →  Facture →  Créer. La livraison que vous venez de créer doit être
affichée dans la zone Document. Si ce n'est pas le cas, saisissez-la. Ensuite,
sélectionnez Sauvegarder.
m) Afin d'examiner le résultat, sélectionnez Facture → Afficher. Lorsque vous appuyez sur
la touche Entrée, le document de facturation que vous venez de créer s'affiche. Si vous
avez bien suivi les étapes, votre type de document de facturation ZF## est
automatiquement sélectionné et votre document de facturation commence par 7000.
Sujet: Contrôle du processus de facturation


## PDF page 48

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Contrôler le processus de facturation
Chapitre 3: Processus de facturation


## PDF page 49

Chapitre 3
Évaluation des connaissances
1.
Une facture peut faire simultanément référence à une commande client et à une livraison.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
2. Si vous voulez vous assurer que les marchandises sont expédiées avant de créer la
facture, sur quoi devez-vous vous baser pour la créer ?
Sélectionnez la réponse correcte.
A Commande client
B Commande d'achat
C Livraison
D Consignes d'expédition


## PDF page 50

Chapitre 3
Évaluation des connaissances - Réponses
1.
Une facture peut faire simultanément référence à une commande client et à une livraison.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
2. Si vous voulez vous assurer que les marchandises sont expédiées avant de créer la
facture, sur quoi devez-vous vous baser pour la créer ?
Sélectionnez la réponse correcte.
A Commande client
B Commande d'achat
C Livraison
D Consignes d'expédition


## PDF page 51

CHAPITRE 4
Types de documents de
facturation spéciaux
Sujet 1
Création de documents de facturation dans la gestion des réclamations
Exercice 4: Créer des documents de facturation dans la gestion des réclamations
Sujet 2
Création de factures pro forma et de vente au comptant
Exercice 5: Créer une facture de vente au comptant et une facture pro forma
OBJECTIFS DU CHAPITRE
●
Créer des documents de facturation dans la gestion des réclamations
●
Créer des factures pro forma et de vente au comptant


## PDF page 52

Chapitre 4
Sujet 1
Création de documents de facturation dans la
gestion des réclamations
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux différents processus de gestion et types de document de
facturation disponibles pour la gestion des réclamations.
Exemple de gestion
Il peut arriver qu'un de vos clients se plaigne des marchandises que vous lui avez envoyées.
Pour le satisfaire, vous voulez lui envoyer un avoir. Dans des cas exceptionnels, vous devez
annuler des factures en raison de données incorrectes. Pour cette raison, vous devez
disposer des connaissances suivantes :
●
connaître le processus et les méthodes de contrôle des différentes opérations
commerciales possibles dans le contexte de la facturation.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Créer des documents de facturation dans la gestion des réclamations
Annulation
Figure 10: Annulation


## PDF page 53

Pour annuler un document de facturation, vous devez créer un document d'annulation. Le
système copie les données à partir du document de référence dans le document d'annulation
et passe une écriture de contrepartie dans le module Comptabilité financière.
Le document de référence du document de facturation (par exemple, la livraison à l'origine de
la facture annulée) peut alors être refacturé.
Pour annuler des avoirs, vous pouvez utiliser le type de document de facturation S2 défini
dans le système standard.
Il n'est pas nécessaire de réaliser le paramétrage du pilotage de la copie pour les annulations.
Le système utilise directement les informations contenues dans le sous-écran Annulation du
type de document de facturation (par exemple, numéro d'affectation et numéro de
référence).
Vous pouvez également annuler des postes un par un dans un document de facturation.
Lorsque vous annulez un document, vous passez à un écran de synthèse comprenant le
document de facturation d'origine ainsi que le document d'annulation. Avant d'effectuer une
mise à jour, vous pouvez comparer les deux documents afin d'éviter toute incohérence lors de
l'annulation. Lors de la mise à jour, le système essaie également de compléter le document de
facturation et le document d'annulation.
Comment annuler un document de facturation
Cancel a billing document.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Cancel the billing document for the order with purchase order number 00S4615-A3.
2. Using the document flow, display the created accounting document for cancellation.
3. Explain Customizing for cancellation billing document type S1.
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 54

Notes de crédit et de débit
Figure 11: Notes de crédit et de débit
Vous pouvez créer des notes de crédit ou de débit à partir des demandes de notes de crédit
ou de débit (documents de vente) ou directement à partir d'un document de facturation si
votre entreprise n'exige pas de procédure de validation dans le cas de réclamations.
Vous pouvez créer ces demandes de plusieurs manières :
●
sans référence à une opération commerciale précédente ;
●
en référence à une commande client ;
●
en référence à un document de facturation.
Le Customizing vous permet de déterminer si le système va activer automatiquement un
blocage facture pour une demande de note de crédit ou de débit.
En tant que salarié, vous pouvez :
●
valider la demande de note de débit ou de crédit après son examen. Vous pouvez décider
du montant ou de la quantité à créditer ou débiter.
●
refuser des postes dans la demande et saisir un motif de refus.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 55

Validation ou refus de demandes d'avoir
Figure 12: Validation ou refus de demandes d'avoir
Pour valider une demande d'avoir vous devez désactiver le blocage facture.
Si le bien-fondé de la réclamation n'a pas encore été établi, vous pouvez saisir un motif de
refus pour chaque poste.
Le système ne reprendra pas la valeur des postes concernés dans le document de
facturation.
L'utilisation du motif de refus vous permet de contrôler si le poste :
●
doit être repris dans l'avoir avec une valeur nulle ;
●
figurera sur l'avoir.
Les demandes de notes de débit sont traitées exactement de la même manière.
Figure 13: Workflow des demandes d'avoir
Généralement, lors de la création d'une demande d’avoir, le système active le blocage de la
facture (avoir) jusqu'à ce qu'un salarié la débloque. Dans votre entreprise, vous pouvez définir
à quel instant la vérification doit être effectuée et par quel salarié, selon la valeur de la
demande de note de crédit.
Si cette valeur est inférieure à une valeur minimale donnée, le système peut valider
automatiquement la demande.
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 56

Le workflow propre au traitement des notes de crédit garantit que le système détermine et
informe automatiquement le salarié (selon la valeur concernée) lors de la création d'une
demande de note de crédit. Le salarié en question peut alors refuser, valider ou traiter la
demande de note de crédit.
Avec l'application Gestion des demandes d'avoir, vous pouvez configurer le workflow pour
optimiser le processus d'approbation des demandes d'avoir. L'application vous permet de
définir les conditions de validation automatique des demandes d’avoir et de définir les
approbateurs des demandes devant être vérifiées. Si un workflow est activé et si les
conditions de lancement configurées sont remplies, le processus d’approbation est initié.
Les spécialistes de processus de gestion peuvent définir des équipes commerciales avec
leurs membres d'équipe et approbateurs. Les experts en configuration peuvent définir et
activer les workflows de demande d'avoir avec leurs valeurs seuils et agents. Le directeur
commercial peut recevoir des avis (Ma boîte de réception ou Avis) pour les demandes d'avoir
en attente d'approbation. Le responsable peut décider d'approuver ou de rejeter les
demandes d'avoir, ou bien demander à des commerciaux internes de les reprendre.
Avant d'utiliser l'application Gestion des demandes d'avoir, vous devez activer le workflow
standard SAP WS00800286 pour ce scénario. Pour plus d'informations, reportez-vous à la
documentation d'aide SAP. En outre, pour pouvoir affecter les fonctions d’approbation de
demande d’avoir requises aux membres de l’équipe responsables dans l'application Gestion
des équipes et responsabilités, les autorisations pertinentes ci-dessous doivent être affectées
à l’utilisateur.
Le workflow de vente pour les demandes d'avoir fournit un processus sécurisé d'approbation
de ces demandes. Il permet d'automatiser l'approbation des demandes d’avoir sous certaines
valeurs seuils. Cela permet de gagner du temps et de minimiser les efforts en envoyant des
notifications aux membres de l'équipe appropriés ainsi que d’accélérer le traitement des
approbations des demandes d'avoir.
Comment créer un avoir
Create a credit memo.
The demo description is based on SAP GUI transactions and SAP Menu path.
Optional demo for the scenario credit memo request workflow - please refer to the SSG
(system set-up guide).
1. Create a credit memo request with reference to the order with the purchase order number
00S4615-A1.
Use the following data:
Field
Data Value
Order Type
G2 (credit memo request)
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 57

Adopt the items P615-100 and P615-200 , and change the quantity of P614-200 to two
pieces.
2. Reject the second item and select Unreasonable request as the reason for rejection.
3. Release the credit memo request using the selection report Sales Documents Blocked for
Billing .
4. Bill the credit memo request and explain the consequences of the reason for rejection for
the credit memo. As a result of the reason for rejection, the second item has the value 0 .
5. Show the Customizing settings that are required for the credit memo request and the
reason for rejection for this process.
Demandes de correction de facture
Figure 14: Processus de correction de facture
La demande de correction de facture constitue une combinaison de la demande d'avoir et de
la demande de note de débit.
Le système crédite intégralement le poste de facture incorrect et crée automatiquement et
simultanément un poste de note de débit. L'écart qui en résulte correspond au montant
définitif à créditer.
Vous devez créer la demande de correction de facture à partir du document de facturation
correspondant (jamais à partir d'une commande client ou d'une demande d'offre).
Lors de la création d'une demande de correction de facture, le système duplique
automatiquement les postes. Cela signifie que pour chaque poste créé dans le document de
facturation, le système en crée un deuxième. Les types de postes créés doivent avoir des
valeurs +/- opposées.
Le système énumère dans un premier temps tous les postes d'avoir puis tous ceux de notes
de débit. Dès que vous indiquez le document et le poste précédents, le système crée la
référence au document de facturation correspondant.
Vous ne pouvez pas modifier le poste d'avoir. En revanche, vous pouvez mettre à jour le poste
de note de débit correspondant en fonction de nouvelles caractéristiques (par exemple,
nouvelle détermination du prix ou modification de la quantité).
Vous pouvez supprimer les notes de crédit et de débit par paires. De cette manière, vous
pouvez supprimer en une seule fois des paires de postes non modifiés.
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 58

Écart de quantité
Figure 15: Écart de quantité
Vous gérez l'écart de quantité lorsque vous traitez une réclamation d'un client à propos d'une
quantité donnée de marchandises endommagées ou de mauvaise qualité.
Le système corrige la quantité à facturer via le poste de note de débit.
Si d'autres paires de postes, créées à partir du document de facturation correspondant, ne
font pas l'objet de modifications, vous pouvez les supprimer en une seule fois en appuyant sur
le bouton Supprimer poste non modifié.
Écart de prix
Figure 16: Écart de prix
Vous gérez l'écart de prix lorsque vous traitez une réclamation d'un client à propos d'un prix
incorrect de marchandises.
Vous devez corriger les éléments de prix dans la note de débit.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 59

Comment créer une demande de correction de facture
Create an invoice correction request.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Create an invoice correction request for the billing document of the order that you created
with reference to purchase order number 4711.
2. Enter order type RK (invoice correction request), sales organization 1010 , distribution
channel 10 , and division 00 . Choose the Copy pushbutton.
3. Change the quantity for the first item from 10 pieces to 8 pieces. Go to the pricing screen
for the second item and reduce the price per piece. Do not make any changes for the third
item.
4. Choose the Delete unchanged item pushbutton.
5. Delete the billing block. Enter an order reason and save the invoice correction request.
6. Create the credit memo for the above invoice correction request.
7. Show the Customizing settings required for this process in Customizing for Sales and
Distribution under Sales →  Sales Documents →  Sales Document Header →  Define Sales
Document Types .
8. On the detail screen for sales document type RK, show that the sales document category
is K (credit memo request) and the indicator is D (invoice correction request).
9. In Customizing for Sales and Distribution under Sales →  Maintain Copy Control for Sales
Documents , select Copying Control: Billing Document to Sales Document .
10. Select the row with target RK and source F2 and go to the detail screen for item category
TAN . Two new fields have been included in copying control for invoice correction requests
(select D for the sales document type):
●
Item category proposal is L2N .
●
Pricing type is D .
The pricing type of the credit memo item is set at E , so that the values are copied and
frozen to prevent changes.
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 60

Gestion des retours
Figure 17: Retours
Vous créez un retour pour des marchandises renvoyées par un client insatisfait.
Les retours sont traités exactement de la même manière que des demandes d'avoir.
Astuce :
L'avoir est créé à partir du document de retour et non de la livraison de retour.
Comment exécuter une gestion des retours
Execute a return process.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Create a return with reference to the order with the purchase order number 00S461515-
A5. Use order type RE (create return).
2. Create a returns delivery and post a goods receipt for the return.
3. Release the return by deleting the billing block.
4. Create a returns credit memo.
5. Demonstrate the Customizing settings required for this process.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 61

Chapitre 4
Exercice 4
Créer des documents de facturation dans la
gestion des réclamations
Exemple de gestion
Le client C615-A## vous adresse une réclamation : le prix du premier poste est trop élevé sur
la facture de la commande d'achat n° ##S4615-A4. Vous avez oublié de tenir compte de
l'accord spécial conclu avec ce client ; vous confirmez donc la validité de la réclamation. Le
montant de l'avoir doit être calculé automatiquement. Vous devez donc savoir comment
effectuer le processus de correction des factures qui est une façon de gérer les réclamations.
Créez des documents de facturation dans la gestion des réclamations.
Utilisez les applications SAP Fiori dédiées à la gestion des réclamations.
1. Accédez à la barre de lancement SAP Fiori. Si vous vous êtes déconnecté, rappelez-la de
nouveau à partir du menu d'applications Microsoft Windows. Connectez-vous avec
l'utilisateur S4615-## et le mot de passe qui vous ont été fournis.
2. Déterminez le numéro de facture en utilisant le flux de documents de la commande qui a
pour référence le numéro de commande d'achat ##S4615-A4.
Numéro de facture :
3. Utilisez la facture concernée comme référence pour créer une demande de correction de
facture.
4. Quel est le nombre de postes créés et pourquoi ?
5. Diminuez le prix du premier poste de la note de débit de 100 EUR par pièce.
6. Supprimez les postes qui n'ont pas été modifiés et saisissez un motif de commande client.
7. Créez un avoir pour la demande de correction de facture. Validez la demande de
correction de facture pour la facturation et notez son numéro.


## PDF page 62

Numéro de la correction de facture :
Enfin, vérifiez le statut de votre demande de correction de facture dans l'application Gérer
les demandes d'avoir - Créer commande client.
Quel est le statut global de votre demande de correction de facture après le traitement de
l’avoir ?
8. Quelle caractéristique du pilotage de la copie pour les demandes de correction de facture
permet de faire apparaître le poste d'avoir et de note de débit dans le document ?
Vérifiez ces options dans le Customizing du système backend.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 63

Chapitre 4
Solution 4
Créer des documents de facturation dans la
gestion des réclamations
Exemple de gestion
Le client C615-A## vous adresse une réclamation : le prix du premier poste est trop élevé sur
la facture de la commande d'achat n° ##S4615-A4. Vous avez oublié de tenir compte de
l'accord spécial conclu avec ce client ; vous confirmez donc la validité de la réclamation. Le
montant de l'avoir doit être calculé automatiquement. Vous devez donc savoir comment
effectuer le processus de correction des factures qui est une façon de gérer les réclamations.
Créez des documents de facturation dans la gestion des réclamations.
Utilisez les applications SAP Fiori dédiées à la gestion des réclamations.
1. Accédez à la barre de lancement SAP Fiori. Si vous vous êtes déconnecté, rappelez-la de
nouveau à partir du menu d'applications Microsoft Windows. Connectez-vous avec
l'utilisateur S4615-## et le mot de passe qui vous ont été fournis.
a) Si vous vous êtes déconnecté de la barre de lancement SAP Fiori, cliquez sur
Microsoft Windows et, pour afficher le menu d'applications, cliquez sur
.
Recherchez la barre de lancement SAP Fiori.
b) Pour lancer la barre de lancement SAP Fiori, cliquez sur l'entrée correspondante dans
la liste des applications.
c) Utilisez l'utilisateur S4615-## et le mot de passe fournis pour vous connecter.
2. Déterminez le numéro de facture en utilisant le flux de documents de la commande qui a
pour référence le numéro de commande d'achat ##S4615-A4.
Numéro de facture :
a) Sélectionnez le groupe de vignettes Ventes (Sales) et lancez l'application Modifier
commande client.
b) Appuyez sur la touche d'aide à la recherche (F4) dans la zone Commande client. Dans
la zone d'écran Critères de recherche, dans la zone N° commande d'achat, saisissez
##S4615-A4, puis cliquez sur Rechercher. Confirmez votre saisie et sélectionnez le
document dans la liste.
c) Dans la commande, cliquez sur le bouton Afficher flux doc.
d) Sélectionnez la Facture F2, puis cliquez sur le bouton Afficher document.


## PDF page 64

e) Notez le numéro de la facture.
Numéro de facture _______________________
3. Utilisez la facture concernée comme référence pour créer une demande de correction de
facture.
a) Sélectionnez le groupe de vignettes Gestion des réclamations, puis lancez l'application
Gérer les demandes d'avoir - Créer commande client.
b) Sélectionnez Créer demande d’avoir et comme type de commande, saisissez : RK, puis
cliquez sur Suite.
c) Entrez le numéro de document de facturation déterminé ci-dessus comme document
de référence, puis cliquez sur Copier.
4. Quel est le nombre de postes créés et pourquoi ?
La demande de correction de facture contient six postes. Pour chacun des trois postes du
document de facturation de référence, le système crée un avoir et une note de débit au
niveau de la demande de correction de facture.
5. Diminuez le prix du premier poste de la note de débit de 100 EUR par pièce.
a) Sélectionnez le poste de la note de débit à partir du premier poste dans le document
de facturation (numéro de poste 40), puis cliquez sur le bouton
 Conditions de
poste.
b) Modifiez le prix PR00 et diminuez-le de 100 euros par pièce.
c) Revenez à l'écran précédent en cliquant sur Retour. La valeur actuelle à créditer après
la modification est de 1 000 EUR.
6. Supprimez les postes qui n'ont pas été modifiés et saisissez un motif de commande client.
a) Appuyez sur le bouton Supprimer poste non modifié. Confirmez la suppression.
b) Sélectionnez la page d'onglet Ventes.
c) Sélectionnez le motif de la commande client : avoir (correction de facture)..
d) Sauvegardez la demande de correction de facture et sélectionnez Sauvegarder, puis
Terminer.
7. Créez un avoir pour la demande de correction de facture. Validez la demande de
correction de facture pour la facturation et notez son numéro.
Numéro de la correction de facture :
Enfin, vérifiez le statut de votre demande de correction de facture dans l'application Gérer
les demandes d'avoir - Créer commande client.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 65

Quel est le statut global de votre demande de correction de facture après le traitement de
l’avoir ?
Statut global : Liquidé
a) Sélectionnez le groupe de vignettes Gestion des réclamations, puis lancez l'application
Gérer les demandes d'avoir - Créer commande client.
b) Saisissez votre client C615-A## et conservez les données du domaine commercial
(organisation commerciale 1010, canal de distribution 10, secteur d'activité 00) et
cliquez sur Lancer.
c) Sélectionnez votre demande d'avoir (demande de correction de facture) de l'exercice
précédent.
d) Cliquez sur le bouton Supprimer blocage de facture.
e) Notez le numéro de la correction de facture :
Numéro de document : _______________________
f) Une fois vos modifications sauvegardées par le système, cliquez sur Terminer pour
fermer l'application.
g) Accédez au groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Création de documents de facturation (VF01).
h) Saisissez le numéro de la demande de correction de facture comme document à
facturer. Exécutez le programme et cliquez sur Sauvegarder.
i) Pour examiner le statut global, cliquez à nouveau sur le groupe de vignettes Gestion
des réclamations, puis lancez l'application Gérer les demandes d'avoir - Créer
commande client.
j) Saisissez votre client C615-A## et conservez les données du domaine commercial,
puis cliquez sur Lancer.
k) Examinez le statut global correspondant au numéro de la demande de correction de
facture. Il est défini sur Terminé.
8. Quelle caractéristique du pilotage de la copie pour les demandes de correction de facture
permet de faire apparaître le poste d'avoir et de note de débit dans le document ?
Vérifiez ces options dans le Customizing du système backend.
a) Accédez au Customizing (code de transaction SPRO) et sélectionnez dans le Guide
d'implémentation : Administration des ventes (ADV) Vente → Gérer pilotage copie pour
documents de vente.
b) Sélectionnez Pilotage copie : facture vers document de vente et appuyez sur le bouton
 Sélectionner.
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 66

c) Cliquez sur le bouton
 Positionner et saisissez le type de document de vente RK et le
type de document de facturation F2. Confirmez vos entrées.
d) Sélectionnez la ligne et dans le volet Structure de dialogue, puis double-cliquez sur
Poste.
e) Sélectionnez le type de poste TAN et cliquez sur le bouton
 (Détail). Dans le
pilotage de la copie, il existe deux propositions de type de poste et deux types de
détermination du prix pour les corrections de factures. Ces entrées constituent la base
des postes d'avoir et de note de débit créés dans la demande de correction de facture.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 67

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Créer des documents de facturation dans la gestion des réclamations
Sujet: Création de documents de facturation dans la gestion des réclamations


## PDF page 68

Chapitre 4
Sujet 2
Création de factures pro forma et de vente au
comptant
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux deux types de documents de facturation spéciaux : la facture pro
forma et la facture de vente au comptant.
Exemple de gestion
Vous devez créer des factures pro forma pour les transactions de commerce extérieur. Vous
avez également besoin d'un type de document de facturation pour des ventes au comptoir, le
client réglant alors immédiatement et emportant lui-même la marchandise. Pour cette raison,
vous devez disposer des connaissances suivantes :
●
connaître le processus et les méthodes de contrôle des différentes opérations
commerciales possibles dans le contexte de la facturation.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Créer des factures pro forma et de vente au comptant
Factures pro forma
Figure 18: Factures pro forma


## PDF page 69

Les types de document de facturation correspondant à des factures pro forma sont
disponibles pour les transactions d'exportation.
Vous pouvez créer des factures pro forma à partir de commandes clients ou de livraisons.
Vous n'avez pas besoin d'enregistrer la sortie de marchandises avant de créer une facture pro
forma à partir d'une livraison.
Selon vos besoins, vous pouvez créer plusieurs factures pro forma, le statut facture n'étant
pas mis à jour dans le document de référence.
Les données des factures pro forma ne sont pas transmises au module Comptabilité
financière.
Astuce :
Dans le pilotage de la copie, la zone Quantité positive./négat. n'est pas accessible
en écriture afin d'éviter qu'une facture pro forma n'entraîne la mise à jour de la
quantité déjà facturée dans le document de référence.
Comment créer une facture pro forma
Create a pro forma invoice.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
Remarque :
Only you are using the Fiori Launch Pad you have the option to get the preview of
the output. Use the app Manage Billing Documents to get a Preview of the output.
1. Create a pro forma invoice for the order with purchase order number 00S4615-A1.
a) On the SAP Menu screen, choose Logistics →  Sales and Distribution →  Billing →
Billing Document →  Create .
b) Enter the order number. In the Default data screen area, select the billing type Pro
Forma for Order (F5).
c) Save the pro forma invoice.
2. Display the document flow and explain that the pro forma invoice does not create an
accounting document.
3. In Customizing for billing type Pro Forma for Order (F5) or Pro Forma for Delivery (F8),
display the account determination for the general ledger (G/L) account fields. They are
blank; therefore, no data is forwarded to accounting.
4. If necessary, display the Pos./neg. quantity field during copying control from TA to F5.
This field is not ready for input because changes would create discrepancies.
Sujet: Création de factures pro forma et de vente au comptant


## PDF page 70

Vente au comptant
Figure 19: Vente au comptant
La vente au comptant désigne un type de commande pour laquelle le client commande,
enlève les marchandises et paie pour ces marchandises immédiatement. La livraison est
traitée dès la saisie de la commande. Vous pouvez imprimer immédiatement une facture au
comptant à partir de la commande, de telle sorte que la facturation sera liée à la commande.
Aucune créance n'est générée pour le client comme c'est le cas pour les commandes clients
urgentes ou standard, car le montant de la facture est enregistré directement sur un compte
de caisse.
Lors d'une vente au comptant, le paiement a lieu au moment de la commande des
marchandises. La facture papier est également imprimée à cet instant précis.
Si le client a déjà reçu les marchandises, la livraison n'est pas pertinente pour le prélèvement.
Une fois les marchandises reçues par le client, la transaction est considérée comme terminée.
SAP vous recommande d'enregistrer la sortie de marchandises en arrière-plan à l'aide d'un
programme. Vous pouvez alors facturer la transaction ultérieurement. Vous utilisez le
processus de facturation créée à partir d'une commande client pour facturer la vente au
comptant, mais la facture n'est pas imprimée. Le numéro de commande client est utilisé
comme référence pour la pièce comptable créée dans la comptabilité financière.
Vente au comptant - Caractéristiques
La vente au comptant présente les caractéristiques suivantes :
●
La commande client et la livraison sont créées en une seule étape bien qu'elles donnent
lieu à deux documents.
●
Pour ne pas faire attendre le client, l'enregistrement de la sortie de marchandises peut
s'effectuer ultérieurement et fait l'objet d'une transaction distincte.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 71

La vente au comptant utilise le type de commande client BV. Ce dernier est associé au type de
message spécifique RD03 qui vous permet d'imprimer une facture papier à partir de la
commande client.
Vous pouvez créer le document de facturation réel ultérieurement, après avoir enregistré la
sortie de marchandises. Pour cela, utilisez le type de document de facturation BV.
Le paramétrage suivant est défini pour le type BV :
●
La facture est créée à partir d'une commande client.
●
Il n'existe aucune détermination des messages car l'impression a déjà été générée lors de
la commande client.
●
Il n'y a pas de nouvelle détermination du prix car le prix ne doit pas différer de celui figurant
sur la facture imprimée.
●
Dans la Comptabilité financière, le montant de la vente est imputé à un compte de caisse
et non à un compte client.
●
Le type de document de facturation SV sert à annuler les ventes au comptant.
Comment créer une facture de vente au comptant
Create a cash sale invoice.
1. Create an order with the following data:
Field
Data Value
Order Type
BV (cash sale)
Sales Organization
1000
Distribution Channel
Division
Sold-To Party
C615-D00
Material
P615-100
Order Quantity
1 PC
Be careful the display the message type RD03 does NOT work at the moment.
2. Post goods issue the delivery
3. Bill the document (order-related) with billing type BV (cash sales).
4. Using the document flow, go to the accounting document that has been created and show
that the transaction was posted in the petty cash account instead of the customer
account.
5. Show the Customizing settings required for this process for billing type BV (cash sales).
Sujet: Création de factures pro forma et de vente au comptant


## PDF page 72

Chapitre 4: Types de documents de facturation spéciaux


## PDF page 73

Chapitre 4
Exercice 5
Créer une facture de vente au comptant et une
facture pro forma
Exemple de gestion
Le client C615-D## achète un vélo référencé sous le numéro d'article P615-4##. Le client
souhaitant l'enlever immédiatement, il paie la facture directement. Vous devez donc savoir
comment créer une facture de vente au comptant.
Utilisez le type de document de facturation Vente au comptant pour traiter une vente au
comptant.
1. Accédez à la barre de lancement SAP Fiori. Si vous vous êtes déconnecté, lancez de
nouveau la barre de lancement SAP Fiori à partir du menu d'applications Microsoft
Windows.
2. Lancez la barre de lancement SAP Fiori et créez une commande avec les données
suivantes :
Zone
Valeur de données
Type de commande
BV (vente au comptant)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-D##
Réf. client
##S4615-BV
Article
P615-4##
Quantité d'ordre
1 pce
Notez le numéro de la commande :
Notez le numéro de livraison :
3. Quel message le système affiche-t-il après la sauvegarde de la commande client ?
4. Une dernière étape doit être effectuée dans le système pour créer le document de
facturation réel et transférer les données vers la comptabilité.


## PDF page 74

Laquelle ?
5. Veuillez exécuter cette étape d'enregistrement de la sortie de marchandises. Créez
ensuite le document de facturation pour transférer les données vers la comptabilité.
6. Vérifiez la pièce comptable.
Consultez la pièce comptable. Quels comptes ont été imputés et pourquoi ?
Création d'une facture pro forma
Exemple de gestion
Pour vos activités d'exportation, vous avez besoin d'établir une facture pour une commande
avant même de livrer le produit. Vous devez donc savoir comment créer une facture pro
forma et comment elle est configurée.
1. Utilisez la barre de lancement SAP Fiori et créez une commande avec les données
suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. client
##S4615-PF
Article
P615-2##
Quantité d'ordre
5 pces
Notez le numéro de la commande :
2. Avant même de livrer les articles, vous avez besoin d'établir une facture. Créez la facture
pro forma pour la commande.
3. Combien de pièces comptables obtenez-vous ? Pourquoi ?
4. Vérifiez ces options dans le Customizing du système backend.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 75

Chapitre 4
Solution 5
Créer une facture de vente au comptant et une
facture pro forma
Exemple de gestion
Le client C615-D## achète un vélo référencé sous le numéro d'article P615-4##. Le client
souhaitant l'enlever immédiatement, il paie la facture directement. Vous devez donc savoir
comment créer une facture de vente au comptant.
Utilisez le type de document de facturation Vente au comptant pour traiter une vente au
comptant.
1. Accédez à la barre de lancement SAP Fiori. Si vous vous êtes déconnecté, lancez de
nouveau la barre de lancement SAP Fiori à partir du menu d'applications Microsoft
Windows.
a) Si vous vous êtes déconnecté, cliquez sur
 Microsoft Windows et, pour afficher le
menu d'applications, cliquez sur
. Recherchez la barre de lancement SAP Fiori.
b) Pour lancer la barre de lancement SAP Fiori, cliquez sur l'entrée correspondante dans
la liste des applications.
c) Utilisez l'utilisateur S4615-## et le mot de passe fournis pour vous connecter.
2. Lancez la barre de lancement SAP Fiori et créez une commande avec les données
suivantes :
Zone
Valeur de données
Type de commande
BV (vente au comptant)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-D##
Réf. client
##S4615-BV
Article
P615-4##
Quantité d'ordre
1 pce
Notez le numéro de la commande :
Notez le numéro de livraison :
a) Accédez au groupe de vignettes Ventes (Sales) et lancez l'application Créer
commande client.


## PDF page 76

b) Saisissez les données comme indiqué dans la tâche et enfin, sélectionnez
Sauvegarder pour sauvegarder le document de vente au comptant.
c) Notez le numéro de la commande :
d) Notez le numéro de livraison :
3. Quel message le système affiche-t-il après la sauvegarde de la commande client ?
a) Le système affiche le message suivant :
La vente au comptant … a été sauvegardée (livraison … créée)
Une livraison a été créée en même temps que la commande client.
4. Une dernière étape doit être effectuée dans le système pour créer le document de
facturation réel et transférer les données vers la comptabilité.
Laquelle ?
Pour une vente de produit sur stock, vous devez procéder à l'enregistrement de la sortie
de marchandises.
5. Veuillez exécuter cette étape d'enregistrement de la sortie de marchandises. Créez
ensuite le document de facturation pour transférer les données vers la comptabilité.
a) Accédez au groupe de vignettes Livraison (Delivery) et lancez l'application Modifier
livraison sortante.
b) Entrez le numéro de livraison, sélectionnez Suite, puis Enreg. sortie march.
c) Dans les détails de la livraison, cliquez sur le bouton Enreg. sortie march. (si vous
ne le voyez pas, élargissez votre fenêtre d'écran). Enfin, sélectionnez Terminer et
fermez l'application.
d) Accédez au groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Création de documents de facturation (VF01).
e) Entrez le numéro de commande client comme document. Exécutez le programme et
sauvegardez le document.
6. Vérifiez la pièce comptable.
Consultez la pièce comptable. Quels comptes ont été imputés et pourquoi ?
Les comptes Caisse, Produit national - produit et TVA collectée ont été imputés. Dans le
type de document de facturation BV, il existe deux imputations : une pour la
comptabilisation des produits sur les comptes généraux et une sur le compte de caisse.
a) Pour afficher le document de facturation que vous venez de créer, sélectionnez
Afficher.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 77

b) Sélectionnez ensuite Gestion comptable.
c) Dans la Liste des pièces en gestion comptable, sélectionnez la Pièce comptable
correspondante et affichez-la.
d) Vous voyez maintenant les comptes Caisse, Produit national - produit et TVA
collectée.
e) Enfin, sélectionnez Terminer et fermez l'application.
Création d'une facture pro forma
Exemple de gestion
Pour vos activités d'exportation, vous avez besoin d'établir une facture pour une commande
avant même de livrer le produit. Vous devez donc savoir comment créer une facture pro
forma et comment elle est configurée.
1. Utilisez la barre de lancement SAP Fiori et créez une commande avec les données
suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. client
##S4615-PF
Article
P615-2##
Quantité d'ordre
5 pces
Notez le numéro de la commande :
a) Accédez au groupe de vignettes Ventes (Sales) et lancez l'application Créer
commande client.
b) Saisissez les données comme indiqué dans la tâche et sauvegardez le document de
vente en sélectionnant Sauvegarder.
c) Notez le numéro de la commande :
d) Enfin, sélectionnez Terminer ou fermez l'application.
2. Avant même de livrer les articles, vous avez besoin d'établir une facture. Créez la facture
pro forma pour la commande.
a) Accédez au groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Création de documents de facturation (VF01).
b) Saisissez le numéro de commande dans la zone Document et remplacez le type de
document de facturation par défaut par F5 Pro forma pour cde.
c) Exécutez le programme et sauvegardez le document.
Sujet: Création de factures pro forma et de vente au comptant


## PDF page 78

3. Combien de pièces comptables obtenez-vous ? Pourquoi ?
Aucune pièce comptable n'apparaît, car une facture pro forma ne transfère pas de
données vers la comptabilité.
4. Vérifiez ces options dans le Customizing du système backend.
a) Accédez au Customizing (code de transaction SPRO), dans le Guide d'implémentation
SAP Customizing : Administration des ventes (ADV)Facturation → Factures → Définir
les types de facture.
b) Sélectionnez Définir les types de facture.
c) Cliquez sur le bouton
 Positionner et saisissez le type de document de facturation
F5. Sélectionnez le type de document de facturation F5 et affichez les détails le
concernant.
d) Prêtez attention à la zone d'écran Déterminat.du compte/du prix : il n'existe aucune
option pour affecter le schéma détermination du compte, étant donné que la zone
Schéma de calcul pour la détermination des comptes est manquante.
Chapitre 4: Types de documents de facturation spéciaux


## PDF page 79

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Créer des factures pro forma et de vente au comptant
Sujet: Création de factures pro forma et de vente au comptant


## PDF page 80

Chapitre 4: Types de documents de facturation spéciaux


## PDF page 81

Chapitre 4
Évaluation des connaissances
1.
Parmi les étapes suivantes, laquelle devez-vous effectuer pour annuler un document de
facturation ?
Sélectionnez la réponse correcte.
A Créer un document d'annulation
B Supprimer la commande client
C Supprimer le document de facturation
D Créer une note de crédit
2. Vous pouvez annuler uniquement un document de facturation entier ; vous ne pouvez pas
annuler des postes un par un.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. De quelle manière pouvez-vous créer des demandes de notes de crédit et de débit ?
Sélectionnez les réponses correctes.
A sans référence à une opération commerciale précédente ;
B en référence à une commande client ;
C en référence à un numéro d'article ;
D en référence à un client.


## PDF page 82

4. Sur quoi devez-vous vous baser pour créer une demande de correction de facture ?
Sélectionnez la réponse correcte.
A Document de facturation
B Commande client
C Commande d'achat
D Demande d’achat
5. Parmi les affirmations suivantes, laquelle s'applique à une demande de correction de
facture ?
Sélectionnez les réponses correctes.
A Les postes sont automatiquement dupliqués et les types de postes créés ont des
valeurs +/- opposées.
B Les postes d'avoir et de note de débit peuvent être modifiés.
C Dans le document, seul le reste est énuméré et enregistré.
D Les notes de crédit et de débit peuvent être supprimées par paires et les paires de
postes non modifiés peuvent être supprimées en une seule fois.
6. Les documents de facturation de type facture pro forma sont-ils automatiquement
transmis au module Comptabilité financière ?
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
7.
Vous devez enregistrer la sortie de marchandises avant de créer une facture pro forma à
partir d'une livraison.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
Chapitre 4: Évaluation des connaissances


## PDF page 83

8. Parmi les affirmations suivantes, lesquelles sont vraies pour la vente au comptant ?
Sélectionnez les réponses correctes.
A La facture est créée à partir d'une livraison.
B Il y a toujours une nouvelle détermination du prix.
C Il n'existe aucune détermination des messages pour le document de facturation.
D Dans la Comptabilité financière, le montant de la vente est imputé à un compte de
caisse.
Chapitre 4: Évaluation des connaissances


## PDF page 84

Chapitre 4
Évaluation des connaissances - Réponses
1.
Parmi les étapes suivantes, laquelle devez-vous effectuer pour annuler un document de
facturation ?
Sélectionnez la réponse correcte.
A Créer un document d'annulation
B Supprimer la commande client
C Supprimer le document de facturation
D Créer une note de crédit
2. Vous pouvez annuler uniquement un document de facturation entier ; vous ne pouvez pas
annuler des postes un par un.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. De quelle manière pouvez-vous créer des demandes de notes de crédit et de débit ?
Sélectionnez les réponses correctes.
A sans référence à une opération commerciale précédente ;
B en référence à une commande client ;
C en référence à un numéro d'article ;
D en référence à un client.


## PDF page 85

4. Sur quoi devez-vous vous baser pour créer une demande de correction de facture ?
Sélectionnez la réponse correcte.
A Document de facturation
B Commande client
C Commande d'achat
D Demande d’achat
5. Parmi les affirmations suivantes, laquelle s'applique à une demande de correction de
facture ?
Sélectionnez les réponses correctes.
A Les postes sont automatiquement dupliqués et les types de postes créés ont des
valeurs +/- opposées.
B Les postes d'avoir et de note de débit peuvent être modifiés.
C Dans le document, seul le reste est énuméré et enregistré.
D Les notes de crédit et de débit peuvent être supprimées par paires et les paires de
postes non modifiés peuvent être supprimées en une seule fois.
6. Les documents de facturation de type facture pro forma sont-ils automatiquement
transmis au module Comptabilité financière ?
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
7.
Vous devez enregistrer la sortie de marchandises avant de créer une facture pro forma à
partir d'une livraison.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
Chapitre 4: Évaluation des connaissances - Réponses


## PDF page 86

8. Parmi les affirmations suivantes, lesquelles sont vraies pour la vente au comptant ?
Sélectionnez les réponses correctes.
A La facture est créée à partir d'une livraison.
B Il y a toujours une nouvelle détermination du prix.
C Il n'existe aucune détermination des messages pour le document de facturation.
D Dans la Comptabilité financière, le montant de la vente est imputé à un compte de
caisse.
Chapitre 4: Évaluation des connaissances - Réponses


## PDF page 87

CHAPITRE 5
Flux de données
Sujet 1
Configuration du flux de données pour les documents de facturation
Exercice 6: Configuration du flux de données pour les documents de facturation
OBJECTIFS DU CHAPITRE
●
Configurer le flux de données pour les documents de facturation


## PDF page 88

Chapitre 5
Sujet 1
Configuration du flux de données pour les
documents de facturation
VUE D'ENSEMBLE DU SUJET
Ce sujet explique les différents impératifs en matière de facturation qui varient d'un
processus de gestion à un autre (en fonction des circonstances selon lesquelles est autorisée
une facturation, en fonction de la quantité à facturer ou de la détermination du prix de vente).
Comme les nouveaux documents de facturation, établis dans le cadre de foires, font l'objet de
différents impératifs, ce sujet vous présentera les options permettant de configurer le flux de
données.
Exemple de gestion
Vos commerciaux doivent pouvoir obtenir rapidement et simplement des informations sur la
chaîne de processus et les statuts des documents individuels. Lorsque vous facturez des
ventes réalisées lors d'une foire, vous souhaitez reprendre les éléments de prix saisis dans la
commande, alors que les frais de transport doivent être redéterminés dans la facture. À cet
effet, vous devez disposer des connaissances suivantes :
●
connaître les documents pouvant servir de base à la création du document de facturation ;
●
connaître la façon dont le flux de documents est représenté dans la chaîne de processus ;
●
connaître les différentes sources des données du document de facturation ;
●
connaître les impératifs à satisfaire pour permettre l'exécution de la facturation ;
●
connaître les différents paramètres de contrôle dans la structure du pilotage de la copie.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Configurer le flux de données pour les documents de facturation


## PDF page 89

Processus de facturation
Figure 20: Processus de facturation
Tout document de facturation doit avoir un document de référence (exception : facturation de
transactions externes).
Ces documents de référence peuvent être les suivants :
●
Document de vente
●
Livraison sortante
●
Document de facturation
Pour effectuer la facturation, vous devez saisir le numéro du document de référence en tant
que transaction à facturer.
Document de référence
Tableau 1: Type de document de référence pour chaque document de facturation
Le tableau suivant énumère le type de document de référence pour chaque document de
facturation :
Document de facturation
Document de référence
Facture
Document de vente ou livraison
Avoir
Demande d'avoir ou document de facturation
Note de débit
Demande de note de débit ou document de
facturation
Avoir sur retours
Document de retours
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 90

Document de facturation
Document de référence
Avoir
Demande de correction de facture
Facture pro forma
Document de vente ou livraison
Annulation de facture
Document de facturation
Annulation avoir
Avoir
Relevé de factures
Documents de facturation
Transaction externe pour document de fac-
turation
Transaction externe
Facturation interne
Livraison
Avoir lié à une ristourne
Demande de ristourne
Pour créer un document de facturation, vous devez toujours faire référence à un document
existant.
Le système reprend alors les données du document de référence dans le document de
facturation.
Si vous facturez à partir d'une livraison, ceci vous permet par exemple de reprendre la
quantité à facturer à partir de la livraison, tandis que les prix proviendront de la commande
client liée.
Le document de référence apparaît en tant que source au niveau de l'en-tête dans la table de
pilotage de la copie.
Flux de données
Figure 21: Flux de données
Chapitre 5: Flux de données


## PDF page 91

Vous pouvez, dans une certaine mesure, adapter le flux de données entre les documents de
référence et les documents de facturation.
Pour ce faire, utilisez :
●
les types de document de facturation (par exemple pour les textes et les partenaires) ;
●
Pilotage de la copie
Les options de pilotage sont les suivantes :
●
L'en-tête comporte des données du commerce extérieur, les numéros d'affectation et de
référence et les numéros de postes.
●
La quantité et la détermination du prix figurent au niveau du poste.
Vous pouvez également utiliser des routines de reprise des données pour adapter le flux de
données à vos impératifs spécifiques. Ceci vous permet par exemple de reprendre les
conditions de paiement à partir de la fiche client et non du document de vente précédent.
Pilotage de la copie
Figure 22: Pilotage de la copie
L'administrateur système peut définir comment les données sont transférées au processus
de facturation dans la table de pilotage de la copie.
Il détermine les contrôles :
●
de l'en-tête ;
La cible est le type de document de facturation et la source est le type de document de
vente.
●
du poste.
La cible est le type de document de facturation et la source est le type de document de
vente et le type de poste.
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 92

Règles de contrôle disponibles au niveau de l'en-tête/du poste
Règles de contrôle au niveau de l'en-tête :
●
Document de référence pouvant être utilisé comme référence pour la facturation ;
●
Détermination des données du commerce extérieur, des numéros d'affectation et de
référence et des numéros de poste.
Règles de contrôle au niveau du poste :
●
Quantité facturée
Quelle est la quantité à facturer : la quantité commandée ou la quantité livrée ?
●
Détermination du prix et taux de change
Faut-il redéterminer les prix ou reprendre les prix de la commande client ? Quel est le taux
de change à appliquer ?
●
Source du prix
De quel document proviennent les conditions indiquées dans le document de facturation
(par exemple, reprise des coûts de transports du document de frais de transport) ?
Conditions de copie
Figure 23: Conditions de copie
Vous pouvez définir les conditions pour la facturation d'un document de vente dans le
pilotage de la copie.
Vous pouvez déterminer des conditions de copie pour l'en-tête et le poste.
Elles vous permettent par exemple d'indiquer si l'enregistrement de la sortie de marchandises
doit s'effectuer avant la facturation.
Vous pouvez définir vos propres conditions à l'aide de la transaction VOFM.
Comment afficher le pilotage de la copie
Demonstrate data flow and copying control.
Chapitre 5: Flux de données


## PDF page 93

1. Navigate to Customizing for Sales and Distribution under Billing →  Billing Documents →
Maintain Copying Control for Billing Documents. Select Copying control: Delivery document
to billing document.
2. Demonstrate copying control at header level for target F2 and source LF.
3. Demonstrate copying control at item level for target F2, source LF, and item category
TAN.
4. Demonstrate copying requirements at header level for target F2 and source LF.
Demonstrate the possible entry routines in the Copying requirements field. If necessary,
go to the source text for routine 3 to explain how the GI status is called. Using routine 011,
you can bill without the GI having been posted first.
5. Demonstrate copying requirements at item level for target F2 and source LF, and item
category TAN.
Astuce :
The routine in the Data VBRK/VBRP field determines how the fields in the
billing document are to be filled.
Quantité facturée
Tableau 2: Quantité facturée dans les différents documents de facturation
Le tableau suivant explique la façon dont est déterminée la quantité facturée dans les
différents documents de facturation :
Document de facturation
Quantité facturée
Basé sur une commande client (ex. : com-
mande standard)
●
Quantité commandée moins quantité déjà
facturée
●
Quantité déjà livrée moins quantité déjà
facturée
Basé sur une demande d'avoir
Quantité commandée moins quantité déjà
facturée
Basé sur une livraison (ex. : types de docu-
ment de facturation F1 et F2)
Quantité déjà livrée moins quantité déjà fac-
turée
Facture pro forma F5
Quantité commandée
Facture pro forma F8
Quantité livrée
La facturation utilise les quantités livrées et commandées. Vous pouvez également prendre
en compte la quantité déjà facturée (suivant le cas). Les exemples du tableau ci-dessus sont
définis dans la version standard du système.
De cette manière, vous pouvez par exemple créer un document de facturation à partir d'une
commande client pour des quantités déjà livrées.
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 94

Comment sélectionner la quantité pertinente pour la facturation
Choose the quantity relevant for billing.
1. Demonstrate the quantity to be billed for item category TAN.
2. Demonstrate copying control from target LF to source F2 with item category TAN.
3. Demonstrate copying control from target LF to source F8 with item category TAN.
Détermination du prix
Figure 24: Vue d'ensemble de la détermination du prix
Le système détermine un schéma de calcul basé sur les données de documents. Le schéma
de document est défini dans le type de document de vente
Le schéma de calcul comporte des types de conditions définis selon une séquence
appropriée. Ces types de conditions définissent les différents éléments de la détermination
du prix, comme les prix, les remises pour offres spéciales, les majorations de frais de
transport, etc.
Une séquence d'accès est définie pour chaque type de condition. Elle détermine la stratégie
de recherche que le système utilise pour la recherche d'enregistrements de conditions
valables.
Pour chaque accès, les données du document sont utilisées pour permettre au système de
rechercher des enregistrements de condition valables dans le fichier des conditions.
Vous pouvez utiliser des barèmes dans des enregistrements de conditions.
Lorsqu'il détermine un enregistrement de condition valable, le système utilise le nombre de
pièces ou la valeur du poste pour trouver le prix ou la remise correspondants, qu'il applique
ensuite dans le document.
Chapitre 5: Flux de données


## PDF page 95

Le système applique ce processus pour chaque type de condition inclus dans le schéma de
calcul.
Détermination du prix dans le document de facturation
Figure 25: Détermination du prix dans le document de facturation
Le tableau suivant décrit les types de détermination de prix que vous pouvez définir pour
les postes au moment de la facturation :
Type de détermination du prix
Description
A
Le système reprend les éléments de prix à
partir du document de référence et les met à
jour en fonction d'un barème.
B
La détermination du prix est exécutée à nou-
veau.
Le système reprend les éléments de prix ma-
nuels et détermine à nouveau le prix des au-
tres.
Le système reprend sans les modifier les élé-
ments de prix du document de référence.
G
Le système reprend sans les modifier les élé-
ments de prix du document de référence. Il
détermine à nouveau les conditions de taxes.
H
Le système reprend sans les modifier les élé-
ments de prix du document de référence. Les
frais de transport sont redéterminés.
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 96

Pour chaque type de document de facturation et chaque type de poste, l'administrateur
système peut affecter un type de détermination du prix ou en définir de nouveaux.
Il peut également spécifier la manière dont le taux doit être déterminé.
Comment utiliser certains types de détermination du prix pour la facturation
Use pricing types for billing.
1. Display the pricing condition record for material P620-100 using the transaction VK13 .
Use the following data:
Field
Data Value
Condition type
PR00
Key Combination
Material with release status
Sales Organization
1010
Distribution Channel
For the validity period, the price increase is before the start of course (initiated via CATT).
2. Create order of order type OR. Set the pricing date in the past so that the prices before the
price increase are included in the order. Use the following data:
Field
Data Value
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C620-A00
Cust. Reference
6-Price
Pricing date
<Last week>
Material
P620-100
Order Quantity
10 PC
3. Create a delivery document use shipping point 1010, do the pick and post goods issue for
the delivery.
4. Create billing document (delivery-related), but do not save default billing type F2 invoice.
Go to the pricing screen. Price is taken from the order (previous price). The reason is
pricing type G in copying control for F2.
5. Create the billing document (delivery-related) again. Change default billing type to F1
invoice. Go to the pricing screen. Price is taken from the current date (today). The reason
is pricing type C in copying control for F1.
Chapitre 5: Flux de données


## PDF page 97

Chapitre 5
Exercice 6
Configuration du flux de données pour les
documents de facturation
Exemple de gestion
En règle générale, vous utilisez le type de document de facturation Facture F2 pour vos
commandes clients. Ce type reprend directement de la commande le prix, les majorations et
les remises. Toutefois, selon un accord passé avec le client, vous devez redéterminer
complètement les prix lors de la facturation. Par ailleurs, pour la facturation de commandes
prises à l'occasion d'une foire, vous souhaitez reprendre les prix à partir de la commande
client mais calculer à nouveau les frais de transport. Vous devez donc savoir comment
satisfaire les différentes exigences de la facturation à effectuer.
Facturation d'une livraison créée antérieurement
1. Connectez-vous au système backend. Utilisez le menu SAP.
2. Facturez la livraison de la commande client qui a pour référence la commande d'achat n
° ##S4615-A5.
Astuce :
Exécutez le programme ; ne sauvegardez pas.
Quel est le type de document de facturation utilisé ?
3. Quel prix est défini pour le premier produit P615-1## (type de condition du prix article
PR00) ?
4. Dans ce cas précis, vous souhaitez utiliser le Type de facture Facture F1 pour facturer.
Comment devez-vous procéder ? Effectuez les étapes nécessaires.


## PDF page 98

5. Quel prix (type de condition PR00) est utilisé maintenant pour le produit P615-1## ?
Sauvegardez la facture.
Vous souhaitez déterminer de nouveau les conditions des frais de transport lors de la
facturation de votre commande Foire ZA##. Procédez à un test et définissez les options du
Customizing nécessaires.
1. Créez tout d'abord une commande client prise à l'occasion d'une foire (type de
commande client ZA##) et utilisez les données suivantes :
Zone
Valeur de données
Type de commande
ZA##
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-D##
Réf. Client
##fret
Article
P615-1## (1 pce)
Notez le prix final calculé.
Prix (zone d'en-tête Valeur nette) dans votre commande client : ______________________
Créez la livraison avec le point d'expédition 1010. Exécutez le prélèvement et
l'enregistrement de la sortie de marchandises.
Notez le numéro de livraison à facturer ultérieurement.
Numéro de livraison : ______________________
2. Indiquez que vous souhaitez reprendre les prix de la commande client, mais recalculer
(redéterminer) les frais de transport pour votre type de document de facturation Foire
ZF## et le type de poste TAN associé au type de livraison LF.
Accédez au Customizing du pilotage de la copie pour les documents de facturation.
Affectez à votre type de facture ZF## et au type de poste TAN associé au type de livraison
LF, la routine de détermination du prix approprié de façon à ce que les prix soient repris de
la commande client, mais que les frais de transport soient redéterminés.
3. Dans le Menu SAP, appelez les détails du partenaire pour votre client C615-D## dans le
domaine commercial (1010/10/00).
Menu SAP : Logistique →  Administration des ventes (ADV) →  Données de base →
Partenaire →  Client →  Afficher →  Administration des ventes (ADV)
Saisissez vos données client C615-D## et l'organisation commerciale 1010, le canal de
distribution 10 et le secteur d'activité 00
Chapitre 5: Flux de données


## PDF page 99

Accédez à l'onglet Facture et notez les incoterms (parties 1 et 2) pour votre client C615-
D##.
4. Créez un enregistrement de conditions des frais de transport avec le type de condition
KF00 et les Incoterms parties 1 et 2 pour votre client C615-D##. Vous souhaitez facturer
10 EUR par kg.
5. Analysez le résultat du paramétrage effectué ci-dessus en facturant la livraison de votre
commande Foire que vous venez de créer.
Quel est le prix final ?
Notez le prix final calculé à l'instant.
Prix (zone d'en-tête Valeur nette) dans le document de facturation : ___________
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 100

Chapitre 5
Solution 6
Configuration du flux de données pour les
documents de facturation
Exemple de gestion
En règle générale, vous utilisez le type de document de facturation Facture F2 pour vos
commandes clients. Ce type reprend directement de la commande le prix, les majorations et
les remises. Toutefois, selon un accord passé avec le client, vous devez redéterminer
complètement les prix lors de la facturation. Par ailleurs, pour la facturation de commandes
prises à l'occasion d'une foire, vous souhaitez reprendre les prix à partir de la commande
client mais calculer à nouveau les frais de transport. Vous devez donc savoir comment
satisfaire les différentes exigences de la facturation à effectuer.
Facturation d'une livraison créée antérieurement
1. Connectez-vous au système backend. Utilisez le menu SAP.
2. Facturez la livraison de la commande client qui a pour référence la commande d'achat n
° ##S4615-A5.
Astuce :
Exécutez le programme ; ne sauvegardez pas.
Quel est le type de document de facturation utilisé ?
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Vente →  Commande client →  Afficher.
b) Pour lancer la recherche, utilisez l'aide à la saisie (F4) dans la zone Commande client.
Dans l'onglet Documents de vente par numéro de commande chez client, dans la zone
N° commande d'achat, saisissez ##S4615-A5. Confirmez votre saisie et sélectionnez
le document dans la liste.
c) Accédez au flux de documents en sélectionnant Environnement →  Afficher flux doc.
Notez le numéro de livraison, puis quittez la transaction.
Numéro de livraison :
d) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
e) Entrez la livraison à facturer et exécutez le programme. La livraison est facturée à
l'aide du type de document de facturation Facture (F2). Ne sauvegardez PAS le
document, passez simplement à la prochaine étape de l'exercice.


## PDF page 101

3. Quel prix est défini pour le premier produit P615-1## (type de condition du prix article
PR00) ?
a) Sélectionnez le premier poste, puis cliquez sur
 (Conditions poste). Le prix du
produit est de 1 400 EUR.
b) Quittez la transaction sans sauvegarder en sélectionnant
 Terminer.
4. Dans ce cas précis, vous souhaitez utiliser le Type de facture Facture F1 pour facturer.
Comment devez-vous procéder ? Effectuez les étapes nécessaires.
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Facturation →  Facture →  Créer.
b) Dans la zone d'écran Données par défaut, dans la zone Type de facture, sélectionnez
Facture (F1). Entrez la livraison à facturer et exécutez le programme.
5. Quel prix (type de condition PR00) est utilisé maintenant pour le produit P615-1## ?
Sauvegardez la facture.
a) Sélectionnez le poste, puis cliquez sur
 (Conditions poste). Le prix du produit est de
1 700 EUR.
b) Sauvegardez votre facture.
Vous souhaitez déterminer de nouveau les conditions des frais de transport lors de la
facturation de votre commande Foire ZA##. Procédez à un test et définissez les options du
Customizing nécessaires.
1. Créez tout d'abord une commande client prise à l'occasion d'une foire (type de
commande client ZA##) et utilisez les données suivantes :
Zone
Valeur de données
Type de commande
ZA##
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-D##
Réf. Client
##fret
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 102

Zone
Valeur de données
Article
P615-1## (1 pce)
Notez le prix final calculé.
Prix (zone d'en-tête Valeur nette) dans votre commande client : ______________________
Créez la livraison avec le point d'expédition 1010. Exécutez le prélèvement et
l'enregistrement de la sortie de marchandises.
Notez le numéro de livraison à facturer ultérieurement.
Numéro de livraison : ______________________
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Vente →  Commande client →  Créer.
b) Saisissez le type de commande ZA## avec l'organisation commerciale 1010, le canal
de distribution 10 et le secteur d'activité 00. Saisissez les données restantes comme
indiqué dans la tâche et enfin, sauvegardez la commande client.
Donneur d'ordre
C615-D##
Réf. Client
##fret
Article
P615-1##
Quantité d'ordre
Notez le numéro de la commande : _______________________________
c) Dans le Menu SAP, sélectionnez Expédition et transport →  Livraison
sortante → Créer →  Document individuel →  Avec référence à la commande client.
d) Saisissez le point d'expédition 1010. Saisissez la date de sélection comme suit : <date
du jour + 10 jours>. Confirmez vos entrées.
e) Accédez à l'onglet Prélèvement et saisissez la Quantité prélevée 1 (elle doit être égale à
la quantité livrée).
f) Cliquez sur le bouton Enregistrer sortie de marchandises. Après l'enregistrement de la
sortie de marchandises, votre livraison est automatiquement sauvegardée.
g) Notez le numéro de livraison.
Numéro de livraison : __________________
2. Indiquez que vous souhaitez reprendre les prix de la commande client, mais recalculer
(redéterminer) les frais de transport pour votre type de document de facturation Foire
ZF## et le type de poste TAN associé au type de livraison LF.
Accédez au Customizing du pilotage de la copie pour les documents de facturation.
Affectez à votre type de facture ZF## et au type de poste TAN associé au type de livraison
LF, la routine de détermination du prix approprié de façon à ce que les prix soient repris de
la commande client, mais que les frais de transport soient redéterminés.
a) Dans le système backend SAP, utilisez le menu Favoris et sélectionnez l'entrée du
Customizing (code de transaction SPRO).
Chapitre 5: Flux de données


## PDF page 103

b) Accédez au Customizing, puis, dans le Guide d'implémentation, sélectionnez :
Administration des ventes (ADV) sous Facturation →  Factures →  Gérer la régie de la
copie pour les factures.
c) Sélectionnez Pilotage copie : document de livraison après facture et cliquez sur le
bouton
 Sélectionner.
d) Sélectionnez
 (Afficher → Modifier) pour passer en mode de modification.
e) Cliquez sur le bouton
 Positionner et saisissez ZF## comme Type de facture et LF
comme Type de livraison.
f) Sélectionnez votre entrée et double-cliquez sur Poste dans Structure de dialogue.
g) Cliquez sur le bouton
 Positionner et saisissez le type de poste TAN.
h) Sélectionnez TAN et cliquez sur
 (Détail).
i) Entrez le type de détermination du prix H (H = Redéfinir les conditions frais de
transport) et cliquez sur Sauvegarder.
3. Dans le Menu SAP, appelez les détails du partenaire pour votre client C615-D## dans le
domaine commercial (1010/10/00).
Menu SAP : Logistique →  Administration des ventes (ADV) →  Données de base →
Partenaire →  Client →  Afficher →  Administration des ventes (ADV)
Saisissez vos données client C615-D## et l'organisation commerciale 1010, le canal de
distribution 10 et le secteur d'activité 00
Accédez à l'onglet Facture et notez les incoterms (parties 1 et 2) pour votre client C615-
D##.
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Données de base →  Partenaire →  Client →  Afficher →  Administration des ventes
(ADV).
b) Saisissez le client C615-D##, l'organisation commerciale 1010, le canal de distribution
10 et le secteur d'activité 00. Confirmez vos entrées.
c) Dans les données du domaine commercial, sélectionnez la page d'onglet Facture. La
valeur dans la zone Incoterms est CFR et ## (votre numéro de groupe) s'affiche à côté.
Les incoterms de votre client sont donc CFR ## (partie 1 : CFR et partie 2 : ## = votre
numéro de groupe).
4. Créez un enregistrement de conditions des frais de transport avec le type de condition
KF00 et les Incoterms parties 1 et 2 pour votre client C615-D##. Vous souhaitez facturer
10 EUR par kg.
a) Dans le menu SAP, sélectionnez Logistique  →  Administration des ventes (ADV)  →
Données de base  →  Conditions  →  Sélection via type de condition  →  Créer.
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 104

b) Saisissez le type de condition KF00 et cliquez sur le bouton Combinaison-clé. Cliquez
sur le bouton : Incoterms (partie 1+2) et confirmez votre saisie.
c) Saisissez les données suivantes :
Zone
Valeur de données
Incoterms
CFR
Incoterms 2
## (votre numéro de groupe)
Montant
Unité
EUR
par
Unité Quantité
KG
d) Confirmez vos entrées et cliquez sur
 Sauvegarder.
5. Analysez le résultat du paramétrage effectué ci-dessus en facturant la livraison de votre
commande Foire que vous venez de créer.
Quel est le prix final ?
Notez le prix final calculé à l'instant.
Prix (zone d'en-tête Valeur nette) dans le document de facturation : ___________
a) Dans le Menu SAP, sélectionnez Logistique →  Administration des ventes (ADV) →
Facturation →  Facture →  Créer.
b) Confirmez le numéro du document de livraison et exécutez le programme.
Sélectionnez le poste, puis cliquez sur
 (Conditions poste). Le prix est rehaussé à
1 900 EUR.
Suite aux modifications effectuées dans le pilotage de la copie, la majoration des frais
de transport est maintenant appliquée au tarif de 10 EUR par KG (type de condition
KF00). Le type de facture par défaut utilisé pour facturer des livraisons de
commandes clients de type ZA## prises à l'occasion d'une foire correspond à ZF##,
car vous l'avez paramétré dans un exercice précédent.
Chapitre 5: Flux de données


## PDF page 105

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Configurer le flux de données pour les documents de facturation
Sujet: Configuration du flux de données pour les documents de facturation


## PDF page 106

Chapitre 5: Flux de données


## PDF page 107

Chapitre 5
Évaluation des connaissances
1.
Comment pouvez-vous créer un document de facturation ?
Sélectionnez les réponses correctes.
A Vous ne pouvez pas créer de document de facturation sans un document de
référence existant.
B Vous pouvez créer de document de facturation sans un document de référence
existant.
C Vous pouvez utiliser n'importe quel document de référence pour un document de
facturation à tout moment, comme pour la création d'une commande client.
D Vous pouvez utiliser un document de référence uniquement pour un document de
facturation pour lequel il existe une entrée de pilotage de la copie.
2. Parmi les options suivantes du pilotage de la copie, quelles sont celles disponibles au
niveau du poste ?
Sélectionnez les réponses correctes.
A Quantité facturée
B Détermination du prix
C Attribution de numéro de poste
D Critère de tri
3. Parmi les quantités facturées suivantes, laquelle s'applique à la facture pro forma F8 ?
Sélectionnez la réponse correcte.
A Quantité livrée
B Quantité commandée
C Quantité commandée moins quantité déjà facturée
D Quantité déjà livrée moins quantité déjà facturée


## PDF page 108

Chapitre 5
Évaluation des connaissances - Réponses
1.
Comment pouvez-vous créer un document de facturation ?
Sélectionnez les réponses correctes.
A Vous ne pouvez pas créer de document de facturation sans un document de
référence existant.
B Vous pouvez créer de document de facturation sans un document de référence
existant.
C Vous pouvez utiliser n'importe quel document de référence pour un document de
facturation à tout moment, comme pour la création d'une commande client.
D Vous pouvez utiliser un document de référence uniquement pour un document de
facturation pour lequel il existe une entrée de pilotage de la copie.
2. Parmi les options suivantes du pilotage de la copie, quelles sont celles disponibles au
niveau du poste ?
Sélectionnez les réponses correctes.
A Quantité facturée
B Détermination du prix
C Attribution de numéro de poste
D Critère de tri
3. Parmi les quantités facturées suivantes, laquelle s'applique à la facture pro forma F8 ?
Sélectionnez la réponse correcte.
A Quantité livrée
B Quantité commandée
C Quantité commandée moins quantité déjà facturée
D Quantité déjà livrée moins quantité déjà facturée


## PDF page 109

CHAPITRE 6
Création de documents de
facturation
Sujet 1
Création de documents de facturation de différentes façons
Exercice 7: Créer des documents de facturation de différentes façons
OBJECTIFS DU CHAPITRE
●
Créer des documents de facturation de différentes façons


## PDF page 110

Chapitre 6
Sujet 1
Création de documents de facturation de
différentes façons
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux différentes options (par exemple celles fournies par l'échéancier de
factures et la facturation en arrière-plan) vous permettant de créer des documents de
facturation dans l'Administration des ventes. Il vous explique également comment vous
pouvez créer des documents de facturation destinés à certains clients et uniquement pour
des dates spécifiques.
Exemple de gestion
La création des factures s'effectue en général une fois par jour. Mais si un client le souhaite,
vous devez facturer les transactions réalisées dans le mois en cours à la fin du mois
seulement. Pour cette raison, vous devez disposer des connaissances suivantes :
●
connaître les différentes façons de créer des documents de facturation ;
●
connaître l'utilité de l'échéancier de factures pour créer des documents de facturation via
une opération de facturation groupée ;
●
connaître l'option de création de factures à des dates spécifiques ;
●
connaître les différentes étapes pour annuler une opération de facturation groupée.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Créer des documents de facturation de différentes façons


## PDF page 111

Facturation à la demande
Figure 26: Facturation à la demande
Vous pouvez indiquer explicitement les documents à facturer. À cet effet, saisissez
manuellement les numéros de documents. Vous saisissez le numéro de commande client si
vous voulez facturer à partir d'une commande client ou le numéro du bon de livraison si vous
voulez facturer à partir d'une livraison.
Si la création d'un document de facturation est impossible, par exemple en raison d'un
blocage de la facture, le système édite un journal des erreurs.
Vous pouvez également sélectionner des postes individuels ou des quantités partielles des
postes à facturer lors de la facturation des livraisons ou des commandes. Pour ce faire,
sélectionnez la fonction Liste de sélection dans la facturation. Lors d'une facturation à partir
d'une livraison, vous ne pouvez modifier les quantités de postes que pour les types de poste
dont la pertinence facture est K.
Sujet: Création de documents de facturation de différentes façons


## PDF page 112

Échéancier de factures
Figure 27: Traitement des échéanciers de factures
En règle générale, vous n'allez pas facturer les transactions une par une. Vous serez plus
vraisemblablement amené à exécuter des opérations groupées périodiques (par exemple,
après l'enregistrement de la sortie de marchandises).
Si vous utilisez l'échéancier, vous devez spécifier le périmètre de la sélection (par exemple,
donneur d'ordre, date de la facture ou pays destinataire). Le système se base sur ce
périmètre pour regrouper les transactions à facturer.
Vous pouvez également spécifier si l'échéancier doit afficher seulement les commandes à
facturer, les livraisons à facturer, ou les deux.
Dans notre exemple, la création de documents de facturation est limitée aux livraisons
effectuées avant le 15 mai pour le donneur d'ordre C1. Le système se base sur ces critères
pour sélectionner la réserve de travail et crée des documents de facturation lors du
traitement de l'échéancier de factures.
Options de facturation
Options de facturation disponibles :
●
Document de facturation individuel
Un document de facturation individuel est créé pour tous les documents sélectionnés dans
l’échéancier de factures. Aucun regroupement n’est effectué. Vous appelez la transaction
VF01 pour chaque document sélectionné.
●
Document de facturation groupé
Tous les documents sélectionnés dans l’échéancier de factures sont facturés. Le système
essaie de les regrouper au mieux. Le traitement des documents sélectionnés s'effectue en
Chapitre 6: Création de documents de facturation


## PDF page 113

arrière-plan. Vous revenez à l’échéancier de factures après avoir traité les documents. Les
icônes vous informent de la réussite ou de l’échec de la facturation des documents.
●
Document de facturation groupé en ligne
Le système appelle la fonction Créer facture (transaction VF01). Les documents sont
regroupés dans la mesure du possible en fonction des critères habituels.
Vous pouvez traiter l'échéancier de factures en mode de simulation. Le système affiche les
documents de facturation sans les sauvegarder. Les transactions contenant des erreurs sont
désignées via le statut de traitement approprié.
Comment traiter des échéanciers de factures
Process the billing due list.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. In the SAP Menu choose Logistics  →  Sales and Distribution  →  Billing  →  Billing
Document  →  Process Billing Due List .
2. Enter billing date from <first day of previous month> to <today>. Enter sold-to party
C615-B00 and select the Delivery-related checkbox.
3. Choose the
 DisplayBillList button. Choose
 ( Simulation ). Two billing documents
were created.
4. Choose the
 Log button. An outbound delivery is blocked for billing. Do not save.
Sujet: Création de documents de facturation de différentes façons


## PDF page 114

Facturation à des dates spécifiques
Figure 28: Création de factures à des dates spécifiques
Vous pouvez opter pour un traitement périodique des factures. Ceci vous permet de
regrouper au sein d'un même document toutes les livraisons pour lesquelles la facturation est
échue à une date donnée.
Pour ce faire, vous devez procéder comme suit :
●
Gérer des dates de facture individuelles dans le calendrier d'entreprise au moyen de règles
spéciales
●
Entrer le calendrier d'entreprise dans la fiche client du payeur (Dates de facturation dans
l'onglet Facture)
Lorsque vous créez un document, le système reprend la date de facture suivante issue du
calendrier d'entreprise comme date de la facture dans la facture générée.
Comment créer des factures à des dates spécifiques
Create an invoice on a specific date.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. In Customizing, display calendar AM for monthly invoice creation.
2. Define the factory calendar AM in the customer master for customer number C615-B00,
sales organization 1010, distribution channel 10, and division 00. In the Invoice dates field,
enter calendar AM .
Chapitre 6: Création de documents de facturation


## PDF page 115

3. Create an order of order type OR. Use the following data:
Field
Data Value
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-B00
Cust Reference
7-2
Material
P615-100
Order Quantity
10 PC
Go to the billing screen header of the order and display the billing date set there (end of
the month) on the basis of the invoice calendar.
4. Deliver the order using shipping point 1010 do the pick and post goods issue for the
delivery
5. Bill the document with reference to delivery with billing type F2.
6. Display the billing due list for customer C615-B00 again. Enter billing date from <first day
of previous month> to <last day of the previous month>. Enter sold-to party C615-B00
and select the Delivery-related checkbox. The outbound delivery just created appears in
the index with the billing date at the end of the month. Do not save unless you do not want
to show background billing.
Traitement en arrière-plan
Figure 29: Facturation en arrière-plan
Sujet: Création de documents de facturation de différentes façons


## PDF page 116

Vous pouvez utiliser un job d'arrière-plan pour créer des factures, ce processus étant
pratique et efficace.
Vous pouvez lancer automatiquement le job d'arrière-plan de diverses manières :
●
Périodiquement (par exemple, tous les lundis à 2 heures)
●
À une date et une heure spécifiques (par exemple, le 19 juin à 8 heures)
Le système peut diviser l'échéancier de factures en plusieurs jobs d'arrière-plan et les lancer
simultanément. Ceci vous assure une utilisation optimisée de votre matériel informatique
grâce à l'exploitation de plusieurs processeurs.
Si vous n'avez pas besoin d'un protocole ni d'informations détaillées, SAP vous recommande
de désactiver ces options dans l'écran de sélection. Cela vous permet d'améliorer les
performances du système.
Annulation
Figure 30: Annulation d'opération de facturation groupée
Vous pouvez annuler une opération de facturation groupée.
Tous les documents de facturation sont annulés dans une opération de facturation groupée.
Le système regroupe tous les documents de facturation annulés sous un numéro d'opération
groupée de type S que vous pouvez afficher via Document de facturation → Protocole.
Vous pouvez ensuite refacturer les documents précédents pour le document de facturation
annulé.
Seuls les utilisateurs disposant de l'autorisation nécessaire peuvent annuler des opérations
de facturation groupée.
Astuce :
Pour annuler une opération de facturation groupée, sélectionnez
Facturation → Système d'information → Factures → Protocole de l'opération
groupée. Cliquez sur les boutons de commande Documents, puis Annuler tout.
Chapitre 6: Création de documents de facturation


## PDF page 117

Comment annuler des opérations de facturation groupées
Cancel a collective billing run.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Call up the log for the collective run you created before in order to cancel it. Choose
Logistics →  Sales and Distribution →  Billing →  Information system →  Billing
Documents →  Log of Collective Run .
2. Select them by entering shipping point 1010 and started by <name according to system
logon>. For scope of list, select the With notes checkbox, the With created documents
checkbox, and the Without cancelled runs checkbox.
3. Select the log of the collective run you started before and choose the Documents button.
4. Cancel the collective run by choosing the Reverse all button. You can only cancel all the
documents in a collective run.
5. To demonstrate that all the documents in the collective run have been canceled, you can
display the billing due list for customer C615-B00 again.
Utilisation des applications de facturation
Les applications suivantes offrent des options supplémentaires pour la facturation : Création
de documents de facturation - Postes d'échéancier de factures et Gestion des documents de
facturation offrent des options supplémentaires de facturation.
Figure 31: Applications de facturation - Autres options de facturation
Outre la méthode traditionnelle pour créer un document de facturation via les transactions
VF01 et VF04, vous disposez d'une application SAP Fiori intitulée Création de documents de
facturation - Postes d'échéancier de factures. L'application SAP Fiori Création de documents
de facturation - Postes d'échéancier de factures met à votre disposition un plus grand nombre
de filtres et d'options de sélection. Lorsque vous utilisez l'application Création de documents
Sujet: Création de documents de facturation de différentes façons


## PDF page 118

de facturation - Postes d'échéancier de factures, vous avez la possibilité de définir des
Options de facture et ainsi de déterminer comment se déroule le processus de facturation.
Vous pouvez définir des options de facture pour que le système effectue automatiquement
les tâches suivantes lors de la création de documents de facturation :
• Saisissez la date de la facture et le type de document de facturation avant la facturation.
Si vous activez cette option et décidez de créer des documents de facturation, le système
demande une date de facture et le type de document de facturation requis avant de créer
des documents de facturation.
• Créer un document de facturation distinct pour chaque poste d'échéancier de factures.
Si vous activez cette option et décidez de créer des documents de facturation, le système
crée des documents de facturation distincts pour chaque poste de l'échéancier de
factures sélectionné.
• Enregistrer automatiquement les documents de facturation. Le système enregistre
automatiquement les documents de facturation que vous créez dans la comptabilité et
déclenche un message (par exemple, une facture par e-mail). Notez que si vous choisissez
de ne pas enregistrer automatiquement vos documents de facturation, vous devrez les
enregistrer manuellement à l'aide de l'application Gestion des documents de facturation.
• Afficher les documents de facturation après leur création. Le système génère et affiche
les documents de facturation temporaires relatifs aux documents commerciaux
sélectionnés pour la facturation. Vous avez alors la possibilité de les sauvegarder ou de les
rejeter. Si vous les sauvegardez, ils sont convertis en documents de facturation finaux,
tandis que si vous les rejetez, vous êtes redirigés vers l'échéancier de factures.
Dans l'application Création de documents de facturation - Postes d'échéancier de factures,
vous pouvez désormais générer et afficher les documents de facturation temporaires avant
de les convertir en documents de facturation finaux. Si toutes les données apparaissant dans
le document de facturation temporaire sont correctes, vous pouvez poursuivre et créer le
document de facturation final en une seule étape. Si vous remarquez une erreur, vous pouvez
rejeter le document de facturation temporaire et recommencer. Vous n'êtes plus contraint
d'annuler les documents de facturation qui ont été créés avec des informations incorrectes,
ce qui s'avère un gain de temps et d'énergie. Cette fonctionnalité permet également de
réduire les discontinuités dans la séquence des numéros de document de facturation. En
d'autres termes, peu de numéros dans la tranche de numéros des documents de facturation
sont gaspillés.
Application Gestion des documents de facturation
En outre, vous disposez de l'application SAP Fiori Gestion des documents de facturation pour
examiner les documents de facturation. Cette application vous permet de gérer les factures,
les factures annulées, les avoirs et autres documents de facturation. Elle inclut des fonctions
d'affichage, de modification, d'enregistrement et d'annulation des documents de facturation.
Vous pouvez également générer des aperçus avant impression de vos documents de
facturation au format PDF.
Vous pouvez sélectionner plusieurs documents de facturation pour les afficher
simultanément. Dans ce cas, le système vous permet de naviguer rapidement entre les
documents de facturation sélectionnés. Vous pouvez afficher et modifier les informations
d’une facture après l’avoir affichée. Pour afficher une synthèse des détails d'un document de
facturation, cliquez sur le numéro de ce document dans la liste. Cette action permet d'afficher
la page d’objet du document de facturation correspondant.
Chapitre 6: Création de documents de facturation


## PDF page 119

Chapitre 6
Exercice 7
Créer des documents de facturation de
différentes façons
Exemple de gestion
Pour sélectionner les documents à traiter via le processus de facturation, votre entreprise
utilise normalement une opération de facturation groupée définie par un périmètre de
sélection plutôt que de traiter chaque facture individuellement. Vous avez convenu avec
certains de vos clients de bloquer toutes les factures pour le mois en cours et de ne les
envoyer qu'à la fin du mois. Vous devez donc savoir comment créer des documents de
facturation en utilisant différentes méthodes.
Création de documents de facturation
1. Accédez au système backend et consultez les options de facturation. Cette fois-ci, vous
souhaitez utiliser l'échéancier de factures.
2. Affichez l'échéancier de factures (code de transaction VF04) pour votre client C615-B##
et sélectionnez la facturation créée à partir d'une livraison (date de la facture définie au
début du mois dernier).
Quelle est la date de facture spécifiée pour les trois livraisons figurant dans l'échéancier ?
3. Créez les documents de facturation pour l'échéancier de factures.
4. Notez le(s) numéro(s) des documents de facturation créés.
Créer automatiquement des documents de facturation basés sur des dates de
facturation convenues
Vous souhaitez créer automatiquement des documents de facturation pour le client C615-
B## chaque fin de mois.
1. Vous devez d'abord gérer l'accord avec votre client. Par conséquent, modifiez les données
de base du client C615-B## pour que toutes les factures à venir soient désormais créées à
la fin de chaque mois.
Utilisez le système backend pour cette partie de l'exercice.
2. Maintenant, votre client C615-B## commande deux pièces de l'article P615-2##. Créez
une commande client standard (type de commande CDCL) avec la référence client ##-
mois.


## PDF page 120

Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-B##
Réf. client
##-mois
Article
P615-2##
Quantité d'ordre
3. Créez la livraison pour cette commande client et effectuez le prélèvement et
l'enregistrement de la sortie de marchandises.
Notez le numéro de livraison.
Numéro de document : _________________________
4. Affichez l'échéancier de factures pour le client C615-B##, sélectionnez la facturation
créée à partir d'une livraison et créez la facture pour votre client.
Astuce :
Sélectionnez la date de facture allant du premier jour au dernier jour du mois
en cours.
Quelle est la date spécifiée pour la livraison que vous venez de créer ?
5. Vous avez utilisé l'échéancier de factures deux fois. Veuillez consulter le protocole de
l'opération groupée des documents de facturation.
Vous souhaitez annuler votre première opération groupée où vous avez facturé trois
livraisons.
Affichez le protocole de l'opération groupée pour l'utilisateur S4615-##. Si nécessaire,
saisissez votre utilisateur dans la zone Lancé par : S4615-# # et cliquez sur Exécuter.
Sélectionnez le groupe dans lequel vous avez créé les trois documents, puis cliquez sur le
bouton Documents. Les détails du protocole s'affichent. Annulez les trois documents de
facturation à la fois, en sélectionnant Annuler tout.
6. Dans un geste de bonne volonté, vous avez convenu avec votre client d’utiliser le donneur
d'ordre C615-B## pour définir la date de facturation <à la fin du mois> pour toutes les
livraisons arrivées à échéance. Par conséquent, vous avez simplement annulé tous les
documents de facturation, pour pouvoir recommencer à zéro. Facturez à nouveau à votre
donneur d'ordre C615-B##, mais cette fois-ci saisissez une date de facture par défaut :
<fin du mois>. Examinez les documents de facturation à la fin.
Chapitre 6: Création de documents de facturation


## PDF page 121

Découverte des applications de facturation
1. Cette fois, vous souhaitez utiliser les applications Fiori pour la facturation. Découvrez les
autres options de facturation avec les applications Création de documents de facturation -
Postes d'échéancier de factures et Gestion des documents de facturation.
Lancez la barre de lancement SAP Fiori. Si vous avez fermé la barre de lancement SAP
Fiori, appelez-la à partir du menu d'applications Microsoft Windows, avec l'utilisateur
S4615-## et le mot de passe qui vous ont été fournis.
2. Accédez au groupe de vignettes Sales (Ventes) et créez une commande client.
3. Utilisez les données suivantes pour créer une commande client standard :
Zone
Valeur
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Zone
Valeur
Donneur d'ordre
C615-A##
Réf. client
##-app-1
DateLivrSouh.
<dans une semaine>
Article
P-Service
Quantité d’ordre
Notez le numéro de la commande : ___________________________
4. Facturez la commande que vous venez de créer, mais cette fois-ci utilisez les applications
Fiori Création de documents de facturation - Postes d'échéancier de factures.
Ouvrez l'application Création de documents de facturation - Postes d'échéancier de
factures.
Dans les zones de filtre, supprimez l’entrée de la zone Date de facturation jusqu'au et
saisissez C615-A## comme Donneur d'ordre.
N’apportez aucune modification aux
 Options de facture. Votre nouveau document
de facturation ne sera pas automatiquement enregistré dans le module Comptabilité
financière. N’apportez aucune modification à cette caractéristique.
Sauvegardez votre document de facturation et notez son numéro.
Numéro de document de facturation : ______________________
5. Quel est le statut du document de facturation que vous venez de créer ? Consultez le flux
de processus. Quel est le contenu de la zone Écriture comptable ? Pour cette partie de
l'exercice, utilisez l'application Gestion des documents de facturation.
6. Annulez le document de facturation que vous venez de créer.
Sujet: Création de documents de facturation de différentes façons


## PDF page 122

7. Appelez votre dernière commande client avec la Réf. client ##-app-1 et définissez la
Quantité d’ordre sur 8.
8. Facturez à nouveau votre commande à l’aide des applications Fiori Création de documents
de facturation - Postes d'échéancier de factures.
Sauvegardez votre nouveau document de facturation et notez son numéro.
Numéro de document de facturation : ______________________
9. Enfin, enregistrez votre document de facturation dans la comptabilité financière.
Consultez le flux de processus. Quel es le contenu de la zone Écriture comptable ?
Chapitre 6: Création de documents de facturation


## PDF page 123

Chapitre 6
Solution 7
Créer des documents de facturation de
différentes façons
Exemple de gestion
Pour sélectionner les documents à traiter via le processus de facturation, votre entreprise
utilise normalement une opération de facturation groupée définie par un périmètre de
sélection plutôt que de traiter chaque facture individuellement. Vous avez convenu avec
certains de vos clients de bloquer toutes les factures pour le mois en cours et de ne les
envoyer qu'à la fin du mois. Vous devez donc savoir comment créer des documents de
facturation en utilisant différentes méthodes.
Création de documents de facturation
1. Accédez au système backend et consultez les options de facturation. Cette fois-ci, vous
souhaitez utiliser l'échéancier de factures.
a) Accédez au système backend et utilisez le Menu SAP.
2. Affichez l'échéancier de factures (code de transaction VF04) pour votre client C615-B##
et sélectionnez la facturation créée à partir d'une livraison (date de la facture définie au
début du mois dernier).
Quelle est la date de facture spécifiée pour les trois livraisons figurant dans l'échéancier ?
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures (code de transaction
VF04).
b) Saisissez la date de facture du <début du mois dernier> au <date du jour>. Saisissez
C615-B## comme donneur d'ordre et cochez la case Lié à livraison.
c) Cliquez sur le bouton
 Afficher l'échéancier de factures. Sauf configuration
supplémentaire, la date de facture coïncide avec la date d'enregistrement de sortie de
marchandises des livraisons. Dans cette formation, la date de facture tombera
probablement la veille ou le premier jour du cours.
3. Créez les documents de facturation pour l'échéancier de factures.
a) Dans l'écran Traiter échéancier de factures, sélectionnez les trois lignes et cliquez sur
 Sauvegarder.


## PDF page 124

4. Notez le(s) numéro(s) des documents de facturation créés.
a) Sélectionnez l'opération groupée que vous avez créée et cliquez sur le bouton
Documents pour afficher les documents de facturation individuels.
Créer automatiquement des documents de facturation basés sur des dates de
facturation convenues
Vous souhaitez créer automatiquement des documents de facturation pour le client C615-
B## chaque fin de mois.
1. Vous devez d'abord gérer l'accord avec votre client. Par conséquent, modifiez les données
de base du client C615-B## pour que toutes les factures à venir soient désormais créées à
la fin de chaque mois.
Utilisez le système backend pour cette partie de l'exercice.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Données de base → Partenaire → Client → Modifier → Administration des
ventes (ADV).
b) Saisissez le donneur d'ordre C615-B##, l'organisation commerciale 1010, le canal de
distribution 10 et le secteur d'activité 00. Confirmez vos entrées.
c) Assurez-vous d'utiliser la vue Données du domaine commercial.
d) Sélectionnez l'onglet Facture, puis dans la zone Dates de facturation, entrez le
calendrier AM pour un décompte mensuel.
e) Sauvegardez vos entrées.
2. Maintenant, votre client C615-B## commande deux pièces de l'article P615-2##. Créez
une commande client standard (type de commande CDCL) avec la référence client ##-
mois.
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-B##
Réf. client
##-mois
Article
P615-2##
Quantité d'ordre
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.
Chapitre 6: Création de documents de facturation


## PDF page 125

b) Saisissez le type de commande CDCL pour la commande client standard et les
données du domaine commercial (1010/10/00). Saisissez tous les autres détails
comme indiqué dans la tâche et enfin, sauvegardez votre commande.
3. Créez la livraison pour cette commande client et effectuez le prélèvement et
l'enregistrement de la sortie de marchandises.
Notez le numéro de livraison.
Numéro de document : _________________________
a) Dans le Menu SAP, sélectionnez Expédition et transport →  Livraison
sortante → Créer →  Document individuel →  Avec référence à la commande client.
b) Saisissez le point d'expédition 1010. Saisissez la date de sélection comme suit : <date
du jour + 10 jours>. Confirmez vos entrées.
c) Accédez à l'onglet Prélèvement et saisissez la Quantité prélevée 2 (elle doit être égale à
la quantité livrée).
d) Cliquez sur le bouton Enregistrer sortie de marchandises. Après l'enregistrement de la
sortie de marchandises, votre livraison est automatiquement sauvegardée.
e) Notez le numéro de livraison.
Numéro de document : _________________________
4. Affichez l'échéancier de factures pour le client C615-B##, sélectionnez la facturation
créée à partir d'une livraison et créez la facture pour votre client.
Astuce :
Sélectionnez la date de facture allant du premier jour au dernier jour du mois
en cours.
Quelle est la date spécifiée pour la livraison que vous venez de créer ?
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures (code de transaction
VF04).
b) Saisissez la date de facture du <début du mois> à la <fin du mois>.
c) Saisissez le donneur d'ordre C615-B## et cochez la case Lié à livraison. La date de
facturation spécifiée correspond à la fin du mois.
 Bouton Afficher l'échéancier de
factures.
d) Dans Traiter échéancier de factures, sélectionnez
 Sauvegarder et créez le
document de facturation.
5. Vous avez utilisé l'échéancier de factures deux fois. Veuillez consulter le protocole de
l'opération groupée des documents de facturation.
Vous souhaitez annuler votre première opération groupée où vous avez facturé trois
livraisons.
Sujet: Création de documents de facturation de différentes façons


## PDF page 126

Affichez le protocole de l'opération groupée pour l'utilisateur S4615-##. Si nécessaire,
saisissez votre utilisateur dans la zone Lancé par : S4615-# # et cliquez sur Exécuter.
Sélectionnez le groupe dans lequel vous avez créé les trois documents, puis cliquez sur le
bouton Documents. Les détails du protocole s'affichent. Annulez les trois documents de
facturation à la fois, en sélectionnant Annuler tout.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Système d'information → Factures → Protocole de l'opération
groupée (code de transaction V.21).
b) Si nécessaire, saisissez votre utilisateur dans la zone Lancé par : S4615-## et cliquez
sur
 Exécuter.
c) Sélectionnez le groupe dans lequel vous avez créé les trois documents, puis cliquez
sur le bouton Documents. Les détails du protocole s'affichent. Annulez les trois
documents de facturation à la fois, en sélectionnant Annuler tout.
d) Une fenêtre pop-up s'ouvre, posant la question : “Opération groupée...
Annuler ? ”Sélectionnez l'option de réponse Oui (bouton o).
6. Dans un geste de bonne volonté, vous avez convenu avec votre client d’utiliser le donneur
d'ordre C615-B## pour définir la date de facturation <à la fin du mois> pour toutes les
livraisons arrivées à échéance. Par conséquent, vous avez simplement annulé tous les
documents de facturation, pour pouvoir recommencer à zéro. Facturez à nouveau à votre
donneur d'ordre C615-B##, mais cette fois-ci saisissez une date de facture par défaut :
<fin du mois>. Examinez les documents de facturation à la fin.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures (code de transaction
VF04).
b) Saisissez la date de facture du <début du mois dernier> à la <date du jour>.
c) Saisissez le donneur d'ordre C615-B## et cochez la case Lié à livraison.
d) Sélectionnez l'onglet Données par défaut et saisissez la Date de facturation : <fin du
mois>.
e) Cliquez sur le bouton
 Afficher l'échéancier de factures.
f) Dans Traiter échéancier de factures, sélectionnez
 Sauvegarder et créez le
document de facturation.
g) Examinez le journal et vérifiez la date de facturation des documents de facturation que
vous venez de créer.
Découverte des applications de facturation
1. Cette fois, vous souhaitez utiliser les applications Fiori pour la facturation. Découvrez les
autres options de facturation avec les applications Création de documents de facturation -
Postes d'échéancier de factures et Gestion des documents de facturation.
Lancez la barre de lancement SAP Fiori. Si vous avez fermé la barre de lancement SAP
Fiori, appelez-la à partir du menu d'applications Microsoft Windows, avec l'utilisateur
S4615-## et le mot de passe qui vous ont été fournis.
Chapitre 6: Création de documents de facturation


## PDF page 127

a) Accédez à la barre de lancement SAP Fiori. Si vous avez fermé la barre de lancement
SAP Fiori, rappelez-la. Sélectionnez Microsoft Windows
 et, pour afficher le menu
d’applications, cliquez sur
 et recherchez la barre de lancement SAP Fiori.
b) Lancez la barre de lancement SAP Fiori.
2. Accédez au groupe de vignettes Sales (Ventes) et créez une commande client.
a) Accédez au groupe de vignettes :Sales (Ventes) et lancez l'application Création de
commandes clients.
3. Utilisez les données suivantes pour créer une commande client standard :
Zone
Valeur
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Zone
Valeur
Donneur d'ordre
C615-A##
Réf. client
##-app-1
DateLivrSouh.
<dans une semaine>
Article
P-Service
Quantité d’ordre
Notez le numéro de la commande : ___________________________
a) Saisissez les données indiquées dans le tableau ci-dessus.
b) Enfin, sauvegardez votre commande client en sélectionnant Sauvegarder.
c) Notez le numéro de la commande.
Numéro de commande : _________________________
4. Facturez la commande que vous venez de créer, mais cette fois-ci utilisez les applications
Fiori Création de documents de facturation - Postes d'échéancier de factures.
Ouvrez l'application Création de documents de facturation - Postes d'échéancier de
factures.
Dans les zones de filtre, supprimez l’entrée de la zone Date de facturation jusqu'au et
saisissez C615-A## comme Donneur d'ordre.
N’apportez aucune modification aux
 Options de facture. Votre nouveau document
de facturation ne sera pas automatiquement enregistré dans le module Comptabilité
financière. N’apportez aucune modification à cette caractéristique.
Sauvegardez votre document de facturation et notez son numéro.
Numéro de document de facturation : ______________________
Sujet: Création de documents de facturation de différentes façons


## PDF page 128

a) Sélectionnez le groupe de vignettes Documents de facturation (Billing Documents),
lancez l'application Création de documents de facturation - Postes d'échéancier de
factures.
b) Définissez le filtre pour la facturation, supprimez l’entrée de la zone Date de facturation
jusqu'au puis, dans la zone Donneur d'ordre, saisissez C615-A##.
c) Appuyez sur Entrée pour confirmer votre entrée et pour lancer la sélection.
d) Laissez les
 Options de facture telles quelles. N'effectuez aucune modification.
e) Sélectionnez votre commande dans l'échéancier de factures.
f) Cliquez sur Créer.
g) La facture créée s’affiche automatiquement avec le Statut Temporaire.
h) Cliquez sur Sauvegarder.
i) Notez le numéro du document de facturation.
Numéro de document de facturation : ______________________
5. Quel est le statut du document de facturation que vous venez de créer ? Consultez le flux
de processus. Quel est le contenu de la zone Écriture comptable ? Pour cette partie de
l'exercice, utilisez l'application Gestion des documents de facturation.
a) Sélectionnez le groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Gestion des documents de facturation.
b) Dans la zone de recherche, saisissez le <numéro de votre document de
facturation>, assurez-vous que la zone Date de facturation jusqu'au est vide et
confirmez votre saisie en appuyant sur Entrée.
c) Dans la liste des documents de facturation, <votre document de facturation>
apparaît avec le statut À enregistrer.
d) Sélectionnez votre document de facturation, puis cliquez sur > à la fin de la ligne.
e) Faites défiler le contenu jusqu'à la zone d'écran Flux de processus.
Quel est le contenu de la zone Écriture comptable ? Réponse : Aucune écriture
comptable.
f) Restez dans cet écran et passez à l'étape suivante.
6. Annulez le document de facturation que vous venez de créer.
a) Sélectionnez Annuler un document de facturation.
b) Dans la boîte de dialogue : Annuler un document de facturation, cliquez sur OK.
c) Fermez la vue de document de facturation et sélectionnez
 Accueil.
7. Appelez votre dernière commande client avec la Réf. client ##-app-1 et définissez la
Quantité d’ordre sur 8.
a) Accédez au groupe de vignettes :Sales (Ventes) et lancez l'application Gestion des
commandes clients.
Chapitre 6: Création de documents de facturation


## PDF page 129

b) Saisissez la Réf. Client : ##-app-1 dans la zone de recherche et cliquez sur Lancer.
c) Sélectionnez votre commande, puis ouvrez l'ordre. Pour cela, cliquez sur > à la fin de la
ligne.
d) Cliquez sur Modifier.
e) Définissez la Quantité d’ordre sur 8.
f) Cliquez sur Sauvegarder, puis sur Terminer.
8. Facturez à nouveau votre commande à l’aide des applications Fiori Création de documents
de facturation - Postes d'échéancier de factures.
Sauvegardez votre nouveau document de facturation et notez son numéro.
Numéro de document de facturation : ______________________
a) Sélectionnez le groupe de vignettes Documents de facturation (Billing Documents),
lancez l'application Création de documents de facturation - Postes d'échéancier de
factures.
b) Définissez le filtre pour la facturation, supprimez l’entrée de la zone Date de facturation
jusqu'au puis, dans la zone Donneur d'ordre, saisissez C615-A##.
c) Appuyez sur Entrée pour confirmer votre entrée et pour lancer la sélection.
d) Sélectionnez votre commande dans l'échéancier de factures.
e) Cliquez sur Créer.
La facture créée s’affiche automatiquement avec le Statut Temporaire.
f) Cliquez sur Sauvegarder.
g) Notez le numéro du document de facturation.
Numéro de document de facturation : ______________________
h) Restez dans cet écran et passez à l'étape suivante.
9. Enfin, enregistrez votre document de facturation dans la comptabilité financière.
Consultez le flux de processus. Quel es le contenu de la zone Écriture comptable ?
a) Sélectionnez Enregistrer document de facturation.
a) Faites défiler le contenu jusqu'à la zone d'écran Flux de processus.
Quel est le contenu de la zone Écriture comptable ?
Vous disposez maintenant d’une pièce comptable et d’une écriture comptable avec un
numéro d'écriture et le statut Non rapproché.
Vos documents de facturation précédents (la première facture et la facture annulée)
ne possèdent pas d’écriture comptable.
Sujet: Création de documents de facturation de différentes façons


## PDF page 130

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Créer des documents de facturation de différentes façons
Chapitre 6: Création de documents de facturation


## PDF page 131

Chapitre 6
Évaluation des connaissances
1.
Vous souhaitez créer une facture. Quelles sont les options disponibles ?
Sélectionnez la réponse correcte.
A Vous pouvez utiliser l'échéancier de factures pour créer une facture.
B Vous devez utiliser l'interface « Facturation générale » pour créer une facture.
C Vous ne pouvez créer des documents de facturation individuels que
manuellement.
D Vous devez utiliser le traitement en arrière-plan.


## PDF page 132

Chapitre 6
Évaluation des connaissances - Réponses
1.
Vous souhaitez créer une facture. Quelles sont les options disponibles ?
Sélectionnez la réponse correcte.
A Vous pouvez utiliser l'échéancier de factures pour créer une facture.
B Vous devez utiliser l'interface « Facturation générale » pour créer une facture.
C Vous ne pouvez créer des documents de facturation individuels que
manuellement.
D Vous devez utiliser le traitement en arrière-plan.


## PDF page 133

CHAPITRE 7
Méthodes de facturation
Sujet 1
Analyse du regroupement et de la ventilation de factures
Exercice 8: Analyser le regroupement et la ventilation de factures
Exercice 9: Interprétation des raisons incitant à ventiler une facture
Sujet 2
Définition de relevés de factures
Sujet 3
Facturation convergente omnicanal
OBJECTIFS DU CHAPITRE
●
Analyser le regroupement et la ventilation de factures
●
Interpréter les raisons incitant à ventiler une facture
●
Définir des relevés de factures
●
Demandes de documents de facturation externes (EBDR)


## PDF page 134

Chapitre 7
Sujet 1
Analyse du regroupement et de la ventilation
de factures
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux options fournies par les différentes méthodes que vous pouvez
utiliser pour la facturation dans l'Administration des ventes. Dans cette optique, vous
découvrirez les factures groupées et les raisons incitant à ventiler automatiquement une
facture.
Exemple de gestion
Un de vos clients souhaite recevoir une seule facture pour toutes les transactions le
concernant. Un autre client vous demande de lui facturer chaque transaction séparément.
Pour cette raison, vous devez disposer des connaissances suivantes :
●
connaître les différentes méthodes de facturation ;
●
connaître les raisons incitant à ventiler une facture.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Analyser le regroupement et la ventilation de factures
●
Interpréter les raisons incitant à ventiler une facture


## PDF page 135

Document de facturation groupé
Figure 32: Document de facturation groupé
En règle générale, le système essaie de regrouper toutes les opérations compatibles entre
elles dans un même document de facturation.
Dans le système SAP, vous pouvez inclure dans un même document de facturation des
postes créés à partir d'une commande client et des postes créés à partir d'une livraison.
Comment créer un document de facturation groupé
Demonstrate collective billing documents.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. On the SAP Easy Access screen, choose Logistics →  Sales and Distribution →  Billing →
Billing Document →  Process Billing Due List .
2. Restrict the selection by specifying the billing date from <first day of the month> to < end
of the month >.
3. Enter sold-to party C615-C00 and select the Delivery-related checkbox.
4. On the Default Data tab page, select Invoice (F1) as the billing type.
5. Display the billing due list.
6. Choose
 ( Simulation ). One invoice is created.
Sujet: Analyse du regroupement et de la ventilation de factures


## PDF page 136

Chapitre 7: Méthodes de facturation


## PDF page 137

Chapitre 7
Exercice 8
Analyser le regroupement et la ventilation de
factures
Exemple de gestion
Vous voulez intégrer les commandes clients et les livraisons correspondantes à un même
document de facturation dans votre entreprise. Cette méthode permet de réduire
considérablement le nombre de factures créées. Vous devez donc connaître les critères sur
lesquels repose le regroupement de factures.
Analyse du regroupement et de la ventilation de factures
Accédez au système backend et utilisez le Menu SAP.
1. Affichez l'échéancier de factures pour le client C615-C##. Vous utilisez la facturation
créée à partir d'une livraison. Dans l'onglet Données déf., sélectionnez le type de
document de facturation Facture (F1). La facturation doit s'effectuer à compter du 1er jour
du mois.
2. Exécutez le processus de facturation en mode simulation (ne sauvegardez PAS).
Combien de factures le système crée-t-il et pourquoi ?
3. À quel niveau l'attribution des numéros de postes et les incréments correspondants sont-
ils générés ?
Utilisez une
 nouvelle fenêtre GUI pour examiner les options du Customizing.
4. Revenez à l'échéancier de factures en sélectionnant l'autre fenêtre SAP GUI. Ne
sauvegardez PAS.
Notez le numéro de la seconde livraison dans l'échéancier de factures. Quittez la
transaction sans sauvegarder.
Numéro de document :


## PDF page 138

Ne sauvegardez PAS. Sélectionnez uniquement
 Terminer.
Chapitre 7: Méthodes de facturation


## PDF page 139

Chapitre 7
Solution 8
Analyser le regroupement et la ventilation de
factures
Exemple de gestion
Vous voulez intégrer les commandes clients et les livraisons correspondantes à un même
document de facturation dans votre entreprise. Cette méthode permet de réduire
considérablement le nombre de factures créées. Vous devez donc connaître les critères sur
lesquels repose le regroupement de factures.
Analyse du regroupement et de la ventilation de factures
Accédez au système backend et utilisez le Menu SAP.
1. Affichez l'échéancier de factures pour le client C615-C##. Vous utilisez la facturation
créée à partir d'une livraison. Dans l'onglet Données déf., sélectionnez le type de
document de facturation Facture (F1). La facturation doit s'effectuer à compter du 1er jour
du mois.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures.
b) Limitez la sélection en définissant la date de facture du <premier jour du mois dernier>
à la <date du jour>.
c) Saisissez le donneur d'ordre C615-C## et cochez la case Lié à livraison.
d) Dans l'onglet Données déf., sélectionnez le type de document de facturation F1
Facture (F1).
e) Affichez l'échéancier de factures, en sélectionnant Afficher l'échéancier de factures.
2. Exécutez le processus de facturation en mode simulation (ne sauvegardez PAS).
Combien de factures le système crée-t-il et pourquoi ?
a) Cliquez sur
 (Simulation). Le système a créé une facture comprenant quatre postes
car les données du document de facturation sont identiques pour les deux livraisons.
Vous pouvez donc les regrouper.
3. À quel niveau l'attribution des numéros de postes et les incréments correspondants sont-
ils générés ?


## PDF page 140

Utilisez une
 nouvelle fenêtre GUI pour examiner les options du Customizing.
a) Cliquez sur
 Nouvelle fenêtre GUI.
b) À partir de vos Favoris, sélectionnez Customizing (code de transaction SPRO) et
cliquez sur le bouton du Customizing Guide de référence SAP. Dans le Guide
d'implémentation, sélectionnez : Administration des ventes
(ADV) → Facturation → Factures → Définir les types de facture.
c) Sélectionnez l'activité Définir les types de facture et cliquez sur le bouton
Sélectionner.
d) Cliquez sur
 Positionner et entrez le type de document de facturation F1 Facture
(F1), puis cliquez sur
 Détail. La zone Incrément Nº poste n'étant pas renseignée, le
système applique un incrément de 1.
4. Revenez à l'échéancier de factures en sélectionnant l'autre fenêtre SAP GUI. Ne
sauvegardez PAS.
Notez le numéro de la seconde livraison dans l'échéancier de factures. Quittez la
transaction sans sauvegarder.
Numéro de document :
Ne sauvegardez PAS. Sélectionnez uniquement
 Terminer.
a) Revenez à l'autre fenêtre SAP GUI, dans l'écran Traiter échéancier de factures.
b) Si vous avez fermé la session de votre dernière fenêtre, dans le Menu SAP,
sélectionnez : Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures.
c) Limitez la sélection en définissant la date de facture du <premier jour du mois dernier>
à la <date du jour>.
d) Saisissez le donneur d'ordre C615-C## et cochez la case Lié à livraison.
e) Dans la page d'onglet Données déf., sélectionnez Facture (F1) comme type de
document de facturation.
f) Affichez l'échéancier de factures et notez le numéro de la seconde livraison.
g) Numéro de document de la seconde livraison :
h) Quittez la transaction en cliquant simplement sur
 Terminer. Ne sauvegardez
PAS.
Chapitre 7: Méthodes de facturation


## PDF page 141

Ventilation de facture
Figure 33: Ventilation automatique de facture
Si les données ou les partenaires figurant dans l'en-tête du document sont différents, le
système procède automatiquement à une ventilation de la facture.
Tous les partenaires et autres informations figurant dans l'en-tête du document de
facturation peuvent entraîner la ventilation d'une facture. Exemple : si les conditions de
paiement dans les deux commandes client sont différentes comme dans la figure.
Ventilation de facture liée au poste
Figure 34: Ventilation de facture liée au poste
Sujet: Analyse du regroupement et de la ventilation de factures


## PDF page 142

L'administrateur système peut définir des conditions de ventilation supplémentaires dans le
Customizing du pilotage de la copie afin d'empêcher le système de regrouper des documents
de vente dans un document de facturation.
Exemple : une ventilation peut être basée sur le groupe de marchandises ou le centre de
profit.
Le système utilise la zone VBRK-ZUKRI dans l'en-tête de facture pour mémoriser ces critères
de ventilation supplémentaires.
Il affiche les zones à l'origine d'une ventilation dans l'analyse de cette ventilation.
Documents de facturation individuels
Figure 35: Documents de facturation individuels
Vous pouvez paramétrer le système SAP pour qu'il crée un document de facturation par
document de vente.
Pour ce faire, sélectionnez la routine de reprise des données 3 dans le Customizing pour le
pilotage de la copie (le numéro du document de référence est défini dans la zone VBRK-
ZUKRI).
Comment forcer une ventilation de facture automatique
Create an automatic invoice split.
1. Create an order of type OR. Use the following data:
Field
Data Value
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
Cust. Reference
8-2
Chapitre 7: Méthodes de facturation


## PDF page 143

Field
Data Value
Material
P615-100 ( 10 PC )
P615-200 ( 10 PC )
Go to the second item and change the terms of payment to ZB02 .
2. Create a deliver for the order using shipping point 1010. Do the pick and post goods issue.
3. Select the billing type Invoice (F1) on the Default Data tab page.
4. Enter billing date from <first day of the month> to <end of the month>. Enter sold-to party
C615-A00 and select the Delivery-related checkbox.
5. Display the billing due list.
6. Select only the delivery that has just been created and choose
 ( Simulation ).
7. Select the two billing documents and choose the Split analysis pushbutton. The different
header fields are terms of payment key.
Comment effectuer une ventilation de facture liée au poste
Create an item-dependent invoice split.
1. Demonstrate the Data VBRK/VBRP field in copying control with the appropriate example
routine for an invoice split in Customizing.
2. Select Copying control: Delivery document to billing document . Select target F1 , source
LF , and item category TAN .
3. Go to the source text for routine 1 (invoice split (sample)) in the Data VBRK/VBRP field to
explain how the VBRK-ZUKRI field is filled. The long text for the field information can also
help you explain the field.
Comment garantir des documents de facturation individuels
Ensure individual billing documents.
1. Display routine 3 (single invoice) in the Data VBRK/VBRP field and explain the setting of
the number of the preceding document in the VBRK-ZUKRI field in the source text. The
long text for field information can also be shown here to help you explain the field.
2. Store routine 3 (single invoice) in copying control from delivery type LF to billing type
ZF20 (item category TAN), so that a separate billing document is created for each sales
document for trade fair billing documents.
Sujet: Analyse du regroupement et de la ventilation de factures


## PDF page 144

Chapitre 7: Méthodes de facturation


## PDF page 145

Chapitre 7
Exercice 9
Interprétation des raisons incitant à ventiler
une facture
Exemple de gestion
Vous avez parfois besoin de modifier manuellement les conditions de paiement au niveau de
la commande client en fonction de l'accord passé avec votre client. Vous souhaitez analyser
l'impact de telles modifications sur la facturation. Pour la facturation liée à une foire, vous
voulez également pouvoir créer un document de facturation individuel pour chaque livraison.
Vous devez donc connaître les critères déclenchant une ventilation de facture et savoir
comment créer un document de facturation pour chaque livraison.
Interprétation des raisons incitant à ventiler une facture
Utilisez le système backend SAP pour cet exercice.
1. Affichez le flux de documents pour la livraison mentionnée dans l'exercice précédent.
Ouvrez en mode de modification la commande client qui correspond au numéro de
commande d'achat ##S4615-A10.
Dans la commande client, modifiez les conditions de paiement en ZB02.
2. Affichez à nouveau l'échéancier de factures pour le client C615-C##. Indiquez la date de
facture du <premier jour du mois> et dans l'onglet Données déf. (Données par défaut),
sélectionnez le type de document de facturation F1 (Facture F1). Exécutez le processus de
facturation en mode de simulation.
Quel est le nombre de factures créées ? Quels sont les critères de ventilation ?
Sauvegardez les factures.
Créez un document de facturation pour chaque livraison
1. Pour votre facture Foire## (type de document de facturation ZF##), vous voulez pouvoir
créer un document de facturation individuel pour chaque livraison. Comment procédez-
vous ?
Exécutez cette étape dans le Customizing.


## PDF page 146

Astuce :
Utilisez le type de document de facturation ZF##, le type de livraison LF et le
type de poste TAN.
Chapitre 7: Méthodes de facturation


## PDF page 147

Chapitre 7
Solution 9
Interprétation des raisons incitant à ventiler
une facture
Exemple de gestion
Vous avez parfois besoin de modifier manuellement les conditions de paiement au niveau de
la commande client en fonction de l'accord passé avec votre client. Vous souhaitez analyser
l'impact de telles modifications sur la facturation. Pour la facturation liée à une foire, vous
voulez également pouvoir créer un document de facturation individuel pour chaque livraison.
Vous devez donc connaître les critères déclenchant une ventilation de facture et savoir
comment créer un document de facturation pour chaque livraison.
Interprétation des raisons incitant à ventiler une facture
Utilisez le système backend SAP pour cet exercice.
1. Affichez le flux de documents pour la livraison mentionnée dans l'exercice précédent.
Ouvrez en mode de modification la commande client qui correspond au numéro de
commande d'achat ##S4615-A10.
Dans la commande client, modifiez les conditions de paiement en ZB02.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Modifier.
b) Dans la zone Nº commande d'achat, saisissez ##S4615-A10 et confirmez votre saisie.
Sélectionnez le résultat de la recherche.
c) Modifiez les conditions de paiement en ZB02 puis sauvegardez la commande.
2. Affichez à nouveau l'échéancier de factures pour le client C615-C##. Indiquez la date de
facture du <premier jour du mois> et dans l'onglet Données déf. (Données par défaut),
sélectionnez le type de document de facturation F1 (Facture F1). Exécutez le processus de
facturation en mode de simulation.
Quel est le nombre de factures créées ? Quels sont les critères de ventilation ?
Sauvegardez les factures.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures.
b) Définissez la date de facture du <premier jour du mois> à la <date du jour>.
c) Saisissez le donneur d'ordre C615-C## et cochez la case Lié à livraison.
d) Dans la page d'onglet Données déf., sélectionnez le type de document de facturation
F1 Facture (F1).


## PDF page 148

e) Cliquez sur le bouton Afficher l'échéancier de factures.
f) Dans la vue Traiter échéancier de factures, sélectionnez tous les documents et cliquez
sur
 Simulation. Deux documents de facturation sont créés.
g) Sélectionnez ces deux documents, puis cliquez sur le bouton Analyse ventilation. Vous
ne pouvez pas regrouper ces commandes en un seul document de facturation, car
elles possèdent des conditions de paiement différentes.
h) Sauvegardez les factures.
Créez un document de facturation pour chaque livraison
1. Pour votre facture Foire## (type de document de facturation ZF##), vous voulez pouvoir
créer un document de facturation individuel pour chaque livraison. Comment procédez-
vous ?
Exécutez cette étape dans le Customizing.
Astuce :
Utilisez le type de document de facturation ZF##, le type de livraison LF et le
type de poste TAN.
a) Le numéro du document de référence doit être copié dans l'en-tête de document de
facturation pour entraîner une ventilation de facture en raison de numéros de livraison
différents. À cet effet, saisissez le numéro du document de référence dans la zone
VBRK-ZUKRI.
b) Accédez au système backend SAP et sélectionnez Customizing (code de transaction
SPRO) dans vos Favoris.
c) Accédez au Guide d'implémentation du Customizing (code de transaction SPRO) :
Administration des ventes (ADV) → Facturation → Factures → Gérer la régie de la
copie pour les factures.
d) Sélectionnez Pilotage copie : document de livraison après facture et cliquez sur le
bouton
 Sélectionner.
e) Sélectionnez la cible ZF## et la source LF, puis double-cliquez sur Poste dans le volet
Structure de dialogue.
f) Cliquez sur
 (Afficher → Modifier). Sélectionnez le type de poste TAN et cliquez sur
le bouton
 Détail.
g) Dans la zone Données VBRK/VBRP, saisissez la routine 3 Facture individuelle.
Chapitre 7: Méthodes de facturation


## PDF page 149

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Analyser le regroupement et la ventilation de factures
●
Interpréter les raisons incitant à ventiler une facture
Sujet: Analyse du regroupement et de la ventilation de factures


## PDF page 150

Chapitre 7: Méthodes de facturation


## PDF page 151

Chapitre 7
Sujet 2
Définition de relevés de factures
VUE D'ENSEMBLE DU SUJET
Ce sujet explique en détail la méthode de facturation spéciale Relevé de factures.
Exemple de gestion
Les membres d'un groupement d'achat doivent chacun recevoir une facture. La centrale
responsable du règlement des factures tient à visualiser toutes les factures dans un relevé.
Pour cette raison, vous devez disposer des connaissances suivantes :
●
connaître le paramétrage requis pour utiliser un relevé de factures.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Définir des relevés de factures
Relevé de factures
Figure 36: Relevé de factures
Ces relevés sont généralement utilisés par des groupements d'achat si la centrale règle les
documents de facturation pour tous les points de vente. La centrale ne reçoit pas toutes les


## PDF page 152

factures individuelles des points de vente mais une liste de factures individuelles des points
de vente mais à des dates données.
Les listes de factures contiennent plusieurs documents de facturation (factures, avoirs et
notes de débit) et vous pouvez les envoyer au payeur à des dates spécifiques ou à intervalles
réguliers.
Gestion de données dans le Customizing de l'Administration des ventes
L'administrateur système doit gérer les données suivantes dans le Customizing de
l'Administration des ventes :
●
Si vous avez négocié un ducroire, gérez le type de condition RL00 (ducroire) ainsi que le
type de condition MW15.
●
Chaque type de document de facturation à inclure dans une liste de factures doit être
affecté à un type de liste de factures. La version standard SAP comprend deux types de
listes de factures : LG pour les avoirs et LR pour les factures et les notes de débit.
Vous devez également gérer les données de base suivantes :
●
Définissez un calendrier d'entreprise spécifiant à quelles dates créer les relevés de
factures. Saisissez le calendrier d'entreprise dans la fiche client du payeur (zone Dates
relevé de facturation dans la page d'onglet Factures).
●
Gérez des enregistrements de condition du type RL00 pour le payeur.
●
Créez des enregistrements de conditions de message pour les catégories de message
LR00 et RD01. Vous pouvez vous baser sur des technologies de communication pour
déterminer si des documents de facturation doivent être envoyés au client lors de la
création de la facture ou si vous voulez attendre la création de la liste de factures pour les
envoyer.
Vous pouvez annuler les listes de factures. Dans le cas de ducroires, le système crée un
document d'annulation pour FI.
Comment définir des relevés de factures
Please make sure you are aware of the information in the set up guide.
Set up an invoice list.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Demonstrate the different payer C615-GC00 for customers C615-GA00 and C615-
GB00, and sales area 1010/10/00.
2. Display the Billing Documents tab page in the master data for payer C615-GC00 and
explain the calendar AM stored in the InvoicingListDates field.
3. Demonstrate the factoring discount created for payer C615-GC00 in distribution channel
10 and condition type RL00.
4. Create the billing documents for the orders with purchase order numbers 00S4615-A11
(customer C615-GB00) and 00S4615-A12 (customer C615-GA00).
5. Display the list of billing documents created for payer C615-GC00.
Chapitre 7: Méthodes de facturation


## PDF page 153

6. Go to one of the invoices and also display the stored dunning block in the accounting
document.
7. Create the invoice list that contains the two billing documents shown above. Choose Work
List for Invoice Lists and specify the billing date from <first day of the week> to <end of the
month>. Enter payer C615-GC00 . Display the worklist for invoice lists. The two billing
documents appear.
8. Save the invoice list. In the collective processing log, choose the Documents pushbutton.
Mention the factoring discount (del credere) provision.
9. Show how to remove the dunning block in the accounting document of the billing item.
SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Définir des relevés de factures
Sujet: Définition de relevés de factures


## PDF page 154

Chapitre 7: Méthodes de facturation


## PDF page 155

Chapitre 7
Sujet 3
Facturation convergente omnicanal
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Demandes de documents de facturation externes (EBDR)
Demandes de documents de facturation externes (EBDR)
Une méthode de facturation qui vous permet de facturer différents types de documents
commerciaux dans votre système SAP S/4HANA avec les données de facturation provenant
des sources externes dans le but de créer des factures client combinées.
La facturation convergente décrit le processus de facturation conjointe de différents types de
documents commerciaux en vue de la création d’une seule facture client. Cette méthode est
recommandée pour facturer simultanément des commandes clients, livraisons ou services
professionnels à un client. En effet, elle consiste à converger plusieurs postes de l'échéancier
de factures (y compris différents types de factures) dans une seule facture client.
Exemple de gestion
Un client achète une offre centrée sur les solutions auprès d'une société informatique. La
solution inclut du matériel informatique (livraison sortante), une licence de logiciel
(commande client), des services de conseil (demande de note de débit) ainsi que des services
numériques d’apprentissage machine fournis dans le cloud (données de facturation basées
sur la consommation externes conservées dans une EBDR). Au cours du processus de
facturation à la fin de chaque mois, vous convergez les données pertinentes pour la
facturation à partir de tous les canaux de sorte à pouvoir envoyer une facture unique
combinée qui facture au client d’après son utilisation de chaque composant de l’offre.


## PDF page 156

Figure 37: Facturation convergente des demandes de documents de facturation externes
La facturation convergente omnicanal va plus loin dans ce concept. En effet, cette approche
vous permet de renseigner votre échéancier de factures (dans l'application Création de
documents de facturation) avec des demandes de documents de facturation externes
(EBDR) qui contiennent les données de facturation provenant de systèmes externes. Vous
pouvez alors créer des factures client regroupant des données de facturation internes et
externes. Vous pouvez ainsi créer facilement des factures pour des offres centrées sur les
solutions qui combinent postes facturables de différents canaux (internes et externes) et
catégories de facturation (par exemple, la facturation occasionnelle, la facturation basée sur
des projets et la facturation basée sur la consommation). Les frais généraux d'administration
traditionnellement associés à la facturation combinée des offres centrées sur les solutions
sont alors considérablement réduits, ainsi que le nombre de factures que vous devez créer et
envoyer aux clients.
Figure 38: Téléchargement d’un fichier Excel des EBDR
Chapitre 7: Méthodes de facturation


## PDF page 157

Les demandes de documents de facturation externes (EBDR) sont des objets qui permettent
de transformer et de conserver les données de facturation que votre système SAP S/4HANA
a reçues depuis une source externe (un système SAP externe, par exemple). Les EBDR vous
permettent de facturer les données de facturation externes en provenance de différentes
sources. En outre, vous pouvez également converger les données de facturation (par
exemple, les données de paiement à l'utilisation) avec les données de facturation internes
(par exemple, les postes facturables d'une livraison). Ceci vous permet de facturer aux clients
les offres qui combinent différents types de facture via une seule facture combinée.
La réserve de travail dans l'application Création de documents de facturation - Postes
d'échéancier de factures répertorie désormais les demandes de documents de facturation
externes. Les demandes de documents de facturation externes contiennent des données de
facturation provenant de sources externes, telles que des systèmes externes SAP ou non
SAP. Ces demandes de documents de facturation externes peuvent être facturées
distinctement ou associées aux documents commerciaux facturables (tels que les livraisons
et les demandes de note de débit) afin de générer des factures clients combinées. Ce
processus est appelé facturation convergente omnicanal. Cette approche omnicanal
appliquée à la facturation présente un grand avantage : elle réduit considérablement les frais
généraux d'administration traditionnellement associés à la facturation combinée des offres
centrées sur les solutions.
Comment créer une demande de document de facturation externe
For the detailed step by step description please refer to the provided System -Setup- Guide.
A file is prepared for you and you can demo the upload of an Excel File.
When in doubt leave it out.
If you do not want to demo it, just show the app Manage Billing Document Request
1. Go to the tile group: Billing Document Request, choose the app: Manage Billing Document
Request and
2. Choose Create
3. Show the option: Download Excel Template
SAP provides an Excel Template. It is ready to be used.
The template should be filled out with your external billing data, making sure that it
conforms to the guidelines specified in the app‘s product assistance. You can find the
guidelines by searching for Manage Billing Document Requests on the SAP Help Portal -
http://help.sap.com .
SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Demandes de documents de facturation externes (EBDR)
Sujet: Facturation convergente omnicanal


## PDF page 158

Chapitre 7: Méthodes de facturation


## PDF page 159

Chapitre 7
Évaluation des connaissances
1.
Quel critère permet de déclencher automatiquement une ventilation de la facture ?
Sélectionnez la réponse correcte.
A Article
B Quantité commandée
C Prix unitaire
D Cond. de paiement
2. Vous pouvez définir une ventilation de facture liée au poste dans le Customizing.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. Vous voulez ajouter un critère de ventilation supplémentaire dans le système. Comment
faire ? Sélectionnez la réponse correcte :
Sélectionnez la réponse correcte.
A Vous devez modifier le Customizing pour le type de document de facturation.
B Vous devez modifier le Customizing pour le pilotage de la copie (zone : VBRK-
ZUKRI).
C Vous devez modifier le Customizing pour le type de poste.
D Vous ne pouvez pas modifier le critère de ventilation car le système effectuera
automatiquement une ventilation de facture.


## PDF page 160

4. Quand pouvez-vous utiliser une liste de factures ? Choisissez les réponses correctes.
Sélectionnez les réponses correctes.
A Lorsque tous les documents de facturation (factures, avoirs et notes de débit) ont
le même payeur.
B Lorsque tous les documents de facturation (factures, avoirs et notes de débit)
possèdent le même donneur d'ordre.
C Lorsque vous voulez facturer à des dates spécifiques ou à intervalles réguliers.
D Lorsque vous voulez éviter d'utiliser un échéancier de factures.
5. Quelles sont les affirmations correctes sur la facturation convergente omnicanal et les
demandes de documents de facturation externes parmi celles ci-dessous ? Choisissez les
réponses correctes.
Sélectionnez les réponses correctes.
A Avec cette méthode de facturation, vous pouvez converger les données de
facturation internes et externes dans des factures client combinées.
B Les demandes de documents de facturation externes doivent être téléchargées à
l'aide de l'exit utilisateur Interface de facturation générale.
C Vous pouvez utiliser un fichier Excel pour télécharger les données de facturation
externes.
D Les demandes de documents de facturation externes sont traitées dans un
échéancier de factures distinct (VF06).
Chapitre 7: Évaluation des connaissances


## PDF page 161

Chapitre 7
Évaluation des connaissances - Réponses
1.
Quel critère permet de déclencher automatiquement une ventilation de la facture ?
Sélectionnez la réponse correcte.
A Article
B Quantité commandée
C Prix unitaire
D Cond. de paiement
2. Vous pouvez définir une ventilation de facture liée au poste dans le Customizing.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. Vous voulez ajouter un critère de ventilation supplémentaire dans le système. Comment
faire ? Sélectionnez la réponse correcte :
Sélectionnez la réponse correcte.
A Vous devez modifier le Customizing pour le type de document de facturation.
B Vous devez modifier le Customizing pour le pilotage de la copie (zone : VBRK-
ZUKRI).
C Vous devez modifier le Customizing pour le type de poste.
D Vous ne pouvez pas modifier le critère de ventilation car le système effectuera
automatiquement une ventilation de facture.


## PDF page 162

4. Quand pouvez-vous utiliser une liste de factures ? Choisissez les réponses correctes.
Sélectionnez les réponses correctes.
A Lorsque tous les documents de facturation (factures, avoirs et notes de débit) ont
le même payeur.
B Lorsque tous les documents de facturation (factures, avoirs et notes de débit)
possèdent le même donneur d'ordre.
C Lorsque vous voulez facturer à des dates spécifiques ou à intervalles réguliers.
D Lorsque vous voulez éviter d'utiliser un échéancier de factures.
5. Quelles sont les affirmations correctes sur la facturation convergente omnicanal et les
demandes de documents de facturation externes parmi celles ci-dessous ? Choisissez les
réponses correctes.
Sélectionnez les réponses correctes.
A Avec cette méthode de facturation, vous pouvez converger les données de
facturation internes et externes dans des factures client combinées.
B Les demandes de documents de facturation externes doivent être téléchargées à
l'aide de l'exit utilisateur Interface de facturation générale.
C Vous pouvez utiliser un fichier Excel pour télécharger les données de facturation
externes.
D Les demandes de documents de facturation externes sont traitées dans un
échéancier de factures distinct (VF06).
Chapitre 7: Évaluation des connaissances - Réponses


## PDF page 163

CHAPITRE 8
Processus de gestion
spécifiques
Sujet 1
Définir des calendriers de facturation
Exercice 10: Définir des calendriers de facturation
Sujet 2
Traitement des acomptes
Exercice 11: Traitement des acomptes (exercice facultatif)
Sujet 3
Traitement des versements échelonnés
OBJECTIFS DU CHAPITRE
●
Définir des calendriers de facturation
●
Traiter des acomptes
●
Traiter des versements échelonnés


## PDF page 164

Chapitre 8
Sujet 1
Définir des calendriers de facturation
VUE D'ENSEMBLE DU SUJET
Ce sujet explique les principales différences entre les calendriers de facturation périodique et
partielle. Dans cette optique, vous découvrirez les options clés du Customizing applicables à
ces calendriers de facturation.
Exemple de gestion
Certains clients vous ont loué un produit, par exemple, un ordinateur. Vous avez conclu avec
eux que la location serait automatiquement facturée tous les mois. Votre entreprise a reçu,
d'un autre client, un contrat pour un important projet. Vous devez facturer des montants
partiels individuels pour ce projet. À cet effet, vous devez disposer des connaissances
suivantes :
●
savoir utiliser la facturation périodique et partielle.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Définir des calendriers de facturation
Calendrier de facturation
Figure 39: Calendrier de facturation
Lorsque vous traitez une commande client, vous pouvez, au lieu de mémoriser une date de
facture unique, enregistrer un calendrier de facturation détaillé avec plusieurs dates de
facture dans le document de vente au niveau du poste.
Vous pouvez également définir un calendrier de facturation au niveau de l'en-tête. Il
s'appliquera alors à tous les postes liés. Ces calendriers de facturation sont associés aux
types de documents de vente.


## PDF page 165

La facturation périodique s'avère souvent utile pour les contrats de location et de service. Elle
permet de facturer un montant total périodiquement à une date donnée.
La facturation partielle, souvent utilisée pour les constructions industrielles, permet d'étaler la
facturation du montant total sur plusieurs dates définies dans un calendrier de facturation.
Selon l'opération commerciale que vous traitez, le système propose automatiquement l'un
des deux types de calendrier de facturation.
Facturation périodique
Figure 40: Facturation périodique
Vous pouvez utiliser la facturation périodique pour des transactions relatives, par exemple, à
des contrats de location.
Les données du contrat mémorisées dans le système peuvent alors servir de base pour créer
le calendrier de facturation.
Les dates de début et de fin définissent la durée du calendrier de facturation. Lorsque cela est
possible, le système les reprend à partir des données du contrat. Vous pouvez décider de ne
pas spécifier de date de fin si la durée est illimitée. Dans ce cas, il est possible d'ajouter de
nouvelles dates jusqu'à l'horizon (l'horizon indique le nombre de périodes de décompte
définies dans le calendrier de facturation).
Vous pouvez créer de nouvelles dates directement dans le calendrier de facturation ou via le
programme RVFPLA01. Le programme doit être exécuté à intervalles réguliers ; en effet, le
système ne calcule pas automatiquement de nouvelles dates lors de la facturation de
périodes individuelles de décompte.
Les dates de facture peuvent vous permettre de déterminer le moment et la fréquence de
facturation, par exemple le premier ou le dernier jour de chaque mois.
Sujet: Définir des calendriers de facturation


## PDF page 166

Comment appliquer un calendrier de facturation pour la facturation périodique
Apply a billing plan for periodic billing.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Create a maintenance contract using the following data:
Field
Data Value
Order Type
WV
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-E##
PO Number
9-1
Material
P615-500
Order Quantity
1 PC
Refer to the item category WVN (maintenance contract item).
Go to the billing plan and explain the significance of the individual fields as well as the
structure and the information for the settlement periods created.
Go to the pricing screen and demonstrate condition type PPSV. On the detail screen, show
this condition type. Show that the Calculat. type field has the value M to indicate quantity-
dependent monthly price.
2. Set the billing date for the contract (order-related). Display the billing due list for customer
C615-E##.
Choose the selection period in such a way that the billing date for the first settlement
period is set.
3. Display the maintenance contract again and demonstrate billing status C (completed) for
the first settlement period.
Chapitre 8: Processus de gestion spécifiques


## PDF page 167

Facturation partielle
Figure 41: Facturation partielle
Lors d'une facturation partielle, la valeur totale à facturer est répartie entre plusieurs dates
selon des règles particulières.
Vous pouvez spécifier autant de dates que nécessaire par calendrier de facturation.
Il est possible de spécifier un blocage de facture pour les dates du calendrier de facturation.
Les modifications (de montants, par exemple) qui surviennent après la création de certains
documents de facturation partielle sont réparties entre les dates restantes du calendrier de
facturation. Le montant résultant du nouveau calcul pour les documents déjà créés est pris en
compte dans la facture finale.
Le système crée une entrée dans l'index de facturation pour chaque date de facture. Ainsi,
l'index de facturation contiendra une entrée pour la facturation partielle concernée à la date
de facture indiquée. Dans ce cas, la facturation est effectuée à partir d'une commande client.
Lorsque vous créez un document de facturation, le système met à jour le statut des dates du
calendrier de facturation.
Vous ne pouvez plus modifier dans le calendrier de facturation les dates pour lesquelles la
facturation a déjà été effectuée.
Vous pouvez afficher les documents de facturation existants au moyen du flux de documents.
Sujet: Définir des calendriers de facturation


## PDF page 168

Figure 42: Calendrier de facturation lié à la facturation partielle
La facturation de projets dans le domaine des constructions industrielles représente un
exemple typique de la facturation partielle. De tels projets comprennent souvent une série de
jalons qui marquent l'achèvement de différentes phases du projet.
Dans le système SAP, les jalons sont mémorisés dans un réseau avec les données de projet
planifiées et réelles. Les jalons sont affectés aux dates du calendrier de facturation puis
bloqués pour facturation jusqu'à la confirmation de leur achèvement.
Dans un calendrier de facturation partielle, vous pouvez désormais contrôler si une date
de facture :
●
est une date fixe ;
●
doit être mise à jour avec la date réelle du jalon ;
●
doit être mise à jour avec la date réelle du jalon seulement si la fabrication est terminée
avant la date de facture planifiée.
Chapitre 8: Processus de gestion spécifiques


## PDF page 169

Règle de facturation
Figure 43: Règle de facturation - Détermination des éléments de calcul de la facturation
Vous pouvez définir une règle de facturation pour chaque date du calendrier de facturation.
Cette règle détermine la manière de calculer la valeur à facturer à une date particulière.
De cette façon, vous pouvez par exemple définir si le montant à facturer représente un
montant fixe ou un pourcentage du montant total.
Le système peut aussi déterminer si le montant à facturer fait l'objet d'une facture finale, dans
laquelle les dates qui n'ont pas encore fait l'objet d'une facturation sont à prendre en compte
également.
Dans le cadre de la détermination du prix, vous pouvez créer des enregistrements de
condition correspondant à des types de condition spéciaux, pour lesquels il est possible de
définir des prix mensuels (pour des coûts de location, par exemple). Ceci vous permet de
facturer une valeur donnée par mois.
Sujet: Définir des calendriers de facturation


## PDF page 170

Customizing des calendriers de facturation
Figure 44: Customizing des calendriers de facturation
Le type de poste du document et la règle concernant la pertinence pour la facturation
déterminent le type du calendrier de facturation (la valeur I implique un calendrier de
facturation à partir de la commande client).
La désignation des dates représente la désignation des dates de facture dans le calendrier,
par exemple, 003 pour la conclusion du contrat et 005 pour l'assemblage. Elles ne jouent
aucun rôle de contrôle.
Les catégories de dates remplissent une fonction de contrôle au niveau de la date de facture.
Elles déterminent par exemple :
●
la règle de facturation à utiliser lors du décompte pour une date de facture ;
●
l'utilisation d'une date fixe comme date de facture ;
●
l'activation d'un blocage de facture pour cette date.
Les règles de détermination de la date permettent de définir les dates de début et de fin dans
le calendrier de facturation ainsi que les dates de facture correspondantes (par exemple, 2
jours avant la fin du mois).
Chaque règle de détermination de date repose sur une date de base à laquelle une période
définie est ajoutée.
L'utilisation de la facturation périodique ou de la facturation partielle et des paramètres de
contrôle appropriés dépend du type de calendrier de facturation.
La date par défaut sert uniquement dans le cas de la facturation partielle. Elle fournit une
séquence de dates utilisées comme références pour déterminer les dates lors du traitement
des commandes.
Chapitre 8: Processus de gestion spécifiques


## PDF page 171

Comment définir un type de calendrier de facturation
Set up a billing plan type.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Explain in IMG how billing plans are customized.
2. As an example, use item category WVN, to which billing plan type 02 for periodic billing is
assigned.
3. Point out that the billing relevance for items with billing plans must be set to I.
4. Go to item category TAO, to which billing plan type 01 for milestone billing is assigned.
Sujet: Définir des calendriers de facturation


## PDF page 172

Chapitre 8: Processus de gestion spécifiques


## PDF page 173

Chapitre 8
Exercice 10
Définir des calendriers de facturation
Exemple de gestion
Vous avez conclu des contrats de maintenance avec certains de vos clients. Chaque mois,
vous facturez à ces clients un montant convenu. Vous devez donc savoir comment utiliser les
calendriers de facturation périodique et configurer leurs options.
Définissez des calendriers de facturation.
1. Créez un contrat de maintenance à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
WV (service et entretien)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-E##
Réf. client (numéro de commande d'achat)
##S6415-PB
Article
P615-5##
Quantité cible
Astuce :
Vous pouvez choisir d'utiliser la barre de lancement de SAP Fiori ou le menu
SAP GUI du système backend.
Astuce :
Description des étapes facultatives pour utiliser le menu SAP GUI du système
backend.
Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Contrat → Créer.
.
2. Dans le contrat, examinez les dates du calendrier de facturation. Notez la règle de calcul
applicable à l'enregistrement des conditions de prix dans une période de décompte.


## PDF page 174

3. Exécutez la facturation pour la première période de décompte (vous devez spécifier une
date de facture correspondant au dernier jour du mois).
4. Affichez à nouveau votre contrat de service.
Quel est maintenant le statut facture pour la première période de décompte ?
5. Consultez le Customizing des postes de facturation périodique et des postes de
facturation partielle. Ils sont organisés en fonction d'un critère spécifique.
Lequel ?
6. Quel critère permet de déterminer la méthode de contrôle au niveau de la période de
décompte ?
Quels paramètres de contrôle sont définis ici ?
Accédez au système backend SAP et sélectionnez Customizing (code de transaction
SPRO) dans vos Favoris.
Chapitre 8: Processus de gestion spécifiques


## PDF page 175

Chapitre 8
Solution 10
Définir des calendriers de facturation
Exemple de gestion
Vous avez conclu des contrats de maintenance avec certains de vos clients. Chaque mois,
vous facturez à ces clients un montant convenu. Vous devez donc savoir comment utiliser les
calendriers de facturation périodique et configurer leurs options.
Définissez des calendriers de facturation.
1. Créez un contrat de maintenance à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
WV (service et entretien)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-E##
Réf. client (numéro de commande d'achat)
##S6415-PB
Article
P615-5##
Quantité cible
Astuce :
Vous pouvez choisir d'utiliser la barre de lancement de SAP Fiori ou le menu
SAP GUI du système backend.
Astuce :
Description des étapes facultatives pour utiliser le menu SAP GUI du système
backend.
Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Contrat → Créer.
.
a) _____________________________
Description pour la barre de lancement de SAP Fiori
Lancez la barre de lancement SAP Fiori.


## PDF page 176

b) Sélectionnez le groupe de vignettes Ventes (Sales) et lancez l'application Gestion des
contrats de vente.
c) Sélectionnez Créer contrat.
d) Saisissez les données comme indiqué dans la tâche.
_______________________________
Description de SAP GUI du système backend
e) Description facultative pour utiliser le menu SAP GUI du système backend.
f) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Contrat → Créer.
g) Saisissez les données comme indiqué dans la tâche.
2. Dans le contrat, examinez les dates du calendrier de facturation. Notez la règle de calcul
applicable à l'enregistrement des conditions de prix dans une période de décompte.
a) Sélectionnez le poste et cliquez sur le bouton Cal.fact (Calendrier de facturation).
b) Sélectionnez une période de décompte puis cliquez sur le bouton
 Conditions. Le
prix du service à fournir est déterminé via le type de condition PPSV.
c) Sélectionnez le type de condition PPSV, puis cliquez sur
 Détail conditions. La zone
Règle de calcul a la valeur M pour indiquer que le prix mensuel dépend de la quantité.
d) Enfin, sauvegardez le document.
3. Exécutez la facturation pour la première période de décompte (vous devez spécifier une
date de facture correspondant au dernier jour du mois).
a) _______________________________
Description pour la barre de lancement de SAP Fiori
b) Dans la barre de lancement SAP Fiori, sélectionnez le groupe de vignettes Documents
de facturation (Billing Documents) et lancez l'application Création de documents de
facturation - Postes d'échéancier de factures.
c) Saisissez votre client dans la zone Donneur d'ordre : C615-E##, puis, dans la zone
Date de facturation jusqu'au, définissez la date sur le <dernier jour du mois>.
d) Cochez Document commercial, puis cliquez sur Créer.
e) Sauvegardez ensuite votre document de facturation.
_______________________________
Description de SAP GUI du système backend
f) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Traiter échéancier de factures.
g) Définissez la date de facture de la <date du jour> au <dernier jour du mois>. Saisissez
le donneur d'ordre C615-E## et cochez la case Lié à une commande client.
h) Affichez l'échéancier de factures.
i) Sauvegardez la liste.
4. Affichez à nouveau votre contrat de service.
Chapitre 8: Processus de gestion spécifiques


## PDF page 177

Quel est maintenant le statut facture pour la première période de décompte ?
a) ___________________________
Description pour la barre de lancement de SAP Fiori
b) Dans la barre de lancement SAP Fiori, sélectionnez le groupe de vignettes Ventes
(Sales) et lancez l'application Gestion des contrats de vente.
c) Saisissez votre client dans la zone Donneur d'ordre : C615-E## et sélectionnez
Lancer.
d) Sélectionnez votre contrat, cliquez sur l'hyperlien de votre numéro de contrat et
sélectionnez l'option Afficher contrat pour afficher les détails de votre contrat.
e) Sélectionnez le poste, puis passez au calendrier de facturation en cliquant sur le
bouton Cal.fact. Le statut facture (zone Statut) de la première période de décompte
est défini sur C (Facturé).
_______________________________
Description de SAP GUI du système backend
f) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Contrat → Afficher.
g) Confirmez le numéro de contrat.
h) Sélectionnez le poste puis passez au calendrier de facturation. Le statut de la première
période de décompte est défini sur C (Facturé).
5. Consultez le Customizing des postes de facturation périodique et des postes de
facturation partielle. Ils sont organisés en fonction d'un critère spécifique.
Lequel ?
Le type de poste détermine l'affectation du poste à un calendrier de facturation périodique
ou à un calendrier de facturation partielle. Exemple : le type du calendrier de facturation
02 (facturation périodique) est affecté au type WVN (poste de contrat de maintenance).
Le type du calendrier 01 (facturation périodique) est affecté, lui, au type de poste TAO
(jalon facture).
6. Quel critère permet de déterminer la méthode de contrôle au niveau de la période de
décompte ?
Quels paramètres de contrôle sont définis ici ?
Accédez au système backend SAP et sélectionnez Customizing (code de transaction
SPRO) dans vos Favoris.
Sujet: Définir des calendriers de facturation


## PDF page 178

a) La catégorie de date représente le critère de contrôle déterminant au niveau de la
période de décompte. À ce niveau, vous pouvez définir des paramètres de contrôle tels
que la règle de facturation, l'utilisation du blocage de la facture et le type de document
de facturation par défaut.
b) Accédez au système backend SAP et sélectionnez Customizing (code de transaction
SPRO) dans vos Favoris.
c) Accédez au Guide d'implémentation du Customizing : Administration des
ventes → Facturation → Calendrier de facturation → Définir et affecter catégorie de
date.
d) Sélectionnez l'activité Gestion type de délai pour type de calendrier de facturation et
cliquez sur le bouton
 Sélectionner.
e) Sélectionnez l'entrée correspondant au type de calendrier de facturation 02 et à la
catégorie de date 01, puis consultez les paramètres de contrôle définis.
Chapitre 8: Processus de gestion spécifiques


## PDF page 179

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Définir des calendriers de facturation
Sujet: Définir des calendriers de facturation


## PDF page 180

Chapitre 8
Sujet 2
Traitement des acomptes
VUE D'ENSEMBLE DU SUJET
Ce sujet décrit en détail l'intégration du traitement des acomptes entre l'Administration des
ventes et la Comptabilité financière.
Exemple de gestion
Votre entreprise a reçu un contrat pour un vaste projet. Un acompte est demandé. Au cours
du projet, vous devrez également facturer des montants partiels individuels. Pour cette
raison, vous devez disposer des connaissances suivantes :
●
savoir comment traiter des acomptes entre l'Administration des ventes et la Comptabilité
financière.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Traiter des acomptes
Acomptes
Figure 45: Traitement des acomptes dans l'Administration des ventes et la Comptabilité financière
Dans le domaine des biens d'équipement ou des constructions industrielles, il est courant de
convenir du versement d'un acompte avec le client.


## PDF page 181

Des acomptes sont créés dès la commande client.
À la date d'échéance correspondante, vous envoyez une demande d'acompte au client
(document de facturation de l'Administration des ventes).
Cette demande SD est automatiquement enregistrée dans le module Comptabilité financière
en tant que demande d'acompte (enregistrée comme poste pour mémoire). Le poste est doté
du code compte général spécial F qui assure l'enregistrement à des fins statistiques.
L'enregistrement est effectué sur un compte collectif spécial permettant de distinguer les
demandes d'acompte des autres créances.
Lors de l'enregistrement d'un encaissement pour un acompte, le système l'affecte à la
demande d'acompte correspondante. Le montant d'acompte versé est également imputé sur
le compte de la commande client. Le poste est affecté du code compte général spécial A.
Lorsque vous traitez une facture partielle ou une facture finale, le système reprend les
acomptes versés en tant qu'acomptes à imputer. En Comptabilité financière, les acomptes
sont déduits du compte collectif spécial puis imputés au compte collectif standard. Les
acomptes à rapprocher sont des postes non soldés pour le client et diminuent le montant
total des créances.
Accords concernant les acomptes dans la commande client
Figure 46: Accords concernant les acomptes dans la commande client
La fonction du calendrier de facturation permet de traiter les acomptes.
Vous pouvez mémoriser un ou plusieurs accords d'acomptes sous la forme de dates dans un
calendrier de facturation.
La valeur de l'acompte convenu avec le client peut correspondre à un montant fixe ou à un
pourcentage de la valeur du poste.
Les règles de facturation suivantes déterminent la nature de l'acompte :
●
Règle de facturation 4 :
acomptes pour la facturation partielle proportionnelle
●
Règle de facturation 5 :
Sujet: Traitement des acomptes


## PDF page 182

acomptes pour la facturation partielle en valeur
Vous pouvez affecter l'accord concernant l'acompte directement à un poste ou le définir
comme valable pour tous les postes de la commande client.
Astuce :
Le type de condition spécial AZWR est prévu pour les postes d'acompte dans les
documents de vente à la place du type de condition habituel PR00. La catégorie
de condition E et la règle de calcul B (montant fixe) sont affectées au type de
condition AZWR. Si vous sélectionnez le type AZWR, tous les autres types de
conditions sont désactivés.
Demande d'acompte
Figure 47: Demande d'acompte
Dès que la date de facture pour l'acompte (dans le calendrier de facturation) est atteinte, le
système crée une facture pour l'acompte et la transmet au client. Vous utilisez le type de
document de facturation FAZ pour la création de la demande d'acompte.
Vous pouvez créer cette demande des deux façons suivantes :
●
automatiquement via le traitement de l'échéancier de factures lors d'une opération de
facturation groupée ;
●
Manuellement en saisissant le numéro de la commande dans la transaction Créer
document de facturation
Le système détermine et affiche automatiquement la taxe lorsque vous créez une demande
d'acompte.
Dans le module Comptabilité financière, la demande d'acompte est générée
automatiquement à partir de la demande créée dans l'Administration des ventes.
Le flux de documents relatif à la commande client vous permet d'afficher les demandes
d'acompte créées dans les modules Administration des ventes et Comptabilité financière.
Chapitre 8: Processus de gestion spécifiques


## PDF page 183

Encaissement des acomptes
Figure 48: Encaissement des acomptes
Après le règlement d'un acompte, le code compte général spécial A permet d'identifier
l'encaissement en Comptabilité financière sous forme d'acompte après la passation de
l'écriture. Vous pouvez sélectionner un encaissement à partir des demandes en cours puis
cliquer sur le bouton Créer acomptes pour l'affecter à un processus.
Les acomptes dotés du code compte général spécial A figurent dans les postes non soldés de
la comptabilité clients.
La demande d'acompte prend la valeur Rapproché dans le flux de documents de la
commande client.
Sujet: Traitement des acomptes


## PDF page 184

Factures partielles
Figure 49: Facture partielle - Décompte final
Pour les factures partielles et la facture finale, les acomptes versés sont repris dans les
documents de facturation en tant qu'acomptes à des fins de rapprochement.
Lors de l'impression, le système indique sur la facture le montant d'acompte versé à
rapprocher pour pouvoir le déduire du montant de créances. Ceci signifie que le
rapprochement s'effectue automatiquement durant l'impression de la facture.
Chapitre 8: Processus de gestion spécifiques


## PDF page 185

Facture partielle - Décompte proportionnel
Figure 50: Facture partielle - Décompte proportionnel
Lors de la facturation partielle, vous pouvez modifier le montant de l'acompte à rapprocher.
Pour ce faire, modifiez le montant du type de condition AZWR dans l'écran de détermination
du prix de ce poste.
Dans ce cas, le montant maximum à rapprocher correspond au montant encaissé au titre
d'acompte moins les montants d'acompte déjà rapprochés.
Au niveau de la dernière facture, le système tient compte de tous les acomptes en attente.
Comment définir des accords concernant les acomptes
Set up down payment agreements.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Create a standard order using the following data:
Field
Data Value
Order Type
OR
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-F00
Sujet: Traitement des acomptes


## PDF page 186

Field
Data Value
Material
P615-600
The requested date for the material is in 6 months.
Demonstrate and explain the item category that is determined, TAO (milestone billing
document).
2. Reference default billing plan type 0001 with (Standard Billing Plan Number)
Ref.BillPlanNo: 0000000012. It has the description S4615. Explain milestone billing plan.
The first down payment date is with date type 01 and billing type FAZ.
Comment créer une demande d'acompte
Create a down payment request.
Demo it according to the exercise or use SAP GUI transactions and SAP Menu path.
1. Create a down payment request for the standard order created in the previous
demonstration.
2. Bill the date for the down payment request (order-related) with billing type FAZ.
3. Note the amount of the down payment to be made (including value-added tax).
4. Display the accounting document for the down payment request that has been created.
5. Display the line items for customer C615-F00 in Financial Accounting.
Comment effectuer un décompte d'acompte
Perform down payment settlement.
Do it according to the exercise or use SAP GUI transactions and SAP Menu path.
1. Post the incoming payment for the down payment request by choosing Accounting →
Financial Accounting →  Accounts Receivable →  Document Entry →  Down Payment →
Down Payment. Use the following data:
Field
Data Value
Document Date
<today’s date>
Account (in the Customer screen area)
C615-F00
Special G/L ind
A
Account (in the Bank screen area)
11100025
Amount (in the Bank screen area)
<down payment amount + value-added
tax>
2. Choose the Requests button. Select the corresponding down payment request, choose
the Create down payments button, and save your posting.
Chapitre 8: Processus de gestion spécifiques


## PDF page 187

3. Display the line items for customer C615-F00 by choosing Accounting →  Financial
Accounting →  Accounts Receivable →  Account →  Display/Change Line Items.
4. Enter customer C615-F00. In the Status screen area, select the Open items radio button.
In the Open at key date field, enter <today’s date>.
5. In the Type screen area, select the Normal items checkbox, the Special G/L transactions
checkbox, and the Noted items checkbox. The down payment request was replaced by a
completed down payment. This has a special G/L account indicator A. Settlement for the
down payment is then carried out via the billing documents that are required in Sales and
Distribution.
6. Create the first “actual” milestone billing document for the order.
7. Delete the billing block in the order for the corresponding settlement period.
8. Bill with reference to order again with billing type F2. The billing document contains two
items. One was created for the invoice amount of the settlement period to be billed and a
second for settlement of the down payment made (created automatically).
9. Go to the condition screen of the down payment item to be settled and explain condition
type AZWR.
10. Save the billing documents.
11. To finish, show again how the line items for customer C615-F00 have changed.
Sujet: Traitement des acomptes


## PDF page 188

Chapitre 8: Processus de gestion spécifiques


## PDF page 189

Chapitre 8
Exercice 11
Traitement des acomptes (exercice facultatif)
Exemple de gestion
En règle générale, votre entreprise demande des acomptes lors de la vente d'équipements
complexes. Vous devez intégrer l'acompte versé par le client aux documents de facturation à
venir. Vous devez donc savoir comment traiter les acomptes.
Traitement des acomptes
Astuce :
Vous pouvez choisir d'utiliser la barre de lancement de SAP Fiori ou le menu SAP
GUI du système backend.
1. Créez une commande client standard à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-F##
Réf. client (numéro de commande d'achat)
##S4615-AZ
Article
P615-6##
Quantité d'ordre
1 pce
2. Accédez au calendrier de facturation et vérifiez le montant de l'acompte ainsi que la date
de versement prévue.
Enfin, sauvegardez la commande et notez son numéro.
3. Créez une facture pour cette demande d'acompte.


## PDF page 190

Astuce :
Sélectionnez une date postérieure à la date d'échéance de l'acompte mais
antérieure à la première date de facture partielle).
De quel type est-elle ?
4. Le client a versé l'acompte facturé. Comptabilisez le paiement.
_________________________________
Description de la barre de lancement SAP Fiori
Dans la barre de lancement SAP Fiori, cliquez sur Gestion des demandes d'acompte dans
le groupe de vignettes Gestion comptable (Accounting).
________________________________________
Description de SAP GUI du système backend
Dans le système backend, dans le Menu SAP, sélectionnez Gestion
comptable → Comptabilité financière → Clients → Écriture → Acompte → Acompte.
Dans la Gestion comptable, saisissez les données suivantes pour enregistrer l'acompte :
Zone
Valeur de données
Date du document
<date du jour>
Compte (dans la zone d'écran Client)
C615-F##
Code CGS
A
Compte (dans la zone d'écran Banque)
11100025
Montant (dans la zone d'écran Banque)
<montant de l'acompte + TVA>
Cliquez sur le bouton Demandes pour affecter cet acompte à la facture pour acompte de
votre commande client.
5. Exécutez la facturation partielle pour la première période de décompte.
Astuce :
supprimez tout d'abord le blocage de la facture au niveau de la date de
décompte correspondante, définie dans le calendrier de facturation. Ensuite,
lorsque vous créez le document de facturation, choisissez une date comprise
entre les dates de la première et de la seconde factures partielles).
Vous devez faire en sorte que le système calcule et intègre à la facture partielle le montant
total de l'acompte versé.
Chapitre 8: Processus de gestion spécifiques


## PDF page 191

6. Comment procéder pour n'imputer qu'une partie de l'acompte versé dans la première
facture partielle ?
7. Vérifiez le flux de documents de la commande client.
Sujet: Traitement des acomptes


## PDF page 192

Chapitre 8
Solution 11
Traitement des acomptes (exercice facultatif)
Exemple de gestion
En règle générale, votre entreprise demande des acomptes lors de la vente d'équipements
complexes. Vous devez intégrer l'acompte versé par le client aux documents de facturation à
venir. Vous devez donc savoir comment traiter les acomptes.
Traitement des acomptes
Astuce :
Vous pouvez choisir d'utiliser la barre de lancement de SAP Fiori ou le menu SAP
GUI du système backend.
1. Créez une commande client standard à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-F##
Réf. client (numéro de commande d'achat)
##S4615-AZ
Article
P615-6##
Quantité d'ordre
1 pce
a) _________________________
Description pour la barre de lancement de SAP Fiori
Lancez la barre de lancement SAP Fiori.
b) Sélectionnez le groupe de vignettes Ventes (Sales) et lancez l'application Créer
commande client.
c) Saisissez les données comme indiqué dans la tâche.
_______________________________
Description de SAP GUI du système backend
d) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.


## PDF page 193

e) Saisissez les données comme indiqué dans la tâche.
2. Accédez au calendrier de facturation et vérifiez le montant de l'acompte ainsi que la date
de versement prévue.
Enfin, sauvegardez la commande et notez son numéro.
a) Sélectionnez le poste, puis cliquez sur
 Afficher détails du poste et
accédez à la page d'onglet Calendrier de facturation.
b) Sauvegardez la commande et notez son numéro : ____________________
3. Créez une facture pour cette demande d'acompte.
Astuce :
Sélectionnez une date postérieure à la date d'échéance de l'acompte mais
antérieure à la première date de facture partielle).
De quel type est-elle ?
a) ____________________________
Description pour la barre de lancement de SAP Fiori
b) Dans la barre de lancement SAP Fiori, sélectionnez le groupe de vignettes Documents
de facturation (Billing Documents) et lancez l'application Création de documents de
facturation (VF01)
c) Saisissez votre numéro de commande généré à la tâche précédente et sélectionnez
Exécuter. Vous pouvez constater que le type de document de facturation FAZ sert de
base à la facturation de la demande d'acompte.
d) Sauvegardez vos données.
_______________________________
Description de SAP GUI du système backend
e) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
f) Saisissez le numéro de commande que vous venez de créer et sélectionnez une date
de facture pour limiter ces dates selon les recommandations mentionnées ci-dessus.
Confirmez votre saisie. Le type de document de facturation FAZ sert de base à la
facturation de la demande d'acompte.
g) Sauvegardez vos données.
4. Le client a versé l'acompte facturé. Comptabilisez le paiement.
Sujet: Traitement des acomptes


## PDF page 194

_________________________________
Description de la barre de lancement SAP Fiori
Dans la barre de lancement SAP Fiori, cliquez sur Gestion des demandes d'acompte dans
le groupe de vignettes Gestion comptable (Accounting).
________________________________________
Description de SAP GUI du système backend
Dans le système backend, dans le Menu SAP, sélectionnez Gestion
comptable → Comptabilité financière → Clients → Écriture → Acompte → Acompte.
Dans la Gestion comptable, saisissez les données suivantes pour enregistrer l'acompte :
Zone
Valeur de données
Date du document
<date du jour>
Compte (dans la zone d'écran Client)
C615-F##
Code CGS
A
Compte (dans la zone d'écran Banque)
11100025
Montant (dans la zone d'écran Banque)
<montant de l'acompte + TVA>
Cliquez sur le bouton Demandes pour affecter cet acompte à la facture pour acompte de
votre commande client.
a) _______________________________
Description pour la barre de lancement de SAP Fiori
Dans la barre de lancement SAP Fiori, sélectionnez le groupe de vignettes Gestion
comptable (Accounting) et lancez l'application Gestion des demandes d'acompte.
b) Saisissez les données suivantes :
Zone
Valeur de données
Date du document
<date du jour>
Compte (dans la zone d'écran Client)
C615-F##
Code CGS
A
Compte (dans la zone d'écran Banque)
11100025
Montant (dans la zone d'écran Banque)
<montant de l'acompte + TVA> 33000
c) Cliquez sur le bouton Demandes.
d) Sélectionnez votre demande d'acompte dans la liste, puis cliquez sur le bouton Créer
acomptes.
e) Cliquez sur Comptabiliser pour sauvegarder vos données.
_______________________________
Description de SAP GUI du système backend
f) Dans le Menu SAP, sélectionnez Gestion comptable → Comptabilité
financière → Clients → Écriture → Acompte → Acompte.
Chapitre 8: Processus de gestion spécifiques


## PDF page 195

g) Saisissez les données comme indiqué dans la tâche.
h) Cliquez sur le bouton Demandes.
i) Sélectionnez la demande d'acompte dans la liste puis cliquez sur le bouton Créer
acomptes.
j) Cliquez sur
 Comptabiliser pour sauvegarder le document.
5. Exécutez la facturation partielle pour la première période de décompte.
Astuce :
supprimez tout d'abord le blocage de la facture au niveau de la date de
décompte correspondante, définie dans le calendrier de facturation. Ensuite,
lorsque vous créez le document de facturation, choisissez une date comprise
entre les dates de la première et de la seconde factures partielles).
Vous devez faire en sorte que le système calcule et intègre à la facture partielle le montant
total de l'acompte versé.
a) ___________________________________
Description de la barre de lancement SAP Fiori
Dans la barre de lancement de SAP Fiori, sélectionnez le groupe de vignettes Ventes
(Sales) et lancez l'application Modifier commande client.
b) Saisissez le numéro de commande généré à la tâche précédente et sélectionnez
Suite.
c) Sélectionnez le poste, puis cliquez sur
 Afficher détails du poste et
accédez à la page d'onglet Calendrier de facturation.
d) Supprimez le blocage du deuxième poste dans la liste.
e) Sauvegardez vos modifications et quittez l'application.
f) Sélectionnez le groupe de vignettes Documents de facturation (Billing Documents) et
lancez l'application Création de documents de facturation (VF01).
g) Saisissez votre numéro de commande généré à la tâche précédente et sélectionnez
Exécuter. Les informations suivantes sont affichées à l'écran :
●
Montant du premier document de facturation partielle
●
Acomptes effectués par le client et devant encore être rapprochés
h) Sauvegardez votre document de facturation.
_______________________________
Description de SAP GUI du système backend
i) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Modifier.
j) Confirmez votre numéro de commande client.
k) Sélectionnez le poste puis Saut → Poste → Calendrier de facturation.
Sujet: Traitement des acomptes


## PDF page 196

l) Supprimez le blocage du deuxième poste dans la liste.
m) Sauvegardez vos modifications et quittez la transaction.
n) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
o) Saisissez le numéro de commande que vous venez de créer et sélectionnez une date
de facture pour limiter ces dates selon les recommandations mentionnées ci-dessus.
Confirmez votre saisie. Deux postes figurent dans le document de facturation :
●
le montant du premier document de facturation partielle ;
●
les acomptes effectués par le client et devant encore être rapprochés.
p) Sauvegardez votre document de facturation.
6. Comment procéder pour n'imputer qu'une partie de l'acompte versé dans la première
facture partielle ?
Le type de condition AZWR sert de base au traitement des acomptes. Si vous ne voulez
effectuer qu'un décompte partiel, vous pouvez sélectionner le poste d'acompte à intégrer
dans le document de facturation, accéder à l'écran de détermination du prix et modifier la
valeur pour le type de condition AZWR.
7. Vérifiez le flux de documents de la commande client.
a) ___________________________
Description pour la barre de lancement de SAP Fiori
Dans la barre de lancement SAP Fiori, sélectionnez le groupe de vignettes Ventes
(Sales) et lancez l'application Modifier commande client.
b) Saisissez votre numéro de commande client généré au cours de cet exercice.
c) Sélectionnez Afficher flux doc.
_______________________________
Description de SAP GUI
d) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Modifier.
e) Confirmez votre numéro de commande client.
f) Sélectionnez Environnement → Afficher flux doc.
Chapitre 8: Processus de gestion spécifiques


## PDF page 197

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Traiter des acomptes
Sujet: Traitement des acomptes


## PDF page 198

Chapitre 8: Processus de gestion spécifiques


## PDF page 199

Chapitre 8
Sujet 3
Traitement des versements échelonnés
VUE D'ENSEMBLE DU SUJET
Ce sujet décrit le processus relatif aux versements échelonnés.
Exemple de gestion
Un client vous commande des marchandises. Après la livraison, vous lui facturez ces
marchandises. Il veut payer en plusieurs règlements. Pour cette raison, vous devez disposer
des connaissances suivantes :
●
savoir comment traiter des versements échelonnés.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Traiter des versements échelonnés
Calendrier des règlements
Figure 51: Calendrier des règlements
Un calendrier des règlements permet au client de payer en plusieurs règlements. Un seul
document de facturation est créé pour l'ensemble des versements. Pour l'impression de la
facture, le système se base sur ce document de facturation et ajoute les dates de règlements
individuels ainsi que les montants exacts correspondants.


## PDF page 200

À chaque versement, il crée une écriture dans le compte client concerné du module
Comptabilité financière.
Vous devez définir les conditions de versements échelonnés dans le Customizing.
Pour les définir, vous devez mentionner le nombre de règlements, le montant en pourcentage
et les conditions de paiement de chaque versement. Si vous imputez une facture liée à des
conditions de versement échelonné, le système se base sur ces informations pour générer le
nombre correspondant d'écritures dans la pièce comptable.
Comment traiter des versements échelonnés
Process installment payments.
The demo description is based on SAP GUI transactions and SAP Menu path. So when in
doubt leave it out.
1. Demonstrate the Sales and Distribution process by creating a standard order. Use the
following data:
Field
Data Value
Order Type
OR
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
PO Number
4712
Payment terms
R001
Material
P615-100
Order Quantity
10 PC
2. Deliver the order using shipping point 1010. Pick delivery and post goods issue. :
3. Create the billing document (with reference to delivery) with billing type F2.
SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Traiter des versements échelonnés
Chapitre 8: Processus de gestion spécifiques


## PDF page 201

Chapitre 8
Évaluation des connaissances
1.
Parmi les opérations commerciales suivantes, lesquelles sont idéales pour la facturation
périodique ?
Sélectionnez les réponses correctes.
A Contrat annuel de services pour des systèmes informatiques
B Contrat de leasing d'une propriété
C Installation d'une éolienne
D Exécution d'un projet de recherche et développement
2. Vous devez indiquer une date de fin afin d'exécuter un calendrier de facturation
périodique.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. Parmi les affirmations suivantes, laquelle s'applique à la facturation partielle et laquelle
s'applique à la facturation périodique ?
Sélectionnez les réponses correctes.
A Vous gérez la date par défaut pour la facturation périodique.
B Vous pouvez déterminer si la date de facture doit être mise à jour avec la date
réelle du jalon.
C Vous pouvez modifier dans le calendrier de facturation les dates pour lesquelles la
facturation a déjà été effectuée.
D Vous pouvez spécifier autant de dates que nécessaire par calendrier de
facturation.


## PDF page 202

4. Dans le Customizing, le type du calendrier de facturation est déterminé à partir du type de
poste par la zone Pertinence pour la facture.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
5. La demande d'acompte dans SD est automatiquement enregistrée dans le module
Comptabilité financière en tant que demande d'acompte.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
6. Pour les factures partielles et la facture finale, le rapprochement s'effectue
automatiquement durant l'impression de la facture
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
7.
Dans un calendrier des règlements, un seul document de facturation est créé pour
l'ensemble des versements échelonnés.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
Chapitre 8: Évaluation des connaissances


## PDF page 203

Chapitre 8
Évaluation des connaissances - Réponses
1.
Parmi les opérations commerciales suivantes, lesquelles sont idéales pour la facturation
périodique ?
Sélectionnez les réponses correctes.
A Contrat annuel de services pour des systèmes informatiques
B Contrat de leasing d'une propriété
C Installation d'une éolienne
D Exécution d'un projet de recherche et développement
2. Vous devez indiquer une date de fin afin d'exécuter un calendrier de facturation
périodique.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
3. Parmi les affirmations suivantes, laquelle s'applique à la facturation partielle et laquelle
s'applique à la facturation périodique ?
Sélectionnez les réponses correctes.
A Vous gérez la date par défaut pour la facturation périodique.
B Vous pouvez déterminer si la date de facture doit être mise à jour avec la date
réelle du jalon.
C Vous pouvez modifier dans le calendrier de facturation les dates pour lesquelles la
facturation a déjà été effectuée.
D Vous pouvez spécifier autant de dates que nécessaire par calendrier de
facturation.


## PDF page 204

4. Dans le Customizing, le type du calendrier de facturation est déterminé à partir du type de
poste par la zone Pertinence pour la facture.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
5. La demande d'acompte dans SD est automatiquement enregistrée dans le module
Comptabilité financière en tant que demande d'acompte.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
6. Pour les factures partielles et la facture finale, le rapprochement s'effectue
automatiquement durant l'impression de la facture
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
7.
Dans un calendrier des règlements, un seul document de facturation est créé pour
l'ensemble des versements échelonnés.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
Chapitre 8: Évaluation des connaissances - Réponses


## PDF page 205

CHAPITRE 9
Détermination des comptes
Sujet 1
Définition de la détermination des comptes
Exercice 12: Définir la détermination des comptes
OBJECTIFS DU CHAPITRE
●
Définir la détermination des comptes


## PDF page 206

Chapitre 9
Sujet 1
Définition de la détermination des comptes
VUE D'ENSEMBLE DU SUJET
Ce sujet décrit en détail les différents domaines dans lesquels s'effectue la détermination des
comptes. Il décrit également le processus de détermination des comptes basé sur la
détermination du compte de produits.
Exemple de gestion
Vous voulez que les produits, les réductions sur ventes et les taxes soient imputés
automatiquement aux comptes correspondants en Comptabilité financière dès la création
d'un document de facturation. Pour cette raison, vous devez disposer des connaissances
suivantes :
●
connaître les différents domaines utilisant la détermination des comptes ;
●
connaître le processus de détermination des comptes.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Définir la détermination des comptes


## PDF page 207

Domaines de la détermination des comptes
Figure 52: Utilisation de la détermination des comptes
Vous devez déterminer les comptes à imputer dans plusieurs domaines :
●
Les comptes généraux pour l'imputation du produit des ventes, des réductions sur ventes
et de la TVA sont déterminés automatiquement lors du transfert de données du document
de facturation au module FI.
●
Lorsque vous traitez une vente au comptant, il est nécessaire de définir un compte de
caisse dans le document (pas d'imputation à un compte client).
●
Le système peut déterminer un compte collectif différent du compte saisi dans la fiche du
payeur.
●
Si vous utilisez des cartes de paiement, l'imputation concernera également des comptes
généraux distincts.
Sujet: Définition de la détermination des comptes


## PDF page 208

Critères d'imputation
Figure 53: Critères d'imputation pour la facturation
Vous créez les comptes de produits dans le module FI pour pouvoir les inclure dans
différentes analyses et effectuer le rapprochement via la fonctionnalité d'analyse du compte
de résultat.
C'est pourquoi, vous pouvez définir plusieurs critères pour la détermination des comptes
appropriés.
Les critères suivants sont définis dans le système standard :
●
Plan comptable
●
Organisation commerciale
●
Groupe d'imputation pour les clients payeurs
Vous pouvez ainsi diviser les clients en différents groupes, clients nationaux et clients
étrangers, par exemple.
●
Groupe d'imputation article
Vous pouvez ainsi diviser les articles en différents groupes, services et articles
commerciaux, par exemple.
●
Clé de compte
Ces clés sont affectées aux types de conditions dans les schémas de calcul. Vous pouvez
alors imputer des conditions, par exemple, des conditions de transport, à des comptes de
produits spéciaux réservés aux transports.
Vous devez vous assurer que le paramétrage de la détermination des comptes correspond au
paramétrage défini dans FI et CO.
Chapitre 9: Détermination des comptes


## PDF page 209

Détermination du compte de produits
Figure 54: Détermination du compte de produits
Le système utilise la technique des conditions pour déterminer le compte.
Dans le type de document de facturation, un schéma de détermination de comptes est défini
pour permettre la détermination des comptes généraux.
Ce schéma contient un ou plusieurs types de conditions, chacun affecté d'une séquence
d'accès.
La séquence d'accès comprend plusieurs accès correspondant à des tables de conditions.
Ces dernières comprennent les zones dont dépend la détermination du compte de produits.
Les données du document sont utilisées pour renseigner les zones clés, afin de permettre au
système de rechercher un compte général correspondant à la combinaison de zones
concernée.
Lorsqu'un accès lui permet de déterminer un compte général, le système spécifie ce dernier
au niveau du document comptable et arrête la recherche.
Astuce :
Le compte d'imputation de la TVA n'est pas défini dans la détermination des
comptes de l'Administration des ventes. L'imputation correspondante est
mémorisée dans le Customizing de la Comptabilité financière sous Paramétrages
de base de la comptabilité financière → TVA sur C.A. → Écriture → Mémoriser les
comptes de TVA.
Sujet: Définition de la détermination des comptes


## PDF page 210

Comment adapter l'imputation
Adjust the account assignment.
Demo it according to the exercise or use SAP GUI transactions.
1. Display the billing documents that you have already created. Demonstrate the
corresponding information stored for account determination.
2. Display the accounting document, and explain the accounts for sales revenues.
3. To see which accounts were assigned, go to the process overview by choosing
Environment →  Acc.determ.analysis →  Revenue accounts.
4. Define account assignment groups for customer and material in Customizing for Sales
and Distribution under Basic Functions →  Account Assignment/Costing →  Revenue
Account Determination → Check Master Data Relevant for Account Assignment.
5. Create a new account assignment group for customers. Enter group 99 and description
Affiliat.comp.reven. and create a new assignment group for customers.
6. Assign the new account assignment group for customers (group 99) in customer C615-
A00 in the customer master record (transaction BP. Display in BP role CUSTOMER -
choose SALES AND DISTRIBUTION show the data for billing).
7. In Customizing, assign account keys to condition types, pricing procedure RVAA01.
Assign account key PR00 (ERL), and KF00 (ERF) or K007 (ERS).
Comment interpréter le schéma détermination du compte
Interpret the account determination procedure.
Demo it according to the exercise or use SAP GUI transactions.
1. In Customizing, display the account determination procedure used to determine G/L
accounts with the billing type F2. Navigate to Customizing for Sales and Distribution under
Basic Functions →  Account Assignment/Costing →  Revenue Account Determination →
Define and Assign Account Determination Procedures.
2. Select the activity Define Account Determination Procedure. Select account determination
procedure KOFI00 and double-click Control data in the Document Structure pane.
3. Explain the account determination process via condition techniques for procedure
KOFI00. Account determination type KOFI is the access sequence KOFI.
4. Demonstrate the accesses from which access sequence KOFI is derived.
5. Demonstrate assignment of G/L accounts for condition table 001:
Field
Data Value
App (application)
CndTy. (condition type)
KOFI
ChAc (chart of accounts)
YCOA
Chapitre 9: Détermination des comptes


## PDF page 211

Field
Data Value
SOrg. (sales organization)
1010
Using account key ERL, account assignment group for customer as 01, and account
assignment group for material as 01, the system determines G/L account 41000000 to
post sales revenues.
Comment définir une nouvelle imputation
Set up a new account assignment.
Demo it according to the exercise or use SAP GUI transactions.
1. Demonstrate new account assignment in the condition table 001 for the account
assignment group used for customer 99. Navigate to Customizing for Sales and
Distribution under Basic Functions →  Account Assignment/Costing →  Revenue Account
Determination →  Assign G/L Accounts.
2. Select table 001 and choose
 (Choose).
3. Choose the New Entries button and enter the following data:
Field
Data Value
App (application)
CndTy. (condition type)
KOFI
ChAc (chart of accounts)
INT
SOrg. (sales organization)
1010
AAG (customer account assignment
group)
AAG (material account assignment group)
ActKy (account key)
ERL
G/L Account
49000000
4. Test the new configuration by creating a standard order. Use the following data:
Field
Data Value
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
PO Number
10-KOFI
Material
P615-100
Sujet: Définition de la détermination des comptes


## PDF page 212

Field
Data Value
Order Quantity
10 PC
Create delivery for the order using shipping point 1010. Carry out picking and posting for
the goods issue.
Analyze the posting in Financial Accounting by viewing the accounting document.
5. Create the billing document (with reference to delivery) with billing type F2.
6. Display the new sales revenue account 49000000 in the accounting document.
7. If necessary, call up the account assignment analysis again.
Chapitre 9: Détermination des comptes


## PDF page 213

Chapitre 9
Exercice 12
Définir la détermination des comptes
Exemple de gestion
Vous voulez améliorer, dans votre entreprise, la procédure de détermination des comptes en
Comptabilité financière, pour les accords passés avec vos clients. Certains de vos clients sont
des entreprises liées. À l'avenir, vous voulez pouvoir imputer le produit des ventes concernant
ces clients à un compte de produits spécial pour les entreprises liées. Vous devez créer de
nouveaux groupes d'imputation pour ces clients afin de faire la distinction entre vos clients
standard et les entreprises liées. Vous devez donc savoir comment exécuter la procédure de
détermination des comptes.
Le client C615-B## représente l'une de ces entreprises liées. À l'avenir, vous voulez imputer
le produit des ventes provenant de ce client au compte 49000000.
Vous allez modifier les options du Customizing. Utilisez donc SAP GUI dans le système
backend pour cet exercice.
1. Dans le Customizing, définissez un nouveau groupe d'imputation. Définissez le groupe
comme suit : < 80 + ## > (par exemple, pour le groupe 13, vous saisissez
< 80 + 13 > = 93). Saisissez la description Groupe ##.
2. Modifiez l'affectation du groupe de comptes pour le client C615-B##. Dans la fiche client,
remplacez le groupe de comptes par votre entrée votre < 80 + ## >.
Astuce :
Utilisez le domaine commercial 1010/10/00 (organisation commerciale :
1010/Canal de distribution : 10/Secteur d'activité : 00).
Paramétrez les options requises pour imputer les produits des ventes d'entreprises liées au
compte 49000000.
1. Vérifiez quelle est la clé de compte correspondant au type de condition PR00 dans le
schéma de calcul que vous utilisez.
Notez la clé de compte _______________.
2. Affichez la pièce comptable correspondant au document de facturation que vous avez
déjà créé pour la commande client standard avec le numéro de commande d'achat
##S4615-A6.


## PDF page 214

À quel compte le produit des ventes était-il imputé jusqu'à présent ?
3. Dans le Customizing, consultez la séquence d'accès. Vous souhaitez utiliser comme table
de clés l'organisation commerciale, le groupe d'imputation clients, le groupe d'imputation
articles et la clé de compte.
Dans quelle table de conditions devez-vous entrer des données ?
4. Vous connaissez maintenant tous les éléments nécessaires pour créer la nouvelle entrée
(voir liste). Affectez le nouveau compte général 49000000 à votre nouvelle combinaison.
●
L'organisation commerciale est 1010.
●
Le groupe d'imputation clients est < 80 + ## >.
●
Le groupe d'imputation articles est 01.
●
La clé de compte est identique à celle utilisée dans la sous-tâche ERL précédente.
Créez l'entrée nécessaire dans la table 001 en saisissant les données suivantes :
Zone
Valeur de données
Apl. (application)
T.Cond (type de condition)
KOFI
PlCp (plan comptable)
YCOA
OrgCm (organisation commerciale)
1010
GIC (groupe d'imputation clients)
<80 + ##>
GImA (groupe d'imputation articles)
CléCp (clé de compte)
ERL
Compte général
49000000
5. Affichez le résultat de votre action en réalisant le processus de vente d'une commande
client standard (CDCL). Utilisez les données suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-B##
Chapitre 9: Détermination des comptes


## PDF page 215

Zone
Valeur de données
Réf. Client
##S4615-KO
Article
P615-1##
Quantité d'ordre
1 pce
Créez une livraison pour cette commande client avec le point d'expédition 1010. Exécutez
le prélèvement et l'enregistrement de la sortie de marchandises.
Consultez la pièce comptable et analysez l'écriture passée en Comptabilité financière.
Sujet: Définition de la détermination des comptes


## PDF page 216

Chapitre 9
Solution 12
Définir la détermination des comptes
Exemple de gestion
Vous voulez améliorer, dans votre entreprise, la procédure de détermination des comptes en
Comptabilité financière, pour les accords passés avec vos clients. Certains de vos clients sont
des entreprises liées. À l'avenir, vous voulez pouvoir imputer le produit des ventes concernant
ces clients à un compte de produits spécial pour les entreprises liées. Vous devez créer de
nouveaux groupes d'imputation pour ces clients afin de faire la distinction entre vos clients
standard et les entreprises liées. Vous devez donc savoir comment exécuter la procédure de
détermination des comptes.
Le client C615-B## représente l'une de ces entreprises liées. À l'avenir, vous voulez imputer
le produit des ventes provenant de ce client au compte 49000000.
Vous allez modifier les options du Customizing. Utilisez donc SAP GUI dans le système
backend pour cet exercice.
1. Dans le Customizing, définissez un nouveau groupe d'imputation. Définissez le groupe
comme suit : < 80 + ## > (par exemple, pour le groupe 13, vous saisissez
< 80 + 13 > = 93). Saisissez la description Groupe ##.
a) Sélectionnez Customizing (code de transaction SPRO) dans votre menu des Favoris.
b) Accédez au Customizing. Cliquez sur le bouton
Guide de référence SAP.
c) Sélectionnez le Guide d'implémentation : Administration des ventes
(ADV) → Fonctions de base → Imputation/calcul du coût de revient → Détermination
du compte de produits → Vérifier les données de base intéressant l'imputation.
d) Sélectionnez l'entrée Clients : groupes d'imputation et cliquez sur le bouton
Sélectionner.
e) Cliquez sur le bouton Nouvelles entrées.
f) Saisissez le groupe d'imputation < 80 + ## > et la description Groupe ## et
sauvegardez votre nouvelle entrée.
Astuce :
Par exemple, pour le groupe 13, saisissez le groupe d'imputation
< 80 + 13 > 93. Saisissez la description Groupe 13.
2. Modifiez l'affectation du groupe de comptes pour le client C615-B##. Dans la fiche client,
remplacez le groupe de comptes par votre entrée votre < 80 + ## >.


## PDF page 217

Astuce :
Utilisez le domaine commercial 1010/10/00 (organisation commerciale :
1010/Canal de distribution : 10/Secteur d'activité : 00).
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Données de base → Partenaire → Client → Modifier → Administration des
ventes (ADV).
b) Saisissez les données suivantes et confirmez vos entrées :
Zone
Valeur de données
Client
C615-B##
Organis. commerciale
1010
Canal distribution
Secteur d'activité
c) Sélectionnez Administration des ventes(ADV) et accédez à l'onglet Facture.
d) Dans la zone Grpe imputation clt, saisissez votre nouveau groupe d'imputation
< 80 + ## >.
e) Sauvegardez vos modifications.
Paramétrez les options requises pour imputer les produits des ventes d'entreprises liées au
compte 49000000.
1. Vérifiez quelle est la clé de compte correspondant au type de condition PR00 dans le
schéma de calcul que vous utilisez.
Notez la clé de compte _______________.
a) Sélectionnez Customizing (code de transaction SPRO) dans votre menu des Favoris.
b) Accédez au Customizing. Cliquez sur le bouton
 Guide de référence SAP.
c) Dans le Customizing, accédez au Guide d'implémentation : Administration des ventes
(ADV) → Fonctions de base → Imputation/calcul du coût de revient → Détermination
du compte de produits → Définir et affecter le code opération comptable.
d) Sélectionnez l'activité Affecter la clé compte et cliquez sur le bouton
 Sélectionner.
e) Utilisez le bouton
 Positionner pour rechercher et sélectionner le schéma de calcul
standard RVAA01. Le type de condition PR00 est affecté à la clé de compte ERL.
2. Affichez la pièce comptable correspondant au document de facturation que vous avez
déjà créé pour la commande client standard avec le numéro de commande d'achat
##S4615-A6.
Sujet: Définition de la détermination des comptes


## PDF page 218

À quel compte le produit des ventes était-il imputé jusqu'à présent ?
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Afficher.
b) Appuyez sur la touche d'aide à la recherche (F4) dans la zone Commande client. Dans
l'onglet Documents de vente par numéro de commande chez client, dans la zone N°
commande d'achat, saisissez ##S4615-A6. Confirmez votre saisie et sélectionnez le
document dans la liste.
c) Accédez au flux de documents en sélectionnant Environnement →  Afficher flux doc.
d) Dans le flux de documents, sélectionnez votre première pièce comptable et cliquez sur
le bouton Afficher document.
e) Tous les produits de ventes ont été imputés au compte 41000000 jusqu'à présent.
3. Dans le Customizing, consultez la séquence d'accès. Vous souhaitez utiliser comme table
de clés l'organisation commerciale, le groupe d'imputation clients, le groupe d'imputation
articles et la clé de compte.
Dans quelle table de conditions devez-vous entrer des données ?
a) Accédez au Customizing de l'Administration des ventes (ADV) sous Fonctions de
base → Imputation/calcul du coût de revient → Détermination du compte de
produits → Définir séquences d'accès et types de détermin. du compte.
b) Sélectionnez l'activité Gérer les séquences d'accès pour détermination des comptes et
cliquez sur le bouton
 Sélectionner.
c) Affichez les accès de la séquence d'accès KOFI et les zones clés sélectionnées. Vous
devez gérer ces données pour la table de conditions 001 comprenant les zones clés
des organisations commerciales, des groupes d'imputation clients et articles et des
clés de comptes.
4. Vous connaissez maintenant tous les éléments nécessaires pour créer la nouvelle entrée
(voir liste). Affectez le nouveau compte général 49000000 à votre nouvelle combinaison.
●
L'organisation commerciale est 1010.
●
Le groupe d'imputation clients est < 80 + ## >.
●
Le groupe d'imputation articles est 01.
●
La clé de compte est identique à celle utilisée dans la sous-tâche ERL précédente.
Créez l'entrée nécessaire dans la table 001 en saisissant les données suivantes :
Zone
Valeur de données
Apl. (application)
Chapitre 9: Détermination des comptes


## PDF page 219

Zone
Valeur de données
T.Cond (type de condition)
KOFI
PlCp (plan comptable)
YCOA
OrgCm (organisation commerciale)
1010
GIC (groupe d'imputation clients)
<80 + ##>
GImA (groupe d'imputation articles)
CléCp (clé de compte)
ERL
Compte général
49000000
a) Accédez au Customizing de l’Administration des ventes (ADV) sous Fonctions de
base →  Imputation/calcul du coût de revient →  Détermination du compte de
produits →  Affecter les comptes généraux.
b) Sélectionnez la table 001 et cliquez sur le bouton
 Sélectionner.
c) Cliquez sur le bouton Nouvelles entrées et saisissez les données suivantes :
Zone
Valeur de données
Apl. (application)
T.Cond (type de condition)
KOFI
PlCp (plan comptable)
YCOA
OrgCm (organisation commerciale)
1010
GIC (groupe d'imputation clients)
80+##
GImA (groupe d'imputation articles)
CléCp (clé de compte)
ERL
Compte général
49000000
d) Enfin,
 sauvegardez votre nouvelle entrée.
5. Affichez le résultat de votre action en réalisant le processus de vente d'une commande
client standard (CDCL). Utilisez les données suivantes :
Zone
Valeur de données
Type de commande
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-B##
Réf. Client
##S4615-KO
Sujet: Définition de la détermination des comptes


## PDF page 220

Zone
Valeur de données
Article
P615-1##
Quantité d'ordre
1 pce
Créez une livraison pour cette commande client avec le point d'expédition 1010. Exécutez
le prélèvement et l'enregistrement de la sortie de marchandises.
Consultez la pièce comptable et analysez l'écriture passée en Comptabilité financière.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.
b) Saisissez le type de commande CDCL pour la commande client standard et les
données du domaine commercial (1010/10/00). Saisissez tous les autres détails
comme indiqué dans la tâche. Puis, sauvegardez votre commande client.
c) Dans le Menu SAP, sélectionnez Expédition et transport → Livraison
sortante → Créer → Document individuel → Avec référence à la commande client.
d) Saisissez le point d'expédition 1010 et la date de sélection <10 jours à compter de la
date du jour>. Confirmez votre saisie.
e) Accédez à l'onglet Prélèvement et dans la zone Quantité prélevée, saisissez 1.
f) Cliquez ensuite sur le bouton : Enreg. sortie march.
g) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
h) Confirmez le numéro du document de livraison et sauvegardez le document de
facturation.
i) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Afficher.
j) Confirmez le numéro du document de facturation et
 sauvegardez le document.
k) Sélectionnez Facture → Afficher et cliquez sur
 Gestion comptable.
l) Sélectionnez la pièce comptable, puis cliquez sur
 Afficher la pièce. Les produits
des ventes devraient désormais être imputés au compte 49000000. Dans le
document de facturation, vous pouvez cliquer sur Environnement → Analyse
imputation → Compte de produits pour obtenir plus d'informations sur la
détermination des comptes.
Chapitre 9: Détermination des comptes


## PDF page 221

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Définir la détermination des comptes
Sujet: Définition de la détermination des comptes


## PDF page 222

Chapitre 9: Détermination des comptes


## PDF page 223

CHAPITRE 10
Interface entre l'Administration
des ventes et la Comptabilité
financière
Sujet 1
Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière
Exercice 13: Ajustement de l'interface entre l'Administration des ventes et la
Comptabilité financière
OBJECTIFS DU CHAPITRE
●
Ajuster l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 224

Chapitre 10
Sujet 1
Ajustement de l'interface entre
l'Administration des ventes et la Comptabilité
financière
VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux zones sélectionnées de l'interface existant entre l’Administration
des ventes et la Comptabilité financière. Il explique comment éviter la création automatique
de pièces comptables et décrit les différentes zones permettant de transférer les données de
l'Administration des ventes à la Comptabilité financière.
Exemple de gestion
Vous voulez effectuer un contrôle supplémentaire de la facture avant de transférer les
données en Comptabilité financière. Vous voulez également transférer des informations
spécifiques dans ce module, informations permettant d'affecter et de différencier différents
éléments en Comptabilité. Pour cette raison, vous devez disposer des connaissances
suivantes :
●
savoir comment éviter la génération automatique de pièces comptables ;
●
savoir comment utiliser différentes zones pour le transfert des données de
l'Administration des ventes à la Comptabilité financière ;
●
savoir comment des partenaires sont transférés à partir de l'Administration des ventes
dans l'optique de la relation centrale/succursales ;
●
connaître l'incidence des écritures négatives, du type de document et des avoirs à date de
valeur sur le type de document de facturation.
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Ajuster l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 225

Transfert vers le module Comptabilité financière
Figure 55: Transfert vers le module Comptabilité financière
Le système transmet au module Comptabilité financière des données de facturation issues de
factures, d'avoirs et de notes de débit et les impute aux comptes appropriés.
Vous pouvez modifier les données suivantes avant de créer une pièce comptable :
●
Date de facture
●
Détermination du prix
●
Détermination des comptes
●
Données de détermination des messages
Après la comptabilisation, vous ne pouvez plus modifier que les données des messages.
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 226

Blocage de comptabilisation
Figure 56: Blocage de comptabilisation
Normalement, le système transfère automatiquement les données concernant la gestion
comptable au module Comptabilité financière.
Toutefois, il se peut que vous ne souhaitiez pas que les données de certains types de
document de facturation soient transférées. Dans ce cas, vous pouvez définir un blocage de
comptabilisation pour les types de document de facturation concernés.
Le système ne généra alors les pièces comptables que lorsque vous aurez validé les
documents de facturation.
Vous pouvez ainsi générer tout d'abord les documents de facturation dans le module
Administration des ventes, les imprimer puis les transférer dans le module Comptabilité
financière.
En procédant ainsi, vous pouvez notamment améliorer les performances de votre système.
Astuce :
Le système génère toutes les pièces comptables ou n'en génère aucune. De ce
fait, si vous avez activé le blocage de comptabilisation ou que des erreurs se sont
produites durant la détermination du compte, le système ne créera pas de pièces
de comptabilité analytique. Pour permettre leur création, vous devez tout
d'abord désactiver le blocage ou corriger l'erreur.
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 227

Numéros de référence
Figure 57: Numéros de référence et numéros d'affectation
Vous pouvez renseigner automatiquement les zones Référence et Affectation de la pièce
comptable à partir des numéros repris de documents de l'Administration des ventes.
Le numéro de référence, spécifié dans l'en-tête de la pièce comptable, est utilisé à des fins de
rapprochement.
Le numéro d'affectation, spécifié au niveau du poste client, sert à trier les numéros de postes.
Dans le Customizing du pilotage de la copie pour la facturation, vous pouvez définir les
numéros à transmettre en tant que numéros de référence ou en tant que numéros
d'affectation.
Types de numéros
Le tableau suivant énumère et décrit les types de numéros.
Type de numéro
Description
A
Numéro de commande d'achat
B
Numéro de commande client
Numéro de livraison
Numéro de livraison externe
E
Numéro de document de facturation
F
Numéro de livraison externe si disponible, si-
non numéro de livraison
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 228

Numéros de référence dans les relevés de factures
Figure 58: Numéros de référence dans les relevés de factures
Vous devez tout d'abord créer des documents de facturation puis les imputer dans le module
Comptabilité financière avant de les regrouper dans un relevé de factures. Le numéro
sauvegardé comme numéro de référence au niveau du paramétrage de la copie est alors
transféré dans le module Comptabilité financière.
Une fois la liste de factures créée, le numéro de référence provenant de la liste de factures
remplace les numéros de référence des documents de facturation individuels. Ceci vous
permet de comptabiliser des encaissements avec le numéro de la liste de factures.
Types de pièces basées sur la transaction
Figure 59: Types de pièces basées sur la transaction
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 229

Vous pouvez différencier des documents les uns des autres dans le module Comptabilité
financière en utilisant le type de pièce. Ce type est mémorisé dans l'en-tête de document.
Jusqu'à présent, le système affectait tous les documents de l'Administration des ventes du
type RV défini en Comptabilité financière.
Vous pouvez effectuer différentes analyses en Comptabilité financière et contrôler différents
critères de tri en utilisant la zone Type de pièce au niveau de la configuration du type de
document de facturation. Cela vous permet de prédéfinir le type de pièce pour chaque type
de document de facturation.
Si cette zone n'est pas renseignée, le système continuera à transférer le type de pièce RV au
module Comptabilité financière via l'interface Comptabilité financière/Contrôle de gestion
(FI/CO).
Centrale et succursales
Figure 60: Centrale et succursales
Durant la gestion des données de base, vous pouvez représenter la relation entre la centrale
et ses succursales.
Pour représenter cette relation, vous pouvez utiliser les fonctions partenaire dans le module
Administration des ventes ou la zone Centrale dans les données comptables de la fiche client.
Jusqu'à présent, vous deviez gérer les données comptables entièrement pour les deux clients
(centrale et succursale). S'il manquait des données comptables pour la succursale, le
système créait les documents de facturation pour cette dernière, mais ne pouvait les
reprendre dans le module Comptabilité financière.
Dans l'Administration des ventes, les fonctions partenaire peuvent varier considérablement
en fonction des impératifs des clients. Par exemple, le donneur d'ordre peut également
remplir la fonction de réceptionnaire.
Les clients ont donc demandé s'il était possible d'éviter la gestion des données comptables
lorsque la succursale d'une société agit en tant que donneur d'ordre, c'est-à-dire comme
client à part entière de l'Administration des ventes.
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 230

Vous pouvez utiliser la zone Succursale/Centrale au niveau du type de document de
facturation pour contrôler les fonctions partenaire du document de facturation à reprendre
dans le module Comptabilité financière. Le système se base alors sur cette zone pour
déterminer s'il doit saisir le donneur d'ordre ou le payeur dans la zone KUNNR (numéro client)
de l'en-tête de facturation.
Si vous ne renseignez pas la zone Succursale/Centrale, le système ignore toute relation
mémorisée au niveau de la zone Centrale. En ce qui concerne les autres options, la relation
mémorisée en Comptabilité financière a priorité sur la relation décrite par les fonctions
partenaire de l'Administration des ventes.
Écritures négatives
Figure 61: Écritures négatives
Dans le système SAP standard, les annulations et les avoirs sont imputés du côté opposé aux
créances dans le compte client.
Dans la ligne de totaux du compte, la "vente" figure en règle générale dans les deux côtés du
compte. Le total n'est pas nul alors qu'aucune vente effective n'a eu lieu.
Certains clients souhaitent donc pouvoir imputer les avoirs et les annulations du même côté
que les créances. Les comptes présentent ainsi un solde nul. La ligne de totaux est alors nulle,
signifiant qu'aucune vente n'a eu lieu.
Si cette option vous intéresse, cochez la zone Écriture négative pour les types de document
de facturation correspondant aux avoirs et aux annulations.
Le système reprend cette information dans le module Comptabilité financière via l'interface
FI/CO.
Cette option modifie uniquement l'affichage des postes non soldés. Elle n'a aucune incidence
sur les processus de Comptabilité financière.
Remarque :
L'enregistrement d'écritures négatives s'effectue dans le module Comptabilité
financière uniquement si la société l'autorise. Ceci est contrôlé dans la table 001.
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 231

Avoirs avec date de valeur
Figure 62: Avoirs avec date de valeur
Lors de la création de demandes d'avoir se référant à un document de facturation, les dates
de facture (date de base pour les délais de paiement) étaient différentes, jusqu'à présent,
dans les deux documents. Il était impossible de rapprocher les créances des dettes.
Vous pouvez maintenant utiliser la période correspondant à la date de base pour les délais de
paiement du document de facturation pour affecter une date de valeur à l'avoir.
Vous disposez désormais d'une zone Note de crédit avec date de valeur au niveau du type de
document de facturation pour piloter l'affectation d'une date de valeur aux avoirs.
Si vous ne renseignez pas cette zone, la procédure habituelle s'applique, c'est-à-dire que
l'avoir est échu immédiatement à la date de facture. La date de base pour les délais de
paiement correspond à la date de facture de l'avoir. Le rapprochement des dettes a lieu
durant le cycle de paiement suivant dans le module Comptabilité financière.
Si vous sélectionnez la zone Note de crédit avec date de valeur dans l'avoir, le document de
facturation de référence ne sera pas rapproché. De plus, si la date de base pour les délais de
paiement du document de facturation d'origine est postérieure à la date de facture définie
dans l'avoir, le système détermine la date de base pour les délais de paiement à partir du
document de facturation d'origine dans la zone Date de valeur (VALDT) de l'avoir.
En revanche, si la date de base pour les délais de paiement est antérieure à la date de facture
actuelle dans l'avoir, il ne copie pas la date.
Comment utiliser un blocage de comptabilisation
Use a posting block.
Perform this demo according to the exercise or use SAP GUI transactions.
1. In Customizing, set a posting block for trade fair type ZF20.
2. Test the new configuration. Create an order with the following data:
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 232

Field
Data Value
Order Type
ZA20
Sales Organization
1010
Distribution Channel
Division
Sold-To Party
C615-A00
PO Number
11-BS
Material
P615-100
Order Quantity
10 PC
3. Deliver the order using shipping point 1010. Pick delivery and post goods issue (via
transfer order).
4. Create the billing document with reference to delivery with billing type ZF20. The system
issues a message to tell you that the accounting documents have not been created.
5. Display the options available for releasing a billing document.
●
Release via Billing Document →  Change, and choosing
 ( Release ToAccounting).
●
Release via Billing Document →  Blocked Billing Docs, and choosing
 ( Release to
Accounting).
Comment définir le transfert de valeurs de zones
Define the transfer of field values.
Demo this according to the exercise or use SAP GUI transactions. When in doubt leave it out.
1. Display the accounting document for a billing document. Demonstrate the information
used to fill the reference number and allocation number fields.
2. Demonstrate how to define the filling of these fields in copying control in Customizing.
Comment adapter un type de document de facturation pour influencer le transfert de
données vers le module Comptabilité financière
Adjust a billing type to influence the data transfer to Financial Accounting.
1. Go to billing type F2 in Customizing to demonstrate the settings for the following fields:
●
Document Type
●
Branch/Head office
●
Negative posting
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 233

●
Credit memo w/ValDat
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 234

Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 235

Chapitre 10
Exercice 13
Ajustement de l'interface entre
l'Administration des ventes et la Comptabilité
financière
Exemple de gestion
Vous voulez toujours contrôler les conditions de paiement des documents de facturation
établis à l'occasion de foires avant de transmettre ces documents au module Comptabilité
financière. Vous voulez donc valider ces documents individuellement au lieu de les
transmettre automatiquement au module Comptabilité financière. Vous devez donc savoir
comment adapter l'interface entre l'Administration des ventes et la Comptabilité financière.
Effectuez le paramétrage approprié afin que les documents de facturation Foire ne soient pas
transmis à la Comptabilité financière dès leur création.
Vous allez modifier les options du Customizing. Pour cela, utilisez SAP GUI dans le système
backend pour cet exercice.
1. Définissez les paramètres pour le type de document de facturation Foire ZF## qui sont
nécessaires pour obtenir le résultat escompté.
2. Testez les résultats dans le menu SAP et réalisez tout le processus de vente pour votre
commande Foire ##.
Créez une commande client à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
ZA## (commande Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. Client
##S4615-BS
Article
P615-1##
Quantité d'ordre
1 pce
Créez la livraison pour votre commande Foire ## avec le point d'expédition 1010.
Exécutez le prélèvement et l'enregistrement de la sortie de marchandises.
Créez le document de facturation.


## PDF page 236

Quel message le système affiche-t-il lorsque vous sauvegardez le document de
facturation ?
3. Après avoir contrôlé les conditions de paiement, quelle est l'étape nécessaire pour créer
les pièces comptables ?
Il existe deux façons d'effectuer cette étape. Décrivez-les.
4. Utilisez l'une de ces deux méthodes pour exécuter cette étape et créer les pièces
comptables.
Recherchez les numéros de l'Administration des ventes figurant déjà dans la pièce comptable
après facturation des commandes de foire.
1. Affichez une pièce comptable pour un document de facturation de type Foire déjà créé.
Quel sont les deux numéros repris et à quel niveau les trouvez-vous ?
2. Quels numéros de l'Administration des ventes permettent de renseigner les zones en
question ?
3. À quel niveau du Customizing effectuez-vous ce paramétrage ? Procédez au paramétrage.
À l'avenir, vous voulez transférer d'autres informations lors du traitement des commandes
passées à l'occasion de foires.
1. Configurez le système de façon à ce qu'il transfère, en vue du rapprochement, des
numéros de commandes clients lors de la facturation de vos commandes de foire se
référant à des livraisons.
2. Utilisez l'option permettant de trier des postes individuels par numéro de document de
facturation repris de l'Administration des ventes.
3. Testez les résultats et réalisez tout le processus de vente pour votre commande Foire ##.
Créez une commande client à l'aide des données suivantes :
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 237

Zone
Valeur de données
Type de commande
ZA## (commande Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. Client
##S4615-Réf
Article
P615-1##
Quantité d'ordre
1 pce
Créez la livraison pour votre commande Foire ## avec le point d'expédition 1010.
Exécutez le prélèvement et l'enregistrement de la sortie de marchandises.
Créez le document de facturation.
Passez à la pièce comptable pour rechercher les informations correspondantes.
Attention :
Le blocage de comptabilisation pour la commande prise lors d'une foire est
toujours actif.
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 238

Chapitre 10
Solution 13
Ajustement de l'interface entre
l'Administration des ventes et la Comptabilité
financière
Exemple de gestion
Vous voulez toujours contrôler les conditions de paiement des documents de facturation
établis à l'occasion de foires avant de transmettre ces documents au module Comptabilité
financière. Vous voulez donc valider ces documents individuellement au lieu de les
transmettre automatiquement au module Comptabilité financière. Vous devez donc savoir
comment adapter l'interface entre l'Administration des ventes et la Comptabilité financière.
Effectuez le paramétrage approprié afin que les documents de facturation Foire ne soient pas
transmis à la Comptabilité financière dès leur création.
Vous allez modifier les options du Customizing. Pour cela, utilisez SAP GUI dans le système
backend pour cet exercice.
1. Définissez les paramètres pour le type de document de facturation Foire ZF## qui sont
nécessaires pour obtenir le résultat escompté.
a) Dans le système backend SAP, sélectionnez le Customizing (code de transaction
SPRO dans vos Favoris.
b) Accédez au Customizing et cliquez sur le bouton
 Guide de référence SAP.
c) Dans l'IMG : Administration des ventes (ADV) → FacturationFacturesDéfinir les types
de facture.
d) Sélectionnez le type de document de facturation Foire ZF## puis cliquez sur
Détail.
e) Cochez la case Blocage comptabil. et sauvegardez vos modifications.
2. Testez les résultats dans le menu SAP et réalisez tout le processus de vente pour votre
commande Foire ##.
Créez une commande client à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
ZA## (commande Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. Client
##S4615-BS


## PDF page 239

Zone
Valeur de données
Article
P615-1##
Quantité d'ordre
1 pce
Créez la livraison pour votre commande Foire ## avec le point d'expédition 1010.
Exécutez le prélèvement et l'enregistrement de la sortie de marchandises.
Créez le document de facturation.
Quel message le système affiche-t-il lorsque vous sauvegardez le document de
facturation ?
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.
b) Saisissez les données comme indiqué dans la tâche.
c) Dans le Menu SAP, sélectionnez Expédition et transport → Livraison
sortante → Créer → Document individuel → Avec référence à la commande client.
d) Saisissez le point d'expédition 1010 et remplacez la date de sélection par <date du
jour + 10 jours>. Confirmez votre saisie.
e) Accédez à l'onglet Prélèvement et dans la zone Quantité prélevée, saisissez 1.
f) Cliquez ensuite sur le bouton Enreg. sortie march.
g) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
h) Confirmez le numéro du document de livraison et sauvegardez le document de
facturation. Le message suivant est affiché :
Document ... sauvegardé (aucune écriture au journal générée)
3. Après avoir contrôlé les conditions de paiement, quelle est l'étape nécessaire pour créer
les pièces comptables ?
Il existe deux façons d'effectuer cette étape. Décrivez-les.
Vous pouvez, d'une part, appeler explicitement le document de facturation en mode de
modification puis cliquer sur le bouton
 (Validation comptabilité financière) afin de
lancer le transfert des données vers la Comptabilité financière. L'autre solution est de
transférer de manière groupée les documents de facturation bloqués.
4. Utilisez l'une de ces deux méthodes pour exécuter cette étape et créer les pièces
comptables.
a) Pour transférer de manière groupée des documents de facturation bloqués, dans le
Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Factures bloquées (code de transaction VXF3).
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 240

b) Saisissez l'organisation commerciale 1010 et <votre ID utilisateur> dans la zone Saisi
par. Dans la zone d'écran Incomplet: Raison, cochez la case Blocage de la comptabilité.
Exécutez le programme.
c) Le document de facturation créé ci-dessus doit figurer dans la liste. Sélectionnez le
document de facturation puis cliquez sur
 (Validation comptabilité financière).
Recherchez les numéros de l'Administration des ventes figurant déjà dans la pièce comptable
après facturation des commandes de foire.
1. Affichez une pièce comptable pour un document de facturation de type Foire déjà créé.
Quel sont les deux numéros repris et à quel niveau les trouvez-vous ?
Le numéro de référence et le numéro d'affectation ont été transférés vers la Comptabilité
financière. Le numéro de référence figure au niveau de l'en-tête et sert durant le
rapprochement. Le numéro d'affectation sauvegardé au niveau du poste sert pour le tri
des postes individuels.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Afficher.
b) Sélectionnez
 Gestion comptable.
c) Sélectionnez la pièce comptable puis cliquez sur
 Afficher la pièce.
d) Consultez les zones indiquant le numéro de référence et le numéro d'affectation.
2. Quels numéros de l'Administration des ventes permettent de renseigner les zones en
question ?
La zone Référence comporte le numéro de commande d'achat. La zone Affectation
comporte le numéro de livraison (double-clic sur la ligne d'écriture du client).
3. À quel niveau du Customizing effectuez-vous ce paramétrage ? Procédez au paramétrage.
a) Accédez au Customizing de l'Administration des ventes (ADV) sous
Facturation → Factures → Gérer la régie de la copie pour les factures.
b) Sélectionnez l'activité Pilotage copie : document de livraison après facture et cliquez
sur le bouton
 Sélectionner.
c) Passez en mode de modification en sélectionnant
d) Sélectionnez la cible ZF## et la source LF, puis cliquez sur
 Détail. Les zones
Numéro d'affectation et Numéro de référence sont au niveau de l'en-tête.
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 241

À l'avenir, vous voulez transférer d'autres informations lors du traitement des commandes
passées à l'occasion de foires.
1. Configurez le système de façon à ce qu'il transfère, en vue du rapprochement, des
numéros de commandes clients lors de la facturation de vos commandes de foire se
référant à des livraisons.
a) Dans la zone Numéro de référence au niveau du pilotage de la copie, saisissez B
(numéro de la commande client).
2. Utilisez l'option permettant de trier des postes individuels par numéro de document de
facturation repris de l'Administration des ventes.
a) Dans la zone Numéro d'affectation au niveau du pilotage de la copie, saisissez E
(numéro actuel de la facture).
b)
 Sauvegardez vos modifications.
3. Testez les résultats et réalisez tout le processus de vente pour votre commande Foire ##.
Créez une commande client à l'aide des données suivantes :
Zone
Valeur de données
Type de commande
ZA## (commande Foire ##)
Organis. commerciale
1010
Canal distribution
Secteur d'activité
Donneur d'ordre
C615-A##
Réf. Client
##S4615-Réf
Article
P615-1##
Quantité d'ordre
1 pce
Créez la livraison pour votre commande Foire ## avec le point d'expédition 1010.
Exécutez le prélèvement et l'enregistrement de la sortie de marchandises.
Créez le document de facturation.
Passez à la pièce comptable pour rechercher les informations correspondantes.
Attention :
Le blocage de comptabilisation pour la commande prise lors d'une foire est
toujours actif.
a) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.
b) Saisissez les données comme indiqué dans la tâche.
c) Dans le Menu SAP, sélectionnez Expédition et transport → Livraison
sortante → Créer → Document individuel → Avec référence à la commande client.
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 242

d) Saisissez le point d'expédition 1010 et remplacez la date de sélection par <date du
jour + 10 jours>. Confirmez votre saisie.
e) Accédez à l'onglet Prélèvement et dans la zone Quantité prélevée, saisissez 1.
f) Cliquez ensuite sur le bouton Enreg. sortie march.
g) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Créer.
h) Confirmez le numéro du document de livraison et sauvegardez le document de
facturation.
i) Pour transférer de manière groupée des documents de facturation bloqués, dans le
Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Factures bloquées.
j) Saisissez l'organisation commerciale 1010 et <votre ID utilisateur> dans la zone Saisi
par. Dans la zone d'écran Incomplet: Raison, cochez la case Blocage de la comptabilité.
Exécutez le programme.
k) Le document de facturation créé ci-dessus doit figurer dans la liste. Sélectionnez le
document de facturation, puis cliquez sur
 Validation comptabilité financière.
l) Dans le Menu SAP, sélectionnez Logistique → Administration des ventes
(ADV) → Facturation → Facture → Afficher.
m) Confirmez le numéro du document de facturation puis cliquez sur le bouton
Gestion comptable.
n) Sélectionnez la pièce comptable, puis cliquez sur
 Afficher la pièce. La zone
Référence doit maintenant comporter le numéro de commande client et la zone
Affectation le numéro du document de facturation.
Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 243

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Ajuster l'interface entre l'Administration des ventes et la Comptabilité financière
Sujet: Ajustement de l'interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 244

Chapitre 10: Interface entre l'Administration des ventes et la Comptabilité financière


## PDF page 245

Chapitre 10
Évaluation des connaissances
1.
Vous devez toujours configurer le numéro d'affectation et de référence dans le
Customizing.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
2. Lors de la configuration du numéro d'affectation et de référence dans le Customizing,
quels sont les critères à prendre en compte ?
Sélectionnez les réponses correctes.
A S'il s'agit d'une zone d'en-tête et donc d'un critère de fractionnement.
B S'il s'agit d'une zone de poste, impliquant que vous devez configurer la routine de
données VBRK/VBRP.
C S'il s'agit d'une zone devant être configurée dans le type de document de
facturation.
D S'il s'agit d'une zone devant être configurée dans le pilotage de la copie.


## PDF page 246

Chapitre 10
Évaluation des connaissances - Réponses
1.
Vous devez toujours configurer le numéro d'affectation et de référence dans le
Customizing.
Indiquez si cette proposition est vraie ou fausse.
Vrai
Faux
2. Lors de la configuration du numéro d'affectation et de référence dans le Customizing,
quels sont les critères à prendre en compte ?
Sélectionnez les réponses correctes.
A S'il s'agit d'une zone d'en-tête et donc d'un critère de fractionnement.
B S'il s'agit d'une zone de poste, impliquant que vous devez configurer la routine de
données VBRK/VBRP.
C S'il s'agit d'une zone devant être configurée dans le type de document de
facturation.
D S'il s'agit d'une zone devant être configurée dans le pilotage de la copie.


## PDF page 247

CHAPITRE 11
Annexe
Sujet 1
Informations supplémentaires sur la gestion des messages, les informations techniques et les
principes comptables de base
OBJECTIFS DU CHAPITRE
●
Décrire la gestion des messages, les détails spécifiques au système et les principes
comptables de base


## PDF page 248

Chapitre 11: Annexe


## PDF page 249

Chapitre 11
Sujet 1
Informations supplémentaires sur la gestion
des messages, les informations techniques et
les principes comptables de base
OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●
Décrire la gestion des messages, les détails spécifiques au système et les principes
comptables de base
Gestion des messages pour les documents de facturation
Figure 63: Nouvelle détermination des messages pour les documents de facturation
Dans SAP S/4HANA, la nouvelle fonctionnalité de gestion des messages est utilisée par
défaut pour les documents de facturation. Il reste néanmoins possible de réactiver l'approche
NAST en définissant un paramètre de Customizing spécifique (pour plus d'informations, voir
la note SAP 2267376).
La nouvelle fonction SAP S/4HANA, gestion des messages est l'infrastructure stratégique de
gestion des messages dans SAP S/4HANA, à laquelle seront ajoutés des prochains
développements. Adobe XFA est la technologie utilisée par défaut pour les modèles de
formulaires fournis dans cette infrastructure, mais les formulaires hérités (SAPscript,
SmartForms, formulaires Adobe) sont toujours pris en charge. Les principaux avantages de la
nouvelle approche sont les suivants :
●
Extensibilité : importante utilisation des vues CDS
●
BRFplus : flexibilité et puissance de la détermination des paramètres de sortie
●
Solution unifiée pour toutes les applications : SD, MM, FIN, etc.
●
SAP Fiori : intégration complète avec les applications SAP Fiori
●
Prise en charge d'options e-mail avancées : configuration flexible, plusieurs destinataires
et différents modèles d'e-mail


## PDF page 250

À la différence de la gestion des messages basée sur NAST, la nouvelle gestion des messages
prend uniquement en charge les canaux impression, e-mail, XML et IDoc (sur site). Les autres
canaux ne sont pas disponibles par défaut.
Figure 64: Table de décisions BRFplus
Dans BRFplus, les tables de décisions permettent de déterminer les différents paramètres de
sortie (catégorie de message, récepteur, modèle de formulaire, etc.).
Lorsqu'une expression de la table de décisions BRFplus est appelée, les lignes sont traitées
l'une après l'autre. Dans chaque ligne, les cellules de la colonne des conditions sont traitées
de gauche à droite. Les valeurs de zone définies dans les colonnes de résultat sont retournées
si la condition est remplie dans chacune des cellules de la colonne d'entrée d'une ligne. Il est
possible de saisir des expressions ou des valeurs directes dans ces cellules. Il est également
possible d'analyser les valeurs de chaque cellule à l'aide d'opérateurs de comparaison, de
plages de valeurs et de modèles.
Figure 65: Tables de décisions pour la détermination des messages
En utilisant les tables des décisions, vous pouvez déterminer la catégorie de message, le
destinataire, le canal, les réglages d'impression et le modèle de formulaire pour les
documents de facturation. Il est possible de réorganiser les lignes de la table afin que les
Chapitre 11: Annexe


## PDF page 251

conditions les plus spécifiques soient vérifiées en premier. Il est également possible
d'importer et d'exporter les tables vers Microsoft Excel.
Interface de facturation générale
Figure 66: Interface de facturation générale
Outre l'application Création de documents de facturation et son approche omnicanal, vous
pouvez toujours utiliser l'exit utilisateur pour l'Interface de facturation générale.
L'interface de facturation générale vous permet de créer des factures dans le système SAP à
partir de documents externes (par exemple, à partir de commandes clients et de livraisons
créées dans un système autre que SAP).
Pour ce faire, vous devez procéder comme suit :
●
Préparer des données dans un fichier séquentiel d'un format approprié
●
indiquer un nombre minimum de zones obligatoires à renseigner à partir des
enregistrements de données ;
●
indiquer les zones restantes obligatoires pour la facturation (via les enregistrements de
données pour le fichier séquentiel ou via le système (zones facultatives)).
Exemples :
●
Zones obligatoires
Fiche client et organisation commerciale
●
Zones facultatives
Fiche article et éléments de prix
Vous pouvez saisir des numéros de référence externes (numéros de livraison ou de
commande client externes, par exemple).
Chemins de menus fréquemment utilisés dans ce cours
Code de transaction
Tâche
Chemin de menus
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 252

Code de transaction
Tâche
Chemin de menus
Données de base
Transaction : BP ou VD03
Affichage du donneur d'ordre
Logistique → Administration
des ventes (ADV) → Données
de base → Partenaire → Cli-
ent → Afficher → Totalité
Transaction : MM02
Affichage de l'article
Logistique → Administration
des ventes (ADV) → Données
de base → Produits → Arti-
cle → Articles divers → Affi-
cher
Transaction : VK33
Affichage d'enregistrements
de conditions (prix, majora-
tions et remises)
Logistique → Administration
des ventes (ADV) → Données
de base → Conditions → Affi-
cher → Prix, Majorations/
déductions, Frais de trans-
port, Taxes
ou
Transaction : VK13
Logistique → Administration
des ventes (ADV) → Données
de base → Conditions → Sé-
lection via type de condition
Traitement des commandes
Transaction : VA01/02/03
Création/modification/affi-
chage d'une commande
Logistique → Administration
des ventes (ADV) → Ven-
te → Commande cli-
ent → Créer/Modifier/Affi-
cher
Contrats-cadres
Transaction : VA41/42/43
Création/modification/affi-
chage d'un contrat
Logistique → Administration
des ventes (ADV) → Ven-
te → Contrat → Créer/Modi-
fier/Afficher
Traitement de l'expédition
Transaction :
VL01n/02n/03n
Création/modification/affi-
chage d'une livraison
Logistique → Administration
des ventes (ADV) → Expédi-
tion et transport → Livraison
sortante → Créer/Modifier/
Afficher → Document indivi-
duel
Transaction : VL02N ou VL23
Enregistrement de la sortie
de marchandises
Logistique → Administration
des ventes (ADV) → Expédi-
tion et transport → Enregis-
trer sortie de marchandi-
ses → Livraison sortante - do-
cument individuel
Chapitre 11: Annexe


## PDF page 253

Code de transaction
Tâche
Chemin de menus
Gestion de la facturation
Transaction : VF01/02/03
Création/modification/affi-
chage d'un document de fac-
turation
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Créer/
Modifier/Afficher
Transaction : VF11
Annulation d'un document de
facturation
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Annuler
Transaction : VF04
Traitement des échéanciers
de factures
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Traiter
échéancier de factures
Transaction : VF06
Facturation en arrière-plan
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Traitement
en arrière-plan
Transaction : VF05
Affichage de la liste des docu-
ments de facturation créés
Logistique → Administration
des ventes (ADV) → Factura-
tion → Système d'informa-
tion → Factures → Liste des
factures
Transaction : VFX3
Affichage de la liste des docu-
ments de facturation bloqués
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Factures
bloquées
Transaction : VF03
Affichage des pièces compta-
bles
Logistique → Administration
des ventes (ADV) → Factura-
tion → Facture → Affi-
cher → Bouton : Gestion
comptable
Transaction : VF25
Création/modification/affi-
chage d'un relevé de factures
Logistique → Administration
des ventes (ADV) → Factura-
tion → Liste de factu-
res → Créer/Modifier/Affi-
cher
Transaction : VF24
Traitement de la réserve de
travail pour les factures
Logistique → Administration
des ventes (ADV) → Factura-
tion → Liste de factu-
res → Échéancier de listes de
factures
Comptabilité financière
Transaction : FBL5
Affichage de postes clients
Logistique → Administration
des ventes (ADV) → Factura-
tion → Environne-
ment → Comptabilité clients
ou
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 254

Code de transaction
Tâche
Chemin de menus
Transaction : FBL5
Gestion comptable → Comp-
tabilité financière → Cli-
ents → Compte → Afficher/
modifier postes
Transaction : F-29
Encaissement pour demande
d'acompte
Gestion comptable → Comp-
tabilité financière → Cli-
ents → Écriture → Acomp-
te → Acompte
Customizing
Tâche
Chemin de menus
Entités organisationnelles
Définition des entités organi-
sationnelles dans SD et FI
Structure de l'entrepri-
se → Définition → Comptabi-
lité financière ou Administra-
tion des ventes (ADV)
Affectation des entités orga-
nisationnelles dans SD et FI
Structure de l'entrepri-
se → Affectation → Compta-
bilité financière ou Adminis-
tration des ventes (ADV)
Ventes
Définition des types de docu-
ments de vente
Administration des ventes
(ADV) → Vente → Docu-
ments de vente → En-tête du
document de vente → Définir
les types de document de
vente
Définition des types de poste
Administration des ventes
(ADV) → Vente → Docu-
ments de vente → Poste de
document de vente → Définir
les types de poste
Pilotage de la copie des docu-
ments de vente
Administration des ventes
(ADV) → Vente → Gérer pilo-
tage copie pour documents
de vente
Facturation
Définition des types de docu-
ment de vente
Administration des ventes
(ADV) → Facturation → Fac-
tures → Définir les types de
facture
Définition de tranches de nu-
méros des documents de
vente
Administration des ventes
(ADV) → Facturation → Fac-
tures → Définir les tranches
de numéros pour les factures
Chapitre 11: Annexe


## PDF page 255

Customizing
Tâche
Chemin de menus
Pilotage de la copie des docu-
ments de vente
Administration des ventes
(ADV) → Facturation → Fac-
tures → Gérer la régie de la
copie pour les factures
Configuration de calendriers
de facturation
Administration des ventes
(ADV) → Facturation → Ca-
lendrier de facturation.....
Fonctions de base SD
Configuration de la détermi-
nation du prix
Administration des ventes
(ADV) → Fonctions de ba-
se → Détermination du
prix → Pilotage de la détermi-
nation du prix
Configuration de la détermi-
nation du compte
Administration des ventes
(ADV) → Fonctions de ba-
se → Imputation/calcul du
coût de revient → Détermina-
tion du compte de produits ...
Comptabilité financière
Définition de conditions de
paiement
Comptabilité financiè-
re → Comptabilité Clients et
Fournisseurs → Transactions
commerciales → Sortie de
facture / décaissement de
l'avoir → Gérer les conditions
de paiement
Informations techniques supplémentaires
Applications SAP Fiori et rôles
La bibliothèque de référence des applications SAP Fiori est une bibliothèque complète
répertoriant tout le contenu SAP pertinent pour la barre de lancement SAP Fiori.
SAP Fiori constitue l'expérience utilisateur sur SAP S/4HANA. Vous pouvez accéder à toutes
les applications via la barre de lancement SAP Fiori. Adoptant le thème visuel de SAP Fiori,
elles présentent toutes un aspect homogène, aussi bien les applications SAP Fiori que les
applications classiques SAP GUI classique et Web Dynpro. Pour la plupart des rôles
utilisateurs dans SAP S/4HANA, il convient d'utiliser en combinaison des applications SAP
Fiori repensées et des applications classiques pour pouvoir effectuer toute la gamme des
tâches utilisateurs. Désormais, SAP S/4HANA met le contenu de la barre de lancement SAP
Fiori à la disposition d'une centaine de rôles utilisateurs.
Ces rôles combinent judicieusement les applications SAP Fiori et les applications classiques,
harmonisées au niveau visuel grâce à la barre de lancement SAP Fiori. Nous avons défini plus
de 7 000 descripteurs d'applications, qui permettent aux administrateurs d'intégrer les
applications classiques présentant le thème SAP Fiori à des catalogues fonctionnels et à des
rôles utilisateurs de la barre de lancement SAP Fiori.
For more information on how to build your own SAP Fiori apps and how to set up a role for
the SAP Fiori launchpad, refer the students to courses like UX100 and UX200.
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 256

SAP_BR_BILLING_CLERK
Gestionnaire du traitement des factures
Le rôle SAP standard pour la partie Facturation s'intitule « Gestionnaire du traitement des
factures ». Les rôles Commercial interne et Directeur commercial sont aussi susceptibles de
vous intéresser.
Dans le cadre de ce cours, nous utilisons un rôle spécifiquement prévu pour la formation.
Structure de table : document de facturation
Figure 67: Structure de table : document de facturation
Structure de table du document de facturation :
VBRK : Document de facturation : données d'en-tête
VBRP : Document de facturation : données de postes
VBPA : Document commercial : partenaires
SADR : adresse
VBFA : flux de documents commerciaux
PRCD_COND : Condition de prix - poste - condition (KONV)
STXH : textes : en-tête
STXL : textes : ligne
Chapitre 11: Annexe


## PDF page 257

Structure de table : relevé de factures
Figure 68: Structure de table : relevé de factures
Principes comptables de base
Contenu :
●
Comptabilité à partie double
●
Comptes de bilan
●
Comptes de résultat
●
Administration des ventes - Exemple
●
Gestion des articles - Exemple
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 258

Figure 69: Comptabilité à partie double
Le principe de base de la comptabilité à partie double est le suivant : toute opération
commerciale est enregistrée sur au moins deux comptes différents, c'est-à-dire qu'elle est
enregistrée au moins deux fois. Dans les cas les plus simples, seuls deux comptes sont
affectés.
Dans ce contexte, vous devez connaître le concept de crédit et débit.
En d'autres termes, vous devez enregistrer une transaction côté débit dans un compte, mais
côté crédit dans un autre.
Principe de base :
Le total des écritures au débit est toujours identique au total des écritures au crédit, et ce,
indépendamment du nombre de comptes concernés.
Chapitre 11: Annexe


## PDF page 259

Figure 70: Types de compte - Comptes de bilan
Les opérations commerciales sont imputées aux comptes (les factures figurent dans les deux
parties où sont enregistrés les mouvements).
Dans un système de comptabilité à partie double, il est possible de subdiviser les comptes en
différents types de comptes de base, eux-mêmes divisés en deux comptes partiels :
●
les comptes de bilan (compte d'immobilisation et compte de capital et débiteur), au niveau
desquels vous enregistrez les stocks et les modifications apportées à ces stocks ;
●
les comptes de résultat (compte de charges et comptes de produits), au niveau desquels
les transactions ayant une incidence sur le revenu net sont enregistrées.
Vous trouverez ci-dessous une équation de base applicable à la structure de tous les
comptes :
Solde initial + acquisitions - cessions = solde de clôture
Cependant, les comptes de base nommés ci-dessus peuvent changer en fonction de
l'imputation du solde initial, des acquisitions, des cessions et du solde final.
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 260

Figure 71: Types de compte - Comptes de résultats
Figure 72: Administration des ventes - Exemple
Chapitre 11: Annexe


## PDF page 261

Figure 73: Administration des ventes - Exemple : enregistrements
Dans l'exemple relatif à une opération commerciale de l'Administration des ventes, une pièce
comptable est créée lors de la sortie de marchandises et/ou de la création de la facture.
Lors de la sortie de marchandises, les marchandises quittent physiquement le magasin. Ce
mouvement se traduit par un enregistrement concernant le stock et la valeur. Le stock
diminue et la quantité d'articles utilisés augmente. L'écriture est donc appelée “Utilisation
d'articles en stock”.
Lors de la facturation, les créances sont cumulées par le client et les additions sont
enregistrées sous les produits (jeu d'écriture : créances imputées aux produits).
Si l'encaissement est effectué dans la Comptabilité financière, les créances seront encore
réduites et l'entrée du montant monétaire sera imputée à un compte bancaire (jeu d'écriture :
banque et créances).
Nous avons volontairement ignoré la comptabilisation de la TVA collectée afin de simplifier
l'exemple.
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base


## PDF page 262

Figure 74: Gestion des articles - Exemple
Figure 75: Exemple MM : enregistrements
Dans cet exemple, un ajout au stock s'effectue au moment de l'entrée de marchandises.
L'écriture de rapprochement s'effectue dans un compte d'attente EM/EF spécial (stock
imputé au compte d'attente EM/EF).
Si la valorisation se base sur des prix standard, il peut s'avérer nécessaire d'enregistrer le
montant de l'écart entre les coûts d'achat et de valorisation sur un compte d'écart de prix.
Lors de la création de la facture, le compte EM/EF est crédité et les engagements sont
cumulés par le fournisseur concerné (compte d'attente EM/EF imputé aux fournisseurs).
Le rapprochement des dettes a lieu durant le cycle de paiement et une cession est alors
enregistrée dans le compte bancaire (dettes imputées à banque).
Nous avons volontairement ignoré la comptabilisation de la TVA afin de simplifier l'exemple.
Chapitre 11: Annexe


## PDF page 263

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●
Décrire la gestion des messages, les détails spécifiques au système et les principes
comptables de base
Sujet: Informations supplémentaires sur la gestion des messages, les informations techniques et les principes comptables de
base
