import os
import whisper
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7907047504:AAHAx_Z52EN0zjd-V0-GVWjcddaVHgSdKjw'
model = whisper.load_model("base")
custom_keyboard = ReplyKeyboardMarkup(
    keyboard=[["⬆️ Subir", "⬇️ Bajar"]],
    resize_keyboard=True,          # Adjusts to fit screen
    one_time_keyboard=False,       # Always visible
    input_field_placeholder="Presiona un botón o envía un audio"
)

async def show_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Controla la pantalla o envía audio 🎤",
        reply_markup=custom_keyboard
    )

async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "⬆️ Subir":
        await update.message.reply_text("📈 Subiendo contenido")
    elif msg == "⬇️ Bajar":
        await update.message.reply_text("📉 Bajando contenido")
    else:
        await update.message.reply_text("Comando no reconocido")
    print(msg)

# Handle voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.voice.file_id)
    path = f"voice_{update.message.from_user.id}.ogg"
    await file.download_to_drive(path)

    result = model.transcribe(path, language="es")
    print(result)
    text = result["text"]

    # Here: transcribe and trigger action
    await update.message.reply_text("🎧 Audio recibido, procesando...")
    os.remove(path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", show_keyboard))  # Send keyboard on /start
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_button_press))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot listo ✅")
    app.run_polling()

if __name__ == "__main__":
    main()