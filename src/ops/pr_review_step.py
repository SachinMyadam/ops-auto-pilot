import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def run_bot():
    print("🚀 AI Code Reviewer Starting...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: print("❌ Missing API Key"); exit(1)

    client = genai.Client(api_key=api_key)
    
    # 1. Read the code file
    try:
        with open("bad_code.py", "r") as f:
            code_content = f.read()
    except FileNotFoundError:
        print("❌ Could not find bad_code.py")
        exit(1)

    print("📋 Analyzing code for bugs...")

    # 2. Ask Gemini to review it
    prompt = f"""
    You are a Senior Python Engineer. Review this code, find the bugs, 
    and rewrite the corrected version.
    
    CODE:
    {code_content}
    """
    
    try:
        # Auto-discover model again
        all_models = list(client.models.list())
        chosen_model = [m.name for m in all_models if "gemini" in m.name][0].replace("models/", "")
        
        response = client.models.generate_content(
            model=chosen_model,
            contents=prompt
        )
        print("\n" + "="*30)
        print("🤖 AI REVIEW REPORT")
        print("="*30)
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_bot()
