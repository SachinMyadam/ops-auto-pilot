import os
from google import genai

def run_bot():
    print("🚀 Starting Bot (Gemini 1.5 Flash)...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is missing")
        exit(1)

    try:
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # We try the specific version '-001' first, as it is often more stable in CI/CD
        model_id = "gemini-1.5-flash-001"
        
        print(f"🔄 Connecting to {model_id}...")
        
        response = client.models.generate_content(
            model=model_id,
            contents="Say 'Hello Hackathon Judges! I am running on Gemini 1.5 Flash!'"
        )
        
        print(f"✅ SUCCESS!")
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ Error connecting to Gemini: {e}")
        # Fallback: specific error handling helps debugging
        if "404" in str(e):
            print("💡 Tip: The model name might be slightly different for your API Key tier.")
        exit(1)

if __name__ == "__main__":
    run_bot()
