# S4650 - Exercices et solutions

Référence compacte destinée à Codex. Utiliser ce fichier en priorité; consulter `S4650_FULL_CLEAN.md` seulement si un détail manque.

## Règle de numérotation
Dans le support, `##` doit être remplacé par le numéro de groupe attribué à l’utilisateur.

## Index

| # | Chapitre | Exercice | PDF page exercice | PDF page solution |
|---:|---|---|---:|---:|
| 1 | Impact des structures organisationnelles | Développement d'une structure organisationnelle | 17 | 18 |
| 2 | Impact des structures organisationnelles | Définition des données de base partagées | 27 | 29 |
| 3 | Pilotage de la copie | Configuration du pilotage de la copie pour un document de vente | 53 | 58 |
| 4 | Pilotage de la copie | Configuration du pilotage de la copie pour un document de livraison | 69 | 71 |
| 5 | Pilotage de la copie | Configuration du pilotage de la copie pour un document de facturation | 75 | 76 |
| 6 | Pilotage de textes | Identification des sources de textes | 89 | 90 |
| 7 | Pilotage de textes | Configuration d'un pilotage de textes dans le Customizing | 109 | 111 |
| 8 | Pilotage de textes | Traitement manuel d'un texte | 117 | 118 |
| 9 | Messages | Ajustement de la détermination des messages | 137 | 139 |
| 10 | Messages | Ajustement et traitement d'une catégorie de message | 159 | 161 |
| 11 | Messages | Création d'une catégorie de message pour la confirmation de commande | 177 | 179 |
| 12 | Extensions et modifications | Utilisation de fonctions de liste standard | 213 | 215 |
| 13 | Extensions et modifications | Ajustement des options de sélection de zones | 235 | 237 |

---

# Exercice 1 - Développement d'une structure organisationnelle

**Chapitre:** Impact des structures organisationnelles  
**Pages PDF:** exercice 17-17; solution 18-20

## Énoncé


### Page 17

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

## Solution SAP du support


### Page 18

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

### Page 19

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

### Page 20

Chapitre 1: Impact des structures organisationnelles

d) Cliquez sur Reprendre.

e) Entrez la règle 1 dans les deux domaines commerciaux.

f) Sauvegardez vos données.

---

# Exercice 2 - Définition des données de base partagées

**Chapitre:** Impact des structures organisationnelles  
**Pages PDF:** exercice 27-28; solution 29-31

## Énoncé


### Page 27

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

### Page 28

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

## Solution SAP du support


### Page 29

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

### Page 30

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

### Page 31

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

# Exercice 3 - Configuration du pilotage de la copie pour un document de vente

**Chapitre:** Pilotage de la copie  
**Pages PDF:** exercice 53-57; solution 58-68

## Énoncé


### Page 53

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

### Page 54

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

### Page 55

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

### Page 56

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

### Page 57

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

## Solution SAP du support


### Page 58

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

### Page 59

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

### Page 60

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

### Page 61

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

### Page 62

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

### Page 63

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

### Page 64

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

### Page 65

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

### Page 66

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

### Page 67

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

### Page 68

Chapitre 2: Pilotage de la copie

---

# Exercice 4 - Configuration du pilotage de la copie pour un document de livraison

**Chapitre:** Pilotage de la copie  
**Pages PDF:** exercice 69-70; solution 71-74

## Énoncé


### Page 69

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

### Page 70

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

## Solution SAP du support


### Page 71

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

### Page 72

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

### Page 73

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

### Page 74

Chapitre 2: Pilotage de la copie

---

# Exercice 5 - Configuration du pilotage de la copie pour un document de facturation

**Chapitre:** Pilotage de la copie  
**Pages PDF:** exercice 75-75; solution 76-77

## Énoncé


### Page 75

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

## Solution SAP du support


### Page 76

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

### Page 77

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

# Exercice 6 - Identification des sources de textes

**Chapitre:** Pilotage de textes  
**Pages PDF:** exercice 89-89; solution 90-91

## Énoncé


### Page 89

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

## Solution SAP du support


### Page 90

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

### Page 91

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

# Exercice 7 - Configuration d'un pilotage de textes dans le Customizing

**Chapitre:** Pilotage de textes  
**Pages PDF:** exercice 109-110; solution 111-116

## Énoncé


### Page 109

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

### Page 110

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

## Solution SAP du support


### Page 111

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

### Page 112

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

### Page 113

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

### Page 114

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

### Page 115

Sujet: Configuration du pilotage de textes

5. Sauvegardez la commande et notez le numéro du document.
a) Sauvegardez la commande.
  Le numéro de commande s'affiche.

b) Notez le numéro du document.

### Page 116

Chapitre 3: Pilotage de textes

---

# Exercice 8 - Traitement manuel d'un texte

**Chapitre:** Pilotage de textes  
**Pages PDF:** exercice 117-117; solution 118-119

## Énoncé


### Page 117

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

## Solution SAP du support


### Page 118

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

### Page 119

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

# Exercice 9 - Ajustement de la détermination des messages

**Chapitre:** Messages  
**Pages PDF:** exercice 137-138; solution 139-146

## Énoncé


### Page 137

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

### Page 138

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

## Solution SAP du support


### Page 139

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

### Page 140

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

### Page 141

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

### Page 142

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

### Page 143

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

### Page 144

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

### Page 145

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

### Page 146

Chapitre 4: Messages

b) Don’t change fields on the next screen and choose Execute.

c) Set LP01 as the Output device and choose the Print Preview button.

d) If the FP_TEST_00 form is displayed in the print preview, the ADS configuration is
correct, and the printer supports PDF forms.

e) If the system displays an error message instead of form, the configuration of ADS is
incorrect

---

# Exercice 10 - Ajustement et traitement d'une catégorie de message

**Chapitre:** Messages  
**Pages PDF:** exercice 159-160; solution 161-165

## Énoncé


### Page 159

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

### Page 160

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

## Solution SAP du support


### Page 161

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

### Page 162

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

### Page 163

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

### Page 164

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

### Page 165

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

# Exercice 11 - Création d'une catégorie de message pour la confirmation de commande

**Chapitre:** Messages  
**Pages PDF:** exercice 177-178; solution 179-185

## Énoncé


### Page 177

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

### Page 178

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

## Solution SAP du support


### Page 179

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

### Page 180

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

### Page 181

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

### Page 182

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

### Page 183

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

### Page 184

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

### Page 185

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

# Exercice 12 - Utilisation de fonctions de liste standard

**Chapitre:** Extensions et modifications  
**Pages PDF:** exercice 213-214; solution 215-217

## Énoncé


### Page 213

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

### Page 214

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

## Solution SAP du support


### Page 215

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

### Page 216

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

### Page 217

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

# Exercice 13 - Ajustement des options de sélection de zones

**Chapitre:** Extensions et modifications  
**Pages PDF:** exercice 235-236; solution 237-241

## Énoncé


### Page 235

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

### Page 236

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

## Solution SAP du support


### Page 237

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

### Page 238

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

### Page 239

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

### Page 240

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

### Page 241

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