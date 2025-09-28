import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

# ================= Импорт =================
from handlers.myid import my_id_handler
from kilt import access, remove_access, list_admins
from groupid import group_id_handler
from translate import get_translate_handlers
from about import about
from help_command import help_command
from word_command import word, set_words, handle_word_choice, my_limit, add_word
from profile_command import profile
from registration import start, get_registration_handler

# ================= Негізгі функция =================
async def main():
    # --- Токенді жүктеу ---
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("❌ .env файлында TOKEN мәні табылмады!")

    # --- Қолданбаны құру ---
    app = ApplicationBuilder().token(token).build()

    # ===== Командалар =====
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", my_id_handler))
    app.add_handler(CommandHandler("groupid", group_id_handler))
    app.add_handler(CommandHandler("access", access))
    app.add_handler(CommandHandler("remove_access", remove_access))
    app.add_handler(CommandHandler("list_admins", list_admins))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("word", word))
    app.add_handler(CommandHandler("set_words", set_words))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("my_limit", my_limit))
    app.add_handler(CommandHandler("add_word", add_word))
    # ====== МҮНДЕМЕЛІ ТҮЗЕТУ: Тіркелуді БІРІНШІ орынға ======
    app.add_handler(get_registration_handler())   # ✅ БІРІНШІ!

    # ====== Батырма таңдау ======
    app.add_handler(CallbackQueryHandler(handle_word_choice))  # ✅ ЕКІНШІ!

    # ===== Аударма =====
    app.add_handlers(get_translate_handlers())

    print("✅ Бот іске қосылды. Telegram-нан /start деп жазып көр!")

    # --- Бот polling ---
    await app.run_polling()

# ================= Басты орын =================
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())