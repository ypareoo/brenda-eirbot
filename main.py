from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
from time import *
import os
import random
import shutil

#code fractionné
from ProbaLib import *
from EchoLib import *
from Constantes import *
from Quote import *




# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="Bonjour ! Je suis une pale copie de la Brenda original.\nPour contacter son créateur : @Paulbosse"
    )      
    
async def horaires(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(path_command_msg+"horaires.txt", "r", encoding="utf-8") as f:
        HORAIRES = f.read()
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=HORAIRES
    )
    
async def bureau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(path_command_msg+"bureau.txt", "r", encoding="utf-8") as f:
        BUREAU = f.read()
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=BUREAU
    )
    
async def playlists(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(path_command_msg+"playlists.txt", "r", encoding="utf-8") as f:
        PLAYLISTS = f.read()
    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=PLAYLISTS
    )
    
async def gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Lire les URLs depuis le fichier gif.txt
        with open("gif.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        # Extraire les URLs (en ignorant les descriptions après le "|")
        urls = [line.split("|")[0].strip() for line in lines if "|" in line]

        # Choisir un GIF aléatoire
        if urls:
            selected_gif = random.choice(urls)
            await update.message.reply_animation(animation=str(selected_gif))
        else:
            await update.message.reply_text("Aucun GIF trouvé dans le fichier.")

    except FileNotFoundError:
        await update.message.reply_text("Le fichier gif.txt est introuvable.")
    except Exception as e:
        await update.message.reply_text(f"Une erreur est survenue : {e}")
        await update.message.reply_text(f"{selected_gif}")





EDIT_PASSWORD = "fallito"

async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérifie que la commande vient d'une conversation privée
    if update.message.chat.type != "private":
        await update.message.reply_text("⛔ Cette commande ne peut être utilisée qu'en message privé bouffon.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Pauvre incompétent le format est incorrect. Utilisation : /edit nom_fichier motdepasse\nPuis envoyez le nouveau contenu du message en revenant à la ligne.")
        return

    nom_fichier = context.args[0]
    mot_de_passe = context.args[1]

    if mot_de_passe != EDIT_PASSWORD:
        await update.message.reply_text("❌ Mot de passe incorrect.")
        return

    # Récupère le texte complet du message sans la commande
    texte_complet = update.message.text
    lignes = texte_complet.split("\n", 1)
    if len(lignes) < 2 or not lignes[1].strip():
        await update.message.reply_text("❌ Aucun nouveau contenu fourni.\nEnvoie le texte juste après la commande, sur une nouvelle ligne.\n\n<c'est relou de devoir toujours tout vous expliquer")
        return

    nouveau_contenu = lignes[1]

    chemin_fichier = os.path.join(path_command_msg, f"{nom_fichier}.txt")

    try:
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        await update.message.reply_text(f"✅ Le fichier `{nom_fichier}.txt` a été mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")
        await update.message.reply_text("❌ Erreur lors de la mise à jour du fichier.")



FICHIER_EVENT = "events.txt"

# Créer le fichier s'il n'existe pas
if not os.path.exists(FICHIER_EVENT):
    with open(FICHIER_EVENT, "w", encoding="utf-8") as f: #utf-8 pour supporter les emojis
        pass

# Sauvegarder un événement dans le fichier
def enregistrer_evenement(chat_id, dt, nom_evenement):
    lignes = []
    updated = False
    print("au secours !!!")
    # Lire et remplacer la ligne de l'utilisateur si elle existe
    with open(FICHIER_EVENT, "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith(f"{chat_id}|"):
                lignes.append(f"{chat_id}|{dt.strftime('%d/%m/%Y %H:%M:%S')}|{nom_evenement}\n")
                updated = True
            else:
                lignes.append(ligne)

    if not updated:
        lignes.append(f"{chat_id}|{dt.strftime('%d/%m/%Y %H:%M:%S')}|{nom_evenement}\n")

    with open(FICHIER_EVENT, "w", encoding="utf-8") as f:
        f.writelines(lignes)

# Récupérer l'événement pour un utilisateur
def lire_evenement(chat_id):
    with open(FICHIER_EVENT, "r", encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith(f"{chat_id}|"):
                _, date_str, nom_evenement = ligne.strip().split("|", 2)
                dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                return dt, nom_evenement
    return None

# Stockage en mémoire : {user_id: (datetime_obj, nom_evenement)}
evenements = {}

# /mainevent JJ/MM/AAAA HH:mm:ss nom de l'evenement
async def mainevent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("oui")
    if len(context.args) < 3:
        await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="""Utilisation : /mainevent JJ/MM/AAAA HH:mm:ss nom de l'événement\nC'est pas compliqué fainéant"""
        )
        return
    print("oui oui oui")
    date_str = context.args[0]
    time_str = context.args[1]
    nom_evenement = " ".join(context.args[2:])

    try:
        print("alors peut-être")
        dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")

        chat_id = update.effective_chat.id
        #evenements[user_id] = (dt, nom_evenement)
        enregistrer_evenement(chat_id, dt, nom_evenement)

        await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"✅ Événement '{nom_evenement}' enregistré pour le {dt.strftime('%d/%m/%Y %H:%M:%S')}."
        )

    except ValueError:
        await update.message.reply_text(
            """❌ Format invalide. Utilise JJ/MM/AAAA HH:mm:ss nom de l'événement\nfait un effort tocard"""
        )
    print("enfin !")

# /countdown
async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    evenement = lire_evenement(chat_id)

    if not evenement:
        await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="Aucun événement majeur enregistré. Utilise /mainevent."
    )
        return

    dt, nom_evenement = evenement
    now = datetime.now()
    delta = dt - now

    if delta.total_seconds() > 0:
        jours = delta.days
        heures, reste = divmod(delta.seconds, 3600)
        minutes, secondes = divmod(reste, 60)

        await update.message.reply_text(
            f"Il reste {jours} jour{'s' if jours > 1 else ''}, {heures} heure{'s' if heures > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''} et {secondes}.{int((time()%1)*5237572478956232624636126727458)} seconde{'s' if secondes > 1 else ''} \n"
            f"avant {nom_evenement}", quote=False
        )
        if jours < 7:
            await update.message.reply_animation(animation="https://tenor.com/bebdW.gif")
    else:
        await update.message.reply_text("Aucun événement majeur enregistré. Utilise /mainevent.")





