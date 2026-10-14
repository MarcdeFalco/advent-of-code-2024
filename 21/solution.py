"""Advent of Code 2024, jour 21 : claviers imbriqués (partie 1 seulement).

Pour chaque clavier, on énumère tous les chemins élémentaires entre deux
touches et on garde les plus courts. Pour taper un code, on développe niveau
par niveau : chaque plus court chemin sur le clavier numérique est traduit en
toutes ses séquences possibles sur le clavier directionnel du premier robot,
puis chacune sur celui du second robot, et on garde la plus courte. Entre deux
touches du code, tous les bras sont revenus sur A, donc chaque touche se
traite indépendamment.
Partie 2 : pas de solution.
"""
from collections import defaultdict

NUMERIQUE = ['789', '456', '123', 'x0A']  # x : case vide
DIRECTIONNEL = ['x^A', '<v>']
MOUVEMENTS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}


def plus_courts_chemins(clavier):
    """chemins[c1, c2] : liste des plus courtes séquences de flèches (suivies
    de A) pour aller de la touche c1 à la touche c2."""
    def touche(x, y):
        if 0 <= y < len(clavier) and 0 <= x < len(clavier[y]):
            return clavier[y][x]
        return 'x'

    chemins = defaultdict(list)

    def explore(debut, x, y, fleches, vus):
        chemins[debut, touche(x, y)].append(fleches + 'A')
        for fleche, (dx, dy) in MOUVEMENTS.items():
            if touche(x + dx, y + dy) != 'x' and (x + dx, y + dy) not in vus:
                explore(debut, x + dx, y + dy, fleches + fleche,
                        vus | {(x + dx, y + dy)})

    for y, ligne in enumerate(clavier):
        for x, c in enumerate(ligne):
            if c != 'x':
                explore(c, x, y, '', {(x, y)})
    for cle, liste in chemins.items():
        longueur = min(len(p) for p in liste)
        chemins[cle] = [p for p in liste if len(p) == longueur]
    return chemins


chemins_numerique = plus_courts_chemins(NUMERIQUE)
chemins_directionnel = plus_courts_chemins(DIRECTIONNEL)


def traductions(sequence, depart='A'):
    """Toutes les séquences qui font taper sequence sur un clavier
    directionnel dont le bras part de depart."""
    if sequence == '':
        return ['']
    resultat = []
    for debut in chemins_directionnel[depart, sequence[0]]:
        for suite in traductions(sequence[1:], sequence[0]):
            resultat.append(debut + suite)
    return resultat


def sequence_minimale(code):
    precedente = 'A'
    sequence = ''
    for c in code:
        # premier robot : toutes les traductions des plus courts chemins
        candidats = []
        for chemin in chemins_numerique[precedente, c]:
            candidats += traductions(chemin)
        # second robot : on garde la plus courte traduction
        meilleure = min((s for candidat in candidats
                         for s in traductions(candidat)), key=len)
        sequence += meilleure
        precedente = c
    return sequence


def partie1(codes):
    return sum(len(sequence_minimale(code)) * int(code[:-1]) for code in codes)


if __name__ == '__main__':
    codes = open('input.txt').read().strip().split('\n')
    print(partie1(codes))
    print('partie 2 non résolue')
