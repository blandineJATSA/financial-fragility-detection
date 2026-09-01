import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from google.cloud import bigquery

PROJECT_ID = "finprev-portfolio"
DATASET = "finprev"


@st.cache_data(ttl=3600)
def load_client_history():
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
    SELECT
        s.client_id, s.mois, s.score_vigilance, s.niveau_vigilance,
        f.solde_fin_mois, f.nb_incidents_paiement, f.nb_decouverts,
        f.revenus_entrants, f.ratio_charges_revenu
    FROM `{PROJECT_ID}.{DATASET}.fct_client_risk_scores` s
    LEFT JOIN `{PROJECT_ID}.{DATASET}.int_monthly_features` f
        ON s.client_id = f.client_id AND s.mois = f.mois
    """
    return client.query(query).to_dataframe()


st.title("Profil client")

df = load_client_history()

client_ids = sorted(df["client_id"].unique())
selected_client = st.selectbox("Sélectionner un client", client_ids)

client_data = df[df["client_id"] == selected_client].sort_values("mois")
dernier_mois = client_data.iloc[-1]

niveau_couleurs = {
    "faible": "#1D9E75", "modere": "#C98A2D",
    "eleve": "#B8631E", "critique": "#B33F1E",
}

couleur = niveau_couleurs.get(dernier_mois["niveau_vigilance"], "#888")

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(
        f"""
        <div style="background-color:{couleur}20; border-left: 4px solid {couleur};
                    padding: 1rem; border-radius: 8px;">
            <div style="color:{couleur}; font-size: 0.9rem;">Niveau de vigilance</div>
            <div style="color:{couleur}; font-size: 1.8rem; font-weight: bold;">
                {dernier_mois['niveau_vigilance'].capitalize()}
            </div>
            <div style="color:{couleur}; font-size: 1.2rem;">
                {str(round(dernier_mois['score_vigilance'], 1)).replace('.', ',')} / 100
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.info(
        "Ce score est un signal de vigilance destiné à guider une analyse humaine. "
        "Il ne constitue pas une décision automatisée."
    )

st.divider()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=client_data["mois"], y=client_data["solde_fin_mois"],
    mode="lines+markers", name="Solde fin de mois",
    line=dict(color="#1B4B66", width=2),
))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.update_layout(
    title="Évolution du solde",
    xaxis_title="Mois", yaxis_title="Solde (€)",
    height=350,
)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Incidents (dernier mois)", int(dernier_mois["nb_incidents_paiement"]))
col2.metric("Découverts (dernier mois)", int(dernier_mois["nb_decouverts"]))
col3.metric("Ratio charges/revenu", str(round(dernier_mois['ratio_charges_revenu'], 2)).replace('.', ','))

st.divider()

recommandations = {
    "faible": "Situation stable, aucune action requise.",
    "modere": "Quelques signaux à surveiller lors du prochain contact client.",
    "eleve": "Signal de dégradation identifié — contact proactif recommandé.",
    "critique": "Signal fort — accompagnement ou offre spécifique à envisager rapidement.",
}
st.subheader("Recommandation")
st.write(recommandations.get(dernier_mois["niveau_vigilance"], ""))