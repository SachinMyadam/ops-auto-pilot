import os
from google import genai

def run_bot():
    print("🚀 Starting Bot (New SDK)...")

    # 1. Check for the API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is missing!")
        exit(1)

    print("✅ Found GOOGLE_API_KEY. Connecting to Gemini...")

    # 2. Configure Gemini (New Client Syntax)
    try:
        client = genai.Client(api_key=api_key)
        
        # 3. Generate Content (Using gemini-1.5-flash)
        # We use single quotes inside double quotes to avoid syntax errors
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents="Say 'Hello Hackathon Judges! I am fully operational!'"
        )
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ GEMINI ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    run_bot()
