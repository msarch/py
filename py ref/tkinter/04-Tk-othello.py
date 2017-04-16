#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


from Tkinter import *
from random import randrange

def aide():
    msg = Toplevel()
    Message(msg, bg ="navy",fg ="ivory",width = 480, font ="Arial 12",
        text ="           * Règles du jeu *\n"\
        "Le plateau de jeu représente un damier de 64 cases, chaque joueur "\
        "dispose  de 32 jetons chacun, chaque face est noire d'un côté, "\
        "blanche de l'autre.\n"\
        "Vous prenez les jetons en les retournant du côté de votre couleur.\n"\
        "Au départ, 2 pions de chaque couleur sont disposés sur les 4 cases "\
        "centrales. A tour de rôle, chacun pose un jeton avec l'obligation "\
        "de retourner au moins un jeton adverse. Votre jeton doit être posé "\
        "de manière à entourer 1 ou plusieurs jetons adverses.\n"\
        "Un jeton peut prendre simultanément dans les direction horizontales, "\
        "veritcales et diagonales.\n"\
        "La partie se termine quand tous le jetons sont posés, ou si aucun "\
        "joueur ne peut plus jouer.\n"\
        "Le vainqueur est celui qui possède le plus de jetons de sa couleur "\
        "sur le plateau.\n"\
        " \n"\
        "Comment jouer :\n"\
        "Pour poser un pion, cliquez sur la cases de votre choix.\n"\
        "Si vous ne pouvez pas jouer, cliquez sur le bouton 'Passe'.\n"\
        "Si vous aimez la difficulté, cliquez sur le bouton 'Handicap' qui "\
        "offre à votre adversaire les 4 cases de coin.")\
        .pack(padx =10, pady =10)

def affichePion(lg,cl):
    x = (cl-1) * 60 + 30
    y = (lg-1) * 60 + 30
    can.selObject = can.find_closest(x, y)
    if tjeu[lg][cl] == 1:
        can.itemconfig(can.selObject,fill ="white", outline ="black")
    else:
        can.itemconfig(can.selObject,fill ="black", outline ="black")

def traceGrille():
    global tjeu
    for lg in range(1,9):
        for cl in range(1,9):
            if tjeu[lg][cl] > 0:
                affichePion(lg,cl)
    comptePions()

def initJeu():
    " Initialisation de l'état du jeu "
    global tjeu
    tjeu =[]
    for i in range(11):
        tjeu.append([9]*10)
    for y in range(1,9):
        for x in range(1,9):
            tjeu[y][x] = 0
    tjeu[4][4] = 1
    tjeu[4][5] = 2
    tjeu[5][4] = 2
    tjeu[5][5] = 1
    can.delete(ALL)
    # A la création de la grille de jeu on affiche sur le canvas 8x8 carrés.
    # Dans chaque carré on dessine un cercle figurant le pion; ce cercle est
    # de la même couleur que le fond, ce qui le rend invisible. Pour afficher
    # un pion, il suffit de modifier sa couleur.
    y = 1
    for lg in range(1,9):
        x = 1
        for cl in range(1,9):
            can.create_rectangle(x,y,x+59,y+59)
            can.create_oval(x+5,y+5,x+53,y+53, fill = "#009000",
                                    outline="#009000")
            x += 60
        y += 60
    traceGrille()

def initHandicap():
    " cases de coin occupées "
    tjeu[1][1] = 2
    tjeu[1][8] = 2
    tjeu[8][1] = 2
    tjeu[8][8] = 2

def nouveauJeu():
    initJeu()
    traceGrille()
    jr = randrange(2)+1
    if jr == 2:
        tourOrdi()

def handicap():
    initHandicap()
    traceGrille()

def passe():
    global npa
    mess.configure(text = ("Joueur passe"))
    npa += 1
    tourOrdi()

def comptePions():
    global blc,nor,rst
    blc,nor = 0,0
    for lg in range(1,9):
        for cl in range(1,9):
            if tjeu[lg][cl] == 1:
                blc += 1
            elif tjeu[lg][cl] == 2:
                nor += 1
    rst = 64 - blc - nor
    nbb.configure(text = ("Blancs : "+ str(blc)))
    nbn.configure(text = ("Noirs : "+ str(nor)))
    nbr.configure(text = ("Reste : "+ str(rst)))

