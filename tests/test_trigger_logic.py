"""Tests for bot.trigger_logic."""

import pytest

from bot.trigger_logic import LlmTriggerState, compute_llm_trigger_state


@pytest.fixture
def triggers():
    return ("Fuckbot", "Friendbot")


def test_keyword_friendbot(triggers):
    state = compute_llm_trigger_state(
        "Hey Friendbot what's up",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=690043477374795826,
    )
    assert state == LlmTriggerState(
        should_respond=True,
        triggers_found=("Friendbot",),
        cdogg_mentioned=False,
    )


def test_keyword_fuckbot(triggers):
    state = compute_llm_trigger_state(
        "Fuckbot help",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=690043477374795826,
    )
    assert state.should_respond is True
    assert state.triggers_found == ("Fuckbot",)
    assert state.cdogg_mentioned is False


def test_case_sensitive_no_match(triggers):
    state = compute_llm_trigger_state(
        "friendbot lowercase",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=690043477374795826,
    )
    assert state.should_respond is False


def test_cdogg_mention_in_content(triggers):
    cid = 690043477374795826
    state = compute_llm_trigger_state(
        f"<@{cid}> you there?",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=cid,
    )
    assert state.should_respond is True
    assert state.triggers_found == ()
    assert state.cdogg_mentioned is True


def test_cdogg_nickname_mention_form(triggers):
    cid = 690043477374795826
    state = compute_llm_trigger_state(
        f"<@!{cid}> ping",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=cid,
    )
    assert state.cdogg_mentioned is True


def test_cdogg_in_mentions_iterable(triggers):
    cid = 690043477374795826
    state = compute_llm_trigger_state(
        "yo",
        [111, cid, 222],
        keyword_triggers=triggers,
        cdogg_user_id=cid,
    )
    assert state.cdogg_mentioned is True
    assert state.should_respond is True


def test_friendbot_and_cdogg(triggers):
    cid = 690043477374795826
    state = compute_llm_trigger_state(
        f"Friendbot ask <@{cid}> too",
        [],
        keyword_triggers=triggers,
        cdogg_user_id=cid,
    )
    assert state.should_respond is True
    assert state.triggers_found == ("Friendbot",)
    assert state.cdogg_mentioned is True
