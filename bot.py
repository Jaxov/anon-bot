from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = '8004499733:AAEzk0ak7wMbYmqN8NsNrNQFCvbcfpsFXOY'

async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message.reply_to_message:
        await message.reply_text("Ответьте на сообщение с вопросом.")
        return

    # Тут логика обработки

    questuion = message.text

    await message.reply_text("Ответ обработан.")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_reply))
app.run_polling()