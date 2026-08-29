# Notes d'exploration des données

## Structure

2000 clients, 36 000 lignes de transactions (1 ligne = 1 client x 1 mois,
sur 18 mois). Aucune valeur manquante, aucun doublon.

## Population

55% salariés, 15% retraités, 14% indépendants, 10% étudiants, 5% sans
emploi. Âge cohérent par statut (étudiants ~21 ans, retraités ~71 ans).

## Constat clé (sans utiliser le profil caché de génération)

607 clients sur 2000 passent en solde négatif au moins une fois sur la
période. Dans les 3 mois précédant ce passage en négatif, trois indicateurs
augmentent déjà de façon mesurable :
- ratio charges/revenus : 0.51 → 0.60
- nombre de découverts : 2.55 → 2.87
- nombre d'incidents de paiement : 1.12 → 1.38

Ce constat, obtenu empiriquement sur les données (sans utiliser la variable
cachée profil_trajectoire qui a servi à générer les données), confirme
qu'un signal précurseur existe et est détectable avant l'incident.

## Construction de la cible : fragile_legal et target_fragile_j3m

`fragile_legal` est approximé avec deux critères combinés (OU logique),
détaillés et justifiés dans `docs/00_business_context.md` :
1. 5+ incidents de paiement dans le mois, combinés à des revenus sous 1500€
2. Au moins un incident de paiement pendant 3 mois consécutifs

Constat empirique : le critère 1 ne se déclenche que dans 0.6% des cas (5
incidents simultanés est rare avec notre paramétrage), le critère 2 porte
l'essentiel de la détection. `fragile_legal` touche 11.2% des mois observés,
`target_fragile_j3m` (devenir fragile dans les 3 prochains mois, sans
l'être déjà) touche 8.3% des observations — une cible exploitable, ni trop
rare ni trop fréquente.

## Point de vigilance pour la modélisation : déséquilibre train/test

Sur un split temporel (train : mois 0-11, test : mois 12-15), le taux de
cible positive passe de 6.2% (train) à 13.2% (test). C'est cohérent avec
notre logique de génération : le mois de bascule des clients en dégradation
est tiré entre 55% et 85% de la période, ce qui concentre mécaniquement les
événements de fragilisation vers la fin de la fenêtre observée. À garder en
tête lors de l'évaluation du modèle — les métriques sur le test reflètent
une période structurellement plus à risque que l'entraînement.

## Pistes de features pour dbt

- Lag, delta et moyennes glissantes (3 et 6 mois) sur revenus, dépenses,
  solde, incidents, découverts
- Ratio solde / revenu
- Tendance (pente) du ratio charges/revenus sur fenêtre glissante
- Statut professionnel et ancienneté (variables statiques)

Écarté : un score composite type "tension financière" à poids arbitraires
— on préfère laisser le modèle apprendre les combinaisons de features
individuelles plutôt que figer une formule non justifiée.