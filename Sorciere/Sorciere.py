# -*- coding: utf-8 -*-

from tkinter import PhotoImage
from turtle import *
from random import randint

squarelength = 100  # Nombre de pixels des petits carrés des grilles

screen = Screen()
witchimage = PhotoImage(file="witch.gif").subsample(10, 10)
screen.addshape("witch", Shape("image", witchimage))
hutimage = PhotoImage(file="hut.gif").subsample(8, 8)
screen.addshape("hut", Shape("image", hutimage))

witch = Turtle(shape="witch")  # La tortue de la sorcière, dessine sa traînée
witch.speed(0); witch.pu()
hut = Turtle(shape="hut")  # La tortue de la cabane (immobile)
hut.speed(5); hut.pu()
gridt = Turtle(visible=False)  # La tortue qui dessine la grille
gridt.speed(0); gridt.pu()
hideturtle(); penup(); goto(0, -250)  # La tortue qui écrit les messages

grids = [(3,3,0,2,2,2), (4,3,0,0,1,2), (3,4,2,2,0,1), (5,3,4,2,2,0), (3,5,2,2,0,4), (4,4,1,2,3,3), (6,3,1,1,5,2), (5,4,2,0,3,0), (4,5,2,0,3,4), (6,4,4,1,1,3), (5,5,1,1,3,3), (6,5,5,1,5,4)]  # Cf class Grid pour la signification de ces nombres

class Grid:

    """
    Une grille est un objet défini par ses dimensions, la position de la
    sorcière et la position de sa maison, possède une représentation graphique
    qui est tracée lors de __init__(), qui déplace les tortues witch et hut aux
    endroits correspondant à l'identité de la grille et initialise une matrice
    contenant les positions déjà visitées par la tortue de la sorcière
    """

    def __init__(self, args):
        global gridt
        x, y, xdeb, ydeb, xfin, yfin = args
        self.x, self.y = x, y  # Dimensions de la grille
        self.witchx, self.witchy = xdeb, ydeb  # Position de la sorcière (commence à 0)
        self.goalx, self.goaly = xfin, yfin  # Position de la cabane
        gridt.clear(); witch.clear()
        top = y * squarelength//2  # Ordonnée en pixels du plus haut point de la grille
        right = x * squarelength//2
        for col in range(-right, right+1, squarelength):
            gridt.pu(); gridt.goto(col, -top)
            gridt.pd(); gridt.goto(col, top)
        for row in range(-top, top+1, squarelength):
            gridt.pu(); gridt.goto(-right, row)
            gridt.pd(); gridt.goto(right, row)
        witch.goto((2*xdeb+1-x) * squarelength//2, (2*ydeb+1-y) * squarelength//2)
        hut.goto((2*xfin+1-x) * squarelength//2, (2*yfin+1-y) * squarelength//2)
        self.matrix = [[True]*y for _ in range(x)]
        self.matrix[xdeb][ydeb] = False  # False signifie "déjà visité"

def play(grid_number):
    grid = Grid(grids[grid_number])  # Initialiser et dessiner la nouvelle grille
    events = []  # Garder les mouvements en mémoire pour undow()

    def nextgame(new=grid_number+1):
        for ch in chs: onkey(None, ch)
        clear()  # Effacer l'éventuel message de félicitations
        play(new % len(grids))

    def fly(x, y, xx, yy):  # Bouger de (x,y) à (xx,yy) en laissant une traînée
        for i in range(1, 6):
            witch.dot(5)
            witch.goto(((5-i)*x + i*xx)//5, ((5-i)*y + i*yy)//5)

    def move(dx, dy, end=False):  # Avancer dans la direction souhaitée si autorisé
        if grid.witchx+dx == grid.goalx and grid.witchy+dy == grid.goaly:
            if len(events) < grid.x*grid.y - 2: return  # Pas encore tout visité
            else: end = True  # Tout visité : entrée dans la cabane acceptée
        for ch in chs: onkey(None, ch)
        if grid.matrix[grid.witchx+dx][grid.witchy+dy]:  # Si pas encore allé là-bas...
            events.append((dx, dy))
            grid.matrix[grid.witchx+dx][grid.witchy+dy] = False
            x, y = witch.pos()
            fly(x, y, x + squarelength*dx, y + squarelength*dy)  # ...aller là-bas
            grid.witchx += dx; grid.witchy += dy
        if end:  # Si arrivé après avoir tout visité, c'est gagné
            for ch in chs: onkey(nextgame, ch)
            write("BRAVO ! La sorcière a pu\n rejoindre sa cabane !", align="center", font=("Courier", 15, "bold"))
        else:
            for ch in chs: onkey(action[ch], ch)

    def left():
        if grid.witchx > 0: move(-1, 0)
    def right():
        if grid.witchx < grid.x-1: move(1, 0)
    def up():
        if grid.witchy < grid.y-1: move(0, 1)
    def down():
        if grid.witchy > 0: move(0, -1)

    def wundo():
        for ch in chs: onkey(None, ch)
        if events:
            grid.matrix[grid.witchx][grid.witchy] = True
            dir = events.pop()
            grid.witchx -= dir[0]; grid.witchy -= dir[1]
            for i in range(10): witch.undo()  # La sorcière fait 10 actions dans fly()
        for ch in chs: onkey(action[ch], ch)

    action = {"Return": None, "s": nextgame, "r": lambda:nextgame(0), "Left": left, "Right": right, "Up": up, "Down": down, "BackSpace": wundo}
    chs = action.keys()
    for ch in chs: onkey(action[ch], ch)
    listen()

if __name__ == "__main__":
    play(0)
    mainloop()
