from openai import OpenAI
from openai import APIError, APIConnectionError, APITimeoutError, RateLimitError
import random
import logging

from config import load_config
from bot.services.user_service import UserService
from config.users import get_user_config
from functions.build_assistant_instructions import build_instructions

# Load configuration
config = load_config()

client = OpenAI(api_key=config.openai_api_key)
logger = logging.getLogger(__name__)

def get_openai_chat(chatinput="", userinput=""):
    """
    Get a chat completion from OpenAI using user-specific prompts.
    
    :param chatinput: The user's message input
    :param userinput: The user identifier (e.g., "username#discriminator" or just "username")
    :return: The completion message object
    """
    # Get user key that matches configuration format
    user_key = UserService.get_user_key_from_string(userinput)
    
    # Get user-specific configuration
    user_config = get_user_config(user_key)
    sentiment = str(random.randint(1, 10))
    
    # Build system prompt from user configuration
    # Note: We need to extract the user ID from the userinput string
    # For Discord, userinput is typically "username#discriminator" format
    # We'll use a placeholder mention format
    audience = f"Tag the user {userinput}"
    current_user_id = f"<@{userinput}>"  # Placeholder format
    
    system_content = build_instructions(
        tone=user_config.tone,
        audience=audience,
        objective=user_config.objective,
        sentiment=sentiment,
        current_user_id=current_user_id
    )
    
    try:
        completion = client.chat.completions.create(
            model=config.openai_fallback_model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": chatinput}
            ],
            temperature=config.openai_temperature,
            max_tokens=config.openai_max_tokens
        )
        
        return completion.choices[0].message
    
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded for user {userinput}: {e}")
        raise
    except APITimeoutError as e:
        logger.error(f"API timeout for user {userinput}: {e}")
        raise
    except APIConnectionError as e:
        logger.error(f"API connection error for user {userinput}: {e}")
        raise
    except APIError as e:
        logger.error(f"OpenAI API error for user {userinput}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_openai_chat for user {userinput}: {e}")
        raise