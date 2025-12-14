"""Test script for OpenAI Assistants API v2 without Discord."""

from openai import OpenAI
from openai import APIError, APIConnectionError, APITimeoutError, RateLimitError
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in environment")
    exit(1)

print(f"Using API key: {api_key[:10]}...{api_key[-4:]}")
print("\n" + "="*60)
print("Testing OpenAI Assistants API v2")
print("="*60 + "\n")

# Try different approaches to set the v2 header
print("Attempt 1: Using default_headers in client initialization")
try:
    client1 = OpenAI(
        api_key=api_key,
        default_headers={"OpenAI-Beta": "assistants=v2"}
    )
    assistant1 = client1.beta.assistants.create(
        model="gpt-4o",
        instructions="You are a helpful assistant.",
        name="TestBot"
    )
    print(f"[SUCCESS] Assistant created with ID: {assistant1.id}")
    # Clean up
    client1.beta.assistants.delete(assistant1.id)
    print("[OK] Assistant deleted\n")
except Exception as e:
    print(f"[FAILED] {e}\n")

print("Attempt 2: Using extra_headers parameter")
try:
    client2 = OpenAI(api_key=api_key)
    assistant2 = client2.beta.assistants.create(
        model="gpt-4o",
        instructions="You are a helpful assistant.",
        name="TestBot2",
        extra_headers={"OpenAI-Beta": "assistants=v2"}
    )
    print(f"[SUCCESS] Assistant created with ID: {assistant2.id}")
    # Clean up
    client2.beta.assistants.delete(assistant2.id)
    print("[OK] Assistant deleted\n")
except Exception as e:
    print(f"[FAILED] {e}\n")

print("Attempt 3: Using with_options() method")
try:
    client3 = OpenAI(api_key=api_key)
    assistant3 = client3.beta.assistants.with_options(
        default_headers={"OpenAI-Beta": "assistants=v2"}
    ).create(
        model="gpt-4o",
        instructions="You are a helpful assistant.",
        name="TestBot3"
    )
    print(f"[SUCCESS] Assistant created with ID: {assistant3.id}")
    # Clean up
    client3.beta.assistants.delete(assistant3.id)
    print("[OK] Assistant deleted\n")
except Exception as e:
    print(f"[FAILED] {e}\n")

print("Attempt 4: Full workflow test (create, thread, message, run)")
try:
    client4 = OpenAI(
        api_key=api_key,
        default_headers={"OpenAI-Beta": "assistants=v2"}
    )
    
    # Create assistant
    assistant = client4.beta.assistants.create(
        model="gpt-4o",
        instructions="You are a helpful assistant. Keep responses brief.",
        name="TestBot4"
    )
    print(f"[OK] Assistant created: {assistant.id}")
    
    # Create thread
    thread = client4.beta.threads.create()
    print(f"[OK] Thread created: {thread.id}")
    
    # Add message
    message = client4.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello! Say hi back in one sentence."
    )
    print(f"[OK] Message added")
    
    # Run assistant
    run = client4.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    print(f"[OK] Run started: {run.id}")
    
    # Wait for completion
    timeout = time.time() + 30
    while run.status in ["queued", "in_progress"]:
        if time.time() > timeout:
            raise TimeoutError("Run timed out")
        time.sleep(1)
        run = client4.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"  Run status: {run.status}")
    
    if run.status == "completed":
        messages = client4.beta.threads.messages.list(thread_id=thread.id)
        if messages.data and messages.data[0].content:
            response = messages.data[0].content[0].text.value
            print(f"[SUCCESS] Response: {response}")
        else:
            print("[ERROR] No response content")
    else:
        print(f"[ERROR] Run failed with status: {run.status}")
    
    # Clean up
    client4.beta.assistants.delete(assistant.id)
    print("[OK] Assistant deleted\n")
    
except Exception as e:
    print(f"[FAILED] {e}")
    import traceback
    traceback.print_exc()
    print()

print("="*60)
print("Test complete!")
print("="*60)

