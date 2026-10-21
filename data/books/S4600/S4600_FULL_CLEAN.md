# S4600 - Processus de vente dans S/4HANA

Source: support SAP S4600, version 23, 4 jours, article 50163026.

> Extraction nettoyée pour Codex. Numéros de pages = pages PDF (page de cours = page PDF - 10 à partir du chapitre 1). La mise en page, certains schémas et tableaux graphiques ne sont pas reproduits; consulter le PDF si un détail visuel est indispensable.


---

## PDF page 1

```text
S4600
Processus de vente dans S/4
HANA

.
.
SUPPORT DE COURS DU PARTICIPANT
COURS AVEC INSTRUCTEUR
.
Version du cours : 23
Durée du cours : 4 Jour(s)
Numéro d'article : 50163026
```

---

## PDF page 5

```text
Sommaire :

ix      Vue d'ensemble du cours

1       Chapitre 1 : Navigation avec SAP Fiori

2                     Sujet: Identification des fonctions clés de SAP Fiori
11                       Exercice 1 : Utilisation de la barre de lancement SAP Fiori

19      Chapitre 2 :Structures d'entreprise

20                    Sujet: Identification des structures d'entreprise dans SAP S/4HANA
Sales
29                      Exercice 2 : Description des structures organisationnelles dans
SAP S/4HANA Sales

37      Chapitre 3 :Synthèse des processus de vente

39                    Sujet: Exécution des processus de ventes SAP S/4HANA
46                    Sujet: Traitement des documents de vente
47                      Exercice 3 : Création d'une commande client
53                      Exercice 4 : Affichage d'une commande client
57                    Sujet: Traitement des livraisons sortantes
61                      Exercice 5 : Création d'une livraison sortante
65                    Sujet: Expédition de marchandises
69                      Exercice 6 : Prélèvement de marchandises
73                    Sujet: Traitement des documents de facturation
77                      Exercice 7 : Création d'un document de facturation
81                      Exercice 8 : Enregistrement d'un encaissement
```

---

## PDF page 6

```text
89      Chapitre 4 :Données de base

90                    Sujet: Gestion des données de base partenaire
95                      Exercice 9 : Création de données de base client
101                     Exercice 10 : Utilisation des données de base partenaire
106                   Sujet: Gestion des données de base article
109                     Exercice 11 : Création d'une fiche article
117                   Sujet: Gestion des fiches infos client-article
119                     Exercice 12 : Création d'une fiche infos client-article
124                   Sujet: Gestion des données de base de condition pour la
détermination du prix
127                     Exercice 13 : Création d'un enregistrement de condition (prix de
vente)
131                     Exercice 14 : Création d'un enregistrement de condition
(remise)
135                     Exercice 15 : Description du contexte des données de base de
condition
138                   Sujet: Explication des sujets complémentaires touchant aux
données de base
145                     Exercice 16 : Création de postes par défaut
151                     Exercice 17 : Gestion des documents de vente incomplets

161     Chapitre 5 :Détermination automatique des données et ordonnancement

162                   Sujet: Analyse des résultats de la détermination automatique des
données
169                     Exercice 18 : Vérification des résultats de la détermination
automatique des données
175                   Sujet: Analyse des résultats de l'ordonnancement de l'expédition et
du transport
179                     Exercice 19 : Vérification des résultats de l'ordonnancement de
l'expédition et du transport

189     Chapitre 6 :Contrôle de disponibilité

190                   Sujet: Exécution d'un contrôle de disponibilité – Principes de base
195                     Exercice 20 : Vérification des principaux facteurs influençant le
contrôle de disponibilité
201                     Exercice 21 : Vérification du transfert des besoins
205                     Exercice 22 : Vérification des options des livraisons complètes
ou partielles
210                   Sujet: Exécution d'un contrôle de disponibilité – Autres sujets
217                     Exercice 23 : Exécution des contrôles de disponibilité
223                     Exercice 24 : Description des fonctions du contrôle de
disponibilité
```

---

## PDF page 7

```text
233     Chapitre 7 : Opération groupée

234                  Sujet: Exécution d’opérations groupées
239                     Exercice 25 : Création des livraisons sortantes via une opération
groupée
243                     Exercice 26 : Achèvement des fonctions d'expédition via une
opération groupée
249                     Exercice 27 : Création de documents de facturation à l'aide
d'une opération groupée

257     Chapitre 8 :Processus supplémentaires dans les ventes

258                  Sujet: Utilisation de documents d'avant-vente
261                     Exercice 28 : Création de documents d'avant-vente
267                     Exercice 29 : Description du traitement des documents d'avant-
vente
270                  Sujet: Exécution de la fabrication sur commande
273                     Exercice 30 : Exécution de la fabrication sur commande
282                  Sujet: Vente de produits de service
283                     Exercice 31 : Vente d’un produit de service

293     Chapitre 9 :Gestion des réclamations

294                  Sujet: Création de demandes d'avoir
299                     Exercice 32 : Création d’une demande d'avoir
306                  Sujet: Annulation de documents de facturation
307                     Exercice 33 : Annulation d’un document de facturation
310                   Sujet: Création de retours
313                     Exercice 34 : Création d’un retour

319     Chapitre   Suivi et analyse des ventes
10 :

320                  Sujet: Utilisation de l’application Traitement des commandes clients
327                     Exercice 35 : Utilisation de l’application Traitement des
commandes clients
331                   Sujet: Gestion des plans commerciaux
333                  Sujet: Utilisation d'applications analytiques
337                     Exercice 36 : Analyse des données à l'aide des applications
analytiques
```

---

## PDF page 8

```text

```

---

## PDF page 9

```text
Vue d'ensemble du cours

PUBLIC CONCERNÉ
Ce cours s'adresse aux participants suivants :

●  Chef de projet

●  Consultant applicatif

●  Responsable de processus de gestion/Responsable d'équipe/Utilisateur de référence

●   Utilisateur
```

---

## PDF page 10

```text

```

---

## PDF page 11

```text
CHAPITRE 1  Navigation avec SAP Fiori

Sujet 1

Identification des fonctions clés de SAP Fiori                                           2
Exercice 1 : Utilisation de la barre de lancement SAP Fiori                                11

OBJECTIFS DU CHAPITRE

●   Identification des fonctions clés de SAP Fiori
```

---

## PDF page 12

```text
Chapitre 1
Sujet 1

Identification des fonctions clés de SAP Fiori

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●   Identification des fonctions clés de SAP Fiori

Expérience utilisateur SAP Fiori
Votre entreprise planifie d'implémenter SAP S/4HANA et vous souhaitez avoir des
informations sur la stratégie d’expérience utilisateur.

Vous vous intéressez notamment à l’interface utilisateur (IU) SAP Fiori.

Concepts et facteurs d’influence

Figure 1: Concepts et facteurs d’influence

L’informatique et l'utilisation d'appareils électroniques ne sont plus réservées aux experts et
se sont répandues dans tous les groupes sociaux. Le matériel haute performance rend
possible une large variété de logiciels ayant différents champs d'application et des utilisations
diverses. Par conséquent, il est important que le logiciel soit facile à utiliser.

Les principaux moteurs de ce développement sont les smartphones et tablettes dotés
d’interfaces utilisateur personnalisées et conviviales. Ces interfaces utilisateur ne sont plus
requises pour fournir un maximum de fonctionnalités, mais plutôt une expérience utilisateur
ergonomique centrée sur le consommateur.
```

---

## PDF page 13

```text
Sujet: Identification des fonctions clés de SAP Fiori

Les logiciels de gestion doivent donc s’adapter et se transformer afin de fournir de bonnes
expériences utilisateur à tous les métiers de l’entreprise. L'interface utilisateur (IU) joue un
rôle important dans le développement de cette dynamique. Pour les logiciels SAP, le défi
consiste à garder une vue claire et à comprendre toute la stratégie SAP relative à l’expérience
utilisateur.

Expérience utilisateur SAP

Figure 2: IU par rapport à UX

Les termes interface utilisateur (IU) et expérience utilisateur (UX) représentent deux
manières de penser différentes.

L'IU, dans une perspective logicielle, décrit l’interface entre l’utilisateur et l'appareil. Elle a
pour objectif d’optimiser l’efficacité pendant l’utilisation.

L'UX adopte le point de vue de l'utilisateur final ; son but est de motiver et de provoquer un
sentiment positif non seulement pendant, mais aussi avant et après l'utilisation. L'UX tente de
créer une expérience positive et motivante pour l’utilisateur.

Types d'utilisateur

Figure 3: Types d'utilisateur
```

---

## PDF page 14

```text
Chapitre 1 : Navigation avec SAP Fiori

Il est possible de trouver divers types d’utilisateur en fonction de l’organisation du domaine,
du service informatique, ainsi que du degré de numérisation.

Néanmoins, dans presque toutes les sociétés, il existe fondamentalement trois types
d'utilisateurs :

●   Utilisateur occasionnel

Il utilise le système occasionnellement et il a donc besoin d'applications simples et
conviviales. Des transactions à une seule étape sont exécutées dans de nombreux cas.

●   Utilisateur clé ou expert

Utilisateur SAP entièrement formé, il connait les processus et les applications disponibles
en détail. Cet utilisateur utilise souvent plusieurs systèmes et différentes IU.

●  Développeur ou programmeur

Il a des connaissances détaillées des processus et du système et se charge de l’adaptation
et l’extension des applications existantes. Généralement, il s’occupe de plusieurs
applications avec différentes IU.

SAP Fiori

Vous souhaitez vous assurer que vos utilisateurs bénéficient de la meilleure expérience qui
soit lors de leur interaction avec SAP Business Suite et qu’ils peuvent accéder aux
applications stratégiques sur n’importe quel appareil, sans difficulté. Vous avez besoin d’une
solution qui s’intègre à l’infrastructure de votre système informatique existant et qui peut
s’étendre pour couvrir vos besoins spécifiques.

Figure 4: Paradigme de l’expérience utilisateur SAP Fiori

Le principe de l'expérience utilisateur SAP Fiori repose sur cinq piliers :

●  Orientée rôle

Les utilisateurs ont accès aux applications nécessaires pour effectuer leurs tâches. Les
applications sont spécifiques à l’exécution de ces tâches.

●  Réactive

L’interface de l’application est réactive, elle s’adapte à la taille et à l'appareil des
utilisateurs qui y accèdent.

●  Simple

Un périmètre de l’application simple : un utilisateur, un cas d’utilisation et jusqu'à trois
écrans pour chaque application.
```

---

## PDF page 15

```text
Sujet: Identification des fonctions clés de SAP Fiori

●  Cohérente

Les applications sont développées avec une structure cohérente. Parlant toutes le même
langage, elles peuvent être implémentées dans plusieurs infrastructures et
environnements.

●  Valeur immédiate

Valeur ajoutée immédiate de par le peu d'obstacles à l'adoption, que ce soit du point de
vue du système informatique ou du point de vue de l'utilisateur.

Qu'est-ce que SAP Fiori ?

Figure 5: Qu'est-ce que SAP Fiori ?

Les applications opérationnelles permettent d’effectuer des tâches de modification, de
création, d’affichage (documents, enregistrements) par exemple, ou sur des processus
entiers avec navigation guidée.

Les applications d’analyse permettent de transformer des informations en actions. Elles vous
donnent un aperçu visuel des sujets complexes, à des fins de surveillance ou de suivi.

Les infos-clés vous donnent l’opportunité de rechercher et d’explorer vos données. Elles
offrent une vue complète des informations essentielles relatives à un objet et permettent une
navigation contextuelle entre les objets liés.
```

---

## PDF page 16

```text
Chapitre 1 : Navigation avec SAP Fiori

Barre de lancement SAP Fiori

Figure 6: Mise en forme de la barre de lancement SAP Fiori - Groupes

La barre de lancement SAP Fiori est une interface qui héberge les applications SAP Fiori et qui
fournit des services, notamment de navigation, de personnalisation, de prise en charge
intégrée et de configuration des applications.

La barre de lancement est le point d'accès aux applications SAP Fiori sur les terminaux
mobiles ou fixes La page d'accueil de la barre de lancement SAP Fiori est la première page
que les utilisateurs voient après s'être connectés. La page d'accueil de la barre de lancement
affiche des vignettes et des liens qui permettent à l'utilisateur de lancer des applications. Les
vignettes sont une représentation visuelle d'une application. Chaque vignette représente une
application de gestion que l’utilisateur peut lancer. Les vignettes/applications affichées pour
les utilisateurs dans la barre de lancement SAP Fiori sont organisées à l'aide de catalogues et
de groupes.

Un catalogue est un ensemble de vignettes que vous souhaitez mettre à disposition pour un
rôle. Ces catalogues sont affectés aux rôles utilisateur. Selon le rôle et les catalogues affectés
au rôle, les utilisateurs peuvent parcourir les catalogues et sélectionner les vignettes.

Les groupes définissent le regroupement, l'ordre de tri et l'apparence générale (vignette ou
lien) des applications qui sont initialement affichées sur la page d'accueil initiale de la barre de
lancement SAP Fiori pour un utilisateur. L'utilisateur peut personnaliser la page Fiori initiale
en ajoutant ou en supprimant des applications à des groupes prédéfinis ou des groupes
personnalisés.
```

---

## PDF page 17

```text
Sujet: Identification des fonctions clés de SAP Fiori

Figure 7: Options de mise en forme de la barre de lancement SAP Fiori

La mise en forme de la barre de lancement SAP Fiori peut être structurée par groupes ou par
espaces et pages.

Figure 8: Mise en forme de la barre de lancement SAP Fiori - Espaces et pages

Un espace sert de point d'entrée pour un rôle utilisateur et affiche les informations et les
fonctions affectées à ce rôle utilisateur. Un espace est représenté comme un élément de
navigation dans la navigation niveaux 1 et 2. Un espace se compose d'une ou de plusieurs
pages utilisées pour structurer davantage le contenu d'un espace.

Une page fait partie d'un espace et un espace peut avoir une ou plusieurs pages. Plusieurs
pages permettent aux utilisateurs de structurer l'espace en plusieurs contextes de travail
autonomes. Les rôles utilisateur avec moins d'applications peuvent utiliser une page par
espace, tandis que les rôles utilisateur avec plus d'applications peuvent utiliser plusieurs
pages par espace. Une page est constituée de sections utilisées pour structurer davantage le
contenu.

Une section structure sémantiquement le contenu d'une page. Une section est constituée de
vignettes qui visualisent le contenu d'un espace. Un titre de section est facultatif.

Les utilisateurs peuvent basculer entre les deux types de présentation à l'aide du menu
Actions utilisateur.
```

---

## PDF page 18

```text
Chapitre 1 : Navigation avec SAP Fiori

Personnalisation de la barre de lancement SAP Fiori

Figure 9: Personnalisation de la barre de lancement SAP Fiori

Les options de personnalisation suivantes sont disponibles dans la barre de lancement
SAP Fiori :

●  Ajout d'applications depuis les catalogues affectés

●  Suppression des applications que vous ne souhaitez pas utiliser

●  Modification et ajout d'applications pour des résultats de rapports filtrés

Par exemple, si l’utilisateur est un gestionnaire de la trésorerie du groupe qui s’intéresse au
marché allemand, il peut créer une application pour accéder directement à la situation
quotidienne de trésorerie du marché allemand. Il peut ainsi y accéder d'un clic depuis la page
d’accueil de la barre de lancement SAP Fiori.

Bibliothèque SAP Fiori

Bibliothèque de référence pour les applications SAP Fiori

La bibliothèque de référence des applications SAP Fiori est une bibliothèque complète
répertoriant tout le contenu SAP pertinent pour la barre de lancement SAP Fiori. À l'aide de la
bibliothèque, vous pouvez :

●  Rechercher des filtres tels que l'aide Type d'application et Version de produit pour
sélectionner les ensembles d'applications requis

●  Rechercher des informations clés pour chaque application, y compris toutes les données
techniques dont vous avez besoin pour l'installation et la configuration
```

---

## PDF page 19

```text
Sujet: Identification des fonctions clés de SAP Fiori

●  Accéder directement aux ressources associées, telles que la documentation de
l'application et la Product Availability Matrix

●  Obtenir des recommandations SAP Fiori (applications SAP Fiori les plus adaptées à
l'utilisation client)

Figure 10: Bibliothèque Fiori
```

---

## PDF page 20

```text
Chapitre 1 : Navigation avec SAP Fiori
```

---

## PDF page 21

```text
Chapitre 1
Exercice 1

Utilisation de la barre de lancement SAP Fiori

Familiarisez-vous avec la barre de lancement SAP Fiori, recherchez et ajoutez des
applications, et créez un groupe de vignettes personnalisé.

Remarque :
Dans les exercices de cette formation, lorsqu’une valeur contient ##, remplacez
ces caractères par le numéro que vous a attribué l'animateur.

1. Lancez la barre de lancement SAP Fiori à partir du menu d'applications Microsoft
Windows et connectez-vous avec l'utilisateur S4600-##. Le mot de passe vous sera fourni
par l'animateur.

2. Créez un groupe de vignettes personnalisé, Mes applications favorites, après le groupe de
vignettes News and Links, et affectez les applications suivantes à votre nouveau groupe :

●  Création de commandes clients VA01

●  Création de livraisons sortantes - À partir des commandes client

●  Gestion des documents de facturation

3. Gérez les valeurs par défaut propres à l'utilisateur suivantes pour faciliter la création de
documents au cours de la formation :

Nom de zone                             Valeur

Société                             1010

Numéro de magasin                   1010

Org. commerciale                     1010

Canal distrib.                        10

Secteur d'activité                     00

4. Recherchez l'application « Modification de commandes clients » sur la page d'accueil.
```

---

## PDF page 22

```text
Chapitre 1
Solution 1

Utilisation de la barre de lancement SAP Fiori

Familiarisez-vous avec la barre de lancement SAP Fiori, recherchez et ajoutez des
applications, et créez un groupe de vignettes personnalisé.

Remarque :
Dans les exercices de cette formation, lorsqu’une valeur contient ##, remplacez
ces caractères par le numéro que vous a attribué l'animateur.

1. Lancez la barre de lancement SAP Fiori à partir du menu d'applications Microsoft
Windows et connectez-vous avec l'utilisateur S4600-##. Le mot de passe vous sera fourni
par l'animateur.

a) Sélectionnez Microsoft Windows      et, pour afficher le menu d’applications, cliquez

sur        .

b) Pour lancer la barre de lancement SAP Fiori, sélectionnez l'entrée correspondante
dans la liste des applications.

c) Saisissez votre utilisateur S4600-## et le mot de passe.

d) Cliquez sur Connexion (Log on).

2. Créez un groupe de vignettes personnalisé, Mes applications favorites, après le groupe de
vignettes News and Links, et affectez les applications suivantes à votre nouveau groupe :

●  Création de commandes clients VA01

●  Création de livraisons sortantes - À partir des commandes client

●  Gestion des documents de facturation

a) Pour lancer le mode de personnalisation, dans le coin supérieur droit de l'écran,

cliquez sur                       .

b) Sélectionnez     Traiter page d’accueil.

c) Pour créer un groupe, sélectionnez + Ajouter groupe à l'emplacement souhaité de la
barre de lancement.

d) Gérez le nom du groupe de vignettes en remplaçant le texte Entrer nom de groupe par
le nouveau nom.
```

---

## PDF page 23

```text
Sujet: Identification des fonctions clés de SAP Fiori

e) Pour ajouter une application dans le nouveau groupe, cliquez sur le signe +.

f) Dans la partie gauche, sélectionnez le catalogue Ventes – Traitement des commandes
clients.

g) Cliquez sur l'icône punaise en-dessous de l'application Création de commandes clients
VA01 pour l'ajouter à votre groupe.

h) Dans la partie gauche, sélectionnez le catalogue SAP: LE – Applications
opérationnelles.

i) Cliquez sur l'icône punaise en-dessous de l'application Création de livraisons sortantes
(à partir des commandes clients) pour l'ajouter à votre groupe.

j) Dans la partie gauche, sélectionnez le catalogue Ventes – Document de facturation.

k) Cliquez sur l'icône punaise en-dessous de l’application Gestion des documents de
facturation pour l'ajouter à votre groupe.

l) Pour revenir à l'écran de personnalisation, dans la partie gauche, cliquez sur         .

m) Pour quitter le mode de personnalisation, en bas à droite de l'écran, cliquez sur
Fermer.

3. Gérez les valeurs par défaut propres à l'utilisateur suivantes pour faciliter la création de
documents au cours de la formation :

Nom de zone                             Valeur

Société                             1010

Numéro de magasin                   1010

Org. commerciale                     1010

Canal distrib.                        10

Secteur d'activité                     00

a) Dans le coin supérieur droit de l'écran, cliquez sur                       .

b) Sélectionnez Options.

c) Sélectionnez la catégorie Valeurs standard.

d) Gérez les valeurs par défaut.

e) Sélectionnez Sauvegarder pour sauvegarder vos valeurs par défaut.

4. Recherchez l'application « Modification de commandes clients » sur la page d'accueil.
a) Cliquez sur l'icône de recherche en haut à droite de l'écran.

b) Saisissez le nom de l'application “Modification de commandes clients” dans la zone de
recherche.
```

---

## PDF page 24

```text
Chapitre 1 : Navigation avec SAP Fiori

c) Le nom de l'application apparaîtra dans la liste déroulante de recherche.

d) Sélectionnez le nom de l'application pour l'ouvrir.
```

---

## PDF page 25

```text
Sujet: Identification des fonctions clés de SAP Fiori

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●   Identification des fonctions clés de SAP Fiori
```

---

## PDF page 26

```text
Chapitre 1 : Navigation avec SAP Fiori
```

---

## PDF page 27

```text
Chapitre 1

Évaluation des connaissances

1.  Parmi les applications suivantes, laquelle vous donne un aperçu visuel des sujets
complexes, à des fins de surveillance ou de suivi ?

Sélectionnez la réponse correcte.

X  A Applications opérationnelles

X  B Applications analytiques

X  C Infos-clés

2. Un utilisateur peut personnaliser la page d'accueil dans la barre de lancement SAP Fiori
par défaut.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 28

```text
Chapitre 1

Évaluation des connaissances - Réponses

1.  Parmi les applications suivantes, laquelle vous donne un aperçu visuel des sujets
complexes, à des fins de surveillance ou de suivi ?

Sélectionnez la réponse correcte.

X  A Applications opérationnelles

X  B Applications analytiques

X  C Infos-clés

Correct. Les applications analytiques vous donnent un aperçu visuel des sujets
complexes, à des fins de surveillance ou de suivi.

2. Un utilisateur peut personnaliser la page d'accueil dans la barre de lancement SAP Fiori
par défaut.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. La fonction permettant de personnaliser la page d'accueil doit être activée dans
la configuration de la barre de lancement.
```

---

## PDF page 29

```text
CHAPITRE 2  Structures d'entreprise

Sujet 1

Identification des structures d'entreprise dans SAP S/4HANA Sales                       20
Exercice 2 : Description des structures organisationnelles dans SAP S/4HANA Sales  29

OBJECTIFS DU CHAPITRE

●   Identification des structures d'entreprise dans SAP S/4HANA Sales
```

---

## PDF page 30

```text
Chapitre 2
Sujet 1

Identification des structures d'entreprise dans
SAP S/4HANA Sales

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●   Identification des structures d'entreprise dans SAP S/4HANA Sales

Entités organisationnelles de l'administration des ventes – Synthèse
Les entités organisationnelles du système SAP représentent la structure d'une entreprise. Par
conséquent, elles correspondent aux entités organisationnelles et/ou juridiques d'une
entreprise. SAP propose des entités organisationnelles pour tous les domaines de votre
entreprise (comptabilité, gestion des achats, production et stockage). Nous allons nous
concentrer sur les éléments liés aux processus d'administration des ventes.

La solution SAP S/4HANA utilise un ensemble d'entités organisationnelles conçues
exclusivement pour le mappage des processus de l'administration des ventes. Il s'agit, par
exemple, de l'organisation commerciale et du canal de distribution. D'autres entités
organisationnelles, telles que la société ou la division, appartiennent à d'autres domaines
mais sont également utilisées pour les processus de traitement des commandes.

Les entités organisationnelles représentées dans la figure sont les plus importantes du
système pour les processus d'administration des ventes.

Figure 11: Entités organisationnelles pour les processus d'administration des ventes
```

---

## PDF page 31

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

Entités organisationnelles – Société
La société est l'entité organisationnelle la plus fine de la comptabilité financière, pour laquelle
il est possible d'établir un plan comptable complet et autonome. Ce plan inclut tous les
enregistrements pertinents et la création de tous les documents justificatifs nécessaires aux
bilans/comptes de résultat.

Une société peut représenter, par exemple, une entreprise au sein d'un groupe ou une filiale.
Elle est liée aux processus d'administration des ventes car le revenu des ventes lui est affecté.

La figure Entité organisationnelle - Société répertorie certains éléments clés de la société en
tant qu'entité organisationnelle.

Figure 12: Entité organisationnelle – Société

Entités organisationnelles - Organisation commerciale
Pour utiliser les fonctions d'administration des ventes dans le système, vous devez disposer
d'au moins une organisation commerciale. Dans les statistiques sur les ventes, l'organisation
commerciale est le niveau de totalisation le plus élevé. Tous les documents commerciaux,
notamment les commandes client, les livraisons sortantes et les documents de facturation,
sont affectés à une organisation commerciale.

Remarque :
Au moins une organisation commerciale doit être définie dans le système, et
chacune doit être affectée de façon unique à une société. Cependant, plusieurs
organisations commerciales peuvent être affectées à une seule société.

L'organisation commerciale peut également être utilisée, par exemple, pour matérialiser une
subdivision du marché au niveau régional, national ou international. La figure Entité
organisationnelle - Organisation commerciale fournit des informations supplémentaires sur
l’organisation commerciale.
```

---

## PDF page 32

```text
Chapitre 2 : Structures d'entreprise

Figure 13: Entité organisationnelle – Organisation commerciale

Entité organisationnelle – Canal de distribution – Chaîne de distribution

Le canal de distribution spécifie la façon dont les marchandises et les services sont distribués.

Les canaux de distribution doivent être affectés à au moins une organisation commerciale
(plusieurs affectations sont possibles). Pour utiliser les fonctions d'administration des ventes,
vous devez disposer d'au moins un canal de distribution dans le système.

Vous pouvez utiliser différents canaux de distribution pour effectuer les tâches suivantes :

●  Définir des responsabilités

●   Établir une structure de prix flexible

●  Différencier les statistiques sur les ventes

En pratique, les entreprises utilisent des canaux de distribution différents pour séparer, par
exemple, les ventes nationales des ventes à l’export. Vous pouvez également utiliser un canal
de distribution produits (pour vendre des produits) et un canal de distribution de service
(pour vendre des services de maintenance et de réparation).

La figure « Entité organisationnelle – Canal de distribution » illustre l'affectation de canaux de
distribution, connus sous le nom de chaîne de distribution.

Une chaîne de distribution se compose d'une organisation commerciale et d'un canal de
distribution. Il s'agit d'une manière de classer l'organisation de la structure commerciale et
d'une méthode de répartition du produit. La figure illustre deux chaînes de distribution
(organisation commerciale/canal de distribution 1) et (organisation commerciale/canal de
distribution 2).
```

---

## PDF page 33

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

Figure 14: Entité organisationnelle – Canal de distribution – Chaîne de distribution

Entités organisationnelles– Secteur d'activité

Vous pouvez regrouper des articles et des services à l'aide de secteurs d'activité.

Un secteur d'activité peut représenter une famille de produits spécifique. Vous pouvez donc
limiter les accords de prix conclus avec un client à un secteur d'activité donné. Vous pouvez
également effectuer des analyses statistiques par secteur d'activité.

L’utilisation des secteurs d’activité au sein de la structure des ventes pourrait être motivée
par le fait que certaines personnes du service des ventes connaissent bien un groupe de
produits spécifique (outils de traitement du métal, par exemple) alors que d'autres possèdent
des connaissances techniques sur un autre groupe de produits (outils de traitement de
polymères, par exemple). À partir des secteurs d'activité correspondants, vous pouvez
prendre en compte ces différences lors de la configuration de la structure commerciale.

Plusieurs secteurs d'activité peuvent être affectés à une organisation commerciale. Pour
utiliser les fonctions d'administration des ventes dans le système, vous devez définir au moins
un secteur d'activité dans le système.

La figure Entité organisationnelle – Secteur d'activité illustre la pertinence des secteurs
d'activité au sein d'une structure organisationnelle.
```

---

## PDF page 34

```text
Chapitre 2 : Structures d'entreprise

Figure 15: Entités organisationnelles– Secteur d'activité

Entité organisationnelle – Domaine commercial

Un domaine commercial est la combinaison d'une organisation commerciale, d'un canal de
distribution et d'un secteur d'activité. Le canal de distribution qu'utilise une organisation
commerciale pour vendre les produits d'un secteur d'activité déterminé est ainsi défini.

Chaque document de vente est affecté à un seul domaine commercial. Cette affectation ne
peut pas être modifiée.

Un domaine commercial ne peut appartenir qu'à une seule société. Cette relation est définie
par l'affectation de l'organisation commerciale correspondante à la société appropriée. Vous
devez définir au moins un domaine commercial dans le système pour exécuter les processus
d'administration des ventes.

Lors du traitement des documents commerciaux, le système accède aux diverses données de
base en fonction du domaine commercial. Il peut s'agir des données de base partenaire, des
prix ou des remises. En outre, le système effectue des contrôles de validité sur certaines
entrées en fonction du domaine commercial.

La figure Entité organisationnelle - Domaine commercial illustre des exemples de domaines
commerciaux.
```

---

## PDF page 35

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

Figure 16: Entité organisationnelle – Domaine commercial

Astuce :
Une structure organisationnelle simple offre souvent plus d'avantages qu'une
structure complexe. Par exemple, elle simplifie la gestion des données de base.
Ne définissez pas des structures organisationnelles complexes dans votre
système pour fournir des options de reporting détaillées. Utilisez plutôt les zones
prévues à cet effet dans les données de base et les documents.

Entités organisationnelles – Distribution
Entités organisationnelles – Division et magasin

Une division est un emplacement dans lequel est conservé le stock article, elle peut
représenter, par exemple, un site de production ou un centre de distribution. Il est possible
d'utiliser plusieurs magasins pour séparer le stock au sein d'une division.

La division et le magasin sont des entités organisationnelles qui peuvent être utilisées par
toutes les zones logistiques du système. Dans l'administration des ventes, une division
représente l'emplacement à partir duquel les articles et les services sont livrés à un client.

Remarque :
Une division utilisée dans un processus d'administration des ventes est également
appelée division chargée de la livraison.

Les informations suivantes relatives à l'utilisation de divisions dans les processus
d'administration des ventes sont importantes :

●  Pour utiliser les fonctions d'administration des ventes dans le système, vous devez
disposer d'au moins une division.

●  Chaque division est affectée à une société de manière unique.
```

---

## PDF page 36

```text
Chapitre 2 : Structures d'entreprise

●  Pour utiliser une division dans un processus d'administration des ventes, vous devez
l'affecter à au moins une combinaison organisation commerciale et canal de distribution.
Plusieurs affectations sont possibles.

●  La division est essentielle pour déterminer le point d'expédition.

La figure Entités organisationnelles - Division et magasin illustre les affectations
correspondantes pour les divisions.

Figure 17: Entités organisationnelles – Division et magasin

Entité organisationnelle – Point d'expédition

L'expédition fait partie intégrante de l'administration des ventes. Le point d'expédition est
l'entité organisationnelle qui contrôle vos activités d'expédition. Chaque livraison sortante est
traitée par un seul point d'expédition.

Le point d'expédition peut être notamment une rampe de chargement de véhicule, un bureau
postal ou un dépôt de chemin de fer. Il peut également représenter un groupe de salariés
responsables de livraisons utilisant un type particulier de transport (par exemple, route,
conteneur d'exportation, etc.) ou éventuellement responsable de livraisons très urgentes.
Chaque point d'expédition doit être affecté à au moins une division, mais plusieurs
affectations sont possibles.

La figure Entité organisationnelle - Point d'expédition présente une synthèse des affectations
possibles des points d'expédition.
```

---

## PDF page 37

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

Figure 18: Entité organisationnelle – Point d'expédition

Entités organisationnelles – Activation de la gestion des emplacements de magasin

Les fonctions de gestion des emplacements de magasin sont souvent nécessaires en
complément des fonctions de la gestion des stocks. Par exemple, une société souhaite suivre
le nombre d'articles dans chaque emplacement, et aussi contrôler et enregistrer tous les
mouvements de marchandises et les articles dans le magasin.

Pour cela, SAP Extended Warehouse Management (EWM) est intégré à SAP S/4HANA. Pour
l'activation des fonctions de gestion des emplacements de magasin correspondantes, des
combinaisons de divisions et de magasins sont liées à un numéro de magasin.

Remarque :
Le numéro de magasin est utilisé dans les deux composantes, LE (Logistics
Execution) et EWM. À noter que le numéro de magasin est une zone à trois
caractères dans LE mais une zone à quatre caractères dans EWM.

Figure 19: Entités organisationnelles – Activation de la gestion des emplacements de magasin
```

---

## PDF page 38

```text
Chapitre 2 : Structures d'entreprise

Entités organisationnelles – SAP EWM

Le numéro de magasin constitue le plus haut niveau d'entité organisationnelle dans la gestion
des emplacements de magasin. En pratique, le numéro de magasin correspond généralement
à un bâtiment physique ou un centre de distribution. Chaque numéro de magasin comporte
une sous-structure qui représente en détail l'organisation physique au sein du complexe de
magasins.

Il existe différentes zones pour le stockage physique des produits dans un magasin. Ces
zones, appelées types de magasin, incluent différents types de rayonnages, de zones de
réception et de sortie des marchandises. Les types de magasin sont représentés sous la
forme d'un groupe d'emplacements présentant des caractéristiques similaires.

Les aires de stockage sont des subdivisions d'un type de magasin. Une aire de stockage
représente un groupe d'emplacements qui présentent un attribut commun (par exemple, les
emplacements qui sont utilisés pour stocker des articles à forte rotation). Les aires de
stockage sont utilisées lors de la détermination de l'emplacement d'entrée en stock.

Les emplacements constituent le niveau le plus bas de la structure organisationnelle. Ils sont
affectés à un type de magasin et à une aire de stockage (le cas échéant). Les emplacements
représentent les lieux physiques où les marchandises sont stockées dans le magasin.

Figure 20: Entités organisationnelles – SAP EWM
```

---

## PDF page 39

```text
Chapitre 2
Exercice 2

Description des structures organisationnelles
dans SAP S/4HANA Sales

Si vous souhaitez exécuter certaines tâches du processus d'administration des ventes, vous
devez connaître les structures organisationnelles concernées. Certaines d'entre elles ne sont
utilisées que dans les processus d'administration des ventes et d'autres s'appliquent
également à d'autres processus et applications.

Tâche 1: Nommer les entités organisationnelles

1. Quelle entité organisationnelle dans la comptabilité financière représente une entité
juridique et une unité comptable indépendante dans le système ?

2. Quelle entité organisationnelle représente une filiale ou un service commercial ?

3. Quelle entité organisationnelle représente un mode de distribution de marchandises au
client (par exemple, ventes usine, commerce de gros ou commerce de détail) ?

4. Quelle entité organisationnelle représente différentes lignes de produits et regroupe des
articles (par exemple, véhicules, accessoires ou pièces de rechange) ?

5. Quelle entité organisationnelle représente un site de fabrication ou un centre de
distribution ?
```

---

## PDF page 40

```text
Chapitre 2 : Structures d'entreprise

6. Dans une division, le stockage des articles peut être réparti entre divers emplacements ou
locaux. Quelle entité organisationnelle représente un tel emplacement ou local ?

7. Quelle entité organisationnelle est obligatoire pour organiser et traiter les livraisons
sortantes aux différents points (par exemple, rampe de chargement de véhicules ou dépôt
de chemin de fer) ?

8. Quelle entité organisationnelle représente un magasin physique ?

Tâche 2: Affectations d'entités organisationnelles

1. Quelles entités organisationnelles sont des composants d'un domaine commercial ?

2. À quelle entité organisationnelle une organisation commerciale est-elle affectée pour
représenter le lien entre les processus des ventes et la comptabilité financière ?

3. À quelle entité organisationnelle un point d'expédition est-il affecté ?

4. Quelle entité organisationnelle permet de regrouper des magasins ?

5. À quelles entités organisationnelles les numéros de magasin sont-ils affectés ?
```

---

## PDF page 41

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

6. À quelles entités organisationnelles les divisions chargées de la livraison sont-elles
affectées ?
```

---

## PDF page 42

```text
Chapitre 2
Solution 2

Description des structures organisationnelles
dans SAP S/4HANA Sales

Si vous souhaitez exécuter certaines tâches du processus d'administration des ventes, vous
devez connaître les structures organisationnelles concernées. Certaines d'entre elles ne sont
utilisées que dans les processus d'administration des ventes et d'autres s'appliquent
également à d'autres processus et applications.

Tâche 1: Nommer les entités organisationnelles

1. Quelle entité organisationnelle dans la comptabilité financière représente une entité
juridique et une unité comptable indépendante dans le système ?

Société

2. Quelle entité organisationnelle représente une filiale ou un service commercial ?

Org. commerciale

3. Quelle entité organisationnelle représente un mode de distribution de marchandises au
client (par exemple, ventes usine, commerce de gros ou commerce de détail) ?

Canal de distribution

4. Quelle entité organisationnelle représente différentes lignes de produits et regroupe des
articles (par exemple, véhicules, accessoires ou pièces de rechange) ?

Secteur d'activité

5. Quelle entité organisationnelle représente un site de fabrication ou un centre de
distribution ?

Division

6. Dans une division, le stockage des articles peut être réparti entre divers emplacements ou
locaux. Quelle entité organisationnelle représente un tel emplacement ou local ?

Magasin
```

---

## PDF page 43

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

7. Quelle entité organisationnelle est obligatoire pour organiser et traiter les livraisons
sortantes aux différents points (par exemple, rampe de chargement de véhicules ou dépôt
de chemin de fer) ?

Point d'expédition

8. Quelle entité organisationnelle représente un magasin physique ?

Numéro de magasin

Tâche 2: Affectations d'entités organisationnelles

1. Quelles entités organisationnelles sont des composants d'un domaine commercial ?

Un domaine commercial comprend une  organisation  commerciale, un  canal de
distribution et un secteur d'activité.

2. À quelle entité organisationnelle une organisation commerciale est-elle affectée pour
représenter le lien entre les processus des ventes et la comptabilité financière ?

L'organisation commerciale est affectée à une société.

3. À quelle entité organisationnelle un point d'expédition est-il affecté ?

Un point d'expédition est affecté à une division.

4. Quelle entité organisationnelle permet de regrouper des magasins ?

Les magasins sont affectés à la division.

5. À quelles entités organisationnelles les numéros de magasin sont-ils affectés ?

Les numéros de magasin sont affectés à des combinaisons de division/magasin.

6. À quelles entités organisationnelles les divisions chargées de la livraison sont-elles
affectées ?

Les divisions chargées de la livraison sont affectées aux combinaisons d'organisation
commerciale et de canal de distribution.
```

---

## PDF page 44

```text
Chapitre 2 : Structures d'entreprise

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●   Identification des structures d'entreprise dans SAP S/4HANA Sales
```

---

## PDF page 45

```text
Chapitre 2

Évaluation des connaissances

1. Une société est la plus petite entité organisationnelle de la comptabilité financière.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Chaque document de vente peut être affecté à plusieurs domaines commerciaux.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 46

