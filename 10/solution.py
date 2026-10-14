"""Advent of Code 2024, jour 10 : chemins à pente constante.

Graphe implicite : une arête relie deux cases voisines dont la hauteur
augmente de 1.
Partie 1 : depuis chaque départ (hauteur 0), parcours en profondeur avec une
pile et un marquage : on compte les sommets de hauteur 9 accessibles.
Partie 2 : le même parcours sans marquage compte les chemins et non plus
les sommets. Il termine car le graphe est acyclique (la hauteur croît
strictement) et les chemins ont au plus 10 cases.
"""

VOISINS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [[int(c) for c in ligne.strip()]
                for ligne in f if ligne.strip()]


def successeurs(carte, x, y):
    for dx, dy in VOISINS:
        xv, yv = x + dx, y + dy
        if (0 <= xv < len(carte[0]) and 0 <= yv < len(carte)
                and carte[yv][xv] == carte[y][x] + 1):
            yield xv, yv


def departs(carte):
    return [(x, y) for y in range(len(carte)) for x in range(len(carte[0]))
            if carte[y][x] == 0]


def score(carte, depart, marquage):
    pile = [depart]
    vus = set()
    total = 0
    while pile:
        x, y = pile.pop()
        if marquage:
            if (x, y) in vus:
                continue
            vus.add((x, y))
        if carte[y][x] == 9:
            total += 1
            continue
        pile.extend(successeurs(carte, x, y))
    return total


def partie1(carte):
    return sum(score(carte, depart, marquage=True)
               for depart in departs(carte))


def partie2(carte):
    return sum(score(carte, depart, marquage=False)
               for depart in departs(carte))


carte = lire_entree('input.txt')
print('Partie 1 :', partie1(carte))
print('Partie 2 :', partie2(carte))
