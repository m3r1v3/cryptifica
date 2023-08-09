import os
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ConversationHandler, ContextTypes
from telegram.constants import ParseMode

from crypto import get_data, get_prices
from chart import get_chart
from database import Favorites


MENU_KEYBOARD = [
    [InlineKeyboardButton("💰 Price", callback_data="price#0-9"),
     InlineKeyboardButton("📈 Chart", callback_data="chart#0-9"),
     InlineKeyboardButton("📝 Review", callback_data="review"),
     InlineKeyboardButton("🔔 Notify", callback_data="alarm")],
    [InlineKeyboardButton("⭐ Favorites", callback_data="favorites"),
     InlineKeyboardButton("🔍 Search", callback_data="search"),
     InlineKeyboardButton("ℹ Info", callback_data="info")]
]


async def send_message(update: Update, text: str, keyboard: list):
    await update.message.reply_text(text=text,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(keyboard))


async def send_alarm_message(context: ContextTypes.DEFAULT_TYPE, text: str, keyboard: list):
    await context.bot.reply_text(text=text,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(keyboard))


async def reply_message(query, text: str, keyboard: list):
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text,
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def reply_photo(query, path: str, caption: str, keyboard: list):
    await query.answer()
    await query.message.delete()
    await query.message.reply_photo(photo=open(path, "rb"),
                                    caption=caption,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def reply_select_cryptocurrency(query, data: list):
    option = query.data.split('#')[0]
    start, end = query.data.split('#')[-1].split("-")

    keyboard = get_keyboard(data[int(start):int(end)], option)


    if len(data) <= int(end) and not int(start):
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data="home")])
    elif len(data) <= int(end):
        keyboard.append(
            [
                InlineKeyboardButton("◀ Back", callback_data=f"{option}#{int(start)-9}-{int(start)}"),
                InlineKeyboardButton("🏠 Home", callback_data="home"),
            ]
        )
    elif int(start) > 0:
        keyboard.append(
            [
                InlineKeyboardButton("◀ Back", callback_data=f"{option}#{int(start)-9}-{int(start)}"),
                InlineKeyboardButton("🏠 Home", callback_data="home"),
                InlineKeyboardButton("▶ Next", callback_data=f"{option}#{int(end)}-{int(end)+8}"),
            ]
        )
    else:
        keyboard.append([
            InlineKeyboardButton("🏠 Home", callback_data="home"),
            InlineKeyboardButton("▶ Next", callback_data=f"{option}#{int(end)}-{int(end)+8}")])


    await reply_message(
        query=query, text="Select cryptocurrency 💬", keyboard=keyboard
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_message(update=update,
                       text=f"Welcome to <b>Cryptifica</b> 👋🏻\n<i>Your personal cryptocurrency checker bot</i> 🤖💰\n\nSelect option 💬",
                       keyboard=MENU_KEYBOARD)


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_message(query=update.callback_query,
                        text=f"Select option 💬",
                        keyboard=MENU_KEYBOARD)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data.split("#")[0] in ["price", "chart", "favorites-add"]:
        await select_cryptocurrency(update, context)
    elif query.data.split("_")[-1] == "search":
        pass
    elif query.data[:6] == "price_":
        await price(update, context)
    elif query.data[:6] == "chart_":
        await chart(update, context)
    elif query.data == "favorites":
        await favorites(update, context)
    elif query.data[:14] == "favorites-add_":
        await favorites_add(update, context)
    elif query.data.split("#")[0] == "favorites-remove":
        await select_favorites_remove(update, context)
    elif query.data[:17] == "favorites-remove_":
        await favorites_remove(update, context)
    elif query.data == "review":
        await review(update, context)
    elif query.data == "alarm":
        await alarm(update, context)
    elif query.data == "alarm_on":
        await alarm_time(update, context)
    elif query.data[:9] == "alarm_on_":
        await alarm_on(update, context)
    elif query.data == "alarm_off":
        await alarm_off(update, context)
    elif query.data == "home":
        await home(update, context)
    elif query.data == "search":
        pass
    elif query.data == "info":
        await info(update, context)


async def select_cryptocurrency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_select_cryptocurrency(update.callback_query, [cryptocurrency['id'] for cryptocurrency in get_data()])


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = get_data(query.data.split("_")[-1])
    name, symbol = data['name'], data['symbol']
    price, percent = data['priceUsd'], '{0:.{1}f}'.format(float(data['changePercent24Hr']), 4)

    keyboard = [[InlineKeyboardButton("◀ Back", callback_data="price#0-9"), InlineKeyboardButton("🏠 Home", callback_data="home")]]

    await reply_message(query=query,
                        text=f"<b>{name} ({symbol})</b> 💰\n\nPrice of <b>{symbol}</b> is <b>${price}</b> (changed on <b>{percent}%</b> in 24 hrs) 💸{'📉' if percent[0] == '-' else '📈'}\n",
                        keyboard=keyboard)


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    create_images_folder()

    data = get_data(query.data.split("_")[-1])
    datas, prices = get_prices(query.data.split("_")[-1])

    chart = get_chart(datas, prices)

    name, symbol = data['name'], data['symbol']

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="chart#0-9"), InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await reply_photo(query=query, path=f"images/{chart}.webp",
                      caption=f"<b>{name} ({symbol})</b> {'📉' if prices[0] > prices[-1] else '📈'}",
                      keyboard=keyboard)
    delete_image(chart)


