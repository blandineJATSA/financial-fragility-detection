"""Injecte les patterns de degradation progressive dans les trajectoires clients.

Voir docs/00_business_context.md pour la definition des profils.

Ce module ne genere pas de vraies transactions : il produit, pour chaque mois
de la trajectoire d'un client en degradation, un jeu de facteurs (multiplicateurs
et taux) que generate_transactions.py applique aux montants de base du client.
"""

import numpy as np


def pick_transition_month(n_months: int, rng: np.random.Generator) -> int:
    """
    Tire le mois de bascule (franchissement des seuils legaux) pour un client
    en degradation progressive. Volontairement variable d'un client a l'autre
    (entre 55% et 85% de la periode observee) pour que le modele apprenne de
    vrais signaux comportementaux, pas juste "le mois calendaire".
    """
    low = int(n_months * 0.55)
    high = int(n_months * 0.85)
    return int(rng.integers(low, high + 1))


def degradation_factors_for_month(month_index: int, transition_month: int) -> dict:
    """
    Retourne les facteurs de degradation pour un mois donne (0-indexe) d'un
    client au profil degradation_progressive.

    Phases :
    - avant (transition_month - 6) : comportement normal
    - de (transition_month - 6) a (transition_month - 1) : signaux faibles,
      degradation progressive et croissante
    - a partir de transition_month : seuils legaux franchis, installes
    """
    signal_start = transition_month - 6

    if month_index < signal_start:
        return {
            "revenu_multiplier": 1.0,
            "charges_multiplier": 1.0,
            "incident_rate": 0.02,
            "decouvert_rate": 0.02,
            "revenu_volatility": 0.05,
        }

    if month_index < transition_month:
        progress = (month_index - signal_start + 1) / 6  # de ~0.17 a 1.0
        return {
            "revenu_multiplier": 1.0 - 0.15 * progress,
            "charges_multiplier": 1.0 + 0.10 * progress,
            "incident_rate": 0.02 + 0.25 * progress,
            "decouvert_rate": 0.05 + 0.35 * progress,
            "revenu_volatility": 0.05 + 0.20 * progress,
        }

    return {
        "revenu_multiplier": 0.80,
        "charges_multiplier": 1.15,
        "incident_rate": 0.55,
        "decouvert_rate": 0.70,
        "revenu_volatility": 0.30,
    }