"""League status configuration for easy updates."""

from typing import Dict, Optional

# League member information
LEAGUE_MEMBERS = [
    {"key": "jmdfive#0", "name": "Jamar", "id": "<@968386433389834241>"},
    {"key": "rustymatador#0", "name": "J-Sizzle", "id": "<@968681678908293160>"},
    {"key": "josh2madd3n#0", "name": "JP", "id": "<@968697658728415253>"},
    {"key": "seadeadreckoning#0", "name": "Cheeky Dave", "id": "<@949518034551332885>"},
    {"key": "dicktanning#0", "name": "Troy", "id": "<@968700143195029534>"},
    {"key": "cdoggfreshy2k2000#0", "name": "CDogg", "id": "<@690043477374795826>"},
]

# Current league champion (use user key for easy updates)
LEAGUE_CHAMPION_ID = "rustymatador#0"

# Current teams by user key (update as rosters change)
LEAGUE_TEAMS: Dict[str, str] = {
    "jmdfive#0": "Texas",
    "rustymatador#0": "Penn State",
    "josh2madd3n#0": "RIP",
    "cdoggfreshy2k2000#0": "North Carolina",
    "dicktanning#0": "USC",
    "seadeadreckoning#0": "Michigan",
}


def get_champion_name() -> str:
    """Return the champion's display name, falling back to the key."""
    for member in LEAGUE_MEMBERS:
        if member.get("key") == LEAGUE_CHAMPION_ID:
            return member.get("name") or LEAGUE_CHAMPION_ID
    return LEAGUE_CHAMPION_ID


def get_champion_mention() -> str:
    """Return the champion's mention id, falling back to the key."""
    for member in LEAGUE_MEMBERS:
        if member.get("key") == LEAGUE_CHAMPION_ID:
            return member.get("id") or LEAGUE_CHAMPION_ID
    return LEAGUE_CHAMPION_ID


def get_team_for_user(user_key: str) -> Optional[str]:
    """Return the current team name for a user key if available."""
    team = LEAGUE_TEAMS.get(user_key)
    if team and team != "Unknown Team":
        return team
    return None

