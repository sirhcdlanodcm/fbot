# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message

load_dotenv()

thread = True
testing = False

dict_objective = {
    "jmdfive#0":"respond in russian 1/3 of the time. Be generally curt, and a little rude. It's his culture. He likes it.",
    "rustymatador#0":"work something really nice about @jmdfive into your response. Remind him frequently about the brevity of life.",
    "josh2madd3n#0": "be really impressed with whatever he said. Praise him and call him your wolf brother in your response.",
    "cdoggfreshy2k2000#0":"work the word bananas into your response, and give him a madden tip.",
    "dicktanning#0":"include a warning about poor financial planning into your response.",
    "seadeadreckoning#0":"work an obscure movie quote into your response. The more obscure, the better. Never say what movie you are referencing."
}

dict_tone = {
    "jmdfive#0":"Snide",
    "rustymatador#0":"Despair",
    "josh2madd3n#0": "Tactical",
    "cdoggfreshy2k2000#0":"Robotic",
    "dicktanning#0":"Seedy",
    "seadeadreckoning#0":"Sarcastic"
}

dict_audience = {
    "jmdfive#0":"Tag the user jmdfive#0",
    "rustymatador#0":"Tag the user rustymatador#0",
    "josh2madd3n#0": "Tag the user josh2madd3n#0",
    "cdoggfreshy2k2000#0":"Tag the user cdoggfreshy2k2000#0",
    "dicktanning#0":"Tag the user dicktanning#0",
    "seadeadreckoning#0":"Tag the user seadeadreckoning#0"
}

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
                custom_instructions = build_instructions(
                    tone = dict_tone[str(message.author)], 
                    audience = dict_audience[str(message.author)], 
                    objective = dict_objective[str(message.author)]
                )

                fbot_response = add_thread_message(chatinput = clean_content, my_instructions = custom_instructions)
            else:
                fbot_response = get_openai_chat(clean_content, str(message.author)).content

            await message.channel.send(fbot_response)

    client.run(os.getenv('bot_private_token'))