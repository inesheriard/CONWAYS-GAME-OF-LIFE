import numpy as np
import pygame as pg

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10
NB_COL = WIDTH // TILE_SIZE
NB_ROW = HEIGHT // TILE_SIZE
MAT = np.random.choice([0,1], size=(NB_ROW, NB_COL), p=[0.85, 0.15])

def update(mat):
    #Calcul du total des voisins à chaque tour
    total_voisins = (
        np.roll(mat, 1, 0) + #case haut
        np.roll(mat, -1, 0) + #case bas
        np.roll(mat, 1, 1) + #case gauche
        np.roll(mat, -1, 1) + #case droite
        np.roll(np.roll(mat, 1, 0), 1, 1) + #case diago (haut gauche)
        np.roll(np.roll(mat, 1, 0), -1, 1) + #case diago (haut droite)
        np.roll(np.roll(mat, -1, 0), 1, 1) + #case diago (bas gauche)
        np.roll(np.roll(mat, -1, 0), -1, 1) #case diago (bas droite)
        )
    
    #Initialisation à chaque tour d'une matrice de 0
    NEW_MAT = np.zeros((NB_ROW, NB_COL), dtype=int) #Règle de mort inutile comme on a ici tout initialisé à 0

    #Règle de naissance
    NEW_MAT[(mat == 0) & (total_voisins == 3)] = 1

    #Règle de survie
    NEW_MAT[(mat == 1) & ((total_voisins == 3) | (total_voisins == 2))] = 1

    return(NEW_MAT)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT)) #Création de la fenêtre
clock = pg.time.Clock() #Création de l'horloge
pg.display.set_caption("Conway's Game of Life")

noir = (0,0,0)
blanc = (255,255,255)
jaune = (255,255,0)
running = True
paused = False

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT: #Quitter le jeu avec la croix
            running = False
        if event.type==pg.KEYDOWN and event.key==pg.K_SPACE: #Mettre en pause
            paused = not paused
        if event.type==pg.MOUSEBUTTONDOWN: #Modifier les cellules en cliquant
            x, y = event.pos
            col_corresp = x // TILE_SIZE
            row_corresp = y // TILE_SIZE
            MAT[row_corresp, col_corresp] = 1 - MAT[row_corresp, col_corresp]



    screen.fill(noir) #Fond noir

    filled_rows, filled_cols =  np.where(MAT == 1)
    for i in range(len(filled_rows)):
        #Calcul des positions x et y en pixels
        x = filled_cols[i]*TILE_SIZE
        y = filled_rows[i]*TILE_SIZE
        pg.draw.rect(screen, blanc, (x, y, TILE_SIZE-1, TILE_SIZE-1)) #Dessin du rectangle (-1 pour laisser un quadrillage)
    if paused == False:
        MAT = update(MAT)
    pg.display.flip()
    clock.tick(7) #Nombre d'images par seconde

pg.quit()