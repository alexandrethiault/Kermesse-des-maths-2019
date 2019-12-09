import pygame
import time
from pygame.locals import *

while True:
    pygame.init()
    fenetre = pygame.display.set_mode((908, 605)) # Taille de l'écran du jeu
    bravo = pygame.image.load("bravo.jpg").convert()
    suivant = pygame.image.load("suivant.jpg").convert()
    horizon = pygame.image.load("horizontale.jpg").convert()
    verti = pygame.image.load("verticale.jpg").convert()
    horizonpetit = pygame.image.load("horizontalepetit.jpg").convert()
    score = 0
    bonnescartes = [0,1,1,0,1,1,1,0,0,1]
    for i in range(10):
        tentatives = 0
        trouve = False
        fin = False
        while not fin:
            joue = pygame.image.load("joue.jpg").convert()
            cocci = pygame.image.load("cocci" + str(i+1) + ".jpg").convert()
            carte1 = pygame.image.load("carte" + str(i+1) + "1" + ".jpg").convert()
            carte2 = pygame.image.load("carte" + str(i+1) + "2" + ".jpg").convert()
            cartescore = pygame.image.load(str(score) + ".jpg").convert()
            fenetre.blit(cocci, (0, 0)) #on place le fond sur l'écran
            fenetre.blit(cartescore, (600, 400))
            fenetre.blit(suivant, (600, 550))
            fenetre.blit(carte1, (10, 400))
            fenetre.blit(carte2, (380, 400))
            fenetre.blit(bravo if trouve else joue, (600, 0))
            fenetre.blit(horizon, (0, 392))
            fenetre.blit(horizon, (0, 597))
            fenetre.blit(verti, (590, 0))
            fenetre.blit(verti, (900, 0))
            fenetre.blit(verti, (0, 0))
            fenetre.blit(horizon, (0, 0))
            fenetre.blit(horizonpetit, (600, 545))
            pygame.display.flip()
            for event in pygame.event.get() :
                if event.type == QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN :
                    x_clic, y_clic = event.pos[0], event.pos[1]
                    if (20<x_clic<220 or 380<x_clic<580) and y_clic > 400:
                        tentatives += 1
                        if x_clic//300 == bonnescartes[i]:
                            trouve = True
                            if tentatives == 1:
                                score += 1
                    if trouve and 600 < x_clic and y_clic > 550:
                        fin = True
    time.sleep(3)
    pygame.quit()
    print("Score : {} points\n----------------".format(score))
    time.sleep(3)
