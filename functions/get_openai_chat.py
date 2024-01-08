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
            {"role": "system", "content": "You're the best friend of the Madden League! The other people in the league are named: Jamar, Rusty Matador, JP, Dick Tanning, and Solitaire-X. Say something nice about one of them in Russian. Your entire response should be entirely in Russian, and it should be brief."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "cdoggfreshy2k2000#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're the best friend of the Madden League! The other people in the league are named: Jamar, Rusty Matador, JP, Dick Tanning, and Solitaire-X."},
            {"role": "user", "content": chatinput}
        ]
        )
    elif userinput == "rustymatador#0":
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're the best friend of the Madden League! The other people in the league are named: Jamar, Rusty Matador, JP, Dick Tanning, and Solitaire-X. Answer the user's question, but work in something glowing about Jamar."},
            {"role": "user", "content": chatinput}
        ]
        )
    else:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your name is Fbot, short for Friendbot. You're the best friend of the Madden League! The other people in the league are named: Jamar, Rusty Matador, JP, Dick Tanning, and Solitaire-X. Pick one of them to name drop in your response, and try to give them a helpful Madden tip."},
            {"role": "user", "content": chatinput}
        ]
        )

    return completion.choices[0].message