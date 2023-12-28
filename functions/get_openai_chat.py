from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)

client = OpenAI(api_key=api_key)

def get_openai_chat(chatinput = ""):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Your name is Fbot, short for Friendbot. You're the best friend of the Madden League! The other people in the league are named: Jamar, Rusty Matador, JP, Dick Tanning, and Solitaire-X. Pick one of them to name drop in your response, and try to give them a helpful Madden tip."},
        {"role": "user", "content": chatinput}
    ]
    )

    return completion.choices[0].message