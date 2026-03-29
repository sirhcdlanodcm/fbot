"""Pure functions for deciding when the Discord bot should invoke the LLM."""

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class LlmTriggerState:
    should_respond: bool
    triggers_found: tuple[str, ...]
    cdogg_mentioned: bool


def compute_llm_trigger_state(
    content: str,
    mention_user_ids: Iterable[int],
    *,
    keyword_triggers: Sequence[str],
    cdogg_user_id: int,
) -> LlmTriggerState:
    """
    Match discord_bot on_message trigger rules without Discord types.

    :param content: message.content
    :param mention_user_ids: user.id for each entry in message.mentions
    :param keyword_triggers: e.g. BOT_TRIGGERS (case-sensitive substring match)
    :param cdogg_user_id: from get_cdogg_user_id()
    """
    triggers = tuple(t for t in keyword_triggers if t in content)
    ids = list(mention_user_ids)
    cdogg = (
        any(uid == cdogg_user_id for uid in ids)
        or f"<@{cdogg_user_id}>" in content
        or f"<@!{cdogg_user_id}>" in content
    )
    return LlmTriggerState(
        should_respond=bool(triggers) or cdogg,
        triggers_found=triggers,
        cdogg_mentioned=cdogg,
    )
