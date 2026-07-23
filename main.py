import os
import json
import feedparser
import requests

RSS_URL = "https://www.men.gov.ma/Ar/Pages/rss.aspx"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LAST_FILE = "last.json"

def load_last():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_last(data):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=30,
    )

def main():
    feed = feedparser.parse(RSS_URL)

    if len(feed.entries) == 0:
        return

    latest = feed.entries[0]

    last = load_last()

    if last.get("id") == latest.id:
        return

    text = f"""
📢 <b>{latest.title}</b>

🔗 {latest.link}
"""

    send_message(text)

    save_last({"id": latest.id})

if __name__ == "__main__":
    main()
