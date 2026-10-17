# Phase 5A — Analyse des sources de provisioning 1010

Aucun candidat n'est sélectionné automatiquement. Le classement porte uniquement sur la complétude des preuves observées.

## COMPANY_CODE_1010

État : **MISSING** — statut : **BLOCKED_NEEDS_SOURCE**

| Tier | Candidat | Attributs observés | Confidence | Suitability |
|---:|---|---|---|---|
| 1 | AE01 | `{"company_code": "AE01", "description": "Country Template AE"}` | MEDIUM | NOT_DETERMINED |
| 1 | AR01 | `{"company_code": "AR01", "description": "Country Template AR"}` | MEDIUM | NOT_DETERMINED |
| 1 | AT01 | `{"company_code": "AT01", "description": "Country Template AT"}` | MEDIUM | NOT_DETERMINED |
| 1 | AU01 | `{"company_code": "AU01", "description": "Country Template AU"}` | MEDIUM | NOT_DETERMINED |
| 1 | BE01 | `{"company_code": "BE01", "description": "Country Template BE"}` | MEDIUM | NOT_DETERMINED |
| 1 | BR01 | `{"company_code": "BR01", "description": "Country Template BR"}` | MEDIUM | NOT_DETERMINED |
| 1 | CH01 | `{"company_code": "CH01", "description": "Country Template CH"}` | MEDIUM | NOT_DETERMINED |
| 1 | CL01 | `{"company_code": "CL01", "description": "Country Template CL"}` | MEDIUM | NOT_DETERMINED |
| 2 | 1710 | `{"company_code": "1710", "description": "Company Code 1710"}` | LOW | NOT_DETERMINED |
| 2 | 2000 | `{"company_code": "2000", "description": "BETA ENERGY LTD"}` | LOW | NOT_DETERMINED |
| 2 | 3000 | `{"company_code": "3000", "description": "GAMMA SERVICES INC"}` | LOW | NOT_DETERMINED |
| 2 | 4000 | `{"company_code": "4000", "description": "DELTA JV OIL PARTNERS"}` | LOW | NOT_DETERMINED |
| 2 | ATS0 | `{"company_code": "ATS0", "description": "Papirus france"}` | LOW | NOT_DETERMINED |
| 2 | BRCI | `{"company_code": "BRCI", "description": "BRASSIVOIRE"}` | LOW | NOT_DETERMINED |
| 2 | BRCO | `{"company_code": "BRCO", "description": "BRASCO"}` | LOW | NOT_DETERMINED |
| 2 | BRLI | `{"company_code": "BRLI", "description": "BRALIMA"}` | LOW | NOT_DETERMINED |
| 2 | CA01 | `{"company_code": "CA01", "description": "EMC-Filiale Canadienne"}` | LOW | NOT_DETERMINED |
| 2 | CA02 | `{"company_code": "CA02", "description": "CAN Tech Solutions LTd."}` | LOW | NOT_DETERMINED |
| 2 | CAN1 | `{"company_code": "CAN1", "description": "CAN Tech Solutions LTd."}` | LOW | NOT_DETERMINED |
| 2 | CAVA | `{"company_code": "CAVA", "description": "CAVANO LTD"}` | LOW | NOT_DETERMINED |

Valeurs/champs manquants :

- `approved_source_candidate_or_manual_creation_decision` — BLOCKED_NEEDS_SOURCE
- `company_name` — BLOCKED_NEEDS_VALUE
- `city` — BLOCKED_NEEDS_VALUE
- `country` — BLOCKED_NEEDS_VALUE
- `currency` — BLOCKED_NEEDS_VALUE
- `language` — BLOCKED_NEEDS_VALUE

Champs à confirmer sur le contrat live :

- all additional fields exposed by the V_T001 detail screen
- which fields are mandatory in TEST 600

## SALES_ORGANIZATION_1010

État : **MISSING** — statut : **BLOCKED_NEEDS_SOURCE**

| Tier | Candidat | Attributs observés | Confidence | Suitability |
|---:|---|---|---|---|
| 1 | 13OC | `{"description": "Org. Cciale WA11", "sales_organization": "13OC"}` | LOW | NOT_DETERMINED |
| 1 | 14OC | `{"description": "14_Org_Cciale", "sales_organization": "14OC"}` | LOW | NOT_DETERMINED |
| 1 | CI10 | `{"description": "DEFRAN CI", "sales_organization": "CI10"}` | LOW | NOT_DETERMINED |
| 1 | CM10 | `{"description": "DEFRAN CM", "sales_organization": "CM10"}` | LOW | NOT_DETERMINED |
| 1 | FR00 | `{"description": "Org. Cciale WA11", "sales_organization": "FR00"}` | LOW | NOT_DETERMINED |
| 1 | FR10 | `{"description": "Org. Cciale WA11", "sales_organization": "FR10"}` | LOW | NOT_DETERMINED |
| 1 | GN10 | `{"description": "DEFRAN GN", "sales_organization": "GN10"}` | LOW | NOT_DETERMINED |
| 1 | SCSO | `{"description": "SALES ORG SCHIBA SAC", "sales_organization": "SCSO"}` | LOW | NOT_DETERMINED |
| 1 | W100 | `{"description": "Org. Cciale WA11", "sales_organization": "W100"}` | LOW | NOT_DETERMINED |
| 2 | 0001 | `{"description": null, "sales_organization": "0001"}` | LOW | NOT_DETERMINED |
| 2 | 0003 | `{"description": null, "sales_organization": "0003"}` | LOW | NOT_DETERMINED |
| 2 | 1710 | `{"description": null, "sales_organization": "1710"}` | LOW | NOT_DETERMINED |
| 2 | CD10 | `{"description": null, "sales_organization": "CD10"}` | LOW | NOT_DETERMINED |

Valeurs/champs manquants :

- `approved_source_candidate_or_manual_creation_decision` — BLOCKED_NEEDS_SOURCE
- `description` — BLOCKED_NEEDS_VALUE
- `statistics_currency` — BLOCKED_NEEDS_VALUE

Champs à confirmer sur le contrat live :

- all additional fields exposed by the V_TVKO detail screen
- which fields are mandatory in TEST 600

## Conclusion

Live READ-only nécessaire : **YES**.

Le script live n'autorise que `STATUS` et `INSPECT`; la navigation jusqu'aux écrans de détail reste manuelle.

1710 n'est ni recommandé ni sélectionné par défaut.
