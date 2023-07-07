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
    if query.data == "value": return value_option(query)
    elif query.data == "alarm": return alarm_option(query)
    elif query.data == "chart": return chart_option(query)
    elif query.data == "review": return review_option(query)
    elif query.data == "back":
    else: await context.bot.wrong_method_name()

def value_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"💲 Current price", reply_markup=InlineKeyboardMarkup(keyboard))
    
def alarm_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"🔔 Notify", reply_markup=InlineKeyboardMarkup(keyboard))

def chart_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📈 Price chart", reply_markup=InlineKeyboardMarkup(keyboard))

def review_option(query):
    keyboard = [
        [InlineKeyboardButton("⬅️", callback_data="back")],
    ]
    await query.answer()
    await query.edit_message_text(text=f"📝 Daily review", reply_markup=InlineKeyboardMarkup(keyboard))

def back(query):
    keyboard = [
        [InlineKeyboardButton("💲", callback_data="value"), InlineKeyboardButton("🔔", callback_data="alarm")],
        [InlineKeyboardButton("📈", callback_data="chart"), InlineKeyboardButton("📝", callback_data="review")],
    ]
    
    await query.answer()
    await query.edit_message_text(
        text=f'Welcome to Cryptifica 👋🏻\n\nYour personal cryptocurrency checker bot 🤖💰\n\nSelect option 💬\n\n💲 Show current price\n🔔 Notify about the cost\n📈 Show price chart\n📝 Daily reviews',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
            f'Something went wrong ⚠\n\nSelect option 💬\n\n💲 Show current price\n🔔 Notify about the cost\n📈 Show price chart\n📝 Daily reviews',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error_handler)

    app.run_polling()