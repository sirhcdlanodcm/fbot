from openai import OpenAI
from openai import APIError, APIConnectionError, APITimeoutError, RateLimitError
import time
import asyncio
import logging

from config import load_config

# Load configuration
config = load_config()

# Create client with v2 Assistants API header
# Tested: default_headers works for all API calls
client = OpenAI(
    api_key=config.openai_api_key,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)
logger = logging.getLogger(__name__)

# Initialize assistant and thread lazily
_assistant = None
_thread = None

def reset_assistant_and_thread():
    """Reset the cached assistant and thread. Useful for testing or after code changes."""
    global _assistant, _thread
    _assistant = None
    _thread = None
    logger.info("Assistant and thread cache cleared")

def get_assistant():
    """Get or create the assistant instance."""
    global _assistant
    if _assistant is None:
        try:
            # Create assistant without file_ids (not needed for basic chat)
            # v2 header is set in client initialization
            _assistant = client.beta.assistants.create(
                model=config.openai_model,
                instructions="",
                name="FBot",
                tools=[]
            )
            logger.info(f"Created assistant with ID: {_assistant.id}")
        except (APIError, APIConnectionError) as e:
            logger.error(f"Failed to create assistant: {e}")
            raise
    return _assistant

def get_thread():
    """Get or create the thread instance."""
    global _thread
    if _thread is None:
        try:
            _thread = client.beta.threads.create()
            logger.info(f"Created thread with ID: {_thread.id}")
        except (APIError, APIConnectionError) as e:
            logger.error(f"Failed to create thread: {e}")
            raise
    return _thread

def _add_thread_message_sync(chatinput="", my_instructions=""):
    """
    Synchronous implementation of adding a message to the thread.
    This will be run in a thread pool to avoid blocking the event loop.
    
    :param chatinput: The user's message input
    :param my_instructions: Custom instructions for this interaction
    :return: The assistant's response text
    """
    try:
        assistant = get_assistant()
        thread = get_thread()
        
        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=chatinput
        )

        # Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=my_instructions
        )

        # Wait for the run to complete
        timeout = time.time() + config.response_timeout
        while run.status in ["queued", "in_progress"]:
            if time.time() > timeout:
                raise TimeoutError("Timed out waiting for the run to complete.")
            
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run.status == "completed":
                # Retrieve the messages added by the Assistant
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                
                # Return the assistant's response (first message is the latest)
                if messages.data and messages.data[0].content:
                    return messages.data[0].content[0].text.value
                else:
                    raise ValueError("No response from assistant")
            
            elif run.status in ["queued", "in_progress"]:
                time.sleep(1)  # Wait for 1 second before the next check
            else:
                raise RuntimeError(f"Run failed with status: {run.status}")
    
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded: {e}")
        raise
    except APITimeoutError as e:
        logger.error(f"API timeout: {e}")
        raise
    except APIConnectionError as e:
        logger.error(f"API connection error: {e}")
        raise
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in add_thread_message: {e}")
        raise

async def add_thread_message(chatinput="", my_instructions=""):
    """
    Add a message to the thread and get a response from the assistant (async).
    Runs the blocking OpenAI calls in a thread pool to avoid blocking the event loop.
    
    :param chatinput: The user's message input
    :param my_instructions: Custom instructions for this interaction
    :return: The assistant's response text
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        _add_thread_message_sync, 
        chatinput, 
        my_instructions
    )