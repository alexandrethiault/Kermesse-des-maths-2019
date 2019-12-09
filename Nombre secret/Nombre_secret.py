# -*- coding: utf-8 -*-

from tkinter import *
from random import *

def restart(): # Fonction de lancement d'une nouvelle partie
    global nombre_a_trouver, nb_essais
    nombre_a_trouver = randint(0, 1000)
    nb_essais = 11
    nb_essais_str.set(str(nb_essais))
    comparaison.set("")
    
def verif(): # Fonction de vérification du test rentré dans le cadre
    global nombre_a_trouver, nb_essais
    try:
        test = int(proposition.get()) 
        if nb_essais > 0:
            if test == nombre_a_trouver :
                comparaison.set(" Bravo, vous avez trouvé !")
                comparaison_txt.configure(foreground="green")
            else:
                comparaison.set(" Proposition trop " + ("petite" if test < nombre_a_trouver else "grande"))
                comparaison_txt.configure(foreground="#00F" if test < nombre_a_trouver else "#808")
                nb_essais -= 1
                nb_essais_str.set(str(nb_essais))
        else:
            comparaison.set(" Nombre de tentatives max dépassé")
            comparaison_txt.configure(foreground="#00F")
    except:
        comparaison.set(" Il faut choisir un entier")
        comparaison_txt.configure(foreground="#F00")

# Création de la fenêtre avec son titre, sa couleur et ses dimensions
fenetre = Tk()
fenetre.title(" Le nombre à deviner")
fenetre.configure(width=500, height=250)
fenetre.resizable(width=FALSE, height=FALSE)

# Création des labels fixes et de l'espace de saisie de la proposition
proposition_txt = Label(fenetre, text=' Proposition :')
proposition = Entry(fenetre, width=5)
nb_essais_txt = Label(fenetre,text=" Nombre de tests restants :")

# Création des labels qui donnent la comparaison et le nombre de tests restants
comparaison = StringVar()
comparaison_txt = Label(fenetre, textvariable=comparaison)
nb_essais_str = StringVar()
nb_essais_num = Label(fenetre, textvariable=nb_essais_str)

# Création des boutons test (appel à verif()) et nouvelle partie (restart())
verif_btn = Button(fenetre, text=" Tester ce nombre ", command=verif)
restart_btn = Button(fenetre, text="   Nouvelle partie   ", bg='grey', command=restart)

# Agencement relatif des éléments définis
proposition_txt.grid(row=1, column=1, sticky=W)
proposition.grid(row=1, column=2, sticky=W)
verif_btn.grid(row=1, column=3, sticky=W)
comparaison_txt.grid(row=2, column=1, sticky=W)
nb_essais_txt.grid(row=3, column=1, sticky=W)
nb_essais_num.grid(row=3, column=2, sticky=W)
restart_btn.grid(row=3, column=3, sticky=W)

restart()
fenetre.mainloop()
