import os
import threading
from flask import Flask
import discord
from discord.ext import tasks
import requests

# --- WEB SERVER VOOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run_webserver():
    # Render stelt zelf de poort in via de environment variabele PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- DISCORD BOT ---
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Ingelogd als {self.user.name}')
        self.vinted_check_task.start()

    @tasks.loop(seconds=60)
    async def vinted_check_task(self):
        print("Checking Vinted...")

if __name__ == "__main__":
    # Start webserver in een aparte thread
    t = threading.Thread(target=run_webserver)
    t.daemon = True
    t.start()
    
    # Start de Discord bot
    if TOKEN:
        client = MyBot()
        client.run(TOKEN)
