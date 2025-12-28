import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# =====================
# الإعدادات
# =====================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = 7181297222  # رقمك فقط

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# =====================
# أوامر البوت
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ هذا البوت خاص")
        return

    keyboard = [
        [InlineKeyboardButton("📱 رقم تليجرام", callback_data="telegram")],
        [InlineKeyboardButton("📞 رقم واتساب", callback_data="whatsapp")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
    ]

    await update.message.reply_text(
        "✅ البوت شغال\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"اخترت: {query.data}")

# =====================
# Flask Webhook
# =====================
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# =====================
# تشغيل التطبيق
# =====================
def main():
    global application
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))

    application.run_polling()

if __name__ == "__main__":
    main()
