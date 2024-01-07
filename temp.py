# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message

load_dotenv()

thread = True
testing = False

if testing:
    clean_content = "testing no instructions on the run. Please write a haiku about the beach."
    test_user = ["cdoggfreshy2k2000#0", "DeadReckoning#6889"]
    fbot_response = add_thread_message(chatinput = clean_content, userinput = test_user)
    print(fbot_response)
else:
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
        
        if "Fuckbot" in message.content:
            clean_content = message.content.replace("Fuckbot", "Fbot")
            print("message.author = " + str(message.author))

            if thread:
                fbot_response = add_thread_message(chatinput = clean_content, userinput = str(message.author))
            else:
                fbot_response = get_openai_chat(clean_content, str(message.author)).content

            await message.channel.send(fbot_response)

    client.run(os.getenv('bot_private_token'))