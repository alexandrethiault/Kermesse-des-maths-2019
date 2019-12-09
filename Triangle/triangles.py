import pygame
from pygame.locals import *

screen = (749,533)
x_m1, x_0, x_1 = 313, 363, 413
y_0, y_1 = 253, 203
x1, y1 = x_0, y_0
x2, y2 = x_0, y_1
x3, y3 = x_1, y_0

pygame.init()
fenetre = pygame.display.set_mode(screen)
fond = pygame.image.load("repere.jpg").convert()
point = pygame.image.load("point.gif").convert()
pointrouge = pygame.image.load("pointrouge.gif").convert()
fenetre.blit(fond, (0, 0))
fenetre.blit(point, (x1, y1))
fenetre.blit(point, (x2, y2))
fenetre.blit(point, (x3, y3))
fenetre.blit(pointrouge, (x_m1+1, y_0+1))
fenetre.blit(pointrouge, (x_0+1, y_1+1))
fenetre.blit(pointrouge, (x_1+1, y_0+1))
pygame.display.flip()

while True:
    point_choisi = None
    while point_choisi is None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos[0], event.pos[1]
                if abs(x-5 - x1)<10 and abs(y-5 - y1)<10:
                    point_choisi = 1
                    if x2 != x3:
                        a = (y2-y3) / (x2-x3)
                        b = y1-a*x1
                if abs(x-5 - x2)<10 and abs(y-5 - y2)<10:
                    point_choisi = 2
                    if x1 != x3:
                        a = (y1-y3) / (x1-x3)
                        b = y2-a*x2
                if abs(x-5 - x3)<10 and abs(y-5 - y3)<10:
                    point_choisi = 3
                    if x1 != x2:
                        a = (y1-y2) / (x1-x2)
                        b = y3-a*x3
                fenetre.blit(fond, (0, 0))
                fenetre.blit(point, (x1 ,y1))
                fenetre.blit(point, (x2, y2))
                fenetre.blit(point, (x3, y3))
                fenetre.blit(pointrouge, (x_m1+1, y_0+1))
                fenetre.blit(pointrouge, (x_0+1, y_1+1))
                fenetre.blit(pointrouge, (x_1+1, y_0+1))
                pygame.display.flip()

    point_place = False
    while not point_place:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                point_place = True
            if event.type == MOUSEMOTION:
                x, y = event.pos[0], event.pos[1]
                if point_choisi == 1:
                    if x3 == x2:
                        newx1 = x1
                        newy1 = y
                    else:
                        newx1 = int((a*y+x - a*b) / (1+a*a))
                        newy1 = int((a*a*y+a*x + b) / (1+a*a))
                    if 0 < newx1+5 < screen[0] and 0 < newy1+5 < screen[1]:
                        x1, y1 = newx1, newy1
                if point_choisi == 2:
                    if x1 == x3:
                        newx2 = x2
                        newy2 = y
                    else:
                        newx2 = int((a*y+x - a*b) / (1+a*a))
                        newy2 = int((a*(a*y+x) + b) / (1+a*a))
                    if 0 < newx2+5 < screen[0] and 0 < newy2+5 < screen[1]:
                        x2, y2 = newx2, newy2
                if point_choisi == 3:
                    if x1 == x2:
                        newx3 = x3
                        newy3 = y
                    else:
                        newx3 = int((a*y+x - a*b) / (1+a*a))
                        newy3 = int((a*a*y+a*x + b) / (1+a*a))
                    if 0 < newx3+5 < screen[0] and 0 < newy3+5 < screen[1]:
                        x3, y3 = newx3, newy3
                fenetre.blit(fond, (0, 0))
                fenetre.blit(point, (x1 ,y1))
                fenetre.blit(point, (x2, y2))
                fenetre.blit(point, (x3, y3))
                fenetre.blit(pointrouge, (x_m1+1, y_0+1))
                fenetre.blit(pointrouge, (x_0+1, y_1+1))
                fenetre.blit(pointrouge, (x_1+1, y_0+1))
                pygame.display.flip()