```text
Chapitre 2

Évaluation des connaissances - Réponses

1. Une société est la plus petite entité organisationnelle de la comptabilité financière.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. La société est l'entité organisationnelle la plus fine de la comptabilité financière,
pour laquelle il est possible d'établir un plan comptable complet et autonome.

2. Chaque document de vente peut être affecté à plusieurs domaines commerciaux.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Chaque document de vente est affecté à un seul domaine commercial. Cette
affectation ne peut pas être modifiée.
```

---

## PDF page 47

```text
CHAPITRE 3  Synthèse des processus de
vente

Sujet 1

Exécution des processus de ventes SAP S/4HANA                                     39

Sujet 2

Traitement des documents de vente                                               46
Exercice 3 : Création d'une commande client                                  47
Exercice 4 : Affichage d'une commande client                                53

Sujet 3

Traitement des livraisons sortantes                                                    57
Exercice 5 : Création d'une livraison sortante                                     61

Sujet 4

Expédition de marchandises                                                      65
Exercice 6 : Prélèvement de marchandises                                 69

Sujet 5

Traitement des documents de facturation                                              73
Exercice 7 : Création d'un document de facturation                              77
Exercice 8 : Enregistrement d'un encaissement                                   81

OBJECTIFS DU CHAPITRE

●  Exécution des processus de ventes SAP S/4HANA

●  Traitement des documents de vente

●  Traiter les livraisons sortantes

●  Expédier des marchandises

●  Traiter les documents de facturation
```

---

## PDF page 48

```text
Chapitre 3 : Synthèse des processus de vente
```

---

## PDF page 49

```text
Chapitre 3
Sujet 1

Exécution des processus de ventes SAP S/
4HANA

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Exécution des processus de ventes SAP S/4HANA

Phases de processus
Un processus d'administration des ventes peut être déclenché par des mesures d'avant-
vente et de marketing (mailing, campagnes Internet, contacts à l'occasion d'une foire ou
campagnes téléphoniques).

Le résultat possible de ces campagnes peut se traduire par une demande d'information sans
engagement du client ou une demande d'offre. Les demandes et les offres permettent de
déterminer les données importantes relatives à ces demandes et peuvent être sauvegardées
comme documents. Si un client passe une commande, vous pouvez alors accéder à ces
documents.

Utilisez ces informations d'avant-vente pour planifier et analyser vos stratégies de marketing
et de vente ainsi que pour déterminer des relations commerciales à long terme avec vos
clients, par exemple en :

●  effectuant un suivi des ventes perdues ;

●  Enregistrement des données d'avant-vente pour faciliter la négociation d'importants
contrats ;

●  vendant des marchandises et des services aux grandes organisations pour lesquelles
l'ensemble du processus doit être documenté.

La figure « Activités d’avant-vente » répertorie certains sujets importants du processus
d'avant-vente.
```

---

## PDF page 50

```text
Chapitre 3 : Synthèse des processus de vente

Figure 21: Activités d'avant-vente

Gestion des commandes client

Si les activités d'avant-vente aboutissent, les clients commandent les marchandises et/ou les
services correspondants. Une commande client est alors créée pour représenter cette étape
du processus dans SAP S/4HANA. La commande client contient toutes les informations
nécessaires au traitement de la demande du client tout au long du cycle du processus.

Le système copie automatiquement les données de base et les informations des tables de
pilotage qui ont été préalablement préparées. Cela permet d'éviter des erreurs lors de la
création des commandes client ainsi que la saisie de données redondantes.

Figure 22: Gestion des commandes clients

Détermination des sources d'approvisionnement

Pour pouvoir être livré au client, un article commandé doit être approvisionné. Le mode
d'approvisionnement d'un article peut dépendre de l'article proprement dit et de la
transaction de vente.

L'article peut être approvisionné comme suit :
```

---

## PDF page 51

```text
Sujet: Exécution des processus de ventes SAP S/4HANA

●  directement à partir du stock ;

●  par un fournisseur (via une demande d'achat ou commande d'achat) ;

●  par sa fabrication (via un ordre planifié ou un ordre de fabrication).

La figure Détermination des sources d'approvisionnement représente l'intégration des
fonctions de gestion des articles dans le processus d'administration des ventes.

Figure 23: Détermination des sources d'approvisionnement

Expédition

Une fois que la détermination des sources d'approvisionnement de l'article demandé est
confirmée, le traitement de l’expédition peut commencer. Dans SAP S/4HANA, la création
des livraisons sortantes est la première étape du processus d'expédition. La livraison sortante
pilote, prend en charge et suit les diverses étapes du traitement, telles que :

●  Prélèvement et confirmation via les fonctions de gestion des emplacements de magasin
(facultatif)

●  Emballage (facultatif)

●  Planification et suivi du transport via des documents de transport (facultatif) ou des ordres
de fret dans SAP S/4HANA Transportation Management (également facultatif)

●  Enregistrement de la sortie de marchandises

Les livraisons sortantes sont généralement créées en référence à une ou plusieurs
commandes clients. De cette manière, les informations pertinentes (articles et quantités)
peuvent être copiées de la commande client dans la livraison.

Pour prendre en charge le prélèvement des articles dans le magasin, des tâches magasin sont
ensuite créées (en fonction des informations incluses dans la livraison). Les tâches magasin
sont essentielles au contrôle des mouvements de stock dans un magasin. La principale
fonction d'une tâche de magasin consiste à indiquer l'emplacement du magasin à partir
duquel les marchandises doivent être prélevées et transférées.

Lorsque vous enregistrez une sortie de marchandises, vous modifiez la quantité et la valeur
des marchandises en stock. Les modifications basées sur la valeur s'appliquent aux comptes
de bilan définis en comptabilité financière.
```

---

## PDF page 52

```text
Chapitre 3 : Synthèse des processus de vente

Figure 24: Expédition

Facturation

Une fois le processus d'expédition terminé, les documents de facturation peuvent être créés.
Vous pouvez les créer avec référence à une ou plusieurs livraisons sortantes lors de la vente
de produits physiques ou avec référence à des commandes clients lors de la vente de
services. Dans les deux cas, les informations pertinentes sont copiées dans le document de
facturation à partir des documents précédents. Le document de facturation sert de source de
données à la comptabilité financière pour faciliter le contrôle et le traitement des
encaissements.

Lorsque vous créez un document de facturation, les comptes généraux sont
automatiquement déterminés et les données pertinentes sont enregistrées. Le système crée
les éléments suivants :

●  Une écriture au débit sur le compte de créances du client

●  Une écriture au crédit sur le compte de produits

Figure 25: Facturation

Paiement

L'encaissement du client est enregistré dans le service de comptabilité. Les données sont
ensuite enregistrées automatiquement comme suit dans les comptes généraux concernés :

●  Une écriture au débit sur le compte de caisse
```

---

## PDF page 53

```text
Sujet: Exécution des processus de ventes SAP S/4HANA

●  Une écriture au crédit sur le compte de créances du client

Remarque :
L'enregistrement des encaissements ne fait pas partie du processus principal
d'administration des ventes. Néanmoins, les factures impayées peuvent avoir des
incidences sur le processus de vente standard si vous vérifiez la ligne de crédit des
clients lors de la création des commandes.

Figure 26: Paiement

Synthèse des processus
La figure « Synthèse des processus » récapitule les documents à prendre en compte dans un
processus d'administration des ventes.

●  Les demandes, les offres, les contrats, les programmes de livraisons et les commandes
sont des exemples de documents de vente.

●  Les livraisons sortantes et les tâches magasin sont des documents faisant partie du
traitement de l’expédition et des emplacements de magasin.

●  Le document de sortie de marchandises contient des modifications concernant le stock et
constitue la base des pièces comptables significatives.

●  Le document de facturation constitue la base des pièces comptables pertinentes.

Les parties gauche et droite de la figure représentent des interfaces clés entre le processus
d'administration des ventes et d'autres composantes.
```

---

## PDF page 54

```text
Chapitre 3 : Synthèse des processus de vente

Figure 27: Synthèse des processus

Flux de processus
La relation entre les documents d'un processus d'administration des ventes peut être affichée
via le flux de processus. Cela vous permet d'accéder à tout moment à l'historique et au statut
en cours des documents.

Selon le document à partir duquel vous appelez le flux de processus, tous les documents
précédents et liés correspondants s'affichent. Le principal statut de traitement peut
également être suivi de cette manière et il est possible d’accéder aux infos-clés des
documents correspondants.

Remarque :
Le flux de processus affiche le processus sous forme de graphique et il est
disponible via les applications correspondantes (par exemple, Gestion des
commandes clients) dans la barre de lancement SAP Fiori.
```

---

## PDF page 55

```text
Sujet: Exécution des processus de ventes SAP S/4HANA

Figure 28: Flux de processus

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Exécution des processus de ventes SAP S/4HANA
```

---

## PDF page 56

```text
Chapitre 3
Sujet 2

Traitement des documents de vente

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Traitement des documents de vente

Gestion des ventes
La création d'un document de vente implique la gestion d'un grand nombre d'informations
obligatoires. Par exemple, chaque document de vente, tel qu'une commande client ou une
offre, doit toujours être affecté à un domaine commercial. De plus, la plupart des documents
de vente doivent contenir un numéro de client et au moins un poste avec un numéro d'article.

S'il existe déjà un document précédent approprié, il est possible de copier les données de ce
document lors de la création d'une commande client. Par exemple, une ou plusieurs offres
peuvent servir de documents de référence à une commande client. Dans ce cas, le système
copie les données applicables dans la commande client, ce qui évite à l'utilisateur de les gérer
manuellement.

La figure « Création d'une commande client » indique les combinaisons possibles d'offres et
de commandes clients.

Figure 29: Création d'une commande client
```

---

## PDF page 57

```text
Chapitre 3
Exercice 3

Création d'une commande client

Dans la plupart des cas, le processus de vente commence par une commande d'articles de la
part du client indiquant la date de livraison qu’il souhaite. Vous pouvez alors créer une
commande client à l'aide de ces informations.

1. Créez une commande client standard à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           4-2##

DateLivrSouh.                         dans 1 semaine

Article                                   Quantité

T-MS1##                           10

T-MS2##                           20

Sauvegardez la commande client et notez le numéro du document.

____________________________________________
```

---

## PDF page 58

```text
Chapitre 3
Solution 3

Création d'une commande client

Dans la plupart des cas, le processus de vente commence par une commande d'articles de la
part du client indiquant la date de livraison qu’il souhaite. Vous pouvez alors créer une
commande client à l'aide de ces informations.

1. Créez une commande client standard à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           4-2##

DateLivrSouh.                         dans 1 semaine

Article                                   Quantité

T-MS1##                           10

T-MS2##                           20

Sauvegardez la commande client et notez le numéro du document.

____________________________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients (VA01).

b) Dans l’écran initial, saisissez les valeurs du type de commande, de l'organisation
commerciale, du canal de distribution et du secteur d'activité.

c) Pour accéder aux détails de la commande, appuyez sur Entrée.

d) Dans l'écran de synthèse, saisissez le donneur d'ordre, la référence client et la date de
livraison souhaitée.

e) Pour confirmer vos entrées, appuyez sur Entrée.

f) Saisissez les données article.

g) Pour confirmer vos entrées, appuyez sur Entrée.
```

---

## PDF page 59

```text
Sujet: Traitement des documents de vente

h) En bas à droite de l’écran, cliquez sur Sauvegarder.
Le numéro de document s'affiche.
```

---

## PDF page 60

```text
Chapitre 3 : Synthèse des processus de vente

Structure des documents de vente
Un document de vente est divisé en trois niveaux : en-tête, poste et échéance. Les données
sont réparties entre ces niveaux comme suit :

●  Niveau de l'en-tête :

Les données de l'en-tête s'appliquent à tout le document. Sont inclus notamment le
numéro du document et des données liées au client telles que celles du donneur d'ordre
concerné.

●  Niveau du poste :

Chaque poste d'un document de vente contient ses propres données. Il comprend
notamment les données relatives aux articles commandés et aux quantités
correspondantes. Chaque document de vente peut contenir plusieurs postes, et le pilotage
de chacun des postes peut être différent. Il peut s'agir, par exemple, de postes de
marchandises, de postes de service, de postes gratuits ou de postes de texte.

●  Niveau de l'échéance :

Les échéances contiennent les quantités et les dates de livraison confirmées. Elles
appartiennent clairement à un poste. Chaque poste devant être livré physiquement doit
comporter au moins une échéance. Un poste peut comprendre plusieurs échéances si, par
exemple, la quantité commandée doit être livrée en plusieurs livraisons partielles à
différents moments.

Remarque :
Certaines données d'en-tête peuvent également être gérées au niveau du poste
(par exemple, le réceptionnaire). Dans ce cas, la saisie au niveau du poste
s'applique aux processus de suivi.

La figure Structure d'un document de vente représente la structure des documents de vente
illustrée par un exemple.
```

---

## PDF page 61

```text
Sujet: Traitement des documents de vente

Figure 30: Structure d'un document de vente
```

---

## PDF page 62

```text
Chapitre 3 : Synthèse des processus de vente
```

---

## PDF page 63

```text
Chapitre 3
Exercice 4

Affichage d'une commande client

Affichez la commande client pour vous familiariser avec la structure d'un document de vente.

1. Affichez la commande client que vous avez saisie précédemment. Notez les conditions de
paiement de l'en-tête de la commande client, la valeur nette totale de la commande et son
poids total.

●  Conditions de paiement : ___________________

●  Valeur nette : ________________________

●  Poids total : ______________________

2. Est-il nécessaire qu'une seule livraison complète soit effectuée pour cette commande ?

3. Depuis quelle division le poste 10 est-il livré ?

4. Quel est le prix unitaire pour les postes 10 et 20 ?

Poste                      Prix unitaire

5. Quelle est la date de livraison de l'échéance pour le poste 10 ?
____________________________________________

6. Quelle est la quantité confirmée dans l'échéance du poste 20 ?
____________________________________________

7. Qui est le destinataire de la facture pour cette commande ?
____________________________________________

8. Quel est le statut de traitement global de la commande client ?
____________________________________________
```

---

## PDF page 64

```text
Chapitre 3
Solution 4

Affichage d'une commande client

Affichez la commande client pour vous familiariser avec la structure d'un document de vente.

1. Affichez la commande client que vous avez saisie précédemment. Notez les conditions de
paiement de l'en-tête de la commande client, la valeur nette totale de la commande et son
poids total.

●  Conditions de paiement : ___________________

●  Valeur nette : ________________________

●  Poids total : ______________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Affichage des commandes
clients.

b) Dans l'écran initial, saisissez le numéro de la commande client que vous avez créée
précédemment.

c) Sélectionnez Entrée.

d) Vous trouverez dans la page à onglet Ventes les zones Conditions de paiement, Valeur
nette et Poids total.

2. Est-il nécessaire qu'une seule livraison complète soit effectuée pour cette commande ?

Dans la page à onglet Ventes, vous trouverez également le code de livraison complète.

3. Depuis quelle division le poste 10 est-il livré ?

Passez à la page à onglet Expédition. Vous y trouverez entre autres informations la
division de livraison.

4. Quel est le prix unitaire pour les postes 10 et 20 ?

Poste                      Prix unitaire

a) Double-cliquez sur le poste 10 pour accéder aux détails du poste.

b) Sélectionnez la page à onglet Conditions.

c) Le prix unitaire est affiché dans la colonne Montant, sur la première ligne des éléments
de prix (type de condition PR00).

d) Répétez ces étapes pour le poste 20.
```

---

## PDF page 65

```text
Sujet: Traitement des documents de vente

5. Quelle est la date de livraison de l'échéance pour le poste 10 ?
____________________________________________
a) Double-cliquez sur le poste 10 pour accéder aux détails du poste.

b) Vous trouverez la date de livraison de l'échéance dans la page à onglet Échéances.

6. Quelle est la quantité confirmée dans l'échéance du poste 20 ?
____________________________________________
a) Double-cliquez sur le poste 20 pour accéder aux détails du poste.

b) Vous trouverez la quantité confirmée de l'échéance dans la page à onglet Échéances.

7. Qui est le destinataire de la facture pour cette commande ?
____________________________________________
a) Depuis n'importe quelle page à onglet de la synthèse, cliquez sur le bouton Afficher
détails en-tête doc.

b) Sélectionnez la page à onglet Partenaires.

c) Le destinataire de la facture s’affiche dans la colonne Partenaire.

8. Quel est le statut de traitement global de la commande client ?
____________________________________________
a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des commandes
clients.

b) Si les filtres de l'application ne sont pas visibles dans l'écran initial, cliquez sur
Développer l’en-tête.

c) Saisissez le numéro de votre commande client comme critère de filtre et cliquez sur
Lancer.
Le statut global de la commande client est affiché dans la liste. Le statut doit être En
cours car aucun document lié n'a encore été créé.
```

---

## PDF page 66

```text
Chapitre 3 : Synthèse des processus de vente

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Traitement des documents de vente
```

---

## PDF page 67

```text
Chapitre 3
Sujet 3

Traitement des livraisons sortantes

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Traiter les livraisons sortantes

Livraisons sortantes
Les livraisons sortantes constituent les documents de base des différentes activités
exécutées lors du processus d'expédition (prélèvement, emballage et enregistrement de la
sortie de marchandises). Dans la plupart des cas, ils sont créés en faisant référence à une ou
plusieurs commandes client prêtes à être expédiées. Grâce à cette référence, le système peut
copier toutes les données nécessaires dans la livraison sortante à partir des commandes.

Vous pouvez créer une ou plusieurs livraisons sortantes avec référence à une seule
commande. Sinon, il est possible de regrouper dans une seule livraison sortante plusieurs
postes de différentes commandes clients. Pour combiner des postes de plusieurs
commandes, ils doivent tous avoir les mêmes valeurs pour les caractéristiques clé du
processus d'expédition, par exemple :

●  Point d'expédition

●  Date d'échéance de la livraison

●  Adresse d'expédition

Le système peut créer des livraisons en ligne ou comme job d'arrière-plan à exécuter pendant
les heures creuses.

La figure Création d'une livraison sortante illustre la création de livraisons sortantes avec
référence à des commandes clients.
```

---

## PDF page 68

```text
Chapitre 3 : Synthèse des processus de vente

Figure 31: Création d'une livraison sortante

Structure des documents de livraison

Un document de livraison est regroupé en deux niveaux : au niveau de l'en-tête et au niveau
du poste. Les données sont réparties entre ces niveaux comme suit :

●  Niveau de l'en-tête :

Les données de l'en-tête s'appliquent à tout le document. Cela comprend notamment les
données du réceptionnaire, ainsi que les délais de traitement de l'expédition.

●  Niveau du poste :

Chaque poste du document de livraison contient ses propres données. Un poste
comprend notamment les données relatives aux articles, aux quantités, aux poids et aux
informations sur le stock. Chaque document de livraison peut contenir plusieurs postes, et
le pilotage de chacun des postes peut être différent. Ce sont, par exemple, des postes de
marchandises, des postes gratuits ou des postes de texte.

Remarque :
Contrairement aux documents de vente, les documents de livraison ne
contiennent aucune échéance. Chaque échéance du document de vente peut
devenir un poste du document de livraison.

La figure « Structure des documents de livraison » illustre la structure des livraisons
sortantes.
```

---

## PDF page 69

```text
Sujet: Traitement des livraisons sortantes

Figure 32: Structure des documents de livraison
```

---

## PDF page 70

```text
Chapitre 3 : Synthèse des processus de vente
```

---

## PDF page 71

```text
Chapitre 3
Exercice 5

Création d'une livraison sortante

Les livraisons sortantes constituent les documents de base de planification et d'exécution des
diverses activités d'expédition. Créez une livraison sortante avec référence à une commande
client.

1. Créez une livraison sortante en référence à une commande client et notez le numéro du
document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

____________________________________________

2. Vérifiez les valeurs des zones suivantes pour la livraison créée :

Poste               Quantité livrée               Magasin

3. Quel est désormais le statut global de la commande client ?
____________________________________________

Astuce :
Utilisez le flux de processus de la livraison sortante pour obtenir ces
informations.

4. Quel est le statut global de la livraison sortante ?

5. Avant la sortie des articles de la division et l'enregistrement de la sortie de marchandises,
affichez l'état des stocks pour l'article T-MS1## dans la division 1010. Notez le nombre de
pièces en stock à utilisation libre.
```

---

## PDF page 72

```text
Chapitre 3
Solution 5

Création d'une livraison sortante

Les livraisons sortantes constituent les documents de base de planification et d'exécution des
diverses activités d'expédition. Créez une livraison sortante avec référence à une commande
client.

1. Créez une livraison sortante en référence à une commande client et notez le numéro du
document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

____________________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes (à partir des commandes client).

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Saisissez le point d'expédition et sélectionnez la bonne date de création planifiée.

d) Sélectionnez Lancer pour lancer la sélection de document.

e) Sélectionnez la ligne contenant le numéro de votre commande client (cochez la case),
puis cliquez sur Créer livraisons.

f) Sélectionnez Afficher journal.

2. Vérifiez les valeurs des zones suivantes pour la livraison créée :

Poste               Quantité livrée               Magasin

a) Dans le journal de livraison, sélectionnez le numéro de la livraison.

b) Vous trouverez les informations requises affichées dans les colonnes correspondantes
dans les infos-clés

3. Quel est désormais le statut global de la commande client ?
____________________________________________
```

---

## PDF page 73

```text
Sujet: Traitement des livraisons sortantes

Astuce :
Utilisez le flux de processus de la livraison sortante pour obtenir ces
informations.

a) Dans les infos-clés de la livraison sortante, sélectionnez Flux du processus.

b) Le statut global de la commande client est maintenant Terminé.

4. Quel est le statut global de la livraison sortante ?

Vous trouverez les informations requises dans la partie supérieure des infos-clés. La
livraison sortante a le statut global En cours.

5. Avant la sortie des articles de la division et l'enregistrement de la sortie de marchandises,
affichez l'état des stocks pour l'article T-MS1## dans la division 1010. Notez le nombre de
pièces en stock à utilisation libre.
a) Dans la barre de lancement SAP Fiori (groupe de vignettes Material Availability), lancez
l'application Stock - Article individuel.

b) Saisissez le numéro d'article et appuyez sur Entrée.

c) Les informations de stock s’affichent à l'écran.
```

---

## PDF page 74

```text
Chapitre 3 : Synthèse des processus de vente

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Traiter les livraisons sortantes
```

---

## PDF page 75

```text
Chapitre 3
Sujet 4

Expédition de marchandises

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Expédier des marchandises

Prélèvement
Gestion des emplacements de magasin – Connexion à SAP EWM

Pour exécuter le processus de prélèvement dans SAP S/4HANA, SAP recommande d'utiliser
SAP Extended Warehouse Management (EWM). Si la livraison sortante créée pendant le
processus de vente est pertinente pour le prélèvement dans un magasin géré par SAP EWM),
elle est transférée à SAP EWM où un ordre de livraison sortante est créé.

Figure 33: Gestion des emplacements de magasin – Connexion à SAP EWM

Un ordre de livraison sortante contient toutes les données nécessaires pour déclencher et
suivre l'intégralité du processus de livraison sortante. En d'autres termes, l'ordre de livraison
sortante est la base de l'exécution des activités de prélèvement.

Lorsque la sortie de marchandises est enregistrée dans SAP EWM, une livraison sortante est
automatiquement créée (dans SAP EWM). Ce document déclenche l'enregistrement de la
sortie de marchandises dans la gestion des stocks.

Les tâches magasin sont utilisées pour exécuter les mouvements de stock dans le magasin.
Elles sont requises pour les activités suivantes :

●  Prélèvement
```

---

## PDF page 76

```text
Chapitre 3 : Synthèse des processus de vente

●  Tâche magasin

●  Mouvements de marchandises internes

●  Transferts

●  Enregistrements d'entrée de marchandises

●  Enregistrements de sortie de marchandises

Tâches magasin

Figure 34: Tâches magasin

La tâche magasin est un document qui indique au magasinier ce qu'il doit faire, par exemple :
Déplacer x palettes du produit y vers l'emplacement ABC. Lorsque la tâche magasin est
exécutée, le magasinier confirme que la quantité du produit est prélevée de l'emplacement
cédant et qu’elle est arrivée à l'emplacement prenant. Tout écart doit être enregistré avec un
code d'exception.

Les tâches magasin sont regroupées dans des ordres magasin. Les ordres magasin sont
utilisés pour contrôler la charge de travail des ressources du magasin. La taille d'un ordre
magasin (comme le nombre d'articles, le poids, les temps requis) est déterminée par les
options de Customizing correspondantes.

Sortie de marchandises
L'enregistrement d'une sortie de marchandises constitue souvent la dernière étape du
processus d'expédition. Lors de cette étape, les opérations suivantes sont automatiquement
exécutées :

●  Gestion des stocks :

Les quantités dans la gestion des stocks et les besoins de livraison dans la planification des
besoins sont mis à jour.

●  Comptes de bilan :

La modification de la valeur dans les comptes de bilan de la comptabilité articles est
enregistrée (les écritures de la pièce comptable correspondante sont basées sur le coût de
l'article).

●  Comptabilité financière :
```

---

## PDF page 77

```text
Sujet: Expédition de marchandises

Des documents supplémentaires sont créés pour la comptabilité financière.

●  Échéancier de factures :

La livraison correspondante peut désormais être utilisée comme base pour la facturation.

●  Mise à jour des statuts :

Le statut de tous les documents associés est mis à jour.

Remarque :
Dans de nombreux processus d'administration des ventes, l'enregistrement des
sorties de marchandises est une condition préalable requise pour la création de
factures à l'étape suivante.

La figure « Enregistrement d'une sortie de marchandises » illustre l'impact d'une sortie de
marchandises.

Figure 35: Enregistrement d'une sortie de marchandises
```

---

## PDF page 78

```text
Chapitre 3 : Synthèse des processus de vente
```

---

## PDF page 79

```text
Chapitre 3
Exercice 6

Prélèvement de marchandises

L'enregistrement d'une sortie de marchandises implique d'abord le prélèvement des articles
correspondants dans le magasin.

1. Créez les tâches magasin correspondantes pour permettre le processus de prélèvement.
Utilisez les informations suivantes :

Nom de zone                             Valeur

Numéro de magasin par défaut           1010

LivrExécLogistq                     Numéro de document de la livraison sor-
tante que vous avez créée à l'exercice pré-
cédent

Date/heure de départ de l'itinéraire          Aujourd'hui et jusqu'à 1 semaine

2. Confirmez les tâches magasin et enregistrez la sortie de marchandises.

3. Une fois que les articles ont quitté la division et que la sortie de marchandises a été
enregistrée, affichez à nouveau les stocks pour l'article T-MS1## dans la division 1010.
Notez le nombre de pièces toujours disponibles en utilisation libre.
____________________________________________

4. Quel nouveau document affecté à la livraison sortante apparaît dans le flux de processus ?
____________________________________________

5. Quel est le statut global de la livraison sortante ?

6. Pourquoi le statut de la livraison sortante n’est-il pas Terminé ?
```

---

## PDF page 80

```text
Chapitre 3
Solution 6

Prélèvement de marchandises

L'enregistrement d'une sortie de marchandises implique d'abord le prélèvement des articles
correspondants dans le magasin.

1. Créez les tâches magasin correspondantes pour permettre le processus de prélèvement.
Utilisez les informations suivantes :

Nom de zone                             Valeur

Numéro de magasin par défaut           1010

LivrExécLogistq                     Numéro de document de la livraison sor-
tante que vous avez créée à l'exercice pré-
cédent

Date/heure de départ de l'itinéraire          Aujourd'hui et jusqu'à 1 semaine

a) Dans la barre de lancement SAP Fiori, lancez l'application Exécution du processus
sortant (groupe de vignettes Shipping and Warehouse Management).

b) Lorsque vous lancez l'application pour la première fois, le système peut vous
demander de définir le magasin par défaut. Dans la boîte de dialogue correspondante,
saisissez le numéro de magasin 1010 et cliquez sur Sauvegarder.

c) En haut à droite de l'écran, cliquez sur Adapter les filtres.

d) Sélectionnez LivrExécLogistq comme critère de filtre supplémentaire.

e) Pour sauvegarder cette variante de filtre pour une utilisation ultérieure, cliquez sur
Sauvegarder sous.

f) Dans la boîte de dialogue Sauvegarder vue, saisissez un nom pour la nouvelle vue.
Vous pouvez également cocher la case Définir comme standard, puis sélectionner
Sauvegarder.

g) Sélectionnez Lancer pour utiliser la nouvelle variante de filtre.

h) Gérez l'entrée de votre choix dans la zone Date/heure de départ pour l'itinéraire en
cliquant sur le bouton situé à droite de la zone.

i) Cliquez sur la flèche, puis sur Du(De)/Au(A) et gérez la période appropriée.

j) Saisissez le numéro de la livraison et cliquez sur Lancer.
Dans la liste, l’ordre de livraison sortante associé à votre livraison s’affiche.

k) Sélectionnez la ligne, puis cliquez sur Créer tâches.

l) Ne quittez pas l'application.

2. Confirmez les tâches magasin et enregistrez la sortie de marchandises.
```

---

## PDF page 81

```text
Sujet: Expédition de marchandises

a) Sélectionnez l’hyperlien du numéro de l'ordre de livraison sortante pour accéder aux
détails correspondants.

b) Cliquez sur Tâches en cours.

c) Sélectionnez les deux tâches magasin dans la liste et cliquez sur Confirmer tâches.
Sélectionnez OK pour confirmer le processus de prélèvement si une fenêtre pop-up
apparaît.

d) Passez maintenant à la catégorie Prélevé en sélectionnant le bouton correspondant.

e) Pour terminer le processus, sélectionnez à nouveau les deux tâches magasin et cliquez
sur Sortie de marchandises.

3. Une fois que les articles ont quitté la division et que la sortie de marchandises a été
enregistrée, affichez à nouveau les stocks pour l'article T-MS1## dans la division 1010.
Notez le nombre de pièces toujours disponibles en utilisation libre.
____________________________________________
a) Dans la barre de lancement SAP Fiori, lancez l'application Stock - Article individuel.

b) Saisissez le numéro d'article et appuyez sur Entrée.
Le stock à utilisation libre a diminué en raison de la sortie de marchandises.

4. Quel nouveau document affecté à la livraison sortante apparaît dans le flux de processus ?
____________________________________________
a) Dans la barre de lancement de SAP Fiori, lancez l'application Gestion des livraisons
sortantes.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Sélectionnez Adapter les filtres.

d) Sélectionnez la zone Livraison sortante, puis cliquez sur OK.

e) Saisissez le numéro de la livraison sortante comme critère de filtre et définissez le
statut global sur SM enregistrée, puis cliquez sur Lancer.

f) Sélectionnez la ligne qui contient votre livraison pour accéder à ses infos-clés.

g) En haut de l'écran, sélectionnez Flux du processus.
Le document article de la sortie de marchandises est répertorié dans le flux de
processus.

5. Quel est le statut global de la livraison sortante ?

Dans les infos-clés de la livraison, vous trouvez le statut global en haut de l'écran. Le statut
global de la livraison sortante est En cours trait.

6. Pourquoi le statut de la livraison sortante n’est-il pas Terminé ?

Le document de facturation associé n'a pas encore été créé.
```

---

## PDF page 82

```text
Chapitre 3 : Synthèse des processus de vente

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Expédier des marchandises
```

---

## PDF page 83

```text
Chapitre 3
Sujet 5

Traitement des documents de facturation

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Traiter les documents de facturation

Documents de facturation
Le principal type de document de facturation est la facture. La création de factures constitue
souvent la dernière étape d'un processus d'administration des ventes. Vous pouvez créer des
factures avec référence aux livraisons sortantes (si vous avez livré de la marchandise au
client) ou avec référence aux commandes client (si vous avez vendu des services).

Le système peut regrouper plusieurs documents précédents (tels que des livraisons
sortantes) dans un document de facturation, à condition que ces documents indiquent les
mêmes valeurs pour les caractéristiques suivantes :

●  Payeur

●  Date de facture

●  Pays destinataire

Le système peut créer des factures en ligne ou comme job d'arrière-plan à exécuter pendant
les heures creuses.

Remarque :
Les autres types de document de facturation, tels que les avoirs, ne sont pas
traités dans ce chapitre.

La figure « Création d'un document de facturation » illustre la création de factures avec
référence aux livraisons sortantes.
```

---

## PDF page 84

```text
Chapitre 3 : Synthèse des processus de vente

Figure 36: Création d'un document de facturation

Structure d'un document de facturation

Un document de facturation est divisé en deux niveaux : niveau de en-tête et niveau poste.
Les données sont réparties entre ces niveaux comme suit :

●  Niveau de l'en-tête :

Les données de l'en-tête s'appliquent à tout le document. L'en-tête comprend notamment
les données relatives au payeur et à la date de facturation.

●  Niveau du poste :

Chaque poste du document de facturation contient ses propres données. Ces données
comprennent, par exemple, des détails sur l'article, les quantités facturées et les valeurs
nettes des postes. Chaque document de facturation peut comprendre plusieurs postes.

La figure « Structure d'un document de facturation » présente la structure des documents de
facturation.
```

---

## PDF page 85

```text
Sujet: Traitement des documents de facturation

Figure 37: Structure d'un document de facturation

Effets d'un document de facturation

Lorsque vous sauvegardez le document de facturation, le système génère automatiquement
tous les documents requis pour la comptabilité. Il passe une écriture au débit sur le compte
de créances du client et une écriture au crédit sur le compte de produits. Les écritures
peuvent être affichées à partir de la pièce comptable correspondante accessible directement
via le document de facturation ou le flux de processus.

En outre, le système peut générer automatiquement d'autres documents pour la comptabilité
financière ainsi que pour le contrôle de gestion et les analyses de rentabilité.

La sauvegarde du document de facturation entraîne les actions suivantes :

●  Le statut de tous les documents de vente, de livraison et de facturation associés est mis à
jour.

●  Les données relatives au plafond de crédit du client sont mises à jour (si la fonction
correspondante est utilisée).

La figure « Effets d'un document de facturation » illustre les effets possibles liés à la création
de documents de facturation.
```

---

## PDF page 86

```text
Chapitre 3 : Synthèse des processus de vente

Figure 38: Effets d'un document de facturation
```

---

## PDF page 87

```text
Chapitre 3
Exercice 7

Création d'un document de facturation

Créez un document de facturation avec référence à la livraison sortante pour facturer les
montants correspondants au client. De plus, vous voulez vous assurer que les documents de
facturation sont automatiquement enregistrés (transfert des données à la comptabilité
financière).

1. Créez le document de facturation pour la livraison sortante de la tâche précédente. Notez
le numéro du document.
____________________________________________

2. Vérifiez la société à laquelle les données ont été imputées dans la comptabilité financière.

3. Quel est le statut global de la livraison sortante ?
____________________________________________

4. Affichez la pièce comptable correspondant au document de facturation et notez les
comptes dans lesquels les différentes écritures ont été passées. Notez le montant total à
payer par T-S50A## Motormarkt Heidelberg.
____________________________________________

____________________________________________

____________________________________________

____________________________________________

5. Quel est le statut global de la pièce comptable ?
```

---

## PDF page 88

```text
Chapitre 3
Solution 7

Création d'un document de facturation

Créez un document de facturation avec référence à la livraison sortante pour facturer les
montants correspondants au client. De plus, vous voulez vous assurer que les documents de
facturation sont automatiquement enregistrés (transfert des données à la comptabilité
financière).

1. Créez le document de facturation pour la livraison sortante de la tâche précédente. Notez
le numéro du document.
____________________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de documents
de facturation.

b) Sélectionnez Options de facturation.

c) Activez Enregistrer automatiquement les documents de facturation et cliquez sur OK.

d) Sélectionnez la ligne contenant le numéro de votre livraison sortante, puis
sélectionnez Créer documents de facturation.

e) Dans l'écran Gestion des documents de facturation, sélectionnez Sauvegarder.
Le numéro de la facture s’affiche en haut à gauche de l'écran.

f) Ne quittez pas l'application.

2. Vérifiez la société à laquelle les données ont été imputées dans la comptabilité financière.

Entre autres informations, la société 1010 correspondante s’affiche dans la catégorie
INFORMATIONS GÉNÉRALES à l'écran.

3. Quel est le statut global de la livraison sortante ?
____________________________________________
a) Dans les infos-clés du document de facturation, sélectionnez FLUX DU PROCESSUS.

b) Dans le flux de processus, sélectionnez la livraison, puis le numéro de livraison (lien
hypertexte) pour accéder aux infos-clés.

c) Vous trouverez le statut global de la livraison en haut de l'écran.
Le statut global de la livraison est maintenant Terminé.

4. Affichez la pièce comptable correspondant au document de facturation et notez les
comptes dans lesquels les différentes écritures ont été passées. Notez le montant total à
payer par T-S50A## Motormarkt Heidelberg.
____________________________________________

____________________________________________

____________________________________________
```

---

## PDF page 89

```text
Sujet: Traitement des documents de facturation

____________________________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des documents de
facturation.

b) Saisissez le numéro du document de facturation comme critère de filtre et appuyez
sur Entrée.

c) Dans la liste, sélectionnez le numéro du document de facturation.

d) Dans la boîte de dialogue, sélectionnez Affichage documents de facturation pour
accéder aux détails du document.

e) Choisissez Gestion comptable en haut de l'écran.

f) Dans la boîte de dialogue Liste des pièces en gestion comptable, double-cliquez sur la
pièce comptable.
Les comptes correspondants s'affichent.

5. Quel est le statut global de la pièce comptable ?

Dans Afficher flux de documents, vous pouvez rechercher le statut dans la colonne
correspondante. La pièce comptable a le statut Non rapproché.
```

---

## PDF page 90

```text
Chapitre 3 : Synthèse des processus de vente

Encaissement
L'enregistrement des encaissements est effectué dans le service de comptabilité financière.
Lorsque vous enregistrez un encaissement, les comptes généraux pertinents sont
automatiquement imputés.

Le système procède comme suit :

●  Comptabilise un débit sur le compte de caisse.

●  Saisie d'un avoir sur le compte de créances du client

Remarque :
Vous pouvez également suivre l'enregistrement des encaissements dans le flux de
processus et la synthèse des statuts. La pièce comptable correspondante reçoit le
statut Rapproché.

La figure « Encaissement » indique les options disponibles pour les encaissements.

Figure 39: Encaissement
```

---

## PDF page 91

```text
Chapitre 3
Exercice 8

Enregistrement d'un encaissement

Lorsqu'un client paie une facture, vous pouvez enregistrer l'encaissement correspondant.

1. Le client a payé à temps et sa demande d'escompte est donc légitime. Notez les valeurs
des conditions de prix respectives que vous pouvez trouver dans le document de
facturation et calculez le montant que le client a dû payer.

Nom de la condition de prix                Valeur de la condition

Prix

TVA collectée

Escompte

Montant à payer

2. Enregistrez l'encaissement à l'aide des informations suivantes :

Nom de zone                             Valeur

Société                             1010

Date comptable                         Date du jour

Date écrit. journal                       Date du jour

Type d'écriture                       DZ (Paiement client)

Compte général                      11100000

Montant                              Montant du paiement calculé

Devise (en regard de la zone Montant)      EUR

Client                              T-S50A##

3. Affichez de nouveau le flux de processus du document de facturation. Quel est désormais
le statut global de la pièce comptable ?
____________________________________________
```

---

## PDF page 92

