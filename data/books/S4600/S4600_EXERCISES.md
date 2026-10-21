# S4600 - Exercices et solutions

Référence compacte destinée à Codex. Utiliser ce fichier en priorité; consulter `S4600_FULL_CLEAN.md` seulement si un détail manque, notamment une figure ou une table complexe.

## Règle de numérotation
Dans le support, remplacer `##` par le numéro de groupe attribué. Le groupe 01 est la cible projet, **pas** une transformation du texte original.

## Index

| # | Chapitre | Exercice | PDF page exercice | PDF page solution |
|---:|---|---|---:|---:|
| 1 | Navigation avec SAP Fiori | Utilisation de la barre de lancement SAP Fiori | 21 | 22 |
| 2 | Structures d’entreprise | Description des structures organisationnelles dans SAP S/4HANA Sales | 39 | 42 |
| 3 | Synthèse des processus de vente | Création d’une commande client | 57 | 58 |
| 4 | Synthèse des processus de vente | Affichage d’une commande client | 63 | 64 |
| 5 | Synthèse des processus de vente | Création d’une livraison sortante | 71 | 72 |
| 6 | Synthèse des processus de vente | Prélèvement de marchandises | 79 | 80 |
| 7 | Synthèse des processus de vente | Création d’un document de facturation | 87 | 88 |
| 8 | Synthèse des processus de vente | Enregistrement d’un encaissement | 91 | 92 |
| 9 | Données de base | Création de données de base client | 105 | 107 |
| 10 | Données de base | Utilisation des données de base partenaire | 111 | 113 |
| 11 | Données de base | Création d’une fiche article | 119 | 121 |
| 12 | Données de base | Création d’une fiche infos client-article | 129 | 131 |
| 13 | Données de base | Création d’un enregistrement de condition (prix de vente) | 137 | 139 |
| 14 | Données de base | Création d’un enregistrement de condition (remise) | 141 | 143 |
| 15 | Données de base | Description du contexte des données de base de condition | 145 | 146 |
| 16 | Données de base | Création de postes par défaut | 155 | 157 |
| 17 | Données de base | Gestion des documents de vente incomplets | 161 | 162 |
| 18 | Détermination automatique des données et ordonnancement | Vérification des résultats de la détermination automatique des données | 179 | 181 |
| 19 | Détermination automatique des données et ordonnancement | Vérification des résultats de l’ordonnancement de l’expédition et du transport | 189 | 191 |
| 20 | Contrôle de disponibilité | Vérification des principaux facteurs influençant le contrôle de disponibilité | 205 | 206 |
| 21 | Contrôle de disponibilité | Vérification du transfert des besoins | 211 | 212 |
| 22 | Contrôle de disponibilité | Vérification des options des livraisons complètes ou partielles | 215 | 217 |
| 23 | Contrôle de disponibilité | Exécution des contrôles de disponibilité | 227 | 229 |
| 24 | Contrôle de disponibilité | Description des fonctions du contrôle de disponibilité | 233 | 234 |
| 25 | Opération groupée | Création des livraisons sortantes via une opération groupée | 249 | 250 |
| 26 | Opération groupée | Achèvement des fonctions d’expédition via une opération groupée | 253 | 254 |
| 27 | Opération groupée | Création de documents de facturation à l’aide d’une opération groupée | 259 | 261 |
| 28 | Processus supplémentaires dans les ventes | Création de documents d’avant-vente | 271 | 273 |
| 29 | Processus supplémentaires dans les ventes | Description du traitement des documents d’avant-vente | 277 | 278 |
| 30 | Processus supplémentaires dans les ventes | Exécution de la fabrication sur commande | 283 | 286 |
| 31 | Processus supplémentaires dans les ventes | Vente d’un produit de service | 293 | 295 |
| 32 | Gestion des réclamations | Création d’une demande d’avoir | 309 | 311 |
| 33 | Gestion des réclamations | Annulation d’un document de facturation | 317 | 318 |
| 34 | Gestion des réclamations | Création d’un retour | 323 | 324 |
| 35 | Suivi et analyse des ventes | Utilisation de l’application Traitement des commandes clients | 337 | 338 |
| 36 | Suivi et analyse des ventes | Analyse des données à l’aide des applications analytiques | 347 | 348 |

---

# Exercice 1 - Utilisation de la barre de lancement SAP Fiori

**Chapitre:** Navigation avec SAP Fiori  
**Pages PDF:** exercice 21-21; solution 22-24

## Énoncé


### Page 21

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

## Solution SAP du support


### Page 22

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

### Page 23

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

### Page 24

```text
Chapitre 1 : Navigation avec SAP Fiori

c) Le nom de l'application apparaîtra dans la liste déroulante de recherche.

d) Sélectionnez le nom de l'application pour l'ouvrir.
```

