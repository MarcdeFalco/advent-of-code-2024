"""Advent of Code 2024, jour 6 : marcheur qui tourne devant les obstacles.

Partie 1 : on simule la marche et on accumule les cases visitées dans un
ensemble.
Partie 2 : on pose un obstacle sur une case, on resimule et on détecte une
boucle dès qu'un état (position, direction) se répète (l'ensemble des états
est fini). Un obstacle utile est forcément sur le chemin de la partie 1 : on
ne teste que ces cases.
"""
from itertools import product

# Gauche, bas, droite, haut : tourner à droite (y vers le bas) revient à
# reculer d'un indice dans cette liste.
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [list(ligne.strip()) for ligne in f if ligne.strip()]


def depart(grille):
    for x, y in product(range(len(grille[0])), range(len(grille))):
        if grille[y][x] == '^':
            return x, y


def tourner_a_droite(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)]


def trajectoire(grille, position, direction):
    """Ensemble des cases visitées jusqu'à la sortie de la grille."""
    largeur, hauteur = len(grille[0]), len(grille)
    x, y = position
    vues = {(x, y)}
    while True:
        dx, dy = direction
        if not (0 <= x + dx < largeur and 0 <= y + dy < hauteur):
            return vues
        if grille[y + dy][x + dx] == '#':
            direction = tourner_a_droite(direction)
        else:
            x += dx
            y += dy
            vues.add((x, y))


def boucle(grille, position, direction):
    """Vrai si la marche repasse par un même état (position, direction)."""
    largeur, hauteur = len(grille[0]), len(grille)
    x, y = position
    etats = {(position, direction)}
    while True:
        dx, dy = direction
        if not (0 <= x + dx < largeur and 0 <= y + dy < hauteur):
            return False
        if grille[y + dy][x + dx] == '#':
            direction = tourner_a_droite(direction)
        else:
            x += dx
            y += dy
            if ((x, y), (dx, dy)) in etats:
                return True
            etats.add(((x, y), (dx, dy)))


def partie1(grille):
    return len(trajectoire(grille, depart(grille), (0, -1)))


def partie2(grille):
    position = depart(grille)
    nb_obstacles = 0
    for x0, y0 in trajectoire(grille, position, (0, -1)):
        if grille[y0][x0] == '.':
            grille[y0][x0] = '#'
            if boucle(grille, position, (0, -1)):
                nb_obstacles += 1
            grille[y0][x0] = '.'
    return nb_obstacles


grille = lire_entree('input.txt')
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
