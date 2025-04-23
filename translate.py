from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from deep_translator import GoogleTranslator

# Тіл бағытын сақтау үшін
user_translation_direction = {}

# Тіл таңдау мәзірі
async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English 🇺🇸", callback_data='to_en')],
        [InlineKeyboardButton("Kazakh 🇰🇿", callback_data='to_kk')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Өз тіліңізді таңдаңыз / Choose your language:", reply_markup=reply_markup)

# Callback: Тілді таңдағанда
async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'to_en':
        user_translation_direction[query.from_user.id] = ('en', 'kk')
        await query.edit_message_text("Translation: English → Kazakh. Type a message.")
    elif query.data == 'to_kk':
        user_translation_direction[query.from_user.id] = ('kk', 'en')
        await query.edit_message_text("Аударма: Қазақша → Ағылшынша. Мәтін жазыңыз.")


# Аударма жасау
async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_translation_direction:
        await update.message.reply_text("Алдымен /translate командасы арқылы тіл бағытын таңдаңыз.")
        return

    src, dest = user_translation_direction[user_id]
    text_to_translate = update.message.text

    try:
        # deep-translator арқылы аударма жасау
        translated = GoogleTranslator(source=src, target=dest).translate(text_to_translate)
        await update.message.reply_text(translated)
    except Exception as e:
        await update.message.reply_text(f"Аудармада қате орын алды: {e}")

# Хендлерлерді қосу
def get_translate_handlers():
    return [
        CommandHandler("translate", choose_language),
        CallbackQueryHandler(language_chosen),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_translation),
    ]
