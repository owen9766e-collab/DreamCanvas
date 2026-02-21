import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# التوكنات
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# إعداد Gemini الجديد
client = genai.Client(api_key=GEMINI_KEY)

# الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(str(e))

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
