# FriendBot

FriendBot (Fbot) is a Discord bot designed to interact with users in a channel, responding to specific triggers with personalized responses. The bot uses OpenAI's GPT-4 to generate context-aware, user-specific responses based on custom configurations for each user.

## Features

- **Responsive Interaction**: FriendBot responds to specific keywords ("Fuckbot" or "Friendbot") in user messages, engaging with users directly in the Discord channel.
- **Personalized Responses**: Responses are customized per-user through prompt engineering, with unique tones, objectives, and writing styles for each user.
- **OpenAI Integration**: Uses OpenAI's Assistants API with GPT-4o for intelligent, context-aware responses.
- **Containerized Deployment**: The bot is containerized using Docker for easy deployment.

## Tech Stack

- **Python**: Core programming language used to build the bot.
- **Discord.py**: Python library for interacting with the Discord API (v2.3+).
- **OpenAI GPT-4o**: Used to generate personalized responses via the Assistants API.
- **Docker**: Containerization technology used to package the application.
- **APScheduler**: Python library for scheduling jobs asynchronously within the bot (optional).

## How It Works

1. **Message Processing**: The bot listens to all messages in the channel. When a user mentions "Fuckbot" or "Friendbot", the bot processes the message.
2. **User Configuration**: The bot retrieves user-specific configurations (tone, objectives, writing style) from predefined settings.
3. **Response Generation**: The bot uses OpenAI's Assistants API with custom instructions to generate a personalized response that matches the user's configuration.
4. **Response Delivery**: The bot replies to the triggering message with the generated response.

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
   ```

### Running the Bot

To run the bot locally:

```bash
python discord_bot.py
```

Or using Docker:

```bash
docker build -t friendbot .
docker run --env-file .env friendbot
```
