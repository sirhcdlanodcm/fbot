from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_openai_chat(chatinput = "", userinput = ""):
    if userinput == "jmdfive#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a vengeful, angry god. Demand the user answer your riddle! Then make up a riddle for the user. Make the riddle unique and weird. You're initiating this conversation, so you can ignore whatever the user sent to you."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "cdoggfreshy2k2000#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a vengeful, angry god. Demand the user answer your riddle! Then make up a riddle for the user. Make the riddle unique and weird. You're initiating this conversation, so you can ignore whatever the user sent to you."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "rustymatador#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a vengeful, angry god. Demand the user answer your riddle! Then make up a riddle for the user. Make the riddle unique and weird. You're initiating this conversation, so you can ignore whatever the user sent to you."},
            {"role": "user", "content": chatinput}
        ]
        )
    else:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a vengeful, angry god. Demand the user answer your riddle! Then make up a riddle for the user."},
            {"role": "user", "content": chatinput}
        ]
        )

    return completion.choices[0].message