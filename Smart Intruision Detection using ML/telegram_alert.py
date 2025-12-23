import requests

BOT_TOKEN = ""
CHAT_ID = ""

def send_intrusion_alert(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": CHAT_ID, "caption": "🚨 Intrusion Detected!"}
        r = requests.post(url, files=files, data=data)

    print("Telegram Alert Sent:", r.json())

