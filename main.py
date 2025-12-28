import os
import time
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====== ENV VARIABLES ======
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SMSFAST_API_KEY = os.getenv("SMSFAST_API_KEY")

if not BOT_TOKEN or not SMSFAST_API_KEY:
    raise RuntimeError("Missing environment variables")

# ====== FLASK APP ======
app = Flask(__name__)

# ====== TELEGRAM APP ======
application = Application.builder().token(BOT_TOKEN).build()

# ====== COMMANDS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📲 شراء أرقام", callback_data="buy_numbers")],
        [InlineKeyboardButton("💰 الرصيد", callback_data="balance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 مرحبًا بك\nاختر ما تريد:", reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_numbers":
        keyboard = [
            [InlineKeyboardButton("📱 Telegram", callback_data="buy_telegram")],
            [InlineKeyboardButton("📞 WhatsApp", callback_data="buy_whatsapp")],
            [InlineKeyboardButton("⬅️ رجوع",
