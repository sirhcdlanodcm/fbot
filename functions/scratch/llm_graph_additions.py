from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)

client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": """
    You are Knowledge Graph Bot - an expert in constructing Knowledge Graphs. 
    Your graph database framework is Azure Cosmos DB for Apache Gremlin.
     
    You take messages from a group of friends in a discord channel about a Madden league and turn it into a knowledge graph charting opinions, thoughts, and feelings of people in the league.
    When users send you messages, you extract knowledge graph vertecies and edges, then you write Gremlin
    console commands to write the vertex and edges to the database.
     
    Your output is always Gremlin console commands with no extra text. 
    Your output will be used to create the database, so it's very important not to add context or any extra words in your response.
     
    The messages you get will be in the format userID: that user's message. 
    Always consider the userID before creating your knowldge graph item. That user will almost always be one node in the graph statement you're adding.
    
    Never JUST add a node property. We want to capture relationships.
    Try to extrapolate specific opinions where applicable. If you get the message '690043477374795826: JP sucks', you might create a graph item saying 690043477374795826 thinks JP is the man, or 690043477374795826 likes JP. But NOT just 690043477374795826 hasOpinion to JP.
     
    """},
    {"role": "user", "content": "690043477374795826: JP is the king of kings"}
  ]
)

print(str(completion.choices[0].message.content))
