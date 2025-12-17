import google.generativeai as genai
import json
import os
import urllib.request
import ssl

config = {
    "name": "PRReviewer",
    "type": "event",
    "subscribes": ["github-webhook"],
    "emits": [],
    "flows": ["ops-flow"]
}

async def handler(event, context):
    # 1. Filter: Only run this logic if it is a "Pull Request" event
    data = event.get("data", {})
    
    # Check if this is a PR event (GitHub sends a "pull_request" key)
    if "pull_request" not in data:
        return # Silent exit (Not a PR)

    # Check action (only review when opened or synchronized)
    action = data.get("action")
    if action not in ["opened", "synchronize", "reopened"]:
        return

    print("🤖 GEMINI AGENT: Detected a Pull Request! Reviewing...")

    api_key = os.getenv("GEMINI_API_KEY")
    discord_url = os.getenv("DISCORD_WEBHOOK_URL")

    # Extract PR Details
    pr = data.get("pull_request", {})
    repo = data.get("repository", {})
    
    pr_title = pr.get("title", "No Title")
    pr_body = pr.get("body", "No Description")
    pr_url = pr.get("html_url")
    pr_user = pr.get("user", {}).get("login", "Unknown Dev")
    repo_name = repo.get("full_name", "Unknown Repo")

    # 2. Ask AI to Review the Intent
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash") 

    prompt = f"""
    You are a Senior Tech Lead. A developer just opened this Pull Request.
    Title: {pr_title}
    Description: {pr_body}
    
    1. Summarize what this PR tries to do in 1 simple sentence.
    2. Give a "Risk Score" (Low/Medium/High) based on the description complexity.
    3. Write a short, encouraging observation.
    
    Output JSON: {{ "summary": "...", "risk": "...", "note": "..." }}
    """

    review = {}
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        review = json.loads(text)
        print(f"✅ AI REVIEW COMPLETE: {review}")
    except Exception as e:
        print(f"⚠️ AI Skip: {e}")
        review = {"summary": "Could not analyze PR.", "risk": "Unknown", "note": "Please check manually."}

    # 3. Send "Code Review" Card to Discord
    discord_msg = {
        "content": (
            f"📝 **New Pull Request Opened!**\n"
            f"👤 **Dev:** `{pr_user}`\n"
            f"📂 **Repo:** `{repo_name}`\n"
            f"🔗 **Link:** [View PR]({pr_url})\n"
            f"──────────────────────\n"
            f"🧐 **AI Summary:** {review.get('summary')}\n"
            f"🔥 **Risk Level:** {review.get('risk')}\n"
            f"💡 **Note:** {review.get('note')}"
        )
    }

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            discord_url, 
            data=json.dumps(discord_msg).encode('utf-8'),
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, context=ctx)
        print("✅ Discord Review Sent!")
    except Exception as e:
        print(f"❌ Failed to send: {e}")
