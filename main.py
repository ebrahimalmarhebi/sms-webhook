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

# ========================
# /start
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # منع أي شخص غيرك
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

# ========================
# Webhook
# ========================
@app.route("/", methods=["POST"])
async def webhook():
    application = Application.builder().token(BOT_TOKEN).build()
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# ========================
# تشغيل Flask
# ========================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=10000)    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "مرحبًا 👋\nاختر من القائمة:",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_tg":
        await query.edit_message_text("📲 شراء رقم Telegram (قريبًا)")
    elif query.data == "buy_wa":
        await query.edit_message_text("📞 شراء رقم WhatsApp (قريبًا)")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ الإعدادات (قريبًا)")

# =====================
# Webhook
# =====================
@app.route("/telegram", methods=["POST"])
async def telegram_webhook():
    data = request.get_json(force=True)
    await application.process_update(Update.de_json(data, application.bot))
    return "ok"

# =====================
# Main
# =====================
logging.basicConfig(level=logging.INFO)

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(buttons))

if __name__ == "__main__":
    application.initialize()
    application.start()
    app.run(host="0.0.0.0", port=10000)