```text
Chapitre 3
Solution 8

Enregistrement d'un encaissement

Lorsqu'un client paie une facture, vous pouvez enregistrer l'encaissement correspondant.

1. Le client a payé à temps et sa demande d'escompte est donc légitime. Notez les valeurs
des conditions de prix respectives que vous pouvez trouver dans le document de
facturation et calculez le montant que le client a dû payer.

Nom de la condition de prix                Valeur de la condition

Prix

TVA collectée

Escompte

Montant à payer

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des documents de
facturation.

b) Saisissez le numéro du document de facturation comme critère de filtre et
sélectionnez Entrée.

c) Sélectionnez la ligne dans la liste pour accéder aux détails du document.

d) Depuis les détails du document de facturation, sélectionnez ÉLÉMENTS DE PRIX en
haut de l'écran.

e) Notez les valeurs correspondantes et calculez le montant à régler.
Calculez le montant pour le paiement : (Total ligne moins ligne (SKTO) Escompte).
Le résultat de votre calcul est le suivant : 1276 - 38,28 = 1237, 72

2. Enregistrez l'encaissement à l'aide des informations suivantes :

Nom de zone                             Valeur

Société                             1010

Date comptable                         Date du jour

Date écrit. journal                       Date du jour

Type d'écriture                       DZ (Paiement client)

Compte général                      11100000

Montant                              Montant du paiement calculé

Devise (en regard de la zone Montant)      EUR
```

---

## PDF page 93

```text
Sujet: Traitement des documents de facturation

Nom de zone                             Valeur

Client                              T-S50A##

a) Dans la barre de lancement SAP Fiori, lancez l'application Comptabilisation des
encaissements.

b) Saisissez les valeurs de zone répertoriées et sélectionnez Proposer postes.

c) Le document correspondant doit à présent être répertorié comme poste non soldé.
Sur la ligne correspondante, cliquez sur Rapprocher.

d) Pour terminer le processus, en bas à droite de l'écran, cliquez sur Comptabiliser.

3. Affichez de nouveau le flux de processus du document de facturation. Quel est désormais
le statut global de la pièce comptable ?
____________________________________________
a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des documents de
facturation.

b) Saisissez le numéro du document de facturation comme critère de filtre et
sélectionnez Entrée.

c) Sélectionnez la ligne dans la liste pour accéder aux détails du document.

d) En haut de l'écran, sélectionnez FLUX DU PROCESSUS.
Le statut de la pièce comptable est passé à Entièrement Rapproché..
```

---

## PDF page 94

```text
Chapitre 3 : Synthèse des processus de vente

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Traiter les documents de facturation
```

---

## PDF page 95

```text
Chapitre 3

Évaluation des connaissances

1.  Laquelle des étapes suivantes est la première étape du processus d'expédition dans SAP
S/4HANA ?

Sélectionnez la réponse correcte.

X  A Prélèvement et confirmation via les fonctions de gestion des emplacements de
magasin

X  B Emballage

X  C Facturation

X  D Création de livraisons sortantes

2. Lequel des niveaux suivants contient les quantités de livraison et les dates de livraison
dans la structure du document de vente ?

Sélectionnez la réponse correcte.

X  A Niveau de l'en-tête

X  B Niveau du poste

X  C Niveau de l'échéance

3. Vous pouvez créer une seule livraison sortante avec référence à une seule commande.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

4. Chaque échéance du document de vente peut devenir un poste du document de livraison.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 96

```text
Chapitre 3 : Évaluation des connaissances

5. Parmi les documents suivants, lequel constitue la base de l'exécution des activités de
prélèvement dans SAP EWM ?

Sélectionnez la réponse correcte.

X  A Ordre de livraison sortante

X  B Document de sortie de marchandises

X  C Tâches magasin

X  D Ordre magasin

6. Les tâches magasin sont regroupées dans des ressources magasin.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

7. Lorsque vous sauvegardez le document de facturation, toutes les pièces requises pour la
comptabilité sont générées.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 97

```text
Chapitre 3

Évaluation des connaissances - Réponses

1.  Laquelle des étapes suivantes est la première étape du processus d'expédition dans SAP
S/4HANA ?

Sélectionnez la réponse correcte.

X  A Prélèvement et confirmation via les fonctions de gestion des emplacements de
magasin

X  B Emballage

X  C Facturation

X  D Création de livraisons sortantes

Correct. Dans SAP S/4HANA, la création de livraisons sortantes est la première étape du
processus d'expédition.

2. Lequel des niveaux suivants contient les quantités de livraison et les dates de livraison
dans la structure du document de vente ?

Sélectionnez la réponse correcte.

X  A Niveau de l'en-tête

X  B Niveau du poste

X  C Niveau de l'échéance

Correct. Les échéances contiennent les quantités de livraison et les dates de livraison
appartenant à un poste.

3. Vous pouvez créer une seule livraison sortante avec référence à une seule commande.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Vous pouvez créer une ou plusieurs livraisons sortantes avec référence à une
seule commande.
```

---

## PDF page 98

```text
Chapitre 3 : Évaluation des connaissances - Réponses

4. Chaque échéance du document de vente peut devenir un poste du document de livraison.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Contrairement aux documents de vente, les documents de livraison ne
contiennent aucune échéance. Chaque échéance du document de vente peut devenir un
poste du document de livraison.

5. Parmi les documents suivants, lequel constitue la base de l'exécution des activités de
prélèvement dans SAP EWM ?

Sélectionnez la réponse correcte.

X  A Ordre de livraison sortante

X  B Document de sortie de marchandises

X  C Tâches magasin

X  D Ordre magasin

Correct. Un ordre de livraison sortante contient toutes les données nécessaires pour
déclencher et suivre l'intégralité du processus de livraison sortante. En d'autres termes,
l'ordre de livraison sortante est la base de l'exécution des activités de prélèvement.

6. Les tâches magasin sont regroupées dans des ressources magasin.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Les tâches magasin sont regroupées dans des ordres magasin. Les ordres
magasin sont utilisés pour contrôler la charge de travail des ressources du magasin.

7. Lorsque vous sauvegardez le document de facturation, toutes les pièces requises pour la
comptabilité sont générées.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Lorsque vous sauvegardez le document de facturation, le système génère
automatiquement tous les documents requis pour la comptabilité.
```

---

## PDF page 99

```text
CHAPITRE 4  Données de base

Sujet 1

Gestion des données de base partenaire                                           90
Exercice 9 : Création de données de base client                               95
Exercice 10 : Utilisation des données de base partenaire                            101

Sujet 2

Gestion des données de base article                                                   106
Exercice 11 : Création d'une fiche article                                      109

Sujet 3

Gestion des fiches infos client-article                                                             117
Exercice 12 : Création d'une fiche infos client-article                                 119

Sujet 4

Gestion des données de base de condition pour la détermination du prix                       124
Exercice 13 : Création d'un enregistrement de condition (prix de vente)               127
Exercice 14 : Création d'un enregistrement de condition (remise)                      131
Exercice 15 : Description du contexte des données de base de condition             135

Sujet 5

Explication des sujets complémentaires touchant aux données de base                        138
Exercice 16 : Création de postes par défaut                                     145
Exercice 17 : Gestion des documents de vente incomplets                             151

OBJECTIFS DU CHAPITRE

●  Gérer les données de base du partenaire/client

●  Gestion des données de base article

●  Gestion des fiches infos client-article

●  Gérer les données de base de condition pour la détermination du prix

●  Expliquer les sujets complémentaires touchant aux données de base
```

---

## PDF page 100

```text
Chapitre 4
Sujet 1

Gestion des données de base partenaire

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Gérer les données de base du partenaire/client

Source de données des documents de vente
Les données des documents de vente peuvent provenir de différentes sources. La plupart des
données copiées sont utilisées comme valeurs par défaut qu'il est possible de remplacer dans
le document, si nécessaire.

Ces sources de données sont notamment les suivantes :

●  Données de base partenaire (client)

●  Données de base article

●  Fiche info client-article (ces données de base permettent notamment de gérer les
numéros d'article du client)

●  Données de base de la condition (s'appliquent à la détermination automatique du prix, telle
qu'un prix d'article ou une remise accordée à un client)

●  Données de base des messages (messages permettant d'envoyer des informations au
client par e-mail, échange de données informatisées (EDI) ou fax. Il peut s'agir, par
exemple, d'une offre ou d'une confirmation de commande imprimée)

●  Tables de pilotage gérées dans le Customizing (en fonction des options de ces tables, on
peut piloter dans les documents de vente les valeurs par défaut provenant de différentes
données)

Remarque :
Un document de vente précédent peut également servir de source de données
pour un autre document de vente. Par exemple, une offre peut servir de source de
données pour une commande client.

La figure « Origine des données dans les documents de vente » illustre les différentes sources
de données des documents de vente.
```

---

## PDF page 101

```text
Sujet: Gestion des données de base partenaire

Origine des données dans les documents de vente

Figure 40: Origine des données dans les documents de vente

Les données sont organisées en vues qui sont affectées aux entités organisationnelles
(division, organisation commerciale, etc.). La structure des fiches permet de représenter de
manière souple les diverses structures organisationnelles d'une organisation.

Lorsque les données correspondantes (telles que des informations sur les partenaires ou
articles) sont intégrées dans un seul objet de base de données, la redondance des données
n'est plus un problème et l'intégrité des données est améliorée. Tous les domaines utilisent
les mêmes données stockées, notamment les ventes, les achats, la gestion des stocks, la
planification des besoins, le contrôle des factures, les finances et les ressources humaines.

Données de base partenaire
Les données de base des clients et fournisseurs sont gérées dans SAP S/4HANA à l'aide de
données de base du partenaire. Grâce à cette approche, il est possible de gérer de façon
centralisée les données de base des clients et des fournisseurs (dans SAP ERP, elles étaient
gérées séparément).

Les données de base partenaire peuvent être gérées via la transaction BP ou à l’aide d’une
application correspondante depuis la barre de lancement SAP Fiori.
```

---

## PDF page 102

```text
Chapitre 4 : Données de base

Figure 41: Approche partenaire dans SAP S/4HANA

Lors de la création d'un partenaire, la catégorie de partenaire doit être sélectionnée. Les
partenaires peuvent être classés en tant que personne, groupe ou organisation. Un groupe
représente des personnes vivant en cohabitation, un couple marié ou un directoire. Une
organisation représente des unités comme une entreprise, un service d'entreprise ou une
association.

Le lien entre un partenaire et d'autres composantes se traduit par un concept de rôle. Un rôle
partenaire correspond à un contexte de gestion dans lequel peut apparaître un partenaire.
Les rôles possibles sont, par exemple, le client SD (pertinent pour les processus de vente), le
client FI ou le fournisseur. Cela garantit que les données de base pertinentes pour les
différents processus peuvent être enregistrées en conséquence et que le partenaire peut être
utilisé pour les fonctions correspondantes (par exemple, donneur d'ordre).

Structure des données de base client

Figure 42: Structure des données de base client
```

---

## PDF page 103

```text
Sujet: Gestion des données de base partenaire

Les données partenaire pertinentes pour les clients (rôles partenaire Client SD et Client FI)
sont regroupées dans les catégories suivantes : données générales, données du domaine
commercial et données société. La fiche client comprend toutes les données nécessaires au
traitement des commandes, des livraisons, des factures et des encaissements des clients.

Les données générales sont valables pour les ventes et la comptabilité. Elles sont communes
à toutes les entités organisationnelles d'un mandant.

Les données du domaine commercial sont propres à l'administration des ventes. Elles
s'appliquent au domaine commercial correspondant (organisation commerciale, canal de
distribution, secteur d'activité).

Les données société sont propres à la comptabilité. Elles s'appliquent à la société
correspondante.

Les données de base client les plus importantes pour l'administration des ventes peuvent être
gérées dans les données du domaine commercial. Pour faciliter la gestion des données, les
zones pertinentes sont réparties dans différentes pages à onglet. Les principales sont les
suivantes :

●  de transfert

●  Expédition

●  Facturation

●  Rôles partenaires

Remarque :
Pour utiliser un client dans différents domaines commerciaux au cours des
processus des ventes, les données de base du client doivent être gérées en
conséquence pour les domaines commerciaux concernés.

Enfin, les données de base client relatives à la société comprennent des informations liées
principalement aux fonctions de comptabilité. C'est pourquoi ces données sont souvent
gérées par le service Comptabilité.
```

---

## PDF page 104

```text
Chapitre 4 : Données de base
```

---

## PDF page 105

```text
Chapitre 4
Exercice 9

Création de données de base client

Un nouveau client souhaite passer une commande et acheter certains articles. Créez une
fiche pour le partenaire (catégorie : organisation) et sauvegardez-la.

1. Créez la fiche partenaire à l'aide des informations suivantes :
Données de base :

Nom de zone                             Valeur

Partenaire                          T-CUS##

Regroupement                       BPAB Num alpha ext (a-z;CUST/
SUPL)

Nom 1                              Motos et autres

Rôles :

ID du rôle                                  Description du rôle

FLCU00                                   Partenaire Client FI

FLCU01                                   Partenaire Client

Adresse :

Nom de zone                             Valeur

Rue                               Rue principale

Numéro de rue                       ##

Code postal                         20111

Ville                               Hambourg

Pays                               DE (Allemagne)

Région                             HH (Hambourg)

Langue                             EN

Domaines commerciaux :

Nom de zone                             Valeur

Organisation commerciale              1010

Canal distribution                     10
```

---

## PDF page 106

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Secteur d'activité                     00

Devise                             EUR

Conditions d'expédition                 ## (+50) Standard

Division livraison                      1010

Incoterms                           DAP (Rendu au lieu destination)

Lieu incoterm 1                       Hambourg

Conditions de paiement                ZB00 Payable immédiatement sans
déduction

Groupe d'imputation client              Revenus intérieurs

Schéma client                        S (client standard)

Catégorie de taxe (pour le pays DE)        TTX1

Classification fiscale                   1 (Soumis aux taxes)

Sociétés :

Nom de zone                             Valeur

Société                             1010

Compte collectif                      12100000

2. Pour la fiche partenaire créée précédemment, notez les valeurs ayant été
automatiquement définies pour les rôles partenaire obligatoires.

Rôle partenaire                      Numéro de partenaire

Donneur d'ordre

Réceptionnaire

Destinataire de la facture

Payeur
```

---

## PDF page 107

```text
Chapitre 4
Solution 9

Création de données de base client

Un nouveau client souhaite passer une commande et acheter certains articles. Créez une
fiche pour le partenaire (catégorie : organisation) et sauvegardez-la.

1. Créez la fiche partenaire à l'aide des informations suivantes :
Données de base :

Nom de zone                             Valeur

Partenaire                          T-CUS##

Regroupement                       BPAB Num alpha ext (a-z;CUST/
SUPL)

Nom 1                              Motos et autres

Rôles :

ID du rôle                                  Description du rôle

FLCU00                                   Partenaire Client FI

FLCU01                                   Partenaire Client

Adresse :

Nom de zone                             Valeur

Rue                               Rue principale

Numéro de rue                       ##

Code postal                         20111

Ville                               Hambourg

Pays                               DE (Allemagne)

Région                             HH (Hambourg)

Langue                             EN

Domaines commerciaux :

Nom de zone                             Valeur

Organisation commerciale              1010

Canal distribution                     10
```

---

## PDF page 108

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Secteur d'activité                     00

Devise                             EUR

Conditions d'expédition                 ## (+50) Standard

Division livraison                      1010

Incoterms                           DAP (Rendu au lieu destination)

Lieu incoterm 1                       Hambourg

Conditions de paiement                ZB00 Payable immédiatement sans
déduction

Groupe d'imputation client              Revenus intérieurs

Schéma client                        S (client standard)

Catégorie de taxe (pour le pays DE)        TTX1

Classification fiscale                   1 (Soumis aux taxes)

Sociétés :

Nom de zone                             Valeur

Société                             1010

Compte collectif                      12100000

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des données de base
clients.

b) Sélectionnez Créer, puis Organisation.

c) Dans la boîte de dialogue Créer organisation, gérez les différentes valeurs de zones
indiquées dans l'exercice (gérer le rôle FLCU01).

d) Sélectionnez OK pour accéder aux détails du partenaire.

e) Accédez à la catégorie Domaines commerciaux.

f) Pour gérer les données du domaine commercial, sélectionnez la flèche située à droite
de la ligne qui contient le domaine commercial, puis saisissez les informations
correspondantes.

g) Dans la partie inférieure droite de l'écran, sélectionnez Appliquer pour revenir aux
données principales du partenaire.

h) Accédez à la catégorie Rôles.

i) Sélectionnez Créer, puis le rôle FLCU00 dans la zone Rôle partenaire.

j) Accédez à la catégorie Sociétés.

k) Assurez-vous que le compte collectif est affiché à côté de la société. Si ce n'est pas le
cas, saisissez-le.
```

---

## PDF page 109

```text
Sujet: Gestion des données de base partenaire

l) Pour sauvegarder/créer le nouveau partenaire, cliquez sur Créer en bas à droite de
l'écran.

Remarque :
Si vous avez accédé aux données de la société en cliquant sur la flèche à
droite de la ligne contenant la société, vous devez sélectionner Appliquer
pour pouvoir sélectionner Sauvegarder.

2. Pour la fiche partenaire créée précédemment, notez les valeurs ayant été
automatiquement définies pour les rôles partenaire obligatoires.

Rôle partenaire                      Numéro de partenaire

Donneur d'ordre

Réceptionnaire

Destinataire de la facture

Payeur

a) Passez à nouveau à la catégorie Domaines commerciaux et sélectionnez la ligne
contenant le domaine commercial géré.

b) Recherchez les informations requises dans la zone d'écran Fonctions partenaire.
```

---

## PDF page 110

```text
Chapitre 4 : Données de base

Rôles partenaire dans les données de base client
Rôles partenaire dans la fiche partenaire (rôle : client)

Au cours d’un processus de ventes dans SAP S/4HANA, plusieurs rôles partenaires sont
importants. Un rôle partenaire est celui qu'un partenaire peut endosser au cours d'un
processus. Par exemple, un client commande certains produits (rôle partenaire : donneur
d'ordre) et un autre client reçoit un article (rôle partenaire : réceptionnaire).

Pour la gestion des commandes clients, les rôles partenaires donneur d'ordre, réceptionnaire,
payeur et destinataire de la facture sont obligatoires :

●  Donneur d'ordre :

Client qui passe la commande.

●  Réceptionnaire :

Client qui reçoit les marchandises ou les services.

●  Destinataire de la facture :

Client qui reçoit la facture.

●  Payeur :

Client qui paie la facture.

Au cours de la gestion d'une commande client, les rôles partenaires peuvent être identiques
ou différents. Comme ils sont obligatoires pour les documents de vente, les valeurs par défaut
correspondantes doivent être gérées dans les données de base partenaire.

D'autres fonctions partenaire, telles que le contact ou le transporteur, ne sont pas
obligatoires pour la gestion des commandes client, mais peuvent être importantes pour des
opérations de vente plus complexes, par exemple, les commandes exportation. C’est
pourquoi ces rôles partenaire peuvent également être gérés dans la fiche partenaire.

La figure Rôles partenaire dans la fiche partenaire (rôle : client) illustre les rôles partenaire
obligatoires pour les processus de vente.

Figure 43: Rôles partenaire dans la fiche partenaire (rôle : client SD)
```

---

## PDF page 111

```text
Chapitre 4
Exercice 10

Utilisation des données de base partenaire

Le client vous informe qu'un réceptionnaire supplémentaire est nécessaire pour les
prochaines livraisons. Pour faciliter la gestion des commandes, enregistrez le réceptionnaire
supplémentaire dans la fiche partenaire du donneur d'ordre. Ensuite, créez une commande
pour ce client.

1. Modifiez la fiche partenaire du donneur d'ordre de l'exercice précédent. Dans les données
du domaine commercial, ajoutez un autre réceptionnaire avec les informations suivantes :

Nom de zone                             Valeur

Client                              T-CUS##

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Réceptionnaire supplémentaire           T-S50A##

2. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-CUS##

Réceptionnaire                       T-S50A##

Réf. client                           5-9##

DateLivrSouh.                        Dans 1 semaine

Article                                        Quantité

T-MS2##                              2

3. Sauvegardez la commande et notez son numéro.
____________________________________________
```

---

## PDF page 112

```text
Chapitre 4 : Données de base

4. Comment pouvez-vous vérifier l'auteur et la date de création de la fiche partenaire dans le
système ?

5. Pouvez-vous gérer diverses adresses pour le client en fonction des sociétés dans la fiche
partenaire ?
```

---

## PDF page 113

```text
Chapitre 4
Solution 10

Utilisation des données de base partenaire

Le client vous informe qu'un réceptionnaire supplémentaire est nécessaire pour les
prochaines livraisons. Pour faciliter la gestion des commandes, enregistrez le réceptionnaire
supplémentaire dans la fiche partenaire du donneur d'ordre. Ensuite, créez une commande
pour ce client.

1. Modifiez la fiche partenaire du donneur d'ordre de l'exercice précédent. Dans les données
du domaine commercial, ajoutez un autre réceptionnaire avec les informations suivantes :

Nom de zone                             Valeur

Client                              T-CUS##

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Réceptionnaire supplémentaire           T-S50A##

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des données de base
clients.

b) Saisissez le numéro du client dans la zone Partenaire puis sélectionnez Lancer.

c) Dans la liste, sélectionnez la ligne contenant le partenaire correspondant.

d) En haut à droite de l'écran, sélectionnez Modifier.

e) Sélectionnez la zone d'écran Domaines commerciaux, puis la ligne contenant votre
domaine commercial.

f) Dans la zone d'écran Fonctions partenaire, sélectionnez Créer.

g) Saisissez le rôle partenaire CL (réceptionnaire) et T-S50A## comme numéro de
partenaire dans l'écran Rôle partenaire.

h) Cliquez sur Appliquer en bas à droite de l'écran.

i) Cliquez sur Sauvegarder pour sauvegarder vos modifications.

2. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10
```

---

## PDF page 114

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Secteur d'activité                     00

Donneur d'ordre                      T-CUS##

Réceptionnaire                       T-S50A##

Réf. client                           5-9##

DateLivrSouh.                        Dans 1 semaine

Article                                        Quantité

T-MS2##                              2

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, renseignez les zones pertinentes et appuyez sur Entrée.

c) Gérez les informations comme indiqué ci-dessus.

3. Sauvegardez la commande et notez son numéro.
____________________________________________

a) Cliquez sur Sauvegarder.
Le numéro de document s’affiche à l'écran.

4. Comment pouvez-vous vérifier l'auteur et la date de création de la fiche partenaire dans le
système ?

Vous trouverez les informations requises dans l’application Gestion des données de base
client, catégorie Données de base, dans la zone Informations générales.

5. Pouvez-vous gérer diverses adresses pour le client en fonction des sociétés dans la fiche
partenaire ?

Non. Les adresses sont gérées indépendamment des entités organisationnelles.
```

---

## PDF page 115

```text
Sujet: Gestion des données de base partenaire

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Gérer les données de base du partenaire/client
```

---

## PDF page 116

```text
Chapitre 4
Sujet 2

Gestion des données de base article

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Gestion des données de base article

Données de base article
Les fiches articles sont utilisées dans différents processus. L'existence d'une fiche article est
obligatoire pour un grand nombre de fonctions de gestion telles que la gestion des stocks, par
exemple.

Dans les données de base article, vous pouvez gérer des informations détaillées (description,
poids ou taxe, par exemple).

Étant donné que plusieurs départements (comme les achats, les ventes, le stockage ou la
comptabilité) utilisent souvent les données de base article, les informations correspondantes
doivent être gérées en conséquence pour ces différents départements.

Figure 44: Données de base article

Données de base article pour l'administration des ventes

Les données de base article s'appliquant aux processus d'administration des ventes sont
disponibles dans plusieurs pages à onglet :

●  Les données de base s'appliquent à tous les domaines. Elles sont gérées indépendamment
des entités organisationnelles.
```

---

## PDF page 117

```text
Sujet: Gestion des données de base article

●  Les pages à onglet ADV : données org.commerc 1 et ADV: données org. commerc 2 ainsi
que le texte ADV sont valides pour l'organisation commerciale et le canal de distribution
correspondants

●  Les pages à onglet ADV : données générales/division sont valides pour la division chargée
de la livraison correspondante.

En modifiant les options du Customizing, vous pouvez masquer certaines zones d'une page à
onglet ou les rendre obligatoires.

Figure 45: Données de base article pour l'administration des ventes
```

---

## PDF page 118

```text
Chapitre 4 : Données de base
```

---

## PDF page 119

```text
Chapitre 4
Exercice 11

Création d'une fiche article

Vous avez ajouté un article à une gamme de produits et vous souhaitez créer la fiche article
correspondante.

1. Le nouvel article est un phare, similaire à l'article existant T-MS1##. Pour ce faire, vous
utilisez l'article T-MS1## comme modèle. Créez la nouvelle fiche article à l'aide des
données ci-après (à l'exception de ces données, l'article a les mêmes propriétés que celles
proposées par le système pour l'article de référence T-MS1##).

Remarque :
Gérez les vues Données de base 1, ADV: données commer 1+2, ADV : données
générales/division et texte ADV

Nom de zone                             Valeur

Numéro d’article                      T-MS4##

Branche                            Commerce

Type d'article                        Prod. commercialisables

Article modèle                       T-MS1##

Division                            1010

Org. commerciale                     1010

Canal de distribution                   10

Classification fiscale                   1

Astuce :
Utilisez également les entités organisationnelles indiquées pour l'article de
référence.

Nom de zone                             Valeur

Description (désignation) de l'article       Phare standard

Quantité minimale commande client       10 pièces

Texte ADV                          Article fragile !

Prix de vente                         35 EUR pour une quantité échelon-
née de 1 pièce ou plus
```

---

## PDF page 120

```text
Chapitre 4 : Données de base

2. Vous souhaitez vérifier si le nouvel article peut désormais être utilisé dans les commandes
clients. Vous allez donc créer une commande client en utilisant les informations
suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-13##

DateLivrSouh.                         dans 10 jours

Article                             T-MS4##

Qté d'ordre                          5 pièces

3. Le système vérifie-t-il la quantité minimale de commande ?
_____________________________________

4. Le texte ADV a-t-il été copié de la fiche article vers la commande client (au niveau du
poste) ?
_____________________________________

5. Sauvegardez la commande client et notez son numéro.
_____________________________________

6. Vous souhaitez vendre vos articles via diverses organisations commerciales. Est-il
possible de gérer plusieurs unités de vente dans la fiche article en fonction de
l'organisation commerciale et du canal de distribution ?

7. Vous souhaitez livrer vos articles à partir de plusieurs divisions. Est-il possible de gérer
plusieurs groupes de chargement dans la fiche article en fonction de la division ?

8. Est-il possible de gérer plusieurs quantités minimales de commande client dans la fiche
article en fonction du secteur d'activité ?
```

---

## PDF page 121

```text
Chapitre 4
Solution 11

Création d'une fiche article

Vous avez ajouté un article à une gamme de produits et vous souhaitez créer la fiche article
correspondante.

1. Le nouvel article est un phare, similaire à l'article existant T-MS1##. Pour ce faire, vous
utilisez l'article T-MS1## comme modèle. Créez la nouvelle fiche article à l'aide des
données ci-après (à l'exception de ces données, l'article a les mêmes propriétés que celles
proposées par le système pour l'article de référence T-MS1##).

Remarque :
Gérez les vues Données de base 1, ADV: données commer 1+2, ADV : données
générales/division et texte ADV

Nom de zone                             Valeur

Numéro d’article                      T-MS4##

Branche                            Commerce

Type d'article                        Prod. commercialisables

Article modèle                       T-MS1##

Division                            1010

Org. commerciale                     1010

Canal de distribution                   10

Classification fiscale                   1

Astuce :
Utilisez également les entités organisationnelles indiquées pour l'article de
référence.

Nom de zone                             Valeur

Description (désignation) de l'article       Phare standard

Quantité minimale commande client       10 pièces

Texte ADV                          Article fragile !

Prix de vente                         35 EUR pour une quantité échelon-
née de 1 pièce ou plus
```

---

## PDF page 122

```text
Chapitre 4 : Données de base

a) Dans la barre de lancement SAP Fiori, lancez l'application Créer article.

b) Saisissez le nouveau numéro d'article, la branche d’activité, le type d'article et le
numéro de l'article de référence.

c) Pour appeler la sélection de vues, sélectionnez Suite.

d) Sélectionnez les vues appropriées.

e) Appelez la boîte de dialogue Niveaux organisationnels en appuyant sur Suite (Entrée).

f) Saisissez les niveaux organisationnels correspondants et incluez-les aussi dans la
section Copier à partir de.

g) Pour appeler les vues sélectionnées de la fiche article, appuyez sur Suite (Entrée).

h) Gérez les valeurs de zone répertoriées dans le tableau ci-dessus.

i) Pour gérer le prix de vente, dans la vue ADV: org. comm1, cliquez d'abord sur le bouton
Conditions.

j) Ne renseignez pas la quantité échelonnée et saisissez le prix de vente (zone Montant).
Revenez ensuite en arrière.

k) Dans la fiche article, sélectionnez Sauvegarder.

2. Vous souhaitez vérifier si le nouvel article peut désormais être utilisé dans les commandes
clients. Vous allez donc créer une commande client en utilisant les informations
suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-13##

DateLivrSouh.                         dans 10 jours

Article                             T-MS4##

Qté d'ordre                          5 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, gérez le type de commande et les entités organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Gérez les données correspondantes comme indiqué dans le tableau ci-dessus.

3. Le système vérifie-t-il la quantité minimale de commande ?
_____________________________________
```

---

## PDF page 123

```text
Sujet: Gestion des données de base article

a) Oui, un message système vous indique que la quantité commandée minimale pour cet
article est de 10 pièces.

b) Acceptez le message en appuyant sur Entrée.

4. Le texte ADV a-t-il été copié de la fiche article vers la commande client (au niveau du
poste) ?
_____________________________________

a) Double-cliquez sur le poste.

b) Sélectionnez la page à onglet Textes.
Le texte ADV de l'article s’affiche.

5. Sauvegardez la commande client et notez son numéro.
_____________________________________

a) Dans la commande client, sélectionnez Sauvegarder.

6. Vous souhaitez vendre vos articles via diverses organisations commerciales. Est-il
possible de gérer plusieurs unités de vente dans la fiche article en fonction de
l'organisation commerciale et du canal de distribution ?

Oui. Dans la fiche article, il existe diverses façons de gérer plusieurs zones, telles que les
unités de vente, en fonction de l'organisation commerciale et du canal de distribution.

7. Vous souhaitez livrer vos articles à partir de plusieurs divisions. Est-il possible de gérer
plusieurs groupes de chargement dans la fiche article en fonction de la division ?

Oui. Dans la fiche article, il existe diverses façons de gérer plusieurs zones telles que le
groupe de chargement en fonction de la division.

8. Est-il possible de gérer plusieurs quantités minimales de commande client dans la fiche
article en fonction du secteur d'activité ?

Non.  Il n'est pas possible de gérer les valeurs de zone des données de base article en
fonction du secteur d'activité. Un secteur d'activité est affecté à un seul article.
```

---

## PDF page 124

```text
Chapitre 4 : Données de base

Ventes propres à un secteur d'activité ou liées à plusieurs secteurs

Ventes liées à plusieurs secteurs d'activité

Le Customizing des types de document de vente inclut certains paramètres qui permettent
de choisir entre la gestion des ventes propres à un secteur d'activité ou valables pour tous les
secteurs. Vous pouvez ajuster ces paramètres pour contrôler :

●   si le secteur d'activité au niveau du poste est copié à partir de la fiche article
correspondante ou si le secteur d'activité figurant dans l'en-tête du document s'applique
également aux postes ;

●   la façon dont le système doit répondre (aucune réaction, message d'avertissement ou
message d'erreur) si le secteur d'activité des articles de la commande client est différent
de celui figurant dans l'en-tête.

Un scénario possible consiste à autoriser les ventes pour tous les secteurs d'activité (ou
centralisées), où plusieurs articles de différents secteurs d'activité peuvent être vendus dans
la même commande client. Ce scénario s’applique généralement à un seul département des
ventes capable de vendre tous les produits d'une entreprise, indépendamment de leur
secteur d’activités.

La figure « Ventes liées à plusieurs secteurs d'activité » représente un exemple de vente multi
secteurs d'activité.

Figure 46: Ventes liées à plusieurs secteurs d'activité

Ventes propres à un secteur d'activité

Les paramètres du Customizing permettent également d'empêcher la vente d'articles dont le
secteur d'activité est différent de celui figurant dans l'en-tête de la commande. Cela
permettrait de réaliser des ventes propres à un secteur d'activité (ou décentralisées), chaque
domaine commercial ne pouvant vendre que des articles affectés à son propre secteur
d'activité. Dans ce cas, il n'est pas possible de regrouper dans la même commande client des
articles de différents secteurs d'activité. Ce scénario représente généralement une
organisation qui a plusieurs départements des ventes, chacun étant responsable de vendre
uniquement les produits propres à sa famille ou à son regroupement.
```

---

## PDF page 125

```text
Sujet: Gestion des données de base article

La figure « Ventes propres à un secteur d'activité » illustre les restrictions des ventes propres
au secteur d'activité.

Figure 47: Ventes propres à un secteur d'activité
```

---

## PDF page 126

```text
Chapitre 4 : Données de base

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Gestion des données de base article
```

---

## PDF page 127

```text
Chapitre 4
Sujet 3

Gestion des fiches infos client-article

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Gestion des fiches infos client-article

Fiche infos client-article
Vous pouvez utiliser une fiche infos client-article pour stocker les données article propres à
un client. Les informations suivantes peuvent notamment être gérées dans la fiche infos
client-article :

●  Référence du numéro d'article propre au client correspondant à votre numéro d'article ;

●  Description de l'article propre au client ;

●  Informations d'expédition propres à l'article définies pour le client (telles que les
tolérances de livraison, le pilotage des livraisons partielles, la valeur par défaut de la
division chargée de la livraison).

La figure « Fiche infos client-article » illustre des informations pouvant être gérées dans une
fiche infos client-article.

Figure 48: Fiche infos client-article
```

---

## PDF page 128

```text
Chapitre 4 : Données de base

Saisie de commandes à l'aide de fiches infos client-article

Si une fiche infos client-article a été définie pour un client et un article, les valeurs par défaut
correspondantes (division chargée de la livraison, par exemple) sont utilisées prioritairement
aux valeurs correspondantes définies dans la fiche client ou article lors de la création d'un
document tel qu'une commande client.

Remarque :
Dans les commandes client, vous pouvez saisir les numéros d'article propres au
client directement dans la page à onglet Acheteur. Le système détermine ensuite
votre numéro d'article via la fiche infos client-article correspondante.

La figure « Saisie de commandes à l'aide de fiches infos client-article » illustre cette fonction.

Figure 49: Saisie de commandes à l'aide de fiches infos client-article
```

---

## PDF page 129

```text
Chapitre 4
Exercice 12

Création d'une fiche infos client-article

Certains clients importants commandent généralement des articles à l'aide de leurs propres
numéros d'article. Pour faciliter la gestion des commandes clients, utilisez les données de
base des fiches infos client-article.

1. L'un de vos clients importants commande des articles en utilisant ses propres numéros
d'article. Créez une fiche infos client-article à l'aide des données suivantes :

Nom de zone                             Valeur

Client                              T-S50A##

Organisation commerciale              1010

Canal de distribution                   10

Produit                             T-MS1##

Article client                         K-MS-##

Description article client                Phare Premium

2. Le client passe une commande pour la première fois en utilisant son propre numéro
d'article. Créez la commande client correspondante à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Organisation commerciale              1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-19##

DateLivrSouh.                         dans 1 semaine

Numéro d'article client                 K-MS-##

Quantité commandée                  10 pièces

3. Sauvegardez la commande client et notez son numéro.
_____________________________________

4. Créez une livraison sortante pour la commande client précédente à l’aide des
informations suivantes et notez le numéro de document.
```

---

## PDF page 130

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

Numéro de livraison : ____________________________________________

5. Vérifiez si la désignation de l'article client apparaît dans la livraison sortante.
```

---

## PDF page 131

```text
Chapitre 4
Solution 12

Création d'une fiche infos client-article

Certains clients importants commandent généralement des articles à l'aide de leurs propres
numéros d'article. Pour faciliter la gestion des commandes clients, utilisez les données de
base des fiches infos client-article.

1. L'un de vos clients importants commande des articles en utilisant ses propres numéros
d'article. Créez une fiche infos client-article à l'aide des données suivantes :

Nom de zone                             Valeur

Client                              T-S50A##

Organisation commerciale              1010

Canal de distribution                   10

Produit                             T-MS1##

Article client                         K-MS-##

Description article client                Phare Premium

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des articles clients.

b) Sélectionnez Créer pour créer une fiche.

c) Gérez les informations correspondantes.

d) Cliquez sur Créer.

2. Le client passe une commande pour la première fois en utilisant son propre numéro
d'article. Créez la commande client correspondante à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Organisation commerciale              1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-19##

DateLivrSouh.                         dans 1 semaine

Numéro d'article client                 K-MS-##

Quantité commandée                  10 pièces
```

---

## PDF page 132

```text
Chapitre 4 : Données de base

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de la transaction, saisissez le type de commande et les données
d’organisation.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Saisissez les valeurs de zone appropriées du tableau ci-dessus.

3. Sauvegardez la commande client et notez son numéro.
_____________________________________

a) Dans la commande client, sélectionnez Sauvegarder.

4. Créez une livraison sortante pour la commande client précédente à l’aide des
informations suivantes et notez le numéro de document.

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

Numéro de livraison : ____________________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) En haut de l'écran, saisissez le point d'expédition et renseignez correctement la zone
Date de création planifiée.

d) Pour lancer la sélection, en haut à droite de l'écran, sélectionnez Lancer.

e) Sélectionnez la commande client pertinente dans la liste puis cliquez sur Créer
livraisons.

f) Pour accéder au journal de la création de la livraison, sélectionnez Afficher journal.

5. Vérifiez si la désignation de l'article client apparaît dans la livraison sortante.
a) Dans le journal, sélectionnez le numéro de la livraison sortante.

b) Sélectionnez la ligne du poste correspondant. Le poste contient la description de
l'article client.
```

---

## PDF page 133

```text
Sujet: Gestion des fiches infos client-article

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Gestion des fiches infos client-article
```

---

## PDF page 134

```text
Chapitre 4
Sujet 4

Gestion des données de base de condition
pour la détermination du prix

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Gérer les données de base de condition pour la détermination du prix

Données de base de condition
Les données de base de condition incluent les données de base des prix, majorations et
remises, frais de transport et taxes.

Chaque enregistrement de condition peut dépendre de diverses caractéristiques. Par
exemple, un prix d'article peut être propre au client ou une remise peut dépendre du client et
du groupe d'articles.

Dans le Customizing, vous pouvez définir de façon souple les caractéristiques principales
dont dépendent les prix, les majorations, les remises ou les frais de transport (vous pouvez
rendre les conditions dépendantes de la plupart des zones du document). Les exemples les
plus courants ont déjà été définis dans le système standard.

Figure 50: Données de base de condition
```

---

## PDF page 135

