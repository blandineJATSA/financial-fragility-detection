"""Tests de sanite pour les scenarios de degradation."""

import numpy as np

from data_generation.fragility_scenarios import (
    degradation_factors_for_month,
    pick_transition_month,
)


def test_transition_month_within_expected_range():
    rng = np.random.default_rng(1)
    for _ in range(100):
        t = pick_transition_month(18, rng)
        assert 9 <= t <= 16


def test_factors_before_signal_start_are_neutral():
    factors = degradation_factors_for_month(0, transition_month=12)
    assert factors["revenu_multiplier"] == 1.0
    assert factors["incident_rate"] == 0.02


def test_degradation_is_monotonic_before_transition():
    transition = 12
    signal_start = transition - 6
    incident_rates = [
        degradation_factors_for_month(m, transition)["incident_rate"]
        for m in range(signal_start, transition)
    ]
    assert incident_rates == sorted(incident_rates)


def test_factors_stable_after_transition():
    f9 = degradation_factors_for_month(9, transition_month=9)
    f15 = degradation_factors_for_month(15, transition_month=9)
    assert f9 == f15