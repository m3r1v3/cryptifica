import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from crypto import get_price, get_symbol


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💰 Price", callback_data="price"), InlineKeyboardButton("📈 Chart", callback_data="chart"),
         InlineKeyboardButton("📝 Review", callback_data="review")],
        [InlineKeyboardButton("🔔 Notify", callback_data="alarm"),
         InlineKeyboardButton("⭐ Favorites", callback_data="favorites"),
         InlineKeyboardButton("ℹ Info", callback_data="info")],
    ]

    await update.message.reply_text(
        text=f"Welcome to Cryptifica 👋🏻\n_Your personal cryptocurrency checker bot_ 🤖💰\n\nSelect option 💬",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def home(query):
    keyboard = [
        [InlineKeyboardButton("💰 Price", callback_data="price"), InlineKeyboardButton("📈 Chart", callback_data="chart"),
         InlineKeyboardButton("📝 Review", callback_data="review")],
        [InlineKeyboardButton("🔔 Notify", callback_data="alarm"),
         InlineKeyboardButton("⭐ Favorites", callback_data="favorites"),
         InlineKeyboardButton("ℹ Info", callback_data="info")],
    ]

    await query.answer()
    await query.edit_message_text(
        text=f"Welcome to Cryptifica 👋🏻\n_Your personal cryptocurrency checker bot_ 🤖💰\n\nSelect option 💬",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "price":
        await price_option(query)
    elif query.data == "price_next":
        await price_option_next(query)
    elif query.data[:6] == "price_":
        await show_price(query)
    elif query.data == "alarm":
        await alarm_option(query)
    elif query.data == "chart":
        await chart_option(query)
    elif query.data == "review":
        await review_option(query)
    elif query.data == "home":
        await home(query)
    elif query.data == "favorites":
        await favorites(query)
    elif query.data == "info":
        await info(query)


async def price_option(query):
    keyboard = [
        [InlineKeyboardButton("ETH", callback_data="price_ethereum"),
         InlineKeyboardButton("BTC", callback_data="price_bitcoin"),
         InlineKeyboardButton("USDT", callback_data="price_tether")],
        [InlineKeyboardButton("USDC", callback_data="price_usd-coin"),
         InlineKeyboardButton("SOL", callback_data="price_solana"),
         InlineKeyboardButton("DAI", callback_data="price_multi-collateral-dai")],
        [InlineKeyboardButton("🏠 Home", callback_data="home"),
         InlineKeyboardButton("▶ Next", callback_data="price_next")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def price_option_next(query):
    keyboard = [
        [InlineKeyboardButton("DOGE", callback_data="price_dogecoin"),
         InlineKeyboardButton("MATIC", callback_data="price_polygon"),
         InlineKeyboardButton("LTC", callback_data="price_litecoin")],
        [InlineKeyboardButton("DOT", callback_data="price_polkadot"),
         InlineKeyboardButton("SHIB", callback_data="price_shiba-inu"),
         InlineKeyboardButton("XMR", callback_data="price_monero")],
        [InlineKeyboardButton("◀ Back", callback_data="price"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def show_price(query):
    price = get_price(query.data[6:])
    name = get_symbol(query.data[6:]).upper()

    keyboard = [
        [InlineKeyboardButton("🏠", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"{name} price 💰\n\nAt the current time, the cost of {name} is ${price}",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def alarm_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(
        text=f"Notify 🔔\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(keyboard))


async def chart_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(
        text=f"📈 Price chart\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(keyboard))


async def review_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(
        text=f"Daily review 📝\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(keyboard))


async def favorites(query):
    keyboard = [
        [InlineKeyboardButton("🌟 Add", callback_data="add_favorite"),
         InlineKeyboardButton("🗑 Remove", callback_data="remove_favorite"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(
        text=f"Your favorite cryptocurrencies ⭐\nThere you can see/add/remove your favorite cryptocurrencies\n\nYour "
             f"favorites ⭐\n\n_You haven't added your favorite cryptocurrencies yet_\n\nSelect option 💬\n\n🌟 Add to "
             f"favorite\n🗑 Remove from favorite\n🏠 Back",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard))


async def info(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.edit_message_text(
        text=f"About Cryptifica ℹ\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard))


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
