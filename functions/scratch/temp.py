from dotenv import load_dotenv
import os
import uuid
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from datetime import datetime

# Get the current timestamp formatted as a string
formatted_timestamp = datetime.now().strftime('%c')

print(formatted_timestamp)

# Load environment variables
load_dotenv()

HOST = os.getenv('HOST')
MASTER_KEY = os.getenv('MASTER_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')
CONTAINER_ID = os.getenv('CONTAINER_ID')
print(f"MASTER_KEY: '{MASTER_KEY}'")

CASSANDRA_PRIMARY_KEY = os.getenv('CASSANDRA_PRIMARY_KEY')
print(f"CASSANDRA_PRIMARY_KEY: '{CASSANDRA_PRIMARY_KEY}'")


def create_items(container):
    print('\nCreating Items\n')

    # Create a SalesOrder object. This object has nested properties and various types including numbers, DateTimes and strings.
    # This can be saved as JSON as is without converting into rows/columns.
    message = get_message()
    container.create_item(body=message)


def get_message():
    # Generate a UUID to use as item_id
    item_id = str(uuid.uuid4())

    print(item_id)

    msg = {'id' : item_id,
            'partitionKey' : '<@968386433389834241>',
            "serverId": "madden_league",
            'timestamp' : datetime.now().strftime('%c'),
            'userId': '<@968386433389834241>'
            }

    return msg


def create_database(database_id, host, master_key):
    client = cosmos_client.CosmosClient(host, {'masterKey': master_key}, user_agent="fbot_dev", user_agent_overwrite=True)
    
    try:
        db = client.create_database(id=database_id)
        print(f'Database with id \'{database_id}\' created')
    except exceptions.CosmosResourceExistsError:
        db = client.get_database_client(database_id)
        print(f'Database with id \'{database_id}\' was found')

    return db

def create_container(container_id, database_id, host, master_key, partition_key='/user_id'):
    try:
        client = cosmos_client.CosmosClient(host, {'masterKey': master_key}, user_agent="fbot_dev", user_agent_overwrite=True)
        db = client.get_database_client(database_id)
    except Exception as e:
        print(f"Error retrieving database: {e}")
        return

    try:
        container = db.create_container(id=container_id, partition_key=PartitionKey(path=partition_key), offer_throughput=500)
        print(f'Container with id \'{container_id}\' created')
    except exceptions.CosmosResourceExistsError:
        container = db.get_container_client(container_id)
        print(f'Container with id \'{container_id}\' was found')

    return container

db = create_database(database_id='fbot', host=HOST, master_key=MASTER_KEY)
create_container(container_id='msg_log', database_id='fbot', host=HOST, master_key=MASTER_KEY, partition_key='/user_id')

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="fbot_dev", user_agent_overwrite=True)
db = client.get_database_client('fbot')
container = db.get_container_client('msg_log')
create_items(container)
