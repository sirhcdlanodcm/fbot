# Migration Guide: Refactoring to Improved Structure

## Overview

This guide shows how to gradually migrate from the current structure to the improved structure.

## Step 1: Use New Configuration System

### Before:
```python
# In discord_bot.py
TESTING_MODE = False
THREAD_ENABLED = True
bot_token = os.getenv('DISCORD_TOKEN')
```

### After:
```python
# In discord_bot.py
from config import load_config

config = load_config()
bot_token = config.discord_token
```

## Step 2: Use User Service

### Before:
```python
# In discord_bot.py
def get_user_key(author):
    # ... lookup logic ...
    
def get_user_configuration(author):
    user_key = get_user_key(author)
    tone = USER_TONES.get(user_key, "Default Tone")
    # ...
```

### After:
```python
# In discord_bot.py
from bot.services.user_service import UserService

def get_user_configuration(author):
    user_config = UserService.get_user_config_for_author(author)
    # Use user_config.tone, user_config.objective
```

## Step 3: Use Constants

### Before:
```python
if "Fuckbot" in message.content or "Friendbot" in message.content:
    return "Sorry, I encountered an error..."
```

### After:
```python
from constants import BOT_TRIGGERS, ERROR_GENERIC

if any(trigger in message.content for trigger in BOT_TRIGGERS):
    return ERROR_GENERIC
```

## Benefits

1. **Centralized Configuration**: All settings in one place
2. **Type Safety**: Dataclasses provide better IDE support
3. **Testability**: Services can be easily mocked
4. **Maintainability**: Clear separation of concerns
5. **Scalability**: Easy to add new features

## Gradual Migration

You don't need to migrate everything at once:

1. Start with configuration (config/)
2. Then extract user service
3. Finally reorganize into bot/ structure

The old code will continue to work alongside the new structure during migration.

