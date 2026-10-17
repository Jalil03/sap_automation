# État actuel de l'environnement SAP de formation — S4615 et S4650

**Date du récapitulatif : 17 octobre 2026.** Système autorisé : **A4H**, mandant **600**, utilisateur technique **ABDELJ**. Transport de Customizing utilisé lorsque nécessaire : **A4HK908422** (non libéré). Ce document synthétise les preuves et suivis déjà présents ; il ne constitue **pas** une nouvelle validation live et aucune écriture SAP n'a été effectuée pour le produire.

## Vue d'ensemble

| Périmètre | Situation actuelle |
|---|---|
| Socle commercial S4615 | Société 1010, organisation commerciale 1010, affectations 1010/10/00 et domaine commercial 1010/10/00 vérifiés. Détermination de prix, variante d'exercice et catégorie de poste BV nécessaires au test initial vérifiées. |
| Données S4615 utilisateur 00 | Client logique `C615-D00` et produit logique `P615-400` créés sous des numéros SAP internes et mappés. Le produit n'a pas les vues comptables/valorisation nécessaires au BV Sales Order ; blocage SAP `C+039` lors de l'extension. |
| Données S4615 groupe 01 | Types `ZA01` et `ZF01` persistés et vérifiés ; les deux champs de facturation de `ZA01` pointent vers `ZF01`. Client `C615-A01` et article `P615-101` non créés : aucune référence de formation sûre et équivalente n'a été établie pour les copier. |
| S4650 groupe 01 | Groupe `01` choisi, canal cible `D1` libre. Exercice 5 terminé par vérification du contrôle de copie existant. Exercice 1 bloqué par l'absence de la division commerciale globale `03` ; `D1` et les domaines commerciaux cibles n'ont pas été créés. Produit `P650-101` non utilisable. |
| Exercices complets | **S4615 : 0/13** ; **S4650 : 1/13**. Les éléments de configuration déjà prêts ne suffisent pas, seuls, à valider un exercice de bout en bout. |

## Environnement et données vérifiées

### Organisation et Customizing S4615

| Objet / réglage | État connu | Preuve et limite |
|---|---|---|
| Société `1010` | EXISTS | Créée depuis `BE01`, vérifiée après réouverture ; plan comptable `CABE`, variante d'exercice `K4`. |
| Organisation commerciale `1010` | EXISTS | Vérification live. |
| `1010` → société `1010` | EXISTS | Affectation vérifiée. |
| Canal `10` → organisation `1010` | EXISTS | Affectation vérifiée. |
| Secteur commercial `00` → organisation `1010` | EXISTS | Affectation vérifiée. |
| Domaine commercial `1010/10/00` | EXISTS | Créé et vérifié ; accepté ensuite par la création de la vue client. |
| Compte collectif client `400000` en société `1010` | EXISTS | Point de contrôle humain vérifié ; compte client, EUR. |
| OVKK `1010/10/00 + A + 02 → A17J02` | EXISTS | Vérification live. |
| VOV4/T184 `BV/CB04/∅/∅ → CBTA` | EXISTS | Sauvegarde et lecture indépendante. |
| Type de commande `ZA01` | EXISTS | Copié de `CS`, sauvegardé, retrouvé après réouverture VOV8 ; livraison `LF`, `FKARV=ZF01`, `FKARA=ZF01`. |
| Type de facture `ZF01` | EXISTS | Copié de `F2`, plage interne `15`, retrouvé après réouverture VOFA. Ne pas recréer. |

La plage `15` et la configuration `ZF01` ne prouvent pas encore qu'une facture `ZF01` issue du flux de formation a été créée : **aucune chaîne ZA01 → LF → PGI → ZF01 n'a été exécutée**.

### Identités et données de base S4615

