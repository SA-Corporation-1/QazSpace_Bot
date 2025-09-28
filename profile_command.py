from telegram import Update
from telegram.ext import ContextTypes
from registration import load_users   # тіркелген қолданушыларды жүктеу функциясы

# /profile командасы
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users = load_users()

    # Қолданушы тіркелген бе?
    user_data = next((u for u in users if u["id"] == user_id), None)

    if not user_data:
        await update.message.reply_text(
            "❌ Сіз әлі тіркелмепсіз. Алдымен /start командасымен тіркеліңіз."
        )
        return

    # Профиль мәліметін шығару
    profile_text = (
        f"👤 Профиль:\n\n"
        f"🆔 ID: {user_data['id']}\n"
        f"👤 Аты: {user_data['first_name']}\n"
        f"💬 Лақап аты: {user_data['username']}\n"
        f"📅 Тіркелген уақыты: {user_data['registered_at']}"
    )

    await update.message.reply_text(profile_text)