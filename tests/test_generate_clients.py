"""Tests de sanite pour la generation de clients synthetiques."""

from data_generation.generate_clients import generate_clients


def test_generate_clients_shape():
    df = generate_clients(500, seed=1)
    assert len(df) == 500
    assert list(df.columns) == [
        "client_id", "age", "statut_pro", "anciennete_mois", "profil_trajectoire"
    ]


def test_profil_trajectoire_global_distribution():
    df = generate_clients(5000, seed=1)
    proportions = df["profil_trajectoire"].value_counts(normalize=True)
    assert proportions["stable"] > 0.5
    assert proportions["fragile_des_le_depart"] < 0.3


def test_etudiants_plus_fragiles_que_salaries():
    df = generate_clients(5000, seed=1)
    taux_fragile = df.groupby("statut_pro")["profil_trajectoire"].apply(
        lambda x: (x == "fragile_des_le_depart").mean()
    )
    assert taux_fragile["etudiant"] > taux_fragile["salarie"]


def test_age_coherent_avec_statut_pro():
    df = generate_clients(3000, seed=1)
    age_moyen = df.groupby("statut_pro")["age"].mean()
    assert age_moyen["etudiant"] < 30
    assert age_moyen["retraite"] > 55
    assert age_moyen["etudiant"] < age_moyen["salarie"] < age_moyen["retraite"]