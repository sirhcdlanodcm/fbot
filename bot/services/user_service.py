"""User service for managing user configurations and lookups."""

from typing import Optional, Union
import discord
from config.users import get_user_config, UserConfig
from constants import DEFAULT_TONE, DEFAULT_OBJECTIVE


class UserService:
    """Service for user-related operations."""
    
    @staticmethod
    def get_user_key(author: Union[discord.Member, discord.User]) -> str:
        """
        Get the user key for looking up configurations.
        Tries multiple formats to match user configurations.
        
        :param author: The Discord user object
        :return: The user key string
        """
        # Try different formats to match user configurations
        username_str = str(author)
        username_name = author.name
        username_with_discrim = f"{author.name}#0"  # Old format fallback
        
        # Import here to avoid circular imports
        from config.users import USER_TONES, USER_OBJECTIVES
        
        # Check which format exists in the configs
        if username_str in USER_TONES or username_str in USER_OBJECTIVES:
            return username_str
        elif username_name in USER_TONES or username_name in USER_OBJECTIVES:
            return username_name
        elif username_with_discrim in USER_TONES or username_with_discrim in USER_OBJECTIVES:
            return username_with_discrim
        else:
            # Return the standard format for logging
            return username_str
    
    @staticmethod
    def get_user_config_for_author(author: Union[discord.Member, discord.User]) -> UserConfig:
        """
        Get user configuration for a Discord author.
        
        :param author: The Discord user object
        :return: UserConfig object
        """
        user_key = UserService.get_user_key(author)
        return get_user_config(user_key)
    
    @staticmethod
    def get_user_key_from_string(userinput: str) -> str:
        """
        Get the user key for looking up configurations from a string.
        Tries multiple formats to match user configurations.
        
        :param userinput: The user identifier string
        :return: The user key string
        """
        from config.users import USER_TONES, USER_OBJECTIVES
        
        # Try different formats to match user configurations
        if userinput in USER_TONES or userinput in USER_OBJECTIVES:
            return userinput
        
        # Try without discriminator if it has one
        if "#" in userinput:
            username_only = userinput.split("#")[0]
            if username_only in USER_TONES or username_only in USER_OBJECTIVES:
                return username_only
        
        # Try adding #0 discriminator (old format)
        username_with_discrim = f"{userinput.split('#')[0] if '#' in userinput else userinput}#0"
        if username_with_discrim in USER_TONES or username_with_discrim in USER_OBJECTIVES:
            return username_with_discrim
        
        # Return original if no match found
        return userinput

