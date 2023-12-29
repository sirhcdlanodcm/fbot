# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from functions.get_openai_chat import get_openai_chat

load_dotenv()
# print(os.getenv('bot_private_token'))

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.content.startswith('Hey Fuckbot'):
        clean_content = message.content.replace("Fuckbot", "Fbot")
        print("message.author = " + str(message.author))
            
        fbot_response = get_openai_chat(clean_content, str(message.author)).content

        await message.channel.send(fbot_response)

client.run(os.getenv('bot_private_token'))