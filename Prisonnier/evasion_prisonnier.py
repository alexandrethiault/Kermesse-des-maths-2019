# -*- coding: utf-8 -*-

from turtle import *
from math import sin, cos, pi
from random import choice, random
from time import time
from tkinter import * # En cas d'erreur d'import, mettre un t majuscule

code = "236524"
root = Tk()
radius = root.winfo_screenheight()*0.38 #typiquement (720 ou 768) * 0.38
root.destroy()
step_length = radius/4
latest = [0]*3 #droite/gauche (1/-1), date, angle de la dernière rotation

names = ["le génie de la cellule", "le manipulateur espiègle", "le démon du prisonnier", "l'esprit maléfique"]
invert = ["d'inverser le trajet.", "de retourner la trajectoire.", "de lui faire faire demi-tour.", "de prolonger son malheur..."]
crime = ["braqué une banque !", "tué quelqu'un !", "écrasé un piéton !", "triché à un jeu de la kermesse !", "volé un paquet de chips !", "téléchargé illégalement une musique des Beatles !", "été possédé, c'est pas pour rien !", "fouetté des chatons"]*10 + ["pris la tirelire de son frère !", "tué une araignée !", "triché à UNO !", "insinué que j'étais moche !", "volé les bonbons de sa soeur !"]
reason = ["Dans sa grâce infinie", "De bonne humeur", "Se moquant du prisonnier", "Comme c'est son anniversaire", "Pour une fois", "Une dernière fois", "Désintéressé"]
accept = ["de laisser faire le prisonnier.", "de ne pas gêner le prisonnier.", "d'accepter le trajet du prisonnier.", "de faire croire au prisonnier qu'il s'en sortirait."]

def draw_circle(t, x0, y0, radius, line="-"):
    t.speed(0)
    if line == "-": t.pu(); t.goto(x0, y0-radius); t.pd(); t.circle(radius); t.pu()
    elif line == "--":
        t.pu(); t.goto(0, -radius)
        for i in range(20):
            t.pd(); t.circle(radius, extent=360./20/4)
            t.pu(); t.circle(radius, extent=360./20/4*3)

def turnr():
    global latest
    angle = 5
    if latest[0] > 0 and time()-latest[1] < 0.5 and angle < 20: angle = latest[2]+5
    t.right(angle)
    latest = [1, time(), angle]

def turnl():
    global latest
    angle = 5
    if latest[0] < 0 and time()-latest[1] < 0.5 and angle < 20: angle = latest[2]+5
    t.left(angle)
    latest = [-1, time(), angle]

def step():
    clear()
    global c
    c += 1
    goto(0, -radius-50)
    write(str(c), align="center", font=("Courier", 16, "bold"))
    goto(0, radius+5)
    x, y = t.pos()
    h = t.heading()
    dotprod = step_length * (x*cos(h*pi/180) + y*sin(h*pi/180))
    if x*x + y*y > 0.25 * radius*radius and dotprod >= 0:
        t.forward(-step_length)
        if dotprod > 0.8 * radius*step_length:
            write("Hahaha ! Tu croyais vraiment que {}\naccepterait de laisser le prisonnier faire ça ?? Retour en arrière !".format(choice(names)), align="center", font=("Courier", 12, "bold"))
        elif x*x + y*y > 0.66 * radius*radius and random() < 0.5:
            write("Attends ! Tu n'as pas l'intention de libérer le prisonnier ??\nIl a quand même {}".format(choice(crime)), align="center", font=("Courier", 14, "bold"))
        else:
            write("Dommage, {} a décidé {}".format(choice(names),choice(invert)), align="center", font=("Courier", 12, "bold"))
    else:
        t.forward(step_length)
        if x*x + y*y > 0.66 * radius*radius and random() < 0.5:
            write("Attends ! Tu n'as pas l'intention de libérer le prisonnier ??\nIl a quand même {}".format(choice(crime)), align="center", font=("Courier", 14, "bold"))
        else:
            write("{}, {}\na décidé {}".format(choice(reason), choice(names), choice(accept)), align="center", font=("Courier", 12, "bold"))
    if sum(i*i for i in t.pos()) > radius*radius:
        clear()
        goto(0, -40)
        write("Bravo ! Après {} pas, le prisonnier\na pu s'échapper...\nLe code de ce jeu est {}.\nAppuyez sur Entrer quand c'est noté.".format(c, code), align="center", font=("Courier", 16, "bold"))
        onkey(endgamestep, "space")

def endgamestep():
    t.forward(step_length)
    x, y = t.pos()
    if x*x + y*y < radius*radius:
        clear()
        write("Mais non !! T'es fou ? Pourquoi t'es\nrevenu dans la prison ?".format(c, code), align="center", font=("Courier", 16, "bold"))
        goto(0,radius+5)
        onkey(step, "space")


def startgame():
    onkey(None, "space")
    global c
    c = 0
    t.ht()
    clear()
    goto(0, -60)
    write("Vous êtes un prisonnier qui tente de s'évader. Il n'y\na pas de mur. Seul obstacle : un esprit maléfique qui\npeut inverser vos mouvements. Appuyez sur les flèches\ndroite/gauche pour modifier la direction du\nprisonnier, appuyez sur espace pour avancer d'un pas.", align="center", font=("Courier", 12, "bold"))
    goto(0,radius+5)
    write("Appuyez sur Entrer pour commencer à jouer", align="center", font=("Courier", 16, "bold"))
    onkey(play, "Return")

def play():
    clear()
    t.ht(); t.speed(0); t.goto(0, 0); t.setheading(90); t.speed(3); t.st()
    onkey(turnr, "Right")
    onkey(turnl, "Left")
    onkey(step, "space")
    onkey(startgame, "Return")

try: hideturtle(); pu(); speed(0) # la tortue qui écrit les messages
except: hideturtle(); pu(); speed(0)
t = Turtle(visible=False) # la tortue du prisonnier
t.turtlesize(2, 2)
draw_circle(t, 0, 0, radius, "-")
for i in range(1, 4): draw_circle(t, 0, 0, radius*i/4, "--")
startgame()
listen()
mainloop()
