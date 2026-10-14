"""Advent of Code 2024, jour 7 : opérateurs pour atteindre une cible.

Les opérateurs sont évalués de gauche à droite. On explore tous les choix
d'opérateurs (3^(n-1) candidats en partie 2) avec une pile explicite d'états
(indice du prochain nombre, valeur partielle), sans élagage.
Partie 1 : somme et produit ; partie 2 : on ajoute la concaténation.
"""


def lire_entree(nom_fichier):
    equations = []
    with open(nom_fichier) as f:
        for ligne in f:
            if ligne.strip():
                cible, nombres = ligne.split(': ')
                equations.append((int(cible), list(map(int, nombres.split()))))
    return equations


def appliquer(operateur, a, b):
    if operateur == '+':
        return a + b
    if operateur == '*':
        return a * b
    return int(str(a) + str(b))    # concaténation '|'


def atteignable(cible, nombres, operateurs):
    pile = [(1, nombres[0])]
    trouve = False
    while pile:
        i, valeur = pile.pop()
        if i == len(nombres):
            if valeur == cible:
                trouve = True
            continue
        for operateur in operateurs:
            pile.append((i + 1, appliquer(operateur, valeur, nombres[i])))
    return trouve


def total_calibrage(equations, operateurs):
    return sum(cible for cible, nombres in equations
               if atteignable(cible, nombres, operateurs))


def partie1(equations):
    return total_calibrage(equations, '+*')


def partie2(equations):
    return total_calibrage(equations, '+*|')


equations = lire_entree('input.txt')
print('Partie 1 :', partie1(equations))
print('Partie 2 :', partie2(equations))
