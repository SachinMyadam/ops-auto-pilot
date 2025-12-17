import os
from google import genai

def run_bot():
    print("🚀 Starting Bot (New SDK)...")
    
    # 1. Get Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is missing")
        return

    # 2. Configure Client
    try:
        client = genai.Client(api_key=api_key)
        
        # 3. Generate Content
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Say 'Hello Hackathon Judges! The Bot is Online!'"
        )
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_bot()
