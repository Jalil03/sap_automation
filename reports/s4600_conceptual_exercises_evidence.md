# S4600 — réponses vérifiées des exercices conceptuels

Source unique : [énoncés et solutions S4600](../data/books/S4600/S4600_EXERCISES.md). Ce document répond aux questions écrites ; aucun résultat SAP live ni personnalisation utilisateur n'est revendiqué.

## Questions exactes et périmètre

Retours de ligne du Markdown source réunis, sans changement des questions. Les réponses numérotées ci-dessous suivent cet ordre.

**Exercice 2, tâche 1 :**

1. Quelle entité organisationnelle dans la comptabilité financière représente une entité juridique et une unité comptable indépendante dans le système ?
2. Quelle entité organisationnelle représente une filiale ou un service commercial ?
3. Quelle entité organisationnelle représente un mode de distribution de marchandises au client (par exemple, ventes usine, commerce de gros ou commerce de détail) ?
4. Quelle entité organisationnelle représente différentes lignes de produits et regroupe des articles (par exemple, véhicules, accessoires ou pièces de rechange) ?
5. Quelle entité organisationnelle représente un site de fabrication ou un centre de distribution ?
6. Dans une division, le stockage des articles peut être réparti entre divers emplacements ou locaux. Quelle entité organisationnelle représente un tel emplacement ou local ?
7. Quelle entité organisationnelle est obligatoire pour organiser et traiter les livraisons sortantes aux différents points (par exemple, rampe de chargement de véhicules ou dépôt de chemin de fer) ?
8. Quelle entité organisationnelle représente un magasin physique ?

**Exercice 2, tâche 2 :**

1. Quelles entités organisationnelles sont des composants d'un domaine commercial ?
2. À quelle entité organisationnelle une organisation commerciale est-elle affectée pour représenter le lien entre les processus des ventes et la comptabilité financière ?
3. À quelle entité organisationnelle un point d'expédition est-il affecté ?
4. Quelle entité organisationnelle permet de regrouper des magasins ?
5. À quelles entités organisationnelles les numéros de magasin sont-ils affectés ?
6. À quelles entités organisationnelles les divisions chargées de la livraison sont-elles affectées ?

**Exercice 15 :**

1. Quelles classes de données de base de condition (4) peuvent être utilisées pour la détermination du prix ?
2. Vous souhaitez vendre des articles via divers canaux de distribution. Est-il possible de gérer les prix dans les enregistrements de condition de différentes façons en fonction du canal de distribution ?
3. Vous avez saisi une commande client. Les prix ont été définis par la fonction de détermination automatique du prix. Pouvez-vous modifier les prix manuellement lors de la saisie de la commande client ?

**Exercice 24 :**

1. Pourquoi le résultat d'un contrôle de disponibilité dans la commande client peut-il dépendre d'un accord de livraison partielle ?
2. Pourquoi faut-il que l'ordonnancement de l'expédition soit réalisé avant le contrôle de disponibilité dans la commande client ?
3. Pourquoi l'ordonnancement de l'expédition est-il réalisé après le contrôle de disponibilité si le poste ne peut être confirmé pour la date de livraison souhaitée ?

**Exercice 29 :**

1. Indiquez certaines des différences existant entre une demande et une offre.
2. Une demande d'offre doit-elle être enregistrée avant de pouvoir créer une offre ?
3. La détermination automatique du prix a-t-elle lieu pendant la saisie d'offres ou de demandes d'offres client ?
4. Pouvez-vous effectuer le contrôle de disponibilité dans une demande d'offre ou une offre client comme dans une commande client ?

Ces quatre énoncés demandent des réponses conceptuelles, pas une connexion ou une saisie SAP. Les vérifications concernent les 24 réponses, pas l'exécution ultérieure de leurs processus.

## Exercice 2 — structures organisationnelles

Tâche 1 (questions 1 à 8) : **société** (entité juridique et comptable indépendante) ; **organisation commerciale** (filiale/service commercial) ; **canal de distribution** (mode de vente au client) ; **secteur d'activité** (ligne de produits) ; **usine** (le support l'appelle « division » dans ce passage : site de fabrication/distribution) ; **emplacement de stockage** (le support l'appelle « magasin » : local dans l'usine) ; **point d'expédition** (traitement des livraisons sortantes) ; **numéro de magasin/warehouse** (magasin physique).

Tâche 2 (questions 1 à 6) : domaine commercial = organisation commerciale + canal de distribution + secteur d'activité ; organisation commerciale → société ; point d'expédition → usine ; emplacements de stockage → usine ; numéro de magasin → combinaison usine/emplacement ; usines livrantes → combinaison organisation commerciale/canal de distribution. La terminologie du support « division » dans les réponses logistiques désigne **plant**, pas `sales_division`.

Vérification : les 14 réponses correspondent à la solution du support (pages indiquées 42–43). **COMPLETED_AND_VERIFIED** pour les questions conceptuelles ; pas de validation de configuration SAP implicite.

## Exercice 15 — données de condition

1. Les quatre classes demandées sont **prix, majorations/remises, fret et taxes**.
2. **Oui.** Le prix peut dépendre de l'organisation commerciale et du canal de distribution, et aussi d'autres critères tels que le client.
3. **Généralement oui**, on peut modifier un prix automatiquement déterminé pendant la saisie d'une commande ; le Customizing ou l'enregistrement de condition peut limiter cette modification.

Vérification : les trois réponses correspondent à la solution page 146. **COMPLETED_AND_VERIFIED** pour les questions ; cela ne prouve pas que les conditions S4600 existent en SAP.

## Exercice 24 — contrôle de disponibilité

1. Si seule une quantité partielle est disponible à la date demandée, un accord autorisant les livraisons partielles permet de confirmer cette quantité à cette date ; sinon, la quantité complète doit attendre une date ultérieure.
2. L'ordonnancement doit d'abord calculer la date de mise à disposition de l'article à partir de la date de livraison demandée et des durées d'emballage, prélèvement, chargement et transport : l'ATP contrôle la disponibilité à cette date de mise à disposition.
3. Si cette date ne permet pas la confirmation, le système ordonnance en aval depuis la première date de mise à disposition possible pour calculer une date de livraison confirmable.

Vérification : les trois réponses correspondent à la solution page 234. **COMPLETED_AND_VERIFIED** pour les questions ; aucun ATP live n'a été exécuté.

## Exercice 29 — documents d'avant-vente

1. Une **demande** exprime les questions du client sur prix, date, etc. ; une **offre** fournit la réponse et engage pendant sa période de validité. La validité de la demande borne le délai de réponse.
2. **Non**, une offre peut être créée sans demande préalable.
3. **Oui**, une détermination automatique du prix peut intervenir dans les demandes et offres, selon le Customizing.
4. **Oui**, un contrôle de disponibilité peut être effectué dans les deux types de documents, selon le Customizing.

Vérification : les quatre réponses correspondent à la solution page 278. **COMPLETED_AND_VERIFIED** pour les questions ; les types de document installés ne sont pas présumés présents.
