from gremlin_python.driver import client, serializer
from dotenv import load_dotenv
import os

# Your Gremlin endpoint and primary key
endpoint = 'https://leagueknowledgegraph.documents.azure.com:443/'

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(dotenv_path)
load_dotenv(dotenv_path)
PRIMARY_KEY=os.getenv('PRIMARY_KEY')
print(PRIMARY_KEY)


# Create a Gremlin client
gremlin_client = client.Client(endpoint, 'g',
                                username="/dbs/graphdb/colls/persons",
                                password=PRIMARY_KEY,
                                message_serializer=serializer.GraphSONSerializersV2d0())

# Gremlin query to add a vertex
query = "g.addV('person').property('id', '2').property('partitionId', 'myPartitionValue').property('name', 'Jane Doe')"


# Execute the query
callback = gremlin_client.submitAsync(query)

if callback.result() is not None:
    print("Vertex Added")
else:
    print("Something went wrong")

# Always a good practice to close the client connection
gremlin_client.close()
