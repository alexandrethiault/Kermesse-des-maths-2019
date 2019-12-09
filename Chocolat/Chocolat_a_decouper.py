# -*- coding: utf-8 -*-

from turtle import *

sizex, sizey = 5.0, 3.5 # Taille des carrés de chocolat pour "shapesize"
col1, col2 = (160./256, 82./256, 45./256), (139./256, 69./256, 19./256)
realy, realx = sizey*20, sizex*20 # Taille des carrés en pixels
h, v = 6, 4 # Nombre de carrés horizontalement et verticalement
_pxmove = [0]+[5*2**(i-1) for i in range(1, h)] # Paramètres utiles à spread_out()

class Square(Turtle):

    """
    Un carré de chocolat est une tortue au début invisible, qui n'écrit pas, 
    en forme de carré déformé, colorée, rapide.
    """

    def __init__(self, x, y, N=True, W=True, S=True, E=True):

        """
        x, y sont les coordonnées pixel du centre du carré
        N, W, S et E sont les bolléens donnant si oui ou non le carré possède 
        un voisin attaché à lui du côté concerné.
        """

        Turtle.__init__(self, shape="square", visible=False)
        self.penup()
        self.shapesize(sizey, sizex, 5)
        self.color(col1, col2) # Couleur des carrés (intérieur, bord)
        self.speed(0)
        self.goto(x, y)
        self.showturtle()
        self.N, self.W, self.S, self.E = N, W, S, E
    def x(self): return self.pos()[0]
    def y(self): return self.pos()[1]
    def setNWSE(self, N, W, S, E): self.N, self.W, self.S, self.E = N, W, S, E

screen = Screen()
try: hideturtle(); penup(); goto(0, -250) # Tortue pour les messages
except: hideturtle(); penup(); goto(0, -250) # 
yertle = Turtle(shape="turtle", visible=False) # Tortue pour les prédécoupes jaues
yertle.speed(0); yertle.pu(); yertle.pencolor("yellow"); yertle.pensize(4)
squares = [[Square(realx*(x-(h-1.)/2), realy*(y-(v-1.)/2)) for y in range(v)] for x in range(h)]

def onmove(self, fun, add=None):

    """
    Analogue de onclick pour le mouvement de la souris. Si fun est None, 
    désattache la fonction attachée au mouvement de la souris
    """

    if fun is None:
        self.cv.unbind('<Motion>')
    else:
        def eventfun(event): fun(self.cv.canvasx(event.x)/self.xscale,\
                                -self.cv.canvasy(event.y)/self.yscale)
        self.cv.bind('<Motion>', eventfun, add)

def restartgame(xcor=None, ycor=None):

    """
    Les arguments sont parfaitement inutiles
    Réinisialise les positions d'origine des carrés et leurs voisins attachés
    """

    screen.onclick(None)
    screen.onclick(None, 3)
    onmove(screen, None)
    clear()
    for x in range(h):
        for y in range(v):
            squares[x][y].goto(realx*(x-(h-1.)/2), realy*(y-(v-1.)/2))
            squares[x][y].setNWSE(y!=v-1., x!=0., y!=0., x!=h-1.)
    play()

