"""Test script for Gemini API connection and model availability."""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from config import load_config

def test_gemini_api():
    """Test Gemini API connection and list available models."""
    print("=" * 60)
    print("Testing Gemini API Connection")
    print("=" * 60)
    
    # Load config
    try:
        config = load_config()
        print(f"[OK] Config loaded")
        print(f"  - LLM Provider: {config.llm_provider}")
        print(f"  - Gemini Model: {config.gemini_model}")
        print(f"  - API Key present: {bool(config.gemini_api_key)}")
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return False
    
    if not config.gemini_api_key:
        print("[ERROR] GEMINI_API_KEY not set in environment")
        return False
    
    # Configure Gemini
    try:
        genai.configure(api_key=config.gemini_api_key)
        print("[OK] Gemini API configured")
    except Exception as e:
        print(f"[ERROR] Failed to configure Gemini: {e}")
        return False
    
    # List available models
    print("\n" + "=" * 60)
    print("Available Models")
    print("=" * 60)
    try:
        models = list(genai.list_models())
        print(f"[OK] Found {len(models)} total models")
        
        # Filter models that support generateContent
        generate_models = [
            m for m in models 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        print(f"\nModels supporting generateContent ({len(generate_models)}):")
        for model in generate_models:
            name = model.name.replace('models/', '')
            print(f"  - {name}")
            if hasattr(model, 'display_name'):
                print(f"    Display Name: {model.display_name}")
        
        # Check if our configured model is available
        configured_model = config.gemini_model
        model_names = [m.name.replace('models/', '') for m in generate_models]
        
        print(f"\n[INFO] Configured model: {configured_model}")
        if configured_model in model_names:
            print(f"[OK] Configured model '{configured_model}' is available!")
        else:
            print(f"[WARNING] Configured model '{configured_model}' NOT found in available models")
            if model_names:
                print(f"[SUGGESTION] Try one of these models instead:")
                for name in model_names[:5]:  # Show first 5
                    print(f"  - {name}")
        
    except Exception as e:
        print(f"[ERROR] Failed to list models: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test generating content with the configured model
    print("\n" + "=" * 60)
    print("Testing Content Generation")
    print("=" * 60)
    
    # Try the configured model first
    test_model = config.gemini_model
    print(f"Testing with model: {test_model}")
    
    try:
        model = genai.GenerativeModel(test_model)
        response = model.generate_content("Say 'Hello, world!' in one sentence.")
        print(f"[OK] Successfully generated content!")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to generate content with '{test_model}': {e}")
        
        # Try alternative models
        if generate_models:
            print(f"\nTrying alternative models...")
            for alt_model in generate_models[:3]:  # Try first 3 alternatives
                try:
                    model_name = alt_model.name.replace('models/', '')
                    print(f"  Trying: {model_name}")
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content("Say 'Hello, world!' in one sentence.")
                    print(f"  [OK] {model_name} works! Response: {response.text}")
                    print(f"\n[SUGGESTION] Update your .env file:")
                    print(f"  GEMINI_MODEL={model_name}")
                    return True
                except Exception as e2:
                    print(f"  [FAILED] {model_name}: {e2}")
        
        return False

if __name__ == "__main__":
    load_dotenv()
    success = test_gemini_api()
    sys.exit(0 if success else 1)