def mouseClic(event):
    " Gestion du clic de la souris "
    global npa,jr
    ty, tx = int(event.y/59)+1, int(event.x/59)+1
    b = 0
    if tjeu[ty][tx] > 0:
        mess.configure(text = ("Coup non valide"))
    else:
        if tjeu[ty][tx+1] == 2:               # à droite
            nx = tx+1
            while tjeu[ty][nx] == 2:
                nx += 1
            if tjeu[ty][nx] == 1:
                b = 1
                nx = tx+1
                while tjeu[ty][nx] == 2:
                    tjeu[ty][nx] = 1
                    affichePion(ty,nx)
                    nx += 1
        if tjeu[ty+1][tx+1] == 2:           # à droite, en bas
            ny, nx = ty+1, tx+1
            while tjeu[ny][nx] == 2:
                ny += 1
                nx += 1
            if tjeu[ny][nx] == 1:
                b = 1
                ny, nx = ty+1, tx+1
                while tjeu[ny][nx] == 2:
                    tjeu[ny][nx] = 1
                    affichePion(ny,nx)
                    ny += 1
                    nx += 1
        if tjeu[ty+1][tx] == 2:             # en bas
            ny = ty+1
            while tjeu[ny][tx] == 2:
                ny += 1
            if tjeu[ny][tx] == 1:
                b = 1
                ny = ty+1
                while tjeu[ny][tx] == 2:
                    tjeu[ny][tx] = 1
                    affichePion(ny,tx)
                    ny += 1
        if tjeu[ty+1][tx-1] == 2:           # en bas, à gauche
            ny, nx = ty+1, tx-1
            while tjeu[ny][nx] == 2:
                ny += 1
                nx -= 1
            if tjeu[ny][nx] == 1:
                b = 1
                ny, nx = ty+1, tx-1
                while tjeu[ny][nx] == 2:
                    tjeu[ny][nx] = 1
                    affichePion(ny,nx)
                    ny += 1
                    nx -= 1
        if tjeu[ty][tx-1] == 2:             # à gauche
            nx = tx-1
            while tjeu[ty][nx] == 2:
                nx -= 1
            if tjeu[ty][nx] == 1:
                b = 1
                nx = tx-1
                while tjeu[ty][nx] == 2:
                    tjeu[ty][nx] = 1
                    affichePion(ty,nx)
                    nx -= 1
        if tjeu[ty-1][tx-1] == 2:           # à gauche, en haut
            ny, nx = ty-1, tx-1
            while tjeu[ny][nx] == 2:
                ny -= 1
                nx -= 1
            if tjeu[ny][nx] == 1:
                b = 1
                ny, nx = ty-1, tx-1
                while tjeu[ny][nx] == 2:
                    tjeu[ny][nx] = 1
                    affichePion(ny,nx)
                    ny -= 1
                    nx -= 1
        if tjeu[ty-1][tx] == 2:             # en haut
            ny = ty-1
            while tjeu[ny][tx] == 2:
                ny -= 1
            if tjeu[ny][tx] == 1:
                b = 1
                ny = ty-1
                while tjeu[ny][tx] == 2:
                    tjeu[ny][tx] = 1
                    affichePion(ny,tx)
                    ny -= 1
        if tjeu[ty-1][tx+1] == 2:           # en haut, à droite
            ny, nx = ty-1, tx+1
            while tjeu[ny][nx] == 2:
                ny -= 1
                nx += 1
            if tjeu[ny][nx] == 1:
                b = 1
                ny, nx = ty-1, tx+1
                while tjeu[ny][nx] == 2:
                    tjeu[ny][nx] = 1
                    affichePion(ny,nx)
                    ny -= 1
                    nx += 1
        if b == 0:
            mess.configure(text = ("Coup non valide"))
        else:
            tjeu[ty][tx] = 1
            affichePion(ty,tx)
            comptePions()
            f = testFin()
            if f == 1:
                finJeu()
            else:
                npa = 0
                tourOrdi()