def play():
    global yertle, c, lit
    c = 0
    lit = (None,)*3 #sert à limiter les clignotements de la prédécoupe

    def info_closest(xcor, ycor):

        """
        Donne le carré le plus proche de la souris à chaque fois qu'elle bouge, 
        ainsi que la direction de découpe dans laquelle la souris penche, à 
        condition qu'une découpe puisse effectivement être faite à cet endroit. 
        Par exemple, si la souris est plutôt en bas du carré (1,2), on renvoie 
        1, 2, "S"
        """

        for x in range(h):
            for y in range(v):
                dx, dy = xcor-squares[x][y].x(), ycor-squares[x][y].y()
                if abs(dx) <= realx*0.5 and abs(dy) <= realy*0.5:
                    if dx*realy + dy*realx < 0:
                        if dx*realy < dy*realx:
                            if squares[x][y].W and dx < -2: return x, y, "W"
                        else:
                            if squares[x][y].S and dy < -2: return x, y, "S"
                    else:
                        if dx*realy < dy*realx:
                            if squares[x][y].N and dy > 2: return x, y, "N"
                        else:
                            if squares[x][y].E and dx > 2: return x, y, "E"

    def light_closest(xcor, ycor):

        """
        Fait tracer à yertle la prédécoupe si une découpe peut effectivement 
        être faite à cet endroit, en gardant en mémoire la dernière prédécoupe 
        dans la variable lit pour limiter les clignotements et en cas de 
        changement, effacer la dernière prédécoupe.
        Contient quelques bugs dus à la simumtanéité de certains événements : 
        j'ai fait ce que j'ai pu mais si la fonction cut() est utilisée à un 
        moment précis pendant les prochain appel à light_closest(), une 
        prédécoupe diagonale peut être tracée. Elle ne reflète pas une action
        potentielle de cut(), qui ne fait que des découpes selon les arêtes.
        """

        global lit
        try: 
            x, y, dir = info_closest(xcor, ycor)
            if (x, y, dir) == lit: return
            else: lit = (x,y,dir)
        except: # Si un clic ne couperait rien, il n'y a rien à tracer 
            lit = (None,)*3
            return yertle.clear()
        if dir in "EW":
            highest, lowest = y, y
            while squares[x][highest].N: highest += 1
            while squares[x][lowest].S: lowest -= 1
            balance = realx/2. if dir == "E" else -realx/2.
            yertle.goto(squares[x][lowest].x()+balance, squares[x][lowest].y()-realy/2.)
            if squares[x][highest].x()+balance == yertle.pos()[0]:
                yertle.pd(); yertle.clear()
                yertle.goto(squares[x][highest].x()+balance, squares[x][highest].y()+realy/2.)
                yertle.pu()
        else:
            highest, lowest = x, x
            while squares[highest][y].E: highest += 1
            while squares[lowest][y].W: lowest -= 1
            balance = realy/2. if dir == "N" else -realy/2.
            yertle.goto(squares[lowest][y].x()-realx/2., squares[lowest][y].y()+balance)
            if squares[highest][y].y()+balance == yertle.pos()[1]:
                yertle.pd(); yertle.clear()
                yertle.goto(squares[highest][y].x()+realx/2., squares[highest][y].y()+balance)
                yertle.pu()

    def bound_to(x, y, cutdir):

        """
        Donne les numéros des carrés qui devront être déplacés dans UN sens par 
        la découpe. Il faut donc l'appeler deux fois pour connaître tous les 
        carrés concernés par une découpe.
        """

        square = squares[x][y]
        curx, cury = x, y
        while squares[curx][cury].S: cury -= 1
        while squares[curx][cury].W: curx -= 1
        lowest = (curx, cury)
        curx, cury = x, y
        while squares[curx][cury].N: cury += 1
        while squares[curx][cury].E: curx += 1
        highest = (curx, cury)
        return [[(x, y) for y in range(lowest[1], highest[1]+1)]\
                        for x in range(lowest[0], highest[0]+1)]

    def spread_out(x0, y0, dir):

        """
        Connaissant les carrés à déplacer dans la direction dir avec un appel à 
        bound_to(), déplace exactement ces carrés dans cette direction sur une 
        distance choisie de façon à empêcher les recouvrements entre les carrés 
        déplacés et d'autres carrés non concernés par la découpe. 
        """

        to_move = bound_to(x0, y0, dir)
        yertle.clear()
        nx = len(to_move)
        ny = len(to_move[0])
        if dir=="N":
            for l in to_move:
                for x, y in l: squares[x][y].sety(squares[x][y].y()-_pxmove[ny])
        elif dir=="E":
            for l in to_move:
                for x, y in l: squares[x][y].setx(squares[x][y].x()-_pxmove[nx])
        elif dir=="S":
            for l in to_move:
                for x, y in l: squares[x][y].sety(squares[x][y].y()+_pxmove[ny])
        elif dir=="W":
            for l in to_move:
                for x, y in l: squares[x][y].setx(squares[x][y].x()+_pxmove[nx])

    def cut(xcor, ycor):

        """
        Fonction principale de découpage. Fait appel à info_closest() pour 
        connaître la découpe en fonction de (xcor, ycor), les coordonnées pixel
        de la souris, puis donne cette information à la fonction spread_out() 
        pour effectuer la découpe. Actualise aussi les informations sur les 
        voisins encore attachés de chaque carré concerné.
        """

        global c
        screen.onclick(None)
        screen.onclick(None, 3)
        onmove(screen, None)
        try:
            x, y, dir = info_closest(xcor, ycor)
            if dir == "S":
                dir = "N"
                y -= 1
            elif dir == "W":
                dir = "E"
                x -= 1
            if dir == "N":
                curx=x
                while squares[curx][y].W:
                    curx -= 1
                squares[curx][y].N = False
                squares[curx][y+1].S = False
                while squares[curx][y].E:
                    curx += 1
                    squares[curx][y].N = False
                    squares[curx][y+1].S = False
                spread_out(x, y+1, "S")
            elif dir == "E":
                cury=y
                while squares[x][cury].S:
                    cury -= 1
                squares[x][cury].E = False
                squares[x+1][cury].W = False
                while squares[x][cury].N:
                    cury += 1
                    squares[x][cury].E = False
                    squares[x+1][cury].W = False
                spread_out(x+1, y, "W")
            spread_out(x, y, dir) # "N" ou "E"
            c += 1
            clear()
            write(("Faîtes un clic droit pour recommencer\n"+" "*30 if c == v*h - 1 else "")+str(c), align="center", font=("Helvetica", 16, "bold"))
        except: pass
        screen.onclick(cut)
        screen.onclick(restartgame, 3)
        onmove(screen, move_handler)

    def move_handler(x, y):

        """
        Sert à dire d'utiliser light_closest à chaque mouvement de la souris, 
        mais ne pas lancer le prochain appel tant que le précédent n'a pas fini.
        """

        onmove(screen, None)
        light_closest(x, y)
        onmove(screen, move_handler)

    onmove(screen, move_handler)
    screen.onclick(cut)
    screen.onclick(restartgame, 3)
    listen()

restartgame()
mainloop()
