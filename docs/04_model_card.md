# Model card

## Objectif

Détecter les clients dont le comportement transactionnel montre des signes
de dégradation financière, avant qu'ils n'atteignent les seuils légaux de
fragilité (`fragile_legal`) — anticipation à horizon de 3 mois
(`target_fragile_j3m`). Le score produit est une aide à l'analyse, jamais
une décision automatisée. Voir `docs/05_ethics_and_limits.md`.

## Données d'entraînement

- 2000 clients synthétiques, 18 mois de transactions
- Split temporel : train sur les mois 0-11, test sur les mois 12-14
  (jamais de split aléatoire, pour éviter la fuite d'information future)
- Déséquilibre de classe documenté entre train (7.5%) et test (11.7%),
  lié à la distribution du mois de bascule dans le générateur synthétique
  (voir `docs/07_data_exploration_notes.md`)

## Algorithme retenu

XGBoost (`n_estimators=200`, `max_depth=4`, `learning_rate=0.05`,
`scale_pos_weight` pour compenser le déséquilibre des classes).

Comparé à deux références :
1. Baseline par règles métier (score additif sur seuils simples)
2. Régression logistique (`class_weight="balanced"`)

## Métriques (sur le jeu de test, mois 12-14)

| Modèle | Recall | Précision | F1 |
|---|---|---|---|
| Baseline règles | 0.949 | 0.263 | 0.412 |
| Régression logistique | 0.862 | 0.331 | 0.478 |
| **XGBoost (retenu)** | **0.956** | **0.386** | **0.55** |

Le recall est priorisé par choix métier : rater un client réellement
fragile coûte plus cher (humainement et réglementairement) qu'une fausse
alerte.

## Features utilisées

`age`, `anciennete_mois`, `revenus_entrants_roll3`, `revenus_entrants_delta`,
`nb_incidents_roll3`, `nb_decouverts_roll3`, `ratio_charges_revenu`,
statut professionnel encodé (dummies).

Features de revenus simplifiées (`revenus_entrants`, `_lag1`, `_roll6`
retirées) suite à un diagnostic de multicolinéarité forte (corrélations
0.86 à 0.99 entre elles) qui rendait les coefficients de la régression
logistique instables. `ratio_charges_revenu` plafonné à 3.0 dans dbt pour
neutraliser des valeurs aberrantes qui écrasaient son échelle.

**`profil_trajectoire` et `fragile_legal` sont explicitement exclus** :
la première est la variable cachée de génération (fuite totale), la
seconde sert à calculer la cible elle-même (fuite directe).

## Explicabilité (SHAP)

`nb_decouverts_roll3` domine largement l'importance globale, suivi de
`nb_incidents_roll3` et `ratio_charges_revenu`. Le statut professionnel a
une importance faible — le modèle s'appuie principalement sur le
comportement récent du client, pas sur son profil socio-professionnel.

Chaque prédiction individuelle est explicable via un waterfall plot SHAP,
destiné à être affiché sur la page "Profil client" du dashboard.

## Limites connues

- Données 100% synthétiques : les résultats ne se transposent pas
  directement à des données bancaires réelles
- `age` ressort avec un poids notable dans SHAP, possiblement lié à la
  corrélation âge/statut construite dans le générateur plutôt qu'à un vrai
  signal comportemental — point de vigilance si le projet évoluait vers
  des données réelles, où l'âge ne doit jamais devenir un proxy dominant
- `nb_incidents_roll3` montre un effet contre-intuitif sur une partie des
  valeurs hautes dans le summary plot SHAP, probablement une interaction
  avec `nb_decouverts_roll3` qui capte déjà une partie du même signal — non
  bloquant, mais non totalement expliqué
- Aucune donnée de démographie sensible (genre, origine) générée ni
  utilisée, par choix — voir `docs/05_ethics_and_limits.md`

## Usage prévu

Aide à l'analyse pour un conseiller ou une équipe spécialisée, en
complément d'une revue humaine.

## Usage interdit

Refus de service, décision de crédit, toute action sans revue humaine.

## Version du modèle

v1 — première version entraînée sur données synthétiques, non déployée.