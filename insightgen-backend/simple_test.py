"""Simple test to verify API key works"""
import google.generativeai as genai

# Your API key
API_KEY = "AIzaSyBtEH131ec-qO8dIaqS6o6M-jJLq4Ns7FA"

genai.configure(api_key=API_KEY)

print("Testing API key...")
print("=" * 60)

# Try the simplest possible model
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, say hi back")
    print("✓ SUCCESS with gemini-pro!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ FAILED with gemini-pro")
    print(f"Error: {e}")
    print()
    
    # Try without 'models/' prefix
    try:
        print("Trying to list models...")
        for m in genai.list_models():
            print(f"  - {m.name}")
    except Exception as e2:
        print(f"Can't list models: {e2}")

print("=" * 60)
