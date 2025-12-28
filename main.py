import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = 7181297222  # Telegram ID حقك

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ هذا البوت خاص.")
        return

    keyboard = [
        [InlineKeyboardButton("📱 شراء رقم", callback_data="buy")],
        [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")]
    ]

    await update.message.reply_text(
        "✅ أهلاً بك، اختر:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.edit_message_text("📱 شراء رقم (قريبًا)")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ الإعدادات (قريبًا)")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
