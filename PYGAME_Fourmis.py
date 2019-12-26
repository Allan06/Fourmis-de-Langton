#______________________________fourmiS DE LANGTON______________________________

# =============================================================================
# fourmi.py
# Version 2.2 (23 Novembre 2018)
# PAJANy_tmp Allan
# 2ème Annee - License Science de l'ingénieur - UTLN
# =============================================================================

import sys
from math import cos, sin, radians
from random import choice
from PYGAME_Terrain import *

L_POS = tuple([i for i in range(POLICE, 20000, POLICE * 2)])


# =========================================================================== #
# ====================|        FONCTIONS PRIVEES       |===================== #
# =========================================================================== #

# Creation d'un tableau avec valeurs aleatoire
# -----------------------------------------------------------------------------
def __table_t(nbcoul):
    """ Fonction retournant une liste de 'n' couleurs aleatoires. """

    liste_coul = []
    ind_coul = 0
    while ind_coul < nbcoul:
        coul = (randint(0, 255), randint(0, 255), randint(0, 255))
        if coul in liste_coul or coul is VERT or coul is NOIR:
            ind_coul -= 1

        else:
            liste_coul.append(coul)
            ind_coul += 1

    return liste_coul


# Vérification des motifs
# -----------------------------------------------------------------------------
def __verif_motifs(fichier, nbr_c):
    """ Verfication des motifs se trouvant dans le fichier 'fichier' de taille
    'NBR_C' (nombre de carracteres = nombre de fourmis + 1). """

    l_motifs = []
    with open(fichier) as mot:
        # Stockage des motifs dans une liste
        for motifs in range(nbr_c):
            l_motifs.append(mot.readline()[0: nbr_c + 1])
            # Si le nombre de motif est inferieur au nombre de fourmis
            if l_motifs[motifs] is '\n':
                print('Erreur : le nombre de motif est inferieur au nombre'
                      ' de fourmis.')
                quit()

        # Affichage des erreurs de syntaxes des entrees
        # ---------------------------------------------------------------------

        ligne = 1     # Initialise la ligne indiquant la position de l'erreur
        for motifs in l_motifs:
            # Si les 2 premiers carracteres sont les memes
            if motifs[0] is not 'G' and motifs[1] is not 'G' or motifs[0] is\
                    not 'D' and motifs[1] is not 'D':
                print("Erreur : ligne %d, caractères 0 et 1. Les 2 premiers"
                      " carracteres doivent etre différent pour un dépacement"
                      " non uniforme." % ligne)
                quit()

            # Si un des caractere est different de 'G' ou 'D'
            for mouv in range(len(motifs)):
                if motifs[mouv] != 'G' and motifs[mouv] is not 'D':
                    print("Erreur : Ecriture dans le fichier %s à la ligne %d"
                          " caractere %d.\nVeuillez n'entrez que 'G' ou 'D'."
                          % (fichier, ligne, mouv + 1))
                    quit()

            ligne += 1

    # Pas de verification par rapport à la taille car au delà de n + 1
    # la suite de mot n'est pas pris en compte car on lit de 0 à n + 1


# Affichage informations des fourmis
# -----------------------------------------------------------------------------
def __affiche_infos(fourmi, num):
    """ Affichage des informations des foourmis. """

    print('\nCOULEUR', fourmi[num][0], '=', fourmi[num][1],
          '\nMOTIFS =', fourmi[num][2],
          '\nDEPLACEMENT =', fourmi[num][5],
          '\nCOMPORTEMENTS =', fourmi[num][8])

    print('\n', 40 * '--')


# Affichage des motifs et des modifications
# -----------------------------------------------------------------------------
def __affiche_motif(fourmi):
    """ Procedure permettant l'affichage des motifs de chaque fourmi. """

    for num in range(len(fourmi)):
        FILL(BLANC, (ECRAN + 2, L_POS[num], STAT, POLICE))
        # Initialisation du premier mot
        BLIT(RENDER(fourmi[num][2][0], 1, NOIR), (ECRAN + 2, L_POS[num]))
        # Initialisation des autres mots
        for _ in range(1, len(fourmi[num][2])):
            BLIT(RENDER(fourmi[num][2][_], 1,
                        fourmi[num][8][fourmi[num][2][_] + str(_)]),
                 (ECRAN + (_ * POLICE) + 2, L_POS[num]))


