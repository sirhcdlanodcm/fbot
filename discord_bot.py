"""
discord_bot.py

A Discord bot designed to interact with users in a server based on specific user configurations and objectives.
"""

import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from functions.build_assistant_instructions import build_instructions, USER_OBJECTIVES, USER_TONES
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message
# from functions.db_functions import save_message, get_container, save_graph_async
from functions.llm_get_graph_command import get_graph_stament
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers import SchedulerAlreadyRunningError
import nest_asyncio
nest_asyncio.apply()
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

## Gremlin endpoint and primary key
endpoint = 'https://leagueknowledgegraph.documents.azure.com:443/'
PRIMARY_KEY=os.getenv('PRIMARY_KEY')

scheduler = AsyncIOScheduler()

# Bot configuration
TESTING_MODE = False
THREAD_ENABLED = True

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.messages = True
# client = discord.Client(intents=intents)

# So we can trigger commands from the bot (just for testing for now)
bot = commands.Bot(command_prefix='!', intents=intents)

def get_user_configuration(author):
    """
    Retrieves user configuration based on the author of a message.

    :param author: The author of the message.
    :return: A dictionary containing tone, audience, and objective.
    """
    tone = USER_TONES.get(str(author), "Default Tone")
    audience = f"Tag the user {author.mention}"
    objective = USER_OBJECTIVES.get(str(author), "Default Objective")
    sentiment = str(random.randint(1, 10))

    return build_instructions(tone=tone, 
                              audience=audience, 
                              objective=objective, 
                              sentiment=sentiment, 
                              current_user_id=author.mention)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    logger.info(f'{bot.user.name} has connected to Discord!')
    try:
        scheduler.add_job(scheduled_message, 'interval', hours=19)
        scheduler.start()
    except SchedulerAlreadyRunningError:
        pass  # Scheduler is already running, no action needed
@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    logger.info(f"Message from {message.author}: {message.content}")

    ## save msg to cassandra db
    # server_name = message.guild.name if message.guild else "Direct Message"
    # print(save_message(user_id=str(message.author.id), server_id=server_name, message_content=message.content, container_id='msg_log', database_id='fbot'))

    ## No action triggered from bot messages
    if message.author == bot.user: 
        return

    ## Trigger the bot with Fuckbot or Friendbot (case-sensitive)
    elif "Fuckbot" in message.content or "Friendbot" in message.content:
        response = await process_message(message)  # Ensure response is awaited
        await message.reply(response)

    ## if not triggering the bot, build the knowledge graph
    # else:
    #     graph_msg = f"Message from {message.author}: {message.content}"
    #     graph_query = get_graph_stament(graph_msg)
    #     graph_query = graph_query.replace("#", "") # Invalid character in Gremlin, apparently.

    #     print("Graph Query Statement:")
    #     print(graph_query)
    #     if graph_query != 'No Knowledge Found':
    #         # Call save_graph asynchronously with your Gremlin connection details
    #         await save_graph_async(graph_query, endpoint, "/dbs/graphdb/colls/persons", PRIMARY_KEY)

    ##Allows the bot to process commands
    await bot.process_commands(message)

async def scheduled_message():
    """
    """
    # List of user IDs to send PMs to
    user_ids = [690043477374795826, 968681678908293160, 968386433389834241, 968697658728415253, 949518034551332885, 968700143195029534]
    user_id = random.choice(user_ids)  # Pick a random user ID from the list.
    user = await bot.fetch_user(user_id)

    # Fetch assistant's message for a user based on custom instructions
    print('Sending PM to ' + str(user))
    logger.info('Sending PM to ' + str(user))

    message = get_openai_chat(" ", str(user)).content
    print(str(message))
    logger.info('PM: ' + str(message))

    # Send the generated message to the selected user
    await user.send(message)

async def process_message(message):
    """
    Processes a message and returns an appropriate response based on the user configuration.

    :param message: The message to process.
    :return: A string containing the bot's response.
    """
    clean_content = message.content.replace("Fuckbot", "Friendbot")
    if THREAD_ENABLED:
        instructions = get_user_configuration(message.author)
        print(instructions)
        logger.info(f"instructions: {instructions}")
        response = add_thread_message(chatinput=clean_content, my_instructions=instructions)
    else:
        response = get_openai_chat(clean_content, str(message.author))
        response = response.content  
    return response


# Run the client
if __name__ == "__main__":
    bot_private_token = os.getenv('bot_private_token')
    if bot_private_token:
        bot.run(bot_private_token)
        # client.run(bot_private_token)
    else:
        print("Bot token not found. Please set BOT_PRIVATE_TOKEN in your environment variables.")
