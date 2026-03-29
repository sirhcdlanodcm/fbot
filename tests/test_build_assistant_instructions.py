"""Tests for functions.build_assistant_instructions."""

from constants import DEFAULT_OBJECTIVE, DEFAULT_TONE
from functions.build_assistant_instructions import build_instructions


def _minimal_prompt(**kwargs):
    return build_instructions(
        tone=DEFAULT_TONE,
        audience="Tag the user <@1>",
        objective=DEFAULT_OBJECTIVE,
        sentiment="5",
        current_user_id="<@1>",
        **kwargs,
    )


def test_standing_in_block_when_flag_true():
    text = _minimal_prompt(standing_in_for_cdogg=True)
    assert "# STANDING IN #" in text
    assert "CDogg" in text


def test_no_standing_in_when_flag_false():
    text = _minimal_prompt(standing_in_for_cdogg=False)
    assert "# STANDING IN #" not in text


def test_includes_league_json_and_champion():
    text = _minimal_prompt()
    assert "madden_league_users" in text
    assert "CDogg" in text
    assert "Cheeky Dave" in text

def test_objective_includes_light_touch_hint():
    text = build_instructions(
        tone=DEFAULT_TONE,
        audience="Tag the user <@1>",
        objective="Tease them gently",
        sentiment="5",
        current_user_id="<@1>",
    )
    assert "# OBJECTIVE #" in text
    assert "optional flavor" in text


def test_default_objective_skips_light_touch_paragraph():
    text = _minimal_prompt()
    assert "# OBJECTIVE #" not in text
    assert "optional flavor" not in text
