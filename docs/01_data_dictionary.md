# Dictionnaire de données

## Table `clients` (data/raw/clients.parquet)

| Colonne | Type | Description |
|---|---|---|
| client_id | string | Identifiant unique (`CLI_00001`, ...) |
| age | int | 18 à 85 ans |
| statut_pro | catégorie | salarie / independant / retraite / etudiant / sans_emploi |
| anciennete_mois | int | Ancienneté du compte, 1 à 240 mois |
| profil_trajectoire | catégorie | stable / degradation_progressive / fragile_des_le_depart |

**Attention — `profil_trajectoire` ne doit jamais être utilisée comme feature du modèle.** C'est une variable de génération qui pilote directement la simulation des transactions : l'utiliser comme feature serait une fuite d'information totale (le modèle "tricherait" en lisant la réponse). Elle sert uniquement à la validation du générateur et à l'analyse a posteriori.

## Table `transactions` (data/raw/transactions.parquet)

| Colonne | Type | Description |
|---|---|---|
| client_id | string | Référence au client |
| mois | int | Index mensuel relatif, 0 à 17 |
| revenus_entrants | float | Revenus simulés du mois |
| depenses_contraintes | float | Charges fixes (loyer, crédits, énergie) |
| depenses_variables | float | Reste à vivre dépensé |
| solde_fin_mois | float | Solde cumulé, plafonné par un découvert autorisé propre à chaque client |
| nb_incidents_paiement | int | Nombre d'incidents de paiement dans le mois |
| nb_decouverts | int | Nombre d'événements de découvert dans le mois |

## Tables à venir (dbt, non construites)

- `stg_clients`, `stg_transactions` : nettoyage/typage (staging)
- `int_monthly_aggregates` : agrégats et features glissantes
- `fct_client_monthly_features` : table finale de features + `target_fragile_j3m`, utilisée pour l'entraînement et le dashboard