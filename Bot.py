from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import datetime
from config import BOT_TOKEN, GROUP_CHAT_ID

user_state = {}

keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("🟢 ورود"), KeyboardButton("🔴 خروج")]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=keyboard
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    user_state[user_id] = text

    if text in ["🟢 ورود", "🔴 خروج"]:
        await update.message.reply_text(
            "📍 لطفاً لوکیشن خود را ارسال کنید",
            reply_markup=ReplyKeyboardRemove()
        )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    location = update.message.location

    action = user_state.get(user_id, "نامشخص")

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = f"""
{action}

👤 {user.first_name}
🆔 @{user.username}
🕒 {time_now}

📍 موقعیت:
https://maps.google.com/?q={location.latitude},{location.longitude}
"""

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

    await update.message.reply_text("ثبت شد ✅", reply_markup=keyboard)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.run_polling()

if __name__ == "__main__":
    main()
