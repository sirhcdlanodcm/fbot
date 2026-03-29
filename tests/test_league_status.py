"""Tests for config.league_status."""

import pytest

from config import league_status as ls


def test_get_cdogg_user_id():
    assert ls.get_cdogg_user_id() == 690043477374795826


def test_get_champion_name_matches_config():
    assert ls.get_champion_name() == "Cheeky Dave"


def test_get_champion_mention():
    assert ls.get_champion_mention() == "<@949518034551332885>"


@pytest.mark.parametrize(
    "key,expected",
    [
        ("rustymatador#0", "Penn State"),
        ("cdoggfreshy2k2000#0", "North Carolina"),
        ("unknown#0", None),
    ],
)
def test_get_team_for_user(key, expected):
    assert ls.get_team_for_user(key) == expected
