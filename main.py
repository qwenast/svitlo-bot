import requests
import time
import os

BOT_TOKEN = os.getenv("9164500873:AAGTP031v3Q9SaZjlZ459_mnkrEwysew4NQ")
CHAT_ID = os.getenv("397398913")
URL = "https://109-94-209-160.sslip.io/api/state"
CHECK_INTERVAL = 45  # проверять каждые 45 секунд

last_state = None

def get_state():
    try:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
        data = r.json()

        if not data.get("has_data"):
            return "unknown"

        if data.get("offline") and data.get("grid_state") == "off":
            return "off"
        if data.get("offline"):
            return "offline"

        return data.get("grid_state", "unknown")
    except Exception as e:
        print("Ошибка получения данных:", e)
        return None

def send_message(text):
    url = f"https://api.telegram.org/bot{9164500873:AAGTP031v3Q9SaZjlZ459_mnkrEwysew4NQ}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": 397398913,
            "text": text,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception as e:
        print("Ошибка отправки:", e)

print("Бот запущен и следит за светом...")

while True:
    state = get_state()
    
    if state and state != last_state and last_state is not None:
        if state == "on":
            send_message("🟢 <b>Світло з'явилося!</b>")
        elif state == "off":
            send_message("🔴 <b>Світло зникло</b>")
        elif state == "offline":
            send_message("⚠️ <b>Немає зв'язку з інвертором</b>")
    
    if state:
        last_state = state
    
    time.sleep(CHECK_INTERVAL)