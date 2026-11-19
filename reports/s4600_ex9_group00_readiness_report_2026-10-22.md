# S4600 - Exercice 9 - Preparation du client T-CUS00

Date : 22/10/2026  
Environnement : A4H / mandant 600 / utilisateur ABDELJ  
Mode : lecture seule, aucune creation SAP

## Resultat

Statut : `READY_FOR_VALUE_DECISION_AND_SCOPED_WRITE_APPROVAL`

`T-CUS00` n'existe pas dans SAP : la cle BP, la cle client, l'ID externe, le
terme de recherche et le nom exact `Motos et autres` ont tous ete controles.
Aucun doublon n'a ete retourne.

Le regroupement `BPAB` existe et contient des BP a numero interne ainsi que des
BP a identifiant alphanumerique. La route API deja prouvee dans cet environnement
utilise cependant un numero SAP genere. La proposition conserve donc `T-CUS00`
dans `SearchTerm1`, capture le numero SAP genere et enregistre le mapping.

## Ecart entre le book et FR10

Les valeurs du book suivantes ne sont pas prouvees dans FR10 :

- compte collectif `12100000` : absent du plan comptable PCOH de FR10 ;
- conditions de paiement `ZB00` : aucune utilisation retournee dans FR10 ;
- condition d'expedition `50` : aucune utilisation retournee dans FR10 ;
- schema client `S` : aucune utilisation retournee dans FR10 ;
- categorie fiscale `TTX1` : aucune utilisation retournee dans FR10.

Elles ne doivent donc pas etre envoyees a SAP.

## Proposition compatible FR10

La reference fonctionnelle est le client allemand FR10 `1000000113`, relu en
direct. Les valeurs proposees sont :

- identite : organisation `BPAB`, nom `Motos et autres`, marqueur `T-CUS00` ;
- adresse du book : Rue principale 00, 20111 Hambourg, DE, region HH, langue EN ;
- roles : `FLCU00` et `FLCU01` ;
- societe : `FR10`, compte collectif `41111000`, conditions de paiement `0002` ;
- domaine commercial : `FR10/10/1W`, EUR, expedition `01`, division livreuse
  `FR10`, DAP Hambourg, conditions de paiement client `0004`, groupe
  d'imputation `C1`, schema client `01` ;
- taxes : les quatre lignes FR10 relues sur le client allemand de reference,
  dont `FR/MWST = 1` ;
- fonctions partenaires attendues : `DO`, `RF`, `PY`, `RM`, toutes vers le
  nouveau client lui-meme.

## Risque et autorisations

La creation ne devrait pas bloquer SAP. Le risque est la creation d'un client
incomplet si une etape intermediaire echoue. Le workflow doit donc etre sequentiel :
LOOKUP, une ecriture, READBACK, puis etape suivante. Aucun retry automatique ne
sera effectue apres une issue ambigue.

La racine, l'adresse et les roles relevent des donnees de base de formation. La
societe et le compte collectif constituent une ecriture FI. Les classifications
fiscales constituent une decision fiscale. L'execution requiert donc une
autorisation explicite couvrant les valeurs exactes de la proposition.

## Preuves

- `runtime/sap_reads/s4600_ex9_group00_readiness_2026-10-22.json`
- `data/provisioning/s4600/S4600_CH4_EX9.group00.target_proposal.json`
- `runtime/sap_reads/s4600_fr10_audit_2026-10-21.json`
