# from aiogremlin import DriverRemoteConnection, Graph
# from gremlin_python.process.anonymous_traversal import traversal
# import os
# import asyncio

# PRIMARY_KEY = os.getenv('PRIMARY_KEY')
# ACCOUNT_NAME = 'leagueknowledgegraph'  # Replace with your Cosmos DB account name

# async def main():
#     endpoint = f'wss://{ACCOUNT_NAME}.gremlin.cosmos.azure.com:443/gremlin'
#     username = "/dbs/graphdb/colls/Persons"  # Replace with your actual db and collection names
#     password = PRIMARY_KEY

#     async with DriverRemoteConnection(endpoint, 'g', username=username, password=password) as conn:
#         g = traversal().withRemote(conn)
#         query = g.addV('person').property('id', '20').property('partitionId', 'testPartition').property('name', 'test aiogremlin')
#         result = await query.toList()

#         if result:
#             print("Vertex Added", result)
#         else:
#             print("Something went wrong")

# asyncio.run(main())
