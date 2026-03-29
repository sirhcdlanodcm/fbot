"""League status configuration for easy updates."""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

CDOGG_USER_KEY = "cdoggfreshy2k2000#0"

# League member information
LEAGUE_MEMBERS = [
    {"key": "jmdfive#0", "name": "Jamar", "id": "<@968386433389834241>"},
    {"key": "rustymatador#0", "name": "Cheeky Dave", "id": "<@949518034551332885>"},
    {"key": "josh2madd3n#0", "name": "JP", "id": "<@968697658728415253>"},
    {"key": "seadeadreckoning#0", "name": "J-Sizzle", "id": "<@968681678908293160>"},
    {"key": "dicktanning#0", "name": "Troy", "id": "<@968700143195029534>"},
    {"key": "cdoggfreshy2k2000#0", "name": "CDogg", "id": "<@690043477374795826>"},
]

# Default champion key if env LEAGUE_CHAMPION is unset or invalid (use user key)
LEAGUE_CHAMPION_ID = "jmdfive#0"

# Env: LEAGUE_CHAMPION — see champion_env_hints().


def _snowflake_from_mention_field(value: str) -> Optional[str]:
    """Parse Discord user id digits from mention or bare numeric string."""
    s = str(value).strip()
    if not s:
        return None
    inner = s.strip("<@!>")
    if inner.isdigit():
        return inner
    return None


def champion_env_hints() -> str:
    """Generic description for logs (does not list roster names or usernames)."""
    return (
        "LEAGUE_CHAMPION must match someone in config/league_status.py LEAGUE_MEMBERS: "
        "roster display name, Discord username (part before # in key), full key (user#0), "
        "numeric Discord user ID, or <@id> mention form"
    )


def get_champion_key() -> str:
    """
    Active champion user key (LEAGUE_MEMBERS key string).

    Override with env LEAGUE_CHAMPION; falls back to LEAGUE_CHAMPION_ID if unset or no match.
    """
    raw = os.getenv("LEAGUE_CHAMPION", "").strip()
    if not raw:
        return LEAGUE_CHAMPION_ID

    needle = raw.lower()
    raw_snowflake = _snowflake_from_mention_field(raw)
    for m in LEAGUE_MEMBERS:
        key = str(m.get("key", ""))
        if not key:
            continue
        name = (m.get("name") or "").strip().lower()
        user_part = key.split("#", 1)[0].lower() if "#" in key else key.lower()
        member_sf = _snowflake_from_mention_field(str(m.get("id", "")))
        if raw_snowflake and member_sf and raw_snowflake == member_sf:
            return key
        if needle == key.lower() or needle == user_part or (name and needle == name):
            return key

    logger.warning(
        "LEAGUE_CHAMPION=%r did not match any member; using default %s. %s",
        raw,
        LEAGUE_CHAMPION_ID,
        champion_env_hints(),
    )
    return LEAGUE_CHAMPION_ID


def log_league_champion_for_operators() -> None:
    """Call once after logging is configured (e.g. from discord on_ready)."""
    key = get_champion_key()
    raw = os.getenv("LEAGUE_CHAMPION", "").strip()
    if raw:
        logger.info(
            "League champion from LEAGUE_CHAMPION=%r -> %s (%s). %s",
            raw,
            _name_for_key(key),
            key,
            champion_env_hints(),
        )
    else:
        logger.info(
            "League champion: %s (%s). Override with env LEAGUE_CHAMPION (no image rebuild). %s",
            _name_for_key(key),
            key,
            champion_env_hints(),
        )


def _name_for_key(key: str) -> str:
    for m in LEAGUE_MEMBERS:
        if m.get("key") == key:
            return str(m.get("name") or key)
    return key


# Current teams by user key (update as rosters change)
LEAGUE_TEAMS: Dict[str, str] = {
    "jmdfive#0": "Texas",
    "rustymatador#0": "Penn State",
    "josh2madd3n#0": "RIP",
    "cdoggfreshy2k2000#0": "North Carolina",
    "dicktanning#0": "USC",
    "seadeadreckoning#0": "Michigan",
}


def get_cdogg_user_id() -> int:
    """Discord numeric user id for CDogg, parsed from LEAGUE_MEMBERS."""
    for member in LEAGUE_MEMBERS:
        if member.get("key") == CDOGG_USER_KEY:
            raw = str(member.get("id", "")).strip()
            # Formats: <@id> or <@!id> (nickname mention)
            inner = raw.strip("<@!>")
            return int(inner)
    raise ValueError(f"No league member with key {CDOGG_USER_KEY!r}")


def get_champion_name() -> str:
    """Return the champion's display name, falling back to the key."""
    ck = get_champion_key()
    for member in LEAGUE_MEMBERS:
        if member.get("key") == ck:
            return member.get("name") or ck
    return ck


def get_champion_mention() -> str:
    """Return the champion's mention id, falling back to the key."""
    ck = get_champion_key()
    for member in LEAGUE_MEMBERS:
        if member.get("key") == ck:
            return member.get("id") or ck
    return ck


def get_team_for_user(user_key: str) -> Optional[str]:
    """Return the current team name for a user key if available."""
    team = LEAGUE_TEAMS.get(user_key)
    if team and team != "Unknown Team":
        return team
    return None
