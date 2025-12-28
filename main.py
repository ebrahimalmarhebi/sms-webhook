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
    CallbackQueryHandler,
    ContextTypes
)

# ======================
# الإعدادات
# ======================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # توكن البوت من Render
OWNER_ID = 7181297222  # رقمك أنت فقط (Chat ID)

# ======================
# Flask
# ======================

app = Flask(__name__)

# ======================
# Telegram Bot
# ======================

logging.basicConfig(level=logging.INFO)

application = Application.builder().token(BOT_TOKEN).build()


# ======================
# /start
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # 🔒 البوت خاص
    if user_id != OWNER_ID:
        await update.message.reply_text("🚫 هذا البوت خاص")
        return

    keyboard = [
        [InlineKeyboardButton("📲 شراء رقم Telegram", callback_data="buy_telegram")],
        [InlineKeyboardButton("📞 شراء رقم WhatsApp", callback_data="buy_whatsapp")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 أهلاً بك\nاختر ما تريد:",
        reply_markup=reply_markup
    )


# ======================
# الأزرار
# ======================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        await query.edit_message_text("🚫 هذا البوت خاص")
        return

    if query.data == "buy_telegram":
        await query.edit_message_text(
            "📲 شراء رقم Telegram\n\n"
            "✍️ اكتب رمز الدولة:\n"
            "مثال:\n"
            "+966 أو SA"
        )

    elif query.data == "buy_whatsapp":
        await query.edit_message_text(
            "📞 شراء رقم WhatsApp\n\n"
            "✍️ اكتب رمز الدولة:\n"
            "مثال:\n"
            "+966 أو SA"
        )

    elif query.data == "settings":
        await query.edit_message_text(
            "⚙️ الإعدادات\n\n"
            "لا توجد إعدادات حالياً"
        )


# ======================
# Webhook
# ======================

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


@app.route("/", methods=["GET"])
def index():
    return "Bot is running"


# ======================
# Handlers
# ======================

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(buttons))


# ======================
# Run
# ======================

if __name__ == "__main__":
    application.run_polling()async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_numbers":
        keyboard = [
            [InlineKeyboardButton("📱 Telegram", callback_data="buy_telegram")],
            [InlineKeyboardButton("📞 WhatsApp", callback_data="buy_whatsapp")],
            [InlineKeyboardButton("⬅️ رجوع",
