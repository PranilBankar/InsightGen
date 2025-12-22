"""Test script to check available Gemini models"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

print("=" * 60)
print("Available Gemini Models:")
print("=" * 60)

try:
    # List all available models
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print()
except Exception as e:
    print(f"Error listing models: {e}")
    print("\nTrying alternative approach...")
    
    # Try common model names
    test_models = [
        'gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'models/gemini-pro',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash',
    ]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello")
            print(f"✓ {model_name} - WORKS!")
        except Exception as e:
            print(f"✗ {model_name} - Failed: {str(e)[:50]}")

print("=" * 60)