---

# Exercice 2 - Description des structures organisationnelles dans SAP S/4HANA Sales

**Chapitre:** Structures d’entreprise  
**Pages PDF:** exercice 39-41; solution 42-43

## Énoncé


### Page 39

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

### Page 40

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

### Page 41

```text
Sujet: Identification des structures d'entreprise dans SAP S/4HANA Sales

6. À quelles entités organisationnelles les divisions chargées de la livraison sont-elles
affectées ?
```

## Solution SAP du support


### Page 42

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

### Page 43

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

# Exercice 3 - Création d’une commande client

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 57-57; solution 58-62

## Énoncé


### Page 57

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

## Solution SAP du support


### Page 58

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

### Page 59

```text
Sujet: Traitement des documents de vente

h) En bas à droite de l’écran, cliquez sur Sauvegarder.
Le numéro de document s'affiche.
```

### Page 60

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

### Page 61

```text
Sujet: Traitement des documents de vente

Figure 30: Structure d'un document de vente
```

### Page 62

```text
Chapitre 3 : Synthèse des processus de vente
```

---

# Exercice 4 - Affichage d’une commande client

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 63-63; solution 64-65

## Énoncé


### Page 63

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

## Solution SAP du support


### Page 64

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

### Page 65

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

# Exercice 5 - Création d’une livraison sortante

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 71-71; solution 72-73

## Énoncé


### Page 71

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

## Solution SAP du support


### Page 72

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

### Page 73

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

# Exercice 6 - Prélèvement de marchandises

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 79-79; solution 80-81

## Énoncé


### Page 79

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

## Solution SAP du support


### Page 80

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

### Page 81

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

# Exercice 7 - Création d’un document de facturation

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 87-87; solution 88-90

## Énoncé


### Page 87

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

## Solution SAP du support


### Page 88

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

### Page 89

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

### Page 90

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

# Exercice 8 - Enregistrement d’un encaissement

**Chapitre:** Synthèse des processus de vente  
**Pages PDF:** exercice 91-91; solution 92-93

## Énoncé


### Page 91

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

## Solution SAP du support


### Page 92

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

### Page 93

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

# Exercice 9 - Création de données de base client

**Chapitre:** Données de base  
**Pages PDF:** exercice 105-106; solution 107-110

## Énoncé


### Page 105

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

### Page 106

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

## Solution SAP du support


### Page 107

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

### Page 108

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

### Page 109

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

### Page 110

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

# Exercice 10 - Utilisation des données de base partenaire

**Chapitre:** Données de base  
**Pages PDF:** exercice 111-112; solution 113-114

## Énoncé


### Page 111

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

### Page 112

```text
Chapitre 4 : Données de base

4. Comment pouvez-vous vérifier l'auteur et la date de création de la fiche partenaire dans le
système ?

5. Pouvez-vous gérer diverses adresses pour le client en fonction des sociétés dans la fiche
partenaire ?
```

## Solution SAP du support


### Page 113

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

### Page 114

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

# Exercice 11 - Création d’une fiche article

**Chapitre:** Données de base  
**Pages PDF:** exercice 119-120; solution 121-125

## Énoncé


### Page 119

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

### Page 120

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

## Solution SAP du support


### Page 121

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

### Page 122

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

### Page 123

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

### Page 124

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

### Page 125

```text
Sujet: Gestion des données de base article

La figure « Ventes propres à un secteur d'activité » illustre les restrictions des ventes propres
au secteur d'activité.

Figure 47: Ventes propres à un secteur d'activité
```

---

# Exercice 12 - Création d’une fiche infos client-article

**Chapitre:** Données de base  
**Pages PDF:** exercice 129-130; solution 131-132

## Énoncé


### Page 129

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

### Page 130

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Point d'expédition                     Z0##

Date de création planifiée                Échue la semaine prochaine

Numéro de livraison : ____________________________________________

5. Vérifiez si la désignation de l'article client apparaît dans la livraison sortante.
```

## Solution SAP du support


### Page 131

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

### Page 132

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

# Exercice 13 - Création d’un enregistrement de condition (prix de vente)

**Chapitre:** Données de base  
**Pages PDF:** exercice 137-138; solution 139-140

## Énoncé


### Page 137

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

### Page 138

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

## Solution SAP du support


### Page 139

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

### Page 140

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

# Exercice 14 - Création d’un enregistrement de condition (remise)

**Chapitre:** Données de base  
**Pages PDF:** exercice 141-142; solution 143-144

## Énoncé


### Page 141

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

### Page 142

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

## Solution SAP du support


### Page 143

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

### Page 144

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

# Exercice 15 - Description du contexte des données de base de condition

**Chapitre:** Données de base  
**Pages PDF:** exercice 145-145; solution 146-146

## Énoncé


### Page 145

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

## Solution SAP du support


### Page 146

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

# Exercice 16 - Création de postes par défaut

**Chapitre:** Données de base  
**Pages PDF:** exercice 155-156; solution 157-160

## Énoncé


### Page 155

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

### Page 156

```text
Chapitre 4 : Données de base