| ID logique du support | ID SAP vérifié | État et limites |
|---|---|---|
| `C615-D00` | Business Partner / client `1000000114` | Mapping `LIVE_VERIFIED`. Rôles FLCU00/FLCU01, vue société `1010`, vue commerciale `1010/10/00` et adresse `1557` vérifiés. C'est le client du scénario de vente au comptant utilisateur 00, **pas** un modèle fonctionnel prouvé pour `C615-A01`. |
| `P615-400` | Article `10000287` | Mapping `LIVE_VERIFIED`. Racine FERT/M, unité `PC`, division `00`, groupe de catégorie de poste `CB04`, usine `1710`, vente `1010/10`, usine livreuse `1710`, disponibilité `SP`, groupe d'imputation `03` et taxe `BE/MWST/1` vérifiés. **Vues Accounting 1/2 et valorisation manquantes** ; article explicitement exclu comme modèle pour `P615-101`. |
| `C615-A01` | Aucun mapping | ID exact absent des contrôles ciblés ; aucune création. |
| `P615-101` | Aucun mapping | ID exact absent des contrôles ciblés ; aucune création. |

Les mappings officiels sont dans [`data/provisioning/phase5_identity_mappings.json`](../data/provisioning/phase5_identity_mappings.json). Le support canonique conserve ses identifiants et ses `##` ; les numéros SAP internes ne s'y substituent pas. L'article provisoire `10000286` n'a jamais été persisté et ne doit pas être réutilisé.

## Blocages actifs et conséquences

