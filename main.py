import discord
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot online")
    channel = client.get_channel(CHANNEL_ID)

    while True:
        await channel.send("🧪 Testbericht – bot werkt")
        await asyncio.sleep(60)

client.run(TOKEN)
