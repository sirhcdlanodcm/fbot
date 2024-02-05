import requests
from dotenv import load_dotenv
import os


#### THIS ISN'T CURRENTLY WORKING. ####

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

# The API endpoint for retrieving a list of assistants
url = 'https://api.openai.com/v1/assistants'

# Headers including the Authorization with your API key
headers = {
    'Authorization': f'Bearer {api_key}'
}

# Sending the GET request
response = requests.get(url, headers=headers)

# Checking the response and extracting the data
if response.status_code == 200:
    assistants = response.json()
    # Print the list of assistants
    print(assistants)
else:
    print("Failed to retrieve assistants. Status code:", response.status_code)