def exploration():
    " Recherche d'un coup jouable par l'ordinateur "
    global texp,nbex
    texp = []
    nbex = 0
    for py in range(1,9):               # on parcoure le tableau de jeu
        for px in range(1,9):           # et on examine chaque case dans
            if tjeu[py][px] == 0:       # les huit directions si la case
                if tjeu[py][px+1] == 1: # est vide, bien entendu
                    x = px + 1
                    n = 0
                    while tjeu[py][x] == 1: # tant qu'il y a des pions adverses
                        n += 1              # nombre de pions
                        x += 1              # on avance d'une case
                    if n > 0 and tjeu[py][x] == 2: # pion ordi = limite
                        nbex += 1   # on renseigne la table d'évaluation :
                                    # sens, nbre de pions, valeur de la case,
                                    # et position de départ
                        tp = (0,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py+1][px+1] == 1:
                    x = px + 1
                    y = py + 1
                    n = 0
                    while tjeu[y][x] == 1:
                        n += 1
                        x += 1
                        y += 1
                    if n > 0 and tjeu[y][x] == 2:
                        nbex += 1
                        tp = (1,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py+1][px] == 1:
                    y = py + 1
                    n = 0
                    while tjeu[y][px] == 1:
                        n += 1
                        y += 1
                    if n > 0 and tjeu[y][px] == 2:
                        nbex += 1
                        tp = (2,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py+1][px-1] == 1:
                    x = px - 1
                    y = py + 1
                    n = 0
                    while tjeu[y][x] == 1:
                        n += 1
                        x -= 1
                        y += 1
                    if n > 0 and tjeu[y][x] == 2:
                        nbex += 1
                        tp = (3,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py][px-1] == 1:
                    x = px - 1
                    n = 0
                    while tjeu[py][x] == 1:
                        n += 1
                        x -= 1
                    if n > 0 and tjeu[py][x] == 2:
                        nbex += 1
                        tp = (4,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py-1][px-1] == 1:
                    x = px - 1
                    y = py - 1
                    n = 0
                    while tjeu[y][x] == 1:
                        n += 1
                        x -= 1
                        y -= 1
                    if n > 0 and tjeu[y][x] == 2:
                        nbex += 1
                        tp = (5,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py-1][px] == 1:
                    y = py - 1
                    n = 0
                    while tjeu[y][px] == 1:
                        n += 1
                        y -= 1
                    if n > 0 and tjeu[y][px] == 2:
                        nbex += 1
                        tp = (6,n,tval[py][px],px,py)
                        texp.append(tp)
                if tjeu[py-1][px+1] == 1:
                    x = px + 1
                    y = py - 1
                    n = 0
                    while tjeu[y][x] == 1:
                        n += 1
                        x += 1
                        y -= 1
                    if n > 0 and tjeu[y][x] == 2:
                        nbex += 1
                        tp = (7,n,tval[py][px],px,py)
                        texp.append(tp)

def ordiJoue():
    global npa, tjeu
    npa = 0
    p, n, v = 0, 0, -100
    for i in range(nbex):   # on explore la table d'évaluation
        exp = texp[i]
        if exp[2] > v:      # pour trouver la meilleure valeur
            v = exp[2]
            p = exp[1]
            n = i
        elif exp[2] == v:   # en cas d'égalité, on fait intervenir
            if exp[1] > p:  # le nombre de pions
                p = exp[1]
                n = i
    exp = texp[n]
    tx = exp[3]
    ty = exp[4]
    for i in range(nbex):   # on explore une seconde fois la table
        exp = texp[i]       # d'évluation pour trouver tous les coups
        x1,y1 = exp[3],exp[4]   # jouables pour une même case
        if x1 == tx and y1 == ty:
            tjeu[y1][x1] = 1
            s = exp[0]
            if s == 0:      # on affiche les pions en fonction du sens
                x = x1
                while tjeu[y1][x] == 1:
                    tjeu[y1][x] = 2
                    affichePion(y1,x)
                    x += 1
            elif s == 1:
                y = y1
                x = x1
                while tjeu[y][x] == 1:
                    tjeu[y][x] = 2
                    affichePion(y,x)
                    y += 1
                    x += 1
            elif s == 2:
                y = y1
                while tjeu[y][x1] == 1:
                    tjeu[y][x1] = 2
                    affichePion(y,x1)
                    y += 1
            elif s == 3:
                x = x1
                y = y1
                while tjeu[y][x] == 1:
                    tjeu[y][x] = 2
                    affichePion(y,x)
                    x -= 1
                    y += 1
            elif s == 4:
                x = x1
                while tjeu[y1][x] == 1:
                    tjeu[y1][x] = 2
                    affichePion(y1,x)
                    x -= 1
            elif s == 5:
                y = y1
                x = x1
                while tjeu[y][x] == 1:
                    tjeu[y][x] = 2
                    affichePion(y,x)
                    y -= 1
                    x -= 1
            elif s == 6:
                y = y1
                while tjeu[y][x1] == 1:
                    tjeu[y][x1] = 2
                    affichePion(y,x1)
                    y -= 1
            elif s == 7:
                y = y1
                x = x1
                while tjeu[y][x] == 1:
                    tjeu[y][x] = 2
                    affichePion(y,x)
                    y -= 1
                    x += 1
    comptePions()
    f = testFin()
    if f == 1:
        finJeu()
    else:
        mess.configure(text = ("A vous de jouer..."))

