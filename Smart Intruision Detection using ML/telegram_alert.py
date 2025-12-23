import requests

BOT_TOKEN = "8387182158:AAFNiqACGTSuHMk3B7aHBsy5sN_T6MDSvxE"
CHAT_ID = "6709507217"

def send_intrusion_alert(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": CHAT_ID, "caption": "🚨 Intrusion Detected!"}
        r = requests.post(url, files=files, data=data)

    print("Telegram Alert Sent:", r.json())

