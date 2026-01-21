import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook, DiscordEmbed

# --- CONFIGURATIE ---
# 1. Plak hier je Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l"

# 2. De Vinted URL die je wilt monitoren (bijv. gefilterd op merk/maat)
# Zorg dat de URL eindigt op &order=newest_first
MONITOR_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30506752509&time=1768988955&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&price_to=20&currency=EUR&order=newest_first"

# --- FLASK SERVER (Voor Render) ---
app = Flask('')

@app.route('/')
def home():
    return "Vinted Monitor is Online!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- VINTED MONITOR LOGICA ---
def start_monitor():
    last_item_id = None
    print("Monitor is opgestart en zoekt naar artikelen...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    while True:
        try:
            # We maken eerst een sessie aan om cookies te accepteren (belangrijk voor Vinted)
            session = requests.Session()
            session.get("https://www.vinted.nl", headers=headers)
            
            response = session.get(MONITOR_URL, headers=headers)
            data = response.json()

            if "items" in data and len(data["items"]) > 0:
                nieuwste_item = data["items"][0]
                item_id = nieuwste_item["id"]

                # Check of dit een nieuw artikel is
                if item_id != last_item_id:
                    if last_item_id is not None:
                        stuur_naar_discord(nieuwste_item)
                    last_item_id = item_id
            
        except Exception as e:
            print(f"Fout tijdens scannen: {e}")
        
        # Wacht 60 seconden voor de volgende check (niet te snel, anders word je verbannen)
        time.sleep(60)

def stuur_naar_discord(item):
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    
    embed = DiscordEmbed(
        title=item.get('title', 'Nieuw artikel!'),
        url=f"https://www.vinted.nl/items/{item['id']}",
        color='03b2f8'
    )
    
    embed.add_embed_field(name="Prijs", value=f"€{item['price']['amount']}")
    embed.add_embed_field(name="Merk", value=item.get('brand_title', 'Onbekend'))
    
    if item.get('photo'):
        embed.set_thumbnail(url=item['photo']['url'])
    
    webhook.add_embed(embed)
    webhook.execute()
    print(f"Melding verstuurd voor item: {item['id']}")

# --- START ALLES ---
if __name__ == "__main__":
    # Start Flask in de achtergrond
    t = threading.Thread(target=run_flask)
    t.start()

    # Start de Vinted monitor
    start_monitor()
