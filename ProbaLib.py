import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from Constantes import *

async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    filepath = "probas.txt"

    if not context.args:
        # Affiche les probas actuelles
        probatext, probavideo = get_probas(chat_id)
        await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"🎯 Probabilité texte : {probatext}\n🎬 Probabilité vidéo : {probavideo}"
        )
        return

    # Vérifie les arguments
    if len(context.args) != 2:
        await update.message.reply_text("❗ Utilisation : /proba probatext probavideo (valeurs entre 0 et 1)")
        return

    try:
        probatext = float(context.args[0])
        probavideo = float(context.args[1])
        if not (0 <= probatext <= 1 and 0 <= probavideo <= 1):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❗ Les probabilités doivent être des nombres entre 0 et 1.\nT'as déjà fait des maths dans ta vie minable ?")
        return

    # Charge et met à jour le fichier
    lignes = []
    found = False
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith(str(chat_id)):
                    lignes.append(f"{chat_id}:{probatext}:{probavideo}\n")
                    found = True
                else:
                    lignes.append(line)
    except FileNotFoundError:
        pass

    if not found:
        lignes.append(f"{chat_id}:{probatext}:{probavideo}\n")

    with open(filepath, "w") as f:
        f.writelines(lignes)

    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="✅ Probabilités mises à jour."
    )

def get_probas(chat_id: int, default_text=1.0, default_video=1.0, filepath="probas.txt"):
    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if int(parts[0]) == chat_id:
                    return float(parts[1]), float(parts[2])
    except FileNotFoundError:
        pass  # Le fichier n'existe pas encore

    return default_text, default_video