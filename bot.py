import requests
import json
import os
import time
from dotenv import load_dotenv
import telebot
from datetime import datetime

# Загрузка токена и chat_id из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("❌ BOT_TOKEN или CHAT_ID не определены в .env")

bot = telebot.TeleBot(BOT_TOKEN)

GIFTS_URL = "https://web.telegram.org/k/assets/tgs/Gift{}.json"
MAX_GIFTS = 100
CHECK_INTERVAL = 30  # каждые 30 секунд
NOTIFY_INTERVAL = 600  # каждые 10 минут
TRACK_FILE = "known_gifts.json"

def load_known_gifts():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r") as f:
            return json.load(f)
    return []

def save_known_gifts(gift_list):
    with open(TRACK_FILE, "w") as f:
        json.dump(gift_list, f, indent=2)

def check_new_gifts():
    known_gifts = load_known_gifts()
    new_gifts = []

    for i in range(1, MAX_GIFTS + 1):
        url = GIFTS_URL.format(i)
        response = requests.get(url)
        if response.status_code == 200 and i not in known_gifts:
            new_gifts.append(i)

    if new_gifts:
        message = f"🎁 Появились новые подарки: {', '.join(f'Gift{i}' for i in new_gifts)}"
        for _ in range(10):
            bot.send_message(CHAT_ID, message)
            time.sleep(1)  # задержка между сообщениями
        all_gifts = sorted(set(known_gifts + new_gifts))
        save_known_gifts(all_gifts)
        return True
    return False

def send_status_message():
    now = datetime.now().strftime('%H:%M:%S')
    bot.send_message(CHAT_ID, f"📬 Проверка подарков... ({now})")

if __name__ == "__main__":
    print("🤖 Бот запущен...")
    last_notify_time = time.time()

    while True:
        try:
            new_found = check_new_gifts()

            # каждые 10 минут — обычный статус
            if time.time() - last_notify_time >= NOTIFY_INTERVAL:
                send_status_message()
                last_notify_time = time.time()

        except Exception as e:
            print(f"❌ Ошибка: {e}")
        time.sleep(CHECK_INTERVAL)