| Blocage | Fait confirmé | Conséquence / condition de reprise |
|---|---|---|
| **C+039 — Material Ledger / usine 1710** | La tentative MM01 d'ajouter Accounting 1/2 à `10000287` s'arrête avant sauvegarde : « Les devises du ledger articles ont été modifiées ». Les vues de valorisation et ML du produit sont absentes. | Le POST BV précédent a échoué avec SAP `V4/210` (« Aucune donnée de comptabilité gérée pour l'article »), sans créer de commande. Ne pas relancer ce POST avant résolution FI/CO/ML approuvée et lecture ciblée de la valorisation. Ne pas modifier ici `10000287`, `1710`, C+039 ou le Material Ledger. |
| **Client `C615-A01` manquant** | Aucun client `C61*` ni BP nommé `S61` trouvé par recherches ciblées. Dans la vue commerciale `1010/10/00`, seul `1000000114` a été retourné. Sa fonction et son adresse de vente au comptant D00 ne prouvent pas l'équivalence requise pour A01. | Trouver une référence de formation sûre avec données client/adresse/vues adéquates, ou établir les valeurs métier et le contrat de création minimal. Ne pas copier arbitrairement D00. |
| **Produit `P615-101` manquant** | Aucun produit `P61*` ni description `S61` trouvé. Dans la vue vente `1010/10`, le seul produit retourné est `10000287`, interdit comme source. | Trouver une référence de formation équivalente utilisable sans Accounting/valorisation 1710, ou établir un autre chemin sûr ; aucune création ni commande ZA01 ne peut être revendiquée à ce stade. Ces recherches bornées ne prouvent pas l'absence de toute référence ailleurs dans SAP. |
| **Division commerciale globale `03` absente** | Scan complet `V_TSPA` S4650 : `03` absente, `00` présente. | S4650 exercice 1 et ses domaines `1010/D1/00` et `/03` restent bloqués. La création de `03`, objet global, n'était pas autorisée dans le périmètre de cet exercice ; ne pas la créer implicitement. |
| **Produit S4650 `P650-101` inutilisable** | MM02 : « L'article P650-101 n'existe pas ou n'est pas activé ». Les recherches ciblées de références `P650-*`/`S650` n'ont pas établi de modèle sûr. | Empêche directement plusieurs tests S4650 et leurs successeurs. Le contrôle MM02 ne distingue pas absence et inactivité. |
| **Documents de formation préchargés non retrouvés** | GET ciblés des références utilisateur 00 `00S4615-A1/A3/A4/A5/A6/A10` : zéro commande. Les références exactes ne prouvent pas qu'aucun objet équivalent n'existe ailleurs. | Les exercices correspondants ne sont pas achevés ; un objet équivalent ne peut être réutilisé que si son comportement et son rattachement au scénario sont démontrés. |

Le réglage `FINSC_001A` `1710/30/10/M/2` a été sauvegardé et relu antérieurement, mais **n'a pas levé C+039**. Aucune procédure d'initialisation ou modification globale de devise n'est autorisée par ce constat. Le blocage C+039 concerne directement la branche BV de S4615 ; les exercices S4650, tels qu'écrits, ne demandent pas la correction de cet article et ne sont pas classés bloqués par C+039.

## Avancement des exercices

### S4615 — 0 terminés / 12 bloqués / 1 restant partiel

- **Exercice 2 : partiel.** La navigation SPRO → SIMG a été vérifiée ; les préférences et Favoris du compte de formation `S4615-##` ne l'ont pas été depuis la session technique ABDELJ.
- **Exercice 3 : configuration partielle prête.** `ZA01` et `ZF01` sont persistés, avec les deux champs de facturation corrects. La chaîne requiert encore `C615-A01` et `P615-101` ; aucune commande, livraison, sortie de marchandises ou facture du scénario n'a été créée.
- **Exercice 5 : bloqué par C+039.** La commande BV utilisateur 00 n'existe pas ; le dernier POST a échoué sans ID de commande.
- **Exercices 1, 4 et 6–13 : bloqués** par leurs documents exacts non retrouvés, données de formation non prouvées ou dépendances transactionnelles. Pour le détail exercice par exercice, voir [`books/S4615/S4615_PROGRESS.md`](../books/S4615/S4615_PROGRESS.md).

### S4650 — 1 terminé / 12 bloqués

- **Groupe `01`**, canal cible `D1` : `D1` libre, domaines `1010/D1/00` et `1010/D1/03` libres ; **aucun des trois n'a été créé**. L'exercice 1 reste bloqué par `03` absent.
- **Exercice 5 terminé** : contrôle de copie existant `F2 ← LF`, exigence en-tête `003`, poste `TAN` avec source de prix `E`, vérifié sans écriture.
- **Exercices 2–4 et 6–13 bloqués** par la dépendance à l'exercice 1, à `P650-101`, aux données/transactions de groupe ou à des sorties non vérifiées. Voir [`books/S4650/S4650_PROGRESS.md`](../books/S4650/S4650_PROGRESS.md).

## Prochaines décisions utiles

1. **S4615 groupe 01 :** fournir ou établir une référence client et une référence produit de formation réellement équivalentes, avec les vues nécessaires et sans recourir à `10000287` ni à la valorisation 1710. Refaire un LOOKUP ciblé avant chaque éventuelle création, puis une lecture indépendante après sauvegarde.
2. **S4615 utilisateur 00 :** faire traiter C+039 par l'administrateur FI/CO Material Ledger dans un changement séparé et contrôlé ; vérifier ensuite les vues Accounting/valorisation de `10000287` avant de reconsidérer la commande BV. Ce sujet ne doit pas être mêlé au bootstrap A01/P101.
3. **S4650 :** obtenir une décision explicite sur la division globale `03` ; établir séparément une référence sûre pour le produit de groupe `P650-101`. Ne pas créer de configuration globale ou de données arbitraires pour contourner ces absences.

## Sources de ce récapitulatif

[`docs/phase5/CURRENT_STATE.md`](../docs/phase5/CURRENT_STATE.md), [`docs/phase5/BLOCKERS.md`](../docs/phase5/BLOCKERS.md), [`docs/phase5/DECISIONS.md`](../docs/phase5/DECISIONS.md), les deux fichiers `books/*/*_PROGRESS.md`, [`data/books/S4650/S4650_PROGRESS.md`](../data/books/S4650/S4650_PROGRESS.md) et le fichier de mappings cité plus haut. En cas de contradiction chronologique, le **dernier readback vérifié** et le suivi d'exercice le plus récent priment sur une ancienne tentative ou un ancien « prochain pas ».
