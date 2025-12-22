"""Quick test for new API key"""
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Reload environment variables
load_dotenv(override=True)

API_KEY = os.getenv('GOOGLE_API_KEY')

print("=" * 60)
print(f"Testing API Key: {API_KEY[:20]}...{API_KEY[-10:]}")
print("=" * 60)

genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('gemini-exp-1206')
    response = model.generate_content("Say 'New API key works!'")
    print("\n✅ SUCCESS!")
    print(f"Response: {response.text}")
    print("\nYour new API key is working perfectly!")
except Exception as e:
    print(f"\n❌ FAILED")
    print(f"Error: {e}")
    print("\nPlease check:")
    print("1. The API key is correctly copied in .env")
    print("2. You've restarted the backend server")

print("=" * 60)
