from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters,
)
import json
import random
from datetime import datetime

# ====== JSON файл ======
REGISTERED_USERS_FILE = "AQPARAT_ORDASY.json"

# ====== Мотивациялық сөздер ======
MOTIVATIONAL_QUOTES = [
    "Бүгінгі кішкентай қадам — ертеңгі үлкен жетістіктің бастауы! 🚀",
    "Ешқашан берілме, арманыңды жүзеге асыруға бір қадам жақынсың! 💪",
    "Білім — болашаққа салынған ең жақсы инвестиция! 📚",
    "Әр күн — жаңа мүмкіндік! 🌟",
    "Өзіңе сен, сонда бәрі де мүмкін! 🔑",
]

# ====== Conversation сатылары ======
ASK_NAME, ASK_USERNAME = range(2)

# ====== Файлдан қолданушыларды оқу ======
def load_users():
    try:
        with open(REGISTERED_USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ====== Файлға қолданушыларды жазу ======
def save_users(users):
    with open(REGISTERED_USERS_FILE, "w") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    print(f"DEBUG: /start командасы user_id: {user_id}")
    
    try:
        users = load_users()
        print(f"DEBUG: {len(users)} қолданушы табылды")
    except Exception as e:
        print(f"DEBUG: Файл оқу қатесі: {e}")
        users = []
    
    # УАҚЫТША: Әрқашан тіркелу батырмасын көрсету
    keyboard = [[InlineKeyboardButton("🎯 ТІРКЕЛУ ТЕСТ", callback_data="register")]]
    await update.message.reply_text(
        "Тіркелу үшін төмендегі батырманы басыңыз:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ====== «Тіркелу» батырмасы ======
async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Атыңды енгізіңіз:")
    return ASK_NAME

# ====== 1-қатам: Аты ======
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["first_name"] = update.message.text
    await update.message.reply_text("Енді лақап атыңды енгіз:")
    return ASK_USERNAME

# ====== 2-қатам: Лақап аты ======
async def ask_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    user = update.message.from_user

    users = load_users()

    new_user = {
        "id": user.id,
        "first_name": context.user_data["first_name"],
        "last_name": user.last_name or "",
        "username": context.user_data["username"],
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    users.append(new_user)
    save_users(users)

    random_quote = random.choice(MOTIVATIONAL_QUOTES)
    await update.message.reply_text(
        f"✅ Тіркелу сәтті аяқталды!\n\n"
        f"Сәлем, {new_user['first_name']}! 👋\n"
        f"{random_quote}"
    )
    return ConversationHandler.END

# ====== Тіркелуден бас тарту ======
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Тіркелу тоқтатылды.")
    return ConversationHandler.END

# ====== Conversation Handler құру ======
def get_registration_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(register_user, pattern="^register$")],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_username)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )