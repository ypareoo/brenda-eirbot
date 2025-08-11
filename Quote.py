import random
import json

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from Constantes import *

# Charger les citations
def load_quotes():
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Enregistrer une citation
def save_quote(text):
    quotes = load_quotes()
    quotes.append(text)
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

# Commande /quote
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quotes = load_quotes()

    if context.args:
        # Texte après /quote
        text = " ".join(context.args)
        save_quote(text)
        await update.message.reply_text("✅ Citation enregistrée.")
    elif update.message.reply_to_message:
        # En réponse à un autre message
        text = update.message.reply_to_message.text
        if text:
            save_quote(text)
            await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="✅ Citation du message enregistrée."
    )
        else:
            await update.message.reply_text("⚠️ Le message ne contient pas de texte.")
    else:
        # Renvoie une citation aléatoire
        if quotes:
            await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"💬 {random.choice(quotes)}"
    )
        else:
            await update.message.reply_text("📭 Aucune citation enregistrée.")