"""Genere la dimension clients (profil statique)."""

import numpy as np
import pandas as pd

STATUT_PRO_CHOICES = ["salarie", "independant", "retraite", "etudiant", "sans_emploi"]
STATUT_PRO_PROBS = [0.55, 0.15, 0.15, 0.10, 0.05]

# Age moyen et ecart-type par statut, avec bornes realistes (clip)
AGE_PARAMS_BY_STATUT = {
    "salarie":     {"mean": 40, "std": 11, "min": 22, "max": 65},
    "independant": {"mean": 42, "std": 11, "min": 24, "max": 70},
    "retraite":    {"mean": 71, "std": 6,  "min": 60, "max": 85},
    "etudiant":    {"mean": 21, "std": 2,  "min": 18, "max": 26},
    "sans_emploi": {"mean": 36, "std": 12, "min": 18, "max": 64},
}

TRAJECTOIRE_CHOICES = ["stable", "degradation_progressive", "fragile_des_le_depart"]

TRAJECTOIRE_PROBS_BY_STATUT = {
    "salarie":     [0.75, 0.20, 0.05],
    "independant": [0.45, 0.40, 0.15],
    "retraite":    [0.80, 0.15, 0.05],
    "etudiant":    [0.40, 0.20, 0.40],
    "sans_emploi": [0.20, 0.20, 0.60],
}


def generate_clients(n_clients: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    client_ids = [f"CLI_{i:05d}" for i in range(1, n_clients + 1)]
    statut_pro = rng.choice(STATUT_PRO_CHOICES, size=n_clients, p=STATUT_PRO_PROBS)

    age = np.empty(n_clients, dtype=int)
    profil_trajectoire = np.empty(n_clients, dtype=object)

    for statut in STATUT_PRO_CHOICES:
        mask = statut_pro == statut
        n = mask.sum()
        if n == 0:
            continue

        params = AGE_PARAMS_BY_STATUT[statut]
        age[mask] = rng.normal(params["mean"], params["std"], size=n).clip(
            params["min"], params["max"]
        ).astype(int)

        profil_trajectoire[mask] = rng.choice(
            TRAJECTOIRE_CHOICES, size=n, p=TRAJECTOIRE_PROBS_BY_STATUT[statut]
        )

    anciennete_mois = rng.integers(1, 241, size=n_clients)

    return pd.DataFrame({
        "client_id": client_ids,
        "age": age,
        "statut_pro": statut_pro,
        "anciennete_mois": anciennete_mois,
        "profil_trajectoire": profil_trajectoire,
    })