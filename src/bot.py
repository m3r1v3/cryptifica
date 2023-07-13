import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
        [InlineKeyboardButton("🔔", callback_data="alarm"), InlineKeyboardButton("⭐", callback_data="favorites"), InlineKeyboardButton("ℹ", callback_data="info")],
    ]
    
    await update.message.reply_text(
        f"Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nSelect option 💬\n\n💲 Show current price\n📈 Show price chart\n📝 Daily reviews\n🔔 Notify about the cost\n⭐ Favorite cryptocurrencies\nℹ About Cryptifica",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "value": await value_option(query)
    elif query.data == "alarm": await alarm_option(query)
    elif query.data == "chart": await chart_option(query)
    elif query.data == "review": await review_option(query)
    elif query.data == "home": await home(query)
    elif query.data == "favorites": await favorites(query)
    elif query.data == "info": await info(query)

async def value_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"💲 Current price", reply_markup=InlineKeyboardMarkup(keyboard))
    
async def alarm_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"🔔 Notify", reply_markup=InlineKeyboardMarkup(keyboard))

async def chart_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📈 Price chart", reply_markup=InlineKeyboardMarkup(keyboard))

async def review_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📝 Daily review", reply_markup=InlineKeyboardMarkup(keyboard))

async def home(query):
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
        [InlineKeyboardButton("🔔", callback_data="alarm"), InlineKeyboardButton("⭐", callback_data="favorites"), InlineKeyboardButton("ℹ", callback_data="info")],
    ]
    
    await query.answer()
    await query.edit_message_text(
        text=f"Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nSelect option 💬\n\n💲 Show current price\n📈 Show price chart\n📝 Daily reviews\n🔔 Notify about the cost\n⭐ Favorite cryptocurrencies\nℹ About Cryptifica",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def info(query):
    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"ℹ About Cryptifica", reply_markup=InlineKeyboardMarkup(keyboard))

async def favorites(query):
    keyboard = [
        [InlineKeyboardButton("🌟", callback_data="add_favorite"), InlineKeyboardButton("🗑", callback_data="home"), InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"⭐ Favorite cryptocurrencies\n\nThere you can see/add/remove your favorite cryptocurrencies\n\nYour favorites ⭐\n\n__You haven't added your favorite cryptocurrencies yet__\n\nSelect option 💬\n\n🌟 Add to favorite\n🗑 Remove from favorite\n🏠 Back", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()