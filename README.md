# 🤖 Telegram FOR CHEATING IN EXAM WITH MIBAND 6

This guide shows **step by step** how to create a **Telegram bot that is always online (24/7)** using **Webhook + Render**, without polling, without keeping your computer on.

The bot:

* Receives messages via **Telegram Webhook**
* Splits long messages into **≤ 95 characters** (no broken words)
* Sends replies with **5 seconds delay before replying** and **5 seconds between messages**
* Works perfectly for **Mi Band 6 notifications**

---

## ✅ Why Webhook + Render?

* True **24/7 uptime** (no sleeping)
* Official & recommended by Telegram
* Faster and more reliable than `getUpdates`
* Free tier is enough
* No UptimeRobot needed

---

## 📦 Requirements

* Telegram account
* A Telegram Bot Token (from **@BotFather**)
* GitHub account
* Render account (login with GitHub)

---

## 🧩 Project Structure

```
project/
│── main.py
│── requirements.txt
```

---

## 🧠 Bot Logic

* Split text **by words** (never cut a word)
* Max **95 characters per message**
* Delay **5 seconds before first reply**
* Delay **5 seconds between each message**

---

## 📝 Step 1: Create `main.py`

```python
import time
import requests
from flask import Flask, request

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
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
```

⚠️ **IMPORTANT:** Replace `YOUR_TELEGRAM_BOT_TOKEN` with your real token.

---

## 📝 Step 2: Create `requirements.txt`

```
flask
requests
```

---

## 🧭 Step 3: Push to GitHub

1. Create a **new GitHub repository** (Public)
2. Upload:

   * `main.py`
   * `requirements.txt`

---

## 🚀 Step 4: Deploy on Render

1. Go to [https://render.com](https://render.com)
2. Login with GitHub
3. Click **New → Web Service**
4. Select your repository
5. Configure:

```
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

6. Click **Create Web Service**
7. Wait until status becomes **Live**

---

## 🌐 Step 5: Get Your Render URL

Render will give you a URL like:

```
https://your-app-name.onrender.com
```

Test it in a browser. You should see:

```
Bot is alive
```

---

## 🔗 Step 6: Set Telegram Webhook

Open this URL in your browser (replace values):

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-app-name.onrender.com/webhook
```

✅ Correct response:

```json
{"ok": true, "result": true, "description": "Webhook was set"}
```

---

## 🧪 Step 7: Test the Bot

1. Open Telegram
2. Send a long message to your bot
3. Bot will:

   * Wait 5 seconds
   * Reply in chunks ≤ 95 characters
   * Send each message every 5 seconds

---

## 🔍 Debugging

Check **Render → Logs**:

* ✅ `POST /webhook 200` → working
* ❌ `404` → webhook URL is wrong

---

## 🔐 Security Notes

* Never publish your bot token
* Use Render **Environment Variables** for production
* Regenerate token if leaked

---

## 🏁 Final Result

✔ 24/7 online
✔ No polling
✔ No missed messages
✔ Optimized for Mi Band 6
✔ Free hosting

---

## 🙌 Credits #WaitAdamMinutes #Tunip

Created with ❤️ for learning and sharing.

Feel free to fork, improve, and share this project.
