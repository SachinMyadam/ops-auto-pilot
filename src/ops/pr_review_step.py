import os
import asyncio
from dotenv import load_dotenv
from google import genai

# This imports the Discord logic you already created
from notify_step import send_discord_alert 

load_dotenv()

def run_bot():
    print("🚀 AI Code Reviewer Starting...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    # We need the Discord Token to send alerts
    discord_token = os.getenv("DISCORD_TOKEN")
    
    if not api_key: print("❌ Missing GOOGLE_API_KEY"); exit(1)

    client = genai.Client(api_key=api_key)
    
    # 1. Read the Buggy Code
    try:
        with open("bad_code.py", "r") as f:
            code_content = f.read()
    except FileNotFoundError:
        print("❌ Could not find bad_code.py"); exit(1)

    # 2. Analyze with Gemini
    try:
        # Auto-discovery logic (Keep this because it works!)
        all_models = list(client.models.list())
        chosen_model = [m.name for m in all_models if "gemini" in m.name][0].replace("models/", "")
        
        print(f"🧠 Analyzing with {chosen_model}...")
        response = client.models.generate_content(
            model=chosen_model,
            contents=f"Find bugs in this code and explain briefly: {code_content}"
        )
        
        ai_report = response.text
        print(f"✅ Analysis Complete.")

        # 3. THE MISSING LINK: Send to Discord
        if discord_token:
            print("📨 Sending Alert to Discord...")
            # This calls your other file!
            asyncio.run(send_discord_alert(ai_report)) 
        else:
            print("⚠️ No Discord Token found. Printing locally only.")
            print(ai_report)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_bot()
