from telegram import Update
from telegram.ext import ContextTypes

async def my_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"🆔 Сенің Telegram ID-ың: `{user_id}`", parse_mode='Markdown')
