import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook, DiscordEmbed

# ================= CONFIGURATIE =================
# BELANGRIJK: Vervang de tekst hieronder door je eigen Discord link!
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l" 

# De link voor Vinted (nieuwste artikelen)
MONITOR_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30506752509&time=1768988955&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&price_to=20&currency=EUR&order=newest_first"
# ================================================

app = Flask('')

@app.route('/')
def home():
    return "Vinted Monitor is online!"

def run_flask():
    # Render heeft een poort nodig om de app levend te houden
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Flask fout: {e}")

def start_monitor():
    last_item_id = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    print("🚀 Monitor wordt gestart...")

    while True:
        try:
            # Sessie starten voor Vinted cookies
            session = requests.Session()
            session.get("https://www.vinted.nl", headers=headers, timeout=10)
            
            response = session.get(MONITOR_URL, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])

                if items:
                    nieuwste_item = items[0]
                    item_id = nieuwste_item["id"]

                    if item_id != last_item_id:
                        if last_item_id is not None:
                            # Stuur naar Discord
                            webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"Nieuw item gevonden: {nieuwste_item.get('title')} - €{nieuwste_item.get('price', {}).get('amount')}")
                            webhook.execute()
                            print(f"✅ Melding verstuurd voor ID: {item_id}")
                        last_item_id = item_id
            else:
                print(f"⚠️ Vinted status: {response.status_code}")

        except Exception as e:
            print(f"❌ Fout bij scannen: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    # Start webserver
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Start scanner
    start_monitor()
