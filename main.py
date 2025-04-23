import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from deep_translator import GoogleTranslator
from handlers.myid import my_id_handler
from kilt import access  # kilt.py файлынан access функциясын импорттау
from groupid import group_id_handler  # groupid.py ішіндегі функцияны импорттау
from translate import get_translate_handlers  # translate.py ішіндегі хендлерлерді импорттау
from about import about  # about.py файлынан импорттаймыз
from help_command import help_command  # help_command.py файлын импорттаймыз

# /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем! QazSpace боты жұмыс істеп тұр 🚀")

# негізгі функция
def main():
    load_dotenv()  # .env файлды жүктейміз
    token = os.getenv("TOKEN")  # .env ішіндегі TOKEN мәнін аламыз

    # Ботты қолдануға дайындау
    app = ApplicationBuilder().token(token).build()

    # Хендлер қосу
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id_handler))  # myid хендлерін қосамыз
    app.add_handler(CommandHandler("access", access))  # /access команданы қосу
    app.add_handler(CommandHandler("groupid", group_id_handler))  # жаңа команда
    app.add_handlers(get_translate_handlers())
    app.add_handler(CommandHandler("about", about))  # /about командасын қосу
    app.add_handler(CommandHandler("help", help_command))

    print("✅ Бот іске қосылды. Telegram-нан /start деп жазып көр!")

    # Ботты іске қосу
    app.run_polling()

if __name__ == "__main__":
    main()
