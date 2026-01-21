import requests
import time
from discord_webhook import DiscordEmbed, DiscordWebhook

# CONFIGURATIE
VINTED_URL = "https://www.vinted.nl/catalog?catalog[]=79&search_by_image_uuid=&page=1&search_id=30516221645&time=1769012825&size_ids[]=207&size_ids[]=208&size_ids[]=209&brand_ids[]=88&status_ids[]=1&status_ids[]=2&price_to=30&currency=EUR&order=newest_first"
WEBHOOK_URL = "https://discord.com/api/webhooks/1463458458996179067/vAfAKHxd45T8rNZjEQ-EEPEi3CVgxCU6JxEEiVYB7v365mvxiWbdOxcMmstsIbXVBw9l"
CHECK_INTERVAL = 60  # Hoeveel seconden tussen elke check

# Headers zijn essentieel om niet direct geblokkeerd te worden
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
}

last_item_id = None

def check_vinted():
    global last_item_id
    print(f"Checking Vinted... {time.strftime('%H:%M:%S')}")
    
    try:
        # We halen de API variant van de pagina op (indien mogelijk) of de HTML
        response = requests.get(VINTED_URL, headers=HEADERS)
        
        # Voor een echte monitor moet je hier de HTML parsen met BeautifulSoup
        # Of gebruik maken van de interne Vinted JSON API als je de juiste cookies hebt.
        
        # Voorbeeld logica:
        # items = response.json()['items']
        # current_item = items[0]
        
        print("Verbinding geslaagd. Nu filteren op nieuwe items...")
        
    except Exception as e:
        print(f"Fout opgetreden: {e}")

if __name__ == "__main__":
    while True:
        check_vinted()
        time.sleep(CHECK_INTERVAL)