# Direction d'une fourmi
# -----------------------------------------------------------------------------
def __orientation(depl):
    """ Cette fonction retourne l'orientation d'une fourmis en fonction du
    depLacement de la fourmis :
    0, vers l'est | 1, vers le sud | 2, vers l'ouest | 3, vers le nord. """

    if depl is 0:

        return 'Est'

    elif depl is 1:

        return 'Sud'

    elif depl is 2:

        return 'Ouest'

    elif depl is 3:

        return 'Nord'


# Comportemnt des fourmis en fonction des motifs
# -----------------------------------------------------------------------------
def __comportement(depl, comp):
    """ Fonction retournant une valeur de 'depl' en fontion de la valeur de
    'comp', comportement de la fourmi actuelle avec les autres fourmis. """

    if comp == 'D':
        if __orientation(depl) is 'Est':
            depl = 1

        elif __orientation(depl) is 'Sud':
            depl = 2

        elif __orientation(depl) is 'Ouest':
            depl = 3

        elif __orientation(depl) is 'Nord':
            depl = 0

    elif comp == 'G':
        if __orientation(depl) is 'Est':
            depl = 3

        elif __orientation(depl) is 'Sud':
            depl = 0

        elif __orientation(depl) is 'Ouest':
            depl = 1

        elif __orientation(depl) is 'Nord':
            depl = 2

    return depl


# Recupère les couleurs des fourmis
# -----------------------------------------------------------------------------
def __recup_coul(fourmi):
    """ Fonction récupérant les couleurs attribuees aux fourmis aleatoirement
    de la liste 'fourmi' et les retourne sous forme de liste. """

    coul_f = []
    for coul in fourmi:
        coul_f.append(coul[1])

    return coul_f


# Attribue une couleur au comportement
# -----------------------------------------------------------------------------
def __comportement_coul(fourmi, coul_f):
    """Analyse le comportement de chaque fourmi dans la liste 'fourmi' et
    attribue une couleur à chaque comportement grâce à 'Coul_F', liste
    contenant la couleur de chaue fourmi (recuperer au prealable
    avec la fonction '__recup_coul'. """

    comp_coul = [BLANC, fourmi[1]]
    for cmp in coul_f:
        if cmp != comp_coul[0] and cmp != comp_coul[1]:
            comp_coul.append(cmp)

    return comp_coul


