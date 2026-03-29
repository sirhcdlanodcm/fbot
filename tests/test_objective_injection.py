"""Tests for bot.objective_injection."""

import pytest

from bot.objective_injection import omit_custom_objective
from constants import DEFAULT_OBJECTIVE


def test_no_custom_objective_never_omits():
    assert omit_custom_objective(DEFAULT_OBJECTIVE, DEFAULT_OBJECTIVE, 0.4, 0.99) is False


def test_probability_one_never_omits_custom():
    assert omit_custom_objective("roast the user", DEFAULT_OBJECTIVE, 1.0, 0.99) is False


def test_probability_zero_always_omits_custom():
    assert omit_custom_objective("roast the user", DEFAULT_OBJECTIVE, 0.0, 0.01) is True


@pytest.mark.parametrize(
    "roll,expected",
    [
        (0.0, False),
        (0.39, False),
        (0.4, True),
        (0.99, True),
    ],
)
def test_threshold_at_p_point_four(roll, expected):
    assert omit_custom_objective("custom line", DEFAULT_OBJECTIVE, 0.4, roll) is expected


def test_probability_clamped_high():
    assert omit_custom_objective("x", DEFAULT_OBJECTIVE, 2.0, 0.5) is False


def test_probability_clamped_low():
    assert omit_custom_objective("x", DEFAULT_OBJECTIVE, -1.0, 0.5) is True
