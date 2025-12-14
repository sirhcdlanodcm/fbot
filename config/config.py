"""Bot configuration settings."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    """Bot configuration settings."""
    # Discord (required fields first for Python 3.7 compatibility)
    discord_token: str
    
    # LLM Provider (required)
    llm_provider: str = "gemini"  # Default to Gemini as requested
    
    # API Keys (optional, depending on provider)
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    # Discord (optional fields)
    command_prefix: str = "!"
    
    # Bot behavior
    testing_mode: bool = False
    
    # Model settings
    openai_model: str = "gpt-4o"
    openai_fallback_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2000  # Increased from 500 for longer Discord responses
    
    gemini_model: str = "gemini-2.5-flash"  # Updated to working model (tested via test_gemini.py)
    
    # Response settings
    response_timeout: int = 60  # seconds
    conversation_history_size: int = 5  # Number of messages to keep in conversation history
    
    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load configuration from environment variables."""
        discord_token = os.getenv('DISCORD_TOKEN') or os.getenv('bot_private_token')
        llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        
        if not discord_token:
            raise ValueError("DISCORD_TOKEN environment variable is not set")
        
        # Load provider-specific API keys
        openai_key = os.getenv('OPENAI_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        # Validate provider-specific keys
        if llm_provider == 'openai' and not openai_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set (required for OpenAI provider)")
        if llm_provider == 'gemini' and not gemini_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set (required for Gemini provider)")
        
        return cls(
            discord_token=discord_token,
            llm_provider=llm_provider,
            openai_api_key=openai_key,
            gemini_api_key=gemini_key,
            gemini_model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            testing_mode=os.getenv('TESTING_MODE', 'False').lower() == 'true',
            openai_model=os.getenv('OPENAI_MODEL', 'gpt-4o'),
            openai_fallback_model=os.getenv('OPENAI_FALLBACK_MODEL', 'gpt-4o-mini'),
            openai_max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '2000')),
            conversation_history_size=int(os.getenv('CONVERSATION_HISTORY_SIZE', '5')),
        )


def load_config() -> BotConfig:
    """Load and return bot configuration."""
    return BotConfig.from_env()

