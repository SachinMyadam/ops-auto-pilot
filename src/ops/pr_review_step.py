import os
import google.generativeai as genai

def run_bot():
    # 1. Check for the API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is missing!")
        exit(1)

    print("✅ Found GOOGLE_API_KEY. Initializing Gemini...")

    # 2. Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # 3. Test a simple generation
        response = model.generate_content("Say 'Hello Hackathon Judges!' if you are working.")
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ Failed to connect to Gemini: {e}")
        exit(1)

if __name__ == "__main__":
    run_bot()
