"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
        conversation_history: str = ""
    ) -> str:
        """
        Generate a response from the LLM.
        
        :param system_prompt: System prompt/instructions
        :param user_message: User message
        :param temperature: Temperature setting (0.0-2.0)
        :param max_tokens: Maximum tokens to generate
        :return: Generated response text
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the model name being used.
        
        :return: Model name string
        """
        pass