# Affichage des fourmis aléatoirement
# -----------------------------------------------------------------------------
def __pos_fourmis(nbr_f, plcmt):
    """ Cette fonction attribue une case à une fourmis, dans une partie du
    tableau divisee en 'nbr_f' parties en fonction de 'PL', qui peut-etre :
    Aleatoire (en tapant : 'Al' ou 'al'),
    Centre (en tapant : 'C' ou 'c'),
    Uniformement aleatoire (en tapant : 'U_Al' ou 'U_al'),
    Uniformement centre (en tapant : 'U_C' ou 'U_c') ou
    Pyramidale(en tapant : 'PYR_Al', 'PYR_C', 'PYR_D' ou 'PYR_Q')"""

    pos = []
    p_append = pos.append
    # Placements normaux
    # -------------------------------------------------------------------------
    # Conditions pour le placement aleatoire
    if nbr_f is 1 and (plcmt is 'Al' or plcmt is 'al'):
        ordonnee, abcisse = randint(0, CASE_H - 1), randint(0, CASE_L - 1)
        p_append([abcisse, ordonnee])

    elif plcmt is 'Al' or plcmt is 'al':
        abcisse = CASE_L // nbr_f
        for num in range(nbr_f):
            ordonnee = randint(0, CASE_H - 1)
            p_append([randint(num * abcisse, (num + 1) * abcisse), ordonnee])

    # Conditions pour le placement centre
    elif nbr_f is 1 and (plcmt == 'C' or plcmt == 'c'):
        ordonnee, abcisse = CASE_H // 2, CASE_L // 2
        p_append([abcisse, ordonnee])

    elif plcmt is 'C' or plcmt == 'c':
        ordonnee, abcisse = CASE_H // 2, CASE_L // nbr_f
        for num in range(nbr_f):
            p_append([(num * abcisse) + (abcisse // 2), ordonnee])

    # Conditions pour le placement uniforme aleatoire
    elif plcmt is 'U_Al' or plcmt == 'u_al':
        ordonnee, abcisse = randint(0, CASE_H - 1), randint(0, CASE_L // nbr_f)
        for num in range(nbr_f):
            p_append([abcisse, ordonnee])

    # Conditions pour le placement uniforme centre
    elif plcmt is 'U_C' or plcmt == 'u_c':
        abcisse, ordonnee = CASE_L // 2, (CASE_H - 1) // 2
        for num in range(nbr_f):
            p_append([abcisse, ordonnee])

    # Placement ciculaire
    # -------------------------------------------------------------------------
    elif plcmt == "CL":
        c_x, c_y = CASE_L // 2, CASE_H // 2
        angle, rayon = 360 // nbr_f, (CASE_H // 3) - (DIM * 10)
        for num in range(nbr_f):
            f_x = trunc(c_x + (rayon * cos(radians(num * angle))))
            f_y = trunc(c_y + (rayon * sin(radians(num * angle))))
            p_append([f_x, f_y])

    # Placements pyramidales
    # -------------------------------------------------------------------------
    # Pyramidale aleatoire
    elif not(nbr_f % 2) and plcmt == 'PYR_Al':
        abcisse = (CASE_L - 1) // nbr_f * 2
        for num in range(nbr_f // 2):
            ordonnee = randint(0, CASE_H - 1)
            p_append([(num * abcisse) + trunc(abcisse / 2), ordonnee])
            p_append([1 + (num * abcisse) + trunc(abcisse / 2), ordonnee])

    # Pyramidale centre
    elif not(nbr_f % 2) and plcmt == 'PYR_C':
        ordonnee, abcisse = (CASE_H - 1) // 2, (CASE_L - 1) // nbr_f * 2
        for num in range(nbr_f // 2):
            p_append([(num * abcisse) + abcisse // 2, ordonnee])
            p_append([1 + (num * abcisse) + abcisse // 2, ordonnee])

    # Pyramidale circulaire
    elif plcmt is 'PYR_CL':
        c_x, c_y = CASE_L // 2, CASE_H // 2
        angle, rayon = 360 // nbr_f * 2, (CASE_H // 3) - (DIM * 10)
        for num in range(nbr_f // 2):
            f_x = trunc(c_x + (rayon * cos(radians(num * angle))))
            f_y = trunc(c_y + (rayon * sin(radians(num * angle))))
            posx1 = trunc(c_x + (rayon * cos(radians(num * angle)))) + 1
            posy1 = trunc(c_y + (rayon * sin(radians(num * angle))))
            p_append([f_x, f_y])
            p_append([posx1, posy1])

    # Pyramidale diagonale
    elif nbr_f % 2 is 0 and plcmt is 'PYR_D':
        ordonnee, abcisse = CASE_H // nbr_f * 2, (CASE_L - 1) // nbr_f * 2
        for num in range(nbr_f // 2):
            p_append([((num * abcisse) + (abcisse // 2)),
                      (num * ordonnee) + (ordonnee // 2)])
            p_append([(1 + (num * abcisse) + (abcisse // 2)),
                      (num * ordonnee) + (ordonnee // 2)])

    #  Pyramidale octale
    elif nbr_f is 8 and plcmt is 'PYR_Q':
        ordonnee, abcisse = CASE_H // 2, CASE_L // 2
        # Milieu haut
        p_append([abcisse + 1, ordonnee // 2])
        p_append([abcisse, ordonnee // 2])
        # Milieu gauche
        p_append([(abcisse // 2), ordonnee])
        p_append([(abcisse // 2) - 1, ordonnee])
        # Mileu bas
        p_append([abcisse, ordonnee + ordonnee // 2])
        p_append([abcisse - 1, ordonnee + ordonnee // 2])
        # Milieu droit
        p_append([(abcisse + abcisse // 2), ordonnee])
        p_append([(abcisse + abcisse // 2) - 1, ordonnee])

    elif not plcmt:

        return 0

    return pos


# Modifications des dictionnaire couleurs et comportements
# -----------------------------------------------------------------------------
def __modif_dic(fourmi, num, mot_a, mot_n):
    """ Procedure permettant la modification des 2 dictionnaires, de mots et de
    couleurs de la liste 'fourmi' et de la fourmi 'num' en fonction de
    l'ancien mot 'mot_a' et du nouveau mot 'mot_n'. """

    coul_tmp = fourmi[num][8][mot_a]
    del(fourmi[num][8][mot_a])
    fourmi[num][7][coul_tmp] = mot_n
    fourmi[num][8][mot_n] = coul_tmp


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Creation des motifs
# -----------------------------------------------------------------------------
def creation_motifs(nbr_f, fichier):
    """ Créele le fichier contenant les motifs de facon aleatoire. """

    mot = ['G', 'D']
    with open(fichier, 'w') as f_mot:
        for _ in range(nbr_f):
            motifs = []
            # Creation de la liste de motifs aleatoire
            for ind_mot in range(nbr_f + 1):
                motifs.append(choice(mot))

            motifs[1] = 'D' if motifs[0] is 'G' else 'G'
            # Ecriture de la liste des motifs dans le fichier
            for ind_mot in range(len(motifs)):
                f_mot.write(motifs[ind_mot])
                f_mot.write('\n')

    return fichier


# Création de fourmis
# -----------------------------------------------------------------------------
def creation_fourmis(fichier, nbr_f, plcmt, f_x=0, f_y=0):
    """Fonction créant 'nbr_f' fourmis, avec un placement 'plcmt' aleatoire ou
    centre et definit les comportements des fourmis à l'aide des motifs se
    trouvant dans le fichier 'fichier' et les associe à une couleur. """

    __verif_motifs(fichier, nbr_f)
    fourmi = []
    var_coul = __table_t(nbr_f)
    posf = __pos_fourmis(nbr_f, plcmt)
    f_append, c_remove = fourmi.append, var_coul.remove
    l_plcmt = ['PYR_C', 'PYR_Al', 'PYR_Q', 'PYR_D', 'PYR_P', 'PYR_CL']
    with open(fichier) as mot:         # Ajouter le comportement de la fourmi
        for num in range(nbr_f):
            # Condition pour la creation des fourmis non evenementiel
            if plcmt:
                f_append([f"F{num + 1}", choice(var_coul),
                         mot.readline()[0:nbr_f + 1], posf[num][0],
                          posf[num][1], randint(0, 3) if
                          (plcmt not in l_plcmt) else 2 - (num % 2), 0])
            # fourmi = [F'i' => nom de la fourmi | couleur |comportement |
            # pos x | pos y | valeur du deplacement | statistique]

            # Condition pour l'ajout manuel de 2 fourmis en mode pyramidale
            else:
                f_append([f"F{num + 1}", choice(var_coul),
                          mot.readline()[0:nbr_f + 1], f_x, f_y,
                          randint(0, 3) if plcmt != 'PYR' else 2 - num, 0])

            # Uniformisation des couleurs
            c_remove(fourmi[num][1])
            fourmi[num][2] = list(fourmi[num][2])

        # Dictionnaires stockant le comportement des fourmis selon des couleurs
        for num in range(nbr_f):
            dic1 = {}        # Dic1 - {Cle = couleurs : valeurs = comportement}
            dic2 = {}        # Dic2 - {Cle = comportement : valeurs = couleurs}
            for j in range(len(fourmi[num][2])):
                dic1[__comportement_coul(fourmi[num],
                                         __recup_coul(fourmi))[j]] =\
                    fourmi[num][2][j] + str(j)
                dic2[fourmi[num][2][j] + str(j)] =\
                    __comportement_coul(fourmi[num], __recup_coul(fourmi))[j]

            # Ajout du dictionnaire dans la liste des informations de la fourmi
            fourmi[num] = fourmi[num] + [dic1] + [dic2]
            # Affichage des informations concernant chaque fourmi
            if plcmt:
                __affiche_infos(fourmi, num)

    return fourmi


# Fonction ajoutant une fourmi sur le terrain
# -----------------------------------------------------------------------------
def ajout_fourmi(fourmi, f_x, f_y, modif=0, depl=None):
    """ Cette fonction ajoute une fourmi à la liste des fourmis, 'fourmi'.
    plcmt = Placement de la fourmi.
    f_x, f_y = Coordonnees de la fourmi.
    depl = Permet de modifie la valeur du deplacement lors de al creation."""

    fourmi.append(creation_fourmis('Mot.txt', len(fourmi) + 1, 0, f_x,
                                   f_y)[len(fourmi)])

    if modif:
        fourmi[len(fourmi) - 1][5] = depl

    with open('Mot.txt') as mot:
        for num in range(len(fourmi)):
            # Vidage des dictionnaires comportant le comportement des fourmis
            # en fonction des couleurs des fourmis
            fourmi[num][7].clear(), fourmi[num][8].clear()
            if len(fourmi[num][2]) == len(fourmi):
                # Rajout d'un motif pour les anciennes fourmis
                fourmi[num][2].append(mot.readline()[len(fourmi)])

            # Creation du nouveau dictionnaire de comportement
            for cmp in range(len(fourmi[num][2])):
                fourmi[num][7][__comportement_coul(fourmi[num],
                                                   __recup_coul(fourmi))[cmp]]\
                    = fourmi[num][2][cmp] + str(cmp)
                fourmi[num][8][fourmi[num][2][cmp] + str(cmp)] =\
                    __comportement_coul(fourmi[num], __recup_coul(fourmi))[cmp]

            __affiche_infos(fourmi, num)

    return fourmi


# Fonction supprimant une fourmi du terrain
# -----------------------------------------------------------------------------
def supp_fourmi(fourmi, coul):
    """ Fonction qui supprime une fourmi de la liste 'fourmi' à partir de sa
    couleur 'coul'. """

    num_f_tmp, rech_f = 0, 1
    remove = fourmi.remove
    while rech_f:
        # Suppression de la fourmi quand la couleur 'coul' est trouve
        if coul is fourmi[num_f_tmp][1]:
            remove(fourmi[num_f_tmp])
            rech_f = False

        else:
            num_f_tmp += 1

    for num in range(len(fourmi)):
        # Effacement des dictionnaires comportant le comportement des fourmis
        # en fonction des couleurs des fourmis
        fourmi[num][7].clear(), fourmi[num][8].clear()
        fourmi[num][2] = fourmi[num][2][0:len(fourmi) + 1]
        # Ceration du nouveau dictionnaire
        for cmp in range(len(fourmi[num][2])):
            fourmi[num][7][__comportement_coul(fourmi[num],
                                               __recup_coul(fourmi))[cmp]]\
                = fourmi[num][2][cmp] + str(cmp)
            fourmi[num][8][fourmi[num][2][cmp] + str(cmp)] =\
                __comportement_coul(fourmi[num], __recup_coul(fourmi))[cmp]

    # Suppression du chemin de la fourmi
    for dico in CASE:
        if CASE[dico] is coul:
            color_case(dico[0], dico[1], BLANC)
            display.flip()

    # Suppression des valeurs srtatistiques
    FILL(BLANC, (ECRAN + 2, POLICE * ESP * len(fourmi), STAT, POLICE * 2))

    return fourmi


# --------------------------------------------------------------------------- #
# -------|      DEPlaCEMENT DES fourmiS - FONCTION PRINCIPALE        |------- #
# --------------------------------------------------------------------------- #

def deplacement_fourmis(iter_total, fourmi, rep_s):
    """ Procedure permettant le deplacement des fourmis avec parametres:
    iter_total : Nombre d'iteration total.
    fourmi : Liste contenant la/les fourmi/s.
    rep_s : 'Y' ou 'N' pour afficher ou ne pas afficher les statistiques."""

    # Nombre et numero de fourmi, temps pause
    nbr_f, num, tps, init_fps, continuer = len(fourmi), 0, 0, time.Clock(), 1
    fps = init_fps.tick
    # Affichage du temps de pause
    affiche_pause(tps)
    # Affichage des motifs des fourmis
    __affiche_motif(fourmi)
    # Initialisation du nombre d'iteration
    iterations = range(iter_total)
    iter_fin = iterations[-1]
    for nbr_iter in iterations:
        display.flip()

        # ------------------------------------------------------------------- #
        # ------|   CAS OU IL N'Y A PLUS DE fourmiS SUR LE TERRAIN   |------- #
        # ------------------------------------------------------------------- #
        if not fourmi:
            continuer = input("Voulez-vous continuer? 'Y' ou 'N' : ")
            # Si on veut continuer, on entre les nouvelles coordonnees
            if continuer is 'Y' or continuer is 'y':
                nbr_f = int(input('Combien de fourmis voulez-vous ajouter sur'
                                  ' le terrain? : '))
                for num in range(nbr_f):
                    x_tmp, y_tmp = -1, -1
                    while not (0 <= x_tmp < CASE_L) and not\
                            (0 <= y_tmp < CASE_H):
                        # Erreur si l'abcisse non compris dans l'intervalle
                        if x_tmp > CASE_L:
                            print("Erreur, abcisse non compris dans"
                                  " l'intervalle, veuillez recommencer")

                        # Erreur si l'ordonnee non compris dans l'intervalle
                        elif y_tmp > CASE_H:
                            print("Erreur, ordonnee non compris dans"
                                  " l'intervalle, veuillez recommencer")

                        # Erreur si l'abcisse et l'ordonnee non compris dans
                        # l'intervalle
                        elif x_tmp > CASE_L - 1 and y_tmp > CASE_H - 1:
                            print("Erreur, abcisse et ordonnee non compris"
                                  " dans l'intervalle, veuillez recommencer")

                        # Affichage du numero de la fourmis
                        print('\n\t\t fourmi 0%d' % (1 + num))
                        # Entree des coordonnees (x, y) de la fourmi
                        print("Entrez l'abcisse de la fourmis", 1 + num,
                              ', compris entre [0, ',
                              CASE_L - 1, '] : x = ', end=' ')
                        x_tmp = int(input())
                        print("Entrez l'ordonee de la fourmis", 1 + num,
                              ', compris entre [0, ',
                              CASE_H - 1, '] : y = ', end=' ')
                        y_tmp = int(input())

                        # Creation de la nouvelle fourmi si les coordonnes sont
                        # correctes
                        if (0 <= x_tmp < CASE_L) and (0 <= y_tmp < CASE_H):
                            # Reponse en vue de la modication du deplacement
                            rep_depl = input("Voulez-vous modifier les"
                                             " déplacements? 'Y' ou 'N' : ")
                            if rep_depl is 'Y' or rep_depl is 'y':
                                # Initialisation de la valeur de depl a -1
                                mod_depl = -1
                                while not 0 <= mod_depl <= 3:
                                    # Valeur du nouveau deplacement
                                    mod_depl = int(input('Entrez la valeur du'
                                                         ' deplacement, entre'
                                                         ' 0 et  3 : '))
                                # Modifiacation des coordonnees, depalacement
                                fourmi = ajout_fourmi(fourmi, x_tmp, y_tmp, 1,
                                                      mod_depl)

                            # Le deplacement n'est pas modifie
                            elif rep_depl is 'N' or rep_depl is 'n':
                                print('DEPlaCEMENT ALEATOIRE')
                                fourmi = ajout_fourmi(fourmi, x_tmp, y_tmp)

            # Sinon le programme se termine
            elif continuer is 'N' or continuer is 'n':
                print('Vous venez de quitter le script')
                quit()

            __affiche_motif(fourmi)
            nbr_f = len(fourmi)

        # ------------------------------------------------------------------- #
        # ----|    VARIABLES RECUPERANT LES INFORMATIONS DE LA FOURMI   |---- #
        # ------------------------------------------------------------------- #
        f_x, f_y = fourmi[num][3], fourmi[num][4]
        depl, val_f = fourmi[num][5], fourmi[num][6]
        # depl va de 0 à 3, valeurs representant léplacement des fourmis:
        # 0 => f_x = f_x - 1 (à gauche) | 1 => f_y = f_y - 1 (en bas)
        # 2 => f_x = f_x + 1 (à droite) | 3 => f_y = f_y + 1 (en haut)
        # val_f = valeur satistique

        # ------------------------------------------------------------------- #
        # ---------|        DEPlaCEMENT AVEC LES OBSTACLES        |---------- #
        # ------------------------------------------------------------------- #
        # Deplacements inverses face aux obstacles
        if CASE[f_x, f_y] is VERT:
            if depl is 0:
                f_x += 1

            elif depl is 1:
                f_y += 1

            elif depl is 2:
                f_x -= 1

            elif depl is 3:
                f_y -= 1

            # Debordements
            # -----------------------------------------------------------------

            if f_x < 0 or f_y < 0 or f_x >= CASE_L or f_y >= CASE_H:
                # Si 'f_x' ou 'f_y' sont < 0 et < 1, ils prennent les valeurs
                # de lalongueur 'CASE_L - 1' et de la hauteur 'CASE_H - 1'
                if f_x < 0:
                    f_x = CASE_L - 1

                elif f_y < 0:
                    f_y = CASE_H - 1
                    # Redessine la ligne d'encadrement du terrain
                    FILL(NOIR, (ECRAN, 0, 1, HAUTEUR))

                # Si 'f_x' ou 'f_y' sont superieur a la longueur 'CASE_L' et
                # la hauteur 'CASE_H' ils prennent les valeurs 0 et 1
                elif f_x >= CASE_L:
                    f_x = 0

                elif f_y >= CASE_H:
                    f_y = 0

        # ------------------------------------------------------------------- #
        # ---------|        DEPlACEMENT SANS LES OBSTACLES        |---------- #
        # ------------------------------------------------------------------- #

        # Var_mot = Dic1['Couleur'] = mot
        var_mot = fourmi[num][7][CASE[(f_x, f_y)]]
        if CASE[(f_x, f_y)] is BLANC:
            color_case(f_x, f_y, fourmi[num][1])
            val_f += 1

        elif CASE[(f_x, f_y)] is fourmi[num][1]:
            color_case(f_x, f_y, BLANC)
            val_f -= 1

        elif CASE[(f_x, f_y)] is not BLANC and CASE[(f_x, f_y)] is not\
                fourmi[num][1]:
            for fmod in fourmi:
                if CASE[(f_x, f_y)] is fmod[1] and CASE[(f_x, f_y)] !=\
                        fourmi[num]:
                    # Modification des statistiques de la  fourmis concerne
                    fmod[6] -= 1

            color_case(f_x, f_y, BLANC)

        # Modification de la valeur de deplacement
        depl = __comportement(depl, var_mot[0])
        # Modification des coordonnees en fonction de depl
        # ---------------------------------------------------------------------
        if depl is 0:
            f_x -= 1

        elif depl is 1:
            f_y -= 1

        elif depl is 2:
            f_x += 1

        elif depl is 3:
            f_y += 1

        # Debordements sans les obstacles
        # ---------------------------------------------------------------------
        if f_x < 0 or f_y < 0 or f_x >= CASE_L or f_y >= CASE_H:
            if f_x < 0:
                f_x = CASE_L - 1

            elif f_y < 0:
                f_y = CASE_H - 1

            elif f_x >= CASE_L:
                f_x = 0
                FILL(NOIR, (ECRAN, 0, 1, HAUTEUR))

            elif f_y >= CASE_H:
                f_y = 0

        # ------------------------------------------------------------------- #
        # ---------|    AFFICHAGE DES INFORMATIONS DE LA FOURMI    |--------- #
        # ------------------------------------------------------------------- #
        # Affichage des stats
        stats(rep_s, num, f"F{num + 1}: {val_f}", fourmi[num][1], nbr_iter,
              iter_fin,
              __orientation(__comportement(depl, var_mot[0])), var_mot[0])

        # Les valeurs (f_x, f_y, depl, val) de chaques fourmis sont modifiees
        fourmi[num][3], fourmi[num][4] = f_x, f_y
        fourmi[num][5], fourmi[num][6] = depl, val_f

        # ------------------------------------------------------------------- #
        # --------------|       GESTION DES EVENEMENTS      |---------------- #
        # ------------------------------------------------------------------- #
        for evt in event.get():
            # Quitte le script en cliquant sur la croix de la FENETRE
            if evt.type is QUIT:
                continuer = 0
                break

            # --------------------------------------------------------------- #
            # ---------------|       GESTION DES MOTIFS       |-------------- #
            # --------------------------------------------------------------- #
            elif evt.type == MOUSEBUTTONUP and evt.button == 1 and\
                    (evt.pos[0] // DIM) >= CASE_L:
                xtmp, ytmp = 0, 0
                # Identification de l'intervalle pour la position de l'ordonnee
                while ytmp < len(fourmi[num][2]) - 1:
                    # Ordonnee de l'extremite gauche du mot <= position
                    # ordonnee <= Ordonnee de l'extremite droite du mot
                    if L_POS[ytmp] <= evt.pos[1] <= L_POS[ytmp + 1]:
                        # Ordonnee de l'extremite gauche du mot
                        posy1 = L_POS[ytmp]
                        # Stocke 'ytmp' representant le numero de la fourmi
                        fmod = ytmp
                        ytmp = len(fourmi[num][2])

                    else:
                        ytmp += 1
                        posy1, fmod = 0, -1

                while xtmp < len(fourmi[fmod][2]):
                    # Abcisse de l'extremite gauche du mot
                    posx1 = ECRAN + 2 + (xtmp * POLICE)
                    # Coordonnees de l'extremite droite du mot
                    posx2, posy2 = posx1 + POLICE, posy1 + POLICE
                    if (posx1 <= evt.pos[0] <= posx2)\
                            and (posy1 <= evt.pos[1] <= posy2) and fmod >= 0:
                        # Stockage de l'ancien Mot
                        anc = fourmi[fmod][2][xtmp]
                        # Modification de l'ancien mot
                        fourmi[fmod][2][xtmp] = 'D' if\
                            fourmi[fmod][2][xtmp] is 'G' else 'G'
                        # Application des modififs aux dico de mots et couleurs
                        __modif_dic(fourmi, fmod, anc + str(xtmp),
                                    fourmi[fmod][2][xtmp] + str(xtmp))
                        # Affichage de la modification
                        BLIT(RENDER(fourmi[fmod][2][xtmp],
                                    1, fourmi[fmod][8][fourmi[fmod][2][xtmp]
                                                       + str(xtmp)]), (posx1,
                                                                       posy1))

                        # Uniformisation des 2 premiers motifs
                        # -----------------------------------------------------
                        # Modification du premier motif
                        if xtmp is 0:
                            fourmi[fmod][2][1] = 'D' if fourmi[fmod][2][1]\
                                                        is 'G' else 'G'
                            __modif_dic(fourmi, fmod,
                                        'D1' if fourmi[fmod][2][0] is 'D' else
                                        'G1', 'G1' if fourmi[fmod][2][0] is 'D'
                                        else 'D1')
                            BLIT(RENDER(fourmi[fmod][2][0], 1, NOIR),
                                 (posx1, posy1))

                        # Modification du second motif
                        elif xtmp is 1:
                            fourmi[fmod][2][0] = 'D' if fourmi[fmod][2][0]\
                                                        is 'G' else 'G'
                            __modif_dic(fourmi, fmod,
                                        'D0' if fourmi[fmod][2][1] is 'D' else
                                        'G0', 'G0' if fourmi[fmod][2][1] is 'D'
                                        else 'D0')
                            BLIT(RENDER(fourmi[fmod][2][1],
                                        1, fourmi[fmod][8][fourmi[fmod][2][1]
                                                           + str(1)]), (posx1,
                                                                        posy1))

                        break
                    xtmp += 1
                __affiche_motif(fourmi)

            # ----------------------------------------------------------------#
            # ------------|    GESTION DU NOMBRE DE fourmiS    |--------------#
            # ----------------------------------------------------------------#
            elif evt.type == MOUSEBUTTONUP and (evt.pos[0] / DIM) < CASE_L:
                # Ajoute une fourmi en cliquant sur le clic gauche de la souris
                if evt.button is 1:
                    fourmi = ajout_fourmi(fourmi, (evt.pos[0] // DIM),
                                          (evt.pos[1] // DIM))

                # Ajoute un obstacle en cliquant sur la molette de la souris
                elif evt.button is 2 and\
                        CASE[(evt.pos[0] // DIM),
                             (evt.pos[1] // DIM)] is BLANC:
                    obstacles(0, (evt.pos[0] // DIM), (evt.pos[1] // DIM))

                # Ajoute 2 fourmis en cliquant sur le clic droit de la souris
                elif evt.button is 3:
                    fourmi = ajout_fourmi(fourmi, (evt.pos[0] // DIM),
                                          (evt.pos[1] // DIM), 1, 0)
                    fourmi = ajout_fourmi(fourmi, (evt.pos[0] // DIM),
                                          (evt.pos[1] // DIM), 1, 2)

                # Supprime une fourmi en poussant la molette vers l'avant
                elif evt.button is 4 and\
                        CASE[(evt.pos[0] // DIM), (evt.pos[1] // DIM)]\
                        is not BLANC and CASE[(evt.pos[0] // DIM),
                                          (evt.pos[1] // DIM)] is not VERT:

                    fourmi = supp_fourmi(fourmi, CASE[(evt.pos[0] // DIM),
                                                      (evt.pos[1] // DIM)])

                # Efface une case en poussant la molette vers le bas
                elif evt.button is 5:
                    color_case((evt.pos[0] // DIM), (evt.pos[1] // DIM), BLANC)

                __affiche_motif(fourmi)
                # Mise à jour du nombre de fourmis
                nbr_f = len(fourmi)

            # ----------------------------------------------------------------#
            # -------------|     GESTION DU TEMPS DE PAUSE     |--------------#
            # ----------------------------------------------------------------#
            elif evt.type == KEYDOWN:
                # Initialisation du temps a 0 seconde
                if evt.key == K_KP0:
                    tps = 0

                # Initialisation du temps a 1 seconde
                elif evt.key == K_KP1:
                    tps = 1

                # Division du temps de pause par 10
                elif evt.key == K_UP:
                    tps += 1
                # Division du temps de pause par 10
                elif evt.key == K_DOWN:
                    tps -= 1 if tps > 0 else 0

                affiche_pause(tps)
                
        if continuer == 0:
            break
        
        # Incremente de 1 s'il reste des fourmis sinon revient a 0
        num = (num + 1) % nbr_f if nbr_f != 0 else nbr_f
        # Affichage du temps
        fps(0)
        affiche_temps(time.get_ticks() // 1000, init_fps.get_fps())
        
        # Mise à jour de l'affichage
        time.delay(tps)

    quit()


# ----------------------------------------------------------------------------#
# ---------------------|          TEST UNITAIRE        |----------------------#
# ----------------------------------------------------------------------------#
if __name__ == '__main__':
    frm = sys.argv[1]      # Disopsitionn des fourmis [PYR_C, C,..]
    sts = sys.argv[2]      # Stats [Y, N]
    rep = sys.argv[3]      # "rep" ajout manuelle des fourmis [Y, N]
    nbf = int(sys.argv[4]) # Nombre de fourmis
    init_grille(1)         # Creation de la grille
    obstacles(0)           # Nombre d'obstacles

    deplacement_fourmis(100000001, creation_fourmis('Mot.txt', nbf, frm) if
    rep is 'N' else [], sts)
