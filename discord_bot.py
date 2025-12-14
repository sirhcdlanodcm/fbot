"""
discord_bot.py

A Discord bot designed to interact with users in a server based on specific user configurations and objectives.
"""

import random
import discord
from discord.ext import commands
import logging

from config import load_config
from bot.services.user_service import UserService
from bot.services.llm_service import LLMService
from bot.services.conversation_history import ConversationHistory
from functions.build_assistant_instructions import build_instructions
from constants import BOT_TRIGGERS, ERROR_TIMEOUT, ERROR_GENERIC, ERROR_REPLY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Initialize conversation history manager
conversation_history = ConversationHistory(max_history_size=config.conversation_history_size)
logger.info(f"Conversation history initialized with max_history_size={config.conversation_history_size}")

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.messages = True
# Note: message_content intent is only needed in discord.py 2.0+
# In 1.7.3, message content is available by default when messages intent is enabled
try:
    intents.message_content = True
except AttributeError:
    # discord.py < 2.0 doesn't have message_content attribute
    pass
bot = commands.Bot(command_prefix=config.command_prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    logger.info(f'{bot.user.name} has connected to Discord!')
    # try:
    #     scheduler.add_job(scheduled_message, 'interval', hours=19)
    #     scheduler.start()
    # except SchedulerAlreadyRunningError:
    #     pass  # Scheduler is already running, no action needed

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    logger.info(f"Message from {message.author}: {message.content}")

    ## No action triggered from bot messages
    if message.author == bot.user: 
        logger.debug(f"Ignoring message from bot itself")
        return

    # Track all messages in conversation history (for context)
    # Use channel ID to maintain separate history per channel/thread
    channel_id = message.channel.id
    author_name = str(message.author.display_name) if hasattr(message.author, 'display_name') else str(message.author)
    conversation_history.add_message(
        channel_id=channel_id,
        author=author_name,
        content=message.content
    )
    logger.debug(f"Added message to conversation history for channel {channel_id}")
    
    # Log current conversation history state
    current_history = conversation_history.get_history(channel_id)
    logger.info(f"Conversation history for channel {channel_id} now has {len(current_history)} messages:")
    for i, msg in enumerate(current_history, 1):
        logger.info(f"  {i}. {msg.author}: {msg.content[:100]}{'...' if len(msg.content) > 100 else ''}")

    ## Trigger the bot with Fuckbot or Friendbot (case-sensitive)
    triggers_found = [trigger for trigger in BOT_TRIGGERS if trigger in message.content]
    if triggers_found:
        logger.info(f"Bot trigger detected: {triggers_found} in message from {message.author}")
        try:
            logger.info(f"Processing message for {message.author}")
            response = await process_message(message)
            logger.info(f"Generated response (length: {len(response)}): {response[:100]}...")
            await message.reply(response)
            logger.info(f"Successfully replied to message from {message.author}")
            
            # Add bot's response to conversation history
            bot_name = bot.user.display_name if hasattr(bot.user, 'display_name') else bot.user.name
            conversation_history.add_message(
                channel_id=channel_id,
                author=bot_name,
                content=response
            )
            logger.debug(f"Added bot response to conversation history for channel {channel_id}")
        except Exception as e:
            logger.error(f"Error replying to message from {message.author}: {e}", exc_info=True)
            await message.reply(ERROR_REPLY)
    else:
        logger.debug(f"No bot triggers found in message. Triggers: {BOT_TRIGGERS}")

    ## Allows the bot to process commands
    await bot.process_commands(message)

# async def scheduled_message():
#     """
#     """
#     # List of user IDs to send PMs to
#     user_ids = [690043477374795826, 968681678908293160, 968386433389834241, 968697658728415253, 949518034551332885, 968700143195029534]
#     user_id = random.choice(user_ids)  # Pick a random user ID from the list.
#     user = await bot.fetch_user(user_id)

#     # Fetch assistant's message for a user based on custom instructions
#     print('Sending PM to ' + str(user))
#     logger.info('Sending PM to ' + str(user))

#     message = get_openai_chat(" ", str(user)).content
#     print(str(message))
#     logger.info('PM: ' + str(message))

#     # Send the generated message to the selected user
#     await user.send(message)

async def process_message(message: discord.Message) -> str:
    """
    Processes a message and returns an appropriate response based on the user configuration.

    :param message: The message to process.
    :return: A string containing the bot's response.
    """
    logger.info(f"process_message called for user: {message.author} (ID: {message.author.id})")
    clean_content = message.content.replace("Fuckbot", "Friendbot")
    logger.debug(f"Cleaned content: {clean_content}")
    
    try:
        # Get user configuration
        logger.debug(f"Fetching user configuration for {message.author}")
        user_config = UserService.get_user_config_for_author(message.author)
        logger.info(f"User config - Tone: {user_config.tone}, Objective: {user_config.objective}")
        
        audience = f"Tag the user {message.author.mention}"
        sentiment = str(random.randint(1, 10))
        logger.debug(f"Audience: {audience}, Sentiment: {sentiment}")

        # Build system prompt
        logger.debug("Building system prompt")
        system_prompt = build_instructions(
            tone=user_config.tone,
            audience=audience,
            objective=user_config.objective,
            sentiment=sentiment,
            current_user_id=message.author.mention
        )
        logger.info(f"System prompt built (length: {len(system_prompt)} chars)")

        # Get conversation history for this channel
        channel_id = message.channel.id
        history_text = conversation_history.format_history_for_llm(
            channel_id=channel_id,
            bot_name=bot.user.name
        )
        if history_text:
            logger.info(f"Including conversation history for channel {channel_id} ({len(history_text)} chars)")
            logger.info(f"=== CONVERSATION HISTORY ===\n{history_text}\n=== END HISTORY ===")
        else:
            logger.warning(f"No conversation history available for channel {channel_id} - this might be a problem!")

        # Generate response using configured LLM provider
        logger.info(f"Calling LLMService.generate_response with provider: {config.llm_provider}")
        logger.debug(f"Parameters - temperature: {config.openai_temperature}, max_tokens: {config.openai_max_tokens}")
        response = LLMService.generate_response(
            provider_name=config.llm_provider,
            system_prompt=system_prompt,
            user_message=clean_content,
            temperature=config.openai_temperature, # Using OpenAI temperature for now, can be made provider-specific
            max_tokens=config.openai_max_tokens, # Using OpenAI max_tokens for now, can be made provider-specific
            conversation_history=history_text
        )
        logger.info(f"LLMService returned response (length: {len(response)} chars)")
        return response
    
    except TimeoutError as e:
        logger.error(f"Timeout while processing message from {message.author}: {e}", exc_info=True)
        return ERROR_TIMEOUT
    
    except Exception as e:
        error_msg = f"Error processing message from {message.author}: {e}"
        logger.error(error_msg, exc_info=True)
        # Also print to console for immediate visibility
        print(f"ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return ERROR_GENERIC


# Run the client
if __name__ == "__main__":
    try:
        bot.run(config.discord_token)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