def testFin():
    fn = 0
    if rst == 0 or blc == 0 or nor == 0 or npa == 2:
        fn = 1
    return fn

def tourOrdi():
    global npa
    f = testFin()
    if f == 0:
        mess.configure(text = ("Je réféchis..."))
        exploration()
        if nbex == 0:       # aucun coup jouable...
            mess.configure(text = ("Je passe mon tour..."))
            npa += 1
            mess.configure(text = ("A vous de jouer..."))
        else:
            ordiJoue()
    else:
        finJeu()

def finJeu():
    if blc > nor:
        ms = "Bravo, vous avez gagné!"
        bk = "yellow"
        fc = "navy"
    elif nor > blc:
        ms = "Désolé, vous avez perdu!"
        bk = "red"
        fc = "yellow"
    else:
        ms = "Match nul!!!"
        bk = "grey"
        fc = "white"
    msg = Toplevel()
    msg.configure(background = "green")
    Message(msg, bg =bk,fg =fc,width = 200, font ="Arial 12",
        text = ms).pack(padx =10, pady =10)

#----------------------------------------------------------------------------
fen = Tk()
fen.title('OTHELLO')
fen.configure(background = "green")

fr1 =Frame(fen,bd =2, relief=SOLID, bg = "green")
b1 = Button(fr1,text="Nouvelle partie",font="Arial 12",width =15,
                    command = nouveauJeu)
b1.pack(side = LEFT, padx =10, pady = 5)
b2 = Button(fr1,text="Handicap",font="Arial 12",width =15,
                    command = handicap)
b2.pack(side = LEFT, padx =10, pady = 5)
b3 = Button(fr1,text="Aide",font="Arial 12",width =15, command = aide)
b3.pack(side = LEFT, padx =10, pady = 5)
fr1.pack()

can = Canvas(fen, bg="#009000", width=476, height=476, bd=2, relief=SOLID)
can.bind("<Button-1>", mouseClic)
can.pack(padx=5, pady=5)

fr2 =Frame(fen,bd =2, relief=SOLID, bg = "green")
mess = Label(fr2, width=40, bg = "white", font="Arial 12")
mess.pack(side=LEFT, padx=5, pady=5)
bp = Button(fr2,text="Passe",font="Arial 12",width =11,
                   command = passe)
bp.pack(side=RIGHT,padx=5,pady=5)
fr2.pack()

fr3 =Frame(fen,bd =2, relief=SOLID, bg = "green")
nbb = Label(fr3, text="Blancs : 2", width = 16, bg = "white", font="Arial 12")
nbb.pack(side=LEFT, padx=6, pady=5)
nbn = Label(fr3, text="Noirs : 2", width = 16, bg = "white",font="Arial 12")
nbn .pack(side=LEFT, padx=6, pady=5)
nbr = Label(fr3, text="Reste : 60", width = 17, bg = "white",font="Arial 12")
nbr.pack(side=LEFT, padx=6, pady=5)
fr3.pack()

tval =[[0,0,0,0,0,0,0,0,0,0],
       [0,1000,100,700,400,400,700,100,1000,0],       # valeur des cases
       [0,100,0,310,310,310,310,0,100,0],
       [0,700,310,350,325,325,350,310,700,0],
       [0,400,310,325,500,500,325,310,400,0],
       [0,400,310,325,500,500,325,310,400,0],
       [0,700,310,350,325,325,350,310,700,0],
       [0,100,0,310,310,310,310,0,100,0],
       [0,1000,100,700,400,400,700,100,1000,0],
       [0,0,0,0,0,0,0,0,0,0]]
texp =[]    # table d'evaluation des cases
nbex = 0    # nbre de cases jouables
tjeu =[]    # tableau du jeu
blc,nor,rst = 2,2,60  # nbre de pions blancs, noirs et restant à jouer
jr,npa = 1,0

fen.mainloop()