```text
Sujet: Gestion des données de base de condition pour la détermination du prix

Enregistrements de condition dans la détermination du prix

Si vous voulez créer un enregistrement de condition, vous devez d'abord choisir le type de
condition approprié. Le type de condition contrôle les propriétés suivantes de
l'enregistrement :

●  Classe de condition (par exemple, prix ou remise) ;

●  Barèmes (les barèmes sont-ils autorisés et une échelle de valeurs ou un barème en
quantité est-il possible ?) ;

●  Niveau (l'enregistrement de données s'applique-t-il au niveau de l'en-tête et/ou du poste
du document ?) ;

●  Période de validité (une valeur par défaut peut être proposée).

La figure « Enregistrements de condition dans la détermination du prix » représente un
exemple d'enregistrement de condition.

Figure 51: Enregistrements de condition dans la détermination du prix

Détermination du prix
La détermination des prix, taxes, remises, etc., est automatique dans la plupart des
documents de vente.

Un ensemble complexe de règles définies dans le Customizing (appelé technique des
conditions) contrôle le mode d'exécution de la détermination automatique du prix. Le
système vérifie entre autres s'il existe des enregistrements de condition pertinents et copie
les valeurs correspondantes dans le document de vente. Selon le type de condition, ces
valeurs sont copiées dans l'en-tête ou le poste respectif.

Remarque :
Si les options de détermination du prix définis dans le Customizing le permettent,
vous pouvez modifier ces valeurs manuellement dans le document de vente (pour
accorder, par exemple, une remise plus importante au client).
```

---

## PDF page 136

```text
Chapitre 4 : Données de base

La figure « Détermination du prix dans les commandes client » illustre les résultats de la
détermination automatique du prix.

Figure 52: Détermination du prix dans les commandes client
```

---

## PDF page 137

```text
Chapitre 4
Exercice 13

Création d'un enregistrement de condition
(prix de vente)

Vous devez définir des accords sur prix pour des clients importants. Ces clients passant
fréquemment des commandes, vous devez leur proposer des prix réduits pour certains
articles en fonction de la quantité commandée.

Comme vous ne voulez pas saisir ces accords chaque fois que vous créez une commande,
utilisez la fonction de détermination automatique du prix dans le système et créez les
données de base de condition appropriées.

1. Créez un enregistrement de condition à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de condition                     PR00

Organisation commerciale              1010

Canal distribution                     10

Client                              T-S50A##

Article                             T-MS1##

Le prix de l'article doit dépendre de la quantité commandée. Vous devez donc gérer le
barème de prix suivant :
Quantité échelonnée                    Montant

1 pièce                              53 EUR pièce

10 pièces                                51 EUR pièce

20 pièces                           49 EUR pièce

2. Après avoir saisi le prix client-article dans le système, vous recevez une autre commande
client. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-23##
```

---

## PDF page 138

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

DateLivrSouh.                         dans 10 jours

Article                             T-MS1##

Qté d'ordre                          10 pièces

3. Lors de la saisie de la commande client, assurez-vous que les prix définis par la fonction
de détermination automatique du prix sont corrects pour l'article T-MS1##.
Quel est le prix unitaire déterminé par le système ?

_______________________________________

4. Sauvegardez la commande client et notez son numéro.
______________________________________
```

---

## PDF page 139

```text
Chapitre 4
Solution 13

Création d'un enregistrement de condition
(prix de vente)

Vous devez définir des accords sur prix pour des clients importants. Ces clients passant
fréquemment des commandes, vous devez leur proposer des prix réduits pour certains
articles en fonction de la quantité commandée.

Comme vous ne voulez pas saisir ces accords chaque fois que vous créez une commande,
utilisez la fonction de détermination automatique du prix dans le système et créez les
données de base de condition appropriées.

1. Créez un enregistrement de condition à l'aide des informations suivantes :

Nom de zone                             Valeur

Type de condition                     PR00

Organisation commerciale              1010

Canal distribution                     10

Client                              T-S50A##

Article                             T-MS1##

Le prix de l'article doit dépendre de la quantité commandée. Vous devez donc gérer le
barème de prix suivant :
Quantité échelonnée                    Montant

1 pièce                              53 EUR pièce

10 pièces                                51 EUR pièce

20 pièces                           49 EUR pièce

a) Dans la barre de lancement SAP Fiori, lancez l'application Définir prix des articles.

b) Saisissez le type de condition PR00 et appuyez sur Entrée.

c) Dans la boîte de dialogue, sélectionnez la combinaison clé Client/Article avec statut de
validation.

d) Saisissez les entités organisationnelles et le numéro du client.

e) En bas à droite de l'écran, cliquez sur Exécuter pour confirmer vos saisies.

f) Saisissez le numéro d'article dans la première ligne vide de la table et sélectionnez
Entrée.
```

---

## PDF page 140

```text
Chapitre 4 : Données de base

g) Sélectionnez la ligne en cochant la case à côté du numéro d'article.

h) En haut de l’écran, cliquez sur Barèmes.

i) Gérez le barème de prix.

j) Cliquez sur Sauvegarder.

2. Après avoir saisi le prix client-article dans le système, vous recevez une autre commande
client. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-23##

DateLivrSouh.                         dans 10 jours

Article                             T-MS1##

Qté d'ordre                          10 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, saisissez les informations organisationnelles et le type de
commande.

c) Pour appeler les détails de la commande, sélectionnez Suite.

d) Gérez les informations appropriées dans la commande client.

3. Lors de la saisie de la commande client, assurez-vous que les prix définis par la fonction
de détermination automatique du prix sont corrects pour l'article T-MS1##.
Quel est le prix unitaire déterminé par le système ?

_______________________________________

a) Double-cliquez sur le poste 10 dans la commande client.

b) Sélectionnez la page à onglet Conditions.
Le système a déterminé le prix de 51 EUR pièce.

4. Sauvegardez la commande client et notez son numéro.
______________________________________

a) Dans la commande client, en bas de l'écran, cliquez sur Sauvegarder.
Le numéro de document s’affiche dans une boîte de dialogue.
```

---

## PDF page 141

```text
Chapitre 4
Exercice 14

Création d'un enregistrement de condition
(remise)

Vous devez gérer une remise spécifique pour un client. Le client doit bénéficier d'une remise
en pourcentage en fonction de la valeur d'un article commandé.

1. Créez un enregistrement de condition à l'aide des informations suivantes. Vous avez
conclu avec le client T-S50A## qu'il doit bénéficier d'une remise en pourcentage à partir
de maintenant pour tous les articles en fonction de la valeur du poste.

Nom de zone                             Valeur

Type de condition                     K007

Organisation commerciale              1010

Canal distribution                     10

Client                              T-S50A##

Gérez le barème de remises suivant :
Valeur barème                         Montant

100 EUR                                               - 1 %

500 EUR                                   -2 %

1 000 EUR                                 -3 %

2. Le client passe la commande suivante. Créez la commande client correspondante sur la
base des informations suivantes :

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-25##

DateLivrSouh.                         dans 10 jours

Article                             T-MS1##
```

---

## PDF page 142

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Qté d'ordre                          10 pièces

3. Lors de la saisie de la commande client, assurez-vous que la remise définie par la fonction
de détermination automatique du prix est correcte.
Quelle est la remise accordée au client déterminée par le système ?

_______________________________________

4. Sauvegardez la commande et notez son numéro.
______________________________________
```

---

## PDF page 143

```text
Chapitre 4
Solution 14

Création d'un enregistrement de condition
(remise)

Vous devez gérer une remise spécifique pour un client. Le client doit bénéficier d'une remise
en pourcentage en fonction de la valeur d'un article commandé.

1. Créez un enregistrement de condition à l'aide des informations suivantes. Vous avez
conclu avec le client T-S50A## qu'il doit bénéficier d'une remise en pourcentage à partir
de maintenant pour tous les articles en fonction de la valeur du poste.

Nom de zone                             Valeur

Type de condition                     K007

Organisation commerciale              1010

Canal distribution                     10

Client                              T-S50A##

Gérez le barème de remises suivant :
Valeur barème                         Montant

100 EUR                                               - 1 %

500 EUR                                   -2 %

1 000 EUR                                 -3 %

a) Dans la barre de lancement SAP Fiori, lancez l'application Définir prix des articles.

b) Saisissez le type de condition K007 et appuyez sur Entrée.

c) Saisissez les entités organisationnelles.

d) Pour confirmer vos données, cliquez sur Exécuter.

e) Saisissez le numéro de client dans la première ligne vide de la table, puis appuyez sur
Entrée.

f) Sélectionnez la ligne en cochant la case en regard du numéro de client.

g) Sélectionnez Barèmes.

h) Gérez le barème des remises et sélectionnez Entrée.

i) Cliquez sur Sauvegarder.

2. Le client passe la commande suivante. Créez la commande client correspondante sur la
base des informations suivantes :
```

---

## PDF page 144

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Type de commande                   CDCL

Org. commerciale                     1010

Canal de distribution                   10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           5-25##

DateLivrSouh.                         dans 10 jours

Article                             T-MS1##

Qté d'ordre                          10 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, saisissez les informations organisationnelles et le type de
commande.

c) Pour appeler les détails de la commande, sélectionnez Suite.

d) Gérez les informations appropriées dans la commande client.

3. Lors de la saisie de la commande client, assurez-vous que la remise définie par la fonction
de détermination automatique du prix est correcte.
Quelle est la remise accordée au client déterminée par le système ?

_______________________________________

a) Double-cliquez sur votre poste dans la commande client.

b) Sélectionnez la page à onglet Conditions.
Le système a déterminé une remise de - 2 % (K007) pour le client en fonction de la
fiche correspondante.

4. Sauvegardez la commande et notez son numéro.
______________________________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document est affecté en interne par le système.
```

---

## PDF page 145

```text
Chapitre 4
Exercice 15

Description du contexte des données de base
de condition

Répondez aux questions suivantes concernant les données de base de condition dans la
détermination du prix.

1. Quelles classes de données de base de condition (4) peuvent être utilisées pour la
détermination du prix ?

2. Vous souhaitez vendre des articles via divers canaux de distribution. Est-il possible de
gérer les prix dans les enregistrements de condition de différentes façons en fonction du
canal de distribution ?

3. Vous avez saisi une commande client. Les prix ont été définis par la fonction de
détermination automatique du prix. Pouvez-vous modifier les prix manuellement lors de la
saisie de la commande client ?
```

---

## PDF page 146

```text
Chapitre 4
Solution 15

Description du contexte des données de base
de condition

Répondez aux questions suivantes concernant les données de base de condition dans la
détermination du prix.

1. Quelles classes de données de base de condition (4) peuvent être utilisées pour la
détermination du prix ?

Prix, majorations/remises, fret, taxes.

2. Vous souhaitez vendre des articles via divers canaux de distribution. Est-il possible de
gérer les prix dans les enregistrements de condition de différentes façons en fonction du
canal de distribution ?

Oui. Le prix est généralement géré en fonction de l'organisation commerciale et du canal
de distribution.  Il peut également être géré en fonction d'autres critères (client, par
exemple).

3. Vous avez saisi une commande client. Les prix ont été définis par la fonction de
détermination automatique du prix. Pouvez-vous modifier les prix manuellement lors de la
saisie de la commande client ?

Oui. Lors de la saisie d'une commande client, vous pouvez généralement modifier le prix
manuellement. Cependant,  il est possible de limiter cette opération en définissant les
options appropriées dans le Customizing ou dans les enregistrements de condition.
```

---

## PDF page 147

```text
Sujet: Gestion des données de base de condition pour la détermination du prix

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Gérer les données de base de condition pour la détermination du prix
```

---

## PDF page 148

```text
Chapitre 4
Sujet 5

Explication des sujets complémentaires
touchant aux données de base

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Expliquer les sujets complémentaires touchant aux données de base

Données de base communes
Données de base communes - Canaux de distribution

Si vous n'avez pas besoin de distinguer les données de base (données de base client, données
de base article et données de base de condition) en fonction des canaux de distribution, vous
pouvez configurer un canal de distribution représentatif. Les données de base du canal de
distribution représentatif s'appliquent à tous les canaux de distribution pour lesquels vous
avez défini cette référence dans le Customizing.

Vous réduisez ainsi l'effort de saisie et de gestion des données de base. En outre, vous pouvez
mettre à jour les statistiques pour les canaux de distribution sans avoir à créer des données
de base pour les différents canaux de distribution.

La figure « Données de base communes - Canaux de distribution » illustre le concept
d'utilisation de canaux de distribution représentatifs.
```

---

## PDF page 149

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

Figure 53: Données de base communes - Canaux de distribution

Données de base communes - Secteurs d'activité

Si vous n'avez pas besoin de distinguer les données de base (données de base client ou
données de base de condition) en fonction des secteurs d'activité, vous devez définir un
secteur d'activité représentatif. Les données de base définies dans le secteur d'activité
représentatif s'appliquent à tous les secteurs d'activité pour lesquels vous avez défini cette
référence.

Vous réduisez ainsi l'effort de saisie et de gestion des données de base. En outre, vous pouvez
mettre à jour les statistiques pour les secteurs d'activité sans avoir à créer des données de
base pour les différents secteurs d'activité.

La figure « Données de base communes - Secteurs d'activité » illustre le concept d'utilisation
de secteurs d'activité représentatifs.
```

---

## PDF page 150

```text
Chapitre 4 : Données de base

Figure 54: Données de base communes - Secteurs d'activité

Données de base des messages
Un message comprend des informations envoyées à un client via divers supports tels que l'e-
mail ou l'échange de données informatisé (EDI). Il peut s'agir d'une offre client ou d'un accusé
de réception imprimé, d'accusés de réception EDI ou de factures télécopiées. Vous pouvez
envoyer des messages pour divers documents commerciaux (commande, livraison sortante,
document de facturation, etc.).

À l'instar de la détermination du prix, la détermination des messages s'appuie sur la technique
de condition. Dans les données de base des messages, vous définissez le support
(imprimante ou télécopie, par exemple), la date et l'heure de création du message ainsi que le
rôle partenaire (qui recevra le message) pour une catégorie de message.

Un message peut être envoyé immédiatement dès sa sauvegarde ou par le biais d'un
programme standard (RSNAST00) exécuté régulièrement. Le format (mise en forme) d'un
message peut être défini à l’aide de différents outils. Le formulaire est ensuite affecté à une
catégorie de message.

Pertinence des données de base des messages
```

---

## PDF page 151

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

Figure 55: Pertinence des données de base des messages

Dans SAP S/4HANA, une deuxième approche de traitement des messages est disponible : la
gestion des sorties SAP S/4HANA. Il s'agit d'une technique complètement différente, basée
sur Business Rule Framework Plus (BRFplus), un ensemble de tables de décisions utilisées
par le système pour identifier le type d'édition, le support d'édition, les options d'impression
appropriés, etc.

La gestion des sorties SAP S/4HANA, constitue l'infrastructure stratégique de gestion des
sorties dans SAP S/4HANA, à laquelle seront ajoutés de prochains développements. Adobe
XFA est la technologie par défaut pour les modèles de formulaires, mais les formulaires
hérités, tels que SAPscript, SmartForms et Adobe Forms, sont toujours pris en charge. Les
principaux avantages de la nouvelle approche sont les suivants :

●   flexibilité et puissance de la détermination des paramètres de sortie

●  Solution unifiée dans toutes les applications : SD, MM, FI, etc.

●  intégration complète aux applications SAP Fiori

●  Support par e-mail : configuration flexible, destinataires multiples et modèles d'e-mails

À la différence de la gestion classique des sorties basée sur les données de base, la nouvelle
gestion des sorties SAP S/4HANA prend en charge uniquement les canaux PRINT, EMAIL,
XML et IDOC (sur site). Les autres canaux ne sont pas disponibles par défaut.

La figure « Table de décisions BRFplus » illustre le concept et l'utilisation des tables de
décisions BRFplus typiques.
```

---

## PDF page 152

```text
Chapitre 4 : Données de base

Figure 56: Table de décisions BRFplus

Postes par défaut
Si un client commande souvent la même combinaison d'articles, ou si vous recommandez
une sélection particulière de produits pour une nouvelle commande, vous pouvez enregistrer
les données fréquemment utilisées en tant que poste par défaut afin de réduire le temps de
traitement des commandes clients.

Si vous le souhaitez, le poste par défaut peut également inclure les quantités commandées
proposées. De plus, vous pouvez afficher une liste des clients affectés à chaque proposition
de postes de vente.

Pendant le traitement des commandes client, vous pouvez récupérer l'ensemble ou une
partie des articles et la quantité de données à partir du poste par défaut, directement dans
votre document de vente. Les postes proposés à partir d’un poste par défaut peuvent
toujours être modifiés dans la commande client.

Avec l'application correspondante, vous pouvez rapidement obtenir une synthèse de tous les
postes de vente par défaut existants. En sélectionnant un poste de la liste, vous pouvez
afficher et traiter les articles et les quantités définies et afficher d'autres informations
pertinentes pour le poste de vente par défaut en cours.

En outre, vous pouvez créer des postes de vente par défaut et définir un critère de recherche
que vous pouvez ensuite utiliser pour extraire plus facilement le poste par défaut lors de la
gestion des commandes client.

La figure « Poste par défaut » illustre l'utilisation des propositions de postes.
```

---

## PDF page 153

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

Figure 57: Poste par défaut
```

---

## PDF page 154

```text
Chapitre 4 : Données de base
```

---

## PDF page 155

```text
Chapitre 4
Exercice 16

Création de postes par défaut

Votre client commande souvent la même combinaison d'articles. Par conséquent, vous
souhaitez enregistrer les données fréquemment utilisées en tant que postes par défaut afin
de réduire le temps de traitement des commandes client.

1. Lancez l'application Gestion des propositions de postes de vente à partir de la barre de
lancement SAP Fiori et créez une proposition de poste de vente à l'aide des données d'en-
tête suivantes :

Nom de zone                             Valeur

Type de document de vente              PV

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Désignation                         Proposition poste Groupe ##

Date de début de validité                 Date du jour

Date de fin de validité                        Fin de l'année

2. Saisissez les articles et les quantités suivantes et sauvegardez la fiche. Notez le numéro
de la fiche.

Numéro d’article                          Quantité

T-MS1##                           5 pces

T-MS2##                           5 pces

Proposition de poste de vente :
______________________________________________________

3. Affectez le nouveau poste par défaut à votre partenaire T-S50A##.

4. Créez une commande client à l'aide des informations suivantes et copiez les articles de la
fiche de la proposition de poste :

Nom de zone                             Valeur

Type de commande                   CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00
```

---

## PDF page 156

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Donneur d'ordre                      T-S50A##

Réf. client                           ##-Proposition

5. Sauvegardez la commande client et notez son numéro.
______________________________________________________
```

---

## PDF page 157

```text
Chapitre 4
Solution 16

Création de postes par défaut

Votre client commande souvent la même combinaison d'articles. Par conséquent, vous
souhaitez enregistrer les données fréquemment utilisées en tant que postes par défaut afin
de réduire le temps de traitement des commandes client.

1. Lancez l'application Gestion des propositions de postes de vente à partir de la barre de
lancement SAP Fiori et créez une proposition de poste de vente à l'aide des données d'en-
tête suivantes :

Nom de zone                             Valeur

Type de document de vente              PV

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Désignation                         Proposition poste Groupe ##

Date de début de validité                 Date du jour

Date de fin de validité                        Fin de l'année

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des propositions des
postes de vente.

b) Sélectionnez Créer pour créer une fiche.

c) Saisissez les valeurs de zone pertinentes répertoriées dans le tableau.

2. Saisissez les articles et les quantités suivantes et sauvegardez la fiche. Notez le numéro
de la fiche.

Numéro d’article                          Quantité

T-MS1##                           5 pces

T-MS2##                           5 pces

Proposition de poste de vente :
______________________________________________________
a) Dans la section Produits, sélectionnez Créer.

b) Saisissez les données du premier article.

c) Répétez ces deux étapes pour le deuxième article.
```

---

## PDF page 158

```text
Chapitre 4 : Données de base

d) Cliquez sur Créer pour sauvegarder la proposition. Le numéro correspondant est
affiché en haut de l’écran.

3. Affectez le nouveau poste par défaut à votre partenaire T-S50A##.
a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion du partenaire.

b) Dans la partie gauche de l'écran, saisissez le numéro de votre partenaire et
sélectionnez Lancer pour lancer la recherche.

c) Dans la partie gauche, double-cliquez sur la ligne qui contient le numéro de votre
partenaire pour accéder aux détails.

d) En haut de l'écran, sélectionnez Passage Affichage -> Modification.

e) Sélectionnez le rôle FLCU01 Client SD (géré) dans la zone Modifier ds rôle par..

f) Choisissez Administration des ventes (ADV) en haut de l'écran.

g) Dans la vue Ordre, saisissez le numéro dans la zone Proposition poste.

h) Cliquez sur Sauvegarder.

4. Créez une commande client à l'aide des informations suivantes et copiez les articles de la
fiche de la proposition de poste :

Nom de zone                             Valeur

Type de commande                   CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           ##-Proposition

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de la transaction, saisissez le type de commande et les entités
organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Dans l'écran de synthèse, saisissez les valeurs des zones.

e) En haut à gauche de l'écran, sélectionnez Proposer des postes.

f) Dans la fenêtre pop-up Proposer des postes, le numéro de la proposition de poste par
défaut doit être affiché. Si ce n'est pas le cas, saisissez le numéro manuellement.
Sélectionnez Proposition avec qté.

5. Sauvegardez la commande client et notez son numéro.
______________________________________________________
a) Dans la commande client, sélectionnez Sauvegarder.
```

---

## PDF page 159

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

Contrôle des données manquantes
Lorsque vous créez des documents dans le processus d'administration des ventes, certaines
données peuvent manquer dans les données de base associées (poids de l'article, par
exemple) et ne peuvent donc pas être copiées dans les documents. Si vous ne pouvez pas
gérer les zones respectives manuellement parce que vous ne connaissez pas les valeurs
correctes, le document reste incomplet. Cependant, la sauvegarde de documents incomplets
est possible si le système est paramétré en conséquence. Selon les zones incomplètes,
l'exécution de certaines fonctions liées (par exemple, la création de livraisons sortantes avec
référence à une commande client) peut ne pas être autorisée tant que le document n'est pas
complété.

L'utilisateur peut obtenir la synthèse des zones incomplètes dans un document à l'aide du
protocole des données manquantes. Les zones respectives sont accessibles directement à
partir de ce protocole si l'utilisateur souhaite les compléter.

Remarque :
Dans le Customizing, vous pouvez déterminer les zones à compléter lors de la
création de documents.

Vous pouvez utiliser plusieurs applications et transactions de type liste pour identifier les
documents incomplets.

La figure « Protocole de document incomplet » illustre le concept de contrôle des données
manquantes.

Figure 58: Protocole des données manquantes
```

---

## PDF page 160

```text
Chapitre 4 : Données de base
```

---

## PDF page 161

```text
Chapitre 4
Exercice 17

Gestion des documents de vente incomplets

Les documents de vente sont parfois incomplets après leur création (en raison de données de
base incomplètes, par exemple). Par conséquent, vous devez savoir identifier et compléter les
documents de vente incomplets. Vous allez maintenant créer une commande client
incomplète, puis exécuter les étapes nécessaires pour la compléter.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Article                             T-MS2##

Qté d'ordre                          10

Assurez-vous que la zone de référence client reste vide et supprimez le poids net au
niveau du poste.

2. Sauvegardez la commande client incomplète et notez son numéro.
______________________________________________________

3. Essayez de créer une livraison sortante avec référence à la commande client incomplète
en utilisant le point d'expédition Z0##. Pouvez-vous la créer ?
_____________________

4. Utilisez l'application appropriée pour identifier et compléter la commande client
incomplète.

5. Complétez la commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Réf. client                           3-9##

Poids net                           20 KG

6. Essayez de créer une deuxième fois la livraison sortante. Pouvez-vous à présent la créer ?
______________________
```

---

## PDF page 162

```text
Chapitre 4
Solution 17

Gestion des documents de vente incomplets

Les documents de vente sont parfois incomplets après leur création (en raison de données de
base incomplètes, par exemple). Par conséquent, vous devez savoir identifier et compléter les
documents de vente incomplets. Vous allez maintenant créer une commande client
incomplète, puis exécuter les étapes nécessaires pour la compléter.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Article                             T-MS2##

Qté d'ordre                          10

Assurez-vous que la zone de référence client reste vide et supprimez le poids net au
niveau du poste.
a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de la transaction, saisissez le type de commande et les entités
organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Dans l'écran de synthèse, saisissez les valeurs des zones.

Astuce :
Lorsque le message d'avertissement concernant la référence client
manquante s'affiche, sélectionnez Entrée pour continuer.

e) Double-cliquez sur le poste.

f) Sélectionnez la page à onglet Expédition.

g) Supprimez le poids net.

2. Sauvegardez la commande client incomplète et notez son numéro.
______________________________________________________
```

---

## PDF page 163

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

a) Dans la commande client, sélectionnez Sauvegarder.
Une boîte de dialogue s'affiche pour vous demander si vous voulez sauvegarder la
commande incomplète.

b) Cliquez sur Sauvegarder.

3. Essayez de créer une livraison sortante avec référence à la commande client incomplète
en utilisant le point d'expédition Z0##. Pouvez-vous la créer ?
_____________________
a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes (à partir des commandes client).

b) Si les filtres de l'application ne sont pas visibles dans l'écran initial, cliquez sur
Développer l’en-tête.

c) Saisissez le point d'expédition Z0## et sélectionnez Échue la semaine prochaine
comme date de création planifiée. Cliquez sur Lancer.

d) Sélectionnez votre commande dans la liste et cliquez sur Créer livraisons.

e) Pour accéder au journal, sélectionnez Afficher journal.
Le système indique que la commande ne peut pas être livrée car elle est incomplète.

4. Utilisez l'application appropriée pour identifier et compléter la commande client
incomplète.
a) Dans la barre de lancement SAP Fiori (groupe de vignettes Analytics and Monitoring),
lancez l'application Liste des documents de vente incomplets.

b) Cliquez sur Lancer.

c) Votre commande client s’affiche dans la liste parmi d’autres documents.

5. Complétez la commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Réf. client                           3-9##

Poids net                           20 KG

a) Dans la liste des commandes incomplètes, sélectionnez la ligne qui contient votre
document incomplet.

b) En haut de l'écran, cliquez sur Compléter données.

c) Saisissez la référence client manquante.

d) Sélectionnez Traiter données suivantes.

e) Sélectionnez la ligne des données manquantes : Net Weight.

f) En haut de l'écran, cliquez sur Compléter données.

g) Saisissez le poids net du poste.

h) Cliquez une deuxième fois sur Traiter données suivantes.
Un message système vous indique que le document est désormais complet.

i) Pour sauvegarder votre commande complète, cliquez sur Sauvegarder.
```

---

## PDF page 164

```text
Chapitre 4 : Données de base

6. Essayez de créer une deuxième fois la livraison sortante. Pouvez-vous à présent la créer ?
______________________
a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Si les filtres de l'application ne sont pas visibles dans l'écran initial, cliquez sur
Développer l’en-tête.

c) Saisissez le point d'expédition Z0## et sélectionnez Échue la semaine prochaine
comme date de création planifiée. Cliquez sur Lancer.

d) Sélectionnez votre commande dans la liste puis, en bas à droite de l'écran, cliquez sur
Créer livraisons.

e) Pour accéder au journal, sélectionnez Afficher journal.
Le système a désormais été en mesure de créer la livraison sortante.
```

---

## PDF page 165

```text
Sujet: Explication des sujets complémentaires touchant aux données de base

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Expliquer les sujets complémentaires touchant aux données de base
```

---

## PDF page 166

```text
Chapitre 4 : Données de base
```

---

## PDF page 167

```text
Chapitre 4

Évaluation des connaissances

1.  Les données de base des clients et fournisseurs sont gérées dans SAP S/4HANA à l'aide
de données de base du partenaire.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Parmi les rôles partenaires suivants, lequel s’applique à un client qui reçoit la facture ?

Sélectionnez la réponse correcte.

X  A Donneur d'ordre

X  B Réceptionnaire

X  C Destinataire de la facture

X  D Payeur

3. Le Customizing des types de document de vente inclut certains paramètres qui
permettent de choisir entre la gestion des ventes propres à un secteur d'activité ou
valables pour tous les secteurs.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

4.  Si une fiche infos client-article a été définie pour un client et un article, les valeurs par
défaut correspondantes sont utilisées prioritairement aux valeurs correspondantes
définies dans la fiche client ou article lors de la création d'un document.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 168

```text
Chapitre 4 : Évaluation des connaissances

5. Parmi les options suivantes, lesquelles sont incluses dans les données de base de
condition ?

Sélectionnez les réponses correctes.

X  A Prix

X  B majorations

X  C Canal de distribution

X  D Frais de transport

X  E Taxes

X  F Remises

6.  Si vous n'avez pas besoin de différencier les données de base en fonction des secteurs
d'activité, vous devez créer des données de base pour les différents secteurs d'activité.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 169

```text
Chapitre 4

Évaluation des connaissances - Réponses

1.  Les données de base des clients et fournisseurs sont gérées dans SAP S/4HANA à l'aide
de données de base du partenaire.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Les données de base des clients et fournisseurs sont gérées dans SAP S/4HANA
à l'aide de données de base du partenaire.

2. Parmi les rôles partenaires suivants, lequel s’applique à un client qui reçoit la facture ?

Sélectionnez la réponse correcte.

X  A Donneur d'ordre

X  B Réceptionnaire

X  C Destinataire de la facture

X  D Payeur

Correct. Le destinataire de la facture est le rôle partenaire applicable à un client qui reçoit
la facture.

3. Le Customizing des types de document de vente inclut certains paramètres qui
permettent de choisir entre la gestion des ventes propres à un secteur d'activité ou
valables pour tous les secteurs.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Le Customizing des types de document de vente inclut certains paramètres qui
permettent de choisir entre la gestion des ventes propres à un secteur d'activité ou
valables pour tous les secteurs.
```

---

## PDF page 170

```text
Chapitre 4 : Évaluation des connaissances - Réponses

4.  Si une fiche infos client-article a été définie pour un client et un article, les valeurs par
défaut correspondantes sont utilisées prioritairement aux valeurs correspondantes
définies dans la fiche client ou article lors de la création d'un document.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Si une fiche infos client-article a été définie pour un client et un article, les valeurs
par défaut correspondantes (division chargée de la livraison, par exemple) sont utilisées
prioritairement aux valeurs correspondantes définies dans la fiche client ou article lors de
la création d'un document tel qu'une commande client.

5. Parmi les options suivantes, lesquelles sont incluses dans les données de base de
condition ?

Sélectionnez les réponses correctes.

X  A Prix

X  B majorations

X  C Canal de distribution

X  D Frais de transport

X  E Taxes

X  F Remises

Correct. Les données de base de condition incluent les données de base des prix, de
majorations, de remises, de fret et de taxes.

6.  Si vous n'avez pas besoin de différencier les données de base en fonction des secteurs
d'activité, vous devez créer des données de base pour les différents secteurs d'activité.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Si vous n'avez pas besoin de distinguer les données de base (données de base
client ou données de base de condition) en fonction des secteurs d'activité, vous devez
définir un secteur d'activité de référence. Les données de base définies dans le secteur
d'activité de référence s'appliquent à tous les secteurs d'activité pour lesquels vous avez
défini cette référence.
```

---

## PDF page 171

```text
CHAPITRE 5  Détermination automatique des
données et ordonnancement

Sujet 1

Analyse des résultats de la détermination automatique des données                           162
Exercice 18 : Vérification des résultats de la détermination automatique des données  169

Sujet 2

Analyse des résultats de l'ordonnancement de l'expédition et du transport                      175
Exercice 19 : Vérification des résultats de l'ordonnancement de l'expédition et du      179
transport

OBJECTIFS DU CHAPITRE

●  Analyser les résultats de la détermination automatique des données

●  Analyser les résultats de l'ordonnancement de l'expédition et du transport
```

---

## PDF page 172

```text
Chapitre 5
Sujet 1

Analyse des résultats de la détermination
automatique des données

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Analyser les résultats de la détermination automatique des données

Détermination de la division
La division jouant un rôle essentiel dans les processus d'administration des ventes, elle est
d'emblée prise en compte lors de la création des commandes clients. Elle s'applique
notamment aux fonctions suivantes :

●  Détermination de la taxe

●  Contrôle de disponibilité

●  Détermination du point d'expédition

Astuce :
Les divisions utilisées dans les processus d'administration des ventes sont
souvent appelées divisions chargées de la livraison car elles représentent le
centre de distribution à partir duquel l'article est livré au client.

Comme la division chargée de la livraison est obligatoire pour l'ensemble du processus, le
système tente automatiquement de déterminer la division adéquate (au niveau du poste) à
partir des données de base lors de la création des commandes clients.

Détermination automatique de la division chargée de la livraison

La figure « Détermination automatique de la division chargée de la livraison » représente les
sources possibles permettant de déterminer automatiquement la division à partir des
données de base ainsi que l'ordre de la recherche de ces données.
```

---

## PDF page 173

```text
Sujet: Analyse des résultats de la détermination automatique des données

Figure 59: Détermination automatique de la division chargée de la livraison

Remarque :
Il est possible de modifier manuellement la valeur de la division déterminée
automatiquement.

S'il n'existe aucune division valide dans les données de base (parce que, par exemple, la zone
correspondante n'est gérée dans aucune base de données), aucune division chargée de la
livraison n'est définie dans le poste du document de vente. Dans ce cas, il n'est pas possible
d'exécuter les fonctions spécifiques mentionnées ci-dessus (détermination des taxes, par
exemple), et le document est incomplet.

Détermination du point d'expédition

Points d'expédition par division chargée de la livraison

Le point d'expédition est l'entité organisationnelle responsable du traitement de l'expédition.
Si vous vendez des produits physiques à livrer au client, le point d'expédition approprié est
d'emblée pris en compte pour les postes correspondants lors de la création des commandes
client, à l'instar de la division chargée de la livraison. Le point d'expédition est notamment
important pour les fonctions suivantes qui en dépendent :

●  Ordonnancement des expéditions

●  Détermination de l'itinéraire

●  Création de la livraison

D'un point de vue organisationnel, les points d'expédition sont affectés aux divisions chargées
de la livraison, comme l’illustre la figure « Points d'expédition par division chargée de la
livraison ».
```

---

## PDF page 174

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

Figure 60: Points d'expédition par division chargée de la livraison

Détermination automatique du point d'expédition

Les points d'expédition étant obligatoires pour le processus, le système tente de déterminer
automatiquement le point d'expédition approprié à chaque poste lié à la livraison d'une
commande client.

La figure « Détermination automatique du point d'expédition » représente les critères
permettant de déterminer le point d'expédition approprié à chaque poste de document de
vente.
```

---

## PDF page 175

```text
Sujet: Analyse des résultats de la détermination automatique des données

Figure 61: Détermination automatique du point d'expédition

Le groupe de chargement se trouve dans la page à onglet ADV : données générales/division
de la fiche article. La condition d'expédition est normalement copiée depuis la fiche partenaire
du donneur d'ordre (page à onglet Expédition) dans l'en-tête du document de vente.
Cependant, le Customizing des types de documents de vente contient un paramètre qui
permet de copier la condition d'expédition depuis le réceptionnaire des marchandises.

Remarque :
Vous pouvez modifier manuellement la valeur du point d'expédition déterminé
automatiquement dans une commande, tant qu'’aucun document de livraison
correspondant n’a été créé.

Détermination de l'itinéraire
L'itinéraire décrit le parcours d'une livraison depuis un point d'expédition jusqu'à la région
dans laquelle se trouve le client. Un itinéraire peut comprendre une ou plusieurs étapes (des
tronçons par exemple), comme l’illustre la figure « Structure d’un itinéraire ».
```

---

## PDF page 176

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

Figure 62: Structure d'un itinéraire

Détermination automatique de l'itinéraire

SAP S/4HANA utilise l'itinéraire pour diverses fonctions de planification du transport, y
compris l'ordonnancement du transport. Pour influencer l'ordonnancement du transport,
l'itinéraire constitue la source des valeurs suivantes :

●  Temps de transit : durée pendant laquelle les marchandises sont en transit

●  Délai de transport : durée nécessaire à l'organisation du moyen de transport

L'itinéraire peut être déterminé automatiquement pour chaque poste lié à la livraison dans le
document de vente.

La figure « Détermination automatique de l’itinéraire » représente les différents critères
utilisés par SAP ERP pour déterminer un itinéraire d'expédition dans des documents de vente.

Figure 63: Détermination automatique de l'itinéraire
```

---

## PDF page 177

```text
Sujet: Analyse des résultats de la détermination automatique des données

La zone de départ est reprise de la table de Customizing concernant le point d'expédition. La
condition d'expédition est copiée à partir de la fiche partenaire (page à ongletExpédition) du
donneur d'ordre ou du réceptionnaire des marchandises (selon les options du Customizing
pour le type de commande client). Le groupe de transports est copié à partir des données de
base article (page à onglet ADV : données générales/division). La zone de transport (ou zone
de réception) est extraite de la fiche partenaire du réceptionnaire (données générales).

Remarque :
SAP S/4HANA peut redéterminer l'itinéraire correspondant dans le document de
livraison.
```

---

## PDF page 178

```text
Chapitre 5 : Détermination automatique des données et ordonnancement
```

---

## PDF page 179

```text
Chapitre 5
Exercice 18

Vérification des résultats de la détermination
automatique des données

Lorsque vous créez des commandes clients, certaines valeurs de zone importantes peuvent
être déterminées automatiquement par le système. Vous allez créer une commande client et
vérifier la détermination automatique de la division, des points d'expédition et des itinéraires
appropriés.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50B##

Réf. client                           6-1##

DateLivrSouh.                         dans 10 jours

Conditions de paiement                ZB00

Article                                   Quantité commandée

T-MS1##                           7

T-MS2##                           8

2. Quelles sont les divisions chargées de la livraison qui ont été déterminées
automatiquement pour ces deux postes ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________

3. Lors de la détermination de la valeur correcte pour la division chargée de la livraison, le
système vérifie trois sources de données de base dans lesquelles la division a pu être
spécifiée. Quelles sont ces sources ?
```

---

## PDF page 180

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

4. De quelle source de données de base provient la valeur de la division chargée de la
livraison du poste 10 ?
___________________________________________

5. Quels points d'expédition ont été déterminés automatiquement pour ces deux postes de
la commande client ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________

6. Le système utilise trois critères pour déterminer le point d'expédition. Quels sont-ils ?

7. Quelles valeurs ont été attribuées aux trois critères pour déterminer automatiquement le
point d'expédition du poste 10 ?
________________________________________________

________________________________________________

________________________________________________

8. Quels itinéraires ont été déterminés pour ces deux postes ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________

9. Le système utilise quatre critères pour déterminer l’itinéraire. Quels sont-ils ?

10. Sauvegardez la commande client et notez le numéro du document.
_______________________________________________
```

---

## PDF page 181

```text
Chapitre 5
Solution 18

Vérification des résultats de la détermination
automatique des données

Lorsque vous créez des commandes clients, certaines valeurs de zone importantes peuvent
être déterminées automatiquement par le système. Vous allez créer une commande client et
vérifier la détermination automatique de la division, des points d'expédition et des itinéraires
appropriés.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50B##

Réf. client                           6-1##

DateLivrSouh.                         dans 10 jours

Conditions de paiement                ZB00

Article                                   Quantité commandée

T-MS1##                           7

T-MS2##                           8

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, saisissez le type de commande et les entités organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Saisissez les zones pertinentes.

2. Quelles sont les divisions chargées de la livraison qui ont été déterminées
automatiquement pour ces deux postes ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________
```

---

## PDF page 182

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

a) La commande client contient les valeurs de zone qui ont été déterminées pour les
divisions chargées de la livraison dans la page à onglet Expédition. La division 1010 a
été déterminée pour les deux postes.

3. Lors de la détermination de la valeur correcte pour la division chargée de la livraison, le
système vérifie trois sources de données de base dans lesquelles la division a pu être
spécifiée. Quelles sont ces sources ?

