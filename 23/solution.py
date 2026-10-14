"""Advent of Code 2024, jour 23 : plus grande clique.

Le graphe est stocké en listes d'adjacence. Retour sur trace :
explore(clique, i) essaie d'étendre la clique courante par chaque sommet
d'indice >= i adjacent à tous ses membres, ce qui énumère chaque clique une
seule fois (indices croissants). Les sommets sont triés par degré
décroissant.
Partie 2 : plus grande clique rencontrée.
Partie 1 : la même énumération
compte les cliques de taille 3 contenant un sommet dont le nom commence par t.
"""
from collections import defaultdict


def lire_graphe(lignes):
    graphe = defaultdict(list)
    for ligne in lignes:
        a, b = ligne.split('-')
        graphe[a].append(b)
        graphe[b].append(a)
    return graphe


def resout(graphe):
    sommets = sorted(graphe, key=lambda s: -len(graphe[s]))
    meilleure = ()
    triangles_t = 0

    def explore(clique, i):
        nonlocal meilleure, triangles_t
        if len(clique) > len(meilleure):
            meilleure = clique
        if len(clique) == 3 and any(s[0] == 't' for s in clique):
            triangles_t += 1
        for j in range(i, len(sommets)):
            x = sommets[j]
            if all(x in graphe[y] for y in clique):
                explore(clique + (x,), j + 1)

    explore((), 0)
    return triangles_t, ','.join(sorted(meilleure))


if __name__ == '__main__':
    graphe = lire_graphe(open('input.txt').read().strip().split('\n'))
    triangles_t, mot_de_passe = resout(graphe)
    print(triangles_t)
    print(mot_de_passe)
