"""Tests for config.league_status."""

import pytest

from config import league_status as ls


@pytest.fixture(autouse=True)
def clear_league_champion_env(monkeypatch):
    monkeypatch.delenv("LEAGUE_CHAMPION", raising=False)


def test_get_cdogg_user_id():
    assert ls.get_cdogg_user_id() == 690043477374795826


def test_get_champion_name_matches_config():
    assert ls.get_champion_name() == "Jamar"


def test_get_champion_mention():
    assert ls.get_champion_mention() == "<@968386433389834241>"


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


@pytest.mark.parametrize(
    "value,expected_key",
    [
        ("Cheeky Dave", "rustymatador#0"),
        ("cheeky dave", "rustymatador#0"),
        ("rustymatador", "rustymatador#0"),
        ("rustymatador#0", "rustymatador#0"),
        ("RUSTYMATADOR#0", "rustymatador#0"),
        ("949518034551332885", "rustymatador#0"),
        ("<@949518034551332885>", "rustymatador#0"),
        ("<@!949518034551332885>", "rustymatador#0"),
        ("Jamar", "jmdfive#0"),
        ("J-Sizzle", "seadeadreckoning#0"),
    ],
)
def test_get_champion_key_from_env(monkeypatch, value, expected_key):
    monkeypatch.setenv("LEAGUE_CHAMPION", value)
    assert ls.get_champion_key() == expected_key


def test_get_champion_key_invalid_env_falls_back(monkeypatch, caplog):
    import logging

    monkeypatch.setenv("LEAGUE_CHAMPION", "not-a-real-coach")
    caplog.set_level(logging.WARNING)
    assert ls.get_champion_key() == ls.LEAGUE_CHAMPION_ID
    assert "did not match" in caplog.text


def test_champion_env_hints_is_generic():
    hints = ls.champion_env_hints()
    assert "LEAGUE_MEMBERS" in hints
    assert "numeric Discord user ID" in hints
    assert "Jamar" not in hints