La fiche info client-article, la fiche partenaire du réceptionnaire des marchandises et la
fiche article.

4. De quelle source de données de base provient la valeur de la division chargée de la
livraison du poste 10 ?
___________________________________________
a) Vous ne souhaitez pas quitter la commande maintenant, ouvrez une page à onglet du
navigateur de la barre de lancement SAP Fiori. Si la page d'accueil de la barre de
lancement SAP Fiori ne s'affiche pas, copiez et collez l'URL (jusqu'à « /flp ») de l'onglet
exécutant l'application Création de commandes clients VA01.

b) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des articles clients.

c) En haut de l'écran, sélectionnez la ligne contenant le texte Filtré par ... pour accéder
aux critères de filtre.

d) Saisissez le client T-S50B##, l'organisation commerciale 1010, le canal de distribution
10 et le produit T-MS1##.

e) Pour lancer la sélection, cliquez sur Lancer.
Comme le système ne trouve pas de fiche correspondante, la valeur de la division
chargée de la livraison n'est clairement pas extraite d'une fiche infos client-article.

f) Pour vérifier l'option suivante, revenez à la page à onglet du navigateur dans laquelle la
commande client est toujours affichée.

g) Sélectionnez Menu → Environnement → Partenaire → Afficher réceptionnaire.

h) Assurez-vous que les données sont affichées pour le rôle partenaire Client.

i) Choisissez Administration des ventes (ADV) en haut de l'écran.
Dans la page à onglet Expédition, la valeur 1010 est gérée en tant que division
appropriée chargée de la livraison.

5. Quels points d'expédition ont été déterminés automatiquement pour ces deux postes de
la commande client ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________

a) Dans la commande client, vous pouvez trouver les points d'expédition déterminés
dans la page à onglet Expédition.
Le point d'expédition Z0## a été déterminé pour les deux postes.
```

---

## PDF page 183

```text
Sujet: Analyse des résultats de la détermination automatique des données

6. Le système utilise trois critères pour déterminer le point d'expédition. Quels sont-ils ?

Le système détermine le point d'expédition d'un poste de commande client en utilisant
comme critères la division chargée de la livraison, les conditions d'expédition et le groupe
de chargement.

7. Quelles valeurs ont été attribuées aux trois critères pour déterminer automatiquement le
point d'expédition du poste 10 ?
________________________________________________

________________________________________________

________________________________________________

a) La division chargée de la livraison 1010 a été utilisée comme premier critère.

b) Pour vérifier les conditions d'expédition dans la commande client, sélectionnez
Menu → Saut → En-tête → Expédition.
La condition d'expédition est Standard ##.

c) Accédez à l'écran de synthèse de la commande client.

d) Sélectionnez le poste 10.

e) Pour accéder à la fiche article, sélectionnez Menu → Environnement → Afficher article.

f) Sélectionnez la page à onglet ADV : Données générales/division.
La valeur pertinente pour le groupe de chargement est Manuel 0003.

8. Quels itinéraires ont été déterminés pour ces deux postes ?
Poste 10 : ___________________________________________

Poste 20 : ___________________________________________

a) Les itinéraires déterminés automatiquement se trouvent dans la page à onglet
Expédition de votre commande client.
L'itinéraire R00030 s'applique aux deux postes.

9. Le système utilise quatre critères pour déterminer l’itinéraire. Quels sont-ils ?

Le système détermine l'itinéraire d'un poste de commande client en utilisant la zone de
départ du point d'expédition, les conditions d'expédition, le groupe de transport et la zone
de transport du réceptionnaire comme critères.

10. Sauvegardez la commande client et notez le numéro du document.
_______________________________________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document s'affiche.
```

---

## PDF page 184

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Analyser les résultats de la détermination automatique des données
```

---

## PDF page 185

```text
Chapitre 5
Sujet 2

Analyse des résultats de l'ordonnancement de
l'expédition et du transport

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Analyser les résultats de l'ordonnancement de l'expédition et du transport

Ordonnancement de l'expédition et du transport
L'ordonnancement de l'expédition et du transport permet au système de vérifier, dans un
document de vente, si une date de livraison souhaitée peut être respectée. Plusieurs
éléments de durée sont pris en compte pour vérifier les dates de livraison. Le tableau suivant
répertorie ces composants ainsi que leur source.

Tableau 1: Éléments de durée pour l’ordonnancement de l'expédition et du transport

Élément de durée               Signific.                     départ

Durée de prélèvement/d'em-  Durée de prélèvement et      Point d'expédition
ballage                      d'emballage de l'article

Temps de chargt          Temps de chargement (sur le  Point d'expédition
camion, par exemple)

Durée de planif du transport  Temps de préparation du       Itinéraire
transport (détermination du
transporteur, par exemple)

Temps de transit          Temps d'acheminement des   Itinéraire
marchandises jusqu'au client

Remarque :
Le système doit déterminer le point d'expédition et l'itinéraire pour chaque poste
du document de vente avant d'utiliser les éléments de durée correspondants pour
l'ordonnancement.

Si les éléments de durée nécessaires sont disponibles, le système peut utiliser deux types
d'ordonnancement (amont et aval) pour calculer les dates suivantes :

●  Date de mise à disposition de l'article :

Date à laquelle une quantité suffisante de marchandises doit être disponible pour le
prélèvement et l'emballage

●  Date de planification du transport :
```

---

## PDF page 186

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

Date à laquelle doit commencer la planification du transport

●  Date de chargement :

Date à laquelle le chargement doit commencer

●  Date de sortie de marchandises :

Date à laquelle les marchandises doivent quitter la division chargée de la livraison afin de
parvenir à temps au client

●  Date de livraison :

Date à laquelle les marchandises parviennent au client

Astuce :
Dans un ordonnancement amont, la date de livraison souhaitée du client est
supposée être la date de livraison à prendre en compte. Dans un
ordonnancement aval, la date de livraison est calculée.

Ordonnancement amont
L'ordonnancement amont est le premier type d'ordonnancement effectué pour un poste de
commande client. Le système vérifie d'abord si la date de livraison souhaitée par le client peut
être respectée. La date de livraison souhaitée constitue donc le point de départ de
l'ordonnancement amont.

À partir de la date de livraison, le système calcule les autres dates pertinentes (telles que la
date de mise à disposition de l'article) en amont à l'aide des éléments de durée disponibles. La
figure « Ordonnancement amont » illustre le concept de l'ordonnancement amont.

Figure 64: Ordonnancement amont

La date calculée de mise à disposition de l'article et la date de planification du transport sont
particulièrement importantes. Les possibilités sont les suivantes selon la position des dates
calculées par rapport à la date de la commande :
```

---

## PDF page 187

```text
Sujet: Analyse des résultats de l'ordonnancement de l'expédition et du transport

●  Après la date de la commande :

Si ces deux dates sont postérieures (dans le futur) à la date de la commande et si l'article
est disponible à la date de sa mise à disposition, la date de livraison souhaitée par le client
peut être confirmée. Une échéance correspondante est créée pour le poste du document
de vente. La date de l'échéance indique que la date de livraison confirmée est identique à la
date de livraison souhaitée par le client.

Astuce :
La livraison sortante correspondante doit être créée à la date la plus proche
des deux dates (mise à disposition de l'article et planification du transport).

●  Avant la date de la commande :

Si l'une des dates ou les deux sont antérieures à la date de la commande (c’est-à-dire dans
le passé), la date de livraison souhaitée ne peut pas être confirmée. Dans ce cas, la
première échéance du poste correspondant ne sera pas confirmée. Le système peut alors
tenter de déterminer une date de livraison confirmable à l'aide de l'ordonnancement aval.

Ordonnancement aval
L'ordonnancement aval prend en compte le même ensemble de délais nécessaires pour le
prélèvement et l'emballage, le chargement, la planification du transport et le transit.
Initialement, il détermine la date au plus tôt à laquelle l'article est disponible en magasin, qui
devient la nouvelle date de mise à disposition de l'article. Le temps de prélèvement et
d'emballage est ajouté à cette date. Le système ajoute ensuite la durée de planification du
transport à la date de la commande. La dernière de ces dates calculées est alors la nouvelle
date de chargement à laquelle le temps de chargement peut être ajouté pour déterminer la
date de sortie des marchandises. Le temps de transit est ensuite ajouté pour établir une date
de livraison confirmable. La figure « Ordonnancement aval » illustre le concept de
l'ordonnancement aval.
```

---

## PDF page 188

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

Figure 65: Ordonnancement aval

Si la quantité complète de l'article commandé peut être confirmée pour la nouvelle date
calculée de mise à disposition de l'article, deux échéances sont générées pour le poste de
document de vente correspondant :

●  La date de la première échéance correspond à la date de livraison souhaitée par le client et
ne présente aucune quantité confirmée.

●  La date de la seconde échéance présente la date de livraison confirmée ainsi que la
quantité confirmée.

Astuce :
Si la quantité complète de l'article commandé ne peut pas être confirmée pour
une seule date et si des livraisons partielles sont nécessaires, le système crée
plusieurs échéances pour les dates de livraison correspondantes.
```

---

## PDF page 189

```text
Chapitre 5
Exercice 19

Vérification des résultats de l'ordonnancement
de l'expédition et du transport

Lors de la saisie d'une commande, vous souhaitez vérifier si la date de livraison souhaitée
peut être respectée. Si la date de livraison souhaitée ne peut pas être confirmée, la première
date de livraison possible est proposée au client.

Vérifiez à quelles dates doivent commencer chacune des étapes de traitement de l'expédition
et du transport afin que les produits commandés arrivent à temps chez le client.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           6-4##

DateLivrSouh.                         dans 1 semaine

Article                      Quantité commandée        Réceptionnaire

T-MS1##                5                     T-S50A##

T-MS3##                     1                     T-S50B##

Astuce :
Pour gérer le réceptionnaire différent pour le deuxième poste, accédez aux
détails du poste et sélectionnez la page à onglet Partenaires. Remplacez le
partenaire déterminé automatiquement pour le réceptionnaire par le
réceptionnaire indiqué ci-dessus.

Autorisez le système à redéterminer la division et le point d'expédition lorsque la fenêtre
pop-up correspondante s'affiche.

2. Déterminez les dates d'expédition pour l'échéance confirmée du poste 10 et notez-les.
```

---

## PDF page 190

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

Nom de zone                             Valeur

Date de livraison

Date de sortie des marchandises

Date de chargement

Date de planification du transport

3. Sauvegardez la commande client et notez le numéro du document.
_______________________________________________

4. Quelles sont les étapes de traitement de l'expédition et du transport à exécuter pour que
les marchandises puissent être chargées à la date déterminée ?

5. Pour vérifier les effets de l'ordonnancement de l'expédition et du transport que vous avez
effectué, essayez de créer une livraison sortante avec référence à la dernière commande
client. Utilisez les informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                 Date du jour

Commande                        Numéro de la dernière commande

La commande client peut-elle être livrée ?

______________________________________________

6. Vérifiez si votre commande client peut être livrée si vous utilisez la date de mise à
disposition de l'article du poste 10 de votre commande comme date de création planifiée.
La commande client apparaît-elle maintenant dans la liste des documents de vente à
livrer ?
____________________________________________________________

Attention :
Ne créez pas la livraison sortante.
```

---

## PDF page 191

```text
Chapitre 5
Solution 19

Vérification des résultats de l'ordonnancement
de l'expédition et du transport

Lors de la saisie d'une commande, vous souhaitez vérifier si la date de livraison souhaitée
peut être respectée. Si la date de livraison souhaitée ne peut pas être confirmée, la première
date de livraison possible est proposée au client.

Vérifiez à quelles dates doivent commencer chacune des étapes de traitement de l'expédition
et du transport afin que les produits commandés arrivent à temps chez le client.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           6-4##

DateLivrSouh.                         dans 1 semaine

Article                      Quantité commandée        Réceptionnaire

T-MS1##                5                     T-S50A##

T-MS3##                     1                     T-S50B##

Astuce :
Pour gérer le réceptionnaire différent pour le deuxième poste, accédez aux
détails du poste et sélectionnez la page à onglet Partenaires. Remplacez le
partenaire déterminé automatiquement pour le réceptionnaire par le
réceptionnaire indiqué ci-dessus.

Autorisez le système à redéterminer la division et le point d'expédition lorsque la fenêtre
pop-up correspondante s'affiche.

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.
```

---

## PDF page 192

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

b) Dans l’écran initial, saisissez le type de commande et les données d’organisation.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Dans l'écran de synthèse de la commande client, saisissez les informations
correspondantes.

e) Double-cliquez sur le poste 20 pour accéder aux détails du poste.

f) Sélectionnez la page à onglet Partenaire.

g) Dans la colonne Partenaire, modifiez le réceptionnaire.

h) Pour confirmer la modification du réceptionnaire, appuyez sur Entrée.

i) Pour confirmer les deux messages d'information, appuyez sur Entrée.

j) Dans la boîte de dialogue, cliquez sur Redéterminer pour autoriser le système à
redéterminer la division et le point d'expédition du poste.

2. Déterminez les dates d'expédition pour l'échéance confirmée du poste 10 et notez-les.

Nom de zone                             Valeur

Date de livraison

Date de sortie des marchandises

Date de chargement

Date de planification du transport

a) Dans la commande client, double-cliquez sur le poste 10 pour accéder aux détails du
poste.

b) Sélectionnez la page à onglet Échéances.

c) Sélectionnez l'échéance avec une quantité confirmée égale à cinq pièces.

d) Au-dessus des échéances, sélectionnez Expédition.
Les différentes dates s'affichent.

3. Sauvegardez la commande client et notez le numéro du document.
_______________________________________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document s'affiche.

4. Quelles sont les étapes de traitement de l'expédition et du transport à exécuter pour que
les marchandises puissent être chargées à la date déterminée ?

La préparation de l'article (prélèvement et emballage) et la planification du transport
doivent être exécutées pour que le chargement puisse commencer à temps.

5. Pour vérifier les effets de l'ordonnancement de l'expédition et du transport que vous avez
effectué, essayez de créer une livraison sortante avec référence à la dernière commande
client. Utilisez les informations suivantes :
```

---

## PDF page 193

```text
Sujet: Analyse des résultats de l'ordonnancement de l'expédition et du transport

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                 Date du jour

Commande                        Numéro de la dernière commande

La commande client peut-elle être livrée ?

______________________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Saisissez le point d'expédition et la date de création planifiée requise.

c) Cliquez sur Lancer.
Votre commande client n'est pas affichée dans la liste car il n’y a aucune échéance
pour la création de la livraison aujourd’hui.

6. Vérifiez si votre commande client peut être livrée si vous utilisez la date de mise à
disposition de l'article du poste 10 de votre commande comme date de création planifiée.
La commande client apparaît-elle maintenant dans la liste des documents de vente à
livrer ?
____________________________________________________________

Attention :
Ne créez pas la livraison sortante.

a) Dans l'application Création de livraisons sortantes, qui doit être encore active, modifiez
la date de création planifiée en sélectionnant Au dans la liste déroulante
correspondante.

b) Sélectionnez la date correspondante dans le calendrier.

c) Pour lancer la sélection, cliquez sur Lancer.
La commande client est à présent répertoriée et une livraison sortante peut être créée.
Le traitement de l'expédition doit commencer à la date de mise à disposition de
l'article pour que les marchandises parviennent au client à la date de livraison
confirmée.
```

---

## PDF page 194

```text
Chapitre 5 : Détermination automatique des données et ordonnancement

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Analyser les résultats de l'ordonnancement de l'expédition et du transport
```

---

## PDF page 195

```text
Chapitre 5

Évaluation des connaissances

1.  Les divisions utilisées dans les processus d'administration des ventes sont souvent
appelées divisions chargées de la livraison.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Parmi les fonctions suivantes, lesquelles dépendent des points d'expédition ?

Sélectionnez les réponses correctes.

X  A Ordonnancement des expéditions

X  B Détermination de l'itinéraire

X  C Création de la livraison

3. Dans un ordonnancement amont, la date de livraison souhaitée du client est supposée
être la date de livraison à prendre en compte.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

4. Le délai de planification du transport utilisé dans l'ordonnancement de l'expédition est
repris du point d'expédition.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 196

```text
Chapitre 5

Évaluation des connaissances - Réponses

1.  Les divisions utilisées dans les processus d'administration des ventes sont souvent
appelées divisions chargées de la livraison.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Les divisions utilisées dans les processus d'administration des ventes sont
souvent appelées divisions chargées de la livraison car elles représentent le centre de
distribution à partir duquel l'article est livré au client.

2. Parmi les fonctions suivantes, lesquelles dépendent des points d'expédition ?

Sélectionnez les réponses correctes.

X  A Ordonnancement des expéditions

X  B Détermination de l'itinéraire

X  C Création de la livraison

Correct. Toutes les fonctions mentionnées ici dépendent des points d'expédition.

3. Dans un ordonnancement amont, la date de livraison souhaitée du client est supposée
être la date de livraison à prendre en compte.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Dans un ordonnancement amont, la date de livraison souhaitée du client est
supposée être la date de livraison à prendre en compte. Dans un ordonnancement aval, la
date de livraison est calculée.
```

---

## PDF page 197

```text
Chapitre 5 : Évaluation des connaissances - Réponses

4. Le délai de planification du transport utilisé dans l'ordonnancement de l'expédition est
repris du point d'expédition.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Le délai de planification du transport est repris de l'itinéraire.
```

---

## PDF page 198

```text
Chapitre 5 : Évaluation des connaissances - Réponses
```

---

## PDF page 199

```text
CHAPITRE 6  Contrôle de disponibilité

Sujet 1

Exécution d'un contrôle de disponibilité – Principes de base                                 190
Exercice 20 : Vérification des principaux facteurs influençant le contrôle de           195
disponibilité
Exercice 21 : Vérification du transfert des besoins                               201
Exercice 22 : Vérification des options des livraisons complètes ou partielles         205

Sujet 2

Exécution d'un contrôle de disponibilité – Autres sujets                                     210
Exercice 23 : Exécution des contrôles de disponibilité                              217
Exercice 24 : Description des fonctions du contrôle de disponibilité                223

OBJECTIFS DU CHAPITRE

●  Exécution d'un contrôle de disponibilité – Principes de base

●  Exécution d'un contrôle de disponibilité – Autres sujets
```

---

## PDF page 200

```text
Chapitre 6
Sujet 1

Exécution d'un contrôle de disponibilité –
Principes de base

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Exécution d'un contrôle de disponibilité – Principes de base

Informations de base relatives aux contrôles de disponibilité
Le contrôle de disponibilité des articles dans un document de vente représente souvent une
fonction très importante pour les commerciaux. Lorsque vous créez une commande client,
vous avez généralement besoin des informations relatives à la quantité disponible des articles
commandés. Sans ces informations, vous ne pouvez pas confirmer la commande avec
certitude.

Attention :
Le contrôle de disponibilité des articles peut être exécuté à l'aide de différentes
stratégies (par exemple, via le contingentement). Dans la section suivante, nous
allons nous concentrer sur la stratégie la plus importante, appelée « disponible à
la vente » (ATP).

Vous pouvez influencer périmètre du contrôle de disponibilité dans les données de base
article. En effet, les besoins en contrôle de disponibilité peuvent varier selon les articles. Dans
la page à onglet ADV : données générales/division (zone Contrôle de disponibilité), vous
pouvez déterminer si et comment le contrôle de disponibilité doit être exécuté pour un article
lors du traitement de la commande.

Diverses options des tables de pilotage du Customizing influencent également le périmètre et
le comportement du contrôle de disponibilité, comme illustré dans la figure « Contrôle de
disponibilité dans les commandes clients ».
```

---

## PDF page 201

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

Figure 66: Contrôle de disponibilité dans les commandes clients

Il est aussi important de connaître la date à laquelle le contrôle de disponibilité doit être
effectué dans les commandes clients que la façon dont il doit être réalisé.

Le système calcule plusieurs dates pour chaque poste de la commande client à partir de
l'ordonnancement de l'expédition et du transport (calcul en amont à partir de la date de
livraison demandée). La date à prendre en compte pour le contrôle de disponibilité est la date
de mise à disposition de l'article. À cette date, la quantité d'articles disponible en stock doit
être suffisante pour correspondre à la date de livraison confirmée du client.

La figure « Contrôle de disponibilité du produit pour la date de mise à disposition de l'article »
illustre ce sujet.

Contrôle de disponibilité du produit pour la date de mise à disposition de l'article

Figure 67: Contrôle de disponibilité du produit pour la date de mise à disposition de l'article

Le contrôle de disponibilité du produit dans les commandes client est effectué au niveau de la
division pour l'article correspondant. La division peut être déterminée automatiquement ou
```

---

## PDF page 202

```text
Chapitre 6 : Contrôle de disponibilité

gérée manuellement. Au cours de la détermination automatique, le système recherche une
valeur de division dans les données de base appropriées selon la séquence suivante :

1. Fiche infos client-article

2. Fiche client réceptionnaire

3. Fiche article

Remarque :
Si vous saisissez manuellement la division chargée de la livraison lors de la
gestion des commandes client, la division que vous indiquez remplace la valeur
par défaut.

Contrôle au niveau de la division

Figure 68: Contrôle au niveau de la division

Vous pouvez influencer le périmètre du contrôle de disponibilité avec les saisies dans
certaines tables de pilotage du Customizing. Vous pouvez, entre autres, définir les
informations à inclure dans le contrôle de disponibilité.

Vous définissez ainsi les types de stock (stock de sécurité, stock en transfert ou stock en
contrôle qualité), les entrées (commandes d'achat ou ordres de fabrication) et les sorties
(commandes client, réservations de la gestion des articles) à inclure dans le contrôle.
```

---

## PDF page 203

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

Vérification du contrôle de disponibilité

Figure 69: Vérification du contrôle de disponibilité
```

---

## PDF page 204

```text
Chapitre 6 : Contrôle de disponibilité
```

---

## PDF page 205

```text
Chapitre 6
Exercice 20

Vérification des principaux facteurs
influençant le contrôle de disponibilité

Vous devez vérifier plusieurs données de base qui impactent les contrôles de disponibilité à
effectuer.

1. Vérifiez la fiche de l'article T-MS3##. Quel groupe de contrôle (contrôle de disponibilité)
est valide pour la division 1010 ?
_________________________

2. Vérifiez la division chargée de la livraison lors de la saisie de la commande client pour
l'organisation commerciale 1010, le canal de distribution 10 et le numéro d'article T-
MS3##.
__________________________

3. Vérifiez la division chargée de la livraison qui est gérée comme valeur par défaut dans la
fiche partenaire T-S50B##, l'organisation commerciale 1010, le canal de distribution 10 et
le secteur d'activité 00.
___________________________

4. Quel est l'ordre d'accès aux données de base lors du traitement d'une commande client
pour déterminer la valeur par défaut de la division chargée de la livraison ?
___________________________________________________________

___________________________________________________________

___________________________________________________________

5. Le contrôle de disponibilité lors de la saisie d'une commande client peut-il être effectué
dans une division différente de celle proposée ?
```

---

## PDF page 206

```text
Chapitre 6
Solution 20

Vérification des principaux facteurs
influençant le contrôle de disponibilité

Vous devez vérifier plusieurs données de base qui impactent les contrôles de disponibilité à
effectuer.

1. Vérifiez la fiche de l'article T-MS3##. Quel groupe de contrôle (contrôle de disponibilité)
est valide pour la division 1010 ?
_________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Modification d’article.

b) Dans l'écran initial, saisissez le numéro d'article.

c) Pour appeler la sélection de vues, appuyez sur Entrée.

d) Sélectionnez la vue ADV : données générales/division.

e) Pour confirmer la sélection, appuyez sur Entrée.

f) Dans la boîte de dialogue, saisissez la division 1010.

g) Pour accéder à la vue sélectionnée, appuyez sur Entrée.
Le groupe de contrôle pour le contrôle de disponibilité 02 est affecté. Si Y2 est affecté,
remplacez-le par 02.

2. Vérifiez la division chargée de la livraison lors de la saisie de la commande client pour
l'organisation commerciale 1010, le canal de distribution 10 et le numéro d'article T-
MS3##.
__________________________

a) Dans la fiche article, accédez à la page à onglet ADV : données org.commer.1.

b) En haut de l’écran, cliquez sur Niveaux organisation.

c) Saisissez l'organisation commerciale et le canal de distribution, puis appuyez sur
Entrée.
La division 1020 est affectée comme division chargée de la livraison.

3. Vérifiez la division chargée de la livraison qui est gérée comme valeur par défaut dans la
fiche partenaire T-S50B##, l'organisation commerciale 1010, le canal de distribution 10 et
le secteur d'activité 00.
___________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des données de base
clients.

b) Saisissez le numéro du partenaire et cliquez sur Lancer.
```

---

## PDF page 207

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

c) Sélectionnez le partenaire dans la liste pour accéder aux détails.

d) Sélectionnez l'onglet Domaines commerciaux.

e) Sélectionnez la ligne comportant l'organisation commerciale 1010, le canal de
distribution 10 et le secteur d'activité 00.

f) La division 1010 est saisie en tant que division chargée de la livraison dans les détails
du domaine commercial.

4. Quel est l'ordre d'accès aux données de base lors du traitement d'une commande client
pour déterminer la valeur par défaut de la division chargée de la livraison ?
___________________________________________________________

___________________________________________________________

___________________________________________________________

a) Lors de la saisie d'une commande client, l'ordre d'accès aux données de base est le
suivant pour déterminer la valeur par défaut de la division chargée de la livraison :

i. Fiche infos client-article

ii. Fiche partenaire (réceptionnaire)

iii. Fiche article

5. Le contrôle de disponibilité lors de la saisie d'une commande client peut-il être effectué
dans une division différente de celle proposée ?

Vous pouvez remplacer manuellement la proposition de division chargée de la livraison
dans la commande client. En outre, dans le cadre du contrôle de disponibilité, vous pouvez
également vérifier la mise à disposition des articles dans d'autres divisions.
```

---

## PDF page 208

```text
Chapitre 6 : Contrôle de disponibilité

Transfert des besoins
Lorsqu'un client commande des articles et vous créez la commande client appropriée, la
fourniture des quantités d'article correspondantes doit être garantie. Pour ce faire, les
besoins en composants découlant des quantités des postes de la commande client sont
transférés automatiquement et deviennent disponibles dans la planification des besoins en
composants (MRP).

Sur la base de ces informations, le responsable peut alors décider de quelle manière l'article
doit être obtenu (commandes d'achat, ordres de fabrication).

Astuce :
Les besoins en articles existants peuvent évidemment influencer le résultat d'un
contrôle de disponibilité.

La figure « Transfert des besoins » représente le transfert des besoins.

Figure 70: Transfert des besoins

Livraisons complètes et partielles
Vous pouvez conclure des accords avec vos clients concernant la création des livraisons. Plus
précisément, certains clients exigent toujours une seule livraison complète (l'intégralité des
quantités de tous les postes de commande doivent être livrés ensemble), alors que d'autres
autorisent les livraisons partielles (par exemple, si un article ne peut pas être confirmé pour la
date de livraison souhaitée). Vous pouvez gérer le paramètre correspondant pour chaque
domaine commercial dans les données de base du partenaire.

Remarque :
La décision relative aux livraisons partielles/complètes influence également le
résultat du contrôle de disponibilité.

La figure « Livraisons complètes et partielles » illustre les deux possibilités.
```

---

## PDF page 209

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

Figure 71: Livraisons complètes et partielles

Accord de livraison partielle

Si les livraisons partielles sont en principe autorisées par le client, vous pouvez également
déterminer si la livraison partielle d'un seul article est possible.

Pour cela, gérez les paramètres correspondants dans la fiche info client-article et/ou dans les
données de base du partenaire. Les principales options des livraisons partielles au niveau du
poste sont les suivantes :

●  Plusieurs livraisons partielles sont autorisées

●  Une seule livraison doit être créée (même si la quantité commandée ne peut pas être
satisfaite)

●  Une seule livraison complète (par poste de commande) est autorisée

●  Livraisons ultérieures non limitées

Comme l'indique la figure « Accord de livraison partielle », la fiche info client-article est
prioritaire lorsque le système détermine la valeur à utiliser dans une commande client.
```

---

## PDF page 210

```text
Chapitre 6 : Contrôle de disponibilité

Figure 72: Accord de livraison partielle

Vous pouvez modifier les paramètres manuellement lorsque vous saisissez une commande
client. Cela peut s'avérer nécessaire si un client préfère généralement des livraisons
complètes (gérées dans les données de base du partenaire) mais autorise une livraison
partielle pour une commande particulière.
```

---

## PDF page 211

```text
Chapitre 6
Exercice 21

Vérification du transfert des besoins

Les quantités d'articles dans les commandes client sont transférées en tant que besoins au
service de planification des besoins en composants. Cette information est essentielle pour
déclencher l'approvisionnement correspondant à temps et avec la quantité appropriée.

1. Vous souhaitez une synthèse de la situation réelle des besoins et des stocks pour un
article donné. Affichez l'état dynamique des stocks actuel pour l'article T-MS3##. Notez le
nombre de pièces en stock dans la division 1010.
___________________________________________________________

2. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           7-6##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS3##

Qté d'ordre                          20 pièces

Sauvegardez la commande client et notez son numéro.

________________________

3. Vous souhaitez à présent vérifier si la quantité commandée a été transférée correctement
comme besoin dans le service de planification des besoins en composants. Affichez une
deuxième fois l'état dynamique des stocks actuel pour l'article T-MS3## et la
division 1010. Quelle quantité a été transférée en tant que besoin ?
_________________________

4. Pour quelle date le besoin a-t-il été transféré ? À quelle date de la commande client cette
date correspond-elle ?
```

---

## PDF page 212

```text
Chapitre 6
Solution 21

Vérification du transfert des besoins

Les quantités d'articles dans les commandes client sont transférées en tant que besoins au
service de planification des besoins en composants. Cette information est essentielle pour
déclencher l'approvisionnement correspondant à temps et avec la quantité appropriée.

1. Vous souhaitez une synthèse de la situation réelle des besoins et des stocks pour un
article donné. Affichez l'état dynamique des stocks actuel pour l'article T-MS3##. Notez le
nombre de pièces en stock dans la division 1010.
___________________________________________________________

a) Dans la barre de lancement SAP Fiori (groupe de vignettes Material Availability), lancez
l'application Contrôle de la couverture article.

b) Saisissez le numéro de l'article et la division.

c) Pour accéder à l'état dynamique des stocks, sélectionnez OK.
La quantité en stock est affichée dans la ligne comportant l'élément MRP Stock.

2. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           7-6##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS3##

Qté d'ordre                          20 pièces

Sauvegardez la commande client et notez son numéro.

________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, saisissez le type de commande et les entités organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.
```

---

## PDF page 213

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

d) Saisissez les données répertoriées dans le tableau ci-dessus.

e) Pour sauvegarder la commande, cliquez sur Sauvegarder.
Le numéro de document s'affiche.

3. Vous souhaitez à présent vérifier si la quantité commandée a été transférée correctement
comme besoin dans le service de planification des besoins en composants. Affichez une
deuxième fois l'état dynamique des stocks actuel pour l'article T-MS3## et la
division 1010. Quelle quantité a été transférée en tant que besoin ?
_________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Contrôle de la couverture
article.

b) Saisissez le numéro de l'article et la division.

c) Pour accéder aux détails, cliquez sur OK.
Vous pouvez voir les besoins de la commande client sur la ligne comportant l’élément
MRP Commande client XX-YY (XX = numéro de commande client, YY = numéro du
poste).

4. Pour quelle date le besoin a-t-il été transféré ? À quelle date de la commande client cette
date correspond-elle ?

La date du besoin (figurant dans la première colonne de l'état dynamique des stocks)
correspond à  la date de mise à disposition de  l'article indiquée dans  le poste de
commande client.
```

---

## PDF page 214

```text
Chapitre 6 : Contrôle de disponibilité
```

---

## PDF page 215

```text
Chapitre 6
Exercice 22

Vérification des options des livraisons
complètes ou partielles

Dans certains cas, le système n'est pas en mesure de confirmer les quantités commandées
de tous les articles pour une date de livraison souhaitée lors de la création de la commande.
Vous pouvez alors fractionner la commande en livraisons partielles ou attendre que les
composants de tous les articles soient disponibles pour une livraison complète. Dans les
données de base, vous pouvez gérer les options de livraisons souhaitées par le client.

1. Vous souhaitez vérifier si les livraisons partielles sont autorisées pour une commande
client. Créez d'abord la commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           7-7##

DateLivrSouh.                         dans 1 semaine

Article                                   Quantité commandée

T-MS1##                           10 pièces

T-MS2##                           10 pièces

2. Déterminez si la commande client peut être partiellement livrée.
Quel accord se rapportant à une livraison complète figure dans la commande ?

__________________________________________________________

3. Quelle donnée de base est la source qui détermine ce code Livraison complète ?

4. Quel accord se rapportant aux livraisons partielles figure dans le poste 10 de la
commande ?
___________________________________________________________
```

---

## PDF page 216

```text
Chapitre 6 : Contrôle de disponibilité

5. Quelles sont les données de base utilisées pour proposer le code LivrPart/poste dans le
poste de commande ?

6. Est-il possible de répartir la quantité totale d'un poste de commande entre plusieurs
livraisons si le code Livraison complète n'est pas sélectionné dans l'en-tête de la
commande ?
```

---

## PDF page 217

```text
Chapitre 6
Solution 22

Vérification des options des livraisons
complètes ou partielles

Dans certains cas, le système n'est pas en mesure de confirmer les quantités commandées
de tous les articles pour une date de livraison souhaitée lors de la création de la commande.
Vous pouvez alors fractionner la commande en livraisons partielles ou attendre que les
composants de tous les articles soient disponibles pour une livraison complète. Dans les
données de base, vous pouvez gérer les options de livraisons souhaitées par le client.

1. Vous souhaitez vérifier si les livraisons partielles sont autorisées pour une commande
client. Créez d'abord la commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           7-7##

DateLivrSouh.                         dans 1 semaine

Article                                   Quantité commandée

T-MS1##                           10 pièces

T-MS2##                           10 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l’écran initial, saisissez le type de commande et les données d’organisation.

c) Pour accéder aux détails de la commande, appuyez sur Entrée.

d) Saisissez les données restantes comme indiqué ci-dessus.

2. Déterminez si la commande client peut être partiellement livrée.
Quel accord se rapportant à une livraison complète figure dans la commande ?

__________________________________________________________

a) Dans la commande client, examinez le contenu de la page à onglet Vente.
```

---

## PDF page 218

```text
Chapitre 6 : Contrôle de disponibilité

La case Livraison complète n'est pas cochée. Cela signifie qu'une livraison complète
n'est pas exigée et que les postes peuvent être fractionnés en plusieurs livraisons.

3. Quelle donnée de base est la source qui détermine ce code Livraison complète ?

Le code est proposé à partir de la fiche partenaire.

4. Quel accord se rapportant aux livraisons partielles figure dans le poste 10 de la
commande ?
___________________________________________________________

a) Double-cliquez sur le poste 10 dans la commande client.

b) Sélectionnez la page à onglet Expédition.
La zone LivrPart/poste est vide. Cela signifie que les livraisons partielles pour ce poste
sont autorisées.

5. Quelles sont les données de base utilisées pour proposer le code LivrPart/poste dans le
poste de commande ?

La valeur par défaut de l’indicateur peut être gérée dans les fiches infos client-article et
dans la fiche partenaire. S’il existe une fiche info client-article, la valeur du code est reprise
de cette source.

6. Est-il possible de répartir la quantité totale d'un poste de commande entre plusieurs
livraisons si le code Livraison complète n'est pas sélectionné dans l'en-tête de la
commande ?

Si le code Livraison complète n'est pas sélectionné dans l'en-tête de la commande,
l'accord de livraison partielle au niveau du poste détermine si la quantité du poste peut
être fractionnée entre plusieurs livraisons.
```

---

## PDF page 219

```text
Sujet: Exécution d'un contrôle de disponibilité – Principes de base

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Exécution d'un contrôle de disponibilité – Principes de base
```

---

## PDF page 220

```text
Chapitre 6
Sujet 2

Exécution d'un contrôle de disponibilité –
Autres sujets

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Exécution d'un contrôle de disponibilité – Autres sujets

Contrôles de disponibilité – Exemple de scénario 1
Voici quelques scénarios pour comprendre le fonctionnement du contrôle de disponibilité des
articles à l'aide de la logique ATP (disponibilité à la vente).

Pour le premier scénario, la situation d'un article est la suivante :

●  100 pièces en stock ;

●  Commandes d'achat existantes pour des quantités égales à 50 et 60 pièces ;

●  Commandes client existantes pour des quantités égales à 100, 40 et 50 pièces.

Voyons à présent quel sera le résultat du contrôle de disponibilité avec la saisie d'une nouvelle
commande client pour 10 pièces de l'article. Le système exécute l'ordonnancement des
livraisons (ordonnancement amont) en fonction de la date de livraison souhaitée par le client
et détermine la date de disponibilité de l'article. Il exécute ensuite le contrôle de disponibilité à
cette date.

La figure « Contrôles de disponibilité - Scénario 1 » illustre la situation décrite.

Figure 73: Contrôles de disponibilité - Scénario 1
```

---

## PDF page 221

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Contrôles de disponibilité - Résultat du scénario 1

Le système peut confirmer les 10 pièces de la nouvelle commande client pour la date de
livraison souhaitée. En effet, les 10 pièces disponibles de la première commande d'achat
(quantité de 50 pièces) peuvent être utilisées pour confirmer la nouvelle demande. En
d'autres termes, la quantité ATP à la date de mise à disposition de l’article est de 10 pièces.

La figure « Contrôles de disponibilité - Résultat du scénario 1 » montre le résultat du premier
scénario.

Figure 74: Contrôles de disponibilité - Résultat du scénario 1

Contrôles de disponibilité – Exemple de scénario 2
Dans le deuxième scénario, l'état initial est le même :

●  100 pièces en stock ;

●  Commandes d'achat existantes pour des quantités égales à 50 et 60 pièces ;

●  Commandes client existantes pour des quantités égales à 100, 40 et 50 pièces.

Une nouvelle commande client est passée, cette fois avec les propriétés suivantes :

●  La quantité commandée est égale à 20 pièces ;

●  Le client exige une livraison complète

●  La date de livraison souhaitée est antérieure à celle du scénario 1

La figure « Contrôles de disponibilité - Scénario 2 » illustre la situation décrite.
```

---

## PDF page 222

```text
Chapitre 6 : Contrôle de disponibilité

Figure 75: Contrôles de disponibilité - Scénario 2

Contrôles de disponibilité - Résultat du scénario 2

Dans ce cas, la date de livraison souhaitée ne peut pas être confirmée par le système. Les
100 pièces en stock devant être utilisées pour la première commande client (égale à
100 pièces), la quantité est insuffisante à la date de mise à disposition de l'article (la quantité
ATP est 0).

Le système utilise les informations sur la disponibilité et l'ordonnancement des livraisons
(ordonnancement aval) afin de déterminer la prochaine date de confirmation possible des
marchandises pour le client.

En raison de l'accord de livraison (livraison complète exigée), les quantités ne peuvent pas
être fractionnées. Par conséquent, la nouvelle date de mise à disposition de l'article sera la
date d'entrée de la quantité correspondant à la deuxième commande d'achat. À partir de
cette nouvelle date de mise à disposition de l'article, le système calcule la date de livraison du
client en ajoutant les composants horaires (durée du prélèvement/d'emballage, par
exemple).

Astuce :
Dans la commande client, le système crée une deuxième échéance avec la
nouvelle date de livraison (confirmable) de l'article concerné.

