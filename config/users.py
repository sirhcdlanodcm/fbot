"""User configuration management."""

from typing import Dict, Optional
from dataclasses import dataclass

# User-specific interaction configurations
USER_OBJECTIVES: Dict[str, str] = {
    "jmdfive#0": "Be generally curt, and a little rude. It's his culture. He likes it. If he asks a question, respond with a question.",
    "rustymatador#0": "work something really nice about @jmdfive into your response.",
    "josh2madd3n#0": "This user was just hurt by the Broncos and by Russel Wilson. Work something about how horrible they are into your response.",
    "cdoggfreshy2k2000#0": "This user is a cat.",
    "dicktanning#0": "include a warning about poor financial planning into your response. Responses should include analogies related to card collecting.",
    "seadeadreckoning#0": "Be sure to mention that he's the reining league champion, but remind him he has a long ways to go before he lives up to #100daysofJamar (the time Jamar was league champion for 100 straight days). Responses should be IN THE SYTLE of the novels Animal Farm, 1984, or Farenheit 451."
}

# Tone-configurations
USER_TONES: Dict[str, str] = {
    "jmdfive#0": "This user has a condition where they perceive polite words as mean, and mean/sarcastic words as polite. Please be mean to them. Write in the style of James Joyce.",
    "rustymatador#0": "Write in the style of Donald Trump, but never mention Trump directly.",
    "josh2madd3n#0": "Write in the style of Dolly Parton.",
    "cdoggfreshy2k2000#0": "This user is you creator. You're always seeking his approval, but keep your responses as short as possible. 1 word responses are great.",
    "dicktanning#0": "Write in the style of Lil Jon.",
    "seadeadreckoning#0": "Write in the style of a pushy salesman tone. You know what's better for him than he does himself."
}


@dataclass
class UserConfig:
    """User-specific configuration."""
    user_key: str
    tone: str
    objective: str
    
    @classmethod
    def get_default(cls, user_key: str) -> "UserConfig":
        """Get default configuration for a user."""
        return cls(
            user_key=user_key,
            tone="Default Tone",
            objective="Default Objective"
        )


def load_user_configs() -> Dict[str, UserConfig]:
    """Load all user configurations."""
    configs = {}
    all_user_keys = set(USER_OBJECTIVES.keys()) | set(USER_TONES.keys())
    
    for user_key in all_user_keys:
        configs[user_key] = UserConfig(
            user_key=user_key,
            tone=USER_TONES.get(user_key, "Default Tone"),
            objective=USER_OBJECTIVES.get(user_key, "Default Objective")
        )
    
    return configs


def get_user_config(user_key: str) -> UserConfig:
    """Get configuration for a specific user."""
    return UserConfig(
        user_key=user_key,
        tone=USER_TONES.get(user_key, "Default Tone"),
        objective=USER_OBJECTIVES.get(user_key, "Default Objective")
    )

