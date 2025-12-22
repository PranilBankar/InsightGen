# How to Get a Valid Google AI Studio API Key

## Your Current Issue
Your API key `AIzaSyBtEH131ec-qO8dIaqS6o6M-jJLq4Ns7FA` is not working with Gemini models.

## Solution: Get a New API Key from Google AI Studio

### Step 1: Go to Google AI Studio
Open this link in your browser:
**https://aistudio.google.com/app/apikey**

### Step 2: Sign In
- Sign in with your Google account
- If you don't have one, create a Google account first

### Step 3: Create API Key
1. Click on **"Create API Key"** or **"Get API Key"**
2. You'll see options:
   - **Create API key in new project** (recommended for beginners)
   - **Create API key in existing project** (if you have Google Cloud project)
3. Click **"Create API key in new project"**

### Step 4: Copy Your API Key
- A new API key will be generated
- It will look like: `AIzaSy...` (similar format to yours)
- **IMPORTANT**: Copy it immediately and save it somewhere safe
- You won't be able to see it again!

### Step 5: Update Your `.env` File
1. Open: `d:\Users\Pranil\Github Repos\CRT_project-Day1\insightgen-backend\.env`
2. Replace the line:
   ```
   GOOGLE_API_KEY=AIzaSyBtEH131ec-qO8dIaqS6o6M-jJLq4Ns7FA
   ```
   With your new key:
   ```
   GOOGLE_API_KEY=YOUR_NEW_API_KEY_HERE
   ```

### Step 6: Restart the Backend
1. Stop the backend server (Ctrl + C)
2. Start it again:
   ```
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Step 7: Test Again
Go to http://localhost:3000 and try generating a dashboard!

---

## Alternative: Check if Your Current Key Works

Your current API key might be valid but for a different Google service. Let me know if:
1. You got this key from Google AI Studio (https://aistudio.google.com)
2. Or from Google Cloud Console (https://console.cloud.google.com)

If it's from Google Cloud Console, you might need to:
1. Enable the "Generative Language API"
2. Or get a new key from Google AI Studio instead

---

## Quick Test
After getting a new key, run this in your backend terminal:
```bash
python verify_api_key.py
```

This will tell you if the new key works!
