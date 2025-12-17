import json
import os
import urllib.request

config = {
    "name": "DiscordNotifier",
    "type": "event",
    "subscribes": ["gemini-decision"],
    "emits": [],
    "flows": ["ops-flow"]
}

async def handler(event, context):
    print("🔔 DiscordNotifier: Waking up...")
    data = event.get("data", {})
    decision = data.get("decision", {})
    
    message = {
        "content": f"🚨 **Build Failure Detected!**\n\n🧠 **Root Cause:** {decision.get('root_cause', 'Unknown')}\n🛠 **Recommended Fix:** {decision.get('action', 'Investigate')}"
    }

    url = os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        print("⚠️ ERROR: DISCORD_WEBHOOK_URL is missing!")
        return {"status": "missing_url"}

    print(f"🚀 Sending message to Discord...")
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(message).encode('utf-8'),
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            print(f"✅ Notification Sent! Status: {response.status}")
            return {"status": "success"}
    except Exception as e:
        print(f"❌ Sending Failed: {str(e)}")
        return {"status": "error"}
