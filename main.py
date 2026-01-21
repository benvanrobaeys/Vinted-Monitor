import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook, DiscordEmbed

# ================= CONFIGURATIE =================
# 1. Plak hier je Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l" 

# 2. De Vinted API URL (zoekt op alle nieuwste artikelen in NL)
# Tip: Verander 'search_text' in de URL om op iets specifieks te zoeken
MONITOR_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30506752509&time=1768988955&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&price_to=20&currency=EUR&order=newest_first"

# 3. Hoe vaak moet de bot checken? (60 seconden is veilig voor Render)
DELAY = 60 
# ================================================

app = Flask('')

@app.route('/')
def home():
    return "Vinted Monitor is online en draait!"

def run_flask():
    # Render vereist dat er een poort open staat
    app.run(host='0.0.0.0', port=8080)

def stuur_naar_discord(item):
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        
        # Maak een mooie layout voor het bericht
        title = item.get('title', 'Geen titel')
        price = item.get('price', {}).get('amount', '??')
        currency = item.get('price', {}).get('currency', 'EUR')
        item_id = item.get('id')
        item_url = f"https://www.vinted.nl/items/{item_id}"
        
        embed = DiscordEmbed(
            title=title,
            description=f"💰 **Prijs:** {price} {currency}\n🏷️ **Merk:** {item.get('brand_title', 'Onbekend')}",
            url=item_url,
            color='03b2f8'
        )
        
        # Voeg foto toe als die er is
        if item.get('photo'):
            embed.set_thumbnail(url=item['photo'].get('url'))
        
        webhook.add_embed(embed)
        webhook.execute()
        print(f"✅ Melding verstuurd: {title}")
    except Exception as e:
        print(f"❌ Fout bij versturen naar Discord: {e}")

def start_monitor():
    last_item_id = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    print("🚀 Vinted monitor is gestart...")

    while True:
        try:
            # Sessie gebruiken om cookies van Vinted te krijgen
            session = requests.Session()
            session.get("https://www.vinted.nl", headers=headers)
            
            response = session.get(MONITOR_URL, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])

                if items:
                    nieuwste_item = items[0]
                    item_id = nieuwste_item["id"]

                    # Check of dit item anders is dan de vorige keer
                    if item_id != last_item_id:
                        if last_item_id is not None:
                            stuur_naar_discord(nieuwste_item)
                        last_item_id = item_id
            elif response.status_code == 429:
                print("⚠️ Vinted blokkeert ons even (Rate Limit). We wachten langer...")
                time.sleep(120)
            else:
                print(f"⚠️ Vinted gaf een foutmelding: {response.status_code}")

        except Exception as e:
            print(f"❌ Er ging iets mis bij het scannen: {e}")
        
        time.sleep(DELAY)

if __name__ == "__main__":
    # Start de Flask server (voor Render) in een aparte thread
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Start de monitor in de hoofdthread
    start_monitor()
