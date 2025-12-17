import os
import json
import urllib.request

# 1. Manually paste your Discord URL here for the test
url = "PASTE_YOUR_DISCORD_WEBHOOK_URL_HERE"

print(f"Testing URL: {url[:30]}...")

msg = {"content": "🚨 **Test Message**: If you see this, your URL is working!"}
req = urllib.request.Request(
    url, 
    data=json.dumps(msg).encode('utf-8'),
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"✅ Success! Status Code: {resp.status}")
except Exception as e:
    print(f"❌ Failed: {e}")
