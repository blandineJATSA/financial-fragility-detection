"""Tests de sanite pour la generation de transactions."""

from data_generation.generate_clients import generate_clients
from data_generation.generate_transactions import REVENU_BASE_BY_STATUT, generate_transactions


def test_generate_transactions_shape():
    clients = generate_clients(50, seed=1)
    tx = generate_transactions(clients, 18, seed=1)
    assert len(tx) == 50 * 18
    assert list(tx.columns) == [
        "client_id", "mois", "revenus_entrants", "depenses_contraintes",
        "depenses_variables", "solde_fin_mois", "nb_incidents_paiement", "nb_decouverts",
    ]


def test_overdraft_floor_is_respected():
    clients = generate_clients(200, seed=7)
    tx = generate_transactions(clients, 18, seed=7)
    merged = tx.merge(clients[["client_id", "statut_pro"]], on="client_id")
    merged["revenu_base"] = merged["statut_pro"].map(REVENU_BASE_BY_STATUT)
    # le multiplicateur du plafond de decouvert ne depasse jamais 2.5x le revenu de base
    assert (merged["solde_fin_mois"] >= -2.5 * merged["revenu_base"] - 1).all()


def test_fragile_profiles_have_lower_average_balance_than_stable():
    clients = generate_clients(300, seed=3)
    tx = generate_transactions(clients, 18, seed=3)
    merged = tx.merge(clients[["client_id", "profil_trajectoire"]], on="client_id")
    avg_by_profile = merged.groupby("profil_trajectoire")["solde_fin_mois"].mean()
    assert avg_by_profile["fragile_des_le_depart"] < avg_by_profile["stable"]
    assert avg_by_profile["degradation_progressive"] < avg_by_profile["stable"]


def test_fragile_profiles_have_more_incidents_than_stable():
    clients = generate_clients(300, seed=3)
    tx = generate_transactions(clients, 18, seed=3)
    merged = tx.merge(clients[["client_id", "profil_trajectoire"]], on="client_id")
    avg_incidents = merged.groupby("profil_trajectoire")["nb_incidents_paiement"].mean()
    assert avg_incidents["fragile_des_le_depart"] > avg_incidents["stable"]