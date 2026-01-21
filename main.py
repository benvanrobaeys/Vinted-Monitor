import discord
import os
import requests
from discord.ext import tasks
from bs4 import BeautifulSoup

# Variabelen ophalen
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
VINTED_URL = os.getenv('VINTED_URL')
PROXY_URL = os.getenv('PROXY_URL') # Mag leeg blijven
REFRESH_RATE = int(os.getenv('REFRESH_RATE', 60))

class VintedBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.last_item_id = None

    async def on_ready(self):
        print(f'{self.user.name} is gestart!')
        self.check_vinted.start()

    @tasks.loop(seconds=REFRESH_RATE)
    async def check_vinted(self):
        if not VINTED_URL or not CHANNEL_ID:
            print("Fout: VINTED_URL of CHANNEL_ID niet ingesteld!")
            return

        channel = self.get_channel(int(CHANNEL_ID))
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        
        # Alleen proxy gebruiken als de variabele is ingevuld
        proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None

        try:
            response = requests.get(VINTED_URL, headers=headers, proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                print("Check gelukt: Geen blokkade.")
                # Hier komt straks de BeautifulSoup logica
            else:
                print(f"Blokkade of fout! Code: {response.status_code}")
                
        except Exception as e:
            print(f"Verbindingsfout: {e}")

client = VintedBot()
client.run(TOKEN)
