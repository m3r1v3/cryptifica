import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nWhat can this bot do:\n\n💲 Show the current value of a cryptocurrency\n🔔 Notify at a specified time about the cost of selected cryptocurrencies\n📈 Show cryptocurrency price chart\n📝 Make daily reviews of selected cryptocurrencies\n\nMade by @m3r1v3')

if __name__ == "__main__":
    app = Application.builder().token(os.environ.get('BOT_TOKEN')).build()
    
    app.add_handler(CommandHandler("start", start))

    app.run_polling()