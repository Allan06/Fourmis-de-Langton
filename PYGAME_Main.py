#______________________________FOURMIS DE LANGTON______________________________

#---------------------------------------------------------------------------------
# Module 02 - Langton_main.py
# Version 1.7 (04 Mai 2017)
# PAJANY Allan
# 1ère Annee - License Science de l'ingénieur - UTLN
#---------------------------------------------------------------------------------

from PYGAME_Fourmis import *


#--------------------------------------------------------------------------------#
#--------------|                  DEBUT                 |---------------#
#--------------------------------------------------------------------------------#

# Initailisation de la fenetre d'acceuil
#---------------------------------------------------------------------------------

def Init_Accueil():
    """ Initialisation et affichage de l'image d'acceuil. """

    accueil = pygame.image.load('accueil.jpg').convert()
    accueil = pygame.transform.scale(accueil, (LA, HA))
    fenetre.blit(accueil, (0, 0))
    pygame.display.flip()


# Initailisation de l'ecran des parametres
#---------------------------------------------------------------------------------

def Init_Parametre():
    """ Initialisation des parametres. """

    # Chargement d'un fond blanc
    fenetre.fill((255, 255, 255))
    # Affichage du grand titre 'PARAMETRE'
    Text_Titre = myfont_GTitre.render('PARAMETRES', 1, (255, 0, 0))
    fenetre.blit(Text_Titre, (LA // 2.5, HA // 60))
    # Soulignement du grand titre
    Text_Soul = myfont_GTitre.render('_______________', 1, (255, 0, 0))
    fenetre.blit(Text_Soul, (LA // 2.5, HA // 50))
    pygame.display.flip()


accueil = pygame.image.load('accueil.jpg').convert()
Init_Accueil()
Parametre = [['Aleatoire', 'Centre', 'Pyramidale'], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                     ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['1000', '10000', '100000', '1000000', '10000000', '100000000']]

P = [['Al', 'C', 'PYR'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1000, 10000, 100000, 1000000, 10000000, 100000000]]
D = {}
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                
        # Accueil et affichage des parametres
        elif event.type == MOUSEBUTTONUP and  event.button == 1 and LA - (LA // 3) < event.pos[0] < LA and 0 < event.pos[1] < HA // 10:
            Init_Parametre()
            for i in range(len(Parametre)):
                if i == 0:
                    fenetre.blit(myfont_titre.render('Positions', 1, (255, 0, 0)), (CASE_L // DIM - 3, 90))
                    for j in range(len(Parametre[i])):
                        # Creation des rectangles de choix
                        Color_Case((CASE_L // DIM - 3) // DIM, (115 + (j * 20)) // DIM, (200, 200, 200))
                        # Affichage des parametres contenus dans la liste 'Parametre'
                        fenetre.blit(myfont_choix.render(Parametre[i][j], 1, (0, 0, 0)), ((CASE_L // DIM - 3) + 15, 93 + ((j + 1) * 20)))
                    
                elif i == 1:
                    fenetre.blit(myfont_titre.render('Nombre de fourmis', 1, (255, 0, 0)), (CASE_L // DIM - 3, 180))
                    for j in range(len(Parametre[i])):
                        Color_Case(((CASE_L // DIM - 3) + (j * 20)) // DIM, 205 // DIM, (200, 200, 200))
                        fenetre.blit(myfont_choix.render(Parametre[i][j], 1, (0, 0, 0)), ((CASE_L // DIM - 3) + (j * 20), 216))
                    
                elif i == 2:
                    fenetre.blit(myfont_titre.render("Nombre d'obstacles", 1, (255, 0, 0)), (CASE_L // DIM - 3, 240))
                    for j in range(len(Parametre[i])):
                        Color_Case(((CASE_L // DIM - 3) + (j * 20)) // DIM, 260 // DIM, (200, 200, 200))
                        fenetre.blit(myfont_choix.render(Parametre[i][j], 1, (0, 0, 0)), ((CASE_L // DIM - 3) + (j * 20), 270))
                        
                elif i == 3:
                    fenetre.blit(myfont_titre.render("Nombre d'iterations", 1, (255, 0, 0)), (CASE_L // DIM - 3, 300))
                    for j in range(len(Parametre[i])):
                        Color_Case((CASE_L // DIM - 3) // DIM, (325 + (j * 20)) // DIM, (200, 200, 200))
                        fenetre.blit(myfont_choix.render(Parametre[i][j], 1, (0, 0, 0)), ((CASE_L // DIM - 3) + 15, 300 + ((j + 1) * 20)))
                        
        # Choix des parametres           
        elif event.type == MOUSEBUTTONUP and  event.button == 3:
            if COORD[event.pos[0] // DIM, event.pos[1] // DIM] == (200, 200, 200):
                
                Color_Case(event.pos[0] // DIM, event.pos[1] // DIM, (0, 255, 0))
                
        pygame.display.flip()
        
print('fin')
