"""Test different Gemini API configurations"""
import google.generativeai as genai
import os

# Load your API key
API_KEY = "AIzaSyBtEH131ec-qO8dIaqS6o6M-jJLq4Ns7FA"

print("=" * 70)
print("Testing Gemini API with your key...")
print("=" * 70)

# Configure API
genai.configure(api_key=API_KEY)

# Test 1: List models
print("\n1. Listing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   ✓ {m.name}")
            
            # Try to use this model
            try:
                model = genai.GenerativeModel(model_name=m.name)
                response = model.generate_content("Say hello")
                print(f"      SUCCESS! Response: {response.text[:50]}")
                print(f"\n✅ WORKING MODEL FOUND: {m.name}")
                break
            except Exception as e:
                print(f"      Failed: {str(e)[:60]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
