# FriendBot

FriendBot (Fbot) is a Discord bot designed to interact with users in a channel, responding to specific triggers with personalized responses. The bot uses Google Gemini to generate context-aware, user-specific responses based on custom configurations for each user.

## Features

- **Responsive Interaction**: FriendBot responds when someone writes "Fuckbot" or "Friendbot", or when they @mention CDogg (league member in `config/league_status.py`). For CDogg mentions, the bot briefly acknowledges he stepped away, then answers the message.
- **Personalized Responses**: Responses are customized per-user through prompt engineering, with unique tones, objectives, and writing styles for each user.
- **LLM Integration**: Uses Google Gemini (configurable to OpenAI) for intelligent, context-aware responses.
- **Conversation History**: Maintains context across messages in each channel for more natural conversations.
- **Containerized Deployment**: The bot is containerized using Docker for easy deployment.

## Tech Stack

- **Python 3.11+**: Core programming language
- **Discord.py**: Python library for interacting with the Discord API (v2.3+)
- **Google Gemini API**: Default LLM provider for generating responses
- **OpenAI API**: Optional alternative LLM provider
- **Docker**: Containerization for deployment

## How It Works

1. **Message Processing**: The bot listens to all messages in the channel. It responds when a user says "Fuckbot" or "Friendbot", or @mentions CDogg (same LLM path; CDogg mentions add brief "cover" instructions in the system prompt).
2. **User Configuration**: The bot retrieves user-specific configurations (tone, objectives, writing style) from predefined settings in `config/users.py`.
3. **Conversation History**: The bot maintains a rolling history of recent messages in each channel for context.
4. **Response Generation**: The bot uses the configured LLM (Gemini by default) with custom instructions to generate a personalized response.
5. **Response Delivery**: The bot replies to the triggering message with the generated response.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Discord bot token
- Google Gemini API key (or OpenAI API key if using OpenAI)

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd fbot
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file:
   ```bash
   cp .env.example .env
   # Then edit .env and add your actual tokens
   ```
   
   Or create `.env` manually with:
   ```env
   DISCORD_TOKEN=your-discord-bot-token
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-2.5-flash
   OPENAI_MAX_TOKENS=2000
   CONVERSATION_HISTORY_SIZE=10
   OBJECTIVE_INJECTION_PROBABILITY=0.4
   REACTION_PROBABILITY=0.1
   ```

   **Optional (if using OpenAI instead):**
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4o
   ```

### Running tests (pytest)

Unit tests live under `tests/`. From the repo root:

```bash
pip install -r requirements.txt
pytest
```

Ad hoc scripts that hit real APIs remain under `scripts/` (for example `python scripts/test_message_processing.py`).

### Running the Bot

**Locally:**
```bash
python discord_bot.py
```

**Using Docker:**
```bash
docker build -t friendbot .
docker run --env-file .env friendbot
```

## Configuration

### User-Specific Settings

User configurations are defined in `config/users.py`. Each user can have:
- **Tone**: Writing style and personality
- **Audience**: How to address the user
- **Objective**: What the bot should focus on

### LLM Provider

The bot supports multiple LLM providers:
- **Google Gemini** (default): Set `LLM_PROVIDER=gemini`
- **OpenAI**: Set `LLM_PROVIDER=openai`

Switch providers by changing the `LLM_PROVIDER` environment variable.

### Per-user objective frequency

`OBJECTIVE_INJECTION_PROBABILITY` (default `0.4`) is the chance each request includes that user’s `USER_OBJECTIVES` line in the system prompt. Use `1.0` for the old “always include” behavior, or `0.0` to never inject persona objectives.

### Random reactions

`REACTION_PROBABILITY` (default `0.1`) is the chance the bot adds a random Unicode emoji reaction to each human message. Set to `0` to disable. The bot needs **Add Reactions** permission in the channel.

## Project Structure

```
fbot/
├── bot/                    # Bot services and providers
│   └── services/
│       ├── llm_service.py  # LLM provider factory
│       ├── providers/      # LLM provider implementations
│       └── conversation_history.py
├── config/                 # Configuration
│   ├── config.py          # Main bot configuration
│   └── users.py           # User-specific settings
├── tests/                  # Pytest unit tests
├── constants.py            # Bot constants and triggers
├── discord_bot.py         # Main bot file
└── requirements.txt       # Python dependencies
```

## Deployment

The bot is designed to run in Docker containers. For deployment instructions, see your cloud provider's documentation.

**Important:** Never commit your `.env` file. The `.dockerignore` file ensures it's not included in Docker builds.

## License

[Your License Here]
