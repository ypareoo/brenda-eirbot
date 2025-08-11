tamere = ["dimache","rot","ui","fshuibnsubndihitler","midi","gg","guillotinee"]
for word in tamere :
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
            dit_le = 0
    if dit_le > 3:
        print("c'est pain au "+a_dire[::-1]+" pas "+word)
