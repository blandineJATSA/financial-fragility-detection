# Méthodologie

## Définition de la cible

`target_fragile_j3m` : le client atteindra les seuils réglementaires de
fragilité dans les 3 prochains mois, alors qu'il ne les a pas encore atteints
au mois M. Cible binaire, calculée a posteriori sur la séquence temporelle.

## Validation temporelle

Le split entraînement/test se fait **par le temps**, jamais aléatoirement :
entraînement sur les premiers mois, test sur les derniers, pour éviter toute
fuite d'information (prédire le passé avec des données du futur).

## Approche de modélisation prévue

1. Baseline par règles métier (score simple, interprétable)
2. Régression logistique (référence interprétable)
3. XGBoost (modèle principal)
4. SHAP pour l'explicabilité de chaque prédiction

## Métriques prévues

Recall et précision (classes déséquilibrées, PR-AUC plus pertinent que
ROC-AUC), plus une métrique métier : proportion de clients réellement devenus
fragiles qui ont été détectés au moins 30 jours à l'avance.

## Statut

TODO — aucun modèle entraîné à ce stade. Cette section sera complétée avec
les résultats réels une fois l'étape modélisation atteinte.