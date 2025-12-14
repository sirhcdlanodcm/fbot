"""Quick test to verify the bot can create an assistant with v2 API."""

from functions.create_openai_assistant import get_assistant, reset_assistant_and_thread
import logging

logging.basicConfig(level=logging.INFO)

print("Testing assistant creation with v2 API...")
print("="*60)

# Reset any cached assistant
reset_assistant_and_thread()

try:
    assistant = get_assistant()
    print(f"[SUCCESS] Assistant created with ID: {assistant.id}")
    print("[OK] The bot should work now!")
    print("\nRestart your bot and try sending a message in Discord.")
except Exception as e:
    print(f"[FAILED] Error: {e}")
    import traceback
    traceback.print_exc()

print("="*60)

