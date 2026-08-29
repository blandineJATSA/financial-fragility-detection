# Architecture technique

## Flux de données

Génération synthétique (Python) → GCS (raw) → BigQuery (raw) → dbt
(staging → intermediate → marts) → modèle Python (scikit-learn puis
XGBoost + SHAP) → table de scores → Streamlit.

## Statut actuel

- [x] Génération de données synthétiques (`data_generation/`)
- [ ] Infrastructure GCP (bucket, dataset, service account)
- [ ] Pipeline dbt (staging, intermediate, marts)
- [ ] Orchestration Airflow (Docker)
- [ ] Modèle + explicabilité SHAP
- [ ] Dashboard Streamlit

## Stack

Python · GCS · BigQuery · dbt-core (adapter BigQuery) · Airflow (Docker Compose local) · scikit-learn / XGBoost · SHAP · Streamlit

## Ce qui est volontairement hors scope

Terraform, Vertex AI, Cloud Composer, CI/CD complet — voir le raisonnement détaillé dans le document d'architecture du dépôt (à copier ici une fois le pipeline GCP construit).