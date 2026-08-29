# Financial Fragility Detection

> Detecter les signaux precoces de fragilite financiere a partir du comportement transactionnel, avant que les seuils reglementaires ne soient atteints.

## Statut du projet

En cours de construction.

## Contexte metier

Depuis la loi de 2013, les banques francaises ont l'obligation legale de detecter leurs clients en situation de fragilite financiere. Les criteres reglementaires detectent cette fragilite une fois qu'elle est deja installee. Ce projet explore la detection de signaux precoces, avant le franchissement de ces seuils, a partir du comportement transactionnel.

Voir docs/00_business_context.md pour le detail.

## Avertissement

Ce projet utilise exclusivement des donnees synthetiques. Il ne s'agit pas d'un dispositif reglementaire bancaire reel. Le score produit est un signal d'aide a l'analyse, jamais une decision automatisee.

## Stack

Python - BigQuery - dbt-core - Airflow (Docker) - scikit-learn / XGBoost - SHAP - Streamlit