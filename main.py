import os
from flask import Flask, request, jsonify
import telebot
import threading

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ===== Telegram Bot =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت شغال الآن!")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"وصلني: {message.text}")

def run_bot():
    bot.infinity_polling(skip_pending=True)

# ===== Flask Webhook =====
@app.route("/", methods=["GET"])
def home():
    return "✅ SMS Webhook شغال"

@app.route("/sms", methods=["POST"])
def sms():
    data = request.json
    bot.send_message(chat_id=message.chat.id, text=str(data))
    return jsonify({"status": "received"})

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=8080)
