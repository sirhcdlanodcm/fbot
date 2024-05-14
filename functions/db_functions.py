# from dotenv import load_dotenv
# import asyncio
# import os
# import uuid
# import azure.cosmos.documents as documents
# import azure.cosmos.cosmos_client as cosmos_client
# import azure.cosmos.exceptions as exceptions
# # from gremlin_python.driver import GraphRuntimeException
# from azure.cosmos.partition_key import PartitionKey
# from datetime import datetime
# from gremlin_python.driver import client, serializer


# # Load environment variables
# load_dotenv()

# ## Cassandra db
# HOST = os.getenv('HOST')
# CASSANDRA_KEY=os.getenv('CASSANDRA_KEY')
# TESTWTFASDF = os.getenv('TESTWTF')
# # print(f"HOST: {HOST}")
# # print(f"CASSANDRA_KEY: {str(CASSANDRA_KEY)}")

# ## Gremlin graph db
# endpoint = 'https://leagueknowledgegraph.documents.azure.com:443/'
# PRIMARY_KEY=os.getenv('PRIMARY_KEY')


# my_cosmos_client = cosmos_client.CosmosClient(HOST, {'masterKey': CASSANDRA_KEY}, user_agent="fbot_dev", user_agent_overwrite=True)

# def get_container(database_id='fbot', container_id='msg_log'):
#     db = my_cosmos_client.get_database_client(database_id)
#     return db.get_container_client(container_id)

# def save_message(user_id, server_id="madden_league", message_content=None, container_id='msg_log', database_id='fbot'):
#     # Generate a UUID to use as the item_id
#     item_id = str(uuid.uuid4())
#     container = get_container(database_id, container_id)

#     message = {
#         'id': item_id,
#         'partitionKey': user_id,
#         "serverId": server_id,
#         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         'userId': user_id,
#         'content': message_content 
#     }

#     try:
#         container.create_item(body=message)
#         return f'Message saved to DB. ID = {item_id}'
#     except exceptions.CosmosHttpResponseError as e:
#         return f'Failed to save message: {str(e)}'


# async def save_graph_async(graph_query, endpoint, username, password):
#     try:
#         gremlin_client = client.Client(endpoint, 'graphdb',
#                                        username=username,
#                                        password=password,
#                                        message_serializer=serializer.GraphSONSerializersV2d0())
#         result = gremlin_client.submitAsync(str(graph_query), 'graphdb', 'Persons')
#         result.result()
#         print("Data written to Gremlin database successfully!")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         gremlin_client.close()