"""Advent of Code 2024, jour 14 : robots sur un tore.

Chaque robot avance de sa vitesse à chaque seconde, modulo la taille de la
grille. Les robots sont rangés dans un dictionnaire position -> vitesses.
Partie 1 : après 100 secondes, produit des nombres de robots par quadrant.
Partie 2 : heuristique, l'image cherchée apparaît au premier instant où
aucune case ne porte deux robots (la configuration est périodique de période
101 * 103, donc la recherche termine).
"""
import re
from collections import defaultdict
from itertools import product

LARGEUR, HAUTEUR = 101, 103


def lire_robots(lignes):
    robots = defaultdict(list)
    for ligne in lignes:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', ligne))
        robots[px, py].append((vx, vy))
    return robots


def avance(robots, w=LARGEUR, h=HAUTEUR):
    """Positions une seconde plus tard."""
    nouveaux = defaultdict(list)
    for (x, y), vitesses in robots.items():
        for vx, vy in vitesses:
            nouveaux[(x + vx) % w, (y + vy) % h].append((vx, vy))
    return nouveaux


def partie1(robots, w=LARGEUR, h=HAUTEUR):
    for _ in range(100):
        robots = avance(robots, w, h)
    # les robots sur les médianes ne comptent pas
    gauche, droite = range(w // 2), range(w // 2 + 1, w)
    haut, bas = range(h // 2), range(h // 2 + 1, h)
    resultat = 1
    quadrants = [(gauche, haut), (gauche, bas), (droite, haut), (droite, bas)]
    for xs, ys in quadrants:
        resultat *= sum(len(robots.get((x, y), []))
                        for x, y in product(xs, ys))
    return resultat


def partie2(robots):
    secondes = 0
    while True:
        secondes += 1
        robots = avance(robots)
        if all(len(vitesses) <= 1 for vitesses in robots.values()):
            return secondes, robots


def dessine(robots):
    for y in range(HAUTEUR):
        print(''.join('#' if robots.get((x, y)) else '.'
                      for x in range(LARGEUR)))


if __name__ == '__main__':
    robots = lire_robots(open('input.txt').read().strip().split('\n'))
    print(partie1(robots))
    secondes, image = partie2(robots)
    dessine(image)
    print(secondes)
