"""Advent of Code 2024, jour 18 : grille qui se bouche.

Partie 1 : plus court chemin de (0, 0) à (70, 70) après la chute des 1024
premiers octets, par un parcours avec file de priorité (tous les pas
coûtent 1).
Partie 2 : on ajoute les obstacles un par un et on refait à chaque fois un
test d'accessibilité (parcours avec pile) depuis le départ ; le premier
obstacle qui rend l'arrivée inaccessible est la réponse.
"""
from heapq import heappush, heappop

DEPART = (0, 0)
ARRIVEE = (70, 70)
TOMBES = 1024
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def voisins(x, y):
    for dx, dy in DIRECTIONS:
        if 0 <= x + dx <= ARRIVEE[0] and 0 <= y + dy <= ARRIVEE[1]:
            yield x + dx, y + dy


def partie1(octets):
    obstacles = set(octets[:TOMBES])
    a_visiter = [(0, DEPART)]
    vus = set()
    while a_visiter:
        pas, (x, y) = heappop(a_visiter)
        if (x, y) == ARRIVEE:
            return pas
        if (pas, x, y) in vus:
            continue
        vus.add((pas, x, y))
        for voisin in voisins(x, y):
            if voisin not in obstacles:
                heappush(a_visiter, (pas + 1, voisin))


def arrivee_accessible(obstacles):
    a_visiter = [DEPART]
    composante = set()
    while a_visiter:
        case = a_visiter.pop()
        if case in composante:
            continue
        composante.add(case)
        for voisin in voisins(*case):
            if voisin not in obstacles:
                a_visiter.append(voisin)
    return ARRIVEE in composante


def partie2(octets):
    obstacles = set()
    for x, y in octets:
        obstacles.add((x, y))
        if not arrivee_accessible(obstacles):
            return f'{x},{y}'


if __name__ == '__main__':
    lignes = open('input.txt').read().strip().split('\n')
    octets = [tuple(map(int, ligne.split(','))) for ligne in lignes]
    print(partie1(octets))
    print(partie2(octets))
