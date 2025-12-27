@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ البوت شغال")

@bot.message_handler(func=lambda m: m.text and not m.text.startswith('/'))
def echo(message):
    bot.send_message(message.chat.id, f"وصلت رسالتك: {message.text}")
