import time
import requests
from flask import Flask, request

TOKEN = "8464535245:AAF3mUMIrJfo4urD-A36XwENTzO2Qh9jLg8"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)


def split_text_no_cut(text, limit=95):
    words = text.split()
    parts = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= limit:
            current = current + " " + word if current else word
        else:
            parts.append(current)
            current = word

    if current:
        parts.append(current)

    return parts


@app.route("/", methods=["GET"])
def home():
    return "Bot is alive", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        parts = split_text_no_cut(text, 95)

        time.sleep(5)
        for p in parts:
            requests.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": p
            })
            time.sleep(5)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
