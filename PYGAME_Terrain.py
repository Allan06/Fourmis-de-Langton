# ______________________________FOURMIS DE LANGTON_____________________________

# =============================================================================
# terrain.py
# Version 2.0 (26 Avril 2018)
# PAJANY Allan
# 2ème Annee - License Science de l'ingénieur - UTLN
# =============================================================================


from math import trunc
from pygame.locals import *
from pygame import display, draw, event, font, time
from random import randint


# =========================================================================== #
# ====================|            CONSTANTES          |===================== #
# =========================================================================== #

LIM = 1300          # Limite de la taille de la taille en largeur
DIM = 6            # Dimension d'une case en pixel
ESP = 2            # Espace entre l'affichage des informations des fourmi
BS = trunc((25 / (DIM * 0.1)))    # Borne redimenssionnant la colonne des stats
CASE_L = (LIM // DIM) - BS            # Nombre de cases en largeur (sans stats)
CASE_H = trunc(LIM / DIM * 0.60)      # Nombre de cases en hauteur
LARGEUR, HAUTEUR = LIM, (DIM * CASE_H)  # Dimensions de la largeur de fenetre
ECRAN = CASE_L * DIM
BLANC, NOIR, VERT = (255, 255, 255), (0, 0, 0), (0, 255, 0)
STAT = LARGEUR - ECRAN

# Initialisation de la fenetre
# -----------------------------------------------------------------------------
font.init()
FENETRE = display.set_mode((LARGEUR, HAUTEUR))
display.set_caption((LIM // 8) * ' ' + 'FOURMIS DE LARGEURNGTON')
FENETRE.fill(BLANC)

# Initialisation des polices d'ecritures de Pygame
# -----------------------------------------------------------------------------
POLICE = 14
Gtitre = font.SysFont("rockwell", POLICE * 4)
Titre = font.SysFont("rockwell", POLICE)
Choix = font.SysFont("rockwell", POLICE * 2)

# Creation du dictionnaire de coordonnees
# -----------------------------------------------------------------------------
CASE = {}
for x in range(CASE_L):
    for y in range(CASE_H):
        CASE[(x, y)] = BLANC
        # {(Abcisse, Ordonnee): Etat}

TAILLE = len(CASE)
BLIT, FILL, LINE = FENETRE.blit, FENETRE.fill, draw.line
RENDER = Titre.render


# =========================================================================== #
# ====================|        FONCTIONS PRIVEES       |===================== #
# =========================================================================== #

# Empeche l'arrêt du script en cliquant sur la souris
# -----------------------------------------------------------------------------
def __events(tps):
    """ Fonction permettant la raffraichissement de l'affichage et de gerer
    l'evenement du clic de la souris qui empeche le bon fonctionnement du
    scripts en cliquant avec la souris. """

    display.update()
    time.delay(tps)
    for evenement in event.get():
        if evenement.type == MOUSEBUTTONUP:
            pass

        elif evenement.type == QUIT:
            quit()


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Creation de la grille
# -----------------------------------------------------------------------------
def init_grille(visuel=1):
    """ Procedure permettanSt la creation de la grille.
    visuel : Dessine le quadrillage normal. """

    # Dessins de la grille
    if visuel:
        # Lignes
        for lig in range(CASE_H + 1):
            FILL(NOIR, (0, lig * DIM, ECRAN, 1))
            __events(0)

        # Colonnes
        for col in range(CASE_L + 1):
            FILL(NOIR, (col * DIM, 0, 1, HAUTEUR))
            __events(0)

    # Colone des stats
    FILL(NOIR, (ECRAN, 0, 1, HAUTEUR))


# Affichage du temps de pause
# -----------------------------------------------------------------------------
def affiche_pause(tps):
    """ Procedure permettant l'affciahage du temps 'tps'. """

    FILL(BLANC, (ECRAN + 2, HAUTEUR - (2 * POLICE), STAT, POLICE))
    BLIT(RENDER("Pause : %ds" % tps, 1, (255, 0, 0)),
         (ECRAN + 2, HAUTEUR - (2 * POLICE)))


# Affiche le temps
# -----------------------------------------------------------------------------
def affiche_temps(tps, fps):
    """ Procédure permettant d'fficher le temps 't'. """

    FILL(BLANC, (ECRAN + 2, HAUTEUR - (4 * POLICE), STAT, POLICE * 2))
    BLIT(RENDER('Fps: %d' % fps, 1, (0, 0, 255)),
         (ECRAN + 2, HAUTEUR - (4 * POLICE)))
    BLIT(RENDER('Temps: %ds' % tps, 1, (0, 0, 255)),
         (ECRAN + 2, HAUTEUR - (3 * POLICE)))


# Coloration d'une case et changement d'etat
# -----------------------------------------------------------------------------
def color_case(posx, posy, coul, marge=1):
    """ Colorie la case de coordonnee '(x, y)' avec la couleur 'col' et modifie
    la valeur des coordonnee '(x, y)' dans le dictionnaire avec 'col'. """

    CASE[(posx, posy)] = coul
    FILL(coul, ((posx * DIM) + marge, (posy * DIM) + marge, (DIM - marge),
                (DIM - marge)))


# Création d'obstacles
# -----------------------------------------------------------------------------
def obstacles(nb_obs, posx=0, posy=0):
    """ Cree 'n' obstacles aléatoirement sur le terrain. """

    obst = []      # Stockage des coordonnees aleatoires des obstacles
    for obs in range(nb_obs):
        obst.append((randint(0, CASE_L - 1), randint(0, CASE_H - 1)))
        color_case(obst[obs][0], obst[obs][1], VERT)

    if posx and posy:
        color_case(posx, posy, VERT)


# Affichage des statistiques des fourmis
# -----------------------------------------------------------------------------
def stats(visuel, num_f, nbr_f, coul, nbr_iter, fin, orient=None, comp=None):
    """" Affiche dynamiquement le nombre de fourmis et le nombre d'iteration.
    rep = 'Y' ou 'N' pour afficher ou ne pas afficher les statistiques.
    num_f = Indice de la fourmis permettant de modifier la valeur de l'abcisse.
    val = Nombre de fourmi sur le terrain.
    coul = Couleur de la fourmi.
    nbr_iter = Iteration qui s'incremente à chaque deplacement des fourmis.
    fin = Le nombre total d'iteration.
    orient = Orientation de la fourmis.
    comp = Comportement de la fourmis."""

    if visuel:
        # Statistiques de repartition d'une fourmi
        # ---------------------------------------------------------------------
        # Initialisation du rectangle blanc
        FILL(BLANC, (ECRAN + 2, (num_f * POLICE * ESP) + 1, STAT, POLICE))
        # Afficher ou non de l'orientation et du comportement de la fourmis
        BLIT(RENDER(nbr_f, 1, coul) if orient is None and comp is None else
             RENDER("%s %s %s" % (nbr_f, orient, comp), 1, coul),
             (ECRAN + 2, num_f * POLICE * ESP))

        # Statistique du nombre d'iteration
        # ---------------------------------------------------------------------
        FILL(BLANC, (ECRAN + 2, HAUTEUR - POLICE, STAT, POLICE))
        BLIT(RENDER("%d/%d" % (nbr_iter, fin), 1, NOIR),
             (ECRAN + 2, HAUTEUR - POLICE))


# =========================================================================== #
# ===================|          TEST UNITAIRE           |==================== #
# =========================================================================== #
if __name__ == '__main__':
    # Grille d'echecs
    # -------------------------------------------------------------------------
    def __echecs(largeur, hauteur):
        """ Tableau d'echecs de largeur 'L' et de ha 'H'. """

        nbc, cpt = 0, 0
        for indx in range(largeur):
            for indy in range(hauteur):
                color_case(indx, indy,
                           NOIR if not (indy + indx) % 2 else BLANC)
                if CASE[indx, indy] == BLANC:
                    nbc += 1
                    stats(1, 14.7, "Cases blanches: %d" % nbc, (105, 105, 105),
                          "Iter: %d" % cpt, TAILLE)

                cpt += 1
                __events(0)

    # Parcours serpentin
    # -------------------------------------------------------------------------
    def __parcours_serpentin(nbcase):
        """ Parcours en serpentin d'un tableau de taille 'n * n'. """

        lcase = []
        h, b, g, d = 0, CASE_H - 1, 0, nbcase - 1  # Gestion de la parité
        icst, jcst, ivar, jvar = 0, 0, 1, 0
        lapp = lcase.append
        while h <= b:
            while (g <= icst <= d) and (h <= jcst <= b):
                lapp((icst, jcst))
                icst += ivar
                jcst += jvar

            if icst > d:
                ivar, jvar = 0, 1
                jcst += 1
                icst -= 1
                h += 1

            if icst < g:
                ivar, jvar = 0, - 1
                jcst -= 1
                icst += 1
                b -= 1

            if jcst > b:
                ivar, jvar = - 1, 0
                icst -= 1
                jcst -= 1
                d -= 1

            if jcst < h:
                ivar, jvar = 1, 0
                icst += 1
                jcst += 1
                g += 1

        return lcase

    # Affichage du titre
    test = font.SysFont("arialblack", 20).render('TEST', 1, (255, 0, 0))
    unit = font.SysFont("arialblack", 20).render('UNITAIRE', 1, (255, 0, 0))
    BLIT(test, (LARGEUR - (STAT // 1.5) + 1, 0))
    BLIT(unit, (LARGEUR - (STAT // 1.3), POLICE * 3))
    init_grille(1)

    # Test 01 - Serpentin en couleurs N/Bc ou aleatoires
    # -------------------------------------------------------------------------
    BLIT(RENDER('TEST 1: SERPENTIN', 1, (0, 128, 0)), (ECRAN + 2, POLICE * 17))
    BLIT(RENDER((40 * '_'), 1, (0, 128, 0)), (ECRAN + 2, POLICE * 17))
    l_srp = __parcours_serpentin(CASE_L)
    s_taille = len(l_srp)
    rep, val = 'E', 0
    # Parcours serpentin en tbleau d'echec
    if rep == 'E':
        for i in range(s_taille):
            color_case(l_srp[i][0], l_srp[i][1], BLANC if i % 2 == 0 else NOIR)
            val = val + 1 if CASE[l_srp[i][0], l_srp[i][1]] == NOIR else val
            stats('Y', 9.2, 'Cases noires = %d' % val, NOIR, 'Iter = %d' % i,
                  TAILLE - 1)
            __events(0)

    # Parcours serpentin en multicolore
    elif rep == 'M':
        for serp in l_srp:
            mul_coul = (randint(0, 255), randint(0, 255), randint(0, 255))
            color_case(serp[0], serp[1], mul_coul)
            __events(0)

    # Test 02 - Echecs, coloration de quelques cases en R/Be
    # -------------------------------------------------------------------------
    BLIT(RENDER('TEST 2: R&B', 1, (0, 128, 0)), (ECRAN + 2, POLICE * 20))
    BLIT(RENDER((40 * '_'), 1, (0, 128, 0)), (ECRAN + 2, POLICE * 20))
    ind, val_r, val_b = 0, 0, 0
    for dic in CASE:
        if ind % 2 == 0 and ind % 3 == 0:
            color_case(dic[0], dic[1], (255, 0, 0))
            val_r += 1
            stats(1, 10.7, 'Cases rouges: %d' % val_r, (255, 0, 0), 'Iter: %d'
                  % ind, TAILLE - 1)

        else:
            color_case(dic[0], dic[1], (0, 0, 255))
            val_b += 1
            stats(1, 11.2, 'Cases bleues = %d' % val_b, (0, 0, 255), 'Iter: %d'
                  % ind, TAILLE - 1)

        ind += 1
        __events(0)

    # Test 03 - Colorations aleatoires N/B
    # -------------------------------------------------------------------------
    BLIT(RENDER('TEST 3: N&B', 1, (0, 128, 0)), (ECRAN + 2, POLICE * 24))
    BLIT(RENDER((40 * '_'), 1, (0, 128, 0)), (ECRAN + 2, POLICE * 24))
    nbr, val_n, val_b = 2, 0, 0
    for _ in range(1):
        # 1er mouvement
        # ---------------------------------------------------------------------
        ind = 0
        for dic in CASE:
            if ind % nbr == 0 and dic[0] % nbr == 0:
                if CASE[dic] != NOIR and CASE[dic] != BLANC:
                    val_b += 1

                elif CASE[dic] == NOIR:
                    val_n -= 1
                    val_b += 1

                color_case(dic[0], dic[1], BLANC)

            else:
                if CASE[dic] != NOIR and CASE[dic] != BLANC:
                    val_n += 1

                elif CASE[dic] == BLANC:
                    val_b -= 1
                    val_n += 1

                color_case(dic[0], dic[1], NOIR)

            stats(1, 12.6, 'Cases blanches: %d' % val_b, (105, 105, 105),
                  'Iter = %d' % ind, TAILLE)
            stats(1, 13.1, 'Cases noires: %d' % val_n, NOIR, 'Iter = %d' % ind,
                  TAILLE)
            ind += 1
            __events(0)

        # 2ème mouvement
        # ---------------------------------------------------------------------
        ind = 0
        for dic in CASE:
            if ind % nbr == 0 and dic[1] % nbr == 0:
                if CASE[dic] == NOIR:
                    val_n = val_n - 1
                    val_b = val_b + 1

                color_case(dic[0], dic[1], BLANC)

            else:
                if CASE[dic] == BLANC:
                    val_b -= 1
                    val_n += 1

                color_case(dic[0], dic[1], NOIR)

            stats(1, 12.6, 'Cases blanches: %d' % val_b, (105, 105, 105),
                  'Iter = %d' % ind, TAILLE)
            stats(1, 13.1, 'Cases noires: %d' % val_n, NOIR, 'Iter = %d' % ind,
                  TAILLE)
            ind += 1
            __events(0)

        # 3ème mouvement
        # ---------------------------------------------------------------------
        ind = 0
        for dic in CASE:
            if ind % nbr == 0 and dic[0] % nbr == 0:
                if CASE[dic] == BLANC:
                    val_b -= 1
                    val_n += 1

                color_case(dic[0], dic[1], NOIR)

            else:
                if CASE[dic] == NOIR:
                    val_n -= 1
                    val_b += 1

                color_case(dic[0], dic[1], BLANC)

            stats(1, 12.6, 'Cases blanches: %d' % val_b, (105, 105, 105),
                  'Iter = %d' % ind, TAILLE)
            stats(1, 13.1, 'Cases noires: %d' % val_n, NOIR, 'Iter = %d' % ind,
                  TAILLE)
            ind += 1
            __events(0)

    # Test 04 - Grille d'echec
    # -------------------------------------------------------------------------
    BLIT(RENDER('TEST 4 - ECHECS', 1, (0, 128, 0)), (ECRAN + 2, POLICE * 28))
    BLIT(RENDER((40 * '_'), 1, (0, 128, 0)), (ECRAN + 2, POLICE * 28))
    __echecs(CASE_L, CASE_H)

# =========================================================================== #
# ==========================|         FIN        |=========================== #
# =========================================================================== #
    Text_Fin = font.SysFont("arialblack", 20).render('FIN', 1, (255, 0, 0))
    BLIT(Text_Fin, (LARGEUR - (STAT // 1.5), HAUTEUR - (10 * POLICE)))
    __events(1000)
    quit()