Nom de zone                             Valeur

Donneur d'ordre                      T-S50A##

Réf. client                           ##-Proposition

5. Sauvegardez la commande client et notez son numéro.
______________________________________________________
```

## Solution SAP du support


### Page 157

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

### Page 158

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

### Page 159

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

### Page 160

```text
Chapitre 4 : Données de base
```

---

# Exercice 17 - Gestion des documents de vente incomplets

**Chapitre:** Données de base  
**Pages PDF:** exercice 161-161; solution 162-164

## Énoncé


### Page 161

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

## Solution SAP du support


### Page 162

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

### Page 163

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

### Page 164

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

# Exercice 18 - Vérification des résultats de la détermination automatique des données

**Chapitre:** Détermination automatique des données et ordonnancement  
**Pages PDF:** exercice 179-180; solution 181-183

## Énoncé


### Page 179

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

### Page 180

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

## Solution SAP du support


### Page 181

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

### Page 182

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

### Page 183

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

# Exercice 19 - Vérification des résultats de l’ordonnancement de l’expédition et du transport

**Chapitre:** Détermination automatique des données et ordonnancement  
**Pages PDF:** exercice 189-190; solution 191-193

## Énoncé


### Page 189

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

### Page 190

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

## Solution SAP du support


### Page 191

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

### Page 192

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

### Page 193

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

# Exercice 20 - Vérification des principaux facteurs influençant le contrôle de disponibilité

**Chapitre:** Contrôle de disponibilité  
**Pages PDF:** exercice 205-205; solution 206-210

## Énoncé


### Page 205

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

## Solution SAP du support


### Page 206

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

### Page 207

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

### Page 208

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

### Page 209

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

### Page 210

```text
Chapitre 6 : Contrôle de disponibilité

Figure 72: Accord de livraison partielle

Vous pouvez modifier les paramètres manuellement lorsque vous saisissez une commande
client. Cela peut s'avérer nécessaire si un client préfère généralement des livraisons
complètes (gérées dans les données de base du partenaire) mais autorise une livraison
partielle pour une commande particulière.
```

---

# Exercice 21 - Vérification du transfert des besoins

**Chapitre:** Contrôle de disponibilité  
**Pages PDF:** exercice 211-211; solution 212-214

## Énoncé


### Page 211

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

## Solution SAP du support


### Page 212

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

### Page 213

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

### Page 214

```text
Chapitre 6 : Contrôle de disponibilité
```

---

# Exercice 22 - Vérification des options des livraisons complètes ou partielles

**Chapitre:** Contrôle de disponibilité  
**Pages PDF:** exercice 215-216; solution 217-218

## Énoncé


### Page 215

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

### Page 216

```text
Chapitre 6 : Contrôle de disponibilité

5. Quelles sont les données de base utilisées pour proposer le code LivrPart/poste dans le
poste de commande ?

6. Est-il possible de répartir la quantité totale d'un poste de commande entre plusieurs
livraisons si le code Livraison complète n'est pas sélectionné dans l'en-tête de la
commande ?
```

## Solution SAP du support


### Page 217

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

### Page 218

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

# Exercice 23 - Exécution des contrôles de disponibilité

**Chapitre:** Contrôle de disponibilité  
**Pages PDF:** exercice 227-228; solution 229-232

## Énoncé


### Page 227

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

### Page 228

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

## Solution SAP du support


### Page 229

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

### Page 230

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

### Page 231

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

### Page 232

```text
Chapitre 6 : Contrôle de disponibilité
```

---

# Exercice 24 - Description des fonctions du contrôle de disponibilité

**Chapitre:** Contrôle de disponibilité  
**Pages PDF:** exercice 233-233; solution 234-237

## Énoncé


### Page 233

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

## Solution SAP du support


### Page 234

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

### Page 235

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

### Page 236

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

### Page 237

```text
Sujet: Exécution d'un contrôle de disponibilité – Autres sujets

Figure 82: Traitement des reliquats – Exemple
```

---

# Exercice 25 - Création des livraisons sortantes via une opération groupée

**Chapitre:** Opération groupée  
**Pages PDF:** exercice 249-249; solution 250-252

## Énoncé


### Page 249

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

## Solution SAP du support


### Page 250

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

### Page 251

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

### Page 252

```text
Chapitre 7 : Opération groupée
```

---

# Exercice 26 - Achèvement des fonctions d’expédition via une opération groupée

**Chapitre:** Opération groupée  
**Pages PDF:** exercice 253-253; solution 254-258

## Énoncé


### Page 253

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

## Solution SAP du support


### Page 254

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

### Page 255

```text
Sujet: Exécution d’opérations groupées

