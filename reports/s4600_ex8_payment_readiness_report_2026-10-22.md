# S4600 — Exercice 8 — Préparation de l'encaissement

Date de contrôle : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ

## Résultat

Statut : `BLOCKED_BOOK_DISCOUNT_AND_FR10_CASH_ACCOUNT_NOT_EVIDENCED`

L'exercice 8 demande d'enregistrer un encaissement après escompte. La facture `90000090` et sa pièce comptable `9300000009` ont été contrôlées en lecture seule.

## Valeurs vérifiées

- Total net : `3100 EUR`.
- TVA : `620 EUR`.
- Total brut et créance client : `3720 EUR`.
- Conditions de paiement : `0004`.
- Statut de rapprochement : `A`, facture ouverte/non rapprochée.
- Condition de prix `SKTO` : absente au niveau des postes et de l'en-tête.
- Taux d'escompte FI `ZBD1P` : `0.000 %`.
- Montant d'escompte `WSKTO` : `0.00 EUR`.
- Base d'escompte `SKFBT` : `0.00 EUR`.

Le montant réellement dû par le client dans l'état actuel est donc `3720 EUR`. Aucun escompte ne peut être inventé pour reproduire le calcul d'exemple du book.

## Blocages avant paiement

1. Le scénario du book exige un escompte légitime, mais la facture FR10 n'en contient aucun.
2. Le book utilise le compte général `11100000` dans la société `1010`. Son équivalent autorisé et compatible avec la société `FR10` n'est pas encore vérifié.
3. La comptabilisation d'un paiement de type `DZ` et le rapprochement de la créance constituent une écriture FI distincte qui nécessite une autorisation explicite portant sur le montant, le compte bancaire/caisse et la pièce à rapprocher.

## Plus petite action nécessaire

Décider si l'exercice doit être adapté à un paiement sans escompte de `3720 EUR`. Si oui, vérifier en lecture seule le compte de trésorerie FR10 à utiliser et le contrat exact de comptabilisation/rapprochement. Une nouvelle autorisation FI sera ensuite nécessaire avant toute écriture.

## Preuves

- `runtime/sap_reads/s4600_ex8_payment_readiness_2026-10-22.json`
- `runtime/sap_reads/s4600_ex7_accounting_document_9300000009_2026-10-22.json`
- `runtime/sap_reads/s4600_ex7_billing_90000090_reconciliation_2026-10-22.json`

## Controle complementaire apres validation de l'adaptation sans escompte

L'adaptation a un paiement sans escompte de `3720 EUR` a ete acceptee. Les controles
complementaires ont ete effectues uniquement en lecture.

- La societe `1010` utilise le plan comptable `CABE`.
- La societe `FR10` utilise le plan comptable `PCOH`.
- Le compte du book `11100000` n'existe pas dans le plan `PCOH` d'apres la lecture
  `A_GLAccountInChartOfAccounts`.
- Aucune ecriture de type `DZ` n'a ete retournee pour `FR10` par
  `API_GLACCOUNTLINEITEM`.
- Aucune ligne FR10 marquee avec une banque societe ou un compte bancaire n'a ete
  retournee par cette API.
- Les comptes observes dans les ecritures FR10 couvrent le stock, fournisseurs,
  clients, TVA, achats, ventes et un compte technique. Aucun compte avec un libelle
  Banque ou Caisse n'a ete observe.
- Le service de gestion des comptes generaux `FAC_MANAGE_GLACCOUNT_SRV` refuse la
  lecture avec HTTP `403` et la lecture RFC directe est temporairement indisponible.

Statut actualise : `BLOCKED_FR10_CASH_ACCOUNT_NOT_EVIDENCED`.

Aucun paiement et aucun lettrage n'ont ete executes. La plus petite action requise est
la communication par le responsable FI du compte Banque/Caisse et, si necessaire, de
la banque societe/ID de compte valides pour `FR10`. Ces valeurs devront ensuite etre
relues dans SAP avant de demander l'autorisation FI exacte de comptabiliser et lettrer
`3720 EUR` contre la piece `9300000009`.

Preuves complementaires :

- `runtime/sap_reads/s4600_ex8_finance_odata_discovery_2026-10-22.json`
- `runtime/sap_reads/s4600_ex8_fr10_dz_line_items_2026-10-22.json`
- `runtime/sap_reads/s4600_ex8_fr10_gl_account_2026-10-22.json`
- `runtime/sap_reads/s4600_ex8_fr10_cash_account_2026-10-22.json`
