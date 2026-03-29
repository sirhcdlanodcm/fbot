"""Tests for bot.services.conversation_history."""

from bot.services.conversation_history import ConversationHistory


def test_add_and_trim_to_max_size():
    h = ConversationHistory(max_history_size=2)
    cid = 100
    h.add_message(cid, "A", "1")
    h.add_message(cid, "B", "2")
    h.add_message(cid, "C", "3")
    msgs = h.get_history(cid)
    assert [m.author for m in msgs] == ["B", "C"]
    assert [m.content for m in msgs] == ["2", "3"]


def test_format_history_sanitizes_fuckbot():
    h = ConversationHistory(max_history_size=10)
    cid = 200
    h.add_message(cid, "User", "Fuckbot said hi")
    out = h.format_history_for_llm(cid, bot_name="TestBot")
    assert "Fuckbot" not in out
    assert "Friendbot" in out


def test_format_skips_bot_author():
    h = ConversationHistory(max_history_size=10)
    cid = 300
    h.add_message(cid, "Human", "hello")
    h.add_message(cid, "MyBot", "beep")
    out = h.format_history_for_llm(cid, bot_name="MyBot")
    assert "Human" in out
    assert "beep" not in out


def test_clear_history():
    h = ConversationHistory(max_history_size=5)
    cid = 400
    h.add_message(cid, "X", "y")
    h.clear_history(cid)
    assert h.get_history(cid) == []
