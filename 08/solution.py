"""Advent of Code 2024, jour 8 : points alignés avec des paires d'antennes.

On regroupe les positions des antennes par fréquence dans un dictionnaire.
Pour chaque couple ordonné (a, b) d'antennes d'une même fréquence :
- partie 1 : l'antinœud est le symétrique de a par rapport à b, soit 2b - a ;
- partie 2 : on part de b et on avance par pas b - a tant qu'on reste dans la
  grille. Le pas n'est pas divisé par pgcd(dx, dy) : ce n'est correct que si
  ce pgcd vaut 1 (c'est le cas sur les entrées du site).
"""
from collections import defaultdict
from itertools import product


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [ligne.strip() for ligne in f if ligne.strip()]


def antennes_par_frequence(grille):
    antennes = defaultdict(list)
    for y, ligne in enumerate(grille):
        for x, c in enumerate(ligne):
            if c != '.':
                antennes[c].append((x, y))
    return antennes


def dans_grille(grille, x, y):
    return 0 <= x < len(grille[0]) and 0 <= y < len(grille)


def partie1(grille):
    antinoeuds = set()
    for positions in antennes_par_frequence(grille).values():
        for (x0, y0), (x, y) in product(positions, repeat=2):
            if (x, y) == (x0, y0):
                continue
            xa, ya = 2 * x - x0, 2 * y - y0
            if dans_grille(grille, xa, ya):
                antinoeuds.add((xa, ya))
    return len(antinoeuds)


def partie2(grille):
    antinoeuds = set()
    for positions in antennes_par_frequence(grille).values():
        for (x0, y0), (x, y) in product(positions, repeat=2):
            dx, dy = x - x0, y - y0
            if (dx, dy) == (0, 0):
                continue
            while dans_grille(grille, x, y):
                antinoeuds.add((x, y))
                x += dx
                y += dy
    return len(antinoeuds)


grille = lire_entree('input.txt')
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
