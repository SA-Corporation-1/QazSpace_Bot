from telegram import Update
from telegram.ext import ContextTypes

async def group_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🛰️ Бұл топтың ID-сі: `{chat_id}`", parse_mode="Markdown"
    )
