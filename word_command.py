import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Сөздерді жүктеу функциясы
def load_words():
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Қолданушының сөз лимитін сақтау функциясы
def save_user_limit(user_id, limit):
    try:
        with open("user_limits.json", "r", encoding="utf-8") as f:
            user_limits = json.load(f)
    except FileNotFoundError:
        user_limits = {}
    
    user_limits[str(user_id)] = limit
    
    with open("user_limits.json", "w", encoding="utf-8") as f:
        json.dump(user_limits, f, ensure_ascii=False, indent=4)

# Қолданушының сөз лимитін жүктеу функциясы
def load_user_limit(user_id):
    try:
        with open("user_limits.json", "r", encoding="utf-8") as f:
            user_limits = json.load(f)
            return user_limits.get(str(user_id), 5)  # Әдепкі 5 сөз
    except FileNotFoundError:
        return 5

# /word командасы — кездейсоқ сөздерді көрсету
async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    words = load_words()
    
    if not words:
        await update.message.reply_text("Сөздер базасы бос немесе табылмады.")
        return
    
    # Қолданушының лимитін алу
    word_limit = load_user_limit(user_id)
    
    # Кездейсоқ сөздерді таңдау
    if len(words) <= word_limit:
        selected_words = words
    else:
        selected_words = random.sample(words, word_limit)
    
    # Хабарды құрастыру
    message = f"🎯 Сізге {word_limit} сөз:\n\n"
    
    for i, word_data in enumerate(selected_words, 1):
        message += (
            f"{i}. **{word_data['word']}**\n"
            f"   Аударма: {word_data['translation']}\n"
            f"   Мысал: {word_data['example']}\n\n"
        )
    
    # Келесі сөздерге өту үшін батырма
    keyboard = [[InlineKeyboardButton("🔄 Келесі сөздер", callback_data="next_words")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# /set_words командасы — күніне қанша сөз жаттайтынын баптау
async def set_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("3 сөз", callback_data="3"), InlineKeyboardButton("5 сөз", callback_data="5")],
        [InlineKeyboardButton("10 сөз", callback_data="10"), InlineKeyboardButton("15 сөз", callback_data="15")],
        [InlineKeyboardButton("20 сөз", callback_data="20")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Күніне қанша сөз жаттайсыз?", reply_markup=reply_markup
    )

# CallbackQueryHandler арқылы жауапты өңдеу
async def handle_word_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    choice = query.data
    
    if choice == "next_words":
        # Келесі сөздерді көрсету
        words = load_words()
        word_limit = load_user_limit(user_id)
        
        if len(words) <= word_limit:
            selected_words = words
        else:
            selected_words = random.sample(words, word_limit)
        
        message = f"🎯 Жаңа {word_limit} сөз:\n\n"
        
        for i, word_data in enumerate(selected_words, 1):
            message += (
                f"{i}. **{word_data['word']}**\n"
                f"   Аударма: {word_data['translation']}\n"
                f"   Мысал: {word_data['example']}\n\n"
            )
        
        keyboard = [[InlineKeyboardButton("🔄 Келесі сөздер", callback_data="next_words")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        # Сөз лимитін сақтау
        save_user_limit(user_id, int(choice))
        
        # Деректі сөздерді бірден көрсету
        words = load_words()
        word_limit = int(choice)
        
        if not words:
            await query.edit_message_text("Сөздер базасы бос. Алдымен сөздерді қосыңыз.")
            return
        
        if len(words) <= word_limit:
            selected_words = words
        else:
            selected_words = random.sample(words, word_limit)
        
        message = f"✅ Сіз {choice} сөз таңдадыңыз! 🎉\n\n"
        message += f"Төменде {word_limit} сөз:\n\n"
        
        for i, word_data in enumerate(selected_words, 1):
            message += (
                f"{i}. **{word_data['word']}**\n"
                f"   Аударма: {word_data['translation']}\n"
                f"   Мысал: {word_data['example']}\n\n"
            )
        
        keyboard = [[InlineKeyboardButton("🔄 Келесі сөздер", callback_data="next_words")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# /my_limit командасы — ағымдағы лимитті көрсету
async def my_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_limit = load_user_limit(user_id)
    
    await update.message.reply_text(f"📊 Сіздің ағымдағы лимитіңіз: {current_limit} сөз/күн")

# /add_word командасы — жаңа сөз қосу (админдер үшін)
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Бұл жерде админдік тексеру қосуға болады
    if context.args and len(context.args) >= 3:
        new_word = {
            "word": context.args[0],
            "translation": context.args[1],
            "example": " ".join(context.args[2:])
        }
        
        words = load_words()
        words.append(new_word)
        
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
        
        await update.message.reply_text(f"✅ Сөз сәтті қосылды: {new_word['word']}")
    else:
        await update.message.reply_text("Қатарымен: /add_word <сөз> <аударма> <мысал>")