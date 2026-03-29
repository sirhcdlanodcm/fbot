"""Configuration module for FriendBot."""

from .config import BotConfig, load_config

__all__ = ["BotConfig", "load_config", "UserConfig", "load_user_configs"]


def __getattr__(name: str):
    if name == "UserConfig":
        from .users import UserConfig

        return UserConfig
    if name == "load_user_configs":
        from .users import load_user_configs

        return load_user_configs
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
