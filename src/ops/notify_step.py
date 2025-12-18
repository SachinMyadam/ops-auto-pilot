import discord
import os
import asyncio

async def send_discord_alert(message):
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("⚠️ No DISCORD_TOKEN found. Skipping alert.")
        return

    # 1. Setup minimal permissions (Intents)
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"✅ Discord Bot Connected as: {client.user}")
        
        # 2. Find a channel to send to
        channel = None
        
        # Option A: Use a specific Channel ID if set in env vars
        specific_channel_id = os.getenv("DISCORD_CHANNEL_ID")
        if specific_channel_id:
            channel = client.get_channel(int(specific_channel_id))
        
        # Option B: Auto-discover the first available text channel
        if not channel:
            print("🔍 No specific channel ID found. Searching for first available channel...")
            for guild in client.guilds:
                for c in guild.text_channels:
                    # Check if bot has permission to send messages here
                    if c.permissions_for(guild.me).send_messages:
                        channel = c
                        break
                if channel: break
        
        # 3. Send the Message
        if channel:
            print(f"📨 Sending alert to channel: #{channel.name}")
            
            # Discord has a 2000 char limit, truncate if needed
            safe_message = message[:1900] + "...(truncated)" if len(message) > 1900 else message
            
            try:
                await channel.send(f"🚨 **AI Code Review Alert**\n{safe_message}")
                print("✅ Alert Sent Successfully!")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
        else:
            print("❌ Could not find ANY channel to post in. Check Bot Permissions.")
        
        # 4. Disconnect
        await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f"❌ Discord Connection Error: {e}")