La figure « Contrôles de disponibilité - Résultat du scénario 2 » contient le résultat du
deuxième scénario.
```

---

## PDF page 223

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Figure 76: Contrôles de disponibilité - Résultat du scénario 2

Contrôles de disponibilité – Exemple de scénario 3
Le troisième scénario est très similaire au deuxième, excepté que le client autorise les
livraisons partielles. L'état initial est donc à nouveau le suivant :

●  100 pièces en stock ;

●  Commandes d'achat existantes pour des quantités égales à 50 et 60 pièces ;

●  Commandes client existantes pour des quantités égales à 100, 40 et 50 pièces.

Les propriétés de la nouvelle commande client sont les suivantes :

●  La quantité commandée est égale à 20 pièces ;

●  Le client souhaite au moins une livraison partielle le plus tôt possible ;

●  La date de livraison souhaitée est la même que celle du scénario 2.

La figure « Contrôles de disponibilité - Scénario 3 » illustre la situation correspondante.
```

---

## PDF page 224

```text
Chapitre 6 : Contrôle de disponibilité

Figure 77: Contrôles de disponibilité - Scénario 3

Contrôles de disponibilité - Résultat du scénario 3

Comme dans le deuxième scénario, il n'est pas possible de confirmer la date de livraison
souhaitée. Cependant, comme les livraisons partielles sont possibles, la nouvelle date de mise
à disposition de l'article pour les 10 premières pièces correspond à la date d'entrée des
50 pièces de la commande d'achat. Avec l'entrée des 60 pièces de la deuxième commande
d'achat, le système obtient la date de mise à disposition de l'article pour les 10 pièces
restantes.

Par conséquent, le système calcule deux dates de livraison pour le client en fonction des deux
nouvelles dates de mise à disposition de l'article.

Astuce :
Dans la commande client, le système crée deux nouvelles échéances pour les
deux nouvelles dates de livraison. Il existe donc trois échéances au total, compte
tenu de la première avec la date de livraison souhaitée non confirmée.

La figure « Contrôles de disponibilité - Résultat du scénario 3 » contient le résultat du
troisième scénario.
```

---

## PDF page 225

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Figure 78: Contrôles de disponibilité - Résultat du scénario 3

Contrôles de disponibilité – Exemple de scénario 4
Le Scénario 4 modifie l'étendue du contrôle de disponibilité en ajoutant le délai de
réapprovisionnement. Le délai de réapprovisionnement peut être spécifié pour chaque article
comme suit :

●  Pour les produits commercialisables : délai de réapprovisionnement = délai prévisionnel de
livraison + temps de réception

●  Pour les produits fabriqués : délai de réapprovisionnement = délai de fabrication interne

Le système suppose que l'article sera disponible au plus tard à la fin du délai de
réapprovisionnement.

Astuce :
Par conséquent, toutes les demandes d'article dont la date de mise à disposition
est postérieure à l'expiration du délai de réapprovisionnement seront confirmées
par le contrôle de disponibilité.

Excepté la modification de l'étendue du contrôle de disponibilité, l'état initial est le même que
dans les autres scénarios :

●  100 pièces en stock ;

●  Commandes d'achat existantes pour des quantités égales à 50 et 60 pièces ;

●  Commandes client existantes pour des quantités égales à 100, 40 et 50 pièces.

Nous recevons une commande client supplémentaire avec les mêmes restrictions qu'au
scénario 2 :

●  La quantité commandée est égale à 20 pièces ;

●  Le client exige une livraison complète
```

---

## PDF page 226

```text
Chapitre 6 : Contrôle de disponibilité

●  La date de livraison souhaitée est antérieure à celle du scénario 1

Comme le système prend maintenant en compte le délai de réapprovisionnement dans le
contrôle de disponibilité et que la date de mise à disposition de l'article se situe après
l'expiration du délai de réapprovisionnement, la date de livraison souhaitée peut être
confirmée.

La figure « Contrôles de disponibilité - Scénario 4 » illustre le scénario 4.

Figure 79: Contrôles de disponibilité - Scénario 4
```

---

## PDF page 227

```text
Chapitre 6
Exercice 23

Exécution des contrôles de disponibilité

Pour tester les options du contrôle de disponibilité, créez une commande client et interprétez
le comportement du système.

1. Pour l'article T-MS3##, vérifiez que le groupe de contrôle (zone Contrôle de disponibilité)
dans la fiche article est défini sur 02 pour la division 1010.

2. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50B##

Réf. client                           7-3##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS3##

Qté d'ordre                          95 pièces

3. Le nombre d'articles disponibles pour la date de livraison souhaitée étant insuffisant,
l'écran du contrôle de disponibilité reste affiché lors de la saisie de la commande.

Astuce :
Si vous avez déjà quitté l'écran de contrôle des disponibilités, sélectionnez le
poste de commande et cliquez sur Contrôler disponibilité du poste.

Pour quelle division le contrôle de disponibilité a-t-il été exécuté ?

4. Combien de pièces pouvez-vous confirmer pour la date de livraison souhaitée ?
```

---

## PDF page 228

```text
Chapitre 6 : Contrôle de disponibilité

5. Vous savez que l'article peut également être livré par la division 1020. Vous voulez donc
savoir si cet article peut être disponible dans cette division. Contrôlez la disponibilité de
l'article dans la division 1020.

Astuce :
Pour vérifier la disponibilité pour une autre division, sur l'écran Contrôle de
disponibilité, sélectionnez Autres divisions.

6. Combien de pièces pouvez-vous confirmer dans la division 1020 à la date de livraison
souhaitée ?

7. Vous décidez de livrer les articles à partir de la division 1020 Modifiez la division de votre
poste en conséquence.

8. Vous voulez savoir si les commandes d'achat existantes ont été prises en compte dans le
contrôle de disponibilité. Examinez l'étendue du contrôle en conséquence.

Astuce :
Vous pouvez afficher l'étendue de ce contrôle dans l'écran du contrôle de
disponibilité ou dans l'écran de synthèse correspondant. Dans l'écran
correspondant, sélectionnez Étendue du contrôle.

9. Déterminez si le délai de réapprovisionnement a été pris en compte dans le contrôle de
disponibilité.

10. Sauvegardez la commande client et notez son numéro.
_______________________
```

---

## PDF page 229

```text
Chapitre 6
Solution 23

Exécution des contrôles de disponibilité

Pour tester les options du contrôle de disponibilité, créez une commande client et interprétez
le comportement du système.

1. Pour l'article T-MS3##, vérifiez que le groupe de contrôle (zone Contrôle de disponibilité)
dans la fiche article est défini sur 02 pour la division 1010.
a) Dans la barre de lancement SAP Fiori, lancez l'application Modification d’article.

b) Saisissez le numéro d'article et appuyez sur Entrée.

c) Sélectionnez la vue ADV : données générales/division, puis appuyez sur Entrée.

d) Saisissez la division 1010 et appuyez sur Entrée.

e) Vérifiez la valeur de la zone Contrôle de disponibilité et remplacez-la par 02 si
nécessaire.

f) Cliquez sur Sauvegarder.

2. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50B##

Réf. client                           7-3##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS3##

Qté d'ordre                          95 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial, saisissez le type de commande et les entités organisationnelles.

c) Pour accéder aux détails de la commande client, appuyez sur Entrée.

d) Saisissez les données répertoriées dans le tableau ci-dessus.

e) Si un message d'avertissement s'affiche indiquant que le point de commande pour le
poste 00010 a été dépassé : 50 pièces, appuyez sur Entrée pour valider.
```

---

## PDF page 230

```text
Chapitre 6 : Contrôle de disponibilité

3. Le nombre d'articles disponibles pour la date de livraison souhaitée étant insuffisant,
l'écran du contrôle de disponibilité reste affiché lors de la saisie de la commande.

Astuce :
Si vous avez déjà quitté l'écran de contrôle des disponibilités, sélectionnez le
poste de commande et cliquez sur Contrôler disponibilité du poste.

Pour quelle division le contrôle de disponibilité a-t-il été exécuté ?

La division concernée figure dans l'écran Contrôle de disponibilité. Il s'agit de la division
1010.

4. Combien de pièces pouvez-vous confirmer pour la date de livraison souhaitée ?

La quantité confirmée pour la date de livraison souhaitée s’affiche.

5. Vous savez que l'article peut également être livré par la division 1020. Vous voulez donc
savoir si cet article peut être disponible dans cette division. Contrôlez la disponibilité de
l'article dans la division 1020.

Astuce :
Pour vérifier la disponibilité pour une autre division, sur l'écran Contrôle de
disponibilité, sélectionnez Autres divisions.

a) Dans l'écran Contrôle de disponibilité, sélectionnez Autres divisions.

b) Dans la boîte de dialogue de Sélection de division, sélectionnez la division 1020.

c) Sélectionnez Contrôler division.

6. Combien de pièces pouvez-vous confirmer dans la division 1020 à la date de livraison
souhaitée ?

La totalité de la quantité peut être confirmée.

7. Vous décidez de livrer les articles à partir de la division 1020 Modifiez la division de votre
poste en conséquence.
a) Cochez la case correspondant à la ligne qui contient la division 1020.

b) Choisissez Division en haut de l'écran.

8. Vous voulez savoir si les commandes d'achat existantes ont été prises en compte dans le
contrôle de disponibilité. Examinez l'étendue du contrôle en conséquence.

Astuce :
Vous pouvez afficher l'étendue de ce contrôle dans l'écran du contrôle de
disponibilité ou dans l'écran de synthèse correspondant. Dans l'écran
correspondant, sélectionnez Étendue du contrôle.
```

---

## PDF page 231

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

a) Dans la commande client, sélectionnez le poste 10 puis cliquez sur Afficher
disponibilité.

b) En haut de l’écran Synthèse des disponibilités, sélectionnez Étendue du ctrle.
Dans ce cas, les commandes d'achat ont également été prises en compte.

9. Déterminez si le délai de réapprovisionnement a été pris en compte dans le contrôle de
disponibilité.

Lorsque  vous  affichez  le  périmètre  de  ce  contrôle,  le  code  Sans  délai  de
réapprovisionnement détermine si le délai de réapprovisionnement a été pris en compte.
Dans ce cas,  le code Sans délai de réapprovisionnement est activé et  le délai de
réapprovisionnement n'a donc pas été pris en compte.

10. Sauvegardez la commande client et notez son numéro.
_______________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document s'affiche.
```

---

## PDF page 232

```text
Chapitre 6 : Contrôle de disponibilité
```

---

## PDF page 233

```text
Chapitre 6
Exercice 24

Description des fonctions du contrôle de
disponibilité

1. Pourquoi le résultat d'un contrôle de disponibilité dans la commande client peut-il
dépendre d'un accord de livraison partielle ?

2. Pourquoi faut-il que l'ordonnancement de l'expédition soit réalisé avant le contrôle de
disponibilité dans la commande client ?

3. Pourquoi l'ordonnancement de l'expédition est-il réalisé après le contrôle de disponibilité
si le poste ne peut être confirmé pour la date de livraison souhaitée ?
```

---

## PDF page 234

```text
Chapitre 6
Solution 24

Description des fonctions du contrôle de
disponibilité

1. Pourquoi le résultat d'un contrôle de disponibilité dans la commande client peut-il
dépendre d'un accord de livraison partielle ?

Si seule une partie de la quantité requise est disponible à la date de livraison souhaitée et
si le client accepte une livraison partielle, la livraison peut être fractionnée et une quantité
partielle peut être confirmée pour la date de livraison souhaitée. Si le client n'autorise pas
les livraisons partielles, la quantité complète ne peut être confirmée qu'à une date
postérieure.

2. Pourquoi faut-il que l'ordonnancement de l'expédition soit réalisé avant le contrôle de
disponibilité dans la commande client ?

Le contrôle de disponibilité s'effectue à la date de mise à disposition de l'article. Les
articles sont requis à cette date car le temps nécessaire à leur emballage, à leur
prélèvement, à leur chargement et à leur transport doit être pris en compte avant la date
de livraison souhaitée. La date de mise à disposition de l'article doit donc être déterminée
dans la commande client avant l'exécution du contrôle de disponibilité.

3. Pourquoi l'ordonnancement de l'expédition est-il réalisé après le contrôle de disponibilité
si le poste ne peut être confirmé pour la date de livraison souhaitée ?

Si le poste ne peut pas être confirmé pour la date de livraison souhaitée, le système
effectue l'ordonnancement de l'expédition à partir de la date de mise à disposition de
l'article au plus tôt (ordonnancement aval) afin de déterminer une date de livraison
confirmable.
```

---

## PDF page 235

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Traitement des reliquats
Il est parfois impossible de confirmer une commande client malgré les différentes options
permettant d'ajuster le périmètre du contrôle de disponibilité. Dans SAP S/4HANA., ces
commandes clients sont appelées reliquats.

La figure « Traitement des reliquats » indique les principales raisons à l'origine des reliquats.

Figure 80: Traitement des reliquats

Traitement des reliquats – Stratégies de confirmation

Dans la plupart des cas, il n'est pas possible de redresser la situation. Le traitement des
reliquats peut néanmoins être une option.

Avec le traitement des reliquats, vous pouvez modifier les confirmations d'article existantes.
Par exemple, vous pouvez réduire la quantité commandée confirmée pour un client (moins
prioritaire) et augmenter la quantité commandée confirmée pour un autre client (plus
prioritaire).

Lors du traitement des reliquats dans SAP S/4HANA., vous pouvez utiliser différentes
stratégies de confirmation. Ces stratégies déterminent la façon de traiter les différents
besoins en article.
```

---

## PDF page 236

```text
Chapitre 6 : Contrôle de disponibilité

Figure 81: Traitement des reliquats – Stratégies de confirmation

Traitement des reliquats – Exemple

Avant de pouvoir exécuter le traitement des reliquats (BOP), plusieurs éléments doivent être
préparés.

un segment BOP contient les critères identifiant un ensemble de besoins à traiter de façon
similaire lors d’un cycle BOP. Le contrôle de disponibilité apportant les confirmations selon le
principe du premier arrivé/premier servi, la méthode de classement des besoins est cruciale.
Un segment BOP doit donc également contenir un hiérarchiseur, qui trie les besoins selon une
séquence dédiée.

une variante BOP contient une série d'options qui définissent les besoins qui sont contrôlés
(segments BOP) et la façon de les traiter (stratégies de confirmation). Chaque cycle BOP se
fonde sur une variante BOP.

Exécution BOP : un contrôle de disponibilité en masse des besoins (par exemple, postes de la
commande client), exécuté comme une étape dédiée dans le processus de traitement des
commandes (par exemple, après une exécution de la planification des besoins ou avant la
création d'un échéancier de livraisons). Un cycle BOP est déclenché en ligne par un utilisateur
autorisé ou planifié comme un job d'arrière-plan par le responsable du traitement des
commandes.

La figure « Traitement des reliquats - Exemple » est un exemple des éléments que peut inclure
une variante de BOP.
```

---

## PDF page 237

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Figure 82: Traitement des reliquats – Exemple
```

---

## PDF page 238

```text
Chapitre 6 : Contrôle de disponibilité

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Exécution d'un contrôle de disponibilité – Autres sujets
```

---

## PDF page 239

```text
Chapitre 6

Évaluation des connaissances

1.  Identifiez la séquence correcte utilisée par le système pour accéder aux données de base
lors de la recherche de la division chargée de la livraison par défaut dans une commande
client.

Classez dans l'ordre

0 Fiche article

0 Fiche infos client-article

0 Fiche client réceptionnaire

2. Parmi les facteurs suivants, lesquels peuvent être pris en compte par le périmètre du
contrôle utilisé pour évaluer la disponibilité du stock lors de la saisie des commandes
client ?

Sélectionnez les réponses correctes.

X  A Commandes client existantes

X  B Priorité de livraison du client

X  C Commandes d'achat

X  D Type d'article

X  E Réservations d'articles

3.  Laquelle des options suivantes contient un ensemble d'options qui définit les besoins
contrôlés et la manière dont ils sont seront gérés lors du traitement des reliquats (BOP) ?

Sélectionnez la réponse correcte.

X  A Segment BOP

X  B Variante BOP

X  C Cycle BOP
```

---

## PDF page 240

```text
Chapitre 6

Évaluation des connaissances - Réponses

1.  Identifiez la séquence correcte utilisée par le système pour accéder aux données de base
lors de la recherche de la division chargée de la livraison par défaut dans une commande
client.

Classez dans l'ordre

3 Fiche article

1 Fiche infos client-article

2 Fiche client réceptionnaire

Correct. Lors de la détermination automatique, le système recherche une valeur par
défaut valide pour la division dans les données de base pertinentes à l'aide de la séquence
suivante : 1. Fiche infos client-article 2. Fiche client réceptionnaire 3. Fiche article.

2. Parmi les facteurs suivants, lesquels peuvent être pris en compte par le périmètre du
contrôle utilisé pour évaluer la disponibilité du stock lors de la saisie des commandes
client ?

Sélectionnez les réponses correctes.

X  A Commandes client existantes

X  B Priorité de livraison du client

X  C Commandes d'achat

X  D Type d'article

X  E Réservations d'articles

Correct. Lors de l'évaluation de la disponibilité du stock, le périmètre du contrôle peut
prendre en compte les commandes client existantes pour l'article, les commandes d'achat
planifiées pour réapprovisionner l'article et les réservations de l’article. D'autres facteurs
potentiels incluent les ordres de fabrication (pour les articles produits en interne), les
documents de livraison, les différentes catégories de stock magasin et si le délai de
réapprovisionnement doit être exclu.
```

---

## PDF page 241

```text
Chapitre 6 : Évaluation des connaissances - Réponses

3.  Laquelle des options suivantes contient un ensemble d'options qui définit les besoins
contrôlés et la manière dont ils sont seront gérés lors du traitement des reliquats (BOP) ?

Sélectionnez la réponse correcte.

X  A Segment BOP

X  B Variante BOP

X  C Cycle BOP

Correct. une variante BOP contient une série d'options qui définissent les besoins qui sont
contrôlés (segments BOP) et la façon de les traiter (stratégies de confirmation). Chaque
cycle BOP se fonde sur une variante BOP.
```

---

## PDF page 242

```text
Chapitre 6 : Évaluation des connaissances - Réponses
```

---

## PDF page 243

```text
CHAPITRE 7  Opération groupée

Sujet 1

Exécution d’opérations groupées                                                   234
Exercice 25 : Création des livraisons sortantes via une opération groupée           239
Exercice 26 : Achèvement des fonctions d'expédition via une opération groupée      243
Exercice 27 : Création de documents de facturation à l'aide d'une opération groupée  249

OBJECTIFS DU CHAPITRE

●  Exécution d’opérations groupées
```

---

## PDF page 244

```text
Chapitre 7
Sujet 1

Exécution d’opérations groupées

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Exécution d’opérations groupées

Réserves de travail
Vous souhaitez créer des documents liés à vos commandes clients. Cette action peut souvent
être effectuée par une opération groupée. Quel que soit le type de document que vous
souhaitez créer, la procédure est très similaire. Vous devez d’abord sélectionner tous les
documents pour lesquels vous voulez créer les documents liés. Vous créez ensuite les
documents liés.

La figure « Utilisation de réserves de travail » présente les étapes de processus pouvant être
effectuées via une opération groupée.

Figure 83: Utilisation de réserves de travail

Une opération groupée permet parfois de créer un seul document lié pour plusieurs
documents précédents. Par exemple, vous pouvez regrouper les articles de trois commandes
client en une seule livraison ou créer une seule facture pour plusieurs livraisons sortantes. En
```

---

## PDF page 245

```text
Sujet: Exécution d’opérations groupées

général, cette procédure est possible mais le résultat dépend des valeurs contenues dans
certaines zones des documents sélectionnés (critères de fractionnement).

Tableau 2: Critères de fractionnement
Le tableau suivant répertorie certains des critères les plus fréquemment utilisés :
Critères                               Conséquence

Réceptionnaires différents dans les com-     Pas de regroupement dans une livraison sor-
mandes client                               tante

Points d'expédition différents dans les com-  Pas de regroupement dans une livraison sor-
mandes client                               tante

Conditions de paiement différentes dans les  Pas de regroupement dans un document de
commandes client                            facturation

Astuce :
Vous pouvez gérer certains des critères qui s'appliquent au regroupement de
documents dans le Customizing.

Opération groupée - Livraisons
Les livraisons sortantes peuvent être créées individuellement par commande client mais
aussi par une opération groupée. À l'aide de cette approche, en fonction de divers critères, le
système peut combiner automatiquement les postes de plusieurs commandes clients pour
réduire le nombre de livraisons sortantes. Cette fonction peut être utilisée comme suit :

●  Traitement en ligne

Utilisez l’application correspondante (Création de livraisons sortantes, par exemple)

●  Traitement en arrière-plan

Utilisez un job d'arrière-plan à exécuter pendant les heures creuses.

Les commandes clients correspondantes peuvent être sélectionnées selon différents critères
comme le point d'expédition et la date de création de la livraison.

Vous obtenez une liste de commandes clients qui répondent à vos critères de sélection. Dans
cette liste, vous pouvez affiner votre sélection à l'aide des fonctions de tri et de filtrage. À
partir de la liste, vous pouvez créer les livraisons sortantes correspondantes.
```

---

## PDF page 246

```text
Chapitre 7 : Opération groupée

Figure 84: Opération groupée de l'échéancier de livraisons

Exemples de création de livraisons sortantes

Certaines zones des données de base et des documents de vente peuvent être utilisées pour
influencer le comportement du système lors d'une opération groupée. Les scénarios suivants
sont de bons exemples :

●  Le client exige une livraison complète.

Cet ajustement signifie que toutes les quantités de tous les postes d'une commande client
donnée doivent être livrées en une seule livraison sortante.

●  Le client n'exige pas de livraison complète.

Vous pouvez définir un accord de livraisons partielles avec le client.

●  Le client autorise la combinaison de commandes.

Le client vous autorise à combiner les postes de plusieurs commandes en une seule
livraison sortante au cours de l'opération groupée. La combinaison de postes de
différentes commandes clients n'est possible que si les postes présentent plusieurs
caractéristiques communes, par exemple :

-   Point d'expédition

-  Date de livraison

-  Réceptionnaire

-   Itinéraire

-  Incoterms

La figure « Exemples de création de livraisons sortantes » illustre les différents scénarios.
```

---

## PDF page 247

```text
Sujet: Exécution d’opérations groupées

Figure 85: Exemples de création de livraisons sortantes
```

---

## PDF page 248

```text
Chapitre 7 : Opération groupée
```

---

## PDF page 249

```text
Chapitre 7
Exercice 25

Création des livraisons sortantes via une
opération groupée

Bien que les commandes clients soient saisies individuellement, les documents liés
correspondants sont généralement créés par le biais d'une opération groupée. Ainsi,
plusieurs documents sont créés en une seule étape.

1. Lancez la création de livraisons sortantes avec référence à plusieurs commandes clients à
l'aide des informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Début de la semaine en cours jusqu'à la fin
de la semaine suivante

2. Pourquoi au moins une des commandes client que vous avez créées apparaît-elle deux
fois dans la liste ?

3. Vérifiez que vous avez sélectionné uniquement les documents qui sont traités par le point
d'expédition Z0##. Sélectionnez toutes les commandes clients et créez les livraisons
sortantes correspondantes.

4. Combien de livraisons sortantes ont été créées ? Notez les numéros des livraisons
sortantes créées.
Nombre de livraisons sortantes : ________________________________________________

Numéros de document : ________________________________________________________
```

---

## PDF page 250

```text
Chapitre 7
Solution 25

Création des livraisons sortantes via une
opération groupée

Bien que les commandes clients soient saisies individuellement, les documents liés
correspondants sont généralement créés par le biais d'une opération groupée. Ainsi,
plusieurs documents sont créés en une seule étape.

1. Lancez la création de livraisons sortantes avec référence à plusieurs commandes clients à
l'aide des informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Début de la semaine en cours jusqu'à la fin
de la semaine suivante

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Saisissez les critères de sélection et cliquez sur Lancer.

2. Pourquoi au moins une des commandes client que vous avez créées apparaît-elle deux
fois dans la liste ?

Parce que cette commande client se compose de deux postes ayant des réceptionnaires
différents. Des livraisons sortantes distinctes sont nécessaires pour livrer ces postes.

3. Vérifiez que vous avez sélectionné uniquement les documents qui sont traités par le point
d'expédition Z0##. Sélectionnez toutes les commandes clients et créez les livraisons
sortantes correspondantes.
a) Dans la liste, sélectionnez tous les documents.

b) Sélectionnez Créer livraisons.

4. Combien de livraisons sortantes ont été créées ? Notez les numéros des livraisons
sortantes créées.
Nombre de livraisons sortantes : ________________________________________________

Numéros de document : ________________________________________________________

a) Sélectionnez Afficher journal.
Les numéros des livraisons créées s’affichent.
```

---

## PDF page 251

```text
Sujet: Exécution d’opérations groupées

Opération groupée - Prélèvement
Pour effectuer le prélèvement SAP S/4HANA, des tâches magasin doivent être créées avec
référence à des ordres de livraisons sortantes dans SAP EWM. Les tâches magasin indiquent
les articles et les quantités à prélever correspondant aux quantités de livraison. Vous pouvez
imprimer la liste de prélèvement pour le magasinier à partir des données de la tâche magasin.
Cette étape peut être exécutée automatiquement.

Le prélèvement peut être confirmé automatiquement ou dans une étape de traitement
distincte. Si la confirmation automatique n'est pas utilisée, vous pouvez également suivre le
prélèvement en confirmant les quantités prélevées manuellement.

La figure « Opération groupée dans un prélèvement » illustre la création groupée des tâches
magasin.

Figure 86: Opération groupée dans un prélèvement

Une fois les tâches magasin confirmées, la sortie de marchandises peut être enregistrée en
conséquence.
```

---

## PDF page 252

```text
Chapitre 7 : Opération groupée
```

---

## PDF page 253

```text
Chapitre 7
Exercice 26

Achèvement des fonctions d'expédition via une
opération groupée

Vous souhaitez à présent exécuter le processus de prélèvement, puis enregistrer la sortie de
marchandises.

1. Créez les tâches magasin qui correspondent aux livraisons à vos clients. Utilisez les
critères suivants pour sélectionner les documents appropriés :

Nom de zone                             Valeur

Date/heure de départ de l'itinéraire        du premier jour de cette semaine à la fin de
la semaine prochaine

Destinataire                         T-S50A## et T-S50B##

2. Confirmez les tâches magasin et enregistrez la sortie de marchandises.
```

---

## PDF page 254

```text
Chapitre 7
Solution 26

Achèvement des fonctions d'expédition via une
opération groupée

Vous souhaitez à présent exécuter le processus de prélèvement, puis enregistrer la sortie de
marchandises.

1. Créez les tâches magasin qui correspondent aux livraisons à vos clients. Utilisez les
critères suivants pour sélectionner les documents appropriés :

Nom de zone                             Valeur

Date/heure de départ de l'itinéraire        du premier jour de cette semaine à la fin de
la semaine prochaine

Destinataire                         T-S50A## et T-S50B##

a) Dans la barre de lancement de SAP Fiori, lancez l'application Exécution du processus
de sortant.

b) Sélectionnez l'icône située à droite de la zone Date/heure de départ de l'itinéraire.

c) Sélectionnez Du(De)/Au(A) et gérez la période.

d) En haut à droite de l'écran, cliquez sur Adapter les filtres.

e) Dans la boîte de dialogue Filtre, sélectionnez Destinataire, puis cliquez sur OK.

f) Gérez les numéros de clients correspondants en plaçant le curseur sur la zone
Destinataire puis saisissez le premier numéro de client.

g) Dès que le numéro souhaité apparaît dans la liste, sélectionnez-le en cliquant dessus.

h) Procédez de même avec le deuxième numéro de client.

i) Pour lancer la sélection, cliquez sur Lancer.

j) Sélectionnez tous les ordres de livraisons sortantes dans la liste puis cliquez sur Créer
tâches.

2. Confirmez les tâches magasin et enregistrez la sortie de marchandises.
a) Dans la liste, sélectionnez le numéro du premier ordre de livraison sortante pour lequel
vous venez de créer des tâches magasin.

b) Sélectionnez Tâches en cours, sélectionnez tous les postes, puis cliquez sur Confirmer
tâches.

c) Lorsque la boîte de dialogue Confirmation s'affiche, cliquez sur OK.
```

---

## PDF page 255

```text
Sujet: Exécution d’opérations groupées

d) Sélectionnez Prélevé, sélectionnez tous les postes à nouveau, puis cliquez sur Sortie
de marchandises.

e) Répétez ces étapes pour les autres ordres de livraison sortante.
```

---

## PDF page 256

```text
Chapitre 7 : Opération groupée

Opération groupée - Documents de facturation
Pour accélérer le processus de création des documents de facturation, vous pouvez créer
plusieurs documents de facturation simultanément à l’aide de l'opération groupée.

L'opération groupée peut être effectuée comme suit :

●  Manuellement, par le biais d'une application appropriée (traitement en ligne)

●  Automatiquement, via un job d'arrière-plan (batch) aux heures creuses

Figure 87: Traitement de l'échéancier de factures

Options de facturation

Pour regrouper plusieurs postes des documents précédents (commandes client, livraisons),
les postes doivent posséder des caractéristiques communes spécifiques. Ces
caractéristiques sont, par exemple, la date de la facture, le payeur et les conditions de
paiement. La liste des caractéristiques communes est gérée dans le Customizing.

Selon ces caractéristiques, différents résultats de l'opération groupée sont possibles :

●  Ventilation de la facture :

Prenons le cas d'une commande client pour laquelle une livraison sortante a été créée. Si
certaines des caractéristiques mentionnées ci-dessus ne sont pas identiques dans les
postes précédents, plusieurs documents de facturation sont créés.

●  Document de facturation distinct pour chaque livraison sortante :

Vous disposez d'une commande client pour laquelle ont été créées deux livraisons
sortantes. Deux documents de facturation sont créés en référence à ces livraisons.

●  Facture groupée :

Vous disposez de deux commandes clients pour lesquelles ont été créées trois livraisons
sortantes (par exemple, autre réceptionnaire des marchandises ou livraison partielle). Un
seul document de facturation est créé avec référence aux livraisons sortantes.
```

---

## PDF page 257

```text
Sujet: Exécution d’opérations groupées

La figure « Options de facturation » montre les options les plus fréquemment utilisées pour la
création de documents de facturation via une opération groupée.

Figure 88: Options de facturation
```

---

## PDF page 258

```text
Chapitre 7 : Opération groupée
```

---

## PDF page 259

```text
Chapitre 7
Exercice 27

Création de documents de facturation à l'aide
d'une opération groupée

Vous voulez créer les documents de facturation avec référence aux livraisons sortantes
correspondantes.

1. Vous souhaitez créer des documents de facturation à l'aide d'une opération groupée.
Utilisez les critères suivants pour sélectionner les livraisons sortantes appropriées :

Nom de zone                             Valeur

Date de facture                       du premier jour de la semaine à J+2 semai-
nes

Org. commerciale                     1010

Point d'expédition                     Z0##

2. Dans la liste, sélectionnez les livraisons sortantes et simulez le résultat de l'opération
groupée.

3. Comparez deux documents pour savoir pourquoi les postes ne peuvent pas être
regroupés en un seul document.

Astuce :
Sélectionnez deux documents, puis Analyse ventilation.

4. Revenez à l'écran Traiter échéancier de factures et créez les documents de facturation à
l'aide d'une opération groupée.

5. Affichez le journal pour savoir combien de documents de facturation ont été créés. Notez
les numéros de document.
Nombre de documents de facturation : ___________

Notez les numéros des documents de facturation :

_________________ _________________ _________________

6. Dans l'un des documents de facturation créés, vérifiez si le processus de vente a pu
s'achever comme prévu. Utilisez le flux de documents du document de facturation pour
obtenir les informations souhaitées.
Le processus de vente est-il terminé ?

____________________________________________________________

Pourquoi ?
```

---

## PDF page 260

```text
Chapitre 7 : Opération groupée

____________________________________________________________

____________________________________________________________
```

---

## PDF page 261

```text
Chapitre 7
Solution 27

Création de documents de facturation à l'aide
d'une opération groupée

Vous voulez créer les documents de facturation avec référence aux livraisons sortantes
correspondantes.

1. Vous souhaitez créer des documents de facturation à l'aide d'une opération groupée.
Utilisez les critères suivants pour sélectionner les livraisons sortantes appropriées :

Nom de zone                             Valeur

Date de facture                       du premier jour de la semaine à J+2 semai-
nes

Org. commerciale                     1010

Point d'expédition                     Z0##

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de documents de
facturation (VF04).

b) Saisissez les critères de sélection répertoriés dans le tableau ci-dessus.

c) Pour lancer la sélection, en bas à droite de l'écran, sélectionnez Afficher l’échéancier
factures.

2. Dans la liste, sélectionnez les livraisons sortantes et simulez le résultat de l'opération
groupée.
a) Sélectionnez les livraisons appropriées.

b) En bas de l'écran, sélectionnez Simulation.

3. Comparez deux documents pour savoir pourquoi les postes ne peuvent pas être
regroupés en un seul document.

Astuce :
Sélectionnez deux documents, puis Analyse ventilation.

a) Sélectionnez deux pièces, puis Analyse ventilation.

b) Selon les documents, différents critères peuvent entraîner une ventilation de facture.
Par exemple :

●  Donneur d'ordre
```

---

## PDF page 262

```text
Chapitre 7 : Opération groupée

●  Payeur

●  Référence clt

●  Conditions de paiement

4. Revenez à l'écran Traiter échéancier de factures et créez les documents de facturation à
l'aide d'une opération groupée.
a) Cliquez sur Retour jusqu'à ce que vous obteniez l'écran Traiter échéancier de factures.

b) Sélectionnez tous les documents.

c) Pour créer les documents de facturation, sélectionnez Document de facturation
groupé.

5. Affichez le journal pour savoir combien de documents de facturation ont été créés. Notez
les numéros de document.
Nombre de documents de facturation : ___________

Notez les numéros des documents de facturation :

_________________ _________________ _________________

a) Dans l'écran Traiter échéancier de factures, en haut de l'écran, sélectionnez Affichage
du protocole.

b) Pour afficher les numéros des documents créés, sélectionnez la ligne contenant le
numéro de groupe correspondant puis cliquez sur Documents.

6. Dans l'un des documents de facturation créés, vérifiez si le processus de vente a pu
s'achever comme prévu. Utilisez le flux de documents du document de facturation pour
obtenir les informations souhaitées.
Le processus de vente est-il terminé ?

____________________________________________________________

Pourquoi ?

____________________________________________________________

____________________________________________________________

a) Sélectionnez une ligne dans le journal et, en haut de l'écran, sélectionnez Flux de
documents.
Le processus de vente est terminé car les pièces comptables (écritures au journal) ont
été créées automatiquement par le système. Le rapprochement des pièces
comptables fait partie du processus de comptabilité financière.
```

---

## PDF page 263

```text
Sujet: Exécution d’opérations groupées

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Exécution d’opérations groupées
```

---

## PDF page 264

```text
Chapitre 7 : Opération groupée
```

---

## PDF page 265

```text
Chapitre 7

Évaluation des connaissances

1.  Vous souhaitez créer des documents liés à vos commandes clients. Cette action peut
souvent être effectuée par opération groupée. Pour cela, sélectionnez tous les documents
pour lesquels vous voulez créer les documents liés, puis créez les documents liés.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Pour accélérer le processus de création des documents de facturation, vous pouvez créer
plusieurs documents de facturation simultanément via l'opération groupée.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

3. Outre l'efficacité et la rapidité, un avantage supplémentaire du traitement groupé est qu'il
détermine automatiquement si plusieurs documents de référence doivent entraîner moins
(ou plus) de documents liés.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 266

```text
Chapitre 7

Évaluation des connaissances - Réponses

1.  Vous souhaitez créer des documents liés à vos commandes clients. Cette action peut
souvent être effectuée par opération groupée. Pour cela, sélectionnez tous les documents
pour lesquels vous voulez créer les documents liés, puis créez les documents liés.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Vous souhaitez créer des documents liés à vos commandes clients. Cette action
peut souvent être effectuée par une opération groupée. La procédure est très similaire,
quel que soit le type de document que vous voulez créer : commencez par sélectionner
tous les documents pour lesquels vous voulez créer les documents liés correspondants.
Vous créez ensuite les documents liés.

2. Pour accélérer le processus de création des documents de facturation, vous pouvez créer
plusieurs documents de facturation simultanément via l'opération groupée.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Pour accélérer le processus de création des documents de facturation, vous
pouvez créer plusieurs documents de facturation simultanément via l'opération groupée.

3. Outre l'efficacité et la rapidité, un avantage supplémentaire du traitement groupé est qu'il
détermine automatiquement si plusieurs documents de référence doivent entraîner moins
(ou plus) de documents liés.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Par exemple, la création groupée de livraisons permet de regrouper plusieurs
commandes client en une seule livraison sortante, à condition que le client l'ait demandée
et que les informations clés de livraison (date de livraison, point d'expédition,
réceptionnaire des marchandises, etc.) soient cohérentes. Si plusieurs postes d'une
commande client ont, par exemple, des adresses de livraison différentes (réceptionnaires
des marchandises), la création groupée de livraisons fractionne automatiquement cette
commande en plusieurs livraisons sortantes.
```

---

## PDF page 267

```text
CHAPITRE 8  Processus supplémentaires
dans les ventes

Sujet 1

Utilisation de documents d'avant-vente                                              258
Exercice 28 : Création de documents d'avant-vente                              261
Exercice 29 : Description du traitement des documents d'avant-vente              267

Sujet 2

Exécution de la fabrication sur commande                                            270
Exercice 30 : Exécution de la fabrication sur commande                         273

Sujet 3

Vente de produits de service                                                       282
Exercice 31 : Vente d’un produit de service                                  283

OBJECTIFS DU CHAPITRE

●   Utilisation des documents d’avant-vente

●  Exécution de la fabrication sur commande

●  Vendre des produits de service
```

---

## PDF page 268

```text
Chapitre 8
Sujet 1

Utilisation de documents d'avant-vente

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●   Utilisation des documents d’avant-vente

Gestion de l'avant-vente
Selon votre branche, votre société peut exécuter des activités différentes avant de sécuriser
les commandes de vos clients. La société peut planifier et réaliser des campagnes de
marketing ou participer à des foires. Vos commerciaux peuvent également rendre visite aux
clients pour présenter vos derniers produits et en discuter.

La liste des activités d'avant-vente possibles étant très longue, la figure « Tâches de support
vente » ne représente que les plus courantes.

Figure 89: Tâches de support vente

Documents d'avant-vente
Concernant les documents dans SAP S/4HANA, il existe deux catégories principales de
document de vente relatives à la partie avant-vente du processus de vente :

●  Demandes
```

---

## PDF page 269

```text
Sujet: Utilisation de documents d'avant-vente

●  Offres

Vous recevez des demandes de vos clients, par exemple sur des prix d'article ou des dates de
livraison. En fonction de ces demandes, vous pouvez créer les offres correspondantes pour
fournir aux clients les informations dont ils ont besoin. Toutefois, lors de la création d'offres,
les références aux demandes sont facultatives et les offres peuvent également être créées à
partir de zéro.

Remarque :
L'utilisation de demandes et d'offres n'est pas obligatoire pour le processus de
vente.

La figure « Documents d’avant-vente » illustre le concept des demandes d'offre et des offres.

Figure 90: Documents d'avant-vente

Flux de documents dans la phase avant-vente

La gestion des statuts est un aspect important de la gestion de l'avant-vente. Par exemple, il
est possible que vous ne soyez pas en mesure de fournir la quantité totale d'une demande à la
date demandée par le client. Ou alors, le client peut décider de s'adresser à un autre
fournisseur parce que le prix proposé dans votre offre ne lui convient pas. Dans les deux cas
les documents d’avant-vente restent ouverts dans votre système.

Plusieurs options permettent de résoudre cette situation. Il est possible, par exemple,
d'utiliser les options standard du Customizing pour liquider les postes de demande au
premier référencement. Pour les offres, l'utilisation d'un motif de refus est un moyen courant
de définir sur « Liquidé » le statut d'un poste.

Astuce :
Lorsque vous utilisez un motif de refus (par exemple, « Trop cher » ou « Date de
livraison trop lointaine »), vous stockez également dans le système des
informations intéressantes susceptibles d'être utilisées dans l'analyse des ventes
et d'influencer vos stratégies de vente dans le futur.
```

---

## PDF page 270

```text
Chapitre 8 : Processus supplémentaires dans les ventes

La figure « Flux de documents dans la phase avant-vente » illustre le flux de documents
possible dans la phase avant-vente.

Figure 91: Flux de documents dans la phase avant-vente
```

---

## PDF page 271

```text
Chapitre 8
Exercice 28

Création de documents d'avant-vente

Vous recevez une demande d'un client et vous créez le document correspondant. Vous créez
une offre en fonction de cette demande. Pour compléter le processus, vous créez une
commande client avec référence à l'offre.

1. Créez une demande d'offre sur la base des informations suivantes :

Nom de zone                             Valeur

Type de demande d'offre                DO

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

DateLivrSouh.                          Date du jour + 3 semaines

Article                             T-MS2##

Quantité                            3 pièces

Vous souhaitez que la demande d'offre client soit traitée d'ici la fin de la semaine.

Astuce :
Lors de la création de la demande d'offre, vous pouvez utiliser la zone Fin de
validité pour gérer un délai de traitement.

2. Sauvegardez la demande d'offre et notez le numéro du document.
___________________________________

3. Étant donné qu'il existe actuellement une demande importante pour l'article demandé,
vous ne voulez proposer au client que deux pièces. L'offre doit être valable à partir
d'aujourd'hui jusqu'à la fin de la semaine prochaine. Créez l'offre avec référence à la
demande à l'aide des informations suivantes :

Nom de zone                             Valeur

Type d'offre                         OF

Organisation commerciale              1010

Canal distribution                     10
```

---

## PDF page 272

```text
Chapitre 8 : Processus supplémentaires dans les ventes

Nom de zone                             Valeur

Secteur d'activité                     00

4. Sauvegardez l'offre et notez son numéro.
___________________________________

5. Le client commande à présent l'article proposé dans l'offre. Créez la commande client
correspondante avec référence à l'offre à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Réf. client                           8-9##

DateLivrSouh.                         dans 3 semaines

Article                             T-MS2##

Quantité d'ordre                      1 pièce

6. Sauvegardez la commande client et notez le numéro de document.
___________________________________

7. Quel est le statut de référence du poste dans la demande d’offre ?
__________________________________________________

8. Quel est le statut de référence du poste dans l’offre ?
__________________________________________________
```

---

## PDF page 273

```text
Chapitre 8
Solution 28

Création de documents d'avant-vente

Vous recevez une demande d'un client et vous créez le document correspondant. Vous créez
une offre en fonction de cette demande. Pour compléter le processus, vous créez une
commande client avec référence à l'offre.

1. Créez une demande d'offre sur la base des informations suivantes :

Nom de zone                             Valeur

Type de demande d'offre                DO

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

DateLivrSouh.                          Date du jour + 3 semaines

Article                             T-MS2##

Quantité                            3 pièces

Vous souhaitez que la demande d'offre client soit traitée d'ici la fin de la semaine.

Astuce :
Lors de la création de la demande d'offre, vous pouvez utiliser la zone Fin de
validité pour gérer un délai de traitement.

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des demandes
client.

b) Sélectionnez Créer demande.

