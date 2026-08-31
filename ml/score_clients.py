"""Score tous les clients avec le modele XGBoost entraine, et ecrit
les resultats dans BigQuery (table finprev.fct_client_risk_scores).

A relancer a chaque fois que le modele est ré-entraîné ou que de nouvelles
données arrivent dans fct_client_monthly_features.
"""

import joblib
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "finprev-portfolio"
DATASET = "finprev"

def main():
    client = bigquery.Client(project=PROJECT_ID)

    # Chargement du modele et des features attendues
    model = joblib.load("ml_artifacts/xgb_model.joblib")
    feature_names = joblib.load("ml_artifacts/feature_names.joblib")

    # Chargement de toute la table de features (pas seulement le test set)
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.fct_client_monthly_features`
    """
    df = client.query(query).to_dataframe()

    # Meme encodage que dans le notebook d'entrainement
    df_encoded = pd.get_dummies(df, columns=["statut_pro"], prefix="statut", drop_first=True)
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)
    X = df_encoded[feature_names].fillna(0)

    # Score de vigilance = probabilite predite, ramenee sur une echelle 0-100
    scores_proba = model.predict_proba(X)[:, 1]
    predictions = model.predict(X)

    # Niveaux de vigilance bases sur les quantiles REELS de la distribution
    # des scores de ce modele (les probabilites XGBoost sont polarisees,
    # des seuils fixes 30/60/80 laisseraient "modere" et "eleve" quasi vides)
    q50, q75, q90 = pd.Series(scores_proba).quantile([0.5, 0.75, 0.9]).values

    def niveau_vigilance(proba):
        if proba < q50:
            return "faible"
        elif proba < q75:
            return "modere"
        elif proba < q90:
            return "eleve"
        else:
            return "critique"

    results = pd.DataFrame({
        "client_id": df["client_id"],
        "mois": df["mois"],
        "score_vigilance": (scores_proba * 100).round(1),
        "niveau_vigilance": [niveau_vigilance(s) for s in scores_proba],
        "prediction": predictions,
        "target_reel": df["target_fragile_j3m"],
        "fragile_legal": df["fragile_legal"],
    })

    # Ecriture dans BigQuery, en remplacant la table a chaque run
    table_id = f"{PROJECT_ID}.{DATASET}.fct_client_risk_scores"
    job = client.load_table_from_dataframe(
        results, table_id,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    )
    job.result()

    print(f"{len(results)} scores ecrits dans {table_id}")
    print()
    print("Seuils utilises (quantiles reels) :")
    print(f"  q50={q50:.3f}  q75={q75:.3f}  q90={q90:.3f}")
    print()
    print("Repartition des niveaux de vigilance :")
    print(results["niveau_vigilance"].value_counts())

if __name__ == "__main__":
    main()