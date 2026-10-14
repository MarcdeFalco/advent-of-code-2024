"""Advent of Code 2024, jour 20 : raccourcis sur un circuit.

Deux parcours en largeur, depuis le départ et depuis l'arrivée, donnent les
distances d_S et d_E de chaque case du circuit. Un raccourci de p1 à p2 coûte
la distance de Manhattan |p1 - p2| (au plus 2 en partie 1, 20 en partie 2), et
le trajet complet dure d_S(p1) + |p1 - p2| + d_E(p2). On énumère les paires
de cases, triées par distance, avec arrêt anticipé dès que le gain ne peut
plus atteindre le seuil de 100.
"""
from collections import deque

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
SEUIL = 100


def lire_circuit(lignes):
    """Ensemble des cases libres, départ et arrivée."""
    libres = set()
    for y, ligne in enumerate(lignes):
        for x, c in enumerate(ligne):
            if c != '#':
                libres.add((x, y))
            if c == 'S':
                depart = (x, y)
            elif c == 'E':
                arrivee = (x, y)
    return libres, depart, arrivee


def distances(libres, source):
    """Parcours en largeur : distance de source à chaque case accessible."""
    a_visiter = deque([(0, source)])
    vus = {}
    while a_visiter:
        t, (x, y) = a_visiter.popleft()
        if (x, y) in vus:
            continue
        vus[x, y] = t
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) in libres:
                a_visiter.append((t + 1, (x + dx, y + dy)))
    return vus


def distance_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def compte_raccourcis(libres, depart, arrivee, longueur_max, seuil=SEUIL):
    depuis_depart = distances(libres, depart)
    depuis_arrivee = distances(libres, arrivee)
    sans_raccourci = depuis_depart[arrivee]
    debuts = sorted(depuis_depart, key=lambda p: depuis_depart[p])
    fins = sorted(depuis_arrivee, key=lambda p: depuis_arrivee[p])
    nombre = 0
    for p1 in debuts:
        if sans_raccourci - depuis_depart[p1] < seuil:
            continue
        for p2 in fins:
            # même avec un raccourci gratuit, le gain serait trop faible,
            # et ce sera pire pour les p2 suivants (plus loin de l'arrivée)
            duree_min = depuis_depart[p1] + depuis_arrivee[p2]
            if sans_raccourci - duree_min < seuil:
                break
            d = distance_manhattan(p1, p2)
            if 1 < d <= longueur_max:
                duree = depuis_depart[p1] + d + depuis_arrivee[p2]
                if sans_raccourci - duree >= seuil:
                    nombre += 1
    return nombre


def partie1(circuit):
    return compte_raccourcis(*circuit, 2)


def partie2(circuit):
    return compte_raccourcis(*circuit, 20)


if __name__ == '__main__':
    circuit = lire_circuit(open('input.txt').read().strip().split('\n'))
    print(partie1(circuit))
    print(partie2(circuit))
