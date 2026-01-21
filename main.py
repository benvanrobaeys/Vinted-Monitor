import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook, DiscordEmbed

# ================= CONFIGURATIE =================
# Zorg dat je hier weer je eigen Discord link plakt!
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l" 

# De API URL gebaseerd op jouw Ralph Lauren filters:
# Sorteren op: Nieuwste eerst, Merk: Ralph Lauren, Maten: S, M, L
MONITOR_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30506752509&time=1768992083&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&currency=EUR&order=newest_first"
# ================================================

app = Flask('')

@app.route('/')
def home():
    return "Ralph Lauren Monitor is LIVE!"

def stuur_naar_discord(item):
    try:
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        
        embed = DiscordEmbed(
            title=item.get('title', 'Nieuwe Ralph Lauren Vondst!'),
            url=f"https://www.vinted.nl/items/{item['id']}",
            color='001C44' # Ralph Lauren blauw
        )
        
        prijs = item.get('price', {}).get('amount', '??')
        
        embed.add_embed_field(name="💰 Prijs", value=f"€{prijs}")
        embed.add_embed_field(name="📏 Maat", value=item.get('size_title', 'S / M / L'))
        embed.add_embed_field(name="✨ Staat", value=item.get('status', 'Heel goed'))
        
        if item.get('photo'):
            embed.set_image(url=item['photo'].get('url'))
        
        webhook.add_embed(embed)
        webhook.execute()
        print(f"✅ Melding verstuurd voor item: {item['id']}")
    except Exception as e:
        print(f"❌ Discord fout: {e}")

def start_monitor():
    # Op 0 zetten zodat hij DIRECT stuurt bij de eerste scan
    last_item_id = 0 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    print("🚀 De Ralph Lauren monitor scant nu op jouw filters...")

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

                    if item_id != last_item_id:
                        stuur_naar_discord(nieuwste)
                        last_item_id = item_id
            else:
                print(f"⚠️ Vinted status: {response.status_code}")

        except Exception as e:
            print(f"❌ Fout tijdens scannen: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    # Start webserver voor Render
    t = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    t.daemon = True
    t.start()

    start_monitor()
