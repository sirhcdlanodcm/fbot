"""User configuration management."""

import random
from typing import Dict, Optional, Sequence, Union, List
from dataclasses import dataclass
from constants import DEFAULT_TONE, DEFAULT_OBJECTIVE
from config.league_status import get_champion_name, get_team_for_user

CURRENT_CHAMPION_NAME = get_champion_name()


def _team_line(user_key: str) -> str:
    team = get_team_for_user(user_key)
    return f" Their current team is {team}." if team else ""

# User-specific interaction configurations
# Values can be a single string or a pool of strings for variation.
USER_OBJECTIVES: Dict[str, Union[str, Sequence[str]]] = {
    "jmdfive#0": [
        f"Be generally curt and a little rude. If he asks a question, respond with a question.{_team_line('jmdfive#0')}",
        f"Lightly roast his play-calling like you have seen it for years.{_team_line('jmdfive#0')}",
        f"Challenge him to a rematch and imply he dodged the last one.{_team_line('jmdfive#0')}",
        f"Remind him the scoreboard has a memory, even if he pretends not to.{_team_line('jmdfive#0')}"
    ],
    "rustymatador#0": [
        f"Work something really nice about @jmdfive into your response.{_team_line('rustymatador#0')}",
        f"Hype his confidence while quietly predicting a late-game collapse.{_team_line('rustymatador#0')}",
        f"Congratulate his roster, then point out one position that is a mess.{_team_line('rustymatador#0')}",
        f"Bring up a funny old league moment like it was yesterday.{_team_line('rustymatador#0')}"
    ],
    "josh2madd3n#0": [
        f"This user was just hurt by the Broncos and by Russel Wilson. Mention how horrible they are.{_team_line('josh2madd3n#0')}",
        f"Tease him about his run defense like it owes you money.{_team_line('josh2madd3n#0')}",
        f"Compare his team to a classic car that looks great but always stalls.{_team_line('josh2madd3n#0')}",
        f"Remind him the comeback is coming, then doubt it anyway.{_team_line('josh2madd3n#0')}"
    ],
    "cdoggfreshy2k2000#0": [
        f"This user used to be great, but he hasn't won in a very long time. Remind him of that.{_team_line('cdoggfreshy2k2000#0')}",
        f"Bring up the glory days when he used to win sometimes.{_team_line('cdoggfreshy2k2000#0')}"
    ],
    "dicktanning#0": [
        f"Include a warning about poor financial planning and use analogies related to card collecting.{_team_line('dicktanning#0')}",
        f"Compare his cap space to a binder with missing rare inserts.{_team_line('dicktanning#0')}",
        f"Talk about trading picks like swapping graded rookies at a show.{_team_line('dicktanning#0')}",
        f"Mention interest rates like they are linebacker ratings.{_team_line('dicktanning#0')}"
    ],
    "seadeadreckoning#0": [
        f"Mention {CURRENT_CHAMPION_NAME} is the reigning league champion, but note he is far from #100daysofJamar. Use a dystopian flavor.{_team_line('seadeadreckoning#0')}",
        f"Praise the crown, then warn the league is watching and waiting. Use a dystopian flavor.{_team_line('seadeadreckoning#0')}",
        f"Say the champion banner is loud, but the dynasty is unproven. Use a dystopian flavor.{_team_line('seadeadreckoning#0')}",
        f"Invoke the idea of a surveillance league where wins are counted forever. Use a dystopian flavor.{_team_line('seadeadreckoning#0')}"
    ]
}

# Tone pool shared by all users
TONE_POOL: List[str] = [
    "Be mean and sarcastic, but in a friendly way he enjoys. Write with a James Joyce flavor.",
    "Keep it curt and cutting, like a veteran trash talker.",
    "Dry wit, short sentences, and a little smug.",
    "Rough and playful, like old friends jawing in a group chat.",
    "Bold, braggy, and confident, but never mention any real person.",
    "Talk like a hype man selling his own greatness.",
    "Over-the-top confidence with simple, punchy lines.",
    "Smooth and smug, like a postgame interview from a winner.",
    "Warm, friendly, and playful with a little country sparkle.",
    "Cheerful and teasing, like a coach with a grin.",
    "Big-hearted but still roasting him gently.",
    "Sing-song cadence without actually singing.",
    "High-energy, loud, and hype, like a sports arena.",
    "Big exclamations, short bursts, lots of swagger.",
    "Over-the-top and rowdy, like a tailgate chant.",
    "Aggressive enthusiasm with quick punchlines.",
    "Respond using only emojis.",
    "Respond using only hashtags.",
    "One-word replies only.",
    "respond only using emojis",
    "Respond only using hashtags",
]

# User-specific tone overrides (optional)
USER_TONES: Dict[str, Union[str, Sequence[str]]] = {}


@dataclass
class UserConfig:
    """User-specific configuration."""
    user_key: str
    tone: Optional[str]
    objective: Optional[str]
    
    @classmethod
    def get_default(cls, user_key: str) -> "UserConfig":
        """Get default configuration for a user."""
        return cls(
            user_key=user_key,
            tone=DEFAULT_TONE,
            objective=DEFAULT_OBJECTIVE
        )


def load_user_configs() -> Dict[str, UserConfig]:
    """Load all user configurations."""
    configs = {}
    all_user_keys = set(USER_OBJECTIVES.keys()) | set(USER_TONES.keys())
    
    for user_key in all_user_keys:
        configs[user_key] = UserConfig(
            user_key=user_key,
            tone=_resolve_tone(user_key),
            objective=_resolve_config_value(USER_OBJECTIVES.get(user_key), DEFAULT_OBJECTIVE)
        )
    
    return configs


def get_user_config(user_key: str) -> UserConfig:
    """Get configuration for a specific user."""
    return UserConfig(
        user_key=user_key,
        tone=_resolve_tone(user_key),
        objective=_resolve_config_value(USER_OBJECTIVES.get(user_key), DEFAULT_OBJECTIVE)
    )


def _resolve_config_value(value: Optional[Union[str, Sequence[str]]], default: str) -> str:
    """Resolve a config value from a single string or a pool of strings."""
    if value is None:
        return default
    if isinstance(value, str):
        return value
    if isinstance(value, Sequence):
        pool = [item for item in value if isinstance(item, str) and item.strip()]
        if not pool:
            return default
        return random.choice(pool)
    return default


def _resolve_tone(user_key: str) -> str:
    """Resolve a tone for a user, using a shared pool by default."""
    override = USER_TONES.get(user_key)
    if override is not None:
        return _resolve_config_value(override, DEFAULT_TONE)
    if not TONE_POOL:
        return DEFAULT_TONE
    return random.choice(TONE_POOL)

