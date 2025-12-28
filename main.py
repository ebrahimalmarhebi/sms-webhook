import os
import logging
from flask import Flask, request

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =====================
# الإعدادات
# =====================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = 7181297222  # رقمك فقط

# =====================
# Flask
# =====================
app = Flask(__name__)

# =====================
# Telegram Handlers
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # السماح لك فقط
    if user_id != OWNER_ID:
        await update.message.reply_text("❌ هذا البوت خاص.")
        return

    keyboard = [
        [InlineKeyboardButton("📱 شراء رقم تليجرام", callback_data="buy_tg")],
        [InlineKeyboardButton("📞 شراء رقم واتساب", callback_data="buy_whatsapp")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
    ]

    await update.message.reply_text(
        "مرحبًا 👋\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        await query.edit_message_text("❌ غير مصرح.")
        return

    if query.data == "buy_tg":
        await query.edit_message_text("📱 شراء رقم تليجرام (قريبًا)")
    elif query.data == "buy_whatsapp":
        await query.edit_message_text("📞 شراء رقم واتساب (قريبًا)")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ الإعدادات (قريبًا)")


# =====================
# Webhook endpoint
# =====================
@app.route("/webhook", methods=["POST"])
async def webhook():
    application = app.config["telegram_app"]
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"


# =====================
# Main
# =====================
def main():
    logging.basicConfig(level=logging.INFO)

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))

    app.config["telegram_app"] = application

    # تشغيل Flask
    app.run(host="0.0.0.0", port=10000)


if __name__ == "__main__":
    main()
