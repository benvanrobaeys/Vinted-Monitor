import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook, DiscordEmbed

# ================= CONFIGURATIE =================
# Plak hier je Webhook URL (die werkte al!)
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l" 

# De zoekopdracht (Bijv. Nike)
MONITOR_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30506752509&time=1768988955&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&price_to=20&currency=EUR&order=newest_first"
# ================================================

app = Flask('')

@app.route('/')
def home():
    return "Vinted Monitor is Actief!"

def stuur_naar_discord(item):
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed = DiscordEmbed(
            title=item.get('title', 'Nieuw item'),
            url=f"https://www.vinted.nl/items/{item['id']}",
            color='03b2f8'
        )
        prijs = item.get('price', {}).get('amount', '??')
        embed.add_embed_field(name="💰 Prijs", value=f"€{prijs}")
        embed.add_embed_field(name="🏷️ Merk", value=item.get('brand_title', 'Onbekend'))
        
        if item.get('photo'):
            embed.set_image(url=item['photo'].get('url'))
        
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        print(f"Discord fout: {e}")

def start_monitor():
    # We zetten last_item_id op 0 zodat hij het eerste item dat hij vindt DIRECT stuurt
    last_item_id = 0 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    print("🚀 Scannen gestart...")

    while True:
        try:
            session = requests.Session()
            session.get("https://www.vinted.nl", headers=headers, timeout=10)
            response = session.get(MONITOR_URL, headers=headers, timeout=10)
            
            if response.status_code == 200:
                items = response.json().get("items", [])
                if items:
                    nieuwste = items[0]
                    item_id = nieuwste["id"]

                    # Als het ID anders is dan de vorige scan, stuur bericht
                    if item_id != last_item_id:
                        stuur_naar_discord(nieuwste)
                        last_item_id = item_id
                        print(f"✅ Item gevonden: {item_id}")
            else:
                print(f"⚠️ Vinted status: {response.status_code}")

        except Exception as e:
            print(f"❌ Scan fout: {e}")
        
        time.sleep(60) # Wacht 1 minuut voor de volgende check

if __name__ == "__main__":
    # Start webserver voor Render
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    t.daemon = True
    t.start()

    start_monitor()
