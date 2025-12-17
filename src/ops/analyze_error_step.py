import google.generativeai as genai
import json
import os
import urllib.request
import ssl
import datetime
import time

config = {
    "name": "AIAnalyzer",
    "type": "event",
    "subscribes": ["analyze-error"],
    "emits": [],
    "flows": ["ops-flow"]
}

# Lock file to prevent parallel execution (Traffic Control)
LOCK_FILE = "/tmp/motia_ai_lock"

async def handler(event, context):
    print("🤖 GEMINI AGENT: Processing Error Log...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    discord_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not api_key or not discord_url:
        print("❌ ERROR: Missing Keys.")
        return

    # 1. TRAFFIC CONTROL (Locking)
    # If another agent is running, we wait for it to finish or timeout
    if os.path.exists(LOCK_FILE):
        if (time.time() - os.path.getmtime(LOCK_FILE)) < 120: # Wait up to 2 mins
            print("✋ Traffic Jam: Waiting for other agent to finish...")
            time.sleep(10) # Simple wait
        
    # Claim the lock
    with open(LOCK_FILE, 'w') as f: f.write("LOCKED")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash") 

    # --- EXTRACT DATA ---
    data = event.get("data", {})
    repo_name = data.get("repository", {}).get("full_name", "Unknown Project")
    job_url = data.get("workflow_run", {}).get("html_url", data.get("url", "#"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    input_log = data.get("error_log", "No error log provided")

    prompt = f"""
    You are a DevOps expert. Analyze this CI/CD error log.
    Log: {input_log}
    
    Output JSON ONLY: {{ "root_cause": "Short explanation", "action": "Specific fix command or step" }}
    """

    decision = {}

    # --- 2. THE RETRY LOOP (Wait for Real Answer) ---
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"🧠 Connecting to Google AI (Attempt {attempt+1}/{max_retries})...")
            response = model.generate_content(prompt)
            decision_text = response.text.replace('```json', '').replace('```', '').strip()
            decision = json.loads(decision_text)
            print(f"✅ GEMINI SUCCESS: {decision}")
            break # Success! Exit loop.
            
        except Exception as e:
            if "429" in str(e):
                wait_time = 70  # Wait 70 seconds to fully clear quota
                print(f"⏳ Quota Limit Hit. Waiting {wait_time}s for Google to cool down...")
                time.sleep(wait_time)
            else:
                print(f"❌ Real Error: {str(e)}")
                decision = {"root_cause": "AI Error", "action": "Check Server Logs"}
                break

    # Release lock
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

    if not decision: 
        print("❌ Failed to get AI response after retries.")
        return

    # --- 3. SEND REAL ANALYSIS TO DISCORD ---
    print("🚀 Sending to Discord...")
    
    formatted_message = (
        f"🚨 **CI/CD Failure Detected!**\n"
        f"📂 **Project:** `{repo_name}`\n"
        f"⏰ **Time:** `{timestamp}`\n"
        f"🔗 **View Logs:** [Click Here]({job_url})\n"
        f"──────────────────────────────────\n"
        f"🧠 **Root Cause:** {decision.get('root_cause')}\n"
        f"🛠 **Recommended Fix:** {decision.get('action')}"
    )

    message = {"content": formatted_message}
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            discord_url, 
            data=json.dumps(message).encode('utf-8'),
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, context=ctx)
        print("✅ Notification Sent!")
    except Exception as e:
        print(f"❌ Discord Failed: {str(e)}")
