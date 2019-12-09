# -*- coding: utf-8 -*-

from turtle import *
from time import sleep

code1 = "F2DA72"  # Si tour à n étage réussie, donner les n 1ers caractères du code
code2 = "C21916"  # idem si tour à n étages réussie parfaitement
above_screen = 700
maxnum = 6

class Disc(Turtle):

    """
    Un disque est une tortue rectangulaire de couleur dépendant de sa taille et  
    de vitesse moyenne. Elle est initialisée hors de l'écran.
    """

    def __init__(self, n):

        """
        Un disque est défini par n, sa taille.
        """

        Turtle.__init__(self, shape="square", visible=False)
        self.penup()
        self.shapesize(1.5, n*1.5, 2)  # Verti, Horiz, Bord
        self.size = n
        self.fillcolor(n/maxnum, 0, 1-n/maxnum)  # RVB
        self.speed(0)
        self.goto(0, above_screen)
        self.speed(5)
        self.showturtle()

class Tower(list):

    """
    Une tour est une liste destinée à contenir des disques
    """

    def __init__(self, x):

        """
        Une tour est définie par une abscisse
        """

        self.x = x

    def push(self, d):

        """
        Déplacer hozirontalement le disque vers la nouvelle tour puis 
        descendre le disque à la bonne hauteur
        """

        d.setx(self.x)
        d.sety(-100+34*len(self))
        self.append(d)

    def pop(self):

        """
        Prendre le sommet de la tour
        """

        d = list.pop(self)
        d.sety(200)
        return d

    def empty(self):

        """
        Vider totalement la tour pour réinitialiser le jeu
        """

        while self:
            d = list.pop(self)
            d.sety(above_screen)

def startgame():

    """
    (Re)commencer le jeu en demandant un (nouveau) nombre d'étages. 
    """

    global state, c, events, n
    state, c = 0, 0  # state : 1 si un disque est levé, 0 sinon. c : compteur de coups
    events = []  # Mémoire des actions, pour pouvoir faire les undo
    n = int(Screen().numinput("Nombre d'étages", "Choisis un nombre entre 3 et {}".format(maxnum), minval=3, maxval=maxnum))
    for i in range(n, 0, -1): t1.push(discs[i])
    play()

def play():

    """
    Fonction centrale pour le jeu. Définit les commandes
    "0": reinitialize
    "1": left, "2": mid, "3": right
    "BackSpace": undo
    "space": None
    "$": autoplay
    """

    global state, c, events, n

    def reinitialize():
        
        """
        Enlever les disques avant d'appeler startgame()
        """
        
        if state==1: undo()
        clear()
        for i in range(1, maxnum+1): discs[i].speed(0)
        for ti in (t1, t2, t3): ti.empty()
        for i in range(1, maxnum+1): discs[i].speed(5)
        startgame()

    def hanoi(n, from_, with_, to_):

        """
        Montre la solution optimale du jeu à n étages où t1,t2,t3=from,with,to 
        """

        if n:
            hanoi(n-1, from_, to_, with_)
            to_.push(from_.pop())
            hanoi(n-1, with_, from_, to_)

    def autoplay():

        """
        Montre la solution optimale du jeu au nombre d'étages sélectionné avant 
        de remettre le joueur en position initiale.
        """
        
        global state, c, events, n
        if state == 1: undo()
        for ch in chs: onkey(None, ch)
        clear()
        for i in range(1, maxnum+1): discs[i].speed((n+6)//2)
        for ti in (t1, t2, t3): ti.empty()
        for i in range(n, 0, -1): t1.push(discs[i])
        hanoi(n, t1, t2, t3)
        sleep(2)
        for ti in (t1, t2, t3): ti.empty()
        for i in range(n, 0, -1): t1.push(discs[i])
        for i in range(1, maxnum+1): discs[i].speed(5)
        state, c = 0, 0
        events = []
        for ch in chs: onkey(action[ch], ch)

    def move(ti, i):

        """
        Mouvement sur la tour ti de numéro i. 
        Si state vaut 0 (rien n'est enlevé), on enlève si possible le sommet de 
        la tout i. Si state vaut 1 (un étage est en attente d'être posé), on 
        regarde si on a le droit de poser cette étage, si oui on le pose, sinon 
        on affiche un message d'erreur. Dans le cas d'un étage posé, le 
        compteur c n'est incrémenté que si l'étage venait d'une autre tour.
        """

        global state, t, c 
        for ch in chs: onkey(None, ch)
        if state == 0:
            if ti:
                t = ti.pop()
                state = 1
                events.append(i)
        elif len(ti) == 0 or t.size < ti[-1].size:
            if i != events[-1]:
                c += 1
                events.append(i)
            else:
                _ = events.pop()
            ti.push(t)
            state = 0
            clear()
            write(str(c), align="center", font=("Courier", 16, "bold"))
        else:
            clear()
            write("Mouvement interdit ! Un étage ne peut\npas être posé sur un autre plus petit.", align="center", font=("Courier", 16, "bold"))
        for ch in chs: onkey(action[ch], ch)

    def left():
        move(t1, 1)
    def mid():
        move(t2, 2)
    def right():
        move(t3, 3)
        if len(t3) == n:
            clear(); goto(0, -300)
            write("Gagné ! Le code de ce jeu est {}.\nAppuie sur 0 dès que c'est noté !\nTu as réussi en {} étapes. {}".format(code1[:n], c, "Bravo !!\nLe code bonus est {}.".format(code2[:n]) if c == 2**n-1 else "Gagne en\nseulement {} étapes pour un 2e code.".format(2**n-1)), align="center", font=("Courier", 16, "bold")); goto(0, -250)

    def undo():

        """
        Annuler le dernier coup. S'il s'agit d'une levée, on repose simplement. 
        """

        for ch in chs: onkey(None, ch)
        global c
        if c and len(events)&1==0:
            clear()
            to_ = events.pop()
            from_ = events.pop()
            eval("t"+str(from_)).push(eval("t"+str(to_)).pop())
            c -= 1
            write(str(c), align="center", font=("Courier", 16, "bold"))
        elif len(events)&1: move(eval("t"+str(events[-1])), events[-1])
        for ch in chs: onkey(action[ch], ch)

    action = {"0": reinitialize, "1": left, "2": mid, "3": right, "BackSpace": undo, "space": None, "$": autoplay}
    chs = action.keys()
    clear(); goto(0, -300)
    write("Appuyer sur :\n1, 2 ou 3 pour prendre ou poser le dernier\nétage de la pile 1, 2 ou 3\nRetour arrière pour annuler le dernier coup\n0 pour réinitialiser le jeu", align="center", font=("Courier", 16, "bold")); goto(0, -250)
    for ch in chs: onkey(action[ch], ch)
    listen()

try: hideturtle(); penup(); goto(0, -250)   #  La tortue qui écrit les messages
except: hideturtle(); penup(); goto(0, -250)
t1, t2, t3 = Tower(-250), Tower(0), Tower(250)  # Créer les 3 tours
base = Turtle(visible=False)  # La tortue qui affiche la base
base.speed(0)
for i in (-250, 0, 250):  # Afficher la base des tours
    base.pu(); base.goto(i-100, -117); base.pd(); base.goto(i+100, -117)
discs = {i: Disc(i) for i in range(1, maxnum+1)}  # Préparer 6 disques
for i in range(1, maxnum+1): discs[i].speed(5)
startgame()  # Lancer le jeu
mainloop()
