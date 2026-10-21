# A4H/600 — inventaire des changements SAP et audit C+039

**Périmètre :** traces locales des phases/exercices S4600, S4610, S4615, S4620 et S4650, rapprochées des lectures SAP ciblées SCU3/SE09 déjà capturées. **Mode : lecture seule.** Aucun changement SAP n'a été effectué pour cet inventaire. Les horodatages du bridge sont en UTC ; le fuseau des heures affichées par SAP/SCU3 n'est pas démontré. `UNKNOWN` signifie que la preuve manque, pas que l'opération n'a pas eu lieu.

## Synthèse

Le [journal détaillé CSV](sap_all_changes_inventory.csv) comporte **46 lignes, une par écriture effective, étape de sauvegarde intermédiaire ou tentative de write rejetée/abandonnée** ; il n'inclut pas les dry-runs et GET. On distingue **17 entités/relations créées et encore vérifiées par l'automatisation**, dont l'adresse 1583 générée en effet de bord de la création du point d'expédition (incluse dans la ligne de création OVXD, pas une deuxième commande) ; **une configuration FINSC_001A finale modifiée/reconstituée** après **une suppression intermédiaire**. Trois créations D00 sont réelles et vérifiées, mais la trace brute permettant d'attribuer le POST à notre automate n'a pas été retrouvée ; elles ne sont **pas** ajoutées au chiffre 17. Les checkpoints humains et la modification T000 par WBS601 restent séparés. Ces nombres ne constituent pas un comptage exhaustif certifié par les journaux de changement SAP : il manque la liste E071/E071K du transport et certaines traces OData historiques.

