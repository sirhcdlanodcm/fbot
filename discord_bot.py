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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

# Load environment variables
load_dotenv()

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
# @client.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # print(f'We have logged in as {client.user}')
    scheduler.add_job(scheduled_message, 'interval', hours=19)
    scheduler.start()

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author == bot.user:
        return

    if "Fuckbot" in message.content or "Friendbot" in message.content:
        response = await process_message(message)  # Ensure response is awaited
        await message.reply(response)

    #Allows the bot to process commands
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

    message = get_openai_chat(" ", str(user)).content
    print(str(message))

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
        response = add_thread_message(chatinput=clean_content, my_instructions=instructions)
    else:
        response = get_openai_chat(clean_content, str(message.author))
        response = response.content  # Adjust based on actual return value structure
    return response


# Run the client
if __name__ == "__main__":
    bot_private_token = os.getenv('bot_private_token')
    if bot_private_token:
        bot.run(bot_private_token)
        # client.run(bot_private_token)
    else:
        print("Bot token not found. Please set BOT_PRIVATE_TOKEN in your environment variables.")
