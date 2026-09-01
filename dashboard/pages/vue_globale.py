import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery

PROJECT_ID = "finprev-portfolio"
DATASET = "finprev"


@st.cache_data(ttl=3600)
def load_scores():
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.fct_client_risk_scores`
    """
    return client.query(query).to_dataframe()


st.title("Détection précoce de fragilité financière")
st.caption("Données synthétiques — outil d'aide à l'analyse, pas une décision automatisée.")

df = load_scores()

nb_clients = df["client_id"].nunique()
nb_signaux_ce_mois = df[df["mois"] == df["mois"].max()]["prediction"].sum()
nb_incidents_legaux = df["fragile_legal"].sum()
taux_couverture = df["target_reel"].mean() * 100


col1, col2, col3, col4 = st.columns(4)
col1.metric("Clients suivis", f"{nb_clients:,}".replace(",", " "))
col2.metric("Signaux détectés (dernier mois)", f"{int(nb_signaux_ce_mois):,}".replace(",", " "))
col3.metric("Mois-clients en fragilité légale", f"{int(nb_incidents_legaux):,}".replace(",", " "))
col4.metric("Taux de couverture cible", f"{taux_couverture:.1f}%".replace(".", ","))

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    evolution = df.groupby("mois").agg(
        signaux_precoces=("prediction", "sum"),
        incidents_legaux=("fragile_legal", "sum"),
    ).reset_index()

    fig1 = px.line(
        evolution, x="mois", y=["signaux_precoces", "incidents_legaux"],
        title="Signaux précoces détectés vs incidents réglementaires",
        labels={"value": "Nombre de client-mois", "mois": "Mois", "variable": ""},
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    repartition = df["niveau_vigilance"].value_counts().reindex(
        ["faible", "modere", "eleve", "critique"]
    ).reset_index()
    repartition.columns = ["niveau_vigilance", "count"]

    fig2 = px.bar(
        repartition, x="niveau_vigilance", y="count",
        title="Répartition des clients par niveau de vigilance",
        labels={"niveau_vigilance": "Niveau", "count": "Nombre de clients"},
        color="niveau_vigilance",
        color_discrete_map={
            "faible": "#1D9E75", "modere": "#C98A2D",
            "eleve": "#B8631E", "critique": "#B33F1E",
        },
    )
    fig2.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Clients à vigilance élevée ou critique")

niveau_filtre = st.multiselect(
    "Filtrer par niveau", ["eleve", "critique"], default=["eleve", "critique"]
)

table = df[df["niveau_vigilance"].isin(niveau_filtre)][
    ["client_id", "mois", "score_vigilance", "niveau_vigilance"]
].sort_values("score_vigilance", ascending=False)

st.dataframe(table, use_container_width=True, hide_index=True)