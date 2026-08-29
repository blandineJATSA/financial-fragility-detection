"""Genere la dimension clients (profil statique)."""

import numpy as np
import pandas as pd

STATUT_PRO_CHOICES = ["salarie", "independant", "retraite", "etudiant", "sans_emploi"]
STATUT_PRO_PROBS = [0.55, 0.15, 0.15, 0.10, 0.05]

TRAJECTOIRE_CHOICES = ["stable", "degradation_progressive", "fragile_des_le_depart"]

# Probabilite du profil de trajectoire, conditionnee par le statut professionnel.
# Les independants ont des revenus plus volatils -> plus de degradation_progressive.
# Les etudiants et sans emploi ont une probabilite plus elevee d'etre fragiles des le depart.
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

    age = rng.normal(loc=42, scale=14, size=n_clients).clip(18, 85).astype(int)

    statut_pro = rng.choice(STATUT_PRO_CHOICES, size=n_clients, p=STATUT_PRO_PROBS)

    anciennete_mois = rng.integers(1, 241, size=n_clients)

    profil_trajectoire = np.empty(n_clients, dtype=object)
    for statut in STATUT_PRO_CHOICES:
        mask = statut_pro == statut
        n = mask.sum()
        if n > 0:
            profil_trajectoire[mask] = rng.choice(
                TRAJECTOIRE_CHOICES, size=n, p=TRAJECTOIRE_PROBS_BY_STATUT[statut]
            )

    return pd.DataFrame({
        "client_id": client_ids,
        "age": age,
        "statut_pro": statut_pro,
        "anciennete_mois": anciennete_mois,
        "profil_trajectoire": profil_trajectoire,
    })