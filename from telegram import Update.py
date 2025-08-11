from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7744709806:AAGaNL4UQxGFbpXhQBfLCIoodBZXW-2fL5I"  # Remplacez par le token fourni par BotFather

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour ! Je suis un bot Telegram minimal.")

# Répondre à chaque message texte
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot lancé...")
    app.run_polling()

if __name__ == '__main__':
    main()
