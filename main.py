import threading
from flask import Flask
# Voeg hier je andere imports toe, zoals:
# from discord_webhook import DiscordWebhook

app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
    # Render gebruikt poort 10000 of een dynamische poort
    app.run(host='0.0.0.0', port=8080)

# Start de Flask server in een aparte "thread" zodat je monitor kan blijven draaien
t = threading.Thread(target=run)
t.start()

# --- HIERONDER KOMT JOUW VINTED MONITOR CODE ---
print("Vinted monitor start nu...")
# Terwijl Flask de poort openhoudt, draait jouw monitor hier verder.
