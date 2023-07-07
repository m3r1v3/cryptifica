import os

from telegram import InlineKeyboardButton, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("🔔", callback_data="alarm")],
        [InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
    ]
    
    await update.message.reply_text(
        f'Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nWhat can this bot do:\n\n💲 Show the current value of a cryptocurrency\n🔔 Notify at a specified time about the cost of selected cryptocurrencies\n📈 Show cryptocurrency price chart\n📝 Make daily reviews of selected cryptocurrencies\n\nMade by @m3r1v3\n\nSelect option 💬',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()