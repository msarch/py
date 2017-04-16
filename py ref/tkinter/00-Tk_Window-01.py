## ================================================================
## TkWin-01, simple tkinter window
## (Tkinter, button, window, GUI)
## ================================================================


# -*- coding: iso-8859-15 -*- 

from Tkinter import *
# creation d'une fenetre
fen1 = Tk()
fen1.title('prog1bis')

# creation d'une zone de saisie
saisie=Entry(fen1)
saisie.configure(fg='red')
saisie.pack()

# creation d'une zone de dessin
can1 = Canvas(fen1, bg='grey', height=190, width=250, borderwidth =10)
can1.pack(side=LEFT)

# creation d'une zone de texte
tex1 = Label(fen1, text='Label avec texte accentuÈ!', fg='red')
tex1.pack(side=TOP)

# creation d'un bouton
bou1 = Button(fen1, text='Button Quitter', command = fen1.destroy)
bou1.pack(side=BOTTOM)

# attente des evenements
fen1.mainloop()

-----