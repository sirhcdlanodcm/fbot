from dotenv import load_dotenv
import os
import uuid
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from datetime import datetime

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(dotenv_path)
load_dotenv(dotenv_path)

HOST = os.getenv('HOST')
MASTER_KEY = os.getenv('CASSANDRA_PRIMARY_KEY')

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="fbot_dev", user_agent_overwrite=True)

def get_container(database_id='fbot', container_id='msg_log'):
    db = client.get_database_client(database_id)
    return db.get_container_client(container_id)

def save_message(user_id, server_id="madden_league", message_content=None, container_id='msg_log', database_id='fbot'):
    # Generate a UUID to use as the item_id
    item_id = str(uuid.uuid4())
    container = get_container(database_id, container_id)

    message = {
        'id': item_id,
        'partitionKey': user_id,
        "serverId": server_id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'userId': user_id,
        'content': message_content 
    }

    try:
        container.create_item(body=message)
        return f'Message saved to DB. ID = {item_id}'
    except exceptions.CosmosHttpResponseError as e:
        return f'Failed to save message: {str(e)}'
