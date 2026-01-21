import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask
from threading import Thread

# --- WEB SERVER VOOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Monitor draait!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- VINTED MONITOR CODE ---
# PLAK HIERONDER JE NIEUWE LINK
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l"

# VERVANG DEZE LINK DOOR JE EIGEN VINTED ZOEKOPDRACHT LINK
VINTED_URL = "https://www.vinted.nl/catalog?brand_ids[]=88&search_by_image_uuid=&page=1&search_id=30505928359&time=1768987123&size_ids[]=207&size_ids[]=208&size_ids[]=209&catalog[]=79&status_ids[]=1&status_ids[]=2&currency=EUR&order=newest_first&price_to=20"

def check_vinted():
    print("Monitor is gestart...")
    last_item_id = None
    
    while True:
        try:
            # Fake een browser bezoek om blokkades te voorkomen
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(VINTED_URL, headers=headers)
            
            # Hier komt normaal de logica om het nieuwste item te vinden
            # Dit is een simpel voorbeeld om de verbinding te testen
            print("Scan uitgevoerd op Vinted...")
            
            time.sleep(60) # Wacht 60 seconden tussen scans
        except Exception as e:
            print(f"Foutje: {e}")
            time.sleep(60)

if __name__ == "__main__":
    keep_alive() # Start de webserver om Render wakker te houden
    check_vinted() # Start de monitor
