# Testing Your Bot

## Quick Test

1. **Start the bot:**
   ```bash
   python discord_bot.py
   ```

2. **You should see:**
   - `[Bot Name] has connected to Discord!`
   - No errors

3. **In Discord, test it:**
   - Go to a channel where the bot has permission
   - Type: `Friendbot hello!` or `Fuckbot hello!`
   - The bot should reply with a personalized message

## Troubleshooting

### Bot doesn't connect
- Check that the bot token is correct
- Make sure the bot is invited to your server
- Check that the bot has proper permissions

### Bot connects but doesn't respond
- Make sure "MESSAGE CONTENT INTENT" is enabled in Discord Developer Portal
- Check that the bot has "Send Messages" permission in the channel
- Look for errors in the console output

### Import errors
- Run: `pip install -r requirements.txt`
- Make sure you're using the correct Python environment

## Expected Behavior

- Bot responds to "Friendbot" or "Fuckbot" in messages
- Responses are personalized based on the user
- Bot uses emojis and hashtags in responses
- Responses are brief and Discord-appropriate

