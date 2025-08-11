import unicodedata
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from Constantes import *
import random
from ProbaLib import *
import shutil
import time
from datetime import datetime, timedelta


def sans_accents(texte):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    ).lower()
    
def charger_triggers():
    try:
        triggers = {}
        if os.path.exists(TRIGGERS_FILE):
            with open(TRIGGERS_FILE, "r", encoding="utf-8") as f:
                for ligne in f:
                    if '|' in ligne:
                        mot, reponse = ligne.strip().split('|', 1)
                        triggers[mot.lower()] = reponse
        return triggers
    except:
        print("erreur dans les triggers")

#s'execute au démarrage
triggers_dict = charger_triggers()



############fonctions nécessaires pour la commande /pp
def get_user_folder(user) -> str:
    # Utilise l'username si disponible, sinon l'ID
    name = user.username if user.username else f"id_{user.id}"
    return os.path.join(PHOTO_DIR, name)

def is_user_excluded(user_id: int) -> bool:
    if not os.path.exists(EXCLUDED_USERS_FILE):
        return False
    with open(EXCLUDED_USERS_FILE, "r") as f:
        excluded_ids = {line.strip() for line in f if line.strip()}
    return str(user_id) in excluded_ids

def is_recent_update(folder_path: str) -> bool:
    print("verif updating")
    timestamp_path = os.path.join(folder_path, TIMESTAMP_FILENAME)
    if not os.path.exists(timestamp_path):
        return False
    try:
        print("encore")
        with open(timestamp_path, "r") as f:
            timestamp_str = f.read().strip()
            last_update = datetime.fromisoformat(timestamp_str)
            return datetime.now() - last_update < UPDATE_INTERVAL
    except Exception:
        return False

def save_timestamp(folder_path: str):
    timestamp_path = os.path.join(folder_path, TIMESTAMP_FILENAME)
    with open(timestamp_path, "w") as f:
        f.write(datetime.now().isoformat())


# 📥 Enregistre toutes les photos de profil d’un utilisateur
async def save_all_profile_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("bg")
    user = update.effective_user
    if not user:
        return

    print(user.id)
    if is_user_excluded(user.id):
        print(f"Utilisateur {user.id} exclu.")
        return
    
    folder_path = get_user_folder(user)

    if is_recent_update(folder_path):
        print(f"Mise à jour déjà effectuée récemment pour {user.id}.")
        return

    print("un")
    # Supprime l'ancien dossier s'il existe
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    print("deux")
    photos = await context.bot.get_user_profile_photos(user.id, limit=100)

    if photos.total_count == 0:
        return

    for index, photo_group in enumerate(photos.photos):
        best_photo = photo_group[-1]  # meilleure résolution
        file = await context.bot.get_file(best_photo.file_id)

        photo_path = os.path.join(folder_path, f"photo_{index + 1}.jpg")
        await file.download_to_drive(photo_path)


async def on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ECHO_ON
    ECHO_ON = True
    
async def off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ECHO_ON
    ECHO_ON = False
    print("off : ",ECHO_ON)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("echo(logie)")
    
    #gestion des photos de profils
    if update.effective_user:
        try:
            await save_all_profile_photos(update, context)
        except Exception as e:
            print(f"Erreur dans la sauvegarde des photos de profils : {e}")
            
    print("echo_on :",ECHO_ON)            
    if not ECHO_ON :
        print("ambiance désactivée")
        return
        
    from urllib.parse import unquote
    import requests

    texte = sans_accents(update.message.text)
    mots = texte.split()
    
    #dit_le
    try:
        for word in mots :
            dit_le = 0
            a_dire = ""
            for lettres in word :
                if dit_le >= 2 :
                    a_dire += lettres
                    dit_le += 1
                elif lettres == "d" and dit_le == 0:
                    dit_le = 1
                elif lettres == "i" and dit_le == 1:
                    dit_le = 2
                else :
                    dit_le = 0
            if dit_le > 2:
                if random.random() < get_probas(update.effective_chat.id)[0]:
                    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=a_dire
    )
    except Exception as e:
        print(f"Erreur dans les dit_le : {e}")
        
    #cri_le
    try:
        for word in mots :
            dit_le = 0
            a_dire = ""
            for lettres in word :
                if dit_le >= 3 :
                    a_dire += lettres
                    dit_le += 1
                elif lettres == "c" and dit_le == 0:
                    dit_le = 1
                elif lettres == "r" and dit_le == 1:
                    dit_le = 2
                elif lettres == "i" and dit_le == 2:
                    dit_le = 3
                else :
                    dit_le = 0
            if dit_le > 3:
                if random.random() < get_probas(update.effective_chat.id)[0]:
                    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=a_dire.upper()
    )
    except Exception as e:
        print(f"Erreur dans les dit_le : {e}")
        
    #chocolatine
    try:
        for word in mots :
            dit_le = 0
            a_dire = ""
            for lettres in word[::-1] : #parcours le mot en partant de la fin
                if dit_le >= 3 :
                    a_dire += lettres
                    dit_le += 1
                elif lettres == "e" and dit_le == 0:
                    dit_le += 1
                elif lettres == "n" and dit_le == 1:
                    dit_le += 1
                elif lettres == "i" and dit_le == 2:
                    dit_le += 1
                else :
                    break
            if dit_le > 3:
                if random.random() < get_probas(update.effective_chat.id)[0]:
                    await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="c'est pain au "+a_dire[::-1]+" pas "+word
    )
    except Exception as e:
        print(f"Erreur dans chocolatine : {e}")
    
    # Vérifie les déclencheurs
    for mot_cle, reponse in triggers_dict.items():
        if sans_accents(mot_cle) == texte:  # on utilise split pour éviter les sous-mots (ex: "ok" dans "poker")
            if random.random() < get_probas(update.effective_chat.id)[0]:
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reponse
                )
            return  # évite d’envoyer aussi une vidéo si un mot est détecté


    try:
        # Télécharge la liste des fichiers vidéo
        page = unquote(requests.get(dataServerAddress).text)
        lignes = page.split('<img src="/__ovh_icons/movie.gif" alt="[VID]"> ')[1:]
        video_names = [i.split('>')[0][9:-1] for i in lignes]

        meilleur_score = 0
        meilleures_videos = []
        for vname in video_names:
            nom_sans_extension = os.path.splitext(sans_accents(vname))[0] #sépare le nom de fichier de son extension (enlève .mp4 du dernier mot)
            mots_video = nom_sans_extension.split('_')
            #list(dict.fromkeys(mots)) --> supprime les doublons
            score = sum(1 for mot in list(dict.fromkeys(mots)) if (mot in mots_video and mot not in stop_words))

            if score >= 1:
                if score > meilleur_score:
                    # Nouvelle meilleure vidéo : on remplace la liste
                    meilleures_videos = [vname]
                    meilleur_score = score
                elif score == meilleur_score:
                    # Même score que le meilleur : on ajoute
                    meilleures_videos.append(vname)
                # Affichage de debug
                print(f"{vname} : {score} correspondances")

        if meilleures_videos:
            video_choisie = random.choice(meilleures_videos)
            video_url = dataServerAddress + video_choisie.replace(" ", "%20")
            if random.random() < get_probas(update.effective_chat.id)[1] + (0.05*(score-1) if get_probas(update.effective_chat.id)[1] > 0 else 0):
                await update.message.reply_video(video=video_url)

    except Exception as e:
        print(f"Erreur dans echo vidéo : {e}")

    # Sinon, ne répond rien si aucune vidéo trouvée