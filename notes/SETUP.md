# Setup Guide

## Environment Variables

The bot requires environment variables to be set. You have two options:

### Option 1: Create a `.env` file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
   Or on Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your actual tokens:
   ```env
   DISCORD_TOKEN=your-actual-discord-bot-token
   OPENAI_API_KEY=your-actual-openai-api-key
   ```

### Option 2: Set System Environment Variables

You can set environment variables in your system instead:

**Windows PowerShell:**
```powershell
$env:DISCORD_TOKEN="your-actual-discord-bot-token"
$env:OPENAI_API_KEY="your-actual-openai-api-key"
```

**Windows Command Prompt:**
```cmd
set DISCORD_TOKEN=your-actual-discord-bot-token
set OPENAI_API_KEY=your-actual-openai-api-key
```

**Linux/Mac:**
```bash
export DISCORD_TOKEN="your-actual-discord-bot-token"
export OPENAI_API_KEY="your-actual-openai-api-key"
```

## Getting Your Tokens

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Reset Token" or "Copy" to get your bot token

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (you won't be able to see it again!)

## Running the Bot

Once your environment variables are set:

```bash
python discord_bot.py
```

## Troubleshooting

If you get an error about missing environment variables:
- Make sure your `.env` file is in the project root directory
- Check that the variable names match exactly (case-sensitive)
- Restart your terminal/IDE after creating/modifying `.env`

