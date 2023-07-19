import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from crypto import get_data
from chart import get_chart


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
    await query.message.delete()
    await query.message.reply_text(
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
    elif query.data == "chart_next":
        await chart_option_next(query)
    elif query.data[:6] == "chart_":
        await show_chart(query)
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
         InlineKeyboardButton("USDT", callback_data="price_tether"),
         InlineKeyboardButton("USDC", callback_data="price_usd-coin")],
        [InlineKeyboardButton("SOL", callback_data="price_solana"),
         InlineKeyboardButton("DAI", callback_data="price_multi-collateral-dai"),
         InlineKeyboardButton("DOGE", callback_data="price_dogecoin"),
         InlineKeyboardButton("MATIC", callback_data="price_polygon")],
        [InlineKeyboardButton("🏠 Home", callback_data="home"),
         InlineKeyboardButton("▶ Next", callback_data="price_next")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def price_option_next(query):
    keyboard = [
        [InlineKeyboardButton("LTC", callback_data="price_litecoin"),
         InlineKeyboardButton("DOT", callback_data="price_polkadot"),
         InlineKeyboardButton("SHIB", callback_data="price_shiba-inu"),
         InlineKeyboardButton("XMR", callback_data="price_monero")],
        [InlineKeyboardButton("XRP", callback_data="price_xrp"),
         InlineKeyboardButton("TRON", callback_data="price_tron"),
         InlineKeyboardButton("BUSD", callback_data="price_binance-usd"),
         InlineKeyboardButton("UNI", callback_data="price_uniswap")],
        [InlineKeyboardButton("◀ Back", callback_data="price"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def show_price(query):
    data = get_data(query.data[6:])
    name, symbol = data['name'], data['symbol']
    price, percent = data['priceUsd'], '{0:.{1}f}'.format(float(data['changePercent24Hr']), 4)

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="price"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"{name} ({symbol}) 💰\n\nAt the current time, the price of "
                                  f"{symbol} is  ${price} 💸\n"
                                  f"Price changed to {percent}% "
                                  f"in 24 hours {'📉' if percent[0] == '-' else '📈'}",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def chart_option(query):
    keyboard = [
        [InlineKeyboardButton("ETH", callback_data="chart_ethereum"),
         InlineKeyboardButton("BTC", callback_data="chart_bitcoin"),
         InlineKeyboardButton("USDT", callback_data="chart_tether"),
         InlineKeyboardButton("USDC", callback_data="chart_usd-coin")],
        [InlineKeyboardButton("SOL", callback_data="chart_solana"),
         InlineKeyboardButton("DAI", callback_data="chart_multi-collateral-dai"),
         InlineKeyboardButton("DOGE", callback_data="chart_dogecoin"),
         InlineKeyboardButton("MATIC", callback_data="chart_polygon")],
        [InlineKeyboardButton("🏠 Home", callback_data="home"),
         InlineKeyboardButton("▶ Next", callback_data="chart_next")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def chart_option_next(query):
    keyboard = [
        [InlineKeyboardButton("LTC", callback_data="chart_litecoin"),
         InlineKeyboardButton("DOT", callback_data="chart_polkadot"),
         InlineKeyboardButton("SHIB", callback_data="chart_shiba-inu"),
         InlineKeyboardButton("XMR", callback_data="chart_monero")],
        [InlineKeyboardButton("XRP", callback_data="chart_xrp"),
         InlineKeyboardButton("TRON", callback_data="chart_tron"),
         InlineKeyboardButton("BUSD", callback_data="chart_binance-usd"),
         InlineKeyboardButton("UNI", callback_data="chart_uniswap")],
        [InlineKeyboardButton("◀ Back", callback_data="chart"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


async def show_chart(query):
    create_images_folder()

    data = get_data(query.data[6:])
    chart = get_chart(query.data[6:])

    name, symbol = data['name'], data['symbol']
    percent = '{0:.{1}f}'.format(float(data['changePercent24Hr']), 4)

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="chart"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_photo(photo=open(f"images/{chart}.webp", "rb"),
                                   caption=f"{name} ({symbol}) {'📉' if percent[0] == '-' else '📈'}",
                                   reply_markup=InlineKeyboardMarkup(keyboard))
    delete_image(chart)


def create_images_folder():
    if not os.path.exists("images"):
        os.makedirs("images")


def delete_image(file_name: str):
    if os.path.isfile(f"images/{file_name}.webp"):
        os.remove(f"images/{file_name}.webp")


async def alarm_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Notify 🔔\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(keyboard))


async def review_option(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Daily review 📝\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2, reply_markup=InlineKeyboardMarkup(keyboard))


async def favorites(query):
    keyboard = [
        [InlineKeyboardButton("🌟 Add", callback_data="add_favorite"),
         InlineKeyboardButton("🗑 Remove", callback_data="remove_favorite"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
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
    await query.message.delete()
    await query.message.reply_text(
        text=f"About Cryptifica ℹ\n\n_This feature is currently under development, please check back soon_ 🐘",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard))


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
