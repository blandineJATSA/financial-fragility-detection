"""Genere les transactions mensuelles par client, selon leur profil de trajectoire."""

import numpy as np
import pandas as pd

from data_generation.fragility_scenarios import (
    degradation_factors_for_month,
    pick_transition_month,
)

REVENU_BASE_BY_STATUT = {
    "salarie": 2200,
    "independant": 2000,
    "retraite": 1500,
    "etudiant": 800,
    "sans_emploi": 600,
}

# Volatilite de base du revenu, independante de toute degradation
# (les independants ont des revenus naturellement plus irreguliers)
VOLATILITY_BASE_BY_STATUT = {
    "salarie": 0.03,
    "independant": 0.12,
    "retraite": 0.02,
    "etudiant": 0.08,
    "sans_emploi": 0.05,
}

CHARGES_CONTRAINTES_RATIO = 0.35

NEUTRAL_FACTORS = {
    "revenu_multiplier": 1.0,
    "charges_multiplier": 1.0,
    "incident_rate": 0.02,
    "decouvert_rate": 0.02,
    "revenu_volatility": 0.0,
}

INSTALLED_FRAGILE_FACTORS = {
    "revenu_multiplier": 0.80,
    "charges_multiplier": 1.15,
    "incident_rate": 0.55,
    "decouvert_rate": 0.70,
    "revenu_volatility": 0.30,
}


def _factors_for_client_month(profil: str, month_index: int, transition_month) -> dict:
    if profil == "stable":
        return NEUTRAL_FACTORS
    if profil == "fragile_des_le_depart":
        return INSTALLED_FRAGILE_FACTORS
    return degradation_factors_for_month(month_index, transition_month)


def generate_transactions(clients_df: pd.DataFrame, n_months: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for _, client in clients_df.iterrows():
        statut = client["statut_pro"]
        profil = client["profil_trajectoire"]
        revenu_base = REVENU_BASE_BY_STATUT[statut]
        volatilite_base = VOLATILITY_BASE_BY_STATUT[statut]

        transition_month = (
            pick_transition_month(n_months, rng)
            if profil == "degradation_progressive"
            else None
        )

        solde = revenu_base * rng.uniform(0.5, 2.0)  # solde de depart, variable par client

        # Plafond de decouvert autorise : au-dela, les paiements sont rejetes
        # plutot que le solde ne s'enfonce indefiniment dans le negatif.
        overdraft_limit = -1 * revenu_base * rng.uniform(1.0, 2.5)

        for month_index in range(n_months):
            factors = _factors_for_client_month(profil, month_index, transition_month)

            volatilite_totale = volatilite_base + factors["revenu_volatility"]
            bruit_revenu = rng.normal(1.0, volatilite_totale)
            revenus_entrants = max(0.0, revenu_base * factors["revenu_multiplier"] * bruit_revenu)

            depenses_contraintes = revenu_base * CHARGES_CONTRAINTES_RATIO * factors["charges_multiplier"]
            depenses_variables = max(
                0.0, (revenu_base * (1 - CHARGES_CONTRAINTES_RATIO)) * rng.normal(1.0, 0.10)
            )

            nb_incidents_paiement = int(rng.poisson(factors["incident_rate"] * 3))
            nb_decouverts = int(rng.poisson(factors["decouvert_rate"] * 5))

            tentative_solde = solde + revenus_entrants - depenses_contraintes - depenses_variables

            if tentative_solde < overdraft_limit:
                # Plafond atteint : un ou plusieurs paiements sont rejetes,
                # le solde ne descend pas plus bas que la limite.
                solde = overdraft_limit
                nb_incidents_paiement += 1
            else:
                solde = tentative_solde

            rows.append({
                "client_id": client["client_id"],
                "mois": month_index,
                "revenus_entrants": round(revenus_entrants, 2),
                "depenses_contraintes": round(depenses_contraintes, 2),
                "depenses_variables": round(depenses_variables, 2),
                "solde_fin_mois": round(solde, 2),
                "nb_incidents_paiement": nb_incidents_paiement,
                "nb_decouverts": nb_decouverts,
            })

    return pd.DataFrame(rows)