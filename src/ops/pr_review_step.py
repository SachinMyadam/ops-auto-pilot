import os
from google import genai

def run_bot():
    print("🚀 Starting Bot (Auto-Discovery Mode)...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: 
        print("❌ Error: GOOGLE_API_KEY is missing")
        exit(1)

    client = genai.Client(api_key=api_key)
    
    try:
        print("📋 Asking Google for available models...")
        # 1. Get list of all models your key can see
        all_models = list(client.models.list())
        
        # 2. Find any model with "gemini" in the name
        # The API returns names like 'models/gemini-1.5-flash'
        available_gemini = [m.name for m in all_models if "gemini" in m.name]
        
        if not available_gemini:
            print("❌ No Gemini models found! Your key might be for Vertex AI, not AI Studio.")
            print(f"Available models: {[m.name for m in all_models]}")
            exit(1)

        # 3. Pick the first one (e.g., 'models/gemini-1.5-flash-001')
        # We remove the 'models/' prefix because the generate function sometimes prefers the short name
        chosen_model = available_gemini[0].replace("models/", "")
        
        print(f"✅ Found {len(available_gemini)} models. Selecting: {chosen_model}")

        # 4. Run it
        response = client.models.generate_content(
            model=chosen_model,
            contents="Say 'Hello Hackathon Judges! I found a working model!'"
        )
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    run_bot()
