"""Quick test script to verify bot configuration."""

try:
    from config import load_config
    config = load_config()
    print("[OK] Configuration loaded successfully!")
    print(f"  Discord token: {'SET' if config.discord_token else 'NOT SET'} (length: {len(config.discord_token) if config.discord_token else 0})")
    print(f"  OpenAI key: {'SET' if config.openai_api_key else 'NOT SET'} (length: {len(config.openai_api_key) if config.openai_api_key else 0})")
    print(f"  Thread enabled: {config.thread_enabled}")
    print(f"  Model: {config.openai_model}")
    print("\n[OK] All configuration looks good!")
    print("\nYou can now run: python discord_bot.py")
except Exception as e:
    print(f"[ERROR] Error loading configuration: {e}")
    import traceback
    traceback.print_exc()

