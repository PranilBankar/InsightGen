"""Verify Google AI Studio API Key"""
import google.generativeai as genai
import sys

API_KEY = "AIzaSyBtEH131ec-qO8dIaqS6o6M-jJLq4Ns7FA"

print("=" * 70)
print("GOOGLE AI STUDIO API KEY VERIFICATION")
print("=" * 70)
print(f"\nAPI Key: {API_KEY[:20]}...{API_KEY[-10:]}")
print()

genai.configure(api_key=API_KEY)

# Test 1: List available models
print("Test 1: Listing available models...")
print("-" * 70)
try:
    models = list(genai.list_models())
    if models:
        print(f"✓ SUCCESS! Found {len(models)} models")
        print("\nAvailable models that support generateContent:")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"  ✓ {m.name}")
    else:
        print("✗ No models found")
except Exception as e:
    print(f"✗ FAILED to list models")
    print(f"Error: {e}")
    print()

# Test 2: Try generating content
print("\n" + "=" * 70)
print("Test 2: Testing content generation...")
print("-" * 70)

test_models = ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash']

for model_name in test_models:
    try:
        print(f"\nTrying {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'API key works!'")
        print(f"✓ SUCCESS!")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"✗ FAILED")
        print(f"Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
