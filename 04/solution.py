"""Advent of Code 2024, jour 4 : mots cachés dans une grille.

Partie 1 : on énumère une case de départ et une direction (dx, dy) parmi les 8
directions, et on lit les 4 lettres si le mot tient dans la grille.
Partie 2 : on lit « MAS » sur les seules diagonales et on compte, pour chaque
case centrale (le A), les diagonales qui y passent ; un centre forme un X dès
qu'il en reçoit deux.
La grille est indexée par grille[y][x].
"""
from collections import defaultdict
from itertools import product

DIAGONALES = [(-1, 1), (1, -1), (1, 1), (-1, -1)]


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [ligne.strip() for ligne in f if ligne.strip()]


def lire_mot(grille, x0, y0, dx, dy, longueur):
    return ''.join(grille[y0 + i * dy][x0 + i * dx] for i in range(longueur))


def partie1(grille):
    largeur, hauteur = len(grille[0]), len(grille)
    total = 0
    for x0, y0, dx, dy in product(range(largeur), range(hauteur),
                                  range(-1, 2), range(-1, 2)):
        if (dx, dy) == (0, 0):
            continue
        if not (0 <= x0 + 3 * dx < largeur and 0 <= y0 + 3 * dy < hauteur):
            continue
        if lire_mot(grille, x0, y0, dx, dy, 4) == 'XMAS':
            total += 1
    return total


def partie2(grille):
    largeur, hauteur = len(grille[0]), len(grille)
    nb_mas = defaultdict(int)   # centre -> nombre de « MAS » qui y passent
    total = 0
    for x0, y0, (dx, dy) in product(range(largeur), range(hauteur),
                                    DIAGONALES):
        if not (0 <= x0 + 2 * dx < largeur and 0 <= y0 + 2 * dy < hauteur):
            continue
        if lire_mot(grille, x0, y0, dx, dy, 3) == 'MAS':
            centre = (x0 + dx, y0 + dy)
            nb_mas[centre] += 1
            # Deux diagonales au plus passent par un centre : on compte le
            # centre au moment où il reçoit la seconde.
            if nb_mas[centre] > 1:
                total += 1
    return total


grille = lire_entree('input.txt')
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
