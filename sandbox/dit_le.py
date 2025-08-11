tamere = ["dimache","rot","ui","fshuibnsubndihitler","midi","gg"]
for word in tamere :
    dit_le = 0
    a_dire = ""
    for lettres in word :
        if dit_le >= 2 :
            a_dire += lettres
            dit_le += 1
        if lettres == "d" and dit_le == 0:
            dit_le = 1
        if lettres == "i" and dit_le == 1:
            dit_le = 2
    if dit_le > 2:
        print(a_dire)
