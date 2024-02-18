"""
discord_bot.py

A Discord bot designed to interact with users in a server based on specific user configurations and objectives.
"""

import os
import random
import discord
from dotenv import load_dotenv

from functions.build_assistant_instructions import build_instructions, USER_OBJECTIVES, USER_TONES
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message


# Load environment variables
load_dotenv()

# Bot configuration
TESTING_MODE = False
THREAD_ENABLED = True


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
                              current_user_id=author)

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "Fuckbot" in message.content or "Friendbot" in message.content:
        response = process_message(message)
        await message.channel.send(response)

def process_message(message):
    """
    Processes a message and returns an appropriate response based on the user configuration.

    :param message: The message to process.
    :return: A string containing the bot's response.
    """
    clean_content = message.content.replace("Fuckbot", "Friendbot")
    if THREAD_ENABLED:
        instructions = get_user_configuration(message.author)
        print(instructions)
        return add_thread_message(chatinput=clean_content, my_instructions=instructions)
    else:
        return get_openai_chat(clean_content, str(message.author)).content

# Run the client
if __name__ == "__main__":
    bot_private_token = os.getenv('bot_private_token')
    if bot_private_token:
        client.run(bot_private_token)
    else:
        print("Bot token not found. Please set BOT_PRIVATE_TOKEN in your environment variables.")
