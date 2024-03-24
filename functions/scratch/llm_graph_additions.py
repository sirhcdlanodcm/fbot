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
    When users send you messages, you extract knowledge graph vertecies and edges, then you write Gremlin
    console commands to write the vertex and edges to the database.
     
    Your output is always Gremlin console commands with no extra text. 
    Your output will be used to create the database, so it's very important not to add context or any extra words in your response.
     
    """},
    {"role": "user", "content": "Jim likes soda."}
  ]
)

print(str(completion.choices[0].message.content))
