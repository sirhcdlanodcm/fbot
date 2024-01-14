# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
from functions.get_openai_chat import get_openai_chat
from functions.create_openai_assistant import add_thread_message, build_instructions
import random

load_dotenv()

thread = True
testing = False

dict_objective = {
    "jmdfive#0":"respond in russian 1/3 of the time. Be generally curt, and a little rude. It's his culture. He likes it. If he asks a question, respond with a question.",
    "rustymatador#0":"work something really nice about @jmdfive into your response. Remind him frequently about the brevity of life.",
    "josh2madd3n#0": "be really impressed with whatever he said. Praise him and call him your wolf brother in your response.",
    "cdoggfreshy2k2000#0":"Help him win a Superbowl and return to the NFC where he belongs.",
    "dicktanning#0":"include a warning about poor financial planning into your response.",
    "seadeadreckoning#0":"work an obscure movie quote into your response. The more obscure, the better. Never say what movie you are referencing."
}

dict_tone = {
    "jmdfive#0":"Snide",
    "rustymatador#0":"Despair",
    "josh2madd3n#0": "Tactical",
    "cdoggfreshy2k2000#0":"Super Robotic, like a stereotypical 80s robot.",
    "dicktanning#0":"Seedy",
    "seadeadreckoning#0":"Super happy. It's the best day of your life."
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
            # print(str(message.author.id))
            print(str(message.author.mention))
            author = message.author.mention

            dict_audience = {
            "jmdfive#0":f"Tag the user {author}",
            "rustymatador#0":f"Tag the user {author}",
            "josh2madd3n#0": f"Tag the user {author}",
            "cdoggfreshy2k2000#0":f"Tag the user {author}",
            "dicktanning#0":f"Tag the user {author}",
            "seadeadreckoning#0":f"Tag the user as {author}"
             }
        
            clean_content = message.content.replace("Fuckbot", "Fbot")
            clean_content = str(author) + ": " + str(clean_content)

            print(clean_content)

            if thread:
                custom_instructions = build_instructions(
                    tone = dict_tone[str(message.author)], 
                    audience = dict_audience[str(message.author)], 
                    objective = dict_objective[str(message.author)],
                    sentiment = random.randint(1,10)
                )

                fbot_response = add_thread_message(chatinput = clean_content, my_instructions = custom_instructions)
            else:
                fbot_response = get_openai_chat(clean_content, str(message.author)).content

            await message.channel.send(fbot_response)

    client.run(os.getenv('bot_private_token'))