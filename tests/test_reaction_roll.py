"""Tests for bot.reaction_roll."""

import pytest

from bot.reaction_roll import should_add_random_reaction


@pytest.mark.parametrize(
    "probability,roll,expected",
    [
        (0.0, 0.01, False),
        (-0.5, 0.01, False),
        (0.1, 0.05, True),
        (0.1, 0.099, True),
        (0.1, 0.1, False),
        (0.1, 0.99, False),
        (1.0, 0.0, True),
        (1.0, 0.999, True),
        (2.0, 0.5, True),
    ],
)
def test_should_add_random_reaction(probability, roll, expected):
    assert should_add_random_reaction(probability, roll) is expected
