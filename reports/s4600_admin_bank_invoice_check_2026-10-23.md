# Contrôle du retour administrateur — FR10

Contrôle du 23 octobre 2026, strictement en lecture seule. Identité RFC vérifiée : A4H / 600 / ABDELJ. Aucun paiement, lettrage ou changement de configuration.

## Résultats vérifiés

| Objet | Preuve actuelle | Conclusion |
| --- | --- | --- |
| Compte bancaire Fiori | API_BANKACCOUNT_SRV : compte interne 1000000030, FR10, EUR, « Encaissements formation » | Existe |
| Banque société | T012K : FR10 / FRB01 / ENC01, EUR, compte général 52110100 | Rattachement bancaire vérifié |
| Compte indiqué par l'administrateur | SKB1 : FR10 / 52110101, EUR, gestion des postes non soldés active, indicateur écritures automatiques seules vide | Existe dans FR10 ; cela ne prouve pas à lui seul la possibilité de comptabiliser un paiement |
| Facture 90000090 | API : FR10, client 1000000112, pièce comptable 9300000009/2026, 3 720 EUR TTC, non annulée | Facture existante comptabilisée |
| Poste client de la facture | BSEG : 9300000009/2026, poste 001, client 1000000112, 3 720 EUR ; pièce de rapprochement vide et date 00000000 | Poste encore ouvert, non lettré |

## Point à clarifier avant un encaissement

Le rattachement bancaire utilise 52110100, tandis que le message administrateur demande 52110101. Cette différence n'est pas une anomalie démontrée : il peut s'agir du compte principal et d'un compte de passage. Faire confirmer le rôle et l'emploi de 52110101 pour la saisie de l'encaissement ; ne modifier aucun rattachement sur cette seule différence.

La facture ouverte est une candidate pour un exercice d'encaissement, pas une facture déjà affectée à un participant. Son affectation doit éviter une réutilisation simultanée. Aucun encaissement n'a été simulé ni comptabilisé par ce contrôle.

Les valeurs par défaut utilisateurs, la structure de bilan, le second magasin et les autres exercices ne sont pas revalidés par cette vérification ciblée. Les numéros d'exercices du message client ne doivent pas être assimilés automatiquement à ceux du book S4600 audité.

## Suite proposée

1. Confirmer auprès de l'administrateur l'emploi de 52110101 comme compte d'encaissement et l'affectation de la facture 90000090.
2. Recevoir la structure de bilan FR10 et le code exact du second magasin lorsqu'ils seront disponibles, puis les contrôler en lecture seule.
3. Conserver les exercices de paiement au statut « prérequis vérifiés partiellement, exécution non validée » ; une écriture FI nécessite une autorisation distincte et un contrat technique éprouvé.

Preuve technique : `runtime/sap_reads/s4600_fr10_bank_invoice_check_2026-10-23.json`.

## Complément de vérification — rôle des comptes et affectation

Contrôle supplémentaire effectué le 23 octobre, toujours sans écriture SAP.

- Plan comptable de FR10 : **PCOH**, devise **EUR**.
- **52110100** : libellé « AFRILAND FIRST BANK », compte rattaché à la banque société ; gestion des postes non soldés inactive.
- **52110101** : libellé « AFRILAND FIRST BANK ENCAISSEMENT », gestion des postes non soldés active. Le rôle encaissement indiqué dans le message administrateur est donc corroboré par SAP ; la différence avec le compte de rattachement bancaire n'est pas, en soi, un blocage.
- Les deux comptes ne portent ni indicateur de blocage de comptabilisation société (`XSPEB`), ni indicateur de suppression société (`XLOEB`). Cela ne démontre pas la totalité des autorisations et contrôles de comptabilisation.
- La facture **90000090**, pièce **9300000009/2026**, reste non lettrée pour **3 720 EUR**. Les champs d'affectation (`ZUONR`) et de texte (`SGTXT`) du poste client sont vides. Aucun participant n'y est identifié ; leur absence ne prouve pas l'absence d'une réservation dans un suivi externe.

Conclusion : le prérequis de compte d'encaissement est établi. Le paiement reste **non testé et non exécuté**. L'attribution de la facture à un participant doit être coordonnée ; aucune réservation n'a été créée. La prochaine vérification technique est l'existence d'une route éprouvée de simulation d'encaissement/lettrage sans comptabilisation, avant toute demande d'autorisation d'écriture FI.

Preuve complémentaire : `runtime/sap_reads/s4600_bank_roles_invoice_assignment_2026-10-23.json`.
