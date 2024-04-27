from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)

client = OpenAI(api_key=api_key)

def get_graph_stament(chatmsg):
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
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
        Try to extrapolate specific opinions where applicable. If you get the message "cdoggfreshy2k2000#0: I like goats", you might generate:
         g.V('cdoggfreshy2k2000#0').fold().coalesce(unfold(), addV('User').property('id', 'cdoggfreshy2k2000#0').property('partitionKey', 'cdoggfreshy2k2000#0')).as('u')
        .V('goats').fold().coalesce(unfold(), addV('Opinion').property('name', 'goats').property('partitionKey', 'goats')).as('o')
        .addE('likes').from('u').to('o').property('partitionKey', 'cdoggfreshy2k2000#0')
         
        All Gremlin DB queries must have a partition key. Remember to make the partition key the userID that initiated the message (from the front of the user-mesage).
        ONLY OUTPUT GREMLIN QUERY SYNTAX! IF YOU DON'T HAVE VALID QUERY, RETURN 'No Knowledge Found'
        
        The nodes you create will frequently already exist. Use a .fold().coalesce(unfold()) pattern so Gremlin will create the vertex if it doesn't exist.
         
        STOP AND THINK: IS YOUR OUTPUT VALID GREMLIN QUERY SYNTAX? Are all properties wrapped in single quotes? Did you remember to add the partition key?
        
        """},
        {"role": "user", "content": chatmsg}
    ]
    )

    return str(completion.choices[0].message.content)
