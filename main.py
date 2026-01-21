import threading
import time
import requests
from flask import Flask
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l" # VERPLICHT INVULLEN

app = Flask('')
@app.route('/')
def home(): return "Online"

def start_monitor():
    # TEST BERICHT: Zo zie je meteen of Discord werkt!
    test_webhook = DiscordWebhook(url=WEBHOOK_URL, content="🚀 De bot is succesvol verbonden met Discord!")
    test_webhook.execute()
    
    last_id = None
    headers = {"User-Agent": "Mozilla/5.0"}
    
    while True:
        try:
            # We zoeken specifiek op 'Nike' om snel resultaat te zien
            url = "https://www.vinted.nl/api/v2/catalog/items?search_text=nike&order=newest_first"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                item = r.json()['items'][0]
                if item['id'] != last_id:
                    if last_id is not None:
                        DiscordWebhook(url=WEBHOOK_URL, content=f"Nieuw item: {item['title']}").execute()
                    last_id = item['id']
        except Exception as e:
            print(f"Fout: {e}")
        time.sleep(60)

threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
start_monitor()
