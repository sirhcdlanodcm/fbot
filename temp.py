# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.getenv('bot_private_token'))