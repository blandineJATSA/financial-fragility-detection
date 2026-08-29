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

## Pistes de features pour dbt

- Tendance (pente) du ratio charges/revenus sur fenêtre glissante
- Fréquence cumulée des découverts sur 3 mois glissants
- Tendance des incidents mineurs, même sous le seuil légal
- Volatilité des revenus sur fenêtre glissante