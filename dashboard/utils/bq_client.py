"""Client BigQuery authentifie via les secrets Streamlit (cloud) ou credentials locaux (dev)."""

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account


@st.cache_resource
def get_bq_client():
    if "gcp_service_account" in st.secrets:
        # Deploiement cloud : credentials depuis les secrets Streamlit
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        return bigquery.Client(credentials=credentials, project=credentials.project_id)
    else:
        # Developpement local : credentials depuis GOOGLE_APPLICATION_CREDENTIALS
        return bigquery.Client(project="finprev-portfolio")