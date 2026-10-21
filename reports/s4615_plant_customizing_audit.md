# S4615 — audit ciblé du plant (A4H/600/ABDELJ)

**Décision : NO-GO** pour le flux non-intercompany `1010/10/00 → point d’expédition 1010 → livraison/PGI`. Aucun plant de la société `1010` ni chaîne d’affectations correspondante n’est établi dans les données live lues. Audit strictement READ-only ; aucune écriture SAP et aucune intervention sur Material Ledger ou C+039.

| Objet | Lecture live complète | Résultat ciblé |
|---|---:|---|
| `T001W` — plants | 41/41 lignes renseignées | Aucun plant avec `BWKEY=1010`. Le plant `1710` utilise `BWKEY=1710`. [Trace](../runtime/sap_gui_responses/f2c8fb11-c626-4070-b121-4bdcf842d95e.json). |
| `T001K` — aire de valorisation/société | 40/40 positions inspectées : 36 lignes renseignées, 4 vides | Aucune ligne `BUKRS=1010` ; `BWKEY=1710 → BUKRS=1710`. [Trace](../runtime/sap_gui_responses/0ae95bed-690b-4291-aea9-6bc5ba35105d.json). |
| `TVKWZ` — organisation/canal/plant | 282/282 positions inspectées : 205 lignes renseignées, 77 vides | Une seule ligne `VKORG=1010, VTWEG=10` : `WERKS=1710`. Pas d’affectation vers un plant de la société `1010`. [Trace](../runtime/sap_gui_responses/d940c103-1bb9-474e-8663-a16081578659.json). |
| `TVSWZ` — plant/point d’expédition | 54/54 lignes lues | Aucune ligne `VSTEL=1010`. Pour `WERKS=1710`, seuls `1710`, `171C`, `171R` sont observés. [Trace](../runtime/sap_gui_responses/3483a023-4f12-439b-8c2a-79c89a3080b1.json). |
| `OVL2` / `V_TVSTZ` — détermination du point d’expédition | 73/73 positions inspectées : 54 lignes renseignées, 19 vides | Aucune règle renseignée avec `VSTEL=1010`. L’écran live est `OVL2 / SAPL0VVW / 1234`, contrôle `tblSAPL0VVWTCTRL_V_TVSTZ`. [Trace](../runtime/sap_gui_responses/17f2d684-14a4-4374-8767-6ea5e2841ab9.json). |

Les totaux SAP/GUI incluent des positions vides : le nombre de lignes renseignées est indiqué séparément. La lecture GridView utilise les index absolus ; le contrôle OVL2 a été parcouru par pages bornées jusqu’à sa dernière position. Le GET `API_PLANT_SRV/A_Plant` déjà réalisé avec `CompanyCode=1010` retournait également zéro résultat ; il n’a pas été répété ici.

## Plan minimal

1. **FI/MM et propriétaire de l’environnement :** approuver un identifiant de plant de formation, son rattachement à la société `1010`, son aire de valorisation et son profil FI/MM/FERT compatible EUR et PGI. Aucun identifiant ni valeur de valorisation ne se déduit du Book. Ne pas réutiliser `1710` par défaut : il dépend de la société `1710` et exposerait un flux intercompany ; C+039 reste séparé.
2. **Customizing commercial/logistique, après approbation du plant :** préparer l’affectation `TVKWZ (1010,10,<plant>)`, puis `TVSWZ (<plant>,1010)`. Confirmer l’existence du point d’expédition `1010` lui-même, non prouvée par ces cinq tables.
3. **Détermination et validation :** définir uniquement la règle OVL2 exacte pour les valeurs de condition d’expédition et groupe de chargement effectivement retenues ; elles ne sont pas déductibles de l’audit. Vérifier ensuite le flux commande → livraison → PGI avec les données de formation, sans détour intercompany.

**Réutilisation d’un plant existant : non justifiée à ce stade.** Aucun plant n’est rattaché à `1010` dans `T001K`. Les affectations commerciales et d’expédition manquent pour le flux demandé. Les changements d’organisation/valorisation exigent une décision et une validation FI/MM ou administrateur ; les affectations commerciales/logistiques peuvent être préparées par l’équipe mais pas écrites sans cible approuvée, droits et transport vérifiés.

Le bridge a été limité aux lectures SE16N `T001W/T001K/TVKWZ/TVSWZ` et OVL2. Il force le mode affichage SE16N, utilise les contrôles observés, et n’active ni Save ni opération EXECUTE. Tests ciblés : **27/27 passés** (`tests.test_s4615_scan`, `tests.test_sap_gui_bridge`).
