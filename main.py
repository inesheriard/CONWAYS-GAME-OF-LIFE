import numpy as np
import pygame as pg

#Constantes et initialisation de la matrice
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10
NB_COL = WIDTH // TILE_SIZE
NB_ROW = HEIGHT // TILE_SIZE
MAT = np.random.choice([0,1], size=(NB_ROW, NB_COL), p=[0.85, 0.15])

#Fonction de mise à jour de la matrice
def update(mat):
    mat_binaire = (mat > 0).astype(int)
    #Calcul du total des voisins à chaque tour
    #Pour ce calcul, on utilise mat_binaire qui ne prend en compte que les 0 et les cases qui ont un âge de 1/+
    total_voisins = (
        np.roll(mat_binaire, 1, 0) + #case haut
        np.roll(mat_binaire, -1, 0) + #case bas
        np.roll(mat_binaire, 1, 1) + #case gauche
        np.roll(mat_binaire, -1, 1) + #case droite
        np.roll(np.roll(mat_binaire, 1, 0), 1, 1) + #case diago (haut gauche)
        np.roll(np.roll(mat_binaire, 1, 0), -1, 1) + #case diago (haut droite)
        np.roll(np.roll(mat_binaire, -1, 0), 1, 1) + #case diago (bas gauche)
        np.roll(np.roll(mat_binaire, -1, 0), -1, 1) #case diago (bas droite)
        )
    
    #Initialisation à chaque tour d'une matrice de 0
    NEW_MAT = np.zeros((NB_ROW, NB_COL), dtype=int) #Règle de mort inutile comme on a ici tout initialisé à 0

    #Règle de naissance à l'âge 1
    NEW_MAT[(mat == 0) & (total_voisins == 3)] = 1

    #Règle de survie et incrémentation de l'âge (pour la coloration dynamique)
    SURVIE = (mat > 0) & ((total_voisins == 3) | (total_voisins == 2))
    NEW_MAT[SURVIE] = MAT[SURVIE]+1

    return(NEW_MAT)

#Début du programme de jeu
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT)) #Création de la fenêtre
clock = pg.time.Clock() #Création de l'horloge
pg.display.set_caption("Conway's Game of Life") #Définition du titre de la fenêtre

#Constantes et calculs pour la coloration dynamique
noir = (0,0,0) #Couleur du fond
blanc = (255,255,255) #Couleur cadette
violet = (50, 0, 80) #Couleur doyenne
AGE_MAX = 20
PALETTE=[] #Liste où l'on stockera les 20 couleurs des 20 âges différents
r, g, b = 255.0, 255.0, 255.0 #Initialisation des 3 codes au max
for i in range(AGE_MAX):
    r -= 10.25 #Pas nécessaire pour aller de 255 à 50 pour le rouge
    g -= 12.75 #Pas nécessaire pour aller de 255 à 0 pour le vert
    b -= 8.75 #Pas nécessaire pour aller de 255 à 80 pour le bleu
    PALETTE.append((int(r), int(g), int(b))) #Ajout du tuple pour chaque couleur

#Initialisation des presets en matrices
glider = np.array(
    [[0,1,0],
    [0,0,1],
    [1,1,1]]
    )

#Début de la boucle de jeu
running = True
paused = False

while running:
    #Gestion d'évènements
    for event in pg.event.get():
        #Quitter le jeu avec la croix
        if event.type==pg.QUIT:
            running = False
        #Mettre en pause
        if event.type==pg.KEYDOWN and event.key==pg.K_SPACE:
            paused = not paused
        #Fonctionnalité de modification des cellules en cliquant
        if event.type==pg.MOUSEBUTTONDOWN:
            x, y = event.pos #Position exacte en pixel
            col_corresp = x // TILE_SIZE #Index de la colonne correspondante à la coordonnée x
            row_corresp = y // TILE_SIZE #Index de la ligne correspondante à la coordonnée y
            MAT[row_corresp, col_corresp] = 1 - MAT[row_corresp, col_corresp] #Changement de l'état (morte/vivante) de la cellule en cliquant
        #Ajout d'un glider en cliquant
        if event.type==pg.KEYDOWN and event.key==pg.K_g:
            (x,y)=pg.mouse.get_pos()
            col_corresp = x // TILE_SIZE
            row_corresp = y // TILE_SIZE
            MAT[row_corresp:row_corresp+3, col_corresp:col_corresp+3]=glider

        

    #Changement des états des cellules (mortes/vivantes) et coloration dynamique
    screen.fill(noir) #Fond noir

    filled_rows, filled_cols =  np.where(MAT > 0)
    for i in range(len(filled_rows)):
        #Calcul des positions x et y en pixels, et initialisation de l'âge
        x = filled_cols[i]*TILE_SIZE
        y = filled_rows[i]*TILE_SIZE
        age = MAT[filled_rows[i], filled_cols[i]]
        index = min(age-1, 19) #Initialisation de l'index à utiliser pour avoir la bonne couleur (on arrête à 19 dans le cas où la cellule vit plus de 20 tours)
        couleur = PALETTE[index]
        if age == 1:
            pg.draw.rect(screen, blanc, (x, y, TILE_SIZE-1, TILE_SIZE-1)) #Dessin du premier rectangle (-1 pour laisser un quadrillage)
        else:
            pg.draw.rect(screen, couleur, (x, y, TILE_SIZE-1, TILE_SIZE-1)) #Changement de couleur
    
    if paused == False:
        MAT = update(MAT) #Perpétuelle mise à jour tant que l'on a pas mis le jeu en pause
    pg.display.flip()
    clock.tick(7) #Nombre d'images par seconde

pg.quit()