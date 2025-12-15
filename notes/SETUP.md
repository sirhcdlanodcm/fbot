# Setup Guide

## Environment Variables

The bot requires environment variables to be set. Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your-discord-bot-token
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash
OPENAI_MAX_TOKENS=2000
CONVERSATION_HISTORY_SIZE=10
```

**Optional (if using OpenAI instead):**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o
```

## Getting Your Tokens

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Reset Token" or "Copy" to get your bot token

### Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy the key

### OpenAI API Key (Optional)
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (you won't be able to see it again!)

## Running the Bot

Once your environment variables are set:

```bash
python discord_bot.py
```

Or with Docker:

```bash
docker build -t friendbot .
docker run --env-file .env friendbot
```

## Troubleshooting

If you get an error about missing environment variables:
- Make sure your `.env` file is in the project root directory
- Check that the variable names match exactly (case-sensitive)
- Restart your terminal/IDE after creating/modifying `.env`
