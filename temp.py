# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message

load_dotenv()

thread = False
testing = False

dict_objective = {
    "jmdfive#0"
}
    If the user messaging you is @jmdfive#0, respond in russian 1/3 of the time. Be generally curt, and a little rude. It's his culture. He likes it.
    If the user messaging you is @rustymatador#0, work something really nice about @jmdfive into your response. Remind him frequently about the brevity of life.
    If the user messaging you is @josh2madd3n#0, be really impressed with whatever he said. Praise him and call him your wolf brother in your response.
    If the user messaging you is @cdoggfreshy2k2000#0 work the word bananas into your response, and give him a madden tip.
    If the user messaging you is @dicktanning#0, include a warning about poor financial planning into your response.
    If the user messaging you is @seadeadreckoning#0, work a bob dylan reference into your response. The more obscure, the better. Never say you're referencing anyone. He gets it.

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
        
        if "Fuckbot" in message.content or "Friendbot" in message.content:
            clean_content = message.content.replace("Fuckbot", "Fbot")
            clean_content = str(message.author) + ": " + str(clean_content)
            print(clean_content)

            if thread:
                fbot_response = add_thread_message(chatinput = clean_content, userinput = str(message.author))
            else:
                fbot_response = get_openai_chat(clean_content, str(message.author)).content

            await message.channel.send(fbot_response)

    client.run(os.getenv('bot_private_token'))