def create_images_folder():
    if not os.path.exists("images"):
        os.makedirs("images")


def delete_image(file_name: str):
    if os.path.isfile(f"images/{file_name}.webp"):
        os.remove(f"images/{file_name}.webp")


async def favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌟 Add", callback_data="favorites-add#0-9"),
         InlineKeyboardButton("🗑 Remove", callback_data="favorites-remove#0-9"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await reply_message(
        query=update.callback_query, text="Select option 💬", keyboard=keyboard
    )


async def favorites_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = get_data(query.data.split("_")[-1])
    favorites = Favorites.get(query.from_user.id).split(",")

    keyboard = [
        [
            InlineKeyboardButton("◀ Back", callback_data="favorites"),
            InlineKeyboardButton("🏠 Home", callback_data="home"),
        ]
    ]

    await query.answer()
    if query.data.split("_")[-1] not in favorites:
        Favorites.add(query.from_user.id, query.data.split("_")[-1])
        await reply_message(query=query, text=f"<b>{data['name']}</b> added to favorites 🌟", keyboard=keyboard)
    else:
        await reply_message(query=query, text=f"<b>{data['name']}</b> already in favorites ⭐", keyboard=keyboard)


def get_keyboard(cryptocurrencies, option):
    keyboard = []
    keyboard_layer = []

    data = get_data()

    for i in range(len(cryptocurrencies[:8])):
        keyboard_layer.append(InlineKeyboardButton(get_cryptocurrency_data(data, cryptocurrencies[i])['symbol'],
                                                   callback_data=f"{option}_{cryptocurrencies[i]}"))
        if i == 3:
            keyboard.append(keyboard_layer)
            keyboard_layer = []
    keyboard.append(keyboard_layer)

    return keyboard


async def select_favorites_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await reply_select_cryptocurrency(query, Favorites.get(query.from_user.id).split(",")[:-1])


async def favorites_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = get_data(query.data.split("_")[-1])

    Favorites.remove(query.from_user.id, query.data.split("_")[-1])

    keyboard = [
        [
            InlineKeyboardButton("◀ Back", callback_data="favorites"),
            InlineKeyboardButton("🏠 Home", callback_data="home"),
        ]
    ]

    await reply_message(query=query, text=f"<b>{data['name']}</b> removed from favorites 🗑", keyboard=keyboard)


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    favorites = Favorites.get(query.from_user.id).split(",")[:-1]
    review = get_favorite_review(get_data(), favorites) if favorites else "You don't have any favorite cryptocurrencies yet. Add to favorites to receive your personalized review 🧾"

    await reply_message(query=query, text=f"Review 📝\n<i>Prices of favorite cryptocurrencies at the current hour 💸</i>\n\n<i>{review}</i>", keyboard=keyboard)


def get_favorite_review(data, favorites):
    reviews = []
    for favorite in favorites:
        d = get_cryptocurrency_data(data, favorite)
        reviews.append(
            f" • {d['name']} ({d['symbol']}) — ${d['priceUsd']} ({'{0:.{1}f}'.format(float(d['changePercent24Hr']), 4)}%) {'📉' if d['changePercent24Hr'][0] == '-' else '📈'}")
    return "\n".join(reviews)


def get_cryptocurrency_data(data, cryptocurrency):
    for d in data:
        if d['id'] == cryptocurrency: return d


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶ On", callback_data="alarm_on"),
         InlineKeyboardButton("⏹ Off", callback_data="alarm_off"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await reply_message(
        query=update.callback_query, text="Select option 💬", keyboard=keyboard
    )


async def alarm_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🕛 0:00", callback_data="alarm_on_0"),
            InlineKeyboardButton("🕗 8:00", callback_data="alarm_on_8"),
            InlineKeyboardButton("🕛 12:00", callback_data="alarm_on_12"),
            InlineKeyboardButton("🕗 20:00", callback_data="alarm_on_20"),
        ],
        [
            InlineKeyboardButton("◀ Back", callback_data="alarm"),
            InlineKeyboardButton("🏠 Home", callback_data="home"),
        ],
    ]

    await reply_message(
        query=update.callback_query, text="Select time ⏰", keyboard=keyboard
    )