c) Dans l'écran initial, saisissez le type de demande d'offre et les entités
organisationnelles.

d) Pour appeler les détails du document, appuyez sur Entrée.

e) Saisissez les données indiquées dans le tableau ci-dessus. N'oubliez pas de saisir la
date de fin de validité.

2. Sauvegardez la demande d'offre et notez le numéro du document.
___________________________________

a) Dans la demande d'offre, sélectionnez Sauvegarder.
```

---

## PDF page 274

```text
Chapitre 8 : Processus supplémentaires dans les ventes

3. Étant donné qu'il existe actuellement une demande importante pour l'article demandé,
vous ne voulez proposer au client que deux pièces. L'offre doit être valable à partir
d'aujourd'hui jusqu'à la fin de la semaine prochaine. Créez l'offre avec référence à la
demande à l'aide des informations suivantes :

Nom de zone                             Valeur

Type d'offre                         OF

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des offres client.

b) Sélectionnez Créer offre.

c) Dans l'écran initial, saisissez le type de d’offre et les entités organisationnelles.

d) Cliquez sur Créer avec référence.

e) Dans la boîte de dialogue Créer avec référence, saisissez le numéro de la demande
d'offre et cliquez sur Copier.

f) Dans l'offre, remplacez la quantité par deux pièces et gérez la date de fin de validité.

4. Sauvegardez l'offre et notez son numéro.
___________________________________

a) Dans l'offre, cliquez sur Sauvegarder.
Le numéro de document s'affiche.

5. Le client commande à présent l'article proposé dans l'offre. Créez la commande client
correspondante avec référence à l'offre à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Réf. client                           8-9##

DateLivrSouh.                         dans 3 semaines

Article                             T-MS2##

Quantité d'ordre                      1 pièce

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des commandes
clients.

b) Sélectionnez Créer commande client - VA01.
```

---

## PDF page 275

```text
Sujet: Utilisation de documents d'avant-vente

c) Dans l’écran initial, saisissez le type de commande et les données d’organisation.

d) Cliquez sur Créer avec référence.

e) Dans la boîte de dialogue Créer avec référence, saisissez le numéro de l'offre, puis
cliquez sur Copier.

f) Gérez les informations pertinentes et modifiez la quantité de l'article en une seule
pièce.

6. Sauvegardez la commande client et notez le numéro de document.
___________________________________

a) Dans la commande client, sélectionnez Sauvegarder.

7. Quel est le statut de référence du poste dans la demande d’offre ?
__________________________________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des demandes
client.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Dans l'écran Gestion des demandes client, saisissez le numéro de votre demande
d'offre et sélectionnez Lancer.

d) Sélectionnez la ligne qui contient votre demande d'offre pour accéder aux détails du
document.

e) En haut de l’écran, cliquez sur Synthèse des statuts.

f) Sélectionnez le poste et cliquez sur Développer tout.
Le statut de référence du poste de la demande d'offre indique qu'elle est Totalement
référencée, même si seulement deux des trois pièces ont été copiées de la demande
d'offre dans l'offre. Dans le paramétrage système standard, un poste de demande
d'offre est marqué comme complètement référencé dès qu'au moins une quantité
partielle du poste est copiée dans une offre.

8. Quel est le statut de référence du poste dans l’offre ?
__________________________________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des offres client.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Dans l'écran Gestion des offres client, saisissez le numéro de votre offre et
sélectionnez Lancer.

d) Sélectionnez la ligne contenant votre offre.

e) En haut de l’écran, cliquez sur Synthèse des statuts.

f) Sélectionnez le poste, puis Développer tout.
Le statut de référence de l'offre indique que celle-ci est Partiellement référencée,
puisque seule une des deux unités de l'offre a été copiée dans la commande client.
Dans le paramétrage système standard, un poste d'offre est marqué comme
complètement référencé uniquement si la quantité totale a été copiée.
```

---

## PDF page 276

```text
Chapitre 8 : Processus supplémentaires dans les ventes
```

---

## PDF page 277

```text
Chapitre 8
Exercice 29

Description du traitement des documents
d'avant-vente

Répondez aux questions suivantes concernant les documents d'avant-vente.

1. Indiquez certaines des différences existant entre une demande et une offre.

2. Une demande d'offre doit-elle être enregistrée avant de pouvoir créer une offre ?

3. La détermination automatique du prix a-t-elle lieu pendant la saisie d'offres ou de
demandes d'offres client ?

4. Pouvez-vous effectuer le contrôle de disponibilité dans une demande d'offre ou une offre
client comme dans une commande client ?
```

---

## PDF page 278

```text
Chapitre 8
Solution 29

Description du traitement des documents
d'avant-vente

Répondez aux questions suivantes concernant les documents d'avant-vente.

1. Indiquez certaines des différences existant entre une demande et une offre.

Les demandes sont des demandes de clients concernant les conditions d’un article (prix,
date de livraison, etc.). Vous devez fournir les informations correspondantes à votre client
en utilisant des offres. Pour les demandes d'offres, la date de validité est utilisée dans le
système comme délai de traitement de la réponse à la demande. Les offres client ont
force d'obligation pendant la période de validité du client.

2. Une demande d'offre doit-elle être enregistrée avant de pouvoir créer une offre ?

Non. Il est possible de créer des offres client sans référence à une demande.

3. La détermination automatique du prix a-t-elle lieu pendant la saisie d'offres ou de
demandes d'offres client ?

Oui. La détermination automatique du prix a lieu (selon le Customizing) lors de la création
de demandes d'offres et d'offres client.

4. Pouvez-vous effectuer le contrôle de disponibilité dans une demande d'offre ou une offre
client comme dans une commande client ?

Oui. Un contrôle de disponibilité peut être effectué lors de la saisie de demande d'offre
client et d'offre client, de même que pendant la saisie de commande client (selon le
Customizing).
```

---

## PDF page 279

```text
Sujet: Utilisation de documents d'avant-vente

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●   Utilisation des documents d’avant-vente
```

---

## PDF page 280

```text
Chapitre 8
Sujet 2

Exécution de la fabrication sur commande

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Exécution de la fabrication sur commande

Flux du processus de fabrication sur commande
La fabrication sur commande se caractérise par le fait que les articles ne sont pas simplement
stockés dans le magasin en attendant d’être vendus, mais qu'ils sont fabriqués exclusivement
pour satisfaire une commande client spécifique. Un besoin indépendant client est généré à
partir du poste de commande client et transféré à la planification des besoins.

L'article peut à présent être fabriqué, et l'entrée de marchandises correspondant au stock
propre à la commande client peut être enregistrée. Dès que la livraison est arrivée à
échéance, l'article peut être livré et la sortie de marchandises enregistrée (ce qui réduit le
stock de la commande client).

La figure « Flux du processus de fabrication sur commande » illustre le flux du même nom.

Figure 92: Flux du processus de fabrication sur commande
```

---

## PDF page 281

```text
Sujet: Exécution de la fabrication sur commande

De la commande client à l'ordre de fabrication

Dans le cadre d'un processus standard de fabrication sur commande, la quantité appropriée
et la date de mise à disposition de l'article sont transférées depuis la commande client à la
planification des besoins en tant que besoin indépendant client.

Une exécution de la planification des besoins en articles (MRP) peut à présent générer
automatiquement un ordre planifié pour l'article et aussi déterminer les besoins dépendants
correspondants à partir de la nomenclature appropriée. En outre, des ordres planifiés
peuvent être créés sur la base de ces besoins dépendants.

Dès que vous êtes prêt à lancer la fabrication, vous créez un ordre de fabrication pour le
produit final en convertissant l'ordre planifié. Le système transfère la quantité confirmée et la
date de mise à disposition de l'article de l'ordre de fabrication à la commande client.

Figure 93: De la commande client à l'ordre de fabrication

Pure fabrication sur commande - Exemple

Le calcul des besoins nets est exécuté individuellement pour chaque commande client et le
stock ne peut pas être permuté entre les commandes. Les ordres planifiés sont créés avec
référence aux commandes clients et sont gérés dans le segment client. Cette référence
directe à une commande client est également conservée dans l'ordre de fabrication.

La réduction des besoins (commande client) et la réduction du stock de fabrication sur
commande ont lieu à la livraison.

La figure « Pure fabrication sur commande - Exemple » montre le traitement individuel des
besoins depuis différentes commandes clients.
```

---

## PDF page 282

```text
Chapitre 8 : Processus supplémentaires dans les ventes

Figure 94: Pure fabrication sur commande - Exemple
```

---

## PDF page 283

```text
Chapitre 8
Exercice 30

Exécution de la fabrication sur commande

Votre client commande un article qui doit être fourni par un processus de fabrication sur
commande. Les données de base nécessaires à la fabrication (nomenclature, gamme) ont
déjà été créées.

1. Avant que le processus ne commence, vérifiez si le groupe de stratégies dans la fiche
article est déjà défini sur 20. Si ce n'est pas le cas, modifiez le groupe de stratégies en
conséquence. Utilisez les informations suivantes :

Nom de zone                             Valeur

Article                             T-F1##

Division                            1010

Le groupe de stratégies se trouve dans la vue Planification des besoins 3.

2. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           8-9##

DateLivrSouh.                         dans 2 semaines

Article                             T-F1##

Quantité d'ordre                      10

3. Sauvegardez la commande client et notez son numéro.
________________________________________

4. À présent, vérifiez la couverture article de l'article pour la division 1010 à l'aide de
l'application correspondante. Les besoins en articles de la commande client sont-ils
couverts ?
________________________________________

5. Planifiez un cycle MRP et utilisez les informations suivantes :
```

---

## PDF page 284

```text
Chapitre 8 : Processus supplémentaires dans les ventes

Nom de zone                             Valeur

Nom du job                          Groupe de planification ##

Division                            1010

Article                             T-F1##

Lancer immédiatement.                    Sélectionné

Composants nomenclature modif:.          Sélectionné

6. Vérifiez à nouveau la couverture article. Comment la situation a-t-elle évolué ?
________________________________________

________________________________________

7. À présent, convertissez l’ordre planifié en ordre de fabrication. Utilisez le numéro d’article
T-F1## et la division de planification 1010 comme critères de sélection.

8. Notez le numéro de l'ordre de fabrication.
________________________________________

9. Vous voulez examiner de plus près l'ordre de fabrication. Le numéro de la commande
client d'origine peut-il y être trouvé ?
________________________________________

10. Lancez l'ordre de fabrication et sauvegardez le document.

11. Enregistrez l'entrée de marchandises pour l’ordre de fabrication.

12. Effectuez un dernier contrôle de la couverture article. Comment la situation a-t-elle
évolué ?
________________________________________

________________________________________

13. Pour poursuivre le processus, créez la livraison sortante avec référence à la commande
client et notez le numéro du document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     1010

Date de création planifiée                 Date du jour + 3 semaines

_______________________________________________

14. Prélevez la livraison sortante et enregistrez la sortie de marchandises.

Remarque :
Vous exécutez maintenant le processus de livraison sans EWM. Étant donné
que cette fois l'article doit être prélevé dans un magasin standard, veuillez
utiliser l'application Prélèvement de livraison sortante.
```

---

## PDF page 285

```text
Sujet: Exécution de la fabrication sur commande

15. Pour finir, revérifiez la couverture article. Les besoins en articles sont-ils toujours
valables ?
___________________________
```

---

## PDF page 286

```text
Chapitre 8
Solution 30

Exécution de la fabrication sur commande

Votre client commande un article qui doit être fourni par un processus de fabrication sur
commande. Les données de base nécessaires à la fabrication (nomenclature, gamme) ont
déjà été créées.

1. Avant que le processus ne commence, vérifiez si le groupe de stratégies dans la fiche
article est déjà défini sur 20. Si ce n'est pas le cas, modifiez le groupe de stratégies en
conséquence. Utilisez les informations suivantes :

Nom de zone                             Valeur

Article                             T-F1##

Division                            1010

Le groupe de stratégies se trouve dans la vue Planification des besoins 3.

a) Dans la barre de lancement SAP Fiori, lancez l'application Modification d’article.

b) Saisissez le numéro d'article et appuyez sur Entrée.

c) Sélectionnez la vue Planification des besoins 3, puis appuyez sur Entrée.

d) Sélectionnez Niveaux organisation, saisissez la division 1010 et appuyez à nouveau sur
Entrée.

e) Vérifiez le groupe de stratégies. S'il n'est pas encore défini sur 20, modifiez-le en
conséquence.
Saisissez 20 comme Groupe de stratégies.

f) En bas à droite de l’écran, cliquez sur Sauvegarder.

2. Créez une commande client sur la base des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           8-9##

DateLivrSouh.                         dans 2 semaines

Article                             T-F1##
```

---

## PDF page 287

```text
Sujet: Exécution de la fabrication sur commande

Nom de zone                             Valeur

Quantité d'ordre                      10

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l’écran initial, saisissez le type de commande et les données d’organisation.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Dans l'écran de synthèse, saisissez les informations correspondantes.

3. Sauvegardez la commande client et notez son numéro.
________________________________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document s'affiche.

4. À présent, vérifiez la couverture article de l'article pour la division 1010 à l'aide de
l'application correspondante. Les besoins en articles de la commande client sont-ils
couverts ?
________________________________________

a) Depuis la barre de lancement SAP Fiori, lancez l’application Contrôle de la couverture
article dans le groupe de vignettes Material Availability.

b) Dans la boîte de dialogue Rechercher article, saisissez le numéro d'article et
sélectionnez la division appropriée.

c) Pour accéder aux détails, cliquez sur OK.
Les besoins en articles de 10 pièces ne sont pas couverts pour le moment.

5. Planifiez un cycle MRP et utilisez les informations suivantes :

Nom de zone                             Valeur

Nom du job                          Groupe de planification ##

Division                            1010

Article                             T-F1##

Lancer immédiatement.                    Sélectionné

Composants nomenclature modif:.          Sélectionné

a) Depuis la barre de lancement SAP Fiori, lancez l’application Ordonnancement des
cycles MRP dans le groupe de vignettes Material Availability.

b) Pour créer un job, sélectionnez Créer.

c) Saisissez le nom du job et sélectionnez Étape 2.

d) Assurez-vous que le paramètre Lancer immédiatement est sélectionné et sélectionnez
Étape 3.
```

---

## PDF page 288

```text
Chapitre 8 : Processus supplémentaires dans les ventes

e) Saisissez la division et l'article, puis sélectionnez le code Composants nomenclature
modif. Cliquez sur Planifier.

f) Continuez à sélectionner Lancer jusqu'à ce que le statut de votre cycle MRP soit
Terminé.

6. Vérifiez à nouveau la couverture article. Comment la situation a-t-elle évolué ?
________________________________________

________________________________________

a) Lancez de nouveau l’application Contrôle de la couverture article avec votre article et la
division 1010.

b) Dans l'écran Gestion de la couverture articles, sélectionnez la catégorie de stock pour
commande client dans la colonne Articles (à gauche de l'écran). Elle est identifiée
StkCliXXXX-YY (où XXXX = le numéro de commande client et YY = le poste de
commande).

c) Un ordre planifié a été créé par le cycle MRP pour couvrir les besoins en articles.

7. À présent, convertissez l’ordre planifié en ordre de fabrication. Utilisez le numéro d’article
T-F1## et la division de planification 1010 comme critères de sélection.
a) Dans l'application Contrôle de la couverture article, dans la ligne contenant le nouvel
ordre planifié, ouvrez les options à droite de Traiter et sélectionnez Convertir.

b) Dans la boîte de dialogue, sélectionnez OK.

8. Notez le numéro de l'ordre de fabrication.
________________________________________

a) Dans l'application Contrôle de la couverture article, le numéro de document de l'ordre
de fabrication est maintenant affiché.

9. Vous voulez examiner de plus près l'ordre de fabrication. Le numéro de la commande
client d'origine peut-il y être trouvé ?
________________________________________

a) Dans l'application Contrôle de la couverture article, sélectionnez le numéro de l'ordre
de fabrication.

b) Les informations pertinentes (ordre de fabrication) sont affichées dans une fenêtre
pop-up. Vous devrez peut-être faire défiler vers le bas pour les voir.

10. Lancez l'ordre de fabrication et sauvegardez le document.
a) En bas à droite de la boîte de dialogue, cliquez sur Ouvrir puis sur Ordre de fabrication
pour naviguer vers le document correspondant.

b) Sélectionnez Menu → Ordre → Modifier.

c) Appuyez sur Entrée pour accéder au mode de modification de l'ordre de fabrication.

d) En haut de l'écran, cliquez sur Lancer ordre.

e) Si la boîte de dialogue Lancer ordre s'affiche, sélectionnez Lancer ordre.

f) Cliquez sur Sauvegarder.

11. Enregistrez l'entrée de marchandises pour l’ordre de fabrication.
```

---

## PDF page 289

```text
Sujet: Exécution de la fabrication sur commande

a) Depuis la barre de lancement SAP Fiori, lancez l’application Enregistrement de
mouvement de stock dans le groupe de vignettes Production.

b) Dans la liste déroulante en haut de l'écran, sélectionnez Entrée de marchandises et
Ordre.

c) Saisissez le numéro de l'ordre de fabrication dans la zone correspondante et appuyez
sur Entrée.

d) Marquez le poste comme OK en cochant la case correspondante et, en bas à droite de
l'écran, cliquez sur Enregistrer.

12. Effectuez un dernier contrôle de la couverture article. Comment la situation a-t-elle
évolué ?
________________________________________

________________________________________

a) Lancez de nouveau l’application Contrôle de la couverture article avec votre article et la
division 1010.
L'ordre de fabrication a disparu de la liste. Une quantité en stock de 10 pièces est
désormais disponible.

13. Pour poursuivre le processus, créez la livraison sortante avec référence à la commande
client et notez le numéro du document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Point d'expédition                     1010

Date de création planifiée                 Date du jour + 3 semaines

_______________________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Saisissez le point d'expédition et sélectionnez Au dans la zone Date de création
planifiée.

d) Sélectionnez la date correcte en utilisant la fonction de calendrier.

e) Cliquez sur Lancer.

f) Sélectionnez la ligne contenant le numéro de votre commande client, puis cliquez sur
Créer livraisons.

g) Sélectionnez Afficher journal.

14. Prélevez la livraison sortante et enregistrez la sortie de marchandises.

Remarque :
Vous exécutez maintenant le processus de livraison sans EWM. Étant donné
que cette fois l'article doit être prélevé dans un magasin standard, veuillez
utiliser l'application Prélèvement de livraison sortante.
```

---

## PDF page 290

```text
Chapitre 8 : Processus supplémentaires dans les ventes

a) Dans la barre de lancement SAP Fiori, lancez l'application Prélèvement de livraison
sortante.

b) Saisissez le numéro de la livraison sortante et appuyez sur Entrée.

c) Dans la zone Quantité prélevée, remplacez la quantité par 10.

d) En bas à droite de l’écran, cliquez sur Sauvegarder.

e) À présent, vous pouvez enregistrer la sortie de marchandises en sélectionnant
Enregistrer sortie de marchandises.

15. Pour finir, revérifiez la couverture article. Les besoins en articles sont-ils toujours
valables ?
___________________________

a) Lancez de nouveau l’application Contrôle de la couverture article avec votre article et la
division 1010.
Les besoins en articles ont été satisfaits et ne figurent donc plus dans la liste.
```

---

## PDF page 291

```text
Sujet: Exécution de la fabrication sur commande

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Exécution de la fabrication sur commande
```

---

## PDF page 292

```text
Chapitre 8
Sujet 3

Vente de produits de service

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Vendre des produits de service

Produits de service
Si vous souhaitez vendre des services, vous devez d'abord gérer les fiches articles
correspondant à vos services. Cependant, vous avez à gérer uniquement les données
pertinentes pour les ventes. Les informations sur le stockage, par exemple, ne sont pas
nécessaires pour les produits de service.

Le type d'article DIEN s'applique aux produits de service et implique moins de données à
gérer. Il inclut, entre autres, le groupe de types de poste LEIS. À partir de ce groupe de types
de poste, le système peut déterminer les types de poste appropriés aux produits de service
dans les documents de vente.

Figure 95: Produits de service

Lorsque vous vendez des services (par exemple, des services de conseil), il est inutile
d'exécuter les fonctions d'expédition au cours du processus. Les postes de service des
commandes client peuvent être facturés directement ; le document de facturation
correspondant est créé directement avec référence à la commande client.
```

---

## PDF page 293

```text
Chapitre 8
Exercice 31

Vente d’un produit de service

Les commandes client permettent également de vendre des services. Pour tester ce type de
processus, examinez un produit de service et utilisez-le dans le processus de vente.

1. Affichez la fiche article du produit de service T-D1## à l'aide des informations suivantes :

Nom de zone                             Valeur

Division                            1010

Organisation commerciale              1010

Canal distribution                     10

Remarque :
Sélectionnez les vues Données de base 1, ADV : Données org. commerciale 1 +
2 et ADV : Données générales/division.

2. Quel type d'article a été utilisé pour cet article ?
_____________________________

3. Quel groupe de types de poste a été affecté au produit de service ?
_____________________________

4. Pour vendre le produit de service, créez une commande client à l'aide des informations
suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Référence client                      8-6##

Article                             T-D1##

Quantité d'ordre                      3 heures

5. Quel type a été déterminé pour le poste ?
_____________________________
```

---

## PDF page 294

```text
Chapitre 8 : Processus supplémentaires dans les ventes

6. Sauvegardez la commande client et notez le numéro de document.
_____________________________

7. Pour terminer le processus, créez la facture avec référence à la commande client. Utilisez
votre client comme critère de sélection et aujourd'hui + 14 jours en tant que valeur pour la
zone Date de la facture jusqu'au. Notez le numéro du document.
_____________________________
```

---

## PDF page 295

```text
Chapitre 8
Solution 31

Vente d’un produit de service

Les commandes client permettent également de vendre des services. Pour tester ce type de
processus, examinez un produit de service et utilisez-le dans le processus de vente.

1. Affichez la fiche article du produit de service T-D1## à l'aide des informations suivantes :

Nom de zone                             Valeur

Division                            1010

Organisation commerciale              1010

Canal distribution                     10

Remarque :
Sélectionnez les vues Données de base 1, ADV : Données org. commerciale 1 +
2 et ADV : Données générales/division.

a) Depuis la barre de lancement SAP Fiori, lancez l'application Affichage d’article.

b) Dans l'écran initial de la transaction, saisissez le numéro d'article et sélectionnez
Entrée.

c) Sélectionnez les vues pertinentes, puis appuyez sur Entrée.

d) Saisissez les entités organisationnelles pertinentes et sélectionnez Entrée.

2. Quel type d'article a été utilisé pour cet article ?
_____________________________

a) Dans la page à onglet Données de base 1, sélectionnez le bouton Informations sur
l'article.
Le type d'article DIEN s’affiche dans la fenêtre pop-up.

3. Quel groupe de types de poste a été affecté au produit de service ?
_____________________________

a) Sélectionnez la page à onglet ADV : Données org. commerciale 2.
Le groupe de types de poste LEIS a été affecté à l'article.

4. Pour vendre le produit de service, créez une commande client à l'aide des informations
suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010
```

---

## PDF page 296

```text
Chapitre 8 : Processus supplémentaires dans les ventes

Nom de zone                             Valeur

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Référence client                      8-6##

Article                             T-D1##

Quantité d'ordre                      3 heures

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de l'application, saisissez le type de commande et les entités
organisationnelles, puis sélectionnez Entrée.

c) Saisissez les informations pertinentes répertoriées dans le tableau.

5. Quel type a été déterminé pour le poste ?
_____________________________

a) Pour appeler les détails du poste, double-cliquez sur le poste.

b) Le type de poste TAD a été déterminé par le système, comme indiqué dans la partie
supérieure de l'écran.

6. Sauvegardez la commande client et notez le numéro de document.
_____________________________

a) Dans la commande client, sélectionnez Sauvegarder.

7. Pour terminer le processus, créez la facture avec référence à la commande client. Utilisez
votre client comme critère de sélection et aujourd'hui + 14 jours en tant que valeur pour la
zone Date de la facture jusqu'au. Notez le numéro du document.
_____________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de documents
de facturation.

b) Saisissez votre client dans la zone Donneur d'ordre, puis gérez l’entrée pour les Date
de la facture jusqu'au. Cliquez sur Lancer.

c) Dans la liste, sélectionnez la ligne contenant le numéro de votre commande client.

d) Sélectionnez Créer documents de facturation.
Les détails de la facture sont affichés à l'écran.

e) Pour terminer le processus, cliquez sur Sauvegarder.
```

---

## PDF page 297

```text
Sujet: Vente de produits de service

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Vendre des produits de service
```

---

## PDF page 298

```text
Chapitre 8 : Processus supplémentaires dans les ventes
```

---

## PDF page 299

```text
Chapitre 8

Évaluation des connaissances

1.  Concernant les documents d'avant-vente dans SAP S/4HANA, l'utilisation des demandes
et des offres est obligatoire pour le processus de vente.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2.  Identifiez la séquence correcte pour le flux du processus de fabrication sur commande, de
la commande client à l'ordre de fabrication.

Classez dans l'ordre

0 La planification des besoins en composants (MRP) génère automatiquement un ordre
planifié pour l'article.

0 Une demande client individuelle est générée à partir de la commande client.

0 Un ordre de fabrication est créé pour le produit final en convertissant l'ordre planifié.

0 Une demande client individuelle est transférée à la planification des besoins.

0 Le système transfère la quantité confirmée et la date de mise à disposition de l'article
de l'ordre de fabrication à la commande client.

3. Le type d'article DIEN s'applique aux produits de service et implique moins de données à
gérer.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 300

```text
Chapitre 8

Évaluation des connaissances - Réponses

1.  Concernant les documents d'avant-vente dans SAP S/4HANA, l'utilisation des demandes
et des offres est obligatoire pour le processus de vente.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. L'utilisation de demandes et d'offres n'est pas obligatoire pour le processus de
vente.

2.  Identifiez la séquence correcte pour le flux du processus de fabrication sur commande, de
la commande client à l'ordre de fabrication.

Classez dans l'ordre

3 La planification des besoins en composants (MRP) génère automatiquement un ordre
planifié pour l'article.

1 Une demande client individuelle est générée à partir de la commande client.

4 Un ordre de fabrication est créé pour le produit final en convertissant l'ordre planifié.

2 Une demande client individuelle est transférée à la planification des besoins.

5 Le système transfère la quantité confirmée et la date de mise à disposition de l'article
de l'ordre de fabrication à la commande client.

Correct. La séquence correcte est : 1. Un besoin indépendant client est généré à partir de
la commande client. 2. Un besoin individuel client est transféré à la planification des
besoins. 3. La planification des besoins en composants (MRP) génère automatiquement
un ordre planifié pour l'article. 4. Un ordre de fabrication pour le produit fini est créé en
convertissant l'ordre planifié. 5. Le système transfère la quantité confirmée et la date de
mise à disposition de l'article de l'ordre de fabrication vers la commande client.
```

---

## PDF page 301

```text
Chapitre 8 : Évaluation des connaissances - Réponses

3. Le type d'article DIEN s'applique aux produits de service et implique moins de données à
gérer.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Le type d'article DIEN s'applique aux produits de service et implique moins de
données à gérer. Il inclut, entre autres, le groupe de types de poste LEIS.
```

---

## PDF page 302

```text
Chapitre 8 : Évaluation des connaissances - Réponses
```

---

## PDF page 303

```text
CHAPITRE 9  Gestion des réclamations

Sujet 1

Création de demandes d'avoir                                                     294
Exercice 32 : Création d’une demande d'avoir                                299

Sujet 2

Annulation de documents de facturation                                            306
Exercice 33 : Annulation d’un document de facturation                         307

Sujet 3

Création de retours                                                                 310
Exercice 34 : Création d’un retour                                             313

OBJECTIFS DU CHAPITRE

●  Créer des demandes d'avoir

●  Annulation des documents de facturation

●  Création des retours
```

---

## PDF page 304

```text
Chapitre 9
Sujet 1

Création de demandes d'avoir

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Créer des demandes d'avoir

Gestion des réclamations
Des problèmes peuvent survenir au cours des différentes étapes dans les processus
d'administration des ventes. Par exemple, un article livré peut avoir été endommagé pendant
son transport ou les prix figurant sur une facture peuvent être erronés.

Pour traiter ces problèmes, vous pouvez utiliser certains types de document standard liés à la
gestion des réclamations. Les types de document les plus importants sont les suivants :

●  Demande d'avoir/de note de débit

Permet de créditer/débiter un montant à un client.

●  Retours

permettent au client de retourner des marchandises.

Dans un grand nombre de cas, vous créez les documents avec référence à un processus
existant. Ainsi, vous disposez toujours d'un flux de documents complet du processus, y
compris tous les documents de réclamation applicables. Il est également possible de copier
une grande partie des informations nécessaires à partir du document de référence, ce qui
accélère la gestion des réclamations.

La figure « Processus de gestion des réclamations » illustre les différentes options se
rapportant aux documents existants.

Figure 96: Processus de gestion des réclamations
```

---

## PDF page 305

```text
Sujet: Création de demandes d'avoir

Demandes d'avoir et de note de débit
Les demandes d'avoir et de note de débit peuvent être créées avec référence à un document
de facturation ou une commande client. Le système peut ainsi déterminer la quantité et la
valeur correctes à partir du document précédent. Lors de la création des documents, le
système vous demande de saisir le motif de la commande client à des fins d'analyse. La liste
des motifs possibles (par exemple, Dommage subi au cours du transport ou Écart de prix)
peut être gérée dans le Customizing.

Lorsque vous créez une demande d'avoir/de note de débit, le document contient
automatiquement un blocage de facture. Ce blocage empêche la facturation immédiate du
document. Une fois la réclamation vérifiée par les responsables, la demande d'avoir/de note
de débit peut être validée en supprimant le blocage de la facture.

Après suppression du blocage de la facture, les documents de facturation correspondants
peuvent être créés et les pièces comptables requises sont générées automatiquement. Ainsi,
les montants corrects sont portés au crédit ou débités du compte client.

Figure 97: Traitement des avoirs et des notes de débit

Approbation d'un avoir

Les réclamations client non justifiées doivent être refusées. Pour garantir que les postes
concernés ne sont pas transférés à un document de facturation, il est possible de saisir un
motif de refus. Les motifs de refus appropriés (par exemple, Demande injustifiée) peuvent
être gérés dans le Customizing.

Les postes refusés ne sont pas copiés dans les documents de facturation bien qu'ils soient
toujours disponibles à des fins d'analyse.
```

---

## PDF page 306

```text
Chapitre 9 : Gestion des réclamations

Figure 98: Approbation d'un avoir

Workflow de demande d'avoir

Généralement, lors de la création d'une demande d’avoir, le système active le blocage de la
facture (avoir) jusqu'à ce que l’employé responsable la débloque. Dans votre entreprise, vous
pouvez définir à quel instant la vérification doit être effectuée et par quel employé
responsable, selon la valeur de la demande de note de crédit.

Si cette valeur est inférieure à une valeur minimale donnée, le système peut valider
automatiquement la demande.

Figure 99: Workflow de demande d'avoir

Le workflow propre au traitement des notes de crédit garantit que le système identifie et
informe automatiquement l'employé responsable selon la valeur concernée lors de la création
d'une demande de note de crédit. Le salarié en question peut alors refuser ou valider la
demande d’avoir.

Avec l'application Gestion du workflow de demande d'avoir, vous pouvez configurer le
workflow pour optimiser le processus d'approbation des demandes d'avoir. L'application vous
permet de définir le cadre de validation automatique des demandes d’avoir, et les
approbateurs des demandes à vérifier. Si un workflow est activé et si les conditions de
lancement configurées sont remplies, le processus d’approbation est initié.
```

---

## PDF page 307

```text
Sujet: Création de demandes d'avoir

Les experts en processus de gestion peuvent définir parmi les membres des équipes
commerciales qui sera approbateur. Les experts en configuration peuvent définir et activer
les workflows de demande d'avoir avec leurs valeurs seuils et agents. Les directeurs
commerciaux peuvent ensuite recevoir des avis (Ma boîte de réception ou Avis) pour les
demandes d'avoir en attente d'approbation. Le responsable peut décider d'approuver ou de
rejeter les demandes d'avoir, ou bien demander à des commerciaux internes de les
reprendre.

Avant d'utiliser l'application Gestion du workflow de demande d'avoir, vous devez activer le
workflow standard SAP WS00800286 pour ce scénario. Pour plus d'informations, reportez-
vous à la documentation d'aide SAP. En outre, pour pouvoir affecter les fonctions
d’approbation de demande d’avoir requises aux membres de l’équipe responsables dans
l'application Gestion des équipes et responsabilités, les autorisations pertinentes doivent être
affectées à l’utilisateur.
```

---

## PDF page 308

```text
Chapitre 9 : Gestion des réclamations
```

---

## PDF page 309

```text
Chapitre 9
Exercice 32

Création d’une demande d'avoir

Création d’une demande d'avoir
Vous vendez des phares à un client. Une fois les phares livrés et payés par le client, ce dernier
se plaint que l'un d'eux a été endommagé pendant le transport. Vous convenez avec le client
qu'il sera crédité du montant qu'il a déjà payé.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           9-1##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS1##

Qté d'ordre                          5 pièces

2. Sauvegardez la commande et notez le numéro du document.
________________________________

3. Créez une livraison sortante pour la commande client précédente à l'aide des informations
suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

4. Notez le numéro de document de la livraison sortante.
________________________________

5. Prélevez la livraison et enregistrez la sortie de marchandises. Utilisez les informations
suivantes :
```

---

## PDF page 310

```text
Chapitre 9 : Gestion des réclamations

Nom de zone                             Valeur

LivrExécLogistq                     Numéro de la livraison sortante qui vient
d'être créée

Date/heure de départ de l'itinéraire          Aujourd'hui à aujourd'hui + 1 semaine

6. Créez le document de facturation avec référence à la livraison sortante et notez le numéro
du document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Dates de facturation jusqu’au              Date du jour + 1 semaine

___________________________________

7. Le client se plaint que trois phares ont été endommagés en transit. Créez une demande
d'avoir correspondante avec référence au document de facturation. Utilisez les
informations suivantes :

Nom de zone                             Valeur

Type commande client                 DNC

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Motif de la commande client             Endommagé lors du transport

8. Sauvegardez la demande d'avoir et enregistrez le numéro de document.
___________________________________

9. Validez la demande d'avoir pour la facturation en supprimant le blocage de la facture.

10. Créez l'avoir pour la demande d'avoir et notez le numéro de document.
___________________________________
```

---

## PDF page 311

```text
Chapitre 9
Solution 32

Création d’une demande d'avoir

Création d’une demande d'avoir
Vous vendez des phares à un client. Une fois les phares livrés et payés par le client, ce dernier
se plaint que l'un d'eux a été endommagé pendant le transport. Vous convenez avec le client
qu'il sera crédité du montant qu'il a déjà payé.

1. Créez une commande client à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           9-1##

DateLivrSouh.                         dans 1 semaine

Article                             T-MS1##

Qté d'ordre                          5 pièces

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de la transaction, saisissez le type de commande et les entités
organisationnelles.

c) Pour appeler les détails de la commande, appuyez sur Entrée.

d) Saisissez les informations pertinentes.

2. Sauvegardez la commande et notez le numéro du document.
________________________________

a) Dans la commande client, sélectionnez Sauvegarder.
Le numéro de document s'affiche.

3. Créez une livraison sortante pour la commande client précédente à l'aide des informations
suivantes :

Nom de zone                             Valeur

Point d'expédition                     Z0##
```

---

## PDF page 312

```text
Chapitre 9 : Gestion des réclamations

Nom de zone                             Valeur

Date de création planifiée                Échue la semaine prochaine

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Si les filtres de l'application ne s’affichent pas, sélectionnez Développer en-tête.

c) Saisissez votre point d'expédition, sélectionnez la date de création planifiée et cliquez
sur Lancer.

d) Sélectionnez la commande client dans la liste et cliquez sur Créer livraisons. Ne quittez
pas l'application.

4. Notez le numéro de document de la livraison sortante.
________________________________

a) Sélectionnez Afficher journal.

b) Pour rechercher le numéro de document, sélectionnez Livraisons.

5. Prélevez la livraison et enregistrez la sortie de marchandises. Utilisez les informations
suivantes :

Nom de zone                             Valeur

LivrExécLogistq                     Numéro de la livraison sortante qui vient
d'être créée

Date/heure de départ de l'itinéraire          Aujourd'hui à aujourd'hui + 1 semaine

a) Dans la barre de lancement de SAP Fiori, lancez l'application Exécution du processus
de sortant.

b) Ajustez la Date/heure de départ de l'itinéraire à la valeur ci-dessus. Pour cela, cliquez
sur le bouton situé à droite de la zone.

c) Cliquez sur la flèche, puis sélectionnez Plage de dates et saisissez les dates de début et
de fin correctes.

d) Saisissez la valeur de la zone Exéc. log. livraison. Si ce filtre n'est pas visible,
sélectionnez Filtres, sélectionnez LE Livraison dans la liste de la boîte de dialogue et
cliquez sur Lancer.

e) Pour lancer la sélection, cliquez sur Lancer.

f) Sélectionnez votre ordre de livraison sortante dans la liste et cliquez sur Créer tâches.

g) Sélectionnez le numéro de l'ordre de livraison sortante pour accéder aux détails du
document.

h) Cliquez sur Tâches en cours.

i) Sélectionnez le poste puis cliquez sur Confirmer tâches. Dans la boîte de dialogue
Confirmation, cliquez sur OK.

j) Sélectionnez Prélevé.
```

---

## PDF page 313

```text
Sujet: Création de demandes d'avoir

k) Sélectionnez à nouveau le poste et cliquez sur Sortie de marchandises.

6. Créez le document de facturation avec référence à la livraison sortante et notez le numéro
du document. Utilisez les informations suivantes :

Nom de zone                             Valeur

Dates de facturation jusqu’au              Date du jour + 1 semaine

___________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de documents
de facturation.

b) Saisissez la date de fin souhaitée dans la zone Date de la facture et cliquez sur Lancer.

c) Sélectionnez la ligne où figure votre livraison sortante et choisissez Créer documents
de facturation.
Résultat
Les détails de la facture sont affichés à l'écran.

d) Pour terminer le processus de facturation, sélectionnez Sauvegarder.
Résultat
Le numéro de document est désormais affiché en haut de l’écran.

7. Le client se plaint que trois phares ont été endommagés en transit. Créez une demande
d'avoir correspondante avec référence au document de facturation. Utilisez les
informations suivantes :

Nom de zone                             Valeur

Type commande client                 DNC

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Motif de la commande client             Endommagé lors du transport

a) Depuis la barre de lancement SAP Fiori, lancez l'application Gestion des demandes
d'avoir.

b) Sélectionnez Créer demande d’avoir.

c) Dans l’écran initial, saisissez le type de commande et les données d’organisation.

d) En bas à droite de l'écran, sélectionnez Créer avec référence.

e) Dans la boîte de dialogue Créer avec référence, saisissez le numéro de votre document
de facturation et cliquez sur Copier.

f) Dans la demande d'avoir, réduisez la quantité à 3. Passez ensuite à la page à onglet
Ventes et sélectionnez le motif de la commande client.

8. Sauvegardez la demande d'avoir et enregistrez le numéro de document.
___________________________________
```

---

## PDF page 314

```text
Chapitre 9 : Gestion des réclamations

a) Cliquez sur Sauvegarder.
Le numéro de document s'affiche.

9. Validez la demande d'avoir pour la facturation en supprimant le blocage de la facture.
a) Depuis la barre de lancement SAP Fiori, lancez l'application Gestion des demandes
d'avoir.

b) Sélectionnez la ligne contenant votre demande d'avoir et cliquez sur Supprimer
blocage de la facture.

10. Créez l'avoir pour la demande d'avoir et notez le numéro de document.
___________________________________

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de documents
de facturation.

b) Sélectionnez la ligne contenant le numéro de votre demande d’avoir.

c) Pour créer l'avoir, sélectionnez Création de documents de facturation.

d) Pour terminer le processus, cliquez sur Sauvegarder.
```

---

## PDF page 315

```text
Sujet: Création de demandes d'avoir

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Créer des demandes d'avoir
```

---

## PDF page 316

```text
Chapitre 9
Sujet 2

Annulation de documents de facturation

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Annulation des documents de facturation

Annulation de documents de facturation
L'annulation d'une facture peut se révéler nécessaire lorsque, par exemple, les conditions de
paiement ou l'adresse du payeur sont incorrectes.

Dans ce cas, un document de facturation séparé (annulation de document de facturation) et
une nouvelle pièce comptable sont générés. Ainsi, toutes les écritures résultant du document
de facturation erroné sont annulées par le ré-enregistrement de chaque poste d'écriture avec
le symbole inverse.

La figure « Annulation d’un document de facturation » illustre l'annulation d'un document de
facturation.

Figure 100: Annulation d'un document de facturation
```

---

## PDF page 317

```text
Chapitre 9
Exercice 33

Annulation d’un document de facturation

Vous pouvez être amené à annuler des documents de facturation contenant des erreurs dues,
par exemple, à des données de base incorrectes.

1. Annulez l'avoir que vous avez créé au cours du dernier exercice. Utilisez le donneur
d'ordre T-S50A## comme critère de sélection.

2. Affichez le flux de documents correspondant à votre avoir. Le document d'annulation y
est-il affiché ?
__________________________________
```

---

## PDF page 318

```text
Chapitre 9
Solution 33

Annulation d’un document de facturation

Vous pouvez être amené à annuler des documents de facturation contenant des erreurs dues,
par exemple, à des données de base incorrectes.

1. Annulez l'avoir que vous avez créé au cours du dernier exercice. Utilisez le donneur
d'ordre T-S50A## comme critère de sélection.
a) Dans la barre de lancement SAP Fiori, lancez l'application Gestion des documents de
facturation.

b) Saisissez le donneur d'ordre ci-dessus comme valeur de filtre et cliquez sur Lancer.

c) Sélectionnez la ligne contenant le numéro de document approprié et cliquez sur
Annuler.

d) Dans la boîte de dialogue Annuler les documents de facturation, confirmez en cliquant
sur OK.

e) Ne quittez pas l'application.

2. Affichez le flux de documents correspondant à votre avoir. Le document d'annulation y
est-il affiché ?
__________________________________

a) Dans l'application Gestion des documents de facturation, sélectionnez la ligne qui
contient le numéro de la facture annulée.

b) En haut de l'écran, sélectionnez Flux du processus.
Le document d’annulation et la pièce comptable correspondante font partie du flux de
documents.
```

---

## PDF page 319

```text
Sujet: Annulation de documents de facturation

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Annulation des documents de facturation
```

---

## PDF page 320

```text
Chapitre 9
Sujet 3

Création de retours

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Création des retours

Retour de marchandises
Lorsqu'un client souhaite renvoyer un article à votre entreprise, vous pouvez créer un
document de retours correspondant pour reproduire le processus dans le système. Ce
document peut être créé avec référence à un document de facturation ou à une commande
client. Le système reçoit ainsi toutes les données requises concernant les quantités et les
accords sur prix du document d'origine, garantissant ainsi la poursuite du traitement des
informations appropriées.

Lors de la création d'un document de retours, le système vous demande de gérer le motif de
la commande client (par exemple, « Dommage subi au cours du transport ») à des fins
d'analyse. En outre, le document contient automatiquement un blocage de facture qui
empêche la création immédiate d'un avoir.

Lorsque les marchandises arrivent à votre magasin, vous devez enregistrer une entrée de
marchandises correspondante. Pour cela, vous devez d'abord créer une livraison de retours
avec référence au document de retours. La quantité concernée est généralement enregistrée
dans une catégorie de stock de retours distincte plutôt que dans le stock à utilisation libre.

Une fois le processus approuvé et le blocage de facture supprimé, l'avoir et les pièces
comptables requises peuvent être créés. Le montant correct est automatiquement porté au
crédit du compte client. Cette étape peut être exécutée indépendamment de l'enregistrement
de l'entrée de marchandises.

Plutôt qu'un crédit, le client peut demander un remplacement gratuit pour les marchandises
retournées. Dans ce cas, au lieu d'un avoir, un document de vente de livraison ultérieure
gratuite est créé avec référence au document de retours. Ce document de livraison ultérieure
gratuite est ensuite livré (mais pas facturé).
```

---

## PDF page 321

```text
Sujet: Création de retours

Figure 101: Gestion des retours
```

---

## PDF page 322

```text
Chapitre 9 : Gestion des réclamations
```

---

## PDF page 323

```text
Chapitre 9
Exercice 34

Création d’un retour

Un client vous informe qu'il a acheté trop de casques de moto. Le client souhaite les retourner
pour obtenir un remboursement. Vous êtes d'accord pour qu'il renvoie les articles et pour
créditer son compte du montant payé.

1. Créez un document de retours à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 RE

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Article                             T-MS3##

Quantité                            3 pièces

Motif de la commande client             Écart quantité

Division                            1020

2. Sauvegardez le document de retours et notez le numéro de document.
_____________________________

3. Les casques sont arrivés. Créez la livraison de retours et notez le numéro de document.
____________________________

4. Enregistrez l'entrée de marchandises de la livraison de retours.

5. Affichez la synthèse des stocks de casques dans la division 1020. Dans quel type de stock
spécial la quantité de l'article a-t-elle été enregistrée ?
____________________________

6. Validez le document des retours pour la facturation en supprimant le blocage de la
facture.

7. Créez l'avoir avec référence au document de retours et notez le numéro du document.
____________________________
```

---

## PDF page 324

```text
Chapitre 9
Solution 34

Création d’un retour

Un client vous informe qu'il a acheté trop de casques de moto. Le client souhaite les retourner
pour obtenir un remboursement. Vous êtes d'accord pour qu'il renvoie les articles et pour
créditer son compte du montant payé.

1. Créez un document de retours à l'aide des informations suivantes :

Nom de zone                             Valeur

Type commande client                 RE

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Article                             T-MS3##

Quantité                            3 pièces

Motif de la commande client             Écart quantité

Division                            1020

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de l'application, saisissez le type de commande et les entités
organisationnelles.

c) Pour appeler les détails du document, appuyez sur Entrée.

d) Saisissez les informations pertinentes répertoriées dans le tableau. N'oubliez pas de
modifier la division du poste et d’indiquer 1020.

e) Si vous recevez un message d'avertissement vous demandant de vérifier la date de la
facture, appuyez sur Entrée pour la valider

2. Sauvegardez le document de retours et notez le numéro de document.
_____________________________

a) Cliquez sur Sauvegarder.
Le numéro de document s'affiche.

3. Les casques sont arrivés. Créez la livraison de retours et notez le numéro de document.
____________________________
```

---

## PDF page 325

```text
Sujet: Création de retours

a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de livraisons
sortantes.

b) Sélectionnez la ligne contenant votre numéro de document de retour, puis Créer
livraisons.

c) Sélectionnez Afficher journal.

4. Enregistrez l'entrée de marchandises de la livraison de retours.
a) Dans la barre de lancement de SAP Fiori, lancez l'application Modifier livraison
sortante.

b) Dans l'écran initial de l'application, saisissez le numéro de document de la livraison des
retours et appuyez sur Entrée.

c) Dans l'écran de synthèse de la livraison, en haut de l'écran, sélectionnez Enregistrer
EM.

5. Affichez la synthèse des stocks de casques dans la division 1020. Dans quel type de stock
spécial la quantité de l'article a-t-elle été enregistrée ?
____________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Stock - Article individuel.

b) Saisissez le numéro d'article en haut de l'écran et appuyez sur Entrée.
La quantité a été enregistrée dans le stock de retours de la division 1020.

6. Validez le document des retours pour la facturation en supprimant le blocage de la
facture.
a) Dans la barre de lancement SAP Fiori, lancez l'application Modification de commandes
clients.

b) Dans l'écran, saisissez le numéro de votre document de retours.

c) Pour appeler les détails du document, appuyez sur Entrée.

d) Pour supprimer le blocage de la facture, dans la liste déroulante de la zone Blocage
facture, sélectionnez la dernière entrée (vide).

e) Cliquez sur Sauvegarder.

7. Créez l'avoir avec référence au document de retours et notez le numéro du document.
____________________________
a) Dans la barre de lancement de SAP Fiori, lancez l'application Création de documents
de facturation.

b) Sélectionnez la ligne contenant le numéro de votre document de retours.

c) Sélectionnez Créer documents de facturation.
Les détails de l’avoir sont affichés à l'écran.

d) Pour terminer le processus, cliquez sur Sauvegarder.
Résultat
Le numéro de document est désormais affiché en haut de l’écran.
```

---

## PDF page 326

```text
Chapitre 9 : Gestion des réclamations

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Création des retours
```

---

## PDF page 327

```text
Chapitre 9

Évaluation des connaissances

1.  Lorsque vous créez une demande d'avoir/de note de débit, le document est facturé
automatiquement et immédiatement.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Lors de l'annulation d'un document de facturation, un document de facturation distinct
est généré et une nouvelle pièce comptable est générée.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

3. Lors de la création du document de retours, le système vous demande de gérer un avoir.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux
```

---

## PDF page 328

```text
Chapitre 9

Évaluation des connaissances - Réponses

1.  Lorsque vous créez une demande d'avoir/de note de débit, le document est facturé
automatiquement et immédiatement.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Lorsque vous créez une demande d'avoir/de note de débit, le document contient
automatiquement un blocage de facture. Ce blocage empêche la facturation immédiate
du document.

2. Lors de l'annulation d'un document de facturation, un document de facturation distinct
est généré et une nouvelle pièce comptable est générée.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Lors de l'annulation d'un document de facturation, un document de facturation
séparé (annulation de document de facturation) et une nouvelle pièce comptable sont
générés.

3. Lors de la création du document de retours, le système vous demande de gérer un avoir.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. Lors de la création d'un document de retours, le système vous demande de gérer
le motif de la commande client (par exemple, « Dommage subi au cours du transport ») à
des fins d'analyse. En outre, le document contient automatiquement un blocage de
facture qui empêche la création immédiate d'un avoir.
```

---

## PDF page 329

```text
CHAPITRE 10  Suivi et analyse des ventes

Sujet 1

Utilisation de l’application Traitement des commandes clients                            320
Exercice 35 : Utilisation de l’application Traitement des commandes clients          327

Sujet 2

Gestion des plans commerciaux                                                         331

Sujet 3

Utilisation d'applications analytiques                                                333
Exercice 36 : Analyse des données à l'aide des applications analytiques             337

OBJECTIFS DU CHAPITRE

●   Utilisation de l’application Traitement des commandes clients

●  Gestion des plans commerciaux

●   Utiliser les applications analytiques
```

---

## PDF page 330

```text
Chapitre 10
Sujet 1

Utilisation de l’application Traitement des
commandes clients

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●   Utilisation de l’application Traitement des commandes clients

L’application Traitement des commandes clients
Traitement des commandes clients : approche traditionnelle

Figure 102: Traitement des commandes clients : approche traditionnelle

Dans un système traditionnel SAP ERP, il est nécessaire d'exécuter plusieurs programmes
pour avoir une vision globale de tous les problèmes liés au processus. Par conséquent,
plusieurs problèmes dans une commande client ne peuvent pas être détectés en une étape,
ce qui fait augmenter le risque de ne pas détecter des situations exceptionnelles.

En outre, il n'est pas possible de suivre la communication et les décisions en lien avec les
problèmes.
```

---

## PDF page 331

```text
Sujet: Utilisation de l’application Traitement des commandes clients

Traitement des commandes clients dans SAP S/4HANA

Figure 103: Traitement des commandes clients dans SAP S/4HANA

Avec SAP S/4HANA, les commerciaux internes ont une vue d'ensemble de la situation
actuelle de traitement des commandes clients et peuvent ainsi décider du périmètre sur
lequel porter leur attention concernant les activités de suivi. Ils peuvent utiliser une liste des
commandes clients qui ne peuvent pas être traitées classées par ordre de priorité, de façon à
ce que les éléments les plus importants soient considérés en premier.

SAP S/4HANA aide les utilisateurs en leur fournissant des informations, des contacts et des
fonctions de collaboration pertinents. Les utilisateurs peuvent également utiliser des notes
pour documenter leurs actions.
```

---

## PDF page 332

```text
Chapitre 10 : Suivi et analyse des ventes

SAP Smart Business en un mot

Figure 104: SAP Smart Business en un mot

SAP Smart Business peut être configuré pour les rôles clés dans toute l'entreprise. Les
utilisateurs fonctionnels peuvent maintenir leur niveau de performance en décidant et en
agissant en temps réel.

SAP Smart Business offre un nouveau modèle de travail, basé sur les exceptions, qui allie
l'analyse à l'action. Vous passez directement d'un point de données du graphique à la
transaction correspondante pour résoudre le problème. Il suit les directives et concepts de
SAP Fiori, par exemple la navigation SAP Fiori.

SAP Smart Business fournit des vignettes qui se trouvent dans la barre de lancement
SAP Fiori. Il vous aide à identifier facilement les exceptions à l'aide de ses visualisations KPI
(indicateurs de performance clés), ceci grâce à des codes couleurs associés aux seuils cibles
définis. Il offre également des applications SAP Fiori (applications de modélisation SAP Smart
Business) pour configurer facilement vos KPI et leur visualisation.
```

---

## PDF page 333

```text
Sujet: Utilisation de l’application Traitement des commandes clients

Nouvelle expérience utilisateur

Figure 105: Nouvelle expérience utilisateur

Avec l’application Traitement des commandes clients SAP, les commerciaux internes
peuvent résoudre des problèmes empêchant les commandes clients d’être traitées.
L’application propose une liste de toutes les commandes clients qui ne peuvent pas être
traitées pour une ou plusieurs raisons. Elle présente les fonctions suivantes :

●   Elle met en évidence les obstacles

●   Elle fournit des informations complémentaires

●   Elle fournit des options spécifiques pour résoudre les problèmes

Ainsi, les commerciaux internes peuvent suivre les commandes clients à des stades critiques,
collaborer avec les contacts internes et externes et répartir les problèmes efficacement pour
garantir un traitement le plus rapide possible des commandes clients à des stades critiques.
```

---

## PDF page 334

```text
Chapitre 10 : Suivi et analyse des ventes

Types de problèmes

Figure 106: Types de problèmes

Résolution de problèmes dans les commandes client – Résoudre le blocage de
facturation

Par exemple, la figure « Résolution de problèmes dans les commandes client – Résoudre le
blocage de la facture » montre comment s’occuper d’une commande incomplète, également
bloquée pour facturation. De nombreuses options sont à la disposition de l’utilisateur :

●  Afficher les informations d'en-tête et la liste des postes bloqués

●  Afficher les détails de chaque poste bloqué

●  Supprimer le blocage de la facture au niveau de l'en-tête et/ou au niveau du poste

●   Vérifier et modifier les conditions de paiement au niveau de l'en-tête et/ou du poste

●  Accéder à l'application Modifier commande client pour effectuer des modifications
supplémentaires
```

---

## PDF page 335

```text
Sujet: Utilisation de l’application Traitement des commandes clients

Figure 107: Résolution de problèmes dans les commandes client – Résoudre le blocage de facturation

De plus, le flux de processus peut également être le point de départ de traitement des
problèmes et offre les fonctions suivantes :

●    Il fournit un aperçu rapide de tout le processus commercial et replace les problèmes dans
le contexte des objets de gestion liés

●    Il représente sous forme graphique tous les documents, leurs relations et le statut du
document

●    Il permet la résolution des problèmes directement à partir du flux de processus comme
point de départ

●    Il montre sous forme graphique le statut actuel (rouge, vert)

●    Il marque d'un cercle rouge le statut global des documents concernés à chaque étape (en
commande, en approvisionnement, en livraison et en facturation)

●    Il passe de rouge à vert quand tous les problèmes sont résolus
```

---

## PDF page 336

```text
Chapitre 10 : Suivi et analyse des ventes

Figure 108: Résolution des problèmes à l'aide du flux de processus : exemple
```

---

## PDF page 337

```text
Chapitre 10
Exercice 35

Utilisation de l’application Traitement des
commandes clients

Vous souhaitez tester les fonctionnalités de l’application Traitement des commandes clients.
Vous créez donc une commande client incomplète et résolvez le problème à l'aide de
l'application correspondante.

1. Créez une commande client et utilisez les données répertoriées dans le tableau.
Supprimez les conditions de paiement de la commande client afin de la rendre
incomplète. Notez le numéro du document.

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           658–##

Article                             T-MS1##

Quantité                            3 pièces

DateLivrSouh.                        Date du jour

____________________________________________

2. Utilisez l'application Traitement des commandes clients (Analyse et résolution) pour
identifier et compléter votre commande client.
```

---

## PDF page 338

```text
Chapitre 10
Solution 35

Utilisation de l’application Traitement des
commandes clients

Vous souhaitez tester les fonctionnalités de l’application Traitement des commandes clients.
Vous créez donc une commande client incomplète et résolvez le problème à l'aide de
l'application correspondante.

1. Créez une commande client et utilisez les données répertoriées dans le tableau.
Supprimez les conditions de paiement de la commande client afin de la rendre
incomplète. Notez le numéro du document.

Nom de zone                             Valeur

Type commande client                 CDCL

Organisation commerciale              1010

Canal distribution                     10

Secteur d'activité                     00

Donneur d'ordre                      T-S50A##

Réf. client                           658–##

Article                             T-MS1##

Quantité                            3 pièces

DateLivrSouh.                        Date du jour

____________________________________________

a) Dans la barre de lancement SAP Fiori, lancez l'application Création de commandes
clients VA01.

b) Dans l'écran initial de l'application, saisissez le type de commande et les entités
organisationnelles.

c) Appuyez sur Entrée pour accéder aux détails du document.

d) Saisissez les valeurs de zones en fonction du tableau.

e) Supprimez la valeur dans la zone conditions de paiement et sélectionnez Sauvegarder.

f) Si le message d'avertissement Entrez Cond. paiement s'affiche, évitez-le en appuyant
surEntrée.

g) Dans la boîte de dialogue Sauvegarder document incomplet, cliquez sur Sauvegarder.
Le numéro de la commande client s'affiche à l'écran.
```

---

## PDF page 339

```text
Sujet: Utilisation de l’application Traitement des commandes clients

2. Utilisez l'application Traitement des commandes clients (Analyse et résolution) pour
identifier et compléter votre commande client.
a) Dans la barre de lancement SAP Fiori (groupe de vignettes Analytics and Monitoring),
lancez l'application Traitement des commandes clients(Analyse et résolution).

b) Sélectionnez le filtre compact            pour afficher les zones de recherche.

c) Saisissez le numéro de la commande client dans la zone Rechercher et appuyez sur
Entrée.

d) Vous verrez plusieurs postes pour la même commande. Sélectionnez la flèche vers la

droite         sur la ligne contenant votre numéro de commande.

e) À gauche de l'écran, le système affiche désormais les différents problèmes de cette
commande client. Sélectionnez Données incomplètes dans la commande client.

f) En haut à droite de l'écran, sélectionnez Modifier données incomplètes.

g) Dans la fenêtre pop-up, sélectionnez Compléter les données.

h) Entrez les conditions de paiement Payable immédiatement sans déduction.

i) Sélectionnez Traiter données suivantes.

j) Cliquez sur Sauvegarder.

k) Cliquez sur Retour     pour revenir à l'écran Suivi des détails de commande client. Si

nécessaire, appuyez sur Entrée pour actualiser votre écran.

l) À gauche de l'écran, le système affiche désormais le problème de livraison de cette
commande client. Sélectionnez Problème de livraison pour commande client.

m) Faites défiler vers le bas pour afficher les détails du poste.

n) Sélectionnez le poste, puis Créer livraison et confirmez la boîte de dialogue.
Tous les problèmes de la commande client sont désormais résolus. Le statut de la
commande client est maintenant Terminé.
```

---

## PDF page 340

```text
Chapitre 10 : Suivi et analyse des ventes

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●   Utilisation de l’application Traitement des commandes clients
```

---

## PDF page 341

```text
Chapitre 10
Sujet 2

Gestion des plans commerciaux

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●  Gestion des plans commerciaux

Plans commerciaux
Des plans commerciaux peuvent être utilisés pour définir les objectifs des ventes pour une
période à venir (par exemple, l'exercice suivant). Les valeurs cibles souhaitées peuvent être
planifiées à l'aide de différentes dimensions, telles que le client, l'article et/ou les entités
organisationnelles.

Avec l'application Gestion des plans commerciaux, ces dimensions peuvent facilement être
sélectionnées. Un schéma du plan correspondant peut alors être généré et téléchargé dans
Microsoft Excel. Après avoir géré les valeurs cibles dans le fichier Excel, il peut être rechargé
dans le plan commercial.

Figure 109: Données du plan commercial

Plusieurs versions d'un plan commercial peuvent être créées pour refléter les fluctuations
potentielles du marché. Par exemple, sur la base d'une croissance potentielle du marché de
20 % pour l’exercice suivant, une version optimiste peut être créée pour refléter cela, en plus
d’une version standard basée sur la performance de l’exercice passé.
```

---

## PDF page 342

```text
Chapitre 10 : Suivi et analyse des ventes

Remarque :
Vous pouvez uniquement rechercher, afficher et traiter des plans commerciaux
créés par l'utilisateur.

Performances des ventes - Planifié/Réel
Après la création des plans commerciaux pour une période planifiée, la performance des
ventes peut être suivie en comparant les valeurs réelles et les valeurs cibles. Elle peut être
suivi en temps réel pour savoir dans quelle mesure les objectifs des ventes sont atteints et
donc, pour obtenir une visibilité sur les performances de vente en cours.

L'application Performance des ventes - Planifié/Réel offre une vue hybride dans laquelle vous
pouvez visualiser de manière efficace la différence entre les données budgétées et les
données réelles dans un graphique, tout en affichant les détails dans un tableau.

Figure 110: Application Performance des ventes - Planifié/Réel

Les données budgétées et réelles sont comparées comme suit :

●  Les valeurs budgétées et réelles représentent les entrées de commande client ou le chiffre
d'affaires, selon ce que vous avez planifié dans la version du plan commercial sélectionnée.

●  Les valeurs budgétées et réelles sont comparées par mois, trimestre ou exercice dans la
période planifiée, selon la manière dont vous avez défini cela dans la version du plan
commercial sélectionnée.

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●  Gestion des plans commerciaux
```

---

## PDF page 343

```text
Chapitre 10
Sujet 3

Utilisation d'applications analytiques

OBJECTIFS DU SUJET
À la fin de ce sujet, vous serez en mesure de :

●   Utiliser les applications analytiques

Applications analytiques

Figure 111: Applications analytiques

Les systèmes SAP ERP modernes sont remis en question par des charges de travail mixtes de
tâches opérationnelles OLTP (Online Transaction Processing) et de requêtes OLAP (Online
Analytical Processing). Par exemple :

●  OLTP : création de commandes clients, de factures et de pièces comptables, et affichage
des données de base clients

●  OLAP : relance, contrôle de la quantité disponible, reporting opérationnel (liste des
commandes client en cours)

Les systèmes de gestion des données actuels sont optimisés pour les charges de travail
transactionnelles quotidiennes ou analytiques. Cette séparation entraîne les inconvénients
suivants :
```

---

## PDF page 344

```text
Chapitre 10 : Suivi et analyse des ventes

●  Le système OLAP ne dispose pas des données les plus actualisées.

●  Le système OLAP a seulement un sous-ensemble prédéfini des données.

●  Un processus ETL (extraction, transformation et chargement) exigeant beaucoup de
ressources est nécessaire pour synchroniser les données dans les deux systèmes.

●  Cela donne lieu à la redondance des données.

●  Différents schémas de données engendrent de la complexité pour les applications
combinant les sources.

Transactions et analyses sur une seule plate-forme in-memory

Figure 112: Transactions et analyses sur une seule plate-forme in-memory

Les applications d'entreprise ont été lancées il y a plusieurs décennies pour servir de
systèmes d'enregistrement pour collecter les commandes clients, les avis d'incidents, les
entrées de journal et d'autres enregistrements liés à des opérations de gestion. Le personnel
métier avait besoin d’un accès à ces informations pour définir comment fixer le prix, planifier
et définir les priorités. Les informaticiens ont ensuite conçu des systèmes analytiques
distincts pour soutenir la prise de décisions sur des plates-formes complètement différentes.
Il paraissait théoriquement logique d'avoir des systèmes distincts sur des plates-formes
différentes pour traiter différentes charges de travail. Pendant des années, on a opté pour des
plates-formes séparées pour garantir une bonne performance des transactions et analyses,
étant donné la différence d'exigences entre la collecte des données et leur analyse. En
pratique, cependant, l’obligation de transférer des données entre les deux plates-formes
sous-jacentes aux deux types de système engendre des retards d’accès aux informations et
réduit la capacité à lier les informations aux actions à cause de l'absence de lien entre les
analyses et les données source. L’entreprise s'expose alors à des risques si les décisionnaires
sont obligés de se fier à des données incomplètes ou obsolètes, ou s'ils ne peuvent pas
connecter les informations d’analyse aux données source.

SAP S/4HANA peut associer les transactions à des analyses en temps réel dans un
environnement unique intégré pour déterminer la meilleure façon d'obtenir des informations
instantanées sur une situation d'urgence. Plutôt que d'utiliser des applications
transactionnelles et analytiques distinctes intégrées à des plates-formes séparées, un
environnement de gestion des données unique pour les deux systèmes d'enregistrement et
```

---

## PDF page 345

```text
Sujet: Utilisation d'applications analytiques

les système de décision (en supposant qu'il est possible d'obtenir une bonne performance
pour chacun) peut avoir les avantages suivants :

●  Les utilisateurs ont accès aux données les plus récentes, ils peuvent les analyser dès
qu'elles sont disponibles au lieu d'attendre le transfert des données, ce qui supprime la
principale cause des retards d'informations. En réduisant les charges indirectes liées aux
plates-formes multiples, il est possible de simplifier les tâches de gestion informatique des
données et les fonctions d'administration des données de gestion.

●  Avec un accès instantané aux données les plus récentes, le personnel de l’entreprise peut
prendre plus rapidement les décisions. Il est aussi possible d'accélérer les processus de
gestion. À titre d'exemple, pendant une transaction, les salariés d'un centre de contact
disposent des données les plus récentes concernant le client. Une recommandation de
vente croisée peut être faite sur les dernières commandes du client ou même sur une
commande en cours.

Architecture de l'analyse en temps réel SAP S/4HANA

Figure 113: Architecture de l'analyse en temps réel SAP S/4HANA

SAP S/4HANA intègre les transactions et les analyses permettant ainsi le reporting
opérationnel sur les données modifiées. Dans SAP S/4HANA, ce concept est mis en œuvre à
l'aide de CDS (Core Data Services) pour le reporting opérationnel en temps réel. Le contenu
est représenté sous forme de modèle de données virtuel (MDV), basé sur les tables
transactionnelles et les tables des données de base SAP S/4HANA. Les vues CDS sont
développées, gérées et étendues dans la couche ABAP du système SAP S/4HANA. Le
système génère des vues d'exécution SQL dans SAP HANA pour exécuter les données lues et
la transformation dans la couche base de données de SAP HANA.

Les avantages de cette approche comprennent l’intégration complète ABAP qui permet par
exemple de réutiliser les autorisations de reporting existantes, etc. SAP peut également
utiliser le moteur analytique (fonctionnalité BW intégrée) pour prendre en charge l'affichage
élaboré des hiérarchies. Ces avantages permettent de créer un nombre beaucoup plus
important de cas d'utilisation pour le modèle de données virtuel. L'analyse SAP S/4HANA
permet non seulement un reporting générique OLAP opérationnel mais aussi des scénarios
```

---

## PDF page 346

```text
Chapitre 10 : Suivi et analyse des ventes

d'analyse intégrée pour des applications hybrides, transactionnelles et analytiques (par
exemple SAP Embedded BI ou cockpits SAP Smart Business) qui reposent sur les mêmes
modèles. L'accès en lecture pour la recherche / les info-clés est aussi disponible.

Utilisateur final : rapport multidimensionnel

Figure 114: Utilisateur final : rapport multidimensionnel

Le reporting multidimensionnel comprend toutes les tâches d'analyse exploratoires pour
diverses questions commerciales. Le filtrage, la rotation, le tri et la réorganisation ad hoc des
données en IU tabulaires ou graphiques sont pris en charge. Une grille Web Dynpro est
utilisée dans ce contexte.
```

---

## PDF page 347

```text
Chapitre 10
Exercice 36

Analyse des données à l'aide des applications
analytiques

Analysez la valeur des entrées de commandes clients avec le reporting multidimensionnel.

1. Lancez l'application Entrée de commandes clients et saisissez EUR comme devise
d'affichage.

2. Vous souhaitez vous concentrer sur le ratio Entrée de commandes et sur le mois en cours.
Ajustez l'analyse en conséquence en utilisant les options de filtre approprié.

3. Pour comparer la valeur des entrées de commandes des différents clients, vous ajoutez le
donneur d'ordre comme analyse descendante supplémentaire.

4. Triez les données en fonction de la valeur de l'entrée de commandes (ordre décroissant)
pour identifier le meilleur client. Accédez à la liste des commandes clients pour ce client.

5. Affichez les données sous forme de graphique et utilisez le type de diagramme à barres.

6. Enfin, exportez le rapport dans Microsoft Excel (sans sauvegarder le fichier).
```

---

## PDF page 348

```text
Chapitre 10
Solution 36

Analyse des données à l'aide des applications
analytiques

Analysez la valeur des entrées de commandes clients avec le reporting multidimensionnel.

1. Lancez l'application Entrée de commandes clients et saisissez EUR comme devise
d'affichage.
a) Dans la barre de lancement SAP Fiori, lancez l'application Entrée de commandes
clients - Analyse flexible.

b) Saisissez EUR comme Devise d'affichage dans la zone correspondante et appuyez sur
Entrée.

2. Vous souhaitez vous concentrer sur le ratio Entrée de commandes et sur le mois en cours.
Ajustez l'analyse en conséquence en utilisant les options de filtre approprié.
a) Cliquez avec le bouton droit de la souris sur Ratios, puis sélectionnez Filtre et
Sélectionner valeur du filtre. Sélectionnez Entrée de commandes comme indicateur
pertinent. Confirmez en cliquant sur OK.

b) Dans la page à onglet Analyse des données, dans le menu contextuel (clic droit) du
mois en cours (par exemple, 11.2020), sélectionnez Filtre → Conserver valeur de filtre.
Vous devrez peut-être faire défiler vers la droite pour trouver le mois en cours.

3. Pour comparer la valeur des entrées de commandes des différents clients, vous ajoutez le
donneur d'ordre comme analyse descendante supplémentaire.
a) Dans la page à onglet Analyse des données, sélectionnez Analyse descendante, puis
Ajouter analyse descendante.

b) Dans la fenêtre pop-up Sélectionner zones, sélectionnez Donneur d'ordre, puis cliquez
sur OK.

4. Triez les données en fonction de la valeur de l'entrée de commandes (ordre décroissant)
pour identifier le meilleur client. Accédez à la liste des commandes clients pour ce client.
a) Sélectionnez la colonne Entrée de commandes.

b) Sélectionnez Trier puis Valeur du ratio (décroissant).

c) Sélectionnez la zone affichant la meilleure valeur.

d) Cliquez sur Accéder à puis sélectionnez Commande client.

e) Revenez à la page à onglet du navigateur qui contient votre analyse.

5. Affichez les données sous forme de graphique et utilisez le type de diagramme à barres.
a) Dans l'analyse, passez à la page à onglet Représentation graphique.

b) Pour modifier les options, sélectionnez le bouton Options.

c) Sélectionnez le type de diagramme Barres et cliquez sur Sauvegarder.
```

---

## PDF page 349

```text
Sujet: Utilisation d'applications analytiques

6. Enfin, exportez le rapport dans Microsoft Excel (sans sauvegarder le fichier).
a) Revenez à la page à onglet Analyse des données.

b) Pour exporter les données, sélectionnez Exporter, puis Exporter en tant que Feuille de
calcul Excel.
```

---

## PDF page 350

```text
Chapitre 10 : Suivi et analyse des ventes

SYNTHÈSE DU SUJET
Vous êtes désormais en mesure de :

●   Utiliser les applications analytiques
```

---

## PDF page 351

```text
Chapitre 10

Évaluation des connaissances

1.  Avec SAP Smart Business, vous pouvez passer directement d'un point de données du
diagramme à la transaction appropriée pour résoudre le problème.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

2. Parmi les options suivantes, laquelle offre une vue hybride pour les commandes client
dans lesquelles vous pouvez visualiser la différence entre les données planifiées et
réelles ?

Sélectionnez la réponse correcte.

X  A Gestion des plans commerciaux

X  B Performances des ventes - Planifié/Réel

X  C Modifier commande client

X  D Application Traitement des commandes clients SAP

3. Parmi les options suivantes, laquelle est utilisée dans SAP S/4HANA pour intégrer les
transactions et les analyses permettant le reporting opérationnel sur les données
modifiées ou le reporting opérationnel en temps réel ?

Sélectionnez la réponse correcte.

X  A SAP ERP

X  B SAP Core Data Services (CDS)

X  C Couche ABAP
```

---

## PDF page 352

```text
Chapitre 10

Évaluation des connaissances - Réponses

1.  Avec SAP Smart Business, vous pouvez passer directement d'un point de données du
diagramme à la transaction appropriée pour résoudre le problème.

Indiquez si cette proposition est vraie ou fausse.

X  Vrai

X  Faux

Correct. SAP Smart Business offre un nouveau modèle de travail, basé sur les exceptions,
qui allie l'analyse à l'action. Vous passez directement d'un point de données du graphique
à la transaction correspondante pour résoudre le problème.

2. Parmi les options suivantes, laquelle offre une vue hybride pour les commandes client
dans lesquelles vous pouvez visualiser la différence entre les données planifiées et
réelles ?

Sélectionnez la réponse correcte.

X  A Gestion des plans commerciaux

X  B Performances des ventes - Planifié/Réel

X  C Modifier commande client

X  D Application Traitement des commandes clients SAP

Correct. L'application Performance des ventes - Planifié/Réel offre une vue hybride dans
laquelle vous pouvez visualiser efficacement la différence entre les données budgétées et
réelles dans un graphique tout en affichant les détails dans une table.
```

---

## PDF page 353

```text
Chapitre 10 : Évaluation des connaissances - Réponses

3. Parmi les options suivantes, laquelle est utilisée dans SAP S/4HANA pour intégrer les
transactions et les analyses permettant le reporting opérationnel sur les données
modifiées ou le reporting opérationnel en temps réel ?

Sélectionnez la réponse correcte.

X  A SAP ERP

X  B SAP Core Data Services (CDS)

X  C Couche ABAP

Correct. SAP S/4HANA intègre les transactions et les analyses permettant ainsi le
reporting opérationnel sur les données modifiées. Avec SAP S/4HANA, ce concept est
pris en charge à l'aide de SAP Core Data Services (CDS) pour le reporting opérationnel en
temps réel.
```
