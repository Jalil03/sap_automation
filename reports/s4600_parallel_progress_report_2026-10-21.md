# Rapport d'avancement S4600 — groupe 00

Date : 21/10/2026  
Environnement autorisé : **A4H / mandant 600 / utilisateur ABDELJ**  
Périmètre : commande et livraison du chapitre 3, audits parallèles des exercices 9, 11, 28 et 31.

## Synthèse

| Élément | Statut | Résultat |
|---|---|---|
| Exercice 3 — commande client | **EXÉCUTÉ ET VÉRIFIÉ** | Commande `154`, type `CS`, domaine `FR10/10/1W`, client `1000000112`, deux postes conformes. |
| Exercice 5 — création de livraison | **EXÉCUTÉ, À TERMINER** | Livraison `80000085` créée depuis la commande `154`; les quantités et références sont conformes. Le magasin est vide sur les deux postes. |
| Exercice 9 — client `T-CUS00` | **MISSING / BLOQUÉ** | Aucun objet exact trouvé. Les décisions FI, fiscales et de numérotation FR10 restent à valider avant création. |
| Exercice 11 — produit `T-MS400` | **MISSING / BLOQUÉ** | Aucun produit exact trouvé. Le modèle, les vues, la fiscalité et le contrat de création complet restent à valider. |
| Exercice 28 — demande → offre → commande | **PARTIELLEMENT PRÊT** | Les types `DO`, `OFF.` et `CS` et les API standard existent. Le contrôle de copie exact reste `UNKNOWN`. |
| Exercice 31 — vente de service | **PARTIELLEMENT PRÊT** | Le service `90000133` existe pour FR10/10, mais `TAD`, le prix PR00 et le flux de facturation restent `UNKNOWN`. |

## 1. Chaîne commerciale exécutée

### Commande client 154

La commande a été créée et relue indépendamment :

- type de commande : `CS`;
- domaine commercial : `FR10 / 10 / 1W`;
- donneur d'ordre : `1000000112`;
- référence client : `4-200`;
- poste 10 : produit `10000282`, quantité 10 PC, montant net 1 500 EUR;
- poste 20 : produit `10000283`, quantité 20 PC, montant net 1 600 EUR;
- division et point d'expédition : `FR10`.

La preuve de lecture ne contient aucun écart.

### Livraison 80000085

Une seule création a été envoyée, après vérification de l'identité SAP, de la commande source et de l'absence de livraison préexistante. Le service a répondu HTTP 201. Le contrat utilisé suit le deep insert documenté par [SAP — Create Outbound Delivery](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/2f36056ae9a044bba55bcbad204b7bc5/ab6845012ee148ba9c2694648c2a0685.html?locale=en-US&state=PRODUCTION&version=2023.latest).

Lecture indépendante obtenue :

| Poste livraison | Référence commande | Produit | Quantité | Division | Magasin |
|---|---|---|---:|---|---|
| `000010` | `154/000010` | `10000282` | 10 PC | `FR10` | vide |
| `000020` | `154/000020` | `10000283` | 20 PC | `FR10` | vide |

La livraison est de type `LF`, avec point d'expédition `FR10` et destinataire `1000000112`. Les statuts globaux de prélèvement et de mouvement de marchandises sont encore `A`; la date réelle de mouvement est vide.

**Conclusion exercice 5 :** la livraison est créée, mais l'exercice n'est pas terminé. Le magasin `0001` doit être renseigné et relu avant le prélèvement. Aucune opération de prélèvement ni sortie de marchandises n'a été exécutée.

## 2. Audit exercice 9 — création de `T-CUS00`

Le client est classé **MISSING** : les clés exactes Business Partner et Customer répondent 404, et les recherches exactes par identifiant externe, terme de recherche et nom `Motos et autres` ne retournent aucun résultat.

La création n'est pas encore sûre, car il faut valider :

- le numéro externe littéral `T-CUS00` ou un numéro SAP interne avec mapping;
- les valeurs FR10 des conditions de paiement, d'expédition, du groupe d'imputation et du schéma client;
- le compte collectif FI;
- les classifications fiscales applicables;
- le contrat complet adresse, rôles, société et domaine commercial.

Les valeurs du client `1000000112` constituent une référence observée, mais ne sont pas une autorisation de copie.

## 3. Audit exercice 11 — création de `T-MS400`

Le produit est classé **MISSING** : la clé exacte, l'ancien identifiant et la désignation exacte `Phare standard` ne retournent aucun produit.

Le produit `10000282` peut fournir une référence technique pour FR10, mais il n'est pas sémantiquement équivalent au produit du book. Avant création, il faut donc :

- approuver explicitement ce modèle ou choisir une autre référence vérifiée;
- confirmer la numérotation;
- prouver le contrat MM01 couvrant les vues vente/usine, le magasin, le texte ADV et la quantité minimale;
- valider les décisions fiscales et de valorisation;
- créer puis relire le produit avant de traiter le prix.

Le prix PR00 de 35 EUR reste **UNKNOWN / non exécutable**. PR00 et la séquence d'accès PR02 existent, mais la lecture API des conditions échoue et le produit cible n'existe pas encore. Un contrôle VK13 exhaustif sera requis avant tout VK11.

## 4. Audit exercice 28 — demande, offre et commande

Les codes français sont confirmés :

- `AF` s'affiche `DO`;
- `AG` s'affiche `OFF.`;
- `TA` s'affiche `CS`.

Les API standard de demande et d'offre répondent correctement. Aucun historique exact n'a toutefois été trouvé pour `FR10/10/1W` et le client `1000000112`. Le contrôle de copie `AF → AG → TA` reste donc **UNKNOWN**, et non `MISSING`.

La plus petite vérification restante est une lecture GUI ciblée, sans sauvegarde, du contrôle de copie. Si elle ne suffit pas, un pilote transactionnel nécessitera une autorisation d'écriture distincte.

## 5. Audit exercice 31 — vente de service

Le produit de service `90000133` est bien présent : type `DIEN`, unité `H`, secteur `1W`, groupe de catégories `LEIS`, avec vue de vente `FR10/10`.

Trois preuves manquent encore :

1. la détermination exacte de la catégorie de poste `TAD` pour `CS + LEIS`;
2. l'existence et les valeurs complètes du prix PR00 applicable à `90000133`;
3. le contrôle de copie et le comportement de facturation liée à la commande de service.

Les prochaines lectures doivent porter sur VOV4, toutes les combinaisons installées de PR02 dans VK13, puis le paramétrage commande → facture. Toute création de prix ou de document pilote devra recevoir une autorisation séparée.

## 6. Prochain ordre de travail recommandé

1. Établir en lecture seule le contrat exact permettant d'affecter le magasin `0001` aux postes `000010` et `000020` de la livraison `80000085`.
2. Demander une autorisation ciblée pour cette modification et le prélèvement. Ne pas lancer la sortie de marchandises à ce stade.
3. Après readback du prélèvement, demander une autorisation séparée pour la sortie de marchandises, puis vérifier immédiatement le document matériel/comptable et ST22.
4. En parallèle de ces validations, terminer les lectures GUI des exercices 28 et 31.
5. Faire valider les fiches cibles de `T-CUS00` et `T-MS400` avant toute création des exercices 9 et 11.

## 7. Sécurité et portée des écritures

- Toutes les opérations ont été limitées à A4H/600/ABDELJ.
- La livraison a fait l'objet d'un lookup anti-doublon avant l'unique POST.
- L'issue a été réconciliée par lecture indépendante; aucun retry aveugle n'a été effectué.
- Aucune écriture de prélèvement, sortie de marchandises, prix, client, produit, demande, offre, facture, FI, taxe, customizing ou Material Ledger n'a été réalisée dans ce lot.
- Aucune nouvelle écriture SAP ne doit être engagée sans autorisation explicite adaptée à l'opération exacte.

## 8. Preuves et artefacts

- `runtime/sap_writes/s4600_ex3_group00_result.json`
- `runtime/sap_writes/s4600_ex5_delivery_order154_result.json`
- `runtime/sap_reads/s4600_ex5_delivery_contract_2026-10-21.json`
- `runtime/sap_reads/s4600_ex9_ex11_group00_2026-10-21.json`
- `runtime/sap_reads/s4600_ex28_ex31_audit_2026-10-21.json`
- `reports/s4600_group00_ex9_ex11_readonly_audit_2026-10-21.md`
- `reports/s4600_group00_ex28_ex31_readonly_audit_2026-10-21.md`
- `scripts/execute_s4600_ex5_order154.py`
- `scripts/audit_s4600_ex9_ex11_group00_readonly.py`
- `scripts/audit_s4600_ex28_ex31_readonly.py`
- `data/provisioning/s4600/S4600_CH3_EX5.order154.workflow_approval.json`

## Verdict final

Le travail en parallèle a accéléré l'avancement sans étendre les autorisations : la chaîne est désormais prouvée jusqu'à la création de la livraison. La priorité est de terminer proprement l'exercice 5 avec le magasin `0001`, le prélèvement, puis une sortie de marchandises séparément autorisée et contrôlée. Les exercices 28 et 31 sont les meilleurs candidats suivants après leurs dernières lectures ciblées. Les exercices 9 et 11 ne doivent pas encore être créés, car leurs valeurs cibles ne sont pas suffisamment validées.
