# FriendBot

FriendBot is a Discord bot designed to interact with users in a channel, responding to specific triggers and building a knowledge graph based on the conversations. This project demonstrates the integration of several technologies, including OpenAI's GPT-4, Neo4j, and Azure, making it a powerful tool for capturing and analyzing social interactions in a Discord environment.

## Features

- **Responsive Interaction**: FriendBot responds to specific keywords in user messages, engaging with users directly in the Discord channel. Responses are customized per-user through prompt engineering.
- **Knowledge Graph Construction**: The bot utilizes OpenAI's GPT-4 to extract knowledge graph nodes and relationships from Discord messages, which are then stored in a Neo4j database.
- **Asynchronous Operations**: Leveraging the `AsyncIOScheduler`, FriendBot handles scheduled tasks and real-time message processing efficiently.
- **Data Persistence**: Messages are logged asynchronously to a Cassandra database for long-term storage and analysis.
- **Containerized Deployment**: The bot is containerized using Docker and deployed on Azure App Services for scalability and ease of management.

## Tech Stack

- **Python**: Core programming language used to build the bot.
- **Discord.py**: Python library for interacting with the Discord API.
- **OpenAI GPT-4**: Used to process and analyze messages for knowledge graph creation.
- **Neo4j**: Graph database used to store the knowledge graph.
- **Cassandra**: NoSQL database used for message logging.
- **Docker**: Containerization technology used to package the application.
- **Azure App Services**: Cloud platform used to deploy and manage the bot.
- **APScheduler**: Python library for scheduling jobs asynchronously within the bot.

## How It Works

1. **Message Processing**: The bot listens to all messages in the channel. When a user mentions the bot or specific keywords, the bot processes the message using GPT-4 and determines the appropriate response.
2. **Knowledge Graph Construction**: For non-trigger messages, the bot constructs a Cypher query to represent the knowledge captured in the conversation and stores it in Neo4j.
3. **Asynchronous Logging**: All messages are asynchronously logged to a Cassandra database for future analysis.
4. **Scheduled Tasks**: Using `APScheduler`, the bot can perform regular tasks such as sending reminders or periodic updates.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker
- Azure account
- Discord account and bot token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FriendBot.git
   cd FriendBot
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables by creating a `.env` file with the following keys:
   ```env
   DISCORD_TOKEN=your-discord-bot-token
   OPENAI_API_KEY=your-openai-api-key
   NEO4J_URI=your-neo4j-uri
   NEO4J_USER=your-neo4j-username
   NEO4J_PASSWORD=your-neo4j-password
   PRIMARY_KEY=your-cassandra-primary-key
   ```

### Running the Bot

To run the bot locally:

```bash
python bot.py
```
