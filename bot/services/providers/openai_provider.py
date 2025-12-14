"""OpenAI provider implementation."""

from openai import OpenAI
from openai import APIError, APIConnectionError, APITimeoutError, RateLimitError
import logging

from bot.services.llm_provider import LLMProvider
from config import load_config

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI Chat Completions API provider."""
    
    def __init__(self, model: str = None, api_key: str = None):
        """
        Initialize OpenAI provider.
        
        :param model: Model name (defaults to config)
        :param api_key: API key (defaults to config)
        """
        config = load_config()
        self.api_key = api_key or config.openai_api_key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.model = model or config.openai_fallback_model
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        conversation_history: str = ""
    ) -> str:
        """Generate response using OpenAI Chat Completions."""
        try:
            # Build messages array
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                # Include history as context in the system message or as a separate user message
                history_context = f"{conversation_history}\n\n"
                messages.append({"role": "user", "content": history_context})
                logger.debug(f"Including conversation history ({len(conversation_history)} chars) in OpenAI request")
            
            # Add the current user message
            messages.append({"role": "user", "content": user_message})
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return completion.choices[0].message.content
        
        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise
        except APITimeoutError as e:
            logger.error(f"OpenAI API timeout: {e}")
            raise
        except APIConnectionError as e:
            logger.error(f"OpenAI API connection error: {e}")
            raise
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI provider: {e}")
            raise
    
    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model

