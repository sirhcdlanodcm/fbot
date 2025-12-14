"""Test script to simulate Discord message processing without Discord connection."""

import os
import sys
from unittest.mock import Mock, MagicMock
from dotenv import load_dotenv

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.services.conversation_history import ConversationHistory
from bot.services.llm_service import LLMService
from bot.services.user_service import UserService
from functions.build_assistant_instructions import build_instructions
from config import load_config
import random

def create_mock_discord_message(content: str, author_name: str = "TestUser", author_id: int = 123456789):
    """Create a mock Discord message object."""
    message = Mock()
    message.content = content
    message.author = Mock()
    message.author.name = author_name
    message.author.display_name = author_name
    message.author.id = author_id
    message.author.mention = f"<@{author_id}>"
    message.channel = Mock()
    message.channel.id = 999999999  # Test channel ID
    return message

def test_message_processing():
    """Test the full message processing flow."""
    print("=" * 60)
    print("Testing Message Processing (No Discord Required)")
    print("=" * 60)
    
    # Load config
    try:
        config = load_config()
        print(f"[OK] Config loaded - Provider: {config.llm_provider}, Model: {config.gemini_model}")
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return False
    
    # Initialize conversation history
    conversation_history = ConversationHistory(max_history_size=config.conversation_history_size)
    print(f"[OK] Conversation history initialized (max_size={config.conversation_history_size})")
    
    # Simulate a conversation
    print("\n" + "=" * 60)
    print("Simulating Conversation")
    print("=" * 60)
    
    # Message 1
    msg1 = create_mock_discord_message("1", "CDogg", 690043477374795826)
    conversation_history.add_message(
        channel_id=msg1.channel.id,
        author=msg1.author.display_name,
        content=msg1.content
    )
    print(f"[OK] Added message 1: {msg1.author.display_name}: {msg1.content}")
    
    # Message 2
    msg2 = create_mock_discord_message("2", "CDogg", 690043477374795826)
    conversation_history.add_message(
        channel_id=msg2.channel.id,
        author=msg2.author.display_name,
        content=msg2.content
    )
    print(f"[OK] Added message 2: {msg2.author.display_name}: {msg2.content}")
    
    # Message 3
    msg3 = create_mock_discord_message("3", "CDogg", 690043477374795826)
    conversation_history.add_message(
        channel_id=msg3.channel.id,
        author=msg3.author.display_name,
        content=msg3.content
    )
    print(f"[OK] Added message 3: {msg3.author.display_name}: {msg3.content}")
    
    # Message 4
    msg4 = create_mock_discord_message("4", "CDogg", 690043477374795826)
    conversation_history.add_message(
        channel_id=msg4.channel.id,
        author=msg4.author.display_name,
        content=msg4.content
    )
    print(f"[OK] Added message 4: {msg4.author.display_name}: {msg4.content}")
    
    # Bot trigger message (using Fuckbot to test sanitization - should be converted to Friendbot)
    trigger_msg = create_mock_discord_message(
        "Fuckbot, what's the next number in the sequence?",
        "CDogg",
        690043477374795826
    )
    conversation_history.add_message(
        channel_id=trigger_msg.channel.id,
        author=trigger_msg.author.display_name,
        content=trigger_msg.content
    )
    print(f"[OK] Added trigger message: {trigger_msg.author.display_name}: {trigger_msg.content}")
    
    # Show conversation history
    print("\n" + "=" * 60)
    print("Conversation History")
    print("=" * 60)
    history = conversation_history.get_history(trigger_msg.channel.id)
    for i, msg in enumerate(history, 1):
        print(f"  {i}. {msg.author}: {msg.content}")
    
    # Format history for LLM
    history_text = conversation_history.format_history_for_llm(
        channel_id=trigger_msg.channel.id,
        bot_name="FBot"
    )
    print(f"\n[INFO] Formatted history ({len(history_text)} chars):")
    print(history_text)
    
    # Get user configuration
    print("\n" + "=" * 60)
    print("User Configuration")
    print("=" * 60)
    try:
        user_config = UserService.get_user_config_for_author(trigger_msg.author)
        print(f"[OK] User config loaded")
        print(f"  - Tone: {user_config.tone}")
        print(f"  - Objective: {user_config.objective}")
    except Exception as e:
        print(f"[ERROR] Failed to get user config: {e}")
        return False
    
    # Build system prompt
    print("\n" + "=" * 60)
    print("System Prompt")
    print("=" * 60)
    audience = f"Tag the user {trigger_msg.author.mention}"
    sentiment = str(random.randint(1, 10))
    
    system_prompt = build_instructions(
        tone=user_config.tone,
        audience=audience,
        objective=user_config.objective,
        sentiment=sentiment,
        current_user_id=trigger_msg.author.mention
    )
    print(f"[OK] System prompt built ({len(system_prompt)} chars)")
    print(f"  - Audience: {audience}")
    print(f"  - Sentiment: {sentiment}")
    
    # Process message (clean content)
    clean_content = trigger_msg.content.replace("Fuckbot", "Friendbot")
    print(f"\n[INFO] Original content: {trigger_msg.content}")
    print(f"[INFO] Cleaned content: {clean_content}")
    
    # Generate response
    print("\n" + "=" * 60)
    print("Generating LLM Response")
    print("=" * 60)
    try:
        response = LLMService.generate_response(
            provider_name=config.llm_provider,
            system_prompt=system_prompt,
            user_message=clean_content,
            temperature=config.openai_temperature,
            max_tokens=config.openai_max_tokens,
            conversation_history=history_text
        )
        
        print(f"[OK] Response generated ({len(response)} chars)")
        print(f"\n{'=' * 60}")
        print("BOT RESPONSE:")
        print(f"{'=' * 60}")
        # Handle Unicode in Windows console
        try:
            # Try to print directly
            print(response)
        except UnicodeEncodeError:
            # Fallback: write to stdout with UTF-8 encoding
            import sys
            sys.stdout.buffer.write(response.encode('utf-8', errors='replace'))
            sys.stdout.buffer.write(b'\n')
        print(f"{'=' * 60}")
        
        # Check if response looks complete
        if len(response) < 20:
            print(f"\n[WARNING] Response seems very short ({len(response)} chars). May be truncated.")
        else:
            print(f"\n[OK] Response length looks good ({len(response)} chars)")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate response: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    load_dotenv()
    success = test_message_processing()
    sys.exit(0 if success else 1)

