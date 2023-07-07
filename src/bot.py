import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("🔔", callback_data="alarm")],
        [InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
    ]
    
    await update.message.reply_text(
        f'Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nSelect option 💬\n\n💲 Show current price\n🔔 Notify about the cost\n📈 Show price chart\n📝 Daily reviews',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "value": value_option(query)
    elif query.data == "alarm": alarm_option(query)
    elif query.data == "chart": chart_option(query)
    elif query.data == "review": review_option(query)
    elif query.data == "back": back(query)

async def value_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"💲 Current price", reply_markup=InlineKeyboardMarkup(keyboard))
    
async def alarm_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"🔔 Notify", reply_markup=InlineKeyboardMarkup(keyboard))

async def chart_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📈 Price chart", reply_markup=InlineKeyboardMarkup(keyboard))

async def review_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📝 Daily review", reply_markup=InlineKeyboardMarkup(keyboard))

async def back(query):
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("🔔", callback_data="alarm")],
        [InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
    ]
    
    await query.answer()
    await query.edit_message_text(
        text=f'Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nSelect option 💬\n\n💲 Show current price\n🔔 Notify about the cost\n📈 Show price chart\n📝 Daily reviews',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()