import json
from telegram import Update
from telegram.ext import ContextTypes

# Қолданушылар тізімі сақталатын файл
USER_LIST_FILE = "Akimsiler.json"

# Админның ID

      # өзіңіздің ID-іңізді мұнда жазыңыз

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

# Қолданушылар тізімін жүктеу
ADMIN_LIST = load_user_list()  # [{"id": 5239409990, "nickname": "Admin1"}, ...]

# Тексеру үшін ADMIN_LIST-ті басып шығару
print("Жүктелген админдер тізімі:", ADMIN_LIST)

# /access командасы — тек админ ғана қолданушыға қолжетімділік бере алады
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Қолданушының ID-і алынады

    # Тек админге ғана қолжетімділік беруге рұқсат
    if user_id not in [admin["id"] for admin in ADMIN_LIST]:
        await update.message.reply_text("Сізге бұл команданы қолдануға рұқсат жоқ!")
        return

    # Қолданушының ID-ін және лақап атын алу
    if len(context.args) < 2:
        await update.message.reply_text("ID және лақап ат жазыңыз! Мысалы: /access 1234567890 AdminName")
        return

    try:
        target_id = int(context.args[0])  # Жіберілген ID
        nickname = " ".join(context.args[1:])  # Лақап ат
    except ValueError:
        await update.message.reply_text("Қате ID! Сан енгізіңіз.")
        return

    if target_id not in [admin["id"] for admin in ADMIN_LIST]:
        ADMIN_LIST.append({"id": target_id, "nickname": nickname})  # Тізімге қосу
        save_user_list(ADMIN_LIST)
        await update.message.reply_text(
            f"Құттықтаймыз, {nickname}! 🎉 Сіз енді біздің қатарымызға қосылдыңыз.\n\n"
            "Дәрежеңіз: Әкімші 🛡️\n\n"
            "Сізге қол жетімді командалар: \n"
            "✅ /remove_access - Қолданушыны админнен шығару\n"
            "✅ /list_admins - Барлық админдерді көру"
        )
    else:
        await update.message.reply_text(f"{target_id} қолданушысы бұрынырақ админдік алған.")

# /remove_access командасы — админді тізімнен алып тастау
async def remove_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Қолданушының ID-і алынады

    # Тек админге ғана қолжетімділік беруге рұқсат
    if user_id not in [admin["id"] for admin in ADMIN_LIST]:
        await update.message.reply_text("Сізге бұл команданы қолдануға рұқсат жоқ!")
        return

    # Қолданушының ID-ін алу
    if len(context.args) == 0:
        await update.message.reply_text("ID жазыңыз!")
        return

    try:
        target_id = int(context.args[0])  # Жіберілген ID
    except ValueError:
        await update.message.reply_text("Қате ID! Сан енгізіңіз.")
        return

    for admin in ADMIN_LIST:
        if admin["id"] == target_id:
            ADMIN_LIST.remove(admin)  # Тізімнен алып тастау
            save_user_list(ADMIN_LIST)
            await update.message.reply_text(f"{admin['nickname']} ({target_id}) админдер тізімінен алынып тасталды!")
            return

    await update.message.reply_text(f"{target_id} қолданушысы админдер тізімінде жоқ.")

# /list_admins командасы — барлық админдердің тізімін көрсету
async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Қолданушының ID-і алынады

    # Тек админге ғана қолжетімділік беруге рұқсат
    if user_id not in [admin["id"] for admin in ADMIN_LIST]:
        await update.message.reply_text("Сізге бұл команданы қолдануға рұқсат жоқ!")
        return

    if not ADMIN_LIST:
        await update.message.reply_text("Админдер тізімі бос.")
        return

    admin_list = "\n".join([f"{admin['nickname']} ({admin['id']})" for admin in ADMIN_LIST])
    await update.message.reply_text(f"Админдер тізімі:\n{admin_list}")