d) Sélectionnez Prélevé, sélectionnez tous les postes à nouveau, puis cliquez sur Sortie
de marchandises.

e) Répétez ces étapes pour les autres ordres de livraison sortante.
```

### Page 256

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

### Page 257

```text
Sujet: Exécution d’opérations groupées

La figure « Options de facturation » montre les options les plus fréquemment utilisées pour la
création de documents de facturation via une opération groupée.

Figure 88: Options de facturation
```

### Page 258

```text
Chapitre 7 : Opération groupée
```

---

# Exercice 27 - Création de documents de facturation à l’aide d’une opération groupée

**Chapitre:** Opération groupée  
**Pages PDF:** exercice 259-260; solution 261-262

## Énoncé


### Page 259

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

### Page 260

```text
Chapitre 7 : Opération groupée

____________________________________________________________

____________________________________________________________
```

## Solution SAP du support


### Page 261

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

### Page 262

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

# Exercice 28 - Création de documents d’avant-vente

**Chapitre:** Processus supplémentaires dans les ventes  
**Pages PDF:** exercice 271-272; solution 273-276

## Énoncé


### Page 271

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

### Page 272

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

## Solution SAP du support


### Page 273

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

### Page 274

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

### Page 275

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

### Page 276

```text
Chapitre 8 : Processus supplémentaires dans les ventes
```

---

# Exercice 29 - Description du traitement des documents d’avant-vente

**Chapitre:** Processus supplémentaires dans les ventes  
**Pages PDF:** exercice 277-277; solution 278-278

## Énoncé


### Page 277

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

## Solution SAP du support


### Page 278

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

# Exercice 30 - Exécution de la fabrication sur commande

**Chapitre:** Processus supplémentaires dans les ventes  
**Pages PDF:** exercice 283-285; solution 286-290

## Énoncé


### Page 283

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

### Page 284

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

### Page 285

```text
Sujet: Exécution de la fabrication sur commande

15. Pour finir, revérifiez la couverture article. Les besoins en articles sont-ils toujours
valables ?
___________________________
```

## Solution SAP du support


### Page 286

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

### Page 287

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

### Page 288

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

### Page 289

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

### Page 290

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

# Exercice 31 - Vente d’un produit de service

**Chapitre:** Processus supplémentaires dans les ventes  
**Pages PDF:** exercice 293-294; solution 295-296

## Énoncé


### Page 293

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

### Page 294

```text
Chapitre 8 : Processus supplémentaires dans les ventes

6. Sauvegardez la commande client et notez le numéro de document.
_____________________________

7. Pour terminer le processus, créez la facture avec référence à la commande client. Utilisez
votre client comme critère de sélection et aujourd'hui + 14 jours en tant que valeur pour la
zone Date de la facture jusqu'au. Notez le numéro du document.
_____________________________
```

## Solution SAP du support


### Page 295

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

### Page 296

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

# Exercice 32 - Création d’une demande d’avoir

**Chapitre:** Gestion des réclamations  
**Pages PDF:** exercice 309-310; solution 311-314

## Énoncé


### Page 309

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

### Page 310

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

## Solution SAP du support


### Page 311

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

### Page 312

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

### Page 313

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

### Page 314

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

# Exercice 33 - Annulation d’un document de facturation

**Chapitre:** Gestion des réclamations  
**Pages PDF:** exercice 317-317; solution 318-318

## Énoncé


### Page 317

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

## Solution SAP du support


### Page 318

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

# Exercice 34 - Création d’un retour

**Chapitre:** Gestion des réclamations  
**Pages PDF:** exercice 323-323; solution 324-325

## Énoncé


### Page 323

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

## Solution SAP du support


### Page 324

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

### Page 325

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

# Exercice 35 - Utilisation de l’application Traitement des commandes clients

**Chapitre:** Suivi et analyse des ventes  
**Pages PDF:** exercice 337-337; solution 338-339

## Énoncé


### Page 337

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

## Solution SAP du support


### Page 338

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

### Page 339

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

# Exercice 36 - Analyse des données à l’aide des applications analytiques

**Chapitre:** Suivi et analyse des ventes  
**Pages PDF:** exercice 347-347; solution 348-349

## Énoncé


### Page 347

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

## Solution SAP du support


### Page 348

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

### Page 349

```text
Sujet: Utilisation d'applications analytiques

6. Enfin, exportez le rapport dans Microsoft Excel (sans sauvegarder le fichier).
a) Revenez à la page à onglet Analyse des données.

b) Pour exporter les données, sélectionnez Exporter, puis Exporter en tant que Feuille de
calcul Excel.
```
