"""LLM Service - Factory for LLM providers."""

import logging

from bot.services.providers.openai_provider import OpenAIProvider
from bot.services.providers.gemini_provider import GeminiProvider
from config import load_config

logger = logging.getLogger(__name__)


class LLMService:
    """Service for generating LLM responses using configured provider."""
    
    @staticmethod
    def generate_response(
        provider_name: str = None,
        system_prompt: str = "",
        user_message: str = "",
        temperature: float = 0.7,
        max_tokens: int = 500,
        conversation_history: str = ""
    ) -> str:
        """
        Generate a response using the configured LLM provider.
        
        :param provider_name: Provider name ('openai' or 'gemini'). Defaults to config.
        :param system_prompt: System prompt/instructions
        :param user_message: User message
        :param temperature: Temperature setting
        :param max_tokens: Maximum tokens to generate
        :param conversation_history: Formatted conversation history (optional)
        :return: Generated response text
        """
        config = load_config()
        provider_name = provider_name or config.llm_provider
        logger.info(f"LLMService.generate_response called - provider: {provider_name}, system_prompt length: {len(system_prompt)}, user_message length: {len(user_message)}, history length: {len(conversation_history)}")
        
        # Get the appropriate provider
        logger.debug(f"Initializing {provider_name} provider")
        if provider_name.lower() == 'openai':
            provider = OpenAIProvider()
        elif provider_name.lower() == 'gemini':
            provider = GeminiProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {provider_name}. Supported: 'openai', 'gemini'")
        
        logger.info(f"Using {provider_name} provider with model: {provider.get_model_name()}")
        logger.debug(f"Generation parameters - temperature: {temperature}, max_tokens: {max_tokens}")
        
        # Generate response
        logger.info(f"Calling provider.generate_response()")
        response = provider.generate_response(
            system_prompt=system_prompt,
            user_message=user_message,
            temperature=temperature,
            max_tokens=max_tokens,
            conversation_history=conversation_history
        )
        logger.info(f"Provider returned response (length: {len(response)} chars)")
        return response

