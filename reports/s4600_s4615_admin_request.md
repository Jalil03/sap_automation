# Demande administrateur ciblée — S4600 / S4615

A4H/600, 19 octobre 2026. Demande de preuves et de décisions, **aucune autorisation de réparation ou de changement global**. Réutiliser la configuration vérifiée ; ne pas recréer société/organisation commerciale 1010, domaine 1010/10/00, client 1000000115, article de base 10000289 ou point d'expédition 1010.

| Périmètre | État établi / besoin | Réponse exacte attendue | Responsable |
|---|---|---|---|
| Partagé : usine 1010 | Aucune usine compatible établie pour société 1010/EUR ; usine 1710 appartient à société 1710 et n'est pas un substitut automatique | Valider création/réutilisation 1010, société/aire de valorisation, niveau de valorisation et compatibilité des devises/ML ; fournir paramètres obligatoires prouvés | SAP org + FI/MM |
| Partagé : valorisation | 10000289 n'a que les données de base ; aucune classe/compte/prix cible approuvé pour cette nouvelle usine | Classe de valorisation FERT et catégorie de référence, contrôle S/V, prix initial/unité, comptes de stock et sortie de marchandises, clés de détermination et compatibilité plan de comptes ; signaler ce qui existe ou doit être créé | FI/MM, décisions sensibles explicites |
| S4600 : usine 1020 | Absence selon audit API existant ; nécessaire au scénario ATP multi-usines | Confirmer contexte société/valorisation et configuration requise pour le scénario 1010/1020, sans copier les données 1710 aveuglément | SAP org + FI/MM |
| S4600 : Z001 | TVST complet 20/20 : absent | Valeurs autorisées du point Z001, adresse et affectations à l'usine, conditions d'expédition/groupes de chargement/détermination nécessaires au Book | SD/LE + propriétaire organisation |
| S4615 : logistique | Point 1010/adresse 1583/BE déjà vérifié ; usine et affectations manquantes | Valider 1010/10→usine, usine→point1010, OVL2 pour condition01 et groupe de chargement justifié ; ne pas recréer le point | SD/LE avec dépendance usine |
| S4600 : magasin/EWM 1010 | API entrepôt accessible, clé 1010 non trouvée ; pas de preuve d'un autre mapping | Confirmer numéro/mapping, intégration usine/emplacement, disponibilité des apps/rôles EWM et données nécessaires ; distinguer objets ERP/EWM | EWM/Basis + MM |
| Participants | ABDELJ ne prouve pas les accès S4600-01/S4615-01 | Fournir sessions participantes autorisées, Fiori/catalogues/apps requis et accès GUI ; ne pas communiquer les mots de passe dans le rapport | Formation/Basis |
| S4615 ex12 : comptes | Book cite INT/YCOA selon passage ; société live 1010 utilise CABE | Arbitrer la traduction fonctionnelle des comptes/déterminations du Book vers CABE. Ne pas appliquer automatiquement 49000000 ni le groupe client81 | FI/SD account determination |
| Séparé : C+039 / 1710 | ML productif ; T000-MWAER USD→XAF par WBS601 le 14/10 ; notre workflow a aussi modifié FINSC_001A le 16/10 | Établir avant/après FINSC, historique ML productif, devises et premières erreurs ; diagnostic/plan contrôlé FI/CO. Aucun CKMSTART, reset ou changement client global automatique | FI/CO ML + Basis |

Preuves : [audit S4600](s4600_full_live_readiness_audit.md), [progression S4615](../books/S4615/S4615_PROGRESS.md), [attribution C+039](sap_c039_attribution.md), [lectures ciblées](sap_training_safe_parallel_progress.md). La causalité C+039 reste **INCONCLUSIVE** ; ne pas attribuer exclusivement à un utilisateur sans l'historique complet.

## Ce qui reste à notre équipe

Lectures SD non exposées par le bridge, résolution des identités T-*, contrats d'exécution ciblés, préparation des 16 objets, validations et futurs documents d'exercices. Ce ne sont pas tous des blocages administrateur. Les documents générés par les exercices doivent être créés dans leur séquence, pas fournis comme Customizing.

Réponse administrateur souhaitée : pour chaque ligne, configuration existante + preuve, décision exacte/approbateur si changement, ou dépendance non résolue. Après réponse : valider les manifestes, obtenir les scopes nécessaires, puis poursuivre les exercices indépendants avant les branches livraison/PGI. Aucun transport à libérer.