async def alarm_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="alarm"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]

    await enable_alarm(update, context)
    await reply_message(query=update.callback_query, text=f"Alarm is enabled on <i>{query.data.split('_')[-1]}:00</i> (UTC) ⏰", keyboard=keyboard)


async def enable_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.job_queue.run_daily(alarmed_review, time=datetime.time(hour=int(query.data.split('_')[-1])), days=(0, 1, 2, 3, 4, 5, 6), name=str(query.message.chat_id), chat_id=query.message.chat_id, data=str(query.from_user.id))


async def alarm_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("◀ Back", callback_data="alarm"),
         InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]

    await disable_alarm(update, context)
    await reply_message(
        query=update.callback_query,
        text="Alarm is disabled ⏰",
        keyboard=keyboard,
    )


async def disable_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.get_jobs_by_name(str(update.callback_query.message.chat_id))[0].schedule_removal()


async def alarmed_review(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    favorites = Favorites.get(int(context.job.data)).split(",")[:-1]
    review = get_favorite_review(get_data(), favorites) if favorites else "You don't have any favorite cryptocurrencies yet. Add to favorites to receive your personalized review 🧾"

    await send_alarm_message(context=context, text=f"Daily Review 📝⏰\n<i>Prices of favorite cryptocurrencies at the current hour 💸</i>\n\n<i>{review}</i>", keyboard=keyboard)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]

    await reply_message(query=query, text=f"About <b>Cryptifica</b> ℹ\n\nHey, {query.from_user.first_name} 👋🏻\n<i>I'm your personal cryptocurrency checker bot, made with ❤ on 🐍 by @m3r1v3 🤖💰</i>\n\n"
                        f"What can I do?\n\n"
                        f"<i> 💰 Show the current cryptocurrency prices\n"
                        f" 📈 Show cryptocurrency price chart for the last 30 days\n"
                        f" 📝 Make review for your favorite cryptocurrencies\n ⭐ Save your cryptocurrencies to favorites\n"
                        f" 🔔 Make review for you in specified time\n"
                        f"...and other features that we will make in the future ✨</i>\n\n"
                        f"Check prices, make charts with me. With <b>Cryptifica</b> 🤖",
                        keyboard=keyboard)


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
