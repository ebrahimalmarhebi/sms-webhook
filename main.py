import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== الإعدادات =====
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = 7181297222  # آيديك فقط

# ===== أمر /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ هذا البوت خاص")
        return

    keyboard = [
        [InlineKeyboardButton("✅ زر تجربة", callback_data="test")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 البوت شغال بنجاح\n\nهذا زر تجربة فقط",
        reply_markup=reply_markup
    )

# ===== التشغيل =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
