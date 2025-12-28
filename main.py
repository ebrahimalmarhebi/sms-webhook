import os
import logging
from flask import Flask, request

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# ========================
# الإعدادات
# ========================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = 7181297222  # Telegram ID حقك فقط

# ========================
# Flask
# ========================
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# ========================
# /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != OWNER_ID:
        await update.message.reply_text("✅ البوت شغال")
        return

    keyboard = [
        [InlineKeyboardButton("📱 شراء رقم تليجرام", callback_data="buy_tg")],
        [InlineKeyboardButton("📞 شراء رقم واتساب", callback_data="buy_whatsapp")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 أهلاً بك\nاختر من القائمة:",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# ========================
# Webhook
# ========================
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# ========================
# تشغيل السيرفر
# ========================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=10000)
