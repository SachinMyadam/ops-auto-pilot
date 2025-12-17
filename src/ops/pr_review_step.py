import os
import google.generativeai as genai

def run_bot():
    print("🚀 Starting Bot...")

    # 1. Check for the API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY is missing!")
        exit(1)

    print("✅ Found GOOGLE_API_KEY. Connecting to Gemini...")

    # 2. Configure Gemini
    try:
        genai.configure(api_key=api_key)
        # UPDATED MODEL NAME: gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. Test generation
        response = model.generate_content("Say 'Hello Hackathon Judges! I am alive!'")
        print(f"🤖 Bot Says: {response.text}")
        
    except Exception as e:
        print(f"❌ GEMINI ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    run_bot()
