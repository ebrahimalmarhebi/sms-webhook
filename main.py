import os
import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1) توكن البوت من Render Env
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment variables")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# 2) أوامر البوت (دردشة)
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "✅ البوت شغال")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"وصلت رسالتك: {message.text}")

# 3) Webhook للتيليجرام (لازم يكون مسار مختلف عن /sms)
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.get_json(force=True))
    bot.process_new_updates([update])
    return "OK", 200

# 4) Endpoint للـ SMS (طلبات خارجية)
@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.get_json(silent=True) or {}
    sender = data.get("from", "Unknown")
    msg = data.get("message", "")

    # (اختياري) أرسل الرسالة لك في تليجرام لو حطيت CHAT_ID بالبيئة
    chat_id = os.getenv("CHAT_ID")
    if chat_id:
        bot.send_message(chat_id, f"📩 SMS من {sender}\n{msg}")

    return jsonify({"status": "received", "data": {"from": sender, "message": msg}}), 200

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

# Render uses PORT env
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
