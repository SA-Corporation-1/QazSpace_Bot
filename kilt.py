import json
from telegram import Update
from telegram.ext import ContextTypes

# Қолданушылар тізімі сақталатын файл
USER_LIST_FILE = "user_list.json"

# Админның ID
ADMIN_ID = 5239409990 # өзіңіздің ID-іңізді мұнда жазыңыз

# Қолданушылар тізімін сақтау
def load_user_list():
    try:
        with open(USER_LIST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Қолданушыны тізімге қосу
def save_user_list(user_list):
    with open(USER_LIST_FILE, "w") as f:
        json.dump(user_list, f)

# /access командасы — тек админ ғана қолданушыға қолжетімділік бере алады
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Қолданушының ID-і алынады

    # Тек админге ғана қолжетімділік беруге рұқсат
    if user_id != ADMIN_ID:
        await update.message.reply_text("Сізде бұл командаға қолжетімділік жоқ. Тек админ ғана рұқсат береді.")
        return

    # Қолданушының ID-ін алу
    if len(context.args) == 0:
        await update.message.reply_text("ID жазыңыз!")
        return

    target_id = int(context.args[0])  # Жіберілген ID
    user_list = load_user_list()

    if target_id not in user_list:
        user_list.append(target_id)  # Тізімге қосу
        save_user_list(user_list)
        await update.message.reply_text(f"{target_id} қолданушысына қолжетімділік берілді!")
    else:
        await update.message.reply_text(f"{target_id} қолданушысы бұрынырақ қолжетімділік алған.")