async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérifie si un argument est fourni (/help commandeX)
    if context.args:
        commande = context.args[0]
        chemin_fichier = os.path.join(HELP_MESSAGE_FILE, f"{commande}.txt")

        if os.path.isfile(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                contenu = f.read()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=contenu
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Aucune aide trouvé pour la commande '{commande}'.\n T'es sûr qu'elle existe au moins ptit con ?"
            )
        return

    # Sinon, lister toutes les commandes
    commandes = []
    for handler in context.application.handlers[0]:
        if isinstance(handler, CommandHandler):
            for nom in handler.commands:
                commandes.append(f"/{nom}")

    commandes = sorted(set(commandes))
    texte = (
        "📜 Commandes disponibles :\n" +
        "\n".join(commandes) +
        "\n\nUtilisez /help <commande> pour voir le détail.\n" +
        "Contactez @Paulbosse pour des suggestions/remarques"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texte
    )

import json

FICHIER_WELCOME = "welcome_message.txt"

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Répond à un message pour le définir comme message de bienvenue.")
        return

    msg = update.message.reply_to_message
    contenu = {}

    if msg.text:
        contenu = {"type": "text", "content": msg.text}
    elif msg.sticker:
        contenu = {"type": "sticker", "content": msg.sticker.file_id}
    elif msg.video:
        contenu = {"type": "video", "content": msg.video.file_id}
    else:
        await update.message.reply_text("❌ Type de message non supporté.")
        return

    with open(FICHIER_WELCOME, "w", encoding="utf-8") as f:
        json.dump(contenu, f)

    await update.message.reply_text("✅ Message de bienvenue enregistré avec succès.")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.new_chat_members:
        return

    # Charge le message de bienvenue
    if not os.path.exists(FICHIER_WELCOME):
        return  # Pas de message défini

    with open(FICHIER_WELCOME, "r", encoding="utf-8") as f:
        contenu = json.load(f)

    try:
        if contenu["type"] == "text":
            await update.message.reply_text(contenu["content"])
        elif contenu["type"] == "sticker":
            await update.message.reply_sticker(contenu["content"])
        elif contenu["type"] == "video":
            await update.message.reply_video(contenu["content"])
    except Exception as e:
        print(f"Erreur en envoyant le message de bienvenue : {e}")




# 🎲 Commande /pp → envoie une photo aléatoire de n’importe quel utilisateur
async def pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Recherche toutes les photos dans tous les sous-dossiers
    all_photos = []
    for root, dirs, files in os.walk(PHOTO_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_photos.append(os.path.join(root, file))

    if not all_photos:
        await context.bot.send_message(chat_id, "Aucune photo enregistrée pour le moment.")
        return

    # Choix aléatoire
    chosen_path = random.choice(all_photos)
    await context.bot.send_photo(chat_id=chat_id, photo=open(chosen_path, 'rb'))
        
        
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return

    username = f"@{user.username}" if user.username else "Aucun nom d'utilisateur"
    user_id = user.id

    message = f"👤 Informations utilisateur :\n\n🔹 Nom d'utilisateur : {username}\n🔹 ID : `{user_id}`"
    
    await update.message.reply_text(message, parse_mode="Markdown")
    

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    
    app.add_handler(CommandHandler("horaires", horaires))
    app.add_handler(CommandHandler("bureau", bureau))
    app.add_handler(CommandHandler("playlists", playlists))
    
    app.add_handler(CommandHandler("mainevent", mainevent))
    app.add_handler(CommandHandler("countdown", countdown))

    
    app.add_handler(CommandHandler("gif", gif))
    
    app.add_handler(CommandHandler("help", help_command))

    
    #app.add_handler(CommandHandler("video", video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CommandHandler("on", on))
    app.add_handler(CommandHandler("off", off))    
    
    app.add_handler(CommandHandler("welcome", set_welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(CommandHandler("proba", proba))
    
    app.add_handler(CommandHandler("edit", edit))
    
    app.add_handler(CommandHandler("pp", pp))

    app.add_handler(CommandHandler("quote", quote))
    
    app.add_handler(CommandHandler("me",me))

    #app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot lancé...")
    app.run_polling()

if __name__ == '__main__':
    main()
