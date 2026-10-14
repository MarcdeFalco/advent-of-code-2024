"""Advent of Code 2024, jour 16 : labyrinthe avec rotations.

Algorithme de Dijkstra sur les états (case, direction) : avancer coûte 1,
tourner puis avancer coûte 1001, le demi-tour est interdit.
Partie 1 : coût du premier élément sorti de la file sur l'arrivée.
Partie 2 : chaque élément de la file transporte son chemin ; on réunit les
cases des chemins arrivés avec le coût optimal. L'élagage ne coupe que les
chemins strictement moins bons, donc les ex aequo sont tous conservés.
"""
from heapq import heappush, heappop

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def lire_labyrinthe(lignes):
    """Grille (liste de listes, grille[y][x]), départ et arrivée."""
    grille = [list(ligne) for ligne in lignes]
    for y, ligne in enumerate(grille):
        for x, c in enumerate(ligne):
            if c == 'S':
                depart = (x, y)
                ligne[x] = '.'
            elif c == 'E':
                arrivee = (x, y)
                ligne[x] = '.'
    return grille, depart, arrivee


def resout(grille, depart, arrivee):
    """Renvoie le coût optimal et l'ensemble des cases des chemins optimaux."""
    a_visiter = []
    heappush(a_visiter, (0, depart, (1, 0), (depart,)))  # départ vers l'est
    meilleur_score = {}
    sur_chemin_optimal = set()
    optimal = None
    while a_visiter:
        score, (x, y), direction, chemin = heappop(a_visiter)
        if (x, y) == arrivee:
            if optimal is None:
                optimal = score
            if score == optimal:  # objectif atteint avec le score optimal
                sur_chemin_optimal.update(chemin)
        for dx, dy in DIRECTIONS:
            if direction == (-dx, -dy):
                continue  # pas de marche arrière
            if grille[y + dy][x + dx] == '.':
                cout = 1 if (dx, dy) == direction else 1001
                etat = (x + dx, y + dy, dx, dy)
                # si on a déjà atteint cette case avec la même orientation
                # et un meilleur score, ce chemin n'est pas optimal
                if (etat in meilleur_score
                        and meilleur_score[etat] < score + cout):
                    continue
                meilleur_score[etat] = score + cout
                heappush(a_visiter, (score + cout, (x + dx, y + dy), (dx, dy),
                                     chemin + ((x + dx, y + dy),)))
    return optimal, sur_chemin_optimal


if __name__ == '__main__':
    lignes = open('input.txt').read().strip().split('\n')
    optimal, cases = resout(*lire_labyrinthe(lignes))
    print(optimal)
    print(len(cases))
