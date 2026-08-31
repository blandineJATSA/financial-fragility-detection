"""Point d'entrée : configure la navigation entre les 2 pages du dashboard."""

import streamlit as st

st.set_page_config(page_title="FinPrev", page_icon="🏦", layout="wide")

pages = {
    "FinPrev": [
        st.Page("pages/vue_globale.py", title="Vue globale", default=True),
        st.Page("pages/profil_client.py", title="Profil client"),
    ]
}

pg = st.navigation(pages)
pg.run()