Les recherches dans [les traces du bridge](../logs/sap_gui_bridge/actions.jsonl), [les mappings](../data/provisioning/phase5_identity_mappings.json), [l'état Phase 5](../docs/phase5/CURRENT_STATE.md) et les fichiers de progression n'ont fourni **aucune écriture attribuable à notre workflow pour S4600, S4610, S4620 ou S4650**. L'exercice 5 S4650 marqué terminé correspond à une lecture de configuration préexistante, non à sa création par nous ([progression S4650](../books/S4650/S4650_PROGRESS.md)). Une absence de trace locale ne prouve pas, à elle seule, une absence universelle de changement SAP.

## Table des objets/changements persistés

La colonne « état » signifie **dernier readback documenté**, non GET renouvelé au moment de rédiger ce rapport. Voir le CSV pour chaque opération, les tentatives et les horodatages disponibles.

| ID SAP / clé | Type et action | Origine | État documenté | Preuve |
|---|---|---|---|---|
| `1010` | Société, création par copie de BE01 | automate, V_T001 | existe après sortie/réentrée | [état Phase 5](../docs/phase5/CURRENT_STATE.md), [bridge](../logs/sap_gui_bridge/actions.jsonl) |
| `1010` | Organisation commerciale, copie de 1710 ; libellé S4615 Training, EUR | automate, V_TVKO | existe | mêmes sources |
| `1010→1010`, `1010/10`, `1010/00` | Affectations commerciale→société, canal→organisation, division→organisation | automate, IMG | existent | [état Phase 5](../docs/phase5/CURRENT_STATE.md) |
| `BV/CB04/∅/∅→CBTA` | Détermination de catégorie de poste VOV4 | automate | existe | [état Phase 5](../docs/phase5/CURRENT_STATE.md), [bridge](../logs/sap_gui_bridge/actions.jsonl) |
| `1710/30` | FINSC_001A : création/sauvegarde, suppression de la ligne intermédiaire, recréation/correction | automate, FINSC_LEDGER | `source=10`, `rate=M`, `date=2`, conversion temps réel active après lecture SE16N | [état Phase 5, lignes 99–103](../docs/phase5/CURRENT_STATE.md), [bridge](../logs/sap_gui_bridge/actions.jsonl) |
| `ZF01` | Type de facture copié de F2 ; catégorie M, plage interne 15 | automate, VOFA | existe après réouverture | [progression S4615](../books/S4615/S4615_PROGRESS.md), [bridge](../logs/sap_gui_bridge/actions.jsonl) |
| `ZA01` | Type de commande copié de CS ; `FKARV=ZF01`, `FKARA=ZF01`, livraison LF | automate, VOV8 | existe après réouverture | [progression S4615](../books/S4615/S4615_PROGRESS.md), [bridge](../logs/sap_gui_bridge/actions.jsonl) |
| `1000000115` | BP racine `C615-A01` | automate, API_BUSINESS_PARTNER | existe, ID logique mappé | [tentative BP](../data/provisioning/s4615/C615-A01.bp_root_attempt.json), [mapping](../data/provisioning/phase5_identity_mappings.json) |
| `1581`; `1000000115/FLCU00`; `1000000115/FLCU01` | Adresse standard puis rôles BP | automate, GUI BP et OData | adresse XXDEFAULT, rôles présents | [checkpoint A01](../data/provisioning/s4615/C615-A01.workflow_checkpoint.json), [tentative adresse](../data/provisioning/s4615/C615-A01.bp_address_attempt.json) |
| `1000000115/1010`; `1000000115/1010/10/00` | Extensions société (`400000`, `0004`) et vente (`EUR`, livraison `01`, prix `02`, groupe `01`, CFR/Bruxelles) | automate, OData | existent après GET indépendant | [tentative société](../data/provisioning/s4615/C615-A01.company.attempt.json), [tentative vente](../data/provisioning/s4615/C615-A01.sales_area.attempt.json) |
| `10000289` | Racine/basic data `P615-101`, FERT/M, PC, division 00 | automate, MM01 | existe ; **aucune vue usine/vente/valorisation prouvée** | [checkpoint produit](../data/provisioning/s4615/P615-101.basic_root_checkpoint.json) |
| `1010`, adresse `1583` | Point d'expédition et son adresse BE | automate, OVXD | TVST/OVXD vérifiés | [checkpoint point](../data/provisioning/s4615/shipping_point_1010_be_checkpoint.json) |
| `1000000114`, `1000000114/1010`, `1000000114/1010/10/00` | BP/client `C615-D00` et extensions | workflow S4615, auteur du POST **non reconstitué** | existent ; mapping vérifié | [état Phase 5, lignes 64–75](../docs/phase5/CURRENT_STATE.md), [mapping](../data/provisioning/phase5_identity_mappings.json) |
| `1557`; `10000287`; `1010/10/00`; `400000/1010`; `1010/10/1710`; `1010/10/00/A/02→A17J02` | Adresse D00, matériel P615-400, zone de vente, compte de rapprochement, affectation usine, OVKK | **points de contrôle humains**, pas créations de l'automate | états vérifiés lors des points de contrôle ; auteur SAP détaillé non confirmé par SCU3 | [état Phase 5](../docs/phase5/CURRENT_STATE.md) |
| `1010→CABE`; variante d'exercice `1010→K4` | Modifications FI/customizing existantes | **points de contrôle humains** | valeurs constatées ; avant précis CABE inconnu, variante K4 précédemment vide | [état Phase 5](../docs/phase5/CURRENT_STATE.md) |
| `T000/600/MWAER` | **USD→XAF** | **WBS601**, SCU3 ; pas attribué à ABDELJ | changement journalisé le 14 octobre 2026 02:57:51, heure SAP/fuseau inconnu | [capture SCU3 T000](../runtime/sap_gui_responses/ef244cbb-75af-47de-b28d-eecdf36960f2.json) |

Les partenaires `DO/RF/PY/RM` d'A01 sont présents et auto-référents, mais le workflow les a classés **SKIPPED_EXISTS** : leur création n'est pas revendiquée. De même, la présence d'objets préexistants ou de valeurs copiées depuis BE01/1710/F2/CS ne constitue pas une modification de ces sources ([checkpoint A01](../data/provisioning/s4615/C615-A01.workflow_checkpoint.json)).

## Écritures annulées, refusées ou incertaines

- FINSC_001A `1710/30` : ligne intermédiaire présentant une devise dérivée XAF, puis **suppression réellement sauvegardée**, recréation et correction finale le 16 octobre. Les valeurs exactes avant la toute première sauvegarde ne sont pas démontrées ; le CSV conserve les opérations séparément ([bridge](../logs/sap_gui_bridge/actions.jsonl), [état Phase 5](../docs/phase5/CURRENT_STATE.md)).
- Quatre POST OData de commande BV pour `00S4615-BV` ont reçu HTTP 400 (`V1/212`, `KI268`, `V1/320`, `V4/210`) ; **aucun SalesOrder ID** n'est enregistré. Les 7 autres lignes du ledger sont des dry-runs, non des écritures ([ledger](../var/sap_runtime/execution_ledger.sqlite3), [état Phase 5](../docs/phase5/CURRENT_STATE.md)).
- Trois POST de rôles A01 refusés (`FSBP_ECC025` avant adresse, puis deux verrous `R1/084`) n'ont pas créé les rôles ; ceux-ci ont été créés ultérieurement par deux opérations distinctes vérifiées ([tentatives FLCU00](../data/provisioning/s4615/C615-A01.FLCU00.attempt.json), [FLCU01](../data/provisioning/s4615/C615-A01.FLCU01.attempt.json)).
- Premier Save OVXD `1010` annulé face à l'adresse obligatoire, sans persistance ; la seconde tentative approuvée `1010/BE` a créé le point ([premier checkpoint](../data/provisioning/s4615/shipping_point_1010_checkpoint.json), [second](../data/provisioning/s4615/shipping_point_1010_be_checkpoint.json)).
- `A_Product` POST P615-400 rejeté « Create not allowed » ; brouillon MM01 `10000286` non sauvegardé ; extension Accounting 1/2 de `10000287/1710` arrêtée par C+039 **avant Save**. Aucun des trois ne constitue un produit ou une vue comptable créé(e) ([état Phase 5](../docs/phase5/CURRENT_STATE.md)).

## Transport, lectures seules et limites

Le [snapshot SE09](../runtime/sap_gui_responses/252dc559-c482-4bed-9f6d-9686bb3af679.json) confirme la demande modifiable `A4HK908422`, propriétaire ABDELJ, description **S4615 Training Setup**, et tâche `A4HK908423`. Les checkpoints relient à cette demande les writes de customizing indiqués dans le CSV, mais **la liste technique des objets/clefs du transport n'a pas été obtenue** ; aucune exhaustivité transport ne peut être revendiquée. Il faut récupérer E071/E071K et l'historique d'objet si une certification d'audit est exigée. SAP documente cette distinction entre en-tête et listes d'objets dans sa [documentation CTS](https://help.sap.com/saphelp_snc700_ehp04/helpdata/en/c7/69bcd5f36611d3a6510000e835363f/content.htm).

Les opérations STATUS, INSPECT, LOOKUP, SE16N, SCU3, SE09, OData GET/`$metadata`, les dry-runs et l'exercice 5 S4650 (VTFLC) sont **des lectures**, non des lignes d'écriture du CSV. L'absence d'une entrée SCU3 ne démontre pas une absence de modification : le journal de table dépend des prérequis de journalisation SAP ([documentation SCU3](https://help.sap.com/saphelp_em92/helpdata/en/c7/69bcd2f36611d3a6510000e835363f/content.htm?no_cache=true)).

## C+039 et causalité

Voir [l'audit dédié](sap_c039_attribution.md). En bref : **notre automatisation a effectivement modifié/reconstitué FINSC_001A 1710/30 le 16 octobre**, mais **T000-MWAER USD→XAF a été journalisé le 14 octobre sous WBS601**. Cette séquence est compatible avec une contribution de notre write FINSC à l'état incohérent, sans prouver qu'il a initié C+039 ; la première occurrence exacte de C+039 et le preimage complet 1710/30 manquent. Conclusion : **INCONCLUSIVE** pour l'attribution causale, et attribution **confirmée** seulement pour nos opérations FINSC.

## Preuves encore nécessaires pour une exhaustivité certifiée

1. Liste E071/E071K et historique de `A4HK908422`/`A4HK908423`, avec clefs et auteurs de tâches ; le SE09 capturé ne montre que l'en-tête.
2. SCU3/DBTABLOG complet avec clefs `FINSC_001A 1710/30`, `T000/600` et filtres de période, plus journaux de changement de vues pertinentes. La capture FINSC du 14 octobre montre WBS601 et des delete/recreate, mais ne démontre pas la clef société complète ([capture SCU3 FINSC](../runtime/sap_gui_responses/ab2fd222-309d-4cb9-9b52-0365e7d8294a.json)).
3. Logs Gateway/OData de POST D00 et exports historiques transport pour attribuer sans réserve BP `1000000114` et ses extensions ; éventuels logs de création humaine de `10000287`, `1557` et des checkpoints FI/SD.
4. Horodatage SAP de la **première** erreur C+039, snapshot avant/après complet de FINSC 1710/30 et état ML productif au 14–16 octobre. Le fuseau SAP doit être confirmé avant comparaison absolue aux traces UTC du bridge.

**Aucun write SAP, transport release ou tentative de réparation n'a été effectué pendant cet audit.**
