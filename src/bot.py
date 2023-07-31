import os
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from crypto import get_data, get_prices
from chart import get_chart
from database import Favorites


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("💰 Price", callback_data="price"), InlineKeyboardButton("📈 Chart", callback_data="chart"),
         InlineKeyboardButton("📝 Review", callback_data="review")],
        [InlineKeyboardButton("⭐ Favorites", callback_data="favorites"),
         InlineKeyboardButton("🔔 Notify", callback_data="alarm"),
         InlineKeyboardButton("ℹ Info", callback_data="info")],
    ]

    await update.message.reply_text(
        text=f"Welcome to Cryptifica 👋🏻\n<i>Your personal cryptocurrency checker bot</i> 🤖💰\n\nSelect option 💬",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def home(query):
    keyboard = [
        [InlineKeyboardButton("💰 Price", callback_data="price"), InlineKeyboardButton("📈 Chart", callback_data="chart"),
         InlineKeyboardButton("📝 Review", callback_data="review")],
        [InlineKeyboardButton("⭐ Favorites", callback_data="favorites"),
         InlineKeyboardButton("🔔 Notify", callback_data="alarm"),
         InlineKeyboardButton("ℹ Info", callback_data="info")],
    ]

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Welcome to Cryptifica 👋🏻\n<i>Your personal cryptocurrency checker bot</i> 🤖💰\n\nSelect option 💬",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "price" or query.data == "chart" or query.data == "favorites_add":
        await select_cryptocurrency(query)
    elif query.data == "price_next" or query.data == "chart_next" or query.data == "favorites_add_next":
        await select_cryptocurrency_next(query)
    elif query.data[:6] == "price_":
        await price(query)
    elif query.data[:6] == "chart_":
        await chart(query)
    elif query.data == "favorites":
        await favorites(query)
    elif query.data[:14] == "favorites_add_":
        await favorites_add(query)
    elif query.data == "favorites_remove":
        await select_favorites_remove(query)
    elif query.data == "favorites_remove_next":
        await select_favorites_remove_next(query)
    elif query.data[:17] == "favorites_remove_":
        await favorites_remove(query)
    elif query.data == "review":
        await review(query)
    elif query.data == "alarm":
        await alarm(query)
    elif query.data == "alarm_on":
        await alarm_time(query)
    elif query.data[:9] == "alarm_on_":
        await alarm_on(query)
    elif query.data == "alarm_off":
        await alarm_off(query)
    elif query.data == "home":
        await home(query)
    elif query.data == "info":
        await info(query)


async def select_cryptocurrency(query):
    option = query.data.split('_')[0]
    keyboard = [
        [InlineKeyboardButton("ETH", callback_data=f"{option}_ethereum"),
         InlineKeyboardButton("BTC", callback_data=f"{option}_bitcoin"),
         InlineKeyboardButton("USDT", callback_data=f"{option}_tether"),
         InlineKeyboardButton("USDC", callback_data=f"{option}_usd-coin")],
        [InlineKeyboardButton("SOL", callback_data=f"{option}_solana"),
         InlineKeyboardButton("DAI", callback_data=f"{option}_multi-collateral-dai"),
         InlineKeyboardButton("DOGE", callback_data=f"{option}_dogecoin"),
         InlineKeyboardButton("MATIC", callback_data=f"{option}_polygon")],
        [InlineKeyboardButton("🏠 Home", callback_data="home"),
         InlineKeyboardButton("▶ Next", callback_data=f"{option}_next")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def select_cryptocurrency_next(query, option):
    option = query.data.split('_')[0]
    keyboard = [
        [InlineKeyboardButton("LTC", callback_data=f"{option}_litecoin"),
         InlineKeyboardButton("DOT", callback_data=f"{option}_polkadot"),
         InlineKeyboardButton("SHIB", callback_data=f"{option}_shiba-inu"),
         InlineKeyboardButton("XMR", callback_data=f"{option}_monero")],
        [InlineKeyboardButton("XRP", callback_data=f"{option}_xrp"),
         InlineKeyboardButton("TRON", callback_data=f"{option}_tron"),
         InlineKeyboardButton("BUSD", callback_data=f"{option}_binance-usd"),
         InlineKeyboardButton("UNI", callback_data=f"{option}_uniswap")],
        [InlineKeyboardButton("◀ Back", callback_data=f"{option}"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def price(query):
    data = get_data(query.data.split("_")[-1])
    name, symbol = data['name'], data['symbol']
    price, percent = data['priceUsd'], '{0:.{1}f}'.format(float(data['changePercent24Hr']), 4)

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="price"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"{name} ({symbol}) 💰\n\nAt the current time, the price of "
                                        f"{symbol} is ${price} 💸\n"
                                        f"Price changed to {percent}% "
                                        f"in 24 hours {'📉' if percent[0] == '-' else '📈'}",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def chart(query):
    create_images_folder()

    data = get_data(query.data.split("_")[-1])

    datas, prices = get_prices(query.data.split("_")[-1])

    chart = get_chart(datas, prices)

    name, symbol = data['name'], data['symbol']

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="chart"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_photo(photo=open(f"images/{chart}.webp", "rb"),
                                    caption=f"{name} ({symbol}) {'📉' if prices[0] > prices[-1] else '📈'}",
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    delete_image(chart)


def create_images_folder():
    if not os.path.exists("images"):
        os.makedirs("images")


def delete_image(file_name: str):
    if os.path.isfile(f"images/{file_name}.webp"):
        os.remove(f"images/{file_name}.webp")


async def favorites(query):
    keyboard = [
        [InlineKeyboardButton("🌟 Add", callback_data="favorites_add"),
         InlineKeyboardButton("🗑 Remove", callback_data="favorites_remove"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Select option 💬",
        reply_markup=InlineKeyboardMarkup(keyboard))


async def favorites_add(query):
    data = get_data(query.data.split("_")[-1])

    favorites = Favorites.get(query.from_user.id).split(",")

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data=f"favorites"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()

    if query.data.split("_")[-1] not in favorites:
        Favorites.add(query.from_user.id, query.data.split("_")[-1])
        await query.message.reply_text(
            text=f"{data['name']} added to favorites 🌟",
            reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.message.reply_text(
            text=f"{data['name']} already in favorites ⭐",
            reply_markup=InlineKeyboardMarkup(keyboard))


def get_favorites_keyboard(favorites):
    keyboard = []
    keyboard_layer = []

    data = get_data()

    for i in range(0, len(favorites[:8])):
        keyboard_layer.append(InlineKeyboardButton(get_favorite_data(data, favorites[i])['symbol'],
                                                   callback_data=f"favorites_remove_{favorites[i]}"))
        if (i + 1) == 4:
            keyboard.append(keyboard_layer)
            keyboard_layer = []
    keyboard.append(keyboard_layer)

    return keyboard


async def select_favorites_remove(query):
    favorites = Favorites.get(query.from_user.id).split(",")[:-1]

    keyboard = get_favorites_keyboard(favorites)[:8]

    if len(favorites) >= 9:
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data="home"),
                         InlineKeyboardButton("▶ Next", callback_data=f"favorites_remove_next")])
    else:
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data="home")])

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def select_favorites_remove_next(query):
    favorites = Favorites.get(query.from_user.id).split(",")[:-1]

    keyboard = get_favorites_keyboard(favorites[8:])
    keyboard.append([InlineKeyboardButton("◀ Back", callback_data=f"favorites_remove"),
                     InlineKeyboardButton("🏠 Home", callback_data="home")])

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text=f"Select cryptocurrency 💬",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def favorites_remove(query):
    data = get_data(query.data.split("_")[-1])

    Favorites.remove(query.from_user.id, query.data.split("_")[-1])

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data=f"favorites"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"{data['name']} removed from favorites 🗑",
        reply_markup=InlineKeyboardMarkup(keyboard))


async def review(query):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    favorites = Favorites.get(query.from_user.id).split(",")[:-1]

    if favorites:
        review = get_favorite_review(get_data(), favorites)
    else:
        review = "You don't have any favorite cryptocurrencies yet. Submit to receive your personalized review 🧾"

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Review 📝\n<i>Prices of your favorite cryptocurrency on the current time 💸</i>\n\n<i>{review}</i>",
        parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


def get_favorite_review(data, favorites):
    reviews = []
    for favorite in favorites:
        d = get_favorite_data(data, favorite)
        reviews.append(
            f" • {d['name']} ({d['symbol']}) — ${d['priceUsd']} ({'{0:.{1}f}'.format(float(d['changePercent24Hr']), 4)}%) {'📉' if d['changePercent24Hr'][0] == '-' else '📈'}")
    return "\n".join(reviews)


def get_favorite_data(data, favorite):
    for d in data:
        if d['id'] == favorite: return d


async def alarm(query):
    keyboard = [
        [InlineKeyboardButton("▶ On", callback_data="alarm_on"),
         InlineKeyboardButton("⏹ Off", callback_data="alarm_off"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Select option 💬",
        reply_markup=InlineKeyboardMarkup(keyboard))


async def alarm_time(query):
    keyboard = [
        [InlineKeyboardButton("🕛 00:00", callback_data="alarm_on_0"),
         InlineKeyboardButton("🕗 8:00", callback_data="alarm_on_8"),
         InlineKeyboardButton("🕛 12:00", callback_data="alarm_on_12"),
         InlineKeyboardButton("🕗 20:00", callback_data="alarm_on_20")],
        [InlineKeyboardButton("◀ Back", callback_data=f"alarm"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Select time ⏰",
        reply_markup=InlineKeyboardMarkup(keyboard))


async def alarm_on(query):
    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data=f"alarm"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]

    enable_alarm(query)

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Alarm is enabled ⏰▶",
        reply_markup=InlineKeyboardMarkup(keyboard))


def enable_alarm(query, hour):
    query.job_queue.run_daily(review, time=datetime.time(hour=int(query.data.split('_')[-1]), minute=0), days=(0, 1, 2, 3, 4, 5, 6), query=query.message.chat_id)


async def alarm_off(query):
    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data=f"alarm"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]

    disable_alarm(query)

    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        text=f"Alarm is disabled ⏰⏹",
        reply_markup=InlineKeyboardMarkup(keyboard))


def disable_alarm(query):
    query.job_queue.get_jobs_by_name(str(query.message.chat_id))[0].schedule_removal()


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
