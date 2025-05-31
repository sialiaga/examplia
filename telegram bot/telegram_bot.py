import os
import whisper
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = '7907047504:AAHAx_Z52EN0zjd-V0-GVWjcddaVHgSdKjw'
model = whisper.load_model("base")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envíame un mensaje de voz y te lo transcribo en español.")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    file = await context.bot.get_file(update.message.voice.file_id)
    local_path = f"voice_{user_id}.ogg"
    await file.download_to_drive(local_path)

    # Transcribe
    result = model.transcribe(local_path, language="es")
    print(result)
    text = result["text"]

    await update.message.reply_text(f"✍️ Transcripción: {text}")
    os.remove(local_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot listening for voice messages...")
    app.run_polling()

if __name__ == "__main__":
    main()