# S4650 - Sujets interfonctionnels dans SAP S/4HANA Sales

Source: support SAP S4650, version 12, 3 jours, article 50151586.

> Version nettoyée pour usage technique/Codex. Les pages de copyright, conventions typographiques, pieds de page et répétitions éditoriales ont été retirés. Le contenu pédagogique, les procédures, valeurs SAP, exercices et solutions sont conservés.


---

## PDF page 1

S4650
Sujets interfonctionnels dans SAP
S/4HANA Sales

SUPPORT DE COURS DE L'ANIMATEUR
COURS AVEC INSTRUCTEUR
Version du cours : 12
Durée du cours : 3 Jours
Numéro d'article : 50151586

---

## PDF page 5

Sommaire :

vii        Vue d'ensemble du cours

1          Chapitre 1: Impact des structures organisationnelles

2                         Sujet: Création d'éléments organisationnels                       40 Minutes
9                             Exercice 1: Développement d'une structure organisationnelle   20 Minutes
14                        Sujet: Gestion des données de base vente partagées et liées à     40 Minutes
        plusieurs secteurs d'activité
19                              Exercice 2: Définition des données de base partagées        20 Minutes

25         Chapitre 2: Pilotage de la copie

26                        Sujet: Modification du pilotage de la copie                       180 Minutes
45                            Exercice 3: Configuration du pilotage de la copie pour un      30 Minutes
            document de vente
61                            Exercice 4: Configuration du pilotage de la copie pour un     30 Minutes
            document de livraison
67                            Exercice 5: Configuration du pilotage de la copie pour un     30 Minutes
            document de facturation

75         Chapitre 3: Pilotage de textes

76                        Sujet: Identification des sources de textes                       35 Minutes
81                            Exercice 6: Identification des sources de textes              15 Minutes
85                        Sujet: Configuration du pilotage de textes                        90 Minutes
101                           Exercice 7: Configuration d'un pilotage de textes dans le     15 Minutes
            Customizing
109                           Exercice 8: Traitement manuel d'un texte                       10 Minutes

117        Chapitre 4: Messages

118                       Sujet: Ajustement de la détermination des messages                 90 Minutes
129                           Exercice 9: Ajustement de la détermination des messages        20 Minutes
140                       Sujet: Ajustement des catégories de messages                      120 Minutes
151                           Exercice 10: Ajustement et traitement d'une catégorie de       15 Minutes
            message
159                       Sujet: Nouvelle fonctionnalité de gestion des messages            60 Minutes
169                           Exercice 11: Création d'une catégorie de message pour la      40 Minutes
            confirmation de commande

---

## PDF page 6

183    Chapitre 5: Extensions et modifications

185               Sujet: Utilisation des technologies d'extension                            30 Minutes
191               Sujet: Ajout de nouvelles zones                                            45 Minutes
197               Sujet: Ajustement des listes dans l'Administration des ventes              60 Minutes
205                   Exercice 12: Utilisation de fonctions de liste standard               20 Minutes
211               Sujet: Configuration de la sélection de zones pour les fiches article     40 Minutes
218               Sujet: Définition de références de zone pour les fiches article           40 Minutes
227                   Exercice 13: Ajustement des options de sélection de zones             30 Minutes
235               Sujet: Modification du système à l'aide des technologies d'extension     180 Minutes
classiques
249               Sujet: Modification du système à l'aide de la structure d'extension        45 Minutes

vi                                                                     © Copyright. Tous droits réservés.

---

## PDF page 7

Vue d'ensemble du cours

PUBLIC CONCERNÉ
Ce cours s'adresse aux participants suivants :
●   Architecte processus métier
●   Responsable de processus de gestion/Responsable d'équipe/Utilisateur de référence

---

## PDF page 8

viii   © Copyright. Tous droits réservés.

---

## PDF page 9

CHAPITRE 1                             Impact des structures
                     organisationnelles

Sujet 1
Création d'éléments organisationnels                                                                         2
Exercice 1: Développement d'une structure organisationnelle                                     9

Sujet 2
Gestion des données de base vente partagées et liées à plusieurs secteurs d'activité                         14
Exercice 2: Définition des données de base partagées                                             19

OBJECTIFS DU CHAPITRE

●   Créer des éléments organisationnels
●   Utiliser les données de base vente partagées et liées à plusieurs secteurs d'activité

---

## PDF page 10

Chapitre 1
    Sujet 1
Création d'éléments organisationnels

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Créer des éléments organisationnels

Création d'éléments organisationnels
Objectif de l'organisation commerciale
Les entités organisationnelles sont des éléments dans la structure organisationnelle du
système SAP S/4HANA. Elles permettent de représenter la structure de votre service des
ventes pour l'utiliser comme cadre du traitement de l'administration des ventes avec le
module Administration des ventes (SD). La structure organisationnelle a une influence sur les
données de base, les processus (chaînes de documents) et le reporting. Les fiches de
l'administration des ventes (par exemple, les fiches clients et les fiches de conditions) ainsi
que les documents de traitement d'opération (par exemple, les ordres et les livraisons) sont
saisis en fonction des entités organisationnelles.
Les informations par défaut enregistrées dans les fiches sont spécifiques à des entités
organisationnelles spécifiques. Chaque document commercial est créé pour un domaine
commercial spécifique de l'organisation. Les données de base qui y sont valides sont
automatiquement transférées vers les documents commerciaux. De plus, vous pouvez définir
différents critères de pilotage pour la gestion des données de base et pour le traitement
d'opération en fonction des entités organisationnelles.

Voici des exemples d'entités organisationnelles qui sont obligatoires dans SD :
●  Organisation commerciale
●   Canal de distribution
●   Secteur d'activité
●   Domaine commercial

Organisation commerciale

Les principales caractéristiques d'une organisation commerciale sont les suivantes :

●   Une organisation commerciale est responsable de la distribution des marchandises et de
la prestation des services.
●   Une organisation commerciale est responsable de la négociation des conditions de vente.
●   L'organisation commerciale est l'élément organisationnel de la logistique représentant la
structure de l'entreprise en fonction de ses impératifs en matière d'administration des
ventes.

---

## PDF page 11

Sujet: Création d'éléments organisationnels

●   Une organisation commerciale est une unité opérationnelle qui est légalement responsable
des produits et détient les droits de recours.
●   L'organisation commerciale possède une adresse.
●   L'organisation commerciale correspond au plus haut niveau de cumul, après le mandant,
utilisé pour les statistiques de l'Administration des ventes et elle dispose de sa propre
devise statistique.
●   Une organisation commerciale est affectée à une seule société.

Vous devez réaliser chaque opération commerciale (commande client ou livraison) pour une
organisation commerciale spécifique.
Vous devez créer au moins une organisation commerciale dans votre système SAP. Vous
pouvez définir vos propres données de base dans une organisation commerciale. Elle peut
avoir ses propres données de base client ou article ainsi que des conditions et une
détermination du prix spécifiques.
Vous pouvez utiliser l'organisation commerciale comme critère de sélection pour l'affichage
d'une liste des documents de vente et pour la création d'échéanciers de livraison et de
facturation. Vous pouvez définir, pour chaque organisation commerciale, différentes
méthodes d'impression des messages liés aux documents de vente et de facturation.

Canal de distribution

 Figure 1: Canal de distribution

Le canal de distribution représente la façon dont vos produits ou services parviennent aux
clients. La figure suivante donne des exemples de canaux de distribution.

Vous pouvez exécuter les activités suivantes pour un canal de distribution :
● Affecter un canal de distribution à une ou à plusieurs organisations commerciales.
●   Affecter une ou plusieurs divisions à l'organisation commerciale et au canal de distribution.
●   Définir vos propres fiches article, client et conditions pour un canal de distribution.

---

## PDF page 12

Chapitre 1: Impact des structures organisationnelles

●   Créer des données de base pour un canal de distribution commun, qui sera ensuite utilisé
dans d'autres canaux de distribution. Pour créer des données de base, vous devez affecter
le canal de distribution commun aux autres canaux de distribution également.
●   Utiliser le canal de distribution comme critère de sélection pour la création de listes.

Les postes d'un document de livraison peuvent correspondre à différents canaux de
distribution. Tous les postes d'un document de facturation font partie d'un même canal de
distribution.

Secteur d'activité

Figure 2: Secteur d'activité

Utilisez un secteur d'activité comme entité organisationnelle pour regrouper les articles ou
services. Affectez un secteur d'activité à une ou à plusieurs organisations commerciales. Un
article fait toujours partie d'un secteur d'activité particulier. Vous saisissez le secteur
d'activité dans la page à onglet ADV : org. commerc. 1 de la fiche article.

Les activités suivantes peuvent être exécutées dans un secteur d'activité :
●  Définir des données de base spécifiques au secteur d'activité pour les clients et les
conditions.
●   Mettre en place un secteur d'activité commun afin de créer des fiches client et des
conditions qui sont valables pour plusieurs secteurs d'activité.
●   Définir, par type de document de vente, que tous les postes de ce document font partie du
même secteur d'activité. Les postes d'un document de livraison ou de facturation peuvent
relever de différents secteurs d'activité.
●   Définir différents modes d'impression des messages associés aux documents de vente
pour chaque secteur d'activité.
●   Utiliser le secteur d'activité comme critère de sélection pour l'affichage d'une liste des
documents de vente et la création d'un échéancier de livraison.

---

## PDF page 13

Sujet: Création d'éléments organisationnels

Imputation du secteur d'activité et du domaine d'activité

 Figure 3: Imputation du secteur d'activité et du domaine d'activité

Le domaine d'activité est une entité organisationnelle de la comptabilité financière interne qui
correspond à une aire d'activité ou à un domaine de responsabilité limité dans l'entreprise.
Les mouvements de valeurs saisis dans la Comptabilité financière (FI) peuvent être ajoutés au
domaine d'activité.

         Attention :
         Dans un projet d'implémentation, il est possible que le client n'utilise pas de
         structure organisationnelle basée sur le concept de secteur d'activité lié à
         l'article SAP S/4HANA. Dans ce cas, il est possible d'utiliser le domaine d'activité
         comme alternative. Toutefois, il ne faut pas oublier que le domaine d'activité est
         principalement une entité financière et il faut veiller à ce que son utilisation par le
         document de vente ne rentre pas en conflit avec son utilisation dans le reporting
         financier.

Toutefois, dans la fiche article SAP, le secteur d'activité ne peut être renseigné qu'une seule
fois. Utilisez le secteur d'activité dans le document de vente pour déterminer le domaine
d'activité à l'aide de l'une des trois règles prédéfinies (voir figure).

---

## PDF page 14

Chapitre 1: Impact des structures organisationnelles

Domaine commercial

Figure 4: Domaine commercial

Un domaine commercial est la combinaison d'une organisation commerciale, d'un canal de
distribution et d'un secteur d'activité.
Utilisez le domaine commercial pour les évaluations et l'affectation du schéma de calcul.
Pour créer des domaines commerciaux, affectez le secteur d'activité et le canal de
distribution aux organisations commerciales. Lors de cette opération, le système propose
automatiquement les secteurs d'activité et les canaux de distribution précédemment affectés
à une organisation commerciale.
Vous pouvez gérer dans la fiche client les données spécifiques à un domaine commercial et
vous pouvez créer des documents de vente pour un domaine commercial donné.

Éléments organisationnels facultatifs dans SD

Figure 5: Éléments organisationnels facultatifs dans SD

---

## PDF page 15

Sujet: Création d'éléments organisationnels

Les éléments organisationnels suivants sont facultatifs dans SD :
Agence commerciale :
●   Une agence commerciale est une entité organisationnelle responsable de l'ADV dans
   une zone géographique donnée.
●   Une agence commerciale assure la liaison entre l'entreprise et le marché régional.
●   Une agence commerciale peut être affectée à un ou plusieurs domaines
   commerciaux.
●   Vous pouvez subdiviser les agences commerciales en plusieurs groupes de vendeurs.

Groupe de vendeurs :
●   Il s'agit de l'entité organisationnelle réalisant les ventes et chargée du processus de
   vente en interne.
●   Un groupe de vendeurs peut être affecté à une ou plusieurs agences commerciales.
●   Un groupe de vendeurs est constitué d'un certain nombre de vendeurs.

Vendeurs :
●   Un vendeur est affecté à une agence commerciale ainsi qu'à un groupe dans la fiche
   du commercial.

L'analyse des ventes peut être exécutée pour différents niveaux de la structure
organisationnelle à l'aide des outils de fonctions analytiques intégrées SAP S/4HANA, de SAP
Business Information Warehouse (BW) et de SAP Business Intelligence (BI).

Comment créer des éléments organisationnels

1. Define a new distribution channel, for example, Y1 (Telephone sales).
a) Go to Customizing for Enterprise Structure under Definition → Sales and
  Distribution → Define, copy, delete, check distribution channel.

b) In the Choose Activity dialog box, choose Define distribution channel and choose the
  Choose button.

c) Choose the New Entries button.

d) Enter the following distribution channel data:
    Field                                        Value
    Distribution Channel                         Y1

    Name                                         Telephone sales

e) Save your data.

f) Return to the Customizing screen.

2. Assign the new distribution channel to sales organization 1010.
a) Go to Customizing for Enterprise Structure under Assignment → Sales and
  Distribution → Assign distribution channel to sales organization.

---

## PDF page 16

Chapitre 1: Impact des structures organisationnelles

b) Choose the New Entries button.

c) Enter the following data:
 Field                                       Value
 Sales Organization                          1010

 Distribution Channel                        Y1

d) Save your data.

e) Return to the Customizing screen.

3. Create two sales areas with the new distribution channel and division 00 (cross-division)
and 03 (motorcycles/bike). Both these divisions must belong to the distribution channel
Y1 within the sales organization 1010.
Enter the following sales area details:
Field                                         Value
Sales Organization                            1010

Distribution Channel                          Y1

Division                                      00 and 03

a) Go to Customizing for Enterprise Structure under Assignment → Sales and
Distribution → Set up sales area.

b) Choose the New Entries button.

c) Enter the two sales areas (1010, Y1, 00) and (1010, Y1, 03).

d) Save your data.

e) Return to the Customizing screen.

4. Maintain the business area account assignment for the new sales area.
a) Go to Customizing for Enterprise Structure under Assignment → Sales and
Distribution → Business Area Account Assignment → Define Rules By Sales Area.

b) Choose the Position button.

c) In the Another entry dialog box, enter 1010 in the Sales Org. field and your new
distribution channel in the corresponding field.

d) Choose Continue.

e) Enter rule 1 in both the sales areas.

f) Save your data.

---

## PDF page 17

Chapitre 1
  Exercice 1
Développement d'une structure
organisationnelle

Exemple de gestion
En vue d'améliorer l'analyse des statistiques de l'Administration des ventes, les cadres
dirigeants de votre entreprise ont décidé d'ajouter un canal de distribution à l'organisation
commerciale 1010. Vous devez configurer ce canal de distribution dans le système SAP.
Développez une structure organisationnelle.

1. Définissez un nouveau canal de distribution pour votre groupe d'activité. Saisissez la
description Canal groupe ##.
Utilisez la table suivante pour déterminer la clé pour votre canal de distribution.

Numéro de groupe        Canal de distribution Numéro de groupe            Canal de distribution
01                      D1                     11                         E1

02                      D2                     12                         E2

03                      D3                     13                         E3

04                      D4                     14                         E4

05                      D5                     15                         E5

06                      D6                     16                         E6

07                      D7                     17                         E7

08                      D8                     18                         E8

09                      D9                     19                         E9

10                      D0                     20                         E0

2. Affectez votre nouveau canal de distribution à l'organisation commerciale 1010.

3. Configurez deux nouveaux domaines commerciaux à l'aide des détails suivants :
Zone                                           Valeur
Organis. commerciale                           1010

Canal de distribution                          Voir tableau à l'étape 1
Secteur d'activité                             00 et 03

4. Gérez l'imputation du domaine d'activité pour vos domaines commerciaux. Choisissez la
règle 1 Détermin. dom. d'activité à partir de div,/sect.act..

---

## PDF page 18

Chapitre 1
Solution 1
Développement d'une structure
organisationnelle

Exemple de gestion
En vue d'améliorer l'analyse des statistiques de l'Administration des ventes, les cadres
dirigeants de votre entreprise ont décidé d'ajouter un canal de distribution à l'organisation
commerciale 1010. Vous devez configurer ce canal de distribution dans le système SAP.
Développez une structure organisationnelle.

1. Définissez un nouveau canal de distribution pour votre groupe d'activité. Saisissez la
description Canal groupe ##.
Utilisez la table suivante pour déterminer la clé pour votre canal de distribution.

Numéro de groupe        Canal de distribution Numéro de groupe          Canal de distribution
01                      D1                     11                       E1

02                      D2                     12                       E2

03                      D3                     13                       E3

04                      D4                     14                       E4

05                      D5                     15                       E5

06                      D6                     16                       E6

07                      D7                     17                       E7

08                      D8                     18                       E8

09                      D9                     19                       E9

10                      D0                     20                       E0

a) Dans le Customizing de la Structure de l'entreprise, sélectionnez
Définition → Administration des ventes (ADV) → Définir, copier, supprimer, contrôler
canal de distribution.

b) Dans la boîte de dialogue Sélection de l'activité, double-cliquez sur Définir le canal de
distribution.

c) Cliquez sur le bouton Nouvelles entrées.

d) Saisissez les détails du canal de distribution suivants :
Zone                                        Valeur
Canal de distribution                       Voir tableau à l'étape 1

---

## PDF page 19

Sujet: Création d'éléments organisationnels

    Zone                                      Valeur
    Nom                                       Canal groupe ##

e) Sauvegardez vos données.

f) Revenez à l'écran Afficher guide d'implémentation.

2. Affectez votre nouveau canal de distribution à l'organisation commerciale 1010.
a) Dans le Customizing de la Structure de l'entreprise, sélectionnez
  Affectation → Administration des ventes (ADV) → Affecter canal de distribution à
  organisation commerciale.

b) Cliquez sur le bouton Nouvelles entrées.

c) Vérifiez les éléments suivants :
    Zone                                      Valeur
    Organis. commerciale                      1010

    Canal de distribution                     Voir tableau à l'étape 1

d) Sauvegardez vos données.

e) Revenez à l'écran Afficher guide d'implémentation.

3. Configurez deux nouveaux domaines commerciaux à l'aide des détails suivants :
Zone                                         Valeur
Organis. commerciale                         1010

Canal de distribution                        Voir tableau à l'étape 1
Secteur d'activité                           00 et 03

a) Dans le Customizing de la Structure de l'entreprise, sélectionnez
  Affectation → Administration des ventes (ADV) → Définir domaine commercial.

b) Cliquez sur le bouton Nouvelles entrées.

c) Entrez ces deux domaines commerciaux.

d) Sauvegardez vos données.

e) Revenez à l'écran Afficher guide d'implémentation.

4. Gérez l'imputation du domaine d'activité pour vos domaines commerciaux. Choisissez la
règle 1 Détermin. dom. d'activité à partir de div,/sect.act..
a) Dans le Customizing de la Structure de l'entreprise, sélectionnez
  Affectation → Administration des ventes (ADV) → Imputation des domaines
  d'activité → Définir les règles par domaine commercial.

b) Cliquez sur le bouton Positionner.

c) Dans la boîte de dialogue Autre entrée, entrez 1010 dans la zone Org.commerciale et
  votre nouveau canal de distribution dans la zone correspondante.

---

## PDF page 20

Chapitre 1: Impact des structures organisationnelles

d) Cliquez sur Reprendre.

e) Entrez la règle 1 dans les deux domaines commerciaux.

f) Sauvegardez vos données.

---

## PDF page 21

Sujet: Création d'éléments organisationnels

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Créer des éléments organisationnels

---

## PDF page 22

Chapitre 1
  Sujet 2
Gestion des données de base vente partagées
et liées à plusieurs secteurs d'activité

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Utiliser les données de base vente partagées et liées à plusieurs secteurs d'activité

Gestion des données de base vente partagées et liées à plusieurs secteurs
d'activité

Figure 6: Concept des données de base partagées

Avant d'effectuer le paramétrage système pour les données de base, vous devez avoir défini
les structures organisationnelles.
Les données de base partagées permettent de réduire le temps requis pour créer et gérer des
données de base. Vous pouvez spécifier, dans le Customizing, les domaines commerciaux
habilités à utiliser les données de base partagées.
Par couple organisation commerciale/canal de distribution, vous pouvez définir le canal de
distribution utilisé pour accéder aux enregistrements de condition et le canal de distribution
utilisé pour accéder aux données de base article et client.
Par couple organisation commerciale/secteur d'activité,vous pouvez définir le secteur
d'activité utilisé pour accéder aux enregistrements de condition et aux données de base
client.

---

## PDF page 23

Sujet: Gestion des données de base vente partagées et liées à plusieurs secteurs d'activité

 Figure 7: Exemple de données de base partagées

La figure montre les options pour définir les canaux de distribution et secteurs d'activité
communs dans le Customizing. Dans l'exemple ci-dessus, les options du Customizing ont été
définies de façon à ce que les données relatives au domaine commercial (1000, 10, 01) de la
fiche client et celles (1000, 10) de la fiche article puissent également être utilisées comme
données de base partagées dans les domaines commerciaux suivants :
●   1000 10 01
●   1000 10 02
●   1000 12 01
●   1000 12 02

Les enregistrements de conditions présentés dans cet exemple ne sont pas partagés, ce
qui vous permet de créer différentes structures de détermination des prix applicables à
chaque entité organisationnelle.

---

## PDF page 24

Chapitre 1: Impact des structures organisationnelles

Figure 8: Limites des données de base partagées

Il est impossible de définir des données de base partagées pour toutes les organisations
commerciales. L'utilisation incorrecte d'une organisation commerciale (mappage au niveau
du canal de distribution, par exemple) entraînerait de lourdes conséquences : vous ne
pourriez en effet pas utiliser les fonctions de données partagées à ce niveau. Dans certains
cas, cette procédure ferait augmenter le nombre de vues SD qui doivent être gérées dans les
données de base.

Figure 9: Données de base partagées et Reporting

Les données d'organisation indiquées dans le document sont transférées aux outils de
reporting SAP Business Information Warehouse (BW) et SAP Business Intelligence à partir
des documents de vente, de livraison et de facturation. Vous bénéficiez ainsi d'un reporting

---

## PDF page 25

Sujet: Gestion des données de base vente partagées et liées à plusieurs secteurs d'activité

détaillé de toutes les structures organisationnelles tout en minimisant le volume des données
de base à créer et à gérer en ayant accès directement aux données de ces documents
organisationnels.
Le secteur d'activité dans l'en-tête du document de vente est proposé à partir du domaine
commercial. Si vous voulez que le secteur d'activité au niveau du poste soit proposé à partir
de la fiche article, vous devez sélectionner la zone Sect. act. poste dans le Customizing pour le
type de document de vente. Si cette zone n'est pas cochée, le secteur d'activité défini dans
l'en-tête du document de vente s'appliquera à tous les postes.

Comment définir des canaux de distribution communs
The new distribution channel Y1 uses the data from sales area 1010, 10, 00 to minimize the
maintenance workload.

1. Assign distribution channel 10 to sales organization 1010 and distribution channel Y1 for
conditions and the customer or material master data.
a) Go to Customizing for Sales and Distribution under Master Data → Define Common
  Distribution Channels.

b) Choose the Position button.

c) Enter 1010 in the Sales Org. field.

d) Enter Y1 in the Distr. Channel field.

e) Choose Continue.

f) Enter 10 in the DCh-Conds and DCh-Cust/Mt fields.

g) Save your data.

h) Return to the main screen.

2. Enter the pricing procedure determination so that orders can be created properly for sales
area (1010, Y1, 00).
a) Go to Customizing for Sales and Distribution under Basic Functions → Pricing →
  Pricing Control → Define and Assign Pricing Procedures.

b) In the Choose Activity dialog box, choose Set Pricing Procedure Determination and
  choose the Choose button.

c) Choose the New Entries button and enter following data:
    Field                                                  Value
    SOrg.                                                  1010

    DChl                                                   Y1

    Dv                                                     00

    Document pricing procedure                             A

    |Customer pricing procedure                            S

    Pricing procedure                                      RVAA01

d) Save your entries.

---

## PDF page 26

Chapitre 1: Impact des structures organisationnelles

3. Test the changes by creating a standard sales order in the new sales area (1010, Y1, 00).
Show how, because of the shared master data, pricing condition records for distribution
channel 10 are used.
Enter the following details:
Field                                         Value
Sold-To Party                                 C650-A00

Cust. Reference                               ##-2-2

Req. deliv. date                              One week from today
Material                                      P650-100

Order quantity                                10

a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Create.

b) Enter OR in the Order Type field.

c) Enter the new sales area (1010, Y1, 00).

d) Choose Enter.

e) Enter the details from the table above.

f) Choose Enter.

g) Select the row containing the item.

h) Choose the Item Conditions pushbutton.

i) Select the row containing condition PR00 on the item condition screen.

j) Choose the Condition rec. pushbutton.
The condition record is created for distribution channel 10.

---

## PDF page 27

Chapitre 1
 Exercice 2
Définition des données de base partagées

 Figure 10: Démonstration et scénario d'exercice : configuration d'un nouveau domaine commercial

Pour mieux comprendre cette rubrique, vous allez configurer un nouveau domaine
commercial. Vous devez prendre des décisions, notamment concernant l'utilisation des
données de base partagées.

Exemple de gestion
En vue de réduire la charge de travail liée à la création et à la gestion des données, votre
nouveau domaine commercial doit reprendre les données du domaine 1010, 10, 00. Vous
devez créer les conditions préalables nécessaires dans le Customizing.
Définissez les données de base partagées.

1. Définissez le canal de distribution 10 comme canal de distribution partagé pour les
conditions et les données de base client ou article de votre canal de distribution.

2. Créez une commande client standard pour les commandes d'achat suivantes dans votre
nouveau domaine commercial (1010, D# ou E#, 00).
Vérifiez les éléments suivants :
Zone                                                   Valeur
Donneur d'ordre                                        C650-A##

Réf. client                                            ##-2-2

DateLivrSouh.                                          Dans une semaine jour pour jour

---

## PDF page 28

Chapitre 1: Impact des structures organisationnelles

Zone                                          Valeur
Article                                       P650-1##

Quantité commandée                            10

Si la boîte de dialogue Domaine commercial pour le client s'affiche, sélectionnez l'entrée
pour OrgCm 1010, Canal 10, Secteur 00. Cliquez sur le bouton Sélectionner (ou double-
cliquez sur l'entrée).
Comment réagit le système ?

3. Copiez le schéma de calcul pour le domaine commercial (1010, 10, 00) dans votre
domaine commercial (1010, D# ou E#, 00).

4. Réessayez de créer une commande client à l'aide des données de l'étape 2. Affichez
l'enregistrement de conditions pour la condition PR00 dans l'écran de condition.
Pour quel canal de distribution l'enregistrement de conditions a-t-il été créé ?

---

## PDF page 29

Chapitre 1
  Solution 2
Définition des données de base partagées

 Figure 10: Démonstration et scénario d'exercice : configuration d'un nouveau domaine commercial

Pour mieux comprendre cette rubrique, vous allez configurer un nouveau domaine
commercial. Vous devez prendre des décisions, notamment concernant l'utilisation des
données de base partagées.

Exemple de gestion
En vue de réduire la charge de travail liée à la création et à la gestion des données, votre
nouveau domaine commercial doit reprendre les données du domaine 1010, 10, 00. Vous
devez créer les conditions préalables nécessaires dans le Customizing.
Définissez les données de base partagées.

1. Définissez le canal de distribution 10 comme canal de distribution partagé pour les
conditions et les données de base client ou article de votre canal de distribution.
a) Dans le Customizing pour Administration des ventes (ADV), sélectionnez Données de
  base → Définir les canaux de distribution communs.

b) Cliquez sur le bouton de commande Positionner.

c) Saisissez 1010 dans la zone Org.commerciale.

d) Entrez le canal de distribution D# ou E#.

e) Cliquez sur Reprendre.

---

## PDF page 30

Chapitre 1: Impact des structures organisationnelles

f) Entrez 10 dans les zones C,d.Condit. et C.d.art/clt.

g) Sauvegardez vos données.

h) Revenez à l'écran principal.

2. Créez une commande client standard pour les commandes d'achat suivantes dans votre
nouveau domaine commercial (1010, D# ou E#, 00).
Vérifiez les éléments suivants :
Zone                                           Valeur
Donneur d'ordre                                C650-A##

Réf. client                                    ##-2-2

DateLivrSouh.                                  Dans une semaine jour pour jour
Article                                        P650-1##

Quantité commandée                             10

Si la boîte de dialogue Domaine commercial pour le client s'affiche, sélectionnez l'entrée
pour OrgCm 1010, Canal 10, Secteur 00. Cliquez sur le bouton Sélectionner (ou double-
cliquez sur l'entrée).
Comment réagit le système ?
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.

b) Sélectionnez CDCL dans la zone Type commande client.

c) Référez-vous au tableau de l'étape et saisissez les données pour votre domaine
commercial.

d) Appuyez sur Entrée.
Le message d'erreur Aucun schéma de calcul n'a pu être déterminé s'affiche. Cliquez
sur Retour.

e) Revenez à l'écran principal.

3. Copiez le schéma de calcul pour le domaine commercial (1010, 10, 00) dans votre
domaine commercial (1010, D# ou E#, 00).
a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez Fonctions de
base → Détermination du prix → Pilotage de la détermination du prix → Définir et
affecter les schémas de calcul.

b) Dans la boîte de dialogue Sélection de l'activité, double-cliquez sur Définir
détermination du schéma de calcul.

c) Cliquez sur le bouton de commande Positionner.

d) Saisissez 1010 dans la zone Org.commerciale.

e) Entrez le canal de distribution 10 et le secteur d'activité 00, puis sélectionnez Suite.

---

## PDF page 31

Sujet: Gestion des données de base vente partagées et liées à plusieurs secteurs d'activité

f) Sélectionnez la ligne contenant le domaine commercial 1010/10/00, le schéma de
   documents A et le schéma client S, puis cliquez sur le bouton de commande Copier
   sous.

g) Remplacez le canal de distribution par votre nouveau canal de distribution D# ou E#.

h) Sauvegardez vos données.

4. Réessayez de créer une commande client à l'aide des données de l'étape 2. Affichez
l'enregistrement de conditions pour la condition PR00 dans l'écran de condition.
Pour quel canal de distribution l'enregistrement de conditions a-t-il été créé ?
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Commande client → Créer.

b) Sélectionnez CDCL dans la zone Type commande client.

c) Entrez les données requises pour votre domaine commercial.

d) Appuyez sur Entrée.

e) Sélectionnez la ligne contenant le poste.

f) Cliquez sur le bouton de commande Conditions postes.

g) Sélectionnez la ligne contenant la condition PR00 sur l'écran de condition pour le
  poste.

h) Cliquez sur le bouton de commande Enreg. condition. L'enregistrement de conditions
  est créé pour le canal de distribution 10.

---

## PDF page 32

Chapitre 1: Impact des structures organisationnelles

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Utiliser les données de base vente partagées et liées à plusieurs secteurs d'activité

---

## PDF page 33

CHAPITRE 2                             Pilotage de la copie

Sujet 1
Modification du pilotage de la copie                                                                 26
Exercice 3: Configuration du pilotage de la copie pour un document de vente              45
Exercice 4: Configuration du pilotage de la copie pour un document de livraison          61
Exercice 5: Configuration du pilotage de la copie pour un document de facturation        67

OBJECTIFS DU CHAPITRE

●   Modifier le pilotage de la copie

---

## PDF page 34

Chapitre 2
  Sujet 1
Modification du pilotage de la copie

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment modifier le pilotage de la copie.

Exemple de gestion
Vous souhaitez créer une routine de transfert de données propre au client. Pour cette raison,
vous devez disposer des connaissances suivantes :
●   Comment modifier le pilotage de la copie dans le but de répondre aux besoins propres au
client

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Modifier le pilotage de la copie

Flux de documents

Figure 11: Flux de documents

Les processus de gestion de l'Administration des ventes sont reflétés par le flux de
documents dans le système SAP. Un processus de gestion se compose de différentes étapes
de traitement enregistrées sous forme de documents. Les données sont copiées du

---

## PDF page 35

Sujet: Modification du pilotage de la copie

document source dans le document cible lors du processus. Ce processus apparaît dans le
flux de documents.
Vous pouvez utiliser le pilotage de la copie pour représenter des conditions liées à vos
processus de gestion et activer d'autres options telles que la mise à jour du flux de
documents.
Par défaut, le flux de documents est mis à jour au niveau de l'en-tête du document. Si la case
MAJ flux documents est cochée dans le pilotage de la copie au niveau du poste, le flux de
documents est également mis à jour pour les postes individuels.
Vous pouvez passer du flux de documents à l'écran d'affichage des documents appropriés.
Vous pouvez également afficher des données supplémentaires sur le statut d'un document
figurant dans le flux.

Comment créer une commande en référence à une offre

       Remarque :
       In this demonstration, you create an order needed for one or more subsequent
       demonstrations in the course.

1. Create a quotation for customer C650-A00 with two items.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution →
  Sales → Quotation → Create.

b) On the Create Quotation: Initial Screen, in the Quotation Type field, enter QT.

c) In the Sales Organization field, enter 1010

d) In the Distribution Channel field, enter 10.

e) In the Division field, enter 00 and choose Enter.

f) On the Create Quotation: Overview screen, in the Sold-To Party field, enter C650-A00.

g) In the Cust. Reference field, enter sample_quotation_00.

h) On the Item Overview tab page, in the Valid-To field, enter the date of the last day of the
  current month.

i) Enter two materials in the table, P650-100 and P650-200, each with an order quantity
   of 10 units.

2. Enter the name and phone number in the data of the header purchase order.
a) On the Create Quotation: Overview screen, choose Goto → Header → Purchase order
  data.

b) On the Create Quotation: Header Data screen, in the Name and Telephone fields, enter
  any example name and telephone number.

c) Save your data.

d) Note the document number of the quotation in the message that appears.

e) Return to the SAP Easy Access screen.

---

## PDF page 36

Chapitre 2: Pilotage de la copie

3. Create an order with reference to this quotation.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Create.

b) On the Create Sales Order: Initial Screen, in the Order Type field, enter OR.

c) Choose Create with Reference.

d) In the Create with Reference dialog box, in the Quot. field, enter the quotation
document number created in the previous step.

4. Copy only one item to the sales order.
a) In the Create with Reference dialog box, choose Item Selection.

b) On the Quotation XXXXXXXX: Selection List for Reference Document screen, deselect
the Selection checkbox of the second item.

c) Choose Copy.

d) On the Create Standard Order: Overview screen, note how only one item is copied to
the sales order from the quotation.

e) Choose Save.
A warning message to enter a PO number is displayed.

f) In the Cust. Reference field, enter sample_quotation_00.

g) Save your data and note the standard order number that is displayed.

h) Return to the SAP Easy Access screen.

5. Display the document flow.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Display.

b) On the Display Sales Order: Initial Screen, choose Enter.

c) On the Display Standard Order XXXXX: Overview screen, choose Display document
flow.

d) On the Document Flow screen, demonstrate the quotation and standard order
documents in the document flow.

---

## PDF page 37

Sujet: Modification du pilotage de la copie

Tâches du pilotage de la copie

 Figure 12: Copying_Control_Overview_Image.ppt

Les tables de pilotage de la copie du Customizing sont des éléments importants de votre
système SAP. Elles pilotent de nombreuses fonctions exécutées lors de la création d'un
document en référence à un document précédent.
Avant que les données ne soient copiées du document source dans le document cible, le
système vérifie si certaines conditions sont remplies.

Exemples de conditions :
● Le document source et le document cible ont-ils le même donneur d'ordre ?
●   Le ou les postes à copier sont-ils déjà refusés dans le document source ?
●   Les postes à copier ont-ils déjà été totalement utilisés en tant que référence ?
●   La période de validité du document source a-t-elle été dépassée ?

Vous pouvez spécifier les données à copier (par exemple, les données d'en-tête, les données
partenaire ou les conditions) lors de l'établissement de la référence.
La fonction Créer avec référence est disponible dans l'écran de saisie initial de la création de
document avec référence ainsi que dans l'écran de synthèse de la création de document de
vente pendant la saisie du document. Cette fonction vous permet par exemple de combiner
plusieurs offres dans une seule commande client.
Il existe des tables de pilotage de la copie distinctes pour les documents de vente, les
livraisons et les documents de facturation.
Il existe des tables de pilotage de la copie pour tous les niveaux d'un document de vente.

---

## PDF page 38

Chapitre 2: Pilotage de la copie

Les niveaux de pilotage de la copie disponibles pour les documents de vente sont les
suivants :
●  En-tête
●     Poste
●     Échéance

Conditions de copie
Certaines conditions doivent être remplies avant qu'il ne soit possible de copier des données
du document source dans le document cible. Les routines ABAP contiennent ces conditions,
qui sont affectées dans les tables de pilotage de la copie utilisant leurs numéros
d'identification (ID).
Vous pouvez également utiliser la transaction VOFM pour créer des routines personnalisées.
Vous pouvez trouver la transaction VOFM dans le Customizing de l'Administration des ventes
(ADV) sous Adaptation du système → Routines → Définir instructions relatives à la copie.
Les routines de transfert de données spécifiées ne sont pas exécutées tant que les conditions
de copie ne sont pas remplies.

Figure 13: Conditions de copie

Comment définir des conditions de copie

1. Define copying requirements for the following documents: Sales orders, Deliveries, Billing
documents, and Sales activities.
a) In Customizing under Sales and Distribution, choose System Modifications →
  Routines → Define Copying Requirements.

b) On the Maintain: Requirements & Formulas screen, choose Copying requirements →
 Orders.

c) On the Maintain: Copying Requirements Sales Orders screen, for sales orders, explain
  how to define copying requirements.

---

## PDF page 39

Sujet: Modification du pilotage de la copie

     Besides the routines delivered to you with the system, you can create your own
     individual routines. You can create and process routines for copying requirements,
     data transfer, requirements and formulas using transaction VOFM.

Pilotage de la copie au niveau de l'en-tête

   Figure 14: Pilotage de la copie - niveau de l'en-tête

Le pilotage de la copie au niveau de l'en-tête vous permet de spécifier les types de documents
sources et cibles utilisables pour la copie.
Si le pilotage de la copie ne contient pas la relation source/cible appropriée, vous ne pouvez
pas créer de document de vente en référence à un document de vente correspondant.

L'écran détaillé d'une combinaison document cible/document source sélectionnée
contient les options suivantes :
●  Conditions de copie
●     Routines de transfert de données
●     Indication des numéros de poste à copier dans le document cible
●     Case à cocher Référence complète
 Si la case Référence complète est cochée, le système copie l'ensemble du document
 source dans le document cible, puis affiche des messages si quelqu'un tente de modifier la
 quantité commandée ou de supprimer un poste.

Comment utiliser des conditions de copie

1. Create a new quotation for customer C650-A00.

---

## PDF page 40

Chapitre 2: Pilotage de la copie

a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Quotation → Create.

b) On the Create Quotation: Initial Screen, in the Quotation Type field, enter QT.

c) In the Sales Organization field, enter 1010

d) In the Distribution Channel field, enter 10.

e) In the Division field, enter 00 and choose Enter.

f) On the Create Quotation: Overview screen, in the Sold-To Party field, enter C650-A00.

g) In the Cust. Reference field, enter sample_quotation_01.

h) In the table, enter material P650-100 with an order quantity of 2 units.

i) On the Item Overview tab page, in the Valid-To field, enter the date of the last day of the
 current month.

j) Save your data, and note the quotation number that is generated.

k) Return to the SAP Easy Access screen.

2. Demonstrate that you can copy a quotation to another quotation.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Quotation → Create.

b) On the Create Quotation: Initial Screen, choose Create with Reference.

c) In the Create with Reference dialog box, choose the Quotation tab and enter the
quotation number noted from the previous step.

d) Choose Copy.
Note that you could create quotation because copying from document type QT to QT
is supported.

e) Return to the SAP Easy Access screen.

3. Create an order with C650-B00 as the sold-to party.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Create.

b) On the Create Sales Order: Initial Screen, enter order type OR and choose Enter.

c) On the Create Standard Order: Overview screen, in the Sold-To Party field, enter C650-
B00.

d) In the Cust. Reference field, enter sample_quotation_01.

4. Try to create a sales document.
As a reference, use the quotation you created in a previous step.
a) Choose Sales Document → Create with Reference.

b) Enter the quotation number you created earlier and choose Copy.
Note that you cannot create the order because the sold-to parties are different.

c) Cancel the Create with Reference dialog box and return to the SAP Easy Access screen.

---

## PDF page 41

Sujet: Modification du pilotage de la copie

5. Activate copying requirement 002 in copying control between QT and OR. Note that you
can now create the order with reference to the quotation.
a) In Customizing for Sales and Distribution, choose Sales → Maintain Copy Control for
  Sales Documents.

b) Choose the activity Copying Control: Sales Document to Sales Document.

c) On the Display View Header: Overview screen, choose Table View →
  Display → Change.

d) Choose Position....

e) In the Another entry dialog box, in the two SalesDocType fields, enter both OR and QT
  and choose Continue.

f) Select the row with Standard Order OR as the target and QT Quotation as the source
   and choose Details.

g) On the Change View “Header” Details screen, change the entry in the Copying
  Requirements field from 001 to 002 and save your data.

h) Return to the SAP Easy Access screen and choose Logistics → Sales and
  Distribution → Sales → Order → Create.

i) Choose Enter.

j) On the Create Standard Order: Overview screen, enter the sold-to party C650-B00 and
   customer reference sample_quotation01 and choose Cust. Reference → Create
   with Reference.

k) Enter the quotation number noted earlier in this demo and choose Copy.

l) Confirm the warning that appears.

m) Choose Save and note the standard order number that is displayed.

Comment créer une routine pour le transfert de données
Create a new routine for data transfer 952 with description Header 650 Demo.

       Remarque :
       If you have a problem with creation of the routine, use routine 951 (already
       created in the system).

       Remarque :
       This demonstration requires you to use the order created in the demonstration
       How to Create an Order with Reference to a Quotation.

1. In Customizing for Sales and Distribution, choose System Adaptation → Routines →
Define FORM Routines for Data Transfers, and on the Maintain: Requirements & Formulas
screen, from the menu bar, choose Data transfer → Orders.

---

## PDF page 42

Chapitre 2: Pilotage de la copie

2. Enter the new routine 952 with description Header 650 Demo and choose Enter.
a) On the Maintain: Data transports Sales orders screen, scroll down to a new line in the
table and enter routine number 952 and description Header 650 Demo.

b) Choose Enter and confirm any dialog boxes that appear.

3. Edit routine 952 and enter the following code:
(from Z_LO650_CODE)
perform daten_kopieren_051.
if tvak-vbtyp = charc.
vbak-bname = cvbak-bname.
vbak-telf1 = cvbak-telf1.
endif.
a) Right-click on the routine 952 entry in the table, and from the context menu, choose
Source text.

b) In the ABAP Editor, scroll down and click at the beginning of the last line.

c) Choose Insert on the button bar to create modification, and enter the new lines of
code.

4. Save and activate routine 952.
a) Save your data.

b) Choose the Activate button.

c) Return to the list of procedures.

d) Select procedure 952 and choose Edit → Activate.

e) Choose Activate.

f) Enter MEC_VA as the package.

          Remarque :
          The following data is displayed:
          ●      CVBAK is the header of the source document.
          ●      VBAK is the header of the target document.
          ●      TVAK-VBTYP = CHARC (C) means that the target document is in order.

5. Run Program RV80HGEN to include the new program in the carrier include of the calling
application.

---

## PDF page 43

Sujet: Modification du pilotage de la copie

           Remarque :
           You have to run program RV80HGEN after creation of new object in VOFM
           transaction.
           See the following SAP notes for more information:
           ●   327220 - VOFM function and its objects
           ●   326560 - Various problems when using VOFM functions

6. Activate form routine 952 instead of 051 in copying control QT → OR.
a) Return to the Maintain: Data transports Sales orders screen.

b) Select the row of routine 952 and choose Edit → Activate.

c) Demonstrate that the checkbox in the Active column of routine 952 is now selected.

d) In Customizing for Sales and Distribution, choose Sales → Maintain Copy Control for
  Sales Documents.

e) In the Choose Activity dialog box, choose Copying Control: Sales Document to Sales
  Document.

f) On the Display View “Header”: Overview screen, choose Display → Change.

g) Choose Position...

h) In the Another entry dialog box, in the two SalesDocType fields, enter OR and QT and
  choose Continue.

i) Select the row with standard order as the target and quotation as the source and
   choose Details.

j) On the Change View “Header”: Details dialog box, in the first DataT field, change the
   entry from 051 to 952 and choose Enter.

k) Save your data and return to the SAP Easy Access screen.

7. Create a sales order for the quotation created in the demonstration How to Create an
Order with Reference to a Quotation with purchase order data. Use the same sold-to party.
Show that the purchase order data is copied.
a) On the SAP Easy Access screen, choose Logistics → Sales and
  Distribution → Sales → Order → Create.

b) On the Create Sales Order: Initial Screen, enter an order type of OR and choose Create
  with Reference.

c) Enter the quotation number created in the demonstration How to Create an Order with
  Reference to a Quotation and choose Copy.

d) On the Create Standard Order: Overview screen, enter the customer reference test.

e) Choose Goto → Header → Purchase Order Data.

---

## PDF page 44

Chapitre 2: Pilotage de la copie

 Demonstrate that on the Create Standard Order: Header Data screen, the purchase
 order data is copied from the quotation to the order as a result of the new data transfer
 routine assigned in the copying control between the sales document types QT and OR.

f) Return to the Create Standard Order: Overview screen and save your data.

Pilotage de la copie au niveau du poste

Figure 15: Pilotage de la copie - niveau du poste

Dans le pilotage de la copie, définissez les paramètres relatifs au niveau du poste pour chaque
type de poste et pour chaque combinaison type de document cible/type de document
source.
L'écran détaillé pour un type de poste contient les conditions de copie et les routines de
transfert de données.

Les entrées utilisées communément sur l'écran détaillé sont les suivantes :
●   Quantité/valeur positive/négative
Cette entrée pilote l'incidence de la copie sur la quantité totale du poste défini dans le
document source.
●   Copier quantité
Cette entrée détermine la quantité qui est copiée dans le document cible (par exemple, un
vide indique la meilleure quantité possible, qui est une quantité de commande ouverte
pour le type de document de vente CDCL).
●   Type de détermination du prix
Cette entrée indique comment les données de détermination de prix doivent être gérées
lors de la copie.
●   MAJ flux documents

---

## PDF page 45

Sujet: Modification du pilotage de la copie

Cette entrée indique si le système doit mettre à jour le flux de documents lors de la copie
d'un document.

Connexion à la détermination du type de poste

 Figure 16: Influence de la détermination du type de poste

Les règles de détermination du type de poste sont également applicables lorsque vous créez
des documents de vente avec référence. Le système ne trouve qu'un seul type de poste.
Si vous avez défini manuellement un type de poste dans le document source, vous devez
saisir une valeur dans la zone Type de poste par défaut de sorte qu'en substituant la
détermination du type de poste, le type de poste correspondant soit activé dans le document
cible.

Pilotage de la copie « Commande vers type d'échéance »
Le type d'échéance est très important. Vous l'utilisez pour que l'intégralité des informations et
le stock soient disponibles pour les processus suivants (par exemple, la livraison). Les postes
d'échéance peuvent par exemple être pertinents pour une livraison.
Vous pouvez piloter le transfert des besoin en activant des codes spécifiques au niveau des
échéances. Chaque code correspond aux options pour le transfert des besoins pour chaque
type d'échéance et peut également être activé à ce niveau.
Vous pouvez également piloter le contrôle de disponibilité au niveau des échéances. Si vous
activez le code, un contrôle de disponibilité est effectué pour une transaction. Le code
correspond aux options du contrôle de disponibilité pour chaque type d'échéance et peut
également être activé à ce niveau.

---

## PDF page 46

Chapitre 2: Pilotage de la copie

Règle de liquidation

Figure 17: Mise à jour du statut de référence

Vous pouvez spécifier le moment de la liquidation d'un poste du document source.

Les règles de liquidation sont les suivantes pour un type de poste :
●     Un poste est liquidé dès qu'il est référencé (Règle de liquidation A).
Dans l'exemple présenté dans la figure Mise à jour du statut de référence, la demande
d'offre est entièrement référencée même si seule une quantité partielle a été copiée dans
l'offre.
●     Un poste n'est liquidé qu'après copie de la totalité de la quantité dans un document lié
(Règle de liquidation B).
Le poste de l'offre n'est référencé que partiellement dans l'exemple illustré dans la figure
Mise à jour du statut de référence, ce qui signifie qu'il est possible d'entrer plusieurs
commandes à partir de ce poste jusqu'à ce que la quantité totale soit utilisée.

Vous pouvez sélectionner ces options de règle de liquidation dans le Customizing lors du
pilotage des types de postes.
Si un poste est refusé, le statut Non référencé ou Liquidé est indiqué dans le document
source.

Comment utiliser une offre comme modèle

1. Create sales document type ZAG.
a) In Customizing for Sales and Distribution , choose Sales → Sales Documents → Sales
 Document Header → Define Sales Document Types.

b) Select the table entry for document type QT.

---

## PDF page 47

Sujet: Modification du pilotage de la copie

c) Choose Edit → Copy as.

d) In the Sales Document Type field, overwrite QT with ZAG and overwrite Quotation with
  Sample Quote: S4650.

e) Choose Enter.

f) Do not confirm the system inquiry Is this entry also relevant for copying control?

g) Save your data and confirm any dialog box that appears.

2. Create new copying controls for source ZAG and target QT.
a) In Customizing for Sales and Distribution , choose Sales → Maintain Copy Control for
  Sales Documents.

b) Choose the activity Copying Control: Sales Document to Sales Document.

c) On the Display View “Header”: Overview screen, choose Table View → Display →
  Change.

d) Choose Position... .

e) In the SalesDocType fields, enter OR and QT and choose Continue.

f) Choose the row of the table with target OR and source QT and choose Copy As.

g) In the Target SalesDocTyp field, replace OR with QT, and in the Ref. SalesDoc Type
  field, replace source QT with ZAG.

h) Ensure the Copying requirements field is set to 002 (header different customer) and
  choose Copy (Enter).

i) To copy all dependent entries, choose copy all.

j) To change the item categories at the item level for copying control, on the Change
   View “Item”: Details screen, in the Pos./neg. quantity field, delete the entry to leave it
   blank.

                   Remarque :
                   If necessary, replace the OR category in the Item Category field with the
                   correct QT categories (for example, replace TANN with AGNN).

   The Pos./neg. quantity field indicates whether, during copying, the quantity or value in
   the target document has a negative effect, positive effect, or no effect at all on the
   quantity still to be completed in the source document.

k) Choose Enter and confirm any dialog box that appears.

3. Save your changes.

4. Create a sample quotation for the customer C650-A00.
Enter the following details:
Field                                              Value
Material P650-100                                  1 piece

RA00 % Discount from Net                           25%

---

## PDF page 48

Chapitre 2: Pilotage de la copie

Field                                        Value
Payment terms                                ZB01 14 Days 3%, 30/2%, 45 net

Incoterms                                    EXW Hamburg

Shipping condition                           01 Standard

a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution →
Sales → Quotation → Create.

b) On the Create Quotation: Initial Screen, enter quotation type ZAG and choose Enter.

c) On the Create Sample Quote: S4650: Overview screen, enter the sold-to party C650-
A00, a valid-to date of the last day of the current month, and the customer reference
sample_quotation02.

d) Enter the material P650-100 with an order quantity of 1 and choose Enter.

e) Enter any required fields for the customer in any dialog box that appears and continue.

f) In the menu of the Sample Quote: S4650: Overview screen, choose Go
 To → Header → Shipping and in the field group Shipping, enter 01.

g) On the Item Overview tab page, select the line of the order and choose Display item
details.

h) On the Conditions tab page, choose Insert Row.

i) In the CnTy field, enter RA00, enter an amount of 25, and choose Enter.

j) On the Billing Document tab page, enter payment terms ZB01 and incoterms EXW with
 the description Hamburg.

k) Choose the Shipping tab and confirm the dialog box that appears.

l) Enter a shipping point of 1010 and choose Back.

m) Save your data and return to the Create Quotation: Initial Screen.

5. Create a quotation for customer C650-B00 with reference to the sample quotation and
display the pricing (25% RA00).
a) Enter a quotation type of QT and choose Enter.

b) Choose Sales Document → Create with Reference.

c) In the Quotation tab page, enter the quotation number of the sample quotation you
created and choose Copy.

d) Confirm any dialog box that appears.

e) Enter a customer reference of Referenced_Quot01 and a valid-to date of the last day
of the current month, and choose Enter.

f) Select the line of the order and choose Goto → Item → Conditions.
 Note that the pricing for sales promotion RA00 is 25%.

g) Return to the Create Quotation: Overview screen and save your data.
Note the document number generated for the quotation.

---

## PDF page 49

Sujet: Modification du pilotage de la copie

6. Display the document flow. The reference is still open.
a) Choose Sales Document → Display.

b) Choose Display document flow and demonstrate the document flow with the reference
  still open.

7. Display the following information from the sample quotation:
Status                                        Value
Overall status                                Open
Reference status                              Not referenced (You can copy it as often as
                                              you need to.)

a) Select the quotation in the document flow and choose Status overview.

b) Expand Current hdr status and demonstrate the total processing status and the
  reference status.

c) Return to the SAP Easy Access screen.

8. Show that you cannot create an order with reference to the sample quotation.
a) On the SAP Easy Access screen, choose Logistics → Sales and
  Distribution → Sales → Order → Create.

b) Press Create with reference, enter the quotation number of the sample quotation
  created earlier, and choose Copy.
  The system displays an error message because in copy control the entry for ZAG and
  OR is not maintained.

Pilotage de la copie « Commande vers livraison »
Lorsque vous utilisez des livraisons, il est très important que vous transfériez toutes les
informations de la commande (par exemple, l'emballage d'expédition ou toute autre
caractéristique spécifique). Cela est pertinent lors de la création d'une livraison en référence à
une commande client.
Vous pouvez contrôler le nombre de commandes pouvant être livrées via une livraison unique
en fonction de certains critères. Si certains critères ne sont pas respectés, les informations ne
sont pas transférées dans les documents de livraison.
Cette règle est très importante dans le sens où elle permet d'améliorer la précision des
documents.
Ce paramétrage peut être effectué au niveau de l'en-tête et du poste.

Comment utiliser le pilotage de la copie « Commande vers livraison »
Configure the copy control to a delivery document so that item category TAN is automatically
allocated in the delivery creation.

1. Set up copy control for a delivery document on the Item level.
a) In Customizing for Logistics, choose Logistics Execution → Shipping → Copying
  Control → Specify Copy Control for Deliveries.

---

## PDF page 50

Chapitre 2: Pilotage de la copie

b) On the Display View "Header": Overview screen, choose Table
View → Display → Change.

c) Choose Position, choose delivery type LF and sales document type ZA##.

d) Double-click on the Item node.

e) Choose Position and enter TAN.

f) On the Conditions tab page, choose 101 Item as the Order Requirement, and 699 Item
 Data as the Item Data.

g) On the Control Data tab page, ensure that Update Document Flow is selected.

2. Create a delivery using one of the orders created in step 1 as a reference.
a) On the Shipping tab page, note the shipping point from the order created on item level
Z0##.

b) Choose a selection date that is in the future, for example, today + two weeks. Ensure
the material to be delivered is in stock.

c) Enter the order number.

d) On the Edit tab page, check the Incompletion Log.

e) Make any necessary adjustments, and save your changes.

Pilotage de la copie « Commande vers livraison vers document de facturation »
Lorsque le processus se poursuit avec des postes pertinents pour la livraison et la facturation,
vous pouvez spécifier les informations à transférer lors de la création d'un document de
facturation, ou encore indiquer comment le système doit prendre en charge d'éventuelles
livraisons supplémentaires et si vous avez besoin d'utiliser une ou plusieurs factures.
Les dates des sorties de marchandises sont transférées à partir de la livraison. Elles sont
importantes pour la détermination des conditions de paiement de la facture.
Le pilotage de la copie de facturation est géré au niveau de l'en-tête et du poste.

Comment utiliser le pilotage de la copie « Livraison vers facturation »
In this demonstration, you check that a single delivery can be split into more than one invoice.

1. Set up copy control for a billing document.
a) In Customizing for Sales and Distribution, choose Billing → Billing
Documents → Maintain Copying Control for Billing Documents.

b) Choose the option Copying control: Delivery document to billing document.

c) Choose Position, enter F2 for the Billing Document and LF for the Delivery Type.

d) Select the line containing these two values, then double-click the Item field (under
Header, in the tree on the left side of the screen).

e) Select TAN from the list and navigate to Details.
The Data VBRK/VBRP field contains 001 Inv. Split (Sample).

2. Set up copy control for a billing document.

---

## PDF page 51

Sujet: Modification du pilotage de la copie

           Remarque :
           When creating a billing document, it is very important that the billing
           document is using the relevant data from the delivery documents. Therefore,
           make sure that the correct settings have been configured.

a) In Customizing for Sales and Distribution, choose Billing → Billing
  Documents → Maintain Copying Control for Billing Documents.

b) Choose the option Copying control: Delivery document to billing document.

c) Choose Position, then enter F2 for the Billing Document and LF for the Delivery Type.

d) Select the line containing these two values, then navigate to Details.
  The routine for copying requirements is 003 Header/dlv.-related.

3. Check that the price is taken from the delivery for example on the Item level.
a) In Customizing for Sales and Distribution, choose Billing → Billing
  Documents → Maintain Copying Control for Billing Documents.

b) Choose the option Copying control: Delivery document to billing document.

c) Choose Position, then enter F2 for the Billing Document and LF for the Delivery Type.

d) Select the line containing these two values, then double-click the Item field.

e) Select TAN from the list and navigate to Details.
  For TAN, the price source is E, for Delivery/Order. This means that pricing elements in
  the billing document will be taken from both the order and delivery, as appropriate.

---

## PDF page 52

Chapitre 2: Pilotage de la copie

---

## PDF page 53

Chapitre 2
 Exercice 3
Configuration du pilotage de la copie pour un
document de vente

Exemple de gestion
Dans votre entreprise, vous êtes souvent amené à créer une offre pour un client donné, mais
la commande client pour cette offre s'adresse à un donneur d'ordre différent. L'offre est
établie pour un article donné et avec certaines conditions, de sorte que vous pouvez l'utiliser
comme exemple pour d'autres clients.
Vérifiez votre système SAP et, si nécessaire, configurez-le de façon à pouvoir créer des
commandes en référence à une offre destinée à différents clients. Si le client de l'offre et de la
commande sont identiques, le système copie dans la commande client les données de
commande d'achat définies dans l'offre.
Testez la création d'une commande en référence à une offre. Configurez votre type de
commande ZA## dans le pilotage de la copie afin d'être autorisé à créer des commandes en
référence à des offres pour différents clients. Les données de commande d'achat doivent
aussi être copiées de l'offre dans la commande.
Le service marketing a demandé une offre de référence (type de document de vente) pour
des promotions spéciales. Les différentes agences commerciales peuvent utiliser cette offre
de référence comme modèle lors de la création d'offres pour des clients particuliers. L'objectif
est d'optimiser le processus de création des offres.
Créez des offres à l'aide d'une offre de référence.

       Remarque :
       Dans cet exercice, vous créez une commande de vente nécessaire pour un ou
       plusieurs exercices suivants de ce cours.

Tâche 1 : Configuration et utilisation du pilotage de la copie
Testez la création d'une commande en référence à une offre.

1. Créez une offre de type OF à partir de la demande d'offre client suivante. L'offre doit être
valable jusqu'à la fin du mois suivant.
Utilisez les données du tableau suivant :
Zone                                             Valeur
Donneur d'ordre                                  C650-A##

Réf. client                                      ##-1-1,1

DateLivrSouh.                                    Dans un délai d'une semaine
Fin de validité                                  Date du jour + 3 jours
Article                                          P650-1##

---

## PDF page 54

Chapitre 2: Pilotage de la copie

Zone                                               Valeur
Quantité commandée                                 10

2. Saisissez un prix net (PN00) de 12,00 EUR par pièce ainsi que le nom du salarié ayant
répondu à la demande d'offre (données de commande d'achat).
Saisissez les données du tableau suivant :
Zone                                           Valeur
Type                                           PN00

Montant                                        12,00

Dev.                                           EUR

par                                            1

Unité Quantité                                 pce

Nom                                            M. Miller

3. Sauvegardez l'offre.

Notez le numéro de l'offre.

4. La succursale du client passe une commande se référant à la nouvelle offre. Essayez de
créer une commande de type ZA## en référence à cette offre.
Vérifiez les éléments suivants :
Zone                                  Valeur
Donneur d'ordre                       C650-B##

Réf. client                           ##-1-1,4

DateLivrSouh.                         Dans un délai d'une semaine

5. Comment réagit le système ?

6. Affectez la condition de copie 002 (En-tête - client différent) dans le pilotage de la copie
du type de commande OF au type de commande ZA##.

7. Affectez la routine de transfert de données 951 à votre type de commande afin que le
système copie aussi les données de commande d'achat.

8. Testez la nouvelle configuration pour le type de commande ZA## en répétant la tâche 1,
étape 4.

9. Sauvegardez la commande.

---

## PDF page 55

Sujet: Modification du pilotage de la copie

Quel est le numéro de commande affiché ?

10. Consultez l'offre que vous avez créée auparavant. Vérifiez le statut dans les données d’en-
tête et notez le statut de référence.

11. Le client C650-A## passe également une commande en référence à l'offre de la tâche 1,
étape 1 (numéro de commande d'achat ##-1-1.1).
Saisissez les éléments suivants :
Zone                                           Valeur
Client                                         C650-A##

Réf. client                                    ##-1-2,6

DateLivrSouh.                                  Dans un délai d'une semaine
Article                                        P650-1##

Quantité                                       4

12. Consultez les données de commande d'achat.

Notez que le nom de l'acheteur provient de l'offre.

13. Sauvegardez la commande.

Quel est le numéro de commande affiché ?

14. Consultez l'offre que vous avez créée auparavant. Vérifiez le statut indiqué dans l'en-tête
et notez le statut global.

Tâche 2 : Conditions spéciales remplies à l'aide du pilotage de la copie
Créez un type de document de vente Offre (avec la description Offre réf ##). Ce document de
vente pourra être utilisé comme modèle pour la création d'offres.
Créez une offre standard basée sur l'offre de référence. Créez une commande se référant à
l'offre de référence.

1. Créez le type d'offre ZQ## en copiant le type d'offre OF.

---

## PDF page 56

Chapitre 2: Pilotage de la copie

            Astuce :
            Confirmez le message du système demandant si l'entrée concerne aussi le
            pilotage de la copie.

2. Modifiez le pilotage de la copie pour la source ZQ## et la cible OF pour qu'un autre client
soit autorisé dans le document cible. De plus, accédez au pilotage de la copie au niveau du
poste et supprimez l'entrée dans la zone Quantité pos./nég. pour qu'elle soit vide.

3. Saisissez une offre de référence ZQ## pour le domaine commercial 1010, 10, 00 et l'article
P650-1##.
Saisissez les données suivantes :

Tableau 1: Création d'une offre
Zone                                          Valeur
Donneur d'ordre                               C650-A##

Réf. client                                   Offre de référence ##

Fin de validité                               Fin du mois prochain
DateLivrSouh.                                 Valeur par défaut
Article                                       P650-1##

Quantité commandée                            1

Tableau 2: Remise promotionnelle
Zone                                          Valeur
Type                                          RA00

Montant                                       30

4. Sauvegardez l'offre de référence et revenez à l'écran SAP Easy Access.

Notez le numéro de l'offre.

5. Créez une offre de type OF se référant à l'offre de référence créée. Utilisez les données du
tableau suivant :
Zone                                          Valeur
Donneur d'ordre                               C650-B##

Réf. client                                   Offre de référence ##

DateLivrSouh.                                 Dans un délai d'une semaine
Article                                       P650-1##

---

## PDF page 57

Sujet: Modification du pilotage de la copie

Zone                                        Valeur
Quantité commandée                          1

6. Vérifiez si la remise promotionnelle est correctement copiée dans l'écran des conditions à
partir de l'offre de référence.

7. Sauvegardez l'offre.

Notez le numéro de l'offre.

8. Consultez l'offre de référence que vous avez créée. Contrôlez le statut dans les données
d'en-tête. Notez le statut global et le statut de référence.

9. Pouvez-vous créer une commande se référant à l'offre de référence ?

---

## PDF page 58

Chapitre 2
Solution 3
Configuration du pilotage de la copie pour un
document de vente

Exemple de gestion
Dans votre entreprise, vous êtes souvent amené à créer une offre pour un client donné, mais
la commande client pour cette offre s'adresse à un donneur d'ordre différent. L'offre est
établie pour un article donné et avec certaines conditions, de sorte que vous pouvez l'utiliser
comme exemple pour d'autres clients.
Vérifiez votre système SAP et, si nécessaire, configurez-le de façon à pouvoir créer des
commandes en référence à une offre destinée à différents clients. Si le client de l'offre et de la
commande sont identiques, le système copie dans la commande client les données de
commande d'achat définies dans l'offre.
Testez la création d'une commande en référence à une offre. Configurez votre type de
commande ZA## dans le pilotage de la copie afin d'être autorisé à créer des commandes en
référence à des offres pour différents clients. Les données de commande d'achat doivent
aussi être copiées de l'offre dans la commande.
Le service marketing a demandé une offre de référence (type de document de vente) pour
des promotions spéciales. Les différentes agences commerciales peuvent utiliser cette offre
de référence comme modèle lors de la création d'offres pour des clients particuliers. L'objectif
est d'optimiser le processus de création des offres.
Créez des offres à l'aide d'une offre de référence.

Remarque :
Dans cet exercice, vous créez une commande de vente nécessaire pour un ou
plusieurs exercices suivants de ce cours.

Tâche 1 : Configuration et utilisation du pilotage de la copie
Testez la création d'une commande en référence à une offre.

1. Créez une offre de type OF à partir de la demande d'offre client suivante. L'offre doit être
valable jusqu'à la fin du mois suivant.
Utilisez les données du tableau suivant :
Zone                                              Valeur
Donneur d'ordre                                   C650-A##

Réf. client                                       ##-1-1,1

DateLivrSouh.                                     Dans un délai d'une semaine
Fin de validité                                   Date du jour + 3 jours
Article                                           P650-1##

---

## PDF page 59

Sujet: Modification du pilotage de la copie

Zone                                               Valeur
Quantité commandée                                 10

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Offre → Créer.

b) Dans l'écran Créer Offre : écran initial, saisissez OF dans la zone Type d'offre.

c) Appuyez sur Entrée.

d) Dans l'écran Créer Offre : synthèse, saisissez les données indiquées dans le tableau.

2. Saisissez un prix net (PN00) de 12,00 EUR par pièce ainsi que le nom du salarié ayant
répondu à la demande d'offre (données de commande d'achat).
Saisissez les données du tableau suivant :
Zone                                           Valeur
Type                                           PN00

Montant                                        12,00

Dev.                                           EUR

par                                            1

Unité Quantité                                 pce

Nom                                            M. Miller

a) Dans l'écran Créer Offre : synthèse, sélectionnez la ligne contenant le poste.

b) Cliquez sur le bouton Conditions poste.

c) Dans l'écran Créer Offre : Données poste, cliquez sur le bouton Insérer ligne.

d) Saisissez les données du tableau (en-tête).

e) Appuyez sur Entrée.

f) Revenez à l'écran Créer Offre : synthèse.

g) Dans l'écran Créer Offre : synthèse, cliquez sur le bouton Afficher détails en-tête.

h) Dans l'écran Créer Offre : données d'en-tête, sélectionnez l'onglet Données commande.

i) Dans la page à onglet Données commande, saisissez les données du tableau dans la
   zone Nom.

j) Revenez à l'écran Créer Offre : synthèse.

3. Sauvegardez l'offre.

Notez le numéro de l'offre.

---

## PDF page 60

Chapitre 2: Pilotage de la copie

a) Sauvegardez vos données et notez le numéro d'offre.

b) Revenez à l'écran SAP Easy Access.

4. La succursale du client passe une commande se référant à la nouvelle offre. Essayez de
créer une commande de type ZA## en référence à cette offre.
Vérifiez les éléments suivants :
Zone                                      Valeur
Donneur d'ordre                           C650-B##

Réf. client                               ##-1-1,4

DateLivrSouh.                             Dans un délai d'une semaine

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.

b) Dans l'écran Créer commande client : écran initial, saisissez ZA## dans la zone Type de
commande client.

c) Appuyez sur Entrée.

d) Dans l'écran Créer cde foire et salon ## : synthèse, dans la zone Donneur d'ordre,
saisissez les données du tableau.

e) Sélectionnez Document de vente → Créer avec référence.
 Si la boîte de dialogue Domaine commercial pour le client s'affiche, sélectionnez
 l'entrée pour OrgCm 1010, Canal 10, Secteur 00. Cliquez sur le bouton Sélectionner
 (ou double-cliquez sur l'entrée).
 Une boîte de dialogue Créer avec référence s'affiche.

f) Dans la boîte de dialogue Créer avec référence, sélectionnez l'onglet Offre.

g) Dans la page à onglet Offre, saisissez le numéro d'offre que vous avez noté dans la
zone Offre.

                 Remarque :
                 Vous pouvez également rechercher votre offre avec le numéro de
                 commande d'achat ##-1-1.1.

h) Cliquez sur le bouton Copier.

5. Comment réagit le système ?

Le système affiche un message d'erreur indiquant que les donneurs d'ordre sont
différents. C650-B## et/ou C650-A## (référence).

a) Confirmez (Entrée), puis cliquez sur Interrompre.

6. Affectez la condition de copie 002 (En-tête - client différent) dans le pilotage de la copie
du type de commande OF au type de commande ZA##.

---

## PDF page 61

Sujet: Modification du pilotage de la copie

a) Configurez la condition de copie 002 (En-tête - client différent) dans le Customizing de
  l'Administration des ventes (ADV) sous Vente → Gérer pilotage copie pour documents
  de vente.

b) Dans la boîte de dialogue Sélection de l'activité, double-cliquez sur Pilotage copie : doc.
  de vente après doc. de vente.

c) Dans l'écran Afficher vue "En-tête" : synthèse, sélectionnez Vue de table →
  Afficher → Modifier.

d) Dans l'écran Modifier vue "En-tête" : synthèse, cliquez sur le bouton Positionner.

e) Dans la boîte de dialogue Autre entrée, saisissez ZA## dans la zone Type doc. vente et
  cliquez sur Suite.

f) Sélectionnez la ligne contenant le document cible ZA## et le document source OF.

g) Cliquez sur le bouton Détail.

h) Dans l'écran Modifier vue "En-tête" : synthèse, saisissez la routine 002 dans la zone
  Disposition copie.

i) Sauvegardez vos données.

7. Affectez la routine de transfert de données 951 à votre type de commande afin que le
système copie aussi les données de commande d'achat.
a) Saisissez la routine 951 dans la zone VBAK.

b) Sauvegardez vos données.

8. Testez la nouvelle configuration pour le type de commande ZA## en répétant la tâche 1,
étape 4.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Commande client → Créer.

b) Saisissez ZA## dans la zone Type commande client et appuyez sur Entrée.

c) Entrez le client C650-B## comme donneur d'ordre et ##-1-1.4 comme référence
  client.

d) Sélectionnez Document de vente → Créer avec référence.

e) Dans la page à onglet Offre, saisissez le numéro d'offre ou recherchez votre offre à
  l'aide du numéro de commande d'achat ##-1-1.1.

f) Cliquez sur Sélection postes.

                   Remarque :
                   Appuyez sur Entrée si un message d'avertissement s'affiche.

g) Réduisez la quantité à la valeur requise.

h) Cliquez sur le bouton Copier.

9. Sauvegardez la commande.

---

## PDF page 62

Chapitre 2: Pilotage de la copie

Quel est le numéro de commande affiché ?

10. Consultez l'offre que vous avez créée auparavant. Vérifiez le statut dans les données d’en-
tête et notez le statut de référence.

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Offre → Afficher.

b) Dans la vue Afficher des offres, saisissez le numéro de l'offre créé précédemment et
cliquez sur Suite (Entrée). L'offre est affichée.

c) Cliquez sur le bouton Afficher détails de l'en-tête.
 Dans la page à onglet Statut, notez que le statut de référence est Partiellement
 référencé.

d) Revenez à l'écran SAP Easy Access.

11. Le client C650-A## passe également une commande en référence à l'offre de la tâche 1,
étape 1 (numéro de commande d'achat ##-1-1.1).
Saisissez les éléments suivants :
Zone                                            Valeur
Client                                          C650-A##

Réf. client                                     ##-1-2,6

DateLivrSouh.                                   Dans un délai d'une semaine
Article                                         P650-1##

Quantité                                        4

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.

b) Saisissez votre type de document de vente et le domaine commercial.

c) Cliquez sur le bouton Créer avec référence.

d) Dans la page à onglet Offre, saisissez le numéro d'offre de l'activité 1-1.1.

e) Cliquez sur le bouton Copier.

f) Saisissez les données telles qu'indiquées dans le tableau ci-dessus.

g) Indiquez que vous souhaitez que la livraison soit effectuée une semaine plus tard.

12. Consultez les données de commande d'achat.

---

## PDF page 63

Sujet: Modification du pilotage de la copie

Notez que le nom de l'acheteur provient de l'offre.

13. Sauvegardez la commande.

Quel est le numéro de commande affiché ?

14. Consultez l'offre que vous avez créée auparavant. Vérifiez le statut indiqué dans l'en-tête
et notez le statut global.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Offre → Afficher.
   L'offre créée précédemment s'affiche.

b) Cliquez sur le bouton Afficher détails en-tête doc.

c) Dans la page à onglet Statut, notez que le statut global est Liquidé.

Tâche 2 : Conditions spéciales remplies à l'aide du pilotage de la copie
Créez un type de document de vente Offre (avec la description Offre réf ##). Ce document de
vente pourra être utilisé comme modèle pour la création d'offres.
Créez une offre standard basée sur l'offre de référence. Créez une commande se référant à
l'offre de référence.

1. Créez le type d'offre ZQ## en copiant le type d'offre OF.

             Astuce :
             Confirmez le message du système demandant si l'entrée concerne aussi le
             pilotage de la copie.

a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez
  Vente → Documents de vente → En-tête du document de vente → Définir les types de
  document de vente.

b) Dans l'écran Modifier vue "Gestion des types de commande client" : synthèse, cliquez
  sur le bouton Positionner.

c) Dans la boîte de dialogue Autre entrée, saisissez OF dans la zone Type doc. vente et
  cliquez sur Suite.

d) Sélectionnez la ligne contenant le type de document de vente OF.

e) Cliquez sur le bouton Copier sous.

f) Dans l'écran Modifier vue "Gestion des types de commande client" : détail ensemble,
   remplacez OF par ZQ## dans la zone Type document vente.

g) Saisissez Offre de ref ## comme description du type de document et appuyez sur
  Entrée.

---

## PDF page 64

Chapitre 2: Pilotage de la copie

h) Le système affiche le message suivant : Type doc. de vente : ZQ## L'entrée concerne-
t-elle aussi le pilotage copies ?. Cliquez sur Oui.

i) Sauvegardez vos données et revenez à l'écran SAP Easy Access.

                 Remarque :
                 Si une boîte de dialogue Gestion des vues de table : écran initial apparaît,
                 cliquez sur Suite.

2. Modifiez le pilotage de la copie pour la source ZQ## et la cible OF pour qu'un autre client
soit autorisé dans le document cible. De plus, accédez au pilotage de la copie au niveau du
poste et supprimez l'entrée dans la zone Quantité pos./nég. pour qu'elle soit vide.
a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez
Vente → Gérer pilotage copie pour documents de vente.

b) Sélectionnez l'activité Pilotage copie : doc. de vente après doc. de vente.

c) Dans l'écran Afficher vue "En-tête" : synthèse, sélectionnez Vue de table → Afficher –>
modifier.

d) Sélectionnez Positionner...

e) Dans les zones Type doc. vente, saisissez OF et ZQ## et cliquez sur Suite.

f) Sélectionnez la ligne de la table ayant pour cible OF et pour source ZQ##, puis cliquez
 sur Détail.

g) Définissez 002 (En-tête client diff.) dans la zone Disposition copie.

h) Double-cliquez sur le nœud Poste.

i) Dans l'écran Modifier vue "Poste" : détail, dans la zone Qté positive/négat., supprimez
 l'entrée pour laisser la zone vide.

j) Sauvegardez vos modifications.

3. Saisissez une offre de référence ZQ## pour le domaine commercial 1010, 10, 00 et l'article
P650-1##.
Saisissez les données suivantes :

Tableau 1: Création d'une offre
Zone                                                Valeur
Donneur d'ordre                                     C650-A##

Réf. client                                         Offre de référence ##

Fin de validité                                     Fin du mois prochain
DateLivrSouh.                                       Valeur par défaut
Article                                             P650-1##

Quantité commandée                                  1

---

## PDF page 65

Sujet: Modification du pilotage de la copie

Tableau 2: Remise promotionnelle
Zone                                          Valeur
Type                                          RA00

Montant                                       30

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Offre → Créer.

b) Dans l'écran Créer Offre : écran initial, saisissez ZQ## dans la zone Type d'offre et
  cliquez sur Entrée.

c) Dans l'écran Créer Offre : synthèse, saisissez les données du tableau Création d'une
  offre.

d) Sélectionnez la ligne contenant le poste.

e) Cliquez sur le bouton Conditions poste.

f) Dans l'écran Créer Offre : Données poste, cliquez sur le bouton Insérer ligne dans la
   partie inférieure de l'écran.

g) Saisissez les données du tableau Remise promotionnelle.

4. Sauvegardez l'offre de référence et revenez à l'écran SAP Easy Access.

Notez le numéro de l'offre.

5. Créez une offre de type OF se référant à l'offre de référence créée. Utilisez les données du
tableau suivant :
Zone                                          Valeur
Donneur d'ordre                               C650-B##

Réf. client                                   Offre de référence ##

DateLivrSouh.                                 Dans un délai d'une semaine
Article                                       P650-1##

Quantité commandée                            1

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Offre → Créer.

b) Saisissez OF dans la zone.

c) Appuyez sur Entrée.

d) Saisissez les données du tableau (en-tête).

e) Sélectionnez Document de vente → Créer avec référence.

---

## PDF page 66

Chapitre 2: Pilotage de la copie

f) Dans la page à onglet Offre, saisissez le numéro d'offre que vous avez noté dans la
 zone Offre.

                 Remarque :
                 Vous pouvez également rechercher le numéro d'offre à l'aide de la
                 commande d'achat Offre de référence ##.

g) Cliquez sur le bouton Copier.

h) Cliquez sur Reprendre.

6. Vérifiez si la remise promotionnelle est correctement copiée dans l'écran des conditions à
partir de l'offre de référence.
a) Pour vérifier la valeur de la remise promotionnelle, sur l'écran Créer Offre : synthèse,
sélectionnez la ligne du poste 10.

b) Cliquez sur le bouton Conditions poste.
Dans l'écran Créer Offre : Données poste, le type de condition RA00 est copié à partir
de l'offre de référence.

c) Revenez à l'écran Créer Offre : synthèse.

7. Sauvegardez l'offre.

Notez le numéro de l'offre.

a) Dans l'écran Créer Offre : synthèse, saisissez la fin du mois suivant dans la zone Fin de
validité.

b) Sauvegardez l'offre.

c) Notez le numéro de l'offre.

d) Revenez à l'écran SAP Easy Access.

8. Consultez l'offre de référence que vous avez créée. Contrôlez le statut dans les données
d'en-tête. Notez le statut global et le statut de référence.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Offre → Afficher.

b) Dans l'écran initial Afficher des offres, dans la zone Offre client, saisissez le numéro
d'offre que vous avez noté puis appuyez sur Entrée.

c) Dans l'écran Afficher Offre [votre numéro d'offre] : synthèse, sélectionnez Saut → En-
tête → Statut.

d) Dans l'écran Afficher Offre [votre numéro d'offre] : synthèse, dans la page d'onglet
Statut, vérifiez les détails suivants :
  Zone                                            Valeur
  Statut global                                   En cours

---

## PDF page 67

Sujet: Modification du pilotage de la copie

    Zone                                        Valeur
    Statut de référence                         Non référencé

e) Revenez à l'écran SAP Easy Access.

9. Pouvez-vous créer une commande se référant à l'offre de référence ?
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Commande client → Créer.

b) Dans l'écran Créer commande client : initial, saisissez CDCL dans la zone Type de
  commande client.

c) Appuyez sur Entrée.

d) Cliquez sur le bouton Créer avec référence.

e) Dans la boîte de dialogue Créer avec référence, saisissez Offre de référence ##
  dans la zone Commande. d'achat.

f) Cliquez sur le bouton Rechercher.

g) Dans la boîte de dialogue Liste des occurrences : entrée X, sélectionnez la ligne
  contenant l'offre de référence.

h) Cliquez sur Copier.

---

## PDF page 68

Chapitre 2: Pilotage de la copie

---

## PDF page 69

Chapitre 2
 Exercice 4
Configuration du pilotage de la copie pour un
document de livraison

Exemple de gestion
Vous devez configurer votre système de façon à ce que les livraisons soient créées en
référence au type de commande ZA##.
Étant donné que vous utilisez les options spéciales dans un type de commande personnalisé,
vous appliquez également le processus aux livraisons, afin que toutes les modifications soient
copiées dans les documents de livraison.

        Remarque :
        Dans cet exercice, vous devez utiliser la commande client créée dans l'exercice
        Configuration du pilotage de la copie pour un document de vente.

Tâche 1 : Configuration au niveau de l'en-tête

1. Vérifiez la condition de copie dans le pilotage de la copie pour le type de livraison LF à
partir du type de commande ZA##. Utilisez les informations du tableau suivant :
Zone                                           Valeur

Cible type de livr.                            LF

Type doc. vte source                           ZA##

Condition commande                             001 (En-tête)

Condit. regroupement                           051 (Regroupement)

2. Vérifiez que la routine de données 001 est affectée, afin que toutes les informations soient
copiées dans la livraison.

3. Créez une livraison.
Référez-vous à l'une des commandes créées au cours des exercices précédents et aux
données du tableau suivant :
Zone                                           Valeur

Point d'expédition                             1010

Date de sélection                              Date du jour + 2 semaines
Ordre                                          Commande créée au cours de l'exercice
                                               précédent

4. Affichez la livraison créée.

---

## PDF page 70

Chapitre 2: Pilotage de la copie

Tâche 2 : Configuration au niveau du poste

1. Vérifiez le pilotage de la copie pour un document de livraison, afin que le type de poste
TAN soit automatiquement affecté lors de la création de la livraison. Utilisez les données
du tableau suivant :
Zone                                                     Valeur

Type livraison                                           LF

Type doc. vente                                          ZA##

Type de poste                                            TAN

Condition commande                                       101

Données de poste                                         699

MAJ flux documents                                       Sélectionner

2. Créez une livraison.
Référez-vous à l'une des commandes créées au cours des exercices précédents et aux
données du tableau suivant :
Zone                                        Valeur

Point d'expédition                          1010

Date de sélection                           Date du jour + 2 semaines
Ordre                                       Commande créée au cours de l'exercice
                                          précédent

---

## PDF page 71

Chapitre 2
 Solution 4
Configuration du pilotage de la copie pour un
document de livraison

Exemple de gestion
Vous devez configurer votre système de façon à ce que les livraisons soient créées en
référence au type de commande ZA##.
Étant donné que vous utilisez les options spéciales dans un type de commande personnalisé,
vous appliquez également le processus aux livraisons, afin que toutes les modifications soient
copiées dans les documents de livraison.

       Remarque :
       Dans cet exercice, vous devez utiliser la commande client créée dans l'exercice
       Configuration du pilotage de la copie pour un document de vente.

Tâche 1 : Configuration au niveau de l'en-tête

1. Vérifiez la condition de copie dans le pilotage de la copie pour le type de livraison LF à
partir du type de commande ZA##. Utilisez les informations du tableau suivant :
Zone                                              Valeur

Cible type de livr.                               LF

Type doc. vte source                              ZA##

Condition commande                                001 (En-tête)

Condit. regroupement                              051 (Regroupement)

a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Pilotage
  copie → Définir régie de la copie pour livraisons.

b) Dans l'écran Afficher vue "En-tête" : synthèse, sélectionnez Vue de table → Afficher –>
  Modifier.

c) Dans l'écran Modifier vue "En-tête" : synthèse, sélectionnez Positionner.

d) Saisissez LF comme Type livraison et ZA## comme Type doc. vente, puis cliquez sur
  Suite (Entrée).

e) Dans l'écran Modifier vue "En-tête" : détail, saisissez les données du tableau.

                   Remarque :
                   Si la zone Condit. regroupement contient la valeur 51 (Regroupement),
                   vous pouvez combiner plusieurs commandes dans une même livraison.

---

## PDF page 72

Chapitre 2: Pilotage de la copie

2. Vérifiez que la routine de données 001 est affectée, afin que toutes les informations soient
copiées dans la livraison.
a) Vérifiez la zone Données d'en-tête ; la valeur doit être 001.

b) Sauvegardez vos modifications.

3. Créez une livraison.
Référez-vous à l'une des commandes créées au cours des exercices précédents et aux
données du tableau suivant :
Zone                                          Valeur

Point d'expédition                            1010

Date de sélection                             Date du jour + 2 semaines
Ordre                                         Commande créée au cours de l'exercice
                                            précédent

a) Dans l'écran SAP Easy Access, sélectionnez Administration des ventes
(ADV) → Expédition et transport → Livraison sortante → Créer → Document
individuel → avec référence à la commande client.

b) Dans l'écran Créer livraison sortante avec référence à la commande client, saisissez les
données du tableau :

c) Vérifiez le protocole des données manquantes dans l'onglet Traiter.

d) Apportez les modifications nécessaires et sauvegardez votre travail.

4. Affichez la livraison créée.

Tâche 2 : Configuration au niveau du poste

1. Vérifiez le pilotage de la copie pour un document de livraison, afin que le type de poste
TAN soit automatiquement affecté lors de la création de la livraison. Utilisez les données
du tableau suivant :
Zone                                                        Valeur

Type livraison                                              LF

Type doc. vente                                             ZA##

Type de poste                                               TAN

Condition commande                                          101

Données de poste                                            699

MAJ flux documents                                          Sélectionner

a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Pilotage
copie → Définir régie de la copie pour livraisons.

b) Dans l'écran Afficher vue "En-tête" : synthèse, sélectionnez Vue de table →
Afficher → Modifier.

c) Dans l'écran Modifier vue "En-tête" : synthèse, cliquez sur le bouton Positionner.

---

## PDF page 73

Sujet: Modification du pilotage de la copie

d) Dans la boîte de dialogue Autre entrée, saisissez les données du tableau (zones Type
  livraison et Type doc. vente).

e) Sélectionnez la première ligne dans la liste En-tête.

f) Dans la structure du dialogue, sélectionnez le dossier Poste.

g) Dans l'écran Modifier vue "Poste" : Modifier vue "Poste" : synthèse, cliquez sur le
  bouton Positionner, puis saisissez les données du tableau (zone Type de poste).

h) Sélectionnez la première ligne dans la liste Poste, puis cliquez sur le bouton Détail.

i) Dans l'écran Modifier vue "Poste" : détail, saisissez les données du tableau (zones
   Condition commande et Données de poste).

j) Cochez la case MAJ flux documents.

2. Créez une livraison.
Référez-vous à l'une des commandes créées au cours des exercices précédents et aux
données du tableau suivant :
Zone                                          Valeur

Point d'expédition                            1010

Date de sélection                             Date du jour + 2 semaines
Ordre                                         Commande créée au cours de l'exercice
                                              précédent

a) Dans l'écran SAP Easy Access, sélectionnez Administration des ventes
  (ADV) → Expédition et transport → Livraison sortante → Créer → Document
  individuel → avec référence à la commande client.

b) Dans l'écran Créer livraison sortante avec référence à la commande client, saisissez les
  données du tableau :

c) Vérifiez le protocole des données manquantes dans l'onglet Traiter.

d) Apportez les modifications nécessaires et sauvegardez votre travail.

---

## PDF page 74

Chapitre 2: Pilotage de la copie

---

## PDF page 75

Chapitre 2
 Exercice 5
Configuration du pilotage de la copie pour un
document de facturation

Exemple de gestion
Lorsqu'un document de facturation est créé, il est très important qu'il reprenne les données
pertinentes des documents de livraison. Pour que cela soit possible, vous devez veiller à ce
que les paramétrages appropriés soient corrects.
Par exemple, les informations sur les prix doivent être issues de la livraison ou dépendre de la
quantité livrée. Si elles proviennent d'autres documents, elles ne pourront être que moins
précises. Si un client commande 10 pièces et en reçoit seulement 8, le document de
facturation doit comporter 8 pièces et non pas 10.

       Remarque :
       Dans cet exercice, vous devez utiliser la commande d'achat créée dans l'exercice
       Configuration du pilotage de la copie pour un document de vente.

1. Veillez à ce que les paramétrages soient corrects. Utilisez les données du tableau suivant :
Zone                                          Valeur

Type de facture                               F2

Type livraison                                LF

2. Vérifiez que les éléments de prix sont repris de la livraison ou de la commande client.
Utilisez les données du tableau suivant :
Zone                                          Valeur

Type de poste                                 TAN

---

## PDF page 76

Chapitre 2
Solution 5
Configuration du pilotage de la copie pour un
document de facturation

Exemple de gestion
Lorsqu'un document de facturation est créé, il est très important qu'il reprenne les données
pertinentes des documents de livraison. Pour que cela soit possible, vous devez veiller à ce
que les paramétrages appropriés soient corrects.
Par exemple, les informations sur les prix doivent être issues de la livraison ou dépendre de la
quantité livrée. Si elles proviennent d'autres documents, elles ne pourront être que moins
précises. Si un client commande 10 pièces et en reçoit seulement 8, le document de
facturation doit comporter 8 pièces et non pas 10.

Remarque :
Dans cet exercice, vous devez utiliser la commande d'achat créée dans l'exercice
Configuration du pilotage de la copie pour un document de vente.

1. Veillez à ce que les paramétrages soient corrects. Utilisez les données du tableau suivant :
Zone                                             Valeur

Type de facture                                  F2

Type livraison                                   LF

a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez
Facturation → Factures → Gérer la régie de la copie pour les factures.

b) Dans la boîte de dialogue Sélection de l'activité, sélectionnez Pilotage copie : document
de livraison après facture et appuyez sur le bouton Sélectionner.

c) Dans l'écran Afficher vue "En-tête" : synthèse, cliquez sur le bouton Positionner.

d) Saisissez les données du tableau dans la boîte de dialogue Autre entrée.

e) Sélectionnez la première ligne et cliquez sur Détail.

f) Dans l'écran Afficher vue "En-tête" : détail, notez la valeur de la zone Disposition copie.
La valeur de la zone Disposition copie est 003 E-T se réf. à livr. Il s'agit de la routine qui
gère les conditions de copie.

g) Revenez à l'écran Afficher vue « En-tête » : synthèse.

2. Vérifiez que les éléments de prix sont repris de la livraison ou de la commande client.
Utilisez les données du tableau suivant :

---

## PDF page 77

Sujet: Modification du pilotage de la copie

Zone                                         Valeur

Type de poste                                TAN

a) Dans l'écran Afficher vue "En-tête" : synthèse, dans la structure du dialogue,
  sélectionnez le dossier Poste.

b) Dans l'écran Afficher vue "Poste" : synthèse, cliquez sur le bouton Positionner.

c) Saisissez les données du tableau dans la boîte de dialogue Autre entrée.

d) Cliquez sur le bouton Détail.

e) Notez les valeurs de la zone Source prix.
  Pour TAN, la valeur de la zone Source prix est E (livraison ou commande). Cela signifie
  que des éléments de la détermination du prix dans le document de facturation sont
  enregistrés à partir de la livraison (le cas échéant) ou à partir de la commande client.

---

## PDF page 78

Chapitre 2: Pilotage de la copie

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Modifier le pilotage de la copie

---

## PDF page 79

Chapitre 2

Évaluation des connaissances

1. Parmi les niveaux suivants, lesquels sont utilisés pour le pilotage de la copie dans les
documents de vente ?
Sélectionnez les réponses correctes.

X    A En-tête

X    B Poste

X    C Niveau organisationnel

X    D Échéance

2. Parmi les options suivantes, lesquelles peuvent être personnalisées dans le pilotage de la
copie au niveau du poste ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Routines de transfert de données

X    C Vérification du contrôle de disponibilité

3. Parmi les options suivantes, lesquelles figurent dans les détails de l'écran de pilotage de la
copie accessible au niveau de l'en-tête ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Case à cocher Référence intégrale

X    C Zone Type de détermination du prix

X    D Type d'échéance proposé

---

## PDF page 80

Chapitre 2: Évaluation des connaissances

4. Parmi les options suivantes, lesquelles figurent dans les détails de l'écran de pilotage de la
copie accessible au niveau des échéances ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Case à cocher Référence intégrale

X    C Zone Type de détermination du prix

X    D Type d'échéance proposé

---

## PDF page 81

Chapitre 2

Évaluation des connaissances - Réponses

1. Parmi les niveaux suivants, lesquels sont utilisés pour le pilotage de la copie dans les
documents de vente ?
Sélectionnez les réponses correctes.

X    A En-tête

X    B Poste

X    C Niveau organisationnel

X    D Échéance

Correct ! Le pilotage de la copie pour les documents de vente peut être configuré au
niveau de l'en-tête, des postes et des échéances. Il n'existe aucun niveau intitulé « niveau
organisationnel ». Pour en savoir plus, reportez-vous au sujet Modification du pilotage de
la copie (Chapitre 2, Sujet 1) dans le cours S4650.

2. Parmi les options suivantes, lesquelles peuvent être personnalisées dans le pilotage de la
copie au niveau du poste ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Routines de transfert de données

X    C Vérification du contrôle de disponibilité

Correct ! Dans le pilotage de la copie au niveau du poste, vous pouvez personnaliser les
conditions de copie et les routines de transfert de données. Le contrôle de disponibilité est
piloté au niveau des échéances par le type d'échéance. Pour en savoir plus, reportez-vous
au sujet Modification du pilotage de la copie (Chapitre 2, Sujet 1) dans le cours S4650.

---

## PDF page 82

Chapitre 2: Évaluation des connaissances - Réponses

3. Parmi les options suivantes, lesquelles figurent dans les détails de l'écran de pilotage de la
copie accessible au niveau de l'en-tête ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Case à cocher Référence intégrale

X    C Zone Type de détermination du prix

X    D Type d'échéance proposé

Correct ! Dans le pilotage de la copie accessible au niveau de l'en-tête, vous pouvez
indiquer des conditions de copie et cocher Référence complète. La zone Type de
détermination du prix est définie au niveau du poste. Le type d'échéance proposé est
défini au niveau du type d'échéance. Pour en savoir plus, reportez-vous au sujet
Modification du pilotage de la copie (Chapitre 2, Sujet 1) dans le cours S4650.

4. Parmi les options suivantes, lesquelles figurent dans les détails de l'écran de pilotage de la
copie accessible au niveau des échéances ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Case à cocher Référence intégrale

X    C Zone Type de détermination du prix

X    D Type d'échéance proposé

Correct ! Dans le pilotage de la copie accessible au niveau des échéances, vous pouvez
indiquer des conditions de copie et un type d'échéance proposé. La case Référence
complète est cochée au niveau de l'en-tête. La zone Type de détermination du prix est
définie au niveau du poste. Pour en savoir plus, reportez-vous au sujet Modification du
pilotage de la copie (Chapitre 2, Sujet 1) dans le cours S4650.

---

## PDF page 83

CHAPITRE 3                             Pilotage de textes

Sujet 1
Identification des sources de textes                                                     76
Exercice 6: Identification des sources de textes                            81

Sujet 2
Configuration du pilotage de textes                                                       85
Exercice 7: Configuration d'un pilotage de textes dans le Customizing        101
Exercice 8: Traitement manuel d'un texte                                     109

OBJECTIFS DU CHAPITRE

●   Identifier les sources de textes
●   Configurer le pilotage de textes

---

## PDF page 84

Chapitre 3
  Sujet 1
Identification des sources de textes

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment identifier les sources de textes dans l'Administration des ventes
(SD).

Exemple de gestion
Suite à la saisie de la commande, vous souhaitez analyser le texte de la commande que vous
traitez. Pour cette raison, vous devez disposer des connaissances suivantes :
●   Connaissances sur la source de texte
●   Comment identifier les sources de textes dans SD
●   Compréhension des critères qui influencent la configuration des textes

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Identifier les sources de textes

Sources de textes

Figure 18: Sources de textes

---

## PDF page 85

Sujet: Identification des sources de textes

Dans le système SAP, les textes sont stockés dans différents objets (par exemple, la fiche
client, la fiche article et l'information client-article) et dans tous les documents.
La fiche client contient des textes centraux qui peuvent être utilisés par tout module, des
textes propres à la Comptabilité et à l'Administration des ventes et des textes destinés aux
contacts. Vous pouvez définir différents types de textes pour chacun de ces domaines.

Voici des exemples de types de textes spécifiques aux ventes :
●  Notes sur les ventes
●   Notes de marketing
●   Spécifications d'expédition

La fiche article contient un texte de commande et un texte ADV.
Les documents contiennent des textes aux niveaux de l'en-tête et du poste. Vous pouvez
saisir des textes dans différentes langues. Pendant la saisie de commande, le système peut
accéder aux textes sauvegardés et les copier dans le document. Vous pouvez également
traiter les textes manuellement et en ajouter de nouveaux.

Textes des processus de gestion

 Figure 19: Textes des processus de gestion

Dans les processus de gestion, vous pouvez utiliser des textes des manières suivantes :
● Enregistrer des textes dans les données de base, puis les copier dans des documents
commerciaux.
●   Copier des textes d'un document de référence dans un autre document commercial, par
exemple, d'une offre dans une commande client ou d'une commande client dans un
document de livraison.
●   Copier les textes dans une langue spécifique.
●   Déterminer les conditions de copie des textes.

---

## PDF page 86

Chapitre 3: Pilotage de textes

●     Copier un texte standard dans un document de vente (par exemple, des vœux à l'occasion
des fêtes de fin d'année).

Comment analyser les sources de textes

1. Create a quotation for customer C650-A00.
a) On the SAP Easy Access screen, choose Logistics → Sales and
 Distribution → Sales → Quotation → Create.

b) On the Create Quotation: Initial Screen, enter quotation type QT and choose Enter.

c) Enter a sold-to party of C650-A00 and a valid-to date of the last day in the current
 month.

2. Create some header text, such as Please check our special offers.
a) Choose Goto → Header → Texts.

b) In the text box of the Form Header text type, add a new line with the text Please check
 our special offers.

c) Return to the Create Quotation: Overview screen.

3. Enter material P650-100 with an order quantity of 1 and choose Enter.

4. Use the text determination analysis in the sales order to display the source of the text
(material).
a) Choose the line of the item you just entered in the table and choose
 Goto → Item → Texts.

b) On the Create Quotation: Item Data screen, choose Display log.

c) Expand the row of Text ty 0001 Material sales text.
 Demonstrate how the text determination analysis displays the source of the text
 (material).

5. Create an order with reference to the quotation.
a) Return to the Create Quotation: Item Data screen and save your data.

b) Note the document number generated for the quotation and return to the SAP Easy
 Access screen.

c) On the SAP Easy Access screen, choose Logistics → Sales and
 Distribution → Sales → Order → Create.

d) Enter an order type of OR and choose Create with Reference.

e) In the Create with Reference window, enter the document number of the quotation you
 just created and choose Copy.

f) Enter customer reference 4711.

6. Show that the header text has been copied.
a) Choose Goto → Header → Texts.

b) Demonstrate that the header text has been copied.

---

## PDF page 87

Sujet: Identification des sources de textes

7. Show the source of the item text.
a) Return to the Create Standard Order: Overview screen.

b) Choose Goto → Item → Texts.

c) On the Create Standard Order: Item Data screen, choose Display log.

d) Expand the row of Text ty 0001 Material sales text.
  Demonstrate that the the text determination analysis shows the source of the item
  text.

The source is now the preceding document.

---

## PDF page 88

Chapitre 3: Pilotage de textes

---

## PDF page 89

Chapitre 3
 Exercice 6
Identification des sources de textes

Exemple de gestion
En tant que salarié d'une agence commerciale, vous avez créé une commande et imprimé la
confirmation correspondante (accusé de réception). Vous trouvez un texte supplémentaire
dans le poste de commande que vous n'avez pas saisi. Vous voulez que l'administrateur
système explique pourquoi le texte est apparu dans le document.

1. Recherchez la commande d'achat numéro ##-1-2.6.

2. Affichez le document et analysez la source du texte ADV relatif à l'article figurant dans le
poste de la commande.

3. D'où vient le texte ADV relatif à l'article (clé d'objet) ?

4. Affichez le texte ADV dans la fiche de l'article P650-1##. Utilisez les données du tableau
suivant :
Zone                                             Valeur
Org. commerciale                                 1010

Canal distrib.                                   10

---

## PDF page 90

Chapitre 3
Solution 6
Identification des sources de textes

Exemple de gestion
En tant que salarié d'une agence commerciale, vous avez créé une commande et imprimé la
confirmation correspondante (accusé de réception). Vous trouvez un texte supplémentaire
dans le poste de commande que vous n'avez pas saisi. Vous voulez que l'administrateur
système explique pourquoi le texte est apparu dans le document.

1. Recherchez la commande d'achat numéro ##-1-2.6.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Afficher.

b) Dans Afficher commande client : écran initial, sélectionnez la zone Commande et
appuyez sur F4.

c) Dans l'écran Document de vente (1), sur la page à onglet Documents de vente par
numéro de commande chez client, saisissez ##-1-2.6 dans la zone Nº commande
d'achat.

d) Cliquez sur Lancer rech.

e) Sélectionnez la ligne contenant la commande.

f) Cliquez sur Reprendre.

g) Dans Afficher commande client : écran initial, sélectionnez Entrée.

2. Affichez le document et analysez la source du texte ADV relatif à l'article figurant dans le
poste de la commande.
a) Dans l'écran Afficher Cmde XX : synthèse, sélectionnez la ligne contenant le poste de
commande 10.

b) Cliquez sur le bouton Afficher détails du poste.

c) Dans l'écran Afficher Cmde XX : Données poste, sélectionnez l'onglet Textes.

d) Dans la page à onglet Textes, cliquez sur Appeler le protocole.

3. D'où vient le texte ADV relatif à l'article (clé d'objet) ?

Le texte ADV relatif à l'article provient de la clé d'objet VBBP, ID 0001 (textes de postes du
document précédent et texte ADV relatif à l'article).

a) Dans l'écran Analyse de la détermination des textes : vue de base, sélectionnez
Ty.txte 0001.

b) Notez les valeurs des colonnes Objet et ID.

---

## PDF page 91

Sujet: Identification des sources de textes

c) Revenez à l'écran SAP Easy Access.

4. Affichez le texte ADV dans la fiche de l'article P650-1##. Utilisez les données du tableau
suivant :
Zone                                          Valeur
Org. commerciale                              1010

Canal distrib.                                10

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Données de base → Produits → Article → Pdts commercialisab. → Afficher.

b) Dans l'écran Afficher article (Écran initial), saisissez P650-1## dans la zone Article.

c) Cliquez sur Sélection des vues.

d) Dans la boîte de dialogue Sélection des vues, sélectionnez la ligne Texte ADV.

e) Cliquez sur Reprendre.

f) Saisissez les données du tableau dans la boîte de dialogue Nvx organisationnels.

g) Cliquez sur Reprendre.
  Le texte ADV s'affiche.

---

## PDF page 92

Chapitre 3: Pilotage de textes

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Identifier les sources de textes

---

## PDF page 93

Chapitre 3
    Sujet 2
Configuration du pilotage de textes

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment configurer le pilotage de textes dans le Customizing des
documents de vente.

Exemple de gestion
Pour la saisie d'une commande, vous devez implémenter des conditions propres au client, par
exemple en traitant les textes existants et parfois en définissant de nouveaux types de textes.
Vous devez aussi parfois lier ces types de textes au traitement des documents. Pour cette
raison, vous devez disposer des connaissances suivantes :
●   Comment définir et affecter des types de textes dans le Customizing
●   Comment configurer le pilotage de textes dans le document de vente

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Configurer le pilotage de textes

Pilotage de textes

 Figure 20: Pilotage de textes : synthèse

---

## PDF page 94

Chapitre 3: Pilotage de textes

Le pilotage de textes est utilisé pour déterminer automatiquement des textes.

Pour déterminer le texte, procédez comme suit :
1. Créez un type de texte pour un objet de texte.

2. Définissez différents schémas de textes.

3. Affectez le type de texte aux schémas de textes définis.

4. Affectez le schéma de textes au type de document ou type de poste approprié.

5. Définissez une séquence d'accès pour chaque type de texte dans le schéma de textes.

6. Définissez des paramètres spécifiques pour chaque type de texte, tels que l'ajout d'un
type de texte dans le protocole de documents incomplets.

Type de texte

Figure 21: Type de texte

Vous pouvez créer un type de texte pour un objet de texte spécifique.
Le système SAP contient un grand nombre de types de textes. Vous pouvez également créer
des types de textes spécifiques à un client donné.

---

## PDF page 95

Sujet: Configuration du pilotage de textes

Séquence d'accès

 Figure 22: Séquence d'accès

Une séquence d'accès consiste en différentes étapes d'accès individuelles. Une séquence
d'accès vous permet de déterminer la modalité de recherche utilisée par le système pour
déterminer automatiquement un texte.
Chaque étape d'accès comprend un objet de texte spécifié et un type de texte faisant office
de source de texte de l'accès. Vous pouvez saisir des conditions pour chaque étape de l'accès
et restreindre ainsi la recherche aux éléments suivants :
●   Rôles partenaires spécifiques
●   Langues spécifiques
●   Toute autre condition que vous pouvez définir vous-même Si vous configurez une nouvelle
séquence d'accès ou que vous modifiez les séquences existantes, vous devez générer des
étapes d'accès afin d'activer cette nouvelle séquence ou les modifications.

---

## PDF page 96

Chapitre 3: Pilotage de textes

Objets de texte autorisés

Figure 23: Objets de texte autorisés

Chaque étape d'accès comprend un objet de texte spécifié faisant office de source de texte de
l'accès. Les objets de texte que vous pouvez utiliser dans l'application Administration des
ventes (SD) sont indiqués dans les valeurs autorisées qui sont illustrées dans la figure Objets
de texte autorisés.

Schéma de textes

Figure 24: Schéma de textes

Les schémas de textes contiennent tous les types de textes pour un contexte donné. Vous
pouvez définir les types de textes pour un objet de texte. Les attributs possibles d'un schéma

---

## PDF page 97

Sujet: Configuration du pilotage de textes

de textes ne sont pas identiques pour les objets de texte du client et du document. En
particulier, les schémas de textes ne comportent pas de séquence d'accès pour les clients.
Vous pouvez indiquer si vous voulez copier le texte ou l'utiliser en tant que référence.

Pour les schémas de textes d'un document, vous pouvez spécifier les caractéristiques
suivantes :
●  Si le texte doit être obligatoire (le texte doit figurer dans le protocole de documents
incomplets)
●   Si le texte doit être déterminé automatiquement
●   Si le texte doit être affiché dans une fenêtre (pop-up) lors de son transfert dans le
document

Affectation de schéma

 Figure 25: Affectation de schéma

Vous devez affecter chaque attribut d'un objet de texte à l'un des schémas de textes définis,
ce qui signifie que lorsque vous créez une fiche client, le système utilise le schéma de textes
qui a été affecté au groupe de comptes de ce client.
Lorsque vous saisissez une commande client, le système utilise le schéma affecté au type de
document de vente pour l'en-tête et le schéma affecté au type de poste pour les postes.

---

## PDF page 98

Chapitre 3: Pilotage de textes

Analyse de la détermination des textes

Figure 26: Analyse de la détermination des textes

Vous pouvez utiliser une fonction d'analyse du pilotage de textes dans les écrans de gestion
des documents de vente (lors de la création et de la modification des documents). Pour
utiliser cette fonction, sélectionnez Saut → En-tête (ou poste) → Textes. Cliquez sur le bouton
Protocole.
À partir de la fonction d'analyse, vous pouvez directement accéder au Customizing et
configurer le pilotage de textes.

Comment créer un type de texte pour le niveau en-tête d'un document de vente
Create text type Y00A for the header level of a sales document.

     Remarque :
     This demonstration requires you to use the sales order type created in the
     demonstration How to Use a Quotation as a Template.

1. Create text type Y00A.
a) In Customizing for Sales and Distribution, choose Basic Functions → Text
Control → Define and Assign Text Determination Procedures.

b) In the Select Activity dialog box, choose Configuration: Texts.

c) On the Customizing Text Determination screen, beside Sales Document, select Header.

d) Choose Text types and confirm any dialog box that appears.

e) Choose New entries and enter the text ID Y00A with a description Header level
Y00A.

f) Save your data.

---

## PDF page 99

Sujet: Configuration du pilotage de textes

2. Copy the text determination procedure Y1 from 01 by using the Copy button and include
text type Y00A. Sometimes, entire values are not copied into the new procedure. Correct
manually if necessary.
a) Return to the Customizing Text Determination screen and choose Change.

b) Select the row of text procedure 01, and choose Copy As.

c) Enter a text procedure Y1 with a description New procedure, and choose Copy.

d) In the Specify object to be copied window, choose copy all.

e) Confirm the dialog box and save your data.

3. Create access sequence 9900 for the text object VBBK, ID Y00A, all languages, and
requirement 1.
a) On the Change View “TextDetProc Sales Doc. Header”: Overview screen, double-click
  Access sequences.

b) Choose New Entries.

c) Enter access sequence 9900 with the description New access sequence, and
  choose Enter.

d) Select the row of access sequence 9900 and double-click Access sequence for Text
  ID’s.

e) Choose New Entries.

f) In an empty row, enter sequence number 10, text object VBBK, and ID Y00A.

g) Scroll the table to the right and select the All languages indicator, enter a requirement
  of 1, and save your data.

4. Assign a text determination procedure to document types ZAG and OR.
a) Double-click Text ID’s in Textprocedure.

b) If the Determine Work Area: Entry dialog box appears, enter a TextDetermProcedure of
  Y1 and choose Continue.

c) Choose New Entries.

d) Enter a new row with a sequence number 20, ID Y00A, and access sequence 9900, and
  double-click Text procedure assignment.

e) In the TxtDe column of sales document type ZAG, enter Y1.

f) Choose Position, enter OR, and choose Continue.

g) In the TxtDe column of sales document type OR, enter Y1.

h) Save your data.
  You have now assigned the text determination procedure to document types QT and
  OR.

5. Test the document flow for the quotation and order. Show the text determination analysis.
a) On the SAP Easy Access screen, choose Logistics → Sales and
  Distribution → Sales → Quotation → Create.

---

## PDF page 100

Chapitre 3: Pilotage de textes

b) Enter a quotation type of ZAG and choose Enter.

c) Enter a sold-to party of C650-A00, a valid-to date of the last day of the current month,
and choose Goto → Header → Texts.

d) Enter some header text, such as Please check our special offers.

e) Go back to the Create Quotation: Overview screen, enter material P650-100 with a
quantity of 1 and choose Enter.

f) Select the row of the item you just entered and choose Goto → Item → Texts.

g) Choose Display Log, and expand Text ty 0001 Material sales text.
The text determination analysis displays the source of the text (material).

h) Return to the Create Quotation: Item Data screen and save your data.

i) Note the document number generated for the quotation.

6. Create an order with reference to the quotation to check the text.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Create.

b) Enter an order type of OR and choose Create with Reference.

c) In the Create with Reference window, enter the quotation number of the quotation you
just created and choose Copy.

d) Enter a customer reference of 4711 and choose Goto → Header → Texts.
Demonstrate that the text has been copied.

e) To demonstrate the text determination analysis, choose Display Log, and expand Text
type Y00A Header Level.

Comment créer un type de texte pour le niveau poste d'un document de vente
Add the item level text type with description label text for all customers that use item
category TAN.

1. Create text type Z001 for the item level of a sales document.
a) In Customizing for Sales and Distribution, choose Basic Functions → Text
Control → Define and Assign Text Determination Procedures.

b) In the Select Activity dialog box, choose Configuration: Texts.

c) On the Customizing Text Determination screen, next to Sales Document, select Item.

d) Choose Text types and confirm any dialog box that appears.

e) Choose New entries and enter the text ID Z001 with a description Item level
sales.

f) Save your data.

2. Create access sequence 9800 for the text object VBBP, ID Z001, all languages, and
requirement 50.

---

## PDF page 101

Sujet: Configuration du pilotage de textes

a) Return to the Customizing Text Determination screen and choose Change.

b) On the Change View “TextDetProc Sales Document Item”: Overview screen, double-
  click Access sequences.

c) Choose New Entries.

d) Enter access sequence 9800 with the description Item access sequence, and
  choose Enter.

e) Select the row of access sequence 9800 and double-click Access sequence for Text
  ID’s.

f) Choose New Entries.

g) In an empty row, enter sequence number 10, text object VBBP, and ID Z001.

h) Scroll the table to the right and select the All languages indicator, enter a requirement
  of 50, and save your data.

3. Copy the text determination procedure Z1 from 01 by using the Copy button and include
Z001.
a) Double-click Textprocedure.

b) Select the row of text procedure 01 and choose Copy As.

c) Enter a text procedure value of Z1 and choose Copy.

d) Choose copy all and confirm the information dialog box that appears.

e) Select the row of text procedure Z1 and double-click Text ID’s in Textprocedure.

f) Choose New Entries and enter sequence number 40, ID Z001, access sequence 9800,
   and choose Enter.

g) Save your data.
  Demonstrate that the text determination procedure Z1 is copied from 01 and it is
  included with the text ID Z001.

4. Assign a text determination procedure to item category TAN.
a) Select the row of sequence number 40 and double-click Text procedure assignment.

b) Choose Postition, enter TAN. and choose Continue.

c) In the TxPrc column of the row of item category TAN, enter Z1 and save your data.

d) Return to the SAP Easy Access screen.

---

## PDF page 102

Chapitre 3: Pilotage de textes

Références et copies

Figure 27: Utilisation de textes en tant que références

Pour chaque type de texte d'un schéma, vous pouvez spécifier si ce texte repris sera copié
(dupliqué) ou utilisé comme référence à partir du document source (modèle).

Les conséquences de l'utilisation d'un texte en tant que référence sont les suivantes :
●  Si vous modifiez le texte dans le document de vente 1, le texte change aussi dans le
document de vente 2.
●   Si vous modifiez le texte dans le document de vente 2, une nouvelle occurrence du texte
est enregistrée. Les modifications apportées au texte du document de vente 1 n'ont
aucune incidence sur le texte du document de vente 2.

---

## PDF page 103

Sujet: Configuration du pilotage de textes

Copie de textes

   Figure 28: Copie de textes

Les conséquences de la copie d'un texte sont les suivantes :
●  Vous pouvez modifier le texte dupliqué dans le document.
●     Les modifications apportées au texte du document de vente 1 n'ont pas d'incidence sur le
 texte du document de vente 2.

La copie des textes consomme plus de mémoire que la référence à des textes d'un document
source. Il est donc recommandé de n'utiliser la fonction de copie que si elle est absolument
indispensable.

Comment utiliser un texte standard en tant que référence
Create a standard text and reference it.

          Remarque :
          This demonstration requires you to use the sales order created in the
          demonstration How to Create an Order with Reference to a Quotation.

1. Create a standard text and enter the following details:
  Field                                          Value
  Text Name                                      S4650

  Text ID                                        SDVD

---

## PDF page 104

Chapitre 3: Pilotage de textes

Field                                          Value
Language                                       Course language

a) On the SAP Easy Access screen, choose Tools → Form Printout
→ SAPscript → Standard Text.

b) On the Standard Text: Request screen, enter the details in the table and choose Create.

2. Enter For up-to-date information, read the test report in the latest
issue of Motorcycle Today and save your data.

3. Change the sales order which was created in the demonstration How to Create an Order
with Reference to a Quotation.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Change.

b) Enter the number of the sales order created in the demonstration How to Create an
Order with Reference to a Quotation and choose Enter.

4. On the Texts tab page for the first item, create a new text.
a) Select the row of item 10 and choose Display item details.

b) Choose the Texts tab.

c) To create a new text, double-click Material sales text.

5. Enter a blank space and choose Detail.

6. On the editor screen, include and expand the standard text module.
a) Choose Include → Text → Standard.

b) Enter the text name S4650, text ID SDVD, and the course language.

c) Select the Expand Immediately indicator and choose Continue.

d) Save your data.

e) Return to the SAP Easy Access screen, and save your data when prompted.

7. Display the sales document on the screen.
a) On the SAP Easy Access screen, choose Logistics → Sales and
Distribution → Sales → Order → Display.

b) On the Display Sales Order: Initial Screen, ensure that the sales order you just changed
is already entered in the Order field and choose Enter.

c) Select the row of item 10 and choose Goto → Item → Texts.
You can see that the standard text is added.

---

## PDF page 105

Sujet: Configuration du pilotage de textes

Document précédent comme source de texte pour les documents de facturation

 Figure 29: Un document précédent comme source de texte dans un document de facturation

Vous pouvez utiliser le Customizing du type de facture afin de sélectionner, pour un
document de facturation donné, le document précédent pour les objets de texte VBBK et
VBBP. Cette sélection s'applique à tous les types de textes du document de facturation
concerné.
Si vous cochez la case Livraison: Texte, les textes correspondants seront issus de la livraison
sortante. Si vous ne cochez pas la case, les textes correspondants seront issus de la
commande.

---

## PDF page 106

Chapitre 3: Pilotage de textes

Routines de transfert de données propres au client

Figure 30: Routine de transfert de données propre au client et applicable aux textes

Vous pouvez également créer des routines de transfert de données pour les textes en
utilisant la transaction VOFM.
L'espace nom réservé aux routines client (clé de deux chiffres) est alors compris entre 50 et
99. Vous trouverez les descriptions des structures de données disponibles dans les routines
types 1 et 2 qui sont standard.

Comment utiliser un exit utilisateur pour les textes
A data transfer routine for texts (no. 91) is available in the training system. With this routine,
you can read standard texts with a composed variable key, such as ZMAT: material number
(for example, ZMAT:P650-100 for Locks).
With this routine, you can extend the access sequence 23 Sales document item/Packing notes
to read a material-specific packaging note. There is no standard configuration in text control
for the material texts. The routine offers a workaround.

1. Ensure that routine 91 is active.
a) In Customizing for Sales and Distribution, choose System Adaptations → Routines →
Define Copying Requirements.

b) On the Maintain: Requirements & Formulas screen, choose Data Transfer → Texts.

c) On the Maintain: Data transports Texts screen, on the row for routine number 91, note
if the Active checkbox is selected or deselected.
The Active checkbox is selected. Routine 91 is active.

2. Create a standard text.

---

## PDF page 107

Sujet: Configuration du pilotage de textes

a) On the SAP Easy Access screen, choose Tools → Form Printout → SAPscript →
  Standard Text.

b) On the Standard Text: Request screen, enter the following details:
    Field                                       Value
    Text Name                                   ZMAT:P650-100

    Text ID                                     SDVD (Std. text for SD forms)

    Language                                    Course language

c) Choose Create.

d) Enter the standard text Material-specific packaging note and save your data.

3. Extend the access sequence 23 (Sales document item/Packing notes) with a new line:
TEXT, SDVD, all languages, UserExit 91 (in field data).
a) In Customizing for Sales and Distribution, choose Basic Functions → Text
  Control → Define and Assign Text Determination Procedures → Configuration: Texts.

b) On the Customizing Text Determination screen, beside Sales Document, select Item
  and choose Change.

c) Double-click Access sequence for Text ID’s.

d) In the Determine Work Area: Entry window, enter access sequence 0023 and choose
  Continue.

e) Choose New Entries and enter a new line in the table with sequence 5, text object
  TEXT, ID SDVD, the All Languages indicator selected, and in the DatTr field enter 91.

f) Save your data.
   If you receive a warning about choosing your key from the allowed namespace, choose
   Enter to continue.

g) Return to the Change View “Sales Document Item Access Sequence 0023”: Overview
  screen and demonstrate that the new line has been created to extend the access
  sequence with data transfer routine 91.

4. Enhance text determination procedure Z1.
a) Double-click Textprocedure.

b) Select the row of text procedure Z1

c) Double-click Text ID's in Textprocedure.

d) Choose New Entries and enter sequence number 20, ID 0003, access sequence 23,
  and choose Enter.

e) Save your data.

5. Create a sales order using material P650-100. Show that the packing note contains your
standard text.
a) On the SAP Easy Access screen, choose Logistics → Sales and
  Distribution → Sales → Order → Create.

---

## PDF page 108

Chapitre 3: Pilotage de textes

b) On the Create Sales Order: Initial Screen, enter an order type of OR and choose Enter.

c) On the Create Standard Order: Overview screen, enter a sold-to party of C650-A00 and
a customer reference of 4711.

d) Enter material P650-100 with an order quantity of 1 and choose Enter.

e) Choose Goto → Item → Texts.

f) On the Create Standard Order: Item Data screen, double-click Packing note for the
course language.
Demonstrate that the packing note contains the created standard text.

g) Save your data.

---

## PDF page 109

Chapitre 3
 Exercice 7
Configuration d'un pilotage de textes dans le
Customizing

Exemple de gestion
En tant que salarié du service client, vous voulez saisir un texte d'en-tête d'offre particulier
dans les offres. Pour ce faire, vous devez configurer un type de texte approprié dans le
système SAP. Configurez le pilotage de textes en créant un schéma de textes.

 Figure 31: Conversion de conditions dans le pilotage des messages

La figure Conversion de conditions dans le pilotage des messages illustre les nouvelles
conditions du service que vous voulez implémenter à l'aide du pilotage de textes. Une autre
partie de l'implémentation concerne le pilotage des messages.

       Remarque :
       Dans cet exercice, vous allez créer une offre avec la référence client ##-2-4.1, qui
       est requise pour les exercices de ce cours.

Création d'un schéma de textes

1. Copiez le schéma de textes 01 afin de créer un schéma de textes pour le document de
vente Textes d'en-tête, groupe ## avec un ID d'une valeur égale à 50 + ## (par exemple,
pour ## = 01, la valeur de l'ID serait 51).

---

## PDF page 110

Chapitre 3: Pilotage de textes

2. Créez votre propre séquence d'accès 90## pour le type de texte Y001. Le texte d'en-tête
de l'offre doit être copié à partir du document de référence dans la langue appropriée.
Utilisez les données du tableau suivant :
Zone                                         Valeur
N°                                           10

Objet texte                                  VBBK

ID                                           Y001

Ttes langues                                 Sélection
Condition                                    1

3. Ajoutez le type de texte Y001 à votre schéma de textes (50 + ##) et affectez-lui la
séquence d'accès 90##.

4. Affectez le nouveau schéma de textes de l'en-tête du document de vente au type de
document ZA##.

Testez le fonctionnement de la nouvelle affectation.

1. Créez une offre de type OF. Utilisez les données de demande d'offre client suivantes :
Zone                                         Valeur
Donneur d'ordre                              C650-B##

Nom                                          M. Smith

N° de demande d'offre                        ##-2-4,1

Fin de validité                              Fin du mois prochain
Article                                      P650-1##

Quantité d’ordre                             1

2. Créez un texte d'en-tête d'offre, par exemple Jusqu'à épuisement du stock.
Toutes les offres sont soumises à une vente préalable.

3. Créez une commande client de type ZA## en référence à l'offre (numéro de commande
d'achat ##-2-4.3).

4. Vérifiez que le texte d'en-tête de l'offre a été copié dans la commande. Si nécessaire,
utilisez la fonction d'analyse de la détermination des textes pour corriger les problèmes
éventuels.

5. Sauvegardez la commande et notez le numéro du document.

---

## PDF page 111

Chapitre 3
 Solution 7
Configuration d'un pilotage de textes dans le
Customizing

Exemple de gestion
En tant que salarié du service client, vous voulez saisir un texte d'en-tête d'offre particulier
dans les offres. Pour ce faire, vous devez configurer un type de texte approprié dans le
système SAP. Configurez le pilotage de textes en créant un schéma de textes.

 Figure 31: Conversion de conditions dans le pilotage des messages

La figure Conversion de conditions dans le pilotage des messages illustre les nouvelles
conditions du service que vous voulez implémenter à l'aide du pilotage de textes. Une autre
partie de l'implémentation concerne le pilotage des messages.

       Remarque :
       Dans cet exercice, vous allez créer une offre avec la référence client ##-2-4.1, qui
       est requise pour les exercices de ce cours.

Création d'un schéma de textes

1. Copiez le schéma de textes 01 afin de créer un schéma de textes pour le document de
vente Textes d'en-tête, groupe ## avec un ID d'une valeur égale à 50 + ## (par exemple,
pour ## = 01, la valeur de l'ID serait 51).

---

## PDF page 112

Chapitre 3: Pilotage de textes

a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez Fonctions de
base → Pilotage texte → Définir et affecter les schémas texte.

b) Dans la boîte de dialogue Sélection de l'activité, sélectionnez Configuration des textes.

c) Dans l'écran Affectation texte customizing, cochez la case d'option En-tête pour l'objet
de texte Document vente.

d) Cliquez sur Modifier.

e) Dans l'écran Modifier vue "Sch. txtes Doc.comm., en-tête" : synthèse, dans la structure
du dialogue, sélectionnez Schéma de textes.

f) Sélectionnez la ligne dont la zone SchTx contient la valeur 01.

g) Cliquez sur Copier sous.

h) Remplacez la clé 01 par la vôtre (50 + ##) et modifiez la description en saisissant
Texte en-tête–gr##.

i) Appuyez sur Entrée.
  Le message Sélectionnez la clé dans l'espace nom autorisé s'affiche.

j) Appuyez sur Entrée.

k) Dans la boîte de dialogue Spécifier des objets à copier, cliquez sur Tout copier.

l) Cliquez sur Copier.

m) Sauvegardez vos données.

2. Créez votre propre séquence d'accès 90## pour le type de texte Y001. Le texte d'en-tête
de l'offre doit être copié à partir du document de référence dans la langue appropriée.
Utilisez les données du tableau suivant :
Zone                                           Valeur
N°                                             10

Objet texte                                    VBBK

ID                                             Y001

Ttes langues                                   Sélection
Condition                                      1

a) Dans la structure du dialogue, sélectionnez Séquences d'accès.

b) Cliquez sur Nouvelles entrées.

c) Dans l'écran Nouvelles entrées (vue Doc.comm., en-tête Séquence accès), saisissez
90## dans la zone Séquence d'accès.

d) Saisissez la description Séq accès gr##.

e) Appuyez sur Entrée.

f) Sélectionnez la ligne contenant la séquence d'accès 90##.

g) Dans la structure du dialogue, double-cliquez sur Séquence d'accès pour ID de texte.

---

## PDF page 113

Sujet: Configuration du pilotage de textes

h) Dans l'écran Modifier vue "Doc.comm, en-tête, Séquence accès 90##" : synthèse,
  cliquez sur Nouvelles entrées.

i) Dans l'écran Nouvelles entrées (vue Doc.comm., en-tête, Séquence accès 90##),
   saisissez les données du tableau.

j) Sauvegardez la séquence d'accès.

k) Revenez à l'écran Modifier vue "Doc.comm, en-tête, Séquence accès" : synthèse.

3. Ajoutez le type de texte Y001 à votre schéma de textes (50 + ##) et affectez-lui la
séquence d'accès 90##.
a) Dans l'écran Modifier vue "Doc.comm, en-tête, Séquence accès" : synthèse, dans la
  structure du dialogue, double-cliquez sur Schéma de textes.

b) Sélectionnez la ligne contenant le schéma de textes avec votre clé (50 + ##).

c) Dans la structure du dialogue, sélectionnez ID de texte dans le schéma de textes.

d) Dans l'écran Modifier vue "Doc.comm, en-tête ID de texte dans le schéma de textes [50
  + ##]" : synthèse, cliquez sur Nouvelles entrées.

e) Dans l'écran Nouvelles entrées (vue Doc.comm., en-tête ID de texte dans le schéma de
  textes [50 + ##]), saisissez 100 dans la zone N°, Y001 dans la zone ID et 90## dans la
  zone SéquenceAccès.

f) Sauvegardez le schéma de textes.

g) Revenez à l'écran du Customizing.

4. Affectez le nouveau schéma de textes de l'en-tête du document de vente au type de
document ZA##.
a) Dans l'écran Modifier vue "ID textes en-tête doc. vente ds schéma textes [50+##]" :
  synthèse, dans la structure du dialogue, double-cliquez sur Affectation schéma de
  textes.

b) Dans la ligne contenant le type de document de vente ZA##, saisissez le schéma de
  textes (50 + ##) dans la zone SchTx.

c) Sauvegardez l'affectation du schéma de textes.

d) Revenez à l'écran SAP Easy Access.

Testez le fonctionnement de la nouvelle affectation.

1. Créez une offre de type OF. Utilisez les données de demande d'offre client suivantes :
Zone                                         Valeur
Donneur d'ordre                              C650-B##

Nom                                          M. Smith

N° de demande d'offre                        ##-2-4,1

Fin de validité                              Fin du mois prochain
Article                                      P650-1##

---

## PDF page 114

Chapitre 3: Pilotage de textes

Zone                                            Valeur
Quantité d’ordre                                1

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Offre → Créer.

b) Dans l'écran Créer Offre : écran initial, saisissez OF dans la zone Type d'offre.

c) Appuyez sur Entrée.

d) Saisissez les données du tableau (en-tête).

2. Créez un texte d'en-tête d'offre, par exemple Jusqu'à épuisement du stock.
Toutes les offres sont soumises à une vente préalable.
a) Cliquez sur Afficher détails en-tête doc.

b) Dans l'écran Créer Offre : données d'en-tête, sur la page à onglet Textes, faites défiler
les informations jusqu'à la fin de la liste des types de textes d'en-tête disponibles.

c) Choisissez le type de texte Y001 Texte d'en-tête offre.

d) Saisissez le texte et appuyez sur Entrée.

e) Dans la page à onglet Données commande, saisissez M. Smith dans la zone Nom.

f) Sauvegardez le document et revenez à l'écran SAP Easy Access.

3. Créez une commande client de type ZA## en référence à l'offre (numéro de commande
d'achat ##-2-4.3).
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.

b) Dans l'écran Créer commande client : écran initial, saisissez ZA## dans la zone Type de
commande client.

c) Cliquez sur Créer avec référence.

d) Dans la boîte de dialogue Créer avec référence, page à onglet Offre, saisissez votre
numéro d'offre.

               Remarque :
               Vous pouvez également rechercher votre offre avec le numéro de
               commande d'achat ##-2-4.1.

e) Cliquez sur Copier.

4. Vérifiez que le texte d'en-tête de l'offre a été copié dans la commande. Si nécessaire,
utilisez la fonction d'analyse de la détermination des textes pour corriger les problèmes
éventuels.
a) Dans l'écran Créer cde foire et salon ## : synthèse, sélectionnez Afficher détails en-tête
doc.

b) Dans l'écran Créer cde foire et salon ## : données d'en-tête, sélectionnez la page à
onglet Textes.

---

## PDF page 115

Sujet: Configuration du pilotage de textes

5. Sauvegardez la commande et notez le numéro du document.
a) Sauvegardez la commande.
  Le numéro de commande s'affiche.

b) Notez le numéro du document.

---

## PDF page 116

Chapitre 3: Pilotage de textes

---

## PDF page 117

Chapitre 3
 Exercice 8
Traitement manuel d'un texte

Exemple de gestion
Vous voulez que le système détermine automatiquement le plus grand nombre de textes
possibles dans un document de vente. Cependant, vous avez quelquefois besoin de traiter
manuellement le texte d'un document.
Utilisez le traitement manuel de textes dans les documents commerciaux.

Création d'un élément de texte

1. Créez un élément de texte avec les données suivantes :
Zone                                           Valeur
Nom de texte                                   Z##

ID de texte                                    SDVD

Langue                                         Langue du cours

Saisissez le texte Consultez les analyses des tests dans le dernier
magazine « Motos ».

Création d'une offre de type OF

1. Créez une offre de type OF pour une demande d'offre client.
Saisissez les données suivantes :
Zone                                           Valeur
Donneur d'ordre                                C650-B##

Réf. client                                    ##-3-2

DateLivrSouh.                                  Dans un délai d'une semaine
Article                                        P650-1##

Quantité d’ordre                               1

Nom                                            M. Smith

2. À la fin du texte ADV relatif à l'article, saisissez l'élément de texte que vous avez créé.

3. Sauvegardez l'offre et notez le numéro du document.

---

## PDF page 118

Chapitre 3
Solution 8
Traitement manuel d'un texte

Exemple de gestion
Vous voulez que le système détermine automatiquement le plus grand nombre de textes
possibles dans un document de vente. Cependant, vous avez quelquefois besoin de traiter
manuellement le texte d'un document.
Utilisez le traitement manuel de textes dans les documents commerciaux.

Création d'un élément de texte

1. Créez un élément de texte avec les données suivantes :
Zone                                        Valeur
Nom de texte                                Z##

ID de texte                                 SDVD

Langue                                      Langue du cours

Saisissez le texte Consultez les analyses des tests dans le dernier
magazine « Motos ».
a) Dans l'écran SAP Easy Access, sélectionnez Outils → Impression du
formulaire → SAPscript → Texte standard.

b) Saisissez les données du tableau (en-tête).

c) Cliquez sur Créer.

d) Saisissez le texte.

e) Sauvegardez l'élément de texte.

f) Revenez à l'écran SAP Easy Access.

Création d'une offre de type OF

1. Créez une offre de type OF pour une demande d'offre client.
Saisissez les données suivantes :
Zone                                        Valeur
Donneur d'ordre                             C650-B##

Réf. client                                 ##-3-2

DateLivrSouh.                               Dans un délai d'une semaine
Article                                     P650-1##

---

## PDF page 119

Sujet: Configuration du pilotage de textes

Zone                                              Valeur
Quantité d’ordre                                  1

Nom                                               M. Smith

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Offre → Créer.

b) Sélectionnez OF dans la zone Type d'offre.

c) Saisissez les données du tableau (en-tête).

d) Cliquez sur Afficher détails en-tête doc.

e) Dans l'écran Créer Offre : données d'en-tête, sélectionnez l'onglet Données commande.

f) Dans la page à onglet Données commande, saisissez les données du tableau (zone
   Nom).

g) Appuyez sur Entrée et revenez à l'écran précédent.

2. À la fin du texte ADV relatif à l'article, saisissez l'élément de texte que vous avez créé.
a) Sélectionnez la ligne du poste de commande 10 et cliquez sur Afficher détails du poste.

b) Dans la page à onglet Textes, sélectionnez le type de texte Texte de vente d'article.

c) Sélectionnez Détail.

d) Positionnez le curseur dans une ligne vide à la fin du texte, puis sélectionnez Intégrer
  → Texte → Standard.

                   Remarque :
                   Vous pouvez également accéder à cette fonction en cliquant sur Standard.

e) Saisissez les données suivantes :
    Zone                                              Valeur
    Nom de texte                                      Z##

    ID de texte                                       SDVD

f) Choisissez la langue.

g) Cochez la case Éclater imméd.

h) Cliquez sur Copier.

i) Sauvegardez le texte et revenez à l'écran Créer Offre : synthèse.

3. Sauvegardez l'offre et notez le numéro du document.
a) Sauvegardez l'offre et notez le numéro du document qui s'affiche.

---

## PDF page 120

Chapitre 3: Pilotage de textes

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Configurer le pilotage de textes

---

## PDF page 121

Chapitre 3

Évaluation des connaissances

1. Parmi les propositions suivantes, lesquelles sont correctes ?
Sélectionnez les réponses correctes.

X    A Vous pouvez enregistrer des textes dans les données de base et les copier dans les
    documents commerciaux (SD).

X    B Vous pouvez déterminer les conditions en fonction desquelles les textes doivent
    être copiés.

X    C Vous ne pouvez copier des textes que dans une seule langue.

X    D Vous pouvez copier un texte standard dans un document de vente.

2. Parmi les sources de textes suivantes, auxquelles avez-vous accès dans la fiche article ?
Sélectionnez les réponses correctes.

X    A Notes de marketing

X    B Texte de livraison

X    C Texte ADV

X    D Texte de commande d'achat

3. Parmi les caractéristiques suivantes, lesquelles pouvez-vous spécifier pour les schémas
de textes utilisés pour le pilotage de textes ?
Sélectionnez les réponses correctes.

X    A Si un texte doit être copié ou utilisé en tant que référence

X    B Si un texte doit être déterminé automatiquement

X    C Si un texte doit être créé automatiquement en fonction du type de document

---

## PDF page 122

Chapitre 3: Évaluation des connaissances

4. La copie de textes consomme plus de mémoire que leur utilisation en tant que références.
La fonction de copie ne doit donc être utilisée que si elle est vraiment nécessaire.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

5. Vous utilisez une séquence d'accès pour que le système recherche le schéma de textes
approprié.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

---

## PDF page 123

Chapitre 3

Évaluation des connaissances - Réponses

1. Parmi les propositions suivantes, lesquelles sont correctes ?
Sélectionnez les réponses correctes.

X    A Vous pouvez enregistrer des textes dans les données de base et les copier dans les
    documents commerciaux (SD).

X    B Vous pouvez déterminer les conditions en fonction desquelles les textes doivent
    être copiés.

X    C Vous ne pouvez copier des textes que dans une seule langue.

X    D Vous pouvez copier un texte standard dans un document de vente.

Correct ! Vous pouvez enregistrer des textes de données de base et les copier dans les
documents de vente ; vous pouvez déterminer les conditions en fonction desquelles les
textes sont copiés vers les documents de vente ; et vous pouvez copier un texte standard
dans un document de vente. Les textes peuvent être copiés dans plusieurs langues si
nécessaire. Pour en savoir plus, reportez-vous au sujet Identification des sources de
textes (Chapitre 3, Sujet 1) dans le cours S4650.

2. Parmi les sources de textes suivantes, auxquelles avez-vous accès dans la fiche article ?
Sélectionnez les réponses correctes.

X    A Notes de marketing

X    B Texte de livraison

X    C Texte ADV

X    D Texte de commande d'achat

Correct ! Depuis la fiche article, vous pouvez accéder aux textes ADV ou aux textes de
commande d'achat. Les notes de marketing et les textes de livraison ne sont pas
enregistrés dans la fiche article. Pour en savoir plus, reportez-vous au sujet Identification
des sources de textes (Chapitre 3, Sujet 1) dans le cours S4650.

---

## PDF page 124

Chapitre 3: Évaluation des connaissances - Réponses

3. Parmi les caractéristiques suivantes, lesquelles pouvez-vous spécifier pour les schémas
de textes utilisés pour le pilotage de textes ?
Sélectionnez les réponses correctes.

X    A Si un texte doit être copié ou utilisé en tant que référence

X    B Si un texte doit être déterminé automatiquement

X    C Si un texte doit être créé automatiquement en fonction du type de document

Correct ! Dans les schémas de textes utilisés pour le pilotage de textes, vous pouvez
spécifier si un texte doit être copié ou utilisé en tant que référence et si un texte doit être
déterminé automatiquement. Il n'existe aucune fonctionnalité permettant de créer un
texte automatiquement en fonction du type de document. Pour en savoir plus, reportez-
vous au sujet Configuration du pilotage de textes (Chapitre 3, Sujet 2) dans le cours
S4650.

4. La copie de textes consomme plus de mémoire que leur utilisation en tant que références.
La fonction de copie ne doit donc être utilisée que si elle est vraiment nécessaire.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! D'un point de vue technique, il est plus judicieux d'utiliser un texte en tant que
référence plutôt que de le copier, car cela nécessite moins de ressources informatiques.
Pour en savoir plus, reportez-vous au sujet Configuration du pilotage de textes
(Chapitre 3, Sujet 2) dans le cours S4650.

5. Vous utilisez une séquence d'accès pour que le système recherche le schéma de textes
approprié.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! Une séquence d'accès permet de rechercher une table de conditions appropriée.
Une séquence d'accès ne recherche pas un schéma de textes. Pour en savoir plus,
reportez-vous au sujet Configuration du pilotage de textes (Chapitre 3, Sujet 2) dans le
cours S4650.

---

## PDF page 125

CHAPITRE 4                             Messages

Sujet 1
Ajustement de la détermination des messages                                                     118
Exercice 9: Ajustement de la détermination des messages                              129

Sujet 2
Ajustement des catégories de messages                                                           140
Exercice 10: Ajustement et traitement d'une catégorie de message                      151

Sujet 3
Nouvelle fonctionnalité de gestion des messages                                                 159
Exercice 11: Création d'une catégorie de message pour la confirmation de commande   169

OBJECTIFS DU CHAPITRE

●   Ajuster la détermination des messages
●   Ajuster les catégories de messages
●   Décrire la nouvelle fonctionnalité de gestion des messages

---

## PDF page 126

Chapitre 4
   Sujet 1
Ajustement de la détermination des messages

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment ajuster la détermination des messages dans l'Administration des
ventes (SD).

Focus is on creating access sequence Z001 for the BA00 output type to enable customer-
specific condition records to be created, for the transmission medium fax.

Exemple de gestion
Afin de répondre aux besoins de différents clients, vous devez définir des conditions pour que
le système détermine si un message doit être généré, son destinataire et le support à utiliser.
Pour cette raison, vous devez disposer des connaissances suivantes :
●    Compréhension de l'objectif des catégories de messages
●    Comment définir différents supports pour l'édition ou l'impression des messages
●    Comment sélectionner les dates/heures de l'envoi des messages
●    Comment ajuster la détermination des messages aux besoins propres au client

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●    Ajuster la détermination des messages

---

## PDF page 127

Sujet: Ajustement de la détermination des messages

Catégories de messages

 Figure 32: Catégories de messages dans SD

Dans le système SAP, les messages servent de moyens de communication, notamment avec
le client. Vous pouvez générer un message relatif à différentes catégories de documents de
vente comme les offres, les commandes clients, les livraisons ou les factures.
Vous pouvez utiliser la technique de conditions si vous voulez que la détermination des
messages dépende de différents critères. Les informations ayant des incidences sur la
détermination des messages (par exemple, le choix du moment de l'édition des messages ou
des supports) sont stockées comme données de base sous la forme d'enregistrements de
conditions de messages.
Il existe une différence entre les messages d'en-tête et les messages de poste. Avec un
message d'en-tête, c'est l'ensemble du document qui est édité. Un message de poste permet
quant à lui d'éditer chaque poste du document séparément.

---

## PDF page 128

Chapitre 4: Messages

Traitement des messages

Figure 33: Supports

Le support détermine le mode d'édition du message. Par exemple, vous pouvez convenir
d'envoyer une confirmation de commande à votre client via échange de données informatisé
(EDI) ou d'envoyer une notification au préalable par le biais d'Internet.
Le programme de traitement approprié contrôle le traitement du message, c'est-à-dire le
transfert des informations. Vous pouvez affecter un programme et les mises en forme
correspondantes à chaque catégorie de message et à chaque support.

---

## PDF page 129

Sujet: Ajustement de la détermination des messages

Stratégie de communication

 Figure 34: Stratégie de communication

Une stratégie de communication est une séquence de types de communication.
Vous pouvez utiliser une stratégie de communication pour une transmission externe. La
stratégie de communication est utilisée pour parcourir la séquence des catégories de
communication données pour rechercher les données de communication correspondant à
l'adresse souhaitée qui est reprise du fichier d'adresses central.
Vous pouvez définir la stratégie de communication en utilisant les données supplémentaires
liées à l'enregistrement de conditions des messages.

---

## PDF page 130

Chapitre 4: Messages

Moment de l'édition des messages

Figure 35: Moment de l'édition des messages

Vous pouvez décider du moment où un message doit être édité.

Les moments disponibles pour l'édition de messages sont les suivants :
●  Un programme standard (RSNAST00) défini pour s'exécuter à des intervalles réguliers
sélectionne le message à envoyer. Vous pouvez ainsi spécifier si ce message doit être
sélectionné à la prochaine exécution du programme (moment de la transmission 1) ou à un
moment défini par l'utilisateur (moment de transmission 2).
●   Un programme de sélection spécial, conçu pour les différents documents de vente (par
exemple, les documents de facturation et de livraison), traite les messages en ligne ou par
lots (moment de transmission 3). Vous pouvez programmer un lot pour assurer ainsi un
traitement régulier (cf. moment 1).
●   Le système édite automatiquement le message dès l'enregistrement du document
(moment de transmission 4).

---

## PDF page 131

Sujet: Ajustement de la détermination des messages

Détermination des messages

 Figure 36: Vue d'ensemble de la détermination des messages

Tout comme pour la détermination du prix et du texte, le système peut utiliser la technique de
conditions pour la détermination des messages. L'enregistrement de conditions d'une
catégorie de message contient les propriétés (par exemple, les supports, le moment de
l'édition des messages ou la langue) de cette catégorie pour un contexte donné. Si les
conditions spécifiées sont remplies, cette catégorie de message est proposée dans le
document avec les propriétés définies.
C'est dans l'enregistrement de conditions que vous indiquez le support, la date/heure de
l'envoi et le rôle partenaire. Le message est envoyé au partenaire dont le rôle correspond à
celui défini dans l'objet sous-jacent (par exemple, la commande client). Il est également
possible de créer des messages ne dépendant d'aucun partenaire (par exemple, des
étiquettes).
Utilisez la fonction d'analyse de l'écran des messages dans les documents de vente afin de
vérifier la détermination de ces messages et de comprendre pourquoi le système a proposé
un message donné ou pourquoi il n'a pas été déterminé.

---

## PDF page 132

Chapitre 4: Messages

Détermination des messages - séquences d'accès

Figure 37: Détermination des messages - séquences d'accès

Une séquence d'accès est une stratégie de recherche utilisée par le système SAP pour
rechercher des enregistrements de conditions de messages valables. Chaque étape d'accès
comprend le nom d'une table de conditions comprenant elle-même les zones clés de ces
enregistrements.
La règle qui régit la séquence de recherche stipule que le système doit effectuer ses
recherches « du particulier au général ».
Pour créer une séquence d'accès, vous pouvez copier une séquence similaire existante et
apporter les modifications nécessaires à la séquence copiée. Si vous définissez vos propres
séquences d'accès, les clés que vous créez doivent commencer par Y ou Z, ces espaces noms
étant réservés à cet effet dans la version standard du système.

---

## PDF page 133

Sujet: Ajustement de la détermination des messages

Détermination des messages - analyse

   Figure 38: Détermination des messages - analyse

Vous pouvez utiliser la fonction d'analyse de la détermination des messages dans les écrans
de document de vente avec les fonctions Créer ou Modifier.
Pour utiliser la fonction d'analyse de la détermination des messages, sélectionnez Autres
fonctions → Messages → En-tête (ou poste) → Traiter. Sélectionnez ensuite Saut → Analyse
de détermination.

Comment configurer la détermination des messages
Show how output is determined using the sales document type OR as an example.

        Remarque :
        In this demonstration, you set up a field relationship that is required for one or
        more subsequent demonstrations in the course.

1. Check that New Output Management is inactive.
a) In Customizing for Cross-Application Components, choose Output Control → Manage
  Application Object Type Activation.

b) For the application type SALES_DOCUMENT, the Status field should be set to
  Application inactive.

2. Display the following:

●    Procedure V10000

●    Output type BA00

●    Access sequence Z001 (order type)

---

## PDF page 134

Chapitre 4: Messages

a) In Customizing for Sales and Distribution, choose Basic Functions → Output
Determination → Output Determination → Output Determination Using the Condition
Technique → Maintain Output Determination for Sales Documents → Maintain Output
Determination Procedure.

b) To display procedure V10000, on the Change View “Procedures”: Overview screen,
select the row of procedure V10000 and double-click Control Data.

c) Return to the Customizing menu and choose Assign Output Determination Procedures.
In the Select Activity dialog box, choose Allocate sales document header.

d) Show how sales document type ZA00 is assigned to output determination procedure
V10000.

e) Return to the Customizing menu and choose Maintain Output Types.

f) To display output type BA00, on the Display View “Output Types”: Overview screen,
select the row of output type BA00 and choose Details.

g) Return to the Customizing menu and choose Maintain Access Sequences.

h) Confirm the information dialog box that appears.

i) To display access sequence Z001, on the Change View “Access Sequences”: Overview
screen, select the row of access sequence Z001 and double-click Accesses.

3. Create a condition record for customer C650-A00 with fax as the medium.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Master
Data → Output → Sales Document → Create.

b) On the Create Output — Condition Records: Sales screen, enter output type BA00 and
choose Key combination.

c) In the Key Combination window, select the Sales Organization/Customer Number radio
button and choose Choose.

d) On the Create Condition Records (Order Confirmation): Fast Entry screeen, enter a new
line with customer C650-A00 and medium 2 (fax), and choose Enter.

e) Save your data.

4. Create an order and show the determination analysis.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution
→ Sales → Order → Create.

b) Enter an order type of ZA00, a distribution channel of 10, and a division of 00 and
choose Enter.

c) On the Create Trade Fair01-Order: Overview screen, enter a sold-to party of C650-A00
and a PO number of OP01.

d) Enter material P650-100 with an order quantity of 1 and choose Enter.

e) Choose Extras → Output → Header → Edit.

f) On the Create Trade Fair01-Order: Output screen, choose Goto → Determin.analysis.
On the Analysis Output screen, demonstrate that the output was not determined since
the fax number for the customer C650-A00 is not found.

---

## PDF page 135

Sujet: Ajustement de la détermination des messages

g) Return to the SAP Easy Access screen, but do not save your data when prompted.

5. On the Address tab page, enter the fax number 1234567 in the customer master of
customer C650-A00.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Master
  Data → Business Partner → Customer → Change → Sales and Distribution.

b) In the Customer Change: Initial Screen dialog box, choose Continue.

c) On the Change Organization: C650-A00, role Customer screen, choose the General
  Data button.

d) On the Change Organization: C650-A00, role Customer screen, in the Address tab
  page, scroll down to the Communication screen area.

e) Enter fax number 1234567 and save your data.

f) On the Change Organization: C650-A00, role Customer screen, choose Cancel.

6. Create the order and check the output.
a) On the SAP Easy Access screen, choose Logistics → Sales and
  Distribution → Sales → Order → Create.

b) Enter an order type of ZA00, a distribution channel of 10, and a division of 00 and
  choose Enter.

c) On the Create Trade Fair01-Order: Overview screen, enter a sold-to party of C650-A00
  and a PO number of OP01.

d) Enter material P650-100 with an order quantity of 1 and choose Enter.

e) Choose Extras → Output → Header → Edit.

f) On the Create Trade Fair01-Order: Output screen, choose Goto → Determin.analysis.
   On the Analysis Output screen, demonstrate that the output is determined since a valid
   fax number is found for the customer C650-A00.

g) Return to the Create Trade Fair01-Order: Overview screen and choose Header output
  preview.
  The print preview is displayed.

h) Return to the Create Trade Fair01-Order: Overview screen and save your data.

---

## PDF page 136

Chapitre 4: Messages

---

## PDF page 137

Chapitre 4
 Exercice 9
Ajustement de la détermination des messages

Exemple de gestion
Alors que dans votre entreprise les confirmations de commande (accusés de réception) sont
généralement imprimées, vos clients préfèrent souvent les recevoir par télécopie. Vous avez
besoin que le système sélectionne automatiquement la télécopie lors de la détermination du
support pour ces clients.
Ajustez la détermination des messages.
Vérifiez que la nouvelle gestion des messages n'est pas activée.

1. Dans le Customizing pour Composantes inter-applications sélectionnez Pilotage des
sorties → Gérer l'activation du type d'objet d'application.

2. Pour le type d'application SALES_DOCUMENT, la zone Statut doit être définie sur
Application inactive.

Identification de la détermination des messages

1. Identifiez le schéma de détermination des messages affecté à l'en-tête du document de
vente pour le type de commande ZA##.

Envoi de la confirmation de commande par télécopie
Le client C650-A## vous demande d'envoyer la confirmation de commande par télécopie.
Configurez le message.

1. Vérifiez les options de la détermination des messages pour savoir si le système SAP vous
autorise à mémoriser cette demande client dans les données de base.

2. Dans quelles combinaisons de zones clés les enregistrements de catégorie de message
BA00 peuvent-ils être dépendants ?

3. Créez un enregistrement de conditions de messages pour le client C650-A## avec la
catégorie de message BA00. Utilisez les données du tableau suivant :
Zone                                        Valeur
Organis. commerciale                        1010

Support                                     Télécopie

Date/heure                                  Envoi via transaction spécifique
                                            à l'application

---

## PDF page 138

Chapitre 4: Messages

Test de la configuration des messages

1. Créez une commande de type ZA## pour une commande d'achat reçue de la part d'un
client. Utilisez les données du tableau suivant :
Zone                                         Valeur
Donneur d'ordre                              C650-A##

Réf. client                                  ##-1-3

DateLivrSouh.                                Dans une semaine
Article                                      P650-1##

Quantité d’ordre                             10

2. Vérifiez si la détermination des messages donne le résultat escompté. Si nécessaire,
utilisez la fonction d'analyse pour localiser les problèmes éventuels.

3. Quel est le problème détecté par l'analyse de la détermination ?

4. Arrêtez la saisie de la commande.

5. Saisissez le numéro de télécopie 123456789 dans la fiche du client C650-A##.

6. Réessayez de créer une commande client à l'aide des données de l'étape 1.

7. Vérifiez si le message est généré.

---

## PDF page 139

Chapitre 4
 Solution 9
Ajustement de la détermination des messages

Exemple de gestion
Alors que dans votre entreprise les confirmations de commande (accusés de réception) sont
généralement imprimées, vos clients préfèrent souvent les recevoir par télécopie. Vous avez
besoin que le système sélectionne automatiquement la télécopie lors de la détermination du
support pour ces clients.
Ajustez la détermination des messages.
Vérifiez que la nouvelle gestion des messages n'est pas activée.

1. Dans le Customizing pour Composantes inter-applications sélectionnez Pilotage des
sorties → Gérer l'activation du type d'objet d'application.

2. Pour le type d'application SALES_DOCUMENT, la zone Statut doit être définie sur
Application inactive.

Identification de la détermination des messages

1. Identifiez le schéma de détermination des messages affecté à l'en-tête du document de
vente pour le type de commande ZA##.
a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez Fonctions de
  base → Pilotage des messages (NAST) → Détermination des
  messages → Détermination des messages via technique de conditions → Gérer la dét.
  des messages pour les documents de vte → Affecter schéma de détermination des
  messages.

b) Dans la boîte de dialogue Sélection de l'activité, double-cliquez sur Affecter l'en-tête de
  document de vente.

c) Cliquez sur Positionner.

d) Dans la boîte de dialogue Autre entrée, saisissez ZA## dans la zone Type doc. vente.

e) Cliquez sur Reprendre.
  Le schéma de détermination des messages V10000 est affecté pour le type de
  commande ZA##.

f) Revenez à l'écran Afficher guide d'implémentation.

Envoi de la confirmation de commande par télécopie
Le client C650-A## vous demande d'envoyer la confirmation de commande par télécopie.
Configurez le message.

1. Vérifiez les options de la détermination des messages pour savoir si le système SAP vous
autorise à mémoriser cette demande client dans les données de base.

---

## PDF page 140

Chapitre 4: Messages

a) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez Fonctions de
base → Pilotage des messages (NAST) → Détermination des
messages → Détermination des messages via technique de conditions → Gérer la dét.
des messages pour les documents de vte → Gérer les catégories de message.

b) Dans l'écran Afficher vue "Catégories de message" : synthèse, sélectionnez la ligne
contenant la catégorie de message BA00.

c) Sélectionnez Détail.
L'entrée Z001 est affectée comme séquence d'accès.

d) Revenez à l'écran Afficher guide d'implémentation.

e) Dans le Customizing de l'Administration des ventes (ADV), sélectionnez Fonctions de
base → Pilotage des messages (NAST) → Détermination des
messages → Détermination des messages via technique de conditions → Gérer les
séquences d'accès.

f) Sélectionnez la ligne contenant la séquence d'accès Z001.

         Remarque :
         Si une boîte de dialogue d'avertissement s'affiche, cliquez sur Suite.

g) Dans la structure du dialogue, sélectionnez Accès.

h) Dans l'écran Modifier vue "Accès" : synthèse, notez les valeurs des zones Z001.

2. Dans quelles combinaisons de zones clés les enregistrements de catégorie de message
BA00 peuvent-ils être dépendants ?

La catégorie de message BA00 peut dépendre des combinaisons de zones clés
Organisation commerciale/Canal de distribution/Secteur d'activité/Client, Organisation
commerciale/Client ou Type de commande client.

a) Pour répondre à la question, utilisez les valeurs des zones de l'écran Modifier vue
« Accès » : synthèse.

b) Revenez à l'écran SAP Easy Access.

3. Créez un enregistrement de conditions de messages pour le client C650-A## avec la
catégorie de message BA00. Utilisez les données du tableau suivant :
Zone                                          Valeur
Organis. commerciale                          1010

Support                                       Télécopie

Date/heure                                    Envoi via transaction spécifique
                                          à l'application

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Données de base → Sortie → Document de vente → Créer.

---

## PDF page 141

Sujet: Ajustement de la détermination des messages

b) Dans l'écran Créer enregistrements condition des messages : Vente, saisissez BA00
  dans la zone Catégorie de message.

c) Cliquez sur Combinaison-clé.

d) Dans la boîte de dialogue Combinaison-clé, cochez la case d'option Organisation
  commerciale/N° client et cliquez sur Sélectionner.

e) Dans l'écran Créer enregistrements condition (Confirmation ordre) : saisie rapide, dans
  la zone Client, saisissez C650-A##.

f) Sélectionnez la zone TypSupport et cliquez sur le bouton d'aide à la saisie.

g) Dans la boîte de dialogue Support du message - X Entrées trouvées, sélectionnez
  l'entrée Télécopie et cliquez sur Reprendre.

h) Dans l'écran Créer enregistrements condition (Confirmation ordre) : saisie rapide,
  sélectionnez la zone Date/heure et cliquez sur le bouton d'aide à la saisie.

i) Dans la boîte de dialogue Date/heure de l'envoi - X Entrées trouvées, sélectionnez
   l'entrée 3 et cliquez sur Reprendre.

j) Dans l'écran Créer enregistrements condition (Confirmation ordre) : saisie rapide,
   appuyez sur Entrée.

k) Sauvegardez vos données.
  Un enregistrement de conditions de messages est créé.

l) Revenez à l'écran SAP Easy Access.

Test de la configuration des messages

1. Créez une commande de type ZA## pour une commande d'achat reçue de la part d'un
client. Utilisez les données du tableau suivant :
Zone                                          Valeur
Donneur d'ordre                               C650-A##

Réf. client                                   ##-1-3

DateLivrSouh.                                 Dans une semaine
Article                                       P650-1##

Quantité d’ordre                              10

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Commande client → Créer.

b) Dans l'écran Créer commande client : écran initial, saisissez ZA## dans la zone Type de
  commande client et cliquez sur Entrée.

c) Dans l'écran Créer cde foire et salon ## : synthèse, saisissez les données indiquées
  dans le tableau.

d) Sauvegardez vos données.

2. Vérifiez si la détermination des messages donne le résultat escompté. Si nécessaire,
utilisez la fonction d'analyse pour localiser les problèmes éventuels.

---

## PDF page 142

Chapitre 4: Messages

a) Sélectionnez Autres fonctions → Messages → En-tête → Traiter.

b) Sélectionnez Saut → Analyse de détermination.

3. Quel est le problème détecté par l'analyse de la détermination ?

Le système n'a pas pu déterminer de numéro de télécopie pour le partenaire C650-A##.

4. Arrêtez la saisie de la commande.
a) Quittez la page de saisie de commande. Ne sauvegardez pas vos données.

5. Saisissez le numéro de télécopie 123456789 dans la fiche du client C650-A##.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Données de base → Partenaire → Client → Modifier → Administration des
ventes (ADV).

b) Dans la boîte de dialogue Client Modifier : écran initial, sélectionnez Suite.

c) Dans l'écran Modifier Client : donn. générales, sur la page à onglet Adresse, faites
défiler les informations vers le bas jusqu'à ce que la zone d'écran Communication soit
visible.

d) Saisissez 123456789 dans la zone Télécopie.

e) Sauvegardez vos données.

f) Revenez à l'écran SAP Easy Access.

6. Réessayez de créer une commande client à l'aide des données de l'étape 1.

7. Vérifiez si le message est généré.

---

## PDF page 143

Sujet: Ajustement de la détermination des messages

Formulaires basés sur le format PDF

 Figure 39: Confirmation de commande : SAPscript et PDF

Dans Form Builder, des formulaires basés sur le format PDF sont définis pour le processus
des ventes. Ils peuvent remplacer les formulaires SAPscript utilisés jusqu'à présent.

Les conditions préalables techniques pour les formulaires basés sur le format PDF sont
les suivantes :
●  SAP ERP 6.0 enhancement package 2 est installé
●   La fonction spécialisée SD_01 doit être active (transaction SFW5)

Les formulaires suivants sont disponibles dans Form Builder :
●  Confirmation de commande (SD_SDOC_FORM01)
●   Facture/document de facturation (SD_INVOICE_FORM01)
●   Liste de factures (SD_BIL_LIST_FORM01)
●   Contact client (SD_CAS_FORM01)
●   Formulaire d'impression pour les informations client (SD_CFS_FORM01)
●   Exemple de publipostage pour les contacts client (SD_CAS_MAIL_FORM01)

Les formulaires basés sur le format PDF sont définis dans Form Builder. Pour accéder à Form
Builder, sur l'écran SAP Easy Access, sélectionnez Outils → Impression de
formulaire → Formulaires interactifs (transaction SFP).
Les clients peuvent utiliser ces formulaires pour configurer leurs propres formulaires.

---

## PDF page 144

Chapitre 4: Messages

Ces formulaires sont affectés à la catégorie de message, comme tous les autres formulaires.
Pour la confirmation de commande SD_SDOC_FORM01, le programme de traitement
approprié est SD_SDOC_PRINT01.

Informations liées
Voir http://help.sap.com.
Pour consulter la documentation dans l'aide en ligne SAP, recherchez SAP Interactive Forms
by Adobe et sélectionnez PDF-based Print Forms.

Comment utiliser des formulaires basés sur le format PDF

     Remarque :
     This is an optional demonstration. If you have already demonstrated the use of
     printed output, there is no need to present this demonstration. However, if your
     demonstration was based purely on the exercise (using fax output), then this
     further demonstration is worth showing.

1. Ensure the following values are assigned to output type BA00, transmission medium 1:
Field                                           Value
Transmission medium                             Print output

Program                                         SD_SDOC_PRINT01

Form routine                                    ENTRY

PDF/SmartForm form                              SD_SDOC_FORM01

Type                                            PDF

a) In Customizing for Sales and Distribution, choose Basic Functions → Output
Determination → Output Determination → Output Determination Using the Condition
Technique → Maintain Output Determination for Sales Documents → Maintain Output
Types.

b) On the Display View "Output Types": Overview screen, enter change mode by choosing
Display → Change.

c) Select the row of output type BA00 and double-click Processing routines.

d) In the row for the transmission medium Print output, ensure that the values in the
above table are entered. Enter them if required, and save your changes.

e) Return to the SAP Easy Access screen.

2. Return to the output condition record created in the previous demonstration and change
the medium from fax (2) to print output (1).
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Master
Data → Output → Sales Document → Change.

---

## PDF page 145

Sujet: Ajustement de la détermination des messages

b) On the Change Output - Condition Records: Sales screen, enter the output type BA00
  and choose Key combination.

c) In the Key Combination window, select the Sales Organization/Customer Number radio
  button and choose Choose.

d) On the Change Order Confirmation (BA00): Selection screen, enter sales organization
  1010 and customer C650-A00. Choose Execute.

e) On the Change Condition Records (Order Confirmation): Fast Change screen, change
  the medium to 1 (Print output). Choose Communication.

f) On the Change Condition Records (Order Confirmation): Communication screen, enter
   an output device of LP01.

g) Save your data.

3. Create an order.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution →
  Sales → Order → Create.

b) On the Create Sales Order: Initial Screen, enter an order type of OR and choose Enter.

c) On the Create Standard Order: Overview screen, enter a sold-to party of C650-A00 and
  a PO number of PDF.

d) Enter material P650-100 with an order quantity of 1 and choose Enter.

e) Choose Extras → Output → Header → Edit.

f) On the Create Standard Order: Output screen, show that the output condition record
   has been found.

g) Return to the Create Standard Order: Overview screen.

h) Choose Header output preview.

i) Return to the Create Standard Order: Overview screen and save your data.

Analyse des erreurs pour les problèmes liés au traitement des formulaires PDF
This demonstration helps to find out solution with printing PDF Forms

1. Use transaction SA38 to execute the program FP_PDF_TEST_00. This enables you to
check the RFC connection to ADS ( Adobe Document Services).
a) Run transaction SA38. Enter the program name FP_PDF_TEST_00 and choose
  Execute.

b) Select the connection ( Usually ADS ) and choose Execute.

c) If the system displays the version number ADS, the configuration of the RFC
  connection to ADS is correct.

2. 2. Run the program FP_TEST_00.
a) Run transaction SA38. Enter the program name FP_TEST_00 and choose Execute.

---

## PDF page 146

Chapitre 4: Messages

b) Don’t change fields on the next screen and choose Execute.

c) Set LP01 as the Output device and choose the Print Preview button.

d) If the FP_TEST_00 form is displayed in the print preview, the ADS configuration is
correct, and the printer supports PDF forms.

e) If the system displays an error message instead of form, the configuration of ADS is
incorrect

---

## PDF page 147

Sujet: Ajustement de la détermination des messages

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Ajuster la détermination des messages

---

## PDF page 148

Chapitre 4
    Sujet 2
Ajustement des catégories de messages

VUE D'ENSEMBLE DU SUJET
Ce sujet décrit les principes de base du traitement des imprimés avec des formulaires basés
sur le format PDF.

The focus of this lesson is to discuss the introduction and modification of outputs in an SAP
S/4HANA system.

Exemple de gestion
Modifier les catégories de messages et satisfaire ainsi les besoins du client est une tâche
essentielle rencontrée dans la majorité des projets d'implémentation. Ces modifications
comprennent l'ajout de zones supplémentaires, de logos et de codes barres ainsi que
l'affichage de textes supplémentaires d'en-tête et de poste. Le client peut également vous
demander d'ajouter de nouvelles catégories de messages spécifiques. Pour cette raison, vous
devez disposer des connaissances suivantes :
●    Compréhension du mode de traitement des catégories de messages dans le système SAP
●    Compréhension du degré de difficulté de l'ajustement de la mise en forme des catégories
de messages
●    Compréhension des étapes nécessaires à l'intégration des catégories de messages
propres au client

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●    Ajuster les catégories de messages

---

## PDF page 149

Sujet: Ajustement des catégories de messages

Extraction et préparation des données

 Figure 40: Extraction et préparation des données

Une base de données stocke la structure et les données des documents qui sont traités en
ligne. Pour transmettre des messages, le système collecte les données nécessaires de cette
base de données et les met en forme en fonction du support demandé.

Impression des données

 Figure 41: Impression des données

Le système extrait et prépare les données en deux étapes distinctes avant d'imprimer les
documents. Les paramètres d'impression sont d'abord définis dans le formulaire basé sur le
format PDF, indépendamment du programme d'édition. Le système envoie ensuite les
messages vers une imprimante ou toute autre unité de sortie.

---

## PDF page 150

Chapitre 4: Messages

Exemple : message BA00 (confirmation de commande)

Figure 42: Exemple : message BA00 (confirmation de commande)

Nouvelles zones pour l'impression des documents

Figure 43: Nouvelles zones pour l'impression des documents : cas 1

---

## PDF page 151

Sujet: Ajustement des catégories de messages

Les modifications des catégories de messages peuvent fournir des zones, des logos et des
codes barres supplémentaires ainsi que l'affichage de textes supplémentaires d'en-tête et de
poste.
Vous pouvez traiter directement dans le PDF ou le formulaire SAPscript les modifications
simples ne nécessitant ni logique de préparation ni nouvelles zones dans la structure de
communication.

Une modification de formulaire est simple si elle remplit les conditions préalables
suivantes :
●  La zone existe déjà dans la structure de communication.
●   La zone ne figure pas déjà dans le formulaire.
●   La zone peut être intégrée au formulaire sous sa forme actuelle.

Nouvelles zones pour l'impression des documents : cas 2

 Figure 44: Nouvelles zones pour l'impression des documents : cas 2

Vous pouvez implémenter la logique utilisée pour renseigner les zones supplémentaires à
l'aide d'un BAdI standard. Les nouvelles zones pour l'impression des documents sont copiées
dans les programmes INCLUDE suivants (structures intégrées à la structure de
communication) :
●   Données d'en-tête des documents de commande dans VBDKAZ (figurant dans VBDKA)
●   Données de poste des documents de commande dans VBDPAZ (figurant dans VBDPA)
●   Données d'en-tête des documents de livraison dans VBDKLZ (figurant dans VBDKL)
●   Données de poste des documents de livraison dans VBDPLZ (figurant dans VBDPL)
●   Données d'en-tête des documents de facturation dans VBDKRZ (figurant dans VBDKR)
●   Données de poste des documents de facturation dans VBDPRZ (figurant dans VBDPR)

---

## PDF page 152

Chapitre 4: Messages

Vous pouvez maintenant traiter la nouvelle zone du formulaire en suivant la procédure décrite
dans le cas 1. Le système doit parfois accéder au programme de traitement (par exemple,
pour lire des données supplémentaires).

Comment ajouter des zones dans un formulaire PDF

This is an optional demonstration. It is suggested this only be shown if the course attendees
express specific interest in the editing of PDF-based forms.

Business Example
You need to add new fields in the PDF Print form at the header level.

1. Open transaction SFP.

2. Enter SD_SDOC_FORM01 into the Form field and choose Display

3. Go to the Properties tab and double-click on the Interface field (with value
SDOC_INTERFACE)

4. Expand the structure on the left side and select SDOC_INTERFACE Form interface.

5. Double click on the SDOC_S_PRT_INTERFACE type name on the right side.

6. In the Dictionary: Display Structure screen, double click on the component type
SDOC_S_PRT_HEAD.

7. In the Dictionary: Display Structure screen, double-click on the VBDKA component.

8. Scroll down to VBDKAZ component type. Double click on this component type.

9. Press the Change button.

10. Add the necessary fields into the VBDKAZ structure, for example:

Component                                      Component type
ZZDESCRIPTION                                  TEXT40

11. Choose the Activate button.

12. Return to the SFP transaction . Go to the Context tab. Expand the structures on the left
side: SDOC_INTERFACE Import SLS_PRT_COM HEAD_DETAIL VBDKA

13. Drag the ZZDESCRIPTION field to the corresponding structure on the right side. Now this
new field ZZDESCRIPTION in available in the PDF Template form .

---

## PDF page 153

Sujet: Ajustement des catégories de messages

Intégration d'une nouvelle catégorie de message

 Figure 45: Intégration d'une nouvelle catégorie de message

Les nouvelles catégories de messages se basent, en règle générale, sur des types de
document existants. Si vous avez besoin de créer des nouvelles données de document, vous
pouvez donc copier la plupart de ces données à partir d'une structure de communication
existante.
Lors de l'écriture du programme de traitement et de sa définition de formulaires, vous avez
besoin d'un programmateur ABAP et d'une personne qui sait utiliser les formulaires PDF ou
SAPscript.

---

## PDF page 154

Chapitre 4: Messages

Exemple - Bon de livraison spécial ZLD0

Figure 46: Exemple - Bon de livraison spécial ZLD0

Il est indispensable d'écrire un programme de traitement pour extraire les données de
transmission et pour le paramétrage de l'édition de formulaire. Vous devez lui attribuer un
nom compris dans l'intervalle de noms du client (par exemple, ZRELE_DELNOTE). Ce
programme doit être basé sur les structures de communication spécifiées, à savoir VBDKL
(vue d'en-tête du document pour les bons de livraison) et VBDPL (vue de poste du document
pour les bons de livraison).
Le programme de traitement ainsi que le formulaire SAPscript correspondant dans lequel a
été programmée la mise en forme requise (portant par exemple le nom LE_SHP_DELNOTE),
sont affectés à la catégorie de message ZLD0 dans le Customizing. Si vous voulez que le
système tienne compte de la catégorie ZLD0 lors de la détermination des messages, vous
devez l'ajouter au schéma de détermination des messages portant sur les livraisons.

Comment inclure un nouveau message
Include a new output.
It has been decided to introduce a new special delivery note (output type ZLD0).

1. Show the assignment of the output determination procedure to the delivery type.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
Functions → Output Control → Output Determination → Maintain Output
Determination for Outbound Deliveries → Assign Output Determination Procedures.

b) In the Select Activity window, select the Assign deliveries (header) option and choose
Choose.

---

## PDF page 155

Sujet: Ajustement des catégories de messages

c) Choose Position.

d) In the Another entry dialog box, enter LF in the Delivery Type field.

e) Choose Continue.
  On the Change View “Delivery Types Output Determination Procedure”: Overview
  screen, it can be seen that the delivery type LF is assigned to the output determination
  procedure V10000.

f) Return to the Customizing screen.

2. Show the content of the output determination procedure V10000.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
  Functions → Output Control → Output Determination → Maintain Output
  Determination for Outbound Deliveries → Maintain Output Determination Procedure.

b) On the Change View “Procedures”: Overview screen, select the row containing the
  entry V10000.

c) In the dialog structure, double-click Control Data.
  On the Change View “Control Data”: Overview screen, it can be seen that output type
  ZLD0 is included as step 50.

d) Return to the Customizing screen.

3. Show output type ZLD0.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
  Functions → Output Control → Output Determination → Maintain Output
  Determination for Outbound Deliveries → Maintain Output Types.

b) On the Display View “Output Types”: Overview screen, choose Position.

c) In the Another entry dialog box, enter ZLD0 in the Output Type field.

d) Choose Continue.

e) On the Display View “Output Types”: Overview screen, select the row containing the
  entry ZLD0 and choose Details.
  Here it can be seen that the access sequence 0005 is assigned to the output type
  ZLD0.

f) In the dialog structure, double-click Processing routines.
   On the Display View “Processing Routines”: Overview screen, it can be seen that for the
   Print output transmission medium, the following details apply:

    Field                                       Value
    Processing Program                          RLE_DELNOTE
    PDF/SmartForm                               LE_SHP_DELNOTE

g) Return to the Customizing screen.

4. Show access sequence 0005.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
  Functions → Output Control → Output Determination → Maintain Output
  Determination for Outbound Deliveries → Maintain Access Sequences.

---

## PDF page 156

Chapitre 4: Messages

b) Confirm the Information dialog box that appears.

c) On the Change View “Access Sequences”: Overview screen, select the row containing
the entry 0005.

d) In the dialog structure, double-click Accesses.
On the Change View “Accesses”: Overview screen, it can be seen there is a single
access based on the Sales Organization and Customer Number fields.

e) On the Change View “Accesses”: Overview screen, select the single access.

f) In the dialog structure, double-click Fields.
On the Change View “Fields”: Overview screen, it can be seen that the combination of
fields is based on condition table 001.

g) Return to the Customizing screen.

5. Show condition table 001.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
Functions → Output Control → Output Determination → Maintain Output
Determination for Outbound Deliveries → Maintain Condition Tables.

b) In the Select Activity window, select the Maintain output condition table for deliveries
option and choose Choose.

c) On the Change Condition Table (Output Shipping) screen, choose the Condition menu.

d) Choose Display.

e) On the Display Condition Table (Output Shipping) screen, enter 001 in the Table field.

f) Choose Enter.
On the Display Condition Table (Output Shipping): Field Overview screen, the Sales
Organization and Customer fields can be seen as the contents of Table 001 on the left-
hand side of the screen.

g) Return to the Customizing screen.

6. Show the definition of the print parameters for shipping point 1010.
a) In Customizing for Logistics Execution, choose Shipping → Basic Shipping
Functions → Output Control → Define print parameters shipping.

b) On the Print Parameters screen, choose Shipping (V2) → Delivery Note Spec. (ZLD0).

c) On the Change View “Print Parameters for Shipping Point”: Overview screen, it can be
seen there is an entry for shipping point 1010 to use output device LP01.

d) Return to the SAP Easy Access screen.

7. Create an output condition record for customer C650-A00 for output type ZLD0.
Use the following details:
Field                                         Value
Sales/Organization                            1010

Medium                                        1 (Print output)

---

## PDF page 157

Sujet: Ajustement des catégories de messages

Field                                       Value
Date/Time                                   3 (Send with application’s own
                                            transaction)

a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Master
  Data → Output → Shipping → Create.

b) On the Create Output – Condition Records: Shipping screen, enter ZLD0 in the Output
  Type field.

c) Choose Key combination.

d) In the Key Combination dialog box, select the Sales Organization/Customer Number
  radio button.

e) Choose Continue.

f) On the Create Condition Records (Delivery Note Spec): Fast Entry screen, enter the
   data from the table above for customer C650-A00.

g) Save your data.

8. Create a sales order.
Use the following details:
Field                                       Value
Sold-To Party                               C650-A00

Cust. Reference                             ##-5-2

Req. deliv. date:                           One week from today
Material                                    P650-100

Order Quantity                              10

a) On the SAP Easy Access screen, choose Logistics → → Sales and
  Distribution → Sales → Order → Create.

b) In the Order Type field, enter OR.

c) Enter the data from the table above.

d) Save your data.

9. Create an outbound delivery for the sales order created in the previous step.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Shipping
  and Transportation → Outbound Delivery → Create → Single Document → With
  Reference to Sales Order.

b) On the Create Outbound Delivery with Order Reference screen, enter 1010 in the
  Shipping Point field.

c) In the Selection date field, change the date to the end of next week and choose
  Continue.

---

## PDF page 158

Chapitre 4: Messages

10. On the output screen for the header, check that the system has found output type ZLD0.
Use the determination analysis to solve any problems.
a) On the Delivery Create: Overview screen, choose Extras → Delivery Output → Header.

b) Check the output determination.

c) Return to the Delivery Create: Overview screen and choose Save.

d) Return to the SAP Easy Access screen.

11. Print preview the ZLD0 output.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution → Shipping
and Transportation → Communication/Printing → Outbound Delivery Output.

b) On the Output from Deliveries screen, ensure that the following details are entered:
Field                                      Value
Output Type                                ZLD0

Shipping Point/Receiving Pt                1010

Delivery                                   Delivery number from last activity

c) Choose Execute.

d) On the Output from Deliveries screen, choose from the list of deliveries by selecting the
checkbox in the Delivery field.

e) Choose Print Preview.
The output of the ZLD0 output is shown.

---

## PDF page 159

Chapitre 4
Exercice 10
Ajustement et traitement d'une catégorie de
message

Exemple de gestion
Pour optimiser le fonctionnement de l'administration des ventes dans votre entreprise, vous
avez créé un bon de livraison spécial (catégorie de message ZLD0) dans le système SAP.
Vos collègues du service Programmation vous informent que la programmation de la
catégorie de message ZLD0 est terminée et que vous pouvez la tester.
Ajustez et traitez la catégorie de message ZLD0. La figure Conversion de conditions dans le
pilotage des messages représente le flux de processus correspondant.
Vous devez procéder aux étapes appropriées dans le pilotage des messages.

Vérification des conditions de la catégorie de message
Vérifiez les conditions de la catégorie de message ZLD0.

1. Vérifiez si la catégorie de message ZLD0 a été correctement paramétrée dans le
Customizing.

2. Quel schéma comprend la catégorie ZLD0 (ZLD0 devant être un message d'en-tête pour
les livraisons) ?

3. Quelle est la séquence d'accès affectée à cette catégorie de message ?

4. Quels sont le programme de traitement et le formulaire affectés ?

Vérification des paramétrages pour pouvoir utiliser la catégorie de message
Vérifiez les paramétrages pour qu'il soit également possible d'utiliser la catégorie de message
ZLD0 pour votre point d'expédition 1010.

1. Affichez les paramètres d'impression pour le point d'expédition 1010. Utilisez les données
du tableau suivant :
Zone                                         Valeur
Point d'expédition                           1010

Unité de sortie                              LP01

Si cette entrée n'existe pas, créez-la de sorte que le message de type ZLD0 pour le point
d'expédition 1010 est envoyé à l'imprimante LP01.

2. Créez des enregistrements de conditions de messages destinés aux clients C650-A## et
C650-B## pour la catégorie de message ZLD0.
Vérifiez les éléments suivants :

---

## PDF page 160

Chapitre 4: Messages

Zone                                        Valeur
Organis. commerciale                        1010

Client                                      C650-A## et C650-B##

Type de support                             1 (Imprimer message)

Date/heure                                  3 (Envoi via transaction spécifique à l'appli-
                                        cation)

3. Créez une commande client de type ZA##. Utilisez les données du tableau suivant :
Zone                                        Valeur
Donneur d'ordre                             C650-A##

Réf. client                                 ##-4-1

DateLivrSouh.                               Dans une semaine
Article                                     P650-100

Quantité d’ordre                            10

Création d'une livraison sortante pour la commande
Créez une livraison sortante pour la commande client créée dans l'étape précédente.

1. Créez une livraison sortante pour la commande client créée dans l'étape précédente.

2. Dans l'écran des messages de l'en-tête, assurez-vous que le système recherche et définit
la catégorie de message ZLD0. Utilisez la fonction d'analyse de la détermination pour
corriger les problèmes éventuels.

3. Si la détermination des messages est correcte, sauvegardez la livraison.

4. Imprimez le bon de livraison.

5. Affichez le message généré dans le spool.

---

## PDF page 161

Chapitre 4
Solution 10
Ajustement et traitement d'une catégorie de
message

Exemple de gestion
Pour optimiser le fonctionnement de l'administration des ventes dans votre entreprise, vous
avez créé un bon de livraison spécial (catégorie de message ZLD0) dans le système SAP.
Vos collègues du service Programmation vous informent que la programmation de la
catégorie de message ZLD0 est terminée et que vous pouvez la tester.
Ajustez et traitez la catégorie de message ZLD0. La figure Conversion de conditions dans le
pilotage des messages représente le flux de processus correspondant.
Vous devez procéder aux étapes appropriées dans le pilotage des messages.

Vérification des conditions de la catégorie de message
Vérifiez les conditions de la catégorie de message ZLD0.

1. Vérifiez si la catégorie de message ZLD0 a été correctement paramétrée dans le
Customizing.
a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Données de
  base → Pilotage des messages → Détermination des messages → Gérer la
  détermination des messages pour les livraisons sortantes → Gérer les catégories de
  message.

b) Dans l'écran Afficher vue "Catégories de message" : synthèse, sélectionnez Positionner.

c) Dans la boîte de dialogue Autre entrée, saisissez ZLD0 dans la zone Catég. message.

d) Cliquez sur Suite.

e) Revenez à l'écran Afficher guide d'implémentation.

2. Quel schéma comprend la catégorie ZLD0 (ZLD0 devant être un message d'en-tête pour
les livraisons) ?
a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Données de
  base → Pilotage des messages → Détermination des messages → Gérer la
  détermination des messages pour les livraisons sortantes → Gérer le schéma de
  détermination des messages.

b) Dans l'écran Modifier vue "Schémas" : synthèse, sélectionnez la ligne contenant
  l'entrée V10000.

c) Dans la structure du dialogue, double-cliquez sur Pilotage.

3. Quelle est la séquence d'accès affectée à cette catégorie de message ?
a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Données de
  base → Pilotage des messages → Détermination des messages → Gérer la

---

## PDF page 162

Chapitre 4: Messages

détermination des messages pour les livraisons sortantes → Gérer les catégories de
message.

b) Dans l'écran Afficher vue "Catégories de message" : synthèse, sélectionnez Positionner.

c) Dans la boîte de dialogue Autre entrée, saisissez ZLD0 dans la zone Catég. message.

d) Cliquez sur Suite.

e) Sélectionnez la ligne contenant l'entrée ZLD0 et cliquez sur Détail.
Dans l'écran Afficher vue "Catégories de message" : détail, la séquence d'accès 0005
est affectée à la catégorie de message ZLD0.

f) Revenez à l'écran Afficher guide d'implémentation.

4. Quels sont le programme de traitement et le formulaire affectés ?
a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Données de
base → Pilotage des messages → Détermination des messages → Gérer la
détermination des messages pour les livraisons sortantes → Gérer les catégories de
message.

b) Dans l'écran Afficher vue "Catégories de message" : synthèse, sélectionnez Positionner.

c) Dans la boîte de dialogue Autre entrée, saisissez ZLD0 dans la zone Catég. message.

d) Cliquez sur Suite.

e) Sélectionnez la ligne contenant la catégorie de message ZLD0.

f) Dans la structure du dialogue, double-cliquez sur Routines de traitement.
Dans l'écran Afficher vue "Routines de traitement" : synthèse, les détails suivants
s'affichent pour le support Sortie imprimante :
Zone                                        Valeur
Programme                                   RLE_DELNOTE
Formulaire                                  LE_SHP_DELNOTE

g) Revenez à l'écran Afficher guide d'implémentation.

Vérification des paramétrages pour pouvoir utiliser la catégorie de message
Vérifiez les paramétrages pour qu'il soit également possible d'utiliser la catégorie de message
ZLD0 pour votre point d'expédition 1010.

1. Affichez les paramètres d'impression pour le point d'expédition 1010. Utilisez les données
du tableau suivant :
Zone                                          Valeur
Point d'expédition                            1010

Unité de sortie                               LP01

Si cette entrée n'existe pas, créez-la de sorte que le message de type ZLD0 pour le point
d'expédition 1010 est envoyé à l'imprimante LP01.

---

## PDF page 163

Sujet: Ajustement des catégories de messages

a) Dans le Customizing de Logistics Execution, sélectionnez Expédition → Données de
  base → Pilotage des messages → Définir le paramètre d'impression Expédition.

b) Dans l'écran Paramètre impression, sélectionnez Expédition (V2) → ZLD0.

c) Dans l'écran Modifier vue "Paramètre d'impression : Point d'expédition : détail, vérifiez
  que ce point d'expédition 1010 est configuré pour utiliser l'imprimante LP01.

d) Si l'entrée n'existe pas, cliquez sur le bouton Nouvelles entrées. Dans l'écran Nouvelles
  entrées : Détail des entrées ajoutées, saisissez 1010 dans la zone Point d'expédition et
  LP01 dans la zone Unité de sortie. Sauvegardez vos données.

e) Revenez à l'écran SAP Easy Access.

2. Créez des enregistrements de conditions de messages destinés aux clients C650-A## et
C650-B## pour la catégorie de message ZLD0.
Vérifiez les éléments suivants :
Zone                                          Valeur
Organis. commerciale                          1010

Client                                        C650-A## et C650-B##

Type de support                               1 (Imprimer message)

Date/heure                                    3 (Envoi via transaction spécifique à l'appli-
                                              cation)

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Données de base → Sortie → Expédition → Créer.

b) Dans l'écran Créer enregistrements condition des messages : Expédition, saisissez
  ZLD0 dans la zone Catégorie de message.

c) Cliquez sur Combinaison-clé.

d) Dans la boîte de dialogue Combinaison-clé, cochez la case d'option Organisation
  commerciale/N° client.

e) Cliquez sur Sélectionner.

f) Dans l'écran Créer enregistrements condition (Bon de livraison) : saisie rapide,
   saisissez les données du tableau (pour les deux clients).

g) Sauvegardez vos données.

3. Créez une commande client de type ZA##. Utilisez les données du tableau suivant :
Zone                                          Valeur
Donneur d'ordre                               C650-A##

Réf. client                                   ##-4-1

DateLivrSouh.                                 Dans une semaine
Article                                       P650-100

---

## PDF page 164

Chapitre 4: Messages

Zone                                         Valeur
Quantité d’ordre                             10

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Commande client → Créer.

b) Dans la zone Type de commande, saisissez ZA##.

c) Saisissez les données du tableau (en-tête).

d) Sauvegardez vos données.

Création d'une livraison sortante pour la commande
Créez une livraison sortante pour la commande client créée dans l'étape précédente.

1. Créez une livraison sortante pour la commande client créée dans l'étape précédente.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Expédition et transport → Livraison sortante → Créer → Document
individuel → avec référence à la commande client.

b) Dans l'écran Créer livraison sortante avec référence à la commande client, saisissez
1010 dans la zone Point d'expédition.

c) Modifiez la date de la zone Date de sélection en choisissant la fin de la semaine
prochaine, puis appuyez sur Entrée.

2. Dans l'écran des messages de l'en-tête, assurez-vous que le système recherche et définit
la catégorie de message ZLD0. Utilisez la fonction d'analyse de la détermination pour
corriger les problèmes éventuels.
a) Dans l'écran Livraison Modifier : synthèse, sélectionnez Autres fonctions → Message de
livraison → En-tête.

b) Sur l'écran Livraison : messages, sélectionnez Saut → Analyse de détermination.

3. Si la détermination des messages est correcte, sauvegardez la livraison.
a) Contrôlez la détermination des messages.

b) Revenez à l'écran Livraison Modifier : synthèse, puis cliquez sur Sauvegarder.

c) Revenez à l'écran SAP Easy Access.

4. Imprimez le bon de livraison.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Expédition et transport → Communication / Impression → Messages pour
livraison sortante.

b) Dans l'écran Messages issus des livraisons, les zones indiquées ci-dessous doivent être
renseignées avec les données du tableau :
Zone                                        Valeur
Type de sortie                              ZLD0

Point expédition/réception                  1010

---

## PDF page 165

Sujet: Ajustement des catégories de messages

    Zone                                        Valeur
    Livraison                                   Numéro livraison de la dernière activité

c) Cliquez sur Exécuter.

d) Dans l'écran Messages issus des livraisons, choisissez la liste des livraisons en cochant
  la case de la zone Livraison.

e) Cliquez sur Traiter.

5. Affichez le message généré dans le spool.
a) Sélectionnez Système → Services → Pilotage des sorties.

b) Dans l'écran Pilotage des sorties : sélection d'ordres spool, cliquez sur Exécuter.

c) Dans l'écran Pilotage des sorties : synthèse des ordres spool, sélectionnez l'ordre spool
  approprié en cochant la case de la zone N° spool.

d) Cliquez sur Afficher contenu.
  Le message de la catégorie de message ZLD0 s'affiche.

---

## PDF page 166

Chapitre 4: Messages

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Ajuster les catégories de messages

---

## PDF page 167

Chapitre 4
    Sujet 3
Nouvelle fonctionnalité de gestion des
messages

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Décrire la nouvelle fonctionnalité de gestion des messages

Nouvelle fonctionnalité de gestion des messages pour les documents de vente et
de facturation

 Figure 47: Nouvelle détermination des messages

La gestion des messages est une fonctionnalité fournie en option dans SAP S/4HANA.
Aucune action n'est obligatoire pour les clients dans ce cadre. Il est néanmoins possible
d'activer l'approche NAST en définissant un paramètre de Customizing spécifique (pour plus
d'informations, voir la note SAP 2228611).
La nouvelle fonctionnalité SAP S/4HANA, gestion des messages constitue l'infrastructure
stratégique de gestion des messages dans SAP S/4HANA, à laquelle seront ajoutés de
prochains développements. Adobe XFA est la technologie utilisée par défaut pour les modèles
de formulaires fournis dans cette infrastructure, mais les formulaires hérités (SAPscript,
SmartForms, formulaires Adobe) sont toujours pris en charge. Les principaux avantages de la
nouvelle approche sont les suivants :
●   Extensibilité : importante utilisation des vues CDS
●   BRFplus : flexibilité et puissance de la détermination des paramètres de sortie
●   Solution unifiée pour toutes les applications : SD, MM, FIN, etc.
●   SAP Fiori : intégration complète avec les applications SAP Fiori

---

## PDF page 168

Chapitre 4: Messages

●   Prise en charge d'options e-mail avancées : configuration flexible, plusieurs destinataires
et différents modèles d'e-mail

À la différence de la gestion des messages basée sur NAST, la nouvelle gestion des messages
prend uniquement en charge les canaux impression, e-mail, XML et IDoc (sur site). Les autres
canaux ne sont pas disponibles par défaut.

Figure 48: Exemple de message - confirmation de commande

Le modèle de formulaire utilisé par la gestion des messages pour générer un document PDF
comprend une source de données (service OData) et la mise en forme du document PDF
(document de conception Adobe Livecycle). Le service OData extrait de la base de données
les données destinées au document de vente, puis l'ensemble de résultats est fusionné avec
le document de conception Adobe Livecycle de façon à générer un document PDF
représentant le document de vente.
Lorsque la fonctionnalité de gestion des messages signale que les messages sont à présent
prêts pour l'impression ou l'envoi par e-mail (lorsque le statut des messages est défini sur En
attente ou Réussite), le document PDF généré est enregistré dans l'archive Knowledge
Provider (KPro). KPro est une infrastructure générale et complète qui met à disposition des
technologies de gestion des documents inter-applications et multi-supports. Dès lors, la
prévisualisation ultérieure du document PDF relatif aux messages émis sera possible depuis
l'archive KPro, pour garantir l'exactitude historique. La prévisualisation d'un message qui n'a
pas encore été émis (toujours au statut En préparation) continuera de refléter les données
telles qu'elles apparaissent dans la transaction en cours.

---

## PDF page 169

Sujet: Nouvelle fonctionnalité de gestion des messages

 Figure 49: Table de décisions BRFplus

Dans BRFplus, les tables de décisions permettent de déterminer les différents paramètres de
sortie (catégorie de message, récepteur, modèle de formulaire, etc.).
Lorsqu'une expression de la table de décisions BRFplus est appelée, les lignes sont traitées
l'une après l'autre. Dans chaque ligne, les cellules de la colonne des conditions sont traitées
de gauche à droite. Les valeurs de zone définies dans les colonnes de résultat sont retournées
si la condition est remplie dans chacune des cellules de la colonne d'entrée d'une ligne. Il est
possible de saisir des expressions ou des valeurs directes dans ces cellules. Il est également
possible d'analyser les valeurs de chaque cellule à l'aide d'opérateurs de comparaison, de
plages de valeurs et de modèles.

 Figure 50: Tables de décisions pour la détermination des messages

---

## PDF page 170

Chapitre 4: Messages

En utilisant les tables des décisions, vous pouvez déterminer la catégorie de message, le
destinataire, le canal, les réglages d'impression et le modèle de formulaire pour les
documents de facturation. Il est possible de réorganiser les lignes de la table afin que les
conditions les plus spécifiques soient vérifiées en premier. Il est également possible
d'importer et d'exporter les tables vers Microsoft Excel.

Définition d'une nouvelle catégorie de message - démonstration
Create new output type as a copy of the existing output type ORDER_CONFIRMATION. The
document should be printed when standard orders are saved for customer C650-A00 and
sales organization 1010.

1. Ensure transports are deactivated before continuing with this demonstration.
a) On the SAP Easy Access screen, choose
Tools → Administration → Administration → Client Administration → Client
Maintenance.

b) In the Display View “Clients”: Overview screen, choose Display → Change.

c) In the dialog box, choose Continue.

d) In the Change View “Clients”: Overview screen, select the entry for client 400 and
choose Details.

e) In the Change View “Clients”: Details screen, under Changes and Transports for Client-
Specific Objects, select the radio button Changes without automatic recording.

f) Choose Save.

2. Ensure New Output Management is active for sales documents.
a) Go to Customizing for Cross-Application Components under Output Control → Manage
Application Object Type Activation.

b) In the Change View “Activation of Application Object Type”: Overview screen, set the
Status field for the application type SALES_DOCUMENT to Application Active.

c) Save your data.

d) Return to the Customizing screen.

3. Define a new output type ORDER_CONFIRMATION_00 with the description
Confirmation Group 00.
a) Go to Customizing for Cross-Application Componentsunder Output Control → Define
Output Types.

b) In the Information dialog box, choose Continue.

c) In the Change View “Output Type”: Overview screen, choose the Position button.

d) Enter the following data:
Field                                       Value
Appl. Object Type                           SALES_DOCUMENT

---

## PDF page 171

Sujet: Nouvelle fonctionnalité de gestion des messages

    Field                                   Value
    Output Type                             ORDER_CONFIRMATION

e) Choose Continue (Enter).

f) Select the line.

g) Choose the Copy As… button.

h) Enter the following data:
    Field                                   Value
    Appl. Object Type                       SALES_DOCUMENT

    Output Type                             ORDER_CONFIRMATION_00

    Text                                    Confirmation Group 00

    Callback Class                          CL_SD_SLS_OUTPUT

i) Choose the Apply (Enter) button.

j) If the warning message Select a key from the allowed namespace is
   displayed, ignore it and choose the Enter button.

k) Save your data.

l) Return to the Customizing screen.

4. Assign the form template SD_SLS_ORDER_CONFIRM to the output type
ORDER_CONFIRMATION_00.
a) Go to Customizing for Cross-Application Components under Output Control → Assign
  Form Templates.

b) In the Change View “Form Template”: Overview screen, choose New Entries.

c) Enter the following data:
    Field                                   Value
    Application Object Type                 SALES_DOCUMENT

    Output Type                             ORDER_CONFIRMATION_00

    Form Type                               1 Output Forms (Gateway Inter-
                                            face)

    Form Template ID                        SD_SLS_ORDER_CONFIRM

d) Save your data.

e) Return to the Customizing screen.

5. Assign Output Type ORDER_CONFIRMATION_00 to Output Channel PRINT.
a) Go to Customizing for Cross-Application Components under Output Control → Assign
  Output Channels.

---

## PDF page 172

Chapitre 4: Messages

b) On the Change View “Channel”: Overview screen, choose New Entries.

c) Enter the following data:
Field                                       Value
Application Object Type                     SALES_DOCUMENT

Output Type                                 ORDER_CONFIRMATION_00

Channel                                     PRINT

d) Save your data.

e) Ensure that Output Channel PRINT is also assigned (as above) to the following Output
Types:
ORDER_CONFIRMATION and ORDER_CONFIRMATION_CHANGE
CASH_SALE and CASH_SALE_CHANGE
SALES_INQUIRY and SALES_INQUIRY_CHANGE
SALES_QUOTATION and SALES_QUOTATION_CHANGE
SALES_CONTRACT and SALES_CONTRACT_CHANGE
CUSTOMER_RETURN and CUSTOMER_RETURN_CHANGE
ORDER_WO_CHARGE and ORDER_WO_CHARGE_CHANGE
DEBIT_MEMO_REQUEST and DEBIT_MEMO_REQUEST_CHANGE
CREDIT_MEMO_REQUEST and CREDIT_MEMO_REQUEST_CHANGE
SEPA_MANDATE

6. Define the Business Rules for the new Output Type.
Go to Customizing for Cross-Application Components under Output Control → Define
Business Rules for Output Determination (transaction OPD).
a) In the Output Parameter Determination screen, choose Sales Document as the value of
Show Rules for and Output Type as the value of Determination Step.

a) Under Maintain Business Rules, choose the Edit button.

b) Choose the Table Settings button to add the document attribute Sales Organization
  to the set of condition criteria.

c) Under the Condition Columns section, choose the Insert Column button. Select the
   option From Context Data Objects and scroll down to the Sales Org row. Select it
   and choose the OK button. The column SALESORGANIZATION will be added to the
   list of condition columns used in the rules for determining output types. Choose the
   OK button.

d) Select the first row in the table and choose the Insert New Row button.

e) Under Document Category, select Direct Value Input. Select the relationship is
  equal to and enter the value C (Order). Choose OK.

---

## PDF page 173

Sujet: Nouvelle fonctionnalité de gestion des messages

    f) Under Sales Document Type, select Direct Value Input. Select the relationship is
       equal to and enter the value TA. Choose OK.

    g) Under Sales Org, select Direct Value Input. Select the relationship is equal to and
       enter the value 1010. Choose OK.

    h) Under Output Type, select Direct Value Input. Enter the value
       ORDER_CONFIRMATION_00. Choose OK.

     i) Scroll to the right and under Dispatch Time, select Direct Value Input. Enter the
        value 1 (Immediately). Choose OK.

     j) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
        ignored.

    k) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

b) In the Output Parameter Determination screen, choose Sales Document as the value of
  Show Rules for and Receiver as the value of Determination Step.

    a) Under Maintain Business Rules, choose the Edit button.

    b) Select the first row in the table and choose the Insert New Row button.

    c) Under Output Type, select Direct Value Input. Select the relationship is equal to and
       enter the value ORDER_CONFIRMATION_00. Choose OK.

    d) Under Role, select Direct Value Input. Enter the value AG. Choose OK.

    e) Under Exclusive Indicator, select Direct Value Input. Enter the value '-' (false).
       Choose OK.

    f) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
       ignored.

    g) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

c) In the Output Parameter Determination screen, choose Sales Document as the value of
  Show Rules for and Channel as the value of Determination Step.

    a) Under Maintain Business Rules, choose the Edit button.

    b) Select the first row in the table and choose the Insert New Row button.

    c) Under Output Type, select Direct Value Input. Select the relationship is equal to and
       enter the value ORDER_CONFIRMATION_00. Choose OK.

    d) Under Role, select Direct Value Input. Select the relationship is equal to and enter
       the value AG. Choose OK.

    e) Under Recipient, select Direct Value Input. Select the relationship is equal to and
       enter the value C650-A00. Choose OK.

    f) Under Channel, select Direct Value Input. Enter the value PRINT. Choose OK.

    g) Under Exclusive Indicator, select Direct Value Input. Enter the value '-'. Choose OK.

---

## PDF page 174

Chapitre 4: Messages

h) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
  ignored.

i) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

d) In the Output Parameter Determination screen, choose Sales Document as the value of
Show Rules for and Printer Settings as the value of Determination Step.

a) Under Maintain Business Rules, choose the Edit button.

b) Select the first row in the table and choose the Insert New Row button.

c) Under Output Type, select Direct Value Input. Select the relationship is equal to and
   enter the value ORDER_CONFIRMATION_00. Choose OK.

d) Under Print Queue, select Direct Value Input. Enter the value LP01. Choose OK.

e) Scroll to the right and under Number of copies, select Direct Value Input. Enter the
  value 1. Choose OK.

f) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
   ignored.

g) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

e) In the Output Parameter Determination screen, select Sales Document as the value of
Show Rules for and Form Template as the value of Determination Step.

a) Under Maintain Business Rules, choose the Edit button.

b) Select the first row in the table and choose the Insert New Row button.

c) Under Output Type, select Direct Value Input. Select the relationship is equal to and
   enter the value ORDER_CONFIRMATION_00. Choose OK.

d) Scroll to the right and under Form Template, select Direct Value Input. Enter the
  value SD_SLS_ORDER_CONFIRM. Choose OK.

e) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
  ignored.

f) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

f) In the Output Parameter Determination screen, choose Sales Document as the value of
Show Rules for and Output Relevance as the value of Determination Step.

a) Under Maintain Business Rules, choose the Edit button.

b) Select the first row in the table and choose the Insert New Row button.

c) Under Output Type, select Direct Value Input. Select the relationship is equal to and
   enter the value ORDER_CONFIRMATION_00. Choose OK.

d) Under Confirm Status, select Direct Value Input. Select the relationship is equal to
  and enter the value C (All schedule lines by MM confirmed).

---

## PDF page 175

Sujet: Nouvelle fonctionnalité de gestion des messages

    e) Choose the Change button and select Insert Include Condition. Select the
       relationship is equal to and insert the space symbol (Item not relevant for
       confirmation) as a value. Choose OK.

    f) Scroll to the right and under Relevance Indicator, select Direct Value Input. Enter
       the value X (true). Choose OK.

    g) Choose the Check button. Warning messages (prefixed with a yellow icon) can be
       ignored.

    h) Choose the Activate button. In the Confirm Activation dialog box, choose Yes.

7. Test the configured solution.
a) Create a sales order using the following data:
    Field                                          Value
    Order Type                                     OR

    Sales Organization                             1010

    Distribution Channel                           10

    Division                                       00

    Sold-to Party                                  C605-A00

    Cust. Reference                                New_Output_123

    Material                                       P605-100

    Quantity                                       10

b) In the menu, choose Extras → Output → Header → Edit.

c) Select the line with the ORDER_CONFIRMATION_00 output type and choose the
  Display PDF button.

d) Save the sales document and note the document number.

8. Demonstrate the processing steps for the new output management.
a) Run transaction BRF+. Choose the Personalize button (upper right corner). Set the
  User Mode to Expert. Save the settings.

b) To display the Output Management application, choose the Search button. Enter the
  following data:
    Field                        Relationship                        Value
    Application Name             is equal to                         OPD*

    Object Type                  is equal to                         Application

   Choose the Search button.

c) Expand the application OPD_V1_SALES_DOCUMENT. In the search results, expand the
  Function node and then select FUNC_OUTPUT_TYPE.

d) Choose the Simulation button. Choose Continue.

---

## PDF page 176

Chapitre 4: Messages

e) Enter the sales document number (with leading zeros) into the Document ID field (field
length is 10 digits).

f) Choose the Execute and Display Processing Steps button.

g) In the Result area, demonstrate the results of execution of the function: Output type
ORDER_CONFIRMATION_00 with dispatch type = 1.

h) Scroll down to the Rule node. Demonstrate the evaluation steps in the table according
to the decision table DEC_TAB_OUTPUT_TYPE.

9. Display the instance of the generated business object for Output Type.
a) Run transaction BOBT.

b) In the Business Object Builder: Test screen, choose the Search button and choose the
business object type APOC_OUTPUT_REQUEST.

c) Choose the Load Node Instances button. Choose By Query → ROOT -
QUERY_BY_ELEMENTS.

d) Enter the number of the sales order created above in the field APPL_OBJECT_ID (with
leading zeros) and enter SALES_DOCUMENT in the field APPL_OBJECT_TYPE (optional).

e) Choose Continue (Enter).

f) Expand the found object and double-click on the Item folder. Demonstrate the
generated instance of the output type on the right-hand side of the screen. Double-
click on the line for the output type ORDER_CONFIRMATION_00 to open the screen
with detailed data.

g) Take a copy of the value of the field ROOT_KEY (on the detail screen).

10. Display the log for processing of the output type.
a) Run transaction SLG1. Enter the value copied above in the External ID field and choose
the Execute button. Demonstrate the log for the generated output type.

---

## PDF page 177

Chapitre 4
Exercice 11
Création d'une catégorie de message pour la
confirmation de commande

Exemple de gestion
Votre entreprise imprime les confirmations de commande standard. Toutefois, certains
clients demandent un formulaire spécial pour les confirmations de commande, une nouvelle
catégorie de message doit donc être créée. Elle peut être copiée à partir du type de message
ORDER_CONFIRMATION existant. Le nouveau message doit être imprimé lorsque les
commandes client de type ZA## sont sauvegardées pour le client C650-B##.
Tâche 1 : Assurez-vous que la nouvelle fonctionnalité de gestion des messages est active
pour les documents de vente.

1. Assurez-vous que la nouvelle fonctionnalité de gestion des messages est active pour les
documents de vente.

Tâche 2 : Définissez une nouvelle catégorie de message ORDER_CONFIRMATION_# #
avec la désignation Groupe de confirmation ##.

1. Définissez une nouvelle catégorie de message ORDER_CONFIRMATION_# # avec la
désignation Groupe de confirmation ##.

Tâche 3 : Affectez le modèle de formulaire SD_SLS_ORDER_CONFIRM à la catégorie de
message ORDER_CONFIRMATION_##.

1. Affectez le modèle de formulaire SD_SLS_ORDER_CONFIRM à la catégorie de message
ORDER_CONFIRMATION_##.

Tâche 4 : Affectez la catégorie de message ORDER_CONFIRMATION_## au Canal de
sortie PRINT

1. Affectez la catégorie de message ORDER_CONFIRMATION_## au canal de sortie PRINT

Tâche 5 : Définissez des règles de gestion pour la nouvelle catégorie de message.
Accédez au Customizing pour Composantes inter-applications sous Pilotage des
messages → Définir règles de gestion pour détermination des messages (transaction OPD).

1. Vérifiez que la catégorie de message ORDER_CONFIRMATION_## et la date/heure
d'envoi 1 sont sélectionnées lorsqu'un document de vente de type ZA## est placé.

2. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est créé pour le donneur
d'ordre (fonction partenaire AG).

3. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est reçu par le client C650-
B##, faisant office de donneur d'ordre, via le canal PRINT (c'est-à-dire comme imprimé).

4. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est imprimé via la file
d'impression LP01. Une copie doit être imprimée.

---

## PDF page 178

Chapitre 4: Messages

5. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est fabriqué au moyen du
modèle de formulaire SD_SLS_ORDER_CONFIRM.

6. Vérifiez que le type de sortie ORDER_CONFIRMATION_# # est fabriqué si le statut de
confirmation du document de vente est défini sur C ou " " (vide).

Tâche 6 : Testez la solution configurée

1. Créez une commande client à l'aide des données suivantes :
Zone                                       Valeur
Type de commande                           ZA##

Organis. commerciale                       1010

Canal distribution                         10

Secteur d'activité                         00

Donneur d'ordre                            C650-B##

Réf. client                                11-22-##

Article                                    P650-1##

Quantité                                   10

2. Vérifiez qu'une sortie de type ORDER_CONFIRMATION_## a été créée.

3. Sauvegardez le document de vente et notez son numéro.

---

## PDF page 179

Chapitre 4
Solution 11
Création d'une catégorie de message pour la
confirmation de commande

Exemple de gestion
Votre entreprise imprime les confirmations de commande standard. Toutefois, certains
clients demandent un formulaire spécial pour les confirmations de commande, une nouvelle
catégorie de message doit donc être créée. Elle peut être copiée à partir du type de message
ORDER_CONFIRMATION existant. Le nouveau message doit être imprimé lorsque les
commandes client de type ZA## sont sauvegardées pour le client C650-B##.
Tâche 1 : Assurez-vous que la nouvelle fonctionnalité de gestion des messages est active
pour les documents de vente.

1. Assurez-vous que la nouvelle fonctionnalité de gestion des messages est active pour les
documents de vente.
a) Accédez au Customizing pour Composantes inter-applications sous Pilotage des
  sorties → Gérer l'activation du type d'objet d'application.

b) Dans l'écran Modifier vue "Activation du type d'objet d'application" : synthèse, vérifiez
  que la zone Statut pour le type d'objet applicatif SALES_DOCUMENT soit définie sur 1
  Application active.

c) Si vous avez modifié le statut, sauvegardez vos données.

d) Revenez à l'écran Afficher guide d'implémentation.

Tâche 2 : Définissez une nouvelle catégorie de message ORDER_CONFIRMATION_# #
avec la désignation Groupe de confirmation ##.

1. Définissez une nouvelle catégorie de message ORDER_CONFIRMATION_# # avec la
désignation Groupe de confirmation ##.
a) Accédez au Customizing pour Composantes inter-applications sous Pilotage des
  sorties → Définir catégories de messages.

b) Dans la boîte de dialogue Information, cliquez sur Suite.

c) Dans l'écran Modifier vue "Catégorie de message" : synthèse, cliquez sur le bouton
  Positionner.

d) Saisissez les données suivantes :
    Zone                                        Valeur
    Type d'objet d'application                  SALES_DOCUMENT

    Type de sortie                              ORDER_CONFIRMATION

e) Sélectionnez Suite (Entrée).

---

## PDF page 180

Chapitre 4: Messages

f) Sélectionnez la ligne.

g) Cliquez sur le bouton Copier sous.

h) Saisissez les données suivantes :
Zone                                       Valeur
Type d'objet d'application                 SALES_DOCUMENT

Type de sortie                             ORDER_CONFIRMATION_##

Texte                                      Confirmation de commande Groupe
                                           ##

Classe de rappel                           CL_SD_SLS_OUTPUT

i) Cliquez sur le bouton Appliquer (Entrée).

j) Si vous obtenez un message d'avertissement Sélectionnez une clé dans
l'espace nom autorisé, ignorez-le et cliquez sur le bouton Entrée.

k) Sauvegardez vos données.

l) Revenez à l'écran Afficher guide d'implémentation.

Tâche 3 : Affectez le modèle de formulaire SD_SLS_ORDER_CONFIRM à la catégorie de
message ORDER_CONFIRMATION_##.

1. Affectez le modèle de formulaire SD_SLS_ORDER_CONFIRM à la catégorie de message
ORDER_CONFIRMATION_##.
a) Accédez au Customizing pour Composantes inter-applications sous Pilotage des
sorties → Affecter des modèles de formulaires.

b) Dans l'écran Modifier vue "Modèle de formulaire" : synthèse, cliquez sur Nouvelles
entrées.

c) Si vous obtenez un message d'avertissement (jaune), ignorez-le et cliquez sur le
bouton Entrée.

d) Saisissez les données suivantes :
Zone                                       Valeur
Type d'objet d'application                 SALES_DOCUMENT

Type de sortie                             ORDER_CONFIRMATION_##

Type form.                                 1 Formulaires d'édition (inter-
                                           face de passerelle)

ID du modèle de formulaire                 SD_SLS_ORDER_CONFIRM

e) Sauvegardez vos données.

f) Revenez à l'écran Afficher guide d'implémentation.

Tâche 4 : Affectez la catégorie de message ORDER_CONFIRMATION_## au Canal de
sortie PRINT

1. Affectez la catégorie de message ORDER_CONFIRMATION_## au canal de sortie PRINT

---

## PDF page 181

Sujet: Nouvelle fonctionnalité de gestion des messages

a) Accédez au Customizing pour Composantes inter-applications sous Pilotage des
  sorties → Affecter les canaux de sortie.

b) Dans l'écran Modifier vue "Canal" : synthèse, cliquez sur Nouvelles entrées.

c) Saisissez les données suivantes :
    Zone                                       Valeur
    Type d'objet d'application                 SALES_DOCUMENT

    Type de sortie                             ORDER_CONFIRMATION_##

    Canal                                      PRINT

d) Sauvegardez vos données.

e) Assurez-vous que le canal de sortie PRINT est également affecté (voir ci-dessus) aux
  types de sortie suivants :
   ORDER_CONFIRMATION et ORDER_CONFIRMATION_CHANGE
   CASH_SALE et CASH_SALE_CHANGE
   SALES_INQUIRY et SALES_INQUIRY_CHANGE
   SALES_QUOTATION et SALES_QUOTATION_CHANGE
   SALES_CONTRACT et SALES_CONTRACT_CHANGE
   CUSTOMER_RETURN et CUSTOMER_RETURN_CHANGE
   ORDER_WO_CHARGE et ORDER_WO_CHARGE_CHANGE
   DEBIT_MEMO_REQUEST et DEBIT_MEMO_REQUEST_CHANGE
   CREDIT_MEMO_REQUEST et CREDIT_MEMO_REQUEST_CHANGE
   SEPA_MANDATE

Tâche 5 : Définissez des règles de gestion pour la nouvelle catégorie de message.
Accédez au Customizing pour Composantes inter-applications sous Pilotage des
messages → Définir règles de gestion pour détermination des messages (transaction OPD).

1. Vérifiez que la catégorie de message ORDER_CONFIRMATION_## et la date/heure
d'envoi 1 sont sélectionnées lorsqu'un document de vente de type ZA## est placé.
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
  comme valeur pour Afficher règles pour et Type d'édition comme valeur de l'Étape de
  détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
  ligne.

d) Sous Catég. document, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
  comme relation et saisissez la valeur X. Cliquez sur OK.

e) Sous Type doc. vente, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
  comme relation et saisissez la valeur ZA##. Cliquez sur OK.

---

## PDF page 182

Chapitre 4: Messages

f) S'il existe une colonne appelée Organisation commerciale, sous Organisation
commerciale sélectionnez Saisie directe de valeur. Sélectionnez Est égal à comme
relation, saisissez la valeur 1010 et cliquez sur OK. S'il n'existe aucune colonne
appelée Organisation commerciale, ignorez cette sous-étape.

g) Sous Type de sortie, sélectionnez Saisie directe de valeur. Saisissez la valeur
ORDER_CONFIRMATION_##. Cliquez sur OK.

h) Faites défiler l'écran vers la droite et sous Date/heure d'envoi, sélectionnez Saisie
directe de valeur. Saisissez la valeur 1 (immédiatement). Cliquez sur OK.

i) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
jaune) peuvent être ignorés.

j) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
sur Oui.

2. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est créé pour le donneur
d'ordre (fonction partenaire AG).
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
comme valeur pour Afficher règles pour et Récepteur comme valeur de l'Étape de
détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
ligne.

d) Sous Type de sortie, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
comme relation et saisissez la valeur ORDER_CONFIRMATION_##. Cliquez sur OK.

e) Sous Rôle, sélectionnez Saisie directe de valeur. Saisissez la valeur AG. Cliquez sur OK.

f) Sous Code exclusif, sélectionnez Saisie directe de valeur. Saisissez la valeur "-" (faux).
Cliquez sur OK.

g) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
jaune) peuvent être ignorés.

h) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
sur Oui.

3. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est reçu par le client C650-
B##, faisant office de donneur d'ordre, via le canal PRINT (c'est-à-dire comme imprimé).
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
comme valeur pour Afficher règles pour et Canal comme valeur de l'Étape de
détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
ligne.

d) Sous Type de sortie, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
comme relation et saisissez la valeur ORDER_CONFIRMATION_##. Cliquez sur OK.

---

## PDF page 183

Sujet: Nouvelle fonctionnalité de gestion des messages

e) Sous Rôle, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à comme
  relation et saisissez la valeur AG. Cliquez sur OK.

f) Sous Destinataire, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
   comme relation et saisissez la valeur C650-B##. Cliquez sur OK.

g) Sous Canal, sélectionnez Saisie directe de valeur. Saisissez la valeur PRINT. Cliquez
  sur OK.

h) Sous Code exclusif, sélectionnez Saisie directe de valeur. Saisissez la valeur "-".
  Cliquez sur OK.

i) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
   jaune) peuvent être ignorés.

j) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
   sur Oui.

4. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est imprimé via la file
d'impression LP01. Une copie doit être imprimée.
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
  comme valeur pour Afficher règles pour et Options d'impression comme valeur de
  l'Étape de détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
  ligne.

d) Sous Type de sortie, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
  comme relation et saisissez la valeur ORDER_CONFIRMATION_##. Cliquez sur OK.

e) Sous File d'impression, sélectionnez Saisie directe de valeur. Saisissez la valeur LP01.
  Cliquez sur OK.

f) Faites défiler l'écran vers la droite et sous Nombre de copies, sélectionnez Saisie
   directe de valeur. Saisissez la valeur 1. Cliquez sur OK.

g) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
  jaune) peuvent être ignorés.

h) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
  sur Oui.

5. Vérifiez que le type de sortie ORDER_CONFIRMATION_## est fabriqué au moyen du
modèle de formulaire SD_SLS_ORDER_CONFIRM.
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
  comme valeur pour Afficher règles pour et Modèle de formulaire comme valeur de
  l'Étape de détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
  ligne.

d) Sous Type de sortie, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
  comme relation et saisissez la valeur ORDER_CONFIRMATION_##. Cliquez sur OK.

---

## PDF page 184

Chapitre 4: Messages

e) Faites défiler l'écran vers la droite et sous Modèle de formulaire, sélectionnez Saisie
directe de valeur. Saisissez la valeur SD_SLS_ORDER_CONFIRM. Cliquez sur OK.

f) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
jaune) peuvent être ignorés.

g) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
sur Oui.

6. Vérifiez que le type de sortie ORDER_CONFIRMATION_# # est fabriqué si le statut de
confirmation du document de vente est défini sur C ou " " (vide).
a) Dans l'écran Détermination des paramètres d'édition, sélectionnez Document de vente
comme valeur pour Afficher règles pour et Pertinence pour édition comme valeur de
l'Étape de détermination.

b) Sous Gérer règles de gestion, cliquez sur le bouton Traiter.

c) Sélectionnez la première ligne du tableau et cliquez sur le bouton Insérer nouvelle
ligne.

d) Sous Type de sortie, sélectionnez Saisie directe de valeur. Sélectionnez Est égal à
comme relation et saisissez la valeur ORDER_CONFIRMATION_##. Cliquez sur OK.

e) Sous Statut de confirmation, sélectionnez Saisie directe de valeur. Sélectionnez la
relation Est égal à et saisissez la valeur C (toutes les échéances par MM
confirmées).

f) Cliquez sur le bouton Modifier et sélectionnez Insérer condition include. Sélectionnez la
relation Est égal à et saisissez le symbole espace (poste non pertinent pour
confirmation) comme valeur. Cliquez sur OK.

g) Faites défiler l'écran vers la droite et sous Code de pertinence, sélectionnez Saisie
directe de valeur. Saisissez la valeur X (Vrai). Cliquez sur OK.

h) Cliquez sur le bouton Contrôler. Les messages d'avertissement (précédés d'une icône
jaune) peuvent être ignorés.

i) Cliquez sur le bouton Activer. Dans la boîte de dialogue Confirmer activation, cliquez
sur Oui.

Tâche 6 : Testez la solution configurée

1. Créez une commande client à l'aide des données suivantes :
Zone                                          Valeur
Type de commande                              ZA##

Organis. commerciale                          1010

Canal distribution                            10

Secteur d'activité                            00

Donneur d'ordre                               C650-B##

Réf. client                                   11-22-##

Article                                       P650-1##

---

## PDF page 185

Sujet: Nouvelle fonctionnalité de gestion des messages

Zone                                         Valeur
Quantité                                     10

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Commande client → Créer.

b) Dans la zone Type de commande, saisissez ZA##.

c) Saisissez les données requises du tableau (en-tête).

2. Vérifiez qu'une sortie de type ORDER_CONFIRMATION_## a été créée.
a) Dans le menu, sélectionnez Autres fonctions → Message → En-tête → Traiter.

b) Pour afficher cette sortie, sélectionnez la ligne contenant la catégorie de message
  ORDER_CONFIRMATION_## et cliquez sur le bouton Afficher document PDF.

3. Sauvegardez le document de vente et notez son numéro.
a) Cliquez sur le bouton Sauvegarder.

---

## PDF page 186

Chapitre 4: Messages

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Décrire la nouvelle fonctionnalité de gestion des messages

---

## PDF page 187

Chapitre 4

Évaluation des connaissances

1. Parmi les fonctions suivantes, lesquelles pouvez-vous utiliser pour voir les ajustements
effectués dans la détermination des messages ?
Sélectionnez la réponse correcte.

X    A Analyse

X    B Enregistrement de conditions

X    C Création

X    D Modification

2. Une stratégie de communication peut être utilisée pour la communication externe.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

3. Avec la détermination des messages, la stratégie permettant d'accéder à des
enregistrements de conditions valides est toujours définie pour que les recherches soient
effectuées « du général au particulier ».
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

4. Parmi les structures suivantes, laquelle pouvez-vous utiliser pour traiter les modifications
ne nécessitant ni logique de préparation de document ou ni nouvelles zones dans la
structure de communication ?
Sélectionnez la réponse correcte.

X    A SAPscript

X    B Programmes INCLUDE

X    C Options d'imprimante

---

## PDF page 188

Chapitre 4: Évaluation des connaissances

5. Parmi les conditions suivantes, lesquelles sont requises pour qu'une modification
« simple » de formulaire (ajout de zone) puisse être effectuée ?
Sélectionnez les réponses correctes.

X    A La zone existe dans la structure de communication.

X    B La zone peut être intégrée au formulaire sous sa forme actuelle.

X    C La zone doit être ajoutée à la structure de communication existante.

6. Parmi les propositions suivantes, laquelle décrit correctement la manière dont une table
de décision de sortie BRFplus est traitée ?
Sélectionnez les réponses correctes.

X    A Chaque ligne de la table est traitée dans la séquence.

X    B Pour chaque ligne, les cellules de la colonne des conditions sont traitées de droite à
 gauche.

X    C Il est possible d'organiser les lignes de la table afin que les ensembles de
 conditions les plus spécifiques soient évalués en premier.

---

## PDF page 189

Chapitre 4

Évaluation des connaissances - Réponses

1. Parmi les fonctions suivantes, lesquelles pouvez-vous utiliser pour voir les ajustements
effectués dans la détermination des messages ?
Sélectionnez la réponse correcte.

X    A Analyse

X    B Enregistrement de conditions

X    C Création

X    D Modification

Correct ! Vous pouvez utiliser la fonction d'analyse pour voir quelles catégories de
messages ont été déterminées. Les enregistrements de conditions, que ce soit en mode
de création ou de modification, ne comportent aucune fonction permettant de voir
l'analyse des messages. Pour en savoir plus, reportez-vous au sujet Détermination des
catégories de messages (Chapitre 4, Sujet 1) dans le cours S4650.

2. Une stratégie de communication peut être utilisée pour la communication externe.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! La stratégie de communication est conçue en vue d'être utilisée pour la
communication externe. Pour en savoir plus, reportez-vous au sujet Détermination des
catégories de messages (Chapitre 4, Sujet 1) dans le cours S4650.

3. Avec la détermination des messages, la stratégie permettant d'accéder à des
enregistrements de conditions valides est toujours définie pour que les recherches soient
effectuées « du général au particulier ».
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! Avec la technique de conditions, toutes les stratégies doivent commencer par
cibler les entrées spécifiques, puis s'intéresser progressivement aux enregistrements de
conditions généraux. Pour en savoir plus, reportez-vous au sujet Détermination des
catégories de messages (Chapitre 4, Sujet 1) dans le cours S4650.

---

## PDF page 190

Chapitre 4: Évaluation des connaissances - Réponses

4. Parmi les structures suivantes, laquelle pouvez-vous utiliser pour traiter les modifications
ne nécessitant ni logique de préparation de document ou ni nouvelles zones dans la
structure de communication ?
Sélectionnez la réponse correcte.

X    A SAPscript

X    B Programmes INCLUDE

X    C Options d'imprimante

Correct ! Vous pouvez utiliser les formulaires SAPscript pour traiter les modifications
simples ne nécessitant ni logique de préparation de document ni nouvelles zones dans la
structure de communication. Les programmes INCLUDE et les options de l'imprimante
n'interviennent pas dans le processus de préparation de document. Pour en savoir plus,
reportez-vous au sujet Ajustement des catégories de messages (Chapitre 4, Sujet 2) dans
le cours S4650.

5. Parmi les conditions suivantes, lesquelles sont requises pour qu'une modification
« simple » de formulaire (ajout de zone) puisse être effectuée ?
Sélectionnez les réponses correctes.

X    A La zone existe dans la structure de communication.

X    B La zone peut être intégrée au formulaire sous sa forme actuelle.

X    C La zone doit être ajoutée à la structure de communication existante.

Correct ! Une modification de formulaire est simple si la zone existe dans la structure de
communication et si cette zone peut être intégrée au formulaire sous son format existant.
S'il est nécessaire d'ajouter la zone à la structure de communication existante, alors le
formulaire n'est plus considéré comme simple. Pour en savoir plus, reportez-vous au sujet
Ajustement des catégories de messages (Chapitre 4, Sujet 2) dans le cours S4650.

6. Parmi les propositions suivantes, laquelle décrit correctement la manière dont une table
de décision de sortie BRFplus est traitée ?
Sélectionnez les réponses correctes.

X    A Chaque ligne de la table est traitée dans la séquence.

X    B Pour chaque ligne, les cellules de la colonne des conditions sont traitées de droite à
 gauche.

X    C Il est possible d'organiser les lignes de la table afin que les ensembles de
 conditions les plus spécifiques soient évalués en premier.

Correct ! Chaque ligne de la table est traitée dans la séquence. Par ligne, les cellules de la
colonne des conditions sont ensuite traitées de gauche à droite. Les lignes peuvent être
organisées comme vous le souhaitez. Pour en savoir plus, reportez-vous au sujet Nouvelle
fonctionnalité de gestion des messages (Chapitre 4, Sujet 3) dans le cours S4650.

---

## PDF page 191

CHAPITRE 5                             Extensions et modifications

Sujet 1
Utilisation des technologies d'extension                                            185

Sujet 2
Ajout de nouvelles zones                                                            191

Sujet 3
Ajustement des listes dans l'Administration des ventes                              197
Exercice 12: Utilisation de fonctions de liste standard                  205

Sujet 4
Configuration de la sélection de zones pour les fiches article                      211

Sujet 5
Définition de références de zone pour les fiches article                            218
Exercice 13: Ajustement des options de sélection de zones              227

Sujet 6
Modification du système à l'aide des technologies d'extension classiques            235

Sujet 7
Modification du système à l'aide de la structure d'extension                        249

OBJECTIFS DU CHAPITRE

●   Utiliser les technologies d'extension
●   Ajouter de nouvelles zones avec la technique de conditions
●   Ajouter de nouvelles zones sans la technique de conditions
●   Utiliser des zones de réserve dans les données de base
●   Ajuster les listes dans l'Administration des ventes

---

## PDF page 192

Chapitre 5: Extensions et modifications

●   Configuration de la sélection de zones pour les fiches article
●   Définir des références de zone pour les fiches article
●   Utiliser des routines
●   Implémenter un exit utilisateur
●   Utiliser un exit client
●   Utiliser des Business Transaction Events
●   Utiliser des Business Add-Ins classiques
●   Utiliser un point d'extension
●   Accéder aux options d'extension

---

## PDF page 193

Chapitre 5
    Sujet 1
Utilisation des technologies d'extension

VUE D'ENSEMBLE DU SUJET
Ce sujet est consacré aux méthodes permettant de procéder à l'extension d'un système SAP
S/4HANA.

Exemple de gestion
Vous devez procéder à l'extension d'un système SAP S/4HANA existant pour couvrir des
besoins supplémentaires propres à un client. Pour cette raison, vous devez disposer des
connaissances suivantes :
●   Compréhension du concept de modification du système et de la terminologie associée
●   Compréhension des types d'extensions disponibles
●   Compréhension des techniques d'extension utilisables

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Utiliser les technologies d'extension

Vue d'ensemble des technologies d'extension
Il existe de nombreuses approches et techniques permettant d'adapter les paramétrages
d'un système SAP S/4HANA.

Customizing
Si vous utilisez le Customizing, vous pouvez configurer des processus de gestion et
Business Functions spécifiques pour votre système en vous servant du Guide
d'implémentation (IMG). Le Guide d'implémentation contient des tables du Customizing
dans lesquelles vous définissez ou sélectionnez des paramètres du Customizing pour
choisir la variante de processus ou de fonction standard que vous souhaitez utiliser.
Ces variantes doivent avoir été préconfigurées par le développeur d'application. Le
programme d'application standard ne fait qu'interpréter les paramétrages du
Customizing. Cela signifie que vous ne pouvez personnaliser que ce qui a été
préconfiguré dans le programme standard par le développeur d'application.
Modification
Contrairement à vos besoins, votre système SAP S/4HANA est adaptable à bien des
égards. Le code source est ouvert et vous pouvez trouver les outils dont vous avez besoin
dans ABAP Workbench. Cependant, toute modification est problématique. Modifier le
système, cela implique en effet de modifier les objets du référentiel SAP directement
dans le système client.

---

## PDF page 194

Chapitre 5: Extensions et modifications

Et si SAP fournit une nouvelle version de l'objet modifié avec un Support Package ou
dans le cadre d'un projet de montée de version, il convient alors de procéder à une
comparaison des modifications.
Extensions
Si vos besoins ne peuvent faire l'objet d'aucune adaptation, vous pouvez utiliser des
extensions ou des développements client. Les extensions vous permettent d'adapter les
objets du référentiel SAP sans qu'il soit besoin de les modifier. Elles pourraient être
comparées à des crochets dont seraient dotés les objets du référentiel SAP, crochets
que vous pourriez utiliser pour fixer vos propres objets. Il existe de nombreuses
techniques permettant de procéder à l'extension d'un système.
Développements client
L'utilisation de développements client s'accompagne de la création de nouveaux objets
du référentiel (propres au client) dans l'espace nom client. Les développements client
sont des programmes développés par le client dont le mode de fonctionnement peut ou
non impliquer l'appel d'objets du référentiel SAP. Par exemple, les clients peuvent créer
des programmes appelant des modules fonction SAP.

Définition des modifications

Figure 51: Définition des modifications

Est considéré comme modification tout ajustement dans votre système d'un objet fourni par
SAP. Dans le système SAP dans lequel il a fait l'objet de son développement initial, un objet du
référentiel est un objet d'origine. Dans votre système client, chaque objet du référentiel SAP
n'existe que sous forme de copie. Il est possible de modifier des copies, mais c'est une
pratique dangereuse.
Lors d'une montée de version, tout objet SAP ayant été modifié dans votre système risque
d'être écrasé par une nouvelle version de ce même objet fournie par SAP. Vous devez alors
procéder à une comparaison des modifications pour rétablir la ou les modifications que vous

---

## PDF page 195

Sujet: Utilisation des technologies d'extension

aviez apportées à votre système. Ce faisant, vous devez comparer l'ancienne version que
vous aviez modifiée à la version nouvellement fournie et copier les modifications
précédemment apportées à l'ancienne version standard dans la nouvelle version livrée par
SAP. Cette opération peut être très longue et vous risquez de faire des erreurs. Avant la
version 4.0B, les modifications n'étaient enregistrées qu'au niveau de l'objet du référentiel
(par exemple, un programme INCLUDE). Depuis la version 4.5A, la granularité
d'enregistrement des modifications est plus fine, ceci grâce à l'assistant de modification.
Il est par conséquent plus intéressant d'utiliser une extension SAP plutôt que de procéder à
une modification. Les extensions permettent elles aussi d'adapter les fonctionnalités de votre
système SAP, mais ne dépendent pas de la version et nécessitent de ce fait beaucoup moins
de maintenance. Afin de préserver la cohérence entre le système de développement et les
systèmes aval, vous devez tout d'abord effectuer l'adaptation (comparaison des
modifications) dans le système de développement, puis transporter les objets modifiés dans
les systèmes aval (en validant la demande de modification que vous avez utilisée).
La modification d'un objet de référentiel d'origine est appelée correction. Vous pouvez
l'effectuer dans le cadre de tâches dites de développement ou de correction. En revanche, la
modification d'une copie est appelée réparation. Vous pouvez l'effectuer dans le cadre de
tâches dites de réparation. La modification d'un référentiel SAP au niveau d'un système client
peut donc être qualifiée de réparation.
À chaque fois qu'un développeur crée ou modifie un objet du référentiel pour la première fois,
le système lui demande sa clé de développeur. Le développeur peut obtenir cette clé au
moyen d'une unique procédure d'enregistrement appelée SAP Software Change Registration
(SSCR). La clé de développeur est liée à l'ID utilisateur du développeur et au numéro de
licence du système SAP.
Le développeur a besoin d'une clé d'accès liée à l'objet (clé d'objet) pour chaque objet du
référentiel SAP à modifier. Il peut l'obtenir au moyen d'un enregistrement d'objet SSCR. Tout
enregistrement doit s'accompagner de la spécification du nom de l'objet du référentiel, du
type d'objet, ainsi que du numéro de licence et de la version du système SAP.

Types d'extensions

 Figure 52: Types d'extensions

---

## PDF page 196

Chapitre 5: Extensions et modifications

La fonction d'une extension de programme est toujours d'appeler un objet dans l'espace nom
client. Les extensions de programme vous permettent d'exécuter une logique de programme
supplémentaire pour un programme d'application SAP.
Vous pouvez utiliser des extensions de menu pour ajouter des points dans un menu standard
SAP. Les points de menu supplémentaires s'intègrent à l'interface utilisateur. Dans la mesure
où cela a été prévu par le développeur SAP, vous pouvez changer le texte des points de menu
et les icônes après que le code de fonction a été implémenté.
Les exits d'écran vous permettent de faire en sorte que des objets supplémentaires
s'affichent dans un écran de programme d'application SAP. Vous pouvez les implémenter en
créant des écrans subordonnés, si possible avec la logique d'exécution. Vous devez
également procéder au transport de données.

Techniques d'extension

Figure 53: Techniques d'extension

Les techniques d'extension disponibles sont les suivantes :

Exit utilisateur
Un exit utilisateur est un point d'un programme SAP à partir duquel un sous-programme
propre au client peut être appelé.
Exit client
Un module fonction d'exit spécial est appelé par le programme d'application SAP. Ce
module fonction appartient à un groupe de fonctions géré par le système d'une manière
particulière.
Business Transaction Events (BTE)
Le programme d'application SAP appelle un module fonction de manière dynamique
dans l'espace nom client.
Business Add-Ins

---

## PDF page 197

Sujet: Utilisation des technologies d'extension

  Le programme d'application appelle une méthode ou instance de classe. Cette classe ou
  instance se trouve dans l'espace nom client.
Points d'extension
  Situés dans des programmes, modules fonction et méthodes SAP, les points d'extension
  sont des endroits au niveau desquels les clients peuvent ajouter une logique
  supplémentaire sous la forme de code source sans avoir à apporter de modification.
Sections d'extension
  Les sections d'extension sont explicitement fournies par SAP pour que les clients
  puissent remplacer un bloc de code source SAP par leur propre logique sans avoir à
  apporter de modification.

Comment utiliser les technologies d'extension
This demonstration shows participants which options are available for specific installations.

1. In Customizing for Sales and Distribution, choose System Modifications → User Exits.
  At this point in the Customizing, there are several enhancement options available, in a
  number of areas.

2. Explain to the participants the differences between the enhancement options.

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●     Utiliser les technologies d'extension

---

## PDF page 198

Chapitre 5: Extensions et modifications

---

## PDF page 199

Chapitre 5
    Sujet 2
Ajout de nouvelles zones

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment modifier le système standard. Vous pouvez utiliser des zones
existantes ou en ajouter des nouvelles en procédant à quelques ajustements.

Exemple de gestion
Lors d'un projet d'implémentation, il peut vous être demandé de modifier les transactions
SAP pour répondre à des besoins clients que ne peuvent satisfaire les options standard du
Customizing. Vous devez utiliser les interfaces du système SAP de façon à ce que les
extensions s'appliquent à toutes les versions (aucune gestion ultérieure ne sera alors
nécessaire). Pour cette raison, vous devez disposer des connaissances suivantes :
●   Compréhension des alternatives que sont les solutions d'ajout de nouvelles zones et
l'utilisation de zones existantes
●   Compréhension des procédures de création de conditions et de formules

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Ajouter de nouvelles zones avec la technique de conditions
●   Ajouter de nouvelles zones sans la technique de conditions
●   Utiliser des zones de réserve dans les données de base

---

## PDF page 200

Chapitre 5: Extensions et modifications

Ajout de nouvelles zones avec la technique de conditions

Figure 54: Ajout de nouvelles zones avec la technique de conditions

Il est recommandé d'employer la technique de conditions pour adapter le système car de
nombreuses fonctions de la composante applicative SD l'utilisent également. Par exemple, la
détermination du prix, le pilotage des messages, la détermination des comptes, la liste
d'articles, l'exclusion et la substitution utilisent cette technique pour déterminer les prix ou les
messages.
Dans chaque composante, toutes les zones autorisées pour l'accès aux enregistrements de
conditions sont regroupées dans leurs propres structures de communication. Les structures
de communication comprennent donc toutes les zones de données utilisables lors de l'accès
à une table de conditions.
Vous ne pouvez analyser que les zones contenues dans la structure de communication
appropriées des séquences d'accès des différentes applications de la technique de
conditions.
Les INCLUDES dans lesquels vous pouvez ajouter de nouvelles zones de données sont liés
aux structures de communication correspondantes. Le système ne les remplace pas lors
d'une montée de version.
Les explications détaillées disponibles dans le Customizing expliquent la procédure d'ajout de
nouvelles zones à l'aide de la technique de conditions. Pour la consulter, recherchez Reprise
de nouvelles zones (via la technique des conditions).

Ajout de nouvelles zones

---

## PDF page 201

Sujet: Ajout de nouvelles zones

1. In Customizing for Sales and Distribution, choose System Adaptation → Create New Fields
(Using Condition Technique) → New Fields for Pricing.

2. Select Use INCLUDE for new fields in Dictionary (batch determtn). Choose Choose.

3. In the ABAP Dictionary: Initial Screen , select the Database table radio button.

4. In the text box next to the Database table button, enter KOMK and choose Display. You may
get a warning about language conflicts. Choose to maintain text in the logon language.
The KOMK structure is displayed.

5. Explain in general terms the contents of the table.

6. Choose the Find button. In the Scan Component List pop-up window, enter KOMKAZ and
choose Close (Enter).
The KOMKAZ include module is displayed.

7. Discuss appended field ZZKVGR1, in particular how it uses standard field KVGR1 as its
template.

8. It may be clearer for the delegates if you now repeat step 4 but search specifically for
KOMKAZ.

Ajout de nouvelles zones sans la technique de conditions

 Figure 55: Ajout de nouvelles zones sans la technique de conditions

         Remarque :
         La procédure d'ajout de nouvelles zones pour l'impression de documents est
         présentée dans le chapitre consacré au traitement des messages.

---

## PDF page 202

Chapitre 5: Extensions et modifications

Le système copie les zones de la base de données clients dans le document de vente en
procédant comme suit :
1. Une zone de la table de la base de données clients (KNA1 ou KNVV) est copiée par
l'INCLUDE (KUAGVZ, KUWEVZ, KURGVZ, et KUREVZ) dans la vue donneur d'ordre,
réceptionnaire ou payeur (KUAGV, KUWEV, KURGV ou KUREV). Un exit utilisateur
(V05E...) permet de transférer cette zone dans la vue à partir des données de base.

2. La zone est copiée de la vue client respective (KUAGV, KUWEV, KURGV, ou KUREV) dans
la table des commandes (VBAK, VBKD, ou VBAP). La zone est remplie dans le programme
MV45AFZZ par un user exit (USEREXIT_MOVE_FIELD_TO_VBAK (_VBAP,_VBKD)).

Le système copie les zones de la base de données articles dans le document de vente en
procédant comme suit :
1. Une zone de la table de la base de données articles (MARA, MARC, ou MVKE) est copiée
dans la vue article (MAAPV ou MAEPV) à l'aide de la structure append.

2. Le système copie ensuite la zone de la vue article dans la table des postes de commande
client (VBAP). Un exit utilisateur (USEREXIT_MOVE_FIELD_TO_VBAP) permet de
renseigner cette zone dans le programme MV45AFZZ.

Comment ajouter de nouvelles zones sans la technique de conditions
In this demonstration, you show how to print different fields on a billing document in the
structure VBDKR.

1. In Customizing for Sales and Distribution, choose System Adaptation → Create New Fields
(Without Condition Technique) → New Fields for Printing Documents.

2. Choose Use INCLUDE for new fields in Dictionary (document print) and choose Choose.

3. Enter the structure VBDKR, and choose Display.

4. Switch to Change mode and add a new row for the WADAT_IST (delivery date) field.

5. Save your changes.

---

## PDF page 203

Sujet: Ajout de nouvelles zones

Zones de réserve dans les bases de données clients et articles

 Figure 56: Zones de réserve dans les bases de données clients et articles

Vous pouvez utiliser des zones de réserve pour toutes les fonctions. Elles sont mémorisées
dans la fiche client. Vous pouvez les renseigner avec une valeur spécifique et les utiliser dans
des cas particuliers.
Des zones différentes sont utilisées pour les données générales de la fiche client et pour les
données du domaine commercial. Cinq zones de trois caractères sont également incluses
dans la fiche article (MVKE).
Vous pouvez saisir des zones pour la gestion de la fiche article dans la vue SD : données 2 de
l'organisation commerciale.
Il existe des tables de contrôle applicables à chaque zone que vous pouvez utiliser pour
spécifier les valeurs autorisées.

         Astuce :
         Si vous voulez utiliser l'une des zones de réserve, vous devez indiquer son nom.
         Vous pouvez le faire dans la transaction CMOD en sélectionnant
         Saut → Extensions globales → Mots-clés → Modifier.
         Comme il s'agit de zones SAP, le système remplace à nouveau ces noms lors
         d'une montée de version. Le même menu comprend donc le point Restaurer
         client et vous permet de restaurer vos noms.

Comment utiliser une zone de réserve dans les données de base

1. Enter a short text for data element KVGR1 as Billing Variant.

---

## PDF page 204

Chapitre 5: Extensions et modifications

a) On the SAP Easy Access screen, choose Tools → ABAP Workbench → Utilities →
Enhancements → Project Management (transaction CMOD).

b) On the Project Management of SAP Enhancements screen, choose Goto → Text
enhancements → Keywords → Change.

c) In the Change Keywords window, enter data element KVGR1 and choose Change.

d) Enter a short description of Billing Variant, depending on the lengths of the available
fields, and save your data.
A message appears informing you that the data element is activated asynchronously.

2. In the relevant checking table, define the list of allowed values.
a) In Customizing for Sales and Distribution, choose Master Data → Business
Partners → Customers → Sales → Maintain Reserve Fields in Customer Master..

b) In the Select Activity pop-up window, select Customer group 1. Choose the Choose
button.

c) The table is currently empty. Choose the New Entries button and enter the following:

●   Blank = STANDARD

●   001 = SPECIAL

Save these entries.

3. Assign the attribute 001 SPECIAL (for example, monthly consolidated billing) to customer
C650-B00.
a) Launch transaction BP. Access customer C650-B00 in change mode, specify BP Role
FLCU01 Customer (defined), select Sales and Distribution and enter Sales Organization
1010, Distribution Channel 10 and Division 00.

b) Select the Additional Data tab. In field Billing Variant (originally Customer Group 1),
enter 001. Save your change.

4. Create a sales order for customer C650-B00 and two items (materials P650-100 and
P650-200). Show that the Billing Variant field is activated and populated in the Additional
Data A tab for the order header.

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Ajouter de nouvelles zones avec la technique de conditions
●   Ajouter de nouvelles zones sans la technique de conditions
●   Utiliser des zones de réserve dans les données de base

---

## PDF page 205

Chapitre 5
     Sujet 3
Ajustement des listes dans l'Administration
des ventes

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment ajuster les listes dans l'Administration des ventes (SD).

There are very flexible standard functions in SD. However, only using the enhancement
option for displayable fields can fulfill all potential customer requirements.

Exemple de gestion
Vous devez personnaliser des listes en fonction des besoins d'un groupe d'utilisateurs. Pour
cette raison, vous devez disposer des connaissances suivantes :
●    Comment utiliser les fonctions standard d'édition de liste dans le système d'administration
des ventes
●    Comment utiliser des variantes d'affichage pour adapter les fonctions d'édition de liste aux
besoins de certains groupes d'utilisateurs
●    Comment optimiser l'affichage des listes à l'aide de variantes d'affichage propres à des
utilisateurs

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●    Ajuster les listes dans l'Administration des ventes

---

## PDF page 206

Chapitre 5: Extensions et modifications

SAP List Viewer

Figure 57: Utilisation des listes à tous les niveaux

Dans de nombreux domaines du système SAP, les listes jouent un rôle essentiel car elles sont
utilisées pour l'organisation du travail quotidien de l'utilisateur final. Il est donc
particulièrement important que le système fournisse une large palette d'options de
personnalisation.
Des fonctions de listes permettent de rechercher et de vérifier des documents de vente dans
le système. Vous pouvez ainsi résoudre différents types de demandes de gestion grâce à ces
fonctions de listes.

Domaines d'information de SD
Les informations fournies par SD peuvent être classées en différents domaines :
●   Liens vers les documents de vente et les fiches articles permettant de rechercher des
opérations commerciales et d'afficher toutes les transactions liées à une fiche article
●   Liste des transactions ayant atteint une certaine phase, par exemple toutes les
commandes à expédier et toutes les offres valides actuellement
●   Flux de documents fournissant des informations susceptibles de permettre de répondre à
des questions telles que « quelles sont les commandes qui ont été copiées à partir
d'offres ? » et « dans quels documents de livraison et de facturation certains postes de
commande ont-ils été entrés ? »
●   Analyses, par exemple des commandes bloquées pour livraison ou des documents en
fonction de leur statut

---

## PDF page 207

Sujet: Ajustement des listes dans l'Administration des ventes

Liens entre les documents de vente et les données de base

 Figure 58: Liens entre les documents de vente et les données de base

Il existe une fonction de liste pour chaque document commercial. Vous pouvez l'utiliser pour
afficher les documents de vente concernant un client ou un article particulier. Vous pouvez
alors afficher tous les documents de vente ou juste les documents en cours.
Les documents de vente en cours sont, par exemple, les demandes et les offres qui ne sont
pas encore entièrement référencées ou les commandes qui ne sont pas encore livrées ou
facturées. Vous pouvez utiliser des critères de sélection supplémentaires pour limiter
davantage les données sélectionnées, par exemple en fonction du canal de distribution ou du
type de document. Vous pouvez modifier la structure de la liste dans les options du système.

---

## PDF page 208

Chapitre 5: Extensions et modifications

Exemple : liste des commandes clients

Figure 59: Exemple : liste des commandes clients

La fonction d'analyse peut être utilisée aux fins suivantes :
●  Utiliser les fonctions de recherche, de tri et de cumul pour traiter les données
sélectionnées. La fonction de recherche peut vous permettre de limiter la liste disponible.
●   Afficher des informations sur le statut de chaque document (par exemple, le statut
Terminé, Livré, Facturé).
●   Modifier l'affichage de la liste à l'aide des variantes d'affichage. Dans certaines listes, vous
pouvez également sauvegarder les variantes d'affichage que vous avez définies.
●   Appeler le document que vous souhaitez traiter depuis la liste.
●   Imprimer les listes ou les envoyer sous forme de document via SAPoffice.

---

## PDF page 209

Sujet: Ajustement des listes dans l'Administration des ventes

ABAP List Viewer - création d'une variante d'affichage

 Figure 60: ABAP List Viewer - création d'une variante d'affichage

Toutes les listes vous permettent de sélectionner l'une des variantes fournies avec le système
standard SAP et de modifier l'affichage de la liste.
Vous ne pouvez pas sauvegarder les modifications apportées à la variante d'affichage en
cours dans les listes ne contenant que les variantes standard SAP. Seules les variantes
d'affichage standard fournies par SAP sont proposées dans l'écran de sélection.
Dans certaines listes, vous pouvez sauvegarder vos propres variantes. Les variantes
d'affichage propres à des utilisateurs doivent commencer par une lettre (A-Z). Les variantes
d'affichage client standards disponibles pour tous les utilisateurs doivent commencer par une
barre oblique (/).
Vous pouvez consulter la documentation de l'outil ABAP List Viewer dans la bibliothèque SAP
sous CA → Composantes inter-applications.

Comment utiliser une liste de commandes

1. Display a work list for a customer.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution →
  Sales → Information System → Orders → List of Sales Orders.

b) In the Sold-to party field, enter C650-A00.

c) In the Material field, enter P650-100.

2. Display a layout for the order of materials.

---

## PDF page 210

Chapitre 5: Extensions et modifications

a) Choose Settings → Layouts → Choose.

b) In the Choose Layout dialog box, choose one of the layouts.

c) Note the differences between this new layout and the default layout.

Nouvelles zones pour la liste des commandes clients

Figure 61: Nouvelle zone pour la liste des commandes clients

Dans l'environnement illustré dans la figure, certaines demandes des clients ne peuvent être
satisfaites que par l'extension du catalogue de zones de base.

Comment utiliser de nouvelles zones pour la liste des commandes clients

1. Display the definition screen for layouts.
a) On the SAP Easy Access screen, choose Logistics → Sales and Distribution →
Sales → Information System → Orders → List of Sales Orders.

b) In the Sold-to party field, enter C650-A00.

c) In the Material field, enter P650-100.

d) Choose Execute.

e) Choose Settings → Layout → Current.
The definition screen for layouts displays.

2. Choose fields to display in the layout.
a) In the list of hidden fields, select Delivery Block and Billing Block.

---

## PDF page 211

Sujet: Ajustement des listes dans l'Administration des ventes

b) Choose Show Selected Fields.
  The field is copied to the Displayed Columns.

c) Choose Adopt.

---

## PDF page 212

Chapitre 5: Extensions et modifications

---

## PDF page 213

Chapitre 5
Exercice 12
Utilisation de fonctions de liste standard

Exemple de gestion
Les listes de documents et les analyses constituent une aide précieuse car elles permettent
aux employés du service client d'organiser leur travail quotidien et de répondre à de
nombreuses questions. Vous pouvez utiliser l'outil ABAP List Viewer pour adapter de
nombreuses fonctions d'information à vos besoins.

Réponse aux questions relatives aux commandes

1. Quelles sont les commandes passées par le client C650-A## depuis le début du mois ?

2. Qui a créé ces commandes dans le système ?

3. Affichez la zone Blocage livraison.

4. Combien de commandes le client a-t-il passées pour l'article P650-1## ?

Affichage de toutes les commandes et du statut d'un document

1. Affichez toutes les commandes concernant l'article P650-1##.

2. Affichez le statut du premier document.

Définition d'une nouvelle mise en forme pour l'affichage de la liste des commandes
Vous voulez maintenant définir une nouvelle mise en forme de la liste des commandes de
façon à visualiser immédiatement les blocages de la livraison et de la facture pour chaque
commande.

1. Modifiez la structure de la liste à l'aide de la mise en forme standard Commandes de façon
à ce que les zones correspondant aux blocages de livraison et de facture soient affichées.

---

## PDF page 214

Chapitre 5: Extensions et modifications

         Remarque :
         Le paramètre utilisateur SD_VARIANT_MAINTAIN est une condition préalable
         à la définition et l'administration de variantes d'affichage dans les rapports des
         ventes.
         Si ce paramètre contient la valeur « A », vous pouvez enregistrer aussi bien des
         variantes standard que des variantes propres à des utilisateurs.
         Si la valeur est « X », vous pouvez enregistrer uniquement des variantes
         standard.
         Si la valeur est « U », vous pouvez enregistrer uniquement des variantes
         propres à des utilisateurs.

2. Sauvegardez cette mise en forme de façon à ce que vous soyez le seul à pouvoir la
sélectionner. Saisissez un nom comprenant la chaîne de caractères S4650-##. Utilisez la
description Groupe de mise en forme ##.

3. Définissez la nouvelle mise en forme comme mise en forme initiale.

---

## PDF page 215

Chapitre 5
Solution 12
Utilisation de fonctions de liste standard

Exemple de gestion
Les listes de documents et les analyses constituent une aide précieuse car elles permettent
aux employés du service client d'organiser leur travail quotidien et de répondre à de
nombreuses questions. Vous pouvez utiliser l'outil ABAP List Viewer pour adapter de
nombreuses fonctions d'information à vos besoins.

Réponse aux questions relatives aux commandes

1. Quelles sont les commandes passées par le client C650-A## depuis le début du mois ?

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Système d'information → Commandes client → Liste des
  commandes client.

b) Dans l'écran Liste des commandes clients, saisissez C650-A## dans la zone Donneur
  d'ordre.

c) Appuyez sur Exécuter.

2. Qui a créé ces commandes dans le système ?

a) Dans l'écran Liste des commandes clients, notez les valeurs figurant dans la zone Créé
  par.
  Dans la ligne de chacune des commandes, l'auteur est indiqué par la valeur qui se
  trouve dans la zone Créé par.

3. Affichez la zone Blocage livraison.
a) Dans l'écran Liste des commandes clients, sélectionnez
  Options → Structure → Modifier.
  L'écran de définition des mises en forme s'affiche.

b) Dans la boîte de dialogue Modifier mise forme, sélectionnez Blocage livraison dans la
  liste de zones située sous Colonnes.

---

## PDF page 216

Chapitre 5: Extensions et modifications

             Remarque :
             Il est possible que cette zone ne soit pas visible en raison de la longueur de
             la liste. Si tel est le cas, utilisez la barre de défilement pour y accéder.

c) Cliquez sur Afficher zones sél. (flèche vers la gauche).
La zone est copiée dans la section Colonnes affichées.

d) Cliquez sur Reprendre.

4. Combien de commandes le client a-t-il passées pour l'article P650-1## ?
a) Sélectionnez Options → Structure → Sélectionner.

b) Dans la boîte de dialogue Sélectionner MeF, sélectionnez 1SAP Ordre - postes.

c) Cliquez sur Reprendre.

d) Dans l'écran Liste des commandes clients par partenaire - postes, sélectionnez la
colonne Article.

e) Cliquez sur Définir filtre.

f) Saisissez P650-1## dans la zone Article.

g) Cliquez sur Exécuter.

Affichage de toutes les commandes et du statut d'un document

1. Affichez toutes les commandes concernant l'article P650-1##.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
(ADV) → Vente → Système d'information → Commandes client → Liste des
commandes client.

b) Dans l'écran Liste des commandes clients, saisissez P650-1## dans la zone Article.

c) Appuyez sur Exécuter.

2. Affichez le statut du premier document.
a) Sélectionnez la première ligne de la table.

b) Sélectionnez Environnement → Statut du document.

Définition d'une nouvelle mise en forme pour l'affichage de la liste des commandes
Vous voulez maintenant définir une nouvelle mise en forme de la liste des commandes de
façon à visualiser immédiatement les blocages de la livraison et de la facture pour chaque
commande.

1. Modifiez la structure de la liste à l'aide de la mise en forme standard Commandes de façon
à ce que les zones correspondant aux blocages de livraison et de facture soient affichées.

---

## PDF page 217

Sujet: Ajustement des listes dans l'Administration des ventes

           Remarque :
           Le paramètre utilisateur SD_VARIANT_MAINTAIN est une condition préalable
           à la définition et l'administration de variantes d'affichage dans les rapports des
           ventes.
           Si ce paramètre contient la valeur « A », vous pouvez enregistrer aussi bien des
           variantes standard que des variantes propres à des utilisateurs.
           Si la valeur est « X », vous pouvez enregistrer uniquement des variantes
           standard.
           Si la valeur est « U », vous pouvez enregistrer uniquement des variantes
           propres à des utilisateurs.

a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Administration des ventes
  (ADV) → Vente → Système d'information → Commandes client → Liste des
  commandes client.

b) Dans l'écran Liste des commandes clients, saisissez le client C650-A## dans la zone
  Donneur d'ordre.

c) Appuyez sur Exécuter.

d) Cliquez sur Options → Structure → Modifier.
  L'écran de définition des mises en forme s'affiche.

e) Dans la liste des zones masquées, sélectionnez Blocage livraison et Blocage facture.

f) Cliquez sur Afficher zones sél. (flèche vers la gauche).
   La zone est copiée dans la section Colonnes affichées.

g) Cliquez sur Reprendre.

2. Sauvegardez cette mise en forme de façon à ce que vous soyez le seul à pouvoir la
sélectionner. Saisissez un nom comprenant la chaîne de caractères S4650-##. Utilisez la
description Groupe de mise en forme ##.
a) Sélectionnez Options → Structure → Sauvegarder en cours.

b) Saisissez le nom et la désignation.

c) Cliquez sur Reprendre.

3. Définissez la nouvelle mise en forme comme mise en forme initiale.
a) Sélectionnez Options → Structure → Gestion.

b) Sélectionnez la colonne Mise en forme qui contient votre mise en forme.

c) Dans l'écran Mise en forme : gestion, sélectionnez la ligne de votre mise en forme.

d) Cliquez sur Activer paramétrage, puis sauvegardez vos données.

---

## PDF page 218

Chapitre 5: Extensions et modifications

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Ajuster les listes dans l'Administration des ventes

---

## PDF page 219

Chapitre 5
    Sujet 4
Configuration de la sélection de zones pour les
fiches article

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Configuration de la sélection de zones pour les fiches article

Vue d'ensemble des options de sélection de zones
Les activités IMG de sélection de zones, lors de la gestion de la fiche article, vous permettent
d'indiquer si une zone doit être masquée, en lecture seule ou accessible en lecture et écriture.
Si la zone est accessible en lecture et écriture, vous pouvez préciser si l'entrée utilisateur est
obligatoire ou facultative.
Vous pouvez tenir compte de divers aspects avec des facteurs déterminants différents. Par
exemple, vous pouvez modifier la sélection de zones pour les articles d'un type donné ou ceux
appartenant à une branche ou une division donnée.

Groupes de sélection de zones et références de zone

 Figure 62: Affectation de zones aux groupes de sélection de zones

Lors du traitement d'une fiche article, plusieurs options de Customizing s'appliquent pour
déterminer la sélection de zones.

---

## PDF page 220

Chapitre 5: Extensions et modifications

Contrairement à d'autres applications, vous ne pouvez pas définir des options de sélection de
zones distinctes pour chacune des zones de la fiche article. Vous pouvez définir ces options
uniquement pour un groupe de zones.
Dans la gestion de la fiche article, l'attribut de zone est piloté par le groupe de sélection de
zones auquel appartient la zone concernée.

Pour chaque groupe de sélection de zones, vous pouvez définir les attributs suivants :
● Masquée
Si vous sélectionnez Masquée, les zones seront supprimées (invisibles) lors de la gestion
de la fiche article correspondante. Cet attribut convient aux zones dont votre entreprise
n'a pas besoin.
●   Affichée
Si vous sélectionnez Affichée, les zones seront affichées à l'écran, mais ne seront pas
accessibles en écriture.
Cet attribut convient aux zones renseignées au sein de votre entreprise (par exemple, au
moment du transfert de données) et dont les valeurs ne doivent pas être modifiées.
●   Entrée obligatoire
Si vous sélectionnez Entrée obligatoire, l'entrée utilisateur sera obligatoire dans ces zones.
Cet attribut convient aux zones qui doivent contenir des données renseignées par les
utilisateurs dans votre entreprise.

          Attention :
          La saisie est requise pour certaines zones dans un système SAP. Ne masquez
          pas ces zones.

●   Entrée facultative
Si vous sélectionnez Entrée facultative, l'entrée utilisateur sera possible, mais non
obligatoire.
Cet attribut convient aux zones dans lesquelles la saisie n'est pas obligatoire, mais
souhaitable pour certaines informations, le cas échéant.

Vous pouvez modifier l'affectation des zones aux groupes de sélection de zones si certaines
zones d'un groupe de sélection de zones doivent être pilotées de manière différente. La
version actuelle de SAP comprend 240 groupes de sélection de zones, dont 40 sont réservés
pour les clients.

---

## PDF page 221

Sujet: Configuration de la sélection de zones pour les fiches article

Sélection de zones pour la fiche article - facteurs déterminants

 Figure 63: Sélection de zones pour la fiche article - facteurs déterminants

Plusieurs facteurs, comme le type d'article et la branche, influencent la sélection de zones.
Ces facteurs sont automatiquement déterminés à partir du contexte en cours.

La sélection de zones pour les fiches article dépend des facteurs suivants :
●  Transaction appelée par l'utilisateur
La sélection de zones sera différente si un utilisateur crée une fiche article ou si le système
affiche une fiche article.
●   Type d'approvisionnement (E ou F) de l'article concerné
La sélection de zones pour les articles en fabrication interne diffère de celle pour les
articles en approvisionnement externe.
●   Type d'article
Vous pouvez définir une sélection de zones propre à chaque type d'article à l'aide d'une
référence de zone. Vous ne pouvez pas exercer une influence sur les zones au niveau du
mandant (table MARA) en fonction d'une division.
●   Division effective
Vous pouvez définir une sélection de zones propre à chaque division à l'aide d'une
référence de zone.
●   Branche affectée à l'article
Vous pouvez définir une sélection de zones distincte pour les articles appartenant à la
branche Industrie chimique et ceux appartenant à la branche Distribution de détail.
●   Système SAP

---

## PDF page 222

Chapitre 5: Extensions et modifications

Vous pouvez définir les références de zone de la livraison SAP, qui s'appliquent en tenant
compte de la solution SAP (solution métier, SAP for Retail ou solution de gestion) et du
niveau de version utilisé. Chaque système SAP possède ses propres options de sélection
de zones à la livraison.

Références de zone

Figure 64: Références de zone

Les références de zone pilotent la sélection de zones. Dans le Customizing, vous pouvez
affecter des références de zone aux facteurs déterminants suivants : type d'article, division et
branche. SAP gère l'affectation d'une référence de zone aux codes de transaction, aux types
d'approvisionnement et à la livraison SAP. Vous ne pouvez pas modifier l'affectation de ces
références de zone dans le Customizing.
Dans le système standard, la plupart des clés des références de zone coïncident avec celles
des facteurs déterminants.

Voici des exemples de références de zone pour différents facteurs déterminants :
●  Type d'article
Référence de zone ROH pour le type d'article ROH (matière première)
●   Division
Référence de zone 0001 pour la division 0001
●   Branche
Référence de zone M pour la branche M (construction mécanique)
●   Transaction
Référence de zone MM01 pour la transaction Créer article (transaction MM01)

●   Type d'approvisionnement

---

## PDF page 223

Sujet: Configuration de la sélection de zones pour les fiches article

Référence de zone E pour les articles avec le type d'approvisionnement E (fabrication
interne)

Si vous avez besoin de modifier la sélection de zones, vous devrez peut-être affecter des
zones à d'autres groupes de sélection de zone.
Vous modifiez le pilotage de sélection de zones via les références de zone. La référence de
zone à modifier dans le processus dépend du facteur déterminant. Par exemple, si votre
modification doit affecter tous les articles de la branche Construction mécanique, modifiez la
référence de zone M.

Groupes de sélection de zones et références de zone

 Figure 65: Groupes de sélection de zones et références de zone

Plusieurs références de zone sont utilisées pour piloter la sélection de zones. Le système relie
les entrées de toutes les références de zone applicables à la transaction concernée.

---

## PDF page 224

Chapitre 5: Extensions et modifications

Attributs de zone et règles de liaison

Figure 66: Attributs de zone et règles de liaison

Les règles de liaison illustrées dans la figure déterminent le résultat de la sélection de zones
pour chaque groupe de sélection de zones. Les règles de liaison sont prédéfinies dans le
système SAP et vous ne pouvez pas les modifier.

Les symboles de la figure revêtent la signification suivante :

Symbole                                                   Signification
–                                                         Masquée
*                                                         Affichée
+                                                         Entrée obligatoire
.                                                         Entrée facultative

Comme illustré dans la figure, si les attributs sont différents, l'attribut avec la priorité la plus
élevée s'applique toujours à chaque groupe de sélection de zones.

Pour configurer la sélection de zones pour les fiches article

1. Identifiez le groupe de sélection de zones contenant la zone à modifier.

2. Déterminez si d'autres zones appartiennent à ce groupe de sélection de zones.

3. Vérifiez si la modification apportée à la sélection de zones doit également s'appliquer aux
autres zones dans le groupe de sélection de zones concerné.

4. Identifiez le facteur déterminant pour la modification de la sélection de zones (type
d'article, par exemple).

---

## PDF page 225

Sujet: Configuration de la sélection de zones pour les fiches article

5. Identifiez la référence de zone actuelle pour ce facteur déterminant.

6. Modifiez la référence de zone ou créez une référence de zone reflétant vos modifications.

7. Testez votre paramétrage. Si vous créez une référence de zone, vous devez d'abord
l'affecter au facteur déterminant (type d'article, par exemple).

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Configuration de la sélection de zones pour les fiches article

---

## PDF page 226

Chapitre 5
  Sujet 5
Définition de références de zone pour les
fiches article

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Définir des références de zone pour les fiches article

Options de la sélection de zones dans le système SAP

Figure 67: Affectation de zones aux groupes de sélection de zones

La figure illustre l'affectation de groupes de sélection de zones aux zones de la fiche article
dans le Customizing.
Vous pouvez utiliser les fonctions disponibles en bas de l'écran pour retrier les entrées de
table ou positionner rapidement le curseur sur une entrée de table donnée. Avant de modifier
le regroupement, affichez une vue d'ensemble du regroupement actuel à l'aide des fonctions
d'impression et d'affichage. Vous pouvez appeler cette fonction depuis la barre de menus via
Vue de table → Imprimer.

---

## PDF page 227

Sujet: Définition de références de zone pour les fiches article

         Astuce :
         Si vous sélectionnez une zone et accédez aux détails, vous trouverez l'attribut
         Proposer contenu de zone. Cet attribut indique que le contenu de zone est
         proposé d'après l'article de référence lors de la création d'une fiche article à
         l'aide d'un article de référence.

Vous pouvez également cliquer sur       (Gestion de la sélection de zones) pour accéder
directement à la gestion de la sélection de zones pour les zones figurant dans ce groupe de
sélection de zones.

Références de zone

 Figure 68: Gestion des références de zone

La figure illustre la gestion des zones appartenant au groupe de sélection de zones 14 dans le
Customizing. Les zones affectées à ce groupe apparaissent dans le bloc supérieur.
Dans la partie centrale de l'écran, vous pouvez choisir si les zones du groupe de sélection de
zones affiché doivent être masquées, en lecture seule ou accessibles en lecture et en écriture
en tant que zones facultatives ou obligatoires. Ces options de variantes de zone sont rangées,
de gauche à droite, de la plus prioritaire à la moins prioritaire, ce qui signifie que le masquage
de zones présente la priorité la plus élevée.
Vous pouvez utiliser les fonctions disponibles en bas de l'écran pour retrier les entrées de
table ou positionner rapidement le curseur sur une entrée de table donnée.
Le système SAP contient des références de zone qui s'appliquent à l'ensemble du mandant.
Les références de zone SAP1 et SAP2 s'appliquent au système SAP standard (solutions

---

## PDF page 228

Chapitre 5: Extensions et modifications

métier). Quant à SAPR, il s'applique aux mandants SAP for Retail. Évitez de modifier ces
références de zone.
Le système SAP comporte la référence de zone KB, valide pour tous les types de mandants.
Si vous modifiez la sélection de zones au niveau du mandant, ajustez cette référence de zone
selon les besoins de votre entreprise.

Utilisez la fonction       (Cas d'emploi) pour consulter l'utilisation qui est faite d'une référence
de zone donnée.

Cas d'emploi d'une référence de zone

Figure 69: Cas d'emploi d'une référence de zone

La référence de zone MM02, par exemple, est un facteur déterminant valide lors de l'appel des
transactions MM02, MM18, MM42 et MMZ2.

---

## PDF page 229

Sujet: Définition de références de zone pour les fiches article

Affectation d'une référence de zone à une division

 Figure 70: Affectation d'une référence de zone à une division

La figure illustre l'affectation de références de zone à différentes divisions dans le
Customizing.

---

## PDF page 230

Chapitre 5: Extensions et modifications

Facteurs déterminants pour la sélection de zones

Figure 71: Zones à geler

Il existe d'autres dépendances logiques aux options de zone. Lorsque vous saisissez FX (code
de taille de lot fixe) dans la zone Taille du lot sous Planification des besoins en composants
(MRP) dans la page à onglet Planif.des besoins 1 de la vue standard, par exemple, la zone
Taille de lot fixe devient obligatoire.
Autre exemple : la zone Groupe march. dans la vue Données de base 1. Cette zone devient
obligatoire lorsque vous sélectionnez des données achats pour la création d'une fiche article.
Vous pouvez définir des zones à geler dans la fiche article. Cette fonction est disponible
uniquement dans les fiches article des solutions métier, et non dans les fiches pour SAP for
Retail. Dans le Customizing, vous indiquez les zones de la fiche article à geler.
Si vous gelez une fiche article, les zones marquées comme devant être gelées dans le
Customizing ne peuvent plus être modifiées lors de la gestion de la fiche article. Dans la boîte
de dialogue illustrée dans la figure, les zones marquées ne sont plus accessibles en écriture, à
l'exception des zones obligatoires dans lesquelles vous devez saisir des données lorsque vous
complétez une fiche article. Les zones sont gelées à compter de la sauvegarde de la fiche
article dans le système.
Si vous marquez une zone de la fiche article comme devant être gelée alors que des
modifications sont déjà planifiées pour cette zone, ces modifications ne seront pas prises en
compte. Vous pouvez geler une fiche article à tout moment lors de la gestion de la fiche
article. Vous ne pouvez annuler le gel que si vous disposez de l'autorisation correspondante et
si l'article n'est pas soumis à la gestion de la configuration.

L'objet d'autorisation pertinent se nomme M_MATE_MAF :
●  Activité 16 : l'utilisateur peut geler les fiches article

---

## PDF page 231

Sujet: Définition de références de zone pour les fiches article

●     Activité 51 : l'utilisateur peut annuler le gel d'une fiche article

Vous pouvez également geler des fiches article et annuler cette opération grâce à la gestion
en masse (zone MARA-MATFI).

Comment ajuster les options pour la sélection de zones article

Business Example
You wish to make General Item Category a mandatory field for materials of Material Type
YR##.
For all other material types, the field should remain optional.
Change the field selection settings for materials of Material Type YR00.

1. Identify the Field Selection Groupfor the General Item Category field.
  a) On the SAP Easy Access screen, choose Logistics → Materials Management → Material
     Master → Change → Immediately (transaction: MM02).

  b) On the Change Material (Initial Screen), enter material P650-100 in the Material field
     and choose the Select View(s) button.

  c) In the Select Views dialog box, select the Basic Data 1 view and choose Continue
     (Enter).

  d) On the Change Material P650-100 (Trading Goods) screen (for the Basic data 1 tab),
     select the GenItemCatGroup field. Show that this can be deleted without triggering a
     message or causing the mandatory field (tick) icon to appear.

  e) Place the cursor on this field and press F1 to open the Performance Assistant dialog
     box.

  f) Choose the Technical Information button. Show that the Table Name is MARA and the
     Field Name is MTPOS_MARA.

  g) In Customizing, go to Logistics → General → Material Master → Field
     Selection → Assign Fields to Field Selection Groups.

  h) On the Change View “Field Groups”: Overview screen, choose the Position on Field
     Name button.

  i) In the Another Entry pop-up window, enter Field Name MARA-MTPOS_MARA. Choose
     the Continue (Enter) button. The field is assigned to Field Selection Group 137.

2. Check whether the Field Selection Group contains any further fields.
  a) a) Choose the Sort by Field Selection Grp button and position on Field Selection Group
     137.
     The only field in Field Selection Group 137 is General Item Category Group. Hence you
     do not need to move this field to a different Field Selection Group.

3. The influencing factor in this scenario is Material Type YR00. Review the Material Type and
identify its field reference.
  a) In Customizing, go to Logistics → General → Material Master → Basic
     Settings → Material Types → Define Attributes of Material Types.

---

## PDF page 232

Chapitre 5: Extensions et modifications

b) On the Change View “Material Types”: Overview screen, select the line for Material
Type YR00. Choose Details.

c) c) On the Change View “Material Types”: Details screen, it is clear that Material Type
YR00 has field reference ROH. The new field selection should apply only to Material
Type YR00, hence a new field reference should be created and assigned to the
Material Type.

4. Specify the new field reference for the desired influencing factor.
a) In Customizing, go to Logistics → General → Material Master → Field
Selection → Maintain Field Selection for Data Screens.

b) On the Change View “Field Selection for Data Screens”: Overview screen, in the Field
selection (Field selection group 1) screen, scroll down to find Field ref. ROH, select it
and choose the Copy as… button.

c) On the Change View “Field Selection for Data Screens”: Details of Selected screen,
overwrite ROH in the Field reference field with new value ZM00 and choose the Apply
(Enter) button.

d) Enter 137 in the sel grp field. Choose the Enter button.

e) In the table with title Field Selection (Field selection group 137), select the Reqd Entry
radio button for Field ref. ZM00. Save and return to the Customizing screen.

5. Assign the new field reference to the desired influencing factor.
a) In Customizing, go to Logistics → General → Material Master → Basic
Settings → Material Types → Define Attributes of Material Types.

b) On the Change View “Material Types”: Overview screen, select the line for Material
Type YR00 - Material Type Group 00. Choose Details.

c) On the Change View “Material types”: Details screen, enter ZM00 in the Field reference
field.

d) Save.
You do not need to consider other influencing factors because the field is optional in
the standard system.

6. Test the change.
a) On the SAP Easy Access screen, choose Logistics → Material Management → Material
Master → Material → Create (General) → Immediately. (transaction MM01).

b) On the Create Material (Initial Screen), select Material Type YR00 Material Type Group
00 and Industry Sector 1 Retail. Choose the Select View(s) button.

c) In the Select View(s) dialog box, choose the Basic Data 1 view and choose Continue
(Enter).

d) On the Create Material (Mat Type Group 00) screen (for the Basic data 1 tab), the
GenItemCatGroup field is now a mandatory field.

e) Return to the SAP Easy Access screen without saving.

f) On the SAP Easy Access screen, choose Logistics → Material Management → Material
Master → Material → Create (General) → Immediately. (transaction MM01).

---

## PDF page 233

Sujet: Définition de références de zone pour les fiches article

g) On the Create Material (Initial Screen), select Material Type HAWA Trading Goods and
  Industry Sector 1 Retail. Choose the Select View(s) button.

h) In the Select View(s) dialog box, choose the Basic Data 1 view and choose Continue
  (Enter).

i) On the Create Material (Trading Goods) screen (for the Basic data 1 tab), the value in
   the GenItemCatGroup field is set to a default of NORM. This can be deleted and is
   clearly still an optional field.

j) Return to the SAP Easy Access screen without saving.

---

## PDF page 234

Chapitre 5: Extensions et modifications

---

## PDF page 235

Chapitre 5
Exercice 13
Ajustement des options de sélection de zones

Exemple de gestion
Vous souhaitez faire de Division chargée de la livraison une zone obligatoire pour les articles
de type YR##.
Pour tous les autres types d'articles, cette zone doit rester facultative.
Modifiez les options de sélection de zones pour les articles de type YR##.

Décrire les étapes relatives au paramétrage de la sélection de zones pour un nouveau
type d'article
Avant d'effectuer les paramétrages de personnalisation requis pour la sélection de zones,
notez les étapes et les entrées nécessaires.

Étape 1 :

Étape 2 :

Étape 3 :

Étape 4 :

Étape 5 :

---

## PDF page 236

Chapitre 5: Extensions et modifications

Étape 6 :

Étape 7 :

1. Effectuez les étapes et les entrées nécessaires avant de définir les options de Customizing
pour la sélection de zones. Afin de paramétrer les options de Customizing pour la
sélection de zones, exécutez les étapes suivantes :

Exécuter les étapes relatives au paramétrage requis de la sélection de zones
Faites de Division chargée de la livraison une zone requise (obligatoire). Pour ce faire, utilisez
une nouvelle référence de zone avec la clé ZM##. La modification doit s'appliquer
uniquement pour le type d'article YR##. Ne modifiez aucune option susceptible d'affecter les
autres groupes de l'exercice ou une personnalisation standard.

1. Exécutez l'étape 1 pour identifier le groupe de sélection de zones pour la zone Division
chargée de la livraison.

2. Exécutez l'étape 2 pour identifier si le groupe de sélection de zones contient des zones
supplémentaires.

3. L'étape 3 n'est pas pertinente pour cet exercice pour les raisons décrites ci-dessus.

4. Exécutez l'étape 4 pour déterminer le facteur déterminant de modification de la sélection
de zones.
Le facteur déterminant dans ce scénario est le Type d'article. Le type d'article YR## doit
rendre la zone Division chargée de la livraison obligatoire, tandis que le type d'article
HAWA, par exemple, doit la conserver comme zone facultative.

5. Exécutez l'étape 5 pour déterminer la référence de zone actuelle pour le facteur
déterminant souhaité. Dans ce scénario, il s'agit de la référence de zone affectée au type
d'article YR##.

6. Exécutez l'étape 6 pour déterminer la nouvelle référence de zone et l'affecter au facteur
déterminant souhaité.

7. Exécutez l'étape 7 pour tester vos modifications.

---

## PDF page 237

Chapitre 5
Solution 13
Ajustement des options de sélection de zones

Exemple de gestion
Vous souhaitez faire de Division chargée de la livraison une zone obligatoire pour les articles
de type YR##.
Pour tous les autres types d'articles, cette zone doit rester facultative.
Modifiez les options de sélection de zones pour les articles de type YR##.

Décrire les étapes relatives au paramétrage de la sélection de zones pour un nouveau
type d'article
Avant d'effectuer les paramétrages de personnalisation requis pour la sélection de zones,
notez les étapes et les entrées nécessaires.

Étape 1 :

Étape 2 :

Étape 3 :

Étape 4 :

Étape 5 :

---

## PDF page 238

Chapitre 5: Extensions et modifications

Étape 6 :

Étape 7 :

1. Effectuez les étapes et les entrées nécessaires avant de définir les options de Customizing
pour la sélection de zones. Afin de paramétrer les options de Customizing pour la
sélection de zones, exécutez les étapes suivantes :
a) Étape 1 : identifiez le groupe de sélection de zones auquel appartient la zone.

b) Étape 2 : vérifiez si d'autres zones figurent dans ce groupe de sélection de zones.

c) Étape 3 : s'il existe d'autres zones dans ce groupe de sélection de zones, choisissez
d'appliquer ou non la sélection de zones à ces autres zones, étant donné que la
sélection de zones peut uniquement être définie pour des groupes de sélection de
zones. Si vous souhaitez appliquer la sélection de zones, aucune autre action n'est
requise. Si vous ne souhaitez pas appliquer la sélection de zones, affectez la zone à un
autre groupe de sélection de zones (vide, si possible) dans l'espace nom client.

d) Étape 4 : Identifiez le facteur déterminant pour la modification de la sélection de zones
(type d'article, par exemple).

e) Étape 5 : identifiez la référence de zone actuelle pour le facteur déterminant souhaité.

f) Étape 6 : Modifiez la référence de zone ou créez une référence reflétant vos
modifications. Si vous créez une référence, affectez-la au facteur déterminant.

g) Étape 7 : Testez votre paramétrage.

Exécuter les étapes relatives au paramétrage requis de la sélection de zones
Faites de Division chargée de la livraison une zone requise (obligatoire). Pour ce faire, utilisez
une nouvelle référence de zone avec la clé ZM##. La modification doit s'appliquer
uniquement pour le type d'article YR##. Ne modifiez aucune option susceptible d'affecter les
autres groupes de l'exercice ou une personnalisation standard.

1. Exécutez l'étape 1 pour identifier le groupe de sélection de zones pour la zone Division
chargée de la livraison.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Gestion des articles → Fiche
article → Article → Modifier → Immédiatement (TRANSACTION MM02).

b) Dans l'écran Modifier article (Écran initial), saisissez le numéro d'article P650-1##
dans la zone Article et cliquez sur le bouton Sélection des vues.

c) Dans la boîte de dialogue Sélection des vues, sélectionnez la vue ADV: données org.
commerciale 1 et cliquez sur Suite (Entrée).

---

## PDF page 239

Sujet: Définition de références de zone pour les fiches article

d) Dans la boîte de dialogue Nvx organisationnels, saisissez 1010 dans la zone Org.
  commerciale et saisissez 10 dans la zone Canal distrib. Sélectionnez Suite (Entrée).

e) Dans l'écran Modifier article P650-1## (Prod. commercialisables) (pour l'onglet ADV:
  org. commerc. 1), essayez de supprimer la valeur de la zone Division livraison. Cette
  opération est possible, ce qui montre que la zone est une zone facultative dans les
  articles de type Produits commercialisables.

f) Sélectionnez la zone Division livraison et appuyez sur F1 pour ouvrir la boîte de
   dialogue Assistant de performance.

g) Cliquez sur le bouton Informations techniques. Notez le nom de table et le nom de zone
  pour la zone.

h) Revenez à l'écran SAP Easy Access, sans sauvegarder les modifications.

i) Dans le Customizing, sélectionnez Logistique → Données générales → Fiche
   article → Options de zone → Affecter zones aux groupes d'options de zones.

j) Dans l'écran Modifier vue "Groupes de zones" : synthèse, cliquez sur le bouton
   Positionner sur nom de zone.

k) Dans la boîte de dialogue Autre entrée, saisissez Nom de zone MVKE-DWERK. Cliquez
  sur le bouton Suite (Entrée). La zone est affectée au Groupe de sélection de zones 95.

l) Restez dans cet écran pour l'étape 2.

2. Exécutez l'étape 2 pour identifier si le groupe de sélection de zones contient des zones
supplémentaires.
a) Cliquez sur le bouton Trier par groupe de sélection de zones et faites défiler jusqu'au
  Groupe de sélection de zones 95.
   La seule zone dans le groupe de sélection de zones 95 est Division chargée de la
   livraison (plus sa description). Vous n'avez donc pas besoin de déplacer ces zones vers
   un autre groupe de sélection de zones.

b) Revenez à l'écran Afficher guide d'implémentation.

3. L'étape 3 n'est pas pertinente pour cet exercice pour les raisons décrites ci-dessus.

4. Exécutez l'étape 4 pour déterminer le facteur déterminant de modification de la sélection
de zones.
Le facteur déterminant dans ce scénario est le Type d'article. Le type d'article YR## doit
rendre la zone Division chargée de la livraison obligatoire, tandis que le type d'article
HAWA, par exemple, doit la conserver comme zone facultative.

5. Exécutez l'étape 5 pour déterminer la référence de zone actuelle pour le facteur
déterminant souhaité. Dans ce scénario, il s'agit de la référence de zone affectée au type
d'article YR##.
a) Dans le Customizing, sélectionnez Logistique → Données générales → Fiche
  article → Options de base → Types d'articles → Déterminer propriétés des types
  d'articles.

b) Dans l'écran Modifier vue "Types d'articles" : synthèse, cliquez sur le bouton
  Positionner. Dans la boîte de dialogue Autre entrée, saisissez le type d'article YR##,
  puis sélectionnez Suite (Entrée).

---

## PDF page 240

Chapitre 5: Extensions et modifications

c) Sélectionnez la ligne pour le type d'article YR##. Cliquez sur Détails.

d) Dans l'écran Modifier vue "Types d'articles" : détail, le type d'article YR## présente la
référence de zone ROH. En effet, le type d'article a été copié depuis le type d'article
ROH. La nouvelle sélection de zones doit s'appliquer uniquement au type d'article
YR##, par conséquent vous devez créer une nouvelle référence de zone et l'affecter à
ce type d'article.

e) Revenez à l'écran Afficher guide d'implémentation.

6. Exécutez l'étape 6 pour déterminer la nouvelle référence de zone et l'affecter au facteur
déterminant souhaité.
a) Dans le Customizing, sélectionnez Logistique → Données générales → Fiche
article → Options de zone → Gérer options de zone pour écran de données.

b) Dans l'écran Modifier vue "Sélection de zones écrans de données" : synthèse, dans
l'écran Sélection zones (groupe sélection zones 1), sélectionnez le bouton Positionner.
Dans la boîte de dialogue Autre entrée, saisissez la référence zone ROH et cliquez sur le
bouton Suite.

c) Dans la table étiquetée Sélection zones (groupe sélection zones 1), sélectionnez
l'entrée pour ROH et cliquez sur le bouton Copier sous…

d) Dans l'écran Modifier vue "Sélection de zones écrans de données" : détails ensemble,
remplacez ROH dans la zone Référence zone par la nouvelle valeur ZM## et cliquez
sur le bouton Reprendre (Entrée).

e) Saisissez 95 dans la zone Grpe sélect. zones. Cliquez sur le bouton Entrée.

f) Dans la table avec le titre Sélection zones (Groupe sélection zones 95), sélectionnez la
case d'option Entr. obl. pour la référence de zone ZM##.

g) Sauvegardez vos données et retournez à l'écran du Customizing.

h) Dans le Customizing, sélectionnez Logistique → Données générales → Fiche
article → Options de base → Types d'articles → Déterminer propriétés des types
d'articles.

i) Dans l'écran Modifier vue "Types d'articles" : synthèse, faites défiler et sélectionnez la
ligne pour Type d'article YR# # - Groupe de types d'article ##. Cliquez sur Détails.

j) Dans l'écran Modifier vue "Types d'articles" : détails, saisissez ZM## dans la zone
Référence de zone.

k) Sauvegardez vos données et retournez à l'écran du Customizing.
Vous n'avez pas besoin de tenir compte d'autres facteurs déterminants puisque cette
zone est facultative dans le système standard.

7. Exécutez l'étape 7 pour tester vos modifications.
a) Dans l'écran SAP Easy Access, sélectionnez Logistique → Gestion des articles → Fiche
article → Article → Créer (général) → Immédiatement (TRANSACTION MM01).

b) Dans l'écran Créer article (Écran initial), sélectionnez le type d'article YR## Groupe de
types d'articles ## et la branche 1 Commerce. Sélectionnez le bouton Sélection des
vues.

---

## PDF page 241

Sujet: Définition de références de zone pour les fiches article

c) Dans la boîte de dialogue Sélectionner les vues, saisissez ADV : données org.
  commerciale 1 et cliquez sur Suite (Entrée).

d) Dans la boîte de dialogue Nvx organisationnels, saisissez 1010 dans la zone Org.
  commerciale et saisissez 10 dans la zone Canal distrib. Sélectionnez Suite (Entrée).

e) Dans l'écran Créer article (Groupe de types d'article Groupe ##) (pour l'onglet ADV :
  org. comm. 1), la zone Division chargée de la livraison est maintenant une zone
  obligatoire.

f) Revenez à l'écran SAP Easy Access.

g) Dans l'écran SAP Easy Access, sélectionnez Logistique → Gestion des articles → Fiche
  article → Article → Créer (général) → Immédiatement (TRANSACTION MM01).

h) Dans l'écran Créer article (Écran initial), sélectionnez le type d'article HAWA Produits
  commercialisables et la branche 1 Commerce. Sélectionnez le bouton Sélection des
  vues.

i) Dans la boîte de dialogue Sélectionner les vues, saisissez ADV : données org.
   commerciale 1 et cliquez sur Suite (Entrée).

j) Dans la boîte de dialogue Nvx organisationnels, saisissez 1010 dans la zone Org.
   commerciale et saisissez 10 dans la zone Canal distrib. Sélectionnez Suite (Entrée).

k) Dans l'écran Créer article (Produits commercialisables) (pour les ventes : onglet Org.
  comm. 1), la zone Division chargée de la livraison est toujours une zone facultative.

l) Revenez à l'écran SAP Easy Access.

---

## PDF page 242

Chapitre 5: Extensions et modifications

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Définir des références de zone pour les fiches article

---

## PDF page 243

Chapitre 5
     Sujet 6
Modification du système à l'aide des
technologies d'extension classiques

VUE D'ENSEMBLE DU SUJET
Ce sujet explique comment modifier le système dans l'Administration des ventes (SD).

This lesson introduces the elements of the SAP enhancement concept to non-developers. It
also focuses on the use of a reserve field (KNVV-KVGR1) to implement a function that was
release independent.

Exemple de gestion
Lors d'un projet d'implémentation, il peut vous être demandé de modifier les transactions
SAP pour répondre à des besoins clients que ne peuvent satisfaire les options standard du
Customizing. Vous devez utiliser les interfaces du système SAP de façon à ce que les
extensions s'appliquent à toutes les versions (aucune gestion ultérieure ne sera alors
nécessaire). Pour cette raison, vous devez disposer des connaissances suivantes :
●    Compréhension des options du Customizing permettant de modifier le système
indépendamment de sa version
●    Compréhension du concept d'extension SAP

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●    Utiliser des routines
●    Implémenter un exit utilisateur
●    Utiliser un exit client
●    Utiliser des Business Transaction Events
●    Utiliser des Business Add-Ins classiques

---

## PDF page 244

Chapitre 5: Extensions et modifications

Routines

Figure 72: Exemple d'une routine client

Les routines sont des sous-programmes courts exécutant différentes fonctions lors du
traitement des documents.

Dans SD, vous pouvez utiliser la transaction VOFM pour créer et traiter des routines pour
les fonctions suivantes :
●  Conditions de copie
Les conditions de copie indiquent si le système peut ou non autoriser la copie. Elles
peuvent stipuler, par exemple, que le même client doit figurer dans l'en-tête du document
si vous copiez une demande d'offre client dans une offre.
●   Transferts de données
Les routines de transfert de données sont des programmes ABAP qui assurent le transfert
des données source vers le document que vous créez. Elles peuvent spécifier, par
exemple, que certaines zones de postes ne peuvent être copiées que parallèlement à
d'autres zones, et ce uniquement dans des contrats, des avoirs et des notes de débit.
●   Conditions et formules
Les routines relatives aux conditions et aux formules sont utilisées pour les fonctions
ayant recours à la technique de conditions. Une condition peut rendre l'exécution d'un
accès dépendante de certaines vérifications. Elle vérifie par exemple si la devise du
document est la même que la devise interne.

La détermination des prix se base sur des formules pour définir une logique spécifique. Vous
ne pouvez pas configurer cette logique en utilisant uniquement le Customizing standard.

---

## PDF page 245

Sujet: Modification du système à l'aide des technologies d'extension classiques

Exits utilisateur

 Figure 73: Exit utilisateur

Un exit utilisateur est un point d'un programme SAP à partir duquel un sous-programme
propre au client peut être appelé. Ce sous-programme est traité dans des INCLUDES
spéciaux.
Ces INCLUDES sont spéciaux de par leur mode d'utilisation (et non pour des raisons
techniques). Ils contiennent des routines FORM vides qui sont les exits utilisateur. Ces
routines sont appelées par les programmes de traitement correspondants. Elles ne sont
fournies qu'une seule fois lors de l'implémentation du système et ne sont jamais remplacées.
Les clients peuvent traiter leurs propres sous-programmes à ce niveau.

       Remarque :
       La règle selon laquelle les exits utilisateur ne sont fournis qu'initialement et jamais
       remplacés connaît des exceptions pour certaines solutions métier. Dans IS-OIL
       par exemple, des exits utilisateur dotés d'un code actif sont également fournis
       pour les versions antérieures à SAP R/3 4.7 dans le cadre d'ajustements propres à
       la branche concernée.

L'appel du sous-programme s'effectue au même endroit. Grâce à ces conventions, vous
pouvez procéder à l'extension des programmes SAP indépendamment de la version et sans
avoir à effectuer d'adaptation à la suite d'une comparaison des modifications. Les exits
utilisateur sont par conséquent considérés comme étant des modifications.

---

## PDF page 246

Chapitre 5: Extensions et modifications

    Remarque :
    Pour plus d'informations, voir la note SAP 381348.

Les exits utilisateur disponibles se trouvent dans le Customizing sous Administration des
ventes (ADV) → Adaptation du système → Exits utilisateur. Pour chacun des chemins
disponibles, vous avez accès à une documentation spécifique, aux exits utilisateur disponibles
et à des informations sur leur utilisation.

Comment implémenter un exit utilisateur

    Remarque :
    This is an optional demonstration.

In the demonstration for reserve fields, we saw how reserve field KVGR1 had been replicated
to communication structure KOMK (in INCLUDE KOMKAZ) as ZZKVGR1. The field has been
relabelled as “Billing Variant”, hence we might now want to use it as a basis for customer
pricing, for example, the customer receives a discount if field KVGR1 is set to ‘001’ in the
customer master.
In order to implement this, the field value must be assigned from field KVGR1 in the sales
document to field ZZKVGR1 in the communication structure. This is performed in a user exit.

1. In Customizing for Sales and Distribution, choose System Adaptation → Create New Fields
(Using Condition Technique) → New Fields for Pricing

2. In the Select Activity pop-up window, select Use user exit for new fields (batch
determination). Choose the Choose button.

3. On the ABAP Editor: Initial Screen screen, enter MV45AFZZ in the Program field, ensure the
Source Code radio button is activated, and select the Change button. Ignore any pop-up
information boxes that appear.

4. On the ABAP Editor: Modify Include MV45AFZZ screen, scroll down the source code until
you find the routine named FORM USEREXIT_PRICING_PREPARE_TKOMK. Explain that
this is the dedicated routine for assigning new header-level document fields and that it
currently contains no executable code. It has only FORM and ENDFORM statements (i.e.
start and end), plus a line of code marked as a comment (* in column 1).

5. Place the cursor on the line under the FORM statement and select the Insert Line Area
button.

6. In the highlighted new line, delete the * in column 1 and enter the following line of
code:TKOMK-ZZKVGR1 = VBAK-KVGR1.
If you wish, you can cut and paste the comment line and use this as the basis for the above
code.

7. Select the Check button. Ensure the system returns the message No syntax errors found
in include MV45AFZZ.

8. Select the Activate button. You will be prompted to create a transport request at this
point. Ensure the system returns the message Object activated.

---

## PDF page 247

Sujet: Modification du système à l'aide des technologies d'extension classiques

If you wish (and time permits), you can demonstrate how it is now possible to use field
KVGR1/ZZKVGR1 (Billing Variant) as a key field for pricing condition records. In order to
do this, perform the following steps in the pricing areas of Customizing and master data:

9. Add field ZZKVGR1 to the field catalog.

10. Create a condition table containing field ZZKVGR1.

11. Use this condition table as the reference for an access in a new access sequence.

12. Create a new condition type (e.g. a discount) and assign it to the above access sequence.

13. Include the new condition type in a new pricing procedure (or perhaps include it in the
standard one).

14. Check that pricing procedure determination will determine this pricing procedure.

15. Create a pricing condition record of the new type.

16. Test by raising a customer order and ensuring this condition record has been used.

Exits client

 Figure 74: Exit client

Les exits client permettent aux clients d'étendre leurs fonctions applicatives. Ils sont
préplanifiés par SAP et sont généralement constitués de plusieurs composantes.
Les programmeurs d'application SAP créent des extensions SAP à partir d'exits de
programme, de menu et d'écran. Une fonction de gestion est fournie à cet effet (code de
transaction SMOD).

---

## PDF page 248

Chapitre 5: Extensions et modifications

Les clients reçoivent un catalogue contenant une vue d'ensemble des extensions SAP
existantes. Ils peuvent ensuite utiliser la transaction CMOD pour combiner les extensions SAP
de leur choix afin de constituer un projet d'extension.
Les extensions SAP sont constituées de composantes : exits de programme, de menu et
d'écran. Chaque composante ne peut être utilisée qu'une seule fois dans une seule extension
SAP (ce qui garantit l'unicité de chaque extension SAP). SAP combine toutes les
composantes d'extension qui constituent ensemble une extension.
Les projets d'extension client sont constitués d'extensions SAP. Chaque extension SAP ne
peut être utilisée qu'une seule fois dans un seul projet d'extension client (ce qui garantit
l'unicité de chaque projet client). Le client doit traiter toutes les extensions qui doivent être
activées ensemble dans le cadre d'un projet d'extension.

Exits client - exemple d'exits de programme : architecture

Figure 75: Exit client - exemple d'exits de programme : architecture

Le module fonction d'exit est appelé à un point donné du code source. Ce point est défini par
le développeur d'application SAP. Au sein du module fonction, à l'aide d'un INCLUDE, il est
possible d'ajouter une fonction dans l'espace nom client.

---

## PDF page 249

Sujet: Modification du système à l'aide des technologies d'extension classiques

Exit de module fonction SDVFX004

 Figure 76: Exemple : exit de module fonction SDVFX004

Le développeur d'application SAP détermine où il est possible d'appeler un module fonction
dans une transaction et définit les données transférées. Le développeur crée également les
modules fonction correspondants avec désignation, interface et documentation.
La documentation SAP décrit les fonctions incluses dans un exit de module fonction.

Comment utiliser des exits client

         Remarque :
         This demo is an optional demo.

Customer exits are used as enhancements of the standard.

1. Using transaction CMOD, create a new project and link it to the enhancement.
a) On the SAP Easy Access screen, choose Tools → ABAP Workbench → Utilities →
  Enhancements → Project Management.

b) On the Project Management of SAP Enhancements screen, enter PROJ_650 in the
  Project field.

c) Choose Create.

d) Enter a short description of your choice in the Short text and choose Save.

e) In the Create Object Directory Entry dialog box, enter the package for your course and
  choose Save.

f) Choose Enhancements assignments and choose the necessary enhancement.

---

## PDF page 250

Chapitre 5: Extensions et modifications

g) Choose Components and choose the component you want to use.
The function module is displayed.

h) Choose one of the includes that begin with ZX.
The system displays a warning that this include will be created.

i) Choose Enter.
The system asks for a package and a transport request.

j) Enter the ABAP code into the selected include.

k) Activate the include program.

l) Return to the Project Management of SAP Enhancements screen and activate the
project.

Business Transaction Events (BTE)

Figure 77: Business Transaction Events (BTE)

Tout comme les exits de programme, les Business Transaction Events vous permettent
d'implémenter une logique supplémentaire dans du code standard. Les programmeurs
d'application SAP déterminent où il est possible de placer des Business Transaction Events
dans le code standard et définissent les données transférées par le système au niveau de
chaque point.
Ils créent également des modules fonction modèles comprenant des désignations, une
interface (paramètres de module fonction) et de la documentation et décrivent les fonctions
possibles avec l'extension dans la documentation SAP associée.

---

## PDF page 251

Sujet: Modification du système à l'aide des technologies d'extension classiques

Interfaces de publication et de souscription et interfaces de processus

 Figure 78: Interfaces de publication et de souscription et interfaces de processus

Interfaces de publication et de souscription
Les interfaces de publication et de souscription vous signalent que des événements
spécifiques se sont produits dans l'application standard SAP. Les données créées sont
par conséquent disponibles dans le logiciel externe. Le logiciel externe ne renvoie pas de
données au système standard SAP.
Interfaces de processus
Il s'agit d'interfaces utilisées pour soumettre des processus de gestion à une autre
commande non implémentée dans le système standard. En d'autres termes, ces
interfaces de processus remplacent les processus standard.

Vous pouvez connecter des développements externes au système standard SAP. Les
développements supplémentaires sont réalisés, en règle générale, dans l'ABAP Workbench.

---

## PDF page 252

Chapitre 5: Extensions et modifications

Business Transaction Events : implémentation

Figure 79: Implémentation d'un Business Transaction Event

Vous pouvez utiliser la transaction FIBF (qui est appelée lorsque vous sélectionnez l'option
Utiliser des Business Transaction Events dans la hiérarchie Comptabilité financière) pour
effectuer toutes les activités requises préalablement à l'utilisation d'un Business Transaction
Event.
Utilisez l'ABAP Workbench pour copier le module fonction modèle SAMPLE_INTERFACE_<N>
dans l'espace nom client (Z_*) d'un groupe de fonctions client. Vous pouvez tout d'abord
regarder l'interface dans la transaction FIBF afin de déterminer ce que doivent être les
paramètres du module fonction et de lire la documentation pour savoir à quoi ils servent.
Vous ne devez pas modifier l'interface lors de la copie du module fonction. Vous pouvez
ajouter le code source de votre choix dans le module fonction, à l'exception toutefois de
l'instruction COMMIT WORK.
Une fois le module créé, vous devez créer un produit dans l'écran d'administration.
Vous devez ensuite affecter le module fonction et le produit au numéro d'événement, puis
enfin marquer le produit comme actif.

Comment utiliser des Business Transaction Events

    Remarque :
    This demo is an optional demo.

1. Show existing interfaces.

---

## PDF page 253

Sujet: Modification du système à l'aide des technologies d'extension classiques

a) Navigate to Customizing for Sales and Distribution under System Modifications →
  Business Transaction Events → Environment → Info system (P/S).

b) In the Selection Attrib. field, enter the field component SD.

c) Choose Execute.
  The existing P/S-interfaces display.

d) For any event, choose Documentation.

e) Return to the Customizing screen.

f) Go to Customizing for Sales and Distribution under System Modifications → Business
   Transaction Events → Environment → Infosystem(Processes).

g) In the Selection Attrib. field, enter the field component SD.

h) Choose Execute.
  Existing process interfaces are display.

i) For any process, choose Documentation.

Business Add-Ins classiques

 Figure 80: Architecture des Business Add-Ins classiques

Contrairement aux exits client, les Business Add-Ins (BAdI) prennent en compte les
modifications apportées au processus de livraison du logiciel. Dans la figure des Business
Add-Ins classiques : architecture, la partie supérieure représente l'écosystème de livraison
type. Celui-ci n'est plus uniquement constitué du fournisseur et de l'utilisateur, mais peut
également intégrer une véritable chaîne de prestataires intermédiaires.

---

## PDF page 254

Chapitre 5: Extensions et modifications

La partie inférieure de la figure représente le mode de fonctionnement des Business Add-Ins.
Un programme d'application SAP fournit l'option d'extension. Cela requiert au moins une
interface, laquelle est associée à une classe d'adaptateurs de Business Add-In ayant pour
fonction de l'implémenter.
L'interface est implémentée par l'utilisateur qui souhaite se servir du Business Add-In.
La force de ce concept réside dans sa réutilisabilité. Tout Business Add-In peut en effet être
implémenté de nombreuses fois, et ce même à chaque fois par un intervenant plus proche de
la fin de la chaîne de livraison du logiciel. Les Business Add-Ins permettent également à
chaque intervenant de proposer des extensions.

Composantes des Business Add-Ins
Les composantes devant être créées lors de la définition d'un Business Add-In sont les
suivantes :
●   Interface
●   Classe générée (classe d'adaptateurs du Business Add-In) qui implémente l'interface

La classe générée (classe d'adaptateurs du Business Add-In) effectue les tâches suivantes :
●   Filtrage
Si des implémentations sont créées pour un Business Add-In dépendant d'un filtre, la
classe d'adaptateurs du Business Add-In garantit que seules les implémentations
appropriées seront appelées.
●   Pilotage
La classe d'adaptateurs du Business Add-In appelle les implémentations actives.

Chaque Business Add-In peut contenir des extensions de programme, de menu et d'écran
(composantes).

---

## PDF page 255

Sujet: Modification du système à l'aide des technologies d'extension classiques

Flux d'un exit de programme pour les Business Add-Ins

 Figure 81: Flux d'un exit de programme pour les Business Add-Ins

La figure représente le flux de processus d'un programme contenant un appel de Business
Add-In.
Une variable faisant référence à l'interface BAdI doit être déclarée dans la partie appropriée
du programme.
Une référence objet (instance de la classe d'adaptateurs du Business Add-In) est générée
dans la première étape par l'appel de la méthode GET_INSTANCE de la classe de service
CL_EXITHANDLER. Cet objet est ensuite utilisé pour appeler la ou les méthodes d'extension
de programme.
Dans la deuxième étape, la méthode d'interface de la classe BAdI est appelée. À ce niveau,
toutes les implémentations actives du Business Add-In sont déterminées, puis les méthodes
implémentées sont appelées.

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Utiliser des routines
●   Implémenter un exit utilisateur
●   Utiliser un exit client
●   Utiliser des Business Transaction Events
●   Utiliser des Business Add-Ins classiques

---

## PDF page 256

Chapitre 5: Extensions et modifications

---

## PDF page 257

Chapitre 5
    Sujet 7
Modification du système à l'aide de la
structure d'extension

VUE D'ENSEMBLE DU SUJET
Ce sujet décrit la structure d'extension et la fonction des points, options et sections
d'extension.

Exemple de gestion
Vous voulez utiliser les nouvelles fonctionnalités de la structure d'extension pour étendre vos
fonctions SAP sans avoir à apporter de modification. Pour cette raison, vous devez disposer
des connaissances suivantes :
●   Compréhension des extensions disponibles dans la structure d'extension
●   Compréhension des points d'extension
●   Compréhension du mode d'accès aux options d'extension

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :
●   Utiliser un point d'extension
●   Accéder aux options d'extension

Extensions de la structure d'extension

 Figure 82: Vue d'ensemble des extensions de la structure d'extension

Outre les nouvelles options d'extension (points/options et sections d'extension), les Business
Add-Ins sont eux aussi gérés dans la structure d'extension. À partir de SAP NetWeaver 7.0,
SAP a modifié la technologie des Business Add-Ins afin d'améliorer les performances. Les
futures extensions seront implémentées à l'aide de la technologie des Business Add-Ins.

---

## PDF page 258

Chapitre 5: Extensions et modifications

Toutefois, le système contient une grande variété d'exits qui ont été implémentés à l'aide de
la technologie des Business Add-Ins classiques. Il est donc intéressant que chacun puisse
avoir une vue d'ensemble de l'utilisation des Business Add-Ins classiques.

Points d'extension

Figure 83: Points d'extension

Les points d'extension sont des endroits des programmes SAP au niveau desquels les clients
peuvent ajouter des fonctions complémentaires sous la forme de code source sans avoir à
apporter de modification. Les points d'extension implicites se situent à certains niveaux du
programme SAP et ne sont pas fournis explicitement par les développeurs SAP. Les points
d'extension explicites sont des points d'extension fournis par les développeurs SAP.

Sections d'extension

Figure 84: Section d'extension

Une section d'extension est une option fournie explicitement par SAP pour le remplacement
d'un bloc de code source SAP par du code source du client.

---

## PDF page 259

Sujet: Modification du système à l'aide de la structure d'extension

Options d'extension
Grâce aux options d'extension, vous pouvez définir les éléments suivants sans avoir à
apporter de modification :
●   Paramètres d'interface (optionnels) supplémentaires dans les modules fonction et
méthodes SAP
●   Attributs et méthodes supplémentaires dans les classes SAP
●   Fonctions de préparation ou de post-traitement pour les méthodes SAP globales
●   Remplacements pour les méthodes SAP globales

Les options d'extension sont toujours implicitement disponibles. Les clients peuvent les
utiliser pour procéder à l'extension des définitions des classes SAP ainsi que des interfaces
des modules fonction et méthodes SAP.

         Astuce :
         Des points et options d'extension implicites existent également dans les objets
         SAP développés avant SAP NetWeaver 7.0.

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :
●   Utiliser un point d'extension
●   Accéder aux options d'extension

---

## PDF page 260

Chapitre 5: Extensions et modifications

---

## PDF page 261

Chapitre 5

Évaluation des connaissances

1. Parmi les objets suivants, lesquels relèvent des technologies d'extension ?
Sélectionnez les réponses correctes.

X    A Données altérables

X    B Développements client

X    C Modification

X    D Données de base

2. Un Business Add-In (BAdI) est une section définie du code source que SAP fournit pour
que le client puisse la remplacer par son propre code.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

3. Parmi les fonctions suivantes de l'Administration des ventes, lesquelles utilisent la
technique de conditions pour la modification du système ?
Sélectionnez les réponses correctes.

X    A Détermination du prix

X    B Pilotage des messages

X    C Détermination des comptes

X    D Contrôle de disponibilité

4. Des zones de réserve sont disponibles dans les objets de données de base des bases de
données clients et articles.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

---

## PDF page 262

Chapitre 5: Évaluation des connaissances

5. Parmi les fonctions d'analyse suivantes, lesquelles pouvez-vous utiliser pour ajuster les
listes ?
Sélectionnez les réponses correctes.

X    A Tri

X    B Affichage

X    C Cumul

X    D Filtre

6. Dans ABAP List Viewer, vous pouvez sauvegarder les modifications apportées à la
variante d'affichage en cours dans les listes ne contenant que les variantes standard SAP.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

7. Parmi les fonctions suivantes, pour lesquelles pouvez-vous créer et traiter des routines à
l'aide de la transaction VOFM ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Transferts de données

X    C Flux de documents

X    D Conditions et formules

8. Une extension SAP peut être réutilisée plusieurs fois dans un même projet d'extension
client.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

---

## PDF page 263

Chapitre 5: Évaluation des connaissances

9. Parmi les propositions suivantes, lesquelles sont vraies pour ce qui est des Business
Transaction Events ?
Sélectionnez les réponses correctes.

X    A Des composantes supplémentaires peuvent être associées au système SAP.

X    B Des interfaces prédéfinies permettent l'accès client.

X    C La logique supplémentaire est toujours définie par SAP.

X    D Deux implémentations peuvent coexister sans problème.

10. Parmi les options suivantes, lesquelles peuvent être gérées dans la structure d'extension ?
Sélectionnez les réponses correctes.

X    A Workbench de modification

X    B Business Add-Ins classiques

X    C Points d'extension explicites

X    D Nouveaux Business Add-Ins

---

## PDF page 264

Chapitre 5

Évaluation des connaissances - Réponses

1. Parmi les objets suivants, lesquels relèvent des technologies d'extension ?
Sélectionnez les réponses correctes.

X   A Données altérables

X   B Développements client

X   C Modification

X   D Données de base

Correct ! Les technologies d'extension SAP englobent les développements client et les
modifications. Les données altérables et les données de base sont des objets de données
de gestion. Pour en savoir plus, reportez-vous au sujet Utilisation des technologies
d'extension (Chapitre 5, Sujet 1) dans le cours S4650.

2. Un Business Add-In (BAdI) est une section définie du code source que SAP fournit pour
que le client puisse la remplacer par son propre code.
Indiquez si cette proposition est vraie ou fausse.

X   Vrai

X   Faux

Correct ! Un Business Add-In (BAdI) est une méthode ou une instance de classe qu'un
client peut développer sans avoir à modifier le code source SAP. Pour en savoir plus,
reportez-vous au sujet Utilisation des technologies d'extension (Chapitre 5, Sujet 6) dans
le cours S4650.

---

## PDF page 265

Chapitre 5: Évaluation des connaissances - Réponses

3. Parmi les fonctions suivantes de l'Administration des ventes, lesquelles utilisent la
technique de conditions pour la modification du système ?
Sélectionnez les réponses correctes.

X    A Détermination du prix

X    B Pilotage des messages

X    C Détermination des comptes

X    D Contrôle de disponibilité

Correct ! La technique de conditions dans l'Administration des ventes est utilisée pour
modifier les fonctionnalités de détermination du prix, de pilotage des messages et de
détermination des comptes. Le contrôle de disponibilité ne passe pas par la technique des
conditions. Pour en savoir plus, reportez-vous au sujet Ajout de nouvelles zones
(Chapitre 5, Sujet 2) dans le cours S4650.

4. Des zones de réserve sont disponibles dans les objets de données de base des bases de
données clients et articles.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! Plusieurs zones de réserve sont mises à la disposition des clients dans les tables
des bases de données clients et articles. Pour en savoir plus, reportez-vous au sujet Ajout
de nouvelles zones (Chapitre 5, Sujet 2) dans le cours S4650.

5. Parmi les fonctions d'analyse suivantes, lesquelles pouvez-vous utiliser pour ajuster les
listes ?
Sélectionnez les réponses correctes.

X    A Tri

X    B Affichage

X    C Cumul

X    D Filtre

Correct ! Pour ajuster les listes, vous pouvez afficher les fonctions d'analyse de type Tri,
Cumul et Filtre. Affichage n'est pas une fonction d'analyse. Pour en savoir plus, reportez-
vous au sujet Ajustement des listes dans l'Administration des ventes (Chapitre 5, Sujet 3)
dans le cours S4650.

---

## PDF page 266

Chapitre 5: Évaluation des connaissances - Réponses

6. Dans ABAP List Viewer, vous pouvez sauvegarder les modifications apportées à la
variante d'affichage en cours dans les listes ne contenant que les variantes standard SAP.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! À l'aide d'ABAP List Viewer, vous pouvez apporter des modifications à tout type
de variante, aussi bien les variantes standard SAP que les variantes propres aux
utilisateurs. Pour en savoir plus, reportez-vous au sujet Ajustement des listes dans
l'Administration des ventes (Chapitre 5, Sujet 3) dans le cours S4650.

7. Parmi les fonctions suivantes, pour lesquelles pouvez-vous créer et traiter des routines à
l'aide de la transaction VOFM ?
Sélectionnez les réponses correctes.

X    A Conditions de copie

X    B Transferts de données

X    C Flux de documents

X    D Conditions et formules

Correct ! Vous pouvez utiliser la transaction VOFM afin de créer des routines pour les
conditions de copie, des transferts de données ainsi que des conditions et formules dans
la détermination du prix. VOFM ne permet pas de créer des routines qui influencent le flux
de documents. Pour en savoir plus, reportez-vous au sujet Modification du système à
l'aide des technologies d'extension classiques (Chapitre 5, Sujet 6) dans le cours S4650.

8. Une extension SAP peut être réutilisée plusieurs fois dans un même projet d'extension
client.
Indiquez si cette proposition est vraie ou fausse.

X    Vrai

X    Faux

Correct ! Les extensions SAP ne peuvent pas être réutilisées plusieurs fois dans un même
projet d'extension client. Pour en savoir plus, reportez-vous au sujet Modification du
système à l'aide des technologies d'extension classiques (Chapitre 5, Sujet 6) dans le
cours S4650.

---

## PDF page 267

Chapitre 5: Évaluation des connaissances - Réponses

9. Parmi les propositions suivantes, lesquelles sont vraies pour ce qui est des Business
Transaction Events ?
Sélectionnez les réponses correctes.

X    A Des composantes supplémentaires peuvent être associées au système SAP.

X    B Des interfaces prédéfinies permettent l'accès client.

X    C La logique supplémentaire est toujours définie par SAP.

X    D Deux implémentations peuvent coexister sans problème.

Correct ! Les Business Transaction Events (BTE) sont des composantes qui peuvent être
utilisées dans le système et fournissent une interface prédéfinie pour l'accès client. Elles
autorisent aussi la coexistence de deux implémentations sans conflit. La logique des
Business Transaction Events n'est pas définie par SAP, mais par le client. Pour en savoir
plus, reportez-vous au sujet Modification du système à l'aide des technologies d'extension
classiques (Chapitre 5, Sujet 6) dans le cours S4650.

10. Parmi les options suivantes, lesquelles peuvent être gérées dans la structure d'extension ?
Sélectionnez les réponses correctes.

X    A Workbench de modification

X    B Business Add-Ins classiques

X    C Points d'extension explicites

X    D Nouveaux Business Add-Ins

Correct ! La structure d'extension inclut les fonctionnalités suivantes : Business Add-Ins
classiques, points d'extension explicites et nouveaux Business Add-Ins. Le workbench de
modification ne fait pas partie de la structure d'extension. Pour en savoir plus, reportez-
vous au sujet Modification du système à l'aide des technologies d'extension classiques
(Chapitre 5, Sujet 7) dans le cours S4650.