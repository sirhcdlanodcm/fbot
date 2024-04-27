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
            {"role": "system", "content": "Write this user a love note in the tone of a civil war soldier writing home."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "cdoggfreshy2k2000#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Write this user a love note in the tone of a civil war soldier writing home."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "rustymatador#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Write this user a love note in the tone of a civil war soldier writing home."},
            {"role": "user", "content": chatinput}
        ]
        )
    else:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Write this user a love note in the tone of a civil war soldier writing home."},
            {"role": "user", "content": chatinput}
        ]
        )

    return completion.choices[